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
#   Abgleich von Hand (Rang + Balken in %) oder per Screenshot der mobiGlas-
#   Seite „Ruf“ (Schritt 2): Die Seite zählt die vollen Balken (= erreichte
#   Ränge), findet die hervorgehobene Kachel (grüner Rahmen = nächster Rang)
#   und misst deren Balken als grüne Lauflänge mit Teilpixeln an den Enden;
#   den Zeitpunkt nimmt sie aus dem Dateinamen (ScreenShot-JJJJ-MM-TT_hh-mm-ss).
#   Geprüft an sechs Screenshots (2000×837): ±2 Prozentpunkte zur Handmessung.
#   Das Bild wird nur im Browser gelesen.
#   Übersicht „Missionen nach Rufstufe“ je Organisation: Missionen der Ruf-Tabelle
#   nach ihrer Mindeststufe, freigeschaltet / als Nächstes / später nach dem
#   geschätzten Stand. Missionstexte optional (Schalter, aus = Standard): Sie
#   kommen zur Laufzeit aus der global.ini im geladenen Spielordner und werden
#   in einem Fenster gezeigt; die Seite selbst enthält keine Missionstexte.
#   Gilden (ab Alpha 5.0, Aufteilung laut Roberts Liste vom 20.11.2026, PTU):
#   Die Organisationen werden nach Gilden gruppiert; wer nicht in der Liste steht,
#   kommt unter „Keiner Gilde zugeordnet“. Alle bekannten Organisationen sind von
#   Anfang an sichtbar, auch ohne Logs; ohne Abgleich lassen sie sich ausblenden.
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
      <label class="rf-toggle"><input type="checkbox" id="rf-hide"> <span class="de">Ohne Abgleich ausblenden</span><span class="en">Hide not aligned</span></label>
      <label class="rf-toggle"><input type="checkbox" id="rf-texts"> <span class="de">Missionstexte anzeigen</span><span class="en">Show mission texts</span></label>
      <span class="rf-stat" id="rf-stat" role="status"></span>
    </div>
    <p class="rf-note" id="rf-texts-note" hidden></p>
    <p class="rf-note"><span class="de">Das Spiel schreibt keine Ruf-Punkte ins Log. Der Reiter rechnet: <b>Stand aus deinem mobiGlas</b> + Ruf der danach abgeschlossenen Missionen (laut Missionsbeschreibung × Faktor). Gleiche einmal je Organisation ab, dann läuft der Balken mit. Gleicher Log-Ordner wie unter „Sitzungen“.</span><span class="en">The game writes no reputation points to the log. This tab computes: <b>the state from your mobiGlas</b> + reputation of the missions completed afterwards (as stated in the mission description × factor). Align once per organisation, then the bar keeps up. Same log folder as under “Sessions”.</span></p>
    <div id="rf-list"></div>
    <p class="rf-note" id="rf-src"></p>
    <dialog id="rf-dlg" aria-labelledby="rf-dlg-h"><h3 id="rf-dlg-h"></h3><div id="rf-dlg-t"></div>
      <form method="dialog"><button class="btn" value="x">✕ <span class="de">Schließen</span><span class="en">Close</span></button></form></dialog>
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
  #view-rep .rf-shot{grid-column:1/-1;display:flex;gap:12px;flex-wrap:wrap;align-items:center;border:2px dashed var(--line);border-radius:10px;padding:10px}
  #view-rep .rf-shot.drag{border-color:var(--accent);background:var(--panel2)}
  #view-rep .rf-shot .btn{min-height:44px}
  #view-rep .rf-shot canvas{max-width:min(420px,100%);height:auto;border-radius:6px;border:1px solid var(--line)}
  #view-rep .rf-shot .rf-res{flex:1 1 240px;font-size:13px;margin:0}
  #view-rep .rf-shot .rf-res.bad{color:var(--bad)}
  #view-rep details summary{cursor:pointer;color:var(--accent);min-height:32px;margin-top:6px}
  #view-rep .rf-tag{display:inline-block;font-size:11.5px;border:1px solid var(--line);border-radius:6px;padding:0 6px;margin-left:4px}
  #view-rep .rf-tag.fail{color:var(--bad);border-color:var(--bad)}
  #view-rep .rf-empty{color:var(--muted);padding:12px 2px}
  #view-rep .rf-toggle{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 10px;border:1px solid var(--line);border-radius:10px;cursor:pointer;font-size:14px}
  #view-rep .rf-toggle input{width:20px;height:20px}
  #view-rep .rf-guild{margin:0 0 18px}
  #view-rep .rf-guild>h2{font-family:var(--disp);font-size:15px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin:14px 0 4px;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
  #view-rep .rf-guild>h2 small{font-size:12px;letter-spacing:0;text-transform:none;color:var(--muted)}
  #view-rep .rf-guild>p{color:var(--muted);font-size:12.5px;margin:0 0 8px}
  #view-rep .rf-toggle.off{opacity:.55;cursor:not-allowed}
  #view-rep .rf-lvl{margin:10px 0 0;border-left:4px solid var(--line);padding:2px 0 2px 10px}
  #view-rep .rf-lvl h4{margin:0 0 4px;font-family:var(--disp);font-size:14px;display:flex;gap:8px;flex-wrap:wrap;align-items:baseline}
  #view-rep .rf-lvl.done{border-left-color:var(--ok)}
  #view-rep .rf-lvl.next{border-left-color:var(--accent);background:var(--panel2);border-radius:0 8px 8px 0}
  #view-rep .rf-lvl.later{opacity:.7}
  #view-rep .rf-lvl ul{list-style:none;margin:0;padding:0;columns:2 340px;column-gap:24px}
  #view-rep .rf-lvl li{break-inside:avoid;display:flex;justify-content:space-between;gap:10px;font-size:13px;padding:3px 0;border-bottom:1px solid var(--line)}
  #view-rep .rf-lvl li small{color:var(--muted);white-space:nowrap}
  #view-rep .rf-mt{font:inherit;font-size:13px;color:var(--accent);background:none;border:0;padding:0;min-height:28px;text-align:left;cursor:pointer;text-decoration:underline}
  #view-rep dialog{max-width:min(720px,92vw);max-height:84vh;border:1px solid var(--line);border-radius:12px;background:var(--panel);color:var(--ink);padding:16px 18px}
  #view-rep dialog::backdrop{background:rgba(0,0,0,.55)}
  #view-rep dialog h3{font-family:var(--disp);margin:0 0 10px}
  #view-rep #rf-dlg-t{white-space:pre-wrap;font-size:14px;line-height:1.5;max-height:62vh;overflow:auto}
  #view-rep dialog form{margin-top:12px;text-align:right}
  #view-rep dialog .btn{min-height:44px}
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
  // Titles with placeholders ("Orange Level Contract: ~mission(Ship) Needs Assistance"): the log has the filled-in name
  for(const x of texts){const parts=[x]; let i=x.indexOf(': '); while(i>=0){parts.push(x.slice(i+2)); i=x.indexOf(': ',i+2);}
    for(const p of parts){const n=normT(p), hit=pats().find(q=>q.re.test(n)); if(hit) return {title:hit.title,e:TAB.missions[hit.title]};}}
  return null;}
