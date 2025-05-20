#!/bin/sh

# This script converts our digital_twin_flow.json to the native NiFi flow.xml.gz format
# when the container starts - to handle importing directly

echo "Setting up NiFi flow template..."

# We'll provide instructions on manual template import since direct XML conversion
# requires specific NiFi libraries
