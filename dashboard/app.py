import json
import threading
from kafka import KafkaConsumer
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app and SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'warehouse-digital-twin'
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory storage for latest sensor readings and alerts
latest_readings = {}
anomaly_alerts = []
# Maximum number of alerts to keep
MAX_ALERTS = 100

# Kafka configuration
kafka_broker = os.environ.get('KAFKA_BROKER', 'localhost:9092')
processed_topic = 'warehouse-processed'
alerts_topic = 'warehouse-alerts'
ml_alerts_topic = 'warehouse-ml-anomalies'

# Process received sensor reading
def process_sensor_data(data):
    sensor_id = data.get('sensor_id')
    if sensor_id:
        latest_readings[sensor_id] = data
        socketio.emit('new_reading', data)

# Process received alert
def process_alert(data, source='rule'):
    timestamp = datetime.now().isoformat()
    
    # Determine alert type and message
    if source == 'ml':
        alert_type = "ML"
        message = f"ML Anomaly detected in {data.get('sensor_type')} sensor in {data.get('zone')} zone"
        # Include ML-specific details if available
        if 'deviation_percent' in data:
            message += f" (Deviation: {data.get('deviation_percent'):.1f}%)"
    else:
        alert_type = "Rule"
        message = f"Anomaly detected in {data.get('sensor_type')} sensor in {data.get('zone')} zone"
    
    alert = {
        'timestamp': timestamp,
        'sensor_id': data.get('sensor_id'),
        'sensor_type': data.get('sensor_type'),
        'value': data.get('value'),
        'zone': data.get('zone'),
        'alert_type': alert_type,
        'message': message
    }
    
    # Add to alerts list and limit size
    anomaly_alerts.append(alert)
    if len(anomaly_alerts) > MAX_ALERTS:
        anomaly_alerts.pop(0)
    
    socketio.emit('new_alert', alert)

# Kafka consumer for processed sensor data
def consume_processed_data():
    logger.info(f"Starting Kafka consumer for {processed_topic} at {kafka_broker}")
    try:
        consumer = KafkaConsumer(
            processed_topic,
            bootstrap_servers=kafka_broker,
            auto_offset_reset='latest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        for message in consumer:
            try:
                data = message.value
                process_sensor_data(data)
            except Exception as e:
                logger.error(f"Error processing sensor data: {e}")
    
    except Exception as e:
        logger.error(f"Failed to start Kafka consumer for processed data: {e}")

# Kafka consumer for rule-based anomaly alerts
def consume_alerts():
    logger.info(f"Starting Kafka consumer for {alerts_topic} at {kafka_broker}")
    try:
        consumer = KafkaConsumer(
            alerts_topic,
            bootstrap_servers=kafka_broker,
            auto_offset_reset='latest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        for message in consumer:
            try:
                data = message.value
                process_alert(data, source='rule')
            except Exception as e:
                logger.error(f"Error processing rule-based alert: {e}")
    
    except Exception as e:
        logger.error(f"Failed to start Kafka consumer for rule-based alerts: {e}")
        
# Kafka consumer for ML-based anomaly alerts
def consume_ml_alerts():
    logger.info(f"Starting Kafka consumer for {ml_alerts_topic} at {kafka_broker}")
    try:
        consumer = KafkaConsumer(
            ml_alerts_topic,
            bootstrap_servers=kafka_broker,
            auto_offset_reset='latest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        for message in consumer:
            try:
                data = message.value
                process_alert(data, source='ml')
            except Exception as e:
                logger.error(f"Error processing ML alert: {e}")
    
    except Exception as e:
        logger.error(f"Failed to start Kafka consumer for ML alerts: {e}")

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/readings')
def get_readings():
    return jsonify(list(latest_readings.values()))

@app.route('/api/alerts')
def get_alerts():
    return jsonify(anomaly_alerts)

@app.route('/api/zones')
def get_zones():
    # Extract unique zones from readings
    zones = set()
    for reading in latest_readings.values():
        if 'zone' in reading:
            zones.add(reading['zone'])
    return jsonify(list(zones))

@app.route('/api/sensor-types')
def get_sensor_types():
    # Extract unique sensor types from readings
    sensor_types = set()
    for reading in latest_readings.values():
        if 'sensor_type' in reading:
            sensor_types.add(reading['sensor_type'])
    return jsonify(list(sensor_types))

# Socket.IO events
@socketio.on('connect')
def handle_connect():
    # Send initial data to newly connected client
    socketio.emit('initial_readings', list(latest_readings.values()))
    socketio.emit('initial_alerts', anomaly_alerts)

if __name__ == '__main__':
    # Start Kafka consumers in background threads
    threading.Thread(target=consume_processed_data, daemon=True).start()
    threading.Thread(target=consume_alerts, daemon=True).start()
    threading.Thread(target=consume_ml_alerts, daemon=True).start()
    
    # Run the Flask app
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    logger.info(f"Starting dashboard application on {host}:{port}")
    socketio.run(app, host=host, port=port, debug=False, allow_unsafe_werkzeug=True)
