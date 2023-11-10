#!/bin/bash

campaigns_path="campaigns/natives"
dist_path="dist/campaigns/natives"

mkdir -p $dist_path

xml2esf $campaigns_path/startpos $dist_path/startpos.esf

cp $campaigns_path/scripting.lua $dist_path
