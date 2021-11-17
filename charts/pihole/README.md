# pihole

Installs pihole in kubernetes

![Version: 2.4.0](https://img.shields.io/badge/Version-2.4.0-informational?style=flat-square) <!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-27-blue.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## Source Code

* <https://github.com/MoJo2600/pihole-kubernetes/tree/master/charts/pihole>
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
- **LoadBalancer**: Exposes the service externally using a cloud provider’s load balancer.

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
| admin | object | `{"existingSecret":"","passwordKey":"password"}` | Use an existing secret for the admin password. |
| admin.existingSecret | string | `""` | Specify an existing secret to use as admin password |
| admin.passwordKey | string | `"password"` | Specify the key inside the secret to use |
| adminPassword | string | `"admin"` | Administrator password when not using an existing secret (see below) |
| affinity | object | `{}` |  |
| antiaff.avoidRelease | string | `"pihole1"` | Here you can set the pihole release (you set in `helm install <releasename> ...`) you want to avoid |
| antiaff.enabled | bool | `false` | set to true to enable antiaffinity (example: 2 pihole DNS in the same cluster) |
| antiaff.strict | bool | `true` | Here you can choose between preferred or required |
| blacklist | object | `{}` | list of blacklisted domains to import during initial start of the container |
| customVolumes.config | object | `{}` | any volume type can be used here |
| customVolumes.enabled | bool | `false` | set this to true to enable custom volumes |
| dnsHostPort.enabled | bool | `false` | set this to true to enable dnsHostPort |
| dnsHostPort.port | int | `53` | default port for this pod |
| dnsmasq.additionalHostsEntries | list | `[]` | Dnsmasq reads the /etc/hosts file to resolve ips. You can add additional entries if you like |
| dnsmasq.customCnameEntries | list | `[]` | Here we specify custom cname entries that should point to `A` records or elements in customDnsEntries array. The format should be:  - cname=cname.foo.bar,foo.bar  - cname=cname.bar.foo,bar.foo  - cname=cname record,dns record |
| dnsmasq.customDnsEntries | list | `[]` | Add custom dns entries to override the dns resolution. All lines will be added to the pihole dnsmasq configuration. |
| dnsmasq.customSettings | string | `nil` | Other options |
| dnsmasq.staticDhcpEntries | list | `[]` | Static DHCP config |
| dnsmasq.upstreamServers | list | `[]` | Add upstream dns servers. All lines will be added to the pihole dnsmasq configuration |
| doh.enabled | bool | `false` | set to true to enabled DNS over HTTPs via cloudflared |
| doh.envVars | object | `{}` | Here you can pass environment variables to the DoH container, for example: |
| doh.name | string | `"cloudflared"` |  |
| doh.probes | object | `{"liveness":{"enabled":true,"failureThreshold":10,"initialDelaySeconds":60,"timeoutSeconds":5}}` | Probes configuration |
| doh.probes.liveness | object | `{"enabled":true,"failureThreshold":10,"initialDelaySeconds":60,"timeoutSeconds":5}` | Configure the healthcheck for the doh container |
| doh.probes.liveness.enabled | bool | `true` | set to true to enable liveness probe |
| doh.probes.liveness.failureThreshold | int | `10` | defines the failure threshold for the liveness probe |
| doh.probes.liveness.initialDelaySeconds | int | `60` | defines the initial delay for the liveness probe |
| doh.probes.liveness.timeoutSeconds | int | `5` | defines the timeout in secondes for the liveness probe |
| doh.pullPolicy | string | `"IfNotPresent"` |  |
| doh.repository | string | `"crazymax/cloudflared"` |  |
| doh.tag | string | `"latest"` |  |
| dualStack.enabled | bool | `false` | set this to true to enable creation of DualStack services or creation of separate IPv6 services if `serviceDns.type` is set to `"LoadBalancer"` |
| extraEnvVars | object | `{}` | extraEnvironmentVars is a list of extra enviroment variables to set for pihole to use |
| extraEnvVarsSecret | object | `{}` | extraEnvVarsSecret is a list of secrets to load in as environment variables. |
| ftl | object | `{}` | values that should be added to pihole-FTL.conf |
| hostNetwork | string | `"false"` | should the container use host network |
| hostname | string | `""` | hostname of pod |
| image.pullPolicy | string | `"IfNotPresent"` | the pull policy |
| image.repository | string | `"pihole/pihole"` | the repostory to pull the image from |
| image.tag | string | `""` | the docker tag, if left empty it will get it from the chart's appVersion |
| ingress | object | `{"annotations":{},"enabled":false,"hosts":["chart-example.local"],"path":"/","tls":[]}` | Configuration for the Ingress |
| ingress.annotations | object | `{}` | Annotations for the ingress |
| ingress.enabled | bool | `false` | Generate a Ingress resource |
| maxSurge | int | `1` | The maximum number of Pods that can be created over the desired number of `ReplicaSet` during updating. |
| maxUnavailable | int | `1` | The maximum number of Pods that can be unavailable during updating |
| monitoring.podMonitor | object | `{"enabled":false}` | Preferably adding prometheus scrape annotations rather than enabling podMonitor. |
| monitoring.podMonitor.enabled | bool | `false` | set this to true to enable podMonitor |
| monitoring.sidecar | object | `{"enabled":false,"image":{"pullPolicy":"IfNotPresent","repository":"ekofr/pihole-exporter","tag":"0.0.10"},"port":9617,"resources":{"limits":{"memory":"128Mi"}}}` | Sidecar configuration |
| monitoring.sidecar.enabled | bool | `false` | set this to true to enable podMonitor as sidecar |
| nodeSelector | object | `{}` |  |
| persistentVolumeClaim | object | `{"accessModes":["ReadWriteOnce"],"annotations":{},"enabled":false,"size":"500Mi"}` | `spec.PersitentVolumeClaim` configuration |
| persistentVolumeClaim.annotations | object | `{}` | specify an existing `PersistentVolumeClaim` to use existingClaim: "" -- Annotations for the `PersitentVolumeClaim` |
| persistentVolumeClaim.enabled | bool | `false` | set to true to use pvc |
| podAnnotations | object | `{}` | Additional annotations for pods |
| podDnsConfig.enabled | bool | `true` |  |
| podDnsConfig.nameservers[0] | string | `"127.0.0.1"` |  |
| podDnsConfig.nameservers[1] | string | `"8.8.8.8"` |  |
| podDnsConfig.policy | string | `"None"` |  |
| privileged | string | `"false"` | should container run in privileged mode |
| probes | object | `{"liveness":{"enabled":true,"failureThreshold":10,"initialDelaySeconds":60,"timeoutSeconds":5},"readiness":{"enabled":true,"failureThreshold":3,"initialDelaySeconds":60,"timeoutSeconds":5}}` | Probes configuration |
| probes.liveness.enabled | bool | `true` | Generate a liveness probe |
| probes.readiness.enabled | bool | `true` | Generate a readiness probe |
| regex | object | `{}` | list of blacklisted regex expressions to import during initial start of the container |
| replicaCount | int | `1` | The number of replicas |
| resources | object | `{}` | We usually recommend not to specify default resources and to leave this as a conscious -- choice for the user. This also increases chances charts run on environments with little -- resources, such as Minikube. If you do want to specify resources, uncomment the following -- lines, adjust them as necessary, and remove the curly braces after 'resources:'. |
| serviceDhcp | object | `{"annotations":{},"enabled":true,"externalTrafficPolicy":"Local","loadBalancerIP":"","loadBalancerIPv6":"","type":"NodePort"}` | Configuration for the DHCP service on port 67 |
| serviceDhcp.annotations | object | `{}` | Annotations for the DHCP service |
| serviceDhcp.enabled | bool | `true` | Generate a Service resource for DHCP traffic |
| serviceDhcp.externalTrafficPolicy | string | `"Local"` | `spec.externalTrafficPolicy` for the DHCP Service |
| serviceDhcp.loadBalancerIP | string | `""` | A fixed `spec.loadBalancerIP` for the DHCP Service |
| serviceDhcp.loadBalancerIPv6 | string | `""` | A fixed `spec.loadBalancerIP` for the IPv6 DHCP Service |
| serviceDhcp.type | string | `"NodePort"` | `spec.type` for the DHCP Service |
| serviceDns | object | `{"annotations":{},"externalTrafficPolicy":"Local","loadBalancerIP":"","loadBalancerIPv6":"","mixedService":false,"port":53,"type":"NodePort"}` | Configuration for the DNS service on port 53 |
| serviceDns.annotations | object | `{}` | Annotations for the DNS service |
| serviceDns.externalTrafficPolicy | string | `"Local"` | `spec.externalTrafficPolicy` for the DHCP Service |
| serviceDns.loadBalancerIP | string | `""` | A fixed `spec.loadBalancerIP` for the DNS Service |
| serviceDns.loadBalancerIPv6 | string | `""` | A fixed `spec.loadBalancerIP` for the IPv6 DNS Service |
| serviceDns.mixedService | bool | `false` | deploys a mixed (TCP + UDP) Service instead of separate ones |
| serviceDns.port | int | `53` | The port of the DNS service |
| serviceDns.type | string | `"NodePort"` | `spec.type` for the DNS Service |
| serviceWeb | object | `{"annotations":{},"externalTrafficPolicy":"Local","http":{"enabled":true,"port":80},"https":{"enabled":true,"port":443},"loadBalancerIP":"","loadBalancerIPv6":"","type":"ClusterIP"}` | Configuration for the web interface service |
| serviceWeb.annotations | object | `{}` | Annotations for the DHCP service |
| serviceWeb.externalTrafficPolicy | string | `"Local"` | `spec.externalTrafficPolicy` for the web interface Service |
| serviceWeb.http | object | `{"enabled":true,"port":80}` | Configuration for the HTTP web interface listener |
| serviceWeb.http.enabled | bool | `true` | Generate a service for HTTP traffic |
| serviceWeb.http.port | int | `80` | The port of the web HTTP service |
| serviceWeb.https | object | `{"enabled":true,"port":443}` | Configuration for the HTTPS web interface listener |
| serviceWeb.https.enabled | bool | `true` | Generate a service for HTTPS traffic |
| serviceWeb.https.port | int | `443` | The port of the web HTTPS service |
| serviceWeb.loadBalancerIP | string | `""` | A fixed `spec.loadBalancerIP` for the web interface Service |
| serviceWeb.loadBalancerIPv6 | string | `""` | A fixed `spec.loadBalancerIP` for the IPv6 web interface Service |
| serviceWeb.type | string | `"ClusterIP"` | `spec.type` for the web interface Service |
| strategyType | string | `"RollingUpdate"` | The `spec.strategyTpye` for updates |
| tolerations | list | `[]` |  |
| topologySpreadConstraints | list | `[]` |  |
| virtualHost | string | `"pi.hole"` |  |
| webHttp | string | `"80"` | port the container should use to expose HTTP traffic |
| webHttps | string | `"443"` | port the container should use to expose HTTPS traffic |
| whitelist | object | `{}` | list of whitelisted domains to import during initial start of the container |

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| MoJo2600 | christian.erhardt@mojo2k.de |  |

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
  <tr>
    <td align="center"><a href="http://www.mojo2k.de"><img src="https://avatars1.githubusercontent.com/u/2462817?v=4" width="100px;" alt=""/><br /><sub><b>Christian Erhardt</b></sub></a></td>
    <td align="center"><a href="https://billimek.com/"><img src="https://avatars0.githubusercontent.com/u/6393612?v=4" width="100px;" alt=""/><br /><sub><b>Jeff Billimek</b></sub></a></td>
    <td align="center"><a href="https://github.com/imle"><img src="https://avatars3.githubusercontent.com/u/4809109?v=4" width="100px;" alt=""/><br /><sub><b>Steven Imle</b></sub></a></td>
    <td align="center"><a href="https://github.com/jetersen"><img src="https://avatars2.githubusercontent.com/u/1661688?v=4" width="100px;" alt=""/><br /><sub><b>Joseph Petersen</b></sub></a></td>
    <td align="center"><a href="https://github.com/SiM22"><img src="https://avatars2.githubusercontent.com/u/5759618?v=4" width="100px;" alt=""/><br /><sub><b>Simon Garcia</b></sub></a></td>
    <td align="center"><a href="https://github.com/AndyG-0"><img src="https://avatars1.githubusercontent.com/u/29743443?v=4" width="100px;" alt=""/><br /><sub><b>Andy Gilbreath</b></sub></a></td>
    <td align="center"><a href="https://github.com/northerngit"><img src="https://avatars0.githubusercontent.com/u/4513272?v=4" width="100px;" alt=""/><br /><sub><b>James Wilson</b></sub></a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/jskswamy"><img src="https://avatars2.githubusercontent.com/u/232449?v=4" width="100px;" alt=""/><br /><sub><b>Krishnaswamy Subramanian</b></sub></a></td>
    <td align="center"><a href="https://github.com/luqasn"><img src="https://avatars2.githubusercontent.com/u/274902?v=4" width="100px;" alt=""/><br /><sub><b>Lucas Romero</b></sub></a></td>
    <td align="center"><a href="https://github.com/konturn"><img src="https://avatars0.githubusercontent.com/u/35545508?v=4" width="100px;" alt=""/><br /><sub><b>konturn</b></sub></a></td>
    <td align="center"><a href="https://github.com/tdorsey"><img src="https://avatars3.githubusercontent.com/u/1218404?v=4" width="100px;" alt=""/><br /><sub><b>tdorsey</b></sub></a></td>
    <td align="center"><a href="https://github.com/alesz"><img src="https://avatars0.githubusercontent.com/u/12436980?v=4" width="100px;" alt=""/><br /><sub><b>Ales Zelenik</b></sub></a></td>
    <td align="center"><a href="https://github.com/dtourde"><img src="https://avatars1.githubusercontent.com/u/49169262?v=4" width="100px;" alt=""/><br /><sub><b>Damien TOURDE</b></sub></a></td>
    <td align="center"><a href="https://github.com/putz612"><img src="https://avatars3.githubusercontent.com/u/952758?v=4" width="100px;" alt=""/><br /><sub><b>Jason Sievert</b></sub></a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/joshua-nord"><img src="https://avatars2.githubusercontent.com/u/1181300?v=4" width="100px;" alt=""/><br /><sub><b>joshua-nord</b></sub></a></td>
    <td align="center"><a href="https://maximilianbo.de/"><img src="https://avatars3.githubusercontent.com/u/9051309?v=4" width="100px;" alt=""/><br /><sub><b>Maximilian Bode</b></sub></a></td>
    <td align="center"><a href="https://github.com/raackley"><img src="https://avatars0.githubusercontent.com/u/1700688?v=4" width="100px;" alt=""/><br /><sub><b>raackley</b></sub></a></td>
    <td align="center"><a href="https://github.com/StoicPerlman"><img src="https://avatars1.githubusercontent.com/u/3152359?v=4" width="100px;" alt=""/><br /><sub><b>Sam Kleiner</b></sub></a></td>
    <td align="center"><a href="https://arpankapoor.com/"><img src="https://avatars3.githubusercontent.com/u/3677810?v=4" width="100px;" alt=""/><br /><sub><b>Arpan Kapoor</b></sub></a></td>
    <td align="center"><a href="https://github.com/chrodriguez"><img src="https://avatars1.githubusercontent.com/u/1460882?v=4" width="100px;" alt=""/><br /><sub><b>Christian Rodriguez</b></sub></a></td>
    <td align="center"><a href="http://dave-cahill.com/"><img src="https://avatars0.githubusercontent.com/u/361096?v=4" width="100px;" alt=""/><br /><sub><b>Dave Cahill</b></sub></a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/golgoth31"><img src="https://avatars2.githubusercontent.com/u/5741421?v=4" width="100px;" alt=""/><br /><sub><b>golgoth31</b></sub></a></td>
    <td align="center"><a href="https://greg.jeanmart.me/"><img src="https://avatars3.githubusercontent.com/u/506784?v=4" width="100px;" alt=""/><br /><sub><b>Greg Jeanmart</b></sub></a></td>
    <td align="center"><a href="https://github.com/ballj"><img src="https://avatars1.githubusercontent.com/u/38097813?v=4" width="100px;" alt=""/><br /><sub><b>Joseph Ball</b></sub></a></td>
    <td align="center"><a href="http://www.oneko.org/"><img src="https://avatars2.githubusercontent.com/u/4233214?v=4" width="100px;" alt=""/><br /><sub><b>Karlos</b></sub></a></td>
    <td align="center"><a href="https://github.com/dza89"><img src="https://avatars0.githubusercontent.com/u/20373984?v=4" width="100px;" alt=""/><br /><sub><b>dza89</b></sub></a></td>
    <td align="center"><a href="https://github.com/mikewhitley"><img src="https://avatars0.githubusercontent.com/u/52802633?v=4" width="100px;" alt=""/><br /><sub><b>mikewhitley</b></sub></a></td>
    <td align="center"><a href="https://github.com/Vashiru"><img src="https://avatars2.githubusercontent.com/u/11370057?v=4" width="100px;" alt=""/><br /><sub><b>Vashiru</b></sub></a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/sam-kleiner"><img src="https://avatars.githubusercontent.com/u/63059772?v=4" width="100px;" alt=""/><br /><sub><b>sam-kleiner</b></sub></a></td>
    <td align="center"><a href="https://www.linkedin.com/in/alexgorbatchev/"><img src="https://avatars.githubusercontent.com/u/65633?v=4" width="100px;" alt=""/><br /><sub><b>Alex Gorbatchev</b></sub></a></td>
    <td align="center"><a href="https://github.com/c-yco"><img src="https://avatars.githubusercontent.com/u/355591?v=4" width="100px;" alt=""/><br /><sub><b>Alexander Rabenstein</b></sub></a></td>
    <td align="center"><a href="http://tibbon.com/"><img src="https://avatars.githubusercontent.com/u/82880?v=4" width="100px;" alt=""/><br /><sub><b>David Fisher</b></sub></a></td>
    <td align="center"><a href="https://github.com/utkuozdemir"><img src="https://avatars.githubusercontent.com/u/1465819?v=4" width="100px;" alt=""/><br /><sub><b>Utku Özdemir</b></sub></a></td>
    <td align="center"><a href="https://mor.re/"><img src="https://avatars.githubusercontent.com/u/7683567?v=4" width="100px;" alt=""/><br /><sub><b>Morre Meyer</b></sub></a></td>
    <td align="center"><a href="https://github.com/johnsondnz"><img src="https://avatars.githubusercontent.com/u/7608966?v=4" width="100px;" alt=""/><br /><sub><b>Donald Johnson</b></sub></a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://winston.milli.ng/"><img src="https://avatars.githubusercontent.com/u/6162814?v=4" width="100px;" alt=""/><br /><sub><b>Winston R. Milling</b></sub></a></td>
    <td align="center"><a href="https://github.com/larivierec"><img src="https://avatars.githubusercontent.com/u/3633214?v=4" width="100px;" alt=""/><br /><sub><b>Christopher Larivière</b></sub></a></td>
    <td align="center"><a href="https://sievenpiper.co/"><img src="https://avatars.githubusercontent.com/u/1131882?v=4" width="100px;" alt=""/><br /><sub><b>Justin Sievenpiper</b></sub></a></td>
    <td align="center"><a href="https://github.com/beastob"><img src="https://avatars.githubusercontent.com/u/76816315?v=4" width="100px;" alt=""/><br /><sub><b>beastob</b></sub></a></td>
    <td align="center"><a href="https://niftyside.io/"><img src="https://avatars.githubusercontent.com/u/653739?v=4" width="100px;" alt=""/><br /><sub><b>Daniel Mühlbachler-Pietrzykowski</b></sub></a></td>
    <td align="center"><a href="https://github.com/consideRatio"><img src="https://avatars.githubusercontent.com/u/3837114?v=4" width="100px;" alt=""/><br /><sub><b>Erik Sundell</b></sub></a></td>
    <td align="center"><a href="https://github.com/Ornias1993"><img src="https://avatars.githubusercontent.com/u/7613738?v=4" width="100px;" alt=""/><br /><sub><b>Kjeld Schouten-Lebbing</b></sub></a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.5.0](https://github.com/norwoodj/helm-docs/releases/v1.5.0)
