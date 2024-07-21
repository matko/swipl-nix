#!/usr/bin/env bash
set -e
if [ -z "$1" ]; then
    echo "Checkout in a temporary directory"
    dir=`mktemp -d`
else
    dir="$1"
fi
util/checkout.py $dir
util/branches_to_hashes.py $dir ./branches.json > ./new_branches.json && mv new_branches.json branches.json
util/tags_to_hashes.py $dir ./tags.json > ./new_tags.json && mv new_tags.json tags.json
util/version_map.py $dir > ./alias.json

if [ -z "$1" ]; then
    echo "Deleting temporary checkout directory"
    rm -rf $dir
fi
