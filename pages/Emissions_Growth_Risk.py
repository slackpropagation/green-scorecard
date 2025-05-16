import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="⚠️ Emissions Growth Risk Map", layout="wide")

st.markdown("## Emissions Growth Risk by Country")
st.markdown("""
This map classifies each country into one of three risk tiers based on their CO₂ emissions growth rate:
- **Non-compliant**: Emissions increased by more than 5%
- **At risk**: Emissions increased slightly (0–5%)
- **On track**: Emissions are declining

Color coding reflects current trajectory and helps identify countries likely to miss climate targets unless action is taken.
""")

# Load data
df = pd.read_csv("data/processed/co2_multi_year_predictions.csv")

# Fix name
df["country"] = df["country"].replace({"South Korea": "Korea, Rep."})

# Before calculating co2_growth_prct, ensure numeric types for co2 and co2_last_year
df["co2"] = pd.to_numeric(df["co2"], errors="coerce")
df["co2_last_year"] = pd.to_numeric(df["co2_last_year"], errors="coerce")

# If co2_growth_prct is missing or all null, estimate it from co2 and co2_last_year
if "co2_growth_prct" not in df.columns or df["co2_growth_prct"].isnull().all():
    # Compute previous year's CO2 if not already included
    df = df.sort_values(["country", "year"])
    df["co2_last_year"] = df.groupby("country")["co2"].shift(1)
    df["co2_growth_prct"] = ((df["co2"] - df["co2_last_year"]) / df["co2_last_year"]) * 100

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

import pycountry

# Generate ISO-3 codes for choropleth
def iso3(name):
    try:
        return pycountry.countries.lookup(name).alpha_3
    except LookupError:
        return None

df["iso_code"] = df["country"].apply(iso3)
df_valid = df[df["growth_risk"] != "unknown"].copy()
df_valid = df_valid[df_valid["iso_code"].notna()].copy()

color_map = {
    "non_compliant": "#d62728",
    "at_risk": "#ff7f0e",
    "on_track": "#2ca02c"
}

df_valid["color"] = df_valid["growth_risk"].map(color_map)

fig = go.Figure(data=go.Choropleth(
    locations=df_valid["iso_code"],
    z=df_valid["growth_risk"].map({"on_track": 0.0, "at_risk": 0.5, "non_compliant": 1.0}).astype(float),
    zmin=0,
    zmax=1.05,  # adjust max so red is not compressed
    colorscale=[
    [0.0, "#2ca02c"],     # on_track
    [0.33, "#2ca02c"],
    [0.3301, "#ff7f0e"],    # at_risk start
    [0.66, "#ff7f0e"],
    [0.6601, "#d62728"],    # non_compliant start
    [1.0, "#d62728"]
],
    
    colorbar=dict(
        title="",
        x=0.07, y=0.5,
        xanchor="center", yanchor="middle",
        len=0.45, thickness=18,
        tickvals=[0.17, 0.52, 0.87],
        ticktext=["On Track", "At Risk", "Non-compliant"],
        tickfont=dict(size=14, color="#FFFFFF"),
        outlinecolor="#FFFFFF", outlinewidth=1
    ),
    marker=dict(
        line=dict(color="white", width=0.5)
    ),
    text=df_valid["country"],
    hovertext=df_valid.apply(
        lambda row: f"{row['country']}<br>Emissions Growth: {row['co2_growth_prct']:.2f}%<br>EPS: {row['eps_score']}<br>Pressure: {row['pressure_level']}",
        axis=1
    ),
    hoverinfo="text",
    showscale=True
))

fig.update_geos(
    projection_type="equirectangular",
    projection_scale=1,
    bgcolor="#2E2E2E",
    showocean=True, oceancolor="#023156",
    showland=True, landcolor="#0e0f1e",
    showcountries=True,
    showcoastlines=True,
    showframe=False,
    scope="world",
    center=dict(lat=0, lon=0),
    lataxis_range=[-60, 85],
    lonaxis_range=[-180, 180],
    domain=dict(x=[0, 1], y=[0, 1])
)

fig.update_layout(
    margin=dict(t=20, l=0, r=0, b=20),
    font=dict(family="Helvetica Neue", color="#FFFFFF", size=16),
    paper_bgcolor="#2E2E2E",
    plot_bgcolor="#2E2E2E",
    height=600
)

fig.add_annotation(
    text="CO₂ Emissions Growth Risk by Country",
    x=0.5, y=1.02, xanchor="center",
    xref="paper", yref="paper",
    showarrow=False,
    font=dict(size=28, color="#e65100", family="Helvetica Neue Bold")
)

fig.add_annotation(
    text="Emissions Growth Risk",
    textangle=-90, xref="paper", yref="paper",
    x=0.00, y=0.5,
    showarrow=False,
    font=dict(size=16, color="#FFFFFF", family="Helvetica Neue Bold")
)

fig.add_annotation(
    text="Source: Our World in Data + OECD EPS",
    xref="paper", yref="paper",
    x=0.005, y=-0.03,
    xanchor="left", yanchor="bottom",
    showarrow=False,
    font=dict(size=16, color="#e65100", family="Helvetica Neue Bold")
)

fig.add_annotation(
    text="Data Year: 2022",
    xref="paper", yref="paper",
    x=0.995, y=-0.03,
    xanchor="right", yanchor="bottom",
    showarrow=False,
    font=dict(size=16, color="#e65100", family="Helvetica Neue Bold")
)

# Render in Streamlit
left_col, _ = st.columns([3, 1])
with left_col:
    with st.container():
        st.markdown(
            """<style>
            .element-container:has(.plot-container) {
                background-color: #2E2E2E !important;
            }
            </style>""",
            unsafe_allow_html=True,
        )
        st.plotly_chart(fig, use_container_width=True)