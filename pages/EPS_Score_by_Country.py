import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="EPS Score by Country", layout="wide")

st.markdown("## How Stringent Are National Climate Policies?")
st.markdown("""
This map visualizes each country’s Environmental Policy Stringency (EPS) score; a measure of how strict their climate-related policies are. Countries with stronger policies appear in deeper green.  
Hovering reveals not just the EPS score but also CO₂ emissions per capita and pressure classification, helping us identify policy–performance mismatches.  
This view sets the stage for the rest of the dashboard by grounding all emissions trends and risk predictions in their policy environment.
""")

# Load real emissions + policy data
df = pd.read_csv("data/processed/co2_policy_merged.csv")

# Filter to most recent year with valid CO₂ data
latest_year = int(df["year"].max())
df = df[(df["year"] == latest_year) & (df["co2"].notna())].copy()

# Fix country names for Plotly compatibility
df["country"] = df["country"].replace({
    "South Korea": "Korea, Rep.",
    "Czechia": "Czech Republic",
    "Myanmar": "Burma",
    "Eswatini": "Swaziland",
    "Democratic Republic of Congo": "Democratic Republic of the Congo",
    "Republic of Congo": "Congo (Brazzaville)",
    "United States": "United States of America",
    "Russia": "Russian Federation",
    "Vietnam": "Viet Nam",
    "Syria": "Syrian Arab Republic",
    "Laos": "Lao PDR",
    "Cape Verde": "Cabo Verde"
})

# ---- Map 1: Total CO₂ ----
st.markdown("### Environmental Policy Stringency (EPS) Score by Country")

# Total CO₂ Map using go.Figure
fig_total = go.Figure(go.Choropleth(
    locations=df["country"],
    locationmode="country names",
    z=df["eps_score"],
    text=df["country"],
    colorscale=["#ffffff", "#00cc44"],
    zmin=0,
    zmax=df["eps_score"].max(),
    colorbar=dict(
        x=0.035, y=0.5,
        xanchor="center", yanchor="middle",
        len=0.45, thickness=18,
        tickfont=dict(size=14, color="#FFFFFF"),
        outlinecolor="#FFFFFF", outlinewidth=1
    ),
    customdata=df[["co2_per_capita", "pressure_level"]],
    hovertemplate=(
        "%{text}<br>"
        "EPS Score: %{z}<br>"
        "CO₂ per Capita: %{customdata[0]}<br>"
        "Pressure: %{customdata[1]}<extra></extra>"
    )
))

fig_total.update_geos(
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
fig_total.update_layout(
    margin=dict(t=20, l=0, r=0, b=20),
    font=dict(family="Helvetica Neue", color="#FFFFFF", size=16),
    paper_bgcolor="#2E2E2E",
    plot_bgcolor="#2E2E2E",
    height=600
)

fig_total.add_annotation(
    text="EPS Score by Country",
    x=0.5, y=1.02, xanchor="center",
    xref="paper", yref="paper",
    showarrow=False,
    font=dict(size=28, color="#e65100", family="Helvetica Neue Bold")
)
fig_total.add_annotation(
    text="EPS Score",
    textangle=-90, xref="paper", yref="paper",
    x=0.00, y=0.5,
    showarrow=False,
    font=dict(size=16, color="#FFFFFF", family="Helvetica Neue Bold")
)
fig_total.add_annotation(
    text="Source: OECD EPS Scores merged with Our World in Data emissions",
    xref="paper", yref="paper",
    x=0.005, y=-0.03,
    xanchor="left", yanchor="bottom",
    showarrow=False,
    font=dict(size=16, color="#e65100", family="Helvetica Neue Bold")
)
fig_total.add_annotation(
    text=f"Data Year: {latest_year}",
    xref="paper", yref="paper",
    x=0.995, y=-0.03,
    xanchor="right", yanchor="bottom",
    showarrow=False,
    font=dict(size=16, color="#e65100", family="Helvetica Neue Bold")
)
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
        st.plotly_chart(fig_total, use_container_width=True)
        
        
        