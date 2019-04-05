# Pi-hole on kubernetes

The [Pi-hole®](https://pi-hole.net/) is a DNS sinkhole that protects your devices from unwanted content, without installing any client-side software.

This repository provides you with everything necessary to deploy pihole on your kubernetes cluster. I'm running an on premise kubernetes cluster and i'm using MetaLB 0.7.3 for loadbalancing and rook/ceph for storage.

## Repository structure
* The folder `pihole` contains a helm chart to install pi-hole on kubernetes. Please see the [README](pihole/README.md) for more details
* The folder `classic` contains kubernetes files to install pi-hole on kubernetes

