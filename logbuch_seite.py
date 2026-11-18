# =============================================================================
# Autor:          Robert Seebauer
# Repository:     https://github.com/Jaegerfeld/StarCitizen-Handels-Planer
# KI-Unterstützung: Erstellt mit Unterstützung von Claude (Anthropic)
# Erstellt:       18.11.2026
# Geändert:       18.11.2026
# Lizenz:         BSD-3-Clause (siehe LICENSE)
#
# Fachliche Funktion:
#   Oberfläche des Reiters „Fracht-Logbuch“ (HTML, CSS, JS): Der Spieler führt
#   Buch, welche Ware in welchen Containern an welcher Station oder auf welchem
#   seiner Schiffe liegt. Links die eigenen Schiffe mit Füllbalken (Überladen
#   je Schiff schaltbar, Standard +1/3), rechts die Orte mit Frachtaufzug nach
#   System und Planet, in der Mitte der gewählte Ort mit seinen Posten.
#   Verschieben per Drag & Drop oder per Klick/Antippen mit Mengenabfrage
#   (Container-Anzahl oder SCU), Einbuchen, Ausbuchen, Journal mit Rückgängig.
#   Warnungen (Laderaum, Containergröße, illegal, flüchtig) sperren nie.
#   Gespeichert wird nur im Browser; Export als JSON (auch wieder einlesbar)
#   und XLSX (ohne fremde Bibliothek, eigener ZIP-Schreiber). Kein Server.
#   Alles ist mit lb- bzw. #view-ledger abgegrenzt.
# =============================================================================
"""HTML, CSS and JS fragments of the "Fracht-Logbuch" tab, inserted by the page builder."""

#: Tab button, placed after the existing view tabs.
LB_TAB = ('    <button class="tab" role="tab" data-view="ledger" aria-selected="false">'
          '<span class="de">Fracht-Logbuch</span><span class="en">Cargo ledger</span></button>\n')

#: Panel and dialogs.
LB_HTML = r"""
  <!-- Cargo ledger -->
  <section class="panel hide" id="view-ledger">
    <div class="lb-bar">
      <button type="button" class="btn" id="lb-undo" disabled>↶ <span class="de">Rückgängig</span><span class="en">Undo</span></button>
      <span class="lb-sp"></span>
      <button type="button" class="btn" id="lb-xlsx">⬇ <span class="de">Export XLSX</span><span class="en">Export XLSX</span></button>
      <button type="button" class="btn" id="lb-json">⬇ <span class="de">Export JSON</span><span class="en">Export JSON</span></button>
      <button type="button" class="btn" id="lb-imp">⬆ <span class="de">JSON einlesen</span><span class="en">Import JSON</span></button>
      <input type="file" id="lb-file" accept=".json,application/json" hidden>
    </div>
    <p class="lb-note"><span class="de">Dein Logbuch wird nur in diesem Browser gespeichert. Sichere es ab und zu per „Export JSON“.</span><span class="en">Your ledger is stored in this browser only. Back it up now and then with “Export JSON”.</span></p>
    <div class="lb-grid">
      <aside class="lb-col" aria-labelledby="lb-hs">
        <h3 id="lb-hs"><span class="de">Meine Schiffe</span><span class="en">My ships</span></h3>
        <div id="lb-ships"></div>
        <button type="button" class="btn lb-add" id="lb-addship">+ <span class="de">Schiff hinzufügen</span><span class="en">Add ship</span></button>
      </aside>
      <main class="lb-mid" id="lb-mid" aria-live="polite"></main>
      <aside class="lb-col" aria-labelledby="lb-hp">
        <h3 id="lb-hp"><span class="de">Orte</span><span class="en">Places</span></h3>
        <label class="lb-f"><span class="de">Suche</span><span class="en">Search</span><input type="search" id="lb-q" autocomplete="off"></label>
        <div class="lb-f2">
          <label class="lb-f"><span class="de">System</span><span class="en">System</span><select id="lb-sys"></select></label>
          <label class="lb-chk"><input type="checkbox" id="lb-only"> <span class="de">nur mit Fracht</span><span class="en">with cargo only</span></label>
        </div>
        <div id="lb-places" class="lb-places"></div>
      </aside>
    </div>
    <details class="lb-journal"><summary><span class="de">Journal</span><span class="en">Journal</span> <span id="lb-jn"></span></summary><ol id="lb-log"></ol></details>
  </section>

  <dialog id="lb-dlg" class="lb-dlg" aria-labelledby="lb-dt"><form method="dialog" id="lb-form"><h3 id="lb-dt"></h3><div id="lb-db"></div><div class="lb-warn" id="lb-dw" role="status"></div><div class="lb-dbtn" id="lb-dbtn"></div></form></dialog>
  <datalist id="lb-wlist"></datalist><datalist id="lb-slist"></datalist>
"""

