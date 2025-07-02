import os
import sys
import base64
from datetime import datetime, timedelta

# Dynamically add root directory to import path so `main.py` can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, root_dir)

from main import graph  # ✅ make sure main.py contains LangGraph setup

def get_last_week_range():
    """Returns the Monday date of the last complete week."""
    today = datetime.today()
    last_monday = today - timedelta(days=today.weekday() + 7)
    return last_monday.strftime("%Y-%m-%d")

def run_pipeline():
    print("🔁 Running LangGraph pipeline via Slack bot...")

    # Run LangGraph pipeline
    result = graph.invoke({
        "owner": "vigyat13",
        "repo": "Nivaan-ChatBot"
    })

    summary_raw = result.get("summary", "[No summary generated]")
    week_start = get_last_week_range()
    summary = f"**Weekly Developer Productivity Report (Week of {week_start})**\n\n{summary_raw}"

    # Chart path is always saved to the root dir
    chart_path = os.path.join(root_dir, "churn_chart.png")
    try:
        with open(chart_path, "rb") as f:
            chart_base64 = base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError:
        print("❌ Error: churn_chart.png not found at", chart_path)
        chart_base64 = ""

    return {
        "summary": summary,
        "chart_base64": chart_base64
    }
