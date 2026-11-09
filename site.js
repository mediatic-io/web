// cabecera: franja translúcida al bajar + menú móvil
const hdr=document.querySelector('header');
const onScroll=()=>hdr.classList.toggle('scrolled',scrollY>20);
addEventListener('scroll',onScroll,{passive:true});onScroll();
const burger=document.querySelector('.burger');
if(burger){
  burger.addEventListener('click',()=>{const o=hdr.classList.toggle('open');burger.setAttribute('aria-expanded',o);document.body.style.overflow=o?'hidden':''});
  document.querySelectorAll('.drawer a').forEach(a=>a.addEventListener('click',()=>{hdr.classList.remove('open');document.body.style.overflow=''}));
}

// avión de Mediatic en el hero: sigue el cursor, deja estela y hace un looping al hacer clic
function initPlane(cv,opt){
  const useMouse=!(opt&&opt.mouse===false);
  const ctx=cv.getContext('2d'),hero=cv.parentElement;
  const still=matchMedia('(prefers-reduced-motion: reduce)').matches;
  let W,H,dpr;
  const size=()=>{dpr=Math.min(devicePixelRatio||1,1.5);W=hero.clientWidth;H=hero.clientHeight;cv.width=W*dpr;cv.height=H*dpr;ctx.setTransform(dpr,0,0,dpr,0,0)};
  size();addEventListener('resize',size);
  let run=true,raf=0;
  const pts=[[1545,590],[342,942],[648,1060],[681,1180],[826,1082],[921,1455]];
  const flapPts=[[648,1060],[681,1180],[826,1082]];
  const cx0=860,cy0=1040,rot=Math.atan2(590-cy0,1545-cx0),S=.08;
  const mk=a=>{const q=new Path2D();a.forEach(([x,y],i)=>{const dx=x-cx0,dy=y-cy0,c=Math.cos(-rot),sn=Math.sin(-rot);const X=(dx*c-dy*sn)*S,Y=(dx*sn+dy*c)*S;i?q.lineTo(X,Y):q.moveTo(X,Y)});q.closePath();return q};
  const plane=mk(pts),fold=mk(flapPts);
  let P={x:W*.2,y:H*.7},V={x:0,y:0},ang=0,mouse=null,loop=0,trail=[],t0=0;
  if(useMouse)hero.addEventListener('mousemove',e=>{const r=hero.getBoundingClientRect();mouse={x:e.clientX-r.left,y:e.clientY-r.top}});
  if(useMouse)hero.addEventListener('mouseleave',()=>{mouse=null});
  if(useMouse)hero.addEventListener('click',e=>{if(!e.target.closest('a,button,input,textarea,label,iframe'))loop=1});
  function tick(ts){
    const t=ts/1000,dt=Math.min(.05,t-t0||.016);t0=t;
    const tx=mouse?mouse.x:W*(.5+.38*Math.sin(t*.45)),ty=mouse?mouse.y:H*(.55+.28*Math.sin(t*.9));
    if(!(still&&!mouse)){V.x+=(tx-P.x)*3.2*dt;V.y+=(ty-P.y)*3.2*dt;V.x*=.93;V.y*=.93;P.x+=V.x*dt*8;P.y+=V.y*dt*8}
    const sp=Math.hypot(V.x,V.y);
    if(sp>3){let a=Math.atan2(V.y,V.x),d=a-ang;d=Math.atan2(Math.sin(d),Math.cos(d));ang+=d*.12}
    let draw=ang;
    if(loop>0){loop+=dt*1.6;draw=ang-(loop-1)*Math.PI*2;if(loop>=2)loop=0}
    trail.push({x:P.x,y:P.y,t});
    while(trail.length&&t-trail[0].t>2.2)trail.shift();
    ctx.clearRect(0,0,W,H);
    ctx.lineCap='round';ctx.setLineDash([2,14]);
    for(let i=1;i<trail.length;i++){const a=1-(t-trail[i].t)/2.2;ctx.strokeStyle='rgba(27,27,203,'+(.55*a)+')';ctx.lineWidth=2+3*a;ctx.beginPath();ctx.moveTo(trail[i-1].x,trail[i-1].y);ctx.lineTo(trail[i].x,trail[i].y);ctx.stroke()}
    ctx.setLineDash([]);
    ctx.save();ctx.translate(P.x,P.y);ctx.rotate(draw);
    ctx.scale(1,1-Math.max(-.5,Math.min(.5,sp*.004))*.4);
    ctx.shadowColor='rgba(27,27,203,.30)';ctx.shadowBlur=12;ctx.shadowOffsetY=10;
    ctx.fillStyle='#1B1BCB';ctx.fill(plane);
    ctx.shadowColor='transparent';ctx.fillStyle='#5a5ae6';ctx.fill(fold);
    ctx.restore();
    raf=run?requestAnimationFrame(tick):0;
  }
  // pausa la animación cuando el avión no está en pantalla
  if('IntersectionObserver' in window)new IntersectionObserver(es=>{run=es[0].isIntersecting;if(run&&!raf)raf=requestAnimationFrame(tick)},{rootMargin:'100px'}).observe(hero);
  raf=requestAnimationFrame(tick);
}
const _f1=document.getElementById('fly');if(_f1)initPlane(_f1);
const _f2=document.getElementById('fly2');if(_f2)initPlane(_f2,{mouse:false});

