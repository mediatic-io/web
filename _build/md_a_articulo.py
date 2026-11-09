import os
# Convierte el "paquete de publicación" .md de un artículo en articulos/<slug>.html
# Uso: python3 md_a_articulo.py ruta.md slug
import re,html,sys,unicodedata
src=open(sys.argv[1]).read();slug_out=sys.argv[2]
sys.path.insert(0,'.')
from ajustes_articulos import REEMPLAZOS_MD,PIES,OMITIR_ALT
for _k,_v in REEMPLAZOS_MD.get(slug_out,{}).items(): src=src.replace(_k,_v)
src=re.sub(r'\[Imagen \d+:','[Imagen:',src)
art=src.split('## 2. Artículo')[1].split('\n---\n')[0].strip().split('\n')
art=[l for l in art if not l.startswith('# ')]
PROVISIONAL={'opciones-marketing-2026','pmu-paradise'}   # artículos cuyas imágenes aún no existen: se publican con un hueco 'Imagen provisional'
TOC_TRAS_IMAGEN={'opciones-marketing-2026'}   # sin vídeo: el índice va debajo de la primera imagen
STRIP_LIST_BOLD={'opciones-marketing-2026'}
INTERNAL={
 'https://www.mediatic.io/casos-de-exito/[nombre-cliente]':'de-profundis.html',
 'https://www.mediatic.io/casos-de-exito/de-profundis':'de-profundis.html',
 'https://www.mediatic.io/blog/descripcion-reels-instagram':'descripcion-reels-instagram.html',
 'https://www.mediatic.io/servicios':'servicios.html',
 'https://www.mediatic.io/blog/mitos-de-instagram':'mitos-de-instagram.html',
 'https://www.mediatic.io/blog/opciones-de-marketing-2026':'opciones-marketing-2026.html',
 'https://www.mediatic.io/blog/mejores-agencias-contenido-barcelona':'mejores-agencias-contenido-barcelona.html',
 'https://www.mediatic.io/blog/gamma-pmu-congress-2026':'gamma-pmu-congress-2026.html',
 'https://www.mediatic.io/contacto':'index.html#contacto" data-link="blog-articulo',
}
AUTOLINK={'Arrieta Micropigmentación':'https://arrietamicropigmentacion.es/','De Profundis':'https://deprofundis.es/es/'}
def inline(t,strip_bold):
    t=html.escape(t,quote=False)
    def link(m):
        txt,url=m.group(1),html.unescape(m.group(2))
        if url in INTERNAL: return '<a href="%s">%s</a>'%(INTERNAL[url],txt)
        return '<a href="%s" target="_blank" rel="noopener">%s</a>'%(url.replace('&','&amp;'),txt)
    t=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,t)
    t=re.sub(r'\*\*(.+?)\*\*',(r'\1' if strip_bold else r'<strong>\1</strong>'),t)
    # enlaces automáticos: cada vez que aparece el nombre, se enlaza (fuera de otros enlaces)
    for nombre,url in AUTOLINK.items():
        partes=re.split(r'(<a .*?</a>)',t)
        t=''.join(p if p.startswith('<a ') else p.replace(nombre,'<a href="%s" target="_blank" rel="noopener">%s</a>'%(url,nombre)) for p in partes)
    return t
def slug(h):
    s=unicodedata.normalize('NFKD',h).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+','-',s).strip('-')[:50]
IMGMAP={}
if '## 5. Imágenes' in src:
    for row in src.split('## 5. Imágenes')[1].split('\n---\n')[0].split('\n'):
        cells=[x.strip() for x in row.strip().strip('|').split('|')]
        if len(cells)>=3 and cells[1].endswith('.webp'): IMGMAP[cells[2]]=cells[1][:-5]
