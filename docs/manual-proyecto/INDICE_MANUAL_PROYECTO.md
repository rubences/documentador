# Manual del Proyecto — Plan de Sostenibilidad Turística en Destino
## Ayuntamiento de San Lorenzo de El Escorial
### Eje de Transición Digital · Fondos NextGenerationEU / PRTR

> **Nota general:** Este esqueleto documental ha sido generado por trazabilidad directa con el
> Pliego de Prescripciones Técnicas (junio 2025, 154 pp.). Cada apartado indica la sección del
> Pliego que lo origina. El contenido marcado como *(Nota: ...)* deberá ser redactado por el
> adjudicatario al finalizar los trabajos (§11 del Pliego).

---

## ESTRUCTURA GENERAL DEL MANUAL

El apartado **11 del Pliego** establece que el Manual del Proyecto debe contener cinco
dimensiones documentales obligatorias, aplicadas a cada una de las 13 actuaciones:

| Dimensión | Abreviatura | Obligatoriedad |
|---|---|---|
| Detalle de cada equipamiento (hardware) | HW | Obligatorio |
| Detalle de cada elemento software | SW | Obligatorio |
| Manual de instrucciones de usuario | MU | Obligatorio |
| Manual de instrucciones de administración | MA | Obligatorio |
| Manual de mantenimiento | MM | Obligatorio (remite al §10) |

---

## ÍNDICE ESTRUCTURADO

---

# PARTE 0 — INTRODUCCIÓN Y MARCO DEL PROYECTO

## 0.1 Objeto del Manual

*(Nota: Identificar el contrato (referencia, fecha de adjudicación), el adjudicatario, el técnico
municipal responsable, y el número de expediente del PSTD. Citar el artículo 11 del Pliego como
fundamento legal de este entregable.)*

## 0.2 Alcance y estructura del documento

*(Nota: Describir cómo se organiza el Manual en cinco secciones transversales y 13 actuaciones;
indicar la versión del documento, fecha de entrega y procedimiento de actualización.)*

## 0.3 Marco normativo aplicable

*(Nota: Reproducir las normativas del §14 del Pliego que afectan directamente a los sistemas
entregados: UNE 178104, UNE 178502, UNE 178201, RGPD, ENS, Ley 9/2017 LCSP, REBT,
Reglamento UE 2021/241, Orden HFP/1030/2021, etc.)*

## 0.4 Acrónimos y glosario técnico

*(Nota: Definir todos los acrónimos usados a lo largo del Manual: PCI, CMS, ANPR, BLE, NFC,
DTI, PSTD, PRTR, DNSH, ENS, PoE, SSID, etc.)*

## 0.5 Datos de contacto del servicio de soporte post-garantía

*(Nota: Según §10.1 del Pliego, el adjudicatario deberá mantener soporte durante 10 años tras la
instalación. Incluir: número de teléfono de atención (horario mínimo 9–17 h laborables), correo
de soporte, SLA de resolución — máximo 3 días laborables para incidencias — y datos de la
persona de contacto asignada.)*

---

# PARTE 1 — DETALLE DE EQUIPAMIENTO (HARDWARE)

