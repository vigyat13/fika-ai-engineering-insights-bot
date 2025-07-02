import os
import argparse
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from typing import TypedDict, Dict, Any, List

from agents.github_ingestor import fetch_commits_api
from agents.diff_analyst import analyze_diff
from agents.insight_narrator import generate_insight
from agents.forecaster import forecast_next_week
from agents.review_map import fetch_review_map, generate_review_map_image

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#general")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
slack_client = WebClient(token=SLACK_BOT_TOKEN)

# Shared state
class GraphState(TypedDict):
    owner: str
    repo: str
    github_data: List[Dict[str, Any]]
    churn_data: Dict[str, Any]
    summary: str
    chart_base64: str
    forecast: str
    influence_map: str

# Nodes

def fetch_fn(state: Dict[str, Any]) -> Dict[str, Any]:
    github_data = fetch_commits_api.invoke({
        "input": {"owner": state["owner"], "repo": state["repo"]}
    })["github_data"]
    return {**state, "github_data": github_data}

def analyze_fn(state: Dict[str, Any]) -> Dict[str, Any]:
    churn_data = analyze_diff.invoke({
        "input": {"github_data": state["github_data"]}
    })
    return {**state, "churn_data": churn_data}

def insight_fn(state: Dict[str, Any]) -> Dict[str, Any]:
    insight = generate_insight.invoke({
        "input": {
            "author_churn": state["churn_data"]["author_churn"],
            "risky_commits": state["churn_data"]["risky_commits"]
        }
    })
    return {**state, "summary": insight["summary"], "chart_base64": insight["chart_base64"]}

def forecast_fn(state: Dict[str, Any]) -> Dict[str, Any]:
    # For demo, generate dummy weekly churn history from current churn
    churn_history = []
    for i in range(4):
        churn_history.append({"week_start": f"2024-06-{i*7+1:02d}", "total_churn": sum(state["churn_data"]["author_churn"].values())})
    forecast = forecast_next_week(churn_history)
    return {**state, "forecast": f"Next week churn: {forecast['forecast_churn']} (Week of {forecast['forecast_week']})"}

def influence_fn(state: Dict[str, Any]) -> Dict[str, Any]:
    graph = fetch_review_map(state["owner"], state["repo"], GITHUB_TOKEN)
    influence_map = generate_review_map_image(graph)
    return {**state, "influence_map": influence_map}

# LangGraph Setup
workflow = StateGraph(GraphState)
workflow.add_node("fetch", RunnableLambda(fetch_fn))
workflow.add_node("analyze", RunnableLambda(analyze_fn))
workflow.add_node("insight", RunnableLambda(insight_fn))
workflow.add_node("forecast_result", RunnableLambda(forecast_fn))
workflow.add_node("influence", RunnableLambda(influence_fn))
workflow.set_entry_point("fetch")
workflow.add_edge("fetch", "analyze")
workflow.add_edge("analyze", "insight")
workflow.add_edge("insight", "forecast_result")
workflow.add_edge("forecast_result", "influence")
workflow.add_edge("influence", END)
graph = workflow.compile()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", default="vigyat13")
    parser.add_argument("--repo", default="Nivaan-ChatBot")
    parser.add_argument("--slack", action="store_true")
    args = parser.parse_args()

    print("\n🔁 Running LangGraph pipeline...")
    result = graph.invoke({"owner": args.owner, "repo": args.repo})

    print("\n📢 Summary:", result["summary"])
    print("\n📈 Forecast:", result["forecast"])
    print("\n🗺️ Influence Map (Base64):", result["influence_map"][:100], "...")

    if args.slack:
        try:
            slack_client.chat_postMessage(
                channel=SLACK_CHANNEL,
                text=f"*Dev Insight Report for `{args.repo}`*\n\n{result['summary']}\n\n📈 {result['forecast']}"
            )
            print(f"✅ Posted to Slack: {SLACK_CHANNEL}")
        except SlackApiError as e:
            print(f"❌ Slack error: {e.response['error']}")
