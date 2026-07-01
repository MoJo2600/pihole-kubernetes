#!/usr/bin/env python3
"""Migrate a pihole-kubernetes values file from the old (2.x) chart to the new (3.0.0) chart.

Handles the mechanical breaking changes:
  * adminPassword            -> admin.password
  * whitelist                -> allowed
  * blacklist                -> denied

For the DoH rewrite (cloudflared -> dnscrypt-proxy) it cannot safely translate
configuration automatically, so it strips the now-obsolete keys and prints a
warning telling you what to review by hand.

Usage:
    python3 migrate-values.py old-values.yaml            # writes to stdout
    python3 migrate-values.py old-values.yaml -o new.yaml

Comments are not preserved (PyYAML limitation). Review the output before use.
"""
import argparse
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")


def migrate(data):
    warnings = []
    changes = []

    # --- simple top-level renames ---
    if "adminPassword" in data:
        admin = data.setdefault("admin", {})
        if not isinstance(admin, dict):
            admin = data["admin"] = {}
        admin.setdefault("password", data.pop("adminPassword"))
        changes.append("adminPassword -> admin.password")

    for old, new in (("whitelist", "allowed"), ("blacklist", "denied")):
        if old in data:
            data[new] = data.pop(old)
            changes.append(f"{old} -> {new}")

    # --- DoH: cloudflared -> dnscrypt-proxy ---
    doh = data.get("doh")
    if isinstance(doh, dict):
        enabled = bool(doh.get("enabled"))

        # Drop the old cloudflared image so the new dnscrypt-proxy default applies.
        repo = str(doh.get("repository", ""))
        if "cloudflared" in repo:
            doh.pop("repository", None)
            doh.pop("tag", None)
            doh.pop("name", None)
            changes.append("removed old cloudflared image (doh.repository/tag/name)")

        # Old per-probe 'probe:' blocks used cloudflared-specific nslookup commands.
        probes = doh.get("probes")
        if isinstance(probes, dict):
            for pname in ("liveness", "readiness"):
                p = probes.get(pname)
                if isinstance(p, dict) and "probe" in p:
                    p.pop("probe", None)
                    changes.append(f"removed doh.probes.{pname}.probe (uses new default)")

        # doh.monitoring was replaced by doh.metrics.
        if "monitoring" in doh:
            doh.pop("monitoring", None)
            changes.append("removed doh.monitoring (replaced by doh.metrics)")

        if enabled:
            warnings.append(
                "DoH is enabled: the sidecar changed from cloudflared to dnscrypt-proxy.\n"
                "      Review 'doh.config' (dnscrypt-proxy TOML) and, if you used\n"
                "      'doh.envVars.TUNNEL_DNS_UPSTREAM', move that intent into 'doh.config'.\n"
                "      To expose metrics, enable [monitoring_ui] in doh.config and set doh.metrics.enabled=true."
            )
        if isinstance(doh.get("envVars"), dict) and "TUNNEL_DNS_UPSTREAM" in doh["envVars"]:
            warnings.append(
                "doh.envVars.TUNNEL_DNS_UPSTREAM is not used by dnscrypt-proxy; "
                "configure upstreams in doh.config instead."
            )

    # --- very old service keys (removed back in 1.8.22) ---
    for legacy in ("serviceTCP", "serviceUDP"):
        if legacy in data:
            data.pop(legacy)
            warnings.append(
                f"'{legacy}' was removed long ago and was dropped; "
                "configure serviceWeb / serviceDns / serviceDhcp instead."
            )

    return changes, warnings


def main():
    ap = argparse.ArgumentParser(description="Migrate old pihole values.yaml to the new chart.")
    ap.add_argument("input", help="path to the old values file")
    ap.add_argument("-o", "--output", help="output file (default: stdout)")
    args = ap.parse_args()

    with open(args.input) as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        sys.exit("Input does not look like a values file (expected a YAML mapping).")

    changes, warnings = migrate(data)

    out = yaml.safe_dump(data, sort_keys=False, default_flow_style=False)
    if args.output:
        with open(args.output, "w") as f:
            f.write(out)
    else:
        sys.stdout.write(out)

    def note(msg):
        print(msg, file=sys.stderr)

    note("")
    note("=== pihole values migration ===")
    if changes:
        note("Applied:")
        for c in changes:
            note(f"  - {c}")
    else:
        note("No key renames were necessary.")
    if warnings:
        note("Review manually:")
        for w in warnings:
            note(f"  ! {w}")
    note("IMPORTANT: The 3.0.0 selector labels changed and are immutable.")
    note("  You must 'helm uninstall' and reinstall (in-place upgrade will fail).")
    note("")


if __name__ == "__main__":
    main()