*(Origen normativo: §11, punto 1º del Pliego — "Detalle de cada equipamiento: fabricante,
modelo, características, mantenimiento necesario, instrucciones de operación y de uso".)*

---

## 1.1 Actuación 1: Plataforma de Ciudad Inteligente (PCI)

*(Origen: §6.1.1 y §6.1.3 del Pliego — "Los servidores hardware serán 2, replicados en espejo";
"Se proveerá de un SAI enrackable"; "2 GPU mínimas Nvidia serie RTX 5000".)*

### 1.1.1 Servidores principales (x2, configuración espejo HA)

*(Nota: Documentar fabricante y modelo exacto de cada servidor. Registrar para cada unidad:
número de serie, procesadores instalados (mínimo: doble Intel Xeon Silver 16 cores), RAM
(mínimo 256 GB), almacenamiento NVMe (mínimo 1 TB) y almacenamiento SATA III SSD
(mínimo 20 TB), controladora RAID, formato rack (máximo 2U), puertos Ethernet 2xGbE,
sistema operativo instalado. Incluir copia del albarán de entrega.)*

### 1.1.2 SAI (Sistema de Alimentación Ininterrumpida)

*(Nota: Fabricante, modelo, capacidad (mínimo 6.000 VA), formato enrackable, tiempo de
autonomía estimado bajo carga nominal, procedimiento de prueba de batería anual.)*

### 1.1.3 Unidades de Procesamiento GPU (x2 mínimo)

*(Nota: Fabricante y modelo exacto (mínimo Nvidia RTX 5000 o equivalente serie), memoria
GDDR6 (mínimo 32 GB por unidad), driver instalado, compatibilidad con motor IA local
(Ollama/LM Studio u otro elegido). Indicar si se instala un tercer servidor para BBDD según
opción valorable del §6.1.3.)*

### 1.1.4 Infraestructura de red del CPD municipal

*(Nota: Describir switches, patch panels y cableado instalados en el centro de datos del
Ayuntamiento para dar conectividad a los servidores de la PCI. Incluir diagrama de rack.)*

---

## 1.2 Actuación 2: Gestor de Contenidos Turísticos (CMS)

*(Origen: §6.2.1 — "Esta actuación constará del software necesario [...] sin hardware propio
adicional a la PCI.")*

### 1.2.1 Ausencia de hardware específico adicional

*(Nota: Confirmar que la actuación se ejecuta íntegramente sobre los servidores de la PCI
(§1.1). Si se instala algún componente hardware auxiliar (p.ej. balanceador físico), documentarlo
aquí con fabricante, modelo y función.)*

---

## 1.3 Actuación 3: Renovación de la Web de Turismo

*(Origen: §6.3 — Solución web alojada en infraestructura PCI o hosting externo si aplica.)*

### 1.3.1 Infraestructura de alojamiento web

*(Nota: Especificar si la web se aloja en los servidores de la PCI o en hosting externo. Si es
externo, documentar proveedor, tipo de plan contratado, SLA de disponibilidad y renovación
de licencias. Si es interno, referenciar al apartado §1.1.)*

---

## 1.4 Actuación 4: Renovación y Realización de App's de Turismo

*(Origen: §6.4 — Aplicación móvil, sin hardware propio. El backend se ejecuta sobre PCI.)*

### 1.4.1 Infraestructura de publicación en stores

*(Nota: Documentar las cuentas de desarrollador en Apple App Store y Google Play Store
utilizadas para publicar la app (titularidad debe quedar en el Ayuntamiento), así como los
certificados de firma de la aplicación y sus fechas de caducidad.)*

---

## 1.5 Actuación 5: Cartelería Digital Centralizada

*(Origen: §6.5.2 del Pliego — "3 paneles informativos exteriores y 5 interiores como mínimo".)*

### 1.5.1 Paneles informativos exteriores (mínimo 3 unidades)

*(Nota: Para cada panel documentar: fabricante y modelo, tecnología LED, dimensiones
(1,5 x 1 m), pixel pitch (3 mm), resolución (mínimo 1920x1080), RAM (mínimo 2 GB),
almacenamiento (mínimo 16 GB), luminosidad (mínimo 7.500 nits), clasificación IP (IP65
frontal / IP54 trasera), ángulo de visión (140° H / 140° V), tipo de estructura monoposte
galvanizado, sistema de cimentación, protecciones eléctricas (magnetotérmicos + diferencial +
sobretensiones), UPS integrado, conectividad (LAN / 4G LTE). Indicar ubicación física
exacta de cada panel (M600/Montescorial, Carretera Estación, Reina Victoria + 2 valorables).)*

### 1.5.2 Paneles informativos interiores (mínimo 5 unidades)

*(Nota: Para cada panel: fabricante y modelo, tecnología (IPS o LED), tamaño, luminosidad
(mínimo 4.000 nits), vida útil (mínimo 40.000 h), alimentación 220V/50Hz, UPS integrado,
conectividad LAN, software de control. Indicar ubicación física: Ayuntamiento, Polideportivo,
Casa de Cultura, Juventud, Escuela de Música.)*

### 1.5.3 Sistema de cableado, alimentación y obra civil asociada

*(Nota: Describir los trabajos de obra civil realizados (canalización, zanjas, puntos de luz),
materiales y empresa subcontratada si aplica. Incluir planos as-built de instalación.)*

---

## 1.6 Actuación 6: Señalización Turística Urbana Inteligente

*(Origen: §6.6.1 y §6.6.2 — "40 puntos en Ruta siglo XVI y Ruta siglo XVIII"; tótems con
Beacons BLE, NFC, QR, Braille y antigrafiti.)*

### 1.6.1 Tótems y señales físicas (mínimo 40 unidades)

*(Nota: Documentar fabricante, modelo y tipo para cada señal (bienvenida en 3 accesos,
interpretativas, orientación peatonal). Material (acero inoxidable + composite), tratamiento
anticorrosión y antigrafiti, dimensiones, opciones de Braille y relieve. Indicar coordenadas GPS
de cada punto de instalación conforme a las 2 rutas turísticas del portal sanlorenzoturismo.es.)*

### 1.6.2 Beacons BLE (unidades embebidas en tótems)

*(Nota: Fabricante y modelo exacto, tecnología Bluetooth Low Energy, rango configurable
10–50 m, autonomía de batería (2–5 años), compatibilidad iOS/Android. Incluir procedimiento
de reemplazo de batería y calendario estimado de sustitución por punto.)*

### 1.6.3 Chips NFC pasivos

*(Nota: Fabricante, estándar NFC (ISO 14443 o ISO 15693), capacidad de memoria, proceso de
programación del chip y herramienta utilizada para su gestión.)*

### 1.6.4 Códigos QR estáticos y dinámicos

*(Nota: Herramienta/plataforma usada para generar y gestionar los QR dinámicos (sin cambio
físico), URL base del servicio, política de caducidad de QR y procedimiento de actualización
de destino.)*

---

## 1.7 Actuación 7: Monitorización de Flujos Turísticos

*(Origen: §6.7.2 — Tipo A: cámaras en altura para grandes superficies; Tipo B: cámaras de
conteo lineal a baja altura. Mínimo 8 puntos de control.)*

### 1.7.1 Cámaras de aforo Tipo A (grandes superficies — mínimo 3 ubicaciones)

*(Nota: Fabricante y modelo, sensor de imagen (CMOS), resolución, ángulo de visión, capacidad
de identificación de trayectorias sin reconocimiento facial, método de montaje en altura,
protocolo de comunicación (PoE, WiFi, 4G), IP y temperatura de operación. Ubicaciones:
Jardines del Príncipe (o equivalente), Plaza de la Constitución, Plaza de Jacinto Benavente
(valorable).)*

### 1.7.2 Cámaras de conteo Tipo B (calles — mínimo 5 ubicaciones)

*(Nota: Fabricante y modelo, doble lente CMOS 1/2.8", resolución mínima 4 MP por lente,
ángulo de visión 98° H / 52° V, tecnología de conteo 3D depth para diferenciación
personas/objetos, precisión 98%, conteo bidireccional simultáneo, conectividad PoE. Indicar
ubicación exacta: Plaza San Lorenzo, Juan de Leyva, Floridablanca, Calleja Larga, cruce REy.)*

### 1.7.3 Unidad de procesamiento local (NVR/servidor de aforo)

*(Nota: Fabricante, modelo, CPU, RAM y almacenamiento del servidor local donde se procesan
los datos de las cámaras. Indicar si se trata de un NVR dedicado o un servicio desplegado en
los servidores de la PCI.)*

### 1.7.4 Infraestructura de red y alimentación

*(Nota: Switches PoE instalados, canalización de cableado, puntos de alimentación eléctrica
en cada emplazamiento. Obra civil asociada.)*

---

## 1.8 Actuación 8: Sistema de Sensorización Ambiental

*(Origen: §6.8.2 — 2 estaciones de sensores ambientales (Zaburdón + Plaza Constitución);
opción valorable: estación meteorológica.)*

### 1.8.1 Estaciones de sensores ambientales (2 unidades)

*(Nota: Fabricante y modelo de cada estación. Documentar para cada parámetro medido el
sensor instalado, su rango de operación, precisión y resolución según especificaciones del
Pliego: ruido acústico; CO (0–1000 ppm ±5 ppm); SO2; NO2; O3 (0–130 µg/m³ ±15 ppb);
PM2.5 y PM10 (0–1000 µg/m³ ±15%); temperatura (−50 a +70 °C ±0,5 °C); humedad
(0–100% ±2%). Indicar protección antivandálica, IP, rango de temperatura de operación,
tipo de soporte/mástil.)*

### 1.8.2 Concentrador de datos (edge gateway por estación)

*(Nota: Fabricante y modelo del concentrador edge, CPU, memoria, almacenamiento local
mínimo (memoria de respaldo 2 días sin alimentación eléctrica según §6.8.2 del Pliego),
conectividad (LAN/WiFi/4G), reloj en tiempo real (RTC), protocolo de envío a PCI.)*

### 1.8.3 Estación meteorológica (opción valorable)

*(Nota: Si fue ofertada y adjudicada, documentar: fabricante, modelo, variables medidas
(temperatura, humedad, viento velocidad/dirección, precipitación, presión atmosférica),
consola receptora, longitud de cableado entre sensores y consola (30 m estándar), mástil,
anclaje, certificación OMM si aplica.)*

### 1.8.4 Infraestructura de soporte, mástiles y obra civil

*(Nota: Describir los soportes estructurales instalados en Zaburdón (exterior Polideportivo) y
Plaza de la Constitución (exterior Ayuntamiento), tipo de anclaje, cumplimiento normativa
eléctrica (REBT), permisos de obra civil obtenidos.)*

---

## 1.9 Actuación 9: Sistema de Información de Aparcamientos Públicos

*(Origen: §6.9.3 — Paneles LED, sensores de conteo, sistema informático de control; 2
aparcamientos subterráneos: Plaza Constitución (1 entrada) y Calle del Rey/Parque Felipe II
(2 entradas).)*

### 1.9.1 Paneles informativos de tráfico rodado (mínimo 3 unidades exteriores)

*(Nota: Fabricante y modelo de cada panel LED. Documentar: dimensiones (100 x 30 cm,
profundidad 17 cm), altura mínima dígitos (20 cm), pixel pitch 4, luminosidad mínima
5.000 nits luz blanca, IP65, temperatura de trabajo (−20 a +55 °C), ángulo apertura visión
≥120°, ciclos encendido mínimos 100.000, conectividad 4G/LTE, baterías de respaldo para
suministro en alumbrado discontinuo, mástil con diseño conforme a cartelería municipal
existente. Indicar ubicación de cada panel.)*

### 1.9.2 Sensores de conteo de vehículos

*(Nota: Indicar tecnología elegida: lazos de inducción magnética (incluir trabajos de fresado
y remate asfáltico) o cámaras frontales en entradas/salidas. Para lazos: fabricante, modelo del
detector, tipo de comunicación inalámbrica con equipo recolector. Para cámaras: resolución,
IP, montaje. Documentar las 3 bocas de acceso: 1 entrada Plaza Constitución + 2 entradas
Calle del Rey (calle Madre Carmen Salles).)*

### 1.9.3 Sistema informático de control (servidor/concentrador)

*(Nota: Fabricante y modelo del equipo de control central, conectividad 4G al backend,
protocolo de cifrado y firma digital de comunicaciones (§6.9.3 del Pliego — "protegida y
encriptada con sistema de firma digital"), alimentación eléctrica continua desde el
aparcamiento.)*

### 1.9.4 Cableado, canalización y obra civil

*(Nota: Describir trabajos de instalación interior en cada aparcamiento subterráneo, tipo de
canalización, materiales de fijación en acera para mástiles de paneles.)*

---

## 1.10 Actuación 10: Sistema de Control Inteligente del Tráfico

*(Origen: §6.10.1 — "50 cámaras ANPR de alta resolución; servidor local; almacenamiento
masivo; panel de visionado; sistemas de medición de velocidad". Centralizado en Policía Local.)*

### 1.10.1 Cámaras ANPR de alta resolución (mínimo 50 unidades)

*(Nota: Fabricante y modelo de las cámaras. Documentar para cada unidad: resolución,
sensor CMOS, velocidad máxima de lectura de matrícula, IR activo/pasivo, IP (mínimo IP66),
temperatura de operación, soporte de instalación (báculo, fachada), alimentación (continua o
alumbrado + batería; valorar apoyo solar según §6.10.5). Indicar las ubicaciones exactas de las
50+ cámaras conforme al listado de §6.10.5: accesos M-600, CHA, vías interiores, Plaza
Constitución, etc.)*

### 1.10.2 Servidor local de procesamiento ANPR

*(Nota: Fabricante, modelo, CPU, RAM, almacenamiento (suficiente para albergar imágenes y
datos según política de retención definida en ENS). Ubicación física: dependencias Policía
Local. Conectividad con PCI.)*

### 1.10.3 Solución de almacenamiento masivo (NAS/SAN)

*(Nota: Fabricante, modelo, capacidad total, tipo RAID, interfaces de conexión, política de
retención de imágenes definida conforme a RGPD y ENS.)*

### 1.10.4 Panel de visionado (sala Policía Local)

*(Nota: Fabricante, modelo y número de monitores del panel de visionado. Resolución,
tamaño, distribución de pantallas, controlador de videowall si aplica.)*

### 1.10.5 Sistemas de medición de velocidad (opción valorable)

*(Nota: Si fue adjudicado, fabricante, modelo, ubicaciones, homologación DGT, comunicación
con servidor ANPR.)*

### 1.10.6 Infraestructura de alimentación y comunicaciones

*(Nota: Describir la solución de alimentación de cada cámara (continua/alumbrado/solar+batería),
canalización de cableado o solución inalámbrica, switch/concentrador de campo.)*

---

## 1.11 Actuación 11: Tarjeta Turística de San Lorenzo de El Escorial

*(Origen: §6.11.3 apartado A — Hardware: impresoras de grabación, tablets Android NFC,
impresoras térmicas de tickets, soportes de sobremesa, tarjetas Mifare Plus EV1.)*

### 1.11.1 Impresoras de grabación de tarjetas (2 unidades)

*(Nota: Fabricante y modelo de cada impresora de tarjetas plásticas, tecnología de grabación
(transferencia térmica, retransferencia), compatibilidad con estándar Mifare Plus EV1 /
ISO 14443, capacidad de estampado fotográfico a color, grabación de chip, capacidad de
almacenamiento de certificado digital.)*

### 1.11.2 Tablets de validación con NFC (número según propuesta)

*(Nota: Fabricante y modelo, procesador >1 GHz quad-core, RAM ≥1,5 GB, lector NFC
integrado, conectividad WiFi + 4G, pantalla 8 pulgadas, IP67, protección antigolpes,
Android 4.4 o superior. Indicar número total de unidades suministradas y su ubicación o
distribución.)*

### 1.11.3 Impresoras térmicas de tickets (por tablet/puesto)

*(Nota: Fabricante, modelo, ancho de papel (58 mm), conectividad Bluetooth, autonomía de
batería.)*

### 1.11.4 Soportes de sobremesa (por puesto)

*(Nota: Material, diseño compacto/resistente, capacidad de alojamiento de tablet + impresora,
sistema de carga con carcasa.)*

### 1.11.5 Tarjetas Mifare Plus EV1 (suministro inicial: 2.000 unidades)

*(Nota: Fabricante, referencia de producto, chip de proximidad sin contacto ISO 14443,
capacidades criptográficas (AES 128-bit), posibilidad de almacenamiento de certificado
digital, personalización gráfica (foto a color, número identificativo, identidad gráfica
municipal). Indicar si se suministra máquina automática de expedición de tarjetas (opción
valorable §6.11.3).)*

### 1.11.6 Máquina automática de expedición (opción valorable)

*(Nota: Si fue adjudicada, documentar fabricante, modelo, ubicación, conectividad, interfaz
de usuario, pasarela de pago integrada.)*

---

## 1.12 Actuación 12: Dinamización e Impulso Digital y Sostenible del Empresariado

*(Origen: §6.12.3 — "Se deberá instalar un sistema de WiFi pública en al menos 2
establecimientos." Hardware menor asociado a la actuación de dinamización.)*

### 1.12.1 Puntos de acceso WiFi en establecimientos participantes (mínimo 2)

*(Nota: Fabricante y modelo de los access points instalados en los establecimientos comerciales
y hosteleros participantes en el programa de dinamización digital. Indicar nombre del
establecimiento, dirección, número de APs, configuración SSID, protocolo de seguridad.)*

### 1.12.2 Dispositivos de apoyo a la formación (si aplica)

*(Nota: Si el adjudicatario proporcionó tablets, pantallas u otro hardware para las sesiones
formativas presenciales, documentarlos aquí con fabricante, modelo y destino final tras
la formación.)*

---

## 1.13 Actuación 13: Modernización y Ampliación de la Red WiFi Municipal

*(Origen: §6.13.3 y §6.13.5 — Reemplazo de 34 puntos existentes + nuevos puntos, Wifi4EU
compatible; cajas exterior, báculo, baterías, protecciones eléctricas.)*

### 1.13.1 Puntos de acceso WiFi nuevos y repuestos (reemplazo de 34 + nuevos)

*(Nota: Fabricante y modelo del access point elegido, estándar WiFi (mínimo WiFi 6 /
802.11ax, Wifi4EU compatible), bandas de frecuencia (2,4 GHz + 5 GHz), potencia de
transmisión, temperatura de operación exterior, IP de protección, formato de montaje
(sobre báculo de farola / en caja exterior / en azotea). Listar los 34 puntos del inventario
actual (§6.13.4) con el tipo de sustitución realizada.)*

### 1.13.2 Controladora/controlador centralizado de red WiFi

*(Nota: Fabricante, modelo, número máximo de APs gestionados, soporte de portal cautivo
multilingüe (castellano + idiomas adicionales), integración con PCI para monitorización de
presencia turística.)*

### 1.13.3 Cortafuegos y filtro de contenidos

*(Nota: Fabricante y modelo del firewall y filtro de contenidos (upgradeados o nuevos
conforme a §6.13.4 que ya incluía cortafuegos existente). Licencias asociadas, política de
filtrado activa.)*

### 1.13.4 Infraestructura eléctrica (baterías, protecciones magnetotérmicas)

*(Nota: Para cada punto de acceso sobre báculo con suministro de alumbrado (discontinuo),
documentar la batería instalada (fabricante, capacidad en Ah, autonomía estimada en horas),
protección magnetotérmica asociada. Listar qué APs disponen de alimentación continua vs.
dependiente de alumbrado.)*

### 1.13.5 Cableado y obra civil

*(Nota: Describir trabajos de zanjado, entubado, conexión de armarios exteriores y puntos de
acceso nuevos. Incluir plano as-built de la red extendida.)*

---

# PARTE 2 — DETALLE DE SOFTWARE

*(Origen normativo: §11, punto 2º del Pliego — "Detalle de cada elemento software: fuente en caso
de software libre, detalle de cada software instalado, árbol de dependencias, mantenimiento
necesario, instrucciones de uso y de administración.")*

---

## 2.1 Actuación 1: Plataforma de Ciudad Inteligente (PCI)

*(Origen: §6.1.3 — Arquitectura multicapa UNE 178104; software libre preferente con licencia GNU;
certificación UNE 178502 y UNE 178104 por entidad ENAC.)*

### 2.1.1 Sistema operativo del servidor

*(Nota: Distribución y versión exacta (Ubuntu Server LTS, RHEL, SUSE, etc.), fecha de soporte
extendido (EOL), procedimiento de actualización de parches de seguridad, repositorios configurados.)*

### 2.1.2 Plataforma de orquestación de contenedores

*(Nota: Nombre y versión (Kubernetes, K3s, Docker Swarm u equivalente de código abierto).
Indicar: repositorio de origen (GitHub/DockerHub), licencia, árbol de dependencias de
imágenes contenedor desplegadas (docker-compose.yml o helm charts), procedure de
actualización de versión.)*

### 2.1.3 Capa de adquisición / interconexión (broker IoT)

*(Nota: Nombre y versión del broker (MQTT — Mosquitto/HiveMQ; AMQP — RabbitMQ;
Kafka u otro). Licencia, repositorio fuente, dependencias. Protocolos soportados según §6.1.3:
REST, SOAP, WebSocket, MQTT, gRPC (valorable), AMQP, Kafka, Webhooks, WebDAV, SFTP.)*

### 2.1.4 Motor de bases de datos

*(Nota: Para cada BBDD instalada documentar: nombre/versión (PostgreSQL, MySQL/MariaDB,
MongoDB, InfluxDB/TimescaleDB, Redis u otro), licencia (GNU/MIT/Apache), repositorio fuente,
árbol de dependencias, versión de driver cliente instalado en la plataforma.)*

### 2.1.5 Motor local de Inteligencia Artificial

*(Nota: Nombre y versión del runtime elegido (Ollama, LM Studio, llama.cpp u otro de código
abierto). Modelos instalados según §6.1.3: Meta Llama 4, Qwen 3, Gemma, OpenAI Whisper.
Para cada modelo: tamaño en GB, licencia (Meta Llama Community, Apache 2.0, etc.),
repositorio fuente (HuggingFace u otro), dependencias CUDA/ROCm.)*

### 2.1.6 Plataforma de Business Intelligence

*(Nota: Nombre y versión (Apache Superset, Metabase, Grafana + Loki u otro). Licencia,
repositorio fuente, dependencias. Compatibilidad PMML (§6.1.3). Procedimiento de exportación
de modelos predictivos.)*

### 2.1.7 Sistema de monitorización y logging

*(Nota: Stack de observabilidad desplegado — Grafana (visualización alertas), Elasticsearch
(logging), y agentes de colección (Logstash, Fluentd, Prometheus u otro). Versiones, licencias,
dependencias.)*

### 2.1.8 Módulo de seguridad y acceso (IAM / VPN)

*(Nota: Solución de autenticación (Keycloak, Authentik u otro — soporte WebAuthN/MFA/OAuth2
según §6.1.3), versión, licencia, árbol de dependencias. Solución VPN para acceso administrativo
(OpenVPN, WireGuard u otro), certificados digitales utilizados.)*

### 2.1.9 Plataforma Open Data (API pública)

*(Nota: Framework de API pública REST (Django REST, FastAPI, Kong u otro), licencia,
dependencias, endpoints publicados, formato de descarga (CSV, JSON, etc.). Compatibilidad
con UNE 178301 Open Data.)*

### 2.1.10 Sistema GIS / cartografía

*(Nota: Solución GIS integrada (GeoServer, MapServer, QGIS Server u otro), versión, licencia,
fuente cartográfica del SIG municipal existente, dependencias de integración.)*

### 2.1.11 Certificaciones UNE obtenidas

*(Nota: Adjuntar copias de los certificados emitidos por entidad inscrita en ENAC para:
UNE 178104:2017 (interoperabilidad PCI) y UNE 178502:2022 (Destinos Turísticos Inteligentes)
según §6.1.3 del Pliego.)*

---

## 2.2 Actuación 2: Gestor de Contenidos Turísticos (CMS)

*(Origen: §6.2.2 y §6.2.3 — "Software modular, escalable, altamente configurable"; software
libre, API REST, Push/Pull, roles y permisos, beacons, cartelería digital.)*

### 2.2.1 Aplicación CMS principal

*(Nota: Nombre y versión del CMS (Drupal, WordPress + headless, Strapi, Directus u otro
software libre). Repositorio fuente (GitHub), rama/tag desplegado, licencia (GPL, MIT, etc.).)*

### 2.2.2 Árbol de dependencias del CMS

*(Nota: Listar todos los módulos/plugins instalados con nombre, versión, licencia y repositorio.
Incluir el fichero package.json / composer.json / requirements.txt según el stack tecnológico.)*

### 2.2.3 API REST y conectores de integración

*(Nota: Documentar los endpoints REST expuestos, autenticación (OAuth2/API Key), endpoints
de integración con PCI, App, señalización digital y cartelería. Incluir especificación OpenAPI
(Swagger) del servicio.)*

### 2.2.4 Sistema de gestión de beacons

*(Nota: Plataforma o módulo utilizado para gestionar los beacons BLE de las señales de la
Actuación 6, configurar mensajes y contenidos asociados. Nombre, versión, licencia, protocolo
de comunicación con los beacons (iBeacon/Eddystone).)*

---

## 2.3 Actuación 3: Renovación de la Web de Turismo

*(Origen: §6.3.2 y §6.3.3 — "Especificaciones frontend"; "Requisitos técnicos específicos".)*

### 2.3.1 Framework frontend

*(Nota: Nombre y versión del framework (React, Vue, Angular, Astro u otro), gestor de paquetes
(npm/pnpm/yarn), versión de Node.js, árbol de dependencias (package.json). Cumplimiento de
normativa de accesibilidad WCAG 2.1 AA obligatoria para la Administración.)*

### 2.3.2 CMS headless o integrado

*(Nota: Si la web consume contenidos del Gestor Turístico (§2.2), documentar la integración API.
Si tiene CMS propio, indicar nombre, versión y licencia.)*

### 2.3.3 Integraciones con otros sistemas

*(Nota: Documentar las integraciones implementadas (§6.3.5 del Pliego): con App turística,
Gestor de Contenidos, PCI, tarjeta turística. Indicar endpoint, protocolo y autenticación de
cada integración.)*

---

## 2.4 Actuación 4: Renovación y Realización de App's de Turismo

*(Origen: §6.4.2 y §6.4.3 — Especificaciones app móvil e integraciones backend.)*

### 2.4.1 Aplicación móvil (iOS + Android)

*(Nota: Framework multiplataforma o nativo usado (Flutter, React Native, Swift/Kotlin nativos),
versión mínima de SO soportada (iOS/Android), repositorio del código fuente. Incluir proceso
de compilación y publicación en stores.)*

### 2.4.2 Backend / API de la app

*(Nota: Stack tecnológico del backend (Node.js, Python/FastAPI, .NET u otro), versión, licencia,
árbol de dependencias. Endpoints documentados (OpenAPI/Swagger). Integración con PCI,
CMS, tarjeta turística y beacons.)*

### 2.4.3 Integración con beacons y funcionalidades de geolocalización

*(Nota: SDK de beacons utilizado, versión, permisos de localización gestionados en la app,
implementación de notificaciones push.)*

---

## 2.5 Actuación 5: Cartelería Digital Centralizada

*(Origen: §6.5.1 — "Software centralizado de gestión de contenidos y monitorización de estado.
El coste de las licencias de software de por vida.")*

### 2.5.1 Software de gestión centralizada (CMS de cartelería / Digital Signage)

*(Nota: Nombre y versión del software Digital Signage elegido (Yodeck, Screenly, Rise Vision u
equivalente). Modalidad de licencia (por vida, perpetua, según §6.5.1), número de licencias,
proveedor, procedimiento de activación y renovación (si aplica). Formatos multimedia
soportados, protocolo de comunicación con los paneles.)*

### 2.5.2 Software embebido en cada panel (firmware)

*(Nota: Versión de firmware de cada panel exterior e interior, procedimiento de actualización
OTA (Over-The-Air), configuración del sistema de control centralizado.)*

---

## 2.6 Actuación 6: Señalización Turística Urbana Inteligente

*(Origen: §6.6.2 — Sistema de gestión de beacons; plataforma online de configuración; QR
dinámicos.)*

### 2.6.1 Plataforma de gestión de beacons

*(Nota: Documentar la plataforma online utilizada para configurar los beacons (Kontakt.io,
Estimote Cloud, solución propia u otra), nombre, versión/plan, URL del panel de administración,
credenciales de acceso almacenadas en gestor de secretos del Ayuntamiento.)*

### 2.6.2 Herramienta de QR dinámicos

*(Nota: Plataforma o solución utilizada para generar y gestionar QR dinámicos (con posibilidad
de cambiar destino sin modificar el código físico). Plan de servicio, propietario del dominio,
SLA de disponibilidad.)*

---

## 2.7 Actuación 7: Monitorización de Flujos Turísticos

*(Origen: §6.7.2 — Software de conteo, mapas de calor, reportes, integración PCI.)*

### 2.7.1 Software de gestión del sistema de aforo

*(Nota: Nombre y versión del software de analítica de flujos. Indicar si es software libre o
propietario. Si propietario: licencia perpetua o de suscripción, número de licencias, proveedor.
Si libre: repositorio fuente, licencia, árbol de dependencias.)*

### 2.7.2 Módulo de integración con PCI

*(Nota: Protocolo y formato de envío de datos de aforo a la Plataforma de Ciudad Inteligente
(REST, MQTT, WebSocket), frecuencia de envío, formato de datos (JSON/CSV), autenticación.)*

---

## 2.8 Actuación 8: Sistema de Sensorización Ambiental

*(Origen: §6.8.3 — "Sistema de gestión y monitorización incluye la programación y procesamiento
en borde de las estaciones.")*

### 2.8.1 Software de gestión y monitorización de sensores (plataforma central)

*(Nota: Nombre y versión del software central de gestión (puede ser un módulo de la PCI o
solución específica). Licencia, repositorio si es software libre, árbol de dependencias.)*

### 2.8.2 Firmware de los concentradores edge

*(Nota: Versión de firmware del gateway edge instalado en cada estación ambiental,
procedimiento de actualización remota, protocolo de envío de datos a la PCI (periodos
configurables según §6.8.2).)*

### 2.8.3 Configuración de umbrales de alerta

*(Nota: Documentar la política de alertas configurada según §6.8.3: umbrales máximo y mínimo
por parámetro (CO, SO2, O3, PM2.5, PM10, temperatura, humedad), zonas fuera de rango,
canales de notificación configurados (email, SMS, plataforma mensajería).)*

---

## 2.9 Actuación 9: Sistema de Información de Aparcamientos Públicos

*(Origen: §6.9.3 — "Sistema informático de control"; "comunicación protegida y encriptada con
sistema de firma digital".)*

### 2.9.1 Sistema informático de control de aparcamientos

*(Nota: Nombre y versión del software de control. Licencia (perpetua según §6.9.3). Módulos:
conteo de vehículos, visualización de plazas libres (verde <80%, naranja 80–90%, rojo >90%),
integración con paneles LED, comunicación 4G con backend, integración con PCI.)*

### 2.9.2 Protocolo de seguridad en comunicaciones

*(Nota: Documentar el sistema de firma digital implementado para autenticar los mensajes entre
los contadores y el sistema de control (según §6.9.3 del Pliego). Certificados utilizados, autoridad
certificadora, periodo de validez y renovación.)*

---

## 2.10 Actuación 10: Sistema de Control Inteligente del Tráfico

*(Origen: §6.10.5 — Software ANPR, conteo, trazabilidad de matrículas, estadísticas, API
abierta para ampliaciones.)*

### 2.10.1 Software de reconocimiento automático de matrículas (ANPR)

*(Nota: Nombre y versión del motor ANPR. Si es propietario: fabricante, número de licencias,
tipo de licencia (perpetua o suscripción). Si incluye componente open source: repositorio y
licencia. Precisión declarada bajo distintas condiciones (noche, lluvia, ángulo). Integración con
bases de datos externas de vehículos (DGT, alertas ITV/seguros) según §6.10.5.)*

### 2.10.2 Software de estadísticas y trazabilidad

*(Nota: Módulo de estadísticas de circulación (conteo por hora/día/mes, tipología de vehículos,
rutas), trazabilidad de matrículas entre cámaras, generación de informes exportables. Acceso
al módulo de trazabilidad restringido a Policía Local con logs de auditoría conforme RGPD.)*

### 2.10.3 API abierta para ampliaciones (incluida en el contrato)

*(Nota: Según §6.10.5 del Pliego — "se proporcionará una API incluida en el precio del contrato
para futuras modificaciones [...] sin necesidad de la empresa adjudicataria". Documentar la
especificación completa de esta API (OpenAPI/Swagger), versión, autenticación y endpoints
disponibles para extensión futura.)*

### 2.10.4 Integración con PCI y gestión de datos personales (RGPD)

*(Nota: Documentar cómo se anonimiza o protege el acceso a matrículas (datos personales) en
cumplimiento del RGPD y el ENS (§6.10.5 del Pliego — "anonimización de datos / control de
acceso a matrículas"). Política de retención de imágenes y datos.)*

---

## 2.11 Actuación 11: Tarjeta Turística de San Lorenzo de El Escorial

*(Origen: §6.11.3 apartado B — Plataforma de gestión, API REST, módulos I–VIII, App móvil,
autenticación 2FA.)*

### 2.11.1 Plataforma de gestión de la Tarjeta Turística

*(Nota: Nombre y versión del software de gestión. Licencia. Documentar los módulos
implementados según §6.11.3-B: I) Consultoría (informe entregado); II) API REST (CRUD
turistas, ciudadanos, servicios, tarjeta virtual); III) Gestión de usuarios (altas/bajas/permisos,
conexión al Padrón Municipal); IV) Gestión de tarjetas (solicitud, duplicado, baja); V) Gestión
de dispositivos (impresoras, validadores, lectores); VI) Módulo de auditoría (trazabilidad ENS);
VII) App web ciudadana; VIII) App móvil iOS+Android.)*

### 2.11.2 Árbol de dependencias del backend

*(Nota: Listar frameworks, librerías y servicios de terceros con nombre, versión y licencia.
Incluir gestor de paquetes usado (pip/npm/composer) y fichero de dependencias generado.)*

### 2.11.3 Pasarela de pago

*(Nota: Proveedor de pasarela de pago designado por el Ayuntamiento, SDK/API utilizado,
versión, certificación PCI-DSS del proveedor. Indicar qué servicios municipales están
habilitados para pago con tarjeta.)*

### 2.11.4 Sistema de autenticación 2FA

*(Nota: Método 2FA implementado (TOTP, WebAuthN, SMS OTP, hardware key). Software/SDK
utilizado, versión, licencia.)*

### 2.11.5 App móvil (iOS + Android)

*(Nota: Framework, versión mínima de SO, publicación en stores (cuentas de desarrollador del
Ayuntamiento), versión actual de la app, changelog. Funcionalidades equivalentes a tarjeta física,
compatibilidad con dispositivos sin NFC, interoperabilidad con plataforma de gestión.)*

---

## 2.12 Actuación 12: Dinamización e Impulso Digital

*(Origen: §6.12.3 — Autodiagnósticos de calidad, plataforma de formación, soluciones
tecnológicas para empresas (reservas, encuestas, cartas digitales, etc.).)*

### 2.12.1 Herramienta de autodiagnóstico de calidad

*(Nota: Plataforma o sistema utilizado para implementar los ≥30 autodiagnósticos de calidad
del empresariado (basado en modelo SEGITTUR o equivalente). Nombre, versión, licencia, URL
del sistema, datos de acceso.)*

### 2.12.2 Soluciones tecnológicas implantadas en establecimientos

*(Nota: Para cada solución tecnológica desplegada en empresas (reservas online, cartas
digitales, gestión medioambiental, encuestas a turistas, paquetización de productos): nombre del
software, versión, licencia, establecimiento donde se implantó, formación recibida. Mínimo:
documentar cada una de las empresas de las ≥30 adheridas al programa.)*

---

## 2.13 Actuación 13: Modernización y Ampliación de la Red WiFi Municipal

*(Origen: §6.13.3 y §6.13.5 — Portal cautivo, controladora WiFi, integración PCI.)*

### 2.13.1 Firmware de los access points

*(Nota: Versión de firmware instalado en todos los APs (nuevos y repuestos). Fabricante,
plataforma de actualización OTA, procedimiento de actualización masiva, política de gestión
de vulnerabilidades.)*

### 2.13.2 Controladora/plataforma de gestión WiFi centralizada

*(Nota: Nombre y versión del software de gestión de red WiFi (UniFi Controller, Cisco DNA,
Aruba Central u otro). Licencia, árbol de dependencias. Configuración de SSIDs: SSID pública
(Wifi4EU) + SSID privada municipal.)*

### 2.13.3 Portal cautivo

*(Nota: Software del portal cautivo (pfSense, Coova-Chilli, solución del fabricante u otro),
versión, idiomas disponibles (castellano + otros según §6.13.4), sistema de autenticación
(usuario/contraseña, redes sociales, Wifi4EU), licencia, árbol de dependencias.)*

### 2.13.4 Módulo de integración con PCI para monitorización de turistas

*(Nota: Documentar cómo la red WiFi envía datos anonimizados de presencia/ocupación de
turistas a la PCI. Protocolo (SNMP, REST, Syslog), formato de datos, frecuencia de envío,
anonimización conforme RGPD.)*

---

# PARTE 3 — MANUAL DE INSTRUCCIONES DE USUARIO

*(Origen normativo: §11, punto 3º del Pliego — "Manual de instrucciones de usuario: compendio
de las instrucciones para usuarios de todos los elementos." Perfil de usuario según §12 del
Pliego: usuarios municipales con capacidad de edición.)*

---

## 3.1 Guía de usuario de la Plataforma de Ciudad Inteligente (PCI)

*(Nota: Instrucciones para usuarios municipales con rol de edición/consulta. Describir cómo
acceder a la consola web de la PCI (URL, VPN requerida, primer acceso, recuperación de
contraseña). Uso del cuadro de mando: filtros, visualizaciones, exportación de informes.
Configuración de alertas. Acceso a Open Data. Basado en §6.1.3-E y §6.1.4 del Pliego.)*

## 3.2 Guía de usuario del Gestor de Contenidos Turísticos (CMS)

*(Nota: Instrucciones para editores de contenido: creación y edición de artículos, eventos,
noticias y puntos de interés. Carga de imágenes/vídeo, georreferenciación en mapa, sistema de
etiquetas. Proceso de publicación/despublicación. Gestión de agenda. Basado en §6.2.2 del Pliego.)*

## 3.3 Guía de usuario de la Web de Turismo

*(Nota: Instrucciones para editores web con acceso al CMS de la web turística. Actualización de
contenidos, gestión de páginas, integración con CMS turístico. Basado en §6.3 del Pliego.)*

## 3.4 Guía de usuario de la App de Turismo (perspectiva del gestor municipal)

*(Nota: Instrucciones para el gestor municipal que actualiza contenidos en la app a través del
CMS. Publicación de notificaciones push, actualización de rutas. Basado en §6.4 del Pliego.)*

## 3.5 Guía de usuario del sistema de Cartelería Digital

*(Nota: Instrucciones para el operador municipal que programa contenidos en los paneles:
carga de multimedia, programación de listas de reproducción, asignación por panel, franjas
horarias y perfiles de contenido. Basado en §6.5.1 del Pliego.)*

## 3.6 Guía de usuario del sistema de Señalización Turística (beacons y QR)

*(Nota: Instrucciones para el gestor que actualiza contenidos asociados a los puntos de
señalización: cambio de destino de QR dinámicos, configuración de mensajes de beacons,
gestión de contenidos multilingüe por punto de señal. Basado en §6.6.2 del Pliego.)*

## 3.7 Guía de usuario del sistema de Monitorización de Flujos Turísticos

*(Nota: Instrucciones para el técnico municipal: consulta de aforos en tiempo real, generación
de informes diarios/semanales/mensuales, consulta de mapas de calor, exportación de datos.
Configuración de alertas de aforo máximo. Basado en §6.7.2 del Pliego.)*

## 3.8 Guía de usuario del sistema de Sensorización Ambiental

*(Nota: Instrucciones para el técnico ambiental: consulta de niveles de contaminación en
tiempo real, historial de datos, generación de informes interactivos, consulta de alertas y
registro de actuaciones. Basado en §6.8.3 del Pliego.)*

## 3.9 Guía de usuario del sistema de Aparcamientos

*(Nota: Instrucciones para el técnico municipal que supervisa el sistema: consulta del estado
de ocupación en tiempo real por aparcamiento, registro de incidencias, generación de reportes
de ocupación. Basado en §6.9 del Pliego.)*

## 3.10 Guía de usuario del sistema de Control de Tráfico

*(Nota: Instrucciones para los agentes de la Policía Local: acceso al panel de visionado,
consulta de imágenes de cámaras, búsqueda de matrículas, consulta de alertas (vehículos en
búsqueda, ITV caducada, seguro), seguimiento de trayectoria de vehículo sospechoso.
Generación de estadísticas. Basado en §6.10.1 y §6.10.5 del Pliego.)*

## 3.11 Guía de usuario de la Tarjeta Turística (personal de atención al ciudadano)

*(Nota: Instrucciones para el personal de oficina que atiende a ciudadanos y turistas: alta de
titulares, solicitud de tarjeta física, carga de servicios, validación de tarjeta con tablet NFC,
cobro con pasarela de pago, gestión de incidencias (pérdida, robo, renovación). Basado en
§6.11.3-B módulos III, IV, V del Pliego.)*

## 3.12 Guía de usuario para empresas (Dinamización Digital)

*(Nota: Instrucciones básicas para los empresarios participantes en el programa: uso de la
herramienta de autodiagnóstico, acceso a las soluciones tecnológicas implantadas (reservas,
cartas digitales, encuestas). Basado en §6.12.3 del Pliego.)*

## 3.13 Guía de usuario de la Red WiFi Municipal (ciudadanos y turistas)

*(Nota: Instrucciones de conexión al portal cautivo Wifi municipal para visitantes: SSID a
seleccionar, proceso de registro/autenticación en el portal cautivo, idiomas disponibles,
condiciones de uso. Basado en §6.13.4 del Pliego.)*

---

# PARTE 4 — MANUAL DE INSTRUCCIONES DE ADMINISTRACIÓN

*(Origen normativo: §11, punto 4º del Pliego — "Manual de instrucciones de administración:
compendio de las instrucciones para administradores de todos los elementos." Perfil según §12
del Pliego: usuarios administradores de sistemas.)*

---

## 4.1 Administración de la Plataforma de Ciudad Inteligente (PCI)

*(Nota: Instrucciones para el administrador de sistemas: gestión del clúster de contenedores
(inicio/parada de pods, escalado horizontal), gestión de usuarios y roles en la plataforma IAM,
configuración de VPN para acceso administrativo (§6.1.3-D), gestión de certificados TLS,
administración de bases de datos (backup, restore, vacuum), gestión del motor IA (cargar nuevos
modelos, eliminar modelos, ajustar GPU allocation), configuración de nuevas fuentes de datos IoT,
actualización de la plataforma. Acceso exclusivo por VPN con certificado digital.)*

## 4.2 Administración del Gestor de Contenidos Turísticos

*(Nota: Instrucciones para el admin del CMS: gestión de usuarios y roles (editor, autor, administrador),
creación de taxonomías y tipos de contenido, configuración de integraciones con PCI y App,
gestión de caché, actualización de módulos/plugins, backup de BBDD, gestión de medios, configuración
del API REST (tokens de autenticación).)*

## 4.3 Administración de la Web de Turismo

*(Nota: Gestión del servidor web (configuración Nginx/Apache, certificados HTTPS, reglas de
caché y CDN si aplica), despliegue de nuevas versiones del frontend (CI/CD pipeline), gestión
DNS del dominio municipal de turismo, monitorización de uptime y rendimiento.)*

## 4.4 Administración de la App de Turismo

*(Nota: Gestión de las cuentas de desarrollador en App Store/Play Store (acceso, permisos,
firmado de apps), proceso de publicación de nuevas versiones, gestión del backend API (logs,
escalado, actualización de dependencias), gestión de notificaciones push.)*

## 4.5 Administración del sistema de Cartelería Digital

*(Nota: Gestión de usuarios y grupos en el software de Digital Signage, alta/baja de nuevos
paneles, configuración de red de paneles, gestión de licencias (verificación de la licencia de
por vida), gestión de plantillas y listas de reproducción, configuración de reglas de emergencia
(mensajes automáticos de emergencia), monitorización del estado de cada panel.)*

## 4.6 Administración del sistema de Señalización Inteligente

*(Nota: Gestión de la plataforma de beacons: alta/baja de beacons, actualización de firmware
OTA, configuración de parámetros BLE (potencia, intervalo de transmisión, UUID), gestión de
contenidos por perfil de visitante, monitorización del estado de la batería de cada beacon,
programación de sustitución de baterías.)*

## 4.7 Administración del sistema de Monitorización de Flujos Turísticos

*(Nota: Gestión del NVR/servidor de aforo: configuración de cámaras (IP, resolución, zona de
detección), umbral de aforo máximo por punto, configuración de alertas y destinatarios,
exportación de datos históricos, gestión de usuarios del sistema, actualización de firmware de
cámaras.)*

## 4.8 Administración del sistema de Sensorización Ambiental

*(Nota: Configuración de los concentradores edge (periodos de envío de datos, umbrales de
alerta por parámetro según especificaciones del §6.8.3), gestión de la calibración de sensores
(procedimiento de calibración en el sistema métrico legal según §6.8.2), actualización de
firmware de estaciones, gestión de usuarios del sistema de monitorización.)*

## 4.9 Administración del sistema de Aparcamientos

*(Nota: Configuración del sistema informático de control: aforos máximos por aparcamiento,
umbrales de color (verde/naranja/rojo), gestión de la conectividad 4G de los paneles,
procedimiento de ajuste manual de conteo en caso de error del sensor, actualización de
firmware de paneles y sensores, gestión de certificados de firma digital para comunicaciones.)*

## 4.10 Administración del sistema de Control de Tráfico

*(Nota: Gestión del servidor ANPR: configuración de cámaras (IP, parámetros de captura,
zona de matrícula), política de retención de datos (RGPD/ENS), gestión de accesos (Policía
Local), auditoría de consultas sobre matrículas (§2.10.4), actualización del software ANPR,
gestión del almacenamiento masivo (alertas de espacio, archivado), integración con bases de
datos externas (DGT), gestión de la API abierta (§2.10.3).)*

## 4.11 Administración de la Tarjeta Turística

*(Nota: Gestión de la plataforma central: configuración de perfiles de servicio disponibles en
la tarjeta, alta/baja de impresoras y terminales de validación, gestión de la pasarela de pago
(configuración de servicios de pago habilitados), administración de la conexión con el Padrón
Municipal, gestión del módulo de auditoría (consulta de logs de trazabilidad según ENS),
actualización del sistema, backup y restore, gestión de certificados 2FA.)*

## 4.12 Administración de las herramientas de Dinamización Digital

*(Nota: Gestión de la plataforma de autodiagnóstico: alta/baja de empresas, visualización de
resultados agregados, exportación de informes, administración de usuarios empresariales,
actualización de los módulos de diagnóstico. Administración de los accesos a soluciones
tecnológicas desplegadas en los establecimientos.)*

## 4.13 Administración de la Red WiFi Municipal

*(Nota: Gestión de la controladora centralizada: alta/baja de APs, actualización masiva de
firmware, configuración de SSIDs y VLANs, gestión del portal cautivo (usuarios registrados,
estadísticas de conexión), gestión del firewall y filtro de contenidos (listas blancas/negras,
actualización de firmas), monitorización de rendimiento y cobertura por zona, gestión de la
integración con PCI para envío de datos de presencia turística.)*

---

# PARTE 5 — MANUAL DE MANTENIMIENTO

*(Origen normativo: §11, punto 5º y §10 completo del Pliego — "Manual de mantenimiento:
manual de todos los mantenimientos que se deben realizar." El Pliego distingue entre:
mantenimiento correctivo (§10.2 — máximo 3 días laborables); mantenimiento perfectivo y
adaptativo (§10.3); y atención al usuario (§10.4 — máximo 3 días laborables). El servicio de
mantenimiento incluye las 10 años siguientes a la instalación con repuestos disponibles.)*

---

## 5.1 Plan de mantenimiento global

### 5.1.1 SLA y compromisos de servicio (§10.1 del Pliego)

*(Nota: Reproducir los compromisos contractuales: disponibilidad del servicio de soporte
(teléfono 9–17 h laborables + correo de soporte), plazo máximo de reparación (3 días
laborables, online o in-situ), disponibilidad de repuestos durante 10 años, coste del
mantenimiento durante garantía (incluido) y post-garantía (opcional Ayuntamiento).)*

### 5.1.2 Clasificación de mantenimientos

*(Nota: Describir los tres tipos de mantenimiento definidos en §10.3 del Pliego:
Perfectivo — nuevas versiones de software, actualizaciones funcionales; Adaptativo — cambios
por normativa legal o evolución tecnológica HW/SW; Correctivo — reparación de averías en
≤3 días laborables.)*

### 5.1.3 Calendario de mantenimientos preventivos

*(Nota: Elaborar una tabla anual con todas las tareas de mantenimiento preventivo de todos
los sistemas, indicando: sistema, tarea, periodicidad (semanal/mensual/trimestral/anual) y
responsable (adjudicatario / personal municipal Obras y Servicios).)*

---

## 5.2 Mantenimiento de la Plataforma de Ciudad Inteligente

*(Nota: Procedimientos de: actualización del sistema operativo (política de parches), renovación
de certificados TLS/VPN, backup y verificación de restauración de BBDD (frecuencia y retención),
actualización de modelos de IA, monitorización de recursos del servidor (CPU/RAM/disco),
prueba de conmutación del servidor espejo HA, mantenimiento del SAI (test de batería anual,
sustitución de baterías según vida útil).)*

## 5.3 Mantenimiento del Gestor de Contenidos y Web de Turismo

*(Nota: Actualización de CMS y plugins (gestión de vulnerabilidades CVE), backup de BBDD
y ficheros, renovación de dominio y certificado SSL de la web, monitorización de uptime,
pruebas de carga periódicas.)*

## 5.4 Mantenimiento de la App de Turismo

*(Nota: Actualización de dependencias del backend y app móvil (gestión de vulnerabilidades),
renovación de certificados de firma de la app en stores, pruebas de regresión antes de
publicar nuevas versiones, monitorización de crash reports.)*

## 5.5 Mantenimiento de la Cartelería Digital

*(Nota: Limpieza de paneles exteriores (periodicidad, productos no abrasivos), verificación
visual de integridad estructural del monoposte, revisión de UPS (test de batería semestral),
actualización de firmware de paneles, verificación de conectividad 4G/LAN, gestión de
licencias del software de Digital Signage.)*

## 5.6 Mantenimiento de la Señalización Turística Inteligente

*(Nota: Inspección visual de tótems y señales (periodicidad trimestral): estado del acero y
composite, ausencia de grafiti (protocolo de limpieza), legibilidad de QR y NFC. Sustitución
de baterías de beacons según calendario por punto (vida útil 2–5 años). Actualización de
firmware de beacons OTA. Revisión de QR dinámicos — accesibilidad de URLs destino.)*

## 5.7 Mantenimiento del sistema de Monitorización de Flujos Turísticos

*(Nota: Limpieza de ópticas de las cámaras (periodicidad semestral), verificación de
alimentación PoE y estado del cableado, actualización de firmware de cámaras, verificación
de la precisión del conteo (prueba con conteo manual de referencia), backup de datos de aforo
histórico, revisión de capacidad del almacenamiento del NVR.)*

## 5.8 Mantenimiento del sistema de Sensorización Ambiental

*(Nota: Calibración de sensores según normativa metrológica legal (periodicidad establecida por
el fabricante para cada sensor — CO, O3, PM, temperatura, humedad). Limpieza de filtros de
las estaciones. Verificación de la memoria de respaldo (2 días de automomía). Actualización de
firmware de los concentradores edge. Verificación de envío de datos a la PCI. Inspección
estructural de mástiles y anclajes (anual).)*

## 5.9 Mantenimiento del sistema de Aparcamientos

*(Nota: Verificación de precisión del conteo (comprobación manual mensual), limpieza de
paneles LED exteriores, revisión de baterías de respaldo de los paneles (conectados a alumbrado
público), prueba de la comunicación 4G, verificación de los lazos de inducción o cámaras de
conteo, actualización de firmware de paneles y sistema de control.)*

## 5.10 Mantenimiento del sistema de Control de Tráfico

*(Nota: Limpieza de ópticas de cámaras ANPR (semestral), verificación de alimentación y
baterías en puntos sin suministro continuo, comprobación de paneles solares si instalados,
actualización del software ANPR (nuevas listas de matrículas, mejoras de motor OCR), gestión
de la capacidad del almacenamiento masivo (política de archivado/borrado RGPD), prueba de
acceso de emergencia al sistema desde Policía Local, renovación de certificados de acceso.)*

## 5.11 Mantenimiento del sistema de Tarjeta Turística

*(Nota: Mantenimiento de impresoras de tarjetas (limpieza de cabezales, reposición de cintas),
mantenimiento de tablets de validación (actualización de SO y app, sustitución de baterías),
reposición de stock de tarjetas Mifare (umbral mínimo de reserva), actualización de la
plataforma de gestión (CMS de la tarjeta), renovación de certificados de la pasarela de pago,
renovación de certificados 2FA, revisión del módulo de auditoría (ENS).)*

## 5.12 Mantenimiento de las herramientas de Dinamización Digital

*(Nota: Verificación del funcionamiento de las soluciones tecnológicas en los establecimientos
participantes, actualización de las herramientas de autodiagnóstico, soporte continuo a los
empresarios adheridos, sesiones de revisión a los 3 y 6 meses del inicio de funcionamiento
(según §12 del Pliego — "2 sesiones presenciales cortas sobre dudas posteriores").)*

## 5.13 Mantenimiento de la Red WiFi Municipal

*(Nota: Actualización de firmware de todos los APs (política de seguridad, vulnerabilidades CVE),
sustitución de baterías en puntos con alimentación de alumbrado público (revisión anual de
capacidad restante), revisión de la cobertura WiFi (medición de señal semestral en zonas
críticas), actualización de listas de filtro de contenidos, renovación de licencias del software
de gestión de red si aplica, revisión del portal cautivo (idiomas, condiciones de uso,
cumplimiento Wifi4EU).)*

---

# PARTE 6 — ANEXOS

## Anexo A — Fichas técnicas de equipamiento

*(Nota: Incluir las fichas técnicas (datasheets) completas de cada dispositivo hardware
significativo suministrado: servidores, SAI, GPUs, paneles LED, tótems, cámaras, sensores
ambientales, paneles de aparcamiento, cámaras ANPR, tablets, impresoras de tarjetas,
access points WiFi. Una ficha por modelo diferente de dispositivo.)*

## Anexo B — Planos as-built de instalaciones

*(Nota: Planos de ubicación georreferenciados de: paneles de cartelería, señalización inteligente
(40 puntos en 2 rutas), cámaras de flujos turísticos (8+ ubicaciones), estaciones ambientales
(2+1 meteorológica), paneles de aparcamiento, cámaras ANPR (50+), access points WiFi (34+
nuevos). Formato: DWG/PDF.)*

## Anexo C — Certificados y documentación legal

*(Nota: Adjuntar: certificado UNE 178104 de la PCI, certificado UNE 178502 de la PCI,
certificados CE de todos los dispositivos hardware exteriores, declaraciones de conformidad
RGPD, declaración DNSH firmada (Anexo II Orden TER/836/2022 según §14.1), documentación
de obra civil entregada a servicios técnicos municipales.)*

## Anexo D — Credenciales y secretos del sistema

*(Nota: Documento de acceso RESTRINGIDO (a custodiar por el técnico responsable del
contrato y el administrador de sistemas municipal). Contendrá: URLs de acceso a cada sistema,
usuarios administradores iniciales, contraseñas de primer acceso (a cambiar tras la entrega),
claves API de integraciones, certificados TLS y claves privadas, accesos a stores de apps,
accesos a cuentas de beacons y QR dinámicos. Almacenamiento recomendado: gestor de
secretos cifrado.)*

## Anexo E — Registro de formación impartida (§12 del Pliego)

*(Nota: Actas de las sesiones de formación presencial impartidas a los 3 perfiles del Pliego:
(1) usuarios municipales con capacidad de edición, (2) personal de mantenimiento de Obras y
Servicios, (3) usuarios administradores de sistemas. Indicar: fecha, lugar, duración, asistentes
firmantes, contenidos impartidos por actuación y perfil. Actas de las 2 sesiones de seguimiento
a los 3 y 6 meses del inicio de funcionamiento.)*

## Anexo F — Registro de incidencias y resoluciones durante la puesta en marcha

*(Nota: Registro cronológico de todas las incidencias detectadas durante la instalación, pruebas
y puesta en marcha, con indicación de: fecha detección, sistema afectado, descripción, fecha
resolución, solución aplicada. Permite demostrar el cumplimiento de los SLAs del §10.2.)*

## Anexo G — Declaración de cumplimiento DNSH y normativa NextGenerationEU

*(Nota: Declaración formal del adjudicatario acreditando el cumplimiento del principio "Do No
Significant Harm" (DNSH) según arts. 9 y 17 del Reglamento (UE) 2020/852, tal como exige
el §14.1 del Pliego. Incluir verificación DNSH por actuación conforme al §5 del Pliego.)*

---

*Fin del Esqueleto del Manual del Proyecto — versión 1.0*
*Elaborado con trazabilidad directa al Pliego de Prescripciones Técnicas, San Lorenzo de El Escorial, junio 2025.*
*Total de actuaciones documentadas: 13 | Dimensiones documentales: 5 | Partes del Manual: 6 + 7 Anexos*
