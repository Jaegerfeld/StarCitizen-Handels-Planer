# Changelog

Alle nennenswerten Änderungen an diesem Projekt. Format nach [Keep a Changelog](https://keepachangelog.com/de/1.0.0/), Versionierung nach [SemVer](https://semver.org/lang/de/).

## [1.1.0] – 2026-10-25

### Geändert
- **Nach Verkaufsort / Nach Kaufort** sind flache, sortierbare Tabellen (eine Zeile je Ort und Ware, Ort als erste Spalte) statt aufklappbarer Gruppen – damit lässt sich nach Marge, Stand und Ort sortieren.
- Neuer Filter **Verkaufsort / Kaufort** (Dropdown) neben Suche und System; Zeilenzähler.

## [1.0.0] – 2026-10-25

### Hinzugefügt
- Erste Version des **SC Handels-Planers** (Standalone-HTML, offline lauffähig), gebaut aus den star-head-Daten.
- **Routen:** legale Bulk-Routen (Kauf-Bestand ≥ 100 SCU), höchste Margen insgesamt, illegale Routen – mit Einsatz und Gewinn pro Ladung für den gewählten Laderaum (Cutlass Black 46, Freelancer 66, Mercury Star Runner 114 SCU oder eigener Wert) und Warnung bei Bestand < Laderaum.
- **Alle Waren:** bester Kauf-/Verkaufsort, Marge, Bestand; Suche, Filter, Sortierung; Detail je Ware mit allen Kauf- und Verkaufsorten.
- **Nach Verkaufsort / Nach Kaufort:** gruppierte Ansichten wie in der Excel-Datei.
- **Täglicher Build** per GitHub Actions (05:00 UTC); Knopf „Neuesten Stand laden (GitHub)“ lädt die `data.json` des letzten Builds von Pages statt star-head direkt.
- **Downloads** in der Online-Version: Excel (`SC_Waren_Handelsuebersicht.xlsx`), Routen-Markdown, `data.json`.
- `handel_core.py` als einzige Stelle der Fachlogik; die lokale Pipeline `update_starhead.py` nutzt dieselben Funktionen (Vergleichslauf 25.10.2026: Routen-Tabellen und Orts-Ansichten identisch).
