---
tags: [plan-de-estudios, modulo, nivel-4]
nivel: 4
prerequisitos: []
estado: parcial — escrito lo que toca a M01 (12.1, 12.2, 12.4, 12.5, 12.8)
actualizado: 2026-10-04
---

# M12 — La tecnología como palanca

**En una frase:** usar lo que ya sabes hacer (programar, medir, automatizar, analizar datos) como la ventaja que un agricultor tradicional tarda años en construir.

**Siglas:** MO = materia orgánica del suelo; CE = conductividad eléctrica (sales, en dS/m); CSV = archivo de texto con columnas separadas por comas (se abre en cualquier hoja de cálculo); GPS = ubicación por satélite del teléfono.

## El fenómeno

Este es el único módulo donde se parte con ventaja. El resto del plan enseña lo que no se sabe; aquí se convierte la experiencia previa en dinero: **medir en vez de estimar, registrar sin trabajo manual, automatizar lo repetitivo y analizar el rendimiento con datos propios.** Es de fondo desde el primer día —el registro de suelo del módulo 1 ya es un sistema de datos— pero su aplicación plena llega cuando hay ciclos que comparar.

El riesgo que hay que evitar está escrito en [`Huerta/Qué sabe quien vive de la agricultura`](../Huerta/Qu%C3%A9%20sabe%20quien%20vive%20de%20la%20agricultura.md): el que llega de fuera creyendo que la tecnología sola gana. Aquí la tecnología es instrumento, no negocio.

## Submódulos y estado

| # | Submódulo | Estado |
|---|---|---|
| 12.1 | Registro digital del ciclo | **escrito (parte de suelo)** |
| 12.2 | Medición en campo | **escrito (parte de suelo)** |
| 12.3 | Automatización del riego | pendiente (va con [[M03 - El agua]]) |
| 12.4 | Ubicación y mapas | **escrito (parte de suelo)** |
| 12.5 | Análisis de datos propios | **escrito (parte de suelo)** |
| 12.6 | Trazabilidad y calidad | pendiente (va con [[M07 - La cosecha y el después]]) |
| 12.7 | Pronóstico y decisión | pendiente (va con [[M09 - El mercado y el cliente]]) |
| 12.8 | Herramientas propias | **escrito (parte de suelo)** |

Lo que sigue es la parte que sostiene a [[M01 - La tierra]]. El resto se escribe cuando toque su módulo.

---

## 12.1 Registro digital del ciclo — el registro de suelo

### Por qué una tabla de texto y no una nota

Un registro de suelo no es prosa: son filas con fecha, punto, método y número. Los tres formatos posibles y su costo real:

| Formato | Ventaja | Costo |
|---|---|---|
| Nota de texto (Obsidian) | Se escribe en el momento, sin fricción | No se puede graficar ni sumar; a la tercera temporada ya nadie lo lee |
| Hoja de cálculo en la nube | Gráficas fáciles | Depende de una cuenta, de internet y de que el proveedor siga ahí; sin historial de cambios por fila |
| **CSV en el repo (git)** | Texto plano, diff por fila, versionado, abre en cualquier hoja de cálculo, no caduca | Requiere disciplina de captura y no tiene interfaz bonita |

Se elige **CSV versionado**. Es la misma razón por la que el resto de esta base es markdown: formato plano, sin dependencia, con historial.

### El esquema (20 columnas, unidades en el encabezado)

```
fecha, punto, lat, lon, profundidad_cm, textura_tacto, vinagre, ph_agua, ph_cacl2,
ph_buffer, mo_pct, ce_ds_m, n_ppm, p_ppm, k_ppm, carbonatos_pct, enmienda,
dosis_g_m2, costo_mxn, nota
```

| Columna | Qué va | Regla |
|---|---|---|
| `fecha` | ISO 8601: `2026-10-04` | Nunca "octubre" |
| `punto` | Identificador corto: `cama-1`, `par-A2` | Debe existir en el croquis (12.4) |
| `lat`, `lon` | Coordenadas del teléfono | 5 decimales; sirven para volver al mismo punto |
| `profundidad_cm` | `0-30`, `0-15` | Rango, no un número, porque es una muestra compuesta |
| `textura_tacto` | `migajon`, `migajon-arenoso`, `arcilloso`… | El diagrama de tacto da clase, no porcentajes |
| `vinagre` | `no`, `leve`, `media`, `fuerte` + gotas | Cualitativo + el dato semicuantitativo |
| `ph_agua`, `ph_cacl2`, `ph_buffer` | Números | **Anotar siempre con qué método se midió**: no se comparan entre métodos |
| `mo_pct`, `ce_ds_m` | Números del laboratorio | Una columna por unidad, no mezclar |
| `carbonatos_pct` | Número (o `>10`) | El dato que decide si vale la pena intentar bajar el pH |
| `enmienda` | Texto: `azufre elemental`, `composta`, `yeso` | Nombre exacto del insumo |
| `dosis_g_m2`, `costo_mxn` | Números | Por m² y total; así se compara entre temporadas |
| `nota` | Texto libre | Obligatorio si algo se salió del protocolo |

