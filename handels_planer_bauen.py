"""SC Handels-Planer bauen: Handelsübersicht + Top-Routen als eine HTML-Datei (offline lauffähig).

Quelle: star-head.de (Community-Daten) über handel_core.fetch_all().
Erzeugt im Skript-Ordner:
  SC_Handels_Planer.html          die App mit eingebetteten Daten
  data.json                       derselbe Datenstand (Knopf "Neuesten Stand laden" holt ihn von Pages)
  SC_Waren_Top_Handelsrouten.md   der Routen-Guide als Markdown
  SC_Waren_Handelsuebersicht.xlsx nur mit --xlsx (braucht openpyxl)

Start:  py handels_planer_bauen.py            (oder Handels_Planer_aktualisieren.bat)
        py handels_planer_bauen.py --cache    (Rohdaten aus handel_cache.json statt star-head; zum Entwickeln)
"""
import json
import pathlib
import sys
from datetime import datetime, timezone

import handel_core as hc
from version import PATCH, VERSION

HERE = pathlib.Path(__file__).resolve().parent
OUT_HTML = HERE / "SC_Handels_Planer.html"
OUT_JSON = HERE / "data.json"
OUT_MD = HERE / "SC_Waren_Top_Handelsrouten.md"
OUT_XLSX = HERE / "SC_Waren_Handelsuebersicht.xlsx"
CACHE = HERE / "handel_cache.json"
DATA_URL = "https://jaegerfeld.github.io/StarCitizen-Handels-Planer/data.json"


def load_rows(use_cache):
    if use_cache and CACHE.exists():
        d = json.loads(CACHE.read_text(encoding="utf-8"))
        print(f"Rohdaten aus {CACHE.name} ({len(d['rows'])} Zeilen).")
        return d["rows"], d["summary"]
    rows, summary = hc.fetch_all()
    if use_cache:
        CACHE.write_text(json.dumps({"rows": rows, "summary": summary}, ensure_ascii=False), encoding="utf-8")
    return rows, summary


def num(v):
    return v if isinstance(v, (int, float)) else None


def build_data(rows, summary):
    """Kompaktes Datenobjekt für die App. Alle Auswertungen kommen aus handel_core."""
    idx = {s["ware"]: i for i, s in enumerate(summary)}
    wares = [{"w": s["ware"], "t": s["typ"], "il": 1 if s["illegal"] else 0, "bp": num(s.get("basePrice")),
              "kp": num(s.get("kaufPreis")), "ko": s.get("kaufOrt", ""), "ks": s.get("kaufSys", ""),
              "ki": num(s.get("kaufInv")), "vp": num(s.get("verkaufPreis")), "vo": s.get("verkaufOrt", ""),
              "vs": s.get("verkaufSys", ""), "m": num(s.get("marge")), "nk": s["nKauf"], "nv": s["nVerkauf"]}
             for s in summary]
    rws = [[idx[r["ware"]], 0 if r["art"] == "Kauf" else 1, r["preis"], r["shop"], r["ort"], r["system"],
            num(r.get("invScu")), r.get("container", ""), r.get("stand", "")] for r in rows]
    routes = {k: [idx[s["ware"]] for s in v] for k, v in hc.select_routes(summary).items()}
    bysell = [[x["vort"], x["sys"], idx[x["ware"]], x["vpreis"], x["kpreis"], x["kort"], x["ksys"], x["marge"], x["stand"]]
              for x in hc.by_sell_location(rows, summary)]
    bybuy = [[x["kort"], x["sys"], idx[x["ware"]], x["kpreis"], x["vpreis"], x["vort"], x["vsys"], x["marge"],
              num(x.get("inv")), x["stand"]] for x in hc.by_buy_location(rows, summary)]
    return {"schema": 1, "version": VERSION, "patch": PATCH, "source": "build",
            "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "wares": wares, "rows": rws, "routes": routes, "bysell": bysell, "bybuy": bybuy,
            "ships": hc.SHIPS, "bulk_min": hc.BULK_MIN_SCU, "routes_n": list(hc.ROUTES_N)}


def main(argv):
    use_cache = "--cache" in argv
    want_xlsx = "--xlsx" in argv
    try:
        rows, summary = load_rows(use_cache)
    except Exception as e:  # noqa: BLE001
        print(f"FEHLER: star-head nicht erreichbar: {e}", file=sys.stderr)
        return 1
    data = build_data(rows, summary)
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = HTML_TEMPLATE.replace("/*__DATA__*/{}", payload).replace("__DATA_URL__", DATA_URL)
    OUT_HTML.write_text(html, encoding="utf-8")
    OUT_JSON.write_text(payload, encoding="utf-8")
    stamp = data["generated"][:10]
    OUT_MD.write_text(hc.routes_md(summary, stamp, PATCH), encoding="utf-8")
    print(f"Geschrieben: {OUT_HTML.name} ({OUT_HTML.stat().st_size // 1024} KB), {OUT_JSON.name}, {OUT_MD.name}")
    if want_xlsx:
        from handel_xlsx import build_xlsx
        build_xlsx(rows, summary, stamp, PATCH, OUT_XLSX)
        print(f"Geschrieben: {OUT_XLSX.name}")
    r = data["routes"]
    print(f"  {len(summary)} Waren, {len(rows)} Preiszeilen, Routen: {len(r['bulk'])} Bulk / "
          f"{len(r['legal'])} legal / {len(r['illegal'])} illegal.")
    return 0


