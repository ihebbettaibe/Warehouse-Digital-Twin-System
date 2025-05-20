```
                        ┌───────────────┐
                        │    Sensors    │
                        └───────┬───────┘
                                │ 
                                ▼
┌───────────────┐      ┌───────────────┐
│  Sensor Data  │◄─────┤     NiFi      │
│   Simulator   │      │   (Ingestion) │
└───────┬───────┘      └───────┬───────┘
        │                      │
        │                      ▼
        │              ┌───────────────┐
        └─────────────►│     Kafka     │
                       │   (Streaming) │
                       └───────┬───────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   Dashboard   │    │  ML Anomaly   │    │  Other Data   │
│      App      │    │   Detection   │    │   Consumers   │
└───────────────┘    └───────────────┘    └───────────────┘
```

*This is an ASCII architecture diagram showing the data flow of the digital twin system. Actual image to be replaced with a proper diagram.*
