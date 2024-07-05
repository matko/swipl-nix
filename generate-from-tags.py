#!/usr/bin/env python
import os
import json
import re
from github import Github, Auth

stable_repo = 'SWI-Prolog/swipl'
devel_repo = 'SWI-Prolog/swipl-devel'

def version(version_string):
    pattern = r"^V(\d+)\.(\d+)\.(\d+)(?:-(\w+))?$"
    m = re.match(pattern, version_string)
    if not m:
        return None

    return {
        "major": int(m.group(1)),
        "minor": int(m.group(2)),
        "patch": int(m.group(3)),
        "suffix": m.group(4)
    }

def tag_commit(tag):
    v = version(tag.name)
    if v is None:
        return None

    return (tag.name, {"sha": tag.commit.sha, "version": v})

def tag_name_is_version(name):
    return name.startswith('V')

def tags_for(g, repo):
    repo = g.get_repo(repo)
    tag_list = [tag_commit(tag) for tag in repo.get_tags()]

    return {tag[0]: tag[1] for tag in tag_list if tag is not None}

def stable_tags(g):
    tags = tags_for(g, stable_repo)

    return {k: v for k, v in tags.items() if v["version"]["minor"] % 2 == 0 }

def devel_tags(g):
    tags = tags_for(g, devel_repo)

    return {k: v for k, v in tags.items() if v["version"]["minor"] % 2 != 0 }

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

    a = None
    if github_token:
        a = Auth.Token(github_token)
    g = Github(auth=a)
    stable_tags = stable_tags(g)
    with open('stable-tags.json', 'w') as f:
        json.dump(stable_tags, f, indent=4)
    devel_tags = devel_tags(g)
    with open('devel-tags.json', 'w') as f:
        json.dump(devel_tags, f, indent=4)
