import json
from CONST import *
import pandas as pd
import pydriller as git
import os

def tocsv(project_id):
    path = os.path.join(ABS_SAVE_PATH, project_id, 'fix_and_introducers_pairs.json')
    file = open(path, 'r')
    table = pd.read_json(file, orient="values")
    try:
        table.columns = ["FAULT_FIXING_COMMIT_HASH", "FAULT_INDUCING_COMMIT_HASH"] 
    except:
        return
    
    table.insert(0, 'PROJECT_ID', project_id)

    return table

if __name__ == "__main__":
    proj = []
    for key in PROJECTS:
        try:
            print(key)
            proj.append(tocsv(key))
        except:
            continue
    all_data = pd.concat(proj)
    save_file = os.path.join(ABS_SAVE_PATH, 'fix_and_introducers_pairs.csv')
    all_data.to_csv(save_file, index=False)
