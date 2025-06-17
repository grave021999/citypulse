# notebooks/test_load.py

import pandas as pd

# Load the full CSV without sampling
df = pd.read_csv("data/processed/rides_for_ml.csv")

print(f"✅ Loaded {len(df)} rows")
print(df.head())
