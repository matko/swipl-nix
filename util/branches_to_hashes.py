#!/usr/bin/env python
from tags import tags, branches
from checksum import rev_to_hash_info
from concurrent.futures import ThreadPoolExecutor
import json
import argparse
import resolve
import sys

def branches_to_hashes(checkout_dir, repo_name, branches, old_map=None):
    with ThreadPoolExecutor() as executor:
        return dict(executor.map(lambda branch: (branch.name, rev_to_hash_info(checkout_dir, repo_name, branch.hash, branch.name, old_map)), branches))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calculate hashes for a set of branches')
    parser.add_argument('checkout_dir')
    parser.add_argument('old_map', nargs='?')

    args = parser.parse_args()
    devel_ts = tags(args.checkout_dir, 'devel')
    old_map = None
    if args.old_map:
        with open(args.old_map, 'r') as file:
            old_map = json.load(file)

    devel_branches = branches(args.checkout_dir, 'devel')
    hashes = branches_to_hashes(args.checkout_dir, 'devel', devel_branches, old_map)

    print(json.dumps(hashes,indent=2))
