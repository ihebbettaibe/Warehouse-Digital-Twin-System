```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ ListenTCP/    │     │ SplitJSON/    │     │ JoltTransform │
│ ListenHTTP    ├────►│ EvaluateJSON  ├────►│               │
└───────────────┘     └───────────────┘     └───────┬───────┘
                                                    │
                                                    ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ PublishKafka  │◄────┤ UpdateAttribute│◄────┤ RouteOnAttribute│
└───────────────┘     └───────────────┘     └───────────────┘
```

*This is an ASCII representation of the NiFi dataflow. Actual image to be replaced with a screenshot of the configured NiFi canvas.*
