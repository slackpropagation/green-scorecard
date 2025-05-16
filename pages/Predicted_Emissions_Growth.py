import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pycountry

# Page setup
st.set_page_config(layout="wide")
st.markdown("## Where Are Emissions Likely to Grow Next?")
st.markdown("""
This page uses a trained machine learning model to identify countries most at risk of increasing their CO₂ emissions in the coming year.
The map below highlights countries with the highest predicted risk scores.
""")

# Load predictions
df = pd.read_csv("data/processed/co2_multi_year_predictions.csv")  # Update path if needed!

# Get latest year
latest_year = df["year"].max()
map_data = df[df["year"] == latest_year].copy()

# Map country names to ISO-3 codes
def iso3(name):
    try:
        return pycountry.countries.lookup(name).alpha_3
    except LookupError:
        return None

map_data["iso_code"] = map_data["country"].map(iso3)
map_data = map_data.dropna(subset=["iso_code", "predicted_growth"])

# Build map (with EPS-style design)
colorscale = [[0, "#00cc44"], [1, "#ef553b"]]
fig = go.Figure(go.Choropleth(
    locations=map_data["iso_code"],
    z=map_data["predicted_growth"],
    text=map_data["country"],
    colorscale=colorscale,
    showscale=False,
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
        text="Predicted CO₂ Emissions Growth by Country",
        x=0.5, y=0.98, xanchor="center",
        font=dict(size=26, color="#e65100", family="Helvetica Neue Bold")
    )
)

fig.add_annotation(
    text="Source: Green Scorecard ML Model Forecasts",
    xref="paper", yref="paper",
    x=0.005, y=-0.03,
    xanchor="left", yanchor="bottom",
    showarrow=False,
    font=dict(size=16, color="#e65100", family="Helvetica Neue Bold")
)

fig.add_annotation(
    text=f"Data Year: {latest_year}",
    xref="paper", yref="paper",
    x=0.995, y=-0.03,
    xanchor="right", yanchor="bottom",
    showarrow=False,
    font=dict(size=16, color="#e65100", family="Helvetica Neue Bold")
)

# Add custom legend annotations at left side of the graph
fig.add_shape(type="rect",
              xref="paper", yref="paper",
              x0=0.03, y0=0.49, x1=0.05, y1=0.51,
              fillcolor="#00cc44",
              line=dict(color="#FFFFFF"))
fig.add_annotation(
    text="On Track",
    xref="paper", yref="paper",
    x=0.055, y=0.502,
    showarrow=False,
    font=dict(size=14, color="#FFFFFF", family="Helvetica Neue Bold"),
    align="left"
)
fig.add_shape(type="rect",
              xref="paper", yref="paper",
              x0=0.03, y0=0.45, x1=0.05, y1=0.47,
              fillcolor="#ef553b",
              line=dict(color="#FFFFFF"))
fig.add_annotation(
    text="At Risk",
    xref="paper", yref="paper",
    x=0.055, y=0.46,
    showarrow=False,
    font=dict(size=14, color="#FFFFFF", family="Helvetica Neue Bold"),
    align="left"
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
        st.plotly_chart(fig, use_container_width=True)

# Add context
st.markdown("""
This map shows the predicted CO₂ emissions growth for each country, using the latest year of forecast data.
Colors indicate binary risk categories: green ("On Track") means no expected increase, red ("At Risk") means likely increase in emissions. Countries in red are likely to face rising emissions unless mitigating actions are taken.
""")