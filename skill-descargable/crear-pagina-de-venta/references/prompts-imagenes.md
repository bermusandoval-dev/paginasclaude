# Imágenes de bonos, regalos y bundle

Dos modos disponibles. Pregunta cuál quiere el usuario si no lo dice; por defecto entrega **prompts** (su flujo ChatGPT + Canva + webp).

## Instrucción base (usar SIEMPRE como núcleo del prompt)
> Crea las imágenes de los bonos y regalos. Debes insertar el título de cada bono y regalo en la imagen correspondiente. Crea imágenes de mockups en diferentes escenarios, ambientes, formatos, dispositivos (laptop, iPad, iPhone), ángulos, libretas, papeles, etc., manteniendo la paleta de colores de la página.

Cada imagen debe: (1) llevar el **título exacto** del bono/regalo visible en la portada/pantalla, (2) variar el escenario/dispositivo/ángulo respecto a las demás para que la galería no sea monótona, y (3) respetar la **paleta de la página** (pásale los hex reales de la paleta elegida).

## Modo 1 — Prompts (para pegar en ChatGPT)
Entrega `prompts-imagenes-<producto>.md`, un bloque por cada slot `IMG_*` del HTML, con este formato:

```
### IMG_BONO_01  → «Título del bono»
Ratio: 3:2 (1200×800)  ·  Escenario: laptop sobre escritorio de madera
Prompt: Professional 3D product mockup of a digital guide titled "«TÍTULO DEL BONO»" shown on a laptop screen on a warm wooden desk, [PALETA: verde oliva #586b2c, dorado #c9a877, crema #f5efe1] accents, soft studio lighting, cozy office ambience, high angle, photorealistic, the exact title text must appear crisp and correctly spelled, no gibberish.
Título a insertar: "«TÍTULO DEL BONO»"
```

Reparte los slots en escenarios/dispositivos variados para cubrir la instrucción:
- IMG_HERO / bundle → composición grupal (varios dispositivos + libretas + carpeta juntos).
- IMG_BONO_01 → laptop; 02 → iPad; 03 → iPhone; 04 → libreta/cuaderno impreso; 05 → papeles/hojas sueltas sobre mesa; 06 → tablet en mano; 07 → flat-lay cenital; 08 → pantalla en escritorio; regalos → variaciones similares.
- IMG_PREVIEW_01..04 → páginas interiores reales (índice, hoja de trabajo, guía, plantilla).
- IMG_GARANTIA → sello/badge. IMG_TESTIMONIO_* → tarjetas de reseña. IMG_TOAST_* → miniaturas. IMG_AUTOR → retrato.

Siempre añade al prompt: paleta con hex reales, "the title text must be spelled exactly and legibly / no gibberish text", y el título aparte en "Título a insertar" (los generadores suelen escribir mal el texto).

## Modo 2 — Generación directa a .webp
Si el usuario pide que las cree yo:
1. Genera cada imagen con la herramienta de generación conectada, usando los prompts anteriores (título insertado + paleta + escenario variado).
2. Descarga/guarda cada una y **conviértela a webp** dimensionada a su uso real (bonos ~600px ancho, hero ~1200px, badge/toast/bumps cuadrados pequeños). Ejemplo de conversión en bash:
   `python3 -c "from PIL import Image; im=Image.open('in.png').convert('RGB'); im.thumbnail((1200,1200)); im.save('IMG_BONO_01.webp','WEBP',quality=82)"`
3. Nombra cada archivo igual que su slot (`IMG_BONO_01.webp`, ...) y colócalo en el `src` correspondiente del HTML (o entrégalos junto al HTML para que el usuario los suba).
4. Verifica que cada webp pese poco (< 150 KB bonos/previews, < 250 KB hero) sin perder legibilidad del título.

## Regla común
Un prompt/imagen por slot; numera igual que en el HTML (`IMG_BONO_01`...) para emparejar 1:1. Mantén paleta e iluminación coherentes en toda la galería.

## Realidad operativa (importante)
- **Tamaño estándar de las imágenes de bono/regalo: 500×500 px, .webp.** Genéralas cuadradas (1:1) y entrégalas a 500×500.
- **Generación:** sí se pueden generar las imágenes desde aquí (con la herramienta conectada), con el título insertado y en la paleta. Requiere **créditos** en el workspace del generador; si se agotan, se corta la tanda — avisa al usuario para que recargue.
- **Descarga/guardado:** el entorno de procesamiento de archivos NO tiene salida a internet, así que no se puede bajar la imagen del CDN del generador y soltarla sola en la carpeta. Método real:
  1. Claude genera la imagen (reemplaza a ChatGPT).
  2. El usuario la descarga desde la tarjeta y la deja en la carpeta conectada (un arrastre).
  3. Claude la lee y la convierte a 500×500 .webp optimizada, nombrada por slot (`IMG_BONO_01.webp`), con PIL:
     `python3 -c "from PIL import Image; im=Image.open('in.png').convert('RGB'); w,h=im.size; s=min(w,h); im=im.crop(((w-s)//2,(h-s)//2,(w-s)//2+s,(h-s)//2+s)); im.resize((500,500), Image.LANCZOS).save('IMG_BONO_01.webp','WEBP',quality=85,method=6)"`
- **Revisar siempre** la ortografía del título en la portada (los generadores fallan en texto largo); si sale mal, regenerar o retocar en Canva.

## Modo 3 — Imágenes provistas por el usuario (solo procesar)
El usuario coloca sus propias imágenes (fotos, capturas, mockups hechos fuera) en la carpeta conectada y Claude solo las **redimensiona, convierte y renombra**. No requiere internet ni créditos.

Pasos:
1. Listar las imágenes de la carpeta (`ls`/`find`).
2. Pedir/confirmar 3 cosas: **tamaño(s)** (por defecto bonos 500×500; el usuario puede dar tamaños distintos por tipo), **patrón de nombres** (ej. `Producto_Bono-01_Titulo.webp`) y si **conservar o borrar** los originales.
3. Procesar por lote con PIL: recorte/relleno según relación de aspecto, resize, guardar como `.webp` (quality ~85), comprimir a peso objetivo (< 150 KB bonos, < 250 KB hero).
4. Colocar el `src` correspondiente en el HTML si aplica, y presentar los archivos resultantes.
5. Para borrar originales, si `rm` da "Operation not permitted", usar `mcp__cowork__allow_cowork_file_delete` y reintentar.

Ejemplo de lote (ajustar tamaño y patrón):
`python3 -c "from PIL import Image,os; [Image.open(p).convert('RGB').resize((500,500)).save(p.rsplit('.',1)[0]+'.webp','WEBP',quality=85,method=6) for p in __import__('glob').glob('*.png')]"`
