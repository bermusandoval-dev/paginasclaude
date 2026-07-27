# MetalMaster (MM) — catálogo de planos de metalistería

Gemelo en metal de WoodMaster 900: **1.200 planos** de herrería/metalistería
para vender como PDFs de 4 páginas (A4, 300 dpi, 100 % en inglés). Modelo de
negocio: catálogo Shopify, entrega vía Google Drive.

Este repo contiene, por ahora, **el motor de datos** (paso 1 de la disciplina
de producción): genera y valida el catálogo antes de producir una sola imagen.

## Estado actual

| Cosa | Estado |
|------|--------|
| Catálogo | ✅ 1.200 planos, `MM-0001`…`MM-1200`, 8 familias × 150 |
| Dificultad | ✅ 400 Beginner / 400 Intermediate / 400 Advanced (por ranking) |
| Política Principiante | ✅ **sin soldadura** (atornillado / plegado / remachado) |
| Validación geométrica | ✅ 0 fallos (`validar.py`) |
| Auditoría de similitud | ✅ 0 pares de gemelos intercambiables (`auditar_similitud.py`) |
| Imágenes / SVG / PDF | ⏳ pendiente (fase 2) |

## Familias e IDs

| Familia | Arquetipo | Rango |
|---------|-----------|-------|
| Workbenches & Work Tables | `banco` | MM-0001…0150 |
| Industrial Shelving & Racks | `estanteria` | MM-0151…0300 |
| Tool Racks & Wall Organizers | `rack_pared` | MM-0301…0450 |
| Shop Carts & Trolleys | `carrito` | MM-0451…0600 |
| Stands & Holders | `soporte` | MM-0601…0750 |
| Metal-Frame Tables (Wood Top) | `mesa_madera` | MM-0751…0900 |
| BBQ, Grills & Fire Pits | `parrilla` | MM-0901…1050 |
| Coat / Shoe Racks & Entry | `perchero` | MM-1051…1200 |

Cada familia tiene **15 subcategorías** (temas de propósito/tamaño, neutrales
de construcción) × **10 planos**. Cada plano recibe **1 de 5 variantes**
constructivas reales (unión, despiece, herrajes y herramientas cambian).

## Arquitectura de código

- **`datos_metal.py`** — configuración maestra: familias, subcategorías,
  acabados, desbastes, herramientas base, bloques de seguridad, escenas.
  Nada que se imprima cambia por reordenar este archivo.
- **`arquetipos.py`** — geometría de los 8 arquetipos. Por arquetipo:
  `DIMS[arq](rng)` (dimensiones), `VARIANTES[arq]` (5 variantes con
  `label/weld/union/vistas`) y `build(arq, d, vkey)` (despiece completo +
  posiciones clave en mm + ángulos por `atan2` + detalle ampliado + herrajes).
  Las notas de cada pieza llevan las palabras clave que dispararán los iconos
  de **forma real** en la página 3 (`tube`, `mitred`, `drilled plate`,
  `folded`, `mesh`, `round rod`, `cut at N deg`…).
- **`catalogo.py`** — orquestador. Escribe `catalogo.json`.
- **`validar.py`** — cierres geométricos independientes por arquetipo/variante.
- **`auditar_similitud.py`** — antídoto contra "todas las hojas iguales".
- **`estabilidad.py`** — snapshot + diff (regla dura: nunca romper entregados).
- **`exportar.py`** — export maestro a CSV (y XLSX si hay `openpyxl`).

### Reglas duras de estabilidad (heredadas de WoodMaster)

1. **Dimensiones con RNG estable por proyecto**:
   `Random(f"{PROYECTO_SEED}|{subcat}|{i}")`. Regenerar el catálogo **nunca**
   cambia un plano ya entregado.
2. **Variantes por mazo barajado por subcategoría**:
   `Random(f"DECK|{subcat}")` sobre `(base * k)[:n]`. Añadir variantes **al
   final** del deck no altera repartos hechos. ⚠️ Renombrar una subcategoría
   **sí** cambia su semilla (reparto y dimensiones): hacerlo solo antes de
   entregar.
3. **Acabado + desbaste** se eligen para que dos gemelos (misma subcat+variante)
   **siempre difieran** → la auditoría de similitud pasa por construcción.
4. **Dificultad por ranking** de score en percentiles, con la política
   *Principiante == sin soldadura*.
5. Antes de tocar `catalogo.py` con planos entregados: `estabilidad.py
   snapshot X` → editar → `estabilidad.py diff X` (0 cambios críticos). La
   dificultad puede moverse por el re-ranking: esos IDs se re-ensamblan (solo
   el footer).

## Uso

```bash
python catalogo.py           # -> catalogo.json (1200 planos)
python validar.py            # cierres geométricos: meta 0 fallos
python auditar_similitud.py  # gemelos no intercambiables
python exportar.py           # -> catalogo_maestro.csv
```

## Identidad visual (para la fase de SVG/PDF)

Fondo blanco, acento naranja `#FF7A1A`, texto carbón. Sans limpia. Franja
naranja de 10 px al pie. Footer: `MetalMaster` + `MM-XXXX · Page N of 4`.

## Próximos pasos (fase 2)

1. Pilotos: 8 planos (1 por familia) de dificultad alta → PDF completo →
   revisión honesta (¿un comprador construye sin adivinar?).
2. Generadores SVG (`materiales_svg`, `planos_svg`, `armado_svg`), pipeline de
   imágenes (Higgsfield / Nano Banana Pro), `ensamblar.py` (en Linux:
   `cairosvg`/Chromium, no Edge headless).
