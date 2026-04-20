# Índice General del Manual del Proyecto

## Plan de Sostenibilidad Turística en Destino — San Lorenzo de El Escorial

**Documento:** Manual del Proyecto

**Versión:** 1.0

**Fecha:** Abril 2026

**Cumple con:** Pliego de Prescripciones Técnicas § 11

**Destinatario:** Ayuntamiento de San Lorenzo de El Escorial

---

## Estructura General

El Manual del Proyecto consta de 6 Partes principales y 7 Anexos de referencia.

Cada Parte corresponde a un requisito específico del Pliego § 11:
- Parte 1: Detalle de Hardware
- Parte 2: Detalle de Software
- Parte 3: Manual de Instrucciones de Usuario
- Parte 4: Manual de Instrucciones de Administración
- Parte 5: Manual de Mantenimiento
- Parte 6: Plan de Formación

---

## PARTE 1: DETALLE DE HARDWARE

Archivo: `parte1-hardware/`

Especificaciones técnicas completas de todos los componentes de infraestructura.

### 1.1 Plataforma de Ciudad Inteligente

Componentes de infraestructura IT: servidores de aplicación, almacenamiento, sistemas de respaldo, conectividad de red, seguridad perimetral.

### 1.2–1.5 Actuaciones de Software

Equipamiento de servidores web y de aplicación, CDN, almacenamiento de medios, infraestructura de apps móviles.

### 1.6–1.13 Actuaciones de Sensórica

Sensores de ocupación, ambientales, tráfico, dispositivos de señalización, infraestructura de comunicación, lectores NFC/RFID.

---

## PARTE 2: DETALLE DE SOFTWARE

Archivo: `parte2-software/`

Inventario completo de componentes software instalados: sistemas operativos, plataformas de aplicación (Fastify, Strapi, Node.js), librerías de infraestructura (RabbitMQ, MariaDB, Valkey, Ollama), dependencias de terceros, árbol de dependencias y versionado.

---

## PARTE 3: MANUAL DE INSTRUCCIONES DE USUARIO

Directorio: `parte3-manual-usuario/`

Instrucciones operativas para usuarios municipales con capacidad de edición de contenidos. Una sección por cada una de las 13 actuaciones.

| Sección | Actuación | Contenido Clave |
| --- | --- | --- |
| 3.1 | Plataforma de Ciudad Inteligente | Acceso, navegación, permisos básicos |
| 3.2 | CMS Turístico | Crear y publicar contenido |
| 3.3 | Web de Turismo | Gestionar páginas y banners |
| 3.4 | Apps de Turismo | Gestionar contenido en apps |
| 3.5 | Cartelería Digital | Programar pantallas digitales |
| 3.6 | Señalización Turística | Gestionar beacons y POI |
| 3.7 | Flujos Turísticos | Consultar datos de afluencia |
| 3.8 | Sensorización Ambiental | Consultar datos ambientales |
| 3.9 | Aparcamientos | Consultar disponibilidad |
| 3.10 | Control de Tráfico | Consultar datos de tráfico |
| 3.11 | Tarjeta Turística | Gestionar beneficios |
| 3.12 | Dinamización Digital | Crear campañas |
| 3.13 | Red WiFi | Consultar datos de cobertura |

---

## PARTE 4: MANUAL DE INSTRUCCIONES DE ADMINISTRACIÓN

Directorio: `parte4-manual-administrador/`

Instrucciones avanzadas para administradores municipales. Cubre gestión de usuarios, permisos, administración de bases de datos, certificados, seguridad, auditoría y compliance.

Una sección por cada una de las 13 actuaciones.

