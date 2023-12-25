import os
import time
from constants import list_of_apache_repos
from parser_java import get_unit_test_files, get_target_files 
from file_metrics import  get_history_files
from modfied_file import get_modifications_of_files

def get_before_same_after_test_vs_target(apache_repo, filename):
    all_test_files = get_unit_test_files(apache_repo)
    if len(all_test_files) == 0:
        print("No test files found")
        return

    map_files = get_target_files(apache_repo, all_test_files)
    
    if len(map_files) == 0:
        print("No target files found")
        return
 
    all_files = [map_['test'] for map_ in map_files] + [map_['target'] for map_ in map_files]
    all_files_info = get_modifications_of_files(apache_repo, all_files)

    map_files_info = []
    for map_ in map_files:
        map_files_info.append({
            'test': all_files_info[map_['test']],
            'target': all_files_info[map_['target']]
        })
    # append results in table_1.txt
    map_before, map_same, map_after = get_history_files(map_files_info)
    branch_name = None
    if len(map_before) > 0:
        branch_name = map_before[0]['test'][0]['commit'].branches
    elif len(map_same) > 0:
        branch_name = map_same[0]['test'][0]['commit'].branches
    elif len(map_after) > 0:
        branch_name = map_after[0]['test'][0]['commit'].branches


    print(f"repo: {apache_repo}")
    print(f"before: {len(map_before)}")
    print(f"same: {len(map_same)}")
    print(f"after: {len(map_after)}")
    repo_name = apache_repo.split('/')[-1]
    with open(filename, 'a') as f:
       f.write(f"{repo_name}\t{branch_name}\t{len(all_test_files)}\t{len(map_files)}\t{len(map_before)}\t{len(map_same)}\t{len(map_after)}\n")





current_time = time.time()
filename = f"table_1_{current_time}.csv"
with open(filename, 'w') as f:
    f.write('name\tbranch_name\ttotal_test_files\ttotal_target_files\tfirst_before\tfirst_same\tfirst_after\n')

for repo_url in list_of_apache_repos[:1]:
    base_apache_repos = "/mnt/data/apache_repos/"
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    repo = os.path.join(base_apache_repos, repo_name)
    get_before_same_after_test_vs_target(repo, filename)