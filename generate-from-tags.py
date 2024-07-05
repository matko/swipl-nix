#!/usr/bin/env python
import os
import json
from github import Github, Auth

stable_repo = 'SWI-Prolog/swipl'
devel_repo = 'SWI-Prolog/swipl-devel'

def tag_commit(tag):
    return (tag.name, tag.commit.sha)

def tag_name_is_version(name):
    return name.startswith('V')

def tags_for(g, repo):
    repo = g.get_repo(repo)
    tag_list = [tag_commit(tag) for tag in repo.get_tags()]

    return {tag[0]: tag[1] for tag in tag_list if tag_name_is_version(tag[0])}

if __name__ == '__main__':
    # it's probably fine to default to no auth, as these are public
    # repos.  However, when running this tool a lot, you're bound to
    # run into a rate limit, as anonymous requests are limited to 60
    # per hour.
    #
    # Therefore, if a token is available, let's use it.
    github_token = os.getenv("GITHUB_TOKEN")
    #if github_token is None:
    #    raise EnvironmentError('GITHUB_TOKEN env var not set')

    a = Auth.Token(github_token)
    g = Github(auth=a)
    stable_tags = tags_for(g, stable_repo)
    with open('stable-tags.json', 'w') as f:
        json.dump(stable_tags, f, indent=4)
    devel_tags = tags_for(g, devel_repo)
    with open('devel-tags.json', 'w') as f:
        json.dump(devel_tags, f, indent=4)
