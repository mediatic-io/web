import re
import time
V=str(int(time.time()))
import os
OUT='/Users/mediaticmac/landing-page/web'
NAV=[('index.html','Home',''),('index.html#resultados','Resultados',''),('index.html#opiniones','Opiniones',''),('contrataciones.html','Contrataciones','contrataciones'),('blog.html','Blog','')]
SITE='https://www.mediatic.io'   # <-- dominio definitivo de la web (sin barra final). Cámbialo aquí si es otro.
IG='https://www.instagram.com/mediatic.io/'
YT='https://www.youtube.com/@mediatic.agencia'
SEO={
 'index.html':('Agencia de contenido viral en Barcelona | Mediatic','Agencia de contenido viral en Barcelona. Multiplicamos por 5 tus visitas y leads en Instagram con menos de 5 horas al mes. Agenda tu llamada.',True),
 'equipo.html':('Equipo de expertos en contenido viral | Mediatic','Conoce al equipo de Mediatic: fundadores, guionistas, filmmakers y editores especializados en crear contenido viral para negocios y marcas personales.',True),
 'clientes.html':('Clientes y casos de éxito en redes sociales | Mediatic','Más de 100 clientes satisfechos y más de 30 nichos viralizados. Mira con quién trabajamos y los resultados que conseguimos con contenido orgánico.',True),
 'blog.html':('Noticias y artículos de contenido orgánico | Mediatic','Noticias y artículos de Mediatic: novedades sobre contenido orgánico para que aprendas y apliques en tu negocio, y logros de la agencia y su equipo.',False),
 'contrataciones.html':('Empleo: Editor, Filmmaker y Guionista | Mediatic','Trabaja con nosotros: buscamos editor, filmmaker y guionista para crear contenido viral en Mediatic, agencia de contenido en Barcelona.',True),
 'aviso-legal.html':('Aviso Legal | Mediatic','Aviso legal de Mediatic Studios SL: identificación del titular, condiciones de uso, medidas de seguridad y propiedad intelectual.',True),
 'politica-privacidad.html':('Política de Privacidad | Mediatic','Política de privacidad de Mediatic Studios SL: cómo tratamos tus datos personales, tus derechos y cómo ejercerlos.',True),
 'politica-cookies.html':('Política de Cookies | Mediatic','Política de cookies de Mediatic Studios SL: qué cookies usamos, para qué sirven y cómo gestionarlas.',True),
 '404.html':('Página no encontrada | Mediatic','La página que buscas no existe. Vuelve al inicio de Mediatic, agencia de contenido viral en Barcelona.',False),
}
# En SEO[...][2]: True = se indexa; False = noindex (blog hasta tener artículos reales, 404 siempre)
CRUMBS={'equipo.html':'Equipo','clientes.html':'Clientes','blog.html':'Blog','contrataciones.html':'Contrataciones','aviso-legal.html':'Aviso Legal','politica-privacidad.html':'Política de Privacidad','politica-cookies.html':'Política de Cookies'}

ART_META={'mitos-redes-sociales.html':dict(
 title='Mitos de las redes sociales: qué importa y qué no | Mediatic',
 desc='¿Importa la hora de publicar? ¿Y los hashtags? Desmontamos los mitos de Instagram y las redes sociales con casos reales de clientes de una agencia de contenido.',
 h1='Mitos de las redes sociales: lo que importa de verdad (y lo que no) para vender',
 cat='Contenido orgánico',date='2026-11-07',fecha='7 de noviembre de 2026',mins=8,yt='kX7RTLibXrs',
 thumb='img/blog/mitos-redes-sociales.jpg',
 excerpt='La hora de publicación, los hashtags, viral o nicho… Respondemos a las dudas más frecuentes sobre Instagram con ejemplos reales de clientes.')}
