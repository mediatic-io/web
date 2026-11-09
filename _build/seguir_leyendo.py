"""Bloque "SEGUIR LEYENDO" que sale al final de cada artículo del blog.

Lo usan build.py (al generar la web) y aplicar_seguir.py (para parchear los HTML ya generados).
Muestra 3 artículos publicados (no borradores): primero los de RELATED y después los más recientes.
"""
import os
import re

N_TARJETAS = 3
_OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _esc(t):
    return t.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')


def elegir(f, ART_META, RELATED):
    ok = lambda k: k != f and k in ART_META and not ART_META[k].get('draft')
    orden = [k for k in RELATED.get(f, []) if ok(k)]
    orden += [k for k in ART_META if ok(k) and k not in orden]  # ART_META ya viene de más reciente a más antiguo
    return orden[:N_TARJETAS]


def seguir(f, ART_META, RELATED, out=_OUT):
    tarjetas = []
    for k in elegir(f, ART_META, RELATED):
        a = ART_META[k]
        img = ''
        if a.get('thumb') and os.path.exists(os.path.join(out, a['thumb'])):
            img = '<img src="%s" alt="" loading="lazy" decoding="async">' % a['thumb']
        fecha = '<time datetime="%s">%s</time>' % (a['date'], a['fecha']) if a.get('date') else ''
        tarjetas.append(
            '<a class="rc" href="%s"><div class="rc-th">%s</div><div class="rc-b"><small>%s</small><b>%s</b></div>'
            '<div class="rc-m"><span>Equipo de Mediatic</span>%s%s</div></a>'
            % (k, img, _esc(a['cat']), a['h1'], '<i>•</i>' if fecha else '', fecha))
    if not tarjetas:
        return ''
    return ('<section class="seguir" aria-labelledby="seg-h"><div class="wrap"><div class="tag">Seguir leyendo</div>'
            '<h2 id="seg-h">Artículos relacionados</h2><div class="rcgrid">%s</div>'
            '<p class="rc-all"><a class="rc-btn" href="blog.html">Ver todos</a></p></div></section>' % ''.join(tarjetas))


_RE_REL = re.compile(r'<section class="related".*?</section>', re.S)
_RE_SEG = re.compile(r'<section class="seguir".*?</section>', re.S)


def parchear(html, f, ART_META, RELATED):
    """Quita el bloque antiguo de relacionados y pone el nuevo tras la sección del artículo. Idempotente."""
    if '<section class="art">' not in html:
        return html
    html = _RE_REL.sub('', html)
    html = _RE_SEG.sub('', html)
    bloque = seguir(f, ART_META, RELATED)
    marca = '</aside></div></section>'
    if marca not in html:
        raise ValueError('no encuentro el final de la sección del artículo en ' + f)
    return html.replace(marca, marca + bloque, 1)
