# scheduled_digest.py

import schedule
import time
import os
import base64
import requests

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from typing import TypedDict, Dict, Any, List

from agents.github_ingestor import fetch_commits_api
from agents.diff_analyst import analyze_diff
from agents.insight_narrator import generate_insight

# 🔐 Slack Env Vars
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

# LangGraph State
class GraphState(TypedDict):
    owner: str
    repo: str
    github_data: List[Dict[str, Any]]
    churn_data: Dict[str, Any]
    summary: str
    chart_base64: str

# Nodes
def fetch_fn(state: Dict[str, Any]) -> Dict[str, Any]:
    github_data = fetch_commits_api.invoke({
        "input": {
            "owner": state["owner"],
            "repo": state["repo"]
        }
    })["github_data"]
    return {**state, "github_data": github_data}

def analyze_fn(state: Dict[str, Any]) -> Dict[str, Any]:
    churn_data = analyze_diff.invoke({
        "input": {
            "github_data": state["github_data"]
        }
    })
    return {**state, "churn_data": churn_data}

def insight_fn(state: Dict[str, Any]) -> Dict[str, Any]:
    insight = generate_insight.invoke({
        "input": {
            "author_churn": state["churn_data"]["author_churn"],
            "risky_commits": state["churn_data"]["risky_commits"]
        }
    })
    return {
        **state,
        "summary": insight["summary"],
        "chart_base64": insight["chart_base64"]
    }

# LangGraph setup
workflow = StateGraph(GraphState)
workflow.add_node("fetch", RunnableLambda(fetch_fn))
workflow.add_node("analyze", RunnableLambda(analyze_fn))
workflow.add_node("insight", RunnableLambda(insight_fn))
workflow.set_entry_point("fetch")
workflow.add_edge("fetch", "analyze")
workflow.add_edge("analyze", "insight")
workflow.add_edge("insight", END)
graph = workflow.compile()

# 📤 Post to Slack
def post_to_slack(summary: str, chart_path: str):
    with open(chart_path, "rb") as image_file:
        image_data = image_file.read()

    # Upload image
    img_response = requests.post(
        "https://slack.com/api/files.upload",
        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
        files={"file": ("chart.png", image_data, "image/png")},
        data={
            "channels": SLACK_CHANNEL_ID,
            "initial_comment": summary,
            "title": "Weekly Dev Report - Code Churn"
        }
    )

    if img_response.status_code != 200 or not img_response.json().get("ok"):
        print("❌ Slack post failed:", img_response.json())
    else:
        print("✅ Slack post successful.")

# 🕓 Weekly digest job (for demo: every 1 min)
def weekly_digest():
    print("⏳ Running scheduled LangGraph report...\n")
    result = graph.invoke({
        "owner": "vigyat13",
        "repo": "Nivaan-ChatBot"
    })

    summary = result["summary"]
    chart_path = "churn_chart.png"
    post_to_slack(summary, chart_path)

# Schedule job
schedule.every(1).minutes.do(weekly_digest)  # change to `.monday.at("09:00")` later

if __name__ == "__main__":
    print("🕔 Scheduler started. Running every 1 minute (for demo).")
    while True:
        schedule.run_pending()
        time.sleep(1)
