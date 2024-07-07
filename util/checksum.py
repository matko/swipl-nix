#!/usr/bin/env python
import argparse
import subprocess
import json
import os

import resolve

def checksum(checkout_dir, repo, version):
    repo_path = resolve.repo_alias_to_path(checkout_dir, repo)

    result = subprocess.run([
        'nix-prefetch-git',
        '--fetch-submodules',
        '--url',
        repo_path,
        '--rev',
        version,
        '--quiet'
        ],
                            stdout=subprocess.PIPE,
                            text=True)

    if result.returncode != 0:
        raise Exception(f'nix-prefetch-git failed with code {result.returncode}')

    data = json.loads(result.stdout)

    return data["hash"]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calculate checksum for a particular version')
    parser.add_argument('checkout_dir')
    parser.add_argument('version')
    parser.add_argument('--repo', choices=['devel', 'release'], required=False, default='release')

    args = parser.parse_args()
    print(checksum(args.checkout_dir, args.repo, args.version))
