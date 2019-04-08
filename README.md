# Pi-hole on kubernetes

The [Pi-hole®](https://pi-hole.net/) is a DNS sinkhole that protects your devices from unwanted content, without installing any client-side software.

This repository provides you with everything necessary to deploy pihole on your kubernetes cluster. I'm running an on premise kubernetes cluster and i'm using MetaLB 0.7.3 for loadbalancing and rook/ceph for storage.

## Repository structure
* The folder `pihole` contains a helm chart to install pi-hole on kubernetes. Please see the [README](pihole/README.md) for more details
* The folder `classic` contains kubernetes files to install pi-hole on kubernetes

## TL;DR;

Clone the repository and create a calues.yaml with your configuration. Mine for usage with metallb looks like this:

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

serviceUDP:
  loadBalancerIP: 192.168.178.252
  annotations:
    metallb.universe.tf/allow-shared-ip: pihole-svc

```

Then deploy everything with helm

```console
$ cd pihole-kubernetes
$ helm upgrade -i pihole ./pihole -f values.yaml
```

You should now have a running pihole instance. You should be able to open the web UI under the url http://192.168.178.252/admin and use the default password 'admin'.