# ============================================================ HTML-Template
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="de" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SC Handels-Planer</title>
<meta name="description" content="Star Citizen Handels-Planer: Top-Handelsrouten, Handelsübersicht aller Waren, Kauf-/Verkaufsorte, Laderaum-Rechner. Daten: star-head.de, täglich neu gebaut.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Exo+2:wght@400;600;800&family=Rajdhani:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#f4f6f8; --panel:#ffffff; --panel2:#eef1f5; --ink:#141922; --muted:#5a6472;
    --line:#d5dbe3; --accent:#0e7c86; --accent2:#c9822a; --ok:#2e8b57; --bad:#b3452f;
    --glow:rgba(14,124,134,.12); --shadow:0 2px 12px rgba(20,30,40,.08);
    --disp:'Rajdhani',system-ui,sans-serif; --body:'Exo 2',system-ui,sans-serif;
  }
  :root[data-theme="dark"]{
    --bg:#0a0e14; --panel:#121822; --panel2:#0e131c; --ink:#e8edf4; --muted:#8b97a8;
    --line:#243040; --accent:#3fd0dd; --accent2:#f0a94a; --ok:#57c98a; --bad:#e8785c;
    --glow:rgba(63,208,221,.12); --shadow:0 4px 22px rgba(0,0,0,.5);
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--body);font-size:15px;line-height:1.45;-webkit-font-smoothing:antialiased}
  .hazard{height:5px;background:repeating-linear-gradient(45deg,var(--accent2) 0 14px,transparent 14px 28px);opacity:.9}
  .wrap{max-width:1280px;margin:0 auto;padding:0 16px 60px}
  header{padding:22px 0 10px}
  .eyebrow{font-family:var(--disp);font-weight:600;letter-spacing:.24em;text-transform:uppercase;color:var(--accent);font-size:11px;margin:0 0 4px}
  h1{font-family:var(--disp);font-weight:800;font-size:clamp(22px,3.5vw,32px);margin:0;letter-spacing:.01em}
  .lede{color:var(--muted);margin:6px 0 0;font-size:14px}
  .toolbar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:14px 0 4px}
  .btn{font-family:var(--disp);font-weight:600;font-size:14px;letter-spacing:.04em;background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px 14px;min-height:36px;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;gap:6px}
  .btn:hover{border-color:var(--accent);color:var(--accent)} .btn:disabled{opacity:.6;cursor:wait}
  .btn.swap{border-style:dashed}
  .stat{font-size:12.5px;color:var(--muted);margin-left:auto}
  .tabs{display:flex;gap:6px;flex-wrap:wrap;margin:14px 0 0;border-bottom:1px solid var(--line)}
  .tab{font-family:var(--disp);font-weight:700;font-size:15px;letter-spacing:.03em;padding:10px 16px;min-height:40px;border:1px solid transparent;border-bottom:none;border-radius:8px 8px 0 0;background:transparent;color:var(--muted);cursor:pointer}
  .tab[aria-selected="true"]{background:var(--panel);color:var(--accent);border-color:var(--line)}
  .panel{background:var(--panel);border:1px solid var(--line);border-top:none;border-radius:0 0 12px 12px;box-shadow:var(--shadow);padding:16px}
  .filters{display:flex;gap:10px;flex-wrap:wrap;align-items:end;margin:0 0 12px}
  .filters label{display:flex;flex-direction:column;gap:4px;font-size:12px;color:var(--muted)}
  .filters input,.filters select{font-family:var(--body);font-size:14px;background:var(--panel2);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:7px 10px;min-height:36px}
  .filters input[type=search]{min-width:220px}
  .filters input[type=number]{width:90px}
  .grp{display:flex;gap:10px;align-items:end;padding:8px 10px;border:1px solid var(--line);border-radius:10px;background:var(--panel2)}
  .grp .ttl{font-family:var(--disp);font-weight:700;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--accent);align-self:center}
  h2{font-family:var(--disp);font-weight:700;font-size:18px;margin:18px 0 2px}
  .sub{color:var(--muted);font-size:13px;margin:0 0 8px}
  .tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;margin:0 0 6px}
  table{width:100%;border-collapse:collapse;font-size:13.5px;min-width:700px}
  th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--line);vertical-align:top}
  th{font-family:var(--disp);font-weight:700;font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);background:var(--panel2);white-space:nowrap;position:sticky;top:0}
  th.sortable{cursor:pointer} th.sortable:hover{color:var(--accent)} th .arr{font-size:10px;margin-left:3px}
  td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
  td.m{font-weight:700;color:var(--ok)}
  tr:last-child td{border-bottom:none}
  tr.row{cursor:pointer} tr.row:hover td{background:var(--glow)} tr.row[aria-expanded="true"] td{background:var(--glow)}
  .ill{display:inline-block;font-size:11px;font-weight:700;border-radius:20px;padding:0 8px;border:1px solid var(--bad);color:var(--bad);margin-left:6px;vertical-align:middle}
  .sys{display:inline-block;font-size:11px;color:var(--muted);border:1px solid var(--line);border-radius:6px;padding:0 6px;margin-left:5px;vertical-align:middle}
  .warn{color:var(--accent2);font-size:11.5px;white-space:nowrap}
  .detail td{background:var(--panel2)} .detail .inner{display:grid;grid-template-columns:1fr 1fr;gap:14px} .detail h4{margin:0 0 6px;font-family:var(--disp);font-size:14px;color:var(--accent)}
  .detail table{min-width:0;font-size:12.5px} .detail th{position:static}
  @media (max-width:800px){.detail .inner{grid-template-columns:1fr}}
  .empty{padding:18px;color:var(--muted);text-align:center}
  .empty button{margin-left:8px}
  .loc{margin:10px 0 0;border:1px solid var(--line);border-radius:10px;overflow:hidden}
  .loc summary{cursor:pointer;padding:9px 12px;font-family:var(--disp);font-weight:700;font-size:15px;background:var(--panel2);list-style:none;display:flex;gap:8px;align-items:center}
  .loc summary::-webkit-details-marker{display:none} .loc summary::before{content:'▸';color:var(--accent);font-size:12px} .loc[open] summary::before{content:'▾'}
  .loc summary .cnt{margin-left:auto;font-size:12px;color:var(--muted);font-weight:500}
  .toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);background:var(--ink);color:var(--bg);padding:10px 16px;border-radius:10px;font-size:14px;opacity:0;transition:.2s;pointer-events:none;z-index:9}
  .toast.show{opacity:1}
  footer{margin-top:28px;color:var(--muted);font-size:12.5px;border-top:1px solid var(--line);padding-top:14px}
  footer a{color:var(--accent)}
  .en{display:none} [data-lang="en"] .de{display:none} [data-lang="en"] .en{display:revert}
  .hide{display:none!important}
