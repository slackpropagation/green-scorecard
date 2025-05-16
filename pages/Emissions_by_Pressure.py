import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Emissions by Policy Pressure Level", layout="wide")

st.markdown("## Are High-Pressure Countries Emitting More or Less?")
st.markdown("""
This bar chart groups countries by their environmental policy pressure level (Low, Medium, High)
and shows the total CO₂ emissions for each group. It helps visualize whether policy strictness aligns with emissions outcomes.
""")

# Load data
df = pd.read_csv("data/processed/co2_multi_year_predictions.csv")

# Filter out missing pressure levels
df = df[df["pressure_level"].notna()]

# Group by pressure level and sum CO₂ emissions
summary = df.groupby("pressure_level", as_index=False)["co2"].sum()

# Violin Plot: CO₂ Emissions Distribution by Policy Pressure Level
st.markdown("### CO₂ Emissions Distribution (Violin Plot)")

fig_violin = px.violin(
    df,
    x="pressure_level",
    y="co2",
    color="pressure_level",
    box=True,
    points="all",
    labels={"co2": "CO₂ Emissions (tons)", "pressure_level": "Policy Pressure"},
    color_discrete_map={
        "Low": "#00cc44",
        "Medium": "#ffa600",
        "High": "#ef553b"
    }
)

fig_violin.update_layout(
    height=630,
    margin=dict(t=30, l=10, r=10, b=60),
    font=dict(family="Helvetica Neue Bold", size=20, color="#FFFFFF"),
    paper_bgcolor="#2E2E2E",
    plot_bgcolor="#2E2E2E",
    xaxis_title_font=dict(size=20),
    yaxis_title_font=dict(size=20),
    xaxis=dict(tickfont=dict(size=14)),
    yaxis=dict(tickfont=dict(size=14)),
    legend=dict(
        font=dict(size=18),
        title_font=dict(size=20)
    )
)
fig_violin.add_annotation(
    text="CO₂ Emissions Spread by Policy Pressure Level",
    x=0.5, y=1.05, xanchor="center",
    xref="paper", yref="paper",
    showarrow=False,
    font=dict(size=28, color="#e65100", family="Helvetica Neue Bold")
)
fig_violin.add_annotation(
    text="Source: Our World in Data – CO₂ and Greenhouse Gas Emissions",
    xref="paper", yref="paper",
    x=-0.063, y=-0.135,
    xanchor="left", yanchor="bottom",
    showarrow=False,
    font=dict(size=16, color="#e65100", family="Helvetica Neue Bold")
)
fig_violin.add_annotation(
    text="Data Year: 2022",
    xref="paper", yref="paper",
    x=1.148, y=-0.135,
    xanchor="right", yanchor="bottom",
    showarrow=False,
    font=dict(size=16, color="#e65100", family="Helvetica Neue Bold")
)
st.plotly_chart(fig_violin, use_container_width=True)