| Sección | Actuación | Contenido Clave |
| --- | --- | --- |
| 4.1 | Plataforma de Ciudad Inteligente | Gestión de usuarios y permisos |
| 4.2 | CMS Turístico | Admin de BD y flujos |
| 4.3 | Web de Turismo | Certificados y dominios |
| 4.4 | Apps de Turismo | Distribución en app stores |
| 4.5 | Cartelería Digital | Admin remota de equipamiento |
| 4.6 | Señalización Turística | Sincronización de beacons |
| 4.7 | Flujos Turísticos | Integridad de datos |
| 4.8 | Sensorización Ambiental | Calibración remota |
| 4.9 | Aparcamientos | Sincronización y análisis |
| 4.10 | Control de Tráfico | Controladores remotos |
| 4.11 | Tarjeta Turística | Auditoría de transacciones |
| 4.12 | Dinamización Digital | Auditoría de campañas |
| 4.13 | Red WiFi | Admin de AP y seguridad |

---

## PARTE 5: MANUAL DE MANTENIMIENTO

Directorio: `parte5-manual-mantenimiento/`

Procedimientos de mantenimiento preventivo y correctivo. Incluye calibración de sensores, actualización de firmware, gestión de backups y procedimientos de recuperación ante fallos.

Una sección por cada una de las 13 actuaciones.

| Sección | Actuación | Contenido Clave |
| --- | --- | --- |
| 5.1 | Plataforma de Ciudad Inteligente | Backups y actualizaciones |
| 5.2 | CMS Turístico | Optimización de BD |
| 5.3 | Web de Turismo | SSL/TLS y parches |
| 5.4 | Apps de Turismo | Análisis de crashes |
| 5.5 | Cartelería Digital | Limpieza y firmware |
| 5.6 | Señalización Turística | Reemplazo de baterías |
| 5.7 | Flujos Turísticos | Calibración de sensores |
| 5.8 | Sensorización Ambiental | Calibración y validación |
| 5.9 | Aparcamientos | Validación de ocupación |
| 5.10 | Control de Tráfico | Actualización de firmware |
| 5.11 | Tarjeta Turística | Auditoría de integridad |
| 5.12 | Dinamización Digital | Auditoría de datos |
| 5.13 | Red WiFi | Firmware de AP y cobertura |

---

## PARTE 6: PLAN DE FORMACIÓN

Directorio: `parte6-plan-formacion/`

Planes detallados de formación presencial para tres perfiles de usuarios municipales. Cumple con requisitos de Pliego § 12.

### 6.1 Formación para Usuarios Municipales (Editores)

Archivo: `6.1-plan-formacion-usuarios-municipales.md`

Participantes: 5–15 usuarios editores de contenidos.

Duración: aproximadamente 27 horas de formación presencial.

Contenido: Operación básica de las 13 actuaciones, creación y edición de contenidos, consulta de datos.

Evaluación: Pruebas prácticas y autonomía funcional en cada actuación.

### 6.2 Formación para Personal de Mantenimiento

Archivo: `6.2-plan-formacion-personal-mantenimiento.md`

Participantes: 3–8 técnicos de Obras y Servicios.

Duración: aproximadamente 32 horas de formación + práctica supervisada en campo.

Contenido: Mantenimiento preventivo, calibración de sensores, diagnóstico de fallos, procedimientos de seguridad.

Evaluación: Intervenciones de mantenimiento en equipamiento real bajo supervisión.

### 6.3 Formación para Administradores de Sistemas

Archivo: `6.3-plan-formacion-administradores-sistemas.md`

Participantes: 2–4 administradores de sistemas municipales.

Duración: aproximadamente 44 horas de formación + práctica avanzada en sandbox y producción.

Contenido: Administración de BD, seguridad, auditoría, compliance regulatorio, planificación de capacidad.

Evaluación: Procedimientos completos de administración en entorno de producción.

---

## ANEXOS

### Anexo 1: Procedimientos de Seguridad

Archivo: `anexos/A1-procedimientos-seguridad.md`

Control de acceso físico, políticas de contraseña, gestión de certificados, auditoría de acceso, cumplimiento GDPR.

### Anexo 2: Matriz de Responsabilidades

Archivo: `anexos/A2-matriz-responsabilidades.md`

