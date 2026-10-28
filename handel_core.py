"""Fachlogik des SC Handels-Planers: Daten von star-head holen und auswerten.

Einzige Stelle für die Handels-Auswertung. Genutzt von
  - handels_planer_bauen.py   (Web-App + data.json, GitHub Actions)
  - update_starhead.py        (lokale Pipeline: xlsx, Routen-md/pdf, Mining-xlsx)

Quelle: https://api.star-head.de/{commodity,shop,shopitem/price,celestialobject,location}
Preis pricePerItem ist in cSCU -> *PRICE_FACTOR = aUEC/SCU.
"""
import concurrent.futures
import json
import re
import urllib.request
from collections import defaultdict

API = "https://api.star-head.de"
PRICE_FACTOR = 100
BULK_MIN_SCU = 100      # ab diesem Kauf-Bestand gilt eine Route als "Bulk"
ROUTES_N = (15, 15, 12)  # Tabellenlängen: Bulk legal, höchste Marge, illegal
# Laderaum-Beispiele für den Rechner (Name, SCU)
SHIPS = [("Cutlass Black", 46), ("Freelancer", 66), ("Mercury Star Runner", 114)]


# ---------------- Abruf ----------------
def loc(shop, ort):
    """Ort sauber: Shop, plus Station in Klammern nur wenn abweichend."""
    shop = shop or ""
    ort = ort or ""
    return f"{shop} ({ort})" if ort and ort != shop else shop


