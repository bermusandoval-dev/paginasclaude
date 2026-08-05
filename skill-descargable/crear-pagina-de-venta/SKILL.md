---
name: crear-pagina-de-venta
description: Arma páginas de venta directa completas (sales page / carta de venta larga) para productos digitales en Shopify — analiza HTML pegado, inserta la info del producto, propone paletas de color y recolorea, traduce y localiza (nombres de reseñas/testimonios/notificaciones según el idioma), genera prompts o imágenes de bonos/regalos, optimiza velocidad y responsive, y ensambla el HTML final (con order bump + JSON + pixel), normalmente 2 páginas. Úsala SIEMPRE que el usuario pegue el HTML de una página y pida analizarla/insertar info/traducirla/cambiar colores/optimizarla, pida "crear/armar la página de venta", "paleta de colores para la página", "prompts para las imágenes de los bonos", "traduce la página a X", "une el order bump y el pixel y dame la página lista", o pegue la URL de un producto pidiendo una página. Modos de entrada: (A) brief del producto, o (B) escaneo de URL.
---

# Crear Página de Venta Directa

Este skill cubre el flujo completo de producción de páginas de venta de productos digitales (estilo Shopify con carrito de order-bumps, countdowns, value stack, bonos, prueba social y FAQ). El objetivo es ahorrarle al usuario los pasos manuales: recibe el HTML + la info + el idioma + los datos técnicos, y devuelve **la(s) página(s) HTML final(es) lista(s) para subir**.

La plantilla base de referencia vive en `assets/plantilla-base.html`. **Nunca reescribas su CSS ni su JavaScript**: su maquetación, animaciones, carrito y optimizaciones ya están calibrados. Solo se reemplaza texto, imágenes, colores (variables CSS) y la configuración técnica.

## El flujo del usuario (11 pasos) y cómo ejecutarlo

El usuario suele trabajar así. Adáptate a en qué punto entra; puedes hacer varios pasos en un mismo turno.

1. **Copia el HTML de una página** y **lo pega** para que lo analices. → Trabaja sobre ESE HTML pegado (es su base real). Usa `assets/plantilla-base.html` solo como referencia de estructura/estilo si construyes desde cero (modo B / sin HTML).
2. **Analiza el HTML.** Identifica secciones, variables de color, bloques de bonos, value stack, config de checkout, pixel y placeholders. Reporta brevemente qué encontraste y qué falta.
3. **Inserta la información** que te pegue (producto, avatar, dolores, oferta, bonos, etc.). Aplica el framework de copy (`references/framework-copy.md`).
4. **Paletas de color.** Propón 3-4 paletas coherentes con la marca/nicho, cada una con sus hex (primary, primary-light, primary-dark, accent, accent-light, accent-deep, black, cream, cream-warm, success, danger). Ver `references/paletas-colores.md`.
5. **Cambia los colores.** Al elegir el usuario, sustituye SOLO las variables CSS en el bloque `#cm-wrap{...}` (y `:root` del carrito si aplica). Un cambio recolorea toda la página.
6. **Revisión.** El usuario revisa. Corrige lo que pida.
7. **Traduce** la página al idioma que indique. Traduce TODO el copy manteniendo estructura y clases intactas.
8. **Localiza** según el idioma: adapta los **nombres y ciudades** de las notificaciones flotantes (arrays `people`/`imgs` del toast), reseñas (`azr-*`) y testimonios (`sw-name`) a nombres/ciudades verosímiles del país destino (ej.: página en portugués → nombres y ciudades de Brasil; en inglés → EE. UU./UK). Traduce también fechas de reseñas y etiquetas ("Verificado", "Compra verificada", "Activa ahora", etc.).
9. **Actualiza** nombre del producto principal, bonos y regalos (títulos, descripciones, valores). Mantén la coherencia numérica del value stack y precios (ver checklist).
10. **Imágenes de bonos y bundle.** Dos modos disponibles (`references/prompts-imagenes.md`):
    - **Prompts:** entrega los prompts con la instrucción exacta del usuario (mockups en distintos escenarios/ambientes/formatos/dispositivos/ángulos, con el título del bono insertado, respetando la paleta) listos para pegar en ChatGPT.
    - **Generación directa:** si el usuario lo pide, genera las imágenes tú mismo (herramienta de generación conectada), con el título insertado y en la paleta, y entrégalas optimizadas en `.webp`.
11. **Optimiza** velocidad y responsive (`references/optimizacion.md`): imágenes a webp con `width`/`height` y lazy (preload solo el hero), iframes de video lazy, y verificación responsive en móvil/tablet/desktop.

**Paso final — Ensamblaje y entrega (normalmente 2 páginas).** El usuario suele pegar: el **HTML del order bump**, el **JSON de la página**, y el **pixel**. Une todo y entrega el/los HTML final(es):
- Inserta el pixel (Utmify u otro) en `window.pixelId` / el `<script>` correspondiente.
- Integra el/los order bump(s) en el carrito (`.cpc-bump` con su `data-variant`, `data-price`, título, descripción, imagen) y actualiza `BUMP_PRICES`.
- Aplica los datos del JSON (variant IDs, dominio de checkout, precios) a `CHECKOUT_DOMAIN`, `MAIN_VARIANT_ID`, `MAIN_PRICE`, `MAIN_COMPARE`.
- **Son 2 páginas:** el usuario pedirá el ensamblaje dos veces (dos productos/idiomas/variantes). Trata cada una como archivo independiente: `pagina-venta-<producto>-1.html` y `-2.html`. No mezcles sus datos.

## Modos de entrada
- **Modo A · Brief:** el usuario da la info. Si falta algo esencial, pídelo en una sola tanda.
- **Modo B · Escaneo de URL:** usa `mcp__workspace__web_fetch` (o navegador si es client-rendered) para extraer nombre, propuesta, tono, avatar, precio, bonos y ángulo.

En ambos, antes de escribir copy define: avatar, nivel de consciencia (Schwartz), dolor #1, deseo #1, mecanismo único y oferta.

## Archivos de referencia
- `references/framework-copy.md` — estrategia de copy (Schwartz, LF8, PAS) y fórmula por sección.
- `references/checklist-reemplazo.md` — mapa de TODO lo reemplazable + config técnica + coherencia numérica.
- `references/paletas-colores.md` — cómo proponer paletas y qué variables CSS cambiar.
- `references/prompts-imagenes.md` — instrucción exacta de imágenes, prompts y generación directa a webp.
- `references/optimizacion.md` — velocidad y responsive.

## Verificación (antes de entregar)
- Sin restos del nicho original ni placeholders `REEMPLAZAR_*` / `IMG_*` sin resolver (salvo los que el usuario deba completar; lístalos).
- Precios/ahorros/% idénticos en todas las secciones y en el JS (`MAIN_PRICE`/`MAIN_COMPARE`/`BUMP_PRICES`).
- Nº de bonos = filas del value stack = conteo del hero/oferta/P.D.
- Idioma consistente: copy + nombres/ciudades localizados + etiquetas traducidas.
- Cada `IMG_*` tiene su prompt o su imagen webp.
- Order bumps del carrito coinciden en número con `BUMP_PRICES` y tienen sus variant IDs.
- Si son 2 páginas, ambas coherentes por separado.

## Entrega
Presenta el/los HTML con `present_files` y resume en 2-3 frases qué producto, qué falta que complete el usuario (variant IDs, imágenes) y que ya está listo para subir a Shopify. No expliques todo el contenido.
