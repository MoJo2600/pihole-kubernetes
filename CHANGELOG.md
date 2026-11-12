# Release Notes

This release brings significant improvements to the Pi-hole Helm chart, including modernized Kubernetes standards and enhanced secure DNS capabilities.

## Breaking Changes

### Standardized Kubernetes Labels
- **Selector labels have changed** from `app`/`release` to `app.kubernetes.io/name` and `app.kubernetes.io/instance`
- **Migration required**: Existing deployments must be fully uninstalled and reinstalled due to immutable selector fields
- All resources now use standardized labels following Helm best practices:
  - `helm.sh/chart`
  - `app.kubernetes.io/name`
  - `app.kubernetes.io/instance`
  - `app.kubernetes.io/version`
  - `app.kubernetes.io/managed-by`

### Admin Password Configuration moved
- **`adminPassword` moved to `admin.password`** - The root-level `adminPassword` value has been moved into the `admin` section
- Update your values files: change `adminPassword: "xxx"` to `admin.password: "xxx"`

### DNS-over-HTTPS (DoH) Overhaul
- **Replaced cloudflared with dnscrypt-proxy** for encrypted DNS resolution
- Cloudflare deprecated the proxy-dns feature in cloudflared
- More flexible and feature-rich encrypted DNS solution

### Use same terminology as pihole
- renamed `whitelist` to `allowed` and `blacklist` to `denied` for inclusive terminology
- Update your values files:
  - `whitelist: [...]` → `allowed: [...]`
  - `blacklist: [...]` → `denied: [...]`

