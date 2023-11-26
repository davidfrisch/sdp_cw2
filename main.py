from pydriller import Repository
import os
from pydriller.metrics.process.change_set import ChangeSet
from subprocess import Popen, PIPE
from datetime import datetime
from pydriller.metrics.process.commits_count import CommitsCount

repo_test_path = "/mnt/data/apache_repos/spark"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", 
          "Oct", "Nov", "Dec"]
MONTHS = {i+1: MONTHS[i] for i in range(len(MONTHS))}


def count_test_commits(repo_path):
    count = 0
    year_month = {}
    # new file to store the commits that contain "test"
    file = open("test_commits.txt", "w")
    for commit in Repository(repo_path).traverse_commits():
        # count number of test files added per month
        month = commit.author_date.month
        year = commit.author_date.year
        if year not in year_month:
            year_month[year] = {}
        if month not in year_month[year]:
            year_month[year][month] = 0



        if " test " in commit.msg.lower():
            year_month[year][month] += 1
            count += 1
            file.write(commit.hash + "\n")
            file.write(commit.msg + "\n")
            file.write("\n")



    for year in year_month:
        for month in year_month[year]:
            print(year, MONTHS[month], year_month[year][month])

    print("Total number of commits: ", count)


# count how many pom.xml files are in the repo
def count_pom_files(repo_path):
    count = 0
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file == "pom.xml":
                # if the content of the file contains "test"
                if "test" in open(os.path.join(root, file)).read().lower():
                    print(os.path.join(root, file))
                    count += 1

    print("Total number of pom.xml files: ", count)

def count_scala_test_files(repo_path):
    count = 0
    test_files = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith("Suite.scala"):
                if "test(" in open(os.path.join(root, file)).read().lower():
                    test_files.append(os.path.join(root, file))

    #remove duplicates
    test_files = list(set(test_files))
    source_files = {}
    for test_file in test_files:
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".scala"):
                    if test_file.split("/")[-1].replace("Suite", "") == file.split("/")[-1]:
                        source_files[test_file] = os.path.join(root, file)
                        break

    # remove duplicates
    print("Total number of source files: ", len(source_files))
    print("Total number of scala test files: ", len(test_files))
    return source_files
    # print("Total number of source files: ", len(source_files))
# check when 

def statistics_of_file(repo_path, filename):
    first_commit = "79515b82f1e8a9c04d7ac9f49095f0d206df5812"
    last_commit = "295c615b16b8a77f242ffa99006b4fb95f8f3487"
    metric = ChangeSet(path_to_repo=repo_path,
                   from_commit=first_commit,
                   to_commit=last_commit)

    maximum = metric.max()
    average = metric.avg()
    print('Maximum number of files committed together: {}'.format(maximum))
    print('Average number of files committed together: {}'.format(average))



# def take_all_test_files_created_before_source_files(repo_path):
    



def info_test_file_before_source_file(repo, test_file, source_file):
    cmd =f"git log -p -- {test_file}"
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, cwd=repo)
    stdout, stderr = p.communicate()
    stdout = stdout.decode("utf-8")
    # find the line that contains the commit hash
    lines = stdout.split("\n")
    commits = []
    dates = []
    for line in lines:
        # take the first commit and date 
        if line.startswith("commit"):
            commits.append(line.split(" ")[1])
        if line.startswith("Date"):
            dates.append(line.split("Date:")[1].strip())

    
            
    if len(commits) != len(dates):
        print("Error: commits and dates are not the same length")
        return
    
    first_commit_test = commits[-1]
    last_commit_test = commits[0]

    # get the date of the first commit
    cmd =f"git log -p -- {source_file}"
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, cwd=repo)
    stdout, stderr = p.communicate()
    stdout = stdout.decode("utf-8")
    # find the line that contains the commit hash
    lines = stdout.split("\n")
    commits_source = []
    dates_source = []
    for line in lines:
        # take the first commit and date 
        if line.startswith("commit"):
            commits_source.append(line.split(" ")[1])
        if line.startswith("Date"):
            dates_source.append(line.split("Date:")[1].strip())

    first_commit_source = commits_source[-1]
    last_commit_source = commits_source[0]

    # check if the first commit of the test file is before the first commit of the source file  Sat Aug 31 19:27:07 2013 -0700
    if datetime.strptime(dates[-1], "%a %b %d %H:%M:%S %Y %z") < datetime.strptime(dates_source[-1], "%a %b %d %H:%M:%S %Y %z"):
        print(f"test file: {test_file}")
        print(f"from commit test: {first_commit_test} date: {dates[-1]}")
        print(f"to commit source: {first_commit_source} date: {dates_source[-1]}")
      
    

    # print(stdout)
    # take the first commit and date
    
""" 
First commit:  e1dc853737fc1739fbb5377ffe31fb2d89935b1f
Last commit:  7120e6b88f2327ffb71c4bca14b10b15aeb26c32
 """

if __name__ == "__main__":
    # see_commit_dates_of_file(repo_test_path, "/mnt/data/apache_repos/spark/sql/core/src/test/scala/org/apache/spark/sql/execution/command/TruncateTableParserSuite.scala")
    # count_pom_files(repo_test_path)
    # count_test_commits(repo_test_path)
    source_test_files = count_scala_test_files(repo_test_path)
    for test_file in source_test_files:
        info_test_file_before_source_file(repo_test_path, test_file, source_test_files[test_file])
    #     "/mnt/data/apache_repos/spark/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/analysis/ResolveUnion.scala", 
    #     "/mnt/data/apache_repos/spark/sql/catalyst/src/test/scala/org/apache/spark/sql/catalyst/analysis/ResolveUnionSuite.scala"
    # )