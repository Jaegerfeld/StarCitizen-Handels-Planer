# =============================================================================
# Autor:          Robert Seebauer
# Repository:     https://github.com/Jaegerfeld/StarCitizen-Handels-Planer
# KI-Unterstützung: Erstellt mit Unterstützung von Claude (Anthropic)
# Erstellt:       20.11.2026
# Geändert:       20.11.2026
# Lizenz:         BSD-3-Clause (siehe LICENSE)
#
# Fachliche Funktion:
#   Reiter „Ruf“: schätzt den Ruf je Organisation als Balken zum nächsten Rang.
#   Das Spiel schreibt keine Ruf-Punkte ins Log; der Reiter rechnet daher
#     Stand = Abgleich aus dem mobiGlas + Σ angegebene XP × Faktor
#   über alle danach abgeschlossenen Missionen. Missionen, Ergebnis,
#   Organisation und „geteilt“ kommen aus den Logs, die der Reiter „Sitzungen“
#   einliest (gleicher Ordner); angegebene XP und Rangschwellen aus der
#   Ruf-Tabelle (ruf_daten.py). Der Faktor wird je Organisation aus zwei
#   Abgleichen gelernt (gemessener Zuwachs ÷ angegebene XP); bis dahin gilt
#   0,55 (Messung an Foxwell, 19./20.11.2026). Geteilte Missionen zählen als
#   Spanne (halber bis voller Betrag), Missionen ohne Wert und Fehlschläge mit 0,
#   werden aber angezeigt. Abgleiche und Favoriten liegen im Browser
#   (localStorage); nichts verlässt den Rechner.
#   Konzept: Konzept_Ruf-Tracker.md, Entscheidungen R1–R8 vom 20.11.2026.
#   Eigenständiges Modul für das spätere Spieler-Cockpit.
# =============================================================================
"""HTML, CSS and JS fragments of the "Ruf" (reputation) tab, inserted by the page builder."""

#: Tab button, placed after the sessions tab.
RF_TAB = ('    <button class="tab" role="tab" data-view="rep" aria-selected="false">'
          '<span class="de">Ruf</span><span class="en">Reputation</span></button>\n')

#: Panel markup.
RF_HTML = r"""
  <!-- Reputation per organisation, estimated from the game logs -->
  <section class="panel hide" id="view-rep">
    <div class="rf-bar">
      <button type="button" class="btn" id="rf-load">📁 <span class="de">Log-Ordner laden …</span><span class="en">Load log folder …</span></button>
      <span class="rf-stat" id="rf-stat" role="status"></span>
    </div>
    <p class="rf-note"><span class="de">Das Spiel schreibt keine Ruf-Punkte ins Log. Der Reiter rechnet: <b>Stand aus deinem mobiGlas</b> + Ruf der danach abgeschlossenen Missionen (laut Missionsbeschreibung × Faktor). Gleiche einmal je Organisation ab, dann läuft der Balken mit. Gleicher Log-Ordner wie unter „Sitzungen“.</span><span class="en">The game writes no reputation points to the log. This tab computes: <b>the state from your mobiGlas</b> + reputation of the missions completed afterwards (as stated in the mission description × factor). Align once per organisation, then the bar keeps up. Same log folder as under “Sessions”.</span></p>
    <div id="rf-list"></div>
    <p class="rf-note" id="rf-src"></p>
  </section>
"""

