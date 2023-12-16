from subprocess import Popen, PIPE
from datetime import datetime

def get_first_sha(repo_path, file):
    """
    Returns the first commit that modified the file.
    """
    cmd =f"git log -p -- {file}"
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, cwd=repo_path)
    stdout, stderr = p.communicate()
    stdout = stdout.decode("utf-8")
    lines = stdout.split("\n")

    # Note: commits are showns newest to oldest, so we need to reverse the list
    reverse_lines = lines[::-1]
    commit = ""
    date = ""
    for line in reverse_lines:
        # take the first commit and date 
        if line.startswith("commit"):
            commit = line.split(" ")[1]
        if line.startswith("Date"):
            date = datetime.strptime(line.split("Date:")[1].strip(), "%a %b %d %H:%M:%S %Y %z")
        
        if commit != "" and date != "":
            break
        
    return (commit, date)



def get_shas_with_dates(repo_path, file):
    """
    Returns a list of commits that modified the file with the date of the commit.
    Similar as get_first_sha, but returns all commits instead of the first one.
    """
    cmd =f"git log -p -- {file}"
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, cwd=repo_path)
    stdout, stderr = p.communicate()
    stdout = stdout.decode("utf-8")
    # find the line that contains the commit hash
    lines = stdout.split("\n")
    data = []
    for index, line  in enumerate(lines):
        commit = ""
        date = ""
        if line.startswith("commit "):
            commit = line.split(" ")[1]
            date_line = lines[index+2]
            if date_line.startswith("Date:"):
                date_line = lines[index+2]
                date = datetime.strptime(date_line.split("Date:")[1].strip(), "%a %b %d %H:%M:%S %Y %z")
            
        if date != "" and commit != "":
            data.append({"commit": commit, "date": date})
    return data