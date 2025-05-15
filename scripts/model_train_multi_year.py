import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import numpy as np

# Load dataset
df = pd.read_csv("data/co2_multi_year_training.csv")

# Drop rows with missing values in key columns
df = df.dropna(subset=["eps_score", "co2_per_capita", "co2_per_gdp", "gdp", "co2", "population"])

# Feature engineering
df["emissions_per_person"] = df["co2"] / df["population"]
df["intensity_ratio"] = df["co2_per_capita"] / (df["eps_score"] + 1e-6)  # avoid divide-by-zero

# Define features and target
features = ["eps_score", "co2_per_capita", "co2_per_gdp", "gdp", "co2", "population", "emissions_per_person", "intensity_ratio"]
X = df[features]
y = df["next_year_growth"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build pipeline with scaling
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestClassifier(random_state=42, class_weight="balanced"))
])

# Random search for hyperparameter tuning
param_grid = {
    "model__n_estimators": [100, 200, 300],
    "model__max_depth": [None, 5, 10],
    "model__min_samples_split": [2, 5, 10],
    "model__min_samples_leaf": [1, 2, 4]
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