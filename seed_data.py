# seed_data.py
import json
import base64
from main import graph  # Importing real LangGraph pipeline

if __name__ == "__main__":
    print("\n🌱 Using seed data to simulate GitHub pipeline...\n")

    with open("data/seed_data.json", "r") as f:
        seed_state = json.load(f)

    result = graph.invoke(seed_state)

    print("\n💬 Final Summary:")
    print(result.get("summary", "No summary generated."))

    if "chart_base64" in result:
        with open("churn_chart_from_seed.png", "wb") as f:
            f.write(base64.b64decode(result["chart_base64"]))
        print("\n📊 Chart image saved as 'churn_chart_from_seed.png'")

    if "influence_map" in result:
        with open("review_influence_map_from_seed.png", "wb") as f:
            f.write(base64.b64decode(result["influence_map"]))
        print("\n🗺️ Review map saved as 'review_influence_map_from_seed.png'")

    if "forecast" in result:
        print(f"\n📈 Forecast: {result['forecast']}")
