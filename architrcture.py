# generate_arch_diagram.py

from main import graph  # Make sure main.py contains your compiled LangGraph `graph`
from pathlib import Path

# Generate the diagram using Mermaid
image_bytes = graph.get_graph().draw_mermaid_png()

# Save to a file
output_path = Path("langgraph_architecture.png")
output_path.write_bytes(image_bytes)

print(f"✅ Architecture diagram saved at: {output_path.resolve()}")
