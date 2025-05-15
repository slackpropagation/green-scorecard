import pandas as pd

# Load the sector-specific EPA file (Power Plants, all years)
epa = pd.read_csv("data/flight.csv", skiprows=6, low_memory=False)

# Preview columns to confirm structure
print("Available columns:", list(epa.columns))

# Select essential columns
filtered = epa[[
    "FACILITY NAME",
    "STATE",
    "REPORTING YEAR",
    "GHGRP ID",
    "GHG QUANTITY (METRIC TONS CO2e)"
]].copy()

# Rename for clarity
filtered = filtered.rename(columns={
    "FACILITY NAME": "facility_name",
    "STATE": "region",
    "REPORTING YEAR": "reporting_year",
    "GHGRP ID": "facility_id",
    "GHG QUANTITY (METRIC TONS CO2e)": "co2_emissions_tons"
})

# Save cleaned dataset
filtered.to_csv("data/epa_benchmarks.csv", index=False)
print("Saved cleaned EPA benchmark data to data/epa_benchmarks.csv")