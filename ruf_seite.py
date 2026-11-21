# =============================================================================
# Autor:          Robert Seebauer
# Repository:     https://github.com/Jaegerfeld/StarCitizen-Handels-Planer
# KI-Unterstützung: Erstellt mit Unterstützung von Claude (Anthropic)
# Erstellt:       20.11.2026
# Geändert:       21.11.2026
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
#   1,0 = wie angegeben (Foxwell 19./20.11.2026 nach richtiger Lesart: 1,2 und
#   1,7, auf 1–2 Pixel gemessen; die frühere 0,55 beruhte auf der falschen
#   Lesart). Geteilte Missionen zählen als
#   Spanne (halber bis voller Betrag), Missionen ohne Wert und Fehlschläge mit 0,
#   werden aber angezeigt. Abgleiche und Favoriten liegen im Browser
#   (localStorage); nichts verlässt den Rechner.
#   Abgleich von Hand (Rang + Balken in %) oder per Screenshot der mobiGlas-
#   Seite „Ruf“ (Schritt 2): Die Seite findet die hervorgehobene Kachel (grüner
#   Rahmen = aktueller Rang, ihr Balken = Weg zum nächsten Rang; volle Balken =
#   durchlaufene Ränge) an den festen Kachelplätzen – relativ, als die Kachel,
#   deren Oberkante klar grüner ist als alle anderen, denn das mobiGlas ist
#   durchscheinend und ein heller Hintergrund färbt alle Kacheln. Lesart am
#   21.11.2026 im Spiel bestätigt: Bei Foxwell ist „Erfahren“ hervorgehoben,
#   und Robert sieht den Auftrag „Fuel Container Demolition“ (Mindeststufe
#   Erfahren). Bis 1.18.0 galt die hervorgehobene Kachel als nächster Rang –
#   alte Abgleiche werden einmal um eine Stufe hochgerechnet (load). Bei Leitern
#   mit der Kachel „Nicht berechtigt“ zählt sie eine Kachel weiter (Tabelle
#   „tiles0“). Den Balken misst sie als grüne Lauflänge
#   mit Teilpixeln an den Enden; den Zeitpunkt nimmt sie aus dem Dateinamen
#   (ScreenShot-JJJJ-MM-TT_hh-mm-ss). Geprüft an Roberts 20 Screenshots vom
#   21.11.2026 (2000×837, alle 20 Kacheln richtig). Das Bild wird nur im
#   Browser gelesen.
#   Mehrfach-Abgleich („Screenshots abgleichen …“): viele Screenshots oder ein
#   ganzer Ordner auf einmal. Die Organisation liest die Seite per
#   Texterkennung aus der Überschrift (tesseract.js 5.1.1, Apache-2.0, erst beim
#   ersten Mehrfach-Abgleich von jsDelivr geladen, feste Version mit
#   SRI-Prüfsumme; Sprachdaten lädt tesseract.js selbst). Je Organisation zählt
#   das neueste Bild; alles steht vor dem Übernehmen in einer Prüfliste, die
#   Organisation ist je Zeile änderbar. Ohne Internet bleibt die Auswahl von Hand.
#   Der Einzel-Abgleich je Organisation bleibt für die Feinjustierung.
#   Rang-Symbole: Jede Karte zeigt die Leiter als Reihe eigener Abzeichen wie die
#   Kacheln im mobiGlas – erreicht gefüllt, die nächste Stufe umrandet, spätere
#   blass. Die Abzeichen sind für dieses Werkzeug gezeichnet (Schild, 1–3 Sterne,
#   ab Stufe 4 Flügel, darüber Winkel bzw. Krone), keine Grafiken aus dem Spiel;
#   sie zeigen die Position in der Leiter, gleich für alle Organisationen.
#   Übersicht „Missionen nach Rufstufe“ je Organisation: Missionen der Ruf-Tabelle
#   nach ihrer Mindeststufe, freigeschaltet / als Nächstes / später nach dem
#   geschätzten Stand. Missionstexte optional (Schalter, aus = Standard): Sie
#   kommen zur Laufzeit aus der global.ini im geladenen Spielordner und werden
#   in einem Fenster gezeigt; die Seite selbst enthält keine Missionstexte.
#   Gilden (ab Alpha 5.0, Aufteilung laut Roberts Liste vom 20.11.2026, PTU):
#   Die Organisationen werden nach Gilden gruppiert; wer nicht in der Liste steht,
#   kommt unter „Keiner Gilde zugeordnet“. Alle bekannten Organisationen sind von
#   Anfang an sichtbar, auch ohne Logs; ohne Abgleich lassen sie sich ausblenden.
#   „Aufs Handy …“ (handy_seite.py) überträgt Rang und Balken der abgeglichenen
#   Organisationen; das Handy zeigt diesen Stand nur an, bis man die Ansicht beendet.
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
      <button type="button" class="btn" id="rf-batch">📷 <span class="de">Screenshots abgleichen …</span><span class="en">Align from screenshots …</span></button>
      <button type="button" class="btn" id="rf-handy">📱 <span class="de">Aufs Handy …</span><span class="en">To the phone …</span></button>
      <span class="rf-stat" id="rf-stat" role="status"></span>
    </div>
    <p class="rf-note" id="rf-texts-note" hidden></p>
    <p class="rf-note"><span class="de">Das Spiel schreibt keine Ruf-Punkte ins Log. Der Reiter rechnet: <b>Stand aus deinem mobiGlas</b> + Ruf der danach abgeschlossenen Missionen (laut Missionsbeschreibung × Faktor). Gleiche einmal je Organisation ab, dann läuft der Balken mit. Gleicher Log-Ordner wie unter „Sitzungen“.</span><span class="en">The game writes no reputation points to the log. This tab computes: <b>the state from your mobiGlas</b> + reputation of the missions completed afterwards (as stated in the mission description × factor). Align once per organisation, then the bar keeps up. Same log folder as under “Sessions”.</span></p>
    <div id="rf-list"></div>
    <p class="rf-note" id="rf-src"></p>
    <dialog id="rf-dlg" aria-labelledby="rf-dlg-h"><h3 id="rf-dlg-h"></h3><div id="rf-dlg-t"></div>
      <form method="dialog"><button class="btn" value="x">✕ <span class="de">Schließen</span><span class="en">Close</span></button></form></dialog>
    <dialog id="rf-bdlg" aria-labelledby="rf-bdlg-h"><h3 id="rf-bdlg-h"><span class="de">Screenshots abgleichen</span><span class="en">Align from screenshots</span></h3>
      <div class="rf-bpick" data-bdrop>
        <p><span class="de">Mehrere Screenshots der mobiGlas-Seite „Ruf“ auf einmal (je Organisation einer, Taste <b>Druck</b> im Spiel). Die Seite erkennt je Bild die Organisation, den erreichten Rang und den Balken; je Organisation zählt das neueste Bild. Du prüfst die Liste, dann übernimmst du sie. Das mobiGlas ist durchscheinend – vor dunklem Hintergrund aufgenommen klappt es am besten.</span><span class="en">Several screenshots of the mobiGlas “Reputation” page at once (one per organisation, <b>Print</b> key in game). The page finds the organisation, the rank reached and the bar in each image; per organisation the newest image counts. You check the list, then apply it. The mobiGlas is translucent – it works best in front of a dark background.</span></p>
        <button type="button" class="btn" id="rf-bfiles">🖼 <span class="de">Screenshots wählen …</span><span class="en">Choose screenshots …</span></button>
        <button type="button" class="btn" id="rf-bdir">📁 <span class="de">Ordner wählen …</span><span class="en">Choose folder …</span></button>
        <small class="de">oder Bilder hierher ziehen · Ordner: <code>StarCitizen\LIVE\screenshots</code></small><small class="en">or drop images here · folder: <code>StarCitizen\LIVE\screenshots</code></small>
        <input type="file" id="rf-bin" accept="image/*" multiple hidden><input type="file" id="rf-bdirin" webkitdirectory multiple hidden>
      </div>
      <p id="rf-bstat" role="status"></p>
      <div id="rf-bres"></div>
      <div class="rf-bbtns"><button type="button" class="btn pri" id="rf-bok" disabled>✓ <span>Übernehmen</span></button>
        <button type="button" class="btn" id="rf-bx">✕ <span class="de">Schließen</span><span class="en">Close</span></button></div>
    </dialog>
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
  #view-rep .rf-org{border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:0;background:var(--panel);min-width:0}
  /* Cards side by side: two or more per row on wide screens, one on narrow ones */
  #view-rep .rf-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,440px),1fr));gap:12px;align-items:start}
  #view-rep .rf-org.fav{border-color:var(--accent)}
  #view-rep .rf-head{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
  #view-rep .rf-head h3{font-family:var(--disp);font-size:17px;letter-spacing:.04em;margin:0;flex:1 1 auto}
  #view-rep .rf-rank{font-family:var(--disp);font-weight:700;font-size:14px;color:var(--accent);display:inline-flex;align-items:center;gap:8px}
  #view-rep .rf-ladder{display:flex;gap:4px;flex-wrap:wrap;margin:8px 0 2px;padding:0;list-style:none}
  #view-rep .rf-ladder li{display:flex;flex-direction:column;align-items:center;width:58px;font-size:10.5px;line-height:1.15;text-align:center;color:var(--muted);border:1px solid transparent;border-radius:8px;padding:3px 2px}
  #view-rep .rf-ladder li.done{color:var(--ink)}
  #view-rep .rf-ladder li.cur{border-color:var(--accent);color:var(--accent);font-weight:700}
  #view-rep .rf-ladder li.next{border-style:dashed;border-color:var(--accent);color:var(--ink)}
  #view-rep .rf-ladder li.later svg{opacity:.45}
  #view-rep .rf-ladder li span{overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;hyphens:auto;overflow-wrap:anywhere}
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
  #view-rep .rf-guild{margin:0 0 14px;border-top:1px solid var(--line)}
  #view-rep.rf-snapmode .rf-bar,#view-rep.rf-snapmode .rf-note{display:none}
  #view-rep .rf-snap{display:flex;gap:10px;flex-wrap:wrap;align-items:center;justify-content:space-between;border:2px solid var(--accent);border-radius:12px;padding:10px 14px;margin:0 0 12px;background:var(--panel2);font-size:14px}
  #view-rep .rf-snap .btn{min-height:44px}
  #view-rep .rf-guild>summary{list-style:none;cursor:pointer;min-height:44px;display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:8px 0}
  #view-rep .rf-guild>summary::-webkit-details-marker{display:none}
  #view-rep .rf-guild>summary::before{content:"▸";color:var(--accent);font-size:16px;transition:transform .15s}
  #view-rep .rf-guild[open]>summary::before{transform:rotate(90deg)}
  #view-rep .rf-guild>summary h2{font-family:var(--disp);font-size:15px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin:0}
  #view-rep .rf-guild>summary small{font-size:12.5px;color:var(--muted)}
  #view-rep .rf-guild>summary .rf-gd{flex-basis:100%;margin-left:26px}
  #view-rep .rf-toggle.off{opacity:.55;cursor:not-allowed}
  #view-rep .rf-lvl{margin:10px 0 0;border-left:4px solid var(--line);padding:2px 0 2px 10px}
  #view-rep .rf-lvl h4{margin:0 0 4px;font-family:var(--disp);font-size:14px;display:flex;gap:8px;flex-wrap:wrap;align-items:baseline}
  #view-rep .rf-lvl.done{border-left-color:var(--ok)}
  #view-rep .rf-lvl.next{border-left-color:var(--accent);background:var(--panel2);border-radius:0 8px 8px 0}
  #view-rep .rf-lvl.later{opacity:.7}
  #view-rep .rf-lvl ul{list-style:none;margin:0;padding:0;columns:2 340px;column-gap:24px}
  #view-rep .rf-lvl li{break-inside:avoid;display:flex;justify-content:space-between;gap:10px;font-size:13px;padding:3px 0;border-bottom:1px solid var(--line)}
  #view-rep .rf-lvl li small{color:var(--muted);white-space:nowrap}
  #view-rep [data-mtwhy]{cursor:help}
  #view-rep .rf-mt{font:inherit;font-size:13px;color:var(--accent);background:none;border:0;padding:0;min-height:28px;text-align:left;cursor:pointer;text-decoration:underline}
  #view-rep dialog{max-width:min(720px,92vw);max-height:84vh;border:1px solid var(--line);border-radius:12px;background:var(--panel);color:var(--ink);padding:16px 18px}
  #view-rep dialog::backdrop{background:rgba(0,0,0,.55)}
  #view-rep dialog h3{font-family:var(--disp);margin:0 0 10px}
  #view-rep #rf-dlg-t{white-space:pre-wrap;font-size:14px;line-height:1.5;max-height:62vh;overflow:auto}
  #view-rep dialog form{margin-top:12px;text-align:right}
  #view-rep dialog .btn{min-height:44px}
  #view-rep #rf-bdlg{max-width:min(980px,96vw);width:100%}
  #view-rep .rf-bpick{display:flex;gap:10px;flex-wrap:wrap;align-items:center;border:2px dashed var(--line);border-radius:10px;padding:10px}
  #view-rep .rf-bpick.drag{border-color:var(--accent);background:var(--panel2)}
  #view-rep .rf-bpick p{flex-basis:100%;margin:0;font-size:13.5px}
  #view-rep .rf-bpick small{color:var(--muted)}
  #view-rep #rf-bstat{font-size:13.5px;margin:10px 0}
  #view-rep #rf-bres{max-height:52vh;overflow:auto}
  #view-rep #rf-bres td{font-size:13px;vertical-align:middle}
  #view-rep #rf-bres tr.bad td:nth-child(3){color:var(--bad)}
  #view-rep #rf-bres select{min-height:40px;font:inherit;font-size:13px;padding:0 6px;border-radius:8px;border:1px solid var(--line);background:var(--panel2);color:var(--ink);max-width:260px}
  #view-rep #rf-bres input[type=checkbox]{width:22px;height:22px}
  #view-rep .rf-bbtns{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end;margin-top:12px}
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
const SKEY='scha_rep_v1', F0=1.0, MINLEARN=200;
let MIGRATED=0;   // alignments converted to the corrected tile reading on this load
const fmt=n=>Math.round(n).toLocaleString(L()==='en'?'en-GB':'de-DE');
const fmtT=s=>s?new Date(s).toLocaleString(L()==='en'?'en-GB':'de-DE',{dateStyle:'short',timeStyle:'short'}):'–';
// Title as in the table: markup of the translation removed, spaces collapsed (same rule as ruf_daten.norm_title).
const normT=s=>String(s||'').replace(/<[^>]+>|\[BP\]\*?|\*/g,' ').replace(/\s+/g,' ').trim();
const compact=s=>String(s||'').toLowerCase().replace(/[^a-z0-9]/g,'');
let OPEN=null;   // organisation whose alignment form is open

