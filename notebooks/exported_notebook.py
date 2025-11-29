#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import pandas as pd
import re

# === SETUP: Your local folder path ===
input_dir = r"C:\Users\INDIAN  OIL\Downloads\LinkedIn Data Public\LinkedIn Data Public"
output_dir = "cleaned_folder"
os.makedirs(output_dir, exist_ok=True)

# === STEP 1: Find all CSV and XLSX files ===
all_files = []
for file in os.listdir(input_dir):
    if file.endswith('.csv') or file.endswith('.xlsx'):
        all_files.append(os.path.join(input_dir, file))

# === STEP 2: Cleaning Function with Encoding & Column Check ===
def clean_file(file_path):
    ext = os.path.splitext(file_path)[1]

    # Try reading with UTF-8, fallback to ISO-8859-1
    try:
        if ext == '.csv':
            try:
                df = pd.read_csv(file_path)
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, encoding='ISO-8859-1')
        else:
            df = pd.read_excel(file_path)
    except Exception as e:
        raise Exception(f" Could not read file: {e}")

    # Ensure required columns exist
    required_columns = {'First Name', 'Last Name', 'Company'}
    if not required_columns.issubset(df.columns):
        # Handle the case where the columns don't exist or are mismatched
        print(f" Error in {file_path}: Missing required columns. Attempting auto-fix...")

        # Rename columns if needed
        df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces
        df.rename(columns={
            'FIRST NAME': 'First Name',
            'LAST NAME': 'Last Name',
            'COMPANY': 'Company'
        }, inplace=True)

        # Save the fixed file
        df.to_csv(file_path, index=False)
        print(f" Fixed and saved: {file_path}")

    # Remove rows where any of the important columns (Full Name, First Name, Last Name) are empty
    df = df.dropna(subset=['First Name', 'Last Name'])

    # Fill missing 'Company' values with "None" (only for Company column)
    df['Company'] = df['Company'].fillna('None')

    # Merge First and Last Name into Full Name
    df['Full Name'] = df['First Name'] + ' ' + df['Last Name']

    # Keep only needed columns
    df = df[['Full Name', 'Company']]

    # Generate cleaned filename
    base = os.path.basename(file_path)
    match = re.search(r'([A-Za-z]+)[ _]([A-Za-z]+)', base)
    if match:
        filename = f"{match.group(1)}_{match.group(2)}.csv"
    else:
        filename = base.replace('.xlsx', '.csv')

    # Save cleaned file
    out_path = os.path.join(output_dir, filename)
    df.to_csv(out_path, index=False)
    return out_path

# === STEP 3: Process All Files ===
cleaned_paths = []
for file_path in all_files:
    try:
        cleaned_path = clean_file(file_path)
        cleaned_paths.append(cleaned_path)
    except Exception as e:
        print(f" Error in {file_path}: {e}")

print(f"\n Cleaned {len(cleaned_paths)} files.")
print(f" Cleaned files saved in: {output_dir}")


# In[ ]:


import os
import pandas as pd
from collections import defaultdict

# === Folder where each student CSV is stored ===
adjacency_folder = "adjacency_folder1"
degree_data = []

# === Build degree data ===
for file in os.listdir(adjacency_folder):
    if file.endswith(".csv"):
        student = file.replace(".csv", "").replace("_", " ")
        path = os.path.join(adjacency_folder, file)
        
        try:
            df = pd.read_csv(path)
            connections = df['Connected To'].dropna()
            degree = len(connections)
            degree_data.append((student, degree))
        except Exception as e:
            print(f"Error in {file}: {e}")

# === Create DataFrame, sort, and save ===
degree_df = pd.DataFrame(degree_data, columns=["Student", "Degree"])
degree_df = degree_df.sort_values(by="Degree", ascending=False).reset_index(drop=True)

# Save to CSV
degree_df.to_csv("student_degrees.csv", index=False, encoding="utf-8-sig")

print(" Degree CSV saved as 'student_degrees.csv'")


# In[4]:


import os
import pandas as pd
from collections import defaultdict
import random

# === Step 1: Load Graph from Adjacency Folder ===
def load_graph(adjacency_folder):
    graph = defaultdict(set)
    for file in os.listdir(adjacency_folder):
        if file.endswith('.csv'):
            person = file.replace('.csv', '').replace("_", " ").strip()
            df = pd.read_csv(os.path.join(adjacency_folder, file))
            connections = df['Connected To'].dropna().astype(str).str.strip().tolist()
            graph[person].update(connections)
    return graph

