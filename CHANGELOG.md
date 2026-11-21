# Changelog

Alle nennenswerten Änderungen an diesem Projekt. Format nach [Keep a Changelog](https://keepachangelog.com/de/1.0.0/), Versionierung nach [SemVer](https://semver.org/lang/de/).

## [1.19.1] – 2026-11-21

### Behoben
- **Ruf: doppelte Karten aus alten Namen der Gildenliste.** 1.13.0–1.15.0 zeigten zusätzlich die Namen aus der fremden Gildenliste („Covalex Independent Haulers“, „Rayari Inc.“, „Wikelo“). Seit 1.15.1 gibt es sie nicht mehr, aber Abgleiche oder Sterne unter diesen Namen blieben im Browser gespeichert und erschienen als eigene Karte. Jetzt werden sie beim Laden der Organisation der Ruf-Tabelle zugeschlagen (Covalex, Rayari Incorporated, Wikelo Emporium); das Spiel kennt nur eine Covalex (Log: CovalexIndependentContractors, mobiGlas: COVALEX).
- Die einmaligen Hinweise zum gespeicherten Stand (zusammengeführte Namen, umgerechnete Abgleiche) erscheinen jetzt gleich beim ersten Öffnen und zusammen in der Statuszeile.

## [1.19.0] – 2026-11-21

### Behoben
- **Ruf: Lesart der mobiGlas-Kacheln korrigiert – die hervorgehobene Kachel ist der aktuelle Rang**, ihr Balken der Weg zum nächsten; volle Balken sind durchlaufene Ränge. Bisher galt sie als nächster Rang, alle Stände lagen damit eine Stufe zu niedrig. Im Spiel bestätigt (21.11.2026): Bei Foxwell ist „Erfahren“ hervorgehoben, und der Auftrag „Fuel Container Demolition“ (Mindeststufe Erfahren) wird angeboten. Die neue Lesart erklärt auch, warum bei Organisationen mit erledigten Missionen „Neutral“ mit Teilbalken hervorgehoben ist, und den halb vollen Balken bei Eckhart.
- **Bisherige Abgleiche werden einmal automatisch umgerechnet**: eine Stufe höher, mit demselben Anteil im Band. Ein Wert genau auf der ersten Schwelle bleibt (nicht eindeutig). Genauer ist ein neuer Abgleich über „Screenshots abgleichen …“.
- **Startfaktor 1,0 statt 0,55** (Ruf wie in der Missionsbeschreibung angegeben). Die 0,55 kamen aus der falschen Lesart; nach der richtigen ergeben die beiden Foxwell-Messungen 1,2 und 1,7 (auf 1–2 Pixel genau). Der je Organisation gelernte Faktor löst den Startwert ab.
- Abgleich-Formular: „Rang (hervorgehobene Kachel)“ und „Balken dieser Kachel in %“ statt „Erreichter Rang“ / „Balken der nächsten Stufe“.

## [1.18.0] – 2026-11-21

### Hinzugefügt
- **Ruf: Rang-Abzeichen.** Jede Karte zeigt die Rangleiter als Reihe von Abzeichen wie die Kacheln im mobiGlas: erreichte Stufen gefüllt, die aktuelle umrandet, die nächste gestrichelt, spätere blass. Neben dem Rangnamen steht das Abzeichen der aktuellen Stufe. Ohne Abgleich ist die Reihe grau und zeigt die Leiter. Auch die Handy-Ansicht zeigt die Abzeichen.
  - Eigene Zeichnung für dieses Werkzeug, keine Grafiken aus dem Spiel: Schild mit 1–3 Sternen, ab der vierten Stufe mit Flügeln, darüber ein oder zwei Winkel, ab der siebten eine Krone. Die Form zeigt die Position in der Leiter, gleich für alle Organisationen.
  - In der Reihe entfällt das Wort, das die meisten Stufen teilen („Senior“ statt „Auftragnehmer Senior“); der volle Name steht im Tooltip und beim aktuellen Rang.

### Behoben
- **Ruf: Klick auf einen Missionstitel tat still nichts**, wenn die Missionstexte ausgeschaltet sind oder die Sprachdatei des Spiels fehlt (z. B. in einer lokal geöffneten Kopie des Planers, die einen eigenen Speicher hat). Jetzt sagt ein Fenster, was fehlt: Schalter „Missionstexte anzeigen“ einschalten bzw. den ganzen Ordner LIVE laden.
- **Grauer Schalter „Missionstexte anzeigen“ ohne Begründung:** Ohne Sprachdatei ist er gesperrt; die Erklärung erschien bisher nur, wenn er vorher an war. Jetzt zeigt ein Klick auf den grauen Schalter den Grund (und ein Tooltip nennt ihn).

## [1.17.0] – 2026-11-21

### Hinzugefügt
- **Ruf: „Screenshots abgleichen …“ – viele Screenshots auf einmal.** Statt jede Organisation einzeln anzuklicken: Screenshots wählen (Mehrfachauswahl), einen ganzen Ordner wählen oder Bilder in das Fenster ziehen. Die Seite erkennt je Bild die Organisation aus der Überschrift, den erreichten Rang und den Balken. Je Organisation zählt das neueste Bild; ältere und schon übernommene Bilder werden nicht übernommen, andere Bilder übersprungen.
  - Vor dem Übernehmen steht alles in einer Prüfliste: je Zeile ein Haken, die erkannte Organisation (änderbar), Rang → nächste Stufe mit Prozent und XP, Zeitpunkt. Der Knopf nennt, wie viele Abgleiche übernommen werden.
  - Texterkennung: tesseract.js 5.1.1 (Apache-2.0), wird erst beim ersten Mehrfach-Abgleich von jsDelivr geladen (feste Version mit Prüfsumme). Ohne Internet wählt man die Organisation je Zeile von Hand. Die Bilder verlassen den Rechner nicht.
  - Der Einzel-Abgleich je Organisation bleibt für die Feinjustierung.
  - Geprüft an 20 Screenshots aus Roberts mobiGlas: alle Organisationen und Ränge richtig erkannt.

### Geändert
- **Screenshot-Messung robuster.** Die hervorgehobene Kachel wird an den festen Kachelplätzen gesucht, als die Kachel, die klar grüner ist als alle anderen. Das mobiGlas ist durchscheinend; ein heller Hintergrund färbt alle Kacheln, ein fester Schwellwert fand die Kachel deshalb bisher nur in 9 von 20 Testbildern. Ist die Kachel nur knapp zu erkennen, weist die Seite darauf hin.
- Leitern, die im mobiGlas mit der Kachel „Nicht berechtigt“ beginnen (Fracht, Sicherheit, Kopfgeld, Notfall), werden beim Zählen der Kacheln berücksichtigt.
- Ist im mobiGlas noch die erste Stufe hervorgehoben (z. B. „Neutral“ mit Teilbalken), zählt der Abgleich den Startwert der Leiter und sagt das.

### Behoben
- **Rangleitern nach Roberts mobiGlas (21.11.2026):** Ling Family Hauling und Northrock Service Group haben die Auftragnehmer-Leiter, Eckhart Security die Sicherheitsleiter (Sicherheitsagent …), Shubin Interstellar endet bei „Auftragnehmer Leitend“. Neu: Civilian Defense Force mit der Ersthelfer-Leiter. Die Mehrheitsregel aus 1.16.0 gilt nur noch für Organisationen ohne Screenshot.
- Rangnamen mit Bindestrich und kleinen Wörtern richtig geschrieben („Senior-Gildenmitglied“, „Ersthelfer in Ausbildung“).

## [1.16.0] – 2026-11-20

### Hinzugefügt
- **Ruf: Rangleitern von sc-market.space.** Bisher kannte der Reiter nur die Stufen, die in Missionsbeschreibungen als Mindest- oder Höchststufe vorkommen; viele Organisationen bekamen deshalb die Auftragnehmer-Stufen nur angenommen. Jetzt ergänzt `ruf_daten.py --sc-market` die Leitern aus der öffentlichen Spieldaten-Schnittstelle von sc-market.space (Stand 4.10-LIVE, Spieldaten vom 14.11.2026). 21 von 22 Organisationen der Ruf-Tabelle haben damit eine belegte Leiter:
  - **Auftragnehmer-Leiter bestätigt** für Adagio, InterSec, FTL Courier, Dead Saints, Highpoint, United Wayfarers Club, neu belegt für Vaughn, Hockrow Agency und Rayari.
  - **Frachtleiter** (Anwärter 0 · Neuling 50 · Junior 250 · Mitglied 5.250 · Erfahren 27.750 · Senior 77.750 · Meister 237.750) für Covalex, Red Wind Linehaul und Ling Family Hauling.
  - **Recco Battaglia** vollständig bis Prestige 3 (neu: Prestige 1 bei 10.800, Prestige 2 bei 30.000).
  - **Bounty Hunters Guild** (Bewerber bis Gildenverwalter, 480.000) und **Wikelo** (Neuer Kunde · Sehr guter Kunde 340 · Bester Kunde 999).
  - Deutsche Rangnamen aus der Sprachdatei des Spiels; Northrock Service Group bleibt ohne Leiter (ihre Missionen verteilen sich ohne klare Mehrheit auf mehrere Laufbahnen).
- Je Organisation zeigt das mobiGlas eine Leiter (von Robert geprüft); bei Organisationen mit Missionen in mehreren Laufbahnen (z. B. Covalex: Fracht und Auftragnehmer) gilt die Leiter, auf die die meisten Missionen gehen.

### Geändert
- Die Ruf-Tabelle wird reproduzierbar gebaut (feste Reihenfolge bei gleichen Missionstiteln).

## [1.15.1] – 2026-11-20

### Behoben
- **Ruf: keine doppelten Organisationen mehr.** Covalex, Rayari und Wikelo hießen in der Gildenliste anders als in der Ruf-Tabelle und konnten doppelt erscheinen; es gelten jetzt die Namen der Tabelle.
- **Alle Organisationen der Ruf-Tabelle werden gezeigt**, auch ohne Rangleiter und ohne Mission im Log (neu sichtbar z. B. Vaughn, Red Wind Linehaul) – jetzt 23.
- **Missionen mit zwei Auftraggebern** („Headhunters, Citizens For Prosperity“) werden in der Ruf-Tabelle getrennt und zählen für beide Organisationen.

## [1.15.0] – 2026-11-20

### Hinzugefügt
- **„Aufs Handy …“ in den Reitern „Ruf“ und „Fracht-Logbuch“.** Auf dem Handy läuft kein Star Citizen, es gibt dort weder Logs noch Screenshots. Der PC zeigt deshalb einen QR-Code (und den Link zum Kopieren) mit dem aktuellen Stand; mit der Handy-Kamera scannen öffnet die Online-Seite mit diesem Stand.
  - **Ruf:** Rang und Balken der abgeglichenen Organisationen, nach Gilden; das Handy zeigt den Stand nur an („Stand vom PC · Zeitpunkt · nur ansehen“), bis man die Ansicht beendet.
  - **Fracht-Logbuch:** Schiffe und Frachtposten; das Handy übernimmt sie als sein Logbuch (fragt vorher, wenn dort schon etwas steht; Rückgängig möglich).
  - Der Stand steckt komprimiert hinter dem „#“ des Links; dieser Teil wird nie an einen Server geschickt und nach dem Öffnen aus der Adresszeile entfernt. Ist er für einen QR-Code zu groß, bleibt der Link zum Selbstschicken.
  - QR-Code: qrcode-generator 1.4.4 (Kazuhiko Arase, MIT), erst beim Öffnen des Dialogs von jsDelivr geladen (feste Version mit Prüfsumme); offline gibt es nur den Link.

## [1.14.0] – 2026-11-20

### Geändert
- **Ruf: kompakter.** Die Karten der Organisationen stehen auf breiten Bildschirmen nebeneinander (zwei je Reihe, bei sehr breiten auch mehr), auf schmalen untereinander.
- **Gilden einklappbar:** Ein Klick auf die Gilden-Überschrift klappt sie ein oder aus; der Zustand bleibt im Browser. Die Überschrift zeigt, wie viele Organisationen abgeglichen sind.
- Der Abgleich-Knopf ist auf allen Karten gleich gewichtet (vorher war er bei jeder Karte ohne Abgleich hervorgehoben).

## [1.13.0] – 2026-11-20

### Geändert
- **Ruf: nach Gilden sortiert, alle Organisationen von Anfang an.** Ab Alpha 5.0 sind die Auftraggeber in Gilden organisiert. Der Reiter gruppiert sie danach: Transport Guild, Resources Guild, Mercenary Guild, Bounty Hunter Guild, Academy of Science, lokale/persönliche Boards (Aufteilung laut Gildenliste, Stand 5.0 PTU). Wer im Testserver 5.0 noch keiner Gilde zugeordnet ist (z. B. Foxwell Enforcement, von Robert am 20.11. im PTU geprüft), erscheint unter „Keiner Gilde zugeordnet“.
- Alle bekannten Organisationen sind sofort sichtbar, auch ohne geladene Logs; abgleichen geht auch ohne Logs. Neuer Schalter „Ohne Abgleich ausblenden“ (Favoriten bleiben sichtbar).
- Organisationen ohne bekannte Rangleiter bekommen die Auftragnehmer-Stufen, deutlich als „angenommen“ markiert.

## [1.12.0] – 2026-11-20

### Hinzugefügt
- **Ruf: Missionen nach Rufstufe.** Je Organisation eine aufklappbare Übersicht aller bekannten Missionen, geordnet nach der Stufe, ab der sie freigeschaltet sind, mit Ruf-Wert. Nach dem Abgleich ist markiert, was freigeschaltet ist, was als Nächstes kommt (mit verbleibenden XP) und was später kommt. Missionen ohne Stufenangabe stehen gesammelt am Ende.
- **Missionstexte, zuschaltbar** (Schalter „Missionstexte anzeigen“, aus = Standard): Ein Klick auf eine Mission öffnet ihren Beschreibungstext in einem Fenster. Der Text kommt zur Laufzeit aus der Sprachdatei des Spiels (`data\Localization\…\global.ini`) im geladenen Ordner `LIVE`; die Seite selbst enthält keine Missionstexte. Ohne Sprachdatei bleibt der Schalter grau, mit Hinweis.

### Behoben
- Missionen mit Namen im Titel (z. B. „Orange Level Contract: MISC Freelancer MAX Needs Assistance“, in der Tabelle „~mission(Ship) Needs Assistance“) werden jetzt erkannt und mitgezählt. Platzhalter erscheinen als [Ship].

## [1.11.0] – 2026-11-20

### Hinzugefügt
- **Ruf: Abgleich per Screenshot.** Im Abgleich-Formular „Screenshot auswerten …“ wählen oder einen Screenshot der mobiGlas-Seite „Ruf“ hineinziehen. Die Seite zählt die vollen Balken (= erreichte Ränge), findet die hervorgehobene Kachel (= nächster Rang) und misst deren Balken auf Teilpixel genau; den Zeitpunkt nimmt sie aus dem Dateinamen. Rang, Prozent und Zeitpunkt werden ausgefüllt, eine Vorschau zeigt den gemessenen Balken rot umrahmt – prüfen und übernehmen. An sechs Screenshots geprüft: höchstens 2 Prozentpunkte Abweichung zur Handmessung, die hervorgehobene Kachel passte jedes Mal. Das Bild wird nur im Browser gelesen.

## [1.10.0] – 2026-11-20

### Hinzugefügt
- **Reiter „Ruf“:** schätzt den Ruf je Organisation als Balken zum nächsten Rang. Das Spiel schreibt keine Ruf-Punkte ins Log; der Reiter rechnet deshalb: Stand aus dem mobiGlas (einmal abgleichen: erreichter Rang + wie weit der Balken der nächsten Stufe gefüllt ist) + Ruf der danach abgeschlossenen Missionen laut Missionsbeschreibung × Faktor.
  - Missionen, Ergebnis (abgeschlossen, fehlgeschlagen, abgebrochen), Organisation und „geteilt“ kommen aus denselben Logs wie im Reiter „Sitzungen“.
  - Angegebene Ruf-Punkte und Rangschwellen stammen aus einer Tabelle, die `ruf_daten.py` aus den Anmerkungen der deutschen Community-Übersetzung baut (nur Zahlen, Titel, Rangnamen; Stand 4.10.3: 510 Missionstitel, 14 Organisationen). Titel und Beschreibung werden exakt gepaart.
  - Der Faktor wird je Organisation aus zwei Abgleichen gelernt; bis dahin gilt 0,55 (Messung an Foxwell, 19./20.11.: es kam etwa die Hälfte der angegebenen Punkte an).
  - Geteilte Missionen zählen als Spanne (halb bis voll, schraffiert im Balken), Missionen ohne Wert und Fehlschläge mit 0, werden aber angezeigt. Favoriten mit Stern oben.
  - Abgleiche und Favoriten bleiben im Browser.

### Geändert
- Sitzungen: Die Log-Auswertung liest zusätzlich die Missionen; der Zwischenspeicher wird deshalb einmal neu aufgebaut.

## [1.9.2] – 2026-11-19

### Behoben
- **Sitzungen: GrimHEX und die Sprungtore Stanton–Nyx werden erkannt.** Das Spiel-Log nennt GrimHEX so statt „Green Imperial Housing Exchange“ und die beiden Tore nach den künftigen Systemen: `RR_JP_NyxCastra` = Stanton Gateway (Nyx), `RR_JP_StantonMagnus` = Nyx Gateway (Stanton), im Spiel geprüft. Das gilt nur, solange Castra und Magnus nicht im Spiel sind, und wird mit jedem Patch neu geprüft.

## [1.9.1] – 2026-11-19

### Behoben
- **Sitzungen: Log-Ordner unter `C:\Programme` ließ sich nicht öffnen.** Chrome sperrt Systemordner für das Merken eines Ordners. „Log-Ordner laden …“ nutzt jetzt das normale Ordner-Auswahlfeld, das dort funktioniert (Chrome fragt „Dateien hochladen?“; die Dateien bleiben auf dem Rechner). „Ordner merken …“ bleibt als Zusatz für Installationen außerhalb von `C:\Programme`. Auch der Ordner `logbackups` allein wird angenommen. Ein Hinweiskasten sagt deutlich, dass der Ordner dann bei jedem Besuch neu geladen werden muss; nach dem Laden steht es auch in der Statuszeile.
- Ausgeblendete Knöpfe im Reiter „Sitzungen“ (z. B. „Neu einlesen“ ohne gemerkten Ordner) erscheinen nicht mehr.

## [1.9.0] – 2026-11-19

### Hinzugefügt
- **Neuer Reiter „Sitzungen“:** liest die Spiel-Logs von Star Citizen (Ordner `StarCitizen\LIVE` oder `PTU`: `Game.log` und `logbackups`) direkt im Browser und zeigt die letzten 25 Sitzungen mit Beginn, Dauer, Ende (normal oder **abgestürzt**), letztem Server/Shard samt Region und IP, letztem Ort, letztem Schiff und Rechtsgebiet.
- Oben stehen **„Letzter Absturz“** und **„Zuletzt“** als eigene Karten, der Shard-Name lässt sich kopieren. Gedacht für die Frage nach einem Absturz: Wo war ich, auf welchem Shard, liegt die Fracht vielleicht noch da?
- Der letzte Ort wird, wo möglich, einem Ort des Fracht-Logbuchs zugeordnet (Raststationen, Sprungtore, Städte, Außenposten); ein Klick öffnet ihn dort.
- Den Ordner merkt sich Chrome/Edge (nach dem Neuladen einmal „Zugriff erlauben“); andere Browser wählen ihn über ein Ordner-Auswahlfeld. Die Logs verlassen den Rechner nicht.

## [1.8.0] – 2026-11-19

### Hinzugefügt
- **Fracht-Logbuch, Umpacken:** Ein Posten lässt sich ganz oder teilweise in eine andere Containergröße umpacken, z. B. 20 × 1 SCU in 1 × 16 + 1 × 4 SCU. Es gibt nur die echten Größen 1, 2, 4, 8, 16, 24 und 32 SCU; was nicht aufgeht, kommt in kleinere Container. Vorschau vor dem Umpacken, Rückgängig möglich.
- **Speicherort frei wählbar:** Unter „Speicherort …“ lässt sich das Logbuch mit einer JSON-Datei verknüpfen, z. B. auf einem USB-Stick oder in einem geteilten Ordner; jede Änderung wird dorthin geschrieben, eine Kopie bleibt im Browser. Wurde die Datei inzwischen woanders geändert, fragt das Logbuch statt zu überschreiben. Funktioniert in Chrome und Edge; in anderen Browsern bleiben Export und Import JSON.
- **Suchergebnisse mit Wert** und Gewinn je Ware und je Ort.

### Behoben
- **Nyx fehlte im Fracht-Logbuch.** UEX kennzeichnet Frachtaufzüge in Nyx nur an alten, stillgelegten Terminals. Jetzt zählen auch Orte mit Waren-Terminal oder Frachtzentrum: Levski, Pyro Gateway, Stanton Gateway und die vier People's Service Stations sind dabei, dazu einige Handelsplätze in Stanton und Pyro (116 statt 102 Orte).

## [1.7.0] – 2026-11-19

### Hinzugefügt
- **Fracht-Logbuch, Suche:** „Ware im Logbuch suchen“ zeigt jede Station und jedes Schiff mit dieser Ware samt Containern; ein Klick springt dorthin.
- **Lagerwert:** Wert je Posten, je Ort, je Schiff und gesamt, nach dem besten Verkaufspreis aus den Daten dieser Seite (star-head), sonst dem UEX-Durchschnitt. Posten ohne bekannten Verkaufspreis (z. B. Erze vor dem Raffinieren) werden genannt statt still weggelassen.
- **Einkaufspreis (optional)** beim Einbuchen, mit Gewinn-Schätzung; Posten mit verschiedenen Einkaufspreisen bleiben getrennt.
- **Bester Verkaufsort** je Ware, mit Sprung zu „Alle Waren“ für alle Verkaufsorte.
- **XLSX-Export** um Einkaufs- und Verkaufspreis, besten Verkaufsort, Wert und Gewinn erweitert.

## [1.6.0] – 2026-11-18

### Hinzugefügt
- **Neuer Reiter „Fracht-Logbuch“:** führt Buch, welche Ware in welchen Containern an welcher Station oder auf welchem deiner Schiffe liegt. Links deine Schiffe mit Füllbalken, rechts alle Orte mit Frachtaufzug nach System und Planet, in der Mitte der gewählte Ort mit seinen Posten.
- **Verschieben** per Drag & Drop oder per Klick/Antippen, mit Mengenabfrage als Container-Anzahl oder SCU; **Einbuchen** und **Ausbuchen**.
- **Überladen** je Schiff schaltbar (Standard +1/3 Laderaum). Warnungen bei vollem Schiff, zu großem Container, illegaler oder flüchtiger Ware; sie sperren nie.
- **Journal** jeder Buchung mit **Rückgängig** (Knopf oder Strg+Z).
- **Speichern** im Browser, **Export JSON** (wieder einlesbar) und **Export XLSX** (Bestand, Schiffe, Journal).
- Stammdaten (Orte, Waren, Schiffe mit Laderaum und Containergrößen) aus der UEX-API, beim täglichen Bau eingebettet.

## [1.5.2] – 2026-11-10

### Geändert
- **„Weitere Tools“ nennt jetzt auch den neuen Schiffskauf-Planer.** Die gemeinsamen Dateien `kopfzeile.py` und `sc_design.py` gelten nun für fünf Tools.

## [1.5.1] – 2026-11-01

### Geändert
- **Kommentare und Docstrings** nach dem Standard von [situation-report](https://github.com/Jaegerfeld/situation-report): Kopfblock mit Autor, Lizenz und fachlicher Funktion in jeder Quelldatei, englische Docstrings im Google-Stil mit `Args`/`Returns`/`Raises`, `#:`-Kommentare an Konstanten, ein Satz über jeder JavaScript-Funktion der Seite. Am Verhalten ändert sich nichts.
- Neue Datei `CONTRIBUTING.md` mit den gemeinsamen Regeln aller vier SC-Tools (Prüfungen, Kommentare, Versionen, gemeinsame Dateien).

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
