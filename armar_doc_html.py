"""
armar_doc_html.py — Genera el HTML de un plano para subirlo a Google Drive
como Google Doc con las imagenes embebidas.

Pipeline validado (sin egress del contenedor, sin transcribir binarios):
  1. Generar hero + grilla en Higgsfield a resolucion 2K (PNG). A 2K las dos
     imagenes entran bajo el limite del importador de Drive; a 4K solo entra
     una, y en .webp no entra ninguna.
  2. Construir el HTML con este modulo (usa data real del catalogo).
  3. Subir con Google_Drive.create_file (contentMimeType='text/html'): Google
     convierte a Doc y descarga/embebe las imagenes del CDN publico.

Los <img src> DEBEN apuntar al rawUrl (PNG) 2K del CDN de Higgsfield.
"""
import html

from armado_pasos import pasos_en


def _cm(mm):
    return f"{mm/10:.0f}"


def armar_html(plan, hero_url, grid_url):
    """Devuelve el HTML de un plano listo para subir como Google Doc."""
    e = html.escape
    d = plan["dims"]
    steps = pasos_en(plan)

    piezas_rows = "".join(
        f"<tr><td>{e(pz['ref'])}</td><td>{e(pz['nombre'])}</td><td>{pz['cantidad']}</td>"
        f"<td>{pz['largo']} mm</td><td>{pz['ancho']} mm</td><td>{e(pz['perfil'])}</td>"
        f"<td>{e(pz.get('nota',''))}</td></tr>"
        for pz in plan["piezas"])
    mat_items = "".join(f"<li>{e(m)}</li>" for m in plan["materiales"])
    herr_rows = "".join(
        f"<tr><td>{e(h['item'])}</td><td>{h['cantidad']}</td><td>{e(h['para_que'])}</td></tr>"
        for h in plan["herrajes"])
    tool_rows = "".join(
        f"<tr><td>{e(t['item'])}</td><td>{e(t['uso'])}</td></tr>"
        for t in plan["herramientas"])
    seg_items = "".join(f"<li>{e(s)}</li>" for s in plan["seguridad"])
    step_items = "".join(f"<li>{e(s)}</li>" for s in steps)

    mm_id = e(plan["id"])
    overall = (f'{d["length"]} x {d["depth"]} x {d["height"]} mm '
               f'({_cm(d["length"])} x {_cm(d["depth"])} x {_cm(d["height"])} cm)') \
        if all(k in d for k in ("length", "depth", "height")) else ""

    return f"""<h1>{mm_id} · {e(plan["titulo"])}</h1>
<p><b>Family:</b> {e(plan["familia"])} &nbsp;|&nbsp; <b>Difficulty:</b> {e(plan["dificultad"])} &nbsp;|&nbsp; <b>Finish:</b> {e(plan["acabado_label"])}</p>
<p><b>Overall size:</b> {overall}. Cut every part before assembly and label it by letter.</p>
<img src="{hero_url}" width="620"/>

<h2>1 · Materials &amp; Tools</h2>
<h3>Stock to buy</h3>
<ul>{mat_items}</ul>
<h3>Hardware</h3>
<table border="1" cellpadding="5" cellspacing="0">
<tr><th>Item</th><th>Qty</th><th>What for</th></tr>{herr_rows}</table>
<h3>Tools required</h3>
<table border="1" cellpadding="5" cellspacing="0">
<tr><th>Tool</th><th>Use</th></tr>{tool_rows}</table>

<h2>2 · Cut List</h2>
<table border="1" cellpadding="5" cellspacing="0">
<tr><th>Ref</th><th>Part</th><th>Qty</th><th>Length</th><th>Width</th><th>Profile</th><th>Note</th></tr>{piezas_rows}</table>
<p>All dimensions in millimetres. Measure your actual stock before cutting and adjust if it differs.</p>

<h2>3 · Assembly — step by step</h2>
<img src="{grid_url}" width="620"/>
<ol>{step_items}</ol>

<h2>4 · Safety</h2>
<ul>{seg_items}</ul>
<p style="color:#888"><i>MetalMaster 900 · {mm_id} · generated plan</i></p>
"""


if __name__ == "__main__":
    import json
    import sys

    plan = json.load(open("catalogo.json"))[0]
    hero = sys.argv[1] if len(sys.argv) > 1 else "HERO_2K_PNG_URL"
    grid = sys.argv[2] if len(sys.argv) > 2 else "GRID_2K_PNG_URL"
    sys.stdout.write(armar_html(plan, hero, grid))
