// ============================================================
//  COOKIES Y TEMA LEGAL
//  - Banner con Aceptar / Rechazar / Configurar (mismo peso visual).
//  - La elección se guarda 12 meses en este navegador (localStorage).
//  - Hasta que la persona acepte, no se carga nada de terceros (mapa, analítica, píxeles).
//  Las URL de los textos legales se configuran en enlaces.js (LEGAL).
// ============================================================
(function(){
  const C=window.MEDIATIC||{},LG=C.LEGAL||{},KEY='mt_consent_v1',MESES=12;
  let st=null;
  try{st=JSON.parse(localStorage.getItem(KEY)||'null');if(st&&Date.now()-st.t>MESES*30*864e5)st=null}catch(e){st=null}

  // enlaces legales (Aviso legal, Privacidad, Cookies)
  document.querySelectorAll('[data-legal]').forEach(a=>{const u=LG[a.dataset.legal];if(u){a.href=u;a.target='_blank';a.rel='noopener'}});

  // contenido de terceros que se carga solo con permiso (p. ej. el mapa de Google)
  function loadEmbed(el){
    if(el.querySelector('iframe'))return;
    const f=document.createElement('iframe');
    f.title=el.dataset.title||'';f.loading='lazy';f.referrerPolicy='no-referrer-when-downgrade';f.src=el.dataset.src;
    el.innerHTML='';el.appendChild(f);
  }
  function applyConsent(){
    if(st&&st.terceros)document.querySelectorAll('[data-embed]').forEach(loadEmbed);
    // ► Aquí se cargarán la analítica y los píxeles cuando se sepa cuáles se usan:
    //   if(st&&st.analitica){ /* Google Analytics, Clarity... */ }
    //   if(st&&st.marketing){ /* Meta Pixel, TikTok Pixel, Google Ads... */ }
    document.dispatchEvent(new CustomEvent('mt-consent',{detail:st||{necesarias:true,analitica:false,marketing:false,terceros:false}}));
  }
  document.addEventListener('click',e=>{const b=e.target.closest('[data-load-embed]');if(b)loadEmbed(b.closest('[data-embed]'))});

  function save(v){st={t:Date.now(),necesarias:true,analitica:!!v.analitica,marketing:!!v.marketing,terceros:!!v.terceros};
    try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}
    hideBanner();hidePanel();applyConsent()}

  // interfaz
  const wrap=document.createElement('div');
  const cookieLink=LG.cookies||'#';
  wrap.innerHTML=
  '<div class="ck" role="dialog" aria-live="polite" aria-label="Aviso de cookies" hidden>'+
    '<p><b>Tu privacidad, tu decisión.</b> Usamos cookies propias y de terceros para que la web funcione, medir su uso y mostrar contenido externo (como el mapa). Puedes aceptarlas, rechazarlas o elegir cuáles. Más información en la <a href="'+cookieLink+'" data-legal="cookies" target="_blank" rel="noopener">Política de cookies</a>.</p>'+
    '<div class="ck-row"><button type="button" class="ck-b ck-no" data-ck="no">Rechazar</button><button type="button" class="ck-b ck-yes" data-ck="yes">Aceptar todas</button></div>'+
    '<button type="button" class="ck-cfg" data-ck="cfg">Configurar</button>'+
  '</div>'+
  '<div class="ckp" role="dialog" aria-modal="true" aria-label="Configurar cookies" hidden><div class="ckp-box">'+
    '<h3>Configurar cookies</h3>'+
    '<label class="ckp-i"><div><b>Necesarias</b><span>Hacen que la web funcione (guardan tu elección de cookies). Siempre activas.</span></div><input type="checkbox" checked disabled></label>'+
    '<label class="ckp-i"><div><b>Analíticas</b><span>Nos dicen cómo se usa la web para mejorarla.</span></div><input type="checkbox" id="ck-an"></label>'+
    '<label class="ckp-i"><div><b>Marketing</b><span>Nos permiten medir de qué anuncio o enlace llegas.</span></div><input type="checkbox" id="ck-mk"></label>'+
    '<label class="ckp-i"><div><b>Contenido de terceros</b><span>Mapa de Google y otros contenidos externos.</span></div><input type="checkbox" id="ck-tr"></label>'+
    '<div class="ck-row"><button type="button" class="ck-b ck-no" data-ck="no">Rechazar todas</button><button type="button" class="ck-b ck-yes" data-ck="yes">Aceptar todas</button></div>'+
    '<button type="button" class="ck-save" data-ck="save">Guardar mi selección</button>'+
  '</div></div>';
  document.body.appendChild(wrap);
  const banner=wrap.querySelector('.ck'),panel=wrap.querySelector('.ckp');
  const showBanner=()=>{banner.hidden=false},hideBanner=()=>{banner.hidden=true};
  const showPanel=()=>{wrap.querySelector('#ck-an').checked=!!(st&&st.analitica);wrap.querySelector('#ck-mk').checked=!!(st&&st.marketing);wrap.querySelector('#ck-tr').checked=!!(st&&st.terceros);panel.hidden=false},hidePanel=()=>{panel.hidden=true};
  wrap.addEventListener('click',e=>{
    const b=e.target.closest('[data-ck]');
    if(b){const k=b.dataset.ck;
      if(k==='yes')save({analitica:1,marketing:1,terceros:1});
      else if(k==='no')save({});
      else if(k==='cfg')showPanel();
      else if(k==='save')save({analitica:wrap.querySelector('#ck-an').checked,marketing:wrap.querySelector('#ck-mk').checked,terceros:wrap.querySelector('#ck-tr').checked});
      return}
    if(e.target===panel)hidePanel();
  });
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!panel.hidden)hidePanel()});
  document.querySelectorAll('[data-open-cookies]').forEach(b=>b.addEventListener('click',showPanel));

  if(!st)showBanner();
  applyConsent();
})();