out=[];i=0;toc=[];faq=[];infaq=False
while i<len(art):
    l=art[i]
    if not l.strip(): i+=1;continue
    if l.startswith('## '):
        h=l[3:].strip();infaq=h.startswith('Preguntas frecuentes')
        sid='preguntas' if infaq else slug(h)
        toc.append((h,sid));out.append('<h2 id="%s">%s</h2>'%(sid,html.escape(h)))
        if infaq: out.append('<div class="afaq">')
        i+=1;continue
    if l.startswith('### '):
        h=l[4:].strip()
        if infaq:
            i+=1
            while not art[i].strip(): i+=1
            out.append('<details><summary>%s</summary><p>%s</p></details>'%(html.escape(h),inline(art[i],True)));faq.append(h)
        else: out.append('<h3>%s</h3>'%html.escape(h))
        i+=1;continue
    if l.startswith('>'):
        q=[]
        while i<len(art) and art[i].startswith('>'):
            q.append(art[i].lstrip('>').strip());i+=1
        cite=''
        if q and q[-1].startswith('—'): cite=q.pop()[1:].strip()
        out.append('<blockquote class="pq"><p>%s</p>%s</blockquote>'%(inline(' '.join(q),True),('<cite>%s</cite>'%inline(cite,True)) if cite else ''));continue
    if l.startswith('|'):
        rows=[]
        while i<len(art) and art[i].startswith('|'):
            rows.append([c.strip() for c in art[i].strip().strip('|').split('|')]);i+=1
        out.append('<div class="tablewrap"><table><thead><tr>'+''.join('<th>%s</th>'%inline(c,True) for c in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>%s</td>'%inline(c,True) for c in r)+'</tr>' for r in rows[2:])+'</tbody></table></div>');continue
    m=re.match(r'^(\d+)\. ',l)
    if m or l.startswith('- '):
        tag='ol' if m else 'ul';items=[]
        while i<len(art) and (re.match(r'^\d+\. ',art[i]) if m else art[i].startswith('- ')):
            items.append('<li>%s</li>'%inline(re.sub(r'^(\d+\. |- )','',art[i]),slug_out in STRIP_LIST_BOLD));i+=1
        out.append('<%s>%s</%s>'%(tag,''.join(items),tag));continue
    if 'URL DEL VÍDEO DE ANÁLISIS' in l: i+=1;continue   # enlace pendiente: no se publica sin URL
    if l.startswith('[Vídeo de YouTube'):
        mv=re.search(r'youtu\.be/([\w-]+)',l)
        out.append('<!--VIDEO:%s-->'%mv.group(1) if mv else '<!--VIDEO-->');i+=1;continue
    if l.startswith('[Imagen:') and any(o in l for o in OMITIR_ALT.get(slug_out,[])): i+=1;continue
    if l.startswith('[Imagen:') and slug_out in PROVISIONAL and not os.path.exists('../img/blog/%s.jpg'%IMGMAP.get(re.search(r'alt="([^"]+)"',l).group(1),'_')):
        alt=re.search(r'alt="([^"]+)"',l).group(1)
        out.append('<!--PROV:%s-->'%alt);i+=1;continue
    if l.startswith('[Imagen:') and 'Pie de foto' in l:
        alt=re.search(r'alt="([^"]+)"',l).group(1)
        cap=re.search(r'Pie de foto: (.*?) \| Foto: ([^\]]+)\]',l)
        out.append('<!--PHOTO:img/blog/%s.jpg|%s|%s|%s-->'%(slug_out,alt,cap.group(1).strip(),cap.group(2).strip()));i+=1;continue
    if l.startswith('[Imagen:') and 'embudo' not in l.lower() and 'esquema de las 6 fases' not in l.lower():
        alt=re.search(r'alt="([^"]+)"',l).group(1)
        fn=IMGMAP.get(alt)
        if fn:
            _c,_a=PIES.get(slug_out,{}).get(fn,('',''))
            out.append('<!--PHOTO:img/blog/%s.jpg|%s|%s|%s-->'%(fn,alt,_c,_a));i+=1;continue
    if l.startswith('[Imagen:'):
        alt=re.search(r'alt="([^"]+)"',l).group(1)
        out.append('<!--FIG:%s|%s-->'%('embudo' if 'Embudo' in alt else 'fases',alt));i+=1;continue
    out.append('<p>%s</p>'%inline(l,False));i+=1
if infaq: out.append('</div>')
body='\n'.join(out)
toch='<nav class="toc" aria-label="Índice del artículo"><b>En este artículo</b><ol>%s</ol></nav>'%''.join('<li><a href="#%s">%s</a></li>'%(sid,html.escape(re.sub(r'^\d+\.\s+','',h))) for h,sid in toc)
body=body.replace('<!--VIDEO-->','<!--VIDEO-->\n'+toch,1)
if '<!--VIDEO-->' not in body and slug_out in TOC_TRAS_IMAGEN:
    body=re.sub(r'(<!--(?:PROV|PHOTO):[^>]*-->)',lambda m:m.group(1)+'\n'+toch,body,count=1)
FIG={'embudo':(['Reels','Historias','Mensajes directos','Venta'],['100%','82%','64%','46%'],'Del impacto a la venta'),
 'fases':(['1 · Idea','2 · Formato','3 · Guion','4 · Grabación','5 · Edición','6 · Publicación'],['100%','88%','76%','60%','48%','36%'],'De mayor a menor importancia')}
def fig(m):
    k,alt=m.group(1),m.group(2);labels,w,cap=FIG[k]
    bars=''.join('<div class="fbar%s" style="width:%s"><span>%s</span></div>'%(' est' if (k=='fases' and n<3) else '',w[n],labels[n]) for n in range(len(labels)))
    note='<p class="fnote">Las tres primeras fases forman la estrategia.</p>' if k=='fases' else ''
    return '<figure class="fig" role="img" aria-label="%s"><figcaption>%s</figcaption>%s%s</figure>'%(alt,cap,bars,note)
body=re.sub(r'<!--FIG:(\w+)\|([^>]*?)-->',fig,body)
sys.path.insert(0,'.')
from ajustes_articulos import AJUSTES
for a,b in AJUSTES.get(slug_out,[]):
    if a in body: body=body.replace(a,b,1)
    else: print('AVISO: no se encontró el texto a retocar:',a[:60])
open('articulos/%s.html'%slug_out,'w').write(body+'\n')
print(len(re.sub('<[^>]+>','',body).split()),'palabras;',len(faq),'preguntas;',body.count('<strong>'),'negritas')
