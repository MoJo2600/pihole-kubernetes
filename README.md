# mojo2600.github.io

[Helm](https://helm.sh) repo for different charts which can be installed on [Kubernetes](https://kubernetes.io)

Further documentation including chart keys, types, and default values is at https://hub.helm.sh/charts/mojo2600/pihole

### Add Helm repository

To install the repo just run:

```bash
helm repo add mojo2600 https://mojo2600.github.io/pihole-kubernetes/
helm repo update
```

### Helm Charts

* [pihole](https://mojo2600.github.io/pihole-kubernetes)

  ```bash
  helm install --name your-release mojo2600/pihole
  ```
  
