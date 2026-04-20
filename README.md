## Proyecto Atlas (Plataforma Smart City)

Este repositorio contiene documentación técnica en LaTeX y una implementación de referencia en Python para estimaciones asistidas por IA.

## Arquitectura de microservicios (Python)

La aplicación Python se ha reestructurado en dos microservicios desacoplados:

- `api-gateway` (FastAPI, puerto `8000`): expone `/api/v1/estimate` y delega la generación al servicio interno.
- `estimation-service` (FastAPI, puerto `8001`): expone `/internal/v1/estimate` y ejecuta la lógica LLM.

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

## Ejecutar en local (sin Docker)

```bash
uvicorn app.estimation.main:app --host 0.0.0.0 --port 8001 --reload
uvicorn app.gateway.main:app --host 0.0.0.0 --port 8000 --reload
```

## Tests

```bash
pytest -q
```

