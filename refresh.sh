#!/usr/bin/env bash
dir=`mktemp -d`
util/checkout.py $dir
util/branches_to_hashes.py $dir > ./branches.json
util/tags_to_hashes.py $dir > ./tags.json
util/version_map.py $dir > ./alias.json

rm -rf $dir
