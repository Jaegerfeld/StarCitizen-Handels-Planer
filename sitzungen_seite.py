# =============================================================================
# Autor:          Robert Seebauer
# Repository:     https://github.com/Jaegerfeld/StarCitizen-Handels-Planer
# KI-Unterstützung: Erstellt mit Unterstützung von Claude (Anthropic)
# Erstellt:       19.11.2026
# Geändert:       20.11.2026
# Lizenz:         BSD-3-Clause (siehe LICENSE)
#
# Fachliche Funktion:
#   Reiter „Sitzungen“: liest die Spiel-Logs von Star Citizen (Game.log und
#   logbackups im Ordner LIVE bzw. PTU) direkt im Browser und zeigt je Sitzung
#   Beginn, Ende, ob sie abgestürzt ist, den letzten Server/Shard mit Region,
#   den letzten Ort und das letzte Schiff. Zweck: Nach einem Absturz sehen, wo
#   man zuletzt war, um liegen gelassene Fracht wiederzufinden. Der Ort wird,
#   wo möglich, einem Ort des Fracht-Logbuchs zugeordnet (Klick öffnet ihn).
#   Ordnerwahl über ein Ordner-Auswahlfeld (geht überall, auch unter
#   C:\Programme, das Chrome für die File System Access API sperrt); wer Star
#   Citizen anderswo installiert hat, kann den Ordner zusätzlich merken lassen
#   (Chrome/Edge). Nichts verlässt den Rechner;
#   die Logs enthalten Spielername und Server-IPs.
#   Log-Zeilen (Stand Alpha 4.10.3): <Join PU> address[…] port[…] shard[…];
#   <RequestLocationInventory> … Location[…]; <Local Route Guard …> | SCHIFF_ID[…];
#   Meldung „Rechtsgebiet von … betreten“ / „Entered … Jurisdiction“; Ende normal
#   CCIGBroker::FastShutdown, Absturz „crash handler“.
#   Für den Reiter „Ruf“ liest parse() zusätzlich die Missionen: Meldungen mit
#   MissionId (Titel), <EndMission> … CompletionType[…], die Organisation aus
#   SendCommsNotification … Missions.Organization.<Org> und „Auftrag geteilt“.
#   Nach jedem Einlesen meldet das Modul „sz:loaded“; der Reiter „Ruf“ hört darauf.
#   Liegt im Ordner eine Sprachdatei (data\Localization\<Sprache>\global.ini),
#   merkt sich das Modul nur den Verweis darauf; gelesen wird sie erst, wenn der
#   Reiter „Ruf“ einen Missionstext anzeigen soll.
# =============================================================================
"""HTML, CSS and JS fragments of the "Sitzungen" (sessions) tab, inserted by the page builder."""

#: Tab button, placed after the cargo ledger tab.
SZ_TAB = ('    <button class="tab" role="tab" data-view="sessions" aria-selected="false">'
          '<span class="de">Sitzungen</span><span class="en">Sessions</span></button>\n')