let PATS=null;
// Regular expressions for the table titles that contain ~mission(…) placeholders.
function pats(){if(PATS) return PATS; PATS=[];
  for(const tt of Object.keys(TAB.missions)) if(tt.includes('~mission(')){
    const src=tt.split(/~mission\([^)]*\)/).map(s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('.+?');
    PATS.push({re:new RegExp('^'+src+'$'),title:tt});}
  return PATS;}
// Title for display: placeholders as [Name].
const prettyT=s=>String(s).replace(/~mission\(([^)|]*)(?:\|[^)]*)?\)/g,'[$1]');
// Guilds from Alpha 5.0 (PTU list, 20.11.2026): name, focus, and the words that identify their mission givers.
const GUILDS=[
  {n:'Transport Guild', d:['Fracht und Kurier','Cargo and courier'], k:['covalex','ftl','ling']},
  {n:'Resources Guild', d:['Rohstoffe und Bergung','Resources and salvage'], k:['shubin','adagio','cornerstone']},
  {n:'Mercenary Guild', d:['Sicherheit, Kampf, Söldner','Security, combat, mercenary'], k:['northrock']},
  {n:'Bounty Hunter Guild', d:['Kopfgeldjagd','Bounty hunting'], k:['bounty']},
  {n:'Academy of Science', d:['Forschung, Sammeln, Erkundung','Research, collecting, exploration'], k:['rayari']},
  {n:'Lokale / persönliche Boards', d:['Terminals außerhalb der Gildenhallen','Terminals outside the guild halls'], k:['wikelo','hockrow']}];
