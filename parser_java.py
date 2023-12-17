import os

"""
    SPECIFIC TO JAVA
    This file contains functions to parse JAVA files and extract test files and target files
"""


def get_unit_test_files(repo_path):
    test_files = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
          if "/test" in root and file.endswith("Test.java"):
              test_files.append(os.path.join(root, file))
          #replace with regex
          elif "test" in file.lower() and file.endswith(".java"):
              test_files.append(os.path.join(root, file))

    unique_test_files = list(set(test_files))
    print("Total number of test files: ", len(unique_test_files))
    return unique_test_files

def get_target_files(repo_path, all_test_files):
    map_files = []
    test_files = list(set(all_test_files))
    for test_file in test_files:
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".java"):
                    if test_file.split("/")[-1].replace("Test", "") == file.split("/")[-1]:
                        test_file_name = test_file.split("/")[-1]
                        map_files.append({'target': file, 'test': test_file_name})
                        break

    print("Total number of target files found: ", len(map_files))
    return map_files