#: Styles, all scoped to the ledger panel and its dialog.
LB_CSS = r"""
  #view-ledger .lb-bar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:0 0 6px}
  #view-ledger .lb-bar .btn{min-height:44px}
  #view-ledger .lb-sp{flex:1}
  #view-ledger .lb-note{color:var(--muted);font-size:12.5px;margin:0 0 12px}
  #view-ledger .lb-grid{display:grid;grid-template-columns:250px minmax(0,1fr) 270px;gap:14px;align-items:start}
  #view-ledger .lb-col{background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:10px}
  #view-ledger h3{font-family:var(--disp);font-size:15px;letter-spacing:.06em;text-transform:uppercase;color:var(--accent);margin:0 0 8px}
  #view-ledger .lb-add{width:100%;margin-top:8px;min-height:44px;justify-content:center}
  .lb-ship,.lb-place{display:block;width:100%;text-align:left;font:inherit;color:var(--ink);background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:8px 10px;margin:0 0 6px;min-height:44px;cursor:pointer}
  .lb-ship:hover,.lb-place:hover,.lb-ship:focus-visible,.lb-place:focus-visible{border-color:var(--accent)}
  .lb-ship[aria-current="true"],.lb-place[aria-current="true"]{border:2px solid var(--accent)}
  .lb-ship.drop,.lb-place.drop{background:var(--glow);border-color:var(--accent);border-style:dashed}
  .lb-ship b,.lb-place b{font-family:var(--disp);font-size:15.5px}
  .lb-ship small,.lb-place small{display:block;color:var(--muted);font-size:12px}
  .lb-fill{position:relative;height:8px;border-radius:5px;background:var(--line);margin:5px 0 2px;overflow:hidden}
  .lb-fill i{position:absolute;left:0;top:0;bottom:0;background:var(--accent)}
  .lb-fill i.over{background:repeating-linear-gradient(45deg,var(--bad) 0 4px,var(--accent2) 4px 8px)}
  .lb-fill s{position:absolute;top:-2px;bottom:-2px;width:2px;background:var(--ink);opacity:.6}
  .lb-scu{font-size:12px;color:var(--muted)} .lb-scu .lb-ow{color:var(--bad);font-weight:700}
  #view-ledger .lb-f{display:flex;flex-direction:column;gap:3px;font-size:12px;color:var(--muted);margin:0 0 8px}
  #view-ledger .lb-f input,#view-ledger .lb-f select,.lb-dlg input,.lb-dlg select{font:inherit;font-size:14px;background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:7px 10px;min-height:40px}
  #view-ledger .lb-f2{display:flex;gap:8px;align-items:end;flex-wrap:wrap}
  .lb-chk{display:flex;gap:6px;align-items:center;font-size:13.5px;min-height:40px;cursor:pointer;margin:0 0 8px}
  .lb-chk input{width:18px;height:18px;accent-color:var(--accent)}
  .lb-places{max-height:640px;overflow:auto;padding-right:2px}
  .lb-gsys{font-family:var(--disp);font-weight:700;font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent2);margin:10px 0 4px}
  .lb-gbody{font-size:12px;color:var(--muted);margin:6px 0 3px}
  .lb-badge{float:right;font-family:var(--disp);font-weight:700;font-size:12.5px;color:var(--accent)}
  #view-ledger .lb-mid{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px;min-height:340px}
  .lb-mid h2{margin:0;font-size:22px}
  .lb-meta{color:var(--muted);font-size:13px;margin:2px 0 10px}
  .lb-acts{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 12px}
  .lb-acts .btn{min-height:44px}
  .lb-acts .btn.pri{background:var(--accent);border-color:var(--accent);color:var(--bg)}
  .lb-ware{border-top:1px solid var(--line);padding:10px 0 6px}
  .lb-ware:first-of-type{border-top:0}
  .lb-wh{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}
  .lb-wh b{font-family:var(--disp);font-size:16.5px} .lb-wh .lb-tot{margin-left:auto;font-family:var(--disp);font-weight:700}
  .lb-tag{font-size:11px;font-weight:700;border-radius:20px;padding:0 8px;border:1px solid var(--line);color:var(--muted)}
  .lb-tag.il{border-color:var(--bad);color:var(--bad)} .lb-tag.vol{border-color:var(--accent2);color:var(--accent2)}
  .lb-chips{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}
  .lb-chip{font:inherit;font-family:var(--disp);font-weight:700;font-size:14px;min-height:44px;min-width:88px;padding:0 12px;border-radius:8px;border:1px solid var(--line);background:var(--panel2);color:var(--ink);cursor:grab}
  .lb-chip:hover,.lb-chip:focus-visible{border-color:var(--accent);color:var(--accent)}
  .lb-chip small{font-weight:500;color:var(--muted);margin-left:4px}
  .lb-empty{color:var(--muted);padding:16px 4px}
  .lb-empty .btn{margin-top:10px;min-height:44px}
  .lb-journal{margin-top:14px;border:1px solid var(--line);border-radius:10px;padding:8px 12px;background:var(--panel2)}
  .lb-journal summary{cursor:pointer;font-family:var(--disp);font-weight:700;min-height:32px;display:flex;align-items:center;gap:6px}
  .lb-journal ol{margin:6px 0 4px;padding-left:22px;max-height:260px;overflow:auto;font-size:13px}
  .lb-journal li{margin:2px 0} .lb-journal time{color:var(--muted);font-variant-numeric:tabular-nums;margin-right:6px}
  .lb-dlg{border:1px solid var(--line);border-radius:12px;background:var(--panel);color:var(--ink);padding:18px 20px;width:min(460px,94vw);box-shadow:var(--shadow)}
  .lb-dlg::backdrop{background:rgba(0,0,0,.45)}
  .lb-dlg h3{font-family:var(--disp);font-size:20px;margin:0 0 10px}
  .lb-dlg label{display:flex;flex-direction:column;gap:4px;font-size:12.5px;color:var(--muted);margin:0 0 10px}
  .lb-dlg .lb-row{display:flex;gap:10px;flex-wrap:wrap}
  .lb-dlg .lb-row>label{flex:1 1 120px}
  .lb-dlg fieldset{border:1px solid var(--line);border-radius:8px;margin:0 0 10px;padding:4px 10px;display:flex;gap:14px}
  .lb-dlg fieldset label{flex-direction:row;align-items:center;gap:6px;font-size:14px;color:var(--ink);margin:0;min-height:40px}
  .lb-dlg .lb-hint{font-size:12.5px;color:var(--muted);margin:-4px 0 10px}
  .lb-warn:empty{display:none}
  .lb-warn{background:var(--panel2);border-left:4px solid var(--accent2);border-radius:0 8px 8px 0;padding:8px 10px;font-size:13px;margin:0 0 10px}
  .lb-warn p{margin:0 0 3px}
  .lb-dbtn{display:flex;gap:10px;flex-wrap:wrap;margin-top:6px}
  .lb-dbtn .btn{min-height:44px}
  .lb-dbtn .pri{background:var(--accent);border-color:var(--accent);color:var(--bg)}
  .lb-dbtn .danger{border-color:var(--bad);color:var(--bad);margin-left:auto}
  @media (max-width:900px){
    #view-ledger .lb-grid{grid-template-columns:minmax(0,1fr)}
    #view-ledger .lb-mid{order:-1}
    .lb-places{max-height:360px}
  }
"""

