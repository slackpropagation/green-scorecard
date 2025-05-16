

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