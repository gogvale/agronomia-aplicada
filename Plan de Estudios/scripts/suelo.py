#!/usr/bin/env python3
"""suelo.py — calculadora determinista para el expediente de suelo.

Cálculos, no opiniones: dosis de enmienda, costo por unidad de pH y plantilla de
registro. Toda constante viene citada en el módulo M01 (`Plan de Estudios/M01 - La tierra.md`)
y en `Huerta/Suelo - textura, pH y enmiendas.md`; aquí solo se hacen las cuentas.

Uso:
    python3 suelo.py azufre --ancho 3 --largo 0.5 --profundidad 15 \
        --ph-actual 8.0 --ph-objetivo 6.5 --textura migajon --cal-libre no \
        --precio-kg 32
    python3 suelo.py composta --ancho 3 --largo 0.5 --profundidad 20 \
        --mo-actual 1.0 --mo-objetivo 3.0 --precio-kg 1.2
    python3 suelo.py cal                            # qué implica la cal libre
    python3 suelo.py plantilla --salida registro_suelo.csv
    python3 suelo.py autoprueba

Sin dependencias. Python 3.8+.
"""

from __future__ import annotations

import argparse
import csv
import sys

# --- Constantes citadas (ver módulo M01) -----------------------------------
# Azufre elemental para bajar una unidad de pH, en suelo migajón:
#   650 lb/acre  -> 73 g/m2   (CSU Extension, Changing Soil pH)
#   0.2 lb/10 ft2 -> 98 g/m2  (Clemson HGIC 1650, 7.5 -> 6.5)
G_M2_POR_PH_MIN = 73.0
G_M2_POR_PH_MAX = 98.0

# Corrección por textura (Clemson: reducir un tercio en arenoso, aumentar la mitad en arcilloso)
FACTOR_TEXTURA = {
    "arenoso": 2.0 / 3.0,
    "migajon": 1.0,
    "arcilloso": 1.5,
}

# Densidad aparente típica (g/cm3) — supuesto de cálculo, editable con --densidad
DENSIDAD_APARENTE = {
    "arenoso": 1.5,
    "migajon": 1.3,
    "arcilloso": 1.15,
}

# Cal libre: 2% de carbonatos en los primeros 15 cm ~ 20 t de cal/acre y
# neutralizarlas pide ~6.5 t de azufre elemental/acre (CSU Extension).
T_CAL_POR_ACRE_2PCT_15CM = 20.0
T_AZUFRE_POR_ACRE_2PCT_15CM = 6.5
M2_POR_ACRE = 4046.86

# Composta: supuestos explícitos, no constantes de literatura.
OM_COMPOSTA_FRACCION = 0.30      # 30% del peso seco de composta es materia orgánica
OM_ESTABILIZADA_ANIO1 = 0.50     # la mitad de esa MO se estabiliza el primer año


def masa_suelo_kg(area_m2: float, profundidad_cm: float, densidad_g_cm3: float) -> float:
    """Masa de suelo de una capa, en kg. 1 m2 x 1 cm = 0.01 m3."""
    return area_m2 * (profundidad_cm / 100.0) * 1000.0 * densidad_g_cm3


def dosis_azufre(area_m2, profundidad_cm, ph_actual, ph_objetivo, textura, cal_libre, densidad=None):
    delta = max(0.0, ph_actual - ph_objetivo)
    factor = FACTOR_TEXTURA[textura]
    dens = densidad if densidad is not None else DENSIDAD_APARENTE[textura]
    # El factor de profundidad es lineal sobre la referencia de 15 cm
    prof_factor = profundidad_cm / 15.0
    g_m2_min = G_M2_POR_PH_MIN * factor * prof_factor
    g_m2_max = G_M2_POR_PH_MAX * factor * prof_factor
    return {
        "delta_ph": delta,
        "efectivo": (not cal_libre) and delta > 0,
        "g_m2_por_unidad_ph_min": g_m2_min,
        "g_m2_por_unidad_ph_max": g_m2_max,
        "g_m2_min": g_m2_min * delta,
        "g_m2_max": g_m2_max * delta,
        "kg_min": g_m2_min * delta * area_m2 / 1000.0,
        "kg_max": g_m2_max * delta * area_m2 / 1000.0,
        "masa_suelo_kg": masa_suelo_kg(area_m2, profundidad_cm, dens),
        "densidad_usada": dens,
    }


