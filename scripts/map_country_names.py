import pandas as pd
from thefuzz import process

# Load EPS dataset
eps_df = pd.read_csv("data/OECD,DF_EPS,+all.csv")
eps_countries = eps_df["Country"].dropna().unique()

# Load OWID CO₂ dataset
owid_df = pd.read_csv("data/owid-co2-data.csv")
owid_countries = owid_df["country"].dropna().unique()

# Match each OECD country to closest OWID country
matches = []
for eps_country in eps_countries:
    best_match, score = process.extractOne(eps_country, owid_countries)
    matches.append({"eps_country": eps_country, "matched_owid_country": best_match, "match_score": score})

# Save to CSV for review
mapping_df = pd.DataFrame(matches)
mapping_df.to_csv("data/country_mapping.csv", index=False)
print("Country mapping saved to data/country_mapping.csv")
