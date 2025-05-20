import json
import time
import random
import datetime
import os
from kafka import KafkaProducer

# Sensor types and their ranges
SENSOR_TYPES = {
    'temperature': {'min': 15, 'max': 35, 'unit': 'C', 'precision': 1},
    'humidity': {'min': 20, 'max': 80, 'unit': '%', 'precision': 0},
    'motion': {'min': 0, 'max': 1, 'unit': 'binary', 'precision': 0},
    'pressure': {'min': 990, 'max': 1030, 'unit': 'hPa', 'precision': 0},
    'door_status': {'min': 0, 'max': 1, 'unit': 'binary', 'precision': 0},
    'battery_level': {'min': 0, 'max': 100, 'unit': '%', 'precision': 0},
    'weight': {'min': 0, 'max': 5000, 'unit': 'kg', 'precision': 0}
}

# Warehouse zones
WAREHOUSE_ZONES = [
    'receiving', 'shipping', 'storage_a', 'storage_b', 'storage_c', 
    'cold_storage', 'packaging', 'loading_dock'
]

# Sensor IDs by type
SENSORS = {}
for sensor_type in SENSOR_TYPES:
    SENSORS[sensor_type] = []
    for zone in WAREHOUSE_ZONES:
        # Create 1-3 sensors of each type in each zone
        for i in range(random.randint(1, 3)):
            SENSORS[sensor_type].append(f"{sensor_type}_{zone}_{i+1}")

def generate_sensor_reading(sensor_id):
    """Generate a realistic sensor reading based on sensor type"""
    sensor_type = sensor_id.split('_')[0]
    sensor_config = SENSOR_TYPES[sensor_type]
    
    # Generate value based on sensor type ranges
    if sensor_config['unit'] == 'binary':
        value = random.randint(sensor_config['min'], sensor_config['max'])
    else:
        value = round(random.uniform(sensor_config['min'], sensor_config['max']), 
                     sensor_config['precision'])
    
    # Add occasional anomalies (5% chance)
    if random.random() < 0.05:
        if sensor_config['unit'] == 'binary':
            value = 1 - value  # Toggle binary value
        else:
            # Generate an anomaly outside normal range
            anomaly_factor = random.choice([-0.5, 0.5])  # Either too low or too high
            range_size = sensor_config['max'] - sensor_config['min']
            value = sensor_config['min'] + range_size * (1 + anomaly_factor)
            value = round(value, sensor_config['precision'])
    
    timestamp = datetime.datetime.now().isoformat()
    zone = '_'.join(sensor_id.split('_')[1:-1])  # Extract zone from sensor ID
    
    return {
        'sensor_id': sensor_id,
        'sensor_type': sensor_type,
        'value': value,
        'unit': sensor_config['unit'],
        'timestamp': timestamp,
        'zone': zone,
        'status': 'active'
    }

def send_to_kafka(producer, data):
    """Send data to Kafka topic"""
    try:
        sensor_type = data['sensor_type']
        producer.send(
            f'warehouse-sensors-{sensor_type}', 
            json.dumps(data).encode('utf-8')
        )
        print(f"Sent: {data}")
    except Exception as e:
        print(f"Error sending to Kafka: {e}")

def main():
    print("Warehouse Sensor Simulator starting...")
    
    # Connect to Kafka
    kafka_broker = os.environ.get('KAFKA_BROKER', 'localhost:9092')
    print(f"Connecting to Kafka at {kafka_broker}")
    
    # Try to connect with retries
    retries = 0
    producer = None
    while retries < 10:
        try:
            producer = KafkaProducer(bootstrap_servers=kafka_broker)
            print("Connected to Kafka successfully")
            break
        except Exception as e:
            print(f"Failed to connect to Kafka, retrying... ({e})")
            retries += 1
            time.sleep(5)
    
    if producer is None:
        print("Failed to connect to Kafka after multiple retries. Exiting.")
        return
    
    # Simulate sensor readings indefinitely
    try:
        while True:
            # For each sensor type
            for sensor_type, sensor_ids in SENSORS.items():
                # Generate data for each sensor
                for sensor_id in sensor_ids:
                    data = generate_sensor_reading(sensor_id)
                    send_to_kafka(producer, data)
            
            # Wait before next batch of readings
            time.sleep(2)
    
    except KeyboardInterrupt:
        print("Simulator stopping...")
        producer.close()
        print("Simulator stopped")

if __name__ == "__main__":
    main()
