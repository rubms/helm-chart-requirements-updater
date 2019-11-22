#!/usr/bin/env python3
import re
import sys
import os
import yaml

pattern = re.compile("^([0-9\w\-_\.]+/[0-9\w\-_\.]+)\s+([0-9\w\-_\.]+).*$")

class Chart:
    def __init__(self, name, repo, version):
        self.name = name
        self.repo = repo
        self.version = version

charts = {}

if len(sys.argv) != 3:
    print("Expected arguments: <path_to_helm_bin> <path_to_helm_chart>")
    sys.exit(1)

import subprocess
completed_process = subprocess.run([sys.argv[1], "search"], stdout=subprocess.PIPE)
for line in str(completed_process.stdout).splitlines():
    m = pattern.match(line)
    if m:
        (chart, version) = m.groups()
        (repo, name) = chart.split("/")
        charts[name] = Chart(name, repo, version)

requirements_path = os.path.join(sys.argv[2], "requirements.yaml")
if not os.path.isfile(requirements_path):
    print("Cannot find a requirements yaml in the specified chart path.")
    sys.exit(2)

with open(requirements_path) as f:
    requirements = yaml.load(f)

for dependency in requirements["dependencies"]:
    if dependency["name"] in charts.keys():
        chart = charts[dependency["name"]]
        if dependency["repository"].replace('@', '') == chart.repo:
            dependency["version"] = chart.version

with open(requirements_path, "w") as f:
    yaml.dump(requirements, f, default_flow_style=False)
