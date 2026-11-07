// ============================================================
//  ENLACES DE LOS BOTONES (para medir con UTM)
//  Pega aquí el enlace de cada botón. Si dejas '' el botón usa el destino por defecto.
//  Si el enlace empieza por http, se abre en una pestaña nueva.
// ============================================================
window.MEDIATIC = {
  DESTINO_POR_DEFECTO: 'index.html#contacto',

  ENLACES: {
    'cabecera':     '',  // Botón de arriba a la derecha: "Agendar llamada" (sale en todas las páginas)
    'contrataciones':'', // Opción "Contrataciones" del menú de arriba
    'hero':         '',  // Botón del inicio: "Quiero conseguir estos resultados"
    'quienes-somos':'',  // Botón de ¿Quiénes somos?: "Quiero que trabajemos juntos"
    'resultados':   '',  // Botón del bloque azul de reels: "Quiero estos resultados"
    'pie':          '',  // Botón "Pedir presupuesto" del pie de página (sale en todas las páginas)
    'blog-lateral': '',  // Botón fijo del lateral de los artículos del blog: "Agendar diagnóstico"
    'blog-articulo':''   // Enlace de texto dentro de los artículos del blog: "agenda una sesión de diagnóstico"
  },

  // Redes sociales del pie de página. Si dejas '' en LinkedIn, el enlace no lleva a ningún sitio.
  REDES: {
    instagram: 'https://www.instagram.com/mediatic.io/',
    youtube:   'https://www.youtube.com/@mediatic.agencia',
    linkedin:  ''
  },

  // Textos legales (pon aquí las URL completas). Se usan en el pie de página, en el aviso de cookies y en el formulario.
  LEGAL: {
    aviso:      'aviso-legal.html',  // Aviso legal
    privacidad: 'politica-privacidad.html',  // Política de privacidad
    cookies:    'politica-cookies.html'   // Política de cookies
  },

  // Formulario de cualificación que se abre en una pestaña nueva al enviar el formulario corto.
  // Cuando lo publiques, pon aquí su URL completa (por ejemplo https://forms.mediatic.io/).
  FORMULARIO: '../formulario/index.html',

  // Datos del formulario corto que viajan al formulario largo (nombre, email, teléfono...).
  // Ponlo en false si prefieres que solo viajen las UTM.
  PASAR_DATOS_AL_FORMULARIO: true,

  // Parámetros de UTM que se guardan y se reenvían al formulario.
  UTM: ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term']
};
