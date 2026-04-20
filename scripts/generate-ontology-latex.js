#!/usr/bin/env node

/**
 * Genera código LaTeX del catálogo de etiquetas de la ontología de mensajería.
 *
 * Lee los esquemas JSON directamente desde atlas-messaging-ontology/schemas/
 * y produce un fichero .tex listo para ser incluido en el manual técnico con \input{}.
 *
 * Uso:
 *   node scripts/generate-ontology-latex.js
 *   node scripts/generate-ontology-latex.js --out manualTecnico/capitulos/03-modulos/ontologia-generada.tex
 *
 * Ejecutar desde la raíz del repositorio atlas-documentation.
 */

import { readdirSync, readFileSync, statSync, writeFileSync, mkdirSync } from 'node:fs'
import { resolve, dirname, join, basename } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const SCHEMAS_DIR = resolve(__dirname, '../../atlas-messaging-ontology/schemas')
const DEFAULT_OUT = resolve(
  __dirname,
  '../manualTecnico/capitulos/03-modulos/ontologia-generada.tex',
)

// ─── Lectura de esquemas ──────────────────────────────────────────────────────

/**
 * Recorre recursivamente el directorio de schemas y devuelve un mapa:
 *   tag base → { request: schema|null, response: schema|null }
 */
function loadSchemas(dir) {
  const registry = new Map()

  function walk(currentDir) {
    const entries = readdirSync(currentDir)
    for (const entry of entries) {
      const fullPath = join(currentDir, entry)
      const stat = statSync(fullPath)
      if (stat.isDirectory()) {
        walk(fullPath)
      } else if (entry === 'request.json' || entry === 'response.json') {
        const schema = JSON.parse(readFileSync(fullPath, 'utf-8'))
        const id = schema.$id // e.g. "tools:ai:llm:request"
        if (!id) continue

        // El tag base es el $id sin el último segmento (:request / :response)
        const parts = id.split(':')
        const kind = parts.at(-1) // "request" | "response"
        if (kind !== 'request' && kind !== 'response') continue
        const baseTag = parts.slice(0, -1).join(':')

        if (!registry.has(baseTag)) registry.set(baseTag, { request: null, response: null })
        registry.get(baseTag)[kind] = schema
      }
    }
  }

  walk(dir)

  // Ordenar alfabéticamente por tag
  return new Map([...registry.entries()].sort())
}

// ─── Helpers LaTeX ────────────────────────────────────────────────────────────

