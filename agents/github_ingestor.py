# agents/github_ingestor.py
from langchain_core.tools import tool
import requests
from typing import Dict, Any
from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@tool
def fetch_commits_api(input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Pulls latest commits from a GitHub repo using GitHub API.
    Input must contain 'owner' and 'repo'.
    """
    owner = input["owner"]
    repo = input["repo"]
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Step 1: Get list of recent commits (first page, latest 30)
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"❌ GitHub API error: {response.status_code}, {response.text}")
    
    parsed_commits = []
    commits = response.json()

    # Step 2: For each commit, fetch detailed stats via /commits/{sha}
    for commit in commits:
        sha = commit.get("sha")
        author = commit.get("author", {}).get("login", "unknown")
        timestamp = commit.get("commit", {}).get("author", {}).get("date")

        commit_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}"
        stats_response = requests.get(commit_url, headers=headers)

        if stats_response.status_code != 200:
            print(f"⚠️ Failed to fetch stats for commit {sha}")
            continue

        stats_data = stats_response.json()
        additions = stats_data.get("stats", {}).get("additions", 0)
        deletions = stats_data.get("stats", {}).get("deletions", 0)
        files_changed = len(stats_data.get("files", []))

        parsed_commits.append({
            "author": author,
            "timestamp": timestamp,
            "additions": additions,
            "deletions": deletions,
            "files_changed": files_changed
        })

    print(f"✅ GitHub data fetched: {len(parsed_commits)} commits with stats")
    return {"github_data": parsed_commits}
