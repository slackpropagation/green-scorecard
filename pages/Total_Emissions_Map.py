import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🌍 Total Emissions by Country", layout="wide")

st.markdown("## 🌍 Where Are the Emissions Coming From?")
st.markdown(
    """
This map shows the most recent total CO₂ emissions by country, using data from Our World in Data.
Countries are shaded by the scale of their emissions, and contextual policy pressure is available on hover.
"""
)

# Load real emissions + policy data
df = pd.read_csv("data/co2_policy_merged.csv")

# Fix country names for Plotly compatibility
df["country"] = df["country"].replace({
    "South Korea": "Korea, Rep."
})

# Build choropleth map
fig = px.choropleth(
    df,
    locations="country",
    locationmode="country names",
    color="co2",
    hover_name="country",
    hover_data=["year", "co2_per_capita", "eps_score", "pressure_level"],
    color_continuous_scale="Reds",
    title="Total CO₂ Emissions by Country (Most Recent Year)"
)

fig.update_layout(
    margin=dict(l=0, r=0, t=60, b=0),
    coloraxis_colorbar=dict(title="Total CO₂ (million tons)")
)

st.plotly_chart(fig, use_container_width=True)