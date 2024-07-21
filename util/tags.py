#!/usr/bin/env python
import os
import git
import json
import argparse

import resolve
from version import Version


def include_version(repo, version):
    if version is None:
        return False

    if not version.is_supported():
        return False

    remainder = 0;
    if repo == 'devel':
        remainder = 1;

    return version.minor % 2 == remainder

def tags(checkout_dir, repo_name):
    repo_path = resolve.repo_alias_to_path(checkout_dir, repo_name)
    repo = git.Repo(repo_path)
    result = list(filter(
        lambda v: include_version(repo_name, v),
        map(lambda t: Version.parse(t.name), repo.tags)))

    result.sort()

    return result

class Branch:
    def __init__(self, name, hash):
        self.name = name
        self.hash = hash

def branches(checkout_dir, repo_name):
    repo_path = resolve.repo_alias_to_path(checkout_dir, repo_name)
    repo = git.Repo(repo_path)
    result = list(map(lambda b: Branch(b.name, b.commit.hexsha), repo.branches))

    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calculate checksum for a particular version')
    parser.add_argument('checkout_dir')
    parser.add_argument('--repo', choices=['devel', 'release'], required=False, default='release')
    args = parser.parse_args()
    print(json.dumps([v.__dict__ for v in tags(args.checkout_dir, args.repo)], indent=2))
