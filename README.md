## Proyecto Atlas (Plataforma Smart City)

Este repositorio contiene documentación técnica en LaTeX y una implementación de referencia en Python para estimaciones asistidas por IA.

## Arquitectura de microservicios (Python)

La aplicación Python se ha reestructurado en dos microservicios desacoplados:

- `api-gateway` (FastAPI, puerto `8000`): expone API pública síncrona y asíncrona.
- `estimation-service` (FastAPI, puerto `8001`): expone API interna y procesa trabajos de estimación.
- `rabbitmq` (puerto `5672`, panel `15672`): desacopla la carga asíncrona de estimaciones largas.

Flujos:

- Síncrono: `POST /api/v1/estimate` -> `POST /internal/v1/estimate`
- Asíncrono: `POST /api/v1/estimate/async` -> cola RabbitMQ -> worker -> `GET /api/v1/estimate/{job_id}`

Observabilidad distribuida:

- Propagación de `x-request-id` y `x-correlation-id` entre gateway y estimation-service.
- Métricas Prometheus por servicio en `/metrics`.

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

Endpoints principales:

- `POST /api/v1/estimate`
- `POST /api/v1/estimate/async`
- `GET /api/v1/estimate/{job_id}`
- `GET /metrics` (en gateway y estimation-service)

## Ejecutar en local (sin Docker)

```bash
uvicorn app.estimation.main:app --host 0.0.0.0 --port 8001 --reload
uvicorn app.gateway.main:app --host 0.0.0.0 --port 8000 --reload
```

## Tests

```bash
pytest -q
```