# === Step 2: Random Walk Function (Allows Revisits) ===
def random_walk(graph, start, end, max_steps=1000):
    if start not in graph or end not in graph:
        print(f" One or both students not found in the graph.")
        return None

    walk = [start]
    current = start

    for _ in range(max_steps):
        if current == end:
            return walk

        neighbors = list(graph[current])
        if not neighbors:
            break  # Dead end

        next_node = random.choice(neighbors)
        walk.append(next_node)
        current = next_node

    return walk if current == end else None

# === Step 3: Try Multiple Random Walks ===
def try_random_walks(graph, start, end, attempts=100, max_steps=1000):
    for i in range(attempts):
        walk = random_walk(graph, start, end, max_steps)
        if walk:
            return walk
    return None

# === Step 4: Run Walk Between Two Students ===
adjacency_folder = "adjacency_folder1"
graph = load_graph(adjacency_folder)

start_student = "Shalini Priya"
end_student = "Rani Kumari"

walk = try_random_walks(graph, start_student, end_student)

if walk:
    print(" Random Walk Found:")
    print(" → ".join(walk))
else:
    print(" No random walk found after multiple attempts.")

# === Optional Debug Info ===
print(f"\n {start_student} connections:", graph.get(start_student, []))
print(f" {end_student} connections:", graph.get(end_student, []))


# In[5]:


def prune_walk(walk):
    """
    Removes cycles from the random walk to return a simple path.
    Keeps the first occurrence of each student.
    """
    if not walk:
        return []

    seen = {}
    pruned_path = []

    for idx, student in enumerate(walk):
        if student in seen:
            # When cycle detected, remove from last seen to current
            cycle_start = seen[student]
            pruned_path = pruned_path[:cycle_start + 1]
        else:
            seen[student] = len(pruned_path)
            pruned_path.append(student)

    return pruned_path

# Example usage after running random_walk():
pruned = prune_walk(walk)

if pruned:
    print("\n  Pruned Path:")
    print(" → ".join(pruned))
else:
    print("  Nothing to prune.")


# In[6]:


import os
import pandas as pd
from collections import defaultdict
import random
import numpy as np

# === Load Graph from Adjacency Folder ===
def load_graph(adjacency_folder):
    graph = defaultdict(set)
    for file in os.listdir(adjacency_folder):
        if file.endswith('.csv'):
            person = file.replace('.csv', '').replace("_", " ").strip()
            df = pd.read_csv(os.path.join(adjacency_folder, file))
            connections = df['Connected To'].dropna().astype(str).str.strip().tolist()
            graph[person].update(connections)
    return graph

# === Random Walk ===
def random_walk(graph, start, end, max_steps=1000):
    if start not in graph or end not in graph:
        return None

    walk = [start]
    current = start

    for _ in range(max_steps):
        if current == end:
            return walk
        neighbors = list(graph[current])
        if not neighbors:
            break
        next_node = random.choice(neighbors)
        walk.append(next_node)
        current = next_node

    return walk if current == end else None

# === Prune Random Walk to Direct Path ===
def prune_walk(walk, start, end):
    if not walk:
        return []
    path = [start]
    for node in walk[1:]:
        path.append(node)
        if node == end:
            break
    return path

# === Perform Multiple Random Walks & Gather Lengths ===
def try_random_walks(graph, start, end, attempts=100, max_steps=1000):
    walk_lengths = []
    pruned_lengths = []
    
    for _ in range(attempts):
        walk = random_walk(graph, start, end, max_steps)
        if walk:
            walk_lengths.append(len(walk))
            pruned_lengths.append(len(prune_walk(walk, start, end)))
    
    return walk_lengths, pruned_lengths

# === Compute Statistics ===
def compute_stats(lengths):
    if not lengths:
        return {"mean": None, "median": None, "std": None}
    return {
        "mean": round(np.mean(lengths), 2),
        "median": round(np.median(lengths), 2),
        "std": round(np.std(lengths), 2)
    }

# === Run for a Pair of Students ===
adjacency_folder = "adjacency_folder1"
graph = load_graph(adjacency_folder)

start_student = "Shalini Priya"
end_student = "Rani Kumari"

walk_lengths, pruned_lengths = try_random_walks(graph, start_student, end_student)

walk_stats = compute_stats(walk_lengths)
pruned_stats = compute_stats(pruned_lengths)

