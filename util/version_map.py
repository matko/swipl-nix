#!/usr/bin/env python
import argparse
import json

from tags import tags
from version import Version

def repo_suffix(repo):
    if repo == 'devel':
        return '-devel'
    else:
        return ''

def version_map(repo, tags):
    remap = {}
    for tag in tags:
        major_str = f'{tag.major}{repo_suffix(repo)}'
        minor_str = f'{tag.major}.{tag.minor}'
        if major_str not in remap or tag > remap[major_str]:
            remap[major_str] = tag
        
        if minor_str not in remap or tag > remap[minor_str]:
            remap[minor_str] = tag

    return {k: v.version for k, v in remap.items()}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='determine an alias map for versions')
    parser.add_argument('checkout_dir')
    args = parser.parse_args()
    ts_stable = tags(args.checkout_dir, 'release')
    ts_devel = tags(args.checkout_dir, 'devel')
    stable_version_map = version_map('release', ts_stable)
    version_map = version_map('devel', ts_devel)
    version_map.update(stable_version_map)

    version_map["latest"] = max(ts_stable).version
    version_map["latest-devel"] = max(ts_devel).version
    print(json.dumps(version_map, indent=2))
