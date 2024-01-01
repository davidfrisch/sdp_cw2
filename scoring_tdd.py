
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

What does it mean "A phase that did not follow TDD"?

* The metric of the target file has increased on a commit but not the test file

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

        if test_value[i] > test_value[i-1] and target_value[i] >= target_value[i-1]:
            score += 1
  
    return score


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

        if test_value[i] <= test_value[i-1] and target_value[i] > target_value[i-1]:
            score -= 1
  
    return score


def __tdd_score_pair(test, target):
    list_of_metric = ["number_methods", "added_lines"] 
    metric_score = {} 
    for metric in list_of_metric:
        pos_score = 0
        neg_score = 0
        merge_history = __merge_history_test_vs_target(test, target, metric)
        pos_score += __pos_evaluation_increased_from_previous_commit(merge_history)
        neg_score += __neg_evaluation_target_has_increased_but_test_has_not(merge_history)
        metric_score[metric] = {"pos_score": pos_score, "neg_score": neg_score}

    return metric_score


def tdd_score(map_files, output_filename):
    if len(map_files) == 0:
        return None

    all_scores = {}
    for map_ in map_files:
        metric_scores = __tdd_score_pair(map_['test'], map_['target'])
        all_scores[map_['target'][0]['filename']] = metric_scores

    avg_pos_number_methods = np.mean([x['number_methods']['pos_score'] for x in all_scores.values()])
    avg_neg_number_methods = np.mean([x['number_methods']['neg_score'] for x in all_scores.values()])
    avg_pos_added_lines = np.mean([x['added_lines']['pos_score'] for x in all_scores.values()])
    avg_neg_added_lines = np.mean([x['added_lines']['neg_score'] for x in all_scores.values()])
    return avg_pos_number_methods, avg_neg_number_methods, avg_pos_added_lines, avg_neg_added_lines