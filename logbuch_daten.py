# =============================================================================
# Autor:          Robert Seebauer
# Repository:     https://github.com/Jaegerfeld/StarCitizen-Handels-Planer
# KI-Unterstützung: Erstellt mit Unterstützung von Claude (Anthropic)
# Erstellt:       18.11.2026
# Geändert:       27.11.2026
# Lizenz:         BSD-3-Clause (siehe LICENSE)
#
# Fachliche Funktion:
#   Stammdaten für den Reiter „Fracht-Logbuch“: Orte mit Frachtaufzug, Waren und
#   Schiffe mit Laderaum, aus der öffentlichen UEX-API 2.0. Das Logbuch selbst
#   (eigene Schiffe, Bestand, Journal) liegt nur im Browser des Spielers; diese
#   Daten liefern nur die Auswahllisten.
#   Orte: UEX führt Terminals; das Frachtlager gilt im Spiel je Station, Stadt
#   oder Außenposten, deshalb werden die Terminals mit Frachtaufzug dazu
#   zusammengefasst (größte Containergröße des Aufzugs je Ort mitgeführt).
#   Schiffe: alle mit Laderaum (SCU > 0), ohne reine Konzepte, mit den erlaubten
#   Containergrößen. Waren: alle sichtbaren, mit Hinweisen illegal/flüchtig.
#   Wikelo-Zutaten: die Namen aller Zutaten aus den Tauschangeboten, wie sie der
#   Wikelo-Planer veröffentlicht (dessen data.json); sie dienen dem Buch für
#   wichtige Gegenstände als Vorschlagsliste. Ist die Datei nicht erreichbar,
#   bleibt die Liste leer und die Seite entsteht trotzdem.
# =============================================================================
"""Master data for the cargo ledger tab (places, commodities, ships) from UEX API 2.0."""
from __future__ import annotations

import json
import pathlib
import re
import time
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
#: UEX API base; requests carry a tool User-Agent.
API = "https://api.uexcorp.space/2.0"
UA = {"User-Agent": "sc-tools-handels-planer (github.com/Jaegerfeld)"}
#: Local cache for ``--cache`` builds (gitignored).
CACHE = HERE / "logbuch_cache.json"
#: Published data of the Wikelo-Planer (built daily); its recipes name the ingredients.
WIKELO_URL = "https://jaegerfeld.github.io/StarCitizen-Wikelo-Planer/data.json"
#: Planet codes the game uses in internal station names (RR_<code>_L<n>, RR_<code>_LEO).
RR_STANTON = {"ArcCorp": "ARC", "Crusader": "CRU", "Hurston": "HUR", "MicroTech": "MIC"}
RR_PYRO = {"Pyro I": 1, "Monox": 2, "Bloom": 3, "Pyro IV": 4, "Pyro V": 5, "Pyro VI": 6, "Terminus": 6}
#: The station that the game log calls RR_<code>_LEO where several orbit the same planet.
RR_LEO = {"Seraphim Station", "Everus Harbor", "Baijini Point", "Port Tressler", "Orbituary", "Ruin Station"}
#: Container sizes in SCU that exist in game.
SIZES = [1, 2, 4, 8, 16, 24, 32]