### Cómo se captura

1. Se generan las columnas vacías una vez:
   ```
   $ python3 "Plan de Estudios/scripts/suelo.py" plantilla --salida registro_suelo.csv
   ```
2. Se llena **una fila por punto y por fecha**.
3. **No se edita una fila vieja**: cada medición nueva es una fila nueva. La serie temporal es el activo, no el último número.
4. Se guarda en el repo. Un ejemplo de tres filas (ilustrativo, no medido):

```csv
fecha,punto,lat,lon,profundidad_cm,textura_tacto,vinagre,ph_agua,ph_cacl2,ph_buffer,mo_pct,ce_ds_m,carbonatos_pct,enmienda,dosis_g_m2,costo_mxn,nota
2026-10-05,cama-1,25.43812,-100.85120,0-15,migajon,fuerte-180,8.1,,,1.2,0.9,9,ninguna,,,calibre: no se toca el pH
2026-10-05,par-A2,25.43790,-100.85100,0-30,migajon,media-60,7.9,,,0.9,0.8,3,ninguna,,,
2026-11-20,cama-1,25.43812,-100.85120,0-15,migajon,fuerte-180,8.0,,,2.6,0.9,9,composta,1200,650,pila propia, costo = gasolina
```

**Lo que este registro permite ver** después de tres temporadas: si la MO sube (la única palanca real), si el pH se mueve (probablemente no, con cal), y cuánto costó cada intento.

## 12.2 Medición en campo — qué se mide y con qué

### La división del trabajo

- **En campo** se decide **dónde** muestrear, **si hay cal** (el vinagre) y se orienta el pH.
- **En laboratorio** se sacan los números que se van a comparar en el tiempo: pH con método, MO, textura, CE, carbonatos, micronutrientes.

