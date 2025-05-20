# Importing NiFi Flow Template

This document explains how to import the Digital Twin flow template into Apache NiFi.

## Steps:

1. Access the NiFi UI at http://localhost:8080/nifi/ 
   (Wait until NiFi is fully started - this may take 2-3 minutes)

2. Import the template:
   a. Click the menu icon (☰) in the top right corner
   b. Select "Upload Template" from the menu
   c. Click "Browse" and navigate to this directory
   d. Select the `digital_twin_flow.json` file and click "Upload"

3. Add the template to the canvas:
   a. Drag the template icon (🧩) from the top toolbar onto the canvas
   b. Select "Digital Twin NiFi Flow Template" from the dropdown
   c. Click "Add"

4. Configure the processors:
   a. Select all components (Ctrl+A or click-and-drag to select all)
   b. Right-click and select "Configure" 
   c. Go to the "Properties" tab
   d. Update the Kafka broker addresses to: `kafka:9092`
   e. Click "Apply"

5. Start the flow:
   a. Select all components (Ctrl+A)
   b. Right-click and select "Start"

## Note:

The NiFi flow is configured to:
- Consume data from Kafka topics matching pattern `warehouse-sensors-.*`
- Process and transform the sensor readings
- Detect anomalies in sensor values
- Publish processed data to `warehouse-processed` Kafka topic
- Publish detected anomalies to `warehouse-alerts` Kafka topic
