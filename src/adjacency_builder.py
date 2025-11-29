import os
import pandas as pd

def extract_name_column(df):
    """
    Detects the column that contains connection names.
    Works even if column names vary.
    """
    possible_cols = ["name", "full name", "first name", "connection", "connections"]

    df_cols_lower = [c.lower().strip() for c in df.columns]

    # match any possible column
    for col in possible_cols:
        if col in df_cols_lower:
            return df.columns[df_cols_lower.index(col)]

    # fallback → first column
    return df.columns[0]


def build_adjacency(cleaned_folder, adjacency_folder):
    """
    Converts each cleaned connection file into an adjacency list CSV
    with *one column* → "connected_to"
    """
    if not os.path.exists(adjacency_folder):
        os.makedirs(adjacency_folder)

    files = [f for f in os.listdir(cleaned_folder) if f.endswith(".csv")]

    for file in files:
        inp_path = os.path.join(cleaned_folder, file)
        out_path = os.path.join(adjacency_folder, file)

        try:
            df = pd.read_csv(inp_path)

            name_col = extract_name_column(df)
            connections = df[name_col].dropna().unique()

            out_df = pd.DataFrame({"connected_to": connections})
            out_df.to_csv(out_path, index=False)

            print(f"✔ Created adjacency → {file}")

        except Exception as e:
            print(f"❌ Failed for {file}: {e}")


if __name__ == "__main__":
    build_adjacency("data/cleaned", "data/adjacency")
