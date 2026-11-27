# Changelog

Alle nennenswerten Änderungen an diesem Projekt. Format nach [Keep a Changelog](https://keepachangelog.com/de/1.0.0/), Versionierung nach [SemVer](https://semver.org/lang/de/).

## [1.29.0] – 2026-11-27

### Hinzugefügt
- **Homebase.** Ein Ort lässt sich als Homebase merken (Knopf **🏠 Als Homebase merken** am gewählten Ort, in der Fracht wie bei den Gegenständen). Die Homebase steht danach in der Ortsliste ganz oben, unabhängig von Suche und Filter, und in jeder Zielauswahl beim Verschieben direkt nach deinen Schiffen. Sie ist mit 🏠 markiert. Es gibt genau eine; **Homebase aufheben** nimmt die Markierung zurück. Rückgängig, Speicherdatei, Export und „Aufs Handy“ nehmen sie mit.

### Geändert
- **Gegenstände: Ortsauswahl wie beim Fracht-Logbuch.** Das Auswahlfeld „Ort oder Schiff“ ist weg. Stattdessen wählst du wie bei der Fracht links ein Schiff oder rechts einen Ort (mit Suche, Systemfilter und „nur mit Gegenständen“); die Mitte zeigt die Gegenstände dort und das Formular zum Eintragen. Ohne gewählten Ort zeigt die Mitte alle Gegenstände mit Suche und Gruppierung.
  - Der gewählte Ort gilt für Fracht und Gegenstände. Ein Knopf am Ort wechselt zwischen beiden Ansichten.
  - Die Ortsliste zeigt bei den Gegenständen die Zahl der Einträge je Ort, bei der Fracht einen Hinweis „🎖 n Gegenstände“.
  - Verschieben geht über **Ändern**: Dort lässt sich der Ort des Eintrags umstellen.

## [1.28.0] – 2026-11-27

### Hinzugefügt
- **Gegenstände: Vorschlagsliste aus dem Wikelo-Planer.** Beim Eintragen schlägt das Buch jetzt die Zutaten aller Tauschangebote von Wikelo vor, so wie sie der [Wikelo-Planer](https://jaegerfeld.github.io/StarCitizen-Wikelo-Planer/app.html) führt; in der Liste steht „Wikelo-Zutat“ daneben. Die Namen kommen beim täglichen Bau aus dessen veröffentlichten Daten und ändern sich mit ihnen. Ist die Datei beim Bau nicht erreichbar, entsteht die Seite ohne diese Vorschläge; die feste Liste und die Warennamen bleiben. Jeder andere Name lässt sich weiter eintragen.

## [1.27.0] – 2026-11-27

### Hinzugefügt
- **Fracht-Logbuch: Buch für wichtige Gegenstände.** Über dem Logbuch steht jetzt der Umschalter **Fracht | Gegenstände**. Unter „Gegenstände“ hältst du fest, was wo liegt, wenn es keine Fracht in Containern ist: Medaillen, MG Scrip, Tauschware für Wikelo, Ressourcen in ihren Qualitätsstufen.
  - Ein Eintrag hat Gegenstand, Stückzahl, Qualität (frei: Zahl oder Stufe wie „Pristine“ oder „Grade AAA“), Ort oder Schiff und eine Notiz. Pflicht sind nur Gegenstand und Ort. Derselbe Gegenstand in gleicher Qualität am selben Ort wird zusammengezählt; verschiedene Qualitäten bleiben getrennte Einträge.
  - Die Orte und Schiffe sind die des Logbuchs. Am gewählten Ort zeigt die Frachtansicht, wie viele Gegenstände dort liegen, und springt hin.
  - Suche über Name, Qualität, Ort und Notiz; die Liste lässt sich nach Gegenstand (mit Summe und Zahl der Orte) oder nach Ort gruppieren.
  - Rückgängig, Journal, Speicherdatei, Export JSON, Export XLSX (eigenes Blatt „Gegenstände“) und „Aufs Handy“ nehmen die Gegenstände mit.
- Die Vorschlagsliste beim Eintragen ist eine feste Liste gängiger Gegenstände plus die Warennamen. Sie ist nicht an den Wikelo-Planer angebunden; jeder andere Name lässt sich eintragen.

## [1.26.2] – 2026-11-26

### Behoben
- **Spielstand 4.10.3.** Kopfzeile, `data.json` und die Routen-Übersicht nannten noch „4.10.2-LIVE“, obwohl 4.10.3 seit dem 12.11.2026 live ist. Die Preise selbst waren aktuell (sie kommen täglich von star-head); falsch war nur die Angabe des Spielstands. Der Screenshot-Auswerter und das SC Cockpit übernehmen die Angabe mit ihrem nächsten Bau.

## [1.26.1] – 2026-11-26

### Geändert
- **Die Adresse dieses Tools leitet ins SC Cockpit weiter.** Der Handels-Planer ist ins [SC Cockpit](https://jaegerfeld.github.io/sc-cockpit/) eingezogen: Fracht (Routen & Waren, Logbuch) und Pilot (Ruf, Sitzungen). Wer https://jaegerfeld.github.io/StarCitizen-Handels-Planer/ öffnet, landet dort im passenden Bereich; online sind deine Daten dieselben, weil Cockpit und Tool denselben Browser-Speicher nutzen. Links von „Aufs Handy“ (`#lb=…`, `#ruf=…`) kommen im Cockpit an.
- Diese Seite selbst bleibt erreichbar: https://jaegerfeld.github.io/StarCitizen-Handels-Planer/app.html. Am Tool hat sich nichts geändert.

## [1.26.0] – 2026-11-26

### Hinzugefügt
- **Fracht-Logbuch: Anschluss ans Cockpit.** Das Logbuch läuft jetzt auch im Bereich „Fracht“ des [SC Cockpits](https://jaegerfeld.github.io/sc-cockpit/). Dort zeigt es die **Merker am Ort**: Ein gewählter Ort listet unter „Hier zu erledigen“ die offenen Merker, die dorthin gehören, zum Beispiel Kaufmerker aus dem Komponenten-Planer mit Händler, Schiff und Preis; ein Schiff listet seine eigenen. Merker lassen sich dort abhaken und für den Ort oder das Schiff neu anlegen. Orte und Schiffe mit Merkern tragen in den Listen „☑ n Merker“, der Filter „nur mit Fracht oder Notiz“ zeigt sie mit an. Im Handels-Planer selbst gibt es keine Merker; hier ändert sich dadurch nichts.

### Geändert
- **Zwei Tabs, ein Logbuch:** Speichert ein anderer Tab (Handels-Planer oder Cockpit) das Logbuch, übernimmt das offene Logbuch diesen Stand, statt ihn beim nächsten Speichern mit dem älteren zu überschreiben. Die Auswahl des Tabs bleibt; „Rückgängig“ beginnt danach neu.

## [1.25.0] – 2026-11-26

### Hinzugefügt
- **Fracht-Logbuch: Notizen.** Unten in der Mitte steht ein Freitextfeld für den gewählten Ort oder das gewählte Schiff (z. B. „hier kaufen: 2 × Kühler“); ohne Auswahl sind es allgemeine Notizen. Der Text wird beim Tippen gespeichert. Orte und Schiffe mit Notiz tragen in den Listen „📝 Notiz“, der Filter heißt jetzt „nur mit Fracht oder Notiz“.
  - Die Notizen stehen in Export JSON, in der Speicherdatei, im XLSX (neues Blatt „Notizen“) und im Paket „Aufs Handy“. Dateien aus älteren Versionen ohne Notizen lassen die Notizen im Browser unberührt.
  - „Rückgängig“ lässt getippte Notizen in Ruhe; nur Einlesen, Datei laden, Übernahme vom PC und das Entfernen eines Schiffs nehmen den Notizstand mit zurück.

## [1.24.0] – 2026-11-25

### Hinzugefügt
- **Sitzungen: Shard-Namen.** Neben der Shard-ID steht jetzt der Name, den das Spiel beim Beitritt zeigt (z. B. `focused_launch` für `pub_euw1b_13165946_180`) – in „Zuletzt“, „Letzter Absturz“ und der Sitzungsliste. Der Name steht nicht im Log und folgt nicht aus der ID; die Zuordnung ist eine Tabelle aus 23 Screenshots (19.–25.11.2026, 18 Shards, ohne Widerspruch). Sie gilt für den Spielstand 4.10.3 (Build 13165946); nach einem Patch zeigen unbekannte Shards wie bisher nur die ID.

## [1.23.0] – 2026-11-24

### Hinzugefügt
- **Gemeinsame Flotte mit dem Komponenten-Planer** (Reiter „Komponenten“ im Schiffskauf-Planer; neu `flotte.py`, byte-gleich in beiden Repos): Die Schiffe im Fracht-Logbuch sind jetzt dieselben wie dort. Legst du ein Schiff in einem Tool an, benennst es um oder entfernst es, ist es im anderen genauso – online, weil beide Seiten auf jaegerfeld.github.io liegen; per Doppelklick geöffnete Offline-Kopien haben je einen eigenen Speicher.
- Ins Logbuch kommen nur Typen mit Laderaum; ein Schiff mit Fracht an Bord wird nie von außen entfernt. Deine bisherigen Logbuch-Schiffe werden beim ersten Start in die gemeinsame Flotte übernommen, Ladung und Journal bleiben unverändert.

## [1.22.0] – 2026-11-21

### Hinzugefügt
- **Knopf „Anleitung + How-To“ in der Kopfzeile** (vor „Was ist neu?“): öffnet einen Dialog mit Reitern – Kurzanleitung, Tutorials Schritt für Schritt und Fragen –, auf Deutsch und Englisch; er folgt der Sprachwahl, auch wenn er offen ist. Die Texte stehen in `ANLEITUNG.md` und `MANUAL.md` und werden wie das Changelog in die Seite eingebacken, gehen also auch in der Offline-Kopie.
- Gemeinsame Kopfzeile Kit 4 (`kopfzeile.py`, byte-gleich in allen fünf Tools); der kleine Markdown-Leser kennt jetzt auch nummerierte Listen.

## [1.21.0] – 2026-11-21

### Hinzugefügt
- **Ruf: Gildenfarben.** Jede Gilde hat eine eigene Farbe (Transport Blau, Resources Bernstein, Mercenary Rot, Bounty Violett, Academy Grün, lokale Boards Magenta, ohne Gilde Grau): als Streifen links an Karten und Zeilen, leichte Tönung oben in der Karte, Linie und Überschrift der Gilde. Im hellen Modus dunklere Töne derselben Farben (Kontrast 5,3 bis 6,9 : 1). Türkis bleibt dem Fortschritt vorbehalten; die Gilde steht weiter auch als Text.
- **Umschalter „Karten | Liste“.** Die Liste zeigt je Organisation eine Zeile mit Abzeichen, Name, Rang, Balken und „≈ XP · noch ≈ … bis …“ – etwa 44 statt 125 px. Ein Klick auf die Zeile klappt die volle Karte auf.
- **Ordnung „nächster Aufstieg zuerst“** (neben „nach Gilde“): alle Organisationen nach dem Anteil am aktuellen Band, ohne Gildengruppen – oben steht, wo der nächste Aufstieg am nächsten ist.
- **Favoriten oben:** Mit Stern markierte Organisationen stehen in einem eigenen Abschnitt vor allen Gilden.
- Gildenfarbe auch in der Prüfliste von „Screenshots abgleichen …“ (Farbpunkt vor der Organisation).
- Ansicht und Ordnung merkt sich der Browser.

### Geändert
- **Kleine Gilden teilen sich eine Zeile:** Jede Gilde ist so breit wie ihre Karten (bis vier), mehrere kleine stehen nebeneinander.
- **Gildenkopf einzeilig:** Name und Anzahl; die Beschreibung steht im Tooltip.
- **Organisationen ohne Abgleich** erscheinen je Gilde als eine Namenszeile statt als leere Karten; ein Klick auf den Namen öffnet die Karte zum Abgleichen.

### Behoben
- Kurznamen werden nie zur bloßen Zahl („Prestige 1“ blieb bisher als „1“ stehen).

## [1.20.1] – 2026-11-21

### Geändert
- **Ruf, „Aufs Handy“: kompakte Karten auch auf dem Handy.** Die übertragene Ansicht zeigt je Organisation dieselbe kompakte Karte wie die obere Hälfte am PC: Abzeichen und Name, Rang, kleine Abzeichen-Leiter, Balken und „≈ XP · noch ≈ … bis …“.

## [1.20.0] – 2026-11-21

### Geändert
- **Ruf: kompakte Karten für den schnellen Überblick.** Jede Karte zeigt oben nur noch, was für den Überblick zählt: Abzeichen und Name, aktuellen Rang, die Leiter als kleine Abzeichen-Reihe, den Balken und eine Zahlenzeile („≈ 15.529 XP · noch ≈ 22.471 bis Leitend“). Ein Klick auf die obere Hälfte oder auf ▾ klappt den Rest auf: beschriftete Leiter, Abgleich-Infos und Faktor, die Knöpfe zum Abgleichen, Missionen seit dem Abgleich und Missionen nach Rufstufe. ▴ klappt wieder zu; beim Abgleichen klappt die Karte von selbst auf.
- Die Karten sind schmaler (ab 300 px statt 440 px): auf breiten Bildschirmen drei oder mehr nebeneinander, auf dem Handy eine Spalte.
- Ohne Abgleich zeigt die Karte „Noch kein Abgleich“, die Zahl der Missionen in den Logs und die graue Leiter.

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
