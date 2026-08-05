# Paletas de color

La página se colorea entera desde variables CSS. Cambiar la paleta = cambiar esas variables, nada más.

## Dónde se cambian
En el HTML, dentro del bloque `#cm-wrap{ ... }` están todas las variables:

```
--primary        color de marca principal (acentos, dots, barras)
--primary-light  variante clara del primary
--primary-dark   fondos oscuros / marrón base
--accent         dorado/secundario (precios, pills, badges)
--accent-light   variante clara del accent (precios grandes)
--accent-deep    variante intensa del accent
--black          texto más oscuro
--black-light    marrón intermedio
--cream          fondo claro principal
--cream-warm     fondo claro alterno
--gray / --dark-gray   textos secundarios
--success        verde (checks, "gratis", garantía)
--danger         rojo/rosa (dolores, tachados)
```

El carrito lateral usa su propio `:root{ --org / --grn / --bg / --card / --bdr ... }`. El `--org` del carrito debe igualar al `--accent` de la página; los verdes (`--grn`) del botón de compra normalmente se dejan (verde = convierte).

## Cómo proponer paletas
Ofrece 3-4 opciones nombradas, cada una con los hex de las variables clave (primary, primary-dark, accent, accent-light, cream, cream-warm) y una frase de para qué encaja. Deriva la paleta del nicho/marca:

- **Salud / bienestar / clínico:** verdes salvia + dorado + crema (la base de la plantilla).
- **Finanzas / negocios / alto ticket:** azul marino/petróleo + dorado + gris claro.
- **Belleza / femenino:** malva/burdeos + rosa dorado + nude.
- **Fitness / masculino / energía:** negro/grafito + naranja o lima + gris.
- **Espiritual / coaching:** morado/índigo + oro + marfil.

Reglas: mantén buen contraste (texto oscuro sobre cream, texto claro sobre dark); el `--success` casi siempre verde y el `--danger` casi siempre rojo/rosa (son señales universales); el CTA de compra suele quedarse verde aunque cambie la marca. Muestra las opciones como muestras (los hex) para que el usuario elija por número.

## Cómo aplicar
Al elegir el usuario, reemplaza SOLO los valores de las variables en `#cm-wrap{...}` (y `--org`/`--bg`/`--card`/`--bdr` del `:root` del carrito para que combine). No toques selectores ni reglas. Verifica contraste en las secciones `bg-dark` (texto claro) y `bg-cream/bg-warm` (texto oscuro).
