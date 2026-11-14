# pihole

Installs pihole in kubernetes

![Version: 3.0.0-rc.3](https://img.shields.io/badge/Version-3.0.0--rc.3-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 2026.11.0](https://img.shields.io/badge/AppVersion-2026.11.0-informational?style=flat-square) <!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-94-blue.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## Source Code

* <https://github.com/MoJo2600/pihole-kubernetes/tree/main/charts/pihole>
* <https://pi-hole.net/>
* <https://github.com/pi-hole>
* <https://github.com/pi-hole/docker-pi-hole>

## Requirements

Kubernetes: `>=1.26.0-0`

## Introduction

[Pi-hole®](https://pi-hole.net/) is a network-wide ad blocker that acts as a DNS sinkhole. This chart deploys Pi-hole (v6) on Kubernetes as a `Deployment`, with separate services for the web interface, DNS (TCP/UDP) and optional DHCP, plus optional encrypted upstream DNS, persistence, Prometheus monitoring and network policies.

> **Note:** Pi-hole v6 is configured through `FTLCONF_*` environment variables, which you pass via [`extraEnvVars`](#values). See the [Pi-hole v6 configuration docs](https://docs.pi-hole.net/docker/configuration/) for the full list of settings.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
  - [Exposing Pi-hole](#exposing-pi-hole)
    - [Making DNS reachable on port 53](#making-dns-reachable-on-port-53-start-here)
  - [Example values.yaml](#example-valuesyaml)
  - [Admin password](#admin-password)
  - [Upstream DNS resolvers](#upstream-dns-resolvers)
  - [Local DNS records](#local-dns-records)
  - [Encrypted upstream DNS (DoH / DoT / DNSCrypt)](#encrypted-upstream-dns-doh--dot--dnscrypt)
  - [Persistence](#persistence)
  - [NetworkPolicy](#networkpolicy)
  - [ServiceAccount](#serviceaccount)
  - [Security context (experimental)](#security-context-experimental)
  - [Health probes](#health-probes)
  - [Upgrades without downtime](#upgrades-without-downtime)
  - [High availability](#high-availability)
- [Troubleshooting](#troubleshooting)
  - [Pi-hole does not start with hostNetwork](#pi-hole-does-not-start-with-hostnetwork)
  - [DHCP](#dhcp)
  - [Admin password from existingSecret is rejected](#admin-password-from-existingsecret-is-rejected)
  - [Query log shows the same client for every query](#query-log-shows-the-same-client-for-every-query)
- [Upgrading](#upgrading)
- [Uninstallation](#uninstallation)
- [Values](#values)

## Prerequisites

- Kubernetes 1.26+
- Helm 3+
- A default `StorageClass` if you enable persistence (`persistentVolumeClaim.enabled`)
- A `LoadBalancer` provider such as [MetalLB](https://metallb.universe.tf/) if you want to expose DNS/web on a routable IP

## Quick Start

```shell
helm repo add mojo2600 https://mojo2600.github.io/pihole-kubernetes/
helm repo update

helm install pihole mojo2600/pihole \
  --namespace pihole --create-namespace \
  --set admin.password=change-me
```

Open the web interface via port-forward:

```shell
kubectl port-forward svc/pihole-web -n pihole 8080:80
# then visit http://localhost:8080/admin
```

Point a client's DNS at the Pi-hole DNS service and you're blocking ads. For a real deployment, expose DNS with a `LoadBalancer` and enable [persistence](#persistence).

## Installation

### Add Helm repository

```shell
helm repo add mojo2600 https://mojo2600.github.io/pihole-kubernetes/
helm repo update
```

### Install the chart

Install with your own values file:

```shell
helm install pihole mojo2600/pihole \
  --namespace pihole --create-namespace \
  --values my-values.yaml
```

Jeff Geerling also made a video walking through the installation of this chart:

[![Jeff Geerling on YouTube](https://img.youtube.com/vi/IafVCHkJbtI/0.jpg)](https://youtu.be/IafVCHkJbtI?t=2655)

### Access the web interface

By default the web service is a `ClusterIP`. Reach it with a port-forward:

```shell
kubectl port-forward svc/pihole-web -n pihole 8080:80
# then visit http://localhost:8080/admin
```

If you did not set `admin.password`, a random password is generated. Retrieve it from the secret:

```shell
kubectl get secret pihole-password -n pihole -o jsonpath='{.data.password}' | base64 -d; echo
```

## Configuration

Every option can be set with `--set key=value` at install time or, preferably, in a `values.yaml` file passed with `--values`. See the [Values](#values) table for the full list of parameters and their defaults.

### Exposing Pi-hole

Choose how the DNS and web services are exposed:

- **ClusterIP** — reachable only inside the cluster (the default for all services). Use with an Ingress or a port-forward.
- **LoadBalancer** — exposes the service on an external IP via your cloud provider or MetalLB.
- **Ingress** — set `ingress.enabled: true` to route the web interface through an ingress controller (which must already be installed).
- **Gateway API** — set `route.enabled: true` and `route.parentRefs` to create an `HTTPRoute` instead of an Ingress (needs the Gateway API CRDs and a Gateway).

#### Making DNS reachable on port 53 (start here)

This is the most common stumbling block for new users. This chart installs Pi-hole, but it **cannot know how your cluster is networked** — so it can't automatically make DNS reachable to your clients. You have to pick an exposure strategy that fits your environment.

Why it needs special attention:

- Clients send DNS queries to **UDP/TCP port 53**, a privileged, fixed port. Your router, phones and laptops cannot be told to use "port 31514" — they expect DNS on `53`.
- The default `serviceDns.type` is **`ClusterIP`**: DNS is only reachable inside the cluster. A `NodePort` doesn't help either, it publishes DNS on a *random high port* (30000–32767), **not** on `53`, which clients on your LAN can't use as their DNS server.
- Port 53 on the nodes is often **already taken** by the host OS resolver (e.g. `systemd-resolved` listening on `127.0.0.53:53`, or `dnsmasq`). Binding Pi-hole directly to the host's port 53 will clash with it.

Common strategies, from most to least recommended:

- **LoadBalancer (recommended).** Give the DNS service its own IP with port 53. On bare metal / home labs use [MetalLB](https://metallb.universe.tf/); on a cloud provider use its native load balancer. Point your clients (or your router's DHCP DNS setting) at that IP:

  ```yaml
  serviceDns:
    type: LoadBalancer
    annotations:
      metallb.universe.tf/loadBalancerIPs: 192.168.178.252
  ```

- **hostNetwork / host port.** Bind DNS directly onto a node's IP on port 53 (`hostNetwork: true`, or `dnsHostPort.enabled: true`). Simple, but the node **must not** already run a resolver on port 53 — otherwise disable `systemd-resolved` (or free up port 53) on that node first.

- **NodePort with a fixed port.** Works, but NodePorts must fall in the `30000–32767` range by default, so you cannot serve `53` directly unless you widen `--service-node-port-range` on the API server. Usually not worth it.

If DNS "isn't working" after install, it's almost always because the DNS service is still a `ClusterIP` (the default) rather than exposed on a routable IP on port 53.

#### `loadBalancerIP` is deprecated

The `spec.loadBalancerIP` field is **deprecated** since Kubernetes 1.24 and may be removed in a future version. It still works in this chart, but prefer your provider's annotation-based approach.

**MetalLB:**

```yaml
serviceDns:
  type: LoadBalancer
  annotations:
    metallb.universe.tf/loadBalancerIPs: 192.168.178.252

serviceWeb:
  type: LoadBalancer
  annotations:
    metallb.universe.tf/loadBalancerIPs: 192.168.178.252
```

**Cloud providers:** consult your provider's documentation for the appropriate annotation (e.g. `service.beta.kubernetes.io/aws-load-balancer-eip-allocations` for AWS).

#### Dual-stack (IPv4 + IPv6)

Set `dualStack.enabled: true` on a dual-stack cluster. Every service then becomes one dual-stack service (`PreferDualStack`) with an IPv4 and an IPv6 address. For a `LoadBalancer`, list both addresses in your load balancer's annotation. This works with MetalLB, Cilium LB IPAM, k3s ServiceLB and the major cloud providers:

```yaml
dualStack:
  enabled: true
serviceDns:
  type: LoadBalancer
  annotations:
    metallb.universe.tf/loadBalancerIPs: 192.168.1.53,fd00::53
    # Cilium: io.cilium/lb-ipam-ips: 192.168.1.53,fd00::53
```

If your load balancer can't serve dual-stack services, set `dualStack.splitLoadBalancer: true`. Each `LoadBalancer` service is then split into an IPv4 service and a separate `-ipv6` service. Set the IPv6 address with `annotationsIPv6` (merged over `annotations` for the `-ipv6` service only) or the deprecated `loadBalancerIPv6`:

```yaml
dualStack:
  enabled: true
  splitLoadBalancer: true
serviceDns:
  type: LoadBalancer
  annotations:
    io.cilium/lb-ipam-ips: 192.168.1.53
  annotationsIPv6:
    io.cilium/lb-ipam-ips: fd00::53
```

### Example values.yaml

A typical home setup exposing web and DNS on a shared MetalLB IP with persistence enabled:

```yaml
ftl:
  dns_hosts: "192.168.178.10 nas.lan"
  dns_cnameRecords: "files.lan,nas.lan"

persistentVolumeClaim:
  enabled: true

serviceWeb:
  type: LoadBalancer
  annotations:
    metallb.universe.tf/loadBalancerIPs: 192.168.178.252
    metallb.universe.tf/allow-shared-ip: pihole-svc

serviceDns:
  type: LoadBalancer
  annotations:
    metallb.universe.tf/loadBalancerIPs: 192.168.178.252
    metallb.universe.tf/allow-shared-ip: pihole-svc
```

### Admin password

Set the web interface password with `admin.password`, or reference an existing secret:

```yaml
admin:
  enabled: true
  # inline password (stored in a generated secret)
  password: change-me
  # or reference your own secret instead:
  existingSecret: ""
  passwordKey: password
```

By default (`admin.password` empty, no `existingSecret`) a random password is generated into the `<release>-password` secret and kept across upgrades. Retrieve it as shown in [Access the web interface](#access-the-web-interface). Set `admin.enabled: false` to disable password authentication entirely. The API then accepts changes from every pod that can reach the web Service, even when an SSO proxy protects the ingress; restrict it with a [NetworkPolicy](#networkpolicy).

> **GitOps (Argo CD, Flux with server-side rendering off):** tools that render the chart without access to the cluster can't see the existing secret and would generate a new password on every sync. Use `existingSecret` (e.g. from External Secrets or Sealed Secrets) instead.

### Upstream DNS resolvers

Pi-hole forwards queries it cannot answer to `DNS1` and `DNS2` (default Google, `8.8.8.8` and `8.8.4.4`). To use a single upstream, set `DNS2: ""`; for more than two, set `ftl.dns_upstreams` (semicolon-separated). With `doh.enabled` the upstream is the dnscrypt-proxy sidecar instead.

The pod's own DNS (used by Pi-hole itself, e.g. to download ad lists) is set separately by `podDnsConfig`; by default it is Pi-hole plus Google's `8.8.8.8`. Change it, for example to use Cloudflare:

```yaml
podDnsConfig:
  enabled: true
  policy: "None"
  nameservers:
  - 127.0.0.1
  - 1.1.1.1
```

To opt out of pod DNS configuration entirely (e.g. when running a service mesh):

```yaml
podDnsConfig:
  enabled: false
```

### Local DNS records

Use Pi-hole v6's own settings for local A/AAAA and CNAME records. They show up under *Settings → Local DNS Records* in the web interface, live in your values (Git), and are applied on every start:

```yaml
ftl:
  # "IP hostname", separated by semicolons
  dns_hosts: "192.168.1.10 nas.lan;192.168.1.11 printer.lan"
  # "alias,target", separated by semicolons
  dns_cnameRecords: "files.lan,nas.lan"
```

Settings set this way are read-only in the web interface. If you prefer to manage records in the web interface instead, leave these unset and enable `persistentVolumeClaim`: Pi-hole stores them in `/etc/pihole/pihole.toml`.

The older `dnsmasq.customDnsEntries` (`address=`), `dnsmasq.customCnameEntries` and `dnsmasq.additionalHostsEntries` still work, but these records do not show in the web interface. A dnsmasq `cname=` only resolves when its target is a host record (`ftl.dns_hosts`, `additionalHostsEntries` or DHCP); a target defined with `address=` returns the CNAME without an address. Other dnsmasq options (e.g. an SRV record: `srv-host=_vlmcs._tcp.lan,kms.lan,1688`) go into `ftl.misc_dnsmasq_lines`.

### Encrypted upstream DNS (DoH / DoT / DNSCrypt)

Set `doh.enabled: true` to run a `dnscrypt-proxy` sidecar that Pi-hole uses as its upstream resolver (this replaces the previously used `cloudflared`). Customize the resolver via `doh.config` (raw dnscrypt-proxy TOML):

```yaml
doh:
  enabled: true
  config: |
    listen_addresses = ['0.0.0.0:5053']
    server_names = ['cloudflare', 'google']
```

To expose Prometheus metrics, enable `[monitoring_ui]` in `doh.config` and set:

```yaml
doh:
  metrics:
    enabled: true
    port: 8080
```

### Persistence

Pi-hole stores its configuration, gravity (block lists) and query database under `/etc/pihole`. Enable a `PersistentVolumeClaim` so this survives pod restarts:

```yaml
persistentVolumeClaim:
  enabled: true
  size: 500Mi
```

Without persistence, block lists and settings are re-created from your Helm values on every restart.

With persistence, the chart updates Pi-hole with the `Recreate` strategy (the old pod stops before the new one starts), so two Pi-holes never write to the same database. Set `persistentVolumeClaim.keep: true` to keep the volume when you `helm uninstall`; a reinstall with the same release name reuses it.

### NetworkPolicy

Set `networkPolicy.enabled: true` to restrict pod traffic:

- **DNS (and DHCP with `serviceDhcp.enabled`)** is allowed from every source, because DNS clients are usually outside the cluster. Restrict it with `networkPolicy.ingress.dnsFrom`, e.g. an `ipBlock` for your LAN.
- **The web interface and the metrics ports** are allowed from pods in all namespaces (`networkPolicy.ingress.from`), which covers ingress controllers and Prometheus. If `serviceWeb` is a `LoadBalancer`, add an `ipBlock` for your network.
- **Without an admin password** (`admin.enabled: false`), this default lets every pod in the cluster reconfigure Pi-hole through the API: DNS records, DHCP, lists, upstreams. An SSO proxy in front of the ingress (Authelia, oauth2-proxy, ...) doesn't change that, because the `<release>-web` Service is still reachable inside the cluster, and Pi-hole's passwordless check only stops browser requests from other websites, not a pod that calls it by IP. Restrict `networkPolicy.ingress.from` to your ingress controller and the API clients you run (e.g. nebula-sync):

  ```yaml
  networkPolicy:
    enabled: true
    ingress:
      from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: kube-system
          podSelector:
            matchLabels:
              app.kubernetes.io/name: traefik
        - podSelector:
            matchLabels:
              app: nebula-sync
  ```

  Add Prometheus too if you scrape the metrics ports.
- **Egress** allows DNS, HTTP/HTTPS (ad lists, DoH), DNS over TLS and traffic inside the cluster (`networkPolicy.egress`). With `serviceDhcp.enabled`, the chart also allows UDP 67/68 out for the DHCP replies to the relay and the clients, and with `ntp.sync` UDP 123 for NTP, even if you override `networkPolicy.egress`.
- **ICMP** can't be allowed with a NetworkPolicy. With DHCP, dnsmasq pings an address before offering it; with the policy enabled that check gets no answer, so dnsmasq assumes the address is free. Keep static addresses outside the DHCP range.

The rules use the pod's ports (`dnsPort`, `webHttp`, ...), not the Service ports.

### ServiceAccount

A dedicated ServiceAccount is created by default (`serviceAccount.create: true`) with `automountServiceAccountToken: false`. To use an existing one, set `serviceAccount.create: false` and `serviceAccount.name`.

### Security context (experimental)

`podSecurityContext` and `containerSecurityContext` are available. Pi-hole requires root at startup, so `runAsNonRoot: true`, `allowPrivilegeEscalation: false` and `readOnlyRootFilesystem: true` are **not** supported. The legacy `privileged` and `capabilities` values still work.

### Process priority (SYS_NICE)

Pi-hole sets `misc.nice=-10` by default, which needs the `SYS_NICE` capability. The chart doesn't add it, so every start logs:

```
WARNING: Linux capability CAP_SYS_NICE is not available, needed for raising the process priority set in misc.nice
WARNING: Insufficient permissions to set process priority to -10 (CAP_SYS_NICE required), process priority remains at 0
```

- **The warning is harmless.** It doesn't affect DNS or DHCP. On Kubernetes the nice value only weighs FTL against the other processes in the Pi-hole container; CPU between pods and containers is shared by cgroup weight (`resources.requests`).
- **To raise FTL's priority,** add `SYS_NICE` where the namespace's Pod Security level allows it. It is not on the list the "baseline" standard allows, which is why the chart doesn't add it by default:
  ```yaml
  containerSecurityContext:
    privileged: false
    capabilities:
      add:
        - SYS_NICE
  ```
- **To silence the warning without the capability,** turn the priority change off (`-999` means disabled):
  ```yaml
  ftl:
    misc_nice: "-999"
  ```
- **Capability names have no `CAP_` prefix.** `CAP_SYS_NICE` is accepted by the API but not granted to the container (visible in `CapEff` in `/proc/1/status`), so the warning stays.

### NTP clock sync

Pi-hole's NTP client (`ntp.sync.active`) is off by default (`ntp.sync: false`): the system clock is not namespaced, so setting it changes the time of the whole node and competes with the node's own chrony/timesyncd. With `ntp.sync: true`, the chart adds the `SYS_TIME` capability it needs, to `containerSecurityContext.capabilities` if that is set, otherwise to `capabilities` (not with `privileged`, and not twice), and allows NTP egress in the NetworkPolicy. Setting `ftl.ntp_sync_active` or `extraEnvVars.FTLCONF_ntp_sync_active` to `true` does the same. Pi-hole's NTP server (`ntp.ipv4/ipv6.active`) is not affected. As with `SYS_NICE`, the capability name has no `CAP_` prefix: `CAP_SYS_TIME` is accepted by the API but not granted.

### Health probes

The chart configures `startupProbe`, `livenessProbe` and `readinessProbe`. The default probe command checks Pi-hole itself, not the upstream DNS servers: the API must report DNS as running, and FTL must answer a local `pi.hole` lookup. It uses `curl`, `jq` and `dig`, so custom images must include these binaries.

### Upgrades without downtime

By default a rolling update stops the old pod before the new one is ready (`maxUnavailable: 1`), so DNS is unavailable for a short time. If the new pod can run next to the old one, start it first:

```yaml
maxUnavailable: 0
maxSurge: 1
```

Keep the default when a second pod cannot start while the first one runs: with `persistentVolumeClaim.enabled` (a `ReadWriteOnce` volume cannot be mounted on another node, and two Pi-holes must not share one `gravity.db`), with `dnsHostPort.enabled`, or with `hostNetwork`. The rollout would then wait forever. For real high availability, see the next section.

### High availability

`replicaCount` greater than 1 does not give you HA: every pod has its own `gravity.db`, and the web interface breaks when the Service sends you to another pod (login loop). Pi-hole can't share its database, so run two independent releases instead and keep them in sync:

1. **Two releases on different nodes.** Each gets its own PVC and its own DNS LoadBalancer IP. Install the same values twice (e.g. `helm install pihole ...` and `helm install pihole-2 ...` in one namespace) with a pod anti-affinity on the label both releases share:

   ```yaml
   serviceDns:
     type: LoadBalancer
     annotations:
       metallb.io/loadBalancerIPs: 192.168.1.53   # a different IP per release
   affinity:
     podAntiAffinity:
       requiredDuringSchedulingIgnoredDuringExecution:
         - labelSelector:
             matchLabels:
               app.kubernetes.io/name: pihole
           topologyKey: kubernetes.io/hostname
   ```

   Keep `serviceDhcp` / Pi-hole's DHCP server on one release only.

2. **Sync with [nebula-sync](https://github.com/lovelaze/nebula-sync).** It copies lists, groups, clients and settings from a primary to the replicas through the Pi-hole v6 API, using the in-cluster web Services (`http://pihole-web.<namespace>.svc|<password>` as `PRIMARY`, `http://pihole-2-web.<namespace>.svc|<password>` as `REPLICAS`). Run it as a small Deployment and pass the passwords from a Secret. Make changes only on the primary; the sync is one-way. With `FULL_SYNC: "false"` you can exclude settings that must differ, e.g. `SYNC_CONFIG_DHCP_EXCLUDE: active` so the replica never starts a second DHCP server.

3. **Give clients both DNS IPs** (router or DHCP settings, e.g. `dhcp-option=6,<ip1>,<ip2>`). DNS clients fail over on their own, no shared virtual IP needed.

Settings from values (`ftl`, `extraEnvVars`, `dnsmasq.*`) are not synced: Pi-hole locks `FTLCONF_*` settings against changes through the API, so set them in both releases' values. A full example is in [discussion #182](https://github.com/MoJo2600/pihole-kubernetes/discussions/182).

## Troubleshooting

### Pi-hole does not start with hostNetwork

With `hostNetwork: true` (or `dnsHostPort.enabled: true`) Pi-hole binds directly to the node's ports. If one of them is already taken on the node, FTL cannot start and the pod restarts. The logs (`kubectl logs <pod> -c pihole`) then show an `Address already in use` error for that port.

- **Port 53 (DNS):** usually `systemd-resolved`'s stub listener. Set `DNSStubListener=no` in `/etc/systemd/resolved.conf` and restart `systemd-resolved` (the steps are at the top of [`examples/dhcp-values.yaml`](examples/dhcp-values.yaml)).
- **Port 80/443 (web interface):** another web server or ingress controller on the node. Move Pi-hole's web server with `webHttp` / `webHttps`.
- **Port 67 (DHCP):** another DHCP server on the node.

If you don't need DHCP, you usually don't need `hostNetwork` at all: expose DNS with a `LoadBalancer` service instead (see [Making DNS reachable on port 53](#making-dns-reachable-on-port-53-start-here)).

### DHCP

DHCP clients find the server with layer-2 broadcasts. Kubernetes Services and load balancers (including MetalLB) only forward unicast IP traffic, so broadcasts from your LAN never reach a normal pod. Two setups work:

1. **Host network:** run Pi-hole with `hostNetwork: true` and the `NET_ADMIN` capability on a node in the LAN, and enable the DHCP server with `FTLCONF_dhcp_*` settings. [`examples/dhcp-values.yaml`](examples/dhcp-values.yaml) is a complete starting point.
2. **DHCP relay:** keep Pi-hole off the host network and run a small DHCP relay with host networking (for example [dhcphelper](https://github.com/homeall/dhcphelper), not part of this chart). It receives the broadcasts and forwards them as unicast to Pi-hole's DHCP service (`serviceDhcp.enabled: true`).

### Admin password from existingSecret is rejected

Pi-hole compares the password byte for byte, so a trailing newline in the secret makes the login fail. This happens when the value was encoded with `echo password | base64` (without `-n`) or written into a file with a final newline. Create the secret without one:

```console
kubectl create secret generic pihole-password --from-literal=password='change-me'
```

### Query log shows the same client for every query

Pi-hole sees the source address of each query. If that is a node, a load balancer pod or an ingress, the client IP was replaced (SNAT) on the way:

- Keep `serviceDns.externalTrafficPolicy: Local` (the default), so Kubernetes does not forward queries through another node.
- k3s ServiceLB (Klipper) always replaces the client IP. Use MetalLB or Cilium as the load balancer, or `hostNetwork`, to see the real clients.

## Upgrading

### To 3.0.0

This is a major release with several breaking changes. **You must fully uninstall and reinstall**, because the Kubernetes selector labels changed and pod selectors are immutable. All changes, including the new features, are in the [3.0 release notes](docs/release-notes-3.0.md).

Breaking changes:
- **Selector labels** changed from `app`/`release` to `app.kubernetes.io/name` / `app.kubernetes.io/instance`. An in-place `helm upgrade` will fail with an immutable-field error.
- **`adminPassword`** moved to **`admin.password`**.
- **`whitelist`** renamed to **`allowed`**, and **`blacklist`** renamed to **`denied`**.
- **DNS-over-HTTPS** now uses `dnscrypt-proxy` instead of `cloudflared`. Review the new `doh.*` values (notably `doh.config`).
- **`virtualHost` now sets Pi-hole's web domain** (`FTLCONF_webserver_domain`) and is added to the ingress hosts. The old `VIRTUAL_HOST` variable was a Pi-hole v5 setting that v6 ignores. Since Pi-hole FTL v6.8, `/` on any other host name returns 404 (only `/admin/` still works), so set `virtualHost` to the host name you use for the web interface. Set it to `""` to opt out.
- **Health probes no longer depend on upstream DNS.** The default probes check Pi-hole itself (API plus a local `pi.hole` lookup) instead of resolving `cloudflare.com`, so an internet outage no longer restarts Pi-hole. Each step has its own timeout, so a hung Pi-hole is now reliably restarted. The dnscrypt-proxy sidecar's liveness probe is a TCP check.
- **Pi-hole now also serves the web interface via HTTPS** on `webHttps` (default 443, with Pi-hole's self-signed certificate) and listens on IPv6 as well. Previously the chart limited Pi-hole to plain HTTP. Set `webHttps: ""` to turn HTTPS off, or `redirectToHttps: true` to redirect HTTP to HTTPS (not compatible with `monitoring.sidecar`).
- **New defaults, so check whether you relied on the old ones** (`scripts/migrate-values.py` warns about each):
  - `serviceDns.type` is `ClusterIP` (was `NodePort`). Set `LoadBalancer` to serve your network.
  - `serviceDns.mixedService` is `true`: one `<release>-dns` Service for TCP and UDP instead of `-dns-tcp` and `-dns-udp` (needs Kubernetes 1.26+).
  - `serviceDhcp.enabled` is `false`. The DHCP Service only helps with a DHCP relay.
  - `admin.password` is empty: a random password is generated and kept across upgrades (was `admin`).
  - `strategyType` is chosen automatically: `Recreate` with a persistent volume, `hostNetwork` or `dnsHostPort`, otherwise `RollingUpdate`.
  - `FTLCONF_dns_listeningMode: all` is set by the chart instead of `extraEnvVars`; override it with `ftl.dns_listeningMode`.
  - Pi-hole's NTP client is off (`ntp.sync: false`). Without `SYS_TIME` it never ran anyway; `ntp.sync: true` turns it on and adds the capability. See [NTP clock sync](#ntp-clock-sync).
- **NetworkPolicy:** DNS is allowed from every source by default (`networkPolicy.ingress.dnsFrom`); before, only pods could reach Pi-hole, so clients behind a LoadBalancer were blocked. The rules now use the pod ports.
- **`ingress.pathType` defaults to `Prefix`** instead of `ImplementationSpecific`, which some ingress controllers (e.g. Cilium) treat as a regex or exact match.
- **Dual-stack LoadBalancer services** are one dual-stack Service each instead of an IPv4 plus an `-ipv6` Service; put both addresses into the load balancer annotation. `dualStack.splitLoadBalancer: true` keeps separate services (needed for `loadBalancerIPv6`). See [Dual-stack](#dual-stack-ipv4--ipv6).
- **`dnsPort` now changes the port Pi-hole listens on** (`FTLCONF_dns_port`). Before, it only changed the container port, and any value other than 53 broke the probes.
- **`doh.metrics.enabled` no longer creates a PodMonitor by itself.** It only exposes the dnscrypt-proxy metrics port. A PodMonitor (which needs the Prometheus Operator CRDs) is created only with `monitoring.podMonitor.enabled: true`, and then also scrapes dnscrypt-proxy. Previously, enabling DoH metrics on a cluster without the Prometheus Operator made the install fail.

Pi-hole image changes since the 2.x charts (container 2026.11.0, FTL v6.9) that may affect you:
- Since FTL v6.8, files that are symlinks in `/etc/pihole` and `/var/log/pihole` are no longer handed over to the `pihole` user. Mount ConfigMaps/Secrets there with `subPath` (as the chart does).
- FTL v6.9 changed `webserver.acl`: IPv4 entries now match IPv4 clients everywhere, and IPv6 entries such as `[::]/0` no longer admit IPv4 clients.
- FTL v6.9 changed regex filters: `{,n}` now means `{0,n}`.
- `adlists`, `allowed`, `denied` and `regex` are only imported when the gravity database is first created. With a persistent volume, later changes to these values have no effect.

A helper script, [`scripts/migrate-values.py`](../../scripts/migrate-values.py), automates the key renames above and warns about the DoH changes and the new defaults. It requires Python 3 and PyYAML (`pip install pyyaml`). Comments are not preserved, so review its output before use.

Migration:

```bash
# 1. Backup your Pi-hole config (if using persistent storage)
kubectl cp <namespace>/<pihole-pod>:/etc/pihole ./pihole-backup

#    and keep the volume on uninstall, so the reinstall (same release name) reuses it.
#    Helm reads this policy from the release, so it has to be set with helm, not kubectl.
#    This only updates the PVC; Pi-hole keeps running.
helm upgrade <release-name> mojo2600/pihole -n <namespace> --version <your 2.x version> --reuse-values \
  --set-string 'persistentVolumeClaim.annotations.helm\.sh/resource-policy=keep'

# 2. Backup your Helm values
helm get values <release-name> -n <namespace> -o yaml > pihole-values-backup.yaml

# 3. Convert the backed-up values to the new format (renames adminPassword,
#    whitelist and blacklist; warns about the DoH changes and the new defaults)
python3 scripts/migrate-values.py pihole-values-backup.yaml -o pihole-values-new.yaml

# 4. Uninstall the existing release
helm uninstall <release-name> -n <namespace>

# 5. Reinstall
helm install <release-name> mojo2600/pihole -n <namespace> -f pihole-values-new.yaml
```

## Uninstallation

To uninstall/delete the `pihole` release:

```bash
helm uninstall pihole -n pihole
```

## Values

The following table lists the configurable parameters of the pihole chart and their default values.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| DNS1 | string | `"8.8.8.8"` | default upstream DNS 1 server to use |
| DNS2 | string | `"8.8.4.4"` | default upstream DNS 2 server to use. Set to "" to use only DNS1 |
| adlists | object | `{}` | list of adlists to import when the gravity database is first created. Only used on a fresh /etc/pihole (no gravity.db yet). With a persistent volume, later changes have no effect; manage lists in the web interface or API instead. The same applies to `allowed`, `denied` and `regex`. |
| admin | object | `{"annotations":null,"enabled":true,"existingSecret":"","password":"","passwordKey":"password"}` | Use an existing secret for the admin password. |
| admin.annotations | string | `nil` | Specify [annotations](docs/Values.md#adminannotations) to be added to the secret |
| admin.enabled | bool | `true` | If set to false admin password will be disabled, password specified below and the pre-existing secret (if specified) will be ignored. |
| admin.existingSecret | string | `""` | Specify an existing secret to use as admin password |
| admin.password | string | `""` | Administrator password when not using an existing secret. Empty (default): a random password is generated once and kept across upgrades (read it from the `<release>-password` secret). GitOps tools that render without cluster access (e.g. Argo CD) would generate a new one on every sync; use `existingSecret` or set a password there |
| admin.passwordKey | string | `"password"` | Specify the key inside the secret to use |
| affinity | object | `{}` |  |
| allowed | object | `{}` | list of allowed domains to import when the gravity database is first created (see `adlists`) |
| antiaff.avoidRelease | string | `"pihole1"` | Here you can set the pihole release (you set in `helm install <releasename> ...`) you want to avoid |
| antiaff.enabled | bool | `false` | set to true to enable antiaffinity (example: 2 pihole DNS in the same cluster) |
| antiaff.namespaces | list | `[]` | Here you can pass namespaces to be part of those included in anti-affinity |
| antiaff.strict | bool | `true` | Here you can choose between preferred or required |
| capabilities | object | `{}` | linux capabilities container should run with @deprecated Use containerSecurityContext.capabilities instead |
| commonLabels | object | `{}` | Labels to add to all deployed objects, including the pods |
| containerSecurityContext | object | `{}` | Container-level security context EXPERIMENTAL: These settings are not fully tested with all Pi-hole features! See https://kubernetes.io/docs/tasks/configure-pod-container/security-context/  Why detailed capability management provides limited security benefit for Pi-hole: Pi-hole requires 10+ capabilities including privileged ones like NET_ADMIN, NET_RAW, DAC_OVERRIDE, SETUID, SETGID. This exceeds Docker's default capability set (NET_ADMIN and SYS_NICE are not in defaults). Dropping ALL and re-adding these capabilities provides minimal security improvement over defaults.  Recommended: Only set privileged: false (prevents full host access) The seccompProfile in podSecurityContext provides additional syscall filtering.  NOT SUPPORTED (Pi-hole needs root at startup): - runAsNonRoot: true - runAsUser/runAsGroup: any value - allowPrivilegeEscalation: false (pihole-FTL runs as the pihole user and gets its capabilities from file capabilities set with setcap) - readOnlyRootFilesystem: true (Pi-hole writes to /etc/pihole, /var/log, etc.) |
| customVolumes.config | object | `{}` | any volume type can be used here |
| customVolumes.enabled | bool | `false` | set this to true to enable custom volumes |
| denied | object | `{}` | list of denied domains to import when the gravity database is first created (see `adlists`) |
| deploymentAnnotations | object | `{}` | Additional annotations for the deployment |
| dhcpPort | string | `"67"` | container port for DHCP traffic. Pi-hole's DHCP server always listens on 67; this only changes the declared port |
| dnsHostPort.enabled | bool | `false` | set this to true to enable dnsHostPort |
| dnsHostPort.port | int | `53` | default port for this pod |
| dnsPort | string | `"53"` | port Pi-hole listens on for DNS inside the pod (sets FTLCONF_dns_port). Change it when port 53 is taken, e.g. with hostNetwork on Talos; the services keep `serviceDns.port` (53) and forward to it |
| dnsmasq | object | `{"additionalHostsEntries":[],"customCnameEntries":[],"customDnsEntries":[],"customSettings":null,"enableCustomDnsMasq":true,"staticDhcpEntries":[],"upstreamServers":[]}` | DNS MASQ settings |
| dnsmasq.additionalHostsEntries | list | `[]` | Dnsmasq reads the /etc/hosts file to resolve ips. You can add additional entries if you like |
| dnsmasq.customCnameEntries | list | `[]` | custom dnsmasq CNAME entries. The target must be a host record (`additionalHostsEntries`, `ftl.dns_hosts` or DHCP), an `address=` entry does not work. Prefer `ftl.dns_cnameRecords` (see "Local DNS records" in the README). The format should be:  - cname=cname.foo.bar,foo.bar |
| dnsmasq.customDnsEntries | list | `[]` | Add custom dns entries to override the dns resolution. All lines will be added to the pihole dnsmasq configuration. |
| dnsmasq.customSettings | string | `nil` | Other options |
| dnsmasq.enableCustomDnsMasq | bool | `true` | Load custom user configuration files from /etc/dnsmasq.d |
| dnsmasq.staticDhcpEntries | list | `[]` | Static DHCP config |
| dnsmasq.upstreamServers | list | `[]` | Add upstream dns servers. All lines will be added to the pihole dnsmasq configuration |
| doh.command | list | `[]` | Custom command to the dnscrypt-proxy container |
| doh.config | string | `"listen_addresses = ['0.0.0.0:5053']\nrequire_dnssec = false\nrequire_nolog = true\nrequire_nofilter = true\ndnscrypt_servers = true\ndoh_servers = true\nodoh_servers = false\nipv6_servers = false\nbootstrap_resolvers = ['9.9.9.9:53', '1.1.1.1:53']\ntimeout = 5000\nkeepalive = 30\nlog_level = 2\nuse_syslog = false\ncache = true\ncache_size = 4096\ncache_min_ttl = 2400\ncache_max_ttl = 86400\ncache_neg_min_ttl = 60\ncache_neg_max_ttl = 600\n\n[sources]\n  [sources.'public-resolvers']\n    urls = [\n      'https://raw.githubusercontent.com/DNSCrypt/dnscrypt-resolvers/master/v3/public-resolvers.md',\n      'https://download.dnscrypt.info/resolvers-list/v3/public-resolvers.md'\n    ]\n    cache_file = '/tmp/public-resolvers.md'\n    minisign_key = 'RWQf6LRCGA9i53mlYecO4IzT51TGPpvWucNSCh1CBM0QTaLn73Y7GFO3'\n    refresh_delay = 73\n  [sources.'relays']\n    urls = [\n      'https://raw.githubusercontent.com/DNSCrypt/dnscrypt-resolvers/master/v3/relays.md',\n      'https://download.dnscrypt.info/resolvers-list/v3/relays.md'\n    ]\n    cache_file = '/tmp/relays.md'\n    minisign_key = 'RWQf6LRCGA9i53mlYecO4IzT51TGPpvWucNSCh1CBM0QTaLn73Y7GFO3'\n    refresh_delay = 73\n"` | Example with monitoring_ui enabled for Prometheus metrics: config: |   listen_addresses = ['0.0.0.0:5053']   server_names = ['cloudflare', 'google']   [monitoring_ui]   enabled = true   listen_address = '0.0.0.0:8080'   prometheus_enabled = true |
| doh.enabled | bool | `false` | set to true to enable encrypted DNS via dnscrypt-proxy (supports DoH, DoT, DNSCrypt) |
| doh.envVars | object | `{}` | Here you can pass environment variables to the dnscrypt-proxy container |
| doh.metrics | object | `{"enabled":false,"port":8080}` | Metrics port configuration (enable if you have [monitoring_ui] in your config) |
| doh.metrics.enabled | bool | `false` | set to true to expose the metrics port in the web Service. It is also scraped by the PodMonitor when `monitoring.podMonitor.enabled` is true |
| doh.metrics.port | int | `8080` | port for Prometheus metrics (must match listen_address in [monitoring_ui] config) |
| doh.name | string | `"dnscrypt-proxy"` | name |
| doh.port | string | `"5053"` | port dnscrypt-proxy listens on (must match listen_addresses in config) |
| doh.probes | object | `{"liveness":{"enabled":true,"failureThreshold":3,"initialDelaySeconds":0,"periodSeconds":10,"probe":{},"successThreshold":1,"timeoutSeconds":5},"readiness":{"enabled":true,"failureThreshold":3,"initialDelaySeconds":0,"periodSeconds":10,"probe":{},"successThreshold":1,"timeoutSeconds":5},"startup":{"enabled":true,"failureThreshold":30,"initialDelaySeconds":5,"periodSeconds":5,"probe":{},"timeoutSeconds":5}}` | Probes configuration |
| doh.probes.liveness | object | `{"enabled":true,"failureThreshold":3,"initialDelaySeconds":0,"periodSeconds":10,"probe":{},"successThreshold":1,"timeoutSeconds":5}` | Configure the healthcheck for the dnscrypt-proxy container |
| doh.probes.liveness.enabled | bool | `true` | set to true to enable liveness probe |
| doh.probes.liveness.failureThreshold | int | `3` | defines the failure threshold for the liveness probe |
| doh.probes.liveness.initialDelaySeconds | int | `0` | defines the initial delay for the liveness probe (can be 0 when startup probe is enabled) |
| doh.probes.liveness.periodSeconds | int | `10` | probe interval in seconds |
| doh.probes.liveness.probe | object | `{}` | customize the liveness probe (leave empty for the default) Default: tcpSocket check on the dnscrypt-proxy port. Resolving a name would depend on the upstream servers, and restarting the sidecar does not help during an internet outage. |
| doh.probes.liveness.successThreshold | int | `1` | threshold until the probe is considered successful |
| doh.probes.liveness.timeoutSeconds | int | `5` | defines the timeout in seconds for the liveness probe |
| doh.probes.readiness.enabled | bool | `true` | set to true to enable readiness probe |
| doh.probes.readiness.failureThreshold | int | `3` | defines the failure threshold for the readiness probe |
| doh.probes.readiness.initialDelaySeconds | int | `0` | defines the initial delay for the readiness probe (can be 0 when startup probe is enabled) |
| doh.probes.readiness.periodSeconds | int | `10` | probe interval in seconds |
| doh.probes.readiness.probe | object | `{}` | customize the readiness probe (leave empty for default using doh.port) Default command: /usr/local/bin/dnsprobe cloudflare.com "127.0.0.1:${doh.port}" |
| doh.probes.readiness.successThreshold | int | `1` | threshold until the probe is considered successful |
| doh.probes.readiness.timeoutSeconds | int | `5` | defines the timeout in seconds for the readiness probe |
| doh.probes.startup.enabled | bool | `true` | set to true to enable startup probe |
| doh.probes.startup.failureThreshold | int | `30` | threshold until the container is considered failed (30 * 5s = 150s max startup time) |
| doh.probes.startup.initialDelaySeconds | int | `5` | defines the initial delay for the startup probe |
| doh.probes.startup.periodSeconds | int | `5` | probe interval in seconds |
| doh.probes.startup.probe | object | `{}` | customize the startup probe (leave empty for default using doh.port) Default command: /usr/local/bin/dnsprobe cloudflare.com "127.0.0.1:${doh.port}" |
| doh.probes.startup.timeoutSeconds | int | `5` | defines the timeout in seconds for the startup probe |
| doh.pullPolicy | string | `"IfNotPresent"` | Pull policy |
| doh.repository | string | `"ghcr.io/klutchell/dnscrypt-proxy"` | repository (using GHCR) |
| doh.tag | string | `"2.1.20"` | image tag |
| dualStack.enabled | bool | `false` | set this to true to enable creation of DualStack services or creation of separate IPv6 services if `serviceDns.type` is set to `"LoadBalancer"` |
| dualStack.splitLoadBalancer | bool | `false` | For LoadBalancer services: `false` (default) creates one dual-stack (PreferDualStack) service with both addresses; list both IPs in your load balancer's annotation. `true` creates an IPv4 service plus a separate `-ipv6` service (set its address with `annotationsIPv6` or `loadBalancerIPv6`), for load balancers that cannot serve dual-stack services. |
| extraContainers | list | `[]` |  |
| extraEnvVars | object | `{}` | extraEnvironmentVars is a list of extra environment variables to set for pihole to use. You can use either scalars or project cm, secrets or pod fields via valueFrom. The chart sets `FTLCONF_dns_listeningMode: all` itself (Pi-hole's default `LOCAL` drops queries that reach the pod through a Service or load balancer); override it here or with `ftl.dns_listeningMode` |
| extraEnvVarsSecret | object | `{}` | extraEnvVarsSecret is a list of secrets to load in as environment variables. |
| extraInitContainers | list | `[]` | any initContainers you might want to run before starting pihole |
| extraObjects | list | `[]` | any extra kubernetes manifests you might want |
| extraVolumeMounts | object | `{}` | any extra volume mounts you might want Use subPath when mounting single files into /etc/pihole or /var/log/pihole: since FTL v6.8, Pi-hole no longer takes ownership of symlinks there (ConfigMap/Secret volumes without subPath consist of symlinks). |
| extraVolumes | object | `{}` | any extra volumes you might want |
| ftl | object | `{}` | Pi-hole v6 settings, passed as `FTLCONF_<key>` environment variables (dots in the setting name become underscores). Settings set this way are read-only in the web interface. Use scalars or valueFrom to project ConfigMaps, Secrets or pod fields. See https://docs.pi-hole.net/docker/configuration/ for all keys. Note: since FTL v6.7.1, `misc.dnsmasq_lines` can no longer be changed through the web interface or API, only here. |
| hostNetwork | string | `"false"` | should the container use host network |
| hostname | string | `""` | hostname of pod |
| image.pullPolicy | string | `"IfNotPresent"` | the pull policy |
| image.repository | string | `"pihole/pihole"` | the repository to pull the image from |
| image.tag | string | `""` | the docker tag, if left empty it will get it from the chart's appVersion |
| ingress | object | `{"annotations":{},"enabled":false,"extraLabels":{},"hosts":["chart-example.local"],"path":"/","pathType":"Prefix","tls":[]}` | Configuration for the Ingress |
| ingress.annotations | object | `{}` | Annotations for the ingress |
| ingress.enabled | bool | `false` | Generate a Ingress resource |
| ingress.extraLabels | object | `{}` | Labels for the ingress, e.g. for the external-dns `--label-filter` |
| ingress.pathType | string | `"Prefix"` | `Prefix` works with every ingress controller; `ImplementationSpecific` is regex or exact match on some (e.g. Cilium) |
| maxSurge | int | `1` | The maximum number of Pods that can be created over the desired number of `ReplicaSet` during updating. |
| maxUnavailable | int | `1` | The maximum number of Pods that can be unavailable during updating |
| monitoring.podMonitor | object | `{"enabled":false}` | PodMonitor for the Prometheus Operator. Without the operator, use prometheus.io scrape annotations in `podAnnotations` instead |
| monitoring.podMonitor.enabled | bool | `false` | set this to true to create a PodMonitor (requires the Prometheus Operator CRDs). Scrapes the exporter sidecar and, with `doh.metrics.enabled`, dnscrypt-proxy |
| monitoring.sidecar | object | `{"enabled":false,"image":{"pullPolicy":"IfNotPresent","repository":"ekofr/pihole-exporter","tag":"v1.3.1"},"port":9617,"resources":{"limits":{"memory":"128Mi"}}}` | Sidecar configuration |
| monitoring.sidecar.enabled | bool | `false` | set this to true to enable podMonitor as sidecar |
| monitoring.sidecar.image.repository | string | `"ekofr/pihole-exporter"` | the repository to use |
| networkPolicy | object | `{"egress":[{"ports":[{"port":53,"protocol":"UDP"},{"port":53,"protocol":"TCP"}]},{"ports":[{"port":80,"protocol":"TCP"},{"port":443,"protocol":"TCP"}]},{"ports":[{"port":853,"protocol":"TCP"}]},{"to":[{"namespaceSelector":{}}]}],"enabled":false,"ingress":{"dnsFrom":[],"from":[{"namespaceSelector":{}}]}}` | NetworkPolicy configuration |
| networkPolicy.egress | list | `[{"ports":[{"port":53,"protocol":"UDP"},{"port":53,"protocol":"TCP"}]},{"ports":[{"port":80,"protocol":"TCP"},{"port":443,"protocol":"TCP"}]},{"ports":[{"port":853,"protocol":"TCP"}]},{"to":[{"namespaceSelector":{}}]}]` | Egress rules (allow DNS and HTTP/HTTPS for upstream resolution and ad list updates) |
| networkPolicy.enabled | bool | `false` | Enable NetworkPolicy |
| networkPolicy.ingress | object | `{"dnsFrom":[],"from":[{"namespaceSelector":{}}]}` | Ingress rules configuration |
| networkPolicy.ingress.dnsFrom | list | `[]` | Allowed sources for DNS (and DHCP with `serviceDhcp.enabled`). Empty (default) allows every source, because DNS clients are usually outside the cluster (through a LoadBalancer, the client IP is kept). Restrict it with ipBlocks for your networks if needed |
| networkPolicy.ingress.from | list | `[{"namespaceSelector":{}}]` | Allowed sources for the web interface and the metrics ports. The default allows pods in all namespaces (ingress controllers, Prometheus); add an ipBlock for your network if `serviceWeb` is a LoadBalancer |
| nodeSelector | object | `{}` | Node selector values |
| ntp.sync | bool | `false` | Let Pi-hole set the system clock from an upstream NTP server (FTL `ntp.sync.active`). The clock is not namespaced: this changes the time of the whole node. Adds the `SYS_TIME` capability (not with privileged) and, with `networkPolicy.enabled`, allows NTP egress (UDP 123). `ftl.ntp_sync_active` or `extraEnvVars.FTLCONF_ntp_sync_active` take precedence. |
| persistentVolumeClaim | object | `{"accessModes":["ReadWriteOnce"],"annotations":{},"enabled":false,"keep":false,"size":"500Mi"}` | `PersistentVolumeClaim` for /etc/pihole |
| persistentVolumeClaim.annotations | object | `{}` | Annotations for the `PersistentVolumeClaim` |
| persistentVolumeClaim.enabled | bool | `false` | set to true to use pvc |
| persistentVolumeClaim.keep | bool | `false` | keep the PersistentVolumeClaim (and your Pi-hole data) on `helm uninstall` (`helm.sh/resource-policy: keep`). A reinstall with the same release name reuses it; delete it by hand when you no longer need it |
| persistentVolumeClaim.size | string | `"500Mi"` | volume claim size |
| podAnnotations | object | `{}` | Additional annotations for pods |
| podDisruptionBudget | object | `{"enabled":false,"minAvailable":1}` | configure a Pod Disruption Budget |
| podDisruptionBudget.enabled | bool | `false` | set to true to enable creating the PDB |
| podDisruptionBudget.minAvailable | int | `1` | minimum number of pods Kubernetes should try to have running at all times |
| podDnsConfig.enabled | bool | `true` |  |
| podDnsConfig.nameservers[0] | string | `"127.0.0.1"` |  |
| podDnsConfig.nameservers[1] | string | `"8.8.8.8"` |  |
| podDnsConfig.policy | string | `"None"` |  |
| podLabels | object | `{}` | Additional labels for the pods only |
| podSecurityContext | object | `{}` | Pod-level security context EXPERIMENTAL: These settings are not fully tested with all Pi-hole features! See https://kubernetes.io/docs/tasks/configure-pod-container/security-context/  Pi-hole Docker image limitations: - Requires root at startup for: gravity database, crontab, permissions, setcap - runAsNonRoot, runAsUser, runAsGroup are NOT SUPPORTED - Pi-hole internally drops privileges after initialization |
| privileged | string | `"false"` | should container run in privileged mode @deprecated Use containerSecurityContext.privileged instead |
| probes | object | `{"liveness":{"command":[],"enabled":true,"failureThreshold":3,"initialDelaySeconds":0,"periodSeconds":10,"successThreshold":1,"timeoutSeconds":5,"type":"command"},"readiness":{"command":[],"enabled":true,"failureThreshold":3,"initialDelaySeconds":0,"periodSeconds":10,"successThreshold":1,"timeoutSeconds":5,"type":"command"},"startup":{"command":[],"enabled":true,"failureThreshold":30,"initialDelaySeconds":5,"periodSeconds":5,"timeoutSeconds":5,"type":"command"}}` | Probes configuration |
| probes.liveness | object | `{"command":[],"enabled":true,"failureThreshold":3,"initialDelaySeconds":0,"periodSeconds":10,"successThreshold":1,"timeoutSeconds":5,"type":"command"}` | Liveness probe of the Pi-hole container |
| probes.liveness.command | list | `[]` | Custom command for the liveness probe (leave empty for default using webHttp/dnsPort) Default command (checks only Pi-hole itself, not the upstream DNS servers; with redirectToHttps the API is called via https://localhost:${webHttps} with -k): /bin/sh -c "curl -sf --max-time 2 http://localhost:${webHttp}/api/info/login | jq -e '.dns == true' >/dev/null && [ -n \"$(dig +short +norecurse +retry=0 +time=2 -p ${dnsPort} @127.0.0.1 pi.hole)\" ]" |
| probes.liveness.failureThreshold | int | `3` | threshold until the probe is considered failing |
| probes.liveness.initialDelaySeconds | int | `0` | wait time before trying the liveness probe (can be 0 when startup probe is enabled) |
| probes.liveness.periodSeconds | int | `10` | probe interval in seconds |
| probes.liveness.successThreshold | int | `1` | threshold until the probe is considered successful |
| probes.liveness.timeoutSeconds | int | `5` | timeout in seconds |
| probes.liveness.type | string | `"command"` | Generate a liveness probe 'type' defaults to command, can be set to 'httpGet' to use a HTTP GET type liveness probe. |
| probes.readiness.command | list | `[]` | Custom command for the readiness probe (leave empty for default using webHttp/dnsPort) Default command (checks only Pi-hole itself, not the upstream DNS servers; with redirectToHttps the API is called via https://localhost:${webHttps} with -k): /bin/sh -c "curl -sf --max-time 2 http://localhost:${webHttp}/api/info/login | jq -e '.dns == true' >/dev/null && [ -n \"$(dig +short +norecurse +retry=0 +time=2 -p ${dnsPort} @127.0.0.1 pi.hole)\" ]" |
| probes.readiness.failureThreshold | int | `3` | threshold until the probe is considered failing |
| probes.readiness.initialDelaySeconds | int | `0` | wait time before trying the readiness probe (can be 0 when startup probe is enabled) |
| probes.readiness.periodSeconds | int | `10` | probe interval in seconds |
| probes.readiness.successThreshold | int | `1` | threshold until the probe is considered successful |
| probes.readiness.timeoutSeconds | int | `5` | timeout in seconds |
| probes.readiness.type | string | `"command"` | Generate a readiness probe 'type' defaults to command, can be set to 'httpGet' to use a HTTP GET type readiness probe. |
| probes.startup.command | list | `[]` | Custom command for the startup probe (leave empty for default using webHttp/dnsPort) Default command (checks only Pi-hole itself, not the upstream DNS servers; with redirectToHttps the API is called via https://localhost:${webHttps} with -k): /bin/sh -c "curl -sf --max-time 2 http://localhost:${webHttp}/api/info/login | jq -e '.dns == true' >/dev/null && [ -n \"$(dig +short +norecurse +retry=0 +time=2 -p ${dnsPort} @127.0.0.1 pi.hole)\" ]" |
| probes.startup.failureThreshold | int | `30` | threshold until the container is considered failed (30 * 5s = 150s max startup time) |
| probes.startup.initialDelaySeconds | int | `5` | wait time before trying the startup probe |
| probes.startup.periodSeconds | int | `5` | probe interval in seconds |
| probes.startup.timeoutSeconds | int | `5` | timeout in seconds |
| probes.startup.type | string | `"command"` | Generate a startup probe 'type' defaults to command, can be set to 'httpGet' to use a HTTP GET type startup probe. The startup probe runs before liveness/readiness probes begin. Once it succeeds, liveness and readiness probes take over. |
| redirectToHttps | bool | `false` | set Pi-hole to redirect traffic sent to the HTTP port to HTTPS. Requires webHttps. The default probes then use HTTPS. Not compatible with monitoring.sidecar (pihole-exporter rejects Pi-hole's self-signed certificate). |
| regex | object | `{}` | list of denied regex expressions to import when the gravity database is first created (see `adlists`) |
| replicaCount | int | `1` | The number of replicas |
| resources | object | `{}` | lines, adjust them as necessary, and remove the curly braces after 'resources:'. |
| revisionHistoryLimit | int | `10` | The number of old ReplicaSets to retain to allow rollback |
| route | object | `{"annotations":{},"apiVersion":"gateway.networking.k8s.io/v1","enabled":false,"extraLabels":{},"filters":[],"hostnames":[],"matches":[{"path":{"type":"PathPrefix","value":"/"}}],"parentRefs":[],"timeouts":{}}` | Gateway API HTTPRoute for the web interface, an alternative to `ingress`. Needs the Gateway API CRDs and a Gateway to attach to (`parentRefs`). |
| route.annotations | object | `{}` | Annotations for the HTTPRoute |
| route.apiVersion | string | `"gateway.networking.k8s.io/v1"` | API version of the HTTPRoute (use `gateway.networking.k8s.io/v1beta1` on Gateway API < 1.0) |
| route.enabled | bool | `false` | Generate an HTTPRoute resource |
| route.extraLabels | object | `{}` | Labels for the HTTPRoute |
| route.filters | list | `[]` | Filters applied to matching requests (e.g. RequestRedirect, RequestHeaderModifier) |
| route.hostnames | list | `[]` | Host names of the route. `virtualHost` is added automatically. |
| route.matches | list | `[{"path":{"type":"PathPrefix","value":"/"}}]` | Request matches of the route rule |
| route.parentRefs | list | `[]` | Gateways (listeners) the route attaches to |
| route.timeouts | object | `{}` | Request timeouts of the route rule |
| serviceAccount | object | `{"annotations":{},"automountServiceAccountToken":false,"create":true,"name":""}` | ServiceAccount configuration |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| serviceAccount.automountServiceAccountToken | bool | `false` | Automatically mount a ServiceAccount's API credentials |
| serviceAccount.create | bool | `true` | Specifies whether a service account should be created |
| serviceAccount.name | string | `""` | The name of the service account to use. If not set and create is true, a name is generated using the fullname template |
| serviceDhcp | object | `{"annotations":{},"annotationsIPv6":{},"enabled":false,"externalTrafficPolicy":"Local","extraLabels":{},"loadBalancerClass":"","loadBalancerIP":"","loadBalancerIPv6":"","nodePort":"","port":67,"type":"NodePort"}` | Configuration for the DHCP service on port 67 |
| serviceDhcp.annotations | object | `{}` | Annotations for the DHCP service |
| serviceDhcp.annotationsIPv6 | object | `{}` | Annotations for the separate IPv6 DHCP Service (`dualStack.enabled` with `splitLoadBalancer: true`), merged over `annotations`. Use it for per-family settings such as `io.cilium/lb-ipam-ips` or `metallb.io/loadBalancerIPs`. |
| serviceDhcp.enabled | bool | `false` | Generate a Service resource for DHCP traffic. Only useful with a DHCP relay: DHCP broadcasts do not pass a Service (see Troubleshooting → DHCP in the README). With `hostNetwork` no Service is needed |
| serviceDhcp.externalTrafficPolicy | string | `"Local"` | `spec.externalTrafficPolicy` for the DHCP Service |
| serviceDhcp.extraLabels | object | `{}` | Labels for the DHCP service |
| serviceDhcp.loadBalancerClass | string | `""` | `spec.loadBalancerClass` for the DHCP Service. Only used if type is LoadBalancer. |
| serviceDhcp.loadBalancerIP | string | `""` | A fixed `spec.loadBalancerIP` for the DHCP Service. DEPRECATED in Kubernetes 1.24+. Use `annotations` with your cloud provider's annotation instead (e.g., `metallb.universe.tf/loadBalancerIPs` for MetalLB). |
| serviceDhcp.loadBalancerIPv6 | string | `""` | A fixed `spec.loadBalancerIP` for the IPv6 DHCP Service (`dualStack.splitLoadBalancer: true` only). DEPRECATED in Kubernetes 1.24+. |
| serviceDhcp.nodePort | string | `""` | Optional node port for the DHCP service |
| serviceDhcp.port | int | `67` | The port of the DHCP service |
| serviceDhcp.type | string | `"NodePort"` | `spec.type` for the DHCP Service |
| serviceDns | object | `{"annotations":{},"annotationsIPv6":{},"externalTrafficPolicy":"Local","extraLabels":{},"loadBalancerClass":"","loadBalancerIP":"","loadBalancerIPv6":"","mixedService":true,"nodePort":"","port":53,"type":"ClusterIP"}` | Configuration for the DNS service on port 53 |
| serviceDns.annotations | object | `{}` | Annotations for the DNS service |
| serviceDns.annotationsIPv6 | object | `{}` | Annotations for the separate IPv6 DNS Service (`dualStack.enabled` with `splitLoadBalancer: true`), merged over `annotations`. Use it for per-family settings such as `io.cilium/lb-ipam-ips` or `metallb.io/loadBalancerIPs`. |
| serviceDns.externalTrafficPolicy | string | `"Local"` | `spec.externalTrafficPolicy` for the DNS Service |
| serviceDns.extraLabels | object | `{}` | Labels for the DNS service |
| serviceDns.loadBalancerClass | string | `""` | `spec.loadBalancerClass` for the DNS Service. Only used if type is LoadBalancer. |
| serviceDns.loadBalancerIP | string | `""` | A fixed `spec.loadBalancerIP` for the DNS Service. DEPRECATED in Kubernetes 1.24+. Use `annotations` with your cloud provider's annotation instead (e.g., `metallb.universe.tf/loadBalancerIPs` for MetalLB). |
| serviceDns.loadBalancerIPv6 | string | `""` | A fixed `spec.loadBalancerIP` for the IPv6 DNS Service (`dualStack.splitLoadBalancer: true` only). DEPRECATED in Kubernetes 1.24+. |
| serviceDns.mixedService | bool | `true` | one Service for DNS over TCP and UDP (`<release>-dns`). Set to false for separate `-dns-tcp` and `-dns-udp` Services |
| serviceDns.nodePort | string | `""` | Optional node port for the DNS service |
| serviceDns.port | int | `53` | The port of the DNS service |
| serviceDns.type | string | `"ClusterIP"` | `spec.type` for the DNS Service. `ClusterIP` is only reachable inside the cluster; to serve your network use `LoadBalancer` (or `hostNetwork`), see "Making DNS reachable on port 53" in the README |
| serviceWeb | object | `{"annotations":{},"annotationsIPv6":{},"externalTrafficPolicy":"Local","extraLabels":{},"http":{"enabled":true,"nodePort":"","port":80},"https":{"enabled":true,"nodePort":"","port":443},"loadBalancerClass":"","loadBalancerIP":"","loadBalancerIPv6":"","type":"ClusterIP"}` | Configuration for the web interface service |
| serviceWeb.annotations | object | `{}` | Annotations for the web interface service |
| serviceWeb.annotationsIPv6 | object | `{}` | Annotations for the separate IPv6 web interface Service (`dualStack.enabled` with `splitLoadBalancer: true`), merged over `annotations`. Use it for per-family settings such as `io.cilium/lb-ipam-ips` or `metallb.io/loadBalancerIPs`. |
| serviceWeb.externalTrafficPolicy | string | `"Local"` | `spec.externalTrafficPolicy` for the web interface Service |
| serviceWeb.extraLabels | object | `{}` | Labels for the web interface service |
| serviceWeb.http | object | `{"enabled":true,"nodePort":"","port":80}` | Configuration for the HTTP web interface listener |
| serviceWeb.http.enabled | bool | `true` | Generate a service for HTTP traffic |
| serviceWeb.http.nodePort | string | `""` | Optional node port for the web HTTP service |
| serviceWeb.http.port | int | `80` | The port of the web HTTP service |
| serviceWeb.https | object | `{"enabled":true,"nodePort":"","port":443}` | Configuration for the HTTPS web interface listener |
| serviceWeb.https.enabled | bool | `true` | Generate a service for HTTPS traffic |
| serviceWeb.https.nodePort | string | `""` | Optional node port for the web HTTPS service |
| serviceWeb.https.port | int | `443` | The port of the web HTTPS service |
| serviceWeb.loadBalancerClass | string | `""` | `spec.loadBalancerClass` for the web interface Service. Only used if type is LoadBalancer. |
| serviceWeb.loadBalancerIP | string | `""` | A fixed `spec.loadBalancerIP` for the web interface Service. DEPRECATED in Kubernetes 1.24+. Use `annotations` with your cloud provider's annotation instead (e.g., `metallb.universe.tf/loadBalancerIPs` for MetalLB). |
| serviceWeb.loadBalancerIPv6 | string | `""` | A fixed `spec.loadBalancerIP` for the IPv6 web interface Service (`dualStack.splitLoadBalancer: true` only). DEPRECATED in Kubernetes 1.24+. |
| serviceWeb.type | string | `"ClusterIP"` | `spec.type` for the web interface Service |
| strategyType | string | `""` | The `spec.strategy.type` for updates. Empty (default) picks it automatically: `Recreate` with a persistent volume, `hostNetwork` or `dnsHostPort` (the new pod could not start next to the old one, or two Pi-holes would share one gravity.db), otherwise `RollingUpdate`. Set `RollingUpdate` or `Recreate` to force one. |
| tolerations | list | `[]` | Toleration |
| topologySpreadConstraints | list | `[]` | Specify a priorityClassName priorityClassName: "" Reference: https://kubernetes.io/docs/concepts/workloads/pods/pod-topology-spread-constraints/ |
| virtualHost | string | `"pi.hole"` | Domain of the web interface. Sets Pi-hole's `webserver.domain` (FTLCONF_webserver_domain) and is added to `ingress.hosts`. Since FTL v6.8, `/` on any other host name returns 404 unless `webserver.serve_all` is enabled. Set to "" to leave both untouched. |
| webHttp | string | `"80"` | port the container should use to expose HTTP traffic |
| webHttps | string | `"443"` | port the container should use to expose HTTPS traffic. When empty Pi-hole does not listen on HTTPS |

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| MoJo2600 | <christian.erhardt@mojo2k.de> |  |

## Credits

[Pi-hole®](https://pi-hole.net/)

## Contributing

Feel free to contribute by making a [pull request](https://github.com/MoJo2600/pihole-kubernetes/pull/new/master).

Please read [Contribution Guide](../../CONTRIBUTING.md) for more information on how you can contribute to this Chart.

## Contributors ✨

Thanks goes to these wonderful people:

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="http://www.mojo2k.de"><img src="https://avatars1.githubusercontent.com/u/2462817?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Christian Erhardt</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://billimek.com/"><img src="https://avatars0.githubusercontent.com/u/6393612?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Jeff Billimek</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/imle"><img src="https://avatars3.githubusercontent.com/u/4809109?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Steven Imle</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jetersen"><img src="https://avatars2.githubusercontent.com/u/1661688?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Joseph Petersen</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/SiM22"><img src="https://avatars2.githubusercontent.com/u/5759618?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Simon Garcia</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/AndyG-0"><img src="https://avatars1.githubusercontent.com/u/29743443?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Andy Gilbreath</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/northerngit"><img src="https://avatars0.githubusercontent.com/u/4513272?v=4&size=100" width="100px;" alt=""/><br /><sub><b>James Wilson</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jskswamy"><img src="https://avatars2.githubusercontent.com/u/232449?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Krishnaswamy Subramanian</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/luqasn"><img src="https://avatars2.githubusercontent.com/u/274902?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Lucas Romero</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/konturn"><img src="https://avatars0.githubusercontent.com/u/35545508?v=4&size=100" width="100px;" alt=""/><br /><sub><b>konturn</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tdorsey"><img src="https://avatars3.githubusercontent.com/u/1218404?v=4&size=100" width="100px;" alt=""/><br /><sub><b>tdorsey</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/alesz"><img src="https://avatars0.githubusercontent.com/u/12436980?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Ales Zelenik</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dtourde"><img src="https://avatars1.githubusercontent.com/u/49169262?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Damien TOURDE</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/putz612"><img src="https://avatars3.githubusercontent.com/u/952758?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Jason Sievert</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/joshua-nord"><img src="https://avatars2.githubusercontent.com/u/1181300?v=4&size=100" width="100px;" alt=""/><br /><sub><b>joshua-nord</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://maximilianbo.de/"><img src="https://avatars3.githubusercontent.com/u/9051309?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Maximilian Bode</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/raackley"><img src="https://avatars0.githubusercontent.com/u/1700688?v=4&size=100" width="100px;" alt=""/><br /><sub><b>raackley</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/StoicPerlman"><img src="https://avatars1.githubusercontent.com/u/3152359?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Sam Kleiner</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://arpankapoor.com/"><img src="https://avatars3.githubusercontent.com/u/3677810?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Arpan Kapoor</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/chrodriguez"><img src="https://avatars1.githubusercontent.com/u/1460882?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Christian Rodriguez</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://dave-cahill.com/"><img src="https://avatars0.githubusercontent.com/u/361096?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Dave Cahill</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/golgoth31"><img src="https://avatars2.githubusercontent.com/u/5741421?v=4&size=100" width="100px;" alt=""/><br /><sub><b>golgoth31</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://greg.jeanmart.me/"><img src="https://avatars3.githubusercontent.com/u/506784?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Greg Jeanmart</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ballj"><img src="https://avatars1.githubusercontent.com/u/38097813?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Joseph Ball</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://www.oneko.org/"><img src="https://avatars2.githubusercontent.com/u/4233214?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Karlos</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dza89"><img src="https://avatars0.githubusercontent.com/u/20373984?v=4&size=100" width="100px;" alt=""/><br /><sub><b>dza89</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mikewhitley"><img src="https://avatars0.githubusercontent.com/u/52802633?v=4&size=100" width="100px;" alt=""/><br /><sub><b>mikewhitley</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Vashiru"><img src="https://avatars2.githubusercontent.com/u/11370057?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Vashiru</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/sam-kleiner"><img src="https://avatars.githubusercontent.com/u/63059772?v=4&size=100" width="100px;" alt=""/><br /><sub><b>sam-kleiner</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.linkedin.com/in/alexgorbatchev/"><img src="https://avatars.githubusercontent.com/u/65633?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Alex Gorbatchev</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/c-yco"><img src="https://avatars.githubusercontent.com/u/355591?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Alexander Rabenstein</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://tibbon.com/"><img src="https://avatars.githubusercontent.com/u/82880?v=4&size=100" width="100px;" alt=""/><br /><sub><b>David Fisher</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/utkuozdemir"><img src="https://avatars.githubusercontent.com/u/1465819?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Utku Özdemir</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://mor.re/"><img src="https://avatars.githubusercontent.com/u/7683567?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Morre Meyer</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/johnsondnz"><img src="https://avatars.githubusercontent.com/u/7608966?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Donald Johnson</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://winston.milli.ng/"><img src="https://avatars.githubusercontent.com/u/6162814?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Winston R. Milling</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/larivierec"><img src="https://avatars.githubusercontent.com/u/3633214?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Christopher Larivière</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://sievenpiper.co/"><img src="https://avatars.githubusercontent.com/u/1131882?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Justin Sievenpiper</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/beastob"><img src="https://avatars.githubusercontent.com/u/76816315?v=4&size=100" width="100px;" alt=""/><br /><sub><b>beastob</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://niftyside.io/"><img src="https://avatars.githubusercontent.com/u/653739?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Daniel Mühlbachler-Pietrzykowski</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/consideRatio"><img src="https://avatars.githubusercontent.com/u/3837114?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Erik Sundell</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Ornias1993"><img src="https://avatars.githubusercontent.com/u/7613738?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Kjeld Schouten-Lebbing</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mrwulf"><img src="https://avatars.githubusercontent.com/u/2494769?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Brandon Wulf</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/DerRockWolf"><img src="https://avatars.githubusercontent.com/u/50499906?v=4&size=100" width="100px;" alt=""/><br /><sub><b>DerRockWolf</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/brnl"><img src="https://avatars.githubusercontent.com/u/3243133?v=4&size=100" width="100px;" alt=""/><br /><sub><b>brnl</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://rafaelgaspar.xyz/"><img src="https://avatars.githubusercontent.com/u/5567?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Rafael Gaspar</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://chadimasri.com/"><img src="https://avatars.githubusercontent.com/u/1502811?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Chadi El Masri</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dfoulkes"><img src="https://avatars.githubusercontent.com/u/8113674?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Dan Foulkes</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/george124816"><img src="https://avatars.githubusercontent.com/u/26443736?v=4&size=100" width="100px;" alt=""/><br /><sub><b>George Rodrigues</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://pascaliske.dev/"><img src="https://avatars.githubusercontent.com/u/7473880?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Pascal Iske</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.reyth.dev/"><img src="https://avatars.githubusercontent.com/u/23526880?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Theo REY</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/piwi3910"><img src="https://avatars.githubusercontent.com/u/12539757?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Watteel Pascal</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/frittenlab"><img src="https://avatars.githubusercontent.com/u/29921946?v=4&size=100" width="100px;" alt=""/><br /><sub><b>simon</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/vince-vibin"><img src="https://avatars.githubusercontent.com/u/99386370?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Vincent</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Keydrain"><img src="https://avatars.githubusercontent.com/u/5723055?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Clint</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tamcore"><img src="https://avatars.githubusercontent.com/u/319917?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Philipp B.</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ebCrypto"><img src="https://avatars.githubusercontent.com/u/44279886?v=4&size=100" width="100px;" alt=""/><br /><sub><b>ebCrypto</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://ucdialplans.com/"><img src="https://avatars.githubusercontent.com/u/44060527?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Ken Lasko</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mbund"><img src="https://avatars.githubusercontent.com/u/25110595?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Mark Bundschuh</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://fotoallerlei.com/"><img src="https://avatars.githubusercontent.com/u/3430656?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Max Rosin</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/yzeng1314"><img src="https://avatars.githubusercontent.com/u/6365365?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Yang</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dwarf-king-hreidmar"><img src="https://avatars.githubusercontent.com/u/45319558?v=4&size=100" width="100px;" alt=""/><br /><sub><b>dwarf-king-hreidmar</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/s94santos"><img src="https://avatars.githubusercontent.com/u/10950164?v=4&size=100" width="100px;" alt=""/><br /><sub><b>s94santos</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/adamrdavid"><img src="https://avatars.githubusercontent.com/u/1854876?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Adam David</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/bkonicek"><img src="https://avatars.githubusercontent.com/u/7397530?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Ben Konicek</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Gabisonfire"><img src="https://avatars.githubusercontent.com/u/6416239?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Gabisonfire</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/giolekva"><img src="https://avatars.githubusercontent.com/u/124899?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Giorgi Lekveishvili</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/paimonsoror"><img src="https://avatars.githubusercontent.com/u/935046?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Paimon Sorornejad</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mivek"><img src="https://avatars.githubusercontent.com/u/9912558?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Jean-Kevin KPADEY</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/aogier"><img src="https://avatars.githubusercontent.com/u/321364?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Alessandro Ogier</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Luukvdm"><img src="https://avatars.githubusercontent.com/u/25098818?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Luuk v/d Maagdenberg</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/sunsided"><img src="https://avatars.githubusercontent.com/u/495335?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Markus Mayer</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/prfj"><img src="https://avatars.githubusercontent.com/u/37109548?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Paulo Jesus</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://blog.bergpb.dev/"><img src="https://avatars.githubusercontent.com/u/11005963?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Lindemberg Barbosa</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://ricardobaltazar.com/"><img src="https://avatars.githubusercontent.com/u/1923140?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Ricardo Baltazar Chaves</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/wolviecb"><img src="https://avatars.githubusercontent.com/u/13783824?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Thomas Andrade</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/alexinthesky"><img src="https://avatars.githubusercontent.com/u/14876221?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Alexandre Chappaz</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/cristiklein"><img src="https://avatars.githubusercontent.com/u/1660833?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Cristian Klein</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://flouret.com/"><img src="https://avatars.githubusercontent.com/u/9397098?v=4&size=100" width="100px;" alt=""/><br /><sub><b>JP Flouret</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/fernferret"><img src="https://avatars.githubusercontent.com/u/72811?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Eric</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/anokfireball"><img src="https://avatars.githubusercontent.com/u/10155170?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Fabian Koller</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/AresiusXP"><img src="https://avatars.githubusercontent.com/u/20631840?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Patricio Danos</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://craigcabrey.com/"><img src="https://avatars.githubusercontent.com/u/894565?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Craig Cabrey</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://kjeldschouten.nl/"><img src="https://avatars.githubusercontent.com/u/7613738?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Kjeld Schouten</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ErikTMA"><img src="https://avatars.githubusercontent.com/u/13119759?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Erik Andersen</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/HakimHC"><img src="https://avatars.githubusercontent.com/u/113886603?v=4&size=100" width="100px;" alt=""/><br /><sub><b>hakahmed</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/i5Js"><img src="https://avatars.githubusercontent.com/u/1070363?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Javi</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Javex"><img src="https://avatars.githubusercontent.com/u/641439?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Flozza</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jomovo"><img src="https://avatars.githubusercontent.com/u/33429636?v=4&size=100" width="100px;" alt=""/><br /><sub><b>jomovo</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.geekbundle.org/"><img src="https://avatars.githubusercontent.com/u/3735459?v=4&size=100" width="100px;" alt=""/><br /><sub><b>madic-creates</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/nolte"><img src="https://avatars.githubusercontent.com/u/538808?v=4&size=100" width="100px;" alt=""/><br /><sub><b>nolte</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/rajsinghtech"><img src="https://avatars.githubusercontent.com/u/26187752?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Raj Singh</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Suiram1701"><img src="https://avatars.githubusercontent.com/u/110390261?v=4&size=100" width="100px;" alt=""/><br /><sub><b>Suiram1701</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/whzy1314"><img src="https://avatars.githubusercontent.com/u/6365365?v=4&size=100" width="100px;" alt=""/><br /><sub><b>whzy1314</b></sub></a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.14.2](https://github.com/norwoodj/helm-docs/releases/v1.14.2)
