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

if len(sys.argv) == 1:
    print("Expected argument: path to helm chart")
    sys.exit(1)

#import subprocess
#completed_process = subprocess.run(["helm", "search"]) #, capture_output=True)
#for line in completed_process.stdout.splitlines():
for line in sys.stdin:
    m = pattern.match(line)
    if m:
        (chart, version) = m.groups()
        (repo, name) = chart.split("/")
        charts[name] = Chart(name, repo, version)

requirements_path = os.path.join(sys.argv[1], "requirements.yaml")
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