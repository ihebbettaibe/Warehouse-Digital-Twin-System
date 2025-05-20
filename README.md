# 🏭 Warehouse Digital Twin System

A comprehensive digital twin implementation for warehouse operations with real-time sensor data processing, anomaly detection using both rule-based and machine learning approaches, and a dynamic dashboard for monitoring.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Docker](https://img.shields.io/badge/docker-required-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

- **Real-time Sensor Monitoring:** Temperature, humidity, motion, pressure, door status, and more
- **Automated Anomaly Detection:** Rule-based and machine learning approaches
- **Interactive Dashboard:** Real-time visualization and alerting
- **Scalable Architecture:** Microservice-based design using Docker containers
- **Open Integration:** Standardized data formats and protocols

## 🏗️ Architecture

![Architecture Diagram](docs/images/architecture_diagram.md)

The system consists of the following components:

1. **Sensor Simulator:** Generates realistic warehouse sensor data
2. **Apache NiFi:** Handles data ingestion and rule-based processing
3. **Apache Kafka:** Enables real-time data streaming
4. **Machine Learning Module:** Provides advanced anomaly detection
5. **Dashboard Application:** Visualizes sensor data and alerts

## 🚀 Quick Start

### Prerequisites

- Docker Desktop and Docker Compose

### Installation

```bash
# Clone this repository
git clone https://github.com/ihebbettaibe/warehouse-digital-twin.git
cd warehouse-digital-twin

# Start the digital twin system
./QuickStart.bat    # Interactive startup (Windows)
# or
./scripts/Start.bat # Direct startup (Windows)
# or
./start.sh          # Linux/Mac
```

### Access

- **Dashboard:** http://localhost:5000
- **Apache NiFi UI:** http://localhost:8080/nifi

## 🔧 Components

### Sensor Data

The system monitors various sensor types:
- Temperature sensors (°C)
- Humidity sensors (%)
- Motion detectors
- Pressure sensors (hPa)
- Door status sensors
- Weight sensors (kg)
- Battery level monitors (%)

### Machine Learning

The ML module provides:
- Unsupervised anomaly detection using Isolation Forest
- Adaptive thresholds that evolve with data patterns
- Multi-dimensional analysis of sensor correlations
- Real-time anomaly scoring and classification

### Dashboard

The dashboard provides:
- Zone-based warehouse visualization
- Real-time sensor readings
- Historical data trends
- Alert management
- Anomaly visualization

## 📊 Screenshots

![Dashboard](docs/images/dashboard_preview.md)
![NiFi Flow](docs/images/nifi_flow.md)
![Anomaly Detection](docs/images/ml_anomaly.md)

## 🛠️ Development

### Project Structure

```
warehouse-digital-twin/
├── docker-compose.yml           # Main configuration
├── QuickStart.bat               # Interactive startup script (Windows)
├── QuickStart.ps1               # PowerShell startup script
├── sensor_simulator/            # Sensor data simulator
├── nifi_flows/                  # NiFi processing flows
├── machine_learning/            # ML-based anomaly detection
├── dashboard/                   # Web dashboard
├── docs/                        # Documentation
└── scripts/                     # Utility scripts
    ├── Start.bat                # Start the system (Windows)
    ├── Start-DigitalTwin.ps1    # Start the system (PowerShell)
    ├── Stop.bat                 # Stop the system (Windows)
    ├── Stop-DigitalTwin.ps1     # Stop the system (PowerShell)
    ├── CheckStatus.bat          # Check system status (Windows)
    ├── Check-Services.ps1       # Check system status (PowerShell)
    └── Setup-GitHub.ps1         # Initialize GitHub repository
```

### Adding New Sensors

1. Add the sensor configuration to the `SENSOR_TYPES` dictionary in `sensor_simulator.py`
2. Update the NiFi flow to process the new sensor type
3. Add appropriate ML models if needed
4. Modify the dashboard to display the new sensor data

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.


