import fetch_jira_bugs as f
from CONST import *
import os
import pydriller as git
import json

if __name__ == '__main__':
    for key in PROJECTS:
        # All the paths needed
        repo_path = os.path.join(ABS_REPO_PATH, key)
        save_path = os.path.join(ABS_SAVE_PATH, key)
        issue_path = os.path.join(to_save, 'issues')
        issue_all_path = os.path.join(to_save, 'issue_list_all.json')
        gitlog_path = os.path.join(to_save, 'gitlog.json')
        print('Processing: ', key)
        # Find the HEAD commit
        for commit in git.Repository(repo_path, order='reverse').traverse_commits():
            com_hash = commit.hash
            break
        # Process gitlog of repository
        print(key,' - Processing gitlog')
        try:
            f.git_log_to_array(com_hash, repo_path, save_path)
        except:
            print("ERROR with gitlog of ", key)
        # Fetch ALL the issues
        print(key, '- Fetching ALL issues')
        try:
            f.fetch(PROJECTS[key], JIRA_LINK, save_path, only_bugs=False)
        except:
            print("ERROR when fetching for ", key)
            print("Moving to the next project...")
            continue
        # Fetch only fixed issues of type BUG
        print(key, '- Fetching BUG issues')
        try:
            f.fetch(PROJECTS[key], JIRA_LINK, save_path, only_bugs=True)
        except:
            print("ERROR when fetching for ", key)
            print("Moving to the next project...")
            continue
        # Make a dict of all issues
        all_issues = f.build_issue_list(to_save+"/issues_all")
        # Insert project's Jira code in the fix pattern
        pattern = FIX_STRING.format(proj=PROJECTS[key], nbr='{nbr}')
        # Find the fixing commit for each issue closed issue
        print(key, ' - Finding fixing commits')
        try:
            fixed_issues = f.find_bug_fixes(issue_path, gitlog_path, pattern, save_path)
        except:
            print("ERROR when finding fixing commits for ", key)
            print("Moving to the next project...")
            continue
        
        # Update the dict with found fixes
        all_issues.update(fixed_issues)
        with open(issue_all_path, 'w') as file:
            file.write(json.dumps(all_issues))
