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
#   Rangleitern von sc-market.space (Schalter --sc-market): Die öffentliche
#   Schnittstelle von sc-market.space nennt alle Ruf-Leitern des Spiels mit
#   Schwellen und je Mission die Leiter („Scope“), auf die ihr Ruf geht. Eine
#   Organisation der Tabelle bekommt die Leiter, auf die die Mehrheit ihrer
#   Missionen geht (ohne den persönlichen Ruf bei Einzelpersonen); passen die
#   Rangnamen aus den Anmerkungen zu einer ihrer Leitern (Ling Family Hauling:
#   „Anwärter“ = Frachtleiter), gilt diese. Ohne klare Mehrheit (Northrock)
#   bleibt die Leiter offen. Organisationen, die nur sc-market kennt, kommen
#   nicht hinzu. Im mobiGlas
#   zeigt jede Organisation eine Leiter (von Robert am 20.11.2026 geprüft).
#   Deutsche Rangnamen kommen aus den RepStanding_*-Schlüsseln der global.ini,
#   sonst bleibt der englische Name. Namen aus den Anmerkungen der Übersetzung
#   haben Vorrang; sc-market ergänzt fehlende Stufen und Leitern.
#   Aufruf: python ruf_daten.py "<…\StarCitizen\LIVE\data\Localization\german_(germany)\global.ini>" [--sc-market]
#   schreibt ruf_tabelle.json; der Seitenbau bettet sie ein.
# =============================================================================
"""Reputation table (mission title → organisation, stated XP; rank ladders) from an annotated global.ini."""
import collections
import datetime
import json
import pathlib
import re
import sys
import time
import urllib.request

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

#: Public game-data interface of sc-market.space.
SCM_API = "https://api.sc-market.space/api/v2/game-data"
#: Scopes that are no rank ladder of an organisation (personal affinity, NPC trust).
SCM_SKIP = {"reputationscope_affinity", "reputationscope_npc_reliability", "reputationscope_npc_fired"}
#: The contractor ladder; its German names come from the annotations of the translation.
SCM_CONTRACTOR = "factionreputationscope"
#: Recco Battaglia's own ladder; annotated German names are kept where the threshold matches.
SCM_BATTAGLIA = "missionproviderreputationscope_battaglia"
#: German rank names per scope: global.ini keys in ladder order (without "Not Eligible").
SCM_DE = {
    "reputationscope_hauling": [f"repstanding_transportguild_rank{i}" for i in range(7)],
    "reputationscope_bounty_bountyhuntersguild": [
        f"repstanding_bounty_{k}_name" for k in
        ("applicant", "probation", "junior", "midlevel", "senior", "masterbountyhunter", "legendarybountyhunter")],
    "reputationscope_wikelo": [f"repstanding_barter_rank{i}_name" for i in range(3)],
}


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