Roles y responsabilidades por perfil, escalada de incidencias, puntos de contacto.

### Anexo 3: Glosario Técnico

Archivo: `anexos/A3-glosario-tecnico.md`

Términos, acrónimos y definiciones técnicas normalizadas.

### Anexo 4: Referencias Normativas

Archivo: `anexos/A4-referencias-normativas.md`

Normas aplicables: UNE 178104:2017, UNE 178501/178502, GDPR, legislación municipal.

### Anexo 5: Matriz de SLA y Garantía

Archivo: `anexos/A5-matriz-sla-garantia.md`

Tiempos de respuesta por tipo de incidencia, períodos de garantía (2 años mínimo), disponibilidad esperada.

### Anexo 6: Procedimientos de Recuperación ante Desastre

Archivo: `anexos/A6-recuperacion-desastre.md`

Backup y restauración, RTO/RPO por servicio, planes de continuidad de negocio.

### Anexo 7: Historial de Versiones y Cambios

Archivo: `anexos/A7-historial-versiones.md`

Registro de cambios del Manual, versiones de software/hardware, actualizaciones y mejoras.

---

## Completitud del Manual

El Manual cubre los cinco requisitos explícitos del Pliego § 11:

1. **Detalle de Equipamiento:** Parte 1 — Especificaciones completas de hardware.
2. **Detalle de Software:** Parte 2 — Inventario de componentes software instalados.
3. **Manual de Usuario:** Parte 3 — Instrucciones para 13 actuaciones.
4. **Manual de Administración:** Parte 4 — Instrucciones avanzadas para 13 actuaciones.
5. **Manual de Mantenimiento:** Parte 5 — Procedimientos preventivos y correctivos para 13 actuaciones.

Además incluye:

6. **Plan de Formación:** Parte 6 — Cumplimiento de requisitos Pliego § 12.
7. **Anexos de Referencia:** Procedimientos de seguridad, SLAs, glosarios, normativa.

---

## Cómo Usar Este Índice

**Para consultar un procedimiento específico:** Busque la Parte y sección en la tabla anterior y acceda al archivo correspondiente en la carpeta indicada.

**Para entender la estructura general:** Lea esta página como visión general; luego navegue a la Parte específica.

**Para búsqueda terminológica:** Consulte Anexo 3 (Glosario Técnico).

**Para tiempos de respuesta y garantía:** Vea Anexo 5 (Matriz de SLA).

**Para escalada de problemas:** Revise Anexo 2 (Matriz de Responsabilidades).

---

## Períodos de Soporte y Formación

Tras completación de formación inicial (primeras 5 semanas):

**Mes 3:** Sesión presencial de soporte (2 horas) — dudas, casos de uso, mejoras.

**Mes 6:** Sesión presencial de soporte (2 horas) — evaluación de procedimientos, temas avanzados.

**Mes 6 en adelante:** Servicio de mantenimiento y soporte técnico continuo (mínimo 10 años desde recepción final).

---

## Información de Control

**Órgano responsable:** Ayuntamiento de San Lorenzo de El Escorial

**Cumplimiento normativo:** Pliego de Prescripciones Técnicas §§ 11–12

**Versión actual:** 1.0

**Fecha de emisión:** Abril 2026

**Clasificación:** Documento Interno — Uso Municipal

---

# Índice General del Manual del Proyecto

## Plan de Sostenibilidad Turística en Destino — San Lorenzo de El Escorial

**Documento:** Manual del Proyecto  
**Versión:** 1.0  
**Fecha:** Abril 2026  
**Cumple con:** Pliego de Prescripciones Técnicas § 11 (Manual del Proyecto)  
**Destinatario:** Ayuntamiento de San Lorenzo de El Escorial

---

## Estructura General del Manual

