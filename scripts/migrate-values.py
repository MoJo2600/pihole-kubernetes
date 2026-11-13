#!/usr/bin/env python3
"""Migrate a pihole-kubernetes values file from the old (2.x) chart to the new (3.0.0) chart.

Handles the mechanical breaking changes:
  * adminPassword            -> admin.password
  * whitelist                -> allowed
  * blacklist                -> denied

For the DoH rewrite (cloudflared -> dnscrypt-proxy) it cannot safely translate
configuration automatically, so it strips the now-obsolete keys and prints a
warning telling you what to review by hand. It also warns about defaults that
changed in 3.0.0 when your values relied on them (service types, admin password,
DHCP service, dual-stack services).

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

    # header line of 'helm get values' without '-o yaml'
    if "USER-SUPPLIED VALUES" in data:
        data.pop("USER-SUPPLIED VALUES")
        changes.append("removed the 'USER-SUPPLIED VALUES' header line")

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

    pvc = data.get("persistentVolumeClaim")
    if isinstance(pvc, dict) and isinstance(pvc.get("annotations"), dict) \
            and pvc["annotations"].get("helm.sh/resource-policy") == "keep":
        pvc["annotations"].pop("helm.sh/resource-policy")
        if not pvc["annotations"]:
            pvc.pop("annotations")
        pvc["keep"] = True
        changes.append("persistentVolumeClaim.annotations helm.sh/resource-policy=keep -> persistentVolumeClaim.keep")

    # --- defaults that changed in 3.0.0 (only relevant when the old values relied on them) ---
    env = data.get("extraEnvVars")
    if isinstance(env, dict) and str(env.get("FTLCONF_dns_listeningMode", "")).lower() == "all":
        env.pop("FTLCONF_dns_listeningMode")
        changes.append("removed extraEnvVars.FTLCONF_dns_listeningMode=all (the chart sets it now)")

    # The NTP client is off now; if SYS_TIME was granted, it ran before, so keep it on
    sec = data.get("containerSecurityContext") or {}
    caps = (sec.get("capabilities") if sec else data.get("capabilities")) or {}
    ntp = data.get("ntp") if isinstance(data.get("ntp"), dict) else {}
    ftl = data.get("ftl") if isinstance(data.get("ftl"), dict) else {}
    if isinstance(caps, dict) and "SYS_TIME" in (caps.get("add") or []) and "sync" not in ntp \
            and "ntp_sync_active" not in ftl \
            and not (isinstance(env, dict) and "FTLCONF_ntp_sync_active" in env):
        data["ntp"] = {**ntp, "sync": True}
        changes.append("ntp.sync=true (SYS_TIME is granted, so Pi-hole's NTP client ran before; it is off by default now)")

    admin = data.get("admin") if isinstance(data.get("admin"), dict) else {}
    if admin.get("enabled", True) and not admin.get("password") and not admin.get("existingSecret"):
        warnings.append(
            "No admin password set: the old default was 'admin', 3.0 generates a random one\n"
            "      (kubectl get secret <release>-password -o jsonpath='{.data.password}' | base64 -d)."
        )

    dns = data.get("serviceDns") if isinstance(data.get("serviceDns"), dict) else {}
    if "type" not in dns:
        warnings.append(
            "serviceDns.type is not set: the default changed from NodePort to ClusterIP.\n"
            "      Set 'serviceDns.type: LoadBalancer' (or NodePort) to serve DNS outside the cluster."
        )
    if "mixedService" not in dns:
        warnings.append(
            "serviceDns.mixedService defaults to true now: one '<release>-dns' Service instead of\n"
            "      '-dns-tcp' and '-dns-udp'. Set it to false to keep the separate Services."
        )

    dhcp = data.get("serviceDhcp") if isinstance(data.get("serviceDhcp"), dict) else {}
    if "enabled" not in dhcp:
        warnings.append(
            "serviceDhcp.enabled defaults to false now. Set it to true only if you use a DHCP relay."
        )

    stack = data.get("dualStack") if isinstance(data.get("dualStack"), dict) else {}
    if stack.get("enabled") and "splitLoadBalancer" not in stack:
        uses_v6_ip = [
            name for name in ("serviceDns", "serviceWeb", "serviceDhcp")
            if isinstance(data.get(name), dict) and data[name].get("loadBalancerIPv6")
        ]
        if uses_v6_ip:
            stack["splitLoadBalancer"] = True
            changes.append(
                "dualStack.splitLoadBalancer=true (keeps the separate -ipv6 services for loadBalancerIPv6 in "
                + ", ".join(uses_v6_ip) + ")"
            )
        else:
            warnings.append(
                "dualStack: LoadBalancer services are now one dual-stack Service each instead of an extra\n"
                "      '-ipv6' Service. List both addresses in the load balancer annotation, or set\n"
                "      'dualStack.splitLoadBalancer: true' to keep the separate Services."
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
    note("  With persistentVolumeClaim.enabled, keep your data on uninstall first (Helm reads the")
    note("  policy from the release, so 'kubectl annotate' is not enough):")
    note("    helm upgrade <release> mojo2600/pihole -n <namespace> --version <your 2.x version> --reuse-values \\")
    note("      --set-string 'persistentVolumeClaim.annotations.helm\\.sh/resource-policy=keep'")
    note("")


if __name__ == "__main__":
    main()