def costo(kg, precio_kg):
    return None if precio_kg is None else kg * precio_kg


def cal_free_perspectiva(area_m2, profundidad_cm):
    """Cuánto azufre pediría neutralizar 2% de cal en la capa dada."""
    ratio_acre = area_m2 / M2_POR_ACRE
    cal_t = T_CAL_POR_ACRE_2PCT_15CM * ratio_acre * (profundidad_cm / 15.0)
    azufre_t = T_AZUFRE_POR_ACRE_2PCT_15CM * ratio_acre * (profundidad_cm / 15.0)
    return {"cal_t": cal_t, "azufre_t": azufre_t, "azufre_kg": azufre_t * 1000.0}


def composta_para_mo(area_m2, profundidad_cm, mo_actual_pct, mo_objetivo_pct, textura, densidad=None):
    dens = densidad if densidad is not None else DENSIDAD_APARENTE[textura]
    masa = masa_suelo_kg(area_m2, profundidad_cm, dens)
    delta_pct = max(0.0, mo_objetivo_pct - mo_actual_pct)
    om_kg = masa * (delta_pct / 100.0)
    composta_kg = om_kg / (OM_COMPOSTA_FRACCION * OM_ESTABILIZADA_ANIO1)
    return {
        "masa_suelo_kg": masa,
        "om_necesaria_kg": om_kg,
        "composta_kg": composta_kg,
        "composta_t": composta_kg / 1000.0,
        "supuestos": f"composta {OM_COMPOSTA_FRACCION:.0%} de MO seca, "
                     f"{OM_ESTABILIZADA_ANIO1:.0%} estabilizada el primer año",
    }


def fila_registro(**kw):
    return {k: v for k, v in kw.items() if v is not None}


def plantilla_csv(path):
    campos = ["fecha", "punto", "lat", "lon", "profundidad_cm", "textura_tacto",
              "vinagre", "ph_agua", "ph_cacl2", "ph_buffer", "mo_pct", "ce_ds_m",
              "n_ppm", "p_ppm", "k_ppm", "carbonatos_pct", "enmienda", "dosis_g_m2",
              "costo_mxn", "nota"]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerow(campos)
    return path, campos


def cmd_azufre(a):
    r = dosis_azufre(a.ancho * a.largo, a.profundidad, a.ph_actual, a.ph_objetivo,
                     a.textura, a.cal_libre, a.densidad)
    area = a.ancho * a.largo
    print(f"Área: {area:.2f} m² · profundidad {a.profundidad:g} cm · textura {a.textura} "
          f"(densidad {r['densidad_usada']:g} g/cm³)")
    print(f"Masa de suelo de esa capa: {r['masa_suelo_kg']:.0f} kg")
    print(f"pH {a.ph_actual:g} → {a.ph_objetivo:g} (Δ {r['delta_ph']:.1f})")
    if a.cal_libre:
        cal = cal_free_perspectiva(area, a.profundidad)
        print("\n⚠ CAL LIBRE DETECTADA: no se calcula dosis de azufre.")
        print(f"   Solo la cal de esa capa equivale a ~{cal['cal_t']:.2f} t de cal, y su")
        print(f"   neutralización pediría ~{cal['azufre_kg']:.0f} kg de azufre")
        print("   (referencia: 2% de cal en 15 cm ~ 20 t de cal/acre y ~6.5 t de azufre/acre).")
        print("   Acción correcta: no enmendar el terreno; trabajar la zona de raíces")
        print("   (cama/maceta), manejar el riego y corregir clorosis férrica.")
        return 0
    if r["delta_ph"] <= 0:
        print("El pH objetivo no es menor que el actual: no hay nada que bajar.")
        return 0
    print(f"Dosis: {r['g_m2_min']:.0f}–{r['g_m2_max']:.0f} g/m² "
          f"({r['g_m2_por_unidad_ph_min']:.0f}–{r['g_m2_por_unidad_ph_max']:.0f} g/m² por unidad de pH)")
    print(f"Total: {r['kg_min']:.2f}–{r['kg_max']:.2f} kg de azufre elemental")
    if a.precio_kg:
        c1, c2 = costo(r["kg_min"], a.precio_kg), costo(r["kg_max"], a.precio_kg)
        print(f"Costo: ${c1:,.0f}–${c2:,.0f} MXN a ${a.precio_kg:g}/kg")
        print(f"Costo por unidad de pH: ${c1/r['delta_ph']:,.0f}–${c2/r['delta_ph']:,.0f} MXN")
    print("Incorporar a los primeros 15 cm, en temporada cálida, y remedir a los 3-4 meses.")
    return 0


