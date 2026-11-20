# =============================================================================
# Autor:          Robert Seebauer
# Repository:     https://github.com/Jaegerfeld/StarCitizen-Handels-Planer
# KI-Unterstützung: Erstellt mit Unterstützung von Claude (Anthropic)
# Erstellt:       20.11.2026
# Geändert:       20.11.2026
# Lizenz:         BSD-3-Clause (siehe LICENSE)
#
# Fachliche Funktion:
#   „Aufs Handy“: überträgt einen Stand vom PC auf das Handy, auf dem kein Star
#   Citizen läuft. Der PC packt den Stand (Reiter „Ruf“: Rang und Balken je
#   Organisation; Reiter „Fracht-Logbuch“: Schiffe und Fracht) als JSON,
#   komprimiert ihn (deflate-raw) und hängt ihn als base64url hinter das „#“ eines
#   Links auf die Online-Seite. Der Teil hinter „#“ wird nie an einen Server
#   geschickt. Der Link erscheint als QR-Code zum Abscannen und zum Kopieren.
#   Beim Öffnen liest die Seite den Stand, übergibt ihn an den Reiter und entfernt
#   ihn wieder aus der Adresszeile.
#   QR-Code: qrcode-generator 1.4.4 von Kazuhiko Arase (MIT-Lizenz), wird erst beim
#   Öffnen des Dialogs von jsDelivr geladen (feste Version, SRI-Prüfsumme); ohne
#   Internet bleibt der Link zum Kopieren.
# =============================================================================
"""HTML, CSS and JS fragments of the "to the phone" transfer, inserted by the page builder."""

#: Dialog markup, shared by the tabs.
HY_HTML = r"""
  <!-- Transfer a state to the phone (QR code / link) -->
  <dialog id="hy-dlg" aria-labelledby="hy-h">
    <h3 id="hy-h"></h3>
    <p id="hy-txt"></p>
    <div id="hy-qr" role="img"></div>
    <p id="hy-msg" role="status"></p>
    <input id="hy-link" type="text" readonly aria-label="Link">
    <div class="hy-btns"><button type="button" class="btn pri" id="hy-copy">⧉ <span class="de">Link kopieren</span><span class="en">Copy link</span></button>
      <form method="dialog"><button class="btn" value="x">✕ <span class="de">Schließen</span><span class="en">Close</span></button></form></div>
  </dialog>
"""

#: Styles of the dialog.
HY_CSS = r"""
  #hy-dlg{max-width:min(460px,94vw);border:1px solid var(--line);border-radius:12px;background:var(--panel);color:var(--ink);padding:16px 18px}
  #hy-dlg::backdrop{background:rgba(0,0,0,.55)}
  #hy-dlg h3{font-family:var(--disp);margin:0 0 8px}
  #hy-dlg p{font-size:13.5px;margin:0 0 10px}
  #hy-qr{display:flex;justify-content:center;margin:6px 0 10px}
  #hy-qr svg{width:min(300px,80vw);height:auto;background:#fff;border-radius:8px;padding:6px}
  #hy-msg{color:var(--muted)}
  #hy-link{width:100%;min-height:44px;font:inherit;font-size:12px;padding:0 10px;border-radius:8px;border:1px solid var(--line);background:var(--panel2);color:var(--ink);box-sizing:border-box}
  #hy-dlg .hy-btns{display:flex;gap:8px;justify-content:flex-end;flex-wrap:wrap;margin-top:12px}
  #hy-dlg .hy-btns form{margin:0}
  #hy-dlg .btn{min-height:44px}
"""