// Mission givers named in the guild list that the reputation table does not know (shown from the start).
const EXTRA=['Covalex Independent Haulers','Cornerstone Developments','Northrock Service Group','Bounty Hunters Guild','Rayari Inc.','Wikelo','Hockrow Agency'];
// Generic giver ids of the log that are no organisation.
const NOORG=new Set(['missiongiver','civilian']);
const known=()=>[...Object.keys(TAB?TAB.ladders:{}),...EXTRA];
const guildOf=o=>{const c=compact(o); return GUILDS.find(g=>g.k.some(k=>c.includes(k)))||null;};
// Display name of an organisation id from the log ("FoxwellEnforcement", "NorthRock" → Northrock Service Group).
function orgName(id){if(!id||NOORG.has(compact(id))) return ''; const c=compact(id);
  for(const o of known()){const k=compact(o); if(k===c||k.startsWith(c.slice(0,10))||c.startsWith(k.slice(0,10))) return o;}
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
// Rank ladder of an organisation; without own data the contractor ladder is assumed (flagged by ladderGuess).
const CONTRACTOR=()=>Object.values(TAB?TAB.ladders:{}).find(l=>l.some(r=>r[1]==='Auftragnehmer Elite'))||[];
const ladderGuess=o=>!(TAB&&TAB.ladders[o]&&TAB.ladders[o].length>1);
const ladder=o=>ladderGuess(o)?CONTRACTOR():TAB.ladders[o];
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

/* ---------- screenshot of the mobiGlas ---------- */
// Measures the reputation tiles of a mobiGlas screenshot: number of full bars (= ranks reached), the highlighted
// tile (green frame = next rank) and the fill of its bar. Sizes scale with the image height (tested at 837 px).
function measureShot(cv){const W=cv.width, H=cv.height, d=cv.getContext('2d',{willReadFrequently:true}).getImageData(0,0,W,H).data, s=H/837;
  const P=(x,y)=>{const i=(y*W+x)*4; return [d[i],d[i+1],d[i+2]];};
  const bright=(x,y)=>{const [r,g]=P(x,y); return g>150&&g-r>60;};
  const frame=(x,y)=>{const [r,g]=P(x,y); return g>120&&g-r>35;};
  const runs=test=>{const out=[]; for(let y=Math.floor(H*.2);y<Math.floor(H*.85);y++){let x=0; while(x<W){if(test(x,y)){const a=x; while(x<W&&test(x,y)) x++; out.push([y,a,x-a]);} x++;}} return out;};
  // Bars: runs of 60..115 px, at least two rows thick (the 1-px tile frame is not)
  let bars=[]; for(const [y,a,n] of runs(bright)){if(n<60*s||n>115*s) continue;
    const b=bars.find(b=>Math.abs(b.a-a)<=30*s&&y-b.yl>0&&y-b.yl<=1);
    if(b){b.rows++; b.yl=y; if(n>b.n){b.y=y; b.a=a; b.n=n;}} else bars.push({y,yl:y,a,n,rows:1});}
  bars=bars.filter(b=>b.rows>=2);
  if(!bars.length) return {err:T('Keine Ruf-Balken gefunden. Ist es die mobiGlas-Seite „Ruf“ mit den Rang-Kacheln einer Organisation?','No reputation bars found. Is it the mobiGlas “Reputation” page with the rank tiles of an organisation?')};
  const L=Math.max(...bars.map(b=>b.n)), full=bars.filter(b=>b.n>=L-3*s).sort((a,b)=>(a.y-b.y>12*s?1:b.y-a.y>12*s?-1:a.a-b.a));
  const y1=Math.min(...full.map(b=>b.y)), cols=full.filter(b=>b.y-y1<12*s).map(b=>b.a).sort((a,b)=>a-b);
  const dx=cols.length>1?cols[1]-cols[0]:184*s;
  const edge=(x,y)=>x<0||x>=W?0:Math.min(1,Math.max(0,(P(x,y)[1]-100)/150));
  // Green run length from the bar start, with the partly green boundary pixels as fractions
  const runAt=(x0,y)=>{let a=-1; for(let x=Math.floor(x0-4*s);x<x0+6*s;x++) if(x>=0&&x<W&&bright(x,y)){a=x; break;}
    if(a<0) return edge(Math.round(x0),y)>.5?edge(Math.round(x0),y):0; let b=a; while(b+1<W&&bright(b+1,y)) b++; return b-a+1+edge(a-1,y)+edge(b+1,y);};
  const cover=(x0,y)=>Math.max(runAt(x0,y-1),runAt(x0,y),runAt(x0,y+1));
  const Lc=Math.max(...full.map(b=>cover(b.a,b.y)));
  const fr=runs(frame).find(([,,n])=>n>=130*s&&n<=190*s);
  let x0,yb,idx,guess=false;
  if(fr){const [by,bx]=fr, col=Math.round((bx+30*s-cols[0])/dx); x0=cols[0]+col*dx;
    const yp=Math.round(by+102*s), gr=yy=>{let t=0; for(let x=Math.round(x0);x<x0+L;x++) if(x<W){const p=P(x,yy); t+=p[1]-p[0];} return t;};
    yb=yp; let best=-1e9; for(let yy=yp-Math.round(8*s);yy<=yp+Math.round(8*s);yy++){const v=gr(yy); if(v>best){best=v; yb=yy;}}
    idx=(yb-y1>40*s?4:0)+col;}
  else{idx=full.length; guess=true; x0=cols[0]+(idx%4)*dx; yb=y1+Math.floor(idx/4)*Math.round(190*s);}
  const pct=Math.max(0,Math.min(100,cover(x0,yb)/Lc*100));
  return {n:full.length, idx, pct:Math.round(pct*10)/10, guess, box:[x0,yb,L], full};}
// Time of the screenshot from its file name ("ScreenShot-2026-11-20_11-59-18-B56.jpg"), else the file date.
function shotTime(f){const m=/(\d{4})-(\d\d)-(\d\d)_(\d\d)-(\d\d)-(\d\d)/.exec(f.name||''); return m?new Date(+m[1],m[2]-1,+m[3],+m[4],+m[5],+m[6]):new Date(f.lastModified||Date.now());}
const localISO=d=>new Date(d.getTime()-d.getTimezoneOffset()*60000).toISOString().slice(0,16);
// Read a screenshot file into the open form: measure, show a preview with the measured bar marked, fill the fields.
async function readShot(f,form){const res=form.querySelector('.rf-res'), o=form.dataset.form, l=ladder(o);
  res.className='rf-res'; res.textContent=T('Lese Screenshot …','Reading screenshot …');
  try{// Image element instead of createImageBitmap: works in more browsers (and in headless tests)
    const url=URL.createObjectURL(f), bm=new Image(); bm.src=url; await new Promise((ok,no)=>{bm.onload=ok; bm.onerror=no;}); URL.revokeObjectURL(url);
    const cv=document.createElement('canvas'); cv.width=bm.naturalWidth; cv.height=bm.naturalHeight; cv.getContext('2d').drawImage(bm,0,0);
    const m=measureShot(cv);
    if(m.err){res.className='rf-res bad'; res.textContent=m.err; return;}
    const reached=l[m.n-1], next=l[m.n];
    if(!reached){res.className='rf-res bad'; res.textContent=T(`${m.n} volle Balken erkannt, aber die Rangleiter von ${o} hat nur ${l.length} Stufen. Ist es der Screenshot dieser Organisation?`,`${m.n} full bars found, but the rank ladder of ${o} has only ${l.length} steps. Is it the screenshot of this organisation?`); return;}
    form.rank.value=String(reached[0]); form.pct.type='text'; form.pct.value=next?String(m.pct).replace('.',L()==='en'?'.':','):'0'; form.t.value=localISO(shotTime(f));
    // Preview: the tile area, the measured bar framed
    const [bx,by,bl]=m.box, x0=Math.max(0,m.full[0].a-60*cv.height/837), y0=Math.max(0,Math.min(...m.full.map(b=>b.y))-140*cv.height/837), w=Math.min(cv.width-x0,800*cv.height/837), h=Math.min(cv.height-y0,420*cv.height/837);
    const pv=form.querySelector('canvas'); pv.width=420; pv.height=Math.round(420*h/w); const c=pv.getContext('2d'); c.drawImage(cv,x0,y0,w,h,0,0,pv.width,pv.height);
    const k=pv.width/w; c.strokeStyle='#ff5a5a'; c.lineWidth=2; c.strokeRect((bx-x0-4)*k,(by-y0-8)*k,(bl+8)*k,16*k); pv.hidden=false;
    const warn=m.guess?T(' Hervorgehobene Kachel nicht gefunden – nächste Stufe nach der Reihenfolge angenommen.',' Highlighted tile not found – next rank assumed by order.'):m.idx!==m.n?T(` Achtung: hervorgehoben ist Kachel ${m.idx+1}, voll sind ${m.n} – bitte prüfen.`,` Note: tile ${m.idx+1} is highlighted, ${m.n} are full – please check.`):'';
    res.className='rf-res'+(warn?' bad':''); res.textContent=T(`Erkannt: ${m.n} Ränge erreicht (bis ${reached[1]})${next?`, Balken ${next[1]} zu ${String(m.pct).replace('.',',')} % gefüllt`:''} · Zeitpunkt ${fmtT(shotTime(f).toISOString())}. Rot markiert ist der gemessene Balken – bitte kurz prüfen und übernehmen.`,`Found: ${m.n} ranks reached (up to ${reached[1]})${next?`, bar ${next[1]} ${m.pct} % filled`:''} · time ${fmtT(shotTime(f).toISOString())}. The measured bar is framed in red – please check and apply.`)+warn;}
  catch(e){res.className='rf-res bad'; res.textContent=T('Bild konnte nicht gelesen werden.','Could not read the image.');}}

/* ---------- missions by rank ---------- */
const TKEY='scha_rep_texts';
let INIMAP=null, INIFILE=null;
const textsOn=()=>{try{return localStorage.getItem(TKEY)==='1';}catch(e){return false;}};
const iniFile=()=>(typeof SZ!=='undefined'&&SZ.ini)?SZ.ini():null;
// Missions of one organisation from the table, grouped by minimum rank (XP threshold); null = no rank given.
function byRank(o){const m=new Map();
  for(const [title,es] of Object.entries(TAB?TAB.missions:{})){const e=es.filter(x=>x[0]===o); if(!e.length) continue;
    const min=e.find(x=>x[3]!=null)?.[3]??null, k=min==null?'x':String(min);
    if(!m.has(k)) m.set(k,{min,list:[]});
    m.get(k).list.push({title,lo:Math.min(...e.map(x=>x[1])),hi:Math.max(...e.map(x=>x[2])),key:e[0][4]});}
  return [...m.values()].sort((a,b)=>(a.min==null)-(b.min==null)||(a.min||0)-(b.min||0));}
function overview(o,est){const groups=byRank(o); if(!groups.length) return '';
  const n=groups.reduce((s,g)=>s+g.list.length,0), mid=est.cal?(est.lo+est.hi)/2:null, l=ladder(o), canText=textsOn()&&!!iniFile();
  const nextMin=mid==null?null:(groups.find(g=>g.min!=null&&g.min>mid)||{}).min;
  const html=groups.map(g=>{const rank=g.min==null?T('Stufe nicht angegeben','Rank not given'):((l.find(r=>r[0]===g.min)||[0,`${fmt(g.min)} XP`])[1]+` (${fmt(g.min)})`);
    const cls=g.min==null||mid==null?'':g.min<=mid?' done':g.min===nextMin?' next':' later';
    const tag=g.min==null||mid==null?'':g.min<=mid?`<span class="rf-tag">✓ ${T('freigeschaltet','unlocked')}</span>`:g.min===nextMin?`<span class="rf-tag">→ ${T(`als Nächstes, noch ≈ ${fmt(g.min-mid)} XP`,`next, ≈ ${fmt(g.min-mid)} XP to go`)}</span>`:`<span class="rf-tag">🔒 ${T('später','later')}</span>`;
    const items=g.list.sort((a,b)=>a.title.localeCompare(b.title)).map(x=>`<li>${canText?`<button type="button" class="rf-mt" data-mt="${esc(x.key)}" data-mtt="${esc(prettyT(x.title))}">${esc(prettyT(x.title))}</button>`:esc(prettyT(x.title))}<small>${x.lo===x.hi?fmt(x.lo):fmt(x.lo)+'–'+fmt(x.hi)} XP</small></li>`).join('');
    return `<div class="rf-lvl${cls}"><h4>${esc(rank)} <small>· ${g.list.length}</small>${tag}</h4><ul>${items}</ul></div>`;}).join('');
  const hint=mid==null?`<p class="rf-meta">${T('Nach dem ersten Abgleich siehst du hier, was freigeschaltet ist und was als Nächstes kommt.','After the first alignment you see here what is unlocked and what comes next.')}</p>`:'';
  return `<details data-ov="${esc(o)}"${OVOPEN.has(o)?' open':''}><summary>${T('Missionen nach Rufstufe','Missions by rank')} (${n})</summary>${hint}${html}</details>`;}
const OVOPEN=new Set();
// Read the needed descriptions from the player's global.ini once (only keys of the table).
async function loadTexts(){const f=iniFile(); if(!f) return null; if(INIMAP&&INIFILE===f) return INIMAP;
  const need=new Set(Object.values(TAB.missions).flat().map(e=>e[4])), map={}, txt=await f.text();
  for(const line of txt.split(/\r?\n/)){const i=line.indexOf('='); if(i<0) continue; const k=line.slice(0,i).split(',')[0].toLowerCase(); if(need.has(k)) map[k]=line.slice(i+1);}
  INIMAP=map; INIFILE=f; return map;}
// Ini value as plain text: "\n" to line breaks, markup removed, placeholders shortened.
const iniText=v=>String(v||'').replace(/\\n/g,'\n').replace(/<\/?EM\d>/g,'').replace(/~mission\(([^)|]*)(?:\|[^)]*)?\)/g,'[$1]');
async function showText(key,title){const dlg=$r('dlg'); $r('dlg-h').textContent=title; $r('dlg-t').textContent=T('Lese Sprachdatei …','Reading language file …');
  if(!dlg.open) dlg.showModal();
  try{const map=await loadTexts(); $r('dlg-t').textContent=map&&map[key]?iniText(map[key]):T('Für diese Mission steht kein Text in der Sprachdatei.','No text for this mission in the language file.');}
  catch(e){$r('dlg-t').textContent=T('Die Sprachdatei konnte nicht gelesen werden – bitte den Log-Ordner neu laden.','The language file could not be read – please load the log folder again.');}}
