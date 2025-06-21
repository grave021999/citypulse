import sqlite3
import pandas as pd

conn = sqlite3.connect("db/traffic.db")
df = pd.read_sql("SELECT * FROM rides_predicted LIMIT 10000", conn)
df.to_csv("data/processed/rides_predicted_sample.csv", index=False)
print("✅ Exported sample rides_predicted_sample.csv")
