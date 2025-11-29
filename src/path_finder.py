import pandas as pd
import networkx as nx
import sys

def load_graph(edge_file="data/edges.csv"):
    df = pd.read_csv(edge_file)

    # Handle both
    if "Source" in df.columns and "Target" in df.columns:
        src, tgt = "Source", "Target"
    elif "A" in df.columns and "B" in df.columns:
        src, tgt = "A", "B"
    else:
        raise ValueError("Unknown edge columns in edges.csv")

    G = nx.DiGraph()   # directed graph
    for _, row in df.iterrows():
        G.add_edge(row[src], row[tgt])
    return G


def find_path(student1, student2, edge_file="data/edges.csv"):
    G = load_graph(edge_file)

    print("\nSearching path between:")
    print("→", student1)
    print("→", student2)

    try:
        path = nx.shortest_path(G, source=student1, target=student2)
        print("\n✔ Shortest Path Found:\n")
        print(" → ".join(path))
        return path

    except nx.NetworkXNoPath:
        print("\n❌ No path exists between these students.")
    except nx.NodeNotFound as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python src/path_finder.py \"Student A\" \"Student B\"")
    else:
        student1 = sys.argv[1]
        student2 = sys.argv[2]
        find_path(student1, student2)
