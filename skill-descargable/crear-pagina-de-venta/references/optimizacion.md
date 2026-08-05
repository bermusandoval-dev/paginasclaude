# Optimización de velocidad y responsive

La plantilla ya trae varias optimizaciones. Este paso las verifica y refuerza sobre el HTML final.

## Imágenes
- **Formato webp** para todos los mockups y capturas (bonos, previews, testimonios, hero, garantía). Si el usuario aún trae PNG/JPG, recomiéndalo o, si generas las imágenes tú, entrégalas ya en webp.
- **`width` y `height` explícitos** en cada `<img>` para evitar layout shift (CLS). El hero ya los tiene.
- **`loading="lazy"`** en todo salvo el hero; el hero lleva `fetchpriority="high"`. Opcional: añadir en `<head>` un `<link rel="preload" as="image" href="IMG_HERO">` para acelerar el LCP.
- Comprime: apunta a < 150 KB por imagen de bono/preview y < 250 KB el hero. Dimensiona a lo que realmente se muestra (los bonos ~500-600px de ancho, no 2000px).
- Los avatares de reseñas (randomuser.me) pueden dejarse o reemplazarse por webp locales.

## Video
- El iframe de Vimeo/YouTube ya va dentro de un contenedor con ratio fijo. Mantén `loading="lazy"` en el iframe. Evita `autoplay` con sonido. Si pesa el `player.js`, cárgalo tras interacción o al hacer scroll.

## Responsive
- La plantilla es mobile-first: contenedores con `max-width` y media queries en `@media(min-width:...)`. Verifica en 3 anchos: móvil (~375px), tablet (~768px) y desktop (~1200px).
- Revisa que la tabla comparativa (`table-layout:fixed`) no desborde en móvil y que el carrito lateral pase a `width:100vw` en <480px (ya está en el CSS).
- Respeta `prefers-reduced-motion` (ya incluido): no añadas animaciones sin su fallback.

## Rendimiento general
- No añadas librerías externas nuevas; el HTML es autónomo salvo fuentes de Google e iframe de video.
- Fuentes: ya se cargan con `media="all" onload` (no bloqueante) y `preconnect`. No añadas más familias de las necesarias.
- Mantén el CSS/JS inline tal como está (evita peticiones extra). No dividas en archivos.
- Al terminar, haz una pasada mental de LCP (hero), CLS (dimensiones de imágenes) y JS (todo diferido/al scroll).
