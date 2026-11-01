# =============================================================================
# Autor:          Robert Seebauer
# Repository:     https://github.com/Jaegerfeld/StarCitizen-Handels-Planer
# KI-Unterstützung: Erstellt mit Unterstützung von Claude (Anthropic)
# Erstellt:       25.10.2026
# Geändert:       28.10.2026
# Lizenz:         BSD-3-Clause (siehe LICENSE)
#
# Fachliche Funktion:
#   Fachlogik des SC Handels-Planers und einzige Stelle der Handels-Auswertung.
#   Holt Waren, Shops und Preise von der star-head.de-API (commodity, shop,
#   shopitem/price, celestialobject, location), ordnet jeden Shop einem
#   Sternensystem (Stanton/Pyro/Nyx) zu und verdichtet je Ware den besten Kauf
#   (günstigster Ort mit Bestand) und den besten Verkauf (teuerster Ort).
#   pricePerItem kommt in cSCU und wird mit PRICE_FACTOR in aUEC/SCU umgerechnet.
#   Arbeitet eigene Konsolen-Daten des SC Screenshot-Auswerters ein (eigene_daten/):
#   gleicher Shop/Ort/Ware/Art wird ersetzt, wenn der eigene Stand gleich alt oder
#   neuer ist; Zeilen mit Konfidenz „pruefen“ werden übersprungen.
#   Wählt die drei Routenlisten (legale Bulk-Routen ab BULK_MIN_SCU Bestand,
#   höchste legale Margen, illegale Routen), baut die Ansichten je Verkaufs- und
#   Kaufort und schreibt den Routen-Guide als Markdown.
#   Genutzt von handels_planer_bauen.py (Web-App, data.json, GitHub Actions) und
#   update_starhead.py (lokale Pipeline: xlsx, Routen-md/pdf, Mining-xlsx).
#   Marge = bester Verkauf − bester Kauf, ohne Sprit, Zeit und Risiko.
# =============================================================================
"""Trade logic: fetch star-head.de prices, merge own data, select routes, render Markdown."""
import concurrent.futures
import json
import re
import urllib.request
from collections import defaultdict

#: Base URL of the star-head.de JSON API.
API = "https://api.star-head.de"
#: The API returns pricePerItem in cSCU; multiplying by this gives aUEC/SCU.
PRICE_FACTOR = 100
#: Minimum buy stock (SCU) for a legal route to count as a bulk route.
BULK_MIN_SCU = 100      # ab diesem Kauf-Bestand gilt eine Route als "Bulk"
#: Table lengths for bulk legal, highest legal margin and illegal routes.
ROUTES_N = (15, 15, 12)  # Tabellenlängen: Bulk legal, höchste Marge, illegal
#: Example cargo holds for the load calculator as (ship name, SCU).
SHIPS = [("Cutlass Black", 46), ("Freelancer", 66), ("Mercury Star Runner", 114)]


# ---------------- Fetching ----------------
def loc(shop, ort):
    """Format a place name as the shop, plus its station in brackets if different.

    Args:
        shop: Shop name (may be None).
        ort: Parent location / station name (may be None).

    Returns:
        "Shop (Station)" or just "Shop" when the station is empty or equal.
    """
    shop = shop or ""
    ort = ort or ""
    return f"{shop} ({ort})" if ort and ort != shop else shop


