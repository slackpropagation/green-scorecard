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
df = pd.read_csv("data/processed/co2_multi_year_predictions.csv")

# Fix name
df["country"] = df["country"].replace({"South Korea": "Korea, Rep."})

# If co2_growth_prct is missing or all null, estimate it from co2 and co2_last_year
if "co2_growth_prct" not in df.columns or df["co2_growth_prct"].isnull().all():
    if "co2_last_year" in df.columns and df["co2_last_year"].notnull().any():
        df["co2_growth_prct"] = ((df["co2"] - df["co2_last_year"]) / df["co2_last_year"]) * 100
    else:
        df["co2_growth_prct"] = None

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
# Keep only countries with recognized ISO codes for choropleth rendering
iso_countries = px.data.gapminder()["country"].unique()
df_valid = df_valid[df_valid["country"].isin(iso_countries)]
df_valid["iso_code"] = df_valid["country"].map(
    dict(zip(px.data.gapminder()["country"], px.data.gapminder()["iso_alpha"]))
)

# Choropleth
fig = px.choropleth(
    df_valid,
    locations="iso_code",
    locationmode="ISO-3",
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