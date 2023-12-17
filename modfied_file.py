from pydriller import Repository


def get_modifications_of_files(repo_path, files):
    """
    Returns the list of modifications of a file in a repository.
    :param repo_path: path to the repository
    :param files: list of paths to the files
    :return: list of modifications
    """

    files_names = [file.split("/")[-1] for file in files]
    files = {file: [] for file in files_names}

    for commit in Repository(repo_path).traverse_commits():
        for m in commit.modified_files:
            if m.filename in files_names:
                files[m.filename].append({'commit': commit, 
                                      'filename': m.filename,
                                      'change_type': m.change_type,
                                      'diff_parsed': m.diff_parsed,
                                      'added_lines': m.added_lines,
                                      'deleted_lines': m.deleted_lines,
                                      'nloc': m.nloc,
                                      'complexity': m.complexity,
                                      'token_count': m.token_count,
                                      })


    return files



