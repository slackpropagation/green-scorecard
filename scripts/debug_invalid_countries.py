import pandas as pd
import plotly.express as px

merged = pd.read_csv("data/simulated_sites_enriched.csv")  # or your post-merge version
invalid = merged[~merged["country"].isin(px.data.gapminder()["country"].unique())]
print("❗ Countries not recognized by Plotly:")
print(invalid["country"].unique())