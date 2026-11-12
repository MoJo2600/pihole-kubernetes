SHELL := /bin/bash
.DEFAULT_GOAL := help

.PHONY: help
help:  ## help target to show available commands with information
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) |  awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: generate-documentation
generate-documentation: ## Generate README.md from template
	docker run --rm --volume "$$(pwd):/helm-docs" -u $$(id -u) jnorwood/helm-docs:latest helm-docs

.PHONY: lint-manifests
lint-manifests: ## Lint the rendered manifests with kube-linter
	kube-linter lint . --config .kube-linter.yaml