# Checklist de Seguridad para Producción

Este documento proporciona un checklist completo de verificación de seguridad para antes de deployar.

---

## 1. Configuración de Redis

| Item | Estado | Notas |
|------|--------|-------|
| Redis con password | ⚠️ Pendiente | Configurar REDIS_PASSWORD |
| TLS para Redis | ⚠️ Pendiente | redis:// → rediss:// |
| Max memory configurado | ⚠️ Pendiente | maxmemory 256mb |
| Eviction policy | ⚠️ Pendiente | allkeys-lru |
| Puerto protegido | ✅Listo | Solo red interna |

---

## 2. Configuración de RabbitMQ

| Item | Estado | Notas |
|------|--------|-------|
| Usuario no guest | ⚠️ Pendiente | Crear usuario específico |
| Password fuerte | ✅Hecho | Configurado en compose |
| TLS habilitado | ⚠️ Pendiente | amqps:// |
| Vhost separado | ⚠️ Pendiente | Para producción |
| Policy de DLQ | ✅Listo | DLQ configurada |
| Límite de conexiones | ⚠️ Pendiente | max_connections |

---

## 3. Docker y Red

| Item | Estado | Notas |
|------|--------|-------|
| Usuario no root | ✅Listo | appuser |
| Redes isoladas | ✅Listo | estimation-network |
| Secrets externalizados | ⚠️ Pendiente | Usar Docker secrets |
| Health checks | ✅Listo | Configurados |
| Recursos limitados | ⚠️ Pendiente | CPU/RAM limits |
| --reload disabled | ✅Listo | En producción |

---

## 4. Dependencias

| Item | Estado | Notas |
|------|--------|-------|
| Deps actualizadas | ⚠️ Pendiente | Revisar security advisories |
| Versiones fijadas | ✅Listo | pyproject.toml |
| Audit dependencias | ⚠️ Pendiente | safety check |
| No dev deps en prod | ✅Listo | --no-dev |

---

## 5. Secrets

| Item | Estado | Notas |
|------|--------|-------|
| INTERNAL_API_KEY | ⚠️ Pendiente | Generar nuevo |
| LLM API keys | ⚠️ Pendiente | Configurar en .env |
| CORS_ORIGINS | ⚠️ Pendiente | Domains específicos |
| RabbitMQ password | ⚠️ Pendiente | Cambiar de default |

---

## 6. Logging

| Item | Estado | Notas |
|------|--------|-------|
| No secrets en logs | ⚠️ Pendiente | Audit code |
| Formato estructurado | ✅Listo | JSON en prod |
| Nivel apropiado | ⚠️ Pendiente | INFO en prod |
| Rotación logs | ⚠️ Pendiente | Configurar |

---

## 7. Producción

| Item | Estado | Notas |
|------|--------|-------|
| APP_ENV=production | ⚠️ Pendiente | Cambiar a production |
| DEBUG=false | ⚠️ Pendiente | No debug |
| Logs a sistema | ⚠️ Pendiente | Stdout |
| Exit handlers | ⚠️ Pendiente | Graceful shutdown |

---

## 8. Certificados SSL/TLS

| Item | Estado | Notas |
|------|--------|-------|
| HTTPS en gateway | ⚠️ Pendiente | Terminar SSL |
| Certificados válidos | ⚠️ Pendiente | LetsEncrypt |
| HSTS | ⚠️ Pendiente | Strict-Transport-Security |

---

## 9. Monitoreo

| Item | Estado | Notas |
|------|--------|-------|
| Métricas Prometheus | ✅Listo | /metrics |
| Alertas seguridad | ⚠️ Pendiente | Rate limit alerts |
| Logs centralizados | ⚠️ Pendiente | ELK/CloudWatch |
| Health checks | ✅Listo | /health |

---

## Comandos de Verificación

```bash
# 1. Verificar secrets
grep -r "password\|key\|secret" app/ --include="*.py" | grep -v "hash\|sha"

# 2. Verificar config de producción
grep "production\|DEBUG" app/**/*.py

# 3. Dependencias con vulnerabilidades
pip install safety
safety check

# 4. Scan de Docker
docker scan estimator:latest

# 5. Audit de código
ruff check app/
```

---

## Checklist de Despliegue

Antes de hacer deploy a producción, ejecutar:

- [ ] INTERNAL_API_KEY generado con `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- [ ] CORS_ALLOWED_ORIGINS configurado
- [ ] RabbitMQ credentials cambiados
- [ ] Redis password configurado
- [ ] APP_ENV=production
- [ ] Health checks funcionan
- [ ] Rate limiting testeado
- [ ] Auth interna testeada
- [ ] Logs sin secrets
- [ ] Tests de seguridad pasan