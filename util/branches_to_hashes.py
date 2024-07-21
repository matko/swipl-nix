#!/usr/bin/env python
from tags import tags, branches
from checksum import rev_to_hash_info
from concurrent.futures import ThreadPoolExecutor
import json
import argparse
import resolve
import sys

def branches_to_hashes(checkout_dir, repo_name, branches):
    with ThreadPoolExecutor() as executor:
        return dict(executor.map(lambda branch: (branch.name, rev_to_hash_info(checkout_dir, repo_name, branch.hash, branch.name)), branches))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calculate hashes for a set of branches')
    parser.add_argument('checkout_dir')

    args = parser.parse_args()
    devel_ts = tags(args.checkout_dir, 'devel')

    devel_branches = branches(args.checkout_dir, 'devel')
    hashes = branches_to_hashes(args.checkout_dir, 'devel', devel_branches)

    print(json.dumps(hashes,indent=2))
