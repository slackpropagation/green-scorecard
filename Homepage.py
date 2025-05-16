import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Green Scorecard", layout="wide")

# === GitHub-style theme settings ===
sns.set_style("whitegrid")
sns.set_context("notebook", font_scale=1.1)
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#D0D7DE",
    "axes.labelcolor": "#24292F",
    "xtick.color": "#57606A",
    "ytick.color": "#57606A",
    "grid.color": "#D0D7DE",
    "text.color": "#24292F",
    "axes.titleweight": "bold",
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "font.family": "Helvetica Neue"
})

# Load data
df = pd.read_csv('data/processed/co2_multi_year_predictions.csv')

# Sidebar filters
st.sidebar.title("Filters")
sites = df["site_id"].unique()
selected_sites = st.sidebar.multiselect("Select Sites", options=sites, default=sites)

# Filter data
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
st.markdown("## Green Scorecard")
st.markdown("### Site-Level CO₂ Emissions Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sites", len(sites))
col2.metric("Total Quarters", df["quarter"].nunique())
col3.metric("Avg. CO₂ Intensity", f"{filtered['emissions_intensity'].mean():.2f} tCO₂ / 1k units")

st.markdown("---")

# Emissions trend
import plotly.express as px
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

# Emissions by policy pressure level
pressure_summary = filtered.groupby("pressure_level")["scope_1_emissions"].sum().reset_index()

fig3 = px.bar(
    pressure_summary,
    x="pressure_level",
    y="scope_1_emissions",
    color="pressure_level",
    title="Total Scope 1 Emissions by Policy Pressure Level",
    labels={"scope_1_emissions": "Tons CO₂", "pressure_level": "Policy Pressure"},
    height=500
)
st.plotly_chart(fig3, use_container_width=True)