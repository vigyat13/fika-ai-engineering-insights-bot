from langchain_core.tools import tool
from typing import Dict, Any
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import os

from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate

# 🔁 Dynamic LLM driver selection
LLM_DRIVER = os.getenv("LLM_DRIVER", "groq").lower()

if LLM_DRIVER == "groq":
    from langchain_groq import ChatGroq
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant"
    )
elif LLM_DRIVER == "openai":
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o"
    )
else:
    raise ValueError(f"❌ Unsupported LLM_DRIVER: {LLM_DRIVER}")

# 🧠 Prompt for weekly developer insight
prompt = PromptTemplate.from_template("""
You are a software engineering analyst bot.

Given:
- Per-author code churn data
- List of risky commits (high churn, many files changed)

Generate a short and crisp insight summary for a weekly developer productivity report.

Author churn:
{author_churn}

Risky commits:
{risky_commits}

Output a helpful and concise report with insights, risks, and positive highlights.
""")

# 🔗 LLM chain
chain = prompt | llm | StrOutputParser()

# 📊 Generate chart
def generate_churn_chart(author_churn: dict) -> str:
    authors = list(author_churn.keys())
    churn_values = list(author_churn.values())

    plt.figure(figsize=(10, 6))
    bars = plt.bar(authors, churn_values, color='skyblue')
    plt.xlabel("Author")
    plt.ylabel("Total Churn")
    plt.title("Code Churn by Author")

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 5, yval, ha='center', va='bottom')

    plt.tight_layout()
    image_path = "churn_chart.png"
    plt.savefig(image_path)

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    chart_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    plt.close()

    print(f"📊 Churn chart saved at: {os.path.abspath(image_path)}")
    return chart_base64

# 🧪 Main tool
@tool
def generate_insight(input: Dict[str, Any]) -> Dict[str, str]:
    """
    Uses Groq or OpenAI LLM to generate a developer productivity insight
    from per-author churn data and risky commits. Also generates a churn chart as a base64 image.
    """
    author_churn = input.get("author_churn", {})
    risky_commits = input.get("risky_commits", [])

    summary = chain.invoke({
        "author_churn": author_churn,
        "risky_commits": risky_commits
    })

    chart_base64 = generate_churn_chart(author_churn)

    return {
        "summary": summary,
        "chart_base64": chart_base64
    }
