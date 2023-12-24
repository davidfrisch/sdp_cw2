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


def get_matching_target_files(repo_path, all_test_files):
    """
    Finds and maps .java files in the repository that match with test files
    in all_test_files (after removing 'Test' from their names, both from start and end).

    :param repo_path: Path to the repository
    :param all_test_files: List of paths to test files
    :return: List of mappings between test files and their corresponding target .java files
    """
    map_files = []
    test_file_bases = set()

    # Generate base names for matching by removing 'Test' from start or end of the file names
    for f in all_test_files:
        base_name = os.path.basename(f).replace(".java", "")
        if base_name.startswith("Test"):
            test_file_bases.add(base_name[4:])  # Remove 'Test' from start
        elif base_name.endswith("Test"):
            test_file_bases.add(base_name[:-4])  # Remove 'Test' from end

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".java"):
                file_base = file.replace(".java", "")
                if file_base in test_file_bases:
                    # Find the original test file name
                    test_file_name = next((f for f in all_test_files if file_base in f), None)
                    if test_file_name:
                        full_target_file_path = os.path.join(root, file)
                        map_files.append({'target': full_target_file_path, 'test': test_file_name})

    print("Total number of matching target files found: ", len(map_files))
    return map_files