import os
import pandas as pd
import re

def clean_all(input_dir, output_dir="cleaned_folder"):
    os.makedirs(output_dir, exist_ok=True)

    all_files = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.endswith(".csv") or f.endswith(".xlsx")
    ]

    cleaned_paths = []

    for file_path in all_files:
        ext = os.path.splitext(file_path)[1]

        # --- read file safely ---
        try:
            if ext == ".csv":
                try:
                    df = pd.read_csv(file_path)
                except UnicodeDecodeError:
                    df = pd.read_csv(file_path, encoding="ISO-8859-1")
            else:
                df = pd.read_excel(file_path)
        except Exception as e:
            print(f"❌ Could not read: {file_path} → {e}")
            continue

        # --- Normalize columns ---
        df.columns = df.columns.str.strip().str.title()

        # POSSIBLE column variations
        possible_first = ["First Name", "Firstname", "Given Name"]
        possible_last = ["Last Name", "Lastname", "Surname"]
        possible_full = ["Full Name", "Name"]

        # Auto-detect name columns
        first_col = next((c for c in possible_first if c in df.columns), None)
        last_col = next((c for c in possible_last if c in df.columns), None)
        full_col = next((c for c in possible_full if c in df.columns), None)

        # If Full Name exists → split into first/last
        if full_col and not (first_col and last_col):
            df["Full Name"] = df[full_col].astype(str)
            parts = df["Full Name"].str.split(" ", n=1, expand=True)
            df["First Name"] = parts[0]
            df["Last Name"] = parts[1] if parts.shape[1] > 1 else ""
            first_col, last_col = "First Name", "Last Name"

        # If still no proper columns → skip this file
        if not (first_col and last_col):
            print(f"⚠️ Skipping {file_path}: No name columns found.")
            continue

        # Company detection
        possible_company = ["Company", "Company Name", "Organization"]
        company_col = next((c for c in possible_company if c in df.columns), None)

        if not company_col:
            df["Company"] = "None"
        else:
            df["Company"] = df[company_col].fillna("None")

        # Create clean format
        df["Full Name"] = df[first_col].astype(str) + " " + df[last_col].astype(str)
        clean_df = df[["Full Name", "Company"]]

        # Output filename
        base = os.path.basename(file_path)
        name_match = re.search(r"([A-Za-z]+)[ _]([A-Za-z]+)", base)

        if name_match:
            out_name = f"{name_match.group(1)}_{name_match.group(2)}.csv"
        else:
            out_name = base.replace(".xlsx", ".csv")

        out_path = os.path.join(output_dir, out_name)
        clean_df.to_csv(out_path, index=False)

        cleaned_paths.append(out_path)

    print(f"\n✨ Cleaned {len(cleaned_paths)} files successfully.")
    return cleaned_paths


if __name__ == "__main__":
    clean_all(r"C:\Users\INDIAN  OIL\Downloads\LinkedIn Data Public\LinkedIn Data Public")