#: Panel markup.
SZ_HTML = r"""
  <!-- Sessions from the game logs -->
  <section class="panel hide" id="view-sessions">
    <div class="sz-bar">
      <button type="button" class="btn" id="sz-pick">📁 <span class="de">Log-Ordner laden …</span><span class="en">Load log folder …</span></button>
      <button type="button" class="btn" id="sz-reload" hidden>⟳ <span class="de">Neu einlesen</span><span class="en">Read again</span></button>
      <button type="button" class="btn" id="sz-remember" hidden>📌 <span class="de">Ordner merken …</span><span class="en">Remember folder …</span></button>
      <input type="file" id="sz-input" webkitdirectory multiple hidden>
      <span class="sz-stat" id="sz-stat" role="status"></span>
    </div>
    <div class="sz-hint" role="note"><span class="de"><b>Bei jedem Besuch neu laden:</b> Liegt Star Citizen unter <code>C:\Programme</code> (Standard), kann sich der Browser den Ordner nicht merken – Chrome sperrt dort den dauerhaften Zugriff. Wähle dann bei jedem Besuch einmal „Log-Ordner laden …“ und den Ordner <code>…\Roberts Space Industries\StarCitizen\LIVE</code> (oder <code>PTU</code>). Liegt Star Citizen woanders, verknüpft „Ordner merken …“ ihn dauerhaft.</span><span class="en"><b>Load again on every visit:</b> If Star Citizen is installed under <code>C:\Program Files</code> (the default), the browser cannot remember the folder – Chrome blocks lasting access there. Then choose “Load log folder …” once per visit and pick <code>…\Roberts Space Industries\StarCitizen\LIVE</code> (or <code>PTU</code>). If Star Citizen is elsewhere, “Remember folder …” links it for good.</span></div>
    <p class="sz-note"><span class="de">Chrome fragt beim Laden „Dateien hochladen?“: Die Dateien bleiben trotzdem auf deinem Rechner, die Seite liest nur <code>Game.log</code> und <code>logbackups</code> und sendet nichts. Die Logs enthalten deinen Spielernamen und Server-Adressen.</span><span class="en">Chrome asks “Upload files?” when loading: the files still stay on your computer, the page only reads <code>Game.log</code> and <code>logbackups</code> and sends nothing. The logs contain your player name and server addresses.</span></p>
    <div id="sz-last"></div>
    <div id="sz-list"></div>
  </section>
"""

#: Styles, scoped to the sessions panel.
SZ_CSS = r"""
  #view-sessions .sz-bar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:0 0 6px}
  #view-sessions .sz-bar .btn{min-height:44px}
  #view-sessions .sz-bar .btn.pri{background:var(--accent);border-color:var(--accent);color:var(--bg)}
  #view-sessions .sz-stat{color:var(--muted);font-size:13px}
  #view-sessions .sz-note{color:var(--muted);font-size:12.5px;margin:0 0 14px}
  #view-sessions [hidden]{display:none!important}
  #view-sessions .sz-hint{background:var(--panel2);border-left:4px solid var(--accent2);border-radius:0 8px 8px 0;padding:10px 12px;margin:4px 0 8px;font-size:14px}
  #view-sessions .sz-hint code{font-size:12.5px;background:var(--panel);border:1px solid var(--line);border-radius:5px;padding:0 4px}
  #view-sessions .sz-hint.loaded{display:none}
  #view-sessions .sz-note code{font-size:12px;background:var(--panel2);border:1px solid var(--line);border-radius:5px;padding:0 4px}
  #view-sessions .sz-last{border:2px solid var(--accent);border-radius:12px;padding:14px 16px;margin:0 0 18px;background:var(--panel2)}
  #view-sessions .sz-last.crash{border-color:var(--bad)}
  #view-sessions .sz-last h3{font-family:var(--disp);font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin:0 0 6px}
  #view-sessions .sz-shard{font-family:ui-monospace,Consolas,monospace;font-size:clamp(17px,2.4vw,22px);font-weight:700;word-break:break-all}
  #view-sessions .sz-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px 18px;margin-top:10px}
  #view-sessions .sz-grid div small{display:block;font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
  #view-sessions .sz-grid div b{font-family:var(--disp);font-size:16px}
  #view-sessions .sz-end{display:inline-block;font-family:var(--disp);font-weight:700;font-size:13px;border-radius:6px;padding:2px 8px;border:1px solid var(--line)}
  #view-sessions .sz-end.crash{color:var(--bad);border-color:var(--bad)}
  #view-sessions .sz-end.ok{color:var(--ok);border-color:var(--ok)}
  #view-sessions .sz-loc{font:inherit;font-family:var(--disp);font-weight:700;font-size:16px;color:var(--accent);background:none;border:0;padding:0;min-height:32px;cursor:pointer;text-decoration:underline;text-align:left}
  #view-sessions .sz-copy{font:inherit;font-size:12.5px;min-height:32px;margin-left:8px;padding:0 10px;border-radius:8px;border:1px solid var(--line);background:var(--panel);color:var(--ink);cursor:pointer;vertical-align:middle}
  #view-sessions table td{vertical-align:top}
  #view-sessions details summary{cursor:pointer;color:var(--accent);min-height:28px}
  #view-sessions details ol{margin:4px 0;padding-left:18px;font-size:12.5px}
  #view-sessions .sz-mono{font-family:ui-monospace,Consolas,monospace;font-size:12.5px;word-break:break-all}
  #view-sessions .sz-empty{color:var(--muted);padding:12px 2px}
"""

