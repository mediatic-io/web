# SEO de la web de Mediatic: qué está hecho y qué te toca

## Ya está hecho en el código (no cambia nada de lo que se ve)
- **Estructura de encabezados**: un único `H1` por página (la Home: "Agencia de contenido viral en Barcelona"), `H2` para cada sección y `H3` solo dentro de una sección. Sin saltos de nivel. Los nombres de la cinta de clientes y los títulos del pie ya no son encabezados.
- **Etiquetas por página**: título único (≤ 62 caracteres), meta descripción única (≤ 150), `canonical`, `robots`, Open Graph y Twitter Card con imagen 1200×630.
- **Datos estructurados (JSON-LD)**: empresa local (dirección de Sant Fruitós de Bages, redes, email), sitio web, página, migas de pan y preguntas frecuentes (Home).
- **Semántica y accesibilidad**: `<main>`, enlace "Saltar al contenido", menús con `<nav>` y `aria-label`, página actual marcada, imágenes con `alt` y tamaño (sin saltos al cargar), cintas duplicadas ocultas para lectores y buscadores.
- **Rendimiento**: fuente en WOFF2 (95 KB en vez de 425 KB), miniaturas de las entrevistas alojadas en la propia web (sin pedir nada a YouTube antes del consentimiento), imágenes bajo el pliegue con carga diferida.
- **Archivos**: `robots.txt`, `sitemap.xml`, `404.html`, favicon y `apple-touch-icon`. La carpeta `web/` ya es autosuficiente.
- Todo se regenera con `python3 _build/build.py`. Los textos de título/descripción y el dominio están al principio de `_build/build.py` (`SITE` y `SEO`).

## Lo que tienes que hacer tú
1. **Confirmar el dominio** y ponerlo en `SITE` (`_build/build.py`, ahora `https://www.mediatic.io`). Después `python3 build.py`.
2. **Publicar solo la carpeta `web/`** (sin `_build/`) en HTTPS. Redirige `mediatic.io` ↔ `www.mediatic.io` a una sola versión.
3. **Antes de indexar el Blog**: está en `noindex` hasta que tenga varios artículos reales (ahora tiene uno). Cuando haya artículos reales, cambia `False` por `True` en la línea de `blog.html` del diccionario `SEO` y regenera.
4. **Vieja landing**: si `index.html` de la carpeta raíz sigue publicada en otra dirección, ponle `noindex` o redirígela a la web nueva para no duplicar contenido.
5. **Google Search Console**: verifica el dominio, envía `https://TU-DOMINIO/sitemap.xml` y pide la indexación de la Home.
6. **Ficha de Google Business Profile** con la misma dirección, nombre y web que aparecen en la página (Plaça Pau Casals, 96, Sant Fruitós de Bages). Es lo más importante para el SEO local. Enlaza tus reseñas de Google y añade teléfono.
7. **Teléfono**: no hay en la web. Añadirlo (con el mismo formato en todas partes) ayuda al SEO local; dime cuál es y lo incluyo en los datos estructurados.
8. **Medir**: cuando decidas qué herramientas usar (Analytics, Pixel...), se activan solo con el consentimiento de cookies.
9. **Contenido**: publica artículos en el Blog con frases que busca la gente ("contenido orgánico", "reels virales", "cómo crecer en Instagram", "agencia de contenido en Barcelona") y enlázalos entre sí y a la Home.
10. **Enlaces externos**: consigue menciones y enlaces a tu web desde los canales y webs de tus clientes, directorios locales y notas de prensa. Es lo que más pesa tras el contenido.
11. **Tras publicar**: mide la velocidad en PageSpeed Insights y revisa en Search Console los informes de indexación y de usabilidad móvil.

## Cuando añadas fotos
- Pon un texto alternativo que describa la imagen ("Equipo de Mediatic grabando un reel en Manresa"), formato JPG/WebP, máximo ~200 KB y con `width`/`height`.
- Nombres de archivo descriptivos (`equipo-mediatic.jpg`, no `IMG_0234.jpg`).
