# SC Handels-Planer – Anleitung

## Kurzanleitung

Der Handels-Planer zeigt dir, welche Ware du wo kaufst und wo du sie mit Gewinn verkaufst. Dazu führst du Buch über deine Fracht, siehst nach einem Absturz, wo du zuletzt warst, und schätzt deinen Ruf je Organisation.

### Die Reiter

- **Routen:** drei Listen – Top legale Bulk-Routen (Kauf-Bestand ab 100 SCU), Höchste Margen insgesamt und Illegale Routen. Mit gewähltem Laderaum siehst du Einsatz und Gewinn pro Ladung.
- **Alle Waren:** jede Ware mit bestem Kauf, bestem Verkauf und Marge. Ein Klick auf eine Zeile zeigt alle Kauf- und Verkaufsorte mit Preis, Bestand und Stand.
- **Nach Verkaufsort** und **Nach Kaufort:** je Ort, was du dort mit Gewinn verkaufen oder einladen kannst.
- **Fracht-Logbuch:** welche Ware in welchen Containern an welcher Station oder auf welchem deiner Schiffe liegt, mit Lagerwert.
- **Sitzungen:** liest die Spiel-Logs und zeigt je Sitzung Server (Shard), letzten Ort, letztes Schiff und ob das Spiel abgestürzt ist.
- **Ruf:** schätzt deinen Ruf je Organisation als Balken zum nächsten Rang, nach einem Abgleich mit deinem mobiGlas.

### Häufige Handgriffe

- Spaltenköpfe anklicken sortiert die Tabelle, ein zweiter Klick dreht die Richtung um.
- Passt nichts zu den Filtern, setzt **Filter zurücksetzen** sie zurück.
- **DE | EN** wechselt die Sprache, **Hell / Dunkel** das Farbschema.
- **Was ist neu?** zeigt die Änderungen der letzten Versionen.
- Im Fracht-Logbuch macht **Rückgängig** (oder Strg+Z) die letzte Änderung rückgängig.

### Woher die Daten kommen

