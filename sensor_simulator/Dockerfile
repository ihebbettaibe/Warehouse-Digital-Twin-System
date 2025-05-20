FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install kafka-python

ENV KAFKA_BROKER=kafka:9092

CMD ["python", "sensor_simulator.py"]
