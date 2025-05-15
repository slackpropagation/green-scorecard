import pandas as pd
import numpy as np

np.random.seed(42)

# Configuration
num_sites = 8
num_quarters = 12
start_year = 2022
site_ids = [f"Site_{chr(65+i)}" for i in range(num_sites)]
site_to_country = {
    "Site_A": "Germany",
    "Site_B": "Brazil",
    "Site_C": "India",
    "Site_D": "United States",
    "Site_E": "South Korea",
    "Site_F": "France",
    "Site_G": "China",
    "Site_H": "United Kingdom"
}
quarters = [f"Q{(q%4)+1}-{start_year + (q//4)}" for q in range(num_quarters)]

# Generate data
records = []
for site in site_ids:
    base_emission = np.random.uniform(1.2e6, 2.5e6)  # tons CO2
    base_output = np.random.uniform(6e6, 10e6)       # MWh
    slope = np.random.normal(-30000, 20000)          # improving or stable
    country = site_to_country[site]
    for i, quarter in enumerate(quarters):
        emissions = base_emission + i * slope + np.random.normal(0, 40000)
        output = base_output + np.random.normal(0, 200000)
        intensity = emissions / output * 1000
        target = base_emission * 0.98**i
        records.append([site, quarter, emissions, output, intensity, target, country])

# Create DataFrame
df = pd.DataFrame(records, columns=[
    "site_id", "quarter", "scope_1_emissions", "output_units",
    "emissions_intensity", "target_emissions", "country"
])

# Save
df.to_csv("data/simulated_sites.csv", index=False)
print("Simulated company data saved to data/simulated_sites.csv")