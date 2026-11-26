# StarCitizen Handels-Planer

Ein Standalone-HTML-Tool (offline lauffähig) für den Warenhandel in Star Citizen: **Top-Handelsrouten**, die **Handelsübersicht aller Waren** mit allen Kauf- und Verkaufsorten, Ansichten **nach Verkaufs- und Kaufort** und ein **Laderaum-Rechner** – Layout und Bedienung wie beim [Bauplan-Planer](https://github.com/Jaegerfeld/StarCitizen-Bauplan-Planer) und [Wikelo-Planer](https://github.com/Jaegerfeld/StarCitizen-Wikelo-Planer).

**🌐 Online-Version:** im SC Cockpit: https://jaegerfeld.github.io/sc-cockpit/#/fracht/handel · Einzelseite: https://jaegerfeld.github.io/StarCitizen-Handels-Planer/app.html

## Funktionen

- **Routen:** drei Tabellen – legale Bulk-Routen (Kauf-Bestand ≥ 100 SCU), höchste Margen insgesamt, illegale Routen – mit Kauf-/Verkaufsort, Preisen, Marge/SCU und, je nach gewähltem Laderaum, **Einsatz und Gewinn pro Ladung**. Warnung, wenn der Bestand am Kaufort kleiner als der Laderaum ist.
- **Alle Waren:** jede Ware mit bestem Kaufort (günstigster Ort mit Bestand), bestem Verkaufsort, Marge, Bestand; Suche, Filter (Typ, legal, System), sortierbare Spalten; Klick auf eine Zeile zeigt **alle** Kauf- und Verkaufsorte mit Preis, Bestand, Container und Stand.
- **Nach Verkaufsort / Nach Kaufort:** je Ort, was sich dort mit Gewinn verkaufen bzw. einladen lässt (Mehr-Waren-Ladung planen).
- **Fracht-Logbuch:** Buch führen, welche Ware in welchen Containern (1–32 SCU) an welcher Station oder auf welchem deiner Schiffe liegt. Schiffe mit Laderaum und Überladen (+1/3, schaltbar), Orte mit Frachtaufzug, Verschieben per Drag & Drop oder Klick, Journal mit Rückgängig, Suche über alle Orte, Lagerwert mit optionalem Einkaufspreis und bestem Verkaufsort, Umpacken in andere Containergrößen. Gespeichert im Browser und wahlweise in einer eigenen Datei (z. B. USB-Stick oder geteilter Ordner, Chrome/Edge), Export als JSON (wieder einlesbar) und XLSX.
- **Sitzungen:** liest die Spiel-Logs (`StarCitizen\LIVE` bzw. `PTU`) im Browser und zeigt je Sitzung Ende (normal/abgestürzt), letzten Server/Shard mit Region, letzten Ort und letztes Schiff – nach einem Absturz sieht man so, wo man war. Die Logs verlassen den Rechner nicht.
- **Ruf:** schätzt aus denselben Logs den Ruf je Organisation als Balken zum nächsten Rang: einmal mit dem mobiGlas abgleichen (Rang + Balken in %), danach zählt der Reiter die abgeschlossenen Missionen laut Missionsbeschreibung mit einem je Organisation gelernten Faktor dazu. Geteilte Missionen als Spanne. Der Abgleich geht auch per Screenshot der mobiGlas-Seite „Ruf“: Die Seite misst die Balken selbst – oder mit vielen Screenshots auf einmal („Screenshots abgleichen …“, Dateien oder ein ganzer Ordner): Die Seite liest die Organisation aus der Überschrift (Texterkennung, tesseract.js beim ersten Mal geladen), nimmt je Organisation das neueste Bild und zeigt vor dem Übernehmen eine Prüfliste. Je Organisation zeigt eine Übersicht alle bekannten Missionen nach der Rufstufe, ab der sie freigeschaltet sind; die Missionstexte lassen sich zuschalten (aus der Sprachdatei im geladenen Spielordner). Die Organisationen sind nach den Gilden ab Alpha 5.0 gruppiert; ohne Abgleich lassen sie sich ausblenden. „Aufs Handy …“ überträgt Rang und Balken per QR-Code aufs Handy (dort nur ansehen); das Fracht-Logbuch kann man genauso aufs Handy übernehmen. Die Ruf-Tabelle (`ruf_tabelle.json`) baut `python ruf_daten.py <Pfad zu global.ini> --sc-market` aus den Anmerkungen der deutschen Community-Übersetzung; die Rangleitern ergänzt die öffentliche Spieldaten-Schnittstelle von [sc-market.space](https://sc-market.space/missions).
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

## Eigene Daten aus Konsolen-Screenshots

Preise, die du selbst an der Handelskonsole abgelesen hast, kommen über den [SC Screenshot-Auswerter](https://github.com/Jaegerfeld/StarCitizen-Screenshot-Auswerter) herein: dessen `auswertung.json` (nach dem Prüfen heruntergeladen) in den Ordner `eigene_daten/` legen und neu bauen. Gleicher Shop + Ware + Art ersetzt die star-head-Zeile, Neues kommt dazu, Zeilen mit Status „zu prüfen“ bleiben draußen. Die Zeilen sind in der Warendetail-Tabelle als „eigene Daten“ markiert. Alternativ `python handels_planer_bauen.py --eigene <Datei|Ordner>`. Der Ordner bleibt lokal (gitignored); die Online-Version enthält nur star-head-Daten.

## Wie es funktioniert

- `handel_core.py` – die **einzige** Stelle mit der Fachlogik: Abruf (`fetch_all`), bester Kauf (günstigster Ort mit Bestand > 0, sonst günstigster) und bester Verkauf (teuerster Ort), Marge, Routen-Auswahl (`select_routes`), Ansichten nach Ort, Routen-Guide als Markdown.
- `handel_xlsx.py` – die Excel-Datei aus denselben Daten.
- `handels_planer_bauen.py` – baut die App; alle Auswertungen kommen aus `handel_core`, die App rendert nur.
- Die Daten sind **community-gepflegt** (star-head.de) und teils Tage alt („Stand“ je Preiszeile). Marge/SCU rechnet ohne Sprit, Zeit und Risiko. Vor dem Kauf im Spiel gegenprüfen.

## Quellen

- Waren, Shops, Preise: **star-head.de** (API `commodity`, `shop`, `shopitem/price`, `celestialobject`, `location`)
- Fracht-Logbuch (Orte mit Frachtaufzug, Waren, Schiffe mit Laderaum): **UEX** (API 2.0 `terminals`, `commodities`, `vehicles`)

## Lizenz

BSD-3-Clause, siehe `LICENSE`. Inoffizielles Fan-Projekt, nicht mit Cloud Imperium Games verbunden. Star Citizen® ist eine Marke von CIG.