/* ---------- stored state ---------- */
function load(){let st; try{st=JSON.parse(localStorage.getItem(SKEY)||'{}');}catch(e){st={};}
  // Until 1.18.0 the highlighted tile counted as the next rank, so stored alignments are one rank too low: move each
  // up one band, keeping its share of the band. A value at the first threshold is left (ambiguous, usually a start).
  if(!st.lesart){let n=0;
    for(const [o,os] of Object.entries(st.orgs||{})){const l=ladder(o); if(l.length<2) continue;
      for(const c of os.cals||[]){const x=c.xp; if(x<=l[0][0]) continue; let j=0; while(j+1<l.length&&x>=l[j+1][0]) j++;
        if(j+1>=l.length) continue; const fr=(x-l[j][0])/(l[j+1][0]-l[j][0]), a=l[j+1][0], b=l[j+2]?l[j+2][0]:a;
        c.xp=Math.round(a+fr*(b-a)); n++;}}
    st.lesart=2; MIGRATED+=n; try{localStorage.setItem(SKEY,JSON.stringify(st));}catch(e){}}
  return st;}
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
// Names as in the table (Covalex, Rayari Incorporated, Wikelo Emporium …) so that nobody appears twice.
const EXTRA=['Cornerstone Developments','Northrock Service Group','Bounty Hunters Guild','Hockrow Agency'];
// Generic giver ids of the log that are no organisation.
const NOORG=new Set(['missiongiver','civilian']);
// All organisations: with a rank ladder, with missions in the table, and the extra ones of the guild list.
const known=()=>{if(!TAB) return EXTRA.slice(); const s=new Set(Object.keys(TAB.ladders)); for(const es of Object.values(TAB.missions)) for(const e of es) s.add(e[0]); for(const x of EXTRA) s.add(x); return [...s];};
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
    const tab=hit?hit.e:null;
    // "Shared" notification with the same title between accepting and ending (it carries no MissionId)
    const shared=shares.some(sh=>(!m.t||sh.t>=m.t)&&sh.t<=e.t&&normT(sh.x)===title);
    // A mission can pay reputation to two organisations at once; each gets its own entry
    const orgs=tab?[...new Set(tab.map(x=>x[0]))]:[orgName(m.org)];
    for(const org of orgs){if(!org) continue; const es=tab?tab.filter(x=>x[0]===org):null;
      out.push({t:e.t,id:e.id,title,org,res:e.r,lo:es?Math.min(...es.map(x=>x[1])):null,hi:es?Math.max(...es.map(x=>x[2])):null,shared});}}
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
// Measures the reputation tiles of a mobiGlas screenshot. The tiles sit at fixed places relative to image centre
// and height (four per row; measured at 2000×837). The highlighted tile (green frame = current rank) is the one whose
// top edge is clearly greener than all others – relative, because the mobiGlas is translucent and a bright
// background tints every tile. Its bar is measured as green run length with fractional edge pixels, against the
// length of the full bars of the tiles before it.
function measureShot(cv){const W=cv.width, H=cv.height, d=cv.getContext('2d',{willReadFrequently:true}).getImageData(0,0,W,H).data, s=H/837;
  const inside=(x,y)=>x>=0&&y>=0&&x<W&&y<H, at=(x,y)=>(Math.round(y)*W+Math.round(x))*4;
  const gr=(x,y)=>{if(!inside(x,y)) return 0; const i=at(x,y); return d[i+1]-d[i];};
  const bright=(x,y)=>{if(!inside(x,y)) return false; const i=at(x,y); return d[i+1]>150&&d[i+1]-d[i]>60;};
  const edge=(x,y)=>inside(x,y)?Math.min(1,Math.max(0,(d[at(x,y)+1]-100)/150)):0;
  const X0=W/2-204*s, Y0=276*s, DX=184*s, DY=186*s, BL=98.5*s;
  const slot=i=>[X0+(i%4)*DX, Y0+Math.floor(i/4)*DY];
  const top=i=>{const [x,y]=slot(i); let best=-1e9;
    for(let yy=Math.round(y-8*s);yy<=Math.round(y+8*s);yy++){let tt=0,n=0; for(let xx=Math.round(x+10*s);xx<x+150*s;xx++){tt+=gr(xx,yy); n++;} best=Math.max(best,tt/n);}
    return best;};
  const sc=[0,1,2,3,4,5,6,7].map(i=>({i,v:top(i)})).sort((p,q)=>q.v-p.v), conf=sc[0].v/Math.max(1,sc[1].v);
  if(sc[0].v<25||conf<1.6) return {err:T('Keine hervorgehobene Rang-Kachel gefunden. Ist es die mobiGlas-Seite „Ruf“ einer Organisation? Ein heller Hintergrund scheint durch das mobiGlas – dann vor dunklerem Hintergrund neu aufnehmen.','No highlighted rank tile found. Is it the mobiGlas “Reputation” page of an organisation? A bright background shows through the mobiGlas – then take it again in front of a darker one.')};
  // Bar of a tile: starts 32 px right of the frame; the row with the most green 93..109 px below its top edge
  const barRow=i=>{const [x,y]=slot(i), bx=x+32*s; let yb=y+101*s, best=-1e9;
    for(let yy=Math.round(y+93*s);yy<=Math.round(y+109*s);yy++){let tt=0; for(let xx=Math.round(bx);xx<bx+BL;xx++) tt+=gr(xx,yy); if(tt>best){best=tt; yb=yy;}}
    return [bx,yb];};
  // Green run length from the bar start, with the partly green boundary pixels as fractions
  const runAt=(x0,y)=>{let a=-1; for(let x=Math.floor(x0-4*s);x<x0+6*s;x++) if(bright(x,y)){a=x; break;}
    if(a<0) return edge(Math.round(x0),y)>.5?edge(Math.round(x0),y):0; let b=a; while(bright(b+1,y)) b++; return b-a+1+edge(a-1,y)+edge(b+1,y);};
  const cover=(x0,y)=>Math.max(runAt(x0,y-1),runAt(x0,y),runAt(x0,y+1));
  const idx=sc[0].i, [bx,yb]=barRow(idx);
  let Lc=0; for(let j=0;j<idx;j++){const [x,y]=barRow(j); Lc=Math.max(Lc,cover(x,y));}
  if(Lc<0.85*BL||Lc>1.2*BL) Lc=BL;   // no full bar before it: nominal length
  const pct=Math.max(0,Math.min(100,cover(bx,yb)/Lc*100));
  return {idx, pct:Math.round(pct*10)/10, weak:conf<2.5, box:[bx,yb,Lc],
    area:[Math.max(0,X0-40*s),Math.max(0,Y0-150*s),Math.min(W,800*s),Math.min(H,500*s)]};}