def _get(endpoint: str) -> list[dict]:
    """Fetch one UEX endpoint and return its ``data`` list."""
    req = urllib.request.Request(f"{API}/{endpoint}", headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["data"]


def _wikelo() -> dict | None:
    """Fetch the published data of the Wikelo-Planer; None if it cannot be had."""
    try:
        req = urllib.request.Request(WIKELO_URL, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except (OSError, ValueError) as e:
        print(f"WARNUNG: Wikelo-Zutaten nicht verfügbar ({e}); die Vorschlagsliste bleibt ohne sie.")
        return None


def load_raw(use_cache: bool) -> dict:
    """Terminals, commodities and vehicles from UEX, or from the cache (valid one day).

    Args:
        use_cache: Read ``logbuch_cache.json`` if it is younger than one day.

    Returns:
        ``{"terminals": [...], "commodities": [...], "vehicles": [...], "wikelo": {...} | None}``.
    """
    if use_cache and CACHE.exists() and time.time() - CACHE.stat().st_mtime < 86400:
        raw = json.loads(CACHE.read_text(encoding="utf-8"))
        if "wikelo" in raw:
            return raw
        # A cache written before the Wikelo list existed: add it once, keep the UEX part.
        raw["wikelo"] = _wikelo()
        CACHE.write_text(json.dumps(raw), encoding="utf-8")
        return raw
    raw = {k: _get(k) for k in ("terminals", "commodities", "vehicles")}
    raw["wikelo"] = _wikelo()
    if use_cache:
        CACHE.write_text(json.dumps(raw), encoding="utf-8")
    return raw


def wikelo_items(data: dict | None) -> list[str]:
    """Names of everything Wikelo's trades ask for or pay with, sorted, each once.

    The Wikelo-Planer keeps a trade's ingredients as text (``"3x Wikelo Favor; 1x Carinite (Pure)"``).
    Counts are dropped; a quality in the name (``... (Grade AA)``) stays, it is part of the item.

    Args:
        data: Published ``data.json`` of the Wikelo-Planer, or None.

    Returns:
        Ingredient names, plus what the currency exchanges pay out (e.g. ``Wikelo Favor``).
    """
    w = (data or {}).get("wikelo") or {}
    trades = list(w.get("ships") or []) + list(w.get("items") or []) + list(w.get("currency_exchanges") or [])
    if isinstance(w.get("intro_mission"), dict):
        trades.append(w["intro_mission"])
    texts = [t.get("recipe") or "" for t in trades if isinstance(t, dict)]
    texts += [t.get("reward") or "" for t in w.get("currency_exchanges") or [] if isinstance(t, dict)]
    names: dict[str, str] = {}
    for text in texts:
        for part in str(text).split(";"):
            name = re.sub(r"^\s*\d+(?:[.,]\d+)?\s*x\s+", "", part, flags=re.IGNORECASE).strip()
            if name:
                names.setdefault(name.lower(), name)
    return sorted(names.values(), key=str.lower)


def rr_code(t: dict) -> str | None:
    """Internal name the game log uses for a station (e.g. ``RR_MIC_L1``, ``RR_JP_PyroNyx``).

    Lets the sessions tab map ``<RequestLocationInventory> Location[RR_…]`` to a place; derived
    from the UEX orbit name (``"<body> Lagrange Point <n>"`` or the body itself for low orbit).

    Args:
        t: UEX terminal record.

    Returns:
        The internal code, or None if the terminal is no rest stop or gateway.
    """
    st, orbit = t.get("space_station_name"), t.get("orbit_name") or ""
    if not st:
        return None
    gate = re.match(r"(\w+) Gateway \((\w+)\)$", st)
    if gate:
        return f"RR_JP_{gate.group(2)}{gate.group(1)}"
    lag = re.match(r"(.+) Lagrange Point (\d)$", orbit)
    body, n = (lag.group(1), lag.group(2)) if lag else (orbit, None)
    # UEX writes the planet both as "MicroTech" and "microTech"; compare without case.
    stanton = {k.lower(): v for k, v in RR_STANTON.items()}
    code = stanton.get(body.lower()) or (f"P{RR_PYRO[body]}" if body in RR_PYRO else None)
    if not code:
        return None
    if n:
        return f"RR_{code}_L{n}"
    return f"RR_{code}_LEO" if st in RR_LEO else None


def places(terminals: list[dict]) -> list[dict]:
    """Stations, cities and outposts where cargo can be stored, one entry per place.

    Args:
        terminals: UEX terminal records.

    Returns:
        Places sorted by system, body and name: id (``system|name``), name, system, body,
        largest container and, for stations, the internal name used in game logs (``rr``).
    """
    out: dict = {}
    for t in terminals:
        # UEX flags freight elevators incompletely (in Nyx only on retired Levski terminals), so a
        # commodity terminal or a cargo center also counts as a place where cargo can be stored.
        storable = (t.get("has_freight_elevator") or t.get("is_cargo_center")
                    or t.get("type") in ("commodity", "commodity_raw"))
        if not storable or not t.get("is_available"):
            continue
        name = (t.get("space_station_name") or t.get("city_name") or t.get("outpost_name")
                or t.get("nickname") or t.get("name"))
        sys_ = t.get("star_system_name") or "?"
        key = (sys_, name)
        # Stable id from system and name, so stored cargo survives new or renamed UEX entries.
        p = out.setdefault(key, {"id": f"{sys_}|{name}", "n": name, "sys": sys_,
                                 "body": t.get("moon_name") or t.get("planet_name") or "",
                                 "max": 0})
        p["max"] = max(p["max"], t.get("max_container_size") or 0)
        rr = rr_code(t)
        if rr:
            p["rr"] = rr
    # Stanton first (the home system), then the others alphabetically.
    return sorted(out.values(), key=lambda p: (p["sys"] != "Stanton", p["sys"], p["body"], p["n"]))


def wares(commodities: list[dict]) -> list[dict]:
    """Visible commodities with category, warning flags (illegal, volatile) and UEX sell price."""
    out = []
    for c in commodities:
        if not c.get("is_visible"):
            continue
        out.append({"id": c["id"], "n": c["name"], "k": (c.get("kind") or "").capitalize(),
                    "il": 1 if c.get("is_illegal") else 0,
                    "vq": 1 if c.get("is_volatile_qt") else 0,
                    "vt": 1 if c.get("is_volatile_time") else 0,
                    # UEX average sell price per SCU, fallback when star-head does not list it.
                    "ps": round(c["price_sell"]) if (c.get("price_sell") or 0) > 0 else None})
    return sorted(out, key=lambda w: w["n"].lower())


def ships(vehicles: list[dict]) -> list[dict]:
    """Ships and vehicles with cargo space and their allowed container sizes."""
    out = []
    for v in vehicles:
        scu = v.get("scu") or 0
        if scu <= 0 or v.get("is_concept"):
            continue
        sizes = [int(s) for s in str(v.get("container_sizes") or "").split(",") if s.strip().isdigit()]
        out.append({"id": v["id"], "n": v.get("name_full") or v["name"], "scu": scu,
                    "cs": max(sizes) if sizes else None})
    return sorted(out, key=lambda s: s["n"].lower())


def build(use_cache: bool = False) -> dict:
    """Build the ledger master data.

    Args:
        use_cache: Use the local cache (development); CI always fetches fresh.

    Returns:
        ``{"places", "wares", "ships", "sizes", "wikelo", "built"}``.

    Raises:
        OSError, ValueError, KeyError: If UEX is unreachable or answers unexpectedly;
            the caller builds the page without the tab's data in that case.
    """
    raw = load_raw(use_cache)
    return {"places": places(raw["terminals"]), "wares": wares(raw["commodities"]),
            "ships": ships(raw["vehicles"]), "sizes": SIZES, "wikelo": wikelo_items(raw.get("wikelo")),
            "built": time.strftime("%d.%m.%Y")}