#: Behaviour. Runs before the page's view switcher, which calls ``LB.render``.
LB_JS = r"""
/* ---------- Cargo ledger ---------- */
const LB=(function(){
const M=/*__LB__*/null;
const KEY='scha_ledger_v1';
const L=()=>(document.documentElement.getAttribute('lang')||'de').slice(0,2);
const T=(de,en)=>L()==='en'?en:de;
const $l=id=>document.getElementById('lb-'+id);
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const nf=n=>Number(n||0).toLocaleString(L()==='en'?'en-US':'de-DE');
if(!M){return {render(){const b=document.getElementById('view-ledger');
  if(b) b.innerHTML=`<p class="lb-empty">${T('Die Stammdaten (Orte, Waren, Schiffe) waren beim letzten Bau nicht erreichbar. Der nächste Bau holt sie neu.','The master data (places, commodities, ships) was unavailable at the last build. The next build fetches it again.')}</p>`;}};}
const PL={}; for(const p of M.places) PL[p.id]=p;
const WA={}; for(const w of M.wares) WA[w.id]=w;
const SH={}; for(const s of M.ships) SH[s.id]=s;

/* ---------- state ---------- */
// The whole ledger: own ships, stock posts (location, commodity, container size, count), journal.
let S={v:1,ships:[],stock:[],log:[],sel:null};
const UNDO=[];
function load(){try{const s=JSON.parse(localStorage.getItem(KEY)||'null'); if(s&&s.v===1) S=Object.assign(S,s);}catch(e){}}
function save(){try{localStorage.setItem(KEY,JSON.stringify(S));}catch(e){}}
// Remember the state before a change so it can be undone.
function snap(){UNDO.push(JSON.stringify({ships:S.ships,stock:S.stock})); if(UNDO.length>50) UNDO.shift();}
function log(text){S.log.unshift({t:new Date().toISOString(),x:text}); if(S.log.length>500) S.log.length=500;}
function commit(text,undoable=true){log(text); save(); render(); toastUndo(text,undoable);}
function undo(){const u=UNDO.pop(); if(!u) return; const o=JSON.parse(u); S.ships=o.ships; S.stock=o.stock; log(T('Rückgängig gemacht','Undone')); save(); render(); toast(T('Rückgängig gemacht.','Undone.'));}
function toastUndo(text){toast(text+' · '+T('Rückgängig: Strg+Z oder Knopf oben','Undo: Ctrl+Z or button above'));}

/* ---------- helpers ---------- */
const shipById=id=>S.ships.find(s=>s.id===id);
function locName(loc){if(!loc) return '–'; const [k,id]=[loc.slice(0,1),loc.slice(2)];
  if(k==='s'){const s=shipById(id); return s?s.n:'?';} const p=PL[id]; return p?p.n:id;}
function used(loc){return S.stock.filter(p=>p.l===loc).reduce((a,p)=>a+p.z*p.n,0);}
// Cargo space of an own ship: base from the data, max with overload switched on.
function cap(s){const base=SH[s.t]?.scu||0; return {base, max:s.ov?Math.round(base*(1+(s.op||33)/100)):base};}
function maxBox(loc){if(!loc) return 32; if(loc[0]==='s'){const s=shipById(loc.slice(2)); return SH[s?.t]?.cs||32;} return PL[loc.slice(2)]?.max||32;}
function wTags(w){if(!w) return ''; return (w.il?`<span class="lb-tag il">⚠ ${T('illegal','illegal')}</span>`:'')+
  (w.vq?`<span class="lb-tag vol">⚡ ${T('Quantum-flüchtig','quantum-volatile')}</span>`:'')+(w.vt?`<span class="lb-tag vol">⏳ ${T('verdirbt mit der Zeit','decays over time')}</span>`:'');}
// Add containers to a location, merging with an existing post of the same commodity and size.
function put(loc,w,z,n){const p=S.stock.find(q=>q.l===loc&&q.w===w&&q.z===z); if(p) p.n+=n; else S.stock.push({l:loc,w,z,n});}
function take(p,n){p.n-=n; if(p.n<=0) S.stock.splice(S.stock.indexOf(p),1);}
function warnings(loc,w,z,addScu){const out=[]; const wa=WA[w];
  if(loc&&loc[0]==='s'){const s=shipById(loc.slice(2)); if(s){const c=cap(s), u=used(loc)+addScu;
    if(u>c.max) out.push(T(`Mehr Fracht als Laderaum: ${nf(u)} von ${nf(c.max)} SCU${s.ov?' (mit Überladen)':''}.`,`More cargo than space: ${nf(u)} of ${nf(c.max)} SCU${s.ov?' (with overload)':''}.`));
    else if(u>c.base) out.push(T(`Überladen: ${nf(u-c.base)} SCU liegen außerhalb des Frachtgitters und können verrutschen oder verloren gehen.`,`Overloaded: ${nf(u-c.base)} SCU sit outside the cargo grid and can shift or be lost.`));}}
  const mb=maxBox(loc); if(z>mb) out.push(loc[0]==='s'?T(`Dieses Schiff nimmt Container nur bis ${mb} SCU.`,`This ship only takes containers up to ${mb} SCU.`):T(`Der Frachtaufzug dort nimmt Container nur bis ${mb} SCU.`,`The freight elevator there only takes containers up to ${mb} SCU.`));
  if(wa?.il) out.push(T('Illegale Ware: Scans und Zoll beachten.','Illegal commodity: mind scans and customs.'));
  if(wa?.vq||wa?.vt) out.push(T('Flüchtige Ware: verdirbt mit der Zeit oder bei Quantum-Sprüngen.','Volatile commodity: decays over time or on quantum jumps.'));
  return out;}

/* ---------- rendering ---------- */
function fillBar(s,loc){const c=cap(s), u=used(loc), top=Math.max(c.max,u,1);
  const pct=Math.min(100,u/top*100), mark=c.base/top*100, over=u>c.base;
  return `<div class="lb-fill" role="img" aria-label="${nf(u)} / ${nf(c.base)} SCU"><i class="${over?'over':''}" style="width:${pct}%"></i>${c.max>c.base?`<s style="left:${mark}%"></s>`:''}</div>
    <div class="lb-scu">${nf(u)} / ${nf(c.base)} SCU${over?` · <span class="lb-ow">⚠ ${T('überladen','overloaded')} +${nf(u-c.base)}</span>`:''}${s.ov&&!over?` · ${T('Überladen an','overload on')} (+${s.op||33} %)`:''}</div>`;}
function renderShips(){const box=$l('ships');
  box.innerHTML=S.ships.length?S.ships.map(s=>{const loc='s:'+s.id;
    return `<button type="button" class="lb-ship" data-loc="${loc}" aria-current="${S.sel===loc}"><b>${esc(s.n)}</b><small>${esc(SH[s.t]?.n||'?')}</small>${fillBar(s,loc)}</button>`}).join('')
   :`<p class="lb-empty">${T('Noch kein Schiff. Lege deine Frachtschiffe an, dann siehst du ihren Laderaum.','No ship yet. Add your cargo ships to see their cargo space.')}</p>`;}
function renderPlaces(){const q=($l('q').value||'').trim().toLowerCase(), sys=$l('sys').value, only=$l('only').checked;
  let html='', lastS='', lastB=null;
  for(const p of M.places){const loc='p:'+p.id, u=used(loc);
    if(sys&&p.sys!==sys) continue; if(only&&!u) continue; if(q&&!(p.n+' '+p.body+' '+p.sys).toLowerCase().includes(q)) continue;
    if(p.sys!==lastS){html+=`<div class="lb-gsys">${esc(p.sys)}</div>`; lastS=p.sys; lastB=null;}
    if(p.body!==lastB){html+=`<div class="lb-gbody">${esc(p.body||T('im All','in space'))}</div>`; lastB=p.body;}
    html+=`<button type="button" class="lb-place" data-loc="${esc(loc)}" aria-current="${S.sel===loc}">${u?`<span class="lb-badge">${nf(u)} SCU</span>`:''}<b>${esc(p.n)}</b>${p.max?`<small>${T('Aufzug bis','elevator up to')} ${p.max} SCU</small>`:''}</button>`;}
  $l('places').innerHTML=html||`<p class="lb-empty">${T('Kein Ort passt zu Suche und Filter.','No place matches the search and filter.')}</p>`;}
function renderMid(){const box=$l('mid'), loc=S.sel;
  if(!loc){box.innerHTML=`<div class="lb-empty"><h2>${T('Fracht-Logbuch','Cargo ledger')}</h2><p>${T('Wähle rechts einen Ort oder links ein Schiff. Dort buchst du Fracht ein und verschiebst sie per Klick oder Ziehen.','Pick a place on the right or a ship on the left. Book cargo in there and move it by click or drag.')}</p>${S.ships.length?'':`<button type="button" class="btn" data-act="addship">+ ${T('Erstes Schiff hinzufügen','Add your first ship')}</button>`}</div>`; return;}
  const isShip=loc[0]==='s', s=isShip?shipById(loc.slice(2)):null, p=isShip?null:PL[loc.slice(2)];
  if(isShip&&!s||!isShip&&!p){S.sel=null; renderMid(); return;}
  const posts=S.stock.filter(q=>q.l===loc), byW={};
  for(const q of posts)(byW[q.w]=byW[q.w]||[]).push(q);
  const meta=isShip?`${esc(SH[s.t]?.n||'?')} · ${T('Container bis','containers up to')} ${SH[s.t]?.cs||'?'} SCU`:`${esc(p.sys)}${p.body?' · '+esc(p.body):''}${p.max?` · ${T('Aufzug bis','elevator up to')} ${p.max} SCU`:''}`;
  let html=`<h2>${esc(isShip?s.n:p.n)}</h2><div class="lb-meta">${meta}</div>${isShip?fillBar(s,loc):''}
    <div class="lb-acts"><button type="button" class="btn pri" data-act="in">+ ${T('Fracht einbuchen','Book cargo in')}</button>${isShip?`<button type="button" class="btn" data-act="editship">✎ ${T('Schiff bearbeiten','Edit ship')}</button>`:''}</div>`;
  const ws=Object.keys(byW).sort((a,b)=>(WA[a]?.n||'').localeCompare(WA[b]?.n||''));
  if(!ws.length) html+=`<p class="lb-empty">${T('Hier liegt nichts. Buche Fracht ein oder ziehe einen Posten von einem anderen Ort hierher.','Nothing here. Book cargo in or drag a post here from another place.')}</p>`;
  for(const w of ws){const list=byW[w].sort((a,b)=>b.z-a.z), tot=list.reduce((a,q)=>a+q.z*q.n,0);
    html+=`<div class="lb-ware"><div class="lb-wh"><b>${esc(WA[w]?.n||'?')}</b>${wTags(WA[w])}<span class="lb-tot">${nf(tot)} SCU</span></div><div class="lb-chips">${list.map(q=>
      `<button type="button" class="lb-chip" draggable="true" data-i="${S.stock.indexOf(q)}" title="${T('Klicken: verschieben oder ausbuchen · Ziehen: auf ein Schiff oder einen Ort','Click: move or book out · Drag: onto a ship or place')}">${q.z} SCU × ${q.n}<small>= ${nf(q.z*q.n)}</small></button>`).join('')}</div></div>`;}
  box.innerHTML=html;}
function renderLog(){$l('jn').textContent=S.log.length?`(${S.log.length})`:'';
  $l('log').innerHTML=S.log.slice(0,200).map(e=>`<li><time>${new Date(e.t).toLocaleString(L()==='en'?'en-GB':'de-DE',{dateStyle:'short',timeStyle:'short'})}</time>${esc(e.x)}</li>`).join('')||`<li>${T('Noch keine Buchung.','No entries yet.')}</li>`;}
function render(){const sys=$l('sys'), cur=sys.value;
  sys.innerHTML=`<option value="">${T('alle Systeme','all systems')}</option>`+[...new Set(M.places.map(p=>p.sys))].map(x=>`<option${x===cur?' selected':''}>${esc(x)}</option>`).join('');
  $l('wlist').innerHTML=M.wares.map(w=>`<option value="${esc(w.n)}">`).join('');
  $l('slist').innerHTML=M.ships.map(s=>`<option value="${esc(s.n)}">${s.scu} SCU</option>`).join('');
  renderShips(); renderPlaces(); renderMid(); renderLog(); $l('undo').disabled=!UNDO.length;}
function select(loc){S.sel=loc; save(); render(); if(matchMedia('(max-width:900px)').matches) $l('mid').scrollIntoView({behavior:'smooth',block:'start'});}

/* ---------- dialogs ---------- */
let dlgOk=null;
// Open the shared dialog with a title, body, live warnings and buttons; ok(form) returns true to close.
function dialog(title,body,buttons,onInput){const d=$l('dlg'); $l('dt').textContent=title; $l('db').innerHTML=body; $l('dw').innerHTML='';
  $l('dbtn').innerHTML=buttons.map(b=>`<button type="button" class="btn ${b.cls||''}" data-b="${b.id}">${b.label}</button>`).join('');
  dlgOk=buttons; const upd=()=>{if(onInput){const w=onInput(); $l('dw').innerHTML=w.map(x=>`<p>⚠ ${esc(x)}</p>`).join('');}};
  $l('db').oninput=upd; $l('db').onchange=upd; upd(); d.showModal(); const f=d.querySelector('input,select'); if(f) f.focus();}
function closeDlg(){$l('dlg').close();}
function targetOptions(except){const sh=S.ships.map(s=>`<option value="s:${s.id}"${'s:'+s.id===except?' disabled':''}>${esc(s.n)}</option>`).join('');
  let pl='',ls=''; for(const p of M.places){if(p.sys!==ls){pl+=(ls?'</optgroup>':'')+`<optgroup label="${esc(p.sys)}">`; ls=p.sys;} pl+=`<option value="p:${esc(p.id)}"${'p:'+p.id===except?' disabled':''}>${esc(p.n)}${p.body?' · '+esc(p.body):''}</option>`;}
  return (sh?`<optgroup label="${T('Meine Schiffe','My ships')}">${sh}</optgroup>`:'')+pl+'</optgroup>';}
// Move (or book out) part of a post; target preset when dropped onto a ship or place.
function openMove(i,target){const p=S.stock[i]; if(!p) return; const w=WA[p.w];
  if(target&&target===p.l) return;
  const body=`<p class="lb-hint">${esc(w?.n||'?')} · ${p.z} SCU × ${p.n} · ${T('liegt in','at')} ${esc(locName(p.l))}</p>
    <label>${T('Nach','To')}<select id="lb-mto">${targetOptions(p.l)}</select></label>
    <fieldset><label><input type="radio" name="lb-mm" value="c" checked> ${T('Container','Containers')}</label><label><input type="radio" name="lb-mm" value="s"> SCU</label></fieldset>
    <label><span id="lb-mlab">${T('Anzahl Container','Number of containers')} (max. ${p.n})</span><input type="number" id="lb-mn" min="1" max="${p.n}" value="${p.n}" inputmode="numeric"></label>`;
  const amount=()=>{const v=Math.floor(+$l('mn').value||0), mode=document.querySelector('input[name=lb-mm]:checked').value;
    if(mode==='s'){if(v%p.z) return {err:T(`${nf(v)} SCU gehen nicht in ${p.z}-SCU-Container auf; nimm ein Vielfaches von ${p.z}.`,`${nf(v)} SCU do not split into ${p.z} SCU containers; use a multiple of ${p.z}.`)}; return {n:v/p.z};}
    return {n:v};};
  dialog(T('Verschieben','Move'),body,[{id:'mv',label:T('Verschieben','Move'),cls:'pri'},{id:'cx',label:T('Abbrechen','Cancel')},{id:'out',label:T('Ausbuchen','Book out'),cls:'danger'}],()=>{
    const mode=document.querySelector('input[name=lb-mm]:checked').value; $l('mlab').textContent=mode==='s'?`SCU (max. ${nf(p.z*p.n)})`:`${T('Anzahl Container','Number of containers')} (max. ${p.n})`;
    const a=amount(); if(a.err) return [a.err]; if(!(a.n>=1&&a.n<=p.n)) return [T(`Menge zwischen 1 und ${p.n} Containern.`,`Amount between 1 and ${p.n} containers.`)];
    return warnings($l('mto').value,p.w,p.z,a.n*p.z);});
  if(target) $l('mto').value=target;
  $l('mto').dispatchEvent(new Event('change',{bubbles:true}));
  dlgAct=b=>{const a=amount(); if(b==='cx'){closeDlg();return;} if(a.err||!(a.n>=1&&a.n<=p.n)){$l('mn').focus();return;}
    if(b==='out'){snap(); take(p,a.n); closeDlg(); commit(T(`Ausgebucht: ${w?.n} ${p.z} SCU × ${a.n} aus ${locName(p.l)}`,`Booked out: ${w?.n} ${p.z} SCU × ${a.n} from ${locName(p.l)}`)); return;}
    const to=$l('mto').value, from=p.l; snap(); take(p,a.n); put(to,p.w,p.z,a.n); closeDlg();
    commit(T(`Verschoben: ${w?.n} ${p.z} SCU × ${a.n} von ${locName(from)} nach ${locName(to)}`,`Moved: ${w?.n} ${p.z} SCU × ${a.n} from ${locName(from)} to ${locName(to)}`));};}
// Book new cargo in at the selected place or ship.
function openIn(){const loc=S.sel, mb=maxBox(loc);
  const body=`<p class="lb-hint">${T('Nach','To')} ${esc(locName(loc))}</p>
    <label>${T('Ware','Commodity')}<input id="lb-iw" list="lb-wlist" autocomplete="off" placeholder="${T('z. B. Laranite','e.g. Laranite')}"></label>
    <div class="lb-row"><label>${T('Containergröße','Container size')}<select id="lb-iz">${M.sizes.map(z=>`<option value="${z}"${z===Math.min(32,mb)?' selected':''}>${z} SCU</option>`).join('')}</select></label>
    <label>${T('Anzahl','Count')}<input type="number" id="lb-in" min="1" value="1" inputmode="numeric"></label></div>`;
  const ware=()=>{const v=($l('iw').value||'').trim().toLowerCase(); return M.wares.find(w=>w.n.toLowerCase()===v)||null;};
  dialog(T('Fracht einbuchen','Book cargo in'),body,[{id:'ok',label:T('Einbuchen','Book in'),cls:'pri'},{id:'cx',label:T('Abbrechen','Cancel')}],()=>{
    const w=ware(), z=+$l('iz').value, n=Math.floor(+$l('in').value||0); const out=[];
    if(($l('iw').value||'').trim()&&!w) out.push(T('Ware nicht gefunden: bitte aus der Liste wählen.','Commodity not found: please pick from the list.'));
    if(n<1) out.push(T('Anzahl mindestens 1.','Count at least 1.'));
    return out.concat(w&&n>=1?warnings(loc,w.id,z,z*n):[]);});
  dlgAct=b=>{if(b==='cx'){closeDlg();return;} const w=ware(), z=+$l('iz').value, n=Math.floor(+$l('in').value||0);
    if(!w){$l('iw').focus();return;} if(n<1){$l('in').focus();return;}
    snap(); put(loc,w.id,z,n); closeDlg(); commit(T(`Eingebucht: ${w.n} ${z} SCU × ${n} in ${locName(loc)}`,`Booked in: ${w.n} ${z} SCU × ${n} at ${locName(loc)}`));};}
// Add or edit an own ship (type from the data, own name, overload switch).
function openShip(edit){const s=edit?shipById(S.sel.slice(2)):null;
  const body=`<label>${T('Schiffstyp','Ship type')}<input id="lb-st" list="lb-slist" autocomplete="off" value="${esc(s?SH[s.t]?.n:'')}" placeholder="${T('z. B. Crusader C2','e.g. Crusader C2')}"></label>
    <label>${T('Eigener Name (optional)','Own name (optional)')}<input id="lb-sn" value="${esc(s?s.n:'')}" placeholder="${T('z. B. Lastesel','e.g. Workhorse')}"></label>
    <label class="lb-chk" style="flex-direction:row"><input type="checkbox" id="lb-so"${s?.ov?' checked':''}> ${T('Überladen erlauben (Fracht außerhalb des Frachtgitters)','Allow overload (cargo outside the cargo grid)')}</label>
    <label>${T('Überladen bis (% über Laderaum)','Overload up to (% above cargo space)')}<input type="number" id="lb-sp" min="1" max="100" value="${s?.op||33}" inputmode="numeric"></label>`;
  const type=()=>{const v=($l('st').value||'').trim().toLowerCase(); return M.ships.find(x=>x.n.toLowerCase()===v)||M.ships.find(x=>x.n.toLowerCase().includes(v)&&v.length>2)||null;};
  const btns=[{id:'ok',label:edit?T('Speichern','Save'):T('Hinzufügen','Add'),cls:'pri'},{id:'cx',label:T('Abbrechen','Cancel')}];
  if(edit) btns.push({id:'del',label:T('Schiff entfernen','Remove ship'),cls:'danger'});
  dialog(edit?T('Schiff bearbeiten','Edit ship'):T('Schiff hinzufügen','Add ship'),body,btns,()=>{const t=type(); const out=[];
    if(($l('st').value||'').trim()&&!t) out.push(T('Schiffstyp nicht gefunden: bitte aus der Liste wählen (nur Schiffe mit Laderaum).','Ship type not found: please pick from the list (ships with cargo space only).'));
    else if(t) out.push(T(`Laderaum ${nf(t.scu)} SCU, Container bis ${t.cs||'?'} SCU.`,`Cargo ${nf(t.scu)} SCU, containers up to ${t.cs||'?'} SCU.`));
    if(edit&&s){const u=used('s:'+s.id); if(u) out.push(T(`Entfernen bucht ${nf(u)} SCU an Bord mit aus.`,`Removing also books out ${nf(u)} SCU on board.`));}
    return out;});
  dlgAct=b=>{if(b==='cx'){closeDlg();return;} const t=type();
    if(b==='del'){snap(); const loc='s:'+s.id; S.stock=S.stock.filter(q=>q.l!==loc); S.ships=S.ships.filter(x=>x!==s); S.sel=null; closeDlg(); commit(T(`Schiff entfernt: ${s.n}`,`Ship removed: ${s.n}`)); return;}
    if(!t){$l('st').focus();return;}
    const name=($l('sn').value||'').trim()||t.n, ov=$l('so').checked, op=Math.max(1,Math.min(100,Math.round(+$l('sp').value||33)));
    snap(); if(edit){Object.assign(s,{t:t.id,n:name,ov,op}); closeDlg(); commit(T(`Schiff geändert: ${name}`,`Ship changed: ${name}`)); return;}
    const id=Date.now().toString(36); S.ships.push({id,t:t.id,n:name,ov,op}); S.sel='s:'+id; closeDlg(); commit(T(`Schiff hinzugefügt: ${name} (${t.n})`,`Ship added: ${name} (${t.n})`));};}
let dlgAct=null;

/* ---------- export / import ---------- */
function download(name,blob){const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=name; document.body.appendChild(a); a.click(); setTimeout(()=>{URL.revokeObjectURL(a.href); a.remove();},500);}
const stamp=()=>new Date().toISOString().slice(0,10);
function exportJson(){download(`SC_Fracht_Logbuch_${stamp()}.json`,new Blob([JSON.stringify({app:'sc-fracht-logbuch',v:1,exported:new Date().toISOString(),ships:S.ships,stock:S.stock,log:S.log},null,1)],{type:'application/json'})); toast(T('JSON gespeichert.','JSON saved.'));}
function importJson(file){const r=new FileReader(); r.onload=()=>{try{const o=JSON.parse(r.result);
    if(o.app!=='sc-fracht-logbuch'||o.v!==1||!Array.isArray(o.ships)||!Array.isArray(o.stock)) throw new Error('format');
    if(!confirm(T(`Logbuch aus „${file.name}“ einlesen? Es ersetzt den Stand in diesem Browser (${S.ships.length} Schiffe, ${S.stock.length} Posten). Rückgängig ist möglich.`,`Import the ledger from “${file.name}”? It replaces the state in this browser (${S.ships.length} ships, ${S.stock.length} posts). Undo is possible.`))) return;
    snap(); S.ships=o.ships; S.stock=o.stock.filter(p=>p&&p.l&&p.n>0); S.log=Array.isArray(o.log)?o.log:[]; S.sel=null;
    commit(T(`Eingelesen: ${file.name} (${S.ships.length} Schiffe, ${S.stock.length} Posten)`,`Imported: ${file.name} (${S.ships.length} ships, ${S.stock.length} posts)`));}
  catch(e){toast(T('Datei nicht lesbar: keine Logbuch-JSON dieses Tools.','File not readable: not a ledger JSON of this tool.'));}}; r.readAsText(file);}
// Minimal XLSX writer: OOXML parts in an uncompressed ZIP (no external library, works offline).
const CRC=(()=>{const t=new Uint32Array(256); for(let n=0;n<256;n++){let c=n; for(let k=0;k<8;k++) c=c&1?0xEDB88320^(c>>>1):c>>>1; t[n]=c>>>0;} return t;})();
function crc32(b){let c=0xFFFFFFFF; for(let i=0;i<b.length;i++) c=CRC[(c^b[i])&255]^(c>>>8); return (c^0xFFFFFFFF)>>>0;}
function zip(files){const enc=new TextEncoder(), parts=[], cen=[]; let off=0;
  for(const f of files){const name=enc.encode(f.name), data=enc.encode(f.data), crc=crc32(data);
    const h=new DataView(new ArrayBuffer(30)); h.setUint32(0,0x04034b50,true); h.setUint16(4,20,true); h.setUint16(6,0x0800,true); h.setUint16(8,0,true);
    h.setUint16(10,0,true); h.setUint16(12,0x5A21,true); h.setUint32(14,crc,true); h.setUint32(18,data.length,true); h.setUint32(22,data.length,true); h.setUint16(26,name.length,true);
    parts.push(new Uint8Array(h.buffer),name,data);
    const c=new DataView(new ArrayBuffer(46)); c.setUint32(0,0x02014b50,true); c.setUint16(4,20,true); c.setUint16(6,20,true); c.setUint16(8,0x0800,true); c.setUint16(10,0,true);
    c.setUint16(12,0,true); c.setUint16(14,0x5A21,true); c.setUint32(16,crc,true); c.setUint32(20,data.length,true); c.setUint32(24,data.length,true); c.setUint16(28,name.length,true); c.setUint32(42,off,true);
    cen.push(new Uint8Array(c.buffer),name); off+=30+name.length+data.length;}
  const csize=cen.reduce((a,b)=>a+b.length,0), e=new DataView(new ArrayBuffer(22));
  e.setUint32(0,0x06054b50,true); e.setUint16(8,files.length,true); e.setUint16(10,files.length,true); e.setUint32(12,csize,true); e.setUint32(16,off,true);
  return new Blob([...parts,...cen,new Uint8Array(e.buffer)],{type:'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});}
function xmlEsc(s){return String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g,'');}
function sheetXml(rows){return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'+
  rows.map((r,i)=>`<row r="${i+1}">`+r.map(v=>typeof v==='number'?`<c t="n"${i===0?' s="1"':''}><v>${v}</v></c>`:`<c t="inlineStr"${i===0?' s="1"':''}><is><t xml:space="preserve">${xmlEsc(v)}</t></is></c>`).join('')+'</row>').join('')+'</sheetData></worksheet>';}
function xlsx(sheets){const ns='http://schemas.openxmlformats.org/', files=[
  {name:'[Content_Types].xml',data:`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="${ns}package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>${sheets.map((s,i)=>`<Override PartName="/xl/worksheets/sheet${i+1}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>`).join('')}</Types>`},
  {name:'_rels/.rels',data:`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="${ns}package/2006/relationships"><Relationship Id="rId1" Type="${ns}officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>`},
  {name:'xl/workbook.xml',data:`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="${ns}spreadsheetml/2006/main" xmlns:r="${ns}officeDocument/2006/relationships"><sheets>${sheets.map((s,i)=>`<sheet name="${xmlEsc(s.name)}" sheetId="${i+1}" r:id="rId${i+1}"/>`).join('')}</sheets></workbook>`},
  {name:'xl/_rels/workbook.xml.rels',data:`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="${ns}package/2006/relationships">${sheets.map((s,i)=>`<Relationship Id="rId${i+1}" Type="${ns}officeDocument/2006/relationships/worksheet" Target="worksheets/sheet${i+1}.xml"/>`).join('')}<Relationship Id="rId${sheets.length+1}" Type="${ns}officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>`},
  {name:'xl/styles.xml',data:`<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="${ns}spreadsheetml/2006/main"><fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><name val="Calibri"/></font></fonts><fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills><borders count="1"><border/></borders><cellStyleXfs count="1"><xf/></cellStyleXfs><cellXfs count="2"><xf xfId="0"/><xf fontId="1" applyFont="1" xfId="0"/></cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>`},
  ...sheets.map((s,i)=>({name:`xl/worksheets/sheet${i+1}.xml`,data:sheetXml(s.rows)}))];
  return zip(files);}
// The three sheets: stock, ships, journal.
function ledgerSheets(){const locInfo=l=>{if(l[0]==='s'){const s=shipById(l.slice(2)); return [T('Schiff','Ship'),s?.n||'?','',''];} const p=PL[l.slice(2)]; return [T('Ort','Place'),p?.n||l.slice(2),p?.sys||'',p?.body||''];};
  const stock=[[T('Art','Kind'),T('Ort/Schiff','Place/ship'),'System',T('Planet/Mond','Planet/moon'),T('Ware','Commodity'),T('Containergröße (SCU)','Container size (SCU)'),T('Anzahl','Count'),'SCU']]
    .concat(S.stock.map(p=>[...locInfo(p.l),WA[p.w]?.n||'?',p.z,p.n,p.z*p.n]));
  const ships=[[T('Name','Name'),T('Typ','Type'),T('Laderaum (SCU)','Cargo (SCU)'),T('Überladen bis (SCU)','Overload up to (SCU)'),T('belegt (SCU)','used (SCU)')]]
    .concat(S.ships.map(s=>{const c=cap(s); return [s.n,SH[s.t]?.n||'?',c.base,c.max,used('s:'+s.id)];}));
  const journal=[[T('Zeit','Time'),T('Buchung','Entry')]].concat(S.log.map(e=>[new Date(e.t).toLocaleString(L()==='en'?'en-GB':'de-DE'),e.x]));
  return [{name:T('Bestand','Stock'),rows:stock},{name:T('Schiffe','Ships'),rows:ships},{name:'Journal',rows:journal}];}
function exportXlsx(){download(`SC_Fracht_Logbuch_${stamp()}.xlsx`,xlsx(ledgerSheets())); toast(T('XLSX gespeichert.','XLSX saved.'));}

/* ---------- events ---------- */
const view=document.getElementById('view-ledger');
view.addEventListener('click',e=>{const a=e.target.closest('[data-act]'); if(a){({in:openIn,addship:()=>openShip(false),editship:()=>openShip(true)})[a.dataset.act](); return;}
  const c=e.target.closest('.lb-chip'); if(c){openMove(+c.dataset.i); return;}
  const l=e.target.closest('[data-loc]'); if(l) select(l.dataset.loc);});
$l('addship').addEventListener('click',()=>openShip(false));
$l('undo').addEventListener('click',undo);
$l('json').addEventListener('click',exportJson);
$l('xlsx').addEventListener('click',exportXlsx);
$l('imp').addEventListener('click',()=>$l('file').click());
$l('file').addEventListener('change',e=>{const f=e.target.files[0]; if(f) importJson(f); e.target.value='';});
for(const id of ['q','sys','only']) $l(id).addEventListener(id==='q'?'input':'change',renderPlaces);
$l('dbtn').addEventListener('click',e=>{const b=e.target.closest('[data-b]'); if(b&&dlgAct) dlgAct(b.dataset.b);});
$l('form').addEventListener('submit',e=>{e.preventDefault(); if(dlgAct) dlgAct(dlgOk?.[0]?.id);});
// Drag a post chip onto a ship or place; the drop opens the move dialog with that target.
view.addEventListener('dragstart',e=>{const c=e.target.closest('.lb-chip'); if(!c) return; e.dataTransfer.setData('text/plain',c.dataset.i); e.dataTransfer.effectAllowed='move';});
view.addEventListener('dragover',e=>{const t=e.target.closest('.lb-ship,.lb-place'); if(!t) return; e.preventDefault(); view.querySelectorAll('.drop').forEach(x=>x!==t&&x.classList.remove('drop')); t.classList.add('drop');});
view.addEventListener('dragleave',e=>{const t=e.target.closest('.lb-ship,.lb-place'); if(t&&!t.contains(e.relatedTarget)) t.classList.remove('drop');});
view.addEventListener('drop',e=>{const t=e.target.closest('.lb-ship,.lb-place'); view.querySelectorAll('.drop').forEach(x=>x.classList.remove('drop')); if(!t) return; e.preventDefault();
  const i=+e.dataTransfer.getData('text/plain'); if(!Number.isNaN(i)) openMove(i,t.dataset.loc);});
document.addEventListener('keydown',e=>{if(view.classList.contains('hide')||$l('dlg').open) return;
  if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='z'&&!/INPUT|SELECT|TEXTAREA/.test(document.activeElement?.tagName||'')){e.preventDefault(); undo();}});

load();
return {render, _state:()=>S, _sheets:ledgerSheets, _xlsx:xlsx};
})();
"""
