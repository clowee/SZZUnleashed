import fetch_jira_bugs as f
from CONST import *
import os
import pydriller as git

if __name__ == '__main__':
    for key in PROJECTS:
        print('Processing: ', key)
        repo_path = os.path.join(ABS_REPO_PATH, key)
        for commit in git.Repository(repo_path, order='reverse').traverse_commits():
            com_hash = commit.hash
            break
        to_save = os.path.join(ABS_SAVE_PATH, key)
        print(key, '- Fetching issues')
        try:
            f.fetch(PROJECTS[key], JIRA_LINK, to_save)
        except:
            print("Error when fetching for ", key)
        print(key,' - Processing gitlog')
        try:
            f.git_log_to_array(com_hash, repo_path, to_save)
        except:
            print("Error with gitlog of ", key)
        pattern = FIX_STRING.format(proj=PROJECTS[key], nbr='{nbr}')
        issue_path = os.path.join(to_save, 'issues')
        gitlog_path = os.path.join(to_save, 'gitlog.json')
        print(key, ' - Finding fixing commits')
        try:
            f.find_bug_fixes(issue_path, gitlog_path, pattern, to_save)
        except:
            print("Error when finding fixing commits for ", key)
