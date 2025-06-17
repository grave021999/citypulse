import pandas as pd
import sqlite3
import joblib

# Load trained model
model = joblib.load("models/demand_model.pkl")

# Connect to SQLite DB
conn = sqlite3.connect("db/traffic.db")

# Load full rides data
df = pd.read_sql("SELECT * FROM rides", conn)

# Preprocessing
df["pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
df["hour"] = df["pickup_datetime"].dt.hour
df["day"] = df["pickup_datetime"].dt.day_name()
df["date"] = df["pickup_datetime"].dt.date

# Predict demand (use same features as model training)
X = df[["hour", "PULocationID", "trip_distance"]]
df["high_demand_predicted"] = model.predict(X)

# Save result to new table
df.to_sql("rides_predicted", conn, if_exists="replace", index=False)

print("✅ Predictions saved to rides_predicted table in traffic.db")