</style>
</head>
<body>
<div class="hazard"></div>
<div class="wrap">
  <header>
    <p class="eyebrow"><span class="de">Handel · Waren · Routen</span><span class="en">Trade · Commodities · Routes</span></p>
    <h1><span class="de">SC Handels-Planer</span><span class="en">SC Trade Planner</span></h1>
    <p class="lede"><span class="de">Was kaufen, wo verkaufen, was bringt eine volle Ladung. Community-Daten von star-head.de – vor dem Kauf im Spiel gegenprüfen.</span><span class="en">What to buy, where to sell, what a full load earns. Community data from star-head.de – verify in game before buying.</span></p>
    <div class="toolbar">
      <button class="btn" id="langBtn" type="button">EN / DE</button>
      <button class="btn" id="themeBtn" type="button"><span class="de">Hell / Dunkel</span><span class="en">Light / Dark</span></button>
      <button class="btn" id="refreshBtn" type="button" title="Neuesten täglich gebauten Datenstand von GitHub laden"><span class="de">🔄 Neuesten Stand laden (GitHub)</span><span class="en">🔄 Load latest build (GitHub)</span></button>
      <a class="btn swap" href="https://jaegerfeld.github.io/StarCitizen-Bauplan-Planer/" target="_blank" rel="noopener">🛠️ <span class="de">Bauplan-Planer</span><span class="en">Blueprint Planner</span></a>
      <a class="btn swap" href="https://jaegerfeld.github.io/StarCitizen-Wikelo-Planer/" target="_blank" rel="noopener">🧮 <span class="de">Wikelo-Planer</span><span class="en">Wikelo Planner</span></a>
      <a class="btn swap" href="https://jaegerfeld.github.io/sc-guides/" target="_blank" rel="noopener">📚 <span class="de">Guides</span><span class="en">Guides</span></a>
      <span class="stat" id="buildStat"></span>
    </div>
  </header>

  <div class="tabs" role="tablist">
    <button class="tab" role="tab" data-view="routes" aria-selected="true"><span class="de">Routen</span><span class="en">Routes</span></button>
    <button class="tab" role="tab" data-view="wares" aria-selected="false"><span class="de">Alle Waren</span><span class="en">All commodities</span></button>
    <button class="tab" role="tab" data-view="sell" aria-selected="false"><span class="de">Nach Verkaufsort</span><span class="en">By sell location</span></button>
    <button class="tab" role="tab" data-view="buy" aria-selected="false"><span class="de">Nach Kaufort</span><span class="en">By buy location</span></button>
  </div>

  <!-- Routen -->
  <section class="panel" id="view-routes">
    <div class="filters">
      <div class="grp">
        <span class="ttl"><span class="de">Laderaum</span><span class="en">Cargo</span></span>
        <label><span class="de">Schiff</span><span class="en">Ship</span><select id="ship"></select></label>
        <label>SCU<input type="number" id="scu" min="1" max="100000" step="1"></label>
      </div>
      <label><span class="de">Kauf in System</span><span class="en">Buy in system</span><select id="rKs"></select></label>
      <label><span class="de">Verkauf in System</span><span class="en">Sell in system</span><select id="rVs"></select></label>
      <label><span class="de">Suche (Ware/Ort)</span><span class="en">Search (commodity/place)</span><input type="search" id="rQ" placeholder="z. B. Gold, Levski"></label>
    </div>
    <div id="routes"></div>
  </section>

  <!-- Alle Waren -->
  <section class="panel hide" id="view-wares">
    <div class="filters">
      <label><span class="de">Suche</span><span class="en">Search</span><input type="search" id="wQ" placeholder="Ware, Ort …"></label>
      <label><span class="de">Typ</span><span class="en">Type</span><select id="wTyp"></select></label>
      <label><span class="de">Legal</span><span class="en">Legal</span><select id="wLeg"><option value="all" data-i18n="all">alle</option><option value="legal" data-i18n="legalOnly">nur legal</option><option value="illegal" data-i18n="illegalOnly">nur illegal</option></select></label>
      <label><span class="de">Kauf in System</span><span class="en">Buy in system</span><select id="wKs"></select></label>
      <label><span class="de">Verkauf in System</span><span class="en">Sell in system</span><select id="wVs"></select></label>
    </div>
    <p class="sub"><span class="de">Zeile anklicken: alle Kauf- und Verkaufsorte der Ware. Bester Kauf = günstigster Ort mit Bestand; bester Verkauf = teuerster Ort.</span><span class="en">Click a row: all buy and sell locations. Best buy = cheapest place with stock; best sell = highest-paying place.</span></p>
    <div id="wares"></div>
  </section>

  <!-- Nach Verkaufsort -->
  <section class="panel hide" id="view-sell">
    <div class="filters">
      <label><span class="de">Suche (Ort/Ware)</span><span class="en">Search (place/commodity)</span><input type="search" id="sQ"></label>
      <label><span class="de">System</span><span class="en">System</span><select id="sSys"></select></label>
    </div>
    <p class="sub"><span class="de">Je Verkaufsort: was man dort mit Gewinn verkaufen kann (gegen den besten Kaufort der Ware). Orte nach bester Marge sortiert.</span><span class="en">Per sell location: what sells at a profit there (vs. the commodity's best buy place). Places sorted by best margin.</span></p>
    <div id="sell"></div>
  </section>

  <!-- Nach Kaufort -->
  <section class="panel hide" id="view-buy">
    <div class="filters">
      <label><span class="de">Suche (Ort/Ware)</span><span class="en">Search (place/commodity)</span><input type="search" id="bQ"></label>
      <label><span class="de">System</span><span class="en">System</span><select id="bSys"></select></label>
    </div>
    <p class="sub"><span class="de">Je Kaufort: was man dort mit guter Marge einladen kann (gegen den besten Verkaufsort der Ware), mit Kauf-Bestand.</span><span class="en">Per buy location: what loads there with a good margin (vs. the commodity's best sell place), with stock.</span></p>
    <div id="buy"></div>
  </section>

  <footer>
    <p><span class="de">Downloads: </span><span class="en">Downloads: </span><a href="SC_Waren_Handelsuebersicht.xlsx">Excel</a> · <a href="SC_Waren_Top_Handelsrouten.md">Routen (Markdown)</a> · <a href="data.json">data.json</a> <span class="de">(nur in der Online-Version)</span><span class="en">(online version only)</span></p>
    <p><span class="de">Marge/SCU = bester Verkaufs- − bester Kaufpreis, ohne Sprit, Zeit und Risiko. Preise sind community-gepflegt und teils Tage alt („Stand"). Illegale Waren nur an versteckten Konsolen; Scan = Verlust + CrimeStat.</span><span class="en">Margin/SCU = best sell − best buy price, excluding fuel, time and risk. Prices are community-maintained and may be days old ("as of"). Illegal goods only at hidden terminals; a scan means loss + CrimeStat.</span></p>
    <p><span class="de">Quelle: </span><span class="en">Source: </span><a href="https://star-head.de" target="_blank" rel="noopener">star-head.de</a> · <a href="https://github.com/Jaegerfeld/StarCitizen-Handels-Planer" target="_blank" rel="noopener">GitHub</a> · <span class="de">Inoffiziell, nicht mit CIG verbunden. Star Citizen® ist eine Marke von CIG. Alle Angaben ohne Gewähr.</span><span class="en">Unofficial, not affiliated with CIG. Star Citizen® is a trademark of CIG. No guarantee.</span></p>
  </footer>
</div>
<div class="toast" id="toast"></div>
<script>
const RAW = /*__DATA__*/{};
const DATA_URL = '__DATA_URL__';
const LS = {theme:'sc_handel_theme', lang:'sc_handel_lang', raw:'sc_handel_raw_v1', ship:'sc_handel_ship'};
const root=document.documentElement;
function load(k){try{const v=localStorage.getItem(k);return v?JSON.parse(v):null;}catch(e){return null;}}
function save(k,v){try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}}
let LANG = load(LS.lang)==='en' ? 'en' : 'de';
const I18N = {
  de:{all:'alle',legalOnly:'nur legal',illegalOnly:'nur illegal',allSys:'alle Systeme',custom:'eigener Wert',
      ware:'Ware',buyAt:'Kaufen bei',buy:'~Kauf',sellAt:'Verkaufen bei',sell:'~Verk.',margin:'Marge/SCU',perLoad:'Gewinn/Ladung',cost:'Einsatz/Ladung',stock:'Bestand',
      typ:'Typ',bestBuy:'Bester Kauf',bestSell:'Bester Verkauf',nPlaces:'#Orte',place:'Ort',price:'Preis',asOf:'Stand',cont:'Container',
      bulk:'Top legale Bulk-Routen',bulkSub:'Kauf-Bestand ≥ {n} SCU – Ware in Menge kaufbar, die praktikablen Frachtrouten.',
      legal:'Höchste Margen insgesamt',legalSub:'Inkl. Nischen- und Kleinmengen – teils nur in Kleinstmengen handelbar, Bestand prüfen.',
      illegal:'Illegale Routen',illegalSub:'Hohe Marge, hohes Risiko. Nur an versteckten Konsolen / Outlaw-Stationen.',
      stockLow:'Bestand < Laderaum',noRows:'Keine Ware passt zu den Filtern.',reset:'Filter zurücksetzen',
      buyPlaces:'Kauforte (günstigster zuerst)',sellPlaces:'Verkaufsorte (teuerster zuerst)',illegalTag:'illegal',
      refOk:'Neuester Stand geladen.',refSame:'Du hast bereits den neuesten Stand.',refErr:'GitHub nicht erreichbar – bestehende Daten bleiben.',loading:'⏳ lädt…',
      built:'gebaut',github:'GitHub-Stand',patch:'Patch',goods:'Waren',prices:'Preiszeilen',goodsN:'Waren'},
  en:{all:'all',legalOnly:'legal only',illegalOnly:'illegal only',allSys:'all systems',custom:'custom',
      ware:'Commodity',buyAt:'Buy at',buy:'~Buy',sellAt:'Sell at',sell:'~Sell',margin:'Margin/SCU',perLoad:'Profit/load',cost:'Outlay/load',stock:'Stock',
      typ:'Type',bestBuy:'Best buy',bestSell:'Best sell',nPlaces:'#Places',place:'Place',price:'Price',asOf:'As of',cont:'Container',
      bulk:'Top legal bulk routes',bulkSub:'Buy stock ≥ {n} SCU – available in quantity, the practical cargo routes.',
      legal:'Highest margins overall',legalSub:'Incl. niche and small quantities – some only tradable in tiny amounts, check stock.',
      illegal:'Illegal routes',illegalSub:'High margin, high risk. Only at hidden terminals / outlaw stations.',
      stockLow:'stock < cargo',noRows:'No commodity matches the filters.',reset:'Reset filters',
      buyPlaces:'Buy places (cheapest first)',sellPlaces:'Sell places (highest first)',illegalTag:'illegal',
      refOk:'Latest build loaded.',refSame:'You already have the latest build.',refErr:'GitHub unreachable – keeping current data.',loading:'⏳ loading…',
      built:'built',github:'GitHub build',patch:'Patch',goods:'commodities',prices:'price rows',goodsN:'commodities'}
};
function t(k,v){let s=(I18N[LANG][k]??I18N.de[k]??k);if(v)for(const x in v)s=s.replace('{'+x+'}',v[x]);return s;}
function fmt(n){return n==null?'–':Math.round(n).toLocaleString(LANG==='de'?'de-DE':'en-US');}
function esc(s){return String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
const $=s=>document.querySelector(s);
let toastT=null;function toast(m){const e=$('#toast');e.textContent=m;e.classList.add('show');clearTimeout(toastT);toastT=setTimeout(()=>e.classList.remove('show'),2600);}

// ---- Daten (eingebaut oder gecachter GitHub-Stand) ----
function loadRaw(){const c=load(LS.raw);return (c&&c.schema===RAW.schema&&c.wares)?c:RAW;}
let D=loadRaw();
let SYS=[], TYPS=[];
function ingest(d){
  D=d; SYS=[...new Set(d.wares.flatMap(w=>[w.ks,w.vs]).filter(Boolean))].sort();
  TYPS=[...new Set(d.wares.map(w=>w.t).filter(Boolean))].sort();
  for(const id of ['rKs','rVs','wKs','wVs','sSys','bSys']) fillSel($('#'+id),SYS,t('allSys'));
  fillSel($('#wTyp'),TYPS,t('all'));
  $('#buildStat').textContent=(d.source==='refresh'?t('github'):t('built'))+' '+d.generated+' · '+t('patch')+' '+d.patch+' · '+d.wares.length+' '+t('goodsN')+' · '+d.rows.length+' '+t('prices');
}
function fillSel(sel,items,first){const cur=sel.value;sel.innerHTML='<option value="">'+esc(first)+'</option>'+items.map(x=>`<option value="${esc(x)}">${esc(x)}</option>`).join('');if([...sel.options].some(o=>o.value===cur))sel.value=cur;}
const W=i=>D.wares[i];
function illTag(w){return w.il?` <span class="ill">${t('illegalTag')}</span>`:'';}
function sysTag(s){return s?` <span class="sys">${esc(s)}</span>`:'';}

// ---- Laderaum ----
function shipSetup(){
  const sel=$('#ship'); sel.innerHTML=D.ships.map(([n,s],i)=>`<option value="${i}">${esc(n)} (${s} SCU)</option>`).join('')+`<option value="custom">${t('custom')}</option>`;
  const p=load(LS.ship)||{i:0,scu:D.ships[0][1]};
  sel.value=p.i; $('#scu').value=p.scu;
  sel.addEventListener('change',()=>{if(sel.value!=='custom')$('#scu').value=D.ships[+sel.value][1];saveShip();renderRoutes();});
  $('#scu').addEventListener('input',()=>{sel.value='custom';saveShip();renderRoutes();});
}
function saveShip(){save(LS.ship,{i:$('#ship').value,scu:+$('#scu').value||0});}
function scuNow(){return Math.max(0,+$('#scu').value||0);}

// ---- Routen ----
function routeTable(ids,n,scu){
  const q=($('#rQ').value||'').trim().toLowerCase(), ks=$('#rKs').value, vs=$('#rVs').value;
  const list=ids.map(W).filter(w=>(!ks||w.ks===ks)&&(!vs||w.vs===vs)&&(!q||(w.w+' '+w.ko+' '+w.vo).toLowerCase().includes(q))).slice(0,n);
  if(!list.length) return `<div class="empty">${t('noRows')}<button class="btn" type="button" data-reset="r">${t('reset')}</button></div>`;
  const rows=list.map(w=>{
    const low=w.ki!=null&&scu>w.ki;
    return `<tr><td><b>${esc(w.w)}</b>${illTag(w)}</td><td>${esc(w.ko)}${sysTag(w.ks)}</td><td class="num">${fmt(w.kp)}</td><td>${esc(w.vo)}${sysTag(w.vs)}</td><td class="num">${fmt(w.vp)}</td><td class="num m">${fmt(w.m)}</td><td class="num">${fmt(w.kp*scu)}</td><td class="num"><b>${fmt(w.m*scu)}</b>${low?` <span class="warn" title="${t('stockLow')}">⚠ ${fmt(w.ki)} SCU</span>`:''}</td></tr>`;}).join('');
  return `<div class="tablewrap"><table><thead><tr><th>${t('ware')}</th><th>${t('buyAt')}</th><th class="num">${t('buy')}</th><th>${t('sellAt')}</th><th class="num">${t('sell')}</th><th class="num">${t('margin')}</th><th class="num">${t('cost')}</th><th class="num">${t('perLoad')}</th></tr></thead><tbody>${rows}</tbody></table></div>`;
}
function renderRoutes(){
  const scu=scuNow(), [nb,nl,ni]=D.routes_n;
  $('#routes').innerHTML=
    `<h2>🏆 ${t('bulk')}</h2><p class="sub">${t('bulkSub',{n:D.bulk_min})}</p>${routeTable(D.routes.bulk,nb,scu)}`+
    `<h2>💰 ${t('legal')}</h2><p class="sub">${t('legalSub')}</p>${routeTable(D.routes.legal,nl,scu)}`+
    `<h2>🕶️ ${t('illegal')}</h2><p class="sub">${t('illegalSub')}</p>${routeTable(D.routes.illegal,ni,scu)}`;
}

// ---- Alle Waren ----
let wSort={k:'m',dir:-1}, wOpen=null;
function renderWares(){
  const q=($('#wQ').value||'').trim().toLowerCase(), typ=$('#wTyp').value, leg=$('#wLeg').value, ks=$('#wKs').value, vs=$('#wVs').value;
  let list=D.wares.map((w,i)=>({w,i})).filter(({w})=>(!typ||w.t===typ)&&(leg==='all'||(leg==='illegal')===!!w.il)&&(!ks||w.ks===ks)&&(!vs||w.vs===vs)&&(!q||(w.w+' '+w.t+' '+w.ko+' '+w.vo).toLowerCase().includes(q)));
  const k=wSort.k, dir=wSort.dir;
  list.sort((a,b)=>{const x=a.w[k],y=b.w[k];if(x==null&&y==null)return 0;if(x==null)return 1;if(y==null)return -1;return (typeof x==='string'?x.localeCompare(y):x-y)*dir;});
  if(!list.length){$('#wares').innerHTML=`<div class="empty">${t('noRows')}<button class="btn" type="button" data-reset="w">${t('reset')}</button></div>`;return;}
  const th=(key,label,num)=>`<th class="sortable${num?' num':''}" data-sort="${key}">${label}${wSort.k===key?`<span class="arr">${dir<0?'▼':'▲'}</span>`:''}</th>`;
  const rows=list.map(({w,i})=>`<tr class="row" data-i="${i}" aria-expanded="${wOpen===i}"><td><b>${esc(w.w)}</b>${illTag(w)}</td><td>${esc(w.t)}</td><td class="num">${fmt(w.kp)}</td><td>${esc(w.ko)}${sysTag(w.ks)}</td><td class="num">${w.ki==null?'–':fmt(w.ki)}</td><td class="num">${fmt(w.vp)}</td><td>${esc(w.vo)}${sysTag(w.vs)}</td><td class="num m">${fmt(w.m)}</td><td class="num">${w.nk}/${w.nv}</td></tr>`+(wOpen===i?detailRow(i):'')).join('');
  $('#wares').innerHTML=`<div class="tablewrap"><table><thead><tr>${th('w',t('ware'))}${th('t',t('typ'))}${th('kp',t('bestBuy'),1)}<th>${t('place')}</th>${th('ki',t('stock'),1)}${th('vp',t('bestSell'),1)}<th>${t('place')}</th>${th('m',t('margin'),1)}<th class="num">${t('nPlaces')}</th></tr></thead><tbody>${rows}</tbody></table></div>`;
}
function detailRow(i){
  const rs=D.rows.filter(r=>r[0]===i), buys=rs.filter(r=>r[1]===0).sort((a,b)=>a[2]-b[2]), sells=rs.filter(r=>r[1]===1).sort((a,b)=>b[2]-a[2]);
  const tbl=(lst,withInv)=>lst.length?`<table><thead><tr><th>${t('place')}</th><th class="num">${t('price')}</th>${withInv?`<th class="num">${t('stock')}</th>`:''}<th>${t('cont')}</th><th>${t('asOf')}</th></tr></thead><tbody>${lst.map(r=>`<tr><td>${esc(r[3])}${r[4]&&r[4]!==r[3]?' <span class="sys">'+esc(r[4])+'</span>':''}${sysTag(r[5])}</td><td class="num">${fmt(r[2])}</td>${withInv?`<td class="num">${r[6]==null?'–':fmt(r[6])}</td>`:''}<td>${esc(r[7])}</td><td>${esc(r[8])}</td></tr>`).join('')}</tbody></table>`:`<p class="sub">–</p>`;
  return `<tr class="detail"><td colspan="9"><div class="inner"><div><h4>${t('buyPlaces')}</h4>${tbl(buys,true)}</div><div><h4>${t('sellPlaces')}</h4>${tbl(sells,false)}</div></div></td></tr>`;
}

// ---- Nach Ort ----
function renderLoc(id,recs,keyIdx,sysIdx,wIdx,cols,qId,sysId){
  const q=($('#'+qId).value||'').trim().toLowerCase(), sys=$('#'+sysId).value;
  const groups=new Map();
  for(const r of recs){ if(sys&&r[sysIdx]!==sys)continue; const w=W(r[wIdx]); if(q&&!(r[keyIdx]+' '+w.w).toLowerCase().includes(q))continue; (groups.get(r[keyIdx])||groups.set(r[keyIdx],[]).get(r[keyIdx])).push(r);}
  if(!groups.size){$('#'+id).innerHTML=`<div class="empty">${t('noRows')}<button class="btn" type="button" data-reset="${id}">${t('reset')}</button></div>`;return;}
  let html='', first=true;
  for(const [k,lst] of groups){
    html+=`<details class="loc"${first?' open':''}><summary>${esc(k)}${sysTag(lst[0][sysIdx])}<span class="cnt">${lst.length} ${t('goods')} · ${t('margin')} ${fmt(lst[0][7])}</span></summary><div class="tablewrap"><table><thead><tr>${cols.map(c=>`<th${c.num?' class="num"':''}>${c.l}</th>`).join('')}</tr></thead><tbody>${lst.map(r=>'<tr>'+cols.map(c=>`<td${c.num?' class="num"':''}${c.m?' class="num m"':''}>${c.f(r)}</td>`).join('')+'</tr>').join('')}</tbody></table></div></details>`;
    first=false;
  }
  $('#'+id).innerHTML=html;
}
function renderSell(){renderLoc('sell',D.bysell,0,1,2,[
  {l:t('ware'),f:r=>`<b>${esc(W(r[2]).w)}</b>${illTag(W(r[2]))}`},{l:t('sell'),num:1,f:r=>fmt(r[3])},{l:t('buy'),num:1,f:r=>fmt(r[4])},
  {l:t('buyAt'),f:r=>esc(r[5])+sysTag(r[6])},{l:t('margin'),m:1,f:r=>fmt(r[7])},{l:t('asOf'),f:r=>esc(r[8])}],'sQ','sSys');}
function renderBuy(){renderLoc('buy',D.bybuy,0,1,2,[
  {l:t('ware'),f:r=>`<b>${esc(W(r[2]).w)}</b>${illTag(W(r[2]))}`},{l:t('buy'),num:1,f:r=>fmt(r[3])},{l:t('stock'),num:1,f:r=>r[8]==null?'–':fmt(r[8])},{l:t('sell'),num:1,f:r=>fmt(r[4])},
  {l:t('sellAt'),f:r=>esc(r[5])+sysTag(r[6])},{l:t('margin'),m:1,f:r=>fmt(r[7])},{l:t('asOf'),f:r=>esc(r[9])}],'bQ','bSys');}

// ---- Views / Events ----
const VIEWS={routes:renderRoutes,wares:renderWares,sell:renderSell,buy:renderBuy};
function showView(v){document.querySelectorAll('.tab').forEach(b=>b.setAttribute('aria-selected',b.dataset.view===v));for(const k in VIEWS)$('#view-'+k).classList.toggle('hide',k!==v);VIEWS[v]();}
document.querySelectorAll('.tab').forEach(b=>b.addEventListener('click',()=>showView(b.dataset.view)));
function rerenderAll(){for(const k in VIEWS)if(!$('#view-'+k).classList.contains('hide'))VIEWS[k]();}
let deb=null;
for(const [id,fn] of [['rQ',renderRoutes],['rKs',renderRoutes],['rVs',renderRoutes],['wQ',renderWares],['wTyp',renderWares],['wLeg',renderWares],['wKs',renderWares],['wVs',renderWares],['sQ',renderSell],['sSys',renderSell],['bQ',renderBuy],['bSys',renderBuy]]){
  const el=$('#'+id); el.addEventListener(el.tagName==='INPUT'?'input':'change',()=>{clearTimeout(deb);deb=setTimeout(fn,130);});
}
document.addEventListener('click',e=>{
  const rs=e.target.closest('[data-reset]'); if(rs){const v=rs.dataset.reset; const ids={r:['rQ','rKs','rVs'],w:['wQ','wTyp','wLeg','wKs','wVs'],sell:['sQ','sSys'],buy:['bQ','bSys']}[v]||[]; ids.forEach(i=>{const el=$('#'+i);el.value=el.id==='wLeg'?'all':'';}); rerenderAll(); return;}
  const th=e.target.closest('th[data-sort]'); if(th){const k=th.dataset.sort; wSort= wSort.k===k?{k,dir:-wSort.dir}:{k,dir:(k==='w'||k==='t')?1:-1}; renderWares(); return;}
  const tr=e.target.closest('tr.row'); if(tr){const i=+tr.dataset.i; wOpen=wOpen===i?null:i; renderWares();}
});
$('#themeBtn').addEventListener('click',()=>{const n=root.getAttribute('data-theme')==='dark'?'light':'dark';root.setAttribute('data-theme',n);save(LS.theme,n);});
$('#langBtn').addEventListener('click',()=>{LANG=LANG==='de'?'en':'de';save(LS.lang,LANG);root.setAttribute('data-lang',LANG);root.setAttribute('lang',LANG);ingest(D);shipSetup();rerenderAll();});
async function refresh(){
  // Lädt den zuletzt auf GitHub gebauten Datenstand (täglich 05:00 UTC); kein Direktzugriff auf star-head aus dem Browser.
  const btn=$('#refreshBtn'); if(btn.dataset.busy)return; btn.dataset.busy='1'; btn.disabled=true;
  try{
    const r=await fetch(DATA_URL,{cache:'no-store'}); if(!r.ok)throw new Error('HTTP '+r.status);
    const g=await r.json(); if(!g||g.schema!==RAW.schema||!Array.isArray(g.wares)||!g.wares.length)throw new Error('schema');
    if(g.generated===D.generated){toast(t('refSame'));return;}
    g.source='refresh'; save(LS.raw,g); ingest(g); shipSetup(); rerenderAll(); toast(t('refOk'));
  }catch(e){toast(t('refErr'));}
  finally{btn.dataset.busy='';btn.disabled=false;}
}
$('#refreshBtn').addEventListener('click',refresh);
$('#refreshBtn').addEventListener('contextmenu',e=>{e.preventDefault();try{localStorage.removeItem(LS.raw);}catch(x){}ingest(RAW);shipSetup();rerenderAll();toast(t('built')+' '+RAW.generated);});

// ---- Init ----
(function init(){
  const th=load(LS.theme); if(th)root.setAttribute('data-theme',th);
  root.setAttribute('data-lang',LANG); root.setAttribute('lang',LANG);
  ingest(D); shipSetup(); showView('routes');
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
