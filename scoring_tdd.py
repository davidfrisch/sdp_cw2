
""" 
This test is to score if a target and its file follows the TDD rules.

From the TDD rules of the description of the CW :
"In Test-Driven-Development, tests are written before the tested code. If a project adopted TDD, the git repository
should reflect this. If a new class (file) is created, then the same or an earlier commit should also create a new
test class (file)."

Rules:

X is the total number of commits of the test and target file.
Y the number of phases that followed TDD
N the number of phases that did not follow TDD

By looking at the metrics:
Metrics are: number_methods, nloc, added_lines, complexity

What does it mean "A phase that followed TDD"?
* A commit where the test file and the target file has been changed
  and the metric of the test file and the target file has increased.

* A commit where the test file and the target file has been changed

* The metric of the test file has increased on commit i 
  and the metric of the target file has increased on commit i+1 but not the test file.

What does it mean "A phase that did not follow TDD"?

* The metric of the target file has increased on a commit i but not the test file

"""

import numpy as np

def __merge_history_test_vs_target(test, target, metric):
    test_file_no_rename = [x for x in test if "RENAME" not in str(x['change_type'])]
    target_file_no_rename = [x for x in target if "RENAME" not in str(x['change_type'])]

    test_file = [(x['commit'].committer_date, x[metric]) for x in test_file_no_rename]
    target_file = [(x['commit'].committer_date, x[metric]) for x in target_file_no_rename]

    test_file.sort(key=lambda x: x[0])
    target_file.sort(key=lambda x: x[0])

    test_file_dates = [x[0] for x in test_file]
    test_file_values = [x[1] for x in test_file]

    target_file_dates = [x[0] for x in target_file]
    target_file_values = [x[1] for x in target_file]

    all_dates = sorted(list(set(test_file_dates + target_file_dates)))
    x_axis = np.arange(len(all_dates))

    test_file_values = [test_file_values[test_file_dates.index(x)] if x in test_file_dates else 0 for x in all_dates]
    target_file_values = [target_file_values[target_file_dates.index(x)] if x in target_file_dates else 0 for x in all_dates]

    return x_axis, test_file_values, target_file_values


def __pos_evaluation_increased_from_previous_commit(commit_history):
    x_axis, test_value, target_value = commit_history
    score = 0
    for i in range(len(x_axis)):
        if i == 0:
            continue
        if not isinstance(test_value[i], int) or not isinstance(test_value[i-1], int):
            continue
        
        if not isinstance(target_value[i], int) or not isinstance(target_value[i-1], int):
            continue

        if test_value[i] > test_value[i-1] and target_value[i] > target_value[i-1]:
            score += 1
  
    return score / len(x_axis) if len(x_axis) > 0 else 0


def __pos_evaluation_test_target_on_same_commit(commit_history):
    x_axis, test_value, target_value = commit_history
    score = 0
    for i in range(len(x_axis)):
        if not isinstance(test_value[i], int) or not isinstance(target_value[i], int):
            continue
        
        if test_value[i] > 0 and target_value[i] > 0:
            score += 1
  
    return score / len(x_axis) if len(x_axis) > 0 else 0


def __neg_evaluation_target_has_increased_but_test_has_not(commit_history):
    x_axis, test_value, target_value = commit_history
    score = 0
    for i in range(len(x_axis)):
        if i == 0:
            continue
        if not isinstance(test_value[i], int) or not isinstance(test_value[i-1], int):
            continue
        
        if not isinstance(target_value[i], int) or not isinstance(target_value[i-1], int):
            continue

        if test_value[i] == test_value[i-1] and target_value[i] > target_value[i-1]:
            score -= 1
  
    return score / len(x_axis) if len(x_axis) > 0 else 0


def __tdd_score_pair(test, target):
    list_of_metric = ["number_methods", "nloc", "added_lines", "complexity"]  
    NUMBER_FUNCTIONS_FOR_POS_SCORING = 2
    tmp_sccore = 0
    pos_score = 0
    for metric in list_of_metric:
        merge_history = __merge_history_test_vs_target(test, target, metric)
        pos_score += __pos_evaluation_increased_from_previous_commit(merge_history)
        pos_score += __pos_evaluation_test_target_on_same_commit(merge_history)
        tmp_sccore += pos_score
        tmp_sccore += __neg_evaluation_target_has_increased_but_test_has_not(merge_history)

    percentage_tdd = pos_score / (len(list_of_metric) * NUMBER_FUNCTIONS_FOR_POS_SCORING)    
    return {"tdd_score": tmp_sccore, "percentage": percentage_tdd}


def tdd_score(map_files):
    if len(map_files) == 0:
        return None

    total_score = 0
    tdd_percentange = {}
    for map_ in map_files:
        results = __tdd_score_pair(map_['test'], map_['target'])
        total_score += results['tdd_score']
        tdd_percentange[map_['target'][0]['filename']] = results['percentage']


    average_score = total_score / len(map_files)
    overall_percentage = sum(tdd_percentange.values()) / len(tdd_percentange.values())
    return average_score, overall_percentage