#: Behaviour. Runs after the tab scripts; RF and LB offer handyData() and fromHandy().
HY_JS = r"""
/* ---------- To the phone (QR code / link) ---------- */
const HY=(function(){
const L=()=>(document.documentElement.getAttribute('lang')||'de').slice(0,2);
const T=(de,en)=>L()==='en'?en:de;
const $h=id=>document.getElementById('hy-'+id);
const ONLINE='__ONLINE__';
const QRLIB={src:'https://cdn.jsdelivr.net/npm/qrcode-generator@1.4.4/qrcode.js',sri:'sha384-8FWZA6BGMXhsfO+BLtrJK0We6gg5o1JyO8xQm6peWDEUs17ACA5ziE/NIAkl9z2k'};
const QRMAX=2300;   // longer links are too dense to scan reliably
const b64u=bytes=>{let s=''; for(const b of bytes) s+=String.fromCharCode(b); return btoa(s).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');};
const unb64u=str=>{const s=atob(str.replace(/-/g,'+').replace(/_/g,'/')); return Uint8Array.from(s,c=>c.charCodeAt(0));};
async function pipe(bytes,stream){return new Uint8Array(await new Response(new Blob([bytes]).stream().pipeThrough(stream)).arrayBuffer());}
// "1." + base64url(deflate-raw(JSON)); "0." + base64url(JSON) where the browser cannot compress.
async function enc(obj){const raw=new TextEncoder().encode(JSON.stringify(obj));
  if(typeof CompressionStream==='function'){try{return '1.'+b64u(await pipe(raw,new CompressionStream('deflate-raw')));}catch(e){}}
  return '0.'+b64u(raw);}
async function dec(code){const [v,body]=[code.slice(0,2),code.slice(2)], bytes=unb64u(body);
  const raw=v==='1.'?await pipe(bytes,new DecompressionStream('deflate-raw')):bytes; return JSON.parse(new TextDecoder().decode(raw));}
const base=()=>/^https?:/.test(location.protocol)?location.origin+location.pathname:ONLINE;
let LIB=null;
function loadLib(){if(window.qrcode) return Promise.resolve(); if(LIB) return LIB;
  LIB=new Promise((ok,no)=>{const s=document.createElement('script'); s.src=QRLIB.src; s.integrity=QRLIB.sri; s.crossOrigin='anonymous'; s.onload=ok; s.onerror=()=>{LIB=null; no();}; document.head.appendChild(s);});
  return LIB;}
// Show the dialog with QR code and link for one tab's state.
async function share(kind,obj,title,text){const dlg=$h('dlg'); $h('h').textContent=title; $h('txt').textContent=text; $h('qr').innerHTML=''; $h('msg').textContent=T('Erzeuge Link …','Creating link …');
  if(!dlg.open) dlg.showModal();
  const link=base()+'#'+kind+'='+await enc(obj); $h('link').value=link;
  if(link.length>QRMAX){$h('msg').textContent=T(`Der Stand ist für einen QR-Code zu groß (${link.length} Zeichen). Kopiere den Link und schick ihn dir selbst (z. B. per Mail oder Messenger).`,`The state is too large for a QR code (${link.length} characters). Copy the link and send it to yourself (e.g. by mail or messenger).`); return;}
  try{await loadLib(); const q=qrcode(0,'L'); q.addData(link); q.make(); $h('qr').innerHTML=q.createSvgTag(4,2);
    $h('qr').setAttribute('aria-label',T('QR-Code mit dem Link','QR code with the link'));
    $h('msg').textContent=T('Mit der Handy-Kamera scannen – oder den Link kopieren und dir schicken.','Scan with the phone camera – or copy the link and send it to yourself.');}
  catch(e){$h('msg').textContent=T('QR-Code nicht verfügbar (offline?). Kopiere den Link und schick ihn dir selbst.','QR code not available (offline?). Copy the link and send it to yourself.');}}
$h('copy').addEventListener('click',async()=>{const b=$h('copy'); try{await navigator.clipboard.writeText($h('link').value); b.lastChild.textContent=' '+T('Kopiert ✓','Copied ✓');}
  catch(e){$h('link').select(); b.lastChild.textContent=' '+T('Markiert – Strg+C','Selected – Ctrl+C');} setTimeout(()=>{b.innerHTML=`⧉ <span class="de">Link kopieren</span><span class="en">Copy link</span>`;},1800);});
// On opening a transfer link: hand the state to its tab and clean the address bar.
async function init(){const m=/^#(ruf|lb)=([01]\.[A-Za-z0-9_-]+)$/.exec(location.hash||''); if(!m) return;
  try{history.replaceState(null,'',location.pathname+location.search);}catch(e){}
  try{const d=await dec(m[2]);
    if(m[1]==='ruf'&&typeof RF!=='undefined'){RF.fromHandy(d); showView('rep');}
    if(m[1]==='lb'&&typeof LB!=='undefined'&&LB.fromHandy){showView('ledger'); LB.fromHandy(d);}}
  catch(e){alert(T('Der Link ist unvollständig oder beschädigt – bitte am PC neu erzeugen.','The link is incomplete or damaged – please create it again on the PC.'));}}
setTimeout(init,0);
return {share, _enc:enc, _dec:dec};
})();
"""