function textsBar(){const box=$r('texts'), lab=box.closest('label'), has=!!iniFile(), note=$r('texts-note');
  box.checked=textsOn(); box.disabled=!has; lab.classList.toggle('off',!has);
  note.hidden=has||!textsOn();
  note.textContent=has?'':T('Missionstexte brauchen die Sprachdatei des Spiels (StarCitizen\\LIVE\\data\\Localization\\…\\global.ini) im geladenen Ordner – die gibt es nur mit installierter Übersetzung. Lade dafür den ganzen Ordner LIVE.','Mission texts need the game’s language file (StarCitizen\\LIVE\\data\\Localization\\…\\global.ini) in the loaded folder – it exists only with a translation installed. Load the whole LIVE folder for it.');}

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
  const rows=est.after.slice().reverse().map(m=>`<tr><td>${fmtT(m.t)}</td><td>${esc(prettyT(m.title))}${m.shared?`<span class="rf-tag">${T('geteilt','shared')}</span>`:''}</td><td>${m.res==='Complete'?'✓':`<span class="rf-tag fail">${esc(m.res==='Fail'?T('fehlgeschlagen','failed'):m.res==='Abandon'?T('abgebrochen','abandoned'):m.res)}</span>`}</td><td class="num">${m.lo==null?'?':m.lo===m.hi?fmt(m.lo):fmt(m.lo)+'–'+fmt(m.hi)}</td></tr>`).join('');
  const det=est.after.length?`<details><summary>${T(est.cal?'Missionen seit dem Abgleich':'Missionen in den geladenen Logs',est.cal?'Missions since the alignment':'Missions in the loaded logs')} (${est.after.length})</summary><div class="tablewrap"><table><thead><tr><th>${T('Ende','End')}</th><th>${T('Mission','Mission')}</th><th>${T('Ergebnis','Result')}</th><th class="num">${T('XP laut Beschreibung','XP as stated')}</th></tr></thead><tbody>${rows}</tbody></table></div></details>`:'';
  const acts=`<div class="rf-acts"><button type="button" class="btn${est.cal?'':' pri'}" data-align="${esc(o)}">⇄ ${T('Stand aus dem mobiGlas abgleichen …','Align with the mobiGlas …')}</button>${os.cals.length?`<button type="button" class="btn" data-undo="${esc(o)}">↶ ${T('Letzten Abgleich entfernen','Remove last alignment')}</button>`:''}</div>`;
  const guess=ladderGuess(o)?`<p class="rf-meta"><span class="est">${T('Rangleiter nicht bekannt – Auftragnehmer-Stufen angenommen.','Rank ladder unknown – contractor ranks assumed.')}</span></p>`:'';
  return `<article class="rf-org${os.fav?' fav':''}" data-org="${esc(o)}"><div class="rf-head"><h3>${esc(o)}</h3>${star}</div>${body}${guess}${acts}${OPEN===o?form(o,est):''}${det}${overview(o,est)}</article>`;}
