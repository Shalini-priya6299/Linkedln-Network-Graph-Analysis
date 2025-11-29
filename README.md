For report here's link: (https://github.com/Shalini-priya6299/Linkedln-Network-Graph-Analysis/blob/main/LinkedIn_Network_Analysis_Report_ShaliniPriya.pdf)

# LinkedIn Network Graph Analysis

A reproducible project for building, analyzing, and visualizing professional network graphs (LinkedIn-style). This repository contains code, notebooks, and scripts to convert LinkedIn connection/export data into a graph, compute network metrics (centrality, community detection, shortest paths), and create interactive visualizations.



Table of contents
- Project overview
- Key features
- Repository structure
- Getting started
- Data collection and privacy
- Typical workflow
- Analysis & visualizations
- Example commands
- Development & contribution
- License & contact

Project overview
This project helps you convert exported LinkedIn connections (or other contact lists) into a network graph, perform exploratory network analysis, detect communities, compute centralities, and produce interactive visualizations (HTML/Plotly/PyVis). It is intended for academic, personal insight, or organizational network analysis — not for automated harvesting or violating platform policies.

Key features
- Parse LinkedIn connection exports and normalize contact data.
- Build a graph (NetworkX) where nodes are people and edges represent connections/relationships.
- Compute network metrics: degree, betweenness, closeness, eigenvector centrality.
- Detect communities (Louvain / modularity-based).
- Visualize graphs interactively (pyvis, plotly) and export static figures (matplotlib/seaborn).
- Provide reusable notebooks and scripts for reproducible analysis.

Repository structure (suggested)
- data/
  - raw/                   # raw exports (CSV/JSON) — NOT checked into VCS
  - processed/             # cleaned and processed datasets (CSV/graphml)
- notebooks/
  - 01-data-cleaning.ipynb
  - 02-build-graph.ipynb
  - 03-analysis.ipynb
  - 04-visualization.ipynb
- scripts/
  - collect_data.py        # optional helpers (API wrapper / import helpers)
  - build_graph.py         # build NetworkX graph from processed CSV
  - analyze_graph.py       # compute metrics and save outputs
  - visualize_graph.py     # export interactive HTML visualizations
- requirements.txt
- README.md
- LICENSE

Getting started (local)
1. Clone the repo
   git clone https://github.com/Shalini-priya6299/Linkedln-Network-Graph-Analysis.git
   cd Linkedln-Network-Graph-Analysis

2. Create a virtual environment (recommended)
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   .venv\Scripts\activate     # Windows

3. Install dependencies
   pip install -r requirements.txt

Common dependencies (adjust to repo's requirements.txt)
- Python 3.8+
- pandas
- networkx
- numpy
- matplotlib
- seaborn
- pyvis (for interactive HTML visualizations)
- python-louvain (community)
- plotly
- scikit-learn (optional)
- jupyterlab / notebook
- beautifulsoup4 / requests or linkedin-api (if using API) — use responsibly
(If your repository already contains a requirements.txt, install from that file.)

Data collection & privacy
- Prefer official export/API: LinkedIn provides a "Download your data" option. Use that CSV/JSON export as your primary data source.
- Never commit raw/PII data to the repository. Add data/raw/ to .gitignore.
- Anonymize or pseudonymize personal data when publishing or sharing results.
- If you consider scraping, stop: scraping LinkedIn can violate their Terms of Service and may be illegal in some jurisdictions.

Typical workflow
1. Export LinkedIn connections (CSV/JSON) or provide a dataset.
2. Place the raw export in data/raw/ (do not commit).
3. Run data cleaning notebook/script to produce data/processed/connections.csv.
4. Run build_graph.py or the corresponding notebook to produce a NetworkX graph and optionally export graphml (data/processed/graph.graphml).
5. Run analyze_graph.py or the notebook to compute metrics and community assignments.
6. Visualize results via visualize_graph.py or notebooks (export interactive HTML to outputs/).

Analysis & visualizations (examples)
- Degree distribution and centrality ranking (top influencers by degree/betweenness).
- Community detection: Louvain algorithm to find clusters (teams, industries, geographies).
- Subgraph analysis: ego networks around key nodes to study local structure.
- Temporal analysis: if timestamps exist, analyze growth and new-connection patterns.
- Interactive visualizations: use PyVis to export an HTML file you can open in a browser.


Contributing
1. Fork the repository
2. Create a feature branch: git checkout -b feature/your-feature
3. Make changes and include tests where applicable
4. Open a pull request describing the change

Contact
Project maintained by: Shalini-priya6299
For questions or contributions, open an issue or pull request on the repository.
