

import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(layout="wide")
st.markdown("## 🌍 Where Are Emissions Likely to Grow Next?")
st.markdown("""
This page uses a trained machine learning model to identify countries most at risk of increasing their CO₂ emissions in the coming year.
The table below highlights the top countries with the highest predicted risk scores.
""")

# Load predictions
df = pd.read_csv("data/processed/co2_multi_year_predictions.csv")

# Select most recent predictions
latest_year = df["year"].max()
top_risk = (
    df[df["year"] == latest_year]
    .sort_values("predicted_growth", ascending=False)
    .head(20)
    [["country", "year", "predicted_growth", "eps_score", "pressure_level"]]
)

# Display results
st.markdown("### 🧠 Top 20 Countries by Predicted Emissions Growth")
st.dataframe(top_risk.reset_index(drop=True), use_container_width=True)

# Choropleth map of predicted growth
import plotly.graph_objects as go
import pycountry

# Map country names to ISO-3 codes
def iso3(name):
    try:
        return pycountry.countries.lookup(name).alpha_3
    except LookupError:
        return None

df["iso_code"] = df["country"].map(iso3)

# Filter and prepare data for map
map_data = df[df["year"] == latest_year].copy()
map_data = map_data.dropna(subset=["iso_code", "predicted_growth"])

# Build map
fig = go.Figure(go.Choropleth(
    locations=map_data["iso_code"],
    z=map_data["predicted_growth"],
    text=map_data["country"],
    colorscale="Reds",
    colorbar=dict(
        title="Predicted<br>Growth",
        x=0.03, y=0.5, len=0.45, thickness=18,
        tickfont=dict(size=14, color="#FFFFFF"),
        outlinecolor="#FFFFFF", outlinewidth=1
    ),
    marker_line_color="#FFFFFF",
    marker_line_width=0.5,
))

fig.update_geos(
    projection_type="equirectangular",
    bgcolor="#2E2E2E",
    showocean=True, oceancolor="#023156",
    showland=True, landcolor="#0e0f1e",
    showcountries=True,
    showcoastlines=True,
    showframe=False,
    domain=dict(x=[0, 1], y=[0, 1])
)

fig.update_layout(
    margin=dict(t=20, l=0, r=0, b=20),
    paper_bgcolor="#2E2E2E",
    plot_bgcolor="#2E2E2E",
    height=600,
    font=dict(family="Helvetica Neue", color="#FFFFFF", size=16),
    title=dict(
        text="🌍 Predicted CO₂ Emissions Growth by Country",
        x=0.5, y=0.98, xanchor="center",
        font=dict(size=26, color="#e65100", family="Helvetica Neue Bold")
    )
)

# Show map
st.plotly_chart(fig, use_container_width=True)

# Add context
st.markdown("""
This map shows the predicted CO₂ emissions growth for each country, using the latest year of forecast data.
Darker shades indicate higher projected increases. Countries in red are likely to face rising emissions unless mitigating actions are taken.
""")