import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📶 EPS Score vs Emissions Intensity", layout="wide")

st.markdown("## 📶 Does Policy Stringency Lower Emissions Intensity?")
st.markdown("""
This scatter plot compares each country's environmental policy stringency (EPS score) to its CO₂ emissions per unit of GDP.
Use this chart to examine whether countries with stricter climate policies tend to emit more efficiently.
""")

# Load data
df = pd.read_csv("data/processed/co2_policy_merged.csv")

# Fix names for compatibility
df["country"] = df["country"].replace({"South Korea": "Korea, Rep."})

# Filter for valid EPS score and CO₂ per capita
filtered = df[df["eps_score"].notna() & df["co2_per_capita"].notna()]

# Build scatter plot without trendline
fig = px.scatter(
    filtered,
    x="eps_score",
    y="co2_per_capita",
    hover_name="country",
    hover_data=["co2", "co2_growth_prct"],
    title="EPS Score vs CO₂ Emissions per Capita",
    labels={
        "eps_score": "Environmental Policy Stringency (EPS)",
        "co2_per_capita": "CO₂ per Capita (tons/person)"
    },
    height=600
)

fig.update_traces(marker=dict(size=10, opacity=0.7), selector=dict(mode='markers'))
fig.update_layout(margin=dict(l=0, r=0, t=60, b=0))

st.plotly_chart(fig, use_container_width=True)
st.caption("Data source: Our World in Data + OECD EPS Index")