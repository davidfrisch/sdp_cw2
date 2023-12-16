from pydriller.metrics.process.change_set import ChangeSet
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller.metrics.process.lines_count import LinesCount

def get_change_set(repo_path, from_commit, to_commit):
    metrics = ChangeSet(path_to_repo=repo_path,
                        from_commit=from_commit,
                        to_commit=to_commit)

    count = metrics.count()
    maximum = metrics.max()
    average = metrics.avg()
    return count, maximum, average


def get_code_churn_file(repo_path, from_commit, to_commit, file):
    metric = CodeChurn(path_to_repo=repo_path,
                        from_commit=from_commit,
                        to_commit=to_commit)

    files_count = metric.count()
    files_max = metric.max()
    files_avg = metric.avg()

    if file not in files_count.keys():
        print('File {} not found in the repository'.format(file))
        return

    file_count = files_count[file]
    file_max = files_max[file]
    file_avg = files_avg[file]

    return file_count, file_max, file_avg



def get_added_lines(repo_path, from_commit, to_commit, file):
    metric = LinesCount(path_to_repo=repo_path,
                        from_commit=from_commit,
                        to_commit=to_commit)

    count = metric.count()

    added_count = metric.count_added()
    added_max = metric.max_added()
    added_avg = metric.avg_added()

    removed_count = metric.count_removed()
    removed_max = metric.max_removed()
    removed_avg = metric.avg_removed()

    if file not in added_count.keys():
        print('File {} not found in the repository'.format(file))
        return
    
    lines_added_count = added_count[file]
    lines_added_max = added_max[file]
    lines_added_avg = added_avg[file]

    lines_removed_count = removed_count[file]
    lines_removed_max = removed_max[file]
    lines_removed_avg = removed_avg[file]

    lines_count = count[file]
    

    return {"lines_count": lines_count, 
            "lines_added_count": lines_added_count, 
            "lines_added_max": lines_added_max, 
            "lines_added_avg": lines_added_avg,
            "lines_removed_count": lines_removed_count,
            "lines_removed_max": lines_removed_max,
            "lines_removed_avg": lines_removed_avg                  
            }