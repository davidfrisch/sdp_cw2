
def get_history_files(map_files):
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

        if len(test_file) == 0 or len(target_file) == 0:
            continue

        first_test_date = test_file[0]['commit'].committer_date
        first_target_date = target_file[0]['commit'].committer_date

        if first_test_date < first_target_date:
            test_files_created_before_target.append({'test': test_file, 'target': target_file, 'first_test_date': first_test_date, 'first_target_date': first_target_date})
        elif first_test_date > first_target_date:
            test_files_created_after_target.append({'test': test_file, 'target': target_file, 'first_test_date': first_test_date, 'first_target_date': first_target_date})
        else:
            test_files_created_same_time_as_target.append({'test': test_file, 'target': target_file, 'first_test_date': first_test_date, 'first_target_date': first_target_date})
        
    return test_files_created_before_target, test_files_created_same_time_as_target, test_files_created_after_target







   
    
  