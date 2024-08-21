#!/usr/bin/env python

from github import Github, Auth
import git
import os
import re
import argparse
from concurrent.futures import ThreadPoolExecutor

script_dir = os.path.dirname(os.path.abspath(__file__))

def package_repo_urls(github_token):
    a = None
    if github_token:
        a = Auth.Token(github_token)
    gh = Github(auth=a)
    org = gh.get_organization('SWI-Prolog')

    repos = org.get_repos(type = 'public')

    return [authenticated_repo_url(repo.clone_url, github_token) for repo in repos if repo.name.startswith('packages-') or repo.name.startswith('contrib-')]

def authenticated_repo_url(url, token):
    if token is None:
        return url
    pattern = r"(https://)(github\.com/.*)"
    replacement = rf"\1{token}@\2"
    return re.sub(pattern, replacement, url)


def ensure_repo(repo_url, repos_path):
    repo_name = os.path.basename(repo_url)
    destination = os.path.join(repos_path, repo_name)

    repo = None
    if os.path.exists(destination):
        print(f'{repo_name} already exists. refreshing..')
        repo = git.Repo(destination)
    else:
        print(f'cloning {repo_name}..')
        repo = git.Repo.clone_from(repo_url, destination, bare=True)

    # always fetch regardless
    # let's make sure we can fetch by just shotgunning in the
    # relevant config every time. Yes, this is silly.
    with repo.config_writer() as config:
        config.set_value('remote "origin"', 'fetch', '+refs/heads/*:refs/remotes/origin/*')
        #config.set_value('remote "origin"', 'fetch', '+refs/tags/*:refs/tags/*')

    repo.remotes.origin.fetch(tags=True, prune=True)

def checkout(dir='repos'):
    print(f'checking out in {dir}')
    os.makedirs(dir, exist_ok=True)

    github_token = os.getenv("GITHUB_TOKEN")
    # first, a list of the non-package repos
    with open(os.path.join(script_dir, '../fixed-repos.list'), 'r') as f:
        static_repos = [authenticated_repo_url(repo.strip(), github_token) for repo in f]

    packages = package_repo_urls(github_token)

    repos = static_repos + packages

    with ThreadPoolExecutor() as executor:
        result = executor.map(lambda url: ensure_repo(url, dir), repos)

    for _ in result:
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='checkout all SWI-Prolog related repositories, or refetch them if they are already checked out.')
    parser.add_argument('directory', help='the directory where the checkout will take place', default='repos', nargs='?')

    args = parser.parse_args()
    checkout(args.directory)
