# Circuit Breaker Manager: Microservice Resilience Platform

`Circuit Breaker Manager` is an end-to-end resilient microservice platform designed for automated health monitoring of external API dependencies, dynamic circuit state management, and real-time observability in distributed FinTech environments. The architecture integrates asynchronous event-driven patterns, Redis-based state caching, and Kubernetes-native orchestration for high-availability deployments.

## System Architecture and Core Components

The pipeline is engineered as a sequence of isolated, reproducible stages replicating industry-standard FinTech workflows:

1. **Async Monitoring & ETL Pipeline:** Automated asynchronous health checks (via `asyncio`) for external banking and payment provider APIs, with structural validation and event-driven logging of service status.
2. **Circuit Breaker Engine:**
    * **State Management:** A robust state machine implementation tracking transitions between **CLOSED**, **OPEN**, and **HALF_OPEN** modes to prevent cascading system failures.
    * **Failure Threshold Logic:** Automated threshold tracking for rapid response to external dependency outages or latency degradation.
3. **Hybrid Observability & Task Engine:**
    * **Event Processing:** Distributed task management via RabbitMQ and Celery for decoupled background processing of health events and configuration updates.
    * **Telemetry Pipeline:** Real-time metrics collection via Prometheus and distributed tracing for auditing and performance analysis.
4. **Generative & Reactive Integration:** WebSocket-based real-time status broadcasting to downstream systems and secure integration with Postgres for persistent configuration storage.

---

## Technical Stack

- **Core Language:** Python 3.12
- **Infrastructure & Orchestration:** Kubernetes (K8s), Docker, Docker Compose
- **Data & Caching:** PostgreSQL, Redis
- **Message Broker:** Celery
- **Observability:** Prometheus, Grafana, Jaeger
- **Framework:** FastAPI
