---
tags: [plan-de-estudios, modulo, nivel-4]
nivel: 4
prerequisitos: []
estado: no-iniciado
actualizado: 2026-10-04
---

# M12 — La tecnología como palanca

**En una frase:** usar lo que ya sabes hacer (programar, medir, automatizar, analizar datos) como la ventaja que un agricultor tradicional tarda años en construir.

## El fenómeno

Este es el único módulo donde se parte con ventaja. El resto del plan enseña lo que no se sabe; aquí se convierte la experiencia previa en dinero: **medir en vez de estimar, registrar sin trabajo manual, automatizar lo repetitivo y analizar el rendimiento con datos propios.** Es de fondo desde el primer día —el cuaderno de campo del módulo 5 ya es un sistema de datos— pero su aplicación plena llega cuando hay ciclos que comparar.

El riesgo que hay que evitar está escrito en [[Huerta/Qué sabe quien vive de la agricultura]]: el que llega de fuera creyendo que la tecnología sola gana. Aquí la tecnología es instrumento, no negocio.

## Submódulos

| # | Submódulo | Qué se estudia | De dónde viene |
|---|---|---|---|
| 12.1 | Registro digital del ciclo | Del cuaderno de papel a la hoja de cálculo o base de datos: campos, captura rápida, cierre de ciclo | Sistemas de Información · TIC |
| 12.2 | Medición en campo | Sensores de humedad y temperatura, tensiómetro con registro, estación mínima, qué comprar y qué no | Agricultura de Precisión |
| 12.3 | Automatización del riego | Timer, electroválvulas, control por humedad, costo y confiabilidad en un clima semiárido | Sistemas de Riego · Hidráulica |
| 12.4 | Ubicación y mapas | Levantar la parcela, medir superficies reales, capas y croquis (SIG simple, GPS del teléfono, topografía básica) | Sistemas de Información Geográfica · Topografía |
| 12.5 | Análisis de datos propios | Rendimiento por m², por variedad, por fecha de siembra; qué gráfica dice qué; errores de conclusión | Técnicas Cuantitativas · Diseños Experimentales · Econometría |
| 12.6 | Trazabilidad y calidad | Lote, fecha, insumo, origen: lo que un comprador serio va a pedir | Inocuidad Alimentaria · Calidad y Competitividad |
| 12.7 | Pronóstico y decisión | Modelos simples de precio, demanda y clima; cuándo conviene un modelo y cuándo la regla de dedo | Manejo de Información Económica · Investigación de Operaciones |
| 12.8 | Herramientas propias | Construir solo lo necesario: scripts, formatos, tableros. La regla del proyecto: la lógica y los números no dependen de un modelo de lenguaje | Determinismo por default |

Nota de método (regla propia de trabajo): **determinismo por default**. Un cálculo de costos o de riego se hace con código y fórmulas, no preguntándole a una IA. La IA sirve para explorar y para escribir el código; los números se calculan.

## Lo que hay que saber antes

Nada para arrancar (12.1 y 12.4 se usan desde el día 1). El resto rinde cuando existen ciclos y números: se apoya en [[M05 - El ciclo del cultivo]], [[M07 - La cosecha y el después]] y [[M08 - Los números del ciclo]].

## Se conecta con el repositorio

- [[Huerta/Experimentos]] — el formato de prueba de una variable aplicado con registro sistemático
- [[M08 - Los números del ciclo]] — la hoja de cálculo del costeo vive aquí con su estructura
- [[M03 - El agua]] — el tensiómetro y el control de riego son este módulo aplicado allá
- [[M04 - El clima y la temporada]] — el registro de temperatura mínima de la cama
- Criterio propio del autor: scripts deterministas por encima de herramientas generativas.

## Notas por crear

- [[Registro digital del ciclo]] — estructura de datos y captura (hoja de cálculo o SQLite)
- [[Sensores y medición automatizada]] — qué comprar, cuánto cuesta, cómo se calibra
- [[Levantamiento y medición de la parcela]] — croquis con medidas reales y superficies
- [[Análisis de rendimiento por m²]] — gráficas propias y errores de conclusión a evitar
- [[Automatización de riego]] — timer, válvulas, control por humedad: costo y riesgos
- [[Trazabilidad - qué pide un comprador serio]] — lote, fecha, insumo, registro

## Tarea del módulo

**Entregable:** un **sistema de registro propio en operación**, con:

1. Un registro digital (hoja de cálculo o base de datos) donde ya estén capturados los datos del ciclo en curso: actividades, insumos, costos, cosecha.
2. Croquis de la parcela con medidas y superficies reales, no estimadas.
3. Al menos una medición automatizada o registrada sin intervención manual (temperatura mínima, humedad o riegos).
4. Una gráfica propia: rendimiento por m², costo por ciclo o riego por semana, con lectura escrita de qué muestra (y qué no).
5. Una herramienta construida a la medida que quite trabajo repetitivo real (cálculo de costeo, generación de calendario, cálculo de riego), en código, con los números fuera del modelo de lenguaje.

**Criterio de éxito:** los números del negocio salen de un sistema propio que otra persona podría usar, y alguna tarea repetitiva dejó de hacerse a mano.

## Referencias disponibles

- Ya en el repositorio: [[Huerta/Experimentos]] (formato de registro), [[M08 - Los números del ciclo]] (estructura de costos) y el criterio de método del autor (determinismo por default)
- Falta buscar al escribir el módulo: precios y especificaciones de sensores de humedad y tensiómetros accesibles en México, controladores de riego, apps de medición de terreno, y ejemplos de bitácoras agrícolas digitales de pequeños productores

## Cierra cuando

El sistema está en uso y el ciclo siguiente se planeó con datos del anterior.

**Aporta a:** todos los módulos, en particular [[M03 - El agua]], [[M07 - La cosecha y el después]], [[M08 - Los números del ciclo]] y [[M13 - La parcela como sistema]].
