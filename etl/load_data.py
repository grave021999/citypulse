import pandas as pd
import sqlite3
import os

# === Extract ===
file_path = "data/raw/yellow_tripdata_2023-01.parquet"
df = pd.read_parquet(file_path)

# === Transform ===
# Select only useful columns
df = df[[
    "tpep_pickup_datetime", 
    "tpep_dropoff_datetime", 
    "trip_distance", 
    "PULocationID", 
    "DOLocationID", 
    "fare_amount"
]]

# Optional: Drop rows with nulls or negative values
df = df.dropna()
df = df[df['trip_distance'] > 0]
df = df[df['fare_amount'] >= 0]

# === Load ===
os.makedirs("db", exist_ok=True)
conn = sqlite3.connect("db/traffic.db")
df.to_sql("rides", conn, if_exists="replace", index=False)

print(f"✅ Loaded {len(df)} rows into SQLite (db/traffic.db)")
