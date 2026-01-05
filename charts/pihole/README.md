# pihole

Installs pihole in kubernetes

![Version: 2.35.0](https://img.shields.io/badge/Version-2.35.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 2025.11.1](https://img.shields.io/badge/AppVersion-2025.11.1-informational?style=flat-square) <!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-27-blue.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## Source Code

* <https://github.com/MoJo2600/pihole-kubernetes/tree/main/charts/pihole>
* <https://pi-hole.net/>
* <https://github.com/pi-hole>
* <https://github.com/pi-hole/docker-pi-hole>

## Installation

Jeff Geerling on YouTube made a video about the installation of this chart:

[![Jeff Geerling on YouTube](https://img.youtube.com/vi/IafVCHkJbtI/0.jpg)](https://youtu.be/IafVCHkJbtI?t=2655)

### Add Helm repository

```shell
helm repo add mojo2600 https://mojo2600.github.io/pihole-kubernetes/
helm repo update
```

### Configure the chart

The following items can be set via `--set` flag during installation or configured by editing the `values.yaml` directly.

#### Configure the way how to expose pihole service:

- **Ingress**: The ingress controller must be installed in the Kubernetes cluster.
- **ClusterIP**: Exposes the service on a cluster-internal IP. Choosing this value makes the service only reachable from within the cluster.
- **LoadBalancer**: Exposes the service externally using a cloud provider's load balancer.

### Deprecation Notice: `loadBalancerIP`

The `spec.loadBalancerIP` field is **deprecated** since Kubernetes 1.24 and may be removed in a future Kubernetes version. While the `loadBalancerIP` values still work in this chart, we recommend migrating to your cloud provider's annotation-based approach.

**For MetalLB users**, use the annotation instead:

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

**For cloud providers**, consult your provider's documentation for the appropriate annotation (e.g., `service.beta.kubernetes.io/aws-load-balancer-eip-allocations` for AWS).

## My settings in values.yaml

```console
dnsmasq:
  customDnsEntries:
    - address=/nas/192.168.178.10
 
  customCnameEntries:
    - cname=foo.nas,nas

persistentVolumeClaim:
  enabled: true

serviceWeb:
  loadBalancerIP: 192.168.178.252
  annotations:
    metallb.universe.tf/allow-shared-ip: pihole-svc
  type: LoadBalancer

serviceDns:
  loadBalancerIP: 192.168.178.252
  annotations:
    metallb.universe.tf/allow-shared-ip: pihole-svc
  type: LoadBalancer
```

## Configuring Upstream DNS Resolvers

By default, `pihole-kubernetes` will configure pod DNS automatically to use Google's `8.8.8.8` nameserver for upstream
DNS resolution. You can configure this, or opt-out of pod DNS configuration completely.

### Changing The Upstream DNS Resolver

For example, to use Cloudflare's resolver:

```yaml
podDnsConfig:
  enabled: true
  policy: "None"
  nameservers:
  - 127.0.0.1
  - 1.1.1.1
```

### Disabling Pod DNS Configuration

If you have other DNS policy at play (for example, when running a service mesh), you may not want to have
`pihole-kubernetes` control this behavior. In that case, you can disable DNS configuration on `pihole` pods:

```yaml
podDnsConfig:
  enabled: false
```

## Upgrading

### To 3.0.0

TODO

### To 2.0.0

This version splits the DHCP service into its own resource and puts the configuration to `serviceDhcp`.

**If you have not changed any configuration for `serviceDns`, you don’t need to do anything.**

If you have changed your `serviceDns` configuration, **copy** your `serviceDns` section into a new `serviceDhcp` section.

### To 1.8.22

To enhance compatibility for Traefik, we split the TCP and UDP service into Web and DNS. This means, if you have a dedicated configuration for the service, you have to
update your `values.yaml` and add a new configuration for this new service.

Before (In my case, with metallb):
```
serviceTCP:
  loadBalancerIP: 192.168.178.252
  annotations:
    metallb.universe.tf/allow-shared-ip: pihole-svc

serviceUDP:
  loadBalancerIP: 192.168.178.252
  annotations:
    metallb.universe.tf/allow-shared-ip: pihole-svc
```

After:
```
serviceWeb:
  loadBalancerIP: 192.168.178.252
  annotations:
    metallb.universe.tf/allow-shared-ip: pihole-svc

serviceDns:
  loadBalancerIP: 192.168.178.252
  annotations:
    metallb.universe.tf/allow-shared-ip: pihole-svc
```

Version 1.8.22 has switched from the deprecated ingress api `extensions/v1beta1` to the go forward version `networking.k8s.io/v1`. This means that your cluster must be running 1.19.x as this api is not available on older versions. If necessary to run on an older Kubernetes Version, it can be done by modifying the ingress.yaml and changing the api definition back. The backend definition would also change from:

```
            backend:
              service:
                name: \{\{ $serviceName \}\}
                port:
                  name: http
```
to:
```
            backend:
              serviceName: \{\{ $serviceName \}\}
              servicePort: http
```

## Uninstallation

To uninstall/delete the `my-release` deployment (NOTE: `--purge` is default behaviour in Helm 3+ and will error):

```bash
helm delete --purge my-release
```

## Configuration

The following table lists the configurable parameters of the pihole chart and the default values.

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| DNS1 | string | `"8.8.8.8"` | default upstream DNS 1 server to use |
| DNS2 | string | `"8.8.4.4"` | default upstream DNS 2 server to use |
| adlists | object | `{}` | list of adlists to import during initial start of the container |
| admin | object | `{"annotations":null,"enabled":true,"existingSecret":"","password":"admin","passwordKey":"password"}` | Use an existing secret for the admin password. |
| admin.annotations | string | `nil` | Specify [annotations](docs/Values.md#admin.annotations) to be added to the secret |
| admin.enabled | bool | `true` | If set to false admin password will be disabled, password specified below and the pre-existing secret (if specified) will be ignored. |
| admin.existingSecret | string | `""` | Specify an existing secret to use as admin password |
| admin.password | string | `"admin"` | Administrator password when not using an existing secret (see below) |
| admin.passwordKey | string | `"password"` | Specify the key inside the secret to use |
| affinity | object | `{}` |  |
| allowed | object | `{}` | list of allowed domains to import during initial start of the container |
| antiaff.avoidRelease | string | `"pihole1"` | Here you can set the pihole release (you set in `helm install <releasename> ...`) you want to avoid |
| antiaff.enabled | bool | `false` | set to true to enable antiaffinity (example: 2 pihole DNS in the same cluster) |
| antiaff.namespaces | list | `[]` | Here you can pass namespaces to be part of those inclueded in anti-affinity |
| antiaff.strict | bool | `true` | Here you can choose between preferred or required |
| capabilities | object | `{}` | linux capabilities container should run with @deprecated Use containerSecurityContext.capabilities instead |
| commonLabels | object | `{}` | Labels to add to all deployed objects |
| containerSecurityContext | object | `{}` | Container-level security context EXPERIMENTAL: These settings are not fully tested with all Pi-hole features! See https://kubernetes.io/docs/tasks/configure-pod-container/security-context/  Why detailed capability management provides limited security benefit for Pi-hole: Pi-hole requires 10+ capabilities including privileged ones like NET_ADMIN, NET_RAW, DAC_OVERRIDE, SETUID, SETGID. This exceeds Docker's default capability set (NET_ADMIN and SYS_NICE are not in defaults). Dropping ALL and re-adding these capabilities provides minimal security improvement over defaults.  Recommended: Only set privileged: false (prevents full host access) The seccompProfile in podSecurityContext provides additional syscall filtering.  NOT SUPPORTED (Pi-hole needs root at startup): - runAsNonRoot: true - runAsUser/runAsGroup: any value - allowPrivilegeEscalation: false (required for setcap) - readOnlyRootFilesystem: true (Pi-hole writes to /etc/pihole, /var/log, etc.) |
| customVolumes.config | object | `{}` | any volume type can be used here |
| customVolumes.enabled | bool | `false` | set this to true to enable custom volumes |
| denied | object | `{}` | list of denied domains to import during initial start of the container |
| deploymentAnnotations | object | `{}` | Additional annotations for the deployment |
| dnsHostPort.enabled | bool | `false` | set this to true to enable dnsHostPort |
| dnsHostPort.port | int | `53` | default port for this pod |
| dnsmasq | object | `{"additionalHostsEntries":[],"customCnameEntries":[],"customDnsEntries":[],"customSettings":null,"enableCustomDnsMasq":true,"staticDhcpEntries":[],"upstreamServers":[]}` | DNS MASQ settings |
| dnsmasq.additionalHostsEntries | list | `[]` | Dnsmasq reads the /etc/hosts file to resolve ips. You can add additional entries if you like |
| dnsmasq.customCnameEntries | list | `[]` | Here we specify custom cname entries that should point to `A` records or elements in customDnsEntries array. The format should be:  - cname=cname.foo.bar,foo.bar  - cname=cname.bar.foo,bar.foo  - cname=cname record,dns record |
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
| doh.metrics.enabled | bool | `false` | set to true to expose the metrics port (8080) in Service and create PodMonitor |
| doh.metrics.port | int | `8080` | port for Prometheus metrics (must match listen_address in [monitoring_ui] config) |
| doh.name | string | `"dnscrypt-proxy"` | name |
| doh.probes | object | `{"liveness":{"enabled":true,"failureThreshold":3,"initialDelaySeconds":0,"periodSeconds":10,"probe":{"exec":{"command":["/usr/local/bin/dnsprobe","cloudflare.com","127.0.0.1:5053"]}},"successThreshold":1,"timeoutSeconds":5},"readiness":{"enabled":true,"failureThreshold":3,"initialDelaySeconds":0,"periodSeconds":10,"probe":{"exec":{"command":["/usr/local/bin/dnsprobe","cloudflare.com","127.0.0.1:5053"]}},"successThreshold":1,"timeoutSeconds":5},"startup":{"enabled":true,"failureThreshold":30,"initialDelaySeconds":5,"periodSeconds":5,"probe":{"exec":{"command":["/usr/local/bin/dnsprobe","cloudflare.com","127.0.0.1:5053"]}},"timeoutSeconds":5}}` | Probes configuration |
| doh.probes.liveness | object | `{"enabled":true,"failureThreshold":3,"initialDelaySeconds":0,"periodSeconds":10,"probe":{"exec":{"command":["/usr/local/bin/dnsprobe","cloudflare.com","127.0.0.1:5053"]}},"successThreshold":1,"timeoutSeconds":5}` | Configure the healthcheck for the dnscrypt-proxy container |
| doh.probes.liveness.enabled | bool | `true` | set to true to enable liveness probe |
| doh.probes.liveness.failureThreshold | int | `3` | defines the failure threshold for the liveness probe |
| doh.probes.liveness.initialDelaySeconds | int | `0` | defines the initial delay for the liveness probe (can be 0 when startup probe is enabled) |
| doh.probes.liveness.periodSeconds | int | `10` | probe interval in seconds |
| doh.probes.liveness.probe | object | `{"exec":{"command":["/usr/local/bin/dnsprobe","cloudflare.com","127.0.0.1:5053"]}}` | customize the liveness probe (uses dnsprobe tool) |
| doh.probes.liveness.successThreshold | int | `1` | threshold until the probe is considered successful |
| doh.probes.liveness.timeoutSeconds | int | `5` | defines the timeout in seconds for the liveness probe |
| doh.probes.readiness.enabled | bool | `true` | set to true to enable readiness probe |
| doh.probes.readiness.failureThreshold | int | `3` | defines the failure threshold for the readiness probe |
| doh.probes.readiness.initialDelaySeconds | int | `0` | defines the initial delay for the readiness probe (can be 0 when startup probe is enabled) |
| doh.probes.readiness.periodSeconds | int | `10` | probe interval in seconds |
| doh.probes.readiness.probe | object | `{"exec":{"command":["/usr/local/bin/dnsprobe","cloudflare.com","127.0.0.1:5053"]}}` | customize the readiness probe (uses dnsprobe tool) |
| doh.probes.readiness.successThreshold | int | `1` | threshold until the probe is considered successful |
| doh.probes.readiness.timeoutSeconds | int | `5` | defines the timeout in seconds for the readiness probe |
| doh.probes.startup.enabled | bool | `true` | set to true to enable startup probe |
| doh.probes.startup.failureThreshold | int | `30` | threshold until the container is considered failed (30 * 5s = 150s max startup time) |
| doh.probes.startup.initialDelaySeconds | int | `5` | defines the initial delay for the startup probe |
| doh.probes.startup.periodSeconds | int | `5` | probe interval in seconds |
| doh.probes.startup.probe | object | `{"exec":{"command":["/usr/local/bin/dnsprobe","cloudflare.com","127.0.0.1:5053"]}}` | customize the startup probe (uses dnsprobe tool) |
| doh.probes.startup.timeoutSeconds | int | `5` | defines the timeout in seconds for the startup probe |
| doh.pullPolicy | string | `"IfNotPresent"` | Pull policy |
| doh.repository | string | `"ghcr.io/klutchell/dnscrypt-proxy"` | repository (using GHCR) |
| doh.tag | string | `"2.1.15"` | image tag |
| dualStack.enabled | bool | `false` | set this to true to enable creation of DualStack services or creation of separate IPv6 services if `serviceDns.type` is set to `"LoadBalancer"` |
| extraContainers | list | `[]` |  |
| extraEnvVars | object | `{"FTLCONF_dns_listeningMode":"all"}` | extraEnvironmentVars is a list of extra enviroment variables to set for pihole to use. You can use either scalars or project cm, secrets or pod fields via valueFrom |
| extraEnvVarsSecret | object | `{}` | extraEnvVarsSecret is a list of secrets to load in as environment variables. |
| extraInitContainers | list | `[]` | any initContainers you might want to run before starting pihole |
| extraObjects | list | `[]` | any extra kubernetes manifests you might want |
| extraVolumeMounts | object | `{}` | any extra volume mounts you might want |
| extraVolumes | object | `{}` | any extra volumes you might want |
| ftl | object | `{}` | values that should be added to pihole-FTL.conf. You can use either scalars or project cm, secrets or pod fields via valueFrom |
| hostNetwork | string | `"false"` | should the container use host network |
| hostname | string | `""` | hostname of pod |
| image.pullPolicy | string | `"IfNotPresent"` | the pull policy |
| image.repository | string | `"pihole/pihole"` | the repostory to pull the image from |
| image.tag | string | `""` | the docker tag, if left empty it will get it from the chart's appVersion |
| ingress | object | `{"annotations":{},"enabled":false,"hosts":["chart-example.local"],"path":"/","pathType":"ImplementationSpecific","tls":[]}` | Configuration for the Ingress |
| ingress.annotations | object | `{}` | Annotations for the ingress |
| ingress.enabled | bool | `false` | Generate a Ingress resource |
| maxSurge | int | `1` | The maximum number of Pods that can be created over the desired number of `ReplicaSet` during updating. |
| maxUnavailable | int | `1` | The maximum number of Pods that can be unavailable during updating |
| monitoring.podMonitor | object | `{"enabled":false}` | Preferably adding prometheus scrape annotations rather than enabling podMonitor. |
| monitoring.podMonitor.enabled | bool | `false` | set this to true to enable podMonitor |
| monitoring.sidecar | object | `{"enabled":false,"image":{"pullPolicy":"IfNotPresent","repository":"ekofr/pihole-exporter","tag":"v1.0.0"},"port":9617,"resources":{"limits":{"memory":"128Mi"}}}` | Sidecar configuration |
| monitoring.sidecar.enabled | bool | `false` | set this to true to enable podMonitor as sidecar |
| monitoring.sidecar.image.repository | string | `"ekofr/pihole-exporter"` | the repository to use |
| networkPolicy | object | `{"egress":[{"ports":[{"port":53,"protocol":"UDP"},{"port":53,"protocol":"TCP"}]},{"ports":[{"port":80,"protocol":"TCP"},{"port":443,"protocol":"TCP"}]},{"to":[{"namespaceSelector":{}}]}],"enabled":false,"ingress":{"from":[{"namespaceSelector":{}}]}}` | NetworkPolicy configuration |
| networkPolicy.egress | list | `[{"ports":[{"port":53,"protocol":"UDP"},{"port":53,"protocol":"TCP"}]},{"ports":[{"port":80,"protocol":"TCP"},{"port":443,"protocol":"TCP"}]},{"to":[{"namespaceSelector":{}}]}]` | Egress rules (allow DNS and HTTP/HTTPS for upstream resolution and ad list updates) |
| networkPolicy.enabled | bool | `false` | Enable NetworkPolicy |
| networkPolicy.ingress | object | `{"from":[{"namespaceSelector":{}}]}` | Ingress rules configuration |
| networkPolicy.ingress.from | list | `[{"namespaceSelector":{}}]` | Allowed sources for ingress traffic |
| nodeSelector | object | `{}` | Node selector values |
| persistentVolumeClaim | object | `{"accessModes":["ReadWriteOnce"],"annotations":{},"enabled":false,"size":"500Mi"}` | `spec.PersitentVolumeClaim` configuration |
| persistentVolumeClaim.annotations | object | `{}` | Annotations for the `PersitentVolumeClaim` |
| persistentVolumeClaim.enabled | bool | `false` | set to true to use pvc |
| persistentVolumeClaim.size | string | `"500Mi"` | volume claim size |
| podAnnotations | object | `{}` | Additional annotations for pods |
| podDisruptionBudget | object | `{"enabled":false,"minAvailable":1}` | configure a Pod Disruption Budget |
| podDisruptionBudget.enabled | bool | `false` | set to true to enable creating the PDB |
| podDisruptionBudget.minAvailable | int | `1` | minimum number of pods Kubernetes should try to have running at all times |
| podDnsConfig.enabled | bool | `true` |  |
| podDnsConfig.nameservers[0] | string | `"127.0.0.1"` |  |
| podDnsConfig.nameservers[1] | string | `"8.8.8.8"` |  |
| podDnsConfig.policy | string | `"None"` |  |
| podSecurityContext | object | `{}` | Pod-level security context EXPERIMENTAL: These settings are not fully tested with all Pi-hole features! See https://kubernetes.io/docs/tasks/configure-pod-container/security-context/  Pi-hole Docker image limitations: - Requires root at startup for: gravity database, crontab, permissions, setcap - runAsNonRoot, runAsUser, runAsGroup are NOT SUPPORTED - Pi-hole internally drops privileges after initialization |
| privileged | string | `"false"` | should container run in privileged mode @deprecated Use containerSecurityContext.privileged instead |
| probes | object | `{"liveness":{"command":["/bin/sh","-c","curl --silent http://localhost/api/info/login | jq 'if (.dns | not) then halt_error(1) end' && dig cloudflare.com @127.0.0.1"],"enabled":true,"failureThreshold":3,"initialDelaySeconds":0,"periodSeconds":10,"successThreshold":1,"timeoutSeconds":5,"type":"command"},"readiness":{"command":["/bin/sh","-c","curl --silent http://localhost/api/info/login | jq 'if (.dns | not) then halt_error(1) end' && dig cloudflare.com @127.0.0.1"],"enabled":true,"failureThreshold":3,"initialDelaySeconds":0,"periodSeconds":10,"successThreshold":1,"timeoutSeconds":5,"type":"command"},"startup":{"command":["/bin/sh","-c","curl --silent http://localhost/api/info/login | jq 'if (.dns | not) then halt_error(1) end' && dig cloudflare.com @127.0.0.1"],"enabled":true,"failureThreshold":30,"initialDelaySeconds":5,"periodSeconds":5,"timeoutSeconds":5,"type":"command"}}` | Probes configuration |
| probes.liveness.failureThreshold | int | `3` | threshold until the probe is considered failing |
| probes.liveness.initialDelaySeconds | int | `0` | wait time before trying the liveness probe (can be 0 when startup probe is enabled) |
| probes.liveness.periodSeconds | int | `10` | probe interval in seconds |
| probes.liveness.successThreshold | int | `1` | threshold until the probe is considered successful |
| probes.liveness.timeoutSeconds | int | `5` | timeout in seconds |
| probes.liveness.type | string | `"command"` | Generate a liveness probe 'type' defaults to command, can be set to 'httpGet' to use a HTTP GET type liveness probe. |
| probes.readiness.failureThreshold | int | `3` | threshold until the probe is considered failing |
| probes.readiness.initialDelaySeconds | int | `0` | wait time before trying the readiness probe (can be 0 when startup probe is enabled) |
| probes.readiness.periodSeconds | int | `10` | probe interval in seconds |
| probes.readiness.successThreshold | int | `1` | threshold until the probe is considered successful |
| probes.readiness.timeoutSeconds | int | `5` | timeout in seconds |
| probes.readiness.type | string | `"command"` | Generate a readiness probe 'type' defaults to command, can be set to 'httpGet' to use a HTTP GET type readiness probe. |
| probes.startup.failureThreshold | int | `30` | threshold until the container is considered failed (30 * 5s = 150s max startup time) |
| probes.startup.initialDelaySeconds | int | `5` | wait time before trying the startup probe |
| probes.startup.periodSeconds | int | `5` | probe interval in seconds |
| probes.startup.timeoutSeconds | int | `5` | timeout in seconds |
| probes.startup.type | string | `"command"` | Generate a startup probe 'type' defaults to command, can be set to 'httpGet' to use a HTTP GET type startup probe. The startup probe runs before liveness/readiness probes begin. Once it succeeds, liveness and readiness probes take over. |
| regex | object | `{}` | list of denied regex expressions to import during initial start of the container |
| replicaCount | int | `1` | The number of replicas |
| resources | object | `{}` | lines, adjust them as necessary, and remove the curly braces after 'resources:'. |
| revisionHistoryLimit | int | `10` | The number of old ReplicaSets to retain to allow rollback |
| serviceAccount | object | `{"annotations":{},"automountServiceAccountToken":false,"create":true,"name":""}` | ServiceAccount configuration |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| serviceAccount.automountServiceAccountToken | bool | `false` | Automatically mount a ServiceAccount's API credentials |
| serviceAccount.create | bool | `true` | Specifies whether a service account should be created |
| serviceAccount.name | string | `""` | The name of the service account to use. If not set and create is true, a name is generated using the fullname template |
| serviceDhcp | object | `{"annotations":{},"enabled":true,"externalTrafficPolicy":"Local","extraLabels":{},"loadBalancerClass":"","loadBalancerIP":"","loadBalancerIPv6":"","nodePort":"","port":67,"type":"NodePort"}` | Configuration for the DHCP service on port 67 |
| serviceDhcp.annotations | object | `{}` | Annotations for the DHCP service |
| serviceDhcp.enabled | bool | `true` | Generate a Service resource for DHCP traffic |
| serviceDhcp.externalTrafficPolicy | string | `"Local"` | `spec.externalTrafficPolicy` for the DHCP Service |
| serviceDhcp.extraLabels | object | `{}` | Labels for the DHCP service |
| serviceDhcp.loadBalancerClass | string | `""` | `spec.loadBalancerClass` for the DHCP Service. Only used if type is LoadBalancer. |
| serviceDhcp.loadBalancerIP | string | `""` | A fixed `spec.loadBalancerIP` for the DHCP Service. DEPRECATED in Kubernetes 1.24+. Use `annotations` with your cloud provider's annotation instead (e.g., `metallb.universe.tf/loadBalancerIPs` for MetalLB). |
| serviceDhcp.loadBalancerIPv6 | string | `""` | A fixed `spec.loadBalancerIP` for the IPv6 DHCP Service. DEPRECATED in Kubernetes 1.24+. |
| serviceDhcp.nodePort | string | `""` | Optional node port for the DHCP service |
| serviceDhcp.port | int | `67` | The port of the DHCP service |
| serviceDhcp.type | string | `"NodePort"` | `spec.type` for the DHCP Service |
| serviceDns | object | `{"annotations":{},"externalTrafficPolicy":"Local","extraLabels":{},"loadBalancerClass":"","loadBalancerIP":"","loadBalancerIPv6":"","mixedService":false,"nodePort":"","port":53,"type":"NodePort"}` | Configuration for the DNS service on port 53 |
| serviceDns.annotations | object | `{}` | Annotations for the DNS service |
| serviceDns.externalTrafficPolicy | string | `"Local"` | `spec.externalTrafficPolicy` for the DHCP Service |
| serviceDns.extraLabels | object | `{}` | Labels for the DNS service |
| serviceDns.loadBalancerClass | string | `""` | `spec.loadBalancerClass` for the DNS Service. Only used if type is LoadBalancer. |
| serviceDns.loadBalancerIP | string | `""` | A fixed `spec.loadBalancerIP` for the DNS Service. DEPRECATED in Kubernetes 1.24+. Use `annotations` with your cloud provider's annotation instead (e.g., `metallb.universe.tf/loadBalancerIPs` for MetalLB). |
| serviceDns.loadBalancerIPv6 | string | `""` | A fixed `spec.loadBalancerIP` for the IPv6 DNS Service. DEPRECATED in Kubernetes 1.24+. |
| serviceDns.mixedService | bool | `false` | deploys a mixed (TCP + UDP) Service instead of separate ones |
| serviceDns.nodePort | string | `""` | Optional node port for the DNS service |
| serviceDns.port | int | `53` | The port of the DNS service |
| serviceDns.type | string | `"NodePort"` | `spec.type` for the DNS Service |
| serviceWeb | object | `{"annotations":{},"externalTrafficPolicy":"Local","extraLabels":{},"http":{"enabled":true,"nodePort":"","port":80},"https":{"enabled":true,"nodePort":"","port":443},"loadBalancerClass":"","loadBalancerIP":"","loadBalancerIPv6":"","type":"ClusterIP"}` | Configuration for the web interface service |
| serviceWeb.annotations | object | `{}` | Annotations for the DHCP service |
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
| serviceWeb.loadBalancerIPv6 | string | `""` | A fixed `spec.loadBalancerIP` for the IPv6 web interface Service. DEPRECATED in Kubernetes 1.24+. |
| serviceWeb.type | string | `"ClusterIP"` | `spec.type` for the web interface Service |
| strategyType | string | `"RollingUpdate"` | The `spec.strategyTpye` for updates |
| tolerations | list | `[]` | Toleration |
| topologySpreadConstraints | list | `[]` | Specify a priorityClassName priorityClassName: "" Reference: https://kubernetes.io/docs/concepts/workloads/pods/pod-topology-spread-constraints/ |
| virtualHost | string | `"pi.hole"` |  |
| webHttp | string | `"80"` | port the container should use to expose HTTP traffic |
| webHttps | string | `"443"` | port the container should use to expose HTTPS traffic |

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| MoJo2600 | <christian.erhardt@mojo2k.de> |  |

## Remarks

### MetalLB 0.8.1+

pihole seems to work without issue in MetalLB 0.8.1+

### MetalLB 0.7.3

MetalLB 0.7.3 has a bug, where the service is not announced anymore, when the pod changes (e.g. update of a deployment). My workaround is to restart the `metallb-speaker-*` pods.

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
      <td align="center" valign="top" width="14.28%"><a href="http://www.mojo2k.de"><img src="https://avatars1.githubusercontent.com/u/2462817?v=4" width="100px;" alt=""/><br /><sub><b>Christian Erhardt</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://billimek.com/"><img src="https://avatars0.githubusercontent.com/u/6393612?v=4" width="100px;" alt=""/><br /><sub><b>Jeff Billimek</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/imle"><img src="https://avatars3.githubusercontent.com/u/4809109?v=4" width="100px;" alt=""/><br /><sub><b>Steven Imle</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jetersen"><img src="https://avatars2.githubusercontent.com/u/1661688?v=4" width="100px;" alt=""/><br /><sub><b>Joseph Petersen</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/SiM22"><img src="https://avatars2.githubusercontent.com/u/5759618?v=4" width="100px;" alt=""/><br /><sub><b>Simon Garcia</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/AndyG-0"><img src="https://avatars1.githubusercontent.com/u/29743443?v=4" width="100px;" alt=""/><br /><sub><b>Andy Gilbreath</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/northerngit"><img src="https://avatars0.githubusercontent.com/u/4513272?v=4" width="100px;" alt=""/><br /><sub><b>James Wilson</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/jskswamy"><img src="https://avatars2.githubusercontent.com/u/232449?v=4" width="100px;" alt=""/><br /><sub><b>Krishnaswamy Subramanian</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/luqasn"><img src="https://avatars2.githubusercontent.com/u/274902?v=4" width="100px;" alt=""/><br /><sub><b>Lucas Romero</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/konturn"><img src="https://avatars0.githubusercontent.com/u/35545508?v=4" width="100px;" alt=""/><br /><sub><b>konturn</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tdorsey"><img src="https://avatars3.githubusercontent.com/u/1218404?v=4" width="100px;" alt=""/><br /><sub><b>tdorsey</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/alesz"><img src="https://avatars0.githubusercontent.com/u/12436980?v=4" width="100px;" alt=""/><br /><sub><b>Ales Zelenik</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dtourde"><img src="https://avatars1.githubusercontent.com/u/49169262?v=4" width="100px;" alt=""/><br /><sub><b>Damien TOURDE</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/putz612"><img src="https://avatars3.githubusercontent.com/u/952758?v=4" width="100px;" alt=""/><br /><sub><b>Jason Sievert</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/joshua-nord"><img src="https://avatars2.githubusercontent.com/u/1181300?v=4" width="100px;" alt=""/><br /><sub><b>joshua-nord</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://maximilianbo.de/"><img src="https://avatars3.githubusercontent.com/u/9051309?v=4" width="100px;" alt=""/><br /><sub><b>Maximilian Bode</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/raackley"><img src="https://avatars0.githubusercontent.com/u/1700688?v=4" width="100px;" alt=""/><br /><sub><b>raackley</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/StoicPerlman"><img src="https://avatars1.githubusercontent.com/u/3152359?v=4" width="100px;" alt=""/><br /><sub><b>Sam Kleiner</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://arpankapoor.com/"><img src="https://avatars3.githubusercontent.com/u/3677810?v=4" width="100px;" alt=""/><br /><sub><b>Arpan Kapoor</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/chrodriguez"><img src="https://avatars1.githubusercontent.com/u/1460882?v=4" width="100px;" alt=""/><br /><sub><b>Christian Rodriguez</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://dave-cahill.com/"><img src="https://avatars0.githubusercontent.com/u/361096?v=4" width="100px;" alt=""/><br /><sub><b>Dave Cahill</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/golgoth31"><img src="https://avatars2.githubusercontent.com/u/5741421?v=4" width="100px;" alt=""/><br /><sub><b>golgoth31</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://greg.jeanmart.me/"><img src="https://avatars3.githubusercontent.com/u/506784?v=4" width="100px;" alt=""/><br /><sub><b>Greg Jeanmart</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ballj"><img src="https://avatars1.githubusercontent.com/u/38097813?v=4" width="100px;" alt=""/><br /><sub><b>Joseph Ball</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://www.oneko.org/"><img src="https://avatars2.githubusercontent.com/u/4233214?v=4" width="100px;" alt=""/><br /><sub><b>Karlos</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dza89"><img src="https://avatars0.githubusercontent.com/u/20373984?v=4" width="100px;" alt=""/><br /><sub><b>dza89</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mikewhitley"><img src="https://avatars0.githubusercontent.com/u/52802633?v=4" width="100px;" alt=""/><br /><sub><b>mikewhitley</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Vashiru"><img src="https://avatars2.githubusercontent.com/u/11370057?v=4" width="100px;" alt=""/><br /><sub><b>Vashiru</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/sam-kleiner"><img src="https://avatars.githubusercontent.com/u/63059772?v=4" width="100px;" alt=""/><br /><sub><b>sam-kleiner</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.linkedin.com/in/alexgorbatchev/"><img src="https://avatars.githubusercontent.com/u/65633?v=4" width="100px;" alt=""/><br /><sub><b>Alex Gorbatchev</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/c-yco"><img src="https://avatars.githubusercontent.com/u/355591?v=4" width="100px;" alt=""/><br /><sub><b>Alexander Rabenstein</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://tibbon.com/"><img src="https://avatars.githubusercontent.com/u/82880?v=4" width="100px;" alt=""/><br /><sub><b>David Fisher</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/utkuozdemir"><img src="https://avatars.githubusercontent.com/u/1465819?v=4" width="100px;" alt=""/><br /><sub><b>Utku Özdemir</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://mor.re/"><img src="https://avatars.githubusercontent.com/u/7683567?v=4" width="100px;" alt=""/><br /><sub><b>Morre Meyer</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/johnsondnz"><img src="https://avatars.githubusercontent.com/u/7608966?v=4" width="100px;" alt=""/><br /><sub><b>Donald Johnson</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://winston.milli.ng/"><img src="https://avatars.githubusercontent.com/u/6162814?v=4" width="100px;" alt=""/><br /><sub><b>Winston R. Milling</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/larivierec"><img src="https://avatars.githubusercontent.com/u/3633214?v=4" width="100px;" alt=""/><br /><sub><b>Christopher Larivière</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://sievenpiper.co/"><img src="https://avatars.githubusercontent.com/u/1131882?v=4" width="100px;" alt=""/><br /><sub><b>Justin Sievenpiper</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/beastob"><img src="https://avatars.githubusercontent.com/u/76816315?v=4" width="100px;" alt=""/><br /><sub><b>beastob</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://niftyside.io/"><img src="https://avatars.githubusercontent.com/u/653739?v=4" width="100px;" alt=""/><br /><sub><b>Daniel Mühlbachler-Pietrzykowski</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/consideRatio"><img src="https://avatars.githubusercontent.com/u/3837114?v=4" width="100px;" alt=""/><br /><sub><b>Erik Sundell</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Ornias1993"><img src="https://avatars.githubusercontent.com/u/7613738?v=4" width="100px;" alt=""/><br /><sub><b>Kjeld Schouten-Lebbing</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mrwulf"><img src="https://avatars.githubusercontent.com/u/2494769?v=4" width="100px;" alt=""/><br /><sub><b>Brandon Wulf</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/DerRockWolf"><img src="https://avatars.githubusercontent.com/u/50499906?v=4" width="100px;" alt=""/><br /><sub><b>DerRockWolf</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/brnl"><img src="https://avatars.githubusercontent.com/u/3243133?v=4" width="100px;" alt=""/><br /><sub><b>brnl</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://rafaelgaspar.xyz/"><img src="https://avatars.githubusercontent.com/u/5567?v=4" width="100px;" alt=""/><br /><sub><b>Rafael Gaspar</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://chadimasri.com/"><img src="https://avatars.githubusercontent.com/u/1502811?v=4" width="100px;" alt=""/><br /><sub><b>Chadi El Masri</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dfoulkes"><img src="https://avatars.githubusercontent.com/u/8113674?v=4" width="100px;" alt=""/><br /><sub><b>Dan Foulkes</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/george124816"><img src="https://avatars.githubusercontent.com/u/26443736?v=4" width="100px;" alt=""/><br /><sub><b>George Rodrigues</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://pascaliske.dev/"><img src="https://avatars.githubusercontent.com/u/7473880?v=4" width="100px;" alt=""/><br /><sub><b>Pascal Iske</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.reyth.dev/"><img src="https://avatars.githubusercontent.com/u/23526880?v=4" width="100px;" alt=""/><br /><sub><b>Theo REY</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/piwi3910"><img src="https://avatars.githubusercontent.com/u/12539757?v=4" width="100px;" alt=""/><br /><sub><b>Watteel Pascal</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/frittenlab"><img src="https://avatars.githubusercontent.com/u/29921946?v=4" width="100px;" alt=""/><br /><sub><b>simon</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/vince-vibin"><img src="https://avatars.githubusercontent.com/u/99386370?v=4" width="100px;" alt=""/><br /><sub><b>Vincent</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Keydrain"><img src="https://avatars.githubusercontent.com/u/5723055?v=4" width="100px;" alt=""/><br /><sub><b>Clint</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/tamcore"><img src="https://avatars.githubusercontent.com/u/319917?v=4" width="100px;" alt=""/><br /><sub><b>Philipp B.</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ebCrypto"><img src="https://avatars.githubusercontent.com/u/44279886?v=4" width="100px;" alt=""/><br /><sub><b>ebCrypto</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://ucdialplans.com/"><img src="https://avatars.githubusercontent.com/u/44060527?v=4" width="100px;" alt=""/><br /><sub><b>Ken Lasko</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mbund"><img src="https://avatars.githubusercontent.com/u/25110595?v=4" width="100px;" alt=""/><br /><sub><b>Mark Bundschuh</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://fotoallerlei.com/"><img src="https://avatars.githubusercontent.com/u/3430656?v=4" width="100px;" alt=""/><br /><sub><b>Max Rosin</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/yzeng1314"><img src="https://avatars.githubusercontent.com/u/6365365?v=4" width="100px;" alt=""/><br /><sub><b>Yang</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/dwarf-king-hreidmar"><img src="https://avatars.githubusercontent.com/u/45319558?v=4" width="100px;" alt=""/><br /><sub><b>dwarf-king-hreidmar</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/s94santos"><img src="https://avatars.githubusercontent.com/u/10950164?v=4" width="100px;" alt=""/><br /><sub><b>s94santos</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/adamrdavid"><img src="https://avatars.githubusercontent.com/u/1854876?v=4" width="100px;" alt=""/><br /><sub><b>Adam David</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/bkonicek"><img src="https://avatars.githubusercontent.com/u/7397530?v=4" width="100px;" alt=""/><br /><sub><b>Ben Konicek</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Gabisonfire"><img src="https://avatars.githubusercontent.com/u/6416239?v=4" width="100px;" alt=""/><br /><sub><b>Gabisonfire</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/giolekva"><img src="https://avatars.githubusercontent.com/u/124899?v=4" width="100px;" alt=""/><br /><sub><b>Giorgi Lekveishvili</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/paimonsoror"><img src="https://avatars.githubusercontent.com/u/935046?v=4" width="100px;" alt=""/><br /><sub><b>Paimon Sorornejad</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mivek"><img src="https://avatars.githubusercontent.com/u/9912558?v=4" width="100px;" alt=""/><br /><sub><b>Jean-Kevin KPADEY</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/aogier"><img src="https://avatars.githubusercontent.com/u/321364?v=4" width="100px;" alt=""/><br /><sub><b>Alessandro Ogier</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Luukvdm"><img src="https://avatars.githubusercontent.com/u/25098818?v=4" width="100px;" alt=""/><br /><sub><b>Luuk v/d Maagdenberg</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/sunsided"><img src="https://avatars.githubusercontent.com/u/495335?v=4" width="100px;" alt=""/><br /><sub><b>Markus Mayer</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/prfj"><img src="https://avatars.githubusercontent.com/u/37109548?v=4" width="100px;" alt=""/><br /><sub><b>Paulo Jesus</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://blog.bergpb.dev/"><img src="https://avatars.githubusercontent.com/u/11005963?v=4" width="100px;" alt=""/><br /><sub><b>Lindemberg Barbosa</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://ricardobaltazar.com/"><img src="https://avatars.githubusercontent.com/u/1923140?v=4" width="100px;" alt=""/><br /><sub><b>Ricardo Baltazar Chaves</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/wolviecb"><img src="https://avatars.githubusercontent.com/u/13783824?v=4" width="100px;" alt=""/><br /><sub><b>Thomas Andrade</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/alexinthesky"><img src="https://avatars.githubusercontent.com/u/14876221?v=4" width="100px;" alt=""/><br /><sub><b>Alexandre Chappaz</b></sub></a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/cristiklein"><img src="https://avatars.githubusercontent.com/u/1660833?v=4" width="100px;" alt=""/><br /><sub><b>Cristian Klein</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://flouret.com/"><img src="https://avatars.githubusercontent.com/u/9397098?v=4" width="100px;" alt=""/><br /><sub><b>JP Flouret</b></sub></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/fernferret"><img src="https://avatars.githubusercontent.com/u/72811?v=4" width="100px;" alt=""/><br /><sub><b>Eric</b></sub></a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.14.2](https://github.com/norwoodj/helm-docs/releases/v1.14.2)
