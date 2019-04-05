# Pi-hole Chart

This directory contains a Kubernetes chart to deploy a
[Pi-hole](https://github.com/itamaro/gcp-go-night-king) DNS sinkhole.

## TL;DR;

```console
$ helm upgrade -i pihole ./pihole -f values.yaml
```

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

serviceUDP:
  loadBalancerIP: 192.168.178.252
  annotations:
    metallb.universe.tf/allow-shared-ip: pihole-svc

```

## Known Issues

* There seems to be a timeout when loading blocklists on startup. I reduces the blocklists
* There is only a sample with metallb to create a LoadBalancer for TCP and UDP on the same IP address, no cloud sample for e.g. AWS
* Currently whitelist.txt and blacklist.txt are read from a configmap so changes in the gui are not possible. I will fix this asap

## Chart details

more to come
