# Absolute path to the directory where projects are cloned
ABS_REPO_PATH = None 
# Absoluta path to the output folder
ABS_SAVE_PATH = None
# Link to the Jira issues tracker (assumes all projects are
# from the same developer)
JIRA_LINK = None 
# A regex used to identify fixing commit messages,
# where 'proj' is the placeholder for project ID in Jira
# and 'nbr' is the placeholder for issue number                 
FIX_STRING = '\[?{proj}-{nbr}\]?\D'
# A dictionary where the keys are the projects' names (repo folders)
# and values are their Jira project ids
PROJECTS = None
