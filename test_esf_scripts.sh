#!/bin/bash

campaigns_path="campaigns/main"
test_project_path="esf_scripts/projects/1830"
dist_path="dist/campaigns/main"

python3 esf_scripts/projects/1830/master.py

mkdir -p $dist_path

xml2esf $campaigns_path/startpos $dist_path/startpos.esf

cp $test_project_path/scripting.lua $dist_path
