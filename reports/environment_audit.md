# Auditoria de Entorno

Fecha de auditoria: 2026-04-20
Workspace auditado: `C:\Users\rjuarcad\OneDrive - Universidad Alfonso X el Sabio\Escritorio\documentador`

## Resumen ejecutivo

El entorno actual **no esta listo todavia** para instalar Microsoft GraphRAG de forma reproducible.

Motivos principales:

1. **WSL no esta instalado** en esta maquina.
2. **La unica version local de Python detectada es 3.13.3**, mientras que la documentacion oficial de GraphRAG indica **Python 3.10-3.12**.
3. **OpenCode esta instalado y responde**, pero la validacion dentro del sandbox de esta sesion mostro un falso positivo de permisos que quedo descartado al repetir la prueba fuera del sandbox.
4. **No se detectaron variables de entorno de proveedores LLM** (`OPENAI`, `AZURE`, `GEMINI`, `ANTHROPIC`, etc.) en la sesion actual.

## Hallazgos verificados

### Sistema operativo y shell

- Sistema operativo: `Microsoft Windows 10.0.26200.8037`
- PowerShell: `5.1.26100.7920`
- Directorio de trabajo: `C:\Users\rjuarcad\OneDrive - Universidad Alfonso X el Sabio\Escritorio\documentador`

### WSL

Comandos ejecutados:

- `wsl.exe --status`
- `wsl.exe -l -v`

Resultado:

- Ambos comandos devolvieron que **Windows Subsystem for Linux no esta instalado**.
- Esto bloquea la preferencia de ejecucion en WSL exigida para este proyecto.

Referencia oficial consultada:

- OpenCode recomienda explicitamente **usar WSL en Windows** para la mejor compatibilidad: <https://opencode.ai/docs/windows-wsl/>

### Python

Comandos ejecutados:

- `python --version`
- `py -0p`
- `py -3.13 --version`
- `py -3.13 -m pip --version`

Resultado:

- `python --version` falla porque el alias `python` del sistema apunta al acceso directo de Microsoft Store.
- `py -0p` detecta:
  - `Python 3.13` en `C:\Users\rjuarcad\AppData\Local\Programs\Python\Python313\python.exe`
- `py -3.13 --version` devuelve `Python 3.13.3`
- `pip` disponible para esa instalacion: `pip 26.0.1`

Compatibilidad oficial verificada:

- La guia oficial de GraphRAG indica **Python 3.10-3.12**: <https://microsoft.github.io/graphrag/get_started/>

Conclusion:

- **Python 3.13.3 no cumple el requisito oficial actual de GraphRAG**.
- Antes de instalar GraphRAG sera necesario disponer de **Python 3.10, 3.11 o 3.12** en el entorno definitivo.

### Git

Comandos ejecutados:

- `git --version`
- `git status --short --branch`

Resultado:

- Git instalado: `git version 2.45.2.windows.1`
- El workspace ya esta dentro de un repositorio Git:
  - rama actual: `main`

Observacion:

- El repositorio **no esta vacio**; ya contiene contenido previo (`manualTecnico/`, `scripts/`, `README.md`, `CLAUDE.md`).
- Las fases posteriores deben respetar este estado y evitar sobrescrituras innecesarias.

### OpenCode

Comandos ejecutados:

- `opencode --version`
- `Get-Command opencode`
- `opencode --help`

Resultado:

- OpenCode instalado: `1.4.6`
- Binario resuelto en:
  - `C:\Users\rjuarcad\scoop\shims\opencode.exe`

Validacion:

- `opencode --help` **funciona correctamente** fuera del sandbox.
- La primera ejecucion dentro del sandbox produjo un error `EPERM` al intentar crear un lock bajo `C:\Users\rjuarcad\.local\state\opencode\locks\...`.
- Se comprobo que la ruta existe y que el usuario tiene permisos sobre ella; por tanto, el error observado en esa primera prueba corresponde a la **restriccion del sandbox de esta sesion**, no a un fallo concluyente de la instalacion local.

Referencia oficial consultada:

- Introduccion e instalacion de OpenCode: <https://opencode.ai/docs/>

### Variables de entorno LLM

Comando ejecutado:

- inspeccion de `Env:` filtrando `OPENAI|GEMINI|ANTHROPIC|AZURE|GOOGLE|OPENROUTER|MISTRAL|AWS|VERTEX`

Resultado:

- **No se detectaron variables de entorno** de proveedores LLM en la sesion actual.

Implicacion:

- En fases posteriores habra que preparar `.env` y `.env.example` sin hardcodear secretos.
- La indexacion y las queries reales no podran validarse hasta disponer de credenciales validas.

## Riesgos y bloqueos

### Bloqueo 1: WSL ausente

Impacto:

- Impide seguir la recomendacion oficial de OpenCode en Windows.
- Aumenta el riesgo de diferencias de comportamiento en scripts, rutas y tooling de CLI.

### Bloqueo 2: Python incompatible para GraphRAG

Impacto:

- GraphRAG no debe instalarse todavia sobre Python 3.13.3 si queremos una instalacion reproducible y alineada con la documentacion oficial.

### Riesgo 3: workspace preexistente

Impacto:

- Hay contenido previo en el repositorio y debemos integrar sin romper la estructura existente.

### Riesgo 4: sin credenciales LLM visibles

Impacto:

- No afecta a la auditoria, pero si bloqueara la validacion funcional completa en fases posteriores si no se resuelve.

## Decision de entorno

Decision documentada para el estado actual de la maquina el **2026-04-20**:

- **Entorno preferido por politica y por documentacion oficial: WSL**
- **Entorno realmente disponible ahora mismo: Windows PowerShell**

Decision operativa:

- **No es posible priorizar WSL porque no esta instalado.**
- Si se continua sin instalar WSL, la unica ruta viable inmediata es **Windows PowerShell**, pero eso seria una **ruta de contingencia**, no la preferida.
- Ademas, incluso en Windows, **no puede continuarse la instalacion real de GraphRAG** hasta incorporar una version compatible de Python (`3.10-3.12`).

## Recomendacion para continuar

Orden recomendado:

1. Instalar WSL.
2. Instalar dentro de WSL una version compatible de Python (`3.10-3.12`).
3. Revalidar OpenCode y seguir el resto de fases desde WSL.

Ruta alternativa, solo si se acepta desviacion controlada:

1. Permanecer en Windows.
2. Instalar Python `3.10-3.12` en Windows.
3. Continuar las siguientes fases en PowerShell, documentando explicitamente la desviacion respecto a la preferencia WSL.

## Estado de la Fase 1

Fase 1 completada.

Veredicto de auditoria:

- **WSL: NO DISPONIBLE**
- **Python compatible con GraphRAG: NO**
- **Git: OK**
- **OpenCode CLI: OK**
- **Variables LLM: NO DETECTADAS**
- **Preparado para pasar a instalacion real: NO TODAVIA**