// Alignment form: reached rank, fill of the next rank's bar, time of the look into the mobiGlas.
function form(o,est){const l=ladder(o), cur=est.cal?band(o,(est.lo+est.hi)/2)[0][1]:(l[0]||[0,''])[1];
  const now=new Date(Date.now()-new Date().getTimezoneOffset()*60000).toISOString().slice(0,16);
  return `<form class="rf-form" data-form="${esc(o)}" novalidate>
    <p class="rf-help">${T('mobiGlas → Ruf → Organisation: Die <b>hervorgehobene Kachel</b> ist der nächste Rang. Der höchste volle Rang ist „erreicht“. Am genauesten: Screenshot auswerten lassen; sonst schätzen, wie weit der Balken der hervorgehobenen Kachel gefüllt ist.','mobiGlas → Reputation → organisation: the <b>highlighted tile</b> is the next rank. The highest full rank is “reached”. Most precise: let the page read a screenshot; otherwise estimate how far the bar of the highlighted tile is filled.')}</p>
    <div class="rf-shot" data-drop><button type="button" class="btn" data-shot>📷 ${T('Screenshot auswerten …','Read screenshot …')}</button><input type="file" accept="image/*" hidden data-shotin>
      <p class="rf-res" role="status">${T('Screenshot der Ruf-Seite dieser Organisation wählen oder hierher ziehen (Ordner <code>StarCitizen\\LIVE\\screenshots</code>). Die Felder werden ausgefüllt.','Choose or drop a screenshot of this organisation’s reputation page (folder <code>StarCitizen\\LIVE\\screenshots</code>). The fields get filled in.')}</p><canvas hidden></canvas></div>
    <label>${T('Erreichter Rang','Rank reached')}<select name="rank">${l.map(([x,n])=>`<option value="${x}"${n===cur?' selected':''}>${esc(n)} (${fmt(x)})</option>`).join('')}</select></label>
    <label>${T('Balken der nächsten Stufe in %','Bar of the next rank in %')}<input name="pct" type="number" inputmode="decimal" min="0" max="100" step="0.5" value="0"></label>
    <label>${T('Zeitpunkt des Blicks','Time of the look')}<input name="t" type="datetime-local" value="${now}"></label>
    <div class="rf-btns"><button type="submit" class="btn pri">✓ ${T('Übernehmen','Apply')}</button><button type="button" class="btn" data-cancel>${T('Abbrechen','Cancel')}</button></div>
    <p class="rf-err" role="alert"></p></form>`;}
