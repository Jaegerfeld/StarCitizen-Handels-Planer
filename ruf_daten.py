# =============================================================================
# Autor:          Robert Seebauer
# Repository:     https://github.com/Jaegerfeld/StarCitizen-Handels-Planer
# KI-Unterstützung: Erstellt mit Unterstützung von Claude (Anthropic)
# Erstellt:       20.11.2026
# Geändert:       20.11.2026
# Lizenz:         BSD-3-Clause (siehe LICENSE)
#
# Fachliche Funktion:
#   Baut die Ruf-Tabelle für den Reiter „Ruf“: je Missionstitel die Organisation
#   und die angegebenen Ruf-Punkte, je Organisation die Rangleiter mit den
#   Schwellen. Quelle sind die Anmerkungen der deutschen Community-Übersetzung
#   in den Missionsbeschreibungen von global.ini („# Ruf: 100 XP (Foxwell
#   Enforcement)“, „# Min. Reputation: Auftragnehmer Senior (5.800 XP)“).
#   Übernommen werden nur Zahlen, Titel und Rangnamen, keine Texte. Titel und
#   Beschreibung werden über den Schlüssel exakt gepaart (…_Title_001 ↔
#   …_Desc_001, …_Title_M_001 ↔ …_Desc_M_001), nicht über einen Präfix-Abgleich.
#   Je Titel steht auch der Schlüssel der Beschreibung (klein geschrieben): Der
#   Reiter „Ruf“ liest den Missionstext damit zur Laufzeit aus der global.ini des
#   Spielers; die Texte selbst stehen nicht in der Tabelle.
#   Rangleitern: Organisationen mit „Auftragnehmer …“-Rängen bekommen die volle
#   Auftragnehmer-Leiter, auch wenn ihre Missionen nur einzelne Stufen nennen.
#   Aufruf: python ruf_daten.py "<…\StarCitizen\LIVE\data\Localization\german_(germany)\global.ini>"
#   schreibt ruf_tabelle.json; der Seitenbau bettet sie ein.
# =============================================================================
"""Reputation table (mission title → organisation, stated XP; rank ladders) from an annotated global.ini."""
import datetime
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
#: Output, embedded by handels_planer_bauen.py.
OUT = HERE / "ruf_tabelle.json"

#: "# Ruf: 100 XP (Foxwell Enforcement)" or "# Ruf: 100 / 150 XP (…)".
RE_RUF = re.compile(r"Ruf: ([\d.]+)(?: / ([\d.]+))? XP \(([^)]+)\)")
#: "# Min. Reputation: Auftragnehmer Senior (5.800 XP)", also "Min. / Max. Reputation: …".
#: The rank name stops at "(" and at the escaped line break "\n" of the ini value.
RE_RANK = re.compile(r"(Min\.|Max\.|Min\. / Max\.) Reputation: ((?:(?!\\n)[^(])+?) \(([\d.]+) XP\)")
#: Markup of the translation inside titles: "<EM4>[BP]</EM4>", "[BP]*".
RE_TAGS = re.compile(r"<[^>]+>|\[BP\]\*?|\*")
#: The last "_title" of a key; the description key has "_desc" in its place
#: (…_Title_001 ↔ …_Desc_001, …_Title_M_001 ↔ …_Desc_M_001).
RE_KEY = re.compile(r"^(.*)_title(.*)$", re.I)


def norm_title(title: str) -> str:
    """Title as it is compared with the log: markup removed, spaces collapsed.

    Args:
        title: Title from global.ini or from a log notification.

    Returns:
        The normalised title.
    """
    return re.sub(r"\s+", " ", RE_TAGS.sub(" ", title)).strip()


def xp(s: str) -> int:
    """Number with German thousands dots ("5.800") as int."""
    return int(s.replace(".", ""))


def read_ini(path: pathlib.Path) -> dict[str, str]:
    """Key → value of a global.ini (key without the ",P" suffix, lower case).

    Args:
        path: Path to global.ini.

    Returns:
        Mapping of lower-case keys to values.
    """
    kv = {}
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        for line in f:
            if "=" in line:
                k, v = line.rstrip("\n").split("=", 1)
                kv[k.split(",")[0].lower()] = v
    return kv


def build(path: pathlib.Path) -> dict:
    """Build the reputation table.

    Args:
        path: Path to the annotated global.ini.

    Returns:
        ``{"stand", "quelle", "missions": {title: [[org, xp_lo, xp_hi, min_rank_xp|None, desc_key], …]},
        "ladders": {org: [[xp, rank], …]}}``.
    """
    kv = read_ini(path)
    missions: dict[str, set] = {}
    ladders: dict[str, set] = {}
    for key, val in kv.items():
        m = RE_KEY.match(key)
        if not m:
            continue
        dkey = f"{m.group(1)}_desc{m.group(2)}"
        desc = kv.get(dkey)
        if not desc or "Ruf:" not in desc:
            continue
        title = norm_title(val)
        ranks = [(kind, name.strip(), xp(x)) for kind, name, x in RE_RANK.findall(desc)]
        min_xp = next((x for kind, _, x in ranks if kind.startswith("Min")), None)
        for lo, hi, org in RE_RUF.findall(desc):
            org = org.strip()
            missions.setdefault(title, set()).add((org, xp(lo), xp(hi or lo), min_xp, dkey))
            for _, name, x in ranks:
                ladders.setdefault(org, set()).add((x, name))
    # Contractor ladder: all "Auftragnehmer …" ranks (and Neutral) seen anywhere; orgs using it get all of it.
    contractor = {(x, n) for v in ladders.values() for x, n in v if n == "Neutral" or n.startswith("Auftragnehmer")}
    for org, v in ladders.items():
        if any(n.startswith("Auftragnehmer") for _, n in v):
            # Only the contractor career; other careers of the same org (Eckhart: "Sicherheitsagent") would mix up the order
            ladders[org] = set(contractor)
    return {
        "stand": datetime.date.today().isoformat(),
        "quelle": "Anmerkungen der deutschen Community-Übersetzung (global.ini): nur Zahlen, Titel, Rangnamen",
        "missions": {t: sorted(map(list, v), key=lambda e: (e[0], e[1])) for t, v in sorted(missions.items())},
        "ladders": {o: sorted(map(list, v)) for o, v in sorted(ladders.items())},
    }


def main(argv: list[str]) -> int:
    """Write ruf_tabelle.json from the global.ini given on the command line.

    Args:
        argv: Command line arguments without the program name.

    Returns:
        Exit code: 0 on success, 2 without a usable path.
    """
    if not argv or not pathlib.Path(argv[0]).is_file():
        print("Aufruf: python ruf_daten.py <Pfad zu global.ini>", file=sys.stderr)
        return 2
    data = build(pathlib.Path(argv[0]))
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"Geschrieben: {OUT.name} – {len(data['missions'])} Missionstitel, {len(data['ladders'])} Organisationen")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
