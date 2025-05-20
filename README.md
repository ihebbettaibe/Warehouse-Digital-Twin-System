# Warehouse Digital Twin System

This project implements a digital twin for warehouse operations, providing real-time monitoring, analysis, and visualization of sensor data.

## Architecture

The system consists of the following components:

1. **Sensor Simulator**: A Python application that generates realistic sensor data mimicking warehouse operations
2. **Apache NiFi**: Handles data ingestion and transformation
3. **Apache Kafka**: Provides real-time data streaming capabilities
4. **Machine Learning Detector**: Uses ML algorithms to identify complex anomalies in sensor data
5. **Dashboard Application**: A Flask-based web application with real-time updates via WebSockets

## Prerequisites

- Docker Desktop and Docker Compose

## Getting Started

1. Clone this repository
2. Navigate to the project directory
3. Run the quickstart script:
   ```powershell
   .\QuickStart.ps1
   ```
   
   Or for a command-line interface:
   ```powershell
   .\scripts\Start-DigitalTwin.ps1
   ```

This script will:
- Check if Docker is running (and help you start it if needed)
- Start all required services with docker-compose
- Provide access links to the dashboard and NiFi UI

### Helper Scripts

We've provided several PowerShell scripts to make managing the system easier:

- `Start-DigitalTwin.ps1`: Starts the entire system
- `Stop-DigitalTwin.ps1`: Shuts down all services
- `Check-Docker.ps1`: Verifies Docker is running
- `Check-Services.ps1`: Monitors the status of all services

> **Note**: When starting the system for the first time, services like NiFi may take 2-3 minutes to fully initialize. 
> The dashboard may show no data until the entire pipeline is running.

## Accessing the System

- **Dashboard**: http://localhost:5000
- **Apache NiFi UI**: http://localhost:8080/nifi/

## System Components

### Sensor Simulator

The sensor simulator generates data for various sensor types:
- Temperature
- Humidity
- Motion detection
- Pressure
- Door status
- Battery level
- Weight

Data is generated for different zones in the warehouse, with occasional anomalies to test the alerting system.

### Apache NiFi Flow

The NiFi flow:
1. Consumes sensor data from Kafka
2. Processes and transforms the data
3. Detects anomalies using configurable thresholds
4. Routes standard readings to the processed data topic
5. Routes anomalies to a dedicated alerts topic

### Kafka Topics

- **warehouse-sensors-{sensor_type}**: Raw sensor readings by type
- **warehouse-processed**: All processed sensor readings
- **warehouse-alerts**: Rule-based detected anomalies
- **warehouse-ml-anomalies**: Machine learning detected anomalies

### Dashboard

The dashboard provides:
- Real-time visualization of sensor readings
- Anomaly alerts and notifications
- Zone-based overview of warehouse conditions
- Historical data charting

## Project Structure

```
warehouse-digital-twin/
├── docker-compose.yml           # Main Docker Compose configuration
├── sensor_simulator/            # Sensor data simulator
│   ├── sensor_simulator.py      # Generates realistic sensor data
│   └── Dockerfile               # Builds simulator container
├── nifi_flows/                  # NiFi flow templates
│   └── digital_twin_flow.json   # Sensor data processing flow
├── kafka_config/                # Kafka configuration files
├── machine_learning/            # ML-based anomaly detection
│   ├── ml_detector.py           # ML service for anomaly detection
│   ├── Dockerfile               # Builds ML container
│   ├── requirements.txt         # Python dependencies
│   ├── models/                  # Trained model storage
│   ├── data/                    # Data storage and samples
│   └── notebooks/               # Jupyter notebooks for analysis
│       └── anomaly_detection_analysis.ipynb
├── dashboard/                   # Real-time web dashboard
│   ├── app.py                   # Flask application
│   ├── templates/               # HTML templates
│   │   └── index.html           # Dashboard UI
│   ├── requirements.txt         # Python dependencies
│   └── Dockerfile               # Builds dashboard container
└── docker/                      # Additional Docker configuration
```

## Customization

### Adding New Sensor Types

1. Add the sensor configuration to the `SENSOR_TYPES` dictionary in `sensor_simulator.py`
2. Update the NiFi flow to process the new sensor type
3. Modify the dashboard to display the new sensor data

### Modifying Anomaly Detection Rules

1. Edit the `DetectAnomaly` processor script in the NiFi flow
2. Adjust the threshold values based on your requirements

## Troubleshooting

### Docker Connection Issues

If you see an error like `unable to get image` or `error during connect`:
1. Run the provided script to check Docker status: `.\Check-Docker.ps1`
2. Make sure Docker Desktop is running (look for the Docker icon in your system tray)
3. If Docker is not running, start Docker Desktop from your Start menu
4. Wait for Docker to fully initialize before running docker-compose

### Kafka Connection Issues

If components can't connect to Kafka:
1. Ensure Kafka container is running: `docker ps | grep kafka`
2. Check Kafka logs: `docker logs kafka`
3. Verify network connectivity between containers

### NiFi Flow Not Processing Data

1. Access the NiFi UI at http://localhost:8080/nifi/
2. Check processor status and error messages
3. Verify Kafka topics exist using a tool like kcat or Kafka UI

### Dashboard Not Displaying Data

1. Check browser console for errors
2. Verify Kafka consumer is running in the dashboard logs
3. Ensure data is flowing through the pipeline by checking Kafka topics
