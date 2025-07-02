# agents/diff_analyst.py
from langchain_core.tools import tool
from typing import Dict, Any

@tool
def analyze_diff(input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyzes code churn and flags risky commits based on total additions and deletions.
    """
    commits = input.get("github_data", [])
    if not isinstance(commits, list):
        raise ValueError(f"❌ Expected 'github_data' to be a list of commits, got {type(commits)}: {commits}")

    risky_commits = []
    churn_by_author = {}

    for commit in commits:
        author = commit.get("author")
        additions = commit.get("additions", 0)
        deletions = commit.get("deletions", 0)
        total_churn = additions + deletions

        churn_by_author[author] = churn_by_author.get(author, 0) + total_churn

        if total_churn > 300 or commit.get("files_changed", 0) > 8:
            risky_commits.append({
                "author": author,
                "total_churn": total_churn,
                "files_changed": commit.get("files_changed", 0),
                "timestamp": commit.get("timestamp")
            })

    print("✅ DiffAnalyst analyzed commit data")
    return {
        "author_churn": churn_by_author,
        "risky_commits": risky_commits
    }
