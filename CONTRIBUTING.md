# Contributing Guidelines

This charts project accepts contributions via GitHub pull requests. This document outlines the process to help get your contribution accepted.

Any type of contribution is welcome; from new features, bug fixes, [tests](#testing) or documentation improvements.

## How to Contribute

1. Fork this repository, develop, and test your changes.
2. Please [allow edits from maintainers](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/allowing-changes-to-a-pull-request-branch-created-from-a-fork) so small changes can be added if necessary.
3. Ensure your Chart changes follow the [technical](#technical-requirements) and [documentation](#documentation-requirements) guidelines, described below.
4. Submit a pull request.

### Reporting a Bug in Helm

This repository is used by Chart developers for maintaining the inofficial pihole helm chart. If your issue is in the Helm tool itself, please use the issue tracker in the [helm/helm](https://github.com/helm/helm) repository.

### Technical Requirements

When submitting a PR make sure that it:

* Must pass CI jobs for linting and test the changes on top of different k8s platforms. (Automatically done by the CI/CD pipeline).
* Must follow [Helm best practices](https://helm.sh/docs/chart_best_practices/).
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

#### Sign Your Work

The sign-off is a simple line at the end of the explanation for a commit. All commits needs to be signed. Your signature certifies that you wrote the patch or otherwise have the right to contribute the material. The rules are pretty simple, you only need to certify the guidelines from [developercertificate.org](https://developercertificate.org/).

Then you just add a line to every git commit message:

```text
Signed-off-by: Joe Smith <joe.smith@example.com>
```

Use your real name (sorry, no pseudonyms or anonymous contributions.)

If you set your `user.name` and `user.email` git configs, you can sign your commit automatically with `git commit -s`.

Note: If your git config information is set properly then viewing the `git log` information for your commit will look something like this:

```text
Author: Joe Smith <joe.smith@example.com>
Date:   Thu Feb 2 11:41:15 2018 -0800

    Update README

    Signed-off-by: Joe Smith <joe.smith@example.com>
```

Notice the `Author` and `Signed-off-by` lines match. If they don't your PR will be rejected by the automated DCO check.

### Documentation Requirements

* A chart's `README.md` must include configuration options. The tables of parameters are automatically generated based on the metadata information from the `values.yaml` file.
* Please update `NOTES.txt` if necessary, including:
    * Any relevant post-installation information for the Chart
    * Instructions on how to access the application or service provided by the Chart

### Merge Approval and Release Process

A maintainer will review the Chart change submission, a validation job in the CI is automatically started. A maintainer may add "LGTM" (Looks Good To Me) or an equivalent comment to indicate that a PR is acceptable. Any change requires at least one LGTM. No pull requests can be merged until at least one maintainer signs off with an LGTM.

Once the Chart has been merged, the release job will automatically run in the CI to package and release the Chart.

## Support Channels

Whether you are a user or contributor, official support channels include:

- GitHub issues: https://github.com/MoJo2600/pihole-kubernetes/issues
- GitHub discussions: https://github.com/MoJo2600/pihole-kubernetes/discussions

Before opening a new issue or submitting a new pull request, it's helpful to search the project - it's likely that another user has already reported the issue you're facing, or it's a known issue that we're already aware of.