function render(){const list=$r('list'), S=(typeof SZ!=='undefined'&&SZ.sessions)?SZ.sessions():[];
  $r('src').textContent=TAB?T(`Ruf-Tabelle: ${Object.keys(TAB.missions).length} Missionstitel, Stand ${TAB.stand}. Quelle: ${TAB.quelle}.`,`Reputation table: ${Object.keys(TAB.missions).length} mission titles, as of ${TAB.stand}. Source: annotations of the German community translation (numbers, titles, rank names only).`):T('Ruf-Tabelle fehlt in diesem Bau.','Reputation table missing in this build.');
  $r('load').classList.toggle('pri',!S.length); textsBar(); if(textsOn()&&iniFile()) loadTexts().catch(()=>{});
  $r('stat').textContent=S.length?(SZ.status?SZ.status():''):'';
  // All known organisations from the start (table, guild list, logs, own alignments), grouped by guild
  const ms=missions(), st=load(), hide=hideOn();
  const orgs=[...new Set([...known(),...ms.map(m=>m.org),...Object.keys(st.orgs||{})])].filter(Boolean);
  const last=o=>ms.filter(m=>m.org===o).map(m=>m.t).sort().pop()||'';
  const shown=orgs.filter(o=>!hide||orgState(st,o).cals.length||orgState(st,o).fav);
  $r('hide').checked=hide;
  const groups=[...GUILDS.map(g=>({g,list:shown.filter(o=>guildOf(o)===g)})),{g:null,list:shown.filter(o=>!guildOf(o))}].filter(x=>x.list.length);
  for(const x of groups) x.list.sort((a,b)=>(orgState(st,b).fav-orgState(st,a).fav)||(orgState(st,b).cals.length>0)-(orgState(st,a).cals.length>0)||last(b).localeCompare(last(a))||a.localeCompare(b));
  const hint=S.length?'':`<p class="rf-empty">${T('Lade den Log-Ordner von Star Citizen (LIVE oder PTU), dann zählt der Reiter deine Missionen mit. Abgleichen geht auch ohne Logs.','Load the Star Citizen log folder (LIVE or PTU), then the tab counts your missions. Aligning works without logs too.')}</p>`;
  const nHidden=orgs.length-shown.length;
  list.innerHTML=hint+(groups.length?groups.map(x=>`<section class="rf-guild"><h2>${esc(x.g?x.g.n:T('Keiner Gilde zugeordnet','No guild assigned'))} <small>${x.list.length}</small></h2>
      <p>${x.g?esc(T(x.g.d[0],x.g.d[1])):T('Im Testserver 5.0 noch keiner Gilde zugeordnet (geprüft 20.11.2026).','Not yet assigned to a guild on the 5.0 test server (checked 20 Nov 2026).')}</p>${x.list.map(o=>card(o,ms,st)).join('')}</section>`).join('')
    :`<p class="rf-empty">${T('Noch keine Organisation abgeglichen. Schalte „Ohne Abgleich ausblenden“ aus, um alle zu sehen.','No organisation aligned yet. Switch off “Hide not aligned” to see all.')}</p>`)
    +(hide&&nHidden?`<p class="rf-note">${T(`${nHidden} Organisationen ohne Abgleich ausgeblendet.`,`${nHidden} organisations without alignment hidden.`)}</p>`:'');
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
  if(e.target.closest('[data-cancel]')){OPEN=null; render(); return;}
  if((b=e.target.closest('[data-shot]'))){b.parentElement.querySelector('[data-shotin]').click(); return;}
  if((b=e.target.closest('[data-mt]'))){showText(b.dataset.mt,b.dataset.mtt);}});