### Web domain and probes follow Pi-hole v6
- **`virtualHost` now sets Pi-hole's web domain** (`FTLCONF_webserver_domain`) and is added to the ingress hosts. The old `VIRTUAL_HOST` variable was a Pi-hole v5 setting that v6 ignores. Since Pi-hole FTL v6.8, `/` on any other host name returns 404 (only `/admin/` still works), so set `virtualHost` to the host name you use for the web interface. Set it to `""` to opt out.
- **Health probes no longer depend on upstream DNS.** The default probes check Pi-hole itself (API plus a local `pi.hole` lookup) instead of resolving `cloudflare.com`, so an internet outage no longer restarts Pi-hole. Each step has its own timeout, so a hung Pi-hole is now reliably restarted. The dnscrypt-proxy sidecar's liveness probe is a TCP check.
- **Pi-hole now also serves the web interface via HTTPS** on `webHttps` (default 443, with Pi-hole's self-signed certificate) and listens on IPv6 as well. Previously the chart limited Pi-hole to plain HTTP. Set `webHttps: ""` to turn HTTPS off, or `redirectToHttps: true` to redirect HTTP to HTTPS (not compatible with `monitoring.sidecar`).
- **`doh.metrics.enabled` no longer creates a PodMonitor by itself.** It only exposes the dnscrypt-proxy metrics port. A PodMonitor (which needs the Prometheus Operator CRDs) is created only with `monitoring.podMonitor.enabled: true`, and then also scrapes dnscrypt-proxy. Previously, enabling DoH metrics on a cluster without the Prometheus Operator made the install fail.

### Pi-hole image changes to be aware of
- Since FTL v6.8, files that are symlinks in `/etc/pihole` and `/var/log/pihole` are no longer handed over to the `pihole` user. Mount ConfigMaps/Secrets there with `subPath` (as the chart does).
- FTL v6.9 changed `webserver.acl`: IPv4 entries now match IPv4 clients everywhere, and IPv6 entries such as `[::]/0` no longer admit IPv4 clients.
- FTL v6.9 changed regex filters: `{,n}` now means `{0,n}`.
- `adlists`, `allowed`, `denied` and `regex` are only imported when the gravity database is first created. With a persistent volume, later changes to these values have no effect.

## Features

- add commonLabels option to apply labels to all deployed objects ([#347](https://github.com/MoJo2600/pihole-kubernetes/issues/347))

### Enhanced Health Probes
- **Added startup probes** for both Pi-hole and DoH containers
- Startup probes allow containers sufficient time to initialize before liveness/readiness probes begin
- Reduced `initialDelaySeconds` to 0 (startup probe handles the delay)
- Probe commands check the Pi-hole API and a local `pi.hole` lookup with `dig`, without depending on upstream DNS
- Leads to faster pod startups (estimated around 80% or higher)

**Why this matters:**
- **No arbitrary wait times** - Previously, `initialDelaySeconds` had to be set to an estimated value. If the container was ready faster, you waited unnecessarily. If slower, health checks failed.
- **Adaptive initialization** - Startup probes actively check if the container is ready. Once successful, liveness/readiness probes take over immediately.
- **Accurate health detection** - The `dig` command verifies actual DNS functionality rather than just open TCP ports. An open port doesn't mean DNS is working.
- **Faster failure detection** - With `failureThreshold: 3`, unhealthy pods are detected and restarted more quickly.

### ServiceAccount Support
- Added configurable ServiceAccount with optional token mounting
- Better security controls for pod identity management

**Why this matters:**
- **Principle of Least Privilege** - Pods can run with a dedicated ServiceAccount instead of the default account, which often has excessive permissions.
- **Controllable token mounting** - `automountServiceAccountToken: false` prevents unnecessary API credentials from being mounted into the pod (security risk if compromised).
- **RBAC integration** - Enables fine-grained permissions if Pi-hole needs Kubernetes API access (e.g., for service discovery).
- **Audit compliance** - Dedicated ServiceAccounts enable better tracking of API access in audit logs.

### Security Context Support (Experimental)
- Added `podSecurityContext` and `containerSecurityContext` configuration options
- Backwards compatible with existing `privileged` and `capabilities` values
- Documented Pi-hole limitations regarding rootless operation

**Why this matters:**
- **Explicit security configuration** - Allows setting `privileged: false` to prevent full host access.
- **Seccomp profiles** - Pod-level `seccompProfile: RuntimeDefault` enables syscall filtering.
- **Transparency** - Documentation explains why detailed capability management provides limited benefit for Pi-hole (requires 10+ capabilities including NET_ADMIN, NET_RAW, SETUID, etc.).

**Important limitations:**
- Pi-hole Docker image requires root at startup for gravity database, crontab, and setcap operations
- `runAsNonRoot`, `runAsUser`, `runAsGroup` are **not supported**
- `allowPrivilegeEscalation: false` is **not supported** (required for setcap)
- `readOnlyRootFilesystem: true` is **not supported** (Pi-hole writes to /etc/pihole, /var/log)

### Dynamic NOTES.txt
- Installation notes now dynamically reflect actual service configuration
- Context-aware access instructions based on service type (Ingress, LoadBalancer, NodePort, ClusterIP)
- Conditional DHCP section and improved kubectl commands with namespace flags

### Helm Chart Modernization
- Upgraded Helm chart to apiVersion v2
- Optimized `.helmignore` to reduce packaged chart size

## Improvements

### DNS Testing
- Extended Helm tests with DNS resolution verification
- New `test-pihole-dns.yaml` validates Pi-hole DNS functionality via nslookup queries

### Documentation
- Added `loadBalancerIP` deprecation notice for Kubernetes 1.24+
- Documented recommended migration path using cloud provider annotations (e.g., `metallb.universe.tf/loadBalancerIPs` for MetalLB)

## Migration Guide

Due to the breaking change in selector labels, you must perform a full reinstall:

```bash
# 1. Backup your Pi-hole configuration (if using persistent storage)
kubectl cp <namespace>/<pihole-pod>:/etc/pihole ./pihole-backup

# 2. Backup your helm custom values
helm get values pihole -n <namespace> > pihole-values-backup.yaml

# 3. Uninstall existing release
helm uninstall pihole -n <namespace>

# 4. Delete the PersistentVolumeClaim if you want a fresh start (optional)
kubectl delete pvc <release-name>-pihole -n <namespace>

# 5. Install new version
helm install <release-name> mojo2600/pihole -n <namespace> -f pihole-values-backup.yaml
```
