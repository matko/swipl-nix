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

def resolve_rev(checkout_dir, repo_alias, rev):
    repo_path = resolve.repo_alias_to_path(checkout_dir, repo_alias)
    repo = git.Repo(repo_path)
    commit = repo.commit(rev)

    return commit.hexsha

def rev_to_hash_info(checkout_dir, repo_alias, rev, revname, old_map):
    resolved_rev = resolve_rev(checkout_dir, repo_alias, rev)
    if old_map and revname in old_map and old_map[revname]['rev'] == resolved_rev:
        print(f'reusing old hash for {revname}', file=sys.stderr)
        hash = old_map[revname]["hash"]
        v = old_map[revname]["version"]
    else:
        print(f'retrieving hash for {revname}', file=sys.stderr)
        hash = checksum(checkout_dir, repo_alias, rev)
        print(f'done retrieving hash for {revname}', file=sys.stderr)
        v = reported_version(checkout_dir, repo_alias, rev)

    repo_name = resolve.repo_alias_to_short_name(repo_alias)
    return {
        "repo": repo_name,
        "rev": resolved_rev,
        "version": v,
        "hash": hash,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calculate checksum for a particular ref')
    parser.add_argument('checkout_dir')
    parser.add_argument('version')
    parser.add_argument('--repo', choices=['devel', 'release'], required=False, default='release')

    args = parser.parse_args()
    print(checksum(args.checkout_dir, args.repo, args.version))
