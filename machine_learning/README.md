# Machine Learning Anomaly Detection for Warehouse Digital Twin

This component adds advanced machine learning capabilities to the Warehouse Digital Twin system for anomaly detection in sensor data.

## Overview

The machine learning module applies Isolation Forest algorithm to detect anomalies that might be missed by traditional threshold-based approaches. It operates in real-time by consuming data from Kafka, analyzing it, and publishing detected anomalies back to Kafka.

## Components

1. **ML Detector Service**: A Python service that consumes sensor data from Kafka, applies machine learning models to detect anomalies, and publishes detected anomalies to a dedicated topic.

2. **Jupyter Notebooks**: Analysis notebooks for model development, testing and visualization.

3. **Pre-trained Models**: Models trained on warehouse sensor data, ready for deployment.

## Features

- **Unsupervised Learning**: Automatically learns normal patterns without requiring labeled training data.
- **Adaptive Thresholds**: Adapts to changing sensor patterns over time.
- **Multi-dimensional Analysis**: Can detect anomalies considering multiple sensor values together.
- **Real-time Processing**: Analyzes data as it arrives with low latency.
- **Online Learning**: Continuously updates models based on new data.

## Architecture

The ML component integrates with the system as follows:

```
Sensor Data → Kafka → NiFi → Processed Data Topic → ML Detector → ML Anomalies Topic → Dashboard
```

## Machine Learning Process

1. **Data Collection**: Initial readings are collected to establish a baseline.
2. **Model Training**: Isolation Forest models are trained for each sensor type.
3. **Anomaly Detection**: New readings are evaluated against models to detect outliers.
4. **Alert Generation**: Detected anomalies are published for visualization and notification.
5. **Continuous Learning**: Models are periodically retrained to adapt to changing patterns.

## Technical Details

- **Algorithm**: Isolation Forest (effective for high-dimensional and multivariate data)
- **Feature Engineering**: Time-based features, statistical aggregations, and sensor-specific preprocessing
- **Evaluation Metrics**: Precision, recall, and F1-score for anomaly detection

## Directory Structure

```
machine_learning/
├── ml_detector.py          # Main ML service for anomaly detection
├── Dockerfile              # Container definition
├── requirements.txt        # Python dependencies
├── models/                 # Trained model storage
├── data/                   # Data storage and sample datasets
└── notebooks/              # Jupyter notebooks for analysis
    └── anomaly_detection_analysis.ipynb
```

## Getting Started

The ML component is automatically integrated with the Warehouse Digital Twin system when using Docker Compose.

To run the ML component independently:

```bash
cd machine_learning
pip install -r requirements.txt
python ml_detector.py
```

## Accessing ML Analysis Notebook

To access the Jupyter notebook for data analysis:

1. Install Jupyter: `pip install jupyter`
2. Navigate to the notebooks directory: `cd machine_learning/notebooks`
3. Start Jupyter: `jupyter notebook`
4. Open the `anomaly_detection_analysis.ipynb` notebook

## Extending the ML Component

To add new machine learning capabilities:

1. Add new model training scripts in the `machine_learning` directory
2. Update `ml_detector.py` to use the new models
3. Add appropriate Kafka topics for the new model outputs
4. Update the dashboard to visualize the new insights
