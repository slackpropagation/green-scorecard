

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load data
df = pd.read_csv("data/simulated_sites.csv")

# Sort for consistency
df = df.sort_values(by=["site_id", "quarter"])

# Calculate binary label: 1 if emissions exceed target, else 0
df["target_breach"] = (df["scope_1_emissions"] > df["target_emissions"]).astype(int)

# Create lag features
df["prev_emissions"] = df.groupby("site_id")["scope_1_emissions"].shift(1)
df["prev_output"] = df.groupby("site_id")["output_units"].shift(1)
df["prev_intensity"] = df.groupby("site_id")["emissions_intensity"].shift(1)

# Drop rows with missing lagged data
df_model = df.dropna(subset=["prev_emissions", "prev_output", "prev_intensity", "target_breach"])

# Features and target
X = df_model[["prev_emissions", "prev_output", "prev_intensity"]]
y = df_model["target_breach"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "data/logistic_model.pkl")
print("Model saved to data/logistic_model.pkl")