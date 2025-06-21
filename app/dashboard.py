import streamlit as st
import pandas as pd
import sqlite3
import numpy as np

st.set_page_config(page_title="CityPulse – Smart Ride Demand AI", layout="wide")
st.title("🚖 CityPulse – Smart Urban Ride Demand Forecasting")
st.markdown("Predict high-demand NYC taxi rides using precomputed AI predictions. Explore demand across day, hour, and distance filters.")

# --- Load precomputed predictions from database ---
@st.cache_data
def load_data():
    conn = sqlite3.connect("data/traffic.db")
    df = pd.read_sql("SELECT * FROM rides_predicted", conn)
    df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])
    df = df[df["trip_distance"] >= 0.1]  # Remove zero-mile trips
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Rides")

# Day of Week
days = sorted(df["day"].unique().tolist())
selected_days = st.sidebar.multiselect("📅 Day of Week", options=days, default=days)

# Hour of Day
hour_range = st.sidebar.slider("🕒 Pickup Hour", 0, 23, (0, 23))

# Trip Distance
min_miles = 0.1
max_miles = float(df["trip_distance"].max())
trip_min, trip_max = st.sidebar.slider("🚕 Trip Distance (mi)", min_miles, max_miles, (0.1, 10.0))

# --- Apply Filters ---
filtered = df[
    df["day"].isin(selected_days) &
    df["hour"].between(hour_range[0], hour_range[1]) &
    df["trip_distance"].between(trip_min, trip_max)
]

# --- KPI Metrics ---
st.markdown("### 📈 Key Performance Metrics (Filtered Data)")
col1, col2, col3 = st.columns(3)
col1.metric("Total Rides", len(filtered))
col2.metric("High-Demand Rides", int(filtered["high_demand_predicted"].sum()))
col3.metric("High-Demand Rate", f"{filtered['high_demand_predicted'].mean() * 100:.2f}%" if len(filtered) > 0 else "0%")

# --- Ride Table ---
st.markdown("### 📋 Sample Ride Predictions")
st.dataframe(filtered[[
    "pickup_datetime", "trip_distance", "fare_amount", "high_demand_predicted"
]].head(100))

# --- Hourly Demand Trend ---
st.markdown("### 📊 Hourly High-Demand Rate")
hour_summary = filtered.groupby("hour")["high_demand_predicted"].mean()
if not hour_summary.empty:
    st.line_chart(hour_summary)
else:
    st.warning("No data to display for selected hour range.")

# --- Heatmap Table ---
st.markdown("### 📆 Day vs Hour Demand Heatmap")
heatmap_data = filtered.groupby(["day", "hour"])["high_demand_predicted"].mean().unstack().fillna(0)
if not heatmap_data.empty:
    st.dataframe(heatmap_data.style.format("{:.2%}"))
else:
    st.warning("No data for heatmap with current filters.")

# --- Simulated Map for High-Demand Trips ---
st.markdown("### 🗺️ High-Demand Ride Map (Simulated Coordinates)")
np.random.seed(42)
filtered["lat"] = 40.75 + np.random.randn(len(filtered)) * 0.01
filtered["lon"] = -73.99 + np.random.randn(len(filtered)) * 0.01
map_data = filtered[filtered["high_demand_predicted"] == 1][["lat", "lon"]]

if not map_data.empty:
    st.map(map_data)
else:
    st.warning("No high-demand rides to show on map.")
