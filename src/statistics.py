import pandas as pd
import networkx as nx

def load_graph(edge_file="data/edges.csv"):
    df = pd.read_csv(edge_file)
    if "Source" in df.columns and "Target" in df.columns:
        src, tgt = "Source", "Target"
    else:
        src, tgt = df.columns[0], df.columns[1]
    G = nx.from_pandas_edgelist(df, source=src, target=tgt, create_using=nx.DiGraph())
    return G, df


def graph_statistics():
    print("\n--- NETWORK STATISTICS ---\n")

    G, edges_df = load_graph()

    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()

    print(f"Total Students (Nodes): {num_nodes}")
    print(f"Total Connections (Edges): {num_edges}")

    # Density (how connected the network is)
    density = nx.density(G)
    print(f"Graph Density: {density:.6f}")

    # Degree statistics
    degree_df = pd.read_csv("data/degree.csv")

    max_degree = degree_df["Degree"].max()
    min_degree = degree_df["Degree"].min()
    avg_degree = degree_df["Degree"].mean()

    top_student = degree_df.loc[degree_df["Degree"].idxmax(), "Student"]
    least_student = degree_df.loc[degree_df["Degree"].idxmin(), "Student"]

    print(f"\nMost Connected Student: {top_student} ({max_degree}) connections")
    print(f"Least Connected Student: {least_student} ({min_degree}) connections")
    print(f"Average Degree: {avg_degree:.2f}")

    # Random walk influence summary
    rw_df = pd.read_csv("data/random_walk_output.csv")
    top_rw = rw_df.sort_values(by="Visits", ascending=False).iloc[0]

    print(f"\nTop Influencer (Random Walk): {top_rw['Student']} ({top_rw['Visits']} visits)")

    # Save summary
    summary = {
        "Total Nodes": [num_nodes],
        "Total Edges": [num_edges],
        "Density": [density],
        "Most Connected Student": [top_student],
        "Max Degree": [max_degree],
        "Least Connected Student": [least_student],
        "Min Degree": [min_degree],
        "Average Degree": [avg_degree],
        "Top Influencer": [top_rw["Student"]],
        "Top Influencer Score": [top_rw["Visits"]]
    }

    summary_df = pd.DataFrame(summary)
    summary_df.to_csv("data/network_statistics.csv", index=False)

    print("\n✔ Statistics saved → data/network_statistics.csv\n")


if __name__ == "__main__":
    graph_statistics()
