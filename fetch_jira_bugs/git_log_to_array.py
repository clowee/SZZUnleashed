""" Dump the git log to a file """
__author__ = "Kristian Berg"
__copyright__ = "Copyright (c) 2018 Axis Communications AB"
__license__ = "MIT"
__credits__ = ["Kristian Berg", "Oscar Svensson"]

import argparse
import subprocess
import sys
import json
import os

def git_log_to_array(init_hash, path_to_repo, path_to_save=None):
    if path_to_save is None:
        path_to_save = ''
    hashes = subprocess.run(['git', 'rev-list', init_hash], cwd=path_to_repo,
        stdout=subprocess.PIPE).stdout.decode('ascii').split()

    logs = []
    i = 0
    for hash_ in hashes:
        entry = subprocess.run(['git', 'show', '--quiet', '--date=iso', hash_],
            cwd=path_to_repo, stdout=subprocess.PIPE)\
            .stdout.decode(errors='replace')
        logs.append(entry)
        i += 1
        if i % 10 == 0:
            print(i, end='\r')

    try:
        os.makedirs(path_to_save, exist_ok=True)
    except FileNotFoundError:
        pass
    path = os.path.join(path_to_save, 'gitlog.json') 
    with open(path, 'w') as f:
        f.write(json.dumps(logs))

# Commits are saved in reverse chronological order from newest to oldest
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="""Convert a git log output to json.
                                                 """)
    parser.add_argument('--from-commit', type=str,
            help="A SHA-1 representing a commit. Runs git rev-list from this commit.")
    parser.add_argument('--repo-path', type=str,
            help="The absolute path to a local copy of the git repository from where the git log is taken.")
    parser.add_argument('--save-path', type=str,
            help="Path to save 'gitlog.json' file.")

    args = parser.parse_args()
    path_to_repo = args.repo_path
    init_hash = args.from_commit
    path_to_save = args.save_path
    git_log_to_array(init_hash, path_to_repo, path_to_save)