Manual del Proyecto (Parte 1–6 + 7 Anexos):
- PARTE 1: DETALLE DE HARDWARE — Componentes, especificaciones, características técnicas
- PARTE 2: DETALLE DE SOFTWARE — Librerías, dependencias, versionado, instrucciones de instalación
- PARTE 3: MANUAL DE INSTRUCCIONES DE USUARIO — 13 secciones (una por actuación) — Operación básica
- PARTE 4: MANUAL DE INSTRUCCIONES DE ADMINISTRACIÓN — 13 secciones (una por actuación) — Gestión avanzada
- PARTE 5: MANUAL DE MANTENIMIENTO — 13 secciones (una por actuación) — Procedimientos preventivos y correctivos
- PARTE 6: PLAN DE FORMACIÓN — 3 perfiles: Usuarios, Técnicos de Mantenimiento, Administradores
- ANEXOS (1–7) — Procedimientos especiales, glosarios, referencias normativas

---

## PARTE 1: DETALLE DE HARDWARE

### 1.1 Plataforma de Ciudad Inteligente (PCI)

**Archivo:** `parte1-hardware/1.1-plataforma-ciudad-inteligente.md`

Descripción de componentes de infraestructura IT:
- Servidores de aplicación
- Infraestructura de almacenamiento
- Sistemas de respaldo y redundancia
- Conectividad de red
- Equipamiento de seguridad perimetral

---

### 1.2–1.5 Actuaciones de Software (CMS, Web, Apps, Cartelería)

**Archivos:** `parte1-hardware/1.2-*.md` a `1.5-*.md`

Equipamiento asociado:

- Servidores web y de aplicación
- CDN y distribución de contenidos
- Almacenamiento de medios

- Infraestructura de apps móviles

---

### 1.6–1.13 Actuaciones de Sensórica e Infraestructura

**Archivos:** `parte1-hardware/1.6-*.md` a `1.13-*.md`


Equipamiento de campo:
- Sensores de ocupación, ambientales, de tráfico
- Dispositivos de señalización (beacons, paneles digitales)
- Infraestructura de comunicación (WiFi, redes de sensores)
- Lectores NFC/RFID para Tarjeta Turística

---

## PARTE 2: DETALLE DE SOFTWARE

### 2.1–2.13 Componentes de Software Instalado

**Archivo:** `parte2-software/software-components.md`


Inventario de:
- Sistemas operativos y versiones
- Plataformas de aplicación (Fastify, Strapi, Node.js)
- Librerías de infraestructura (RabbitMQ, MariaDB, Valkey, Ollama)
- Dependencias de terceros
- Árbol de dependencias y versioning

---

## PARTE 3: MANUAL DE INSTRUCCIONES DE USUARIO

**Directorio:** `parte3-manual-usuario/`

Instrucciones operativas para usuarios municipales editores de contenidos (13 actuaciones):

| # | Sección | Contenido |
| --- | --- | --- |
| 3.1 | Plataforma de Ciudad Inteligente | Acceso a PCI, navegación, permisos básicos |
| 3.2 | Gestor de Contenidos Turísticos | Crear, editar, publicar contenido turístico |
| 3.3 | Renovación de la Web de Turismo | Gestionar páginas, banners, menús web |
| 3.4 | Renovación y Realización de Apps | Gestionar contenido en app móvil |
| 3.5 | Cartelería Digital Centralizada | Programar contenido en pantallas digitales |
| 3.6 | Señalización Turística Urbana Inteligente | Gestionar beacons y puntos de interés |
| 3.7 | Monitorización de Flujos Turísticos | Consultar datos de afluencia en tiempo real |
| 3.8 | Sistema de Sensorización Ambiental | Consultar datos medioambientales |
| 3.9 | Sistema de Información de Aparcamientos | Consultar disponibilidad de plazas |
| 3.10 | Sistema de Control Inteligente del Tráfico | Consultar datos de tráfico y flujos |
| 3.11 | Tarjeta Turística | Gestionar beneficios y descuentos |
| 3.12 | Dinamización e Impulso Digital del Empresariado | Crear campañas y gestionar participación |
| 3.13 | Modernización de la Red WiFi Municipal | Consultar datos de cobertura y uso |

