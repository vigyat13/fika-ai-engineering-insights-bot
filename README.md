# FIKA AI Engineering Productivity Bot

🚀 **Track developer productivity and identify engineering risks, right inside Slack.**

This is a submission for the **FIKA AI Research Engineering-Productivity Intelligence MVP Challenge**. The bot analyzes GitHub commit activity and provides weekly productivity insights, charts, and recommendations — all triggered with a simple `/dev-report` command in Slack.

---

## 📦 Features

* ✅ **LangGraph Agent Pipeline**:

  * **GitHub Ingestor**: Pulls commit data via GitHub REST API.
  * **Diff Analyst**: Analyzes code churn, risky diffs, and file-level impact.
  * **Insight Narrator**: Summarizes risk, highlights, and recommendations.

* 🧠 **AI-Generated Summaries** using Groq LLM (OpenAI-compatible).

* 📊 **Visual Reports**:

  * Developer-wise churn charts
  * Review influence map (stretch goal)

* 💬 **Slack Bot** (Bolt SDK + Socket Mode)

  * Trigger: `/dev-report`
  * Output: chart + narrative summary

* 🔁 **Pluggable LLM Driver**: switch between Groq or OpenAI.

* 🗓️ **Scheduled Monday Digests** (stretch goal)

* 🧪 **Seeded Repo Analysis** using `vigyat13/Nivaan-ChatBot` GitHub repo.

---

## 🧠 Architecture Diagram

> \[📎 Insert Architecture Diagram Image Here — LangGraph Nodes, Slack, GitHub, Chart Output, Storage Layer]

### 👇 LangGraph Flow

```
GitHubIngestor
     |
     v
DiffAnalyst → ForecastAgent → ReviewGraphBuilder
     |
     v
InsightNarrator
     |
     v
SlackBotOutput
```

---
## 🧠 Architecture Diagram

This diagram shows the LangGraph orchestration pipeline and agent transitions:

![LangGraph Agent Flow](architecture_diagram.png)


## 🛠️ Tech Stack

* **Python 3.10+**
* **LangChain + LangGraph**
* **Slack Bolt SDK (Python)**
* **Matplotlib** (for churn charts)
* **networkx** (for review influence maps)
* **GitHub REST API**
* **Docker + Docker Compose**
* **Groq/OpenAI API (pluggable)**

---

## 🚀 Quickstart

```bash
git clone https://github.com/yourusername/fika-mvp
cd fika-mvp

# Copy and fill the required secrets
cp .env.example .env

# Build and run the app
docker compose up
```

### ✅ Slack Bot Commands

```bash
/dev-report   # Generates weekly developer productivity report
```

---

## 🔐 Environment Variables

Store in a `.env` file (excluded in .gitignore):

```env
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
GITHUB_TOKEN=ghp_...
GROQ_API_KEY=gsk_...
LLM_DRIVER=groq  # or 'openai'
```

---

## 🧪 Seed Data

To get insights instantly, we analyze the public repo:

```bash
GitHub Repo: vigyat13/Nivaan-ChatBot
```

Change owner/repo in `main.py` or pass via CLI:

```bash
python main.py --owner vigyat13 --repo Nivaan-ChatBot
```

---

## 🧠 Example Output

**Weekly Developer Productivity Report (Week of 2025-06-24)**

**Key Insights:**

* VigyatSingh13 contributed the most with 236 lines changed.
* One high-risk commit (202 lines, 17 files) on May 8.

**Positive Highlights:**

* Vigyat13 had efficient low-churn commits.

**Recommendations:**

* Review high-churn commits.
* Add code reviews + CI checks.

📊 Attached chart: churn\_chart.png

---

## 📽️ Loom Demo

> \[📎 Link to Loom video demo here — showing `/dev-report` in Slack and architecture walkthrough]

---

## 📁 Folder Structure

```
fki-mvp-challenge/
│
├── agents/
│   ├── __init__.py
│   ├── data_harvester.py          # GitHub data puller
│   ├── diff_analyst.py            # Commit/churn analyzer
│   ├── insight_narrator.py        # Narrative builder
│   ├── chart_generator.py         # Matplotlib chart maker
│   ├── review_map.py              # Optional stretch goal
│   ├── forecaster.py              # Optional stretch goal
│   ├── scheduled.py               # Monday auto-drop logic
│
├── bot/
│   ├── __init__.py
│   ├── slack_bot.py               # Slack command listener
│   ├── langgraph_pipeline.py      # Calls LangGraph workflow
│   ├── churn_chart.png            # Saved weekly chart
│   ├── review_influence_map.png   # Optional: review heatmap
│
├── data/
│   └── seed_data.json             # Fake GitHub commits for demo
│
├── icons/
│   └── Slack_icon.png             # Optional UI branding
│
├── utils/
│   ├── github_client.py           # REST API wrapper for GitHub
│
├── .env                           # Secrets like SLACK tokens
├── .gitignore
├── README.md                      # Project guide
├── requirements.txt               # All pip packages
├── architecture_diagram.py       # Auto-generates architecture PNG
├── architecture_diagram.png      # Rendered system diagram
├── main.py                        # Entry LangGraph + graph setup
├── docker-compose.yml            # 🔁 One command run
├── Dockerfile                     # API image builder
└── seed_data.py                   # Fakes GitHub data (optional CLI)


---

## 📬 Submission

* ✅ All MVP features complete
* ✅ Stretch goals implemented
* ✅ PR submitted to FIKA challenge repo
* ✅ Loom demo attached

---

## 👨‍💻 Author

**Vigyat Singh**
[GitHub: vigyat13](https://github.com/vigyat13)

---

## 📄 License

MIT (for open-source release by FIKA, if selected)