#: Styles, scoped to the reputation panel.
RF_CSS = r"""
  #view-rep [hidden]{display:none!important}
  #view-rep .rf-bar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:0 0 6px}
  #view-rep .rf-bar .btn{min-height:44px}
  #view-rep .btn.pri{background:var(--accent);border-color:var(--accent);color:var(--bg)}
  #view-rep .rf-stat{color:var(--muted);font-size:13px}
  #view-rep .rf-note{color:var(--muted);font-size:12.5px;margin:0 0 14px;max-width:80ch}
  #view-rep .rf-org{border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:0 0 12px;background:var(--panel)}
  #view-rep .rf-org.fav{border-color:var(--accent)}
  #view-rep .rf-head{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
  #view-rep .rf-head h3{font-family:var(--disp);font-size:17px;letter-spacing:.04em;margin:0;flex:1 1 auto}
  #view-rep .rf-rank{font-family:var(--disp);font-weight:700;font-size:14px;color:var(--accent)}
  #view-rep .rf-star{font:inherit;font-size:18px;min-width:44px;min-height:44px;border:1px solid var(--line);border-radius:10px;background:var(--panel2);color:var(--muted);cursor:pointer}
  #view-rep .rf-star[aria-pressed="true"]{color:var(--accent);border-color:var(--accent)}
  #view-rep .rf-track{position:relative;height:14px;border-radius:7px;background:var(--panel2);border:1px solid var(--line);overflow:hidden;margin:10px 0 4px}
  #view-rep .rf-fill{position:absolute;left:0;top:0;bottom:0;background:var(--accent)}
  #view-rep .rf-unc{position:absolute;top:0;bottom:0;background:repeating-linear-gradient(135deg,var(--accent) 0 4px,transparent 4px 8px);opacity:.55}
  #view-rep .rf-nums{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font-size:13px}
  #view-rep .rf-nums b{font-family:var(--disp);font-size:15px}
  #view-rep .rf-meta{color:var(--muted);font-size:12.5px;margin:6px 0 0}
  #view-rep .rf-meta .est{color:var(--warn,#c0841a)}
  #view-rep .rf-acts{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
  #view-rep .rf-acts .btn{min-height:44px}
  #view-rep .rf-form{border-top:1px dashed var(--line);margin-top:12px;padding-top:12px;display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px 14px;align-items:end}
  #view-rep .rf-form label{display:flex;flex-direction:column;gap:4px;font-size:13px}
  #view-rep .rf-form select,#view-rep .rf-form input{min-height:44px;font:inherit;padding:0 10px;border-radius:8px;border:1px solid var(--line);background:var(--panel2);color:var(--ink)}
  #view-rep .rf-form .rf-help{grid-column:1/-1;color:var(--muted);font-size:12.5px;margin:0}
  #view-rep .rf-form .rf-err{grid-column:1/-1;color:var(--bad);font-size:13px;margin:0}
  #view-rep .rf-form .rf-btns{display:flex;gap:8px;flex-wrap:wrap}
  #view-rep details summary{cursor:pointer;color:var(--accent);min-height:32px;margin-top:6px}
  #view-rep .rf-tag{display:inline-block;font-size:11.5px;border:1px solid var(--line);border-radius:6px;padding:0 6px;margin-left:4px}
  #view-rep .rf-tag.fail{color:var(--bad);border-color:var(--bad)}
  #view-rep .rf-empty{color:var(--muted);padding:12px 2px}
"""

