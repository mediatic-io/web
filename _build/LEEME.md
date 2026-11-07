# Cómo se genera la web

Las páginas de `web/` (index, equipo, clientes, blog, contrataciones, los artículos del blog y las tres legales) se **generan** con `build.py`.
Para cambiar un texto de forma permanente, edítalo aquí y vuelve a ejecutar:

    python3 build.py

(Si editas directamente los `.html` de `web/`, el siguiente `build.py` los sobrescribe.)

## Archivos de contenido
- `entrevistas.json`: las charlas con clientes (apartado Opiniones). Cada una lleva id de YouTube, nombre, nicho, frase y resumen corto.
- `faq_data.py`: preguntas frecuentes y respuestas.
- `about.html`: texto de ¿Quiénes somos?
- `quote.html`: bloque de contacto (formulario y mapa).
- `legal/`: textos de Aviso legal, Privacidad y Cookies copiados de legal.mediatic.io.
- `articulos/`: texto de cada artículo del blog (su título, fecha, vídeo y portada se definen en `ART_META` de `build.py`).
- `build.py`: menú, pie, clientes, equipo, reseñas, resultados y el resto.

## Entrevistas nuevas de YouTube
    python3 actualizar_entrevistas.py
Detecta los vídeos del canal con título `#N - "Frase" | Cliente` que aún no estén en `entrevistas.json`, los añade arriba y regenera la web.
Después rellena `niche` y `context` de la nueva entrada (opcional) y ejecuta `python3 build.py`.
El feed solo recuerda los últimos 15 vídeos del canal: ejecútalo al menos cada dos semanas.

## Otros ajustes
- `../enlaces.js`: enlaces de cada botón (UTM), redes sociales, textos legales y formulario de candidatura/cualificación.

## SEO
- `SITE` (dominio) y el diccionario `SEO` (título, descripción y si se indexa cada página) están al principio de `build.py`.
- `build.py` también genera `sitemap.xml`, `robots.txt` y `404.html`.
- Detalle y tareas pendientes en `../SEO-INSTRUCCIONES.md`.
