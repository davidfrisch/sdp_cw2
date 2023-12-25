from pydriller import Repository
import os
def git_see_merge(repo_path, hash):
    show_result = os.popen(f"cd {repo_path} && git show --numstat {hash}").read()
    if show_result == "":
        return
    
    show_results_arrays = show_result.split("\n")
    all_files_changes = []
    for line in show_results_arrays:
        if ".java" in line:
            added_lines, deleted_lines, file = line.split("\t")
            filename = file.split("/")[-1].strip()
            added_lines = int(added_lines)
            deleted_lines = int(deleted_lines)
            all_files_changes.append({
                'filename': filename,
                'added_lines': added_lines,
                'deleted_lines': deleted_lines,
                'merge': True
            })
            
    return all_files_changes

def  get_modifications_of_files(repo_path, files):
    """
    Returns the list of modifications of a file in a repository.
    :param repo_path: path to the repository
    :param files: list of paths to the files
    :return: list of modifications
    """

    files_names = [file.split("/")[-1] for file in files]
    files = {file: [] for file in files_names}

    

    for commit in Repository(repo_path).traverse_commits():
        if commit.merge:
            all_files_changes = git_see_merge(repo_path, commit.hash)
            for file_changes in all_files_changes:
                if file_changes['filename'] in files_names:
                      files[file_changes['filename']].append({'commit': commit, 
                                      'filename': file_changes['filename'],
                                      'change_type': "MERGE",
                                      'added_lines': file_changes['added_lines'],
                                      'deleted_lines': file_changes['deleted_lines'],
                                      'size': file_changes['added_lines'] + file_changes['deleted_lines'],
                                      'nloc': None,
                                      'complexity': None,
                                      'token_count': None,
                                      'number_methods': None,
                                      'number_methods_before': None,
                                      })

      
        for m in commit.modified_files:
            if m.filename in files_names:
                files[m.filename].append({'commit': commit, 
                                      'filename': m.filename,
                                      'change_type': m.change_type,
                                      'added_lines': m.added_lines,
                                      'deleted_lines': m.deleted_lines,
                                      'size': m.added_lines + m.deleted_lines,
                                      'nloc': m.nloc,
                                      'complexity': m.complexity,
                                      'token_count': m.token_count,
                                      'number_methods': len(m.methods),
                                      'number_methods_before': len(m.methods_before),
                                      })


    return files
