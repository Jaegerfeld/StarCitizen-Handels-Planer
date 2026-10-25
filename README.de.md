# StarCitizen Handels-Planer

Ein Standalone-HTML-Tool (offline lauffähig) für den Warenhandel in Star Citizen: **Top-Handelsrouten**, die **Handelsübersicht aller Waren** mit allen Kauf- und Verkaufsorten, Ansichten **nach Verkaufs- und Kaufort** und ein **Laderaum-Rechner** – Layout und Bedienung wie beim [Bauplan-Planer](https://github.com/Jaegerfeld/StarCitizen-Bauplan-Planer) und [Wikelo-Planer](https://github.com/Jaegerfeld/StarCitizen-Wikelo-Planer).

**🌐 Online-Version:** https://jaegerfeld.github.io/StarCitizen-Handels-Planer/

## Funktionen

- **Routen:** drei Tabellen – legale Bulk-Routen (Kauf-Bestand ≥ 100 SCU), höchste Margen insgesamt, illegale Routen – mit Kauf-/Verkaufsort, Preisen, Marge/SCU und, je nach gewähltem Laderaum, **Einsatz und Gewinn pro Ladung**. Warnung, wenn der Bestand am Kaufort kleiner als der Laderaum ist.
- **Alle Waren:** jede Ware mit bestem Kaufort (günstigster Ort mit Bestand), bestem Verkaufsort, Marge, Bestand; Suche, Filter (Typ, legal, System), sortierbare Spalten; Klick auf eine Zeile zeigt **alle** Kauf- und Verkaufsorte mit Preis, Bestand, Container und Stand.
- **Nach Verkaufsort / Nach Kaufort:** je Ort, was sich dort mit Gewinn verkaufen bzw. einladen lässt (Mehr-Waren-Ladung planen).
- **Laderaum-Rechner:** Cutlass Black (46), Freelancer (66), Mercury Star Runner (114) oder eigener SCU-Wert.
- Zweisprachig (DE/EN), Hell/Dunkel, Auswahl bleibt im Browser gespeichert.
- **Täglich frische Daten:** die Online-Version wird jeden Tag neu gebaut (GitHub Actions, 05:00 UTC). Der Knopf „Neuesten Stand laden (GitHub)“ holt die `data.json` dieses Builds von GitHub Pages – auch aus einer Offline-Kopie heraus – statt star-head direkt abzufragen. Rechtsklick auf den Knopf setzt auf die eingebauten Build-Daten zurück.
- **Downloads** (Online-Version): `SC_Waren_Handelsuebersicht.xlsx` (Übersicht · Nach Verkaufsort · Nach Kaufort · Alle Preise · Info), `SC_Waren_Top_Handelsrouten.md`, `data.json`.

## Nutzung

- **Einfach benutzen:** die Online-Version oben öffnen oder `SC_Handels_Planer.html` doppelklicken (läuft komplett offline).
- **Mit frischen Daten neu bauen:** `Handels_Planer_aktualisieren.bat` (Windows) / `.sh` (Linux) / `.command` (macOS) starten, oder:

  ```bash
  python handels_planer_bauen.py          # HTML + data.json + Routen-Markdown
  python handels_planer_bauen.py --xlsx   # zusätzlich die Excel-Datei (braucht openpyxl)
  python handels_planer_bauen.py --cache  # Rohdaten aus handel_cache.json (zum Entwickeln, schont star-head)
  ```

  Das zieht Waren, Shops und Preise von star-head.de (rund 280 Abfragen, 10–30 s) und backt sie in `SC_Handels_Planer.html`. Es wird nur die Python-Standardbibliothek benötigt; `openpyxl` nur für `--xlsx`.

## Wie es funktioniert

- `handel_core.py` – die **einzige** Stelle mit der Fachlogik: Abruf (`fetch_all`), bester Kauf (günstigster Ort mit Bestand > 0, sonst günstigster) und bester Verkauf (teuerster Ort), Marge, Routen-Auswahl (`select_routes`), Ansichten nach Ort, Routen-Guide als Markdown.
- `handel_xlsx.py` – die Excel-Datei aus denselben Daten.
- `handels_planer_bauen.py` – baut die App; alle Auswertungen kommen aus `handel_core`, die App rendert nur.
- Die Daten sind **community-gepflegt** (star-head.de) und teils Tage alt („Stand“ je Preiszeile). Marge/SCU rechnet ohne Sprit, Zeit und Risiko. Vor dem Kauf im Spiel gegenprüfen.

## Quellen

- Waren, Shops, Preise: **star-head.de** (API `commodity`, `shop`, `shopitem/price`, `celestialobject`, `location`)

## Lizenz

BSD-3-Clause, siehe `LICENSE`. Inoffizielles Fan-Projekt, nicht mit Cloud Imperium Games verbunden. Star Citizen® ist eine Marke von CIG.