def cmd_composta(a):
    r = composta_para_mo(a.ancho * a.largo, a.profundidad, a.mo_actual, a.mo_objetivo,
                         a.textura, a.densidad)
    print(f"Masa de suelo de la capa: {r['masa_suelo_kg']:.0f} kg")
    print(f"MO {a.mo_actual:g}% → {a.mo_objetivo:g}%: hacen falta {r['om_necesaria_kg']:.1f} kg de MO")
    print(f"Composta necesaria: {r['composta_kg']:.0f} kg ({r['composta_t']:.2f} t)")
    print(f"Supuestos: {r['supuestos']} — es estimación, no dato de laboratorio.")
    if a.precio_kg:
        print(f"Costo: ${r['composta_kg']*a.precio_kg:,.0f} MXN a ${a.precio_kg:g}/kg")
    return 0


def cmd_cal(a):
    cal = cal_free_perspectiva(a.ancho * a.largo, a.profundidad)
    print(f"Para {a.ancho*a.largo:.2f} m² × {a.profundidad:g} cm, si hubiera 2% de cal:")
    print(f"  cal en la capa: ~{cal['cal_t']:.3f} t")
    print(f"  azufre para neutralizarla: ~{cal['azufre_kg']:.0f} kg "
          f"({cal['azufre_t']:.3f} t)")
    print("  Referencia: 2% de cal en los primeros 15 cm ~ 20 t de cal/acre y ~6.5 t de azufre/acre.")
    print("  Conclusión: en suelo calcáreo el azufre no es herramienta de terreno.")
    return 0


def cmd_plantilla(a):
    path, campos = plantilla_csv(a.salida)
    print(f"Plantilla escrita en {path} con {len(campos)} columnas:")
    print("  " + ", ".join(campos))
    return 0


