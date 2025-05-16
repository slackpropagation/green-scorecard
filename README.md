# Green Scorecard: ESG Emissions Intelligence Dashboard

![Version](https://img.shields.io/badge/version-1.0.0-blue) | [MIT License](LICENSE)

**Last Updated:** May 15, 2025

## Table of Contents

- [A Story of Impact](#a-story-of-impact)
- [Who This Dashboard Empowers](#who-this-dashboard-empowers)
- [Setup & Requirements](#setup--requirements)
- [Data Sources](#data-sources)
- [How the ML Model Works](#how-the-ml-model-works)
- [Why It Matters](#why-it-matters)
- [Exploring the Dashboard](#exploring-the-dashboard)
- [Key Visualizations & Insights](#key-visualizations--insights)
- [Strategic Takeaways](#strategic-takeaways)
- [Example Use Cases](#example-use-cases)
- [Next Steps & Recommendations](#next-steps--recommendations)
- [Folder Structure](#folder-structure)
- [License](#license)

## A Story of Impact

> *Imagine you’re a sustainability leader, a policymaker, or an investor. You know climate change is urgent, but the data is overwhelming and fragmented. Which regions or sites should you focus on? Where are emissions rising fastest, and what’s driving those changes? How can you prove progress—and spot trouble—before it’s too late?*
>
> The **Green Scorecard** dashboard is your answer. It weaves together emissions, policy, and economic data, using advanced machine learning to turn complexity into clarity. With interactive visuals and clear risk signals, you can see not just what’s happening, but why—and what to do next.

## Who This Dashboard Empowers

- **ESG & Sustainability Teams:** Prioritize decarbonization projects, benchmark sites, and report with confidence.
- **Regulators & Policymakers:** Identify compliance gaps, assess policy effectiveness, and target interventions.
- **Investors & Boards:** Track ESG risk, verify progress, and support transparent climate disclosures.
- **Site Managers & Operations:** Understand local targets, risks, and opportunities for rapid improvement.

## Setup & Requirements

- Python 3.10+
- [See `requirements.txt`](requirements.txt) for full package list (pandas, numpy, scikit-learn, xgboost, matplotlib, seaborn, plotly, streamlit, etc.)
- All scripts and notebooks should be run from the project root directory

```bash
# Install dependencies
pip install -r requirements.txt
```

### Quick Start

```bash
git clone https://github.com/yourorg/green-scorecard.git
cd green-scorecard
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run dashboard/streamlit_app.py
```

## Data Sources

The Green Scorecard leverages multiple authoritative datasets to provide a comprehensive and accurate view of emissions and ESG risk:

- **Historical CO₂ Emissions:**  
  Time series data from **Our World in Data** (OWID) spanning 1990–2022, covering 200+ countries and key sectors. Updated annually. Data includes scope 1 and scope 2 emissions where available.

- **Policy & Regulatory Pressure:**  
  Compiled from the **Environmental Policy Stringency (EPS) database** by the OECD, combined with national regulatory filings and third-party ESG providers. Updated quarterly to reflect latest policy changes and compliance deadlines.

- **Site & Regional Targets:**  
  Custom datasets provided by partnering organizations, detailing emissions reduction targets for specific operational sites or regions. Data is aggregated and anonymized to protect confidentiality.

- **Economic & Demographic Context:**  
  GDP, population, income group, and regional classifications sourced from the **World Bank** and **United Nations** databases. Used for normalization and benchmarking.

### Data Harmonization and Quality

All datasets undergo preprocessing to align temporal and geographic scopes, standardize units and categories, and remove inconsistencies. Missing values are imputed where possible using statistical methods. Data limitations, such as gaps in reporting or differing methodologies, are transparently documented in accompanying metadata.

## How the ML Model Works

The dashboard’s forecasts are powered by a **gradient-boosted regression tree (XGBoost)** model that predicts emissions growth for each country, region, or operational site. This model was chosen for its strong performance on tabular data and its ability to capture complex, non-linear relationships while maintaining interpretability.

The modeling pipeline includes:

- **Data Cleaning:**  
  - Aggregates diverse datasets on emissions, economic indicators, and regulatory environments.  
  - Handles missing or inconsistent values using imputation techniques and filtering to ensure data quality.  
  - Aligns data across time and geography to create consistent year-over-year records.

- **Feature Engineering:**  
  - **Core Features:**  
    - CO₂ emissions per capita and total emissions intensity, reflecting both absolute and relative environmental impact.  
    - Population, GDP, year, and region to provide socio-economic and temporal context.  
    - Policy lag and Environmental Policy Stringency (EPS) scores to capture regulatory pressure and timing effects.  
  - **Derived Features:**  
    - Rolling volatility over 3 years to model fluctuations and uncertainty in emissions.  
    - Log transformations of economic metrics to normalize skewed data distributions.  
    - Compliance status flags to indicate whether entities met previous targets.  
    - Interaction terms between region and income group or policy variables to detect combined effects.

- **Model Training:**  
  - Uses cross-year data splits to simulate real-world forecasting: training on all years prior to the test year to evaluate predictive accuracy over time.  
  - Hyperparameters such as learning rate, tree depth, subsample ratios, and number of estimators are tuned via randomized search to balance bias-variance trade-offs.  
  - Performance is evaluated using multiple metrics:  
    - Mean Absolute Error (MAE) to measure average prediction error.  
    - Mean Squared Error (MSE) to penalize larger deviations more heavily.  
    - R² score to quantify overall explanatory power and fit quality.

- **Interpretability & Risk Insights:**  
  - Feature importance charts reveal which factors most influence emissions growth predictions, enabling domain experts to validate and understand the model’s decisions.  
  - Generates risk rankings and predicted likelihoods of target breaches for each country, region, or site, helping prioritize interventions.

This rigorous approach ensures the dashboard delivers **reliable, transparent, and actionable forecasts**—allowing stakeholders to make informed decisions proactively, rather than simply reacting to unforeseen risks.

## Why It Matters

- **Tighter Regulations:**  
  Governments worldwide are enacting stricter climate policies to meet global targets like the Paris Agreement. Non-compliance can lead to significant financial penalties, legal challenges, and damage to corporate reputation.

- **Transparency Demanded:**  
  Investors, customers, and the public increasingly expect companies and governments to provide credible, data-driven evidence of their ESG performance and climate commitments. Transparent reporting builds trust and supports capital access.

- **Proactive Action:**  
  Traditional reporting often lags behind real-world emissions changes. By using predictive analytics, organizations can anticipate risks and intervene early—avoiding costly penalties, operational disruptions, and reputational harm.

- **Resource Optimization:**  
  With finite budgets for sustainability initiatives, this dashboard helps prioritize investments where they will have the greatest impact, ensuring efficient use of capital and faster progress toward decarbonization goals.

- **Competitive Advantage:**  
  Early adopters of data-driven ESG strategies can better navigate regulatory complexity, improve stakeholder confidence, and differentiate themselves in markets increasingly shaped by sustainability criteria.

- **Global Impact:**  
  Addressing climate change requires coordinated action across multiple levels. This tool empowers decision-makers at all scales—from global regulators to local site managers—to align efforts and accelerate meaningful emissions reductions.

## Key Visualizations & Insights

### 1. Where Are Emissions Coming From—and How Fairly?

This foundational visualization pair provides both the *scale* and *equity* perspectives crucial to understanding global emissions dynamics:

#### **a. Total CO₂ Emissions Map**
- **What it shows:**  
  This choropleth map visualizes the absolute annual CO₂ emissions by country (latest year available, 2022). Countries are shaded on a green-to-brown spectrum, where darker brown indicates higher emissions.  
- **Why it matters:**  
  Identifying the largest emitters is vital for targeting international climate efforts, policy negotiations, and investment in decarbonization technologies. It highlights the countries driving the global carbon footprint.  
- **Data nuances:**  
  Totals reflect reported scope 1 emissions; however, reporting standards vary by country and sector. Large populous countries may dominate totals due to scale rather than intensity.

![Total CO₂ Emissions Map](outputs/Total_CO2_Emissions_by_Country.png)

#### **b. CO₂ Emissions Per Capita Map**
- **What it shows:**  
  This map adjusts emissions by population size, revealing emissions intensity per person. Darker shades highlight countries with the highest per capita carbon footprints.  
- **Why it matters:**  
  This perspective underscores climate equity—smaller or wealthier countries with high per capita emissions bear a disproportionate responsibility per person compared to populous nations with lower individual footprints.  
- **Interpretation guidance:**  
  This map helps policymakers, investors, and stakeholders balance absolute emissions reductions with fairness and differentiated responsibilities. It also exposes opportunities where behavior or technology change can have outsized impact.

![CO₂ Emissions Per Capita Map](outputs/CO2_Emissions_Per_Capita_by_Country.png)

**Together, these maps help you weigh both absolute and relative responsibility—crucial for fair climate strategies.**

### 2. Are High-Pressure Countries Emitting More or Less?

This analysis explores the relationship between environmental policy pressure and actual emissions outcomes, providing insight into the effectiveness of regulatory frameworks worldwide.

#### **CO₂ Emissions by Policy Pressure (Violin Plot)**
- **What it shows:**  
  This violin plot depicts the distribution of country-level CO₂ emissions segmented by three policy pressure categories: Low, Medium, and High. The shape and spread illustrate how emissions vary within each group, capturing both central tendencies and outliers.

- **Why it matters:**  
  Understanding how emissions correlate with policy pressure helps stakeholders assess if stricter regulations lead to meaningful emissions reductions. It reveals whether high-pressure countries successfully contain emissions or if exceptions and challenges persist despite regulatory efforts.

- **Key observations:**  
  - Countries under **High** policy pressure often show a more concentrated distribution with lower median emissions, indicating effective regulatory impact in many cases.  
  - The **Medium** pressure group exhibits wider variance, suggesting mixed results where some countries struggle to meet targets while others perform well.  
  - **Low** pressure countries tend to have broader and higher emissions distributions, reflecting fewer constraints and potentially higher environmental risk.

- **How to use:**  
  Policymakers and ESG analysts can use this chart to identify policy areas needing reinforcement and to benchmark country performance within pressure categories. It also helps in setting realistic expectations for emissions reductions tied to policy ambition.

![Emissions by Policy Pressure](outputs/Emissions_by_Pressure.png)

**This chart empowers more targeted, equitable climate action.**

### 3. Emissions Growth Risk by Country

This visualization categorizes countries based on their recent CO₂ emissions growth rates, providing a clear, at-a-glance picture of global climate progress and emerging risks.

- **Non-compliant:** Countries with emissions increasing by more than 5%, indicating rapid growth that threatens climate targets and compliance obligations.
- **At risk:** Countries with moderate emissions growth between 0% and 5%, signaling potential challenges in maintaining or improving current trajectories.
- **On track:** Countries where emissions are declining, showing successful mitigation efforts and alignment with decarbonization goals.

**Why it matters:**  
By color-coding nations according to risk tiers, stakeholders can quickly identify geographic hotspots where climate action is most urgently needed. This helps prioritize resources, monitor policy effectiveness, and engage in timely interventions.

**Data nuances:**  
Growth calculations are based on year-over-year changes in scope 1 emissions, which can be affected by reporting delays and data quality variations. The classification thresholds are designed to balance sensitivity with practical actionability.

**Key use:**  
This map enables decision-makers, investors, and regulators to instantly scan for problem areas, celebrate progress, and make data-driven decisions on allocating capital and support.

![Emissions Growth Risk](outputs/Emissions_Growth_Risk.png)

### 4. How Stringent Are National Climate Policies?

This section explores the strength and impact of climate regulations globally by examining Environmental Policy Stringency (EPS) scores alongside emissions data, providing vital context for understanding policy effectiveness.

#### **a. Environmental Policy Stringency (EPS) Score Map**
- **What it shows:**  
  A global map shading each country by its EPS score, which quantifies the strictness of its climate-related policies. Darker green areas indicate stronger and more comprehensive regulatory frameworks.

- **Why it matters:**  
  Policy stringency directly influences a country’s ability to curb emissions. This map helps stakeholders understand regulatory environments, identify leaders in climate governance, and pinpoint regions where policy reinforcement may be needed.

- **Data considerations:**  
  EPS scores integrate multiple policy dimensions, including carbon pricing, renewable energy mandates, and emissions standards. However, the effectiveness of policies depends not only on stringency but also on enforcement and economic factors.

- **How to use:**  
  Use this visualization as a baseline to interpret emissions and risk trends elsewhere in the dashboard. It helps explain why some countries achieve emissions reductions while others lag despite economic growth.

![EPS Score by Country](outputs/EPS_Score_by_Country.png)

#### **b. CO₂ Emissions Per Capita vs. EPS Score (Scatter Plot)**
- **What it shows:**  
  This scatter plot compares each country’s per capita CO₂ emissions against its EPS score, revealing how policy ambition translates (or fails to translate) into actual emissions performance.

- **Why it matters:**  
  It highlights policy–performance mismatches where high stringency hasn’t yet led to emissions reductions, indicating implementation gaps or external challenges. Conversely, it showcases best-practice leaders achieving low emissions with strong policies.

- **Interpretation guidance:**  
  Countries clustered in the high EPS but high emissions quadrant warrant further investigation and potential support. Those in the low emissions, high EPS quadrant serve as benchmarks for effective climate governance.

- **How to use:**  
  Stakeholders can leverage this analysis to tailor interventions, share successful policy models, and prioritize funding or technical assistance.

**Together, these visualizations provide a comprehensive lens on how national climate policies shape emissions outcomes—critical for designing smarter, fairer, and more effective climate strategies.**

### 5. Where Are Emissions Likely to Grow Next?

Harnessing advanced machine learning techniques, this visualization forecasts future CO₂ emissions growth at the country, regional, and site levels—providing early warning signals for emerging climate risks.

- **ML-Powered Forecast:**  
  An interactive map displays predicted emissions growth for the upcoming year, based on a gradient-boosted regression model trained on historical emissions, economic indicators, and policy data.

- **Color Coding:**  
  - **Green ("On Track")** indicates entities forecasted to maintain or reduce emissions, aligning with climate targets.  
  - **Red ("At Risk")** flags those predicted to experience emissions increases, highlighting urgent intervention needs.

- **Why it matters:**  
  Predictive insights allow stakeholders to shift from reactive to proactive management—allocating resources, updating policies, and engaging partners before emissions actually rise.

- **Data Integrity:**  
  Predictions incorporate uncertainty measures and are regularly validated against new data to ensure reliability. Users should interpret forecasts alongside contextual knowledge.

- **How to use:**  
  Use this map to prioritize regions and sites for policy reinforcement, technology deployment, and investment. It serves as a strategic planning tool for sustainability leaders, regulators, and investors.

![Predicted Emissions Growth](outputs/Predicted_Emissions_Growth.png)

## Strategic Takeaways

### Major Risk Points
- Rising emissions are concentrated in economically active regions where environmental policies are less stringent or poorly enforced, creating hotspots of regulatory and climate risk.
- Countries classified under “Medium pressure” exhibit the most inconsistent emissions trends, indicating that policy implementation and enforcement vary widely, presenting both challenges and opportunities for targeted intervention.
- Persistent emissions growth in these zones signals a critical need for focused technical assistance, policy reform, and investment to curb escalating climate impacts.
- Failure to address these risk points may lead to significant non-compliance penalties, increased carbon pricing exposure, and damage to corporate and national reputations on the global stage.

### High-Performing Patterns

- **Best-in-class examples:**  
  Countries and regions that combine **strict environmental policies** with **sustained low or declining per capita emissions** demonstrate effective climate governance and strong commitment to decarbonization. These leaders often invest in clean technologies, enforce rigorous standards, and incentivize green innovation.  
- **Economic decoupling:**  
  Several success stories show that **economic growth can be decoupled from emissions increases**, meaning GDP expands without a corresponding rise in carbon output. This highlights the potential for sustainable development and the effectiveness of policies promoting energy efficiency, renewable energy adoption, and circular economy principles.  
- **Key drivers:**  
  Common characteristics among high performers include robust regulatory frameworks, transparent monitoring, public-private partnerships, and targeted investments in low-carbon infrastructure.  
- **Lessons learned:**  
  These patterns serve as models for other countries and sites aiming to balance economic development with environmental stewardship, offering replicable strategies to accelerate global emissions reductions.

**Understanding these patterns helps stakeholders identify scalable best practices and prioritize efforts for maximum climate impact.**

### Actionable Fixes

- **Tighten policy where risk is highest:**  
  Prioritize strengthening environmental regulations and enforcement in regions or sites identified as high risk by emissions growth and policy gap analyses. This may include updating emissions standards, increasing monitoring and reporting requirements, and enhancing penalties for non-compliance.

- **Launch rapid-response decarbonization programs:**  
  Deploy targeted interventions—such as technology upgrades, energy efficiency projects, and renewable energy investments—in “At Risk” and “Non-compliant” sites highlighted by the ML model. Rapid action can prevent further emissions growth and improve overall compliance rates.

- **Study and replicate successful strategies:**  
  Analyze the underlying factors driving compliance and emissions reductions in high-performing countries or sites, using feature importance insights from the model. Scale proven policies, operational practices, and incentive mechanisms across similar regions or facilities within your portfolio to accelerate decarbonization.

- **Engage stakeholders and build capacity:**  
  Collaborate with local governments, industry leaders, and community organizations to build awareness, share best practices, and strengthen institutional capacity for sustained emissions management.

- **Continuous monitoring and adaptation:**  
  Implement ongoing tracking of emissions and policy changes, using dashboard insights to adjust strategies in real time and maintain momentum toward targets.

**These targeted fixes empower decision-makers to move from risk identification to effective action—maximizing climate impact and minimizing financial and reputational risks.**

## Example Use Cases

### Regulatory Risk Monitoring
Use the Green Scorecard dashboard to continuously monitor emissions and compliance risks across all operational sites, countries, and regions in your portfolio. The ML-driven risk scores identify entities most likely to exceed emissions targets before actual breaches occur. This early warning system enables compliance officers and sustainability teams to:
- Prioritize audits and inspections based on predicted risk levels.
- Proactively engage with high-risk sites to implement corrective actions.
- Reduce potential regulatory fines and reputational damage by addressing issues early.
- Track effectiveness of interventions over time with updated risk forecasts.

### Targeted Policy Intervention
Leverage detailed insights from emissions trends, policy pressure scores, and risk categorizations to design and deploy focused interventions. For example:
- Allocate technical assistance and training programs to sites struggling under medium policy pressure but showing rising emissions.
- Use financial incentives or subsidies strategically in regions where policy enforcement is weaker to accelerate emissions reductions.
- Collaborate with local regulators and community stakeholders to strengthen enforcement mechanisms where non-compliance risk is highest.
- Tailor interventions to specific sectors or site characteristics identified through the dashboard’s feature importance analysis.

### Strategic Investment Planning
Inform capital allocation decisions by combining emissions performance data with policy environment and risk forecasts. This helps investors, sustainability officers, and corporate strategists to:
- Identify underperforming regions with high policy stringency but delayed emissions improvements, signaling high-impact investment opportunities.
- Recognize success stories where investments and policies have successfully decoupled emissions from economic growth, serving as models for replication.
- Optimize the balance between risk and return by focusing resources on projects and geographies with the greatest potential emissions reduction per dollar invested.
- Support ESG-driven investment theses with credible, data-backed insights that satisfy investor due diligence.

### Transparent ESG Reporting
Enhance corporate and governmental ESG disclosures by integrating comprehensive, data-rich visualizations and forecasts from the Green Scorecard dashboard. Benefits include:
- Providing investors and stakeholders with clear evidence of emissions trends, compliance status, and future risks.
- Strengthening trust and credibility through transparent, objective reporting backed by robust data and predictive analytics.
- Facilitating alignment with global ESG reporting frameworks (e.g., TCFD, SASB, GRI) by supplying granular, auditable data.
- Enabling customized reports and dashboards for different stakeholder groups—from executive boards to public regulators.

### Benchmarking & Best Practice Replication
Utilize the dashboard’s analytical capabilities to benchmark performance across sites, countries, or business units and uncover the key drivers of success. This enables organizations to:
- Identify top-performing sites and regions with consistently low emissions and strong compliance.
- Analyze feature importance to understand which policies, operational practices, or economic factors most influence positive outcomes.
- Develop tailored playbooks and policy recommendations based on proven strategies.
- Scale best practices rapidly across similar operational contexts to maximize emissions reductions and compliance rates.
- Drive continuous improvement through data-driven feedback loops and iterative policy refinement.

These use cases demonstrate how the Green Scorecard is not just a reporting tool, but a strategic platform that empowers proactive, targeted, and impactful climate action across organizations and governments.

## Next Steps & Recommendations

- **Quick Win: Immediate Engagement with High-Risk Regions**  
  Prioritize direct outreach and support to countries, regions, and sites flagged as “At Risk” or “Non-compliant” by the dashboard’s ML model. This involves coordinating with local regulators, sustainability managers, and community stakeholders to:  
  - Review current policies and enforcement mechanisms.  
  - Identify short-term actionable measures to curb emissions growth (e.g., operational changes, technology upgrades).  
  - Set clear milestones and reporting timelines to track progress.  
  Quick, focused interventions here can prevent escalating risks and costly penalties, while building momentum for longer-term change.

- **Policy Gap Analysis and Targeted Reform**  
  Conduct a comprehensive gap analysis in regions where strong policy frameworks exist but emissions reductions lag. This includes:  
  - Evaluating policy design, enforcement consistency, and compliance barriers.  
  - Identifying economic or social factors undermining policy effectiveness.  
  - Recommending reforms such as tightening regulations, improving monitoring infrastructure, or incentivizing green investments.  
  - Collaborating with policymakers to prioritize reforms that deliver measurable emissions impact within realistic timelines.

- **Dashboard Expansion and User Training**  
  Scale the Green Scorecard deployment across additional departments, regions, and stakeholder groups to maximize its impact. Key steps:  
  - Customize dashboard views and filters to suit different user needs (executives, site managers, regulators).  
  - Develop training programs and documentation to ensure users understand data interpretations and can make confident decisions.  
  - Establish feedback channels to continuously improve usability and relevance based on user input.  
  Broad adoption amplifies data-driven decision-making and fosters a culture of proactive sustainability management.

- **Integration of Real-Time Data and Continuous Model Retraining**  
  Upgrade data pipelines to ingest live emissions, economic, and policy data feeds, enabling near real-time monitoring. Additionally:  
  - Implement automated retraining of ML models as new data arrives to maintain forecasting accuracy.  
  - Build alerting systems that notify stakeholders immediately of emerging risks or anomalies.  
  - Enhance scenario responsiveness, allowing dynamic updates in strategy based on the latest intelligence.  
  This real-time capability shifts organizations from reactive to anticipatory climate risk management.

- **Scenario Planning and “What-If” Simulations**  
  Leverage the dashboard’s modeling framework to run simulations testing the impact of potential policy changes, economic shifts, or technological adoption. This supports:  
  - Stress-testing current decarbonization strategies under different assumptions.  
  - Quantifying emissions reductions achievable with proposed interventions or investments.  
  - Comparing alternative pathways to prioritize actions with the greatest climate benefit.  
  - Communicating risks and opportunities effectively to stakeholders and decision-makers.  
  Scenario planning fosters agile, evidence-based strategy development in an uncertain and fast-evolving climate landscape.

**Implementing these next steps ensures that the Green Scorecard is not just a reporting tool but a catalyst for measurable climate progress—driving informed action, continuous learning, and sustainable transformation at scale.**

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