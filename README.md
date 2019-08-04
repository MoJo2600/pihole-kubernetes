# Pi-hole on kubernetes

The [Pi-hole®](https://pi-hole.net/) is a DNS sinkhole that protects your devices from unwanted content, without installing any client-side software.

This repository provides you with everything necessary to deploy pihole on your kubernetes cluster. I'm running an on premise kubernetes cluster and i'm using [MetalLB](https://metallb.universe.tf) 0.7.2 for loadbalancing and [glusterfs](https://github.com/gluster/gluster-kubernetes) for storage.

## Repository structure
* The folder `pihole` contains a helm chart to install pi-hole on kubernetes. Please see the [README](pihole/README.md) for more details
* The folder `classic` contains kubernetes files to install pi-hole on kubernetes

## TL;DR;

Download the latest release and unzip the archive. Create a values.yaml with your configuration. Basic configuration with metallb looks like this (Find an full example in the folder `example`):

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

You should now have a running pihole instance. You should be able to open the web UI under the url [http://192.168.178.252/admin](http://192.168.178.252/admin) and use the default password 'admin'.

## Changelog

### 0.1

* Updated to latest pihole release 4.3.1-4_amd64 
* Added liveness and readiness checks
* You are now able to configure adlists, whitelists and blacklists in the configuration and have pihole load them during startup. (See `example\` folder)

## Remarks

### MetalLB 0.7.3

MetalLB 0.7.3 has a bug, where the service is not announced anymore, when the pod changes (e.g. update of a deployment). My workaround is to restart the `metallb-speaker-*` pods.

### MetalLB 0.8.1

I did not test pihole-kubernetes with version 0.8.1. Please let me know if it works.