// Tiles before the first rank in the mobiGlas ("Nicht berechtigt" for hauling, security, bounty, emergency).
const offOf=o=>(TAB&&TAB.tiles0&&TAB.tiles0[o])||0;
// Rank reached and bar for one measured screenshot of organisation o: the highlighted tile is the current rank,
// its bar the way to the next one. Highlighted "Nicht berechtigt" (negative standing) counts as the first threshold.
function interpret(o,m){const l=ladder(o), k=m.idx-offOf(o);
  if(k<0) return {reached:l[0],next:null,pct:0,below:true};
  if(k>=l.length) return {err:T(`Hervorgehoben ist Kachel ${m.idx+1}, die Rangleiter von ${o} hat aber nur ${l.length+offOf(o)} Kacheln. Ist es der Screenshot dieser Organisation?`,`Tile ${m.idx+1} is highlighted, but the rank ladder of ${o} has only ${l.length+offOf(o)} tiles. Is it the screenshot of this organisation?`)};
  return {reached:l[k],next:l[k+1]||null,pct:l[k+1]?m.pct:0};}
const xpOf=r=>r.reached[0]+(r.next?(r.next[0]-r.reached[0])*r.pct/100:0);
const pctTxt=p=>String(p).replace('.',L()==='en'?'.':',');
// Time of the screenshot from its file name ("ScreenShot-2026-11-20_11-59-18-B56.jpg"), else the file date.
function shotTime(f){const m=/(\d{4})-(\d\d)-(\d\d)_(\d\d)-(\d\d)-(\d\d)/.exec(f.name||''); return m?new Date(+m[1],m[2]-1,+m[3],+m[4],+m[5],+m[6]):new Date(f.lastModified||Date.now());}
const localISO=d=>new Date(d.getTime()-d.getTimezoneOffset()*60000).toISOString().slice(0,16);
// Image file to canvas (Image element instead of createImageBitmap: works in more browsers and in headless tests).
async function shotCanvas(f){const url=URL.createObjectURL(f), bm=new Image(); bm.src=url;
  try{await new Promise((ok,no)=>{bm.onload=ok; bm.onerror=no;});} finally{URL.revokeObjectURL(url);}
  const cv=document.createElement('canvas'); cv.width=bm.naturalWidth; cv.height=bm.naturalHeight; cv.getContext('2d').drawImage(bm,0,0); return cv;}