# === Output the Stats ===
print(f"📊 Random Walk Stats between '{start_student}' and '{end_student}':")
print("  - Mean Length:", walk_stats["mean"])
print("  - Median Length:", walk_stats["median"])
print("  - Std Deviation:", walk_stats["std"])

print(f"\n🌿 Pruned Path Stats:")
print("  - Mean Length:", pruned_stats["mean"])
print("  - Median Length:", pruned_stats["median"])
print("  - Std Deviation:", pruned_stats["std"])


# In[7]:


import os
import pandas as pd
import random
import numpy as np
from collections import defaultdict

# === Step 1: Load Graph from CSV Files ===
def load_graph(adjacency_folder):
    graph = defaultdict(set)  # This will hold each student's connections (adjacency list)
    
    # Loop through all CSV files in the folder
    for file in os.listdir(adjacency_folder):
        if file.endswith('.csv'):  # Check if the file is a CSV
            person = file.replace('.csv', '').replace("_", " ").strip()  # Extract student name
            df = pd.read_csv(os.path.join(adjacency_folder, file))  # Read the CSV file
            connections = df['Connected To'].dropna().astype(str).str.strip().tolist()  # Get the connected people
            graph[person].update(connections)  # Add connections to the graph
    
    return graph  # Return the constructed graph


# === Step 2: Perform a Random Walk ===
def random_walk(graph, start, end, max_steps=1000):
    # Ensure both start and end students are in the graph
    if start not in graph or end not in graph:
        return None  # Return None if either student isn't in the graph

    walk = [start]  # Start the walk with the starting student
    current = start  # Set the current student to the starting student

    # Perform random steps
    for _ in range(max_steps):
        if current == end:  # Stop if we reach the destination student
            return walk
        neighbors = list(graph[current])  # Get the neighbors (connections) of the current student
        if not neighbors:  # If there are no neighbors, stop the walk
            break
        next_node = random.choice(neighbors)  # Pick a random neighbor
        walk.append(next_node)  # Add this student to the walk
        current = next_node  # Move to the next student

    # If we reached the destination, return the walk; otherwise, return None
    return walk if current == end else None


# === Step 3: Prune the Random Walk to Remove Cycles (Loops) ===
def prune_walk(walk, start, end):
    if not walk:
        return []
    path = [start]  # Start the pruned path with the starting student
    for node in walk[1:]:  # Loop through the rest of the walk (except the start)
        path.append(node)  # Add each student to the path
        if node == end:  # Stop if we reach the destination student
            break
    return path  # Return the pruned path


# === Step 4: Run Multiple Random Walks & Gather Walk Lengths ===
def try_random_walks(graph, start, end, attempts=100, max_steps=1000):
    walk_lengths = []  # List to store lengths of random walks
    pruned_lengths = []  # List to store lengths of pruned paths
    
    # Try multiple random walks
    for _ in range(attempts):
        walk = random_walk(graph, start, end, max_steps)
        if walk:
            walk_lengths.append(len(walk))  # Add the length of the random walk
            pruned_lengths.append(len(prune_walk(walk, start, end)))  # Add the length of the pruned path
    
    return walk_lengths, pruned_lengths


# === Step 5: Compute Statistics (Mean, Median, Std Dev) ===
def compute_stats(lengths):
    if not lengths:
        return {"mean": None, "median": None, "std": None}  # Return None if no lengths
    
    # Calculate mean, median, and standard deviation of the walk lengths
    return {
        "mean": round(np.mean(lengths), 2),
        "median": round(np.median(lengths), 2),
        "std": round(np.std(lengths), 2)
    }


# === Step 6: Run the Function for Two Students ===
adjacency_folder = "adjacency_folder1"  # Folder where your CSV files are located
graph = load_graph(adjacency_folder)  # Load the graph from the CSV files

# Define the start and end students
start_student = "Shalini Priya"  # Replace with the starting student's name
end_student = "Rani Kumari"  # Replace with the ending student's name

# Perform random walks and calculate the lengths
walk_lengths, pruned_lengths = try_random_walks(graph, start_student, end_student)

# Compute statistics for the random walks and pruned paths
walk_stats = compute_stats(walk_lengths)
pruned_stats = compute_stats(pruned_lengths)

# === Output the Results ===
print(f"📊 Random Walk Stats between '{start_student}' and '{end_student}':")
print("  - Mean Length:", walk_stats["mean"])
print("  - Median Length:", walk_stats["median"])
print("  - Std Deviation:", walk_stats["std"])

