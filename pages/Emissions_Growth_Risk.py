import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

color_map = {
    "non_compliant": "#d62728",
    "at_risk": "#ff7f0e",
    "on_track": "#2ca02c"
}

df_valid["color"] = df_valid["growth_risk"].map(color_map)

fig = go.Figure(data=go.Choropleth(
    locations=df_valid["iso_code"],
    z=df_valid["growth_risk"].map({"on_track": 1, "at_risk": 2, "non_compliant": 3}),
    text=df_valid["country"],
    hovertext=df_valid.apply(
        lambda row: f"{row['country']}<br>Emissions Growth: {row['co2_growth_prct']:.2f}%<br>EPS: {row['eps_score']}<br>Pressure: {row['pressure_level']}",
        axis=1
    ),
    hoverinfo="text",
    colorscale=[
        [0.0, "#2ca02c"],   # on_track
        [0.5, "#ff7f0e"],   # at_risk
        [1.0, "#d62728"]    # non_compliant
    ],
    colorbar=dict(
        x=0.045, y=0.5,
        xanchor="center", yanchor="middle",
        len=0.45, thickness=18,
        tickvals=[1, 2, 3],
        ticktext=["On Track", "At Risk", "Non-compliant"],
        tickfont=dict(size=14, color="#FFFFFF"),
        outlinecolor="#FFFFFF", outlinewidth=1
    )
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

# Bar chart: Risk Status by Policy Pressure
st.markdown("### 🧊 Risk Status by Policy Pressure")
st.markdown("This bar chart breaks down how emissions growth risk aligns with each country's policy pressure level.")

# Group data
risk_counts = (
    df_valid.groupby(["pressure_level", "growth_risk"])
            .size()
            .reset_index(name="count")
)

# Bar chart
fig_bar = px.bar(
    risk_counts,
    x="pressure_level",
    y="count",
    color="growth_risk",
    barmode="stack",
    color_discrete_map={
        "non_compliant": "#d62728",
        "at_risk": "#ff7f0e",
        "on_track": "#2ca02c"
    },
    category_orders={"pressure_level": ["low", "medium", "high"]},
    labels={"pressure_level": "Policy Pressure", "count": "Number of Countries"}
)
fig_bar.update_layout(margin=dict(t=40, b=40))
st.plotly_chart(fig_bar, use_container_width=True)

st.caption("Data source: Our World in Data + OECD EPS Index")