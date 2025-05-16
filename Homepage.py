import streamlit as st

st.set_page_config(page_title="Green Scorecard Overview", layout="wide")

# Read the README.md file
with open("README.md", "r", encoding="utf-8") as f:
    readme_content = f.read()

# Render the markdown content from README.md
st.markdown(readme_content)