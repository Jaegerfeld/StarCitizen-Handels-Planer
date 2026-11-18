# =============================================================================
# Autor:          Robert Seebauer
# Repository:     https://github.com/Jaegerfeld/StarCitizen-Handels-Planer
# KI-Unterstützung: Erstellt mit Unterstützung von Claude (Anthropic)
# Erstellt:       18.11.2026
# Geändert:       19.11.2026
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
# =============================================================================
"""Master data for the cargo ledger tab (places, commodities, ships) from UEX API 2.0."""
from __future__ import annotations

import json
import pathlib
import time
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
#: UEX API base; requests carry a tool User-Agent.
API = "https://api.uexcorp.space/2.0"
UA = {"User-Agent": "sc-tools-handels-planer (github.com/Jaegerfeld)"}
#: Local cache for ``--cache`` builds (gitignored).
CACHE = HERE / "logbuch_cache.json"
#: Container sizes in SCU that exist in game.
SIZES = [1, 2, 4, 8, 16, 24, 32]


def _get(endpoint: str) -> list[dict]:
    """Fetch one UEX endpoint and return its ``data`` list."""
    req = urllib.request.Request(f"{API}/{endpoint}", headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["data"]


def load_raw(use_cache: bool) -> dict:
    """Terminals, commodities and vehicles from UEX, or from the cache (valid one day).

    Args:
        use_cache: Read ``logbuch_cache.json`` if it is younger than one day.

    Returns:
        ``{"terminals": [...], "commodities": [...], "vehicles": [...]}``.
    """
    if use_cache and CACHE.exists() and time.time() - CACHE.stat().st_mtime < 86400:
        return json.loads(CACHE.read_text(encoding="utf-8"))
    raw = {k: _get(k) for k in ("terminals", "commodities", "vehicles")}
    if use_cache:
        CACHE.write_text(json.dumps(raw), encoding="utf-8")
    return raw


def places(terminals: list[dict]) -> list[dict]:
    """Stations, cities and outposts with a freight elevator, one entry per place.

    Args:
        terminals: UEX terminal records.

    Returns:
        Places sorted by system, body and name: id (``system|name``), name, system, body,
        largest container.
    """
    out: dict = {}
    for t in terminals:
        if not t.get("has_freight_elevator") or not t.get("is_available"):
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
        ``{"places", "wares", "ships", "sizes", "built"}``.

    Raises:
        OSError, ValueError, KeyError: If UEX is unreachable or answers unexpectedly;
            the caller builds the page without the tab's data in that case.
    """
    raw = load_raw(use_cache)
    return {"places": places(raw["terminals"]), "wares": wares(raw["commodities"]),
            "ships": ships(raw["vehicles"]), "sizes": SIZES,
            "built": time.strftime("%d.%m.%Y")}
