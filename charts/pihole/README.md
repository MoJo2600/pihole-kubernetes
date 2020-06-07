pihole
======
Installs pihole in kubernetes

Source code can be found [here](https://github.com/MoJo2600/pihole-kubernetes/tree/master/charts/pihole)

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

serviceTCP:
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


## Uninstallation

To uninstall/delete the `my-release` deployment:

```bash
helm delete --purge my-release
```

## Configuration

The following table lists the configurable parameters of the pihole chart and the default values.

## Chart Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| DNS1 | string | `"8.8.8.8"` |  |
| DNS2 | string | `"8.8.4.4"` |  |
| adlists | object | `{}` |  |
| admin.existingSecret | string | `""` |  |
| admin.passwordKey | string | `"password"` |  |
| adminPassword | string | `"admin"` |  |
| affinity | object | `{}` |  |
| blacklist | object | `{}` |  |
| dnsmasq.additionalHostsEntries | list | `[]` |  |
| dnsmasq.customDnsEntries | list | `[]` |  |
| doh.enabled | bool | `false` |  |
| doh.name | string | `"cloudflared"` |  |
| doh.pullPolicy | string | `"IfNotPresent"` |  |
| doh.repository | string | `"crazymax/cloudflared"` |  |
| doh.tag | string | `"latest"` |  |
| extraEnvVars | object | `{}` |  |
| extraEnvVarsSecret | object | `{}` |  |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository | string | `"pihole/pihole"` |  |
| image.tag | string | `"4.3.2-1"` |  |
| ingress.annotations | object | `{}` |  |
| ingress.enabled | bool | `false` |  |
| ingress.hosts[0] | string | `"chart-example.local"` |  |
| ingress.path | string | `"/"` |  |
| ingress.tls | list | `[]` |  |
| nodeSelector | object | `{}` |  |
| persistentVolumeClaim.accessModes[0] | string | `"ReadWriteOnce"` |  |
| persistentVolumeClaim.annotations | object | `{}` |  |
| persistentVolumeClaim.enabled | bool | `false` |  |
| persistentVolumeClaim.existingClaim | bool | `false` |  |
| persistentVolumeClaim.size | string | `"500Mi"` |  |
| probes.liveness | object | `{"enabled":true,"failureThreshold":10,"initialDelaySeconds":60,"timeoutSeconds":5}` | Configure the healthcheck for the ingress controller |
| probes.readiness.enabled | bool | `true` |  |
| probes.readiness.failureThreshold | int | `3` |  |
| probes.readiness.initialDelaySeconds | int | `60` |  |
| probes.readiness.timeoutSeconds | int | `5` |  |
| regex | object | `{}` |  |
| replicaCount | int | `1` |  |
| resources | object | `{}` |  |
| serviceTCP.annotations | object | `{}` |  |
| serviceTCP.externalTrafficPolicy | string | `"Local"` |  |
| serviceTCP.loadBalancerIP | string | `""` |  |
| serviceTCP.type | string | `"NodePort"` |  |
| serviceUDP.annotations | object | `{}` |  |
| serviceUDP.externalTrafficPolicy | string | `"Local"` |  |
| serviceUDP.loadBalancerIP | string | `""` |  |
| serviceUDP.type | string | `"NodePort"` |  |
| tolerations | list | `[]` |  |
| whitelist | object | `{}` |  |

## Remarks

### MetalLB 0.7.3

MetalLB 0.7.3 has a bug, where the service is not announced anymore, when the pod changes (e.g. update of a deployment). My workaround is to restart the `metallb-speaker-*` pods.

### MetalLB 0.8.1+

pihole seems to work without issue in MetalLB 0.8.1+

## Credits

[Pi-hole®](https://pi-hole.net/)

## Contributing

Feel free to contribute by making a [pull request](https://github.com/MoJo2600/pihole-kubernetes/pull/new/master).

Please read the official [Contribution Guide](https://github.com/helm/charts/blob/master/CONTRIBUTING.md) from Helm for more information on how you can contribute to this Chart.
