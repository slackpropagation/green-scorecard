import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Green Scorecard", layout="wide")

st.title("🌱 Green Scorecard – CO₂ Emissions Dashboard")

# Load data
df = pd.read_csv("data/simulated_sites.csv")

# Sidebar filters
sites = df["site_id"].unique()
selected_sites = st.sidebar.multiselect("Select Sites", sites, default=sites)

# Filtered view
filtered = df[df["site_id"].isin(selected_sites)]

# Risk classification
def classify_risk(row):
    delta = row["scope_1_emissions"] - row["target_emissions"]
    if delta > row["target_emissions"] * 0.10:
        return "non_compliant"
    elif delta > 0:
        return "at_risk"
    else:
        return "on_track"

filtered["risk_flag"] = filtered.apply(classify_risk, axis=1)

# KPI Cards
col1, col2, col3 = st.columns(3)
col1.metric("Total Sites", len(sites))
col2.metric("Total Quarters", df["quarter"].nunique())
col3.metric("Avg. CO₂ Intensity", f"{filtered['emissions_intensity'].mean():.2f} tCO₂ / 1k units")

# Emissions trend
fig = px.line(filtered, x="quarter", y="scope_1_emissions", color="site_id",
              title="Site-Level Scope 1 Emissions Over Time")
fig.update_layout(xaxis_title="Quarter", yaxis_title="Tons CO₂", height=500)
st.plotly_chart(fig, use_container_width=True)

# Risk by site – bar chart
risk_summary = filtered.groupby(["site_id", "risk_flag"])["scope_1_emissions"].sum().reset_index()

fig2 = px.bar(
    risk_summary,
    x="site_id",
    y="scope_1_emissions",
    color="risk_flag",
    title="Total Scope 1 Emissions by Site and Risk Status",
    labels={"scope_1_emissions": "Tons CO₂", "site_id": "Site"},
    height=500
)
st.plotly_chart(fig2, use_container_width=True)