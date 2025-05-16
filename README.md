# Green Scorecard: ESG Emissions Intelligence Dashboard

![Version](https://img.shields.io/badge/version-1.0.0-blue) | [MIT License](LICENSE)

**Last Updated:** May 15, 2025

## Table of Contents

- [Executive Summary](#executive-summary)
- [Setup & Requirements](#setup--requirements)
- [Data Sources](#data-sources)
- [ML Model Methodology](#ml-model-methodology)
- [Why It Matters](#why-it-matters)
- [Interactive Exploration & Trend Analysis](#interactive-exploration--trend-analysis)
- [Key Graphs & Insights](#key-graphs--insights)
  - [1. Global Emissions Choropleth](#1-global-emissions-choropleth)
  - [2. Emissions by Policy Pressure](#2-emissions-by-policy-pressure)
  - [3. Risk Status & Compliance](#3-risk-status--compliance)
  - [4. Emissions vs Target (Per Site)](#4-emissions-vs-target-per-site)
  - [5. Predicted Future Breaches](#5-predicted-future-breaches)
- [Strategic Takeaways](#strategic-takeaways)
- [Example Use Cases](#example-use-cases)
- [Next Steps & Recommendations](#next-steps--recommendations)
- [Folder Structure](#folder-structure)
- [License](#license)

## Executive Summary

Green Scorecard delivers an actionable analytics dashboard to **track, visualize, and predict carbon emissions and ESG risk** across countries, regions, and operational sites. It combines regulatory pressure, economic factors, and machine learning–based forecasting to tell a clear story:  
**Where are emissions coming from? Are we compliant? Where do we need to act now?**

By breaking down emissions performance across policy context, geography, risk status, and site-level targets, this tool enables sustainability teams and decision makers to:

- Pinpoint top-emitting regions and track performance against policy pressure  
- Identify sites and regions at greatest risk of falling behind compliance or sustainability goals  
- Reveal underperforming assets requiring urgent intervention  
- Highlight the factors most predictive of future target breaches  
- Support scenario planning and proactive resource allocation using ML-driven forecasts

Ultimately, the dashboard serves as an **ESG “command center”**—guiding organizations toward the most impactful decarbonization strategies, focusing attention on emerging risks, and enabling transparent reporting for stakeholders and regulators.

## Setup & Requirements

- Python 3.10+
- [See `requirements.txt`](requirements.txt) for full package list (includes pandas, numpy, scikit-learn, xgboost, matplotlib, seaborn, plotly, streamlit, etc.)
- All scripts and notebooks should be run from the project root directory

```bash
# Install dependencies
pip install -r requirements.txt

### Quick Start

```bash
git clone https://github.com/yourorg/green-scorecard.git
cd green-scorecard
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run dashboard/streamlit_app.py

## Data Sources

- **Historical CO₂ Emissions:**  
  Country-level, sector-level time series data (processed from official datasets)

- **Policy & Regulatory Pressure:**  
  Country/regional ESG policy intensity, compliance deadlines, and EPS/scorecard indicators

- **Site & Regional Targets:**  
  Custom emissions reduction goals by operational site or region

- **Economic & Demographic Context:**  
  GDP, population, income group, region mapping, and related drivers


## ML Model Methodology

This project leverages a **gradient-boosted regression tree (XGBoost)** model to predict future emissions growth for each country, region, or operational site. The modeling pipeline includes:

- **Data Collection & Cleaning**
  - Aggregates, cleans, and harmonizes emissions, economic, and regulatory datasets.
  - Handles missing values and standardizes categorical/ordinal features.
  - Aligns year-over-year records for robust growth and volatility calculations.

- **Feature Engineering**
  - **Core Features:** CO₂ per capita, emissions intensity, population, GDP, year, region, policy lag, and EPS score.
  - **Derived Signals:** Rolling volatility (3-year std), log-transformed economic metrics, region × income group, and compliance status.
  - **Interaction Terms:** Regional and policy pressure cross-features for richer modeling.

- **Model Training & Validation**
  - Trains XGBoost regression models using cross-year splits (train on prior years, test on most recent).
  - Tunes hyperparameters via randomized search (e.g., `max_depth`, `learning_rate`, `subsample`, `n_estimators`).
  - Evaluates using MAE, MSE, and R² for both accuracy and practical interpretability.

- **Interpretability & Risk Insights**
  - Extracts and visualizes feature importance for transparency.
  - Outputs predicted emissions growth and risk rankings for each entity.
  - Identifies factors most associated with policy breaches and non-compliance.

- **Performance Metrics**
  - **MAE** (Mean Absolute Error) for average prediction error.
  - **MSE** (Mean Squared Error) to penalize large misses.
  - **R² Score** for overall model fit and explainability.
  - Full predictions and explanations are exported for dashboarding and further analytics.

This methodology delivers reliable, explainable emissions forecasts—empowering ESG, sustainability, and compliance teams to focus resources and take proactive, data-driven action.

## Why It Matters

- **Regulatory Pressure:**  
  Climate policy is tightening worldwide—non-compliance means reputational and financial risk.

- **Transparency:**  
  Investors, stakeholders, and the public demand credible ESG progress and data-driven climate action.

- **Proactive Action:**  
  Predictive analytics allow organizations to get ahead of emerging risks, prioritize interventions, and maximize the impact of decarbonization strategies.

## Interactive Exploration & Trend Analysis

In the live Green Scorecard dashboard, stakeholders can interactively filter emissions and compliance data by **country**, **policy pressure level**, **region**, or **site**, enabling rapid segmentation and analysis without any coding required.  
Dynamic visualizations—such as choropleth maps, trend lines, and bar charts—let users:

- **Drill into specific segments** to see how emissions and compliance trends differ across regions, countries, or operational sites.  
- **Contextualize regulatory risk** by observing the distribution of policy pressure and the frequency of target breaches within the dataset.  
- **Rapidly compare scenarios** (e.g., high vs. low policy pressure, compliant vs. non-compliant regions) and make data-driven ESG strategy decisions in real time.

## What You'll See

In the following sections, you’ll find five interactive visualizations that explore different dimensions of emissions performance, regulatory risk, and predictive compliance analytics:

1. **Global Emissions Choropleth** – total emissions by country, with policy/regulatory overlays.
2. **Emissions by Policy Pressure** – bar charts highlighting emissions distribution across regulatory pressure levels.
3. **Risk Status & Compliance** – identify regions or sites most at risk for non-compliance.
4. **Emissions vs Target (Per Site)** – diverging bar charts comparing actual emissions against site-level targets.
5. **Predicted Future Breaches** – a ranked table and visuals spotlighting sites or regions most likely to breach targets in the next period, as forecasted by the ML model.

Each chart is paired with a concise key insight and practical context to guide stakeholder interpretation and action.

## Key Graphs & Insights

### 1. Where Are the Emissions Coming From — and How Fairly?

This section features two side-by-side interactive maps that provide both global scale and context to the emissions story. Together, they help stakeholders see not just *who* emits the most, but also *how* those emissions are distributed relative to population.

#### **a. Total CO₂ Emissions Map**
- **What it shows:**  
  Visualizes each country’s total annual CO₂ emissions (latest year: 2022), using a green-to-brown gradient to highlight the world’s top emitters.
- **Key insight:**  
  Countries like China, the U.S., and India dominate in total emissions. This view grounds the global scale of the climate challenge.
- **How to use:**  
  Hover to view country names and exact emissions totals (metric tons).  
  Use this map for high-level benchmarking, priority setting, and comparing national contributions.

![Total CO₂ Emissions Map](outputs/Total_CO2_Emissions_by_Country.png)

#### **b. CO₂ Emissions Per Capita Map**
- **What it shows:**  
  Adjusts for population, revealing which countries have the highest emissions per person (data: 2022).
- **Key insight:**  
  Smaller, industrialized nations (e.g., Qatar, Australia, U.S.) often top the per capita rankings—contrasting with populous countries that may have large totals but lower individual impact.
- **How to use:**  
  This perspective encourages a nuanced understanding of climate equity and fairness in emissions responsibility.  
  Use for policy conversations about differentiated responsibilities and equitable target setting.

![CO₂ Emissions Per Capita Map](outputs/CO2_Emissions_Per_Capita_by_Country.png)

**Together, these maps provide a comprehensive view of both absolute and relative emissions, enabling more informed discussions on climate action, fairness, and strategic focus.**

### 2. Are High-Pressure Countries Emitting More or Less?

#### **CO₂ Emissions Distribution by Policy Pressure (Violin Plot)**
- **What it shows:**  
  This violin plot visualizes the distribution of country-level CO₂ emissions across three environmental policy pressure levels: Low, Medium, and High.
- **Key insight:**  
  It reveals how emissions are spread within each policy context, making it easy to spot whether high-pressure environments tend to have lower, more tightly grouped emissions—or if outliers persist regardless of regulation.
- **How to use:**  
  Compare the shape, spread, and median of emissions distributions for each policy group.  
  Use this visualization to explore whether stricter environmental regulations are effectively containing emissions, or if significant disparities remain.

![Emissions by Policy Pressure](outputs/Emissions_by_Pressure.png)

**This chart provides a nuanced, data-driven view of the relationship between policy stringency and real-world emissions, empowering more targeted and equitable climate strategies.**

### 3. Emissions Growth Risk by Country

This map categorizes each country into risk tiers according to their recent CO₂ emissions growth rates, providing a global snapshot of climate progress and vulnerability.

- **What it shows:**  
  Each country is color-coded by risk level based on its most recent emissions growth:
    - **Non-compliant:** Emissions increased by more than 5%
    - **At risk:** Emissions increased slightly (0–5%)
    - **On track:** Emissions are declining
- **Key insight:**  
  The map visually spotlights countries at greatest risk of missing their climate targets, helping direct attention to areas requiring urgent policy or technological intervention.
- **How to use:**  
  Instantly scan for emerging problem areas and track global progress toward decarbonization goals.  
  Use the risk tiers to support decision-making around resource allocation, international collaboration, or further investigation.

![Emissions Growth Risk](outputs/Emissions_Growth_Risk.png)

**This visualization transforms complex emissions trends into actionable intelligence—empowering stakeholders to proactively address rising risks and celebrate progress where it’s happening.**

### 4. How Stringent Are National Climate Policies?

This section explores the strength of climate policy frameworks globally, using both a policy stringency map and a scatter plot to compare policy ambition with actual performance.

#### **a. Environmental Policy Stringency (EPS) Score Map**
- **What it shows:**  
  Each country is shaded according to its Environmental Policy Stringency (EPS) score—a direct indicator of how tough their climate regulations are. Darker green denotes stricter policy.
- **Key insight:**  
  Provides instant context for understanding why some countries may be progressing faster (or slower) on climate goals.
- **How to use:**  
  Hover over each country to see its EPS score, CO₂ emissions per capita, and policy pressure classification.
  This map is foundational for interpreting all other dashboard trends and risk signals.

![EPS Score by Country](outputs/EPS_Score_by_Country.png)

#### **b. CO₂ Emissions Per Capita vs. EPS Score (Scatter Plot)**
- **What it shows:**  
  Plots each country’s CO₂ emissions per capita against its EPS score, revealing the relationship between policy strictness and actual emission rates.
- **Key insight:**  
  Quickly highlights cases where high policy ambition hasn’t (yet) translated to lower per capita emissions, as well as success stories where strong policy aligns with strong performance.
- **How to use:**  
  Use this scatter plot to identify policy–performance mismatches, inform discussions about best practices, and inspire data-driven policy recommendations.

**Together, these charts ground all emissions analysis in the real-world context of national climate policy—enabling sharper, fairer, and more strategic decision-making.**

### 5. Where Are Emissions Likely to Grow Next?

This page harnesses machine learning predictions to spotlight future climate risk—highlighting where emissions are expected to rise if no further action is taken.

- **What it shows:**  
  An interactive map visualizing each country’s predicted CO₂ emissions growth for the upcoming year, as forecast by the trained ML model.  
  Colors represent binary risk categories:
    - **Green ("On Track"):** No expected increase in emissions
    - **Red ("At Risk"):** Likely increase in emissions next year
- **Key insight:**  
  Enables early detection of potential future problem areas, so that interventions can be targeted before emissions actually spike.
- **How to use:**  
  Use this map to prioritize proactive engagement, allocate resources efficiently, and plan climate policy updates.  
  Countries highlighted in red are strategic priorities for preemptive action and support.

![Predicted Emissions Growth](outputs/Predicted_Emissions_Growth.png)

**By forecasting emissions growth risk, this visualization empowers stakeholders to shift from reactive to truly proactive climate management—focusing attention and resources where they’ll have the greatest impact.**

## Strategic Takeaways

Our analysis uncovers key risk zones and high-impact opportunities across global emissions and climate policy landscapes:

### Major Risk Points

- **Top Risk:** The largest concentration of rising emissions occurs in countries or regions with high economic activity but insufficient policy pressure. Many of these countries show persistent year-over-year emissions growth, highlighting where urgent policy and technological interventions are needed most.

### Optimization Goals

- **Focus on Policy Lag:** Countries with recent policy adoption (“medium pressure” zones) often show the greatest variability in emissions outcomes. Target these regions for support—bridging the gap between policy rollout and real emissions impact.
- **Support Rapid Decarbonization:** Direct resources to “at risk” countries where emissions are plateauing or growing slightly. These represent pivotal moments for intervention to shift trends downward.

### High-Performing Patterns

- **Best-in-class examples:**  
  - Countries with strict environmental policy (high EPS) and low or declining per capita emissions are leading the way.  
  - Regions with strong economic growth but emissions decoupling from GDP are particularly noteworthy—these should be studied and showcased as success stories.

### Actionable Fixes

- **Tighten Policy Where Needed:** Use the dashboard’s risk and compliance overlays to identify gaps where policy pressure lags behind emissions realities. Prioritize these for regulatory updates and enforcement.
- **Target “At Risk” Sites:** Launch targeted technical assistance and funding initiatives in countries flagged as “At Risk” or “Non-compliant” by the ML model.  
- **Benchmark and Replicate Success:** Study the feature importance chart to identify what factors most strongly drive compliance and emissions reductions; then, replicate successful policies and interventions across similar countries or regions.

## Example Use Cases

### Regulatory Risk Monitoring
Automatically flag countries and regions at highest risk of exceeding emissions targets in the coming year, based on ML predictions. Enable sustainability teams to prioritize regulatory filings, compliance interventions, or international negotiations where they're most urgently needed.

### Targeted Policy Intervention
Direct technical and policy support to “at risk” or “non-compliant” countries identified by the dashboard’s risk map and forecast model. Deploy rapid-response decarbonization programs, incentives, or capacity-building in those areas to prevent target breaches.

### Strategic Investment Planning
Guide capital allocation and technology deployment by focusing on regions where policy stringency is high but performance lags—indicating readiness for rapid improvement with the right investments. Similarly, identify “success stories” to inform best practices and support ESG communications.

### Transparent ESG Reporting
Use visualizations and model outputs to deliver credible, transparent disclosures for board meetings, investor reports, and public ESG filings. Export annotated graphs, compliance heatmaps, and predictive risk tables to back up narrative claims with data.

### Benchmarking and Best Practice Replication
Benchmark performance and policy stringency across multiple countries or business units. Identify top performers and analyze the key drivers behind their success—using feature importance charts—to inform strategies for other regions.

## Next Steps & Recommendations

### Quick Win – Focus on High-Risk Regions
Immediately prioritize engagement with countries flagged as “At Risk” or “Non-compliant” by the ML model. Initiate targeted outreach and policy review sessions with local teams, aiming for measurable progress on emissions growth within the next reporting period.

### Policy Gap Analysis & Action
Conduct a gap analysis in countries where emissions performance is poor despite moderate-to-high policy stringency. Recommend tailored interventions—such as increased enforcement, sector-specific regulation, or financial incentives—to close the policy–performance gap.

### Dashboard Expansion & User Training
Roll out the Green Scorecard dashboard to additional regions and teams. Organize training sessions to ensure ESG, compliance, and executive users are equipped to interpret the data and leverage model insights for proactive planning.

### Integrate Real-Time Data Feeds
Upgrade the analytics pipeline to ingest and process real-time emissions, policy, and economic updates. Enhance the model with continuous retraining and live monitoring, aiming for predictive accuracy improvements and faster response to emerging risks.

### Scenario Planning & ML Model Refinement
Use the dashboard to run “what-if” scenarios—simulating the impact of policy changes or economic shocks on future emissions. Continuously refine the ML model by incorporating new features, additional data sources, and regular cross-validation to sustain and improve forecast quality.

## Folder Structure

```
green-scorecard/
├── data/
│   ├── model/
│   │   └── [Trained ML models for emissions growth prediction]
│   ├── processed/
│   │   └── [Cleaned and feature-engineered datasets ready for analysis]
│   └── raw/
│       └── [Original raw datasets from external sources and APIs]
├── outputs/
│   └── [Exported visualizations]
├── pages/
│   └── [Streamlit app page scripts that define dashboard visualizations]
├── scripts/
│   └── [Python scripts for data cleaning, merging, and ML training]
├── .gitignore
├── Homepage.py
├── LICENSE
├── README.md
└── requirements.txt
```

## License

This project is licensed under the MIT License.  
You are free to use, modify, and distribute it with attribution.  
See the [LICENSE](LICENSE) file for full terms.

## Contributing & Contact

Contributions and feedback are welcome. Please open an issue or submit a pull request on GitHub.  

## Changelog

- **v1.0.0** (2025-05-15): Initial release with ML model, five visualization pages, and actionable recommendations.
