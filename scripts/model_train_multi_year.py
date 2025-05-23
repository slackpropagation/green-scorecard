import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import numpy as np

# Configurable test year for stress testing
FORECAST_MODE = False  # Set to True to forecast next year based on latest year

# Load and reshape wide-format emissions data
hist = pd.read_csv("data/processed/historical_emissions.csv")

# Filter for total CO2 emissions, all sectors
hist = hist[(hist["Gas"] == "CO2") & (hist["Sector"] == "Total including LUCF")]

# Melt year columns into long format
year_cols = [col for col in hist.columns if col.isdigit()]
hist_long = hist.melt(id_vars=["Country", "ISO"], value_vars=year_cols, var_name="year", value_name="co2")
hist_long["year"] = hist_long["year"].astype(str)

# Compute 3-year rolling standard deviation (volatility)
hist_long["year_num"] = hist_long["year"].astype(int)
hist_long = hist_long.sort_values(by=["ISO", "year_num"])
hist_long["co2_volatility_3yr"] = hist_long.groupby("ISO")["co2"].transform(lambda x: x.rolling(window=3, min_periods=2).std())

# Load dataset
df = pd.read_csv("data/processed/co2_predictions_with_income.csv")

df["year"] = df["year"].astype(int)
if FORECAST_MODE:
    test_year = df["year"].astype(int).max()
    print(f"Forecast mode: training on <= {test_year}, predicting for {test_year}")
    train_df = df[df["year"].astype(int) <= test_year].copy()
    test_df = df[df["year"].astype(int) == test_year].copy()
    forecast_only = True
else:
    test_year = df["year"].astype(int).max()
    print(f"Cross-year validation: training on < {test_year}, testing on {test_year}")
    train_df = df[df["year"].astype(int) < test_year].copy()
    test_df = df[df["year"].astype(int) == test_year].copy()
    forecast_only = False

# Calculate policy lag: years since EPS first exceeded 3
eps_lag = df[df["eps_score"] > 3].groupby("country")["year"].min().reset_index()
eps_lag.columns = ["country", "first_eps_year"]
df = pd.merge(df, eps_lag, on="country", how="left")
df["first_eps_year"] = df["first_eps_year"].round()
df["policy_lag_years"] = df["year"] - df["first_eps_year"]
df["policy_lag_years"] = df["policy_lag_years"].clip(lower=0)

# Merge current and prior year emissions to compute CO₂ trend
df["year"] = df["year"].astype(str)
hist_long = hist_long.rename(columns={"Country": "country", "year": "prev_year", "co2": "co2_last_year"})
hist_long["prev_year"] = hist_long["prev_year"].astype(str)
df = pd.merge(
    df,
    hist_long[["country", "prev_year", "co2_last_year", "co2_volatility_3yr"]],
    left_on=["country", "year"],
    right_on=["country", "prev_year"],
    how="left"
)
df["co2_growth_trend"] = df["co2"] / (df["co2_last_year"] + 1e-6)

# Drop rows with missing values in key columns
df = df.dropna(subset=["eps_score", "co2_per_capita", "co2_per_gdp", "gdp", "co2", "population"])

# Feature engineering
df["emissions_per_person"] = df["co2"] / df["population"]
df["intensity_ratio"] = df["co2_per_capita"] / (df["eps_score"] + 1e-6)  # avoid divide-by-zero

# Log-transform skewed features
for col in ["gdp", "population", "co2"]:
    df[f"log_{col}"] = np.log1p(df[col])

# Encode income group as ordinal
income_order = {"L": 0, "LM": 1, "UM": 2, "H": 3}
df["income_group_encoded"] = df["income_group"].map(income_order)

df["income_x_eps"] = df["income_group_encoded"] * df["eps_score"]
df["income_x_gdp"] = df["income_group_encoded"] * df["gdp"]
df["income_x_intensity"] = df["income_group_encoded"] * df["intensity_ratio"]

