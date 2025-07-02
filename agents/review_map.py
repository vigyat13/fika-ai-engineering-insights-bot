import networkx as nx
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import os
import requests

def fetch_review_map(owner: str, repo: str, token: str) -> nx.DiGraph:
    headers = {"Authorization": f"Bearer {token}"}
    pulls_url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=all&per_page=20"
    
    response = requests.get(pulls_url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Error fetching PRs: {response.status_code} - {response.text}")
        return nx.DiGraph()

    pulls = response.json()
    graph = nx.DiGraph()

    for pr in pulls:
        pr_number = pr.get("number")
        author = pr.get("user", {}).get("login")

        if not author:
            continue

        reviews_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
        reviews_response = requests.get(reviews_url, headers=headers)

        if reviews_response.status_code != 200:
            print(f"⚠️ Skipped PR #{pr_number}: Failed to fetch reviews")
            continue

        reviews = reviews_response.json()
        reviewers = {
            review["user"]["login"]
            for review in reviews
            if review.get("user") and review["user"]["login"] != author
        }

        for reviewer in reviewers:
            graph.add_edge(author, reviewer)

    # ✅ Fallback dummy graph for empty maps
    if graph.number_of_nodes() == 0:
        print("⚠️ No review interactions found. Adding dummy graph.")
        graph.add_edge("Author", "Reviewer")

    print(f"✅ Review graph built: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
    return graph

def generate_review_map_image(graph: nx.DiGraph) -> str:
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graph, seed=42)

    nx.draw(
        graph, pos,
        with_labels=True,
        node_color='lightblue',
        edge_color='gray',
        node_size=3000,
        font_size=10,
        arrows=True,
        width=1.5,
        alpha=0.9
    )

    image_path = "review_influence_map.png"
    plt.savefig(image_path)

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    base64_image = base64.b64encode(buffer.read()).decode("utf-8")
    plt.close()

    print(f"📌 Review influence map saved at: {os.path.abspath(image_path)}")
    return base64_image
