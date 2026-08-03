# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 15:31:25 2025

@author: sandr
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 13:27:49 2025

@author: sandr
"""
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import radians, sin, cos, sqrt, atan2
import random

# Load real flight data from LGB to PHX
real_flight_file = "./Raw_Data/LGB-PHX.xlsx"
real_flight_df = pd.read_excel(real_flight_file)

# Extract relevant columns
real_flight_df = real_flight_df[['Latitude', 'Longitude', 'Altitude']]

# Generate a random hazard
num_hazards = random.randint(1, 3)

def generate_hazard(df):
    """Generate a random hazard within the flight path."""
    random_index = random.randint(10, len(df) - 10)
    return {
        "Latitude": df.iloc[random_index]['Latitude'] + random.uniform(-0.2, 0.2),
        "Longitude": df.iloc[random_index]['Longitude'] + random.uniform(-0.2, 0.2),
        "Altitude": random.randint(24000, 39000),  # FL240-FL390
        "Radius_NM": random.randint(0, 15)
    }

# Generate hazards
raw_hazards = [generate_hazard(real_flight_df) for _ in range(num_hazards)]
# Print hazard information
for i, hazard in enumerate(raw_hazards):
    print(f"\nWX DATA - HAZARD {i + 1}:")
    print(f"Lat: {hazard['Latitude']}")
    print(f"Long: {hazard['Longitude']}")
    print(f"Alt: {hazard['Altitude']} ft")
    print(f"Radius: {hazard['Radius_NM']} NM")

# Merge hazards that are within 50NM of each other
hazards = []
while raw_hazards:
    base_hazard = raw_hazards.pop(0)
    close_hazards = [h for h in raw_hazards if sqrt((h['Latitude'] - base_hazard['Latitude'])**2 + (h['Longitude'] - base_hazard['Longitude'])**2) * 69 <= 50]
    
    for h in close_hazards:
        raw_hazards.remove(h)
        base_hazard['Latitude'] = (base_hazard['Latitude'] + h['Latitude']) / 2
        base_hazard['Longitude'] = (base_hazard['Longitude'] + h['Longitude']) / 2
        base_hazard['Altitude'] = max(base_hazard['Altitude'], h['Altitude'])
        base_hazard['Radius_NM'] = max(base_hazard['Radius_NM'], h['Radius_NM']) + 5
    
    hazards.append(base_hazard)

# Filter out hazards with radius <= 3NM (proceed with planned flight route)
hazards = [h for h in hazards if h['Radius_NM'] > 3]

# Convert nautical miles to degrees
def nm_to_deg(nm):
    return nm / 69

# Function to find optimized rejoin point at the planned destination
def find_rejoin_point():
    return len(real_flight_df) - 1

# Function to generate avoidance path

def generate_avoidance_path(before_detour_index, rejoin_index, hazard):
    num_detour_points = 100
    t_values = np.linspace(0, 1, num_detour_points)
    
    lat_start, lon_start, alt_start = real_flight_df.iloc[before_detour_index]
    lat_end, lon_end, alt_end = real_flight_df.iloc[rejoin_index]
    
    control_lat1 = hazard["Latitude"] + 0.1
    control_lon1 = hazard["Longitude"] + 0.1
    control_alt1 = max(alt_start, hazard["Altitude"] + 3000)
    
    control_lat2 = hazard["Latitude"] + 0.15
    control_lon2 = hazard["Longitude"] + 0.15
    control_alt2 = max(alt_end, hazard["Altitude"] + 2000)
    
    detour_lat = ((1 - t_values) ** 3 * lat_start + 3 * (1 - t_values) ** 2 * t_values * control_lat1 +
                  3 * (1 - t_values) * t_values ** 2 * control_lat2 + t_values ** 3 * lat_end)
    detour_lon = ((1 - t_values) ** 3 * lon_start + 3 * (1 - t_values) ** 2 * t_values * control_lon1 +
                  3 * (1 - t_values) * t_values ** 2 * control_lon2 + t_values ** 3 * lon_end)
    detour_alt = ((1 - t_values) ** 3 * alt_start + 3 * (1 - t_values) ** 2 * t_values * control_alt1 +
                  3 * (1 - t_values) * t_values ** 2 * control_alt2 + t_values ** 3 * alt_end)
    
    # Smooth altitude changes to avoid dramatic ascent or descent
    max_rate_change = 200  # Limit altitude change per waypoint to 200 ft
    for i in range(1, len(detour_alt)):
        if detour_alt[i] > detour_alt[i - 1] + max_rate_change:
            detour_alt[i] = detour_alt[i - 1] + max_rate_change
        elif detour_alt[i] < detour_alt[i - 1] - max_rate_change:
            detour_alt[i] = detour_alt[i - 1] - max_rate_change
    
    return pd.DataFrame({'Latitude': detour_lat, 'Longitude': detour_lon, 'Altitude': detour_alt})

# Adjust flight path with avoidance maneuvers
adjusted_flight_df = real_flight_df.copy()

for hazard in hazards:
    closest_index = real_flight_df.iloc[(real_flight_df[['Latitude', 'Longitude']] - [hazard["Latitude"], hazard["Longitude"]]).pow(2).sum(1).idxmin()].name
    before_detour_index = max(0, closest_index - 5)
    rejoin_index = find_rejoin_point()
    
    detour_path = generate_avoidance_path(before_detour_index, rejoin_index, hazard)
    adjusted_flight_df = pd.concat([
        adjusted_flight_df.iloc[:before_detour_index],
        detour_path,
        adjusted_flight_df.iloc[rejoin_index:]
    ], ignore_index=True)

# Ensure the last 50 waypoints match the planned flight path altitude and descent slope
# ONLY if any hazard has a radius greater than 5NM
if any(hazard['Radius_NM'] > 5 for hazard in hazards):
    if len(adjusted_flight_df) >= 50:
        adjusted_flight_df.iloc[-50:, adjusted_flight_df.columns.get_loc('Altitude')] = real_flight_df.iloc[-50:, real_flight_df.columns.get_loc('Altitude')].values
        adjusted_flight_df['Slope'] = adjusted_flight_df['Altitude'].diff().fillna(0)
        real_flight_df['Slope'] = real_flight_df['Altitude'].diff().fillna(0)
        adjusted_flight_df.iloc[-50:, adjusted_flight_df.columns.get_loc('Slope')] = real_flight_df.iloc[-50:, real_flight_df.columns.get_loc('Slope')].values

# Save adjusted flight path
adjusted_flight_df.to_csv("Optimized_Avoidance_Path.csv", index=False)

'''
Display Distances
'''
def compute_distance(df):
    return sum([sqrt((df.iloc[i+1]['Latitude'] - df.iloc[i]['Latitude'])**2 + (df.iloc[i+1]['Longitude'] - df.iloc[i]['Longitude'])**2) * 69 for i in range(len(df)-1)])

# Compute original and adjusted flight distances
original_distance_nm = compute_distance(real_flight_df)
adjusted_distance_nm = compute_distance(adjusted_flight_df)

# Print distances
print(f"\nOriginal Flight Path Distance: {original_distance_nm:.2f} NM")
print(f"Adjusted Flight Path Distance: {adjusted_distance_nm:.2f} NM")
print(f"Added Distance due to WXA {adjusted_distance_nm - original_distance_nm:.2f} ({(adjusted_distance_nm / original_distance_nm - 1) * 100:.1f}%)")


'''
Plot Alternative Flight Path
'''

# Plot hazard avoidance radius
plt.figure(figsize=(10, 6))
for hazard in hazards:
    plt.scatter(hazard['Longitude'], hazard['Latitude'], color='purple', s=100, marker='x', label='Hazard')
    hazard_circle = plt.Circle((hazard['Longitude'], hazard['Latitude']), nm_to_deg(hazard["Radius_NM"]), color='purple', fill=False, linestyle='dashed')
    plt.gca().add_patch(hazard_circle)
    # avoidance_circle = plt.Circle((hazard['Longitude'], hazard['Latitude']), nm_to_deg(hazard["Avoidance_NM"]), color='blue', fill=False, linestyle='dashed', label='Avoidance Radius')
    # plt.gca().add_patch(avoidance_circle)

plt.plot(real_flight_df['Longitude'], real_flight_df['Latitude'], 'ro-', label='Planned Flight Path', alpha=0.6)
plt.plot(adjusted_flight_df['Longitude'], adjusted_flight_df['Latitude'], 'bo-', label='Avoidance Flight Path', alpha=0.6)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Planned vs. Avoidance Flight Path with Avoidance Radius")
plt.legend()
plt.grid(True)
plt.show()
'''
Plot the difference in Alt from Planned & Avoidance Path
'''
# Extract relevant columns
adjusted_flight_df = pd.read_csv("Optimized_Avoidance_Path.csv")
adjusted_flight_df = adjusted_flight_df[['Latitude', 'Longitude', 'Altitude']]

# Plot altitude profiles
plt.figure(figsize=(12, 6))
plt.plot(range(len(real_flight_df)), real_flight_df['Altitude'], 'r-', label='Planned Flight Path', alpha=0.7)
plt.plot(range(len(adjusted_flight_df)), adjusted_flight_df['Altitude'], 'b-', label='Avoidance Flight Path', alpha=0.7)

# Labels and title
plt.xlabel("Waypoint Index")
plt.ylabel("Altitude (ft)")
plt.title("Altitude Profile: Planned vs Avoidance Flight Path")
plt.legend()
plt.grid(True)

# Show plot
plt.show()
'''
PLOT 3d 
'''
# Plot updated 3D flight path
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

ax.plot(real_flight_df['Longitude'], real_flight_df['Latitude'], real_flight_df['Altitude'], 'r-', label='Planned Flight Path', alpha=0.7)
ax.plot(adjusted_flight_df['Longitude'], adjusted_flight_df['Latitude'], adjusted_flight_df['Altitude'], 'b-', label='Optimized Avoidance Flight Path', alpha=0.7)

for hazard in hazards:
    u = np.linspace(0, 2 * np.pi, 20)
    v = np.linspace(0, np.pi, 10)
    x = nm_to_deg(hazard['Radius_NM']) * np.outer(np.cos(u), np.sin(v)) + hazard['Longitude']
    y = nm_to_deg(hazard['Radius_NM']) * np.outer(np.sin(u), np.sin(v)) + hazard['Latitude']
    z = (hazard['Altitude'] * np.outer(np.ones(np.size(u)), np.cos(v)))
    ax.plot_surface(x, y, z, color='purple', alpha=0.3, edgecolor='k')

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_zlabel("Altitude (ft)")
ax.set_title("Optimized 3D Flight Path with Hazards")
ax.legend()
plt.show()