def autoprueba():
    ok = True

    def chk(nombre, obtenido, esperado, tol=1e-6):
        nonlocal ok
        bien = abs(obtenido - esperado) <= tol
        ok = ok and bien
        print(f"  [{'ok ' if bien else 'FALLA'}] {nombre}: {obtenido:.4f} (esperado {esperado:.4f})")

    # 1. Cama de 3 m x 0.5 m, 15 cm, migajón: masa de suelo
    chk("masa de suelo 1.5 m² × 15 cm × 1.3", masa_suelo_kg(1.5, 15, 1.3), 292.5, 1e-6)
    # 2. Dosis por unidad de pH en migajón, 15 cm, sin factor de profundidad
    r = dosis_azufre(1.5, 15, 8.0, 6.5, "migajon", False)
    chk("g/m² por unidad de pH (mín)", r["g_m2_por_unidad_ph_min"], 73.0, 1e-6)
    chk("g/m² por unidad de pH (máx)", r["g_m2_por_unidad_ph_max"], 98.0, 1e-6)
    # 3. ΔpH 1.5 y 1.5 m² -> 164.25 g … 220.5 g
    chk("kg totales (mín)", r["kg_min"], 73.0 * 1.5 * 1.5 / 1000.0, 1e-9)
    chk("kg totales (máx)", r["kg_max"], 98.0 * 1.5 * 1.5 / 1000.0, 1e-9)
    # 4. Textura arenosa = 2/3 de la dosis migajón
    ra = dosis_azufre(1.0, 15, 7.5, 6.5, "arenoso", False)
    chk("factor arenoso", ra["g_m2_min"], 73.0 * 2 / 3, 1e-9)
    # 5. Arcilloso = 1.5x
    rc = dosis_azufre(1.0, 15, 7.5, 6.5, "arcilloso", False)
    chk("factor arcilloso", rc["g_m2_min"], 73.0 * 1.5, 1e-9)
    # 6. Profundidad doble = dosis doble
    rp = dosis_azufre(1.0, 30, 7.5, 6.5, "migajon", False)
    chk("factor profundidad 30 cm", rp["g_m2_min"], 73.0 * 2, 1e-9)
    # 7. Con cal libre, la dosis no es efectiva
    rcal = dosis_azufre(1.0, 15, 8.0, 6.5, "migajon", True)
    chk("cal libre => efectivo=0", float(rcal["efectivo"]), 0.0, 1e-9)
    # 8. Perspectiva de cal: 1 acre aprox
    c = cal_free_perspectiva(M2_POR_ACRE, 15)
    chk("cal en 1 acre (t)", c["cal_t"], 20.0, 1e-6)
    chk("azufre en 1 acre (t)", c["azufre_t"], 6.5, 1e-6)
    # 9. Composta: subir 1% de MO en 1.5 m² × 15 cm migajón
    comp = composta_para_mo(1.5, 15, 1.0, 2.0, "migajon")
    chk("MO necesaria (kg)", comp["om_necesaria_kg"], 292.5 * 0.01, 1e-9)
    chk("composta (kg)", comp["composta_kg"], (292.5 * 0.01) / 0.15, 1e-9)
    # 10. Costo
    chk("costo 2 kg a $32", costo(2.0, 32.0), 64.0, 1e-9)

    print("AUTOPRUEBA:", "TODO OK" if ok else "HAY FALLAS")
    return 0 if ok else 1


def main(argv=None):
    p = argparse.ArgumentParser(description="Calculadora de suelo (determinista).")
    sub = p.add_subparsers(dest="cmd", required=True)

    def comunes(sp):
        sp.add_argument("--ancho", type=float, default=3.0, help="ancho en m (default 3)")
        sp.add_argument("--largo", type=float, default=0.5, help="largo en m (default 0.5)")
        sp.add_argument("--profundidad", type=float, default=15.0, help="cm (default 15)")
        sp.add_argument("--textura", choices=list(FACTOR_TEXTURA), default="migajon")
        sp.add_argument("--densidad", type=float, default=None, help="g/cm³ (default: según textura)")

    a1 = sub.add_parser("azufre", help="dosis de azufre elemental para bajar pH")
    comunes(a1)
    a1.add_argument("--ph-actual", type=float, required=True)
    a1.add_argument("--ph-objetivo", type=float, required=True)
    a1.add_argument("--cal-libre", action="store_true", help="la prueba del vinagre burbujeó")
    a1.add_argument("--precio-kg", type=float, default=None, help="MXN por kg de azufre")
    a1.set_defaults(func=cmd_azufre)

    a2 = sub.add_parser("composta", help="composta para subir materia orgánica")
    comunes(a2)
    a2.add_argument("--mo-actual", type=float, required=True, help="% de materia orgánica")
    a2.add_argument("--mo-objetivo", type=float, required=True)
    a2.add_argument("--precio-kg", type=float, default=None)
    a2.set_defaults(func=cmd_composta)

    a3 = sub.add_parser("cal", help="qué significa tener cal libre")
    comunes(a3)
    a3.set_defaults(func=cmd_cal)

    a4 = sub.add_parser("plantilla", help="escribe la plantilla CSV del registro")
    a4.add_argument("--salida", default="registro_suelo.csv")
    a4.set_defaults(func=cmd_plantilla)

    a5 = sub.add_parser("autoprueba", help="verifica los cálculos contra valores conocidos")
    a5.set_defaults(func=lambda a: autoprueba())

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