/** Escapa caracteres especiales de LaTeX */
function tex(str) {
  if (str === undefined || str === null) return ''
  return String(str)
    .replace(/\\/g, '\\textbackslash{}')
    .replace(/&/g, '\\&')
    .replace(/%/g, '\\%')
    .replace(/\$/g, '\\$')
    .replace(/#/g, '\\#')
    .replace(/_/g, '\\_')
    .replace(/\{/g, '\\{')
    .replace(/\}/g, '\\}')
    .replace(/~/g, '\\textasciitilde{}')
    .replace(/\^/g, '\\textasciicircum{}')
}

/** Formatea el tipo de una propiedad del schema */
function formatType(prop) {
  if (prop.oneOf) return prop.oneOf.map(o => o.type ?? 'any').join(' / ')
  if (prop.type === 'array' && prop.items) return `${prop.items.type ?? 'object'}[]`
  return prop.type ?? 'any'
}

/** Formatea las restricciones de una propiedad como texto corto */
function formatConstraints(prop) {
  const parts = []
  if (prop.enum) parts.push(prop.enum.map(v => `\\texttt{${tex(v)}}`).join(', '))
  if (prop.minimum !== undefined) parts.push(`mín: ${prop.minimum}`)
  if (prop.maximum !== undefined) parts.push(`máx: ${prop.maximum}`)
  if (prop.minLength !== undefined) parts.push(`minLen: ${prop.minLength}`)
  if (prop.maxLength !== undefined) parts.push(`maxLen: ${prop.maxLength}`)
  if (prop.minItems !== undefined) parts.push(`minItems: ${prop.minItems}`)
  if (prop.maxItems !== undefined) parts.push(`maxItems: ${prop.maxItems}`)
  if (prop.default !== undefined) parts.push(`default: \\texttt{${tex(String(prop.default))}}`)
  if (prop.pattern) parts.push(`patrón: \\texttt{${tex(prop.pattern)}}`)
  if (prop.format) parts.push(`formato: \\texttt{${tex(prop.format)}}`)
  return parts.join('; ')
}

/** Genera una tabla longtable para los campos de un esquema */
function renderPropertiesTable(schema) {
  if (!schema?.properties) return '\\textit{Sin propiedades definidas.}\n\n'

  const required = new Set(schema.required ?? [])
  const lines = []

  lines.push('\\begin{center}')
  lines.push(
    '\\begin{longtable}{@{} l l c p{4.5cm} p{4cm} @{}}',
  )
  lines.push('\\toprule')
  lines.push(
    '\\textbf{Campo} & \\textbf{Tipo} & \\textbf{Req.} & \\textbf{Descripción} & \\textbf{Restricciones} \\\\',
  )
  lines.push('\\midrule')
  lines.push('\\endfirsthead')
  lines.push('\\midrule')
  lines.push(
    '\\textbf{Campo} & \\textbf{Tipo} & \\textbf{Req.} & \\textbf{Descripción} & \\textbf{Restricciones} \\\\',
  )
  lines.push('\\midrule')
  lines.push('\\endhead')
  lines.push('\\midrule')
  lines.push('\\multicolumn{5}{r}{\\footnotesize\\itshape Continúa en la siguiente página} \\\\')
  lines.push('\\endfoot')
  lines.push('\\bottomrule')
  lines.push('\\endlastfoot')

  for (const [name, prop] of Object.entries(schema.properties)) {
    const type = tex(formatType(prop))
    const req = required.has(name) ? '\\checkmark' : ''
    const desc = tex(prop.description ?? '')
    const constraints = formatConstraints(prop)
    lines.push(
      `  \\texttt{${tex(name)}} & \\texttt{${type}} & ${req} & ${desc} & ${constraints} \\\\`,
    )
  }

  lines.push('\\end{longtable}')
  lines.push('\\end{center}')
  lines.push('')

  return lines.join('\n')
}

/** Genera el bloque LaTeX de un schema (request o response) */
function renderSchema(title, schema) {
  const lines = []
  lines.push(`\\paragraph{${title}}`)
  lines.push('')

  if (!schema) {
    lines.push('\\textit{Esquema no disponible.}')
    lines.push('')
    return lines.join('\n')
  }

  lines.push(`\\textbf{Tag:} \\texttt{${tex(schema.$id)}}\\\\`)
  lines.push(`\\textit{${tex(schema.description ?? '')}}`)
  lines.push('')
  lines.push(renderPropertiesTable(schema))

  return lines.join('\n')
}

// ─── Agrupación por dominio ───────────────────────────────────────────────────

function groupByDomain(registry) {
  const domains = new Map()
  for (const [tag, schemas] of registry) {
    const domain = tag.split(':')[0]
    if (!domains.has(domain)) domains.set(domain, new Map())
    domains.get(domain).set(tag, schemas)
  }
  return domains
}

// ─── Generador principal ──────────────────────────────────────────────────────

function generateLatex(registry) {
  const totalTags = registry.size
  const domains = groupByDomain(registry)
  const lines = []

  lines.push('% ─────────────────────────────────────────────────────────────────')
  lines.push('% FICHERO GENERADO AUTOMÁTICAMENTE')
  lines.push('% Comando: node scripts/generate-ontology-latex.js')
  lines.push('% Fuente:  atlas-messaging-ontology/schemas/')
  lines.push(`% Etiquetas registradas: ${totalTags}`)
  lines.push('% No editar manualmente — los cambios se perderán en la siguiente generación.')
  lines.push('% ─────────────────────────────────────────────────────────────────')
  lines.push('')
  lines.push('% Requiere en main.tex: \\usepackage{longtable}, \\usepackage{amssymb}')
  lines.push('')

  lines.push('\\subsection{Catálogo de etiquetas}')
  lines.push(`\\label{sec:ontologia-catalogo}`)
  lines.push('')
  lines.push(
    `El catálogo recoge las ${totalTags} etiquetas actualmente registradas en la ontología, organizadas por dominio funcional. ` +
      `Este contenido se genera automáticamente desde los esquemas JSON del repositorio \\texttt{atlas-messaging-ontology}.`,
  )
  lines.push('')

  for (const [domain, tags] of domains) {
    lines.push(`\\subsubsection{Dominio \\texttt{${tex(domain)}}}`)
    lines.push(`\\label{sec:ontologia-dominio-${tex(domain)}}`)
    lines.push('')

    for (const [tag, schemas] of tags) {
      // Etiqueta como subsubsection dentro del dominio
      lines.push(`\\subparagraph{\\texttt{${tex(tag)}}}`)
      lines.push(`\\label{sec:tag-${tex(tag).replace(/:/g, '-')}}`)
      lines.push('')

      const parts = tag.split(':')
      lines.push(
        `Dominio: \\texttt{${tex(parts[0])}} — Categoría: \\texttt{${tex(parts[1])}} — Acción: \\texttt{${tex(parts.slice(2).join(':'))}}`,
      )
      lines.push('')

      lines.push(renderSchema('Petición (request)', schemas.request))
      lines.push(renderSchema('Respuesta (response)', schemas.response))
      lines.push('')
    }
  }

  return lines.join('\n')
}

// ─── CLI ──────────────────────────────────────────────────────────────────────

const args = process.argv.slice(2)
const outIndex = args.indexOf('--out')
const outPath = outIndex !== -1 && args[outIndex + 1] ? resolve(args[outIndex + 1]) : DEFAULT_OUT

let registry
try {
  registry = loadSchemas(SCHEMAS_DIR)
} catch (err) {
  console.error(`Error leyendo schemas en ${SCHEMAS_DIR}:`)
  console.error(err.message)
  process.exit(1)
}

if (registry.size === 0) {
  console.error(`No se encontraron esquemas en ${SCHEMAS_DIR}`)
  process.exit(1)
}

const latex = generateLatex(registry)
mkdirSync(dirname(outPath), { recursive: true })
writeFileSync(outPath, latex, 'utf-8')
console.log(`✓ ${registry.size} etiquetas → ${outPath}`)
