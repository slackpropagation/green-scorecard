import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import numpy as np

# Load dataset
df = pd.read_csv("data/co2_predictions_with_income.csv")

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
region_df = pd.read_csv("data/country_regions.csv")  # expects columns: iso_code, region
df = pd.merge(df, region_df, on="iso_code", how="left")

# One-hot encode region
region_dummies = pd.get_dummies(df["region"], prefix="region")
df = pd.concat([df, region_dummies], axis=1)

# Encode region as numeric to create interaction
region_codes = {region: i for i, region in enumerate(df["region"].dropna().unique())}
df["region_code"] = df["region"].map(region_codes)

# Region × income interaction
df["region_x_income"] = df["region_code"] * df["income_group_encoded"]

# Define features and target
features = [
    "eps_score", "co2_per_capita", "co2_per_gdp", "log_gdp", "log_co2", "log_population",
    "emissions_per_person", "intensity_ratio", "income_group_encoded",
    "income_x_eps", "income_x_gdp", "income_x_intensity",
    "region_x_income"
] + region_dummies.columns.tolist()
X = df[features]
y = df["next_year_growth"]

# Compute class imbalance ratio
neg, pos = np.bincount(y)
scale_pos_weight = neg / pos
print(f"Using scale_pos_weight: {scale_pos_weight:.2f}")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

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

# Evaluate
y_pred = search.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Add predictions to full dataset
df["predicted_growth"] = search.predict(X)

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