#: Behaviour. Runs after the cargo ledger script (uses LB.places and LB.openLoc).
SZ_JS = r"""
/* ---------- Sessions from the game logs ---------- */
const SZ=(function(){
const L=()=>(document.documentElement.getAttribute('lang')||'de').slice(0,2);
const T=(de,en)=>L()==='en'?en:de;
const $z=id=>document.getElementById('sz-'+id);
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
// Cache key v2: sessions also carry the missions for the reputation tab.
const MAXF=25, CKEY='scha_sessions_cache_v2';
const DIR_OK=typeof window.showDirectoryPicker==='function';
let DIR=null, PERM=false, SESS=[], BUSY=false, SRC='', INI=null;

/* ---------- parsing ---------- */
// One session per log file: start, end, how it ended, server joins, last place, ship, jurisdiction.
const RE={join:/^<([^>]+)> \[Notice\] <Join PU> address\[([^\]]*)\] port\[(\d+)\] shard\[([^\]]*)\]/gm,
  loc:/^<([^>]+)> .*?<RequestLocationInventory> Player\[[^\]]*\] requested inventory for Location\[([^\]]+)\]/gm,
  ship:/^<([^>]+)> .*?<Local Route Guard[^>]*>.*?\| ([A-Z]{3,5}_[A-Za-z0-9_]+?)_\d{9,}\[/gm,
  jur:/^<([^>]+)> .*?notification "(?:Rechtsgebiet von ([^:"]+?) betreten|Entered ([^:"]+?) Jurisdiction)/gm,
  ts:/^<(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z)>/gm,
  // Missions (reputation tab): notifications with a MissionId carry the title; <EndMission> the result.
  mnote:/^<([^>]+)> \[Notice\] <SHUDEvent_OnNotification> Added notification "([^"]*)" \[\d+\] to queue\. New queue size: \d+, MissionId: \[([0-9a-f-]{36})\]/gm,
  mend:/^<([^>]+)> \[Notice\] <EndMission> Ending mission for player\. MissionId\[([0-9a-f-]{36})\].*?CompletionType\[(\w+)\]/gm,
  morg:/SendCommsNotification \+?Missions\.Organization\.([A-Za-z]+)[^\n]*? - Mission: \[([0-9a-f-]{36})\]/g,
  mshare:/^<([^>]+)> \[Notice\] <SHUDEvent_OnNotification> Added notification "(?:Auftrag geteilt|Contract Shared|Mission Shared): ([^"]*)"/gm};
function all(re,text){re.lastIndex=0; const out=[]; let m; while((m=re.exec(text))) out.push(m); return out;}
function parse(text,name){
  const ts=all(RE.ts,text.slice(0,20000)), tail=all(RE.ts,text.slice(-60000));
  const crash=text.includes('crash handler taking over')||text.includes('All crash related data');
  const normal=text.includes('CCIGBroker::FastShutdown');
  const joins=all(RE.join,text).map(m=>({t:m[1],addr:m[2],port:m[3],shard:m[4]}));
  const locs=all(RE.loc,text).filter(m=>m[2]!=='INVALID_LOCATION_ID'), ships=all(RE.ship,text), jurs=all(RE.jur,text);
  const last=a=>a.length?a[a.length-1]:null, lo=last(locs), sh=last(ships), ju=last(jurs);
  return {name,start:ts[0]?.[1]||'',end:tail.length?tail[tail.length-1][1]:'',ended:crash?'crash':normal?'ok':'open',joins,
    loc:lo?{t:lo[1],raw:lo[2]}:null, ship:sh?{t:sh[1],raw:sh[2]}:null, jur:ju?{t:ju[1],n:ju[2]||ju[3]}:null, mis:missions(text)};}
// Missions of one log: per MissionId the first time, the distinct notification texts (one is the title) and the
// organisation; the ends with their result; "shared" notifications by title.
function missions(text){const ids={}, Z='00000000-0000-0000-0000-000000000000';
  for(const m of all(RE.mnote,text)){if(m[3]===Z) continue; const o=ids[m[3]]||(ids[m[3]]={t:m[1],x:[],org:''});
    const s=m[2].replace(/:\s*$/,''); if(o.x.length<6&&!o.x.includes(s)) o.x.push(s);}
  RE.morg.lastIndex=0; let g; while((g=RE.morg.exec(text))){const o=ids[g[2]]; if(o&&!o.org) o.org=g[1]; else if(!o) ids[g[2]]={t:'',x:[],org:g[1]};}
  return {ids, ends:all(RE.mend,text).map(m=>({t:m[1],id:m[2],r:m[3]})), shares:all(RE.mshare,text).map(m=>({t:m[1],x:m[2].replace(/:\s*$/,'')}))};}

/* ---------- names ---------- */
// Region from the shard name, e.g. pub_euw1b_13165946_260 -> euw1.
const REG={euw1:['EU-West','EU West'],euc1:['EU-Mitte','EU Central'],use1:['US-Ost','US East'],usw2:['US-West','US West'],usw1:['US-West','US West'],ape1:['Asien-Ost','Asia East'],apse2:['Asien-Pazifik Südost','Asia Pacific Southeast'],apne1:['Asien-Pazifik Nordost','Asia Pacific Northeast']};
function region(shard){const m=/^pub_([a-z]+\d)/.exec(shard||''); if(!m) return ''; const r=REG[m[1]]; return r?`${T(r[0],r[1])} (${m[1]})`:m[1];}
const MAKERS={AEGS:'Aegis',ANVL:'Anvil',ARGO:'Argo',BANU:'Banu',CNOU:'C.O.',CRUS:'Crusader',DRAK:'Drake',ESPR:'Esperia',GAMA:'Gatac',GLSN:'Gallant',GRIN:'Greycat',KRIG:'Kruger',MISC:'MISC',MRAI:'Mirai',ORIG:'Origin',RSI:'RSI',TMBL:'Tumbril',VNCL:'Vanduul',XIAN:'Aopoa'};
function shipName(raw){const p=raw.split('_'); const mk=MAKERS[p[0]]||p[0]; return mk+' '+p.slice(1).join(' ');}
// Split internal names into words: "HDMSEdmond" -> hdms edmond, "Area056" -> area 056.
const words=s=>String(s).replace(/([a-z])([A-Z])/g,'$1 $2').replace(/([A-Z]+)([A-Z][a-z])/g,'$1 $2').replace(/([A-Za-z])(\d)/g,'$1 $2').toLowerCase().split(/[^a-z0-9]+/).filter(Boolean);
const STOP=new Set(['stanton','nyx','pyro','outpost','station','the','and','von','mining','hydro','base','paf','rr','social']);
// Map an internal location name to a cargo-ledger place: internal station codes first, then shared words and numbers.
// Log names that differ from the place name. Castra and Magnus are the systems these gateways will lead to
// later; as long as Castra and Magnus are not in the game, the codes stand for the Stanton–Nyx gateways.
// Check this on every patch (Game.log: Location[RR_JP_…]).
const ALIAS={GrimHEX:'Green Imperial Housing Exchange',RR_JP_NyxCastra:'RR_JP_NyxStanton',RR_JP_StantonMagnus:'RR_JP_StantonNyx'};
function placeOf(raw){const P=(typeof LB!=='undefined'&&LB.places)||[]; if(!raw) return null;
  const al=ALIAS[raw]; if(al){const hit=P.find(p=>p.rr===al||p.n===al); if(hit) return hit;}
  const byRR=P.find(p=>p.rr===raw); if(byRR) return byRR;
  // Drop system/planet prefixes such as "Stanton1b" or "Nyx": their digits are no part of the place name.
  const core=String(raw).split('_').filter(x=>!/^(Stanton|Pyro|Nyx)\d*[a-z]?$/.test(x)).join('_');
  const norm=x=>/^\d+$/.test(x)?String(+x):x;
  const w=words(core).filter(x=>!STOP.has(x)).map(norm), nums=w.filter(x=>/^\d+$/.test(x)), txt=w.filter(x=>!/^\d+$/.test(x));
  let best=null, score=0;
  for(const p of P){const pw=new Set(words(p.n).map(norm));
    if(nums.some(n=>!pw.has(n))) continue;
    const s=txt.filter(x=>pw.has(x)).length;
    if(s>score){score=s; best=p;}}
  // At least one shared word (a number alone never counts); two if the internal name has many words.
  return score>=1&&(score>=2||txt.length<=2)?best:null;}
function prettyLoc(raw){return String(raw).replace(/^RR_/,'').replace(/_/g,' ').replace(/([a-z])([A-Z])/g,'$1 $2');}

/* ---------- reading the folder ---------- */
function cacheGet(){try{return JSON.parse(localStorage.getItem(CKEY)||'{}');}catch(e){return {};}}
function cacheSet(c){try{const keys=Object.keys(c); if(keys.length>80) for(const k of keys.slice(0,keys.length-80)) delete c[k]; localStorage.setItem(CKEY,JSON.stringify(c));}catch(e){}}
// The newest MAXF log files of a folder: Game.log plus logbackups/*.log.
async function filesFromDir(dir){const out=[];
  try{const g=await dir.getFileHandle('Game.log'); out.push(await g.getFile());}catch(e){}
  try{const b=await dir.getDirectoryHandle('logbackups'); for await (const [n,h] of b.entries()) if(h.kind==='file'&&n.endsWith('.log')) out.push(await h.getFile());}catch(e){}
  return out;}
// Language file of the game (data/Localization/<language>/global.ini) in the chosen folder; German first.
function iniFromInput(list){const c=[...list].filter(f=>/(^|\/)data\/Localization\/[^/]+\/global\.ini$/i.test(f.webkitRelativePath||''));
  return c.find(f=>/german/i.test(f.webkitRelativePath))||c[0]||null;}
async function iniFromDir(dir){try{const loc=await (await dir.getDirectoryHandle('data')).getDirectoryHandle('Localization'); let first=null;
    for await (const [n,h] of loc.entries()){if(h.kind!=='directory') continue; try{const f=await (await h.getFileHandle('global.ini')).getFile(); if(/german/i.test(n)) return f; first=first||f;}catch(e){}}
    return first;}catch(e){return null;}}
// Accept the LIVE/PTU folder (Game.log + logbackups/*.log) or the logbackups folder itself.
function filesFromInput(list){return [...list].filter(f=>{const p=(f.webkitRelativePath||f.name).split('/');
  return (p.length===2&&p[1]==='Game.log')||(p.length===2&&p[0]==='logbackups'&&p[1].endsWith('.log'))||(p.length===3&&p[1]==='logbackups'&&p[2].endsWith('.log'));});}
async function readFiles(files,label,once){if(BUSY) return; BUSY=true; SRC=label;
  const pick=files.sort((a,b)=>b.lastModified-a.lastModified).slice(0,MAXF);
  if(!pick.length){BUSY=false; stat(T('In diesem Ordner liegen keine Game.log und kein logbackups-Ordner. Bitte den Ordner LIVE (oder PTU) wählen.','No Game.log or logbackups folder here. Please choose the LIVE (or PTU) folder.')); render(); loaded(); return;}
  const cache=cacheGet(); SESS=[]; let i=0;
  for(const f of pick){i++; stat(T(`Lese ${i} von ${pick.length} Sitzungen …`,`Reading ${i} of ${pick.length} sessions …`));
    const key=f.name+'|'+f.size+'|'+f.lastModified; let s=cache[key];
    if(!s){s=parse(await f.text(),f.name); if(f.name!=='Game.log') cache[key]=s;}
    SESS.push(s); await new Promise(r=>setTimeout(r,0));}
  cacheSet(cache); SESS.sort((a,b)=>(b.start||'').localeCompare(a.start||'')); BUSY=false;
  stat(T(`${label} · ${SESS.length} Sitzungen gelesen · ${new Date().toLocaleTimeString('de-DE',{hour:'2-digit',minute:'2-digit'})}`,`${label} · ${SESS.length} sessions read · ${new Date().toLocaleTimeString('en-GB',{hour:'2-digit',minute:'2-digit'})}`)+(once?T(' · beim nächsten Besuch erneut laden (Ordner wird nicht gemerkt)',' · load again on your next visit (folder is not remembered)'):'')); render(); loaded();}
function stat(t){$z('stat').textContent=t;}
// Tell other tabs (reputation) that the sessions changed.
function loaded(){document.dispatchEvent(new CustomEvent('sz:loaded'));}

/* ---------- remembered folder (Chrome/Edge) ---------- */
function idb(){return new Promise((res,rej)=>{const r=indexedDB.open('scha_sessions',1); r.onupgradeneeded=()=>r.result.createObjectStore('h'); r.onsuccess=()=>res(r.result); r.onerror=()=>rej(r.error);});}
async function idbSet(v){try{const db=await idb(); await new Promise(res=>{const tx=db.transaction('h','readwrite'); tx.objectStore('h').put(v,'dir'); tx.oncomplete=res; tx.onerror=res;});}catch(e){}}
async function idbGet(){try{const db=await idb(); return await new Promise(res=>{const r=db.transaction('h').objectStore('h').get('dir'); r.onsuccess=()=>res(r.result||null); r.onerror=()=>res(null);});}catch(e){return null;}}
// Main way: the folder input works everywhere, also under C:\Program Files.
function pick(){$z('input').click();}
// Optional: remember the folder (Chrome/Edge). Chrome refuses folders under C:\Program Files.
async function remember(){
  try{const d=await window.showDirectoryPicker({id:'sc-logs',mode:'read'}); DIR=d; PERM=true; await idbSet(d); INI=await iniFromDir(d); await readFiles(await filesFromDir(d),d.name);}
  catch(e){stat(T('Nicht gemerkt. Liegt Star Citizen unter C:\\Programme, sperrt Chrome das Merken; nimm dann „Log-Ordner laden …“.','Not remembered. If Star Citizen is under C:\\Program Files, Chrome blocks remembering; use “Load log folder …” instead.'));}}
async function reload(){if(!DIR) return pick();
  try{if(!PERM) PERM=(await DIR.requestPermission({mode:'read'}))==='granted'; if(PERM){INI=await iniFromDir(DIR); await readFiles(await filesFromDir(DIR),DIR.name);}}
  catch(e){stat(T('Ordner nicht erreichbar.','Folder not reachable.'));}}
// Draw the empty state at once; the remembered folder (IndexedDB) may answer late or not at all.
async function init(){render(); const d=DIR_OK?await Promise.race([idbGet(),new Promise(r=>setTimeout(()=>r(null),1500))]):null; if(d){DIR=d; try{PERM=(await d.queryPermission({mode:'read'}))==='granted';}catch(e){PERM=false;}}
  if(DIR&&PERM){INI=await iniFromDir(DIR); await readFiles(await filesFromDir(DIR),DIR.name);} else render();}

/* ---------- rendering ---------- */
const fmtT=s=>s?new Date(s).toLocaleString(L()==='en'?'en-GB':'de-DE',{dateStyle:'short',timeStyle:'short'}):'–';
const tOnly=s=>s?new Date(s).toLocaleTimeString(L()==='en'?'en-GB':'de-DE',{hour:'2-digit',minute:'2-digit'}):'';
function dur(a,b){if(!a||!b) return '–'; const m=Math.max(0,Math.round((new Date(b)-new Date(a))/60000)); return m>=60?`${Math.floor(m/60)} h ${m%60} min`:`${m} min`;}
function endTag(s){return s.ended==='crash'?`<span class="sz-end crash">⚠ ${T('abgestürzt','crashed')} ${tOnly(s.end)}</span>`
  :s.ended==='ok'?`<span class="sz-end ok">✓ ${T('beendet','closed')} ${tOnly(s.end)}</span>`:`<span class="sz-end">… ${T('läuft oder ohne Abschluss','running or no proper end')}</span>`;}
function locHtml(l){if(!l) return '–'; const p=placeOf(l.raw);
  return p?`<button type="button" class="sz-loc" data-loc="p:${esc(p.id)}" title="${T('Im Fracht-Logbuch öffnen','Open in the cargo ledger')}">${esc(p.n)}</button>`:`<span title="${esc(l.raw)}">${esc(prettyLoc(l.raw))}</span>`;}
function render(){const last=$z('last'), list=$z('list'), has=!!SESS.length;
  $z('pick').classList.toggle('pri',!has&&!(DIR&&!PERM)); $z('reload').hidden=!DIR; $z('remember').hidden=!DIR_OK||!!DIR;
  $z('reload').innerHTML=DIR&&!PERM?`🔓 ${T('Zugriff erlauben und einlesen','Allow access and read')}`:`⟳ ${T('Neu einlesen','Read again')}`;
  $z('reload').classList.toggle('pri',!!(DIR&&!PERM));
  if(!has){last.innerHTML=''; list.innerHTML=`<p class="sz-empty">${DIR&&!PERM?T(`Der Ordner „${esc(DIR.name)}“ ist gemerkt; der Browser braucht nach dem Neuladen einmal deine Erlaubnis.`,`The folder “${esc(DIR.name)}” is remembered; after reloading, the browser needs your permission once.`)
    :T('Lade den Log-Ordner von Star Citizen (LIVE oder PTU). Dann siehst du hier, auf welchem Server und wo du zuletzt warst, auch nach einem Absturz.','Load the Star Citizen log folder (LIVE or PTU). Then you see here which server you were on and where, also after a crash.')}</p>`; return;}
  // "Last" = the newest session that joined a server (menu-only sessions are skipped).
  const s=SESS.find(x=>x.joins.length)||SESS[0], j=s.joins[s.joins.length-1];
  // The newest crash, if it is not the session shown as "last": after a crash one usually starts again.
  const c=SESS.find(x=>x.ended==='crash'&&x.joins.length), cj=c&&c.joins[c.joins.length-1];
  const crashCard=c&&c!==s?`<div class="sz-last crash"><h3>⚠ ${T('Letzter Absturz','Last crash')} · ${fmtT(c.end)}</h3>
    <div class="sz-shard">${esc(cj.shard)}<button type="button" class="sz-copy" data-copy="${esc(cj.shard)}">${T('kopieren','copy')}</button></div>
    <div class="sz-grid"><div><small>Region</small><b>${esc(region(cj.shard))}</b></div><div><small>Server</small><b class="sz-mono">${esc(cj.addr+':'+cj.port)}</b></div>
      <div><small>${T('Letzter Ort','Last place')}</small>${locHtml(c.loc)}${c.loc?`<small>${tOnly(c.loc.t)}</small>`:''}</div>
      <div><small>${T('Letztes Schiff','Last ship')}</small><b>${c.ship?esc(shipName(c.ship.raw)):'–'}</b></div></div></div>`:'';
  last.innerHTML=crashCard+`<div class="sz-last${s.ended==='crash'?' crash':''}"><h3>${T('Zuletzt','Last time')} · ${fmtT(s.start)}</h3>
    ${j?`<div class="sz-shard">${esc(j.shard)}<button type="button" class="sz-copy" data-copy="${esc(j.shard)}">${T('kopieren','copy')}</button></div>`:`<div>${T('Kein Server-Beitritt in dieser Sitzung.','No server join in this session.')}</div>`}
    <div class="sz-grid">
      <div><small>Region</small><b>${j?esc(region(j.shard)):'–'}</b></div>
      <div><small>Server</small><b class="sz-mono">${j?esc(j.addr+':'+j.port):'–'}</b>${j?`<small>${T('beigetreten','joined')} ${tOnly(j.t)}</small>`:''}</div>
      <div><small>${T('Letzter Ort','Last place')}</small>${locHtml(s.loc)}${s.loc?`<small>${tOnly(s.loc.t)}</small>`:''}</div>
      <div><small>${T('Letztes Schiff','Last ship')}</small><b>${s.ship?esc(shipName(s.ship.raw)):'–'}</b>${s.ship?`<small>${tOnly(s.ship.t)}</small>`:''}</div>
      <div><small>${T('Rechtsgebiet','Jurisdiction')}</small><b>${s.jur?esc(s.jur.n):'–'}</b>${s.jur?`<small>${tOnly(s.jur.t)}</small>`:''}</div>
      <div><small>${T('Ende','End')}</small>${endTag(s)}</div>
    </div></div>`;
  list.innerHTML=`<h2>${T('Letzte Sitzungen','Recent sessions')}</h2><div class="tablewrap"><table><thead><tr><th>${T('Beginn','Start')}</th><th>${T('Dauer','Duration')}</th><th>${T('Ende','End')}</th><th>${T('Letzter Shard','Last shard')}</th><th>${T('Letzter Ort','Last place')}</th><th>${T('Letztes Schiff','Last ship')}</th><th>${T('Server-Beitritte','Server joins')}</th></tr></thead><tbody>${SESS.map(x=>{const lj=x.joins[x.joins.length-1];
    return `<tr><td>${fmtT(x.start)}</td><td>${dur(x.start,x.end)}</td><td>${endTag(x)}</td><td>${lj?`<span class="sz-mono">${esc(lj.shard)}</span><br><small>${esc(region(lj.shard))}</small>`:'–'}</td><td>${locHtml(x.loc)}</td><td>${x.ship?esc(shipName(x.ship.raw)):'–'}</td>
      <td>${x.joins.length?`<details><summary>${x.joins.length}</summary><ol>${x.joins.map(k=>`<li>${tOnly(k.t)} · <span class="sz-mono">${esc(k.shard)}</span></li>`).join('')}</ol></details>`:'0'}</td></tr>`}).join('')}</tbody></table></div>
    <p class="sz-note">${T('Mehrere Beitritte in einer Sitzung entstehen meist über das Hauptmenü. Maßgeblich ist der letzte. Ob das Spiel dich gezielt auf denselben Shard zurücklässt, steht nicht im Log.','Several joins in one session usually come from the main menu; the last one counts. Whether the game lets you back onto the same shard is not in the log.')}</p>`;}

/* ---------- events ---------- */
$z('pick').addEventListener('click',pick);
$z('reload').addEventListener('click',reload);
$z('remember').addEventListener('click',remember);
$z('input').addEventListener('change',e=>{INI=iniFromInput(e.target.files); const f=filesFromInput(e.target.files); const root=(e.target.files[0]?.webkitRelativePath||'').split('/')[0]; readFiles(f,root||'Logs',true); e.target.value='';});
document.getElementById('view-sessions').addEventListener('click',async e=>{const c=e.target.closest('[data-copy]');
  if(c){try{await navigator.clipboard.writeText(c.dataset.copy); c.textContent=T('kopiert ✓','copied ✓');}catch(x){c.textContent=T('nicht möglich','not possible');} setTimeout(()=>{c.textContent=T('kopieren','copy');},1600); return;}
  const l=e.target.closest('[data-loc]'); if(l&&typeof LB!=='undefined'&&LB.openLoc) LB.openLoc(l.dataset.loc);});
let started=false;
return {render(){if(!started){started=true; init();} else render();}, start(){if(!started){started=true; init();}},
  pick, sessions:()=>SESS, ini:()=>INI, _setIni:f=>{INI=f;}, status:()=>$z('stat').textContent, _parse:parse, _placeOf:placeOf, _fromInput:filesFromInput, _read:readFiles, _shipName:shipName, _load:(list)=>{SESS=list; render(); loaded();}};
})();
"""