#: Behaviour. Runs after the sessions script (uses SZ.sessions, SZ.pick, SZ.start).
RF_JS = r"""
/* ---------- Reputation per organisation ---------- */
const RF=(function(){
const TAB=/*__RUF__*/null;
const L=()=>(document.documentElement.getAttribute('lang')||'de').slice(0,2);
const T=(de,en)=>L()==='en'?en:de;
const $r=id=>document.getElementById('rf-'+id);
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const SKEY='scha_rep_v1', F0=0.55, MINLEARN=200;
const fmt=n=>Math.round(n).toLocaleString(L()==='en'?'en-GB':'de-DE');
const fmtT=s=>s?new Date(s).toLocaleString(L()==='en'?'en-GB':'de-DE',{dateStyle:'short',timeStyle:'short'}):'–';
// Title as in the table: markup of the translation removed, spaces collapsed (same rule as ruf_daten.norm_title).
const normT=s=>String(s||'').replace(/<[^>]+>|\[BP\]\*?|\*/g,' ').replace(/\s+/g,' ').trim();
const compact=s=>String(s||'').toLowerCase().replace(/[^a-z0-9]/g,'');
let OPEN=null;   // organisation whose alignment form is open

/* ---------- stored state ---------- */
function load(){try{return JSON.parse(localStorage.getItem(SKEY)||'{}');}catch(e){return {};}}
function save(s){try{localStorage.setItem(SKEY,JSON.stringify(s));}catch(e){}}
function orgState(st,o){st.orgs=st.orgs||{}; return st.orgs[o]||(st.orgs[o]={cals:[],fav:false});}

/* ---------- table lookups ---------- */
// Table entry for one mission: the first notification text (or its part after "Prefix: ") that is a known title.
function lookup(texts){if(!TAB) return null;
  for(const x of texts){const parts=[x]; let i=x.indexOf(': '); while(i>=0){parts.push(x.slice(i+2)); i=x.indexOf(': ',i+2);}
    for(const p of parts){const e=TAB.missions[normT(p)]; if(e) return {title:normT(p),e};}}
  return null;}
// Display name of an organisation id from the log ("FoxwellEnforcement", "BountyHunterGuild").
function orgName(id){if(!TAB||!id) return id||''; const c=compact(id);
  for(const o of Object.keys(TAB.ladders)){const k=compact(o); if(k===c||k.startsWith(c.slice(0,10))||c.startsWith(k.slice(0,10))) return o;}
  return id.replace(/([a-z])([A-Z])/g,'$1 $2');}
// Title of a mission without a table entry: the text of the accept notification without its prefix.
function plainTitle(texts){const x=texts[0]||''; const i=x.indexOf(': '); return i>0?x.slice(i+2):x;}

/* ---------- missions from the sessions ---------- */
// All ended missions over the loaded sessions, oldest first: time, title, organisation, result, stated XP, shared.
function missions(){const S=(typeof SZ!=='undefined'&&SZ.sessions)?SZ.sessions():[]; const ids={}, ends=[], shares=[];
  for(const s of S){if(!s.mis) continue;
    for(const [id,o] of Object.entries(s.mis.ids)){const a=ids[id]||(ids[id]={t:o.t,x:[],org:''}); if(o.t&&(!a.t||o.t<a.t)) a.t=o.t;
      for(const x of o.x) if(!a.x.includes(x)) a.x.push(x); if(!a.org&&o.org) a.org=o.org;}
    ends.push(...s.mis.ends); shares.push(...s.mis.shares);}
  const seen=new Set(), out=[];
  for(const e of ends.sort((a,b)=>a.t.localeCompare(b.t))){if(seen.has(e.id)) continue; seen.add(e.id);
    const m=ids[e.id]||{t:'',x:[],org:''}, hit=lookup(m.x), title=hit?hit.title:normT(plainTitle(m.x));
    const tab=hit?hit.e:null, org=tab?tab[0][0]:orgName(m.org);
    if(!org) continue;
    const lo=tab?Math.min(...tab.map(x=>x[1])):null, hi=tab?Math.max(...tab.map(x=>x[2])):null;
    // "Shared" notification with the same title between accepting and ending (it carries no MissionId)
    const shared=shares.some(sh=>(!m.t||sh.t>=m.t)&&sh.t<=e.t&&normT(sh.x)===title);
    out.push({t:e.t,id:e.id,title,org,res:e.r,lo,hi,shared});}
  return out;}

/* ---------- estimate ---------- */
const ladder=o=>(TAB&&TAB.ladders[o])||[];
// Rank band for an XP value: [reached rank, next rank or null].
function band(o,x){const l=ladder(o); let i=0; while(i+1<l.length&&x>=l[i+1][0]) i++; return [l[i]||[0,'–'],l[i+1]||null];}
// Stated XP of a completed mission as [low, high] after the factor; shared missions count half to full.
function gain(m,f){if(m.res!=='Complete'||m.lo==null) return [0,0]; return [m.shared?m.lo*f/2:m.lo*f, m.hi*f];}
// Factor of an organisation: learned from the last two alignments when enough stated XP lies between them.
function factor(o,list,cals){if(cals.length>=2){const a=cals[cals.length-2], b=cals[cals.length-1];
    const between=list.filter(m=>m.org===o&&m.t>a.t&&m.t<=b.t&&m.res==='Complete'&&m.lo!=null&&!m.shared);
    const stated=between.reduce((s,m)=>s+(m.lo+m.hi)/2,0);
    if(stated>=MINLEARN&&b.xp>a.xp) return {f:Math.min(3,Math.max(0.05,(b.xp-a.xp)/stated)),learned:true,stated};}
  return {f:F0,learned:false};}
function estimate(o,list,st){const os=orgState(st,o), cal=os.cals[os.cals.length-1]||null, fac=factor(o,list,os.cals);
  const mine=list.filter(m=>m.org===o), after=cal?mine.filter(m=>m.t>cal.t):mine;
  let lo=0, hi=0, stated=0; for(const m of after){const g=gain(m,fac.f); lo+=g[0]; hi+=g[1]; if(m.res==='Complete'&&m.lo!=null) stated+=(m.lo+m.hi)/2;}
  return {cal,fac,mine,after,lo:cal?cal.xp+lo:null,hi:cal?cal.xp+hi:null,stated,
    unknown:after.filter(m=>m.res==='Complete'&&m.lo==null).length, failed:after.filter(m=>m.res==='Fail'||m.res==='Abandon').length,
    shared:after.filter(m=>m.res==='Complete'&&m.shared).length};}

/* ---------- rendering ---------- */
function bar(o,est){const mid=(est.lo+est.hi)/2, [cur,next]=band(o,mid);
  if(!next) return {cur,next,html:`<div class="rf-track"><div class="rf-fill" style="width:100%"></div></div>`};
  const span=next[0]-cur[0], p=x=>Math.max(0,Math.min(100,(x-cur[0])/span*100));
  return {cur,next,html:`<div class="rf-track" role="img" aria-label="${T('Fortschritt','Progress')} ${Math.round(p(mid))} %"><div class="rf-fill" style="width:${p(est.lo)}%"></div><div class="rf-unc" style="left:${p(est.lo)}%;width:${Math.max(0,p(est.hi)-p(est.lo))}%"></div></div>`};}
function card(o,list,st){const est=estimate(o,list,st), os=orgState(st,o);
  const star=`<button type="button" class="rf-star" data-fav="${esc(o)}" aria-pressed="${os.fav}" aria-label="${T('Favorit','Favourite')}" title="${T('Oben anheften','Pin to top')}">${os.fav?'★':'☆'}</button>`;
  let body;
  if(!est.cal){body=`<p class="rf-meta">${T(`${est.mine.filter(m=>m.res==='Complete').length} abgeschlossene Missionen in den geladenen Logs. Noch kein Abgleich – trag einmal ein, was dein mobiGlas zeigt.`,`${est.mine.filter(m=>m.res==='Complete').length} completed missions in the loaded logs. Not aligned yet – enter once what your mobiGlas shows.`)}</p>`;}
  else{const b=bar(o,est), mid=(est.lo+est.hi)/2, range=est.hi-est.lo>=1?` <small>(${fmt(est.lo)}–${fmt(est.hi)})</small>`:'';
    const up=b.cur[1]!==band(o,est.cal.xp)[0][1]?` <span class="rf-tag">${T('rechnerisch aufgestiegen','computed rank-up')}</span>`:'';
    body=`<div class="rf-head"><span class="rf-rank">${esc(b.cur[1])}${up}</span></div>${b.html}
      <div class="rf-nums"><span><b>≈ ${fmt(mid)} XP</b>${range}</span><span>${b.next?T(`noch ≈ ${fmt(Math.max(0,b.next[0]-mid))} bis ${esc(b.next[1])} (${fmt(b.next[0])})`,`≈ ${fmt(Math.max(0,b.next[0]-mid))} to ${esc(b.next[1])} (${fmt(b.next[0])})`):T('höchster Rang','top rank')}</span></div>
      <p class="rf-meta">${T('Abgleich','Aligned')} ${fmtT(est.cal.t)} (${fmt(est.cal.xp)} XP) · ${T(`seit dann ${est.after.filter(m=>m.res==='Complete').length} Missionen, +${fmt(est.stated)} XP laut Beschreibung`,`since then ${est.after.filter(m=>m.res==='Complete').length} missions, +${fmt(est.stated)} XP as stated`)}
        · ${T('Faktor','factor')} ${est.fac.f.toFixed(2).replace('.',L()==='en'?'.':',')} ${est.fac.learned?T('(gelernt)','(learned)'):`<span class="est">${T('(geschätzt – zweiter Abgleich macht ihn genau)','(estimated – a second alignment makes it exact)')}</span>`}
        ${est.unknown?` · <span class="est">+? ${T(`aus ${est.unknown} Missionen ohne Wert`,`from ${est.unknown} missions without a value`)}</span>`:''}
        ${est.shared?` · ${T(`${est.shared} geteilt (halb bis voll gezählt)`,`${est.shared} shared (counted half to full)`)}`:''}
        ${est.failed?` · ${T(`${est.failed} fehlgeschlagen/abgebrochen (0 gezählt)`,`${est.failed} failed/abandoned (counted 0)`)}`:''}</p>`;}
  const rows=est.after.slice().reverse().map(m=>`<tr><td>${fmtT(m.t)}</td><td>${esc(m.title)}${m.shared?`<span class="rf-tag">${T('geteilt','shared')}</span>`:''}</td><td>${m.res==='Complete'?'✓':`<span class="rf-tag fail">${esc(m.res==='Fail'?T('fehlgeschlagen','failed'):m.res==='Abandon'?T('abgebrochen','abandoned'):m.res)}</span>`}</td><td class="num">${m.lo==null?'?':m.lo===m.hi?fmt(m.lo):fmt(m.lo)+'–'+fmt(m.hi)}</td></tr>`).join('');
  const det=est.after.length?`<details><summary>${T(est.cal?'Missionen seit dem Abgleich':'Missionen in den geladenen Logs',est.cal?'Missions since the alignment':'Missions in the loaded logs')} (${est.after.length})</summary><div class="tablewrap"><table><thead><tr><th>${T('Ende','End')}</th><th>${T('Mission','Mission')}</th><th>${T('Ergebnis','Result')}</th><th class="num">${T('XP laut Beschreibung','XP as stated')}</th></tr></thead><tbody>${rows}</tbody></table></div></details>`:'';
  const acts=`<div class="rf-acts"><button type="button" class="btn${est.cal?'':' pri'}" data-align="${esc(o)}">⇄ ${T('Stand aus dem mobiGlas abgleichen …','Align with the mobiGlas …')}</button>${os.cals.length?`<button type="button" class="btn" data-undo="${esc(o)}">↶ ${T('Letzten Abgleich entfernen','Remove last alignment')}</button>`:''}</div>`;
  return `<article class="rf-org${os.fav?' fav':''}" data-org="${esc(o)}"><div class="rf-head"><h3>${esc(o)}</h3>${star}</div>${body}${acts}${OPEN===o?form(o,est):''}${det}</article>`;}
// Alignment form: reached rank, fill of the next rank's bar, time of the look into the mobiGlas.
function form(o,est){const l=ladder(o), cur=est.cal?band(o,(est.lo+est.hi)/2)[0][1]:(l[0]||[0,''])[1];
  const now=new Date(Date.now()-new Date().getTimezoneOffset()*60000).toISOString().slice(0,16);
  return `<form class="rf-form" data-form="${esc(o)}" novalidate>
    <p class="rf-help">${T('mobiGlas → Ruf → Organisation: Die <b>hervorgehobene Kachel</b> ist der nächste Rang. Der höchste volle Rang ist „erreicht“; schätze, wie weit der Balken der hervorgehobenen Kachel gefüllt ist.','mobiGlas → Reputation → organisation: the <b>highlighted tile</b> is the next rank. The highest full rank is “reached”; estimate how far the bar of the highlighted tile is filled.')}</p>
    <label>${T('Erreichter Rang','Rank reached')}<select name="rank">${l.map(([x,n])=>`<option value="${x}"${n===cur?' selected':''}>${esc(n)} (${fmt(x)})</option>`).join('')}</select></label>
    <label>${T('Balken der nächsten Stufe in %','Bar of the next rank in %')}<input name="pct" type="number" inputmode="decimal" min="0" max="100" step="0.5" value="0"></label>
    <label>${T('Zeitpunkt des Blicks','Time of the look')}<input name="t" type="datetime-local" value="${now}"></label>
    <div class="rf-btns"><button type="submit" class="btn pri">✓ ${T('Übernehmen','Apply')}</button><button type="button" class="btn" data-cancel>${T('Abbrechen','Cancel')}</button></div>
    <p class="rf-err" role="alert"></p></form>`;}
function render(){const list=$r('list'), S=(typeof SZ!=='undefined'&&SZ.sessions)?SZ.sessions():[];
  $r('src').textContent=TAB?T(`Ruf-Tabelle: ${Object.keys(TAB.missions).length} Missionstitel, Stand ${TAB.stand}. Quelle: ${TAB.quelle}.`,`Reputation table: ${Object.keys(TAB.missions).length} mission titles, as of ${TAB.stand}. Source: annotations of the German community translation (numbers, titles, rank names only).`):T('Ruf-Tabelle fehlt in diesem Bau.','Reputation table missing in this build.');
  $r('load').classList.toggle('pri',!S.length);
  $r('stat').textContent=S.length?(SZ.status?SZ.status():''):'';
  if(!S.length){list.innerHTML=`<p class="rf-empty">${T('Lade den Log-Ordner von Star Citizen (LIVE oder PTU), dann erscheinen hier deine Organisationen.','Load the Star Citizen log folder (LIVE or PTU), then your organisations appear here.')}</p>`; return;}
  const ms=missions(), st=load(), orgs=[...new Set([...ms.map(m=>m.org),...Object.keys(st.orgs||{})])];
  const last=o=>ms.filter(m=>m.org===o).map(m=>m.t).sort().pop()||'';
  orgs.sort((a,b)=>(orgState(st,b).fav-orgState(st,a).fav)||last(b).localeCompare(last(a)));
  list.innerHTML=orgs.length?orgs.map(o=>card(o,ms,st)).join(''):`<p class="rf-empty">${T('In den geladenen Logs ist keine abgeschlossene Mission.','No completed mission in the loaded logs.')}</p>`;
  if(OPEN){const f=document.querySelector(`#view-rep [data-form="${CSS.escape(OPEN)}"] select`); if(f) f.focus();}}

/* ---------- events ---------- */
$r('load').addEventListener('click',()=>{if(typeof SZ!=='undefined') SZ.pick();});
document.addEventListener('sz:loaded',()=>{if(!document.getElementById('view-rep').classList.contains('hide')) render();});
const view=document.getElementById('view-rep');
view.addEventListener('click',e=>{const st=load(); let b;
  if((b=e.target.closest('[data-fav]'))){const os=orgState(st,b.dataset.fav); os.fav=!os.fav; save(st); render(); return;}
  if((b=e.target.closest('[data-align]'))){OPEN=OPEN===b.dataset.align?null:b.dataset.align; render(); return;}
  if((b=e.target.closest('[data-undo]'))){const os=orgState(st,b.dataset.undo); const c=os.cals.pop(); save(st); render();
    $r('stat').textContent=c?T(`Abgleich vom ${fmtT(c.t)} entfernt.`,`Alignment of ${fmtT(c.t)} removed.`):''; return;}
  if(e.target.closest('[data-cancel]')){OPEN=null; render();}});
view.addEventListener('submit',e=>{const f=e.target.closest('[data-form]'); if(!f) return; e.preventDefault();
  const o=f.dataset.form, l=ladder(o), x0=+f.rank.value, i=l.findIndex(r=>r[0]===x0), next=l[i+1];
  const pct=parseFloat(String(f.pct.value).replace(',','.')), err=f.querySelector('.rf-err');
  if(!(pct>=0&&pct<=100)){err.textContent=T('Bitte einen Wert von 0 bis 100 eintragen.','Please enter a value from 0 to 100.'); f.pct.focus(); return;}
  const t=f.t.value?new Date(f.t.value).toISOString():new Date().toISOString();
  const xp=x0+(next?(next[0]-x0)*pct/100:0), st=load(), os=orgState(st,o);
  os.cals.push({t,xp:Math.round(xp)}); os.cals.sort((a,b)=>a.t.localeCompare(b.t)); save(st); OPEN=null; render();
  $r('stat').textContent=T(`${o}: Abgleich gespeichert (${fmt(xp)} XP).`,`${o}: alignment saved (${fmt(xp)} XP).`);});

let started=false;
return {render(){if(!started){started=true; if(typeof SZ!=='undefined') SZ.start();} render();}, _missions:missions, _estimate:(o)=>estimate(o,missions(),load()), _band:band};
})();
"""
