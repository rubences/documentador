# Seguridad del Proyecto Documentador

## Políticas de Seguridad

Este documento establece las políticas de seguridad para el proyecto Documentador. Todos los miembros del equipo deben cumplir estas políticas.

---

## 1. Autenticación y Autorización

### 1.1 Autenticación Interna entre Servicios

**Política:** Todos los endpoints `/internal/*` requieren autenticación mediante header `x-internal-api-key`.

**Implementación:**
- El header debe coincidir con `INTERNAL_API_KEY` en configuración
- Usar comparación de tiempo constante (`hmac.compare_digest`) para prevenir timing attacks
- En desarrollo, se puede deshabilitar con `INTERNAL_AUTH_ENABLED=false`

**Responsabilidad:** Los operadores deben rotar `INTERNAL_API_KEY` cada 90 días.

### 1.2 Rate Limiting

**Política:** Todo cliente está limitado a un número máximo de requests.

**Límites por defecto:**
| Tier | Por Minute | Por Hour |
|------|-----------|---------|
| Default | 30 | 200 |
| Authenticated | 60 | 1000 |

**Implementación:**
- Rate limiting aplicado por IP del cliente
- Headers `X-RateLimit-*` visibles en responses
- HTTP 429 cuando se excede límite

**Excepciones:** Endpoints `/health`, `/metrics` están exentos.

---

## 2. Configuración de Seguridad

### 2.1 Variables de Entorno

**Política:** Nunca commitear secrets en código. Usar variables de entorno o secrets managers.

**Variables requeridas en producción:**

```bash
# Autenticación
INTERNAL_API_KEY=<generado>
INTERNAL_AUTH_ENABLED=true

# CORS
CORS_ALLOWED_ORIGINS=https://dominio-oficial.com

# LLM
OPENAI_API_KEY=<key>
ANTHROPIC_API_KEY=<key>

# RabbitMQ
RABBITMQ_USER=estimation_user
RABBITMQ_PASSWORD=<password-fuerte>

# Redis (opcional)
REDIS_PASSWORD=<password-fuerte>
```

### 2.2 Credentiales por Defecto

**Política:** Nunca deployar con credenciales por defecto.

- ❌ `guest:guest` para RabbitMQ
- ❌ `INTERNAL_API_KEY` por defecto en producción
- ❌ Credenciales hardcodeadas en código

### 2.3 CORS

**Política:** CORS debe permitir solo orígenes específicos.

**Configuración:**
- `allow_origins`: Lista explícita de orígenes, nunca `*`
- `allow_credentials`: `true` solo si es necesario
- `allow_methods`: Lista explícita, nunca `["*"]`

---

## 3. Validación de Inputs

### 3.1 Longitud de Input

**Política:** Todo input de usuario debe tener límites de longitud.

```python
transcription: str = Field(
    ...,  # REQUIRED
    min_length=50,  # Mínimo razonable
    max_length=25000,  # ~25k tokens máximo
)
```

### 3.2 Sanitización

**Política:** Todo input debe ser sanitizado antes de procesamiento.

**Reglas:**
- Remover caracteres de control (`\x00-\x08`, `\x0b`, `\x0c`, `\x0e-\x1f`)
- Normalizar whitespace
- Detectar patrones de inyección conocido

### 3.3 Validación de Job ID

**Política:** Solo UUIDs válidos pueden usarse como job IDs.

```python
if not InputSanitizer.validate_uuid_safe(job_id):
    raise HTTPException(400, "Invalid job_id format")
```

---

## 4. Almacenamiento Seguro

### 4.1 Redis Jobs

**Política:** Jobs en Redis deben expirar automáticamente.

```python
# TTL por defecto: 24 horas
REDIS_JOB_TTL_SECONDS=86400
```

**Responsabilidad:** Monitorear uso de Redis y ajustar TTL según necesidad.

### 4.2 Outbox Pattern

