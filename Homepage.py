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