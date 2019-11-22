# Helm Chart Requirements Updater

A Helm plugin to update the requirements in your chart to the latest available version.

## Requirements

* Python >= 3
* Helm: installed and inited

## Installation

```
helm plugin install https://github.com/rubms/helm-chart-requirements-updater
```

## Usage

`requirements-update` is able to parse the output given by `helm search`, using that information to update the requirements in the Helm chart provided as an argument:

```bash
helm repo update
helm requirements-update <path_to_your_chart>
```