def get(path):
    req = urllib.request.Request(API + path, headers={"User-Agent": "Mozilla/5.0 sc-handel"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.loads(r.read().decode("utf-8"))


def get_prices(cid, tt):
    try:
        return get(f"/shopitem/price?commodityId={cid}&tradeType={tt}") or []
    except Exception:
        return []


def sys_heuristic(name):
    n = name or ""
    if re.match(r"^(ARC|HUR|CRU|MIC)\s?L\d", n):
        return "Stanton"
    if re.match(r"^PYR\d", n) or "Pyro" in n:
        return "Pyro"
    if "Nyx" in n or "Delamar" in n or "Levski" in n:
        return "Nyx"
    if "Stanton" in n:
        return "Stanton"
    return ""


def build_system_lookup():
    """Ort-/Shopname -> Sternensystem (Stanton/Pyro/Nyx)."""
    cel = get("/celestialobject")
    celsys = {c["name"]: (c.get("system") or {}).get("name") for c in cel if c.get("system")}
    locations = get("/location")

    def root_name(node):
        while node.get("parent"):
            node = node["parent"]
        return node.get("name")

    locsys = {}
    for loc_ in locations:
        rn = root_name(loc_)
        locsys[loc_["name"]] = celsys.get(rn) or sys_heuristic(rn) or sys_heuristic(loc_["name"])
    for k, v in celsys.items():
        locsys.setdefault(k, v)
    return locsys


def _price_row(c, x, kind, shopmap):
    sm = shopmap.get((x.get("shop") or {}).get("id"),
                     {"name": (x.get("shop") or {}).get("name", ""), "loc": "", "sys": ""})
    return {"ware": c["name"], "typ": c.get("type", ""), "illegal": c.get("isIllegal", False),
            "art": kind, "preis": round((x.get("pricePerItem") or 0) * PRICE_FACTOR, 2),
            "shop": sm["name"], "ort": sm["loc"], "system": sm["sys"],
            "invScu": x.get("maxInventoryScu"),
            "container": "/".join((z or "").replace("Size", "") for z in (x.get("containerSizes") or [])),
            "stand": (x.get("lastUpdated") or "")[:10]}


def summarise(c, b, s):
    """Beste Kauf-/Verkaufsstelle einer Ware. Bester Kauf = günstigster Ort MIT Bestand (>0),
    sonst günstigster überhaupt; bester Verkauf = teuerster Ort."""
    buy_p = [r for r in b if r["preis"] > 0]
    sell_p = [r for r in s if r["preis"] > 0]
    buy_stock = [r for r in buy_p if (r["invScu"] or 0) > 0]
    best_buy = min(buy_stock or buy_p, key=lambda r: r["preis"]) if buy_p else None
    best_sell = max(sell_p, key=lambda r: r["preis"]) if sell_p else None
    return {"ware": c["name"], "typ": c.get("type", ""), "illegal": c.get("isIllegal", False),
            "basePrice": c.get("basePrice", ""),
            "kaufPreis": best_buy["preis"] if best_buy else "",
            "kaufOrt": loc(best_buy["shop"], best_buy["ort"]) if best_buy else "",
            "kaufSys": best_buy["system"] if best_buy else "",
            "kaufInv": best_buy["invScu"] if best_buy else "",
            "verkaufPreis": best_sell["preis"] if best_sell else "",
            "verkaufOrt": loc(best_sell["shop"], best_sell["ort"]) if best_sell else "",
            "verkaufSys": best_sell["system"] if best_sell else "",
            "marge": round(best_sell["preis"] - best_buy["preis"], 2) if (best_buy and best_sell) else "",
            "nKauf": len(b), "nVerkauf": len(s)}


def fetch_all(log=print):
    """Alle Waren, Shops und Preise laden -> (rows, summary).
    rows: eine Zeile je Shop/Ware/Art; summary: eine Zeile je Ware mit bestem Kauf/Verkauf."""
    log("Lade Stammdaten ...")
    commodities = get("/commodity")
    shops = get("/shop")
    locsys = build_system_lookup()

    def shop_system(s):
        pn = (s.get("parent") or {}).get("name")
        return (locsys.get(pn) or locsys.get(s.get("name"))
                or sys_heuristic(pn) or sys_heuristic(s.get("name")) or "")

    shopmap = {s["id"]: {"name": s.get("name", ""), "loc": (s.get("parent") or {}).get("name", ""),
                         "sys": shop_system(s)} for s in shops}
    log(f"  {len(commodities)} Waren, {len(shops)} Shops. Lade Preise ...")
    rows, summary = [], []

    def work(c):
        b = [_price_row(c, x, "Kauf", shopmap) for x in get_prices(c["id"], "Buy")]
        s = [_price_row(c, x, "Verkauf", shopmap) for x in get_prices(c["id"], "Sell")]
        return c, b, s

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for c, b, s in ex.map(work, commodities):
            rows.extend(b)
            rows.extend(s)
            summary.append(summarise(c, b, s))
    log(f"  {len(rows)} Preiszeilen aggregiert.")
    return rows, summary


# ---------------- Eigene Daten (Export des Screenshot-Auswerters) ----------------
def merge_eigene(rows, summary, eintraege, log=print):
    """Konsolen-Daten aus dem SC Screenshot-Auswerter (Schema sc-konsole-export/1) in die
    star-head-Zeilen einarbeiten: gleicher Shop + Ware + Art wird ersetzt, Neues kommt dazu;
    jede übernommene Zeile trägt quelle="eigene". Danach wird summary (bester Kauf/Verkauf)
    neu berechnet, damit Routen und Orts-Ansichten dieselbe Logik sehen."""
    known = {s["ware"]: s for s in summary}
    index = {(r["ware"], r["art"], r["shop"], r["ort"]): i for i, r in enumerate(rows)}
    rows = list(rows)
    n_new = n_upd = n_skip = 0
    for e in eintraege:
        ware, art, shop = e.get("ware", ""), e.get("art", ""), e.get("shop", "")
        preis = e.get("preis_auec_scu")
        if ware not in known or art not in ("Kauf", "Verkauf") or not shop or not isinstance(preis, (int, float)) or preis <= 0:
            n_skip += 1
            continue
        if e.get("konfidenz") == "pruefen":
            n_skip += 1
            continue
        s = known[ware]
        key = (ware, art, shop, e.get("ort", ""))
        old = rows[index[key]] if key in index else None
        row = {"ware": ware, "typ": s["typ"], "illegal": s["illegal"], "art": art, "preis": float(preis),
               "shop": shop, "ort": e.get("ort", ""), "system": e.get("system", "") or (old or {}).get("system", ""),
               "invScu": e.get("bestand_scu") if art == "Kauf" and e.get("bestand_scu") is not None else (old or {}).get("invScu"),
               "container": (old or {}).get("container", ""), "stand": (e.get("stand") or "")[:10], "quelle": "eigene"}
        if old is None:
            index[key] = len(rows)
            rows.append(row)
            n_new += 1
        elif row["stand"] >= (old.get("stand") or ""):
            rows[index[key]] = row
            n_upd += 1
        else:
            n_skip += 1
    by_ware = {}
    for r in rows:
        by_ware.setdefault(r["ware"], ([], []))[0 if r["art"] == "Kauf" else 1].append(r)
    new_summary = []
    for s in summary:
        c = {"name": s["ware"], "type": s["typ"], "isIllegal": s["illegal"], "basePrice": s.get("basePrice", "")}
        b, v = by_ware.get(s["ware"], ([], []))
        new_summary.append(summarise(c, b, v))
    log(f"  Eigene Daten: {n_upd} Zeilen ersetzt, {n_new} neu, {n_skip} übersprungen (unbekannt, ohne Preis, zu prüfen oder älter).")
    return rows, new_summary


# ---------------- Auswertung ----------------
def _num(v):
    return isinstance(v, (int, float))


def select_routes(summary):
    """Die drei Routenlisten (absteigend nach Marge): bulk (legal, Kauf-Bestand >= BULK_MIN_SCU),
    legal (alle legalen), illegal."""
    valid = [s for s in summary if _num(s.get("marge")) and s["marge"] > 0
             and _num(s.get("kaufPreis")) and _num(s.get("verkaufPreis"))]
    legal = [s for s in valid if not s["illegal"]]
    illegal = [s for s in valid if s["illegal"]]
    bulk = [s for s in legal if _num(s.get("kaufInv")) and s["kaufInv"] >= BULK_MIN_SCU]
    for lst in (bulk, legal, illegal):
        lst.sort(key=lambda s: -s["marge"])
    return {"bulk": bulk, "legal": legal, "illegal": illegal}


def by_sell_location(rows, summary):
    """Je Verkaufsort: was lässt sich dort profitabel verkaufen (gegen den besten Kaufort der Ware)?
    Sortiert: Orte nach bester Marge, darin Waren nach Marge."""
    buymap = {s["ware"]: (s["kaufPreis"], s.get("kaufOrt", ""), s.get("kaufSys", ""))
              for s in summary if _num(s.get("kaufPreis"))}
    recs = []
    for r in rows:
        if r["art"] != "Verkauf" or not (r["preis"] > 0) or r["ware"] not in buymap:
            continue
        bp, bo, bsys = buymap[r["ware"]]
        marge = round(r["preis"] - bp, 2)
        if marge <= 0:
            continue
        recs.append({"vort": loc(r["shop"], r["ort"]), "sys": r["system"], "ware": r["ware"], "typ": r["typ"],
                     "illegal": r["illegal"], "vpreis": r["preis"], "kpreis": bp, "kort": bo, "ksys": bsys,
                     "marge": marge, "stand": r["stand"]})
    top = defaultdict(float)
    for x in recs:
        top[x["vort"]] = max(top[x["vort"]], x["marge"])
    recs.sort(key=lambda x: (-top[x["vort"]], x["vort"], -x["marge"]))
    return recs


def by_buy_location(rows, summary):
    """Je Kaufort: was lässt sich dort mit guter Marge einladen (gegen den besten Verkaufsort der Ware)?"""
    sellmap = {s["ware"]: (s["verkaufPreis"], s.get("verkaufOrt", ""), s.get("verkaufSys", ""))
               for s in summary if _num(s.get("verkaufPreis"))}
    krecs = []
    for r in rows:
        if r["art"] != "Kauf" or not (r["preis"] > 0) or r["ware"] not in sellmap:
            continue
        sp, so, ssys = sellmap[r["ware"]]
        marge = round(sp - r["preis"], 2)
        if marge <= 0:
            continue
        krecs.append({"kort": loc(r["shop"], r["ort"]), "sys": r["system"], "ware": r["ware"], "typ": r["typ"],
                      "illegal": r["illegal"], "kpreis": r["preis"], "vpreis": sp, "vort": so, "vsys": ssys,
                      "marge": marge, "inv": r.get("invScu"), "stand": r["stand"]})
    ktop = defaultdict(float)
    for x in krecs:
        ktop[x["kort"]] = max(ktop[x["kort"]], x["marge"])
    krecs.sort(key=lambda x: (-ktop[x["kort"]], x["kort"], -x["marge"]))
    return krecs


# ---------------- Routen-Guide (Markdown) ----------------
def fmt(n):
    return f"{n:,.0f}".replace(",", ".")


def _table(items, n):
    lines = ["| Ware | Kaufen bei | ~Kauf | Verkaufen bei | ~Verk. | Marge/SCU | je 100 SCU |",
             "|---|---|---:|---|---:|---:|---:|"]
    for s in items[:n]:
        lines.append(f'| **{s["ware"]}** | {s["kaufOrt"]} | {fmt(s["kaufPreis"])} '
                     f'| {s["verkaufOrt"]} | {fmt(s["verkaufPreis"])} '
                     f'| **{fmt(s["marge"])}** | {fmt(s["marge"] * 100)} |')
    return "\n".join(lines)


def routes_md(summary, stamp, patch):
    """Der Routen-Guide als Markdown (Text wie bisher in update_starhead.py)."""
    r = select_routes(summary)
    n_bulk, n_legal, n_ill = ROUTES_N
    ships = " · ".join(f"{n} ≈ {scu} SCU" for n, scu in SHIPS)
    return f"""# Top-Handelsrouten — Star Citizen (auto-generiert)

**Stand:** Daten abgerufen **{stamp}** · Spielstand **{patch}** · Quelle: star-head.de (Community-Daten)
**Marge/SCU** = bester Verkaufs- − bester Kaufpreis. „je 100 SCU" = grober Gewinn für eine 100-SCU-Ladung (ohne Sprit/Zeit/Risiko).

> ⚠️ **Vor dem Kauf prüfen:** Preise sind community-gepflegt und teils veraltet; Bestände schwanken.
> Die exakten Zahlen im Zweifel im Spiel / in `SC_Waren_Handelsuebersicht.xlsx` (Blatt „Alle Preise", Spalte „Stand") gegenchecken.

---

## 1) 🏆 Top legale Bulk-Routen (Kauf-Bestand ≥ {BULK_MIN_SCU} SCU)
Das sind die praktikablen „echten" Frachtrouten — Ware in Menge kaufbar.

{_table(r["bulk"], n_bulk)}

**Für deine Schiffe (Marge × Laderaum):** {ships}.
Beispiel Top-Route oben: Marge/SCU × {SHIPS[0][1]} ({SHIPS[0][0]}) bzw. × {SHIPS[-1][1]} ({SHIPS[-1][0]}) pro voller Ladung.

---

## 2) 💰 Höchste Margen insgesamt (inkl. Nischen-/Kleinmengen)
Höchste Marge pro SCU — aber teils nur in Kleinstmengen handelbar (Handsammel-Ware). Volumen im xlsx prüfen.

{_table(r["legal"], n_legal)}

---

## 3) 🕶️ Illegale Routen (hohe Marge, hohes Risiko)
Nur an versteckten Handelskonsolen / Outlaw-Stationen. Scan = Verlust + Crimestat.

{_table(r["illegal"], n_ill)}

---

## Nutzung & Update
- **Vollständige Daten:** `SC_Waren_Handelsuebersicht.xlsx` (alle {len(summary)} Waren, alle Kauf-/Verkaufsorte).
- **Online:** https://jaegerfeld.github.io/StarCitizen-Handels-Planer/ (täglich neu gebaut).
- **Neu ziehen (1–2×/Woche):** `update_starhead.py` ausführen → aktualisiert xlsx + diesen Guide automatisch.
- **Realismus:** Bestand `-`/`0` im xlsx = Ware gerade nicht auf Lager. Immer „Stand" beachten.

### Quelle
- star-head.de — Waren-Übersicht (offizielle API), abgerufen {stamp}
"""