---

## PARTE 4: MANUAL DE INSTRUCCIONES DE ADMINISTRACIÓN

**Directorio:** `parte4-manual-administrador/`

Instrucciones avanzadas para administradores municipales (13 actuaciones):

| # | Sección | Contenido |
| --- | --- | --- |
| 4.1 | Plataforma de Ciudad Inteligente | Gestión de usuarios, roles, permisos, auditoría |
| 4.2 | Gestor de Contenidos Turísticos | Admin de BD, usuarios, flujos de publicación |
| 4.3 | Renovación de la Web de Turismo | Certificados, dominios, escalabilidad |
| 4.4 | Renovación y Realización de Apps | Distribución en app stores, versioning |
| 4.5 | Cartelería Digital Centralizada | Admin remota, actualización firmware |
| 4.6 | Señalización Turística Urbana Inteligente | Sincronización de beacons, usuarios API |
| 4.7 | Monitorización de Flujos Turísticos | Integridad de datos, alertas |
| 4.8 | Sistema de Sensorización Ambiental | Calibración remota, auditoría |
| 4.9 | Sistema de Información de Aparcamientos | Sincronización, validación, análisis |
| 4.10 | Sistema de Control Inteligente del Tráfico | Controladores remotos, planes semafóricos |
| 4.11 | Tarjeta Turística | Auditoría de transacciones, compliance |
| 4.12 | Dinamización e Impulso Digital del Empresariado | Auditoría de campañas, integridad |
| 4.13 | Modernización de la Red WiFi Municipal | Admin de AP, seguridad, monitorización |

---

## PARTE 5: MANUAL DE MANTENIMIENTO

**Directorio:** `parte5-manual-mantenimiento/`

Procedimientos de mantenimiento preventivo y correctivo (13 actuaciones):

| # | Sección | Contenido |
| --- | --- | --- |
| 5.1 | Plataforma de Ciudad Inteligente | Backups, actualizaciones, monitorización |
| 5.2 | Gestor de Contenidos Turísticos | Optimización de BD, limpieza de datos |
| 5.3 | Renovación de la Web de Turismo | SSL/TLS, parches de seguridad |
| 5.4 | Renovación y Realización de Apps | Análisis de crashes, gestión de versiones |
| 5.5 | Cartelería Digital Centralizada | Limpieza, actualizaciones firmware |
| 5.6 | Señalización Turística Urbana Inteligente | Reemplazo de baterías, validación de alcance |
| 5.7 | Monitorización de Flujos Turísticos | Calibración de sensores, auditoría de datos |
| 5.8 | Sistema de Sensorización Ambiental | Calibración, limpieza, validación |
| 5.9 | Sistema de Información de Aparcamientos | Validación de ocupación, recalibración |
| 5.10 | Sistema de Control Inteligente del Tráfico | Firmware, reemplazo de LED |
| 5.11 | Tarjeta Turística | Auditoría de integridad, transacciones |
| 5.12 | Dinamización e Impulso Digital del Empresariado | Auditoría de datos, limpieza |
| 5.13 | Modernización de la Red WiFi Municipal | Firmware de AP, cobertura, site surveys |

---

## PARTE 6: PLAN DE FORMACIÓN

**Directorio:** `parte6-plan-formacion/`

### 6.1 Plan de Formación para Usuarios Municipales (Editores de Contenidos)

**Archivo:** `6.1-plan-formacion-usuarios-municipales.md`

- Perfil de participantes: 5–15 usuarios editores
- Duración: ~27 horas de formación presencial
- Contenidos: Operación básica de las 13 actuaciones
- Evaluación: Pruebas prácticas y autonomía funcional

---

### 6.2 Plan de Formación para Personal de Mantenimiento

**Archivo:** `6.2-plan-formacion-personal-mantenimiento.md`

