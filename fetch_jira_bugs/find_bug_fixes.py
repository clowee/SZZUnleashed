""" Identify bugfixes in Jenkins repository given a list of issues """
__author__ = "Kristian Berg"
__copyright__ = "Copyright (c) 2018 Axis Communications AB"
__license__ = "MIT"

import os
import json
import re
import argparse

def find_bug_fixes(issue_path, gitlog_path, gitlog_pattern, save_path=None):
    """ Identify bugfixes in Jenkins repository given a list of issues """
    if save_path is None:
        save_path = ''

    i = 0 # Used to display progress
    no_matches = []
    matches_per_issue = {}
    total_matches = 0

    issue_list = build_issue_list(issue_path)
    with open(gitlog_path) as f:
        gitlog = json.loads(f.read())

    for key in issue_list:
        nbr = key.split('-')[1]
        matches = []

        for commit in gitlog:
            pattern = gitlog_pattern.format(nbr=nbr)
            if re.search(pattern, commit):
                matches.append(commit)
        total_matches += len(matches)
        matches_per_issue[key] = len(matches)

        if matches:
            selected_commit = commit_selector_heuristic(matches)
            if not selected_commit:
                no_matches.append(key)
            else:
                issue_list[key]['hash'] = \
                    re.search('(?<=^commit )[a-z0-9]+(?=\n)', \
                    selected_commit).group(0)
                issue_list[key]['commitdate'] = \
                    re.search('(?<=\nDate:   )[0-9 -:+]+(?=\n)',\
                    selected_commit).group(0)
        else:
            no_matches.append(key)

        # Progress counter
        i += 1
        if i % 10 == 0:
            print(i, end='\r')

    print('Total issues: ' + str(len(issue_list)))
    print('Issues matched to a bugfix: ' + str(len(issue_list) - len(no_matches)))
    print('Percent of issues matched to a bugfix: ' + \
          str((len(issue_list) - len(no_matches)) / len(issue_list)))
    for key in no_matches:
        issue_list.pop(key)
    
    try:
        os.makedirs(save_path, exist_ok=True)
    except FileNotFoundError:
        pass
    save_fixed = os.path.join(save_path, 'issue_list.json')
    with open(save_fixed, 'w') as f:
        f.write(json.dumps(issue_list))

    return issue_list



