# Checklist de reemplazo — plantilla-base.html

La plantilla usa dos tipos de marcadores. Reemplázalos TODOS. Al terminar, no debe quedar ninguno.

- `REEMPLAZAR_*` → texto de copy o dato técnico.
- `IMG_*` → URL de imagen. Deja el mismo identificador en el HTML y en el documento de prompts, para emparejar 1:1. Si aún no hay imágenes, deja el `IMG_*` tal cual y avisa al usuario.

Verificación rápida al final (en bash):
`grep -n "REEMPLAZAR" pagina-venta-*.html` y `grep -n "IMG_" pagina-venta-*.html` no deben devolver nada inesperado.

## A. Cabecera y meta
- `REEMPLAZAR_TITLE`, `REEMPLAZAR_SUBTITULO` en `<title>`.
- `window.pixelId = "69d090e5cb8ccca5df6420f3"` → poner el pixel real de Utmify del usuario, o borrar el bloque `<script>` del pixel si no usa Utmify.

## B. Hero
- `REEMPLAZAR_HERO_TITULAR` + `REEMPLAZAR_SUBRAYADO` (dentro de `<u>`).
- `REEMPLAZAR_HERO_SUBTITULO` (promesa en una frase).
- `REEMPLAZAR_NOMBRE_PRODUCTO` (aparece muchas veces en toda la página — reemplaza todas).
- `REEMPLAZAR_DESCRIPCION_PRODUCTO_1_PARRAFO`.
- `IMG_HERO` (se usa en hero, carrito, oferta principal y oferta final: mismo archivo).
- `REEMPLAZAR_TITULO_DOLOR`, `REEMPLAZAR_DOLOR_1..5`.
- `REEMPLAZAR_TITULO_GANANCIA`, `REEMPLAZAR_GANANCIA_1..5`, `REEMPLAZAR_PRUEBA_SOCIAL_CIFRA`.
- `REEMPLAZAR_NOTA_CIERRE_HERO`.

## C. Cómo funciona
- `REEMPLAZAR_EYEBROW`, `REEMPLAZAR_TITULO_COMO_FUNCIONA`, `REEMPLAZAR_INTRO_COMO_FUNCIONA`.
- `REEMPLAZAR_PASO_1..3_TITULO` y `_TEXTO`.

## D. Sobre el producto
- `REEMPLAZAR_TITULO_SOBRE`, `REEMPLAZAR_SOBRE_1..5_*`. Ajusta el conteo "N bonos + N regalos".

## E. Comparativa
- `REEMPLAZAR_TITULO_COMPARATIVA`, `REEMPLAZAR_COL1/COL2`, `REEMPLAZAR_PRODUCTO_CORTO`, `REEMPLAZAR_FILA_1..4`.
- `$PRECIO_HOY` en la celda resaltada.

## F. Features + Autoridad
- `REEMPLAZAR_TITULO_FEATURES`, `REEMPLAZAR_INTRO_FEATURES`.
- `REEMPLAZAR_FEATURE_1..6_TITULO` y `_TEXTO`.
- `REEMPLAZAR_AUTORIDAD_LABEL/TITULO/SUB`, `REEMPLAZAR_NOMBRE_1..4` (o quita pills si no aplica).

## G. Mecanismo
- `REEMPLAZAR_EYEBROW_MECANISMO`, `REEMPLAZAR_TITULO_MECANISMO`, `REEMPLAZAR_INTRO_MECANISMO`.
- `REEMPLAZAR_MEC_1..3_TITULO` y `_TEXTO`, `REEMPLAZAR_CIERRE_MECANISMO`.

## H. Cita y vistazo dentro
- `REEMPLAZAR_CITA`, `REEMPLAZAR_ATRIBUCION_CITA`.
- `REEMPLAZAR_TITULO_VISTAZO`, `REEMPLAZAR_INTRO_VISTAZO`.
- `IMG_PREVIEW_01..04`.

## I. Bonos y regalos (crítico para la coherencia)
- Duplica el bloque `.bonus-card-item` hasta tener uno por cada bono y regalo. Cambia por bloque: número ("Bono 0X"/"Regalo 0X"), label ("Bono"/"Regalo"), `«REEMPLAZAR_BONO_XX_TITULO»`, `REEMPLAZAR_BONO_XX_DESCRIPCION`, valor `$XX`, e `IMG_BONO_XX` / `IMG_REGALO_XX`.
- El bloque `.gift-block` resume: ajusta "N Bonos + N Regalos" y `$PRECIO_ANTES` (valor total).

