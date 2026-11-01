# Changelog

Alle nennenswerten Änderungen an diesem Projekt. Format nach [Keep a Changelog](https://keepachangelog.com/de/1.0.0/), Versionierung nach [SemVer](https://semver.org/lang/de/).

## [1.5.0] – 2026-11-01

### Hinzugefügt
- **Gemeinsames Design** aller vier SC-Tools in `sc_design.py` (in allen vier Repos identisch, wie `kopfzeile.py`): Farben für Hell und Dunkel, Schriften (Rajdhani für Überschriften, Exo 2 für Text), Knöpfe, Eingabefelder, Fokusrahmen, Lösch-Knopf-Stil.
- **Handy und Tablet:** Auf schmalen Bildschirmen (unter 920 px) zeigen Tools mit mehreren Bereichen oben Reiter statt nebeneinanderliegender Spalten; der Hauptinhalt kommt zuerst. Auf Touch-Geräten sind Knöpfe, Felder und Häkchen mindestens 44 px groß. Kein seitliches Scrollen mehr bei 390 px Breite; breite Tabellen scrollen nur in ihrem Rahmen.
- Kopfzeile am Handy kompakter: Einzeiler auf zwei Zeilen gekürzt, „Weitere Tools“ klappt auf.

### Behoben
- Die Laderaum-Gruppe (Schiff, SCU) bricht auf schmalen Bildschirmen um; vorher scrollte die Seite bei Handybreite seitlich.

## [1.4.0] – 2026-11-01

### Hinzugefügt
- **„Was ist neu?“** in der Kopfzeile: zeigt dieses Changelog in einem Dialog, mit der aktuellen Version im Titel und einem Link auf die Datei auf GitHub. Der Text wird beim Bauen aus `CHANGELOG.md` übernommen und funktioniert auch in der Offline-Kopie. Schließen per Esc, Klick daneben oder ✕.

### Geändert
- **Einheitliche Kopfzeile** in allen vier SC-Tools (Bauplan-, Wikelo-, Handels-Planer, Screenshot-Auswerter): Kicker, Titel mit Version, Einzeiler, Aktionszeile (Sprache DE | EN mit sichtbarer aktiver Sprache, Hell/Dunkel, „Was ist neu?“, Tool-Aktionen, „Neuesten Stand laden“), eigene Zeile „Weitere Tools“ mit denselben Zielen in derselben Reihenfolge, Datenzeile. Quelle ist `kopfzeile.py`, in allen vier Repos identisch.

## [1.3.0] – 2026-10-28

### Hinzugefügt
- **Eigene Daten:** Exporte des [SC Screenshot-Auswerters](https://github.com/Jaegerfeld/StarCitizen-Screenshot-Auswerter) (`auswertung.json`) im Ordner `eigene_daten/` – oder per `--eigene <Datei|Ordner>` – werden beim Bauen in die star-head-Daten eingemischt: gleicher Shop + Ware + Art wird ersetzt, Neues kommt dazu, Zeilen „zu prüfen“ bleiben draußen. Routen, Warenübersicht und Orts-Ansichten rechnen damit; in der Warendetail-Tabelle und der Statuszeile sind diese Zeilen als „eigene Daten“ markiert.

## [1.2.0] – 2026-10-25

### Geändert
- **Nach Verkaufsort / Nach Kaufort:** Systeme als **Mehrfachauswahl** (Kästchen Stanton · Pyro · Nyx) statt Dropdown – z. B. Pyro und Stanton zusammen. Nichts angehakt = alle Systeme.

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
