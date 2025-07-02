import os
import base64
import traceback
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from langgraph_pipeline import run_pipeline  # Ensure this file exists and works

# Load environment variables from .env
load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

# Initialize Slack App
app = App(token=SLACK_BOT_TOKEN)

@app.command("/dev-report")
def handle_dev_report(ack, body, respond):
    ack()  # Acknowledge immediately

    user = body.get("user_name")
    channel_id = body.get("channel_id")
    print(f"✅ /dev-report command received from @{user} in channel {channel_id}")

    try:
        # Run LangGraph pipeline
        result = run_pipeline()
        summary = result.get("summary", "")
        chart_base64 = result.get("chart_base64", "")

        if not chart_base64:
            respond("⚠️ No chart generated. Please ensure the pipeline ran correctly.")
            return

        # Save chart to file
        chart_path = "churn_chart.png"
        with open(chart_path, "wb") as f:
            f.write(base64.b64decode(chart_base64))
        print("📊 Chart saved locally")

        # Upload to Slack
        response = app.client.files_upload_v2(
            channel=channel_id,  # ✅ correct key
            file=chart_path,
            filename="churn_chart.png",
            title="Developer Productivity Report",
            initial_comment=summary
        )

        print("📎 File uploaded to Slack:", response["file"]["id"])

    except Exception as e:
        print("❌ Exception occurred while handling /dev-report:\n", traceback.format_exc())
        respond("❌ Something went wrong while generating the report. Please try again later.")

# Entry point
if __name__ == "__main__":
    print("🚀 Starting Fika MVP Slack bot...")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