## J. Oferta principal (value stack + precio)
- `REEMPLAZAR_BADGE_BESTSELLER`, `REEMPLAZAR_ETIQUETA_PRODUCTO`, `REEMPLAZAR_SUBTITULO_PRODUCTO`, `REEMPLAZAR_PROMESA_OFERTA`.
- Value stack: `REEMPLAZAR_PRODUCTO_CORTO`, `REEMPLAZAR_RESUMEN_NUCLEO`, una fila `.value-stack-row` por cada bono/regalo (título + `$XX.00`), última con `super`. **La suma de valores debe cuadrar con `$PRECIO_ANTES`.**
- `$PRECIO_ANTES`, `$PRECIO_HOY`, `$AHORRO`, `XX% dto.` (coherentes en toda la página).
- `REEMPLAZAR_TEXTO_URGENCIA_PRECIO`, `REEMPLAZAR_AUDIENCIA`.
- `IMG_GARANTIA` (badge de garantía; se usa aquí y en la sección de garantía).
- `REEMPLAZAR_CTA_PRINCIPAL`.

## K. Para quién / Qué descubrirás
- `REEMPLAZAR_PARA_QUIEN_1..5`, `REEMPLAZAR_DESCUBRIRAS_1..5`.

## L. Autor, estadísticas, testimonios, reseñas
- `IMG_AUTOR`, `REEMPLAZAR_AUTOR_NOMBRE/ROL/HISTORIA`, `REEMPLAZAR_CRED_1..3`.
- `REEMPLAZAR_STAT_1/STAT_2` (los `data-target` numéricos puedes ajustarlos).
- `REEMPLAZAR_TITULO_TESTIMONIOS`, `IMG_TESTIMONIO_01..04`, `REEMPLAZAR_TESTIMONIO_1..4`, `REEMPLAZAR_NOMBRE_1..4`, `REEMPLAZAR_LINEA_PRUEBA`.
- Reseñas: `REEMPLAZAR_N valoraciones`, y por reseña `REEMPLAZAR_NOMBRE/TITULO_RESENA/FECHA/RESENA_1..3`. Los avatares usan randomuser.me (puedes dejarlos o cambiarlos).

## M. Beneficios, garantía, objeciones, FAQ
- `REEMPLAZAR_DETALLE` (beneficios), `REEMPLAZAR_TEXTO_GARANTIA`.
- `REEMPLAZAR_RAZON_1/2`, `REEMPLAZAR_OBJECION_1..4` + `REEMPLAZAR_RESPUESTA_1..4`.
- `REEMPLAZAR_FAQ_1..5_PREGUNTA` y `_RESPUESTA` (hay 2 FAQ fijas de pago/garantía que puedes ajustar).

## N. Oferta final y P.D.
- `REEMPLAZAR_PD_1`, `REEMPLAZAR_PD_2`.
- Precios `$PRECIO_HOY` / `$PRECIO_ANTES` en la oferta final.

## O. Prueba social flotante (toast)
- `IMG_TOAST_01..03` (fotos pequeñas de producto/personas) y `REEMPLAZAR_NOMBRE_CIUDAD_1..3`. Puedes añadir más entradas a los arrays `imgs` y `people`.

## P. Footer
- `REEMPLAZAR_DISCLAIMER_LEGAL` (importante en nichos sensibles).

## Q. CONFIGURACIÓN TÉCNICA (bloque JS al final)
Localiza el comentario `CONFIGURACION DE PRECIOS Y CHECKOUT` y ajusta:
- `MAIN_PRICE` = precio hoy en **centavos** (p.ej. $19.99 → `1999`).
- `MAIN_COMPARE` = precio antes en centavos (p.ej. $245.00 → `24500`).
- `BUMP_PRICES` = array `[[precio,compare], ...]` en centavos, uno por order bump. Debe coincidir en número con los bloques `.cpc-bump` del carrito.
- `CHECKOUT_DOMAIN` = `https://tu-tienda.myshopify.com` o dominio propio de Shopify.
- `MAIN_VARIANT_ID` = ID numérico de variante del producto principal en Shopify.
- En cada `.cpc-bump`: `data-variant="..."` (ID de variante del bump) y `data-price="..."` (centavos). Ajusta también `REEMPLAZAR_BUMP_0X_TITULO/DESCRIPCION` y `IMG_BUMP_0X`.
- Si el usuario no tiene aún los variant IDs, deja los `REEMPLAZAR_VARIANT_*` y avísale: la página funciona, pero el botón de checkout no llevará al carrito correcto hasta ponerlos.
- Si NO es Shopify: el checkout hace fallback a `CHECKOUT_DOMAIN + '/cart/<ids>'`. Para otra pasarela, sustituye la función `cpcGoCheckout` por un simple `window.location.href = 'URL_DE_TU_CHECKOUT'`.
- Si hay menos/más de 2 order bumps: añade o elimina bloques `.cpc-bump` (con id `b0`, `b1`, `b2`...) y ajusta `BUMP_PRICES` para que tengan la misma longitud.

## Coherencia numérica (revisión final obligatoria)
El mismo precio hoy, precio antes, ahorro y % deben aparecer idénticos en: `#cm-bar` (implícito), value stack, offer-box (2 veces), carrito (`cpc-main-compare`, `cpc-main-price`, `cpc-main-badge`), `gift-block`, y P.D. Además `MAIN_PRICE`/`MAIN_COMPARE` en el JS deben corresponder a esos mismos números.
