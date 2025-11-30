import os
import pandas as pd
import matplotlib.pyplot as plt


# 1. DEGREE DISTRIBUTION

def plot_degree_distribution(degree_file="data/degree.csv"):
    df = pd.read_csv(degree_file)

    plt.figure(figsize=(10, 5))
    plt.hist(df["Degree"], bins=40, color="#6C5CE7")
    plt.title("Degree Distribution of Students")
    plt.xlabel("Number of Connections")
    plt.ylabel("Count of Students")
    plt.tight_layout()
    plt.savefig("data/degree_distribution.png")
    plt.close()

    print(" Saved --> data/degree_distribution.png")



# 2. TOP CONNECTED STUDENTS

def plot_top_students(degree_file="data/degree.csv", top_n=10):
    df = pd.read_csv(degree_file)
    top = df.sort_values(by="Degree", ascending=False).head(top_n)

    plt.figure(figsize=(14,6))
    plt.bar(top["Student"], top["Degree"], color="#00B894")
    plt.xticks(rotation=75)
    plt.title(f"Top {top_n} Most Connected Students")
    plt.ylabel("Degree (Connections)")
    plt.tight_layout()
    plt.savefig("data/top_students.png")
    plt.close()

    print(" Saved --> data/top_students.png")



# 3. TOP COMPANIES (Count in network)

def plot_top_companies(cleaned_folder="data/cleaned"):
    companies = []

    for file in os.listdir(cleaned_folder):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(cleaned_folder, file))
            companies.extend(df["Company"].dropna().tolist())

    comp_df = pd.DataFrame(companies, columns=["Company"])
    top = comp_df["Company"].value_counts().head(20)

    plt.figure(figsize=(12,6))
    plt.barh(top.index, top.values, color="#0984E3")
    plt.title("Top 20 Most Common Companies in Connections")
    plt.xlabel("Frequency")
    plt.tight_layout()
    plt.savefig("data/top_companies.png")
    plt.close()

    print("✔ Saved → data/top_companies.png")



# 4. INDUSTRY DISTRIBUTION GRAPH

def plot_industry_distribution(cleaned_folder="data/cleaned"):
    industries = {
        "Tech": 0,
        "Finance": 0,
        "Education": 0,
        "Engineering": 0,
        "Other": 0
    }

    keywords = {
        "Tech": ["tech", "software", "it", "digital", "ai"],
        "Finance": ["bank", "finance", "capital", "money"],
        "Education": ["university", "school", "college", "institute"],
        "Engineering": ["engineer", "engineering", "mechanical", "electrical"]
    }

    for file in os.listdir(cleaned_folder):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(cleaned_folder, file))

            for comp in df["Company"].fillna("None"):
                cl = comp.lower()
                found = False

                for category, words in keywords.items():
                    if any(w in cl for w in words):
                        industries[category] += 1
                        found = True
                        break

                if not found:
                    industries["Other"] += 1

    # Plotting the bar graph
    plt.figure(figsize=(10,6))
    plt.bar(industries.keys(), industries.values(), color="#6C5CE7")
    plt.title("Industry Distribution of Connections")
    plt.ylabel("Count of People")
    plt.tight_layout()
    plt.savefig("data/industry_distribution.png")
    plt.close()

    print(" Saved --> data/industry_distribution.png")



# 5. RUN ALL VISUALIZATIONS

def generate_all_plots():
    print("\n Generating visualizations...\n")

    plot_degree_distribution()
    plot_top_students(top_n=10)
    plot_top_companies()
    plot_industry_distribution()

    print("\n All visualizations completed! Files saved inside /data/ folder.\n")

if __name__ == "__main__":
    generate_all_plots()
