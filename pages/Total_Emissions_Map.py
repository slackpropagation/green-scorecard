import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="⚠️ Risk by Policy Pressure", layout="wide")

st.markdown("## ⚠️ Are We at Risk of Falling Behind?")
st.markdown(
    """
This chart shows how site compliance risk varies by the policy pressure level of the countries they operate in.
It helps identify whether stricter policy environments lead to better emissions target performance.
"""
)


# Load data
df = pd.read_csv("data/simulated_sites_enriched.csv")

# Calculate risk flag
def classify_risk(row):
    delta = row["scope_1_emissions"] - row["target_emissions"]
    if delta > row["target_emissions"] * 0.10:
        return "non_compliant"
    elif delta > 0:
        return "at_risk"
    else:
        return "on_track"

df["risk_flag"] = df.apply(classify_risk, axis=1)

# Count sites by country and risk_flag
site_risks = df.groupby(["country", "risk_flag"])["site_id"].nunique().reset_index()

# Total sites per country
total_sites = df.groupby("country")["site_id"].nunique().reset_index(name="total_sites")

# Non-compliant sites per country
non_compliant = site_risks[site_risks["risk_flag"] == "non_compliant"].rename(columns={"site_id": "non_compliant_sites"})

# Merge and calculate %
merged = pd.merge(total_sites, non_compliant[["country", "non_compliant_sites"]], on="country", how="left")
merged["non_compliant_sites"] = merged["non_compliant_sites"].fillna(0)
merged["non_compliant_rate"] = merged["non_compliant_sites"] / merged["total_sites"] * 100

# Add EPS score and pressure
merged = pd.merge(merged, df[["country", "eps_score", "pressure_level"]].drop_duplicates(), on="country", how="left")

# Fix country name for Plotly compatibility
merged["country"] = merged["country"].replace({
    "South Korea": "Korea, Rep."
    
})
# Map
fig = px.choropleth(
    merged,
    locations="country",
    locationmode="country names",
    color="non_compliant_rate",
    hover_name="country",
    hover_data=["non_compliant_sites", "total_sites", "pressure_level", "eps_score"],
    color_continuous_scale="Reds",
    title="Non-Compliant Site Rate by Country"
)

fig.update_layout(
    margin=dict(l=0, r=0, t=60, b=0),
    coloraxis_colorbar=dict(title="% Non-Compliant")
)

st.plotly_chart(fig, use_container_width=True)