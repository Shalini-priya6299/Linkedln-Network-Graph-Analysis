import os
from cleaner import clean_all
from adjacency_builder import build_adjacency
from degree_builder import build_degrees
from graph_builder import build_graph
from visualizer import generate_all_plots

RAW_DATA_PATH = r"C:\Users\INDIAN  OIL\Downloads\LinkedIn Data Public\LinkedIn Data Public"

def main():
    print("\n STEP 1: Cleaning raw LinkedIn data...")
    clean_all(RAW_DATA_PATH, output_dir="data/cleaned")

    print("\n STEP 2: Creating adjacency lists...")
    build_adjacency("data/cleaned", "data/adjacency")

    print("\n STEP 3: Building degree file...")
    build_degrees("data/adjacency", "data/degree.csv", "data/connected_to")

    print("\n STEP 4: Building edge list for full network graph...")
    build_graph("data/adjacency", "data/edges.csv")

    print("\n STEP 5: Generating all visualizations...")
    generate_all_plots()

    print("\n ALL TASKS COMPLETED SUCCESSFULLY ")

if __name__ == "__main__":
    main()
