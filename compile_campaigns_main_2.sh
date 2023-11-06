#!/bin/bash

campaigns_path="campaigns/main_2"
dist_path="dist/campaigns/main_2"

mkdir -p $dist_path

xml2esf $campaigns_path/startpos $dist_path/startpos.esf

cp $campaigns_path/scripting.lua $dist_path