// Read a screenshot file into the open form: measure, show a preview with the measured bar marked, fill the fields.
async function readShot(f,form){const res=form.querySelector('.rf-res'), o=form.dataset.form, l=ladder(o);
  res.className='rf-res'; res.textContent=T('Lese Screenshot …','Reading screenshot …');
  try{const cv=await shotCanvas(f), m=measureShot(cv);
    if(m.err){res.className='rf-res bad'; res.textContent=m.err; return;}
    const r=interpret(o,m);
    if(r.err){res.className='rf-res bad'; res.textContent=r.err; return;}
    form.rank.value=String(r.reached[0]); form.pct.type='text'; form.pct.value=r.next?pctTxt(r.pct):'0'; form.t.value=localISO(shotTime(f));
    // Preview: the tile area, the measured bar framed
    const [bx,by,bl]=m.box, [x0,y0,w,h]=m.area, pv=form.querySelector('canvas'); pv.width=420; pv.height=Math.round(420*h/w);
    const c=pv.getContext('2d'); c.drawImage(cv,x0,y0,w,h,0,0,pv.width,pv.height);
    const k=pv.width/w; c.strokeStyle='#ff5a5a'; c.lineWidth=2; c.strokeRect((bx-x0-4)*k,(by-y0-8)*k,(bl+8)*k,16*k); pv.hidden=false;
    const warn=m.weak?T(' Die Kachel war nur knapp zu erkennen (heller Hintergrund?) – bitte prüfen.',' The tile was barely visible (bright background?) – please check.'):'';
    res.className='rf-res'+(warn?' bad':'');
    res.textContent=(r.below?T(`Erkannt: „Nicht berechtigt“ ist hervorgehoben – gezählt als ${fmt(l[0][0])} XP.`,`Found: “Not eligible” is highlighted – counted as ${fmt(l[0][0])} XP.`)
      :r.next?T(`Erkannt: Rang ${r.reached[1]}, Weg zu ${r.next[1]} zu ${pctTxt(r.pct)} % gefüllt`,`Found: rank ${r.reached[1]}, way to ${r.next[1]} ${r.pct} % filled`)
      :T(`Erkannt: höchster Rang ${r.reached[1]}`,`Found: top rank ${r.reached[1]}`))
      +T(` · Zeitpunkt ${fmtT(shotTime(f).toISOString())}. Rot markiert ist der gemessene Balken – bitte kurz prüfen und übernehmen.`,` · time ${fmtT(shotTime(f).toISOString())}. The measured bar is framed in red – please check and apply.`)+warn;}
  catch(e){res.className='rf-res bad'; res.textContent=T('Bild konnte nicht gelesen werden.','Could not read the image.');}}

/* ---------- several screenshots at once ---------- */
const OCRLIB={src:'https://cdn.jsdelivr.net/npm/tesseract.js@5.1.1/dist/tesseract.min.js',sri:'sha384-GJqSu7vueQ9qN0E9yLPb3Wtpd7OrgK8KmYzC8T1IysG1bcvxvIO4qtYR/D3A991F'};
let OCRP=null, BATCH=[], BSTOP=false;
// Text recognition (English model: the organisation names are written in Latin capitals), loaded once on demand.
function ocrWorker(){if(OCRP) return OCRP;
  OCRP=new Promise((ok,no)=>{if(window.Tesseract) return ok(); const sc=document.createElement('script'); sc.src=OCRLIB.src; sc.integrity=OCRLIB.sri; sc.crossOrigin='anonymous'; sc.onload=ok; sc.onerror=no; document.head.appendChild(sc);})
    .then(()=>Tesseract.createWorker('eng')).catch(e=>{OCRP=null; throw e;});
  return OCRP;}
// Title line with the organisation name above the tiles, enlarged; white capitals become black on white.
function titleCanvas(cv){const s=cv.height/837, x=Math.max(0,cv.width/2-200*s), y=140*s, w=Math.min(cv.width-x,840*s), h=56*s, k=2;
  const c=document.createElement('canvas'); c.width=Math.round(w*k); c.height=Math.round(h*k); const g=c.getContext('2d',{willReadFrequently:true});
  g.drawImage(cv,x,y,w,h,0,0,c.width,c.height); const im=g.getImageData(0,0,c.width,c.height), p=im.data;
  for(let i=0;i<p.length;i+=4){const v=0.299*p[i]+0.587*p[i+1]+0.114*p[i+2]>185?0:255; p[i]=p[i+1]=p[i+2]=v;}
  g.putImageData(im,0,0); return c;}
// Edit distance of a name to its best matching part of the read text.
function subDist(pn,tx){let prev=new Array(tx.length+1).fill(0);
  for(let i=1;i<=pn.length;i++){const cur=[i]; for(let j=1;j<=tx.length;j++) cur[j]=Math.min(prev[j]+1,cur[j-1]+1,prev[j-1]+(pn[i-1]===tx[j-1]?0:1)); prev=cur;}
  return Math.min(...prev);}
// Known organisation that best matches the read title (at least 75 % of its letters right), else null.
function matchOrg(text){const tx=compact(text); if(tx.length<3) return null; let best=null;
  for(const o of known()){const k=compact(o); const sc=1-subDist(k,tx)/k.length; if(!best||sc>best.sc) best={o,sc};}
  return best&&best.sc>=0.75?best:null;}
// Which rows are applied by default: newest image per organisation, readable, not applied before.
function markBatch(){const st=load(), seen=new Set();
  for(const b of BATCH){b.old=false; b.dup=false; if(!b.org){b.ok=false; continue;}
    const cals=(st.orgs&&st.orgs[b.org]&&st.orgs[b.org].cals)||[];
    b.dup=cals.some(c=>Math.abs(new Date(c.t)-b.t)<60000); b.old=seen.has(b.org); seen.add(b.org);
    b.ok=!b.old&&!b.dup&&!interpret(b.org,b.m).err;}}