// Remember which overviews are open across re-renders
view.addEventListener('toggle',e=>{const d=e.target.closest&&e.target.closest('[data-ov]'); if(d){if(d.open) OVOPEN.add(d.dataset.ov); else OVOPEN.delete(d.dataset.ov);}},true);
const HKEY='scha_rep_hide';
function hideOn(){try{return localStorage.getItem(HKEY)==='1';}catch(e){return false;}}
$r('hide').addEventListener('change',e=>{try{localStorage.setItem(HKEY,e.target.checked?'1':'0');}catch(x){} render();});
$r('texts').addEventListener('change',e=>{try{localStorage.setItem(TKEY,e.target.checked?'1':'0');}catch(x){} render();});
view.addEventListener('change',e=>{const i=e.target.closest('[data-shotin]'); if(i&&i.files[0]) readShot(i.files[0],i.closest('form'));});
view.addEventListener('dragover',e=>{const z=e.target.closest('[data-drop]'); if(z){e.preventDefault(); z.classList.add('drag');}});
view.addEventListener('dragleave',e=>{const z=e.target.closest('[data-drop]'); if(z) z.classList.remove('drag');});
view.addEventListener('drop',e=>{const z=e.target.closest('[data-drop]'); if(!z) return; e.preventDefault(); z.classList.remove('drag');
  const f=[...(e.dataTransfer?.files||[])].find(f=>f.type.startsWith('image/')); if(f) readShot(f,z.closest('form'));});
