# mojo2600.github.io
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

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
  

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/konturn"><img src="https://avatars0.githubusercontent.com/u/35545508?v=4?s=100" width="100px;" alt=""/><br /><sub><b>konturn</b></sub></a><br /><a href="https://github.com/MoJo2600/pihole-kubernetes/commits?author=konturn" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!