def get(path):
    """Fetch one star-head API endpoint and decode its JSON.

    Args:
        path: Endpoint path including query string, e.g. "/commodity".

    Returns:
        The decoded JSON value (usually a list of dicts).

    Raises:
        urllib.error.URLError: On network or HTTP errors.
        ValueError: If the response is not valid JSON.
    """
    req = urllib.request.Request(API + path, headers={"User-Agent": "Mozilla/5.0 sc-handel"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.loads(r.read().decode("utf-8"))


def get_prices(cid, tt):
    """Fetch all shop prices of one commodity for one trade type.

    Errors are swallowed so that one failing commodity does not stop the whole run.

    Args:
        cid: star-head commodity id.
        tt: Trade type, "Buy" or "Sell".

    Returns:
        List of shopitem price records, or an empty list on any error.
    """
    try:
        return get(f"/shopitem/price?commodityId={cid}&tradeType={tt}") or []
    except Exception:
        return []


def sys_heuristic(name):
    """Guess the star system from a place name when the API hierarchy has none.

    Args:
        name: Location or shop name (may be None).

    Returns:
        "Stanton", "Pyro", "Nyx" or "" if no rule matches.
    """
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
    """Build a lookup from location/shop name to star system.

    Walks each location up to its root body and takes that body's system; falls back
    to sys_heuristic() for names the API does not place in a system.

    Returns:
        Dict mapping place name to "Stanton", "Pyro", "Nyx" or "".

    Raises:
        urllib.error.URLError: If the API is unreachable.
    """
    cel = get("/celestialobject")
    celsys = {c["name"]: (c.get("system") or {}).get("name") for c in cel if c.get("system")}
    locations = get("/location")

    def root_name(node):
        """Return the name of the topmost parent of a location node."""
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
    """Turn one API price record into a flat price row (one shop, commodity, trade type).

    Args:
        c: Commodity record from /commodity.
        x: Price record from /shopitem/price.
        kind: "Kauf" (buy) or "Verkauf" (sell).
        shopmap: Shop id -> {"name", "loc", "sys"}.

    Returns:
        Row dict with price in aUEC/SCU, shop, location, system, stock, container sizes
        and the date of the last community update ("stand").
    """
    sm = shopmap.get((x.get("shop") or {}).get("id"),
                     {"name": (x.get("shop") or {}).get("name", ""), "loc": "", "sys": ""})
    return {"ware": c["name"], "typ": c.get("type", ""), "illegal": c.get("isIllegal", False),
            "art": kind, "preis": round((x.get("pricePerItem") or 0) * PRICE_FACTOR, 2),
            "shop": sm["name"], "ort": sm["loc"], "system": sm["sys"],
            "invScu": x.get("maxInventoryScu"),
            "container": "/".join((z or "").replace("Size", "") for z in (x.get("containerSizes") or [])),
            "stand": (x.get("lastUpdated") or "")[:10]}


def summarise(c, b, s):
    """Summarise one commodity: its best buy and best sell place and the margin.

    Best buy is the cheapest place with stock > 0, falling back to the cheapest place
    overall; best sell is the highest-paying place. Rows with price 0 are ignored.

    Args:
        c: Commodity record (needs "name"; "type", "isIllegal", "basePrice" optional).
        b: Buy price rows of this commodity.
        s: Sell price rows of this commodity.

    Returns:
        Summary dict; price, place and margin fields are "" when no valid price exists.
    """
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
    """Load all commodities, shops and prices from star-head (8 parallel workers).

    Args:
        log: Callable for progress messages.

    Returns:
        Tuple (rows, summary): rows has one entry per shop, commodity and trade type;
        summary has one entry per commodity with its best buy and sell.

    Raises:
        urllib.error.URLError: If the master data endpoints are unreachable.
    """
    log("Lade Stammdaten ...")
    commodities = get("/commodity")
    shops = get("/shop")
    locsys = build_system_lookup()

    def shop_system(s):
        """Return the star system of a shop via its parent location or name."""
        pn = (s.get("parent") or {}).get("name")
        return (locsys.get(pn) or locsys.get(s.get("name"))
                or sys_heuristic(pn) or sys_heuristic(s.get("name")) or "")

    shopmap = {s["id"]: {"name": s.get("name", ""), "loc": (s.get("parent") or {}).get("name", ""),
                         "sys": shop_system(s)} for s in shops}
    log(f"  {len(commodities)} Waren, {len(shops)} Shops. Lade Preise ...")
    rows, summary = [], []

    def work(c):
        """Fetch and convert buy and sell prices of one commodity."""
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


# ---------------- Own data (export of the screenshot evaluator) ----------------
def merge_eigene(rows, summary, eintraege, log=print):
    """Merge terminal data from the SC screenshot evaluator into the star-head rows.

    Entries follow the schema sc-konsole-export/1. A row with the same commodity, trade
    type, shop and location is replaced when the own date is the same or newer; unknown
    combinations are added. Entries are skipped if the commodity is unknown to star-head,
    the trade type is not "Kauf"/"Verkauf", the shop is empty, the price is missing or
    <= 0, the confidence is "pruefen", or the own date is older. Stock, system and
    container fall back to the replaced row. Merged rows carry quelle="eigene". The
    summary is then recomputed with summarise() so routes and location views use the
    same logic.

    Args:
        rows: star-head price rows from fetch_all().
        summary: Per-commodity summary from fetch_all().
        eintraege: Entries ("eintraege") of one or more export files.
        log: Callable for the result message.

    Returns:
        Tuple (rows, summary) with the merged rows and the recomputed summary.
    """
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


# ---------------- Evaluation ----------------
def _num(v):
    """Return True if v is a number (empty fields are stored as "")."""
    return isinstance(v, (int, float))


def select_routes(summary):
    """Select the three route lists, each sorted by margin (highest first).

    Only commodities with a positive margin and both prices are considered.

    Args:
        summary: Per-commodity summary.

    Returns:
        Dict with "bulk" (legal, buy stock >= BULK_MIN_SCU), "legal" (all legal) and
        "illegal" lists of summary entries.
    """
    valid = [s for s in summary if _num(s.get("marge")) and s["marge"] > 0
             and _num(s.get("kaufPreis")) and _num(s.get("verkaufPreis"))]
    legal = [s for s in valid if not s["illegal"]]
    illegal = [s for s in valid if s["illegal"]]
    bulk = [s for s in legal if _num(s.get("kaufInv")) and s["kaufInv"] >= BULK_MIN_SCU]
    for lst in (bulk, legal, illegal):
        lst.sort(key=lambda s: -s["marge"])
    return {"bulk": bulk, "legal": legal, "illegal": illegal}


def by_sell_location(rows, summary):
    """List what sells profitably at each sell location against the commodity's best buy.

    Args:
        rows: Price rows.
        summary: Per-commodity summary (source of the best buy price and place).

    Returns:
        Records with sell place, system, commodity, prices, buy place and margin; only
        positive margins. Places are sorted by their best margin, commodities within a
        place by margin.
    """
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
    """List what can be bought profitably at each buy location against the best sell place.

    Args:
        rows: Price rows.
        summary: Per-commodity summary (source of the best sell price and place).

    Returns:
        Records with buy place, system, commodity, prices, sell place, margin and stock;
        only positive margins. Places are sorted by their best margin, commodities within
        a place by margin.
    """
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


# ---------------- Route guide (Markdown) ----------------
def fmt(n):
    """Format a number without decimals and with a dot as thousands separator."""
    return f"{n:,.0f}".replace(",", ".")


def _table(items, n):
    """Render the first n route entries as a Markdown table.

    Args:
        items: Summary entries with prices, places and margin.
        n: Maximum number of rows.

    Returns:
        The Markdown table as a string.
    """
    lines = ["| Ware | Kaufen bei | ~Kauf | Verkaufen bei | ~Verk. | Marge/SCU | je 100 SCU |",
             "|---|---|---:|---|---:|---:|---:|"]
    for s in items[:n]:
        lines.append(f'| **{s["ware"]}** | {s["kaufOrt"]} | {fmt(s["kaufPreis"])} '
                     f'| {s["verkaufOrt"]} | {fmt(s["verkaufPreis"])} '
                     f'| **{fmt(s["marge"])}** | {fmt(s["marge"] * 100)} |')
    return "\n".join(lines)


def routes_md(summary, stamp, patch):
    """Render the route guide (bulk, highest margin, illegal) as German Markdown.

    Args:
        summary: Per-commodity summary.
        stamp: Date of the data fetch, shown in the guide.
        patch: Game version the data refers to.

    Returns:
        The complete Markdown document.
    """
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
