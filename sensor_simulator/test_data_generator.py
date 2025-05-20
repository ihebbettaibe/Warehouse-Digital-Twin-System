#!/usr/bin/env python3
"""
Test Data Generator for Warehouse Digital Twin
This script generates a series of test data points including normal readings and anomalies
to verify the functionality of the entire system.
"""

import json
import time
import random
import datetime
import os

# Function to generate normal readings for each sensor type
def generate_normal_reading(sensor_id, sensor_type, location):
    now = datetime.datetime.now().isoformat()
    reading = {
        "sensor_id": sensor_id,
        "timestamp": now,
        "location": location,
        "type": sensor_type
    }
    
    # Generate appropriate values based on sensor type
    if sensor_type == "temperature":
        reading["value"] = round(random.uniform(18.0, 24.0), 1)  # Normal temperature range
        reading["unit"] = "C"
    elif sensor_type == "humidity":
        reading["value"] = round(random.uniform(40.0, 60.0), 1)  # Normal humidity range
        reading["unit"] = "%"
    elif sensor_type == "motion":
        reading["value"] = random.choice([0, 0, 0, 1])  # Mostly no motion
        reading["unit"] = "binary"
    elif sensor_type == "pressure":
        reading["value"] = round(random.uniform(1010.0, 1020.0), 1)  # Normal atmospheric pressure
        reading["unit"] = "hPa"
    elif sensor_type == "door":
        reading["value"] = random.choice([0, 0, 0, 1])  # Mostly closed doors
        reading["unit"] = "binary"
    elif sensor_type == "weight":
        reading["value"] = round(random.uniform(100.0, 500.0), 1)  # Normal weight range
        reading["unit"] = "kg"
    elif sensor_type == "battery":
        reading["value"] = round(random.uniform(80.0, 100.0), 1)  # Normal battery level
        reading["unit"] = "%"
    
    return reading

# Function to generate anomaly readings
def generate_anomaly_reading(sensor_id, sensor_type, location):
    reading = generate_normal_reading(sensor_id, sensor_type, location)
    
    # Override with anomalous values
    if sensor_type == "temperature":
        reading["value"] = round(random.uniform(30.0, 35.0), 1)  # High temperature
    elif sensor_type == "humidity":
        reading["value"] = round(random.uniform(80.0, 95.0), 1)  # High humidity
    elif sensor_type == "pressure":
        reading["value"] = round(random.uniform(980.0, 990.0), 1)  # Low pressure
    elif sensor_type == "weight":
        reading["value"] = round(random.uniform(800.0, 1000.0), 1)  # Excessive weight
    elif sensor_type == "battery":
        reading["value"] = round(random.uniform(10.0, 20.0), 1)  # Low battery
        
    return reading

# Define sensor types and locations
sensor_types = ["temperature", "humidity", "motion", "pressure", "door", "weight", "battery"]
locations = ["zone-a", "zone-b", "zone-c", "loading-dock", "cold-storage"]

# Create sensor IDs
sensors = []
for i in range(1, 21):  # 20 sensors
    sensor_type = random.choice(sensor_types)
    location = random.choice(locations)
    sensors.append({
        "id": f"sensor-{i:03d}",
        "type": sensor_type,
        "location": location
    })

# Generate a mix of normal and anomalous readings
print("Generating test data...")
test_data = []

# 50 normal readings
for _ in range(50):
    sensor = random.choice(sensors)
    reading = generate_normal_reading(sensor["id"], sensor["type"], sensor["location"])
    test_data.append(reading)
    print(json.dumps(reading))
    time.sleep(0.1)

# 10 anomalous readings
print("\nGenerating anomalous readings...")
for _ in range(10):
    sensor = random.choice(sensors)
    anomaly = generate_anomaly_reading(sensor["id"], sensor["type"], sensor["location"])
    test_data.append(anomaly)
    print(json.dumps(anomaly))
    time.sleep(0.1)

# Save test data to a file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
data_dir = "/app/test_data"

# Create directory if it doesn't exist
os.makedirs(data_dir, exist_ok=True)

# Write the test data to a file
filename = f"{data_dir}/test_data_{timestamp}.json"
with open(filename, 'w') as f:
    json.dump(test_data, f, indent=2)

print(f"\nTest data generation complete. Generated {len(test_data)} readings.")
print(f"Data saved to {filename}")
print("\nTest data has been generated and sent to the system.")
print("Check the dashboard to see if the data is being displayed correctly.")
