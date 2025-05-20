FROM python:3.9-slim

WORKDIR /app

# Install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Create necessary directories
RUN mkdir -p models data

# Run the ML detector
CMD ["python", "ml_detector.py"]
