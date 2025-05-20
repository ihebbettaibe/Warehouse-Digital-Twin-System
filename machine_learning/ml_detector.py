# Machine Learning Anomaly Detection for Warehouse Digital Twin
# This module uses machine learning to detect anomalies in sensor data

import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import os
import json
from datetime import datetime, timedelta
from kafka import KafkaConsumer, KafkaProducer
import logging
import time
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MLAnomalyDetector:
    def __init__(self, model_dir='models', data_dir='data'):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_dir = os.path.join(self.base_dir, model_dir)
        self.data_dir = os.path.join(self.base_dir, data_dir)
        
        # Create directories if they don't exist
        os.makedirs(self.model_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Model parameters
        self.models = {}
        self.scalers = {}
        self.training_data = {}
        self.min_training_samples = 100
        
        # Kafka configuration
        self.kafka_broker = os.environ.get('KAFKA_BROKER', 'localhost:9092')
        self.input_topic = 'warehouse-processed'
        self.output_topic = 'warehouse-ml-anomalies'
        
        # Reading history
        self.reading_history = {}
        self.max_history_size = 1000

    def initialize_models(self):
        """Initialize or load pre-existing models for each sensor type"""
        sensor_types = ['temperature', 'humidity', 'pressure', 'battery_level', 'weight']
        
        for sensor_type in sensor_types:
            model_path = os.path.join(self.model_dir, f'{sensor_type}_model.pkl')
            scaler_path = os.path.join(self.model_dir, f'{sensor_type}_scaler.pkl')
            
            if os.path.exists(model_path) and os.path.exists(scaler_path):
                logger.info(f"Loading existing model for {sensor_type}")
                try:
                    self.models[sensor_type] = joblib.load(model_path)
                    self.scalers[sensor_type] = joblib.load(scaler_path)
                except Exception as e:
                    logger.error(f"Error loading model for {sensor_type}: {e}")
                    self._create_new_model(sensor_type)
            else:
                logger.info(f"Creating new model for {sensor_type}")
                self._create_new_model(sensor_type)
    
    def _create_new_model(self, sensor_type):
        """Create a new Isolation Forest model for a sensor type"""
        self.models[sensor_type] = IsolationForest(
            n_estimators=100,
            max_samples='auto',
            contamination=0.05,
            random_state=42
        )
        self.scalers[sensor_type] = StandardScaler()
        self.training_data[sensor_type] = []
    
    def train_model(self, sensor_type):
        """Train model for a specific sensor type using collected data"""
        if sensor_type not in self.training_data or len(self.training_data[sensor_type]) < self.min_training_samples:
            logger.warning(f"Not enough data to train model for {sensor_type}. Need at least {self.min_training_samples} samples.")
            return False
        
        try:
            data = np.array(self.training_data[sensor_type]).reshape(-1, 1)
            data_scaled = self.scalers[sensor_type].fit_transform(data)
            
            self.models[sensor_type].fit(data_scaled)
            
            # Save model and scaler
            joblib.dump(self.models[sensor_type], os.path.join(self.model_dir, f'{sensor_type}_model.pkl'))
            joblib.dump(self.scalers[sensor_type], os.path.join(self.model_dir, f'{sensor_type}_scaler.pkl'))
            
            logger.info(f"Successfully trained model for {sensor_type} with {len(data)} samples")
            
            # Save training data for reference
            df = pd.DataFrame({'value': self.training_data[sensor_type]})
            df.to_csv(os.path.join(self.data_dir, f'{sensor_type}_training_data.csv'), index=False)
            
            return True
            
        except Exception as e:
            logger.error(f"Error training model for {sensor_type}: {e}")
            return False
    
    def detect_anomaly(self, sensor_type, value):
        """Detect if a sensor reading is an anomaly using the trained model"""
        if sensor_type not in self.models:
            logger.warning(f"No model available for {sensor_type}")
            return False
        
        # For binary sensors, no need for ML detection
        if sensor_type in ['motion', 'door_status']:
            return False
        
        try:
            # Add to training data if still collecting
            if len(self.training_data.get(sensor_type, [])) < self.min_training_samples:
                self.training_data[sensor_type].append(value)
                return False
            
            # Process single sample
            X = np.array([[value]])
            X_scaled = self.scalers[sensor_type].transform(X)
            
            # Predict returns 1 for inliers and -1 for outliers
            prediction = self.models[sensor_type].predict(X_scaled)[0]
            anomaly_score = self.models[sensor_type].score_samples(X_scaled)[0]
            
            is_anomaly = prediction == -1
            
            # If it's an anomaly, log detailed information
            if is_anomaly:
                logger.info(f"ML detected anomaly in {sensor_type}: value={value}, score={anomaly_score}")
            
            return is_anomaly
            
        except Exception as e:
            logger.error(f"Error detecting anomaly for {sensor_type}: {e}")
            return False
    
    def process_reading(self, reading):
        """Process a sensor reading to store history and detect anomalies"""
        sensor_id = reading.get('sensor_id')
        sensor_type = reading.get('sensor_type')
        value = reading.get('value')
        
        if not sensor_id or not sensor_type or value is None:
            return None
        
        # Keep track of readings history
        if sensor_id not in self.reading_history:
            self.reading_history[sensor_id] = []
        
        # Add to history and limit size
        self.reading_history[sensor_id].append({
            'timestamp': reading.get('timestamp'),
            'value': value
        })
        
        if len(self.reading_history[sensor_id]) > self.max_history_size:
            self.reading_history[sensor_id].pop(0)
        
        # Detect anomaly using ML
        if len(self.reading_history[sensor_id]) >= 10:  # Need some history first
            ml_anomaly = self.detect_anomaly(sensor_type, value)
            
            # If ML detected an anomaly, enhance reading with ML information
            if ml_anomaly:
                enhanced_reading = reading.copy()
                enhanced_reading['ml_anomaly'] = True
                enhanced_reading['detection_method'] = 'machine_learning'
                enhanced_reading['alert_level'] = 'warning'
                
                # Analyze pattern
                values = [item['value'] for item in self.reading_history[sensor_id][-10:]]
                enhanced_reading['recent_avg'] = sum(values) / len(values)
                enhanced_reading['recent_std'] = np.std(values)
                enhanced_reading['deviation_percent'] = abs((value - enhanced_reading['recent_avg']) / enhanced_reading['recent_avg']) * 100 if enhanced_reading['recent_avg'] != 0 else 0
                
                return enhanced_reading
        
        return None

    def start_consumer(self):
        """Start consuming from Kafka input topic"""
        logger.info(f"Starting Kafka consumer for {self.input_topic}")
        try:
            consumer = KafkaConsumer(
                self.input_topic,
                bootstrap_servers=self.kafka_broker,
                auto_offset_reset='latest',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            producer = KafkaProducer(
                bootstrap_servers=self.kafka_broker,
                value_serializer=lambda x: json.dumps(x).encode('utf-8')
            )
            
            logger.info("Connected to Kafka successfully")
            
            # Train models periodically in a separate thread
            threading.Thread(target=self._periodic_training, daemon=True).start()
            
            # Main loop processing messages
            for message in consumer:
                try:
                    reading = message.value
                    enhanced_reading = self.process_reading(reading)
                    
                    if enhanced_reading:
                        # Send to ML anomalies topic
                        producer.send(self.output_topic, enhanced_reading)
                        logger.info(f"ML anomaly detected and sent to Kafka: {enhanced_reading['sensor_id']}")
                        
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
        
        except Exception as e:
            logger.error(f"Kafka consumer error: {e}")
    
    def _periodic_training(self):
        """Periodically train models with new data"""
        while True:
            time.sleep(300)  # Train every 5 minutes
            logger.info("Starting periodic model training")
            
            for sensor_type in self.models.keys():
                if sensor_type in ['motion', 'door_status']:
                    continue  # Skip binary sensors
                    
                if len(self.training_data.get(sensor_type, [])) >= self.min_training_samples:
                    success = self.train_model(sensor_type)
                    if success:
                        logger.info(f"Successfully retrained model for {sensor_type}")

def main():
    logger.info("Starting Machine Learning Anomaly Detector")
    detector = MLAnomalyDetector()
    detector.initialize_models()
    detector.start_consumer()

if __name__ == "__main__":
    main()
