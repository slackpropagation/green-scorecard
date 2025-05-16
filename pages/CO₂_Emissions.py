import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Total Emissions by Country", layout="wide")

st.markdown("## Where Are the Emissions Coming From — and How Fairly?")
st.markdown(
    """
This page includes two maps to highlight both total CO₂ emissions and emissions per capita.  
The first map shows the top emitters in absolute terms; the second adjusts for population size to reveal who emits most on a per-person basis.
"""
)

# Load real emissions + policy data
df = pd.read_csv("data/raw/owid-co2-data.csv")

# Filter to most recent year with valid CO₂ data
latest_year = df["year"].max()
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
st.markdown("### Total CO₂ Emissions")

# Total CO₂ Map using go.Figure
fig_total = go.Figure(go.Choropleth(
    locations=df["country"],
    locationmode="country names",
    z=df["co2"],
    text=df["country"],
    colorscale=["#00cc44", "#a0522d"],
    zmin=0,
    zmax=df["co2"].quantile(0.95),
    colorbar=dict(
        x=0.045, y=0.5,
        xanchor="center", yanchor="middle",
        len=0.45, thickness=18,
        tickfont=dict(size=14, color="#FFFFFF"),
        outlinecolor="#FFFFFF", outlinewidth=1
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
    text="Total CO₂ Emissions by Country",
    x=0.5, y=1.02, xanchor="center",
    xref="paper", yref="paper",
    showarrow=False,
    font=dict(size=28, color="#e65100", family="Helvetica Neue Bold")
)
fig_total.add_annotation(
    text="Total CO₂ (metric tons)",
    textangle=-90, xref="paper", yref="paper",
    x=0.00, y=0.5,
    showarrow=False,
    font=dict(size=16, color="#FFFFFF", family="Helvetica Neue Bold")
)
fig_total.add_annotation(
    text="Source: Our World in Data – CO₂ and Greenhouse Gas Emissions",
    xref="paper", yref="paper",
    x=0.005, y=-0.03,
    xanchor="left", yanchor="bottom",
    showarrow=False,
    font=dict(size=16, color="#e65100", family="Helvetica Neue Bold")
)
fig_total.add_annotation(
    text="Data Year: 2022",
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
        st.markdown(""" 
        This map visualizes each country’s total annual CO₂ emissions, highlighting the countries contributing the most to global emissions. The color gradient ranges from green to brown, making it easier to spot major emitters.  
        Emissions data is pulled from Our World in Data and is filtered to include the most recent year (2022) for which data is available. Hovering over a country reveals its name and exact emissions total in metric tons.
        """)

# ---- Map 2: CO₂ per Capita ----
st.markdown("### CO₂ Emissions Per Capita")

fig_capita = go.Figure(go.Choropleth(
    locations=df["country"],
    locationmode="country names",
    z=df["co2_per_capita"],
    text=df["country"],
    colorscale=["#00cc44", "#a0522d"],
    zmin=0,
    zmax=df["co2_per_capita"].quantile(0.95),
    colorbar=dict(
        x=0.038, y=0.5,
        xanchor="center", yanchor="middle",
        len=0.45, thickness=18,
        tickfont=dict(size=14, color="#FFFFFF"),
        outlinecolor="#FFFFFF", outlinewidth=1
    )
))

fig_capita.update_geos(
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
fig_capita.update_layout(
    margin=dict(t=20, l=0, r=0, b=20),
    font=dict(family="Helvetica Neue", color="#FFFFFF", size=16),
    paper_bgcolor="#2E2E2E",
    plot_bgcolor="#2E2E2E",
    height=600
)
fig_capita.add_annotation(
    text="CO₂ Emissions Per Capita by Country",
    x=0.5, y=1.02, xanchor="center",
    xref="paper", yref="paper",
    showarrow=False,
    font=dict(size=28, color="#e65100", family="Helvetica Neue Bold")
)
fig_capita.add_annotation(
    text="CO₂ per Capita",
    textangle=-90, xref="paper", yref="paper",
    x=0.00, y=0.5,
    showarrow=False,
    font=dict(size=16, color="#FFFFFF", family="Helvetica Neue Bold")
)
fig_capita.add_annotation(
    text="Source: Our World in Data – CO₂ and Greenhouse Gas Emissions",
    xref="paper", yref="paper",
    x=0.005, y=-0.03,
    xanchor="left", yanchor="bottom",
    showarrow=False,
    font=dict(size=16, color="#e65100", family="Helvetica Neue Bold")
)
fig_capita.add_annotation(
    text="Data Year: 2022",
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
        st.plotly_chart(fig_capita, use_container_width=True)
        st.markdown("""
        This map shows CO₂ emissions per capita, which helps reveal how emissions scale relative to population. Countries with high per-person emissions stand out more clearly here than in the total emissions map.  
        This view helps contrast industrialized nations with high per capita emissions against populous nations that emit more in total but less per person. Data is sourced from Our World in Data for 2022.
        """)