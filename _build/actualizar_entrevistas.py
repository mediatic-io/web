#!/usr/bin/env python3
"""
Añade a la web las entrevistas nuevas del canal de YouTube de Mediatic.

Cómo funciona:
  1. Lee el feed público del canal (no hace falta clave de API).
  2. Se queda con los vídeos cuyo título sigue el formato
         #N - "Frase del cliente" | Nombre del cliente
     (el mismo que ya usáis: «#12 - "Mis clientas alucinan al ver mis vídeos" | Emilia Stella»).
  3. Si el vídeo no está ya en entrevistas.json, lo añade arriba de todo.
  4. Regenera las páginas (build.py).

El feed de YouTube solo devuelve los últimos 15 vídeos del canal, así que hay que ejecutarlo
al menos cada par de semanas. Uso:   python3 actualizar_entrevistas.py
(Con --lista PLxxxxxxxx usa una lista de reproducción en lugar de todo el canal.)
"""
import json, re, sys, html, subprocess, urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
JSON = AQUI / 'entrevistas.json'
CANAL = 'UCUkxYaDK3xu4GEPsXbCA4tw'

def feed_url(argv):
    if '--lista' in argv:
        return 'https://www.youtube.com/feeds/videos.xml?playlist_id=' + argv[argv.index('--lista') + 1]
    return 'https://www.youtube.com/feeds/videos.xml?channel_id=' + CANAL

def leer_feed(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'mediatic-web-updater'})
    xml = urllib.request.urlopen(req, timeout=20).read().decode('utf-8')
    for m in re.finditer(r'<entry>(.*?)</entry>', xml, re.S):
        b = m.group(1)
        vid = re.search(r'<yt:videoId>([^<]+)', b).group(1)
        titulo = html.unescape(re.search(r'<title>([^<]*)', b).group(1))
        yield vid, titulo

PATRON = re.compile(r'^#(\d+)\s*[-–—]\s*["“«](.+?)["”»]\s*\|\s*(.+)$')

def iniciales(nombre):
    pal = [p for p in re.split(r'\s+', nombre) if p and p.lower() not in ('dra', 'dr', 'de', 'la', 'el')]
    return ''.join(p[0].upper() for p in pal[:2]) or nombre[:2].upper()

def descargar_miniatura(vid):
    """Guarda la miniatura del vídeo en web/img/entrevistas/ (640x360) para no depender de YouTube al cargar la web."""
    destino = AQUI.parent / 'img' / 'entrevistas' / (vid + '.jpg')
    destino.parent.mkdir(parents=True, exist_ok=True)
    for calidad in ('maxresdefault', 'hqdefault'):
        try:
            req = urllib.request.Request('https://i.ytimg.com/vi/%s/%s.jpg' % (vid, calidad), headers={'User-Agent': 'Mozilla/5.0'})
            datos = urllib.request.urlopen(req, timeout=20).read()
            if len(datos) > 5000:
                destino.write_bytes(datos)
                try:
                    from PIL import Image
                    im = Image.open(destino).convert('RGB').resize((640, 360))
                    im.save(destino, quality=82, optimize=True)
                except Exception:
                    pass
                return
        except Exception:
            continue
    print('  (no se pudo descargar la miniatura de %s; se mostrará vacía)' % vid)

def main():
    datos = json.loads(JSON.read_text(encoding='utf-8'))
    ya = {d['id'] for d in datos}
    nuevas = []
    for vid, titulo in leer_feed(feed_url(sys.argv)):
        m = PATRON.match(titulo)
        if not m or vid in ya:
            continue
        n, frase, nombre = int(m.group(1)), m.group(2).strip(), m.group(3).strip()
        nuevas.append({'id': vid, 'n': n, 'name': nombre, 'niche': '', 'iniciales': iniciales(nombre),
                       'avatar': '', 'headline': '“%s”' % frase, 'context': ''})
    if not nuevas:
        print('No hay entrevistas nuevas.')
        return
    nuevas.sort(key=lambda d: -d['n'])
    for d in nuevas:
        descargar_miniatura(d['id'])
    JSON.write_text(json.dumps(nuevas + datos, ensure_ascii=False, indent=1), encoding='utf-8')
    for d in nuevas:
        print('NUEVA  #%d  %s  (%s)' % (d['n'], d['name'], d['headline']))
    print('\nAñadidas %d. Rellena "niche" y "context" de cada una en entrevistas.json (puedes dejarlos vacíos)\n'
          'y vuelve a ejecutar:  python3 build.py' % len(nuevas))
    subprocess.run([sys.executable, str(AQUI / 'build.py')], check=True)

if __name__ == '__main__':
    main()
