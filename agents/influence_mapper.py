import networkx as nx
import matplotlib.pyplot as plt

def generate_influence_map(reviews: List[Dict[str, str]]) -> str:
    """
    Takes reviews: List of {'reviewer': str, 'author': str} and plots a directed graph.
    """
    G = nx.DiGraph()
    for r in reviews:
        G.add_edge(r['reviewer'], r['author'])

    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=2000, font_size=10)
    plt.title("Reviewer → Author Influence Map")

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    plt.close()

    return image_base64
