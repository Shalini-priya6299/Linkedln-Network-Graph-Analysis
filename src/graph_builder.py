import os
import pandas as pd

def build_graph(adjacency_folder="data/adjacency", output_edges="data/edges.csv"):
    """
    EXACT logic from your assignment.ipynb:
    For each student file:
        - read connected_to list
        - create edges: (student, connection)
    Save all edges in edges.csv
    """

    edges = []

    for file in os.listdir(adjacency_folder):
        if file.endswith(".csv"):

            student = file.replace(".csv", "").replace("_", " ").strip()
            file_path = os.path.join(adjacency_folder, file)

            try:
                df = pd.read_csv(file_path)

                # detect the name column (in your notebook it was always first column)
                col = df.columns[0]

                # build edges
                for conn in df[col].dropna():
                    conn = str(conn).strip()
                    if conn:
                        edges.append((student, conn))

            except Exception as e:
                print(f"❌ Error reading {file}: {e}")

    # convert to DataFrame EXACTLY LIKE notebook
    edges_df = pd.DataFrame(edges, columns=["Source", "Target"])
    edges_df.drop_duplicates(inplace=True)

    # save
    edges_df.to_csv(output_edges, index=False, encoding="utf-8-sig")

    print(f"✔ edges.csv created → {output_edges}")
    print(f"Total edges: {len(edges_df)}")


if __name__ == "__main__":
    build_graph()
