# pihole

Installs pihole in kubernetes

![Version: 1.8.22](https://img.shields.io/badge/Version-1.8.22-informational?style=flat-square) ![AppVersion: 5.2](https://img.shields.io/badge/AppVersion-5.2-informational?style=flat-square)

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

serviceTCPHTTP:
  loadBalancerIP: 192.168.178.252
  annotations:
    metallb.universe.tf/allow-shared-ip: pihole-svc
  type: LoadBalancer

serviceTCPDNS:
  loadBalancerIP: 192.168.178.252
  annotations:
    metallb.universe.tf/allow-shared-ip: pihole-svc
  type: LoadBalancer

serviceUDP:
  loadBalancerIP: 192.168.178.252
  annotations:
    metallb.universe.tf/allow-shared-ip: pihole-svc
  type: LoadBalancer

```

## Upgrading

### To 1.8.22

To enhance compatibility for traefik, we split the HTTP service into TCPHTTP and TCPDNS. This means, if you have a dedicated configuration for the service, you have to
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
serviceTCPHTTP:
  loadBalancerIP: 192.168.178.252
  annotations:
    metallb.universe.tf/allow-shared-ip: pihole-svc

serviceTCPDNS:
  loadBalancerIP: 192.168.178.252
  annotations:
    metallb.universe.tf/allow-shared-ip: pihole-svc

serviceUDP:
  loadBalancerIP: 192.168.178.252
  annotations:
    metallb.universe.tf/allow-shared-ip: pihole-svc
```

## Uninstallation

To uninstall/delete the `my-release` deployment:

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
| dnsmasq.upstreamServers | list | `[]` |  |
| doh.enabled | bool | `false` |  |
| doh.envVars | object | `{}` |  |
| doh.name | string | `"cloudflared"` |  |
| doh.pullPolicy | string | `"IfNotPresent"` |  |
| doh.repository | string | `"crazymax/cloudflared"` |  |
| doh.tag | string | `"latest"` |  |
| extraEnvVars | object | `{}` |  |
| extraEnvVarsSecret | object | `{}` |  |
| hostNetwork | string | `"false"` |  |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository | string | `"pihole/pihole"` |  |
| image.tag | string | `"v5.2"` |  |
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
| probes.liveness | object | `{"enabled":true,"failureThreshold":10,"initialDelaySeconds":60,"timeoutSeconds":5}` | Configure the healthcheck for the ingress controller |
| probes.readiness.enabled | bool | `true` |  |
| probes.readiness.failureThreshold | int | `3` |  |
| probes.readiness.initialDelaySeconds | int | `60` |  |
| probes.readiness.timeoutSeconds | int | `5` |  |
| regex | object | `{}` |  |
| replicaCount | int | `1` |  |
| resources | object | `{}` |  |
| serviceTCPDNS.annotations | object | `{}` |  |
| serviceTCPDNS.externalTrafficPolicy | string | `"Local"` |  |
| serviceTCPDNS.loadBalancerIP | string | `""` |  |
| serviceTCPDNS.type | string | `"NodePort"` |  |
| serviceTCPHTTP.annotations | object | `{}` |  |
| serviceTCPHTTP.externalTrafficPolicy | string | `"Local"` |  |
| serviceTCPHTTP.loadBalancerIP | string | `""` |  |
| serviceTCPHTTP.type | string | `"ClusterIP"` |  |
| serviceUDP.annotations | object | `{}` |  |
| serviceUDP.externalTrafficPolicy | string | `"Local"` |  |
| serviceUDP.loadBalancerIP | string | `""` |  |
| serviceUDP.port | int | `53` |  |
| serviceUDP.protocol | string | `"UDP"` |  |
| serviceUDP.type | string | `"NodePort"` |  |
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

Please read the official [Contribution Guide](https://github.com/helm/charts/blob/master/CONTRIBUTING.md) from Helm for more information on how you can contribute to this Chart.

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.4.0](https://github.com/norwoodj/helm-docs/releases/v1.4.0)
