import os
import sys
from constants import list_random_repos_apache_java_100_forks

def git_clone(repo_url):
  if not os.path.exists(apache_dir):
    os.makedirs(apache_dir)

  for repo_url in list_random_repos_apache_java_100_forks:
    repo_name = repo_url.split("/")[-1].split(".")[0]
    repo_path = os.path.join(apache_dir, repo_name)
    if not os.path.exists(repo_path):
      os.system(f"git clone {repo_url} {repo_path}")
    else:
      print(f"{repo_path.split('/')[-1]} already exists")
  

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.realpath(__file__))
    apache_dir = os.path.join(base_dir, "..","apache_repos")
    git_clone(list_random_repos_apache_java_100_forks)