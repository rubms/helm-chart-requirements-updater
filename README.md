# Helm Chart Requirements Updater
A command to update the requirements in your chart to the latest available option

## Usage

`requirements-updater` is able to parse the output given by `helm search`, using that information to update the requirements in the Helm chart provided as argument:

```bash
helm repo update
helm search | helm-requirements-updater.py ./mychart
```

## Pending features

Providing `requirements-updater` as a Helm plugin.