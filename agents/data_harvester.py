# agents/data_harvester.py
from langchain_core.tools import tool
from typing import Dict, Any

@tool
def fetch_github_data(input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates fetching commit data from GitHub.
    Returns a dictionary with a list of commit dictionaries.
    """
    # Dummy commit data
    commits = [
        {
            "author": "alice",
            "additions": 120,
            "deletions": 30,
            "files_changed": 3,
            "timestamp": "2025-06-30T12:00:00Z"
        },
        {
            "author": "bob",
            "additions": 200,
            "deletions": 150,
            "files_changed": 10,
            "timestamp": "2025-06-30T13:00:00Z"
        },
        {
            "author": "alice",
            "additions": 80,
            "deletions": 20,
            "files_changed": 2,
            "timestamp": "2025-06-30T14:00:00Z"
        },
    ]
    return {"github_data": commits}
