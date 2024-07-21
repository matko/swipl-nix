#!/usr/bin/env python
import argparse
import subprocess
import json
import os
import sys
import git

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

def reported_version(checkout_dir, repo_alias, rev):
    repo_path = resolve.repo_alias_to_path(checkout_dir, repo_alias)
    repo = git.Repo(repo_path)
    commit = repo.commit(rev)
    blob = commit.tree / 'VERSION'
    return blob.data_stream.read().decode('utf-8').rstrip()

def rev_to_hash_info(checkout_dir, repo_alias, rev, revname=None):
    print(f'about to retrieve hash for {revname or rev}', file=sys.stderr)
    c = checksum(checkout_dir, repo_alias, rev)
    v = reported_version(checkout_dir, repo_alias, rev)
    repo_name = resolve.repo_alias_to_short_name(repo_alias)
    print(f'done retrieving hash for {revname or rev}', file=sys.stderr)
    return {
        "repo": repo_name,
        "rev": rev,
        "version": v,
        "hash": c,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calculate checksum for a particular ref')
    parser.add_argument('checkout_dir')
    parser.add_argument('version')
    parser.add_argument('--repo', choices=['devel', 'release'], required=False, default='release')

    args = parser.parse_args()
    print(checksum(args.checkout_dir, args.repo, args.version))
