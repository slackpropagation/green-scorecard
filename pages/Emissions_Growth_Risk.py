import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="⚠️ Emissions Growth Risk by Country", layout="wide")

st.markdown("## ⚠️ Are We at Risk of Falling Behind?")
st.markdown("""
This map shows which countries are currently at risk based on their recent CO₂ emissions growth.
We classify countries into three risk tiers using their emissions growth rate:
- **Non-compliant**: growth > 5%
- **At risk**: 0–5%
- **On track**: declining emissions
""")

# Load data
df = pd.read_csv("data/co2_policy_merged.csv")

# Fix name
df["country"] = df["country"].replace({"South Korea": "Korea, Rep."})

# Define risk flag
def classify_growth_risk(row):
    if pd.isna(row["co2_growth_prct"]):
        return "unknown"
    elif row["co2_growth_prct"] > 5:
        return "non_compliant"
    elif row["co2_growth_prct"] > 0:
        return "at_risk"
    else:
        return "on_track"

df["growth_risk"] = df.apply(classify_growth_risk, axis=1)

# Filter
df_valid = df[df["growth_risk"] != "unknown"]

# Choropleth
fig = px.choropleth(
    df_valid,
    locations="country",
    locationmode="country names",
    color="growth_risk",
    hover_name="country",
    hover_data=["co2_growth_prct", "eps_score", "pressure_level"],
    color_discrete_map={
        "non_compliant": "#d62728",
        "at_risk": "#ff7f0e",
        "on_track": "#2ca02c"
    },
    title="CO₂ Emissions Growth Risk by Country"
)

fig.update_layout(margin=dict(l=0, r=0, t=60, b=0))
st.plotly_chart(fig, use_container_width=True)

st.caption("Data source: Our World in Data + OECD EPS Index")