def canon(file): return SITE+('/' if file=='index.html' else '/'+file)
def esc(t): return t.replace('&','&amp;').replace('"','&quot;').replace('<','&lt;')
def jsonld(file,title,desc):
    org={"@type":"ProfessionalService","@id":SITE+"/#organization","name":"Mediatic","legalName":"MEDIATIC STUDIOS SL","url":SITE+"/","logo":SITE+"/logo-mediatic-azul.png","image":SITE+"/img/og-image.jpg","description":"Agencia de contenido viral en Barcelona especializada en crear contenido orgánico para Instagram, para negocios y marcas personales.","email":"info@mediatic.io","slogan":"Agencia de contenido viral en Barcelona","address":{"@type":"PostalAddress","streetAddress":"Plaça Pau Casals, 96","addressLocality":"Sant Fruitós de Bages","addressRegion":"Barcelona","postalCode":"08272","addressCountry":"ES"},"areaServed":{"@type":"AdministrativeArea","name":"Barcelona"},"sameAs":[IG,YT]}
    site={"@type":"WebSite","@id":SITE+"/#website","url":SITE+"/","name":"Mediatic","inLanguage":"es-ES","publisher":{"@id":SITE+"/#organization"}}
    pg={"@type":"WebPage","@id":canon(file)+"#webpage","url":canon(file),"name":title,"description":desc,"inLanguage":"es-ES","isPartOf":{"@id":SITE+"/#website"},"about":{"@id":SITE+"/#organization"}}
    graph=[org,site,pg]
    if file in CRUMBS:
        graph.append({"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Inicio","item":SITE+"/"},{"@type":"ListItem","position":2,"name":CRUMBS[file],"item":canon(file)}]})
    if file in ART_META:
        a=ART_META[file]
        graph.append({"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Inicio","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"Blog","item":canon('blog.html')},{"@type":"ListItem","position":3,"name":a['h1'],"item":canon(file)}]})
        graph.append({"@type":"BlogPosting","@id":canon(file)+"#article","mainEntityOfPage":{"@id":canon(file)+"#webpage"},"headline":a['h1'],"description":a['desc'],"datePublished":a['date'],"dateModified":a['date'],"inLanguage":"es-ES","author":{"@id":SITE+"/#organization"},"publisher":{"@id":SITE+"/#organization"},"image":SITE+("/"+a['thumb'] if os.path.exists(os.path.join(OUT,a['thumb'])) else "/img/og-image.jpg"),"articleSection":a['cat']})
        _q=re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>',open(os.path.join(OUT,'_build','articulos',file),'r').read())
        if _q: graph.append({"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',a2)}} for q,a2 in _q]})
    if file=='index.html':
        exec(open('/Users/mediaticmac/landing-page/web/_build/faq_data.py').read(),globals())
        graph.append({"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ_DATA]})
    return json.dumps({"@context":"https://schema.org","@graph":graph},ensure_ascii=False,separators=(',',':')).replace('</','<\\/')

from PIL import Image as _Img
_lw,_lh=_Img.open(os.path.join(OUT,'logo-mediatic-azul.png')).size
def header(cur):
    items=''.join('<li><a href="%s"%s%s%s>%s</a></li>'%(h,' class="on"' if h==cur else '',' aria-current="page"' if h==cur else '',(' data-link="%s"'%k) if k else '',n) for h,n,k in NAV)
    drawer=''.join('<a href="%s"%s>%s</a>'%(h,(' data-link="%s"'%k) if k else '',n) for h,n,k in NAV)
    return f'''<header>
  <nav class="drawer" aria-label="Menú móvil">{drawer}</nav>
  <a class="brand" href="index.html" aria-label="Mediatic, ir al inicio"><img src="logo-mediatic-azul.png" alt="Mediatic" width="{_lw}" height="{_lh}"></a>
  <nav class="menu" aria-label="Principal"><ul>{items}</ul></nav>
  <a class="btn sm hdr-cta" href="index.html#contacto" data-link="cabecera"><span class="long">Agendar llamada</span><span class="short">Agendar</span> <i>→</i></a>
  <button class="burger" aria-label="Abrir menú" aria-expanded="false"><span></span><span></span><span></span></button>
</header>'''
FOOT='''<footer><div class="wrap">
  <div class="fcols">
    <div class="fcol"><p class="ftitle">Redes sociales</p>
      <a data-social="instagram" href="https://www.instagram.com/mediatic.io/" target="_blank" rel="noopener">Instagram</a><a data-social="youtube" href="https://www.youtube.com/@mediatic.agencia" target="_blank" rel="noopener">YouTube</a><a data-social="linkedin" href="#">LinkedIn</a>
      <small>Mediatic Studios SL ©2026</small>
    </div>
    <nav class="fcol" aria-label="Páginas de interés"><p class="ftitle">Páginas de interés</p>
      <a href="index.html">Home</a><a href="equipo.html">Equipo</a><a href="clientes.html">Clientes</a><a href="blog.html">Blog</a><a href="index.html#contacto">Contacto</a><a href="contrataciones.html" data-link="contrataciones">Contrataciones</a></nav>
    <nav class="fcol" aria-label="Legal"><p class="ftitle">Legal</p>
      <a data-legal="aviso" href="aviso-legal.html">Aviso legal</a><a data-legal="privacidad" href="politica-privacidad.html">Política de privacidad</a><a data-legal="cookies" href="politica-cookies.html">Política de cookies</a><button type="button" data-open-cookies>Configurar cookies</button></nav>
  </div>
</div>
<div class="fplanes" aria-hidden="true" role="presentation"><svg viewBox="0 -14 1600 274" preserveAspectRatio="xMidYMid meet"><defs><symbol id="mtp" viewBox="342 590 1203 865"><polygon points="1545,590 342,942 648,1060 681,1180 826,1082 921,1455" fill="#F0F0EF"/><polygon points="648,1060 681,1180 826,1082" fill="#1B1BCB" fill-opacity=".38"/></symbol></defs><path d="M-20 123.8 L0 128.0 L20 132.2 L40 136.3 L60 140.4 L80 144.4 L100 148.2 L120 151.9 L140 155.4 L160 158.8 L180 161.8 L200 164.7 L220 167.2 L240 169.5 L260 171.4 L280 173.0 L300 174.3 L320 175.2 L340 175.8 L360 176.0 L380 175.8 L400 175.3 L420 174.4 L440 173.2 L460 171.6 L480 169.7 L500 167.5 L520 165.0 L540 162.2 L560 159.2 L580 155.9 L600 152.4 L620 148.7 L640 144.9 L660 140.9 L680 136.8 L700 132.7 L720 128.5 L740 124.4 L760 120.2 L780 116.1 L800 112.1 L820 108.3 L840 104.5 L860 101.0 L880 97.7 L900 94.5 L920 91.7 L940 89.1 L960 86.8 L980 84.8 L1000 83.2 L1020 81.8 L1040 80.9 L1060 80.3 L1080 80.0 L1100 80.1 L1120 80.6 L1140 81.4 L1160 82.6 L1180 84.1 L1200 86.0 L1220 88.2 L1240 90.6 L1260 93.4 L1280 96.4 L1300 99.7 L1320 103.2 L1340 106.8 L1360 110.6 L1380 114.6 L1400 118.6 L1420 122.8 L1440 126.9 L1460 131.1 L1480 135.2 L1500 139.3 L1520 143.4 L1540 147.2 L1560 151.0 L1580 154.6 L1600 157.9 L1620 161.1 L1640 164.0" fill="none" stroke="#F0F0EF" stroke-opacity=".55" stroke-width="5" stroke-linecap="round" stroke-dasharray="1 17"/><g class="pb" style="animation-delay:-0.0s"><g transform="rotate(44.8 90 146.3)" opacity="0.9"><use href="#mtp" x="15" y="92.4" width="150" height="107.9"/></g></g><g class="pb" style="animation-delay:-0.9s"><g transform="rotate(37.0 300 174.3)" opacity="1"><use href="#mtp" x="240" y="131.2" width="120" height="86.3"/></g></g><g class="pb" style="animation-delay:-1.8s"><g transform="rotate(26.3 520 165.0)" opacity="0.55"><use href="#mtp" x="425" y="96.7" width="190" height="136.6"/></g></g><g class="pb" style="animation-delay:-2.7s"><g transform="rotate(22.1 740 124.4)" opacity="1"><use href="#mtp" x="670" y="74.0" width="140" height="100.7"/></g></g><g class="pb" style="animation-delay:-3.6s"><g transform="rotate(26.5 930 90.3)" opacity="0.85"><use href="#mtp" x="875" y="50.8" width="110" height="79.1"/></g></g><g class="pb" style="animation-delay:-4.5s"><g transform="rotate(36.3 1130 81.0)" opacity="0.6"><use href="#mtp" x="1042" y="18.0" width="175" height="125.8"/></g></g><g class="pb" style="animation-delay:-5.4s"><g transform="rotate(44.3 1330 105.0)" opacity="1"><use href="#mtp" x="1262" y="56.4" width="135" height="97.1"/></g></g><g class="pb" style="animation-delay:-6.3s"><g transform="rotate(45.1 1520 143.4)" opacity="0.8"><use href="#mtp" x="1457" y="98.4" width="125" height="89.9"/></g></g></svg></div></footer>'''
def page(file,title,body):
    st,desc,index=SEO.get(file,(title,'',True))
    robots='index,follow,max-image-preview:large' if index else 'noindex,follow'
    cls=' class="mfaq"' if body.rstrip().endswith('</section>') and 'faq-blue' in body[-1500:] else ''
    html=f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(st)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
{"" if file=="404.html" else '<link rel="canonical" href="'+canon(file)+'">'}
<meta name="theme-color" content="#1B1BCB">
<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="Mediatic"><meta property="og:locale" content="es_ES">
<meta property="og:title" content="{esc(st)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon(file)}">
<meta property="og:image" content="{SITE}/img/og-image.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Mediatic, agencia de contenido viral en Barcelona">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(st)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{SITE}/img/og-image.jpg">
<link rel="preload" href="assets/fonts/SFProDisplay-Bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles.css?v={V}">
<script type="application/ld+json">{jsonld(file,st,desc)}</script>
</head>
<body>
<a class="skip" href="#contenido">Saltar al contenido</a>
{header(file)}
<main id="contenido"{cls}>
{body}
</main>
{FOOT}
<script src="enlaces.js?v={V}"></script>
<script src="site.js?v={V}"></script>
<script src="cookies.js?v={V}"></script>
</body></html>'''
    open(os.path.join(OUT,file),'w').write(html)

CLIENTES_ORDEN=[1, 2, 3, 5, 4, 8, 7, 9, 10, 16, 11, 12, 20, 13, 14, 21, 15, 17, 23, 18, 19, 24, 22, 25, 26, 27, 28, 30, 29, 31, 6, 32, 33]
CLIENTES_NOMBRES={1: 'Manuel Costiña', 2: 'UPC', 3: 'Holcim', 4: 'Condis', 5: 'Adrià Solà Pastor', 6: 'Tengo un Plan', 7: 'Cenando con Pablo', 8: 'Làctics La Torre', 9: 'Banc de Sang', 10: 'Laboratorios SVR', 11: 'Vilà Vila', 12: 'Port Calella', 13: 'Sencor', 14: 'Sistach Security', 15: 'Cafès del Bages', 16: 'Oscar RGB', 17: 'SD Finance', 18: 'ICO', 19: 'IMP', 20: 'Pedro SEO', 21: 'Gisela Jorba', 22: 'De Profundis', 23: 'Mario Cozma', 24: 'Karoma', 25: 'Claudia&Julia', 26: 'Pol Corominas', 27: 'Sosa', 28: 'La School of Dance', 29: 'PrintDossier', 30: 'Peter Lead', 31: 'Centre Enric Pintado', 32: 'LC Lasers', 33: 'Jack Beds'}
CLIENTES_FRASES={1: 'Chef', 2: 'Universidad politécnica pública', 3: 'Soluciones de construcción', 4: 'Supermercados desde 1961', 5: 'Creador con +1M en YouTube', 6: 'Podcast de emprendimiento', 7: 'Creador gastro, +500K en YouTube', 8: 'Productos lácteos', 9: 'Banco de sangre de Catalunya', 10: 'Dermocosmética francesa', 11: 'Grupo empresarial', 12: 'Inmobiliaria', 13: 'Electrónica y electrodomésticos', 14: 'Sistemas de seguridad', 15: 'Tostadores de café', 16: 'Creador de contenido', 17: 'Asesoría financiera', 18: 'Instituto de comunicación', 19: 'Instituto de marca personal', 20: 'Experto SEO, +500K seguidores', 21: 'Experta en micropigmentación', 22: 'Buceo técnico', 23: 'Transporte y logística, +70K', 24: 'Peluquería en Manresa', 25: 'Tienda online de cocina', 26: 'Marca personal', 27: 'Ingredientes para gastronomía', 28: 'Escuela de baile', 29: 'Impresión online', 30: 'Agencia SEO en Barcelona', 31: 'Clínica dental', 32: 'Soluciones láser industriales', 33: 'Marca de colchones'}
def card(n,dup=False):
    nm=CLIENTES_NOMBRES[n].replace('&','&amp;')
    return ('<div class="cl"%s><div class="ph"><img src="img/clientes/c%02d.jpg" alt="%s" width="480" height="480" decoding="async"></div><p class="cn">%s</p><p>%s</p></div>'
            %(' aria-hidden="true"' if dup else '',n,'' if dup else nm,nm,CLIENTES_FRASES[n]))
r1=''.join(card(n) for n in CLIENTES_ORDEN)
r1d=''.join(card(n,True) for n in CLIENTES_ORDEN)
MARQ='<div class="marquee"><div class="track">%s%s%s</div></div>'%(r1,r1d,r1d)
SERV='''<div class="cards3">
 <div class="card"><div class="ico"></div><span class="chip">Done for you</span><h3>Servicio 1</h3><p class="d">[Descripción corta del servicio completo.]</p><ul><li>Beneficio 1</li><li>Beneficio 2</li><li>Beneficio 3</li><li>Beneficio 4</li></ul><a class="btn" href="index.html#contacto" data-link="servicios-1">Quiero saber más <i>→</i></a></div>
 <div class="card"><div class="ico"></div><span class="chip">Consultoría</span><h3>Servicio 2</h3><p class="d">[Descripción corta del servicio de estrategia.]</p><ul><li>Beneficio 1</li><li>Beneficio 2</li><li>Beneficio 3</li></ul><a class="btn" href="index.html#contacto" data-link="servicios-2">Quiero saber más <i>→</i></a></div>
 <div class="card hl"><div class="ico"></div><span class="chip">Diagnóstico 1:1</span><h3>Sesión de diagnóstico</h3><p class="d">[Descripción corta de la sesión de diagnóstico.]</p><ul><li>Beneficio 1</li><li>Beneficio 2</li><li>Beneficio 3</li></ul><a class="btn" href="index.html#contacto" data-link="servicios-3">Reserva tu sesión <i>→</i></a></div>
</div>'''
CASES='''<div class="cards2">
 <div class="case"><div class="vid"><div class="play">▶</div></div><h3>[Cliente A] consiguió <u>[resultado]</u> en [tiempo] con Mediatic.</h3><ul><li>Llegó a Mediatic con [punto de partida].</li><li>Diseñamos la estrategia y operamos [qué hicimos].</li><li>[Resultado destacado].</li></ul></div>
 <div class="case"><div class="vid"><div class="play">▶</div></div><h3>[Cliente B] consiguió <u>[resultado]</u> con Mediatic.</h3><ul><li>Llegó a Mediatic con [punto de partida].</li><li>Operamos su cuenta con [qué hicimos].</li><li>[Resultado destacado].</li></ul></div>
</div>'''
TESTI='''<section class="testi"><div class="wrap"><blockquote>“[Testimonio de cliente: 2–4 líneas contando cómo Mediatic cambió su resultado.]”</blockquote>
<div class="n">Nombre cliente</div><div class="s">00K Seguidores</div>
<div class="avs"><div class="av on"></div><div class="av"></div><div class="av"></div><div class="av"></div><div class="av"></div><div class="av"></div></div></div></section>'''
def head(tag,h1,sub): return f'<section class="page-head"><div class="wrap"><div class="tag">{tag}</div><h1>{h1}</h1><p class="sub">{sub}</p></div></section>'

ABOUT=open('/Users/mediaticmac/landing-page/web/_build/about.html').read()
import json,html as _h
_E=json.load(open('/Users/mediaticmac/landing-page/web/_build/entrevistas.json'))
def _card(t):
    name=_h.escape(t['name']);vid=t['id']
    if t.get('avatar'): av='<img src="%s" alt="%s" width="64" height="64" loading="lazy">'%(t['avatar'],name)
    else: av='<span class="rinit" aria-hidden="true">%s</span>'%_h.escape(t.get('iniciales','')[:2])
    return ('<article class="rcard"><div class="rthumb" data-yt="%s" data-kind="h" role="button" tabindex="0" aria-label="Ver charla con %s"><img src="img/entrevistas/%s.jpg" alt="Charla con %s: vídeo de la entrevista" width="640" height="360" loading="lazy" decoding="async"><span class="rplay">&#9654;</span></div>'
      '<div class="rauth">%s<b>%s</b>%s</div>'
      '<h3>%s</h3>%s</article>')%(vid,name,vid,name,av,name,('<span>%s</span>'%_h.escape(t['niche'])) if t.get('niche') else '',_h.escape(t['headline']),('<p>%s</p>'%_h.escape(t['context'])) if t.get('context') else '')
RESULTS=('<section class="results" id="opiniones"><div class="wrap"><div class="tag">Opiniones</div>'
 '<h2 class="sec-h"><span class="strike">No lo decimos nosotros</span><br><span class="hand">lo dicen ellos</span></h2>'
 '<p class="sub" style="max-width:700px">Charlas con nuestros clientes que revelan su opinión sobre el servicio.</p>'
 '<div class="rgrid">'+''.join(_card(t) for t in _E)+'</div></div></section>')
_RES_ROWS=[[1, 37, 73, 34, 70, 31, 67, 28, 64, 25, 61, 22, 58, 19, 55, 16, 52, 13, 49, 10, 46, 7, 43, 4, 40], [26, 62, 23, 59, 20, 56, 17, 53, 14, 50, 11, 47, 8, 44, 5, 41, 2, 38, 74, 35, 71, 32, 68, 29, 65], [15, 51, 12, 48, 9, 45, 6, 42, 3, 39, 75, 36, 72, 33, 69, 30, 66, 27, 63, 24, 60, 21, 57, 18, 54]]
def _rrow(ids,rev):
    cards=''.join('<div class="rr"><img src="img/resultados/v%02d.jpg" alt="Vídeo de resultados de un cliente de Mediatic" width="360" height="563" loading="lazy" decoding="async"></div>'%i for i in ids)
    dup=''.join('<div class="rr" aria-hidden="true"><img src="img/resultados/v%02d.jpg" alt="" width="360" height="563" loading="lazy" decoding="async"></div>'%i for i in ids)
    return '<div class="rrow"><div class="rtrack%s">%s%s</div></div>'%(' rev' if rev else '',cards,dup)
RES2=('<section class="reels" id="resultados"><div class="wrap"><div class="reels-box">'
 '<div class="reels-head"><div class="tag">Resultados</div>'
 '<h2 class="sec-h">+300 millones de views, <span class="hand">y sumando</span></h2></div>'
 '<div class="reels-rows">'+_rrow(_RES_ROWS[0],False)+_rrow(_RES_ROWS[1],True)+_rrow(_RES_ROWS[2],False)+'</div>'
 '<div class="reels-cta"><a class="btn light" href="index.html#contacto" data-link="resultados">Quiero estos resultados <i>→</i></a></div>'
 '</div></div></section>')
_PEOPLE=[("Roger Gaona","Fundador"),("Esteve Gaona","Fundador"),("Betlem Boixader","Director de edición"),("Anna Martínez","Copywriter"),("Mireia Sallés","Copywriter"),("Gerard Torres","Filmmaker"),("Juan Andrés","Editor"),("Juanjo","Editor")]
MTSVG='<svg viewBox="0 0 100 100" aria-hidden="true"><polygon fill="#fff" points="80,28.5 20,46.1 35.3,52 37,58 44.2,53.1 48.9,71.7"/></svg>'
import unicodedata
def _slug(n): return re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',n).encode('ascii','ignore').decode().lower()).strip('-')
def _member(i):
    n,r=_PEOPLE[i-1]
    sl=_slug(n)
    def ph(suffix,label):
        f='img/equipo/%s%s.jpg'%(sl,suffix)
        if os.path.exists(os.path.join(OUT,f)): return '<img src="%s" alt="%s" loading="lazy">'%(f,(n if not suffix else n+' (foto de broma)'))
        return '<span>%s</span>'%label
    return ('<div class="member" tabindex="0"><div class="mphoto main">'+ph('','Foto')+'</div><div class="mphoto joke">'+ph('-broma','¡Foto de broma!')+'</div>'
            '<div class="mlabel"><i class="in">'+MTSVG+'</i><div><b>%s</b><span>%s</span></div></div></div>')%(n,r)
TEAM_GRID='<div class="mgrid">'+''.join(_member(i) for i in range(1,9))+'</div>'
TEAM=('<section class="team-sec" id="equipo"><div class="wrap"><div class="tag">Equipo</div>'
 '<h2 class="sec-h">¿Quién está detrás de <span class="acc">Mediatic</span>?</h2>'
 '<p class="sub" style="margin-bottom:8px">Nuestro equipo de expertos en contenido</p>'+TEAM_GRID+'</div></section>')
_REV=[("Pedro SEO","+240.000 seguidores","Llevo tiempo trabajando con Roger y Steve y no puedo estar más contento con sus servicios. Son creativos, profesionales y siempre entregan contenido de calidad adaptado a lo que necesito. Si quieres crecer en redes sociales, pruébalos.","img/clientes/c20.jpg"),
("Tengo un Plan","+2.450.000 seguidores","Gente muy profesional!","img/clientes/c06.jpg"),
("Cenando con Pablo","+928.000 seguidores","Buen trabajo por su parte durante un evento gastronómico en Barcelona, ¡Muchas gracias!","img/clientes/c07.jpg"),
("Top Catalan Restaurants","+140.000 seguidores","Nos crearon un vídeo promocional para dar visibilidad a nuestro proyecto. Grandes profesionales, creativos y de trato cercano y ágil.","img/clientes/top-catalan-restaurants.jpg"),
("Sor Lucía Caram","+150.000 seguidores","Unos grandes profesionales. La calidad de su trabajo en redes, cuidando todos los detalles, los hace una opción importante para dar a conocer una marca, un proyecto, una idea. ¡Gracias!","img/clientes/sor-lucia-caram.jpg"),
("Mario Cozma","+77.400 seguidores","Llevamos trabajando con ellos más de 8 meses y muy contentos, son muy top. ¡Espero que sigan así muchos años!","img/clientes/c23.jpg"),
("Pol Corominas","+240.000 seguidores","Destaco su profesionalidad, su cercanía y la facilidad para trabajar con ellos. Un equipo creativo, resolutivo y muy alineado con lo que necesita cualquier negocio.","img/clientes/c26.jpg"),
("Instituto de Comunicación","+280.000 seguidores","Nos ha encantado trabajar juntos. La grabación fue súper efectiva: grabamos todo lo propuesto y los chicos hicieron incluso más de lo que se pedía. Un placer.","img/clientes/c18.jpg")]
def _gslide(i,n,sub,txt,img):
    return ('<figure class="gq%s%s" data-i="%d"><blockquote>“%s”</blockquote>'
            '<figcaption><b>%s</b><span>%s</span></figcaption></figure>')%(' on' if i==0 else '',(' long' if len(txt)>200 else (' mid' if len(txt)>140 else '')),i,txt,n,sub)
def _gav(i,n,img):
    inner=('<img src="%s" alt="%s" width="120" height="120">'%(img,n)) if img else '<span>%s</span>'%''.join(w[0] for w in n.split()[:2]).upper()
    return '<button class="gav%s" data-i="%d" aria-label="Reseña de %s">%s</button>'%(' on' if i==0 else '',i,n,inner)
REVIEWS=('<section class="greviews" id="resenas" aria-labelledby="h-resenas"><div class="wrap"><h2 class="sr-only" id="h-resenas">Reseñas de clientes en Google</h2>'
 '<div class="grate"><span class="stars">★★★★★</span><b>5,0</b><span>+150 reseñas en Google</span></div>'
 '<div class="gstage">'+''.join(_gslide(i,n,sub,txt,img) for i,(n,sub,txt,img) in enumerate(_REV))+'</div>'
 '<div class="gnav"><button class="garr" data-d="-1" aria-label="Anterior">←</button>'+''.join(_gav(i,n,img) for i,(n,sub,txt,img) in enumerate(_REV))+'<button class="garr" data-d="1" aria-label="Siguiente">→</button></div>'
 '</div></section>')
exec(open('/Users/mediaticmac/landing-page/web/_build/faq_data.py').read())
faq=''.join('<details><summary>%s</summary><p>%s</p></details>'%(q,a) for q,a in FAQ_DATA)
FAQ_BLUE='<section class="faq faq-blue" id="faq"><div class="wrap"><div class="tag">Por si te quedas con dudas</div><h2 class="sec-h">Preguntas frecuentes</h2><p class="sub">Resuelve todas las dudas que tengas.</p><div class="faq-list">'+faq+'</div></div></section>'
QUOTE=open('/Users/mediaticmac/landing-page/web/_build/quote.html').read()
# HOME
page('index.html','Mediatic | Agencia de contenido orgánico',f'''
<section class="hero"><div class="wrap hero-wrap">
 <h1>Agencia de <span class="acc">contenido viral</span><br>en Barcelona</h1>
 <p class="hero-sub">Multiplicamos <b class="hl">x5</b> tus <b class="hl">visitas</b> y <b class="hl">leads</b><br>en Instagram con menos de 5h al mes</p>
 <a class="btn" href="index.html#contacto" data-link="hero">Quiero conseguir estos resultados <i>→</i></a></div><canvas id="fly"></canvas></section>
<section class="team-photo-sec"><div class="wrap"><div class="team-photo-wrap"><div class="team-photo">Foto de equipo</div>
 <div class="stats">
  <div class="stat"><b><span class="pl">+</span><span class="cnt" data-to="100">100</span></b><span>Clientes satisfechos</span></div>
  <div class="stat"><b><span class="pl">+</span><span class="cnt" data-to="300" data-suf="M">300M</span></b><span>Millones de views</span></div>
  <div class="stat"><b><span class="pl">+</span><span class="cnt" data-to="30">30</span></b><span>Nichos viralizados</span></div>
 </div></div></div></section>
<section><div class="wrap"><div class="tag">Clientes</div><h2 class="sec-h" style="margin-bottom:28px">Estos son nuestros <span class="strike">clientes</span> <span class="hand">amigos</span></h2>{MARQ}</div></section>
{ABOUT}
{RESULTS}{RES2}{TEAM}{REVIEWS}{QUOTE}
{FAQ_BLUE}''')


page('equipo.html','Equipo | Mediatic',head('Equipo','¿Quién está detrás de <span class="acc">Mediatic</span>?','Nuestro equipo de expertos en contenido')+'<section style="padding-top:0"><div class="wrap"><h2 class="sr-only">Miembros del equipo de Mediatic</h2>'+TEAM_GRID+'</div></section>')

page('clientes.html','Clientes | Mediatic',head('Clientes','Estos son nuestros <span class="strike">clientes</span> <span class="hand">amigos</span>','Negocios, marcas y creadores que ya crecen en redes sociales con Mediatic.')+f'<section><div class="wrap">{MARQ}</div></section>{RESULTS}{RES2}{REVIEWS}')

BLOG_CATS=['Contenido orgánico','Instagram y TikTok','Agencia y equipo']
def _post(i):
    return f'<a class="post" href="#" data-cat="{BLOG_CATS[(i-1)%3]}"><div class="th"></div><div class="c">{BLOG_CATS[(i-1)%3]}</div><h3>[Título del artículo {i}]</h3><p class="sub" style="font-size:16px">[Resumen de 1–2 líneas del artículo.]</p></a>'
def _real(f,a):
    th='<div class="th" style="background:url(%s) center/cover"></div>'%a['thumb'] if os.path.exists(os.path.join(OUT,a['thumb'])) else '<div class="th"></div>'
    return f'<a class="post" href="{f}" data-cat="{a["cat"]}">{th}<div class="c">{a["cat"]}</div><h3>{a["h1"]}</h3><p class="sub" style="font-size:16px">{a["excerpt"]}</p></a>'
posts=''.join(_real(f,a) for f,a in ART_META.items())
bfilter='<div class="bfilter" role="group" aria-label="Filtrar artículos por categoría"><button type="button" class="on" data-cat="">Todos</button>'+''.join(f'<button type="button" data-cat="{c}">{c}</button>' for c in BLOG_CATS)+'</div>'
page('blog.html','Blog | Mediatic',head('Blog','Noticias y artículos de <span class="acc">Mediatic</span>','Últimas noticias y novedades sobre el funcionamiento del contenido orgánico, para que aprendas y apliques en tu negocio. Y también las noticias y logros de la agencia y su equipo.')+f'<section><div class="wrap">{bfilter}<h2 class="sr-only">Últimos artículos del blog</h2><div class="posts">{posts}</div></div></section>'+FAQ_BLUE)

# ---- artículos del blog ----
for _f,_a in ART_META.items():
    SEO[_f]=(_a['title'],_a['desc'],True)
    _body=open(os.path.join(OUT,'_build','articulos',_f)).read()
    _vid=('<div class="avid" data-vid="%s" role="button" tabindex="0" aria-label="Reproducir el vídeo: %s">%s<span class="rplay">&#9654;</span></div>'%(_a['yt'],esc(_a['h1']),('<img src="%s" alt="Vídeo: %s" width="1280" height="720" loading="lazy" decoding="async">'%(_a['thumb'],esc(_a['h1']))) if os.path.exists(os.path.join(OUT,_a['thumb'])) else ''))
    _body=_body.replace('<!--VIDEO-->',_vid)
    _aside=('<aside class="aside" aria-label="Contacto"><div class="aside-in">'
      '<div class="acta hl"><span>Crece con nosotros</span><h2>¿Hablamos de tu proyecto?</h2><p>Te decimos si podemos multiplicar por 5 tus visitas y leads con menos de 5 horas al mes.</p><a class="btn" href="index.html#contacto" data-link="blog-lateral">Agendar diagnóstico <i>→</i></a></div>'
      '</div></aside>')
    _head=('<section class="page-head art-head"><div class="wrap"><nav class="crumbs" aria-label="Migas de pan"><a href="index.html">Home</a><i>›</i><a href="blog.html">Blog</a><i>›</i><span aria-current="page">%s</span></nav><h1>%s</h1><p class="byline">%s · Por el equipo de <b>Mediatic</b> · <time datetime="%s">%s</time> · %d min de lectura</p></div></section>'%(_a['h1'],_a['h1'],_a['cat'],_a['date'],_a['fecha'],_a['mins']))
    page(_f,_a['h1'],_head+'<section class="art"><div class="wrap art-grid"><article class="prose">'+_body+'</article>'+_aside+'</div></section>')


# ---- PÁGINAS LEGALES (texto copiado tal cual de legal.mediatic.io) ----
_LEG=[('aviso-legal.html','Aviso Legal'),('politica-privacidad.html','Política de Privacidad'),('politica-cookies.html','Política de Cookies')]
def _legal(file,title):
    body=open(SP_LEGAL+'/'+file).read()
    for a,b in (('/aviso-legal','aviso-legal.html'),('/politica-privacidad','politica-privacidad.html'),('/politica-cookies','politica-cookies.html')):
        body=body.replace('href="'+a+'"','href="'+b+'"')
    tabs=''.join('<a href="%s"%s>%s</a>'%(f,' class="on"' if f==file else '',t) for f,t in _LEG)
    page(file,title+' | Mediatic','<section class="page-head" style="padding-bottom:10px"><div class="wrap"><div class="tag">Información legal</div></div></section><section style="padding-top:0"><div class="wrap"><nav class="legal-tabs">'+tabs+'</nav><article class="legal">'+body+'</article></div></section>')
SP_LEGAL='/Users/mediaticmac/landing-page/web/_build/legal'
for _f,_t in _LEG: _legal(_f,_t)

# ---- CONTRATACIONES ----
JOBS='''<article class="job"><div class="jtop"><i class="jico"><svg viewBox="0 0 100 100" aria-hidden="true"><polygon fill="#fff" points="80,28.5 20,46.1 35.3,52 37,58 44.2,53.1 48.9,71.7"/></svg></i><span class="jbadge">Posición abierta</span></div><h3>Editor</h3><p>Conviertes vídeo en bruto en reels que retienen hasta el final. Buscamos a alguien con ojo para el ritmo, los subtítulos y el montaje pensado para redes sociales.</p><div class="jchips"><span>Reels</span><span>Montaje</span><span>Subtítulos</span><span>Retención</span></div><div class="jfoot"><span>Remoto · Jornada completa, media jornada o freelance</span><a class="btn sm" href="mailto:info@mediatic.io?subject=Candidatura%20Editor%20-%20Mediatic" data-link="aplicar-editor">Aplicar <i>→</i></a></div></article><article class="job"><div class="jtop"><i class="jico"><svg viewBox="0 0 100 100" aria-hidden="true"><polygon fill="#fff" points="80,28.5 20,46.1 35.3,52 37,58 44.2,53.1 48.9,71.7"/></svg></i><span class="jbadge">Posición abierta</span></div><h3>Filmmaker</h3><p>Buscamos a alguien con experiencia grabando y editando reels hablados a cámara para redes sociales. Si vives en España y crees que encajas, cuéntanos sobre ti.</p><div class="jchips"><span>Reels a cámara</span><span>Grabación</span><span>Edición</span></div><div class="jfoot"><span>Jornada completa, media jornada o freelance</span><a class="btn sm" href="../filmmakers/index.html" data-link="aplicar-filmmaker" target="_blank" rel="noopener">Aplicar <i>→</i></a></div></article><article class="job"><div class="jtop"><i class="jico"><svg viewBox="0 0 100 100" aria-hidden="true"><polygon fill="#fff" points="80,28.5 20,46.1 35.3,52 37,58 44.2,53.1 48.9,71.7"/></svg></i><span class="jbadge">Posición abierta</span></div><h3>Guionista</h3><p>Buscamos a alguien con experiencia guionizando reels virales para redes sociales. Si vives en España y crees que encajas, cuéntanos sobre ti.</p><div class="jchips"><span>Reels virales</span><span>Hooks</span><span>Copywriting</span></div><div class="jfoot"><span>Presencial · Jornada completa, media jornada o freelance</span><a class="btn sm" href="../guionistas/index.html" data-link="aplicar-guionista" target="_blank" rel="noopener">Aplicar <i>→</i></a></div></article>'''
page('contrataciones.html','Contrataciones | Mediatic','<section class="page-head" style="padding-bottom:10px"><div class="wrap"><div class="tag">Posiciones abiertas</div><h1>Encuentra tu sitio en <span class="acc">Mediatic</span></h1><p class="sub">Buscamos gente que quiera hacer el mejor trabajo de su carrera. Estos son los roles que tenemos abiertos. Si no ves el tuyo pero crees que sumas, escríbenos igual.</p></div></section><section style="padding-top:20px"><div class="wrap"><h2 class="sr-only">Posiciones abiertas en Mediatic</h2><div class="jobs">'+JOBS+'</div><p class="jmore">¿No es un rol que encaje contigo, pero quieres trabajar con nosotros? <a href="mailto:info@mediatic.io?subject=Quiero%20trabajar%20en%20Mediatic" data-link="contrataciones-escribenos">Escríbenos igual →</a></p></div></section>'+FAQ_BLUE)

# ---- 404, robots.txt y sitemap.xml ----
page('404.html','Página no encontrada | Mediatic','<section class="page-head" style="min-height:62vh"><div class="wrap"><div class="tag">Error 404</div><h1>Esta página <span class="acc">no existe</span></h1><p class="sub" style="margin-bottom:30px">Puede que el enlace esté roto o que la página haya cambiado de sitio. Vuelve al inicio y te llevamos a donde quieras.</p><a class="btn" href="index.html">Ir al inicio <i>→</i></a></div></section>')
import datetime
_hoy=datetime.date.today().isoformat()
_urls=[f for f,(t,d,idx) in SEO.items() if idx and f!='404.html']
open(os.path.join(OUT,'sitemap.xml'),'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n'%(canon(f),_hoy,'1.0' if f=='index.html' else ('0.3' if f.startswith(('aviso','politica')) else '0.8')) for f in _urls)+'</urlset>\n')
open(os.path.join(OUT,'robots.txt'),'w').write('User-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: %s/sitemap.xml\n'%SITE)
print('ok')
