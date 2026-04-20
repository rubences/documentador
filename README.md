# Proyecto Atlas (Plataforma Smart City)

Este repositorio contiene documentación técnica en LaTeX y una implementación de referencia en Python para estimaciones asistidas por IA.

## Arquitectura de microservicios (Python)

La aplicación Python se ha reestructurado en dos microservicios desacoplados:

- `api-gateway` (FastAPI, puerto `8000`): expone API pública síncrona y asíncrona.
- `estimation-service` (FastAPI, puerto `8001`): expone API interna y procesa trabajos de estimación.
- `rabbitmq` (puerto `5672`, panel `15672`): desacopla la carga asíncrona de estimaciones largas.
- `redis` (puerto `6379`): persiste estado de jobs asíncronos y cola outbox.

Flujos:

- Síncrono: `POST /api/v1/estimate` -> `POST /internal/v1/estimate`
- Asíncrono: `POST /api/v1/estimate/async` -> cola RabbitMQ -> worker -> `GET /api/v1/estimate/{job_id}`

Resiliencia:

- Gateway con `timeouts` estrictos y `circuit breaker` (fail-fast en 503 cuando downstream está degradado).
- Publicación asíncrona con patrón `Outbox` en Redis para entrega eventual.
- RabbitMQ con topología `main + retry + DLQ` y reintentos exponenciales en consumidor.

Observabilidad distribuida:

- Propagación de `x-request-id` y `x-correlation-id` entre gateway y estimation-service.
- Métricas Prometheus por servicio en `/metrics`.
- Estado del circuit breaker visible en `/health` del gateway.

Contratos compartidos:

- `app/shared/schemas/estimation.py`

Entrypoints:

- Gateway: `app.gateway.main:app`
- Estimation service: `app.estimation.main:app`

Compatibilidad:

- `app.main:app` apunta al gateway para no romper arranques previos.

## Ejecutar con Docker Compose

```bash
docker compose up --build
```

Servicios:

- Gateway: `http://localhost:8000/health`
- Estimation service: `http://localhost:8001/health`
- RabbitMQ Management: `http://localhost:15672`
- Redis: `redis://localhost:6379/0`

Endpoints principales:

- `POST /api/v1/estimate`
- `POST /api/v1/estimate/async`
- `GET /api/v1/estimate/{job_id}`
- `GET /metrics` (en gateway y estimation-service)

## Variables de entorno clave

Gateway:

- `ESTIMATION_SERVICE_URL`
- `GATEWAY_TIMEOUT_CONNECT_SECONDS`
- `GATEWAY_TIMEOUT_READ_SECONDS`
- `GATEWAY_TIMEOUT_WRITE_SECONDS`
- `GATEWAY_TIMEOUT_POOL_SECONDS`
- `GATEWAY_CIRCUIT_BREAKER_FAILURE_THRESHOLD`
- `GATEWAY_CIRCUIT_BREAKER_RECOVERY_TIMEOUT_SECONDS`
- `GATEWAY_CIRCUIT_BREAKER_HALF_OPEN_SUCCESS_THRESHOLD`

Estimation-service / mensajería:

- `RABBITMQ_ENABLED`
- `RABBITMQ_URL`
- `RABBITMQ_EXCHANGE`
- `RABBITMQ_QUEUE`
- `RABBITMQ_ROUTING_KEY`
- `RABBITMQ_RETRY_EXCHANGE`
- `RABBITMQ_RETRY_QUEUE`
- `RABBITMQ_DLQ_EXCHANGE`
- `RABBITMQ_DLQ_QUEUE`
- `RABBITMQ_MAX_RETRIES`
- `RABBITMQ_BASE_RETRY_DELAY_MS`
- `REDIS_URL`
- `REDIS_JOB_KEY_PREFIX`
- `OUTBOX_KEY_PREFIX`
- `OUTBOX_DISPATCH_BATCH_SIZE`
- `OUTBOX_DISPATCH_INTERVAL_SECONDS`

## Ejecutar en local (sin Docker)

```bash
uvicorn app.estimation.main:app --host 0.0.0.0 --port 8001 --reload
uvicorn app.gateway.main:app --host 0.0.0.0 --port 8000 --reload
```

## Tests

```bash
pytest -q
```

Cobertura relevante:

- Integración gateway con latencia/fallos/propagación de IDs.
- Comportamiento del circuit breaker (apertura y recuperación).
- Persistencia de estado asíncrono en Redis (job store) sin depender de infraestructura externa en tests.

