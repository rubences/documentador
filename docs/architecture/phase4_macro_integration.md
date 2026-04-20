# FASE 4 - Integracion macro GraphRAG + OpenCode + Chatbot

## Objetivo

Definir como la infraestructura robusta (Gateway + Circuit Breaker + RabbitMQ + Redis + Outbox + DLQ) soporta cargas pesadas de GraphRAG sin degradar la experiencia interactiva de OpenCode y Chatbot.

## Principio no negociable: fronteras separadas

- Frontera de ingestión/indexación: procesos pesados, asíncronos, no bloqueantes.
- Frontera de consulta interactiva: latencia acotada, fail-fast, sin acoplamiento al pipeline pesado.
- OpenCode y Chatbot nunca acceden directamente a storage interno de GraphRAG.
- Toda interacción pasa por Gateway y/o MCP Bridge con contratos HTTP/AMQP estables.

## Arquitectura objetivo (sobre la base actual)

Componentes de entrada:

- api-gateway: entrada unica para OpenCode, Chatbot y API externa.
- mcp-bridge-service: adaptador de herramientas para OpenCode (Tools/MCP).

Componentes de procesamiento:

- estimation-service: ya existente, protegido con RabbitMQ/Outbox/DLQ.
- graphrag-query-service: servicio de consulta semantica para preguntas interactivas.
- graphrag-ingestion-service: servicio batch para indexacion/reindexacion pesada.

Componentes de infraestructura:

- RabbitMQ: bus de eventos y comandos asíncronos.
- Redis: estado de jobs, outbox y cache temporal de resultados.
- Observabilidad: Prometheus + request-id/correlation-id extremo a extremo.

## Contratos recomendados (codigo/API)

Consultas interactivas (OpenCode/Chatbot):

- POST /api/v1/graphrag/query
- SLA objetivo: p95 <= 2-4s para consultas locales; timeout duro en gateway.
- Respuesta parcial/fallback si GraphRAG no responde en ventana.

Ingestión pesada (offline/batch):

- POST /api/v1/graphrag/ingestion/async
- Devuelve job_id y correlation_id inmediatos (202).
- Estado por GET /api/v1/graphrag/jobs/{job_id} persistido en Redis.

Eventos sugeridos (AMQP):

- graphrag.ingestion.requested
- graphrag.ingestion.started
- graphrag.ingestion.completed
- graphrag.ingestion.failed
- graphrag.query.requested
- graphrag.query.completed

## Flujo OpenCode (Tools/MCP)

- OpenCode invoca tool MCP (queryGraphRag, refreshIndex, getJobStatus).
- MCP Bridge traduce Tool call a API Gateway.
- Gateway aplica timeout/circuit breaker y propaga x-request-id + x-correlation-id.
- Si es consulta, enruta a graphrag-query-service.
- Si es indexacion, crea evento en outbox y publica a RabbitMQ.
- Worker de ingestion consume, ejecuta pipeline GraphRAG pesado y publica estado.

Resultado:

- OpenCode conserva UX interactiva porque nunca espera indexaciones largas sincronicamente.
- Chatbot comparte el mismo canal robusto de consulta y fallback.

## Flujo Chatbot

- Chatbot -> Gateway -> graphrag-query-service.
- Si query-service falla o excede timeout:
- Gateway responde fallback controlado y marca metrica de degradacion.
- Circuit Breaker evita cascada de latencia sobre toda la conversacion.

## Flujo GraphRAG Ingestion

- Trigger (manual/cron/evento) -> Gateway async endpoint.
- Gateway persiste comando en outbox (Redis) y responde 202.
- Outbox dispatcher publica en RabbitMQ.
- Worker ingestion procesa dataset, chunks y actualizacion de indice.
- Errores transitorios: retry exponencial.
- Errores definitivos: DLQ + estado failed en Redis.

## Por que evita monolito distribuido

- Separacion explicita de bounded contexts (query vs ingestion).
- Contratos estables y versionables entre servicios.
- Estado de larga duracion fuera de memoria local.
- Mecanismos de resiliencia en borde (gateway) y en bus (DLQ/retries/outbox).

## Mapeo directo a lo ya implementado

Ya disponible en este repo:

- Circuit Breaker + timeout configurable en gateway.
- Observabilidad con request-id/correlation-id y /metrics.
- RabbitMQ con retry exchange + DLQ.
- Outbox en Redis para publicacion fiable.
- Estado async en Redis para jobs.

Extensiones fase siguiente (implementacion de GraphRAG/OpenCode):

- Crear graphrag-query-service y graphrag-ingestion-service.
- Crear mcp-bridge-service para OpenCode Tools.
- Añadir endpoints /api/v1/graphrag/* en gateway.
- Definir schemas JSON para eventos graphrag.*.

## Codigo TikZ (arquitectura macro)

Ver archivo:

- docs/architecture/phase4_macro_integration.tikz

Este diagrama esta listo para incrustar en el manual tecnico con \input{}.