print(f"\n🌿 Pruned Path Stats:")
print("  - Mean Length:", pruned_stats["mean"])
print("  - Median Length:", pruned_stats["median"])
print("  - Std Deviation:", pruned_stats["std"])


# In[8]:


import os
import pandas as pd
import random
import numpy as np
from collections import defaultdict

# === Step 1: Load Graph from CSV Files ===
def load_graph(adjacency_folder):
    graph = defaultdict(set)  # This will hold each student's connections (adjacency list)
    
    # Loop through all CSV files in the folder
    for file in os.listdir(adjacency_folder):
        if file.endswith('.csv'):  # Check if the file is a CSV
            person = file.replace('.csv', '').replace("_", " ").strip()  # Extract student name
            df = pd.read_csv(os.path.join(adjacency_folder, file))  # Read the CSV file
            connections = df['Connected To'].dropna().astype(str).str.strip().tolist()  # Get the connected people
            graph[person].update(connections)  # Add connections to the graph
    
    return graph  # Return the constructed graph


# === Step 2: Perform a Random Walk ===
def random_walk(graph, start, end, max_steps=1000):
    # Ensure both start and end students are in the graph
    if start not in graph or end not in graph:
        return None  # Return None if either student isn't in the graph

    walk = [start]  # Start the walk with the starting student
    current = start  # Set the current student to the starting student

    # Perform random steps
    for _ in range(max_steps):
        if current == end:  # Stop if we reach the destination student
            return walk
        neighbors = list(graph[current])  # Get the neighbors (connections) of the current student
        if not neighbors:  # If there are no neighbors, stop the walk
            break
        next_node = random.choice(neighbors)  # Pick a random neighbor
        walk.append(next_node)  # Add this student to the walk
        current = next_node  # Move to the next student

    # If we reached the destination, return the walk; otherwise, return None
    return walk if current == end else None


# === Step 3: Prune the Random Walk to Remove Cycles (Loops) ===
def prune_walk(walk, start, end):
    if not walk:
        return []
    path = [start]  # Start the pruned path with the starting student
    for node in walk[1:]:  # Loop through the rest of the walk (except the start)
        path.append(node)  # Add each student to the path
        if node == end:  # Stop if we reach the destination student
            break
    return path  # Return the pruned path


# === Step 4: Run Multiple Random Walks & Gather Walk Lengths ===
def try_random_walks(graph, start, end, attempts=100, max_steps=1000):
    walk_lengths = []  # List to store lengths of random walks
    pruned_lengths = []  # List to store lengths of pruned paths
    
    # Try multiple random walks
    for _ in range(attempts):
        walk = random_walk(graph, start, end, max_steps)
        if walk:
            walk_lengths.append(len(walk))  # Add the length of the random walk
            pruned_lengths.append(len(prune_walk(walk, start, end)))  # Add the length of the pruned path
    
    return walk_lengths, pruned_lengths


# === Step 5: Compute Statistics (Mean, Median, Std Dev) ===
def compute_stats(lengths):
    if not lengths:
        return {"mean": None, "median": None, "std": None}  # Return None if no lengths
    
    # Calculate mean, median, and standard deviation of the walk lengths
    return {
        "mean": round(np.mean(lengths), 2),
        "median": round(np.median(lengths), 2),
        "std": round(np.std(lengths), 2)
    }


# === Step 6: Run the Function for Two Students ===
adjacency_folder = "adjacency_folder1"  # Folder where your CSV files are located
graph = load_graph(adjacency_folder)  # Load the graph from the CSV files

# Define the start and end students
start_student = "Shalini Priya"  # Replace with the starting student's name
end_student = "Rani Kumari"  # Replace with the ending student's name

# Perform random walks and calculate the lengths
walk_lengths, pruned_lengths = try_random_walks(graph, start_student, end_student)

# Compute statistics for the random walks and pruned paths
walk_stats = compute_stats(walk_lengths)
pruned_stats = compute_stats(pruned_lengths)

# === Output the Results ===
print(f"📊 Random Walk Stats between '{start_student}' and '{end_student}':")
print("  - Mean Length:", walk_stats["mean"])
print("  - Median Length:", walk_stats["median"])
print("  - Std Deviation:", walk_stats["std"])

print(f"\n🌿 Pruned Path Stats:")
print("  - Mean Length:", pruned_stats["mean"])
print("  - Median Length:", pruned_stats["median"])
print("  - Std Deviation:", pruned_stats["std"])


# In[ ]:




