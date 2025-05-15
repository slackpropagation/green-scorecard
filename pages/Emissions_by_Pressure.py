

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
df = pd.read_csv("data/co2_policy_merged.csv")

# Filter out missing pressure levels
df = df[df["pressure_level"].notna()]

# Group by pressure level and sum CO₂ emissions
summary = df.groupby("pressure_level", as_index=False)["co2"].sum()

# Plot
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

st.caption("Data source: Our World in Data + OECD EPS Index")