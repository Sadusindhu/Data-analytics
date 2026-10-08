"""
Script: prepare_git_push.py
Clones Sadusindhu/Data-analytics, copies mini project-2 into mini-project-2/,
and commits it ready for pushing.
"""

import os
import shutil
import subprocess

def prepare():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    repo_sync_dir = os.path.join(base_dir, "_repo_sync")
    
    if os.path.exists(repo_sync_dir):
        shutil.rmtree(repo_sync_dir)
        
    print(f"Cloning https://github.com/Sadusindhu/Data-analytics.git into {repo_sync_dir}...")
    subprocess.run(["git", "clone", "https://github.com/Sadusindhu/Data-analytics.git", repo_sync_dir], check=True)
    
    dest_folder = os.path.join(repo_sync_dir, "mini-project-2")
    
    # Copy files
    print("Copying mini project-2 files...")
    shutil.copytree(
        base_dir, 
        dest_folder, 
        ignore=shutil.ignore_patterns("_repo_sync", "temp_repo", "*.tmp", ".git")
    )
    
    # Configure author and commit
    subprocess.run(["git", "-C", repo_sync_dir, "config", "user.name", "SADU VENKATA NAGA SAI DURGA SINDHU"], check=True)
    subprocess.run(["git", "-C", repo_sync_dir, "config", "user.email", "venkatanaga380@gmail.com"], check=True)
    subprocess.run(["git", "-C", repo_sync_dir, "add", "."], check=True)
    subprocess.run([
        "git", "-C", repo_sync_dir, "commit", "-m", 
        "Add Mini Project 2: Customer Churn Analysis (datasets, analysis, visualizations, Power BI dashboard, and project report)"
    ], check=True)
    
    print("\nCommit created successfully in _repo_sync!")
    subprocess.run(["git", "-C", repo_sync_dir, "log", "-n", "2", "--oneline"], check=True)

if __name__ == "__main__":
    prepare()
