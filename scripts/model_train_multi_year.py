

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Load multi-year dataset
df = pd.read_csv("data/co2_multi_year_training.csv")

# Drop any remaining rows with missing values in key features
df = df.dropna(subset=["eps_score", "co2_per_capita", "co2_per_gdp", "gdp", "co2", "population"])

# Define features and target
X = df[["eps_score", "co2_per_capita", "co2_per_gdp", "gdp", "co2", "population"]]
y = df["next_year_growth"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred))

df["predicted_growth"] = model.predict(X)

df.to_csv("data/co2_multi_year_predictions.csv", index=False)
print("✅ Predictions saved to data/co2_multi_year_predictions.csv")

# Save model
joblib.dump(model, "data/multi_year_co2_model.pkl")
print("✅ Model saved to data/multi_year_co2_model.pkl")