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

```yaml
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

| Key                                  | Type   | Default                                                                              | Description                                          |
|--------------------------------------|--------|--------------------------------------------------------------------------------------|------------------------------------------------------|
| DNS1                                 | string | `"8.8.8.8"`                                                                          |                                                      |
| DNS2                                 | string | `"8.8.4.4"`                                                                          |                                                      |
| adlists                              | object | `{}`                                                                                 |                                                      |
| admin.existingSecret                 | string | `""`                                                                                 |                                                      |
| admin.passwordKey                    | string | `"password"`                                                                         |                                                      |
| adminPassword                        | string | `"admin"`                                                                            |                                                      |
| affinity                             | object | `{}`                                                                                 |                                                      |
| blacklist                            | object | `{}`                                                                                 |                                                      |
| dnsmasq.additionalHostsEntries       | list   | `[]`                                                                                 |                                                      |
| dnsmasq.customDnsEntries             | list   | `[]`                                                                                 |                                                      |
| doh.enabled                          | bool   | `false`                                                                              |                                                      |
| doh.name                             | string | `"cloudflared"`                                                                      |                                                      |
| doh.pullPolicy                       | string | `"IfNotPresent"`                                                                     |                                                      |
| doh.repository                       | string | `"crazymax/cloudflared"`                                                             |                                                      |
| doh.tag                              | string | `"latest"`                                                                           |                                                      |
| doh.envVars                          | object | `{}`                                                                                 |                                                      |
| extraEnvVars                         | object | `{}`                                                                                 |                                                      |
| extraEnvVarsSecret                   | object | `{}`                                                                                 |                                                      |
| image.pullPolicy                     | string | `"IfNotPresent"`                                                                     |                                                      |
| image.repository                     | string | `"pihole/pihole"`                                                                    |                                                      |
| image.tag                            | string | `"5.1.1"`                                                                            |                                                      |
| ingress.annotations                  | object | `{}`                                                                                 |                                                      |
| ingress.enabled                      | bool   | `false`                                                                              |                                                      |
| ingress.hosts[0]                     | string | `"chart-example.local"`                                                              |                                                      |
| ingress.path                         | string | `"/"`                                                                                |                                                      |
| ingress.tls                          | list   | `[]`                                                                                 |                                                      |
| nodeSelector                         | object | `{}`                                                                                 |                                                      |
| persistentVolumeClaim.accessModes[0] | string | `"ReadWriteOnce"`                                                                    |                                                      |
| persistentVolumeClaim.annotations    | object | `{}`                                                                                 |                                                      |
| persistentVolumeClaim.enabled        | bool   | `false`                                                                              |                                                      |
| persistentVolumeClaim.existingClaim  | bool   | `false`                                                                              |                                                      |
| persistentVolumeClaim.size           | string | `"500Mi"`                                                                            |                                                      |
| probes.liveness                      | object | `{"enabled":true,"failureThreshold":10,"initialDelaySeconds":60,"timeoutSeconds":5}` | Configure the healthcheck for the ingress controller |
| probes.readiness.enabled             | bool   | `true`                                                                               |                                                      |
| probes.readiness.failureThreshold    | int    | `3`                                                                                  |                                                      |
| probes.readiness.initialDelaySeconds | int    | `60`                                                                                 |                                                      |
| probes.readiness.timeoutSeconds      | int    | `5`                                                                                  |                                                      |
| regex                                | object | `{}`                                                                                 |                                                      |
| replicaCount                         | int    | `1`                                                                                  |                                                      |
| resources                            | object | `{}`                                                                                 |                                                      |
| serviceTCP.annotations               | object | `{}`                                                                                 |                                                      |
| serviceTCP.externalTrafficPolicy     | string | `"Local"`                                                                            |                                                      |
| serviceTCP.loadBalancerIP            | string | `""`                                                                                 |                                                      |
| serviceTCP.type                      | string | `"NodePort"`                                                                         |                                                      |
| serviceUDP.annotations               | object | `{}`                                                                                 |                                                      |
| serviceUDP.externalTrafficPolicy     | string | `"Local"`                                                                            |                                                      |
| serviceUDP.loadBalancerIP            | string | `""`                                                                                 |                                                      |
| serviceUDP.type                      | string | `"NodePort"`                                                                         |                                                      |
| tolerations                          | list   | `[]`                                                                                 |                                                      |
| whitelist                            | object | `{}`                                                                                 |                                                      |
| monitoring.podMonitor.enabled        | bool   | `false`                                                                              |                                                      |
| monitoring.sidecar.enabled           | bool   | `false`                                                                              |                                                      |
| monitoring.sidecar.port              | int    | `9617`                                                                               |                                                      |
| monitoring.sidecar.image.repository  | string | `ekofr/pihole-exporter`                                                              |                                                      |
| monitoring.sidecar.image.tag         | bool   | `0.0.9`                                                                              |                                                      |
| monitoring.sidecar.image.pullPolicy  | bool   | `IfNotPresent`                                                                       |                                                      |
| monitoring.sidecar.resources         | object | `{}`                                                                                 |                                                      |


## HowTo

### Pi-Hole in HA mode (multi-pod) (Thanks @brnl)

You need a central storage, available to all pods like NFS.

#### values for Pi-Hole HA for nginx ingress example


```yaml
replicaCount: 2

persistentVolumeClaim:
  enabled: true
  accessModes:
    - ReadWriteMany
  storageClass: nfs-client

ingress:
  enabled: true
  hosts:
    # Set your favorite hostname. It must resolve to the ingress IP-address. You could add this in PiHole itself
    # once you use it as your DNS-server. Until then, please add it to your hosts file.
    - pihole.local
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/affinity: "cookie"
    nginx.ingress.kubernetes.io/affinity-mode: "persistent"
    nginx.ingress.kubernetes.io/session-cookie-name: "route"
    nginx.ingress.kubernetes.io/session-cookie-expires: "172800"
    nginx.ingress.kubernetes.io/session-cookie-max-age: "172800"
This should also work with Treafik, which is the default on K3S but I didn't test this:
```


#### values for Pi-Hole HA for traefik ingress example


```yaml
replicaCount: 2

persistentVolumeClaim:
  enabled: true
  accessModes:
    - ReadWriteMany
  storageClass: nfs-client

ingress:
  enabled: true
  hosts:
    # Set your favorite hostname. It must resolve to the ingress IP-address. You could add this in PiHole itself
    # once you use it as your DNS-server. Until then, please add it to your hosts file.
    - pihole.local
  annotations:
    kubernetes.io/ingress.class: traefik

serviceTCP:
  annotations:
    traefik.ingress.kubernetes.io/affinity: "true"
    traefik.ingress.kubernetes.io/session-cookie-name: "sticky"
```

Additionally you can force kubernetes to schedule the pods on different hosts:

```yaml
antiaff:
  enabled: true
  # Here you can set the pihole release (you set in `helm install <releasename> ...`)
  # you want to avoid
  avoidRelease: pihole1
  # Here you can choose between preferred or required
  strict: true
```

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
