---
tags: [granja, arteaga, fuentes, ligas]
fuente: fuentes-importantes-agricolas.txt (listado generado con Gemini)
verificado: 2026-10-02
metodo: curl -sSL con user-agent de navegador, una por una, 2026-10-02
---

# Fuentes y recursos locales — verificadas

Las 16 ligas del listado original, revisadas una por una el 2026-10-02. El resultado importa porque el listado salió de un LLM: los modelos inventan URLs con una seguridad que no se distingue de la verdad.

**Resumen:** 10 viven con contenido real, 4 están bloqueadas (existen, no se dejan leer), **1 está rota** (el dominio no existe) y 5 son relleno comercial. Al final, las 6 ligas que el plan nombra sin dar y que sí encontramos.

## Viven (contenido real)

| Fuente | Liga | Qué es en realidad |
|---|---|---|
| SEDER Coahuila | `coahuila.gob.mx/seder/` → redirige a `seder.coahuila.gob.mx` | Sitio estatal de desarrollo rural. 43 KB. La liga buena es la de destino. |
| Arteaga, apoyos a manzana | `arteaga.gob.mx/refuerzan-arteaga-y-estado-apoyo-a-productores-de-manzana/` | Nota municipal sobre el fondo de $11 MDP. 193 KB. |
| UAAAN | `uaaan.edu.mx` | Portal de "La Narro". 459 KB. |
| Cursos UAAAN | `cursosenlinea.uaaan.mx` | Ver la liga rota abajo: el dominio que trae el listado no existe. |
| Cornell BF 101 | `smallfarmcourses.com/p/bf-101-como-iniciar-su-negocio-agricola` | Curso real, en español. 481 KB. |
| FAO — guía de capacitación | `openknowledge.fao.org/server/api/core/bitstreams/325d8fbc-…/content` | **PDF real, 1.38 MB.** La liga más valiosa del listado después de la Ley Agraria. |
| InfoLibros | `infolibros.org/libros-pdf-gratis/temas-varios/agricultura/` | Recopilación de PDFs gratuitos. 310 KB. Calidad variable. |
| Modelos de plan de negocios | `modelosdeplandenegocios.com/blogs/news/agricola-estudio-mercado` | Blog comercial. 417 KB. |
| WEAGRO | `weagro.ua/es/blog/plan-de-negocio-en-el-sector-agricola-…` | Blog de proyecto universitario, orientado a España. 180 KB. |
| PR Farm Credit | `prfarmcredit.com/blog/10-consejos-…-industria-agricola/` | Puerto Rico Farm Credit. Genérico. 188 KB. |

## Bloqueadas (existen, no se dejan leer)

El servidor las pide con un navegador y contesta con una página de reto o un 403. No significa que estén caídas.

- **`gob.mx/agricultura/acciones-y-programas/produccion-para-el-bienestar-2026`** — devuelve 200 pero solo 1.8 KB de "Challenge Validation" (Cloudflare). El programa existe; la página canónica de SADER es la misma ruta **sin** el `-2026`. El sufijo del año no se pudo confirmar.
- **`gob.mx/pa/articulos/los-convenios-y-contratos-en-ejidos-y-comunidades-…`** — mismo reto de Cloudflare. El artículo existe: aparece en buscador con ese título exacto.
- **`mexico.justia.com/federales/leyes/ley-agraria/…`** — 403. No hace falta: la Ley Agraria oficial en PDF está abajo.
- **`vun.inifap.gob.mx/BibliotecaWeb/_Content?/=14`** y **`?/=10269`** — 403 las dos; también la raíz `/_Content`. El WAF del INIFAP rechaza clientes automatizados. El patrón de la URL es el correcto, pero **los identificadores `14` y `10269` no se pudieron comprobar**. Entrar a mano a `vun.inifap.gob.mx/BibliotecaWeb/_Content`.

## Rota

- **`cursosenlinea.uaaan.edu.mx`** — el dominio **no existe** (no resuelve en DNS). El correcto es **`cursosenlinea.uaaan.mx`** (200, "Cursos en Línea"). Es el error más limpio del listado: un `.edu.mx` de más.

## Relleno de captación (viven, pero no son autoridad)

`zeroclm.com` (despacho privado que publica sobre el art. 79 para atraer clientes), `modelosdeplandenegocios.com`, `weagro.ua`, `prfarmcredit.com` e `infolibros.org`. Ninguna es fuente institucional. Sirven para una idea general; no para citar un requisito, un plazo o un monto.

## Ligas que el plan nombra y no da (encontradas y verificadas)

| Qué | Liga | Estado |
|---|---|---|
| **Ley Agraria** vigente, PDF oficial (última reforma DOF 14-11-2025) | `diputados.gob.mx/LeyesBiblio/pdf/LAgra.pdf` | 200, 716 KB — la fuente que hay que usar en lugar de Justia |
| **SNIIM**, precios de mayoreo de Coahuila | `economia-sniim.gob.mx/PreciosProdSelPorEstado.asp?edo=7` | 200 — Coahuila es el estado `7` |
| SNIIM, portal general | `economia-sniim.gob.mx/nuevo/` | 200 |
| **Fertilizantes para el Bienestar** | `gob.mx/agricultura/acciones-y-programas/programa-de-fertilizantes-para-el-bienestar` | Existe (Cloudflare no deja leer) |
| **Padrón Ganadero Nacional** | `pgn.org.mx` | ⚠️ **certificado SSL vencido** — no lo abras. Usar `gob.mx/agricultura/acciones-y-programas/inscripcion-al-padron-ganadero-nacional` |
| **Fierro de herrar y señal de sangre**, trámite estatal | `tramitescoahuila.gob.mx/tramites/secretar%C3%ADa-de-desarrollo-rural/expedici%C3%B3n-registro-fierro-herrar.html` | 200, 99 KB. La variante con `-y-se%C3%B1al-de-sangre` que sale primero en buscadores da **404**. |
| Fierro de herrar explicado por la SEDER | `seder.coahuila.gob.mx/preguntas.html` | 200 |

Los requisitos y costos de los trámites pecuarios están en [[Tenencia de tierra y registros pecuarios]].

## Lecciones para el siguiente listado

1. **Un `.edu.mx` inventado** (los cursos de la UAAAN) y **un `-2026` sin confirmar** (la página de SADER) — los dos errores típicos: sufijos plausibles que el modelo añade porque suenan bien.
2. **El 40% del listado no es institucional.** Cuando un LLM arma una bibliografía mete blogs de captación que aparecen bien posicionados. Se distinguen porque ninguna dice quién firma.
3. **Las ligas que el propio texto menciona y no incluye** (SNIIM, padrón ganadero, fertilizantes) resultaron más útiles que varias de las que sí incluyó. Lo que le faltaba al listado era justo lo operativo.
