import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

with open("anomaly_log.json") as f:
    data = json.load(f)

if not data:
    print("⚠️ No data in anomaly_log.json")
    exit()

df = pd.DataFrame(data)

# Patch: Handle aircraft_1 and aircraft_2 instead of 'aircraft'
aircrafts = []
if "aircraft_1" in df.columns:
    aircrafts.extend(df["aircraft_1"].dropna().tolist())
if "aircraft_2" in df.columns:
    aircrafts.extend(df["aircraft_2"].dropna().tolist())

if aircrafts:
    pd.Series(aircrafts).value_counts().plot(kind="bar", color="skyblue")
    plt.title("Anomalies per Aircraft")
    plt.xlabel("Aircraft Callsign")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("AircraftAnomalyCountsOverTime.png")
    plt.close()
    print("✅ Saved AircraftAnomalyCountsOverTime.png")
else:
    print("⚠️ No aircraft data found in anomaly log.")

if "position" in df.columns:
    df["longitude"] = df["position"].apply(lambda x: x[0])
    df["latitude"] = df["position"].apply(lambda x: x[1])
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x="longitude", y="latitude", hue="type")
    plt.title("Anomaly Geospatial Distribution")
    plt.savefig("anomaly_geospatial_map.png")
    plt.close()
    print("✅ Saved anomaly_geospatial_map.png")

if "time" in df.columns:
    df["time"] = pd.to_datetime(df["time"])
    timeline = df.set_index("time").resample("1T").size()
    timeline.plot(marker="o")
    plt.title("Anomaly Timeline")
    plt.xlabel("Time")
    plt.ylabel("Anomaly Count per Minute")
    plt.tight_layout()
    plt.savefig("anomaly_timeline.png")
    plt.close()
    print("✅ Saved anomaly_timeline.png")

if "position" in df.columns and "aircraft_1" in df.columns:
    plt.figure(figsize=(8, 6))
    for ac in set(df["aircraft_1"]):
        subset = df[df["aircraft_1"] == ac]
        if "position" in subset.columns:
            coords = subset["position"].tolist()
            x = [p[0] for p in coords]
            y = [p[1] for p in coords]
            plt.plot(x, y, label=ac)
    plt.title("Aircraft Route Traces for Anomalies")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("route_trace_plot.png")
    plt.close()
    print("✅ Saved route_trace_plot.png")

if "status" in df.columns:
    df["status"].value_counts().plot.pie(autopct="%1.1f%%")
    plt.title("Aircraft Status Breakdown")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("status_pie_chart.png")
    plt.close()
    print("✅ Saved status_pie_chart.png")

# import json
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from datetime import datetime

# # Load anomaly log
# with open("anomaly_log.json", "r") as f:
#     data = json.load(f)

# # Convert to DataFrame
# df = pd.DataFrame(data)
# df["time"] = pd.to_datetime(df["time"])
# df["longitude"] = df["position"].apply(lambda x: x[0])
# df["latitude"] = df["position"].apply(lambda x: x[1])

# # --- Bar Chart: Anomalies per Aircraft ---
# plt.figure(figsize=(10, 5))
# df["aircraft"].value_counts().plot(kind="bar", color="skyblue")
# plt.title("Anomalies per Aircraft")
# plt.xlabel("Aircraft ID")
# plt.ylabel("Number of Anomalies")
# plt.tight_layout()
# plt.savefig("anomalies_per_aircraft.png")
# plt.close()

# # --- Geospatial Map (Scatter Plot) ---
# plt.figure(figsize=(10, 6))
# sns.scatterplot(data=df, x="longitude", y="latitude", hue="aircraft", palette="tab10", s=60)
# plt.title("Geospatial Distribution of Anomalies")
# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.tight_layout()
# plt.savefig("anomaly_geospatial_map.png")
# plt.close()

# # --- Timeline Plot (Time Series) ---
# plt.figure(figsize=(12, 6))
# df.set_index("time").resample("1T").size().plot(kind="line", marker="o")
# plt.title("Anomaly Timeline (Per Minute)")
# plt.xlabel("Time")
# plt.ylabel("Number of Anomalies")
# plt.tight_layout()
# plt.savefig("anomaly_timeline.png")
# plt.close()

# # --- Route Trace (Line Plot) for Each Aircraft ---
# plt.figure(figsize=(10, 6))
# for aircraft, group in df.groupby("aircraft"):
#     group_sorted = group.sort_values("time")
#     plt.plot(group_sorted["longitude"], group_sorted["latitude"], label=aircraft)
# plt.title("Route Trace of Aircraft During Anomalies")
# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
# plt.legend()
# plt.tight_layout()
# plt.savefig("route_trace_plot.png")
# plt.close()

# # --- Pie Chart: Status Distribution ---
# if "status" in df.columns:
#     status_counts = df["status"].value_counts()
#     plt.figure(figsize=(6, 6))
#     plt.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%", startangle=140)
#     plt.title("Final Status Distribution")
#     plt.tight_layout()
#     plt.savefig("status_pie_chart.png")
#     plt.close()