// reproductor en ventana para entrevistas y reels
(function(){
  const m=document.createElement('div');m.className='modal';
  m.innerHTML='<button class="x" aria-label="Cerrar">✕</button><div class="box"></div>';
  document.body.appendChild(m);
  const box=m.querySelector('.box');
  const close=()=>{m.classList.remove('on','v');box.innerHTML='';document.body.style.overflow=''};
  const open=(id,k)=>{m.classList.toggle('v',k==='v');box.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>';m.classList.add('on');document.body.style.overflow='hidden'};
  document.addEventListener('click',e=>{const t=e.target.closest('[data-yt]');if(t){open(t.dataset.yt,t.dataset.kind);return}if(e.target===m||e.target.closest('.x'))close()});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')close();if((e.key==='Enter'||e.key===' ')&&e.target.matches('.rthumb')){e.preventDefault();open(e.target.dataset.yt,'h')}});
})();

// reseñas de Google: selector de reseñas con flechas y avatares
(function(){
  const st=document.querySelector('.gstage');if(!st)return;
  const qs=[...st.querySelectorAll('.gq')],avs=[...document.querySelectorAll('.gav')];let cur=0;
  const go=i=>{cur=(i+qs.length)%qs.length;qs.forEach((q,k)=>q.classList.toggle('on',k===cur));avs.forEach((a,k)=>a.classList.toggle('on',k===cur));const gn=document.querySelector('.gnav'),ac=avs[cur];if(gn&&ac&&gn.scrollWidth>gn.clientWidth+2)gn.scrollTo({left:ac.offsetLeft-(gn.clientWidth-ac.offsetWidth)/2,behavior:'smooth'})};
  avs.forEach((a,k)=>a.addEventListener('click',()=>go(k)));
  document.querySelectorAll('.garr').forEach(b=>b.addEventListener('click',()=>go(cur+ +b.dataset.d)));
})();

// enlaces de cada botón (configurables en enlaces.js) + UTM
(function(){
  const C=window.MEDIATIC||{},L=C.ENLACES||{},UTM=C.UTM||[];
  // guarda las UTM de la visita para reenviarlas aunque cambie de página
  try{
    const q=new URLSearchParams(location.search);const saved=JSON.parse(sessionStorage.getItem('mt_utm')||'{}');let ch=false;
    UTM.forEach(k=>{if(q.get(k)){saved[k]=q.get(k);ch=true}});
    if(ch)sessionStorage.setItem('mt_utm',JSON.stringify(saved));
  }catch(e){}
  document.querySelectorAll('a[data-link]').forEach(a=>{
    const u=L[a.dataset.link];
    if(u){a.href=u;if(/^https?:/i.test(u)){a.target='_blank';a.rel='noopener'}}
    else if(C.DESTINO_POR_DEFECTO){a.setAttribute('href',a.getAttribute('href')||C.DESTINO_POR_DEFECTO)}
  });
})();

// formulario corto: valida y abre el formulario largo en una pestaña nueva
(function(){
  const f=document.getElementById('qform');if(!f)return;
  const C=window.MEDIATIC||{},note=f.querySelector('.qnote');
  const say=t=>{note.textContent=t;note.hidden=false};
  f.addEventListener('submit',e=>{
    e.preventDefault();
    const d=Object.fromEntries(new FormData(f).entries());
    if(!d.nombre||!d.nombre.trim())return say('Escribe tu nombre.');
    if(!/^\S+@\S+\.\S+$/.test(d.email||''))return say('Escribe un correo electrónico válido.');
    if(!/[0-9]{6,}/.test((d.telefono||'').replace(/\D/g,'')))return say('Escribe tu número de teléfono.');
    if(!f.consent.checked)return say('Acepta la Política de Privacidad para continuar.');
    const url=new URL(C.FORMULARIO||'../formulario/index.html',location.href);
    try{const s=JSON.parse(sessionStorage.getItem('mt_utm')||'{}');Object.keys(s).forEach(k=>url.searchParams.set(k,s[k]))}catch(_){}
    if(C.PASAR_DATOS_AL_FORMULARIO!==false){
      ['nombre','email','telefono','instagram','necesidad'].forEach(k=>{if(d[k]&&d[k].trim())url.searchParams.set(k,d[k].trim())});
    }
    const w=window.open(url.toString(),'_blank','noopener');
    if(!w)location.href=url.toString();
    say('Se ha abierto el formulario para terminar tu solicitud.');
  });
})();

// redes sociales del pie (se configuran en enlaces.js)
document.querySelectorAll('[data-social]').forEach(a=>{const u=((window.MEDIATIC||{}).REDES||{})[a.dataset.social];if(u){a.href=u;a.target='_blank';a.rel='noopener'}else{a.style.display='none'}});

// equipo: el clic no hace nada en ordenador (la foto de broma solo sale al pasar el cursor); en móvil se alterna al tocar
const _touch=matchMedia('(hover: none)');
document.querySelectorAll('.member').forEach(m=>m.addEventListener('click',e=>{e.preventDefault();if(_touch.matches)m.classList.toggle('flip');else{m.classList.remove('flip');m.blur()}}));

/* blog: filtro por categorías */
(function(){var f=document.querySelector('.bfilter');if(!f)return;var posts=[].slice.call(document.querySelectorAll('.post[data-cat]'));
f.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var c=b.getAttribute('data-cat');
[].forEach.call(f.querySelectorAll('button'),function(x){x.classList.toggle('on',x===b)});
var n=0;posts.forEach(function(p){var h=!!c&&p.getAttribute('data-cat')!==c;p.hidden=h;if(!h)n++});var e=document.querySelector('.bempty');if(e)e.hidden=n>0})})();

/* blog: el vídeo del artículo se reproduce en su sitio (youtube-nocookie) */
(function(){document.querySelectorAll('.avid[data-vid]').forEach(function(b){function go(){if(b.classList.contains('on'))return;b.classList.add('on');
var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+b.dataset.vid+'?autoplay=1&rel=0';f.title='Vídeo del artículo';f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';f.allowFullscreen=true;b.appendChild(f)}
b.addEventListener('click',go);b.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();go()}})})})();
