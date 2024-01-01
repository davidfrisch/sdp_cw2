import os

"""
    SPECIFIC TO JAVA
    This file contains functions to parse JAVA files and extract test files and target files
"""
def get_unit_test_files(repo_path):
    test_files = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if "test" in file.lower() and file.endswith(".java"):
                  test_files.append({"file": os.path.join(root, file), "name": file})

    # remove with same name
    unique_test_files = []
    for test_file in test_files:
        if test_file["name"] not in [x["name"] for x in unique_test_files]:
            unique_test_files.append(test_file)

    unique_test_files = [x["file"] for x in unique_test_files]        
    print("Total number of test files: ", len(unique_test_files))
    return unique_test_files



def select_best_target_file(test_file, target_files):
    """
        Given a test file, select the best target file
    """
    # Get the directory of the test file
    # Take the target name closest to the test file name
    test_directory = test_file.split("/")
    candiate_score = []
    for candidate_index in range(len(target_files)):
        candidate = target_files[candidate_index]
        candidate_directory = candidate.split("/")
        score = 0
        for index in range(len(test_directory)):
            if test_directory[index] == candidate_directory[index]:
                score += 1
            else:
                break
        candiate_score.append(score)
    
    # Get the candidate with the highest score
    max_score = max(candiate_score)
    max_score_index = candiate_score.index(max_score)
    return target_files[max_score_index]



def get_target_files(repo_path, all_test_files):
    """
        Given a list of test files, find the corresponding target files
    """
    map_files = []
    test_files = list(set(all_test_files))
    for test_file in test_files:
        # Find the corresponding target file
        target_candidate = []
        for root, dirs, files in os.walk(repo_path):
            # For each files in a directory
            for file in files:
                if file.endswith(".java"):
                    if test_file.split("/")[-1].replace("Test", "") == file.split("/")[-1]:
                        test_file_name = test_file.split("/")[-1]
                        target_candidate.append(os.path.join(root, file))
                        break

        if len(target_candidate) == 0:
            continue

        if len(target_candidate) == 1:
            map_files.append({'target': target_candidate[0].split("/")[-1], 'test': test_file_name, 'test_path': test_file, 'target_path': target_candidate[0]})
                        
        if len(target_candidate) > 1:
            best_target_file = select_best_target_file(test_file, target_candidate)
            map_files.append({'target': best_target_file.split("/")[-1], 'test': test_file_name, 'test_path': test_file, 'target_path': best_target_file})
        
        
    map_witout_duplicates = drop_occurences(map_files)
    return map_witout_duplicates


def drop_occurences(map_files):
    """
        Drop occurences of target files with more than 1 occurence.
    """
    target_occurences = {}
    for map_ in map_files:
        target = map_['target']
        test_path = map_['test_path']

        if target not in target_occurences:
            target_occurences[target] = { 'occurences': 0, 'test_files': [] }
            target_occurences[target]['test_files'].append(test_path)

        target_occurences[target]['occurences'] += 1
        target_occurences[target]['test_files'].append(test_path)
    
    # only show occurences with mroe than 1
    target_occurences = {k: v for k, v in target_occurences.items() if v['occurences'] > 1}

    target_occurences = list(target_occurences.keys())

    # drop occurences
    new_map = []
    for map_ in map_files:
        target = map_['target']
        if target not in target_occurences:
            new_map.append(map_)

    print("Total number of test/target pairs:", len(new_map))
    return new_map
      