- Perfil de participantes: 3–8 técnicos de Obras y Servicios
- Duración: ~32 horas de formación + práctica supervisada
- Contenidos: Mantenimiento preventivo, calibración, diagnóstico
- Evaluación: Intervenciones en equipamiento bajo supervisión

---

### 6.3 Plan de Formación para Administradores de Sistemas

**Archivo:** `6.3-plan-formacion-administradores-sistemas.md`

- Perfil de participantes: 2–4 administradores de sistemas
- Duración: ~44 horas de formación + práctica avanzada
- Contenidos: Administración, seguridad, auditoría, compliance
- Evaluación: Procedimientos completos en sandbox y producción

---

## ANEXOS

### Anexo 1: Procedimientos de Seguridad

**Archivo:** `anexos/A1-procedimientos-seguridad.md`

- Control de acceso físico
- Políticas de contraseña
- Gestión de certificados
- Auditoría y cumplimiento GDPR

---

### Anexo 2: Matriz de Responsabilidades

**Archivo:** `anexos/A2-matriz-responsabilidades.md`

- Roles y responsabilidades por perfil
- Escalada de incidencias
- Puntos de contacto

---

### Anexo 3: Glosario Técnico

**Archivo:** `anexos/A3-glosario-tecnico.md`

- Términos y acrónimos utilizados
- Definiciones normalizadas

---

### Anexo 4: Referencias Normativas

**Archivo:** `anexos/A4-referencias-normativas.md`

- UNE 178104:2017 (Plataforma de Ciudad Inteligente)
- UNE 178501/178502 (Destinos Turísticos Inteligentes)
- Normativa de protección de datos (GDPR)
- Legislación municipal aplicable

---

### Anexo 5: Matriz de SLA y Garantía

**Archivo:** `anexos/A5-matriz-sla-garantia.md`

- Tiempos de respuesta por tipo de incidencia
- Períodos de garantía (2 años mínimo)
- Disponibilidad esperada

---

### Anexo 6: Procedimientos de Recuperación ante Desastre

**Archivo:** `anexos/A6-recuperacion-desastre.md`

- Procedimientos de backup y restauración
- RTO/RPO por servicio
- Planes de continuidad

---

### Anexo 7: Historial de Versiones y Cambios

**Archivo:** `anexos/A7-historial-versiones.md`

- Registro de cambios del Manual
- Versiones de software/hardware
- Actualizaciones y mejoras

---

## Notas sobre la Estructura

1. **Completitud:** El Manual cubre los 5 requisitos del Pliego §11:
   - ✅ Detalle de equipamiento
   - ✅ Detalle de software
   - ✅ Manual de instrucciones de usuario
   - ✅ Manual de instrucciones de administración
   - ✅ Manual de mantenimiento

2. **Formación:** Integrada en Parte 6 (Plan de Formación), cumpliendo Pliego §12.

3. **Garantía y Mantenimiento:** Referenciados en Partes 5 y Anexos, cumpliendo Pliego §§ 9–10.

4. **Trazabilidad:** Cada sección menciona referencia a Pliego §6.x (actuaciones) y apartados relevantes.

---

## Cómo usar este Índice

- Use este documento como referencia de estructura global.
- Navegue a la carpeta y archivo específico para consultar procedimientos detallados.
- Busque en el Anexo 3 (Glosario) si encuentra términos desconocidos.
- Consulte Anexo 5 (SLA) para tiempos de respuesta y garantía.
- Escale según Anexo 2 (Matriz de Responsabilidades) si requiere soporte técnico.

---


## Información de Contacto y Soporte

Periodos de soporte presencial tras finalización de formación:
- **Mes 3:** Sesión de soporte presencial (2 horas)
- **Mes 6:** Sesión de soporte presencial (2 horas)

Servicio de mantenimiento y soporte técnico: **10 años mínimos desde la recepción.**

---

**Documento controlado por:** Ayuntamiento de San Lorenzo de El Escorial  
**Cumplimiento:** Pliego de Prescripciones Técnicas § 11  
**Versión actual:** 1.0 | Abril 2026
