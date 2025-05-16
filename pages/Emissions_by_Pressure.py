import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📊 Emissions by Policy Pressure Level", layout="wide")

st.markdown("## 📊 Are High-Pressure Countries Emitting More or Less?")
st.markdown("""
This bar chart groups countries by their environmental policy pressure level (Low, Medium, High)
and shows the total CO₂ emissions for each group. It helps visualize whether policy strictness aligns with emissions outcomes.
""")

# Load data
df = pd.read_csv("data/processed/co2_multi_year_predictions.csv")

# Filter out missing pressure levels
df = df[df["pressure_level"].notna()]

# Group by pressure level and sum CO₂ emissions
summary = df.groupby("pressure_level", as_index=False)["co2"].sum()

# Plot total emissions
fig = px.bar(
    summary,
    x="pressure_level",
    y="co2",
    color="pressure_level",
    title="Total CO₂ Emissions by Policy Pressure Level",
    labels={"co2": "Total CO₂ (tons)", "pressure_level": "Policy Pressure"},
    height=500
)

fig.update_layout(margin=dict(l=0, r=0, t=60, b=0))
st.plotly_chart(fig, use_container_width=True)

# Calculate average CO2 emissions per country within each pressure level
avg_per_country = df.groupby(["pressure_level", "country"], as_index=False)["co2"].mean()
avg_summary = avg_per_country.groupby("pressure_level", as_index=False)["co2"].mean()

# Plot average emissions per country
fig_avg = px.bar(
    avg_summary,
    x="pressure_level",
    y="co2",
    color="pressure_level",
    title="Average CO₂ Emissions per Country by Policy Pressure Level",
    labels={"co2": "Average CO₂ (tons)", "pressure_level": "Policy Pressure"},
    height=500
)

fig_avg.update_layout(margin=dict(l=0, r=0, t=60, b=0))
st.plotly_chart(fig_avg, use_container_width=True)

st.caption("Data source: Our World in Data + OECD EPS Index")

# Treemap: CO₂ Contribution by Country within Pressure Levels
st.markdown("### 🗺️ CO₂ Contribution Breakdown by Country (Treemap)")

fig_treemap = px.treemap(
    df,
    path=["pressure_level", "country"],
    values="co2",
    color="pressure_level",
    color_discrete_map={
        "Low": "#00cc44",
        "Medium": "#ffa600",
        "High": "#ef553b"
    },
    title="CO₂ Emissions Treemap by Policy Pressure Level and Country",
)

fig_treemap.update_layout(margin=dict(t=60, l=0, r=0, b=0))
st.plotly_chart(fig_treemap, use_container_width=True)

# Box Plot: CO₂ Emissions Distribution by Policy Pressure Level
st.markdown("### 📦 CO₂ Emissions Distribution by Policy Pressure Level")

fig_box = px.box(
    df,
    x="pressure_level",
    y="co2",
    color="pressure_level",
    title="Distribution of CO₂ Emissions by Policy Pressure Level",
    labels={"co2": "CO₂ Emissions (tons)", "pressure_level": "Policy Pressure"},
)

fig_box.update_layout(margin=dict(t=60, l=0, r=0, b=0))
st.plotly_chart(fig_box, use_container_width=True)

# Violin Plot: CO₂ Emissions Distribution by Policy Pressure Level
st.markdown("### 🎻 CO₂ Emissions Distribution (Violin Plot)")

fig_violin = px.violin(
    df,
    x="pressure_level",
    y="co2",
    color="pressure_level",
    box=True,
    points="all",
    title="Violin Plot of CO₂ Emissions by Policy Pressure Level",
    labels={"co2": "CO₂ Emissions (tons)", "pressure_level": "Policy Pressure"},
)

fig_violin.update_layout(margin=dict(t=60, l=0, r=0, b=0))
st.plotly_chart(fig_violin, use_container_width=True)