view.addEventListener('submit',e=>{const f=e.target.closest('[data-form]'); if(!f) return; e.preventDefault();
  const o=f.dataset.form, l=ladder(o), x0=+f.rank.value, i=l.findIndex(r=>r[0]===x0), next=l[i+1];
  const pct=parseFloat(String(f.pct.value).replace(',','.')), err=f.querySelector('.rf-err');
  if(!(pct>=0&&pct<=100)){err.textContent=T('Bitte einen Wert von 0 bis 100 eintragen.','Please enter a value from 0 to 100.'); f.pct.focus(); return;}
  const t=f.t.value?new Date(f.t.value).toISOString():new Date().toISOString();
  const xp=x0+(next?(next[0]-x0)*pct/100:0), st=load(), os=orgState(st,o);
  os.cals.push({t,xp:Math.round(xp)}); os.cals.sort((a,b)=>a.t.localeCompare(b.t)); save(st); OPEN=null; render();
  $r('stat').textContent=T(`${o}: Abgleich gespeichert (${fmt(xp)} XP).`,`${o}: alignment saved (${fmt(xp)} XP).`);});

let started=false;
return {render(){if(!started){started=true; if(typeof SZ!=='undefined') SZ.start();} render();}, _missions:missions, _estimate:(o)=>estimate(o,missions(),load()), _band:band, _measure:measureShot, _guildOf:o=>(guildOf(o)||{}).n||'', _orgName:orgName, _byRank:byRank, _iniText:iniText, _loadTexts:loadTexts};
})();
"""
