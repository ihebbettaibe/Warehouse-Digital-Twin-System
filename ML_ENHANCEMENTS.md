# Machine Learning Enhancement for Warehouse Digital Twin

## Overview

This document describes the machine learning capabilities added to the Warehouse Digital Twin system to enhance anomaly detection and provide predictive insights.

## Machine Learning Features

### 1. Advanced Anomaly Detection

The ML component uses **Isolation Forest** algorithm to detect anomalies that might be missed by traditional threshold-based approaches. This algorithm is particularly effective for:

- Detecting subtle patterns and correlations across multiple sensors
- Adapting to seasonal changes in the warehouse environment
- Identifying anomalies in high-dimensional data
- Learning normal behavior without requiring labeled training data

### 2. Real-time Processing Pipeline

The ML processing pipeline consists of several stages:

1. **Data Collection**: Sensor readings are consumed from Kafka topics
2. **Feature Extraction**: Raw readings are transformed into meaningful features
3. **Anomaly Detection**: The Isolation Forest model scores each reading
4. **Alert Generation**: Anomalies are published back to Kafka for visualization

### 3. Continuous Learning

The ML system continuously improves by:

- Collecting initial data to establish a baseline
- Periodically retraining models to adapt to changing patterns
- Maintaining separate models for different sensor types and warehouse zones

## Technical Implementation

### Data Flow

```
Sensor Data → Kafka → NiFi → Processed Data Topic → ML Detector → ML Anomalies Topic → Dashboard
```

### ML Component Architecture

- **Input**: Processed sensor readings from `warehouse-processed` Kafka topic
- **Processing**: Python-based ML service with scikit-learn models
- **Output**: ML-detected anomalies to `warehouse-ml-anomalies` Kafka topic
- **Storage**: Trained models are saved to disk for persistence and analysis

### Dashboard Integration

The dashboard is enhanced to:

- Display ML-detected anomalies with special styling
- Show confidence scores for detected anomalies
- Provide insights into why an anomaly was detected

## Extending the ML Component

### Adding New Models

To add new machine learning capabilities:

1. Create a new Python script in the `machine_learning` directory
2. Update the Kafka topic configuration for new inputs/outputs
3. Update the dashboard to visualize the new insights

### Training Custom Models

For advanced users who want to train custom models:

1. Explore the Jupyter notebook in `machine_learning/notebooks/`
2. Modify the training parameters and features
3. Export the trained model to the `models` directory

## Future Enhancements

- **Predictive Maintenance**: Forecast when equipment might fail based on sensor trends
- **Inventory Optimization**: Predict optimal inventory levels based on warehouse conditions
- **Energy Efficiency**: Suggest optimal environmental settings to reduce energy consumption
- **Pattern Recognition**: Identify recurring patterns in warehouse operations