- Preise, Bestände und Orte kommen von [star-head.de](https://star-head.de). Sie sind von der Community gepflegt und teils Tage alt (Spalte „Stand“). Prüf die Preise vor dem Kauf im Spiel.
- Marge/SCU rechnet ohne Sprit, Zeit und Risiko.
- Die Online-Version wird jeden Tag neu gebaut. **Neuesten Stand laden (GitHub)** holt diesen Stand, auch in einer Offline-Kopie. Ein Rechtsklick auf den Knopf geht zurück zu den eingebauten Daten.
- Die Orte, Waren und Schiffe im Fracht-Logbuch kommen von UEX.

### Was im Browser bleibt

- Logbuch, Abgleiche, Favoriten, Schiffswahl, Sprache und Farbschema liegen nur in deinem Browser (localStorage). Nichts davon geht an einen Server.
- Die Spiel-Logs und Screenshots liest die Seite nur im Browser. Sie verlassen deinen Rechner nicht.
- Eine lokal geöffnete Kopie (`SC_Handels_Planer.html`) hat einen eigenen Speicher, getrennt von der Online-Version. Was du online eingetragen hast, siehst du dort nicht.
- Die Seite läuft auch offline. Nur der QR-Code bei **Aufs Handy …**, die Texterkennung bei **Screenshots abgleichen …** und **Neuesten Stand laden (GitHub)** brauchen Internet.

## Tutorial: Route planen

Ziel: Du findest eine lohnende Route für dein Schiff und weißt, was eine volle Ladung kostet und bringt.

1. Öffne den Reiter **Routen**.
2. Wähle unter **Laderaum** bei **Schiff** dein Schiff (Cutlass Black, Freelancer oder Mercury Star Runner). Für ein anderes Schiff trag die SCU direkt ins Feld **SCU** ein; die Auswahl springt dann auf „eigener Wert“.
3. Schränke bei Bedarf **Kauf in System** und **Verkauf in System** ein, z. B. auf das System, in dem du gerade bist.
4. Lies die Liste **Top legale Bulk-Routen**. Hier ist die Ware am Kaufort in Menge vorrätig.
5. Vergleiche die Spalten **Einsatz/Ladung** (so viel aUEC brauchst du) und **Gewinn/Ladung** (so viel bleibt ohne Kosten übrig).
6. Steht neben dem Gewinn ein ⚠ mit einer SCU-Zahl, ist der Bestand am Kaufort kleiner als dein Laderaum. Dann bekommst du dort keine volle Ladung.
7. Willst du eine bestimmte Ware oder einen Ort, tipp ihn in **Suche (Ware/Ort)**, z. B. „Gold“ oder „Levski“.
8. Für alle Alternativen wechsle zu **Alle Waren**, such die Ware und klick auf ihre Zeile. Links stehen die Kauforte (günstigster zuerst), rechts die Verkaufsorte (teuerster zuerst).
9. Prüf die Spalte **Stand**. Ist der Preis alt, prüf ihn im Spiel an der Konsole, bevor du kaufst.

### Tipps

- **Höchste Margen insgesamt** enthält auch Waren, die es nur in Kleinstmengen gibt. Achte auf den Bestand.
- **Illegale Routen** gehen nur an versteckten Konsolen. Bei einem Scan verlierst du die Ware und bekommst CrimeStat.
- Für eine Rückfracht öffne **Nach Kaufort** und wähle deinen Zielort unter **Kaufort**. Dann siehst du, was du dort mit Gewinn einladen kannst.
- Dein gewähltes Schiff und die SCU merkt sich der Browser.

## Tutorial: Fracht verbuchen

Ziel: Du trägst dein Frachtschiff ein, buchst gekaufte Ware ein und verschiebst sie an eine Station.

1. Öffne den Reiter **Fracht-Logbuch**.
2. Klick links unter **Meine Schiffe** auf **+ Schiff hinzufügen**.
3. Tipp bei **Schiffstyp** den Namen und wähle ihn aus der Liste. Die Liste enthält nur Schiffe mit Laderaum. Einen Namen kannst du unter **Eigener Name (optional)** vergeben. Das Schiff gehört zu deiner gemeinsamen Flotte: Online steht es mit demselben Namen auch im Reiter **Komponenten** des Schiffskauf-Planers, und Schiffe von dort (mit Laderaum) erscheinen hier.
4. Willst du Fracht außerhalb des Frachtgitters erfassen, setz den Haken bei **Überladen erlauben (Fracht außerhalb des Frachtgitters)**. Das Feld **Überladen bis (% über Laderaum)** steht auf 33. Klick dann **Hinzufügen**.
5. Das neue Schiff ist ausgewählt. Klick in der Mitte auf **+ Fracht einbuchen**.
6. Wähle die **Ware** aus der Liste, die **Containergröße** und die **Anzahl**. Den **Einkaufspreis je SCU** kannst du eintragen, dann schätzt das Logbuch deinen Gewinn. Klick **Einbuchen**.
7. Die Fracht erscheint als Posten (z. B. „32 SCU × 4“) mit Lagerwert und bestem Verkaufsort. Der Füllbalken des Schiffs zeigt, wie voll es ist.
8. Zum Verschieben zieh den Posten auf einen Ort rechts unter **Orte** oder auf ein anderes Schiff. Oder klick den Posten an und wähle das Ziel bei **Nach**.
9. Gib im Fenster die Menge an, als **Container** oder in **SCU**, und klick **Verschieben**. Verkaufte Ware entfernst du mit **Ausbuchen**.
10. Hat dein Schiff andere Containergrößen, nimm im selben Fenster **Umpacken …**, wähle die **Neue Containergröße** und klick **Umpacken**.
11. Klappe unten das **Journal** auf. Dort steht jede Buchung mit Uhrzeit.
12. Unten in der Mitte steht das Feld **Notizen**. Es gehört zum gewählten Ort oder Schiff, zum Beispiel „hier kaufen: 2 × Kühler“. Ist nichts gewählt, schreibst du **Allgemeine Notizen**. Der Text wird beim Tippen gespeichert; Orte und Schiffe mit Notiz tragen in den Listen das Zeichen „📝 Notiz“, und der Filter **nur mit Fracht oder Notiz** zeigt sie mit an. Die Notizen stehen auch in den Exporten und in der Speicherdatei.
13. Im [SC Cockpit](https://jaegerfeld.github.io/sc-cockpit/) läuft dasselbe Logbuch im Bereich **Fracht**. Dort zeigt es zusätzlich die **Merker** am Ort, zum Beispiel Kaufmerker aus dem Komponenten-Planer. Ist das Logbuch in zwei Tabs offen, übernimmt jeder den Stand des anderen, sobald der speichert.

### Tipps

- **Ware im Logbuch suchen** zeigt, wo eine Ware überall liegt. Ein Klick auf einen Treffer öffnet den Ort.
- **Gegenstände** (Umschalter über dem Logbuch) ist das Buch für alles, was keine Container-Fracht ist: Medaillen, MG Scrip, Tauschware, Ressourcen mit Qualität. Trag Gegenstand, Stückzahl und Ort ein; Qualität und Notiz sind freiwillig. Die Suche findet einen Gegenstand an allen Orten, **Gruppieren nach** ordnet die Liste nach Gegenstand oder Ort. Ein Klick auf einen Ort öffnet ihn in der Frachtansicht.
- Warnungen (Laderaum voll, Container zu groß, illegal, verdirbt) sperren nie. Sie weisen dich nur darauf hin.
- **alle Verkaufsorte ↗** springt zu **Alle Waren** mit dieser Ware.
- Sichere dein Logbuch mit **Export JSON** und lies es mit **JSON einlesen** wieder ein. **Export XLSX** erzeugt eine Excel-Datei.
- In Chrome und Edge legt **Speicherort …** das Logbuch zusätzlich in eine Datei, z. B. auf einem USB-Stick.
- **Aufs Handy …** zeigt einen QR-Code. Das Handy übernimmt damit Schiffe, Fracht und Gegenstände als sein Logbuch.

## Tutorial: Ruf abgleichen

Ziel: Du siehst je Organisation, wie weit du vom nächsten Rang entfernt bist.

1. Öffne den Reiter **Ruf** und klick **Log-Ordner laden …**. Wähle den Ordner `…\Roberts Space Industries\StarCitizen\LIVE` (oder `PTU`). Lädst du den ganzen Ordner LIVE, kann der Reiter später auch Missionstexte zeigen.
2. Mach im Spiel einen Screenshot (Taste **Druck**) der mobiGlas-Seite „Ruf“, je Organisation einen. Am besten vor dunklem Hintergrund, denn das mobiGlas ist durchscheinend.
3. Klick **Screenshots abgleichen …**. Wähle die Bilder mit **Screenshots wählen …** oder den ganzen Ordner mit **Ordner wählen …** (`StarCitizen\LIVE\screenshots`). Du kannst die Bilder auch ins Fenster ziehen.
4. Beim ersten Mal lädt die Seite die Texterkennung (einige MB). Danach erkennt sie je Bild Organisation, Rang und Balken.
5. Prüf die Liste. Je Zeile kannst du den Haken entfernen oder die Organisation ändern. Je Organisation zählt das neueste Bild.
6. Klick den Knopf unten, z. B. **5 Abgleiche übernehmen**. Die Organisationen erscheinen jetzt als Karten mit Rang und Balken.
7. Für eine einzelne Organisation klick auf die obere Hälfte ihrer Karte oder auf ▾. Organisationen ohne Abgleich stehen unter „Ohne Abgleich“ als Namen; ein Klick klappt die Karte auf. Dann klick **Stand aus dem mobiGlas abgleichen …**.
8. Lass dort per **Screenshot auswerten …** die Felder ausfüllen, oder trag sie selbst ein: **Rang (hervorgehobene Kachel)** ist dein aktueller Rang, **Balken dieser Kachel in %** der Weg zum nächsten Rang. Prüf **Zeitpunkt des Blicks** und klick **Übernehmen**.
9. Ab dem Abgleich zählt der Reiter jede Mission, die du danach abschließt, aus den Logs dazu. Lade dafür nach dem Spielen den Log-Ordner neu.
10. Aufgeklappt zeigt die Karte unter **Missionen nach Rufstufe**, welche Missionen freigeschaltet sind und was als Nächstes kommt.

### Tipps

- Gleiche eine Organisation später ein zweites Mal ab. Dann lernt der Reiter, wie viel Ruf eine Mission dort wirklich bringt (Faktor), und die Schätzung wird genauer.
- Geteilte Missionen zählen als Spanne (halber bis voller Betrag). Fehlgeschlagene und abgebrochene Missionen zählen 0.
- Mit dem Stern (☆) heftest du eine Organisation oben unter **Favoriten** an.
- **Karten | Liste** und **Ordnen:** „nächster Aufstieg zuerst“ zeigen dir schnell, wo der nächste Rang am nächsten ist.
- Ein falscher Abgleich? **Letzten Abgleich entfernen** in der aufgeklappten Karte.
- **Aufs Handy …** schickt Rang und Balken per QR-Code aufs Handy. Dort kannst du den Stand nur ansehen.

## Fragen

### Wo war ich vor dem Absturz?

1. Öffne den Reiter **Sitzungen** und klick **Log-Ordner laden …**.
2. Wähle den Ordner `…\StarCitizen\LIVE` (oder `PTU`). Chrome fragt „Dateien hochladen?“; die Dateien bleiben trotzdem auf deinem Rechner.
3. Oben steht die Karte **Zuletzt**, nach einem Absturz zusätzlich **Letzter Absturz**. Dort siehst du den Shard – mit dem Namen, den das Spiel beim Beitritt zeigt, falls er bekannt ist, darunter die ID –, Region, Server, **Letzter Ort** und **Letztes Schiff**.
4. Ist der letzte Ort ein unterstrichener Name, öffnet ein Klick diesen Ort im Fracht-Logbuch. **kopieren** kopiert die Shard-ID.

### Warum muss ich den Log-Ordner jedes Mal neu laden?

Liegt Star Citizen unter `C:\Programme` (Standard), erlaubt Chrome keinen dauerhaften Zugriff. Liegt es woanders, verknüpft **Ordner merken …** den Ordner dauerhaft (nur Chrome und Edge). Der Reiter liest die neuesten 25 Log-Dateien.

### Warum sind die Preise anders als im Spiel?

Die Preise sind von der Community gemeldet und teils Tage alt. Die Spalte **Stand** zeigt, wann. Prüf den Preis vor dem Kauf an der Konsole.

### Warum zeigt der Ruf-Reiter keine Missionstexte?

Die Texte kommen aus der Sprachdatei des Spiels im geladenen Ordner. Lade über **Log-Ordner laden …** den ganzen Ordner LIVE, nicht nur `logbackups`, und schalte **Missionstexte anzeigen** ein. Ist der Schalter grau, zeigt ein Klick darauf den Grund.

### Wie bringe ich mein Logbuch auf einen anderen Rechner?

Mit **Export JSON** und **JSON einlesen**, mit **Speicherort …** (Chrome und Edge) über eine gemeinsame Datei oder mit **Aufs Handy …** aufs Handy.
