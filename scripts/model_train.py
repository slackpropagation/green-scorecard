

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# Load data
df = pd.read_csv("data/co2_policy_merged.csv")

# Filter rows with required features
df = df.dropna(subset=["co2_growth_prct", "eps_score", "co2_per_capita", "co2_per_unit_energy", "co2"])

# Define binary target: 1 if emissions are increasing, else 0
df["co2_risk_flag"] = (df["co2_growth_prct"] > 0).astype(int)

# Define features and target
X = df[["eps_score", "co2_per_capita", "co2_per_unit_energy", "co2"]]
y = df["co2_risk_flag"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "data/co2_risk_model.pkl")
print("✅ Model saved to data/co2_risk_model.pkl")