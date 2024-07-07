import os
def repo_alias_to_short_name(repo):
    if repo == 'devel':
        return 'swipl-devel'
    elif repo == 'release':
        return 'swipl'
    else:
        raise Exception(f'not a valid repo type: {repo}')

def repo_alias_to_name(repo):
    short_name = repo_alias_to_short_name(repo)
    return short_name + '.git'

def repo_alias_to_path(checkout_dir, repo):
    repo_name = repo_alias_to_name(repo)

    return os.path.join(checkout_dir, repo_name)

