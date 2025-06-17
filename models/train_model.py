import pandas as pd
import time
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

start = time.time()

print("📦 Loading data...")
df = pd.read_csv("data/processed/rides_for_ml.csv")
print(f"✅ Loaded {len(df)} rows")

# Create binary label
df["high_demand"] = (df["fare_amount"] > 20).astype(int)

# Features and label
X = df[["hour", "PULocationID", "trip_distance"]]
y = df["high_demand"]

print("🔧 Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("🧠 Training model (RandomForest)...")
model = RandomForestClassifier(n_estimators=20, max_depth=15, random_state=42)
model.fit(X_train, y_train)

print("📊 Evaluating model...")
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/demand_model.pkl")
print(f"✅ Model saved as models/demand_model.pkl in {time.time() - start:.2f} seconds")
