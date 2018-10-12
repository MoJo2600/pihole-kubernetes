# PiHole on kubernetes

A sample deployment for pihole on a kubernetes cluster. I'm running an on premise kubernetes cluster and i'm using MetaLB for loadbalancing and rook for storage.

Installation:
* First setup the service to get an ip for your installation
* Update the deployment file with the server IP from step 1
* Deploy everything else

When everything went right, you should be able to access the pihole installation on the specified IP