def scm_get(path: str, **params) -> object:
    """One GET request to the sc-market game-data interface.

    Args:
        path: Path below ``SCM_API``.
        **params: Query parameters.

    Returns:
        The decoded JSON answer.
    """
    query = "&".join(f"{k}={v}" for k, v in params.items())
    req = urllib.request.Request(f"{SCM_API}{path}{'?' + query if query else ''}",
                                 headers={"User-Agent": "StarCitizen-Handels-Planer"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def fetch_scm() -> dict:
    """Rank ladders, missions (organisation and scope only) and game version from sc-market.space.

    Returns:
        ``{"version": str, "ranks": [...], "missions": [[org, scope], …]}``.
    """
    versions = scm_get("/versions")
    version = next((v["version_number"] for v in versions if v.get("is_active")), "?")
    ranks = scm_get("/missions/reputation-ranks")["ranks"]
    missions, page = [], 1
    while True:
        d = scm_get("/missions/search", page_size=100, page=page)
        missions += [[m.get("reputation_reward_faction") or "", m.get("reward_scope") or ""] for m in d["missions"]]
        if not d["missions"] or len(missions) >= d["total"]:
            break
        page += 1
        time.sleep(0.3)   # be gentle with a free service
    return {"version": version, "ranks": ranks, "missions": missions}


def de_name(raw: str) -> str:
    """Rank name from global.ini as shown: escaped line break as space, all-caps names in title case."""
    name = re.sub(r"\\n", " ", raw).strip()
    return name.title() if name.isupper() else name


def scm_ladders(scm: dict, kv: dict[str, str], seen: dict[str, set], orgs: set[str]) -> tuple[dict, dict]:
    """One ladder per organisation from the sc-market data.

    Args:
        scm: Result of :func:`fetch_scm`.
        kv: The global.ini (German rank names).
        seen: Ladders already read from the annotations (org → {(xp, name)}).
        orgs: Organisations of the table; others are left out.

    Returns:
        ``(ladders, scopes)``: org → [(xp, name), …] and org → chosen scope.
    """
    by_scope = collections.defaultdict(list)
    for r in scm["ranks"]:
        if r["threshold"] >= 0:   # "Not Eligible" (negative) is no rank of the ladder
            by_scope[r["scope_code"]].append((r["threshold"], r["standing_display_name"]))
    for code, ranks in by_scope.items():
        ranks.sort()
        keys = SCM_DE.get(code)
        if keys and len(keys) == len(ranks):
            by_scope[code] = [(x, de_name(kv[k]) if kv.get(k) else n) for (x, n), k in zip(ranks, keys, strict=True)]
    count = collections.defaultdict(collections.Counter)
    for org, scope in scm["missions"]:
        if org in orgs and scope and scope not in SCM_SKIP and scope in by_scope:
            count[org][scope] += 1
    ladders, scopes = {}, {}
    for org, c in count.items():
        names = {n.casefold() for _, n in seen.get(org, ())}
        # A scope whose rank names match the annotations wins; otherwise the scope of most missions
        scope = next((s for s, _ in c.most_common() if names & {n.casefold() for _, n in by_scope[s]}), None)
        if scope is None:
            top, n = c.most_common(1)[0]
            if 2 * n <= sum(c.values()):
                continue   # no clear majority: ladder stays unknown
            scope = top
        scopes[org] = scope
        ladders[org] = by_scope[scope]
    return ladders, scopes


def build(path: pathlib.Path, scm: dict | None = None) -> dict:
    """Build the reputation table.

    Args:
        path: Path to the annotated global.ini.
        scm: Optional sc-market data (:func:`fetch_scm`) that completes the rank ladders.

    Returns:
        ``{"stand", "quelle", "missions": {title: [[org, xp_lo, xp_hi, min_rank_xp|None, desc_key], …]},
        "ladders": {org: [[xp, rank], …]}, "scopes": {org: scope}}``.
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
        for lo, hi, orgs in RE_RUF.findall(desc):
            # Some missions name two organisations at once ("Headhunters, Citizens For Prosperity")
            for org in (o.strip() for o in orgs.split(",") if o.strip()):
                missions.setdefault(title, set()).add((org, xp(lo), xp(hi or lo), min_xp, dkey))
                for _, name, x in ranks:
                    ladders.setdefault(org, set()).add((x, name))
    # Contractor ladder: all "Auftragnehmer …" ranks (and Neutral) seen anywhere; orgs using it get all of it.
    contractor = {(x, n) for v in ladders.values() for x, n in v if n == "Neutral" or n.startswith("Auftragnehmer")}
    for org, v in ladders.items():
        if any(n.startswith("Auftragnehmer") for _, n in v):
            # Only the contractor career; other careers of the same org (Eckhart: "Sicherheitsagent") would mix up the order
            ladders[org] = set(contractor)
    quelle = "Anmerkungen der deutschen Community-Übersetzung (global.ini): nur Zahlen, Titel, Rangnamen"
    scopes = {}
    if scm:
        orgs = {e[0] for v in missions.values() for e in v} | set(ladders)
        extra, scopes = scm_ladders(scm, kv, ladders, orgs)
        for org, lad in extra.items():
            if scopes[org] == SCM_CONTRACTOR:
                # Same thresholds; the German names come from the annotations
                if contractor:
                    ladders[org] = set(contractor)
            elif scopes[org] == SCM_BATTAGLIA:
                have = {x: n for x, n in ladders.get(org, ())}
                ladders[org] = {(x, have.get(x, n)) for x, n in lad}
            else:
                ladders[org] = set(lad)
        quelle += f"; Rangleitern ergänzt aus sc-market.space ({scm['version']})"
    return {
        "stand": datetime.date.today().isoformat(),
        "quelle": quelle,
        "missions": {t: sorted(map(list, v), key=lambda e: (e[0], e[1], e[2], e[4])) for t, v in sorted(missions.items())},
        "ladders": {o: sorted(map(list, v)) for o, v in sorted(ladders.items())},
        "scopes": dict(sorted(scopes.items())),
    }


def main(argv: list[str]) -> int:
    """Write ruf_tabelle.json from the global.ini given on the command line.

    Args:
        argv: Command line arguments without the program name.

    Returns:
        Exit code: 0 on success, 2 without a usable path.
    """
    use_scm = "--sc-market" in argv
    argv = [a for a in argv if a != "--sc-market"]
    if not argv or not pathlib.Path(argv[0]).is_file():
        print("Aufruf: python ruf_daten.py <Pfad zu global.ini> [--sc-market]", file=sys.stderr)
        return 2
    data = build(pathlib.Path(argv[0]), fetch_scm() if use_scm else None)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"Geschrieben: {OUT.name} – {len(data['missions'])} Missionstitel, {len(data['ladders'])} Organisationen")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