def build_issue_list(path):
    def format_date(date):
        date = date.replace('T', ' ') 
        date = date.replace('.000', ' ') 
        return date
    """ Helper method for find_bug_fixes """
    issue_list = {}
    for filename in os.listdir(path):
        with open(path + '/' + filename) as f:
            for issue in json.loads(f.read())['issues']:
                issue_list[issue['key']] = {}
                try:
                    issue_list[issue['key']]['priority'] = issue['fields']['priority']['name']
                except:
                    issue_list[issue['key']]['priority'] = None
                try:
                    issue_list[issue['key']]['type'] = issue['fields']['issuetype']['name']
                except:
                    issue_list[issue['key']]['type'] = None
                try:
                    issue_list[issue['key']]['status'] = issue['fields']['status']['name']
                except:
                    issue_list[issue['key']]['status'] = None
                try:
                    issue_list[issue['key']]['resolution'] = issue['fields']['resolutiion']['name']
                except:
                    issue_list[issue['key']]['resolution'] = None
                try:
                    issue_list[issue['key']]['labels'] = issue['fields']['labels']
                except:
                    issue_list[issue['key']]['status'] = None
                try:
                    issue_list[issue['key']]['summary'] = issue['fields']['summary']
                except:
                    issue_list[issue['key']]['summary'] = None
                try:
                    issue_list[issue['key']]['description'] = issue['fields']['description']
                except:
                    issue_list[issue['key']]['description'] = None
                try:
                    issue_list[issue['key']]['timeoriginalestimate'] = issue['fields']['timeoriginalestimate']
                except:
                    issue_list[issue['key']]['timeoriginalestimate'] = None
                try:
                    issue_list[issue['key']]['aggregatetimeoriginalestimate'] = issue['fields']['aggregatetimeoriginalestimate']
                except:
                    issue_list[issue['key']]['aggregatetimeoriginalestimate'] = None

                try:
                    created_date = issue['fields']['created']
                    issue_list[issue['key']]['creationdate'] = format_date(created_date)
                except:
                    issue_list[issye['key']]['creationdate'] = None

                try:
                    res_date = issue['fields']['resolutiondate']
                    issue_list[issue['key']]['resolutiondate'] = format_date(res_date)
                except:
                    issue_list[issue['key']]['resolutiondate'] = None 
                try:
                    up_date = issue['fields']['updated']
                    issue_list[issue['key']]['updatedate'] = format_date(up_date)
                except:
                    issue_list[issue['key']]['update'] = None 
                try:
                    due_date = issue['fields']['duedate']
                    issue_list[issue['key']]['duedate'] = format_date(due_date)
                except:
                    issue_list[issue['key']]['duedate'] = None 
                try:
                    issue_list[issue['key']]['watchcount'] = issue['fields']['watches']['watchCount'] 
                except:
                    issue_list[issue['key']]['watchcount'] = None
                try:
                    issue_list[issue['key']]['aggregatetimespent'] = issue['fields']['aggregatetimespent'] 
                except:
                    issue_list[issue['key']]['aggregatetimespent'] = None
                try:
                    issue_list[issue['key']]['timespent'] = issue['fields']['timespent'] 
                except:
                    issue_list[issue['key']]['timespent'] = None
                try:
                    issue_list[issue['key']]['timeestimate'] = issue['fields']['timeestimate'] 
                except:
                    issue_list[issue['key']]['timeestimate'] = None
                try:
                    issue_list[issue['key']]['votes'] = issue['fields']['votes']['votes']
                except:
                    issue_list[issue['key']]['votes'] = None
                try:
                    issue_list[issue['key']]['reporter'] = issue['fields']['reporter']['name']
                except:
                    issue_list[issue['key']]['reporter'] = None
                try:
                    issue_list[issue['key']]['creator_name'] = issue['fields']['creator']['name']
                except:
                    issue_list[issue['key']]['creator_name'] = None
                try:
                    issue_list[issue['key']]['creator_active'] = issue['fields']['creator']['active']
                except:
                    issue_list[issue['key']]['creator_active'] = None
                try:
                    issue_list[issue['key']]['assignee'] = issue['fields']['assignee']['name']
                except:
                    issue_list[issue['key']]['assignee'] = None
                try:
                    issue_list[issue['key']]['aggregatetimeestimate'] = issue['fields']['aggregatetimeestimate']
                except:
                    issue_list[issue['key']]['aggregatetimeestimate'] = None
                try:
                    issue_list[issue['key']]['versions'] = [item['name'] for item in issue['fields']['versions']]
                except:
                    issue_list[issue['key']]['versions'] = None
                try:
                    issue_list[issue['key']]['fixversions'] = [item['name'] for item in issue['fields']['fixVersions']]
                except:
                    issue_list[issue['key']]['fixversions'] = None
                try:
                    issue_list[issue['key']]['progresspercent'] = 100*issue['fields']['progress']['progress']/issue['fields']['progress']['total']
                except:
                    issue_list[issue['key']]['progresspercent'] = None
            
    return issue_list

def commit_selector_heuristic(commits):
    """ Helper method for find_bug_fixes.
    Commits are assumed to be ordered in reverse chronological order.
    Given said order, pick first commit that does not match the pattern.
    If all commits match, return newest one. """
    for commit in commits:
        if not re.search('[Mm]erge|[Cc]herry|[Nn]oting', commit):
            return commit
    return commits[0]


if __name__ == '__main__':
    """ Main method """
    parser = argparse.ArgumentParser(description="""Identify bugfixes. Use this script together with a
                                                    gitlog.json and a path with issues. The gitlog.json
                                                    is created using the git_log_to_array.py script and
                                                    the issue directory is created and populated using
                                                    the fetch.py script.""")
    parser.add_argument('--gitlog', type=str,
                        help='Path to json file containing gitlog')
    parser.add_argument('--issue-list', type=str,
                        help='Path to directory containing issue json files')
    parser.add_argument('--gitlog-pattern', type=str,
                        help='Pattern to match a bugfix')
    parser.add_argument('--save-path', type=str,
                        help='Path to write issue_list.json')
    args = parser.parse_args()

    find_bug_fixes(args.issue_list, args.gitlog, args.gitlog_pattern, args.save_path)
