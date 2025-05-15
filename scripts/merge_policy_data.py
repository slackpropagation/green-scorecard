import pandas as pd

# Load simulated site data and policy data
sites = pd.read_csv("data/simulated_sites.csv")
policy = pd.read_csv("data/regional_policy.csv")

# Merge on country
merged = pd.merge(sites, policy, on="country", how="left")

# Save merged output
merged.to_csv("data/simulated_sites_enriched.csv", index=False)
print("✅ Merged site data with policy pressure saved to data/simulated_sites_enriched.csv")