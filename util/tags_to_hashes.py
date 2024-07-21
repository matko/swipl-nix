#!/usr/bin/env python
from tags import tags, branches
from checksum import rev_to_hash_info
from concurrent.futures import ThreadPoolExecutor
import json
import argparse
import resolve
import sys

def versions_to_hashes(checkout_dir, repo_name, versions, old_map=None):
    with ThreadPoolExecutor() as executor:
        return dict(executor.map(lambda version: (version.version, rev_to_hash_info(checkout_dir, repo_name, version.tag, version.tag[1:], old_map)), versions))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calculate hashes for a set of tags')
    parser.add_argument('checkout_dir')
    parser.add_argument('old_map', nargs='?')

    args = parser.parse_args()
    old_map = None
    if args.old_map:
        with open(args.old_map, 'r') as file:
            old_map = json.load(file)
    stable_ts = tags(args.checkout_dir, 'release')
    devel_ts = tags(args.checkout_dir, 'devel')

    hashes = versions_to_hashes(args.checkout_dir, 'release', stable_ts, old_map)
    devel_hashes = versions_to_hashes(args.checkout_dir, 'devel', devel_ts, old_map)
    hashes.update(devel_hashes)

    print(json.dumps(hashes,indent=2))
