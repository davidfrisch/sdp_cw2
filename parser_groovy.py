import os

"""
    ADAPTED FOR GROOVY
    This file contains functions to parse GROOVY files and extract test files and target files
"""

def get_unit_test_files(repo_path):
    test_files = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if "/test" in root and file.lower().endswith("Test.groovy"):
                test_files.append(os.path.join(root, file))
            #replace with regex
            elif "test" in file.lower() and file.endswith(".groovy"):
                test_files.append(os.path.join(root, file))
            else:
                print("Not a test file: ", file)

    print("Total number of test files: ", len(test_files))
    return test_files

def get_target_files(repo_path, all_test_files):
    map_files = []
    test_files = list(set(all_test_files))
    for test_file in test_files:
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".groovy"):
                    if test_file.split("/")[-1].replace("Test", "") == file.split("/")[-1]:
                        map_files.append({'target': os.path.join(root, file), 'test': test_file})
                        break

    print("Total number of target files found: ", len(map_files))
    return map_files
