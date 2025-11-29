import os
import pandas as pd

def find_connection_column(df):
    """
    Detects the correct connection column name in any file.
    """
    possible_cols = ["connected_to", "Connected To", "Connected_to", "connected to"]

    for col in df.columns:
        if col.strip().lower().replace(" ", "_") == "connected_to":
            return col

    # fallback: first column
    return df.columns[0]


def build_degrees(adjacency_folder="data/adjacency",
                  degree_output="data/degree.csv",
                  connections_output="data/connected_to"):
    
    os.makedirs(connections_output, exist_ok=True)
    degree_data = []

    for file in os.listdir(adjacency_folder):
        if not file.endswith(".csv"):
            continue

        student_name = file.replace(".csv", "").replace("_", " ").strip()
        path = os.path.join(adjacency_folder, file)

        try:
            df = pd.read_csv(path)

            conn_col = find_connection_column(df)  # auto-detect column

            connections = df[conn_col].dropna().unique()
            degree = len(connections)

            # save individual connections list
            individual_out = os.path.join(connections_output, file)
            pd.DataFrame({"connected_to": connections}).to_csv(individual_out, index=False)

            degree_data.append((student_name, degree))

            print(f"✔ {student_name}: {degree} connections")

        except Exception as e:
            print(f"❌ Error in {file}: {e}")

    # create degree file
    degree_df = pd.DataFrame(degree_data, columns=["Student", "Degree"])
    degree_df = degree_df.sort_values(by="Degree", ascending=False)
    degree_df = degree_df.drop_duplicates(subset=["Student"], keep="first")

    degree_df.to_csv(degree_output, index=False)

    print(f"\n✨ Degree file saved → {degree_output}")
    print(f"📁 Connected lists saved → {connections_output}")


if __name__ == "__main__":
    build_degrees()
