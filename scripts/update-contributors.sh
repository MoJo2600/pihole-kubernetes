#!/usr/bin/env bash
# Adds everyone who contributed to a merged pull request but is not yet listed in
# .all-contributorsrc, then regenerates the contributor tables in the READMEs.
#
# Contributors are
#   - the authors of merged pull requests (bots excluded), and
#   - GitHub users named in "Co-authored-by: ... <id+login@users.noreply.github.com>"
#     trailers on the default branch (squash merges keep these).
#
# Contribution types come from the conventional-commit type of the author's PR titles
# (docs -> doc, test -> test, ci/build -> infra, chore/deps -> maintenance, else code).
# People already listed are left alone, so manual edits in .all-contributorsrc stay.
#
# Needs: gh (GH_TOKEN), jq, git with full history, `npm ci` for all-contributors-cli
# (it reads PRIVATE_TOKEN to look up names and avatars).
# Run from the repository root:  scripts/update-contributors.sh [--dry-run]
set -euo pipefail

dry_run=false
[[ "${1:-}" == "--dry-run" ]] && dry_run=true

rc=.all-contributorsrc
ref="${CONTRIBUTORS_REF:-HEAD}"
is_bot='(\[bot\]$|^(dependabot|renovate|github-actions|release-please)$)'

known=$(jq -r '.contributors[].login | ascii_downcase' "$rc")

# login<TAB>pr title, one line per merged PR by a human
prs=$(gh pr list --state merged --limit 5000 --json author,title \
  --jq '.[] | select(.author.is_bot | not) | "\(.author.login)\t\(.title)"')

coauthors=$(git log "$ref" --format='%(trailers:key=Co-authored-by,valueonly)' |
  sed -nE 's/.*<([0-9]+\+)?([^@>]+)@users\.noreply\.github\.com>.*/\2/Ip' | sort -fu)

type_of() {
  case "$(sed -nE 's/^([a-zA-Z]+)(\(.*\))?!?:.*/\1/p' <<<"$1" | tr '[:upper:]' '[:lower:]')" in
    docs) echo doc ;;
    test) echo test ;;
    ci | build) echo infra ;;
    chore | deps) echo maintenance ;;
    *) echo code ;;
  esac
}

declare -A types=()
while IFS=$'\t' read -r login title; do
  [[ -z "$login" ]] && continue
  types[$login]+="$(type_of "$title"),"
done <<<"$prs"
while read -r login; do
  [[ -z "$login" ]] && continue
  # a co-author who also opened PRs keeps those types; otherwise credit code
  match=$(printf '%s\n' "${!types[@]}" | grep -ixF -- "$login" || true)
  [[ -z "$match" ]] && types[$login]+="code,"
done <<<"$coauthors"

added=0
for login in $(printf '%s\n' "${!types[@]}" | sort -f); do
  lower=${login,,}
  grep -qxF -- "$lower" <<<"$known" && continue
  [[ "$lower" =~ $is_bot ]] && continue
  contributions=$(tr ',' '\n' <<<"${types[$login]}" | sed '/^$/d' | sort -u | paste -sd, -)
  echo "add $login ($contributions)"
  if ! $dry_run; then
    npx --no-install all-contributors add "$login" "$contributions"
  fi
  added=$((added + 1))
done

if ! $dry_run && ((added > 0)); then
  # refresh the badge count and tables in every file listed in .all-contributorsrc
  npx --no-install all-contributors generate
fi
echo "$added new contributor(s)"
