from pydriller.metrics.process.code_churn import CodeChurn


def get_code_churn_file(repo_path, from_commit, to_commit, file):
    metric = CodeChurn(path_to_repo=repo_path,
                        from_commit=from_commit,
                        to_commit=to_commit,
                        add_deleted_lines_to_churn=True)
  
    files_count = metric.count()
    files_max = metric.max()
    files_avg = metric.avg()
    full_path_file = None


    for file_path in files_count.keys():
        if isinstance(file_path, str) and file_path.endswith(file):
            full_path_file = file_path
            break

    if full_path_file is None:
        print(f'File {file} not found in the repository'.format(file))
        return None, None, None
    
    file_count = files_count[full_path_file]
    file_max = files_max[full_path_file]
    file_avg = files_avg[full_path_file]

    return file_count, file_max, file_avg
