#!/usr/bin/env python
from tags import tags
from checksum import checksum
from concurrent.futures import ThreadPoolExecutor
import json
import argparse
import resolve

def version_to_hash_info(checkout_dir, repo_alias, version):
    c = checksum(checkout_dir, repo_alias, version.tag)
    repo_name = resolve.repo_alias_to_short_name(repo_alias)
    return {
        "repo": repo_name,
        "rev": version.tag,
        "hash": c,
    }

def versions_to_hashes(checkout_dir, repo_name, versions):

    with ThreadPoolExecutor() as executor:
        return dict(executor.map(lambda version: (version.version, version_to_hash_info(checkout_dir, repo_name, version)), versions))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calculate hashes for a set of tags')
    parser.add_argument('checkout_dir')
    parser.add_argument('--repo', choices=['devel', 'release'], required=False, default='release')

    args = parser.parse_args()
    stable_ts = tags(args.checkout_dir, 'release')
    devel_ts = tags(args.checkout_dir, 'devel')
    stable_hashes = versions_to_hashes(args.checkout_dir, 'release', stable_ts)
    hashes = versions_to_hashes(args.checkout_dir, 'devel', devel_ts)
    hashes.update(stable_hashes)
    print(json.dumps(hashes,indent=2))
