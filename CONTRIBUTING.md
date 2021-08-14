# Contributing Guidelines

This charts project accepts contributions via GitHub pull requests. This document outlines the process to help get your contribution accepted.

### Reporting a Bug in Helm

This repository is used by Chart developers for maintaining the official charts for Kubernetes Helm. If your issue is in the Helm tool itself, please use the issue tracker in the [helm/helm](https://github.com/helm/helm) repository.

## How to Contribute to an Existing Chart

1. Fork this repository, develop and test your Chart changes.
1. Please [allow edits from maintainers](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/allowing-changes-to-a-pull-request-branch-created-from-a-fork) so small changes can be added if necessary.
1. Ensure your Chart changes follow the [technical](#technical-requirements) and [documentation](#documentation-requirements) guidelines, described below.
1. Submit a pull request.

### Technical Requirements

* All Chart dependencies should also be submitted independently
* Must pass the linter (`helm lint`)
* Must successfully launch with default values (`helm install .`)
    * All pods go to the running state (or NOTES.txt provides further instructions if a required value is missing e.g. [minecraft](https://github.com/helm/charts/blob/master/stable/minecraft/templates/NOTES.txt#L3))
    * All services have at least one endpoint
* Must include source GitHub repositories for images used in the Chart
* Images should not have any major security vulnerabilities
* Must be up-to-date with the latest stable Helm/Kubernetes features
    * Use Deployments in favor of ReplicationControllers
* Should follow Kubernetes best practices
    * Include Health Checks wherever practical
    * Allow configurable [resource requests and limits](http://kubernetes.io/docs/user-guide/compute-resources/#resource-requests-and-limits-of-pod-and-container)
* Provide a method for data persistence (if applicable)
* Support application upgrades
* Allow customization of the application configuration
* Provide a secure default configuration
* Do not leverage alpha features of Kubernetes
* Includes a [NOTES.txt](https://helm.sh/docs/topics/charts/#chart-license-readme-and-notes) explaining how to use the application after install
* Follows [best practices](https://helm.sh/docs/chart_best_practices/)
  (especially for [labels](https://helm.sh/docs/chart_best_practices/labels/)
  and [values](https://helm.sh/docs/chart_best_practices/values/))

### Documentation Requirements

* Please update the `README.md.gotmpl` file and not the `README.md`, as the `README.md` is automatically generated with helm-docs
* Please update `NOTES.txt` if necessary, including:
    * Any relevant post-installation information for the Chart
    * Instructions on how to access the application or service provided by the Chart

### Add yourself to the list of contributors

See the documentation on how to use the bot [here](https://allcontributors.org/docs/en/bot/usage)

### Merge Approval and Release Process

A maintainer will review the Chart change submission, a validation job in the CI is automatically started. A maintainer may add "LGTM" (Looks Good To Me) or an equivalent comment to indicate that a PR is acceptable. Any change requires at least one LGTM. No pull requests can be merged until at least one maintainer signs off with an LGTM.

Once the Chart has been merged, the release job will automatically run in the CI to package and release the Chart.

## Support Channels

Whether you are a user or contributor, official support channels include:

- GitHub issues: https://github.com/MoJo2600/pihole-kubernetes/issues
- GitHub discussions: https://github.com/MoJo2600/pihole-kubernetes/discussions

Before opening a new issue or submitting a new pull request, it's helpful to search the project - it's likely that another user has already reported the issue you're facing, or it's a known issue that we're already aware of.
