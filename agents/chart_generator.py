import matplotlib.pyplot as plt
import base64
from io import BytesIO
import os

def generate_churn_chart(author_churn: dict) -> str:
    # 📊 Plot
    authors = list(author_churn.keys())
    churn_values = list(author_churn.values())

    plt.figure(figsize=(10, 6))
    bars = plt.bar(authors, churn_values, color='skyblue')
    plt.xlabel("Author")
    plt.ylabel("Total Churn")
    plt.title("Code Churn by Author")

    # Annotate values
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + 0.1, yval + 5, yval, ha='center')

    # ✅ Save to disk (for verification/debugging)
    image_path = "churn_chart.png"
    plt.savefig(image_path)
    print(f"📁 Saved churn chart to: {os.path.abspath(image_path)}")

    # 🧠 Convert to Base64
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    plt.close()

    return image_base64