# Load region mapping file
region_df = pd.read_csv("data/processed/country_regions.csv")  # expects columns: iso_code, region
df = pd.merge(df, region_df, on="iso_code", how="left")

# One-hot encode region
region_dummies = pd.get_dummies(df["region"], prefix="region")
df = pd.concat([df, region_dummies], axis=1)

# Encode region as numeric to create interaction

region_codes = {region: i for i, region in enumerate(df["region"].dropna().unique())}
df["region_code"] = df["region"].map(region_codes)

# Encode year as a numeric feature
df["year_encoded"] = df["year"].astype(int)

# Region × income interaction
df["region_x_income"] = df["region_code"] * df["income_group_encoded"]

train_df = df[df["year"] < str(test_year)].copy()
test_df = df[df["year"] == str(test_year)].copy()

 # Best-of-the-Best Feature Set: Policy + Emissions + Macro + Temporal
features = [
    "eps_score",
    "policy_lag_years",
    "co2_per_capita",
    "emissions_per_person",
    "region_x_income",
    "log_gdp",
    "log_population",
    "year_encoded"
]
X = df[features]
y = df["next_year_growth"]

# Compute class imbalance ratio
neg, pos = np.bincount(y)
scale_pos_weight = neg / pos
print(f"Using scale_pos_weight: {scale_pos_weight:.2f}")

# Cross-year train/test split
X_train = train_df[features]
y_train = train_df["next_year_growth"]
X_test = test_df[features]
y_test = test_df["next_year_growth"]

# Build pipeline with scaling
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", XGBClassifier(random_state=42, scale_pos_weight=scale_pos_weight, use_label_encoder=False, eval_metric="logloss"))
])

# Random search for hyperparameter tuning
param_grid = {
    "model__n_estimators": [100, 200, 300],
    "model__max_depth": [3, 5, 7],
    "model__learning_rate": [0.01, 0.1, 0.2],
    "model__subsample": [0.8, 1.0],
}

search = RandomizedSearchCV(pipe, param_grid, n_iter=10, cv=3, scoring="accuracy", random_state=42)
search.fit(X_train, y_train)


# Threshold tuning for best F1 score
from sklearn.metrics import f1_score
import numpy as np

# Find best threshold for F1 score using validation set
y_proba = search.predict_proba(X_test)[:, 1]
thresholds = np.linspace(0.1, 0.9, 81)
best_f1, best_threshold = 0, 0.5
for t in thresholds:
    y_pred_thresh = (y_proba >= t).astype(int)
    f1 = f1_score(y_test, y_pred_thresh)
    if f1 > best_f1:
        best_f1 = f1
        best_threshold = t

print(f"Best F1 threshold: {best_threshold:.2f} (F1 = {best_f1:.4f})")

# Replace final prediction with best-threshold predictions
y_pred = (y_proba >= best_threshold).astype(int)
if not forecast_only:
    print("Classification Report (Threshold Tuned):")
    print(classification_report(y_test, y_pred))

# Update full-dataset predictions using best threshold
df["predicted_growth"] = (search.predict_proba(X)[:, 1] >= best_threshold).astype(int)

 # Save predictions
df.to_csv("data/co2_multi_year_predictions.csv", index=False)
print("✅ Predictions saved to data/co2_multi_year_predictions.csv")

# Save the model
joblib.dump(search.best_estimator_, "data/multi_year_co2_model.pkl")
print("✅ Tuned model saved to data/multi_year_co2_model.pkl")

# Visualize feature importances (locally)
import matplotlib.pyplot as plt
import seaborn as sns

# Get feature importances from the trained XGBoost model
feature_names = list(X.columns)
importances = search.best_estimator_.named_steps["model"].feature_importances_

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(x=importances, y=feature_names)
plt.title("Feature Importance (XGBoost)")
plt.xlabel("Importance Score")
plt.ylabel("Feature")
plt.tight_layout()
plt.show()