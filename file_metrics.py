from process_metrics import get_code_churn_file

def get_history_files(map_files, repo_path):
    """
    Returns a list of test files that were created before the target file, 
            a list of test files that were created after the target file, 
            a list of test files that were created at the same time as the target file during a merge
            and a list of test files that were created at the same time as the target file.
    """
    test_files_created_before_target = []
    test_files_created_after_target = []
    test_files_created_same_time_as_target = []
    for pair in map_files:
        test_file = pair['test']
        target_file = pair['target']
        test_files_merged = []
        for event in test_file:
            if (str(event["change_type"])) == "MERGE":
                test_files_merged.append(event['commit'].hash)
        
        test_target_merged = []
        for event in target_file:
            if (str(event["change_type"])) == "MERGE":
                if event['commit'].hash in test_files_merged:
                    test_target_merged.append(event)

        if len(test_file) == 0 or len(target_file) == 0:
            continue
        
        first_test_date = test_file[0]['commit'].committer_date
        first_target_date = target_file[0]['commit'].committer_date

        first_test_hash = test_file[0]['commit'].hash
        first_target_hash = target_file[0]['commit'].hash
        test_file_name = test_file[0]['filename']
        target_file_name = target_file[0]['filename']
       
        test_code_churn,_,_ = get_code_churn_file(repo_path, first_test_hash, first_test_hash, test_file_name)
        target_code_churn,_,_ = get_code_churn_file(repo_path, first_target_hash, first_target_hash, target_file_name)

        test_code_churn = test_code_churn if isinstance(test_code_churn, int) else 0
        target_code_churn = target_code_churn if isinstance(target_code_churn, int) else 0

        if first_test_date < first_target_date:
            test_files_created_before_target.append({'test': test_file, 'target': target_file, 'first_test_date': first_test_date, 'first_target_date': first_target_date, 'merges': test_target_merged, 'test_code_churn': test_code_churn, 'target_code_churn': target_code_churn})
        elif first_test_date > first_target_date:
            test_files_created_after_target.append({'test': test_file, 'target': target_file, 'first_test_date': first_test_date, 'first_target_date': first_target_date, 'merges': test_target_merged, 'test_code_churn': test_code_churn, 'target_code_churn': target_code_churn})
        else:
            test_files_created_same_time_as_target.append({'test': test_file, 'target': target_file, 'first_test_date': first_test_date, 'first_target_date': first_target_date, 'merges': test_target_merged, 'test_code_churn': test_code_churn, 'target_code_churn': target_code_churn})
        
    return test_files_created_before_target, test_files_created_same_time_as_target, test_files_created_after_target


def get_avg_code_churn_test_target(map_files):
    """
      The function computes the average code churn for files with 'target_code_churn' and 'test_code_churn' values, 
      returning the average for each one.
    """
    all_code_churn_test = []
    all_code_churn_target = []
    for i in range(len(map_files)):
        test_churn_value = map_files[i]['test_code_churn']
        target_churn_value = map_files[i]['target_code_churn']
        all_code_churn_test.append(test_churn_value)
        all_code_churn_target.append(target_churn_value)

    avg_test = sum(all_code_churn_test) / len(all_code_churn_test) if len(all_code_churn_test) > 0 else 0
    avg_target = sum(all_code_churn_target) / len(all_code_churn_target) if len(all_code_churn_target) > 0 else 0
    return avg_test, avg_target


def get_avg_code_churn_sum(map_files):
    """
      The function computes the average code churn for files with 'target_code_churn' and 'test_code_churn' values, 
      returning the overall average.
    """
    average = []
    for i in range(0, len(map_files)):
        value_target_code_churn = map_files[i]['target_code_churn'] if isinstance(map_files[i]['target_code_churn'], int) else 0
        value_test_code_churn = map_files[i]['test_code_churn'] if isinstance(map_files[i]['test_code_churn'], int) else 0
        average.append((value_target_code_churn + value_test_code_churn) / 2)

    return sum(average) / len(average) if len(average) > 0 else 0