async function batchRead(files){const st=$r('bstat');
  files=[...files].filter(f=>/^image\//.test(f.type)||/\.(jpe?g|png|webp|bmp)$/i.test(f.name)).sort((p,q)=>shotTime(q)-shotTime(p));
  BATCH=[]; BSTOP=false; $r('bres').innerHTML=''; $r('bok').disabled=true;
  if(!files.length){st.textContent=T('Keine Bilder gefunden.','No images found.'); return;}
  let worker=null, skipped=0;
  for(let i=0;i<files.length&&!BSTOP;i++){const f=files[i]; st.textContent=T(`Lese Bild ${i+1} von ${files.length} …`,`Reading image ${i+1} of ${files.length} …`);
    let cv; try{cv=await shotCanvas(f);}catch(e){skipped++; continue;}
    const m=measureShot(cv); if(m.err){skipped++; continue;}
    if(worker===null){st.textContent=T('Lade die Texterkennung (nur beim ersten Mal, einige MB) …','Loading text recognition (first time only, a few MB) …');
      try{worker=await ocrWorker();}catch(e){worker=false;}}
    let hit=null, raw='';
    if(worker){try{const r=await worker.recognize(titleCanvas(cv)); raw=r.data.text.replace(/\s+/g,' ').trim(); hit=matchOrg(raw);}catch(e){}}
    BATCH.push({f,t:shotTime(f),m,org:hit?hit.o:'',raw,ok:false});}
  markBatch(); renderBatch(skipped,worker===false);}
function batchRow(b,i){const orgs=known().sort((p,q)=>p.localeCompare(q));
  const opts=[`<option value="">${T('– nicht erkannt, bitte wählen –','– not recognised, please choose –')}</option>`,...orgs.map(o=>`<option${o===b.org?' selected':''}>${esc(o)}</option>`)].join('');
  let info, bad=false;
  if(!b.org){bad=true; info=T('Organisation nicht erkannt','Organisation not recognised')+(b.raw?` (${T('gelesen','read')}: „${esc(b.raw.slice(0,40))}“)`:'');}
  else{const r=interpret(b.org,b.m);
    if(r.err){bad=true; info=esc(r.err);}
    else info=(r.below?T(`„Nicht berechtigt“ · ${fmt(r.reached[0])} XP`,`“Not eligible” · ${fmt(r.reached[0])} XP`)
      :r.next?`${esc(r.reached[1])} → ${esc(r.next[1])} ${pctTxt(r.pct)} % · ≈ ${fmt(xpOf(r))} XP`:`${esc(r.reached[1])} · ${T('höchster Rang','top rank')}`)
      +(b.old?' · '+T('älteres Bild, nicht übernommen','older image, not applied'):'')+(b.dup?' · '+T('schon übernommen','applied before'):'')
      +(b.m.weak?' · '+T('Kachel nur knapp erkannt (heller Hintergrund?)','tile barely visible (bright background?)'):'');}
  return `<tr class="${bad?'bad':''}"><td><input type="checkbox" data-bi="${i}"${b.ok?' checked':''}${b.org?'':' disabled'} aria-label="${T('übernehmen','apply')}"></td>
    <td><select data-bo="${i}" aria-label="${T('Organisation','Organisation')}">${opts}</select></td><td>${info}</td><td>${fmtT(b.t.toISOString())}</td></tr>`;}
let BSKIP=0, BNOOCR=false;
function renderBatch(skipped,noOcr){if(skipped!=null){BSKIP=skipped; BNOOCR=noOcr;} const n=BATCH.length;
  $r('bres').innerHTML=n?`<div class="tablewrap"><table><thead><tr><th>✓</th><th>${T('Organisation','Organisation')}</th><th>${T('Erkannt','Found')}</th><th>${T('Zeitpunkt','Time')}</th></tr></thead><tbody>${BATCH.map(batchRow).join('')}</tbody></table></div>`:'';
  bCount();}
function bCount(){const n=BATCH.length, k=BATCH.filter(b=>b.ok).length;
  $r('bstat').textContent=(n?T(`${n} Ruf-Screenshots gelesen`,`${n} reputation screenshots read`):T('Kein Ruf-Screenshot gefunden','No reputation screenshot found'))
    +(BSKIP?T(`, ${BSKIP} andere Bilder übersprungen`,`, ${BSKIP} other images skipped`):'')+'. '
    +(n?T(`${k} zum Übernehmen ausgewählt – bitte prüfen; die Organisation lässt sich je Zeile ändern.`,`${k} selected to apply – please check; the organisation can be changed per row.`):'')
    +(BNOOCR?' '+T('Texterkennung nicht verfügbar (offline?) – bitte die Organisation je Zeile wählen.','Text recognition not available (offline?) – please choose the organisation per row.'):'');
  const ok=$r('bok'); ok.disabled=!k; ok.lastChild.textContent=k?T(`${k} Abgleiche übernehmen`,`Apply ${k} alignments`):T('Übernehmen','Apply');}
function applyBatch(){const st=load(); let k=0;
  for(const b of BATCH){if(!b.ok||!b.org) continue; const r=interpret(b.org,b.m); if(r.err) continue;
    const os=orgState(st,b.org); os.cals.push({t:b.t.toISOString(),xp:Math.round(xpOf(r))}); os.cals.sort((p,q)=>p.t.localeCompare(q.t)); k++;}
  save(st); $r('bdlg').close(); render();
  $r('stat').textContent=T(`${k} Abgleiche aus Screenshots gespeichert.`,`${k} alignments from screenshots saved.`);}

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
    const items=g.list.sort((a,b)=>a.title.localeCompare(b.title)).map(x=>`<li>${canText?`<button type="button" class="rf-mt" data-mt="${esc(x.key)}" data-mtt="${esc(prettyT(x.title))}">${esc(prettyT(x.title))}</button>`:`<span data-mtwhy="${esc(prettyT(x.title))}">${esc(prettyT(x.title))}</span>`}<small>${x.lo===x.hi?fmt(x.lo):fmt(x.lo)+'–'+fmt(x.hi)} XP</small></li>`).join('');
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
// Click on a title while texts are off: say what is missing instead of doing nothing.
function showWhy(title){const dlg=$r('dlg'); $r('dlg-h').textContent=title;
  $r('dlg-t').textContent=!textsOn()?T('Missionstexte sind ausgeschaltet. Schalte oben „Missionstexte anzeigen“ ein, dann öffnet ein Klick auf den Titel den Text.','Mission texts are switched off. Switch on “Show mission texts” at the top, then a click on the title opens the text.')
    :T('Die Sprachdatei des Spiels fehlt (StarCitizen\\LIVE\\data\\Localization\\…\\global.ini). Lade über „Log-Ordner laden …“ den ganzen Ordner LIVE, nicht nur „logbackups“. Hinweis: Eine lokal geöffnete Datei des Planers hat einen eigenen Speicher – dort den Ordner einmal neu wählen.','The game’s language file is missing (StarCitizen\\LIVE\\data\\Localization\\…\\global.ini). Load the whole LIVE folder via “Load log folder …”, not just “logbackups”. Note: a locally opened copy of the planner has its own storage – choose the folder there once again.');
  if(!dlg.open) dlg.showModal();}
async function showText(key,title){const dlg=$r('dlg'); $r('dlg-h').textContent=title; $r('dlg-t').textContent=T('Lese Sprachdatei …','Reading language file …');
  if(!dlg.open) dlg.showModal();
  try{const map=await loadTexts(); $r('dlg-t').textContent=map&&map[key]?iniText(map[key]):T('Für diese Mission steht kein Text in der Sprachdatei.','No text for this mission in the language file.');}
  catch(e){$r('dlg-t').textContent=T('Die Sprachdatei konnte nicht gelesen werden – bitte den Log-Ordner neu laden.','The language file could not be read – please load the log folder again.');}}
function textsBar(){const box=$r('texts'), lab=box.closest('label'), has=!!iniFile(), note=$r('texts-note');
  box.checked=textsOn(); box.disabled=!has; lab.classList.toggle('off',!has);
  // The reason shows when the switch was on before or when someone clicks the greyed switch (no silent grey box)
  note.hidden=has||!(textsOn()||WHYTEXTS);
  lab.title=has?'':T('Braucht die Sprachdatei des Spiels – den ganzen Ordner LIVE laden.','Needs the game’s language file – load the whole LIVE folder.');
  note.textContent=has?'':T('Missionstexte brauchen die Sprachdatei des Spiels (StarCitizen\\LIVE\\data\\Localization\\…\\global.ini) im geladenen Ordner – die gibt es nur mit installierter Übersetzung. Lade dafür über „Log-Ordner laden …“ den ganzen Ordner LIVE, nicht nur „logbackups“. Eine lokal geöffnete Kopie des Planers hat einen eigenen Speicher – dort den Ordner einmal neu wählen.','Mission texts need the game’s language file (StarCitizen\\LIVE\\data\\Localization\\…\\global.ini) in the loaded folder – it exists only with a translation installed. Load the whole LIVE folder via “Load log folder …”, not just “logbackups”. A locally opened copy of the planner has its own storage – choose the folder there once again.');}
let WHYTEXTS=false;

/* ---------- to the phone ---------- */
const PKEY='scha_rep_snap';
const loadSnap=()=>{try{return JSON.parse(localStorage.getItem(PKEY)||'null');}catch(e){return null;}};
// Rank and bar of every aligned organisation (for the phone, which has no logs)
function handyData(){const ms=missions(), st=load(), out=[];
  for(const o of Object.keys(st.orgs||{})){const os=st.orgs[o]; if(!os.cals||!os.cals.length) continue;
    const e=estimate(o,ms,st), mid=(e.lo+e.hi)/2, [cur,next]=band(o,mid);
    out.push([o,cur[1],cur[0],next?next[1]:null,next?next[0]:null,Math.round(e.lo),Math.round(e.hi),os.fav?1:0]);}
  return {t:new Date().toISOString(),o:out};}
function fromHandy(d){if(!d||!Array.isArray(d.o)) throw new Error('format'); try{localStorage.setItem(PKEY,JSON.stringify(d));}catch(e){} render();}
function renderSnap(d){const list=$r('list');
  const card=([o,rank,cx,next,nx,lo,hi])=>{const mid=(lo+hi)/2, span=nx!=null?nx-cx:0, p=x=>span?Math.max(0,Math.min(100,(x-cx)/span*100)):100;
    return `<article class="rf-org"><div class="rf-head"><h3>${esc(o)}</h3></div><div class="rf-head"><span class="rf-rank">${rankBadge(o,mid)}${esc(rank)}</span></div>${ladderStrip(o,mid)}
      <div class="rf-track" role="img" aria-label="${T('Fortschritt','Progress')} ${Math.round(p(mid))} %"><div class="rf-fill" style="width:${p(lo)}%"></div><div class="rf-unc" style="left:${p(lo)}%;width:${Math.max(0,p(hi)-p(lo))}%"></div></div>
      <div class="rf-nums"><span><b>≈ ${fmt(mid)} XP</b>${hi-lo>=1?` <small>(${fmt(lo)}–${fmt(hi)})</small>`:''}</span><span>${next?T(`noch ≈ ${fmt(Math.max(0,nx-mid))} bis ${esc(next)}`,`≈ ${fmt(Math.max(0,nx-mid))} to ${esc(next)}`):T('höchster Rang','top rank')}</span></div></article>`;};
  const rows=d.o.slice().sort((a,b)=>b[7]-a[7]||a[0].localeCompare(b[0]));
  const groups=[...GUILDS.map(g=>({g,list:rows.filter(r=>guildOf(r[0])===g)})),{g:null,list:rows.filter(r=>!guildOf(r[0]))}].filter(x=>x.list.length);
  list.innerHTML=`<div class="rf-snap"><span>📱 ${T(`Stand vom PC · ${fmtT(d.t)} · nur ansehen`,`State from the PC · ${fmtT(d.t)} · view only`)}</span><button type="button" class="btn" data-snapend>${T('Ansicht beenden','End view')}</button></div>`
    +(groups.length?groups.map(x=>`<details class="rf-guild" open><summary><h2>${esc(x.g?x.g.n:T('Keiner Gilde zugeordnet','No guild assigned'))}</h2><small>${x.list.length}</small></summary><div class="rf-cards">${x.list.map(card).join('')}</div></details>`).join('')
    :`<p class="rf-empty">${T('Im übertragenen Stand ist keine Organisation abgeglichen.','No organisation is aligned in the transferred state.')}</p>`);}

/* ---------- rank badges ---------- */
// Own badge for position i of a ladder (drawn for this tool): shield with 1–3 stars, from the fourth rank on with
// wings, then one or two chevrons above, from the seventh a crown. st: 'done' filled, 'next' outlined in accent,
// 'later' outlined grey.
function starPath(cx,cy,r){let p=''; for(let k=0;k<10;k++){const a=-Math.PI/2+k*Math.PI/5, rr=k%2?r*.45:r; p+=(k?'L':'M')+(cx+rr*Math.cos(a)).toFixed(2)+' '+(cy+rr*Math.sin(a)).toFixed(2);} return p+'Z';}
function badge(i,st,sz){const fill=st==='done', col=st==='later'?'var(--muted)':'var(--accent)';
  const sf=fill?'var(--bg)':col, n=Math.min(3,i+1), ys=i<3?18:19;
  const pos=n===1?[[16,ys]]:n===2?[[12.5,ys],[19.5,ys]]:[[16,ys-4.5],[12,ys+2.5],[20,ys+2.5]];
  let g=`<path d="M16 7 L25 10.5 V17 C25 23 21 27.5 16 29.5 C11 27.5 7 23 7 17 V10.5 Z" fill="${fill?col:'none'}" stroke="${col}" stroke-width="1.6" stroke-linejoin="round"/>`;
  g+=pos.map(([x,y])=>`<path d="${starPath(x,y,n===3?3.2:3.6)}" fill="${sf}"/>`).join('');
  if(i>=3) g+=`<path d="M7 13 L1.5 10.5 L2.5 15 L1.5 17.5 L7 19.5 Z M25 13 L30.5 10.5 L29.5 15 L30.5 17.5 L25 19.5 Z" fill="${fill?col:'none'}" stroke="${col}" stroke-width="1.2" stroke-linejoin="round"/>`;
  if(i===4||i===5) for(let k=0;k<i-3;k++) g+=`<path d="M11.5 ${(6.3-k*2.7).toFixed(1)} L16 ${(3.6-k*2.7).toFixed(1)} L20.5 ${(6.3-k*2.7).toFixed(1)}" fill="none" stroke="${col}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>`;
  if(i>=6) g+=`<path d="M10 5.5 L11.5 1.5 L14 4 L16 0.8 L18 4 L20.5 1.5 L22 5.5 Z" fill="${fill?col:'none'}" stroke="${col}" stroke-width="1.2" stroke-linejoin="round"/>`;
  return `<svg width="${sz}" height="${sz}" viewBox="0 0 32 32" aria-hidden="true" focusable="false">${g}</svg>`;}
// Ladder as a row of badges like the mobiGlas tiles; x = XP now (null: not aligned, all grey).
function ladderStrip(o,x){const l=ladder(o); if(!l.length) return '';
  let cur=-1; if(x!=null) l.forEach((r,i)=>{if(x>=r[0]) cur=i;});
  // Short labels: the first word most ranks share ("Auftragnehmer", "Sicherheitsagent") is left out; full name in the tooltip
  const fw={}; for(const r of l){const w=r[1].split(' ')[0]; fw[w]=(fw[w]||0)+1;}
  const com=Object.keys(fw).find(w=>fw[w]>=3&&fw[w]>=l.length/2), short=n=>com&&n.startsWith(com+' ')?n.slice(com.length+1):n;
  const items=l.map(([xp,n],i)=>{const st=x==null?'later':i<=cur?'done':i===cur+1?'next':'later', cls=i===cur?'cur':st;
    return `<li class="${cls}" title="${esc(n)} · ${fmt(xp)} XP">${badge(i,st==='done'?'done':st,30)}<span>${esc(short(n))}</span></li>`;}).join('');
  const lab=x==null?T(`Rangleiter, ${l.length} Stufen`,`Rank ladder, ${l.length} ranks`):T(`Stufe ${cur+1} von ${l.length}`,`Rank ${cur+1} of ${l.length}`);
  return `<ul class="rf-ladder" role="img" aria-label="${esc(lab)}">${items}</ul>`;}
const rankBadge=(o,x)=>{const l=ladder(o); let cur=0; l.forEach((r,i)=>{if(x>=r[0]) cur=i;}); return badge(cur,'done',26);};

/* ---------- rendering ---------- */
function bar(o,est){const mid=(est.lo+est.hi)/2, [cur,next]=band(o,mid);
  if(!next) return {cur,next,html:`<div class="rf-track"><div class="rf-fill" style="width:100%"></div></div>`};
  const span=next[0]-cur[0], p=x=>Math.max(0,Math.min(100,(x-cur[0])/span*100));
  return {cur,next,html:`<div class="rf-track" role="img" aria-label="${T('Fortschritt','Progress')} ${Math.round(p(mid))} %"><div class="rf-fill" style="width:${p(est.lo)}%"></div><div class="rf-unc" style="left:${p(est.lo)}%;width:${Math.max(0,p(est.hi)-p(est.lo))}%"></div></div>`};}
function card(o,list,st){const est=estimate(o,list,st), os=orgState(st,o);
  const star=`<button type="button" class="rf-star" data-fav="${esc(o)}" aria-pressed="${os.fav}" aria-label="${T('Favorit','Favourite')}" title="${T('Oben anheften','Pin to top')}">${os.fav?'★':'☆'}</button>`;
  let body;
  if(!est.cal){body=`<p class="rf-meta">${T(`${est.mine.filter(m=>m.res==='Complete').length} abgeschlossene Missionen in den geladenen Logs. Noch kein Abgleich – trag einmal ein, was dein mobiGlas zeigt.`,`${est.mine.filter(m=>m.res==='Complete').length} completed missions in the loaded logs. Not aligned yet – enter once what your mobiGlas shows.`)}</p>`+ladderStrip(o,null);}
  else{const b=bar(o,est), mid=(est.lo+est.hi)/2, range=est.hi-est.lo>=1?` <small>(${fmt(est.lo)}–${fmt(est.hi)})</small>`:'';
    const up=b.cur[1]!==band(o,est.cal.xp)[0][1]?` <span class="rf-tag">${T('rechnerisch aufgestiegen','computed rank-up')}</span>`:'';
    body=`<div class="rf-head"><span class="rf-rank">${rankBadge(o,mid)}${esc(b.cur[1])}${up}</span></div>${ladderStrip(o,mid)}${b.html}
      <div class="rf-nums"><span><b>≈ ${fmt(mid)} XP</b>${range}</span><span>${b.next?T(`noch ≈ ${fmt(Math.max(0,b.next[0]-mid))} bis ${esc(b.next[1])} (${fmt(b.next[0])})`,`≈ ${fmt(Math.max(0,b.next[0]-mid))} to ${esc(b.next[1])} (${fmt(b.next[0])})`):T('höchster Rang','top rank')}</span></div>
      <p class="rf-meta">${T('Abgleich','Aligned')} ${fmtT(est.cal.t)} (${fmt(est.cal.xp)} XP) · ${T(`seit dann ${est.after.filter(m=>m.res==='Complete').length} Missionen, +${fmt(est.stated)} XP laut Beschreibung`,`since then ${est.after.filter(m=>m.res==='Complete').length} missions, +${fmt(est.stated)} XP as stated`)}
        · ${T('Faktor','factor')} ${est.fac.f.toFixed(2).replace('.',L()==='en'?'.':',')} ${est.fac.learned?T('(gelernt)','(learned)'):`<span class="est">${T('(geschätzt – zweiter Abgleich macht ihn genau)','(estimated – a second alignment makes it exact)')}</span>`}
        ${est.unknown?` · <span class="est">+? ${T(`aus ${est.unknown} Missionen ohne Wert`,`from ${est.unknown} missions without a value`)}</span>`:''}
        ${est.shared?` · ${T(`${est.shared} geteilt (halb bis voll gezählt)`,`${est.shared} shared (counted half to full)`)}`:''}
        ${est.failed?` · ${T(`${est.failed} fehlgeschlagen/abgebrochen (0 gezählt)`,`${est.failed} failed/abandoned (counted 0)`)}`:''}</p>`;}
  const rows=est.after.slice().reverse().map(m=>`<tr><td>${fmtT(m.t)}</td><td>${esc(prettyT(m.title))}${m.shared?`<span class="rf-tag">${T('geteilt','shared')}</span>`:''}</td><td>${m.res==='Complete'?'✓':`<span class="rf-tag fail">${esc(m.res==='Fail'?T('fehlgeschlagen','failed'):m.res==='Abandon'?T('abgebrochen','abandoned'):m.res)}</span>`}</td><td class="num">${m.lo==null?'?':m.lo===m.hi?fmt(m.lo):fmt(m.lo)+'–'+fmt(m.hi)}</td></tr>`).join('');
  const det=est.after.length?`<details><summary>${T(est.cal?'Missionen seit dem Abgleich':'Missionen in den geladenen Logs',est.cal?'Missions since the alignment':'Missions in the loaded logs')} (${est.after.length})</summary><div class="tablewrap"><table><thead><tr><th>${T('Ende','End')}</th><th>${T('Mission','Mission')}</th><th>${T('Ergebnis','Result')}</th><th class="num">${T('XP laut Beschreibung','XP as stated')}</th></tr></thead><tbody>${rows}</tbody></table></div></details>`:'';
  const acts=`<div class="rf-acts"><button type="button" class="btn" data-align="${esc(o)}">⇄ ${T('Stand aus dem mobiGlas abgleichen …','Align with the mobiGlas …')}</button>${os.cals.length?`<button type="button" class="btn" data-undo="${esc(o)}">↶ ${T('Letzten Abgleich entfernen','Remove last alignment')}</button>`:''}</div>`;
  const guess=ladderGuess(o)?`<p class="rf-meta"><span class="est">${T('Rangleiter nicht bekannt – Auftragnehmer-Stufen angenommen.','Rank ladder unknown – contractor ranks assumed.')}</span></p>`:'';
  return `<article class="rf-org${os.fav?' fav':''}" data-org="${esc(o)}"><div class="rf-head"><h3>${esc(o)}</h3>${star}</div>${body}${guess}${acts}${OPEN===o?form(o,est):''}${det}${overview(o,est)}</article>`;}
// Alignment form: current rank (highlighted tile), fill of its bar, time of the look into the mobiGlas.
function form(o,est){const l=ladder(o), cur=est.cal?band(o,(est.lo+est.hi)/2)[0][1]:(l[0]||[0,''])[1];
  const now=new Date(Date.now()-new Date().getTimezoneOffset()*60000).toISOString().slice(0,16);
  return `<form class="rf-form" data-form="${esc(o)}" novalidate>
    <p class="rf-help">${T('mobiGlas → Ruf → Organisation: Die <b>hervorgehobene Kachel</b> ist dein aktueller Rang, ihr Balken der Weg zum nächsten. Am genauesten: Screenshot auswerten lassen; sonst den hervorgehobenen Rang wählen und schätzen, wie weit sein Balken gefüllt ist.','mobiGlas → Reputation → organisation: the <b>highlighted tile</b> is your current rank, its bar the way to the next one. Most precise: let the page read a screenshot; otherwise choose the highlighted rank and estimate how far its bar is filled.')}</p>
    <div class="rf-shot" data-drop><button type="button" class="btn" data-shot>📷 ${T('Screenshot auswerten …','Read screenshot …')}</button><input type="file" accept="image/*" hidden data-shotin>
      <p class="rf-res" role="status">${T('Screenshot der Ruf-Seite dieser Organisation wählen oder hierher ziehen (Ordner <code>StarCitizen\\LIVE\\screenshots</code>). Die Felder werden ausgefüllt.','Choose or drop a screenshot of this organisation’s reputation page (folder <code>StarCitizen\\LIVE\\screenshots</code>). The fields get filled in.')}</p><canvas hidden></canvas></div>
    <label>${T('Rang (hervorgehobene Kachel)','Rank (highlighted tile)')}<select name="rank">${l.map(([x,n])=>`<option value="${x}"${n===cur?' selected':''}>${esc(n)} (${fmt(x)})</option>`).join('')}</select></label>
    <label>${T('Balken dieser Kachel in %','Bar of this tile in %')}<input name="pct" type="number" inputmode="decimal" min="0" max="100" step="0.5" value="0"></label>
    <label>${T('Zeitpunkt des Blicks','Time of the look')}<input name="t" type="datetime-local" value="${now}"></label>
    <div class="rf-btns"><button type="submit" class="btn pri">✓ ${T('Übernehmen','Apply')}</button><button type="button" class="btn" data-cancel>${T('Abbrechen','Cancel')}</button></div>
    <p class="rf-err" role="alert"></p></form>`;}
function render(){const list=$r('list'), S=(typeof SZ!=='undefined'&&SZ.sessions)?SZ.sessions():[];
  const snapD=loadSnap(); document.getElementById('view-rep').classList.toggle('rf-snapmode',!!snapD); if(snapD){renderSnap(snapD); return;}
  $r('src').textContent=TAB?T(`Ruf-Tabelle: ${Object.keys(TAB.missions).length} Missionstitel, Stand ${TAB.stand}. Quelle: ${TAB.quelle}.`,`Reputation table: ${Object.keys(TAB.missions).length} mission titles, as of ${TAB.stand}. Source: annotations of the German community translation (numbers, titles, rank names only).`):T('Ruf-Tabelle fehlt in diesem Bau.','Reputation table missing in this build.');
  $r('load').classList.toggle('pri',!S.length); textsBar(); if(textsOn()&&iniFile()) loadTexts().catch(()=>{});
  $r('stat').textContent=S.length?(SZ.status?SZ.status():''):'';
  if(MIGRATED){$r('stat').textContent=T(`${MIGRATED} bisherige Abgleiche auf die korrigierte Lesart umgerechnet (eine Stufe höher). Genauer ist ein neuer Abgleich: „Screenshots abgleichen …“.`,`${MIGRATED} earlier alignments converted to the corrected reading (one rank up). A new alignment is more precise: “Align from screenshots …”.`); MIGRATED=0;}
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
  const closed=gClosed();
  list.innerHTML=hint+(groups.length?groups.map(x=>{const gn=x.g?x.g.n:'-', aligned=x.list.filter(o=>orgState(st,o).cals.length).length;
      return `<details class="rf-guild" data-guild="${esc(gn)}"${closed.has(gn)?'':' open'}><summary><h2>${esc(x.g?x.g.n:T('Keiner Gilde zugeordnet','No guild assigned'))}</h2><small>${x.list.length} ${x.list.length===1?T('Organisation','organisation'):T('Organisationen','organisations')}${aligned?` · ${aligned} ${T('abgeglichen','aligned')}`:''}</small>
      <small class="rf-gd">${x.g?esc(T(x.g.d[0],x.g.d[1])):T('Im Testserver 5.0 noch keiner Gilde zugeordnet (geprüft 20.11.2026).','Not yet assigned to a guild on the 5.0 test server (checked 20 Nov 2026).')}</small></summary>
      <div class="rf-cards">${x.list.map(o=>card(o,ms,st)).join('')}</div></details>`;}).join('')
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
  if((b=e.target.closest('[data-mt]'))){showText(b.dataset.mt,b.dataset.mtt); return;}
  if((b=e.target.closest('[data-mtwhy]'))){showWhy(b.dataset.mtwhy); return;}
  if(e.target.closest('[data-snapend]')){try{localStorage.removeItem(PKEY);}catch(x){} render();}});
$r('handy').addEventListener('click',()=>{const d=handyData();
  if(!d.o.length){$r('stat').textContent=T('Noch keine Organisation abgeglichen – erst abgleichen, dann aufs Handy.','No organisation aligned yet – align first, then send to the phone.'); return;}
  HY.share('ruf',d,T('Ruf aufs Handy','Reputation to the phone'),T(`Rang und Balken von ${d.o.length} abgeglichenen Organisationen, Stand jetzt. Das Handy zeigt ihn nur an; für einen neuen Stand hier wieder scannen.`,`Rank and bar of ${d.o.length} aligned organisations, as of now. The phone only shows it; scan again here for a newer state.`));});
// Remember which overviews are open across re-renders
view.addEventListener('toggle',e=>{const d=e.target.closest&&e.target.closest('[data-ov]'); if(d){if(d.open) OVOPEN.add(d.dataset.ov); else OVOPEN.delete(d.dataset.ov);}},true);
const HKEY='scha_rep_hide', GKEY='scha_rep_gclosed';
// Guilds the player has folded in (remembered in the browser).
function gClosed(){try{return new Set(JSON.parse(localStorage.getItem(GKEY)||'[]'));}catch(e){return new Set();}}
view.addEventListener('toggle',e=>{const g=e.target.closest&&e.target.closest('[data-guild]'); if(!g||e.target!==g) return; const s=gClosed();
  if(g.open) s.delete(g.dataset.guild); else s.add(g.dataset.guild); try{localStorage.setItem(GKEY,JSON.stringify([...s]));}catch(x){}},true);
function hideOn(){try{return localStorage.getItem(HKEY)==='1';}catch(e){return false;}}
$r('hide').addEventListener('change',e=>{try{localStorage.setItem(HKEY,e.target.checked?'1':'0');}catch(x){} render();});
$r('texts').closest('label').addEventListener('click',()=>{if($r('texts').disabled){WHYTEXTS=true; textsBar();}});
$r('texts').addEventListener('change',e=>{try{localStorage.setItem(TKEY,e.target.checked?'1':'0');}catch(x){} render();});
view.addEventListener('change',e=>{const i=e.target.closest('[data-shotin]'); if(i&&i.files[0]) readShot(i.files[0],i.closest('form'));});
view.addEventListener('dragover',e=>{const z=e.target.closest('[data-drop]'); if(z){e.preventDefault(); z.classList.add('drag');}});
view.addEventListener('dragleave',e=>{const z=e.target.closest('[data-drop]'); if(z) z.classList.remove('drag');});
view.addEventListener('drop',e=>{const z=e.target.closest('[data-drop]'); if(!z) return; e.preventDefault(); z.classList.remove('drag');
  const f=[...(e.dataTransfer?.files||[])].find(f=>f.type.startsWith('image/')); if(f) readShot(f,z.closest('form'));});
// Several screenshots at once
$r('batch').addEventListener('click',()=>{BATCH=[]; $r('bres').innerHTML=''; $r('bstat').textContent=''; $r('bok').disabled=true; $r('bok').lastChild.textContent=T('Übernehmen','Apply'); $r('bdlg').showModal();});
$r('bfiles').addEventListener('click',()=>$r('bin').click());
$r('bdir').addEventListener('click',()=>$r('bdirin').click());
for(const id of ['bin','bdirin']) $r(id).addEventListener('change',e=>{const fs=[...e.target.files]; e.target.value=''; batchRead(fs);});
$r('bx').addEventListener('click',()=>{BSTOP=true; $r('bdlg').close();});
$r('bok').addEventListener('click',applyBatch);
$r('bres').addEventListener('change',e=>{const c=e.target.closest('[data-bi]'), s=e.target.closest('[data-bo]');
  if(c){BATCH[+c.dataset.bi].ok=c.checked; bCount();}
  if(s){BATCH[+s.dataset.bo].org=s.value; markBatch(); renderBatch();}});
const bz=document.querySelector('#rf-bdlg [data-bdrop]');
bz.addEventListener('dragover',e=>{e.preventDefault(); bz.classList.add('drag');});
bz.addEventListener('dragleave',()=>bz.classList.remove('drag'));
$r('bdlg').addEventListener('dragover',e=>e.preventDefault());
$r('bdlg').addEventListener('drop',e=>{e.preventDefault(); bz.classList.remove('drag'); batchRead(e.dataTransfer?.files||[]);});
view.addEventListener('submit',e=>{const f=e.target.closest('[data-form]'); if(!f) return; e.preventDefault();
  const o=f.dataset.form, l=ladder(o), x0=+f.rank.value, i=l.findIndex(r=>r[0]===x0), next=l[i+1];
  const pct=parseFloat(String(f.pct.value).replace(',','.')), err=f.querySelector('.rf-err');
  if(!(pct>=0&&pct<=100)){err.textContent=T('Bitte einen Wert von 0 bis 100 eintragen.','Please enter a value from 0 to 100.'); f.pct.focus(); return;}
  const t=f.t.value?new Date(f.t.value).toISOString():new Date().toISOString();
  const xp=x0+(next?(next[0]-x0)*pct/100:0), st=load(), os=orgState(st,o);
  os.cals.push({t,xp:Math.round(xp)}); os.cals.sort((a,b)=>a.t.localeCompare(b.t)); save(st); OPEN=null; render();
  $r('stat').textContent=T(`${o}: Abgleich gespeichert (${fmt(xp)} XP).`,`${o}: alignment saved (${fmt(xp)} XP).`);});

let started=false;
return {render(){if(!started){started=true; if(typeof SZ!=='undefined') SZ.start();} render();}, _missions:missions, _estimate:(o)=>estimate(o,missions(),load()), _band:band, handyData, fromHandy, _measure:measureShot, _interpret:interpret, _matchOrg:matchOrg, _titleCanvas:titleCanvas, _ocr:ocrWorker, _batchRead:files=>batchRead(files), _batch:()=>BATCH, _guildOf:o=>(guildOf(o)||{}).n||'', _orgName:orgName, _byRank:byRank, _iniText:iniText, _loadTexts:loadTexts};
})();
"""
