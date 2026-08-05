# Framework de copy — Página de Venta Directa

Este documento traduce marcos clásicos de respuesta directa (Eugene Schwartz, LF8, PAS) a fórmulas concretas para cada sección de `assets/plantilla-base.html`. Léelo antes de escribir. La meta no es rellenar huecos: es construir un argumento de venta que lleve al lector del dolor a la compra sin fricción.

## 1. Define primero el núcleo estratégico

Antes de escribir una sola línea, deja explícito (4-6 líneas):

- **Avatar:** quién es, en qué situación está, qué palabras usa para describir su problema.
- **Nivel de consciencia (Schwartz):** ¿dónde está?
  - *Inconsciente:* no sabe que tiene el problema → abre con una historia/identidad o un dato que lo despierte.
  - *Consciente del problema:* siente el dolor, no conoce soluciones → abre agitando el problema.
  - *Consciente de la solución:* sabe que hay soluciones, no conoce la tuya → abre con el mecanismo único.
  - *Consciente del producto:* conoce tu producto, duda → abre con oferta, prueba y diferenciación.
  - *El más consciente:* listo para comprar → abre con la oferta y la urgencia.
  El titular del hero (`REEMPLAZAR_HERO_TITULAR`) y el primer bloque cambian por completo según esto.
- **Dolor #1** y **Deseo #1** (el más visceral de cada uno).
- **Mecanismo único:** la razón de "por qué funciona" que hace tu producto distinto (alimenta la sección de mecanismo).
- **Oferta:** producto núcleo + bonos + regalos + precio + garantía.

## 2. LF8 y deseos base

Carga emocionalmente titulares, bullets, bonos y CTAs apelando a deseos primarios: supervivencia/salud, disfrutar, evitar el miedo/dolor/peligro, aprobación social, superioridad/estatus, protección de los seres queridos, pertenencia, comodidad (evitar esfuerzo). Cada bullet de dolor toca un miedo; cada bullet de ganancia toca un deseo. Evita adjetivos vacíos; usa escenas concretas ("cada sesión se siente distinta e incompleta" > "es desorganizado").

## 3. Estructura PAS ampliada (mapa de la página)

La plantilla ya sigue este orden. Respétalo:

1. **Hook (hero):** promesa grande + subpromesa + descripción de qué es. `REEMPLAZAR_HERO_TITULAR`, `REEMPLAZAR_HERO_SUBTITULO`.
2. **Problema (agitación):** el bloque `pain-card`. 5 dolores que el avatar reconoce como propios. Empieza con "El problema NO es tu..." para desarmar la culpa.
3. **Giro a la ganancia:** el bloque `gain-card`. 5-6 resultados concretos + 1 bullet de prueba social con cifra.
4. **Cómo funciona (3 pasos):** proceso simple y ordenado. Reduce la sensación de esfuerzo.
5. **Comparativa:** tu producto vs. las 2 alternativas típicas del nicho (gratis / caro-genérico). La columna resaltada siempre gana.
6. **Features + Autoridad:** 6 features (qué incluye, con beneficio) + bloque de autoridad (nombres/referentes o credenciales que dan respaldo).
7. **Mecanismo ("por qué funciona"):** 3 razones en orden lógico. Es el corazón intelectual de la oferta.
8. **Vistazo dentro:** previews reales del producto (imágenes).
9. **Bonos y regalos:** cada uno con nombre entre comillas «», descripción de beneficio y valor tachado → Gratis.
10. **Oferta principal:** value stack (suma de valores → total tachado → precio hoy → ahorro), caja de precio, urgencia, escasez, CTA.
11. **Para quién es / Qué descubrirás:** confirma encaje y anticipa contenido.
12. **Autor + Estadísticas + Testimonios + Reseñas:** prueba social en capas.
13. **Garantía:** invierte el riesgo.
14. **Por qué es accesible + Objeciones:** justifica el precio bajo y derriba las 4 objeciones top.
15. **FAQ:** 7-9 preguntas reales.
16. **Oferta final + P.D.:** repite oferta y cierra con 2 P.D. (valor/riesgo y urgencia).

## 4. Fórmulas por sección

**Titular hero.** Fórmula: [Verbo de logro] + [resultado deseado] + [con/sin fricción]. Lo que va dentro de `<u></u>` es el beneficio emocional. Ej.: "Domina X con **estructura, confianza y resultados reales**".

**Sub-promesa (itálica verde).** Una frase que resume el qué + para quién + diferenciador ("...desde la primera sesión, sin improvisar").

**Bullets de dolor.** Estructura: [situación concreta] + [consecuencia emocional]. Usa **negritas** en la frase clave. 5 bullets.

**Bullets de ganancia.** Estructura: [logras X] usando [el mecanismo]. Verbos en presente ("Reprocesas...", "Eliminas..."). El último bullet es cifra de prueba ("Ya usado por N personas en N países").

**Comparativa.** Filas = las capacidades donde tu producto gana. Las alternativas llevan ❌/⚠️; tu columna, ✅. Nunca menciones marcas reales de competidores; usa categorías ("Cursos genéricos", "PDF gratuitos").

**Features.** Título corto (2-4 palabras) + una frase de beneficio, no de característica.

**Autoridad.** Si el producto se basa en referentes/metodologías públicas, lístalos como pills y aclara que está "inspirado en / basado en los principios de" (no implica aval). Si es marca propia, usa credenciales y cifras.

**Mecanismo.** 3 razones en secuencia causal: primero A, que habilita B, que produce C. Cierra con una frase-mantra en itálica.

**Bonos.** Nombre entre «» que suene a producto ("«Cuaderno de Trabajo de...»"). Descripción: qué es + qué resuelve, en una frase. Valor individual coherente (que sumados + núcleo ≈ precio "antes").

**Value stack.** Cada fila = un ítem con su valor. La suma debe cuadrar con `PRECIO_ANTES`. Última fila con `super`.

**Precio y anclaje.** Ancla alto (valor real) → tacha → precio hoy → % de ahorro. El mismo trío de números aparece en: bar superior, value stack, offer-box (x2), carrito (`cpc-main-*`), y P.D. Deben ser idénticos.

**Urgencia/escasez.** Countdown + "N viendo ahora" + "quedan N plazas". Mantén cifras verosímiles.

**Objeciones.** Las 4 dudas más probables del avatar, cada una respondida en una frase que reencuadra, no que discute.

**FAQ.** Mezcla logística (acceso, pago, garantía) con dudas de fondo (¿me sirve?, ¿reemplaza X?). Respuestas honestas y breves.

**P.D.** P.D. = recap de valor + inversión + inversión de riesgo. P.P.D. = urgencia (cuando el contador llegue a cero, sube el precio).

## 5. Reglas de credibilidad

- No prometas resultados garantizados fuera de lo que cubre la garantía de reembolso.
- No inventes estudios, cifras médicas/clínicas ni certificaciones oficiales. La prueba social (testimonios, nº de usuarios) debe presentarse como afirmaciones de marketing verosímiles, no como datos científicos.
- En nichos sensibles (salud, dinero, legal), añade el disclaimer del footer y evita afirmaciones de eficacia terapéutica/financiera absolutas.
- Tono: por defecto "tú" (cercano, directo). Cambia a "usted" solo si el usuario lo pide.