Pretender medir en campo lo que da el laboratorio es el error caro: los kits caseros están hechos para suelo ácido y no se calibran con la precisión para seguir décimas en suelo alcalino (CSU GardenNotes #222). El kit barato **distingue un 6 de un 8, nada más**.

### Instrumentos, con precios verificados el 2026-10-04

| Instrumento | Para qué sirve de verdad | Precio | Proveedor |
|---|---|---|---|
| Medidor 4 en 1 (pH, humedad, temperatura, luz) | Orientación gruesa; el pH de estos aparatos es notoriamente flojo | **$279** (marketplace) | Amazon MX [1] |
| Medidor de pH de bolsillo Hanna HI98107 | pH de agua y de extractos; el escalón real de entrada | **$1,364.16** | Hulk Scientific [2] |
| Medidor de pH de bolsillo Hanna HI98103 | Igual, otra referencia | $1,513 | Grow Depot [3] |
| Medidor de pH OHAUS ST10 (0.1 pH) | Verificación rápida | $1,613.22 | Mercalab [4] |
| Kit de campo LaMotte 5928-01 (macronutrientes) | Análisis de campo completo; rango profesional | $16,033 | Hydrocultura [5] |
| Kit de pH y CE directos de suelo (KITSOIL) | Medición directa en pasta de suelo saturado | $16,273.57 | Proain [6] |
| Sensor de humedad de suelo YL-69 (Arduino/PIC) | Automatizar la humedad; hay que calibrarlo contra peso | $239 | Megacentral [7] |
| Tensiómetro Irrometer, 15 cm | La medida honesta de cuándo regar | $1,968-$2,412 | Hydrocultura / Kosmos [8][9] |

Lectura de la tabla: **el escalón útil está en ~$1,400** (un medidor de bolsillo con calibración), no en $279 ni en $16,000. El de $279 sirve para saber si estás en 6 o en 8; el tensiómetro es para [[M03 - El agua]], no para el suelo, pero se compra en la misma decisión.

### Cómo se mide bien el pH de un suelo

1. **Calibrar el medidor** con las soluciones buffer que trae (pH 4 y 7) antes de cada sesión de medición. Sin calibrar, el número es decorativo.
2. **Preparar la muestra:** suelo seco al aire, tamizado de piedras, relación 1:1 con agua destilada (o 0.01 M de CaCl₂ para la medición estable), reposar y medir la suspensión, no el suelo seco.
3. **Anotar el método** (`ph_agua` o `ph_cacl2`). El pH en agua y en CaCl₂ difieren ~0.6 unidades y el de CaCl₂ es el estable entre estaciones (UGA Circular 875).
4. **Limpiar el electrodo** entre muestras y no tocar la punta con los dedos.
5. **Registrar el número en la fila de ese día**, no en el cuaderno para "pasarlo después" — el "después" no llega.

### Actividad 12.2 (parte de suelo)

- [ ] Mide pH con el instrumento disponible en cinco puntos y anota el método usado en cada uno.
- [ ] Calibra el medidor y **vuelve a medir la misma muestra tres veces**: si los tres números no coinciden, ahí está tu error de instrumento y hay que buscarlo, no ignorarlo.
- [ ] Compara tu medición de campo contra la del laboratorio para el mismo punto: la diferencia es tu error de método, y hay que conocerlo.

## 12.4 Ubicación y mapas — levantar el terreno

### Para qué

Todo el plan se presupuesta **por m²** y las decisiones de suelo dependen de dónde está la capa dura y dónde hay sombra. Sin croquis medido no hay costo por m² ni comparación entre temporadas: solo hay recuerdos.

### Cómo se levanta, sin instrumentos caros

1. **Medir con cinta** los lados útiles de cada bloque (no el cerco: el ancho que realmente se siembra).
2. **Georreferenciar los puntos de muestreo** con el GPS del teléfono (precisión típica de 3-5 m, suficiente). Se anotan `lat`/`lon` en el registro.
3. **Dibujar a escala** en papel o con cualquier editor: cama, macetas, sombra, agua, caliche, caminos, pendiente.
4. **Marcar la orientación** (norte) y la hora de sol de tarde: en este sitio la cama recibe sol pleno de tarde, y eso se dibuja, no se recuerda.
5. **Anotar los obstáculos permanentes**: dónde se pone dura la barreta (caliche), por dónde corre el agua en una lluvia fuerte.

```
   N
   ↑
   ┌─────────────────────────────── parcela (medida, no estimada)
   │   ┌────┐  sombra de mañana (malla 30-40%)
   │   │cama│  3.0 m × 0.5 m = 1.5 m²
   │   └────┘
   │   • A1     • A2        ← puntos de muestreo con lat/lon
   │        ▓▓▓▓▓  caliche a 35 cm (medido con barreta)
   │   • A3          •  toma de agua
   └───────────────────────────────
```

### Regla de oro del levantamiento

**Se vuelve al mismo punto en la misma coordenada cada temporada.** Los puntos de muestreo son fijos y numerados; si cambian de lugar, la serie temporal se rompe y ya no se puede decir si el suelo cambió o si muestreaste otra cosa.

### Actividad 12.4 (parte de suelo)

- [ ] Croquis a escala de la cama y la parcela, con medidas reales, superficies calculadas, sombra, agua y caliche.
- [ ] Toma las coordenadas de los puntos de muestreo y agrégalas al registro.
- [ ] Calcula las superficies reales y anótalas: son el denominador de todos los costos por m² del plan.

## 12.5 Análisis de datos propios — qué graficar y qué no

### Las tres gráficas que sí sirven

| Gráfica | Qué muestra | Cuándo tiene sentido |
|---|---|---|
| **MO % en el tiempo** (por punto) | Si la palanca de fondo está funcionando | Después de 2-3 ciclos |
| **Costo por unidad de pH / por punto de MO** | Qué insumo deja más por peso | Desde la primera enmienda |
| **Rendimiento por m²** o piezas cosechadas | Si el suelo mejoró se ve aquí, al final | Cada ciclo |

### Los tres errores de conclusión que hay que evitar

1. **Comparar pH medido con métodos distintos.** Si un año mides en agua (1:1) y otro en CaCl₂, la diferencia de ~0.6 unidades es del método, no del suelo. **Solo se grafica una serie con el mismo método en todas las filas.**
2. **Confundir la variación estacional con un cambio real.** El pH medido en agua puede moverse cerca de una unidad entre el suelo lavado por las lluvias de invierno y el suelo fertilizado de primavera, sin que la acidez real haya cambiado. **El método estable para seguir cambios es CaCl₂.**
3. **Tomar un punto por la tendencia.** Un dato no es una serie. Y un cambio que no se confirmó con el testigo —la franja o maceta sin enmendar— puede ser clima, no enmienda.

Esta última es la regla de método que ya está en [`Huerta/Experimentos`](../Huerta/Experimentos.md): **una variable por prueba, con testigo**, y el registro anotado en el momento.

### La lectura honesta del caso Arteaga

Si el pH en agua bajó de 8.1 a 7.8 pero **el vinagre sigue burbujeando igual**, no se corrigió nada: se movió la lectura. La cal sigue ahí y el pH regresa. Es el mismo razonamiento por el que el estudio chileno con 5.2% de carbonatos movió el pH de 8.31 a 8.03 y nada más.

### Actividad 12.5 (parte de suelo)

- [ ] Grafica la MO de cada punto en el tiempo (aunque hoy sea un solo punto de partida: la gráfica empieza cuando empieza el registro).
- [ ] Escribe la lectura de tu gráfica: qué muestra y **qué no** puede mostrar todavía.
- [ ] Anota la regla de comparación que vas a respetar (método de pH fijo, vuelta al mismo punto, testigo sin enmendar).

## 12.8 Herramientas propias — `suelo.py`

### Qué es

Un script de ~300 líneas sin dependencias, en `Plan de Estudios/scripts/suelo.py`, que hace las cuentas del expediente de suelo: dosis de azufre por unidad de pH, costo, composta para subir materia orgánica, la perspectiva de la cal libre y la plantilla del registro.

### Por qué determinista

Regla del plan: **la lógica y los números no dependen de un modelo de lenguaje.** Un cálculo de dosis se hace con constantes citadas, fórmulas visibles y una autoprueba que falla si alguien cambia una constante sin darse cuenta. Un LLM puede escribir el código y explicarlo; no puede *ser* la calculadora.

```
$ python3 suelo.py autoprueba
  [ok ] masa de suelo 1.5 m² × 15 cm × 1.3: 292.5000 (esperado 292.5000)
  [ok ] g/m² por unidad de pH (mín): 73.0000 (esperado 73.0000)
  [ok ] factor arenoso: 48.6667 (esperado 48.6667)
  [ok ] factor arcilloso: 109.5000 (esperado 109.5000)
  [ok ] cal libre => efectivo=0: 0.0000 (esperado 0.0000)
  [ok ] composta (kg): 19.5000 (esperado 19.5000)
  …
AUTOPRUEBA: TODO OK
```

### Cómo está diseñado

- **Las constantes traen su cita** en el encabezado del archivo (CSU, Clemson, UF/IFAS, USU) y en `M01 - La tierra`.
- **Los supuestos están marcados como supuestos** (densidad aparente por textura, 30% de MO en la composta, 50% estabilizada el primer año) — no se disfrazan de datos de literatura.
- **La autoprueba fija los valores** de cada fórmula contra valores conocidos. Si se cambia una constante, la autoprueba avisa.
- **Con cal libre el script se niega** a dar una dosis y explica por qué: la herramienta incorpora la conclusión agronómica, no solo la aritmética.

### Cómo se extiende (pendiente)

- Subcomando `yeso` para enmienda de estructura en arcillas sódicas.
- Salida `--json` para pegar la fila directo al registro.
- Lectura del CSV para graficar la serie (sin librerías externas: SVG dibujado a mano).
- El mismo patrón para los módulos siguientes: `riego.py` ([[M03 - El agua]]) y `costeo.py` ([[M08 - Los números del ciclo]]).

### Actividad 12.8 (parte de suelo)

- [ ] Corre el script con tus números y verifica que el resultado coincide con lo que calculaste a mano en el módulo 1.
- [ ] Cambia una constante a propósito y mira cómo la autoprueba falla. Eso es lo que protege los cálculos.
- [ ] Escribe una extensión propia (aunque sea una línea de salida extra) y hazla pasar la autoprueba.

---

## Tarea del módulo (parcial: cubre la parte de suelo)

**Entregable hasta aquí, para el expediente de suelo de [[M01 - La tierra]]:**

1. `registro_suelo.csv` en marcha: al menos las filas de la cama y de dos puntos de la parcela, con coordenadas, método de pH anotado y carbonatos.
2. Croquis medido y a escala, con superficies reales y los puntos de muestreo numerados.
3. Una gráfica propia de MO o de costo por m², con su lectura escrita (qué muestra y qué no).
4. Al menos una medición de campo verificada contra laboratorio, con la diferencia anotada como error de método.
5. El script corriendo con tus números, con la autoprueba en verde y una extensión propia.

**Criterio de éxito:** los números del suelo salen de un sistema propio que otra persona podría usar, y alguna tarea repetitiva (calcular dosis, armar la plantilla) dejó de hacerse a mano.

**Pendiente para completar el módulo:** 12.3 automatización del riego (con [[M03 - El agua]]), 12.6 trazabilidad e inocuidad (con [[M07 - La cosecha y el después]]), 12.7 pronóstico y decisión (con [[M09 - El mercado y el cliente]]).

## Notas por crear

- [[Registro digital del ciclo]] — estructura de datos, captura y respaldo (el detalle de 12.1) **← ya esbozado aquí**
- [[Sensores y medición automatizada]] — qué comprar, cuánto cuesta, cómo se calibra
- [[Levantamiento y medición de la parcela]] — croquis, GPS, superficies reales **← ya esbozado aquí**
- [[Análisis de rendimiento por m²]] — gráficas propias y errores de conclusión a evitar **← ya esbozado aquí**
- [[Automatización de riego]] — timer, válvulas, control por humedad: costo y riesgos
- [[Trazabilidad - qué pide un comprador serio]] — lote, fecha, insumo, registro

## Referencias disponibles

- Ya en el repositorio: [`Huerta/Experimentos`](../Huerta/Experimentos.md) (formato de prueba de una variable), [[M08 - Los números del ciclo]] (estructura de costos), [[M01 - La tierra]] (las constantes que usa el script y las fuentes de los precios)
- Falta buscar al escribir el resto: especificaciones de sensores de humedad y tensiómetros accesibles en México, controladores de riego, apps de medición de terreno, ejemplos publicados de bitácoras agrícolas digitales de pequeños productores

[1] Medidor de suelo 4 en 1 — Amazon México (precio de marketplace, verificado 2026-10-04): <https://www.amazon.com.mx/Medidor-Temperatura-Humedad-Intensidad-Jardiner%C3%ADa/dp/B0BGS6TXXZ>
[2] Hanna HI98107 — Hulk Scientific, $1,364.16 (verificado 2026-10-04): <https://hulkscientific.com.mx/products/hi98107-medidor-de-ph-0-0-14-0-digital-de-bolsillo-rojo-hanna>
[3] Hanna HI98103 — Grow Depot México, $1,513 (verificado 2026-10-04): <https://growdepotmexico.com/producto/medidor-de-bolsillo-de-ph-hanna-instruments/>
[4] OHAUS Starter ST10 — Mercalab, $1,613.22 (verificado 2026-10-04): <https://mercalab.com/products/medidor-ph-bolsillo-verificacion-0-1ph-st10-ohaus-30073970>
[5] Kit LaMotte 5928-01 — Hydrocultura, $16,033 (verificado 2026-10-04): <https://hydrocultura.com/products/lamotte-5928-01-kit-profesional-de-analisis-de-suelo>
[6] KITSOIL pH y CE directos de suelo — Proain, $16,273.57 (verificado 2026-10-04): <https://proain.com/products/kit-de-medidores-de-ph-y-ec-directos-de-suelo-kitsoil>
[7] Sensor de humedad YL-69 — Megacentral, $239 (verificado 2026-10-04): <https://megacentral.com.mx/product/sensor-de-humedad-de-suelo-yl-69-para-arduino-y-pic-monitoreo-preciso-y-automatizacion-de-riego-modelo-baq75u2-ideal-para-jardineria-inteligente/>
[8] Tensiómetro Irrometer SR 15 cm — Proain, $2,322.67 + IVA (verificado 2026-10-04): <https://proain.com/products/tensiometro-sr-diferentes-medidas>
[9] Tensiómetro Irrometer Modelo R 15 cm — Kosmos Scientific, $2,412.62 + IVA (verificado 2026-10-04): <https://www.kosmos.com.mx/tienda/catalog/irrometer-tensiometers-15cm-inch-model-pr-2026.html>

Referencias de método (citadas en el texto): CSU Extension GardenNotes #222 (kits caseros en suelo alcalino) <https://cmg.extension.colostate.edu/Gardennotes/222.pdf> · UGA Extension Circular 875 (pH en agua vs CaCl₂ y variación por sales) <https://fieldreport.caes.uga.edu/publications/C875/soil-testing-soil-ph-and-salt-concentration> · Scielo Chile 2007 (el caso de 5.2% de carbonatos) <https://scielo.conicyt.cl/pdf/agrtec/v67n2/at07.pdf>

## Cierra cuando

La tarea está entregada y el sistema de registro sigue en uso al ciclo siguiente, ya sin trabajo manual que sobre.

**Aporta a:** todos los módulos, en particular [[M01 - La tierra]], [[M03 - El agua]], [[M07 - La cosecha y el después]], [[M08 - Los números del ciclo]] y [[M13 - La parcela como sistema]].
