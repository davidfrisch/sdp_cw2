
from fs_utils import get_first_sha, get_shas_with_dates
from process_metrics import get_code_churn_file, get_added_lines


def get_test_history(repo_path, map_files):
    """
    Returns a list of test files that were created before the target file, 
            a list of test files that were created after the target file, 
            and a list of test files that were created at the same time as the target file.
    """
    test_files_created_before_target = []
    test_files_created_after_target = []
    test_files_created_same_time_as_target = []
    for pair in map_files:
        test_file = pair['test']
        target_file = pair['target']
        # get the first commit of the test file
        _, test_date = get_first_sha(repo_path, test_file)
        _, target_date = get_first_sha(repo_path, target_file)
        if test_date < target_date:
            test_files_created_before_target.append({'test': test_file, 'target': target_file, 'test_date': test_date, 'target_date': target_date})
        elif test_date > target_date:
            test_files_created_after_target.append({'test': test_file, 'target': target_file, 'test_date': test_date, 'target_date': target_date})
        else:
            test_files_created_same_time_as_target.append({'test': test_file, 'target': target_file, 'test_date': test_date, 'target_date': target_date})
        
    return test_files_created_before_target, test_files_created_same_time_as_target, test_files_created_after_target


    
def get_diff_of_file(repo_path, file):
    """
    Returns a list of commits that modified the file.
    """

    relative_file_path = file.replace(repo_path+"/", "")
    shas_with_dates = get_shas_with_dates(repo_path, file)
    data = []
    for sha_date in shas_with_dates:
        commit = sha_date['commit']
        count, maximum, average = get_code_churn_file(repo_path, commit, commit, relative_file_path)
        data.append({"file": file, "commit": commit, "date": sha_date['date'], "count": count, "maximum": maximum, "average": average})

    return data


def get_added_lines_file(repo_path, file):
    """
    Returns a list of commits that modified the file.
    """

    relative_file_path = file.replace(repo_path+"/", "")
    shas_with_dates = get_shas_with_dates(repo_path, file)
    data = []
    for sha_date in shas_with_dates:
        commit = sha_date['commit']
        stats_lines = get_added_lines(repo_path, commit, commit, relative_file_path)

        data.append({"file": file, "commit": commit, "date": sha_date['date'],
                      "lines_count": stats_lines['lines_count'], 
                    "lines_added_count": stats_lines['lines_added_count'], 
                    "lines_added_max": stats_lines['lines_added_max'], 
                    "lines_added_avg": stats_lines['lines_added_avg'],
                    "lines_removed_count": stats_lines['lines_removed_count'],
                    "lines_removed_max": stats_lines['lines_removed_max'],
                    "lines_removed_avg": stats_lines['lines_removed_avg']              
                    })

    return data





   
    
  