**Política:** Usar el patrón de cola segura para mensajería.

**Implementación:**
- `claim_pending`: Mover a cola de procesamiento
- `mark_sent`: Solo llamar después de éxito
- `requeue`: Si falla, vuelve a pending

### 4.3 Contraseña RabbitMQ

**Polícita:** Usar credenciales fuertes.

**Requisitos:**
- Mínimo 16 caracteres
- Mezcla mayúsculas, minúsculas, números, símbolos
- Sin palabras del diccionario

---

## 5. Logging y Monitoreo

### 5.1 Logging de Seguridad

**Política:** Loggear eventos de seguridad sin exponer datos sensibles.

**Eventos a loggear:**
-Intentos de autenticación fallidos
- Rate limiting triggers
- Posibles inyecciones detectadas
- Errores de validación

**Datos a excluir de logs:**
- API keys (completo)
- Passwords
- Transcripciones de usuarios (truncar a 100 chars)

### 5.2 Health Checks

**Política:**health checks deben verificar dependencias críticas.

**Implementación:**
- Redis: Test de ping
- RabbitMQ: Verificar conexión
- Estimation service: Verificar disponibilidad

---

## 6. Headers de Seguridad

**Política:** Todos los responses deben incluir headers de seguridad.

```python
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'",
}
```

---

## 7. Network Security

### 7.1 Redes Aislamiento

**Política:** Servicios deben comunicarse solo por red interna.

**docker-compose.yml:**
```yaml
networks:
  estimation-network:
    driver: bridge
```

### 7.2 Puertos

**Política:** No exponer puertos innecesarios.

- Puerto 8000 (gateway): Expuesto solo si es necesario
- Puerto 8001 (estimation): Solo para salud interna
- Puerto 5672 (RabbitMQ): Solo red interna
- Puerto 6379 (Redis): Solo red interna

---

## 8. Procedimientos de Seguridad

### 8.1 Rotación de Credenciales

| Credencial | Frecuencia | Procedimiento |
|-----------|------------|---------------|
| INTERNAL_API_KEY | 90 días | Generar nueva, actualizar en todos los servicios |
| RabbitMQ password | 90 días | Actualizar en Docker config |
| Redis password | 90 días | Actualizar en Docker config |
| LLM API keys | 180 días | Rotar en proveedor |

### 8.2 Respuesta a Incidentes

**Si detectas una vulnerabilidad:**

1. **NO** intentar corregir sin approval
2. Documentar steps para reproducir
3. Reportar al lead de seguridad o tech lead
4. Si es críticos → actualizar inmediatamente

### 8.3 Auditoría

**Revisiones de seguridad:**
- Mensual: Review de logs de seguridad
- Trimestral: Pen test básico
- Anual: Auditoría completa

---

## 9. Dependencias

### 9.1 Actualización de Paquetes

**Política:** Mantener dependencias actualizadas.

```bash
#定期mente
uv pip list --outdated
uv pip upgrade
#O revisar Security advisories
```

### 9.2 Verified Versions

**Reglas:**
- Siempre usar versiones específicas (`>=` no es suficiente para producción)
- Revisar changelogs antes de actualizar
- Testear en staging antes de producción

---

## 10. Checklist de Despliegue Seguro

Antes de deployar a producción, verificar:

- [ ] `INTERNAL_API_KEY` generado y configurado
- [ ] `CORS_ALLOWED_ORIGINS` configurado con dominios específicos
- [ ] Credenciales RabbitMQ cambiados de por defecto
- [ ] Rate limiting configurado
- [ ] Logs de seguridad habilitados
- [ ] Health checks funcionando
- [ ] TTL de Redis configurado
- [ ] Headers de seguridad activos
- [ ] Redisolación aplicada
- [ ] Sin credenciales en código

---

## Contacto de Seguridad

**Reporte de vulnerabilidades:** security@ejemplo.com

**Emergencias:** +xx-xxx-xxxx