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

        if first_test_date < first_target_date:
            test_files_created_before_target.append({'test': test_file, 'target': target_file, 'first_test_date': first_test_date, 'first_target_date': first_target_date, 'merges': test_target_merged, 'test_code_churn': test_code_churn, 'target_code_churn': target_code_churn})
        elif first_test_date > first_target_date:
            test_files_created_after_target.append({'test': test_file, 'target': target_file, 'first_test_date': first_test_date, 'first_target_date': first_target_date, 'merges': test_target_merged, 'test_code_churn': test_code_churn, 'target_code_churn': target_code_churn})
        else:
            test_files_created_same_time_as_target.append({'test': test_file, 'target': target_file, 'first_test_date': first_test_date, 'first_target_date': first_target_date, 'merges': test_target_merged, 'test_code_churn': test_code_churn, 'target_code_churn': target_code_churn})
        
    return test_files_created_before_target, test_files_created_same_time_as_target, test_files_created_after_target
