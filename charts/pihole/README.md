# pihole

Installs pihole in kubernetes

![Version: 1.8.25](https://img.shields.io/badge/Version-1.8.25-informational?style=flat-square) ![AppVersion: 5.2.1](https://img.shields.io/badge/AppVersion-5.2.1-informational?style=flat-square)
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)
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

## Upgrading

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
| DNS1 | string | `"8.8.8.8"` |  |
| DNS2 | string | `"8.8.4.4"` |  |
| adlists | object | `{}` |  |
| admin.existingSecret | string | `""` |  |
| admin.passwordKey | string | `"password"` |  |
| adminPassword | string | `"admin"` |  |
| affinity | object | `{}` |  |
| antiaff.avoidRelease | string | `"pihole1"` |  |
| antiaff.enabled | bool | `false` |  |
| antiaff.strict | bool | `true` |  |
| blacklist | object | `{}` |  |
| customVolumes.config | object | `{}` |  |
| customVolumes.enabled | bool | `false` |  |
| dnsmasq.additionalHostsEntries | list | `[]` |  |
| dnsmasq.customDnsEntries | list | `[]` |  |
| dnsmasq.staticDhcpEntries | list | `[]` |  |
| dnsmasq.upstreamServers | list | `[]` |  |
| doh.enabled | bool | `false` |  |
| doh.envVars | object | `{}` |  |
| doh.name | string | `"cloudflared"` |  |
| doh.probes.liveness.enabled | bool | `true` |  |
| doh.probes.liveness.failureThreshold | int | `10` |  |
| doh.probes.liveness.initialDelaySeconds | int | `60` |  |
| doh.probes.liveness.timeoutSeconds | int | `5` |  |
| doh.pullPolicy | string | `"IfNotPresent"` |  |
| doh.repository | string | `"crazymax/cloudflared"` |  |
| doh.tag | string | `"latest"` |  |
| extraEnvVars | object | `{}` |  |
| extraEnvVarsSecret | object | `{}` |  |
| hostNetwork | string | `"false"` |  |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository | string | `"pihole/pihole"` |  |
| image.tag | string | `"v5.2.1"` |  |
| ingress.annotations | object | `{}` |  |
| ingress.enabled | bool | `false` |  |
| ingress.hosts[0] | string | `"chart-example.local"` |  |
| ingress.path | string | `"/"` |  |
| ingress.tls | list | `[]` |  |
| monitoring.podMonitor.enabled | bool | `false` |  |
| monitoring.sidecar.enabled | bool | `false` |  |
| monitoring.sidecar.image.pullPolicy | string | `"IfNotPresent"` |  |
| monitoring.sidecar.image.repository | string | `"ekofr/pihole-exporter"` |  |
| monitoring.sidecar.image.tag | string | `"0.0.10"` |  |
| monitoring.sidecar.port | int | `9617` |  |
| monitoring.sidecar.resources.limits.memory | string | `"128Mi"` |  |
| nodeSelector | object | `{}` |  |
| persistentVolumeClaim.accessModes[0] | string | `"ReadWriteOnce"` |  |
| persistentVolumeClaim.annotations | object | `{}` |  |
| persistentVolumeClaim.enabled | bool | `false` |  |
| persistentVolumeClaim.size | string | `"500Mi"` |  |
| privileged | string | `"false"` |  |
| probes.liveness | object | `{"enabled":true,"failureThreshold":10,"initialDelaySeconds":60,"timeoutSeconds":5}` | Configure the healthcheck for the doh container |
| probes.readiness.enabled | bool | `true` |  |
| probes.readiness.failureThreshold | int | `3` |  |
| probes.readiness.initialDelaySeconds | int | `60` |  |
| probes.readiness.timeoutSeconds | int | `5` |  |
| regex | object | `{}` |  |
| replicaCount | int | `1` |  |
| resources | object | `{}` |  |
| serviceDns.annotations | object | `{}` |  |
| serviceDns.externalTrafficPolicy | string | `"Local"` |  |
| serviceDns.loadBalancerIP | string | `""` |  |
| serviceDns.type | string | `"NodePort"` |  |
| serviceWeb.annotations | object | `{}` |  |
| serviceWeb.externalTrafficPolicy | string | `"Local"` |  |
| serviceWeb.loadBalancerIP | string | `""` |  |
| serviceWeb.type | string | `"ClusterIP"` |  |
| tolerations | list | `[]` |  |
| virtualHost | string | `"pi.hole"` |  |
| webHttp | string | `"80"` |  |
| webHttps | string | `"443"` |  |
| whitelist | object | `{}` |  |

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

Please read [Contribution Guide](CONTRIBUTING.md) for more information on how you can contribute to this Chart.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

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
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.5.0](https://github.com/norwoodj/helm-docs/releases/v1.5.0)
