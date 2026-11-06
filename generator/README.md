# Vorschau-Webseite + Angebot aus einem Google-Maps-Link

## Bedienoberfläche (empfohlen)
Doppelklick auf **`Webseiten-Generator.command`** im Hauptordner (beim ersten Mal ggf. Rechtsklick → Öffnen, weil
macOS Skripte aus dem Internet blockiert). Die Oberfläche öffnet sich im Browser (`http://127.0.0.1:8765`, nur auf
diesem Rechner erreichbar):
1. Google-Maps-Link einfügen, optional Excel + Fotos auswählen
2. Design (1–10) und Farbkonzept (1–10) anklicken – oder **„＋ Eigenes Farbkonzept“**: Hintergrund, Text und Akzent
   wählen, Abstufungen werden abgeleitet (Feinabstimmung möglich), Kontrast-Warnung, Live-Vorschau; gespeicherte
   Farbkonzepte landen in `generator/eigene_farben.json` und stehen dann in der Liste
3. „Vorschau erstellen“ (ca. 2 s) oder „Kundenauswahl“ (alle Designs + Farben, ca. 1–2 Min.) – Ergebnis rechts,
   Links zu Webseite, Angebot und Auswahl-PDF
Der Google-API-Schlüssel kann unter „Einstellungen“ gespeichert werden (`generator/einstellungen.json`, nicht im Git).

## Kommandozeile

```
cd ~/Programmieren/Friseurwebseite
GOOGLE_MAPS_API_KEY=<Schlüssel> .venv/bin/python generator/erstelle_webseite.py "<Google-Maps-Link>" --excel <salon.xlsx>
```
Link und Excel sind jeweils optional (mindestens eins von beiden). `--nicht-oeffnen` unterdrückt das automatische Öffnen.

## Designs und Farbkonzepte (10 x 10, frei kombinierbar)
`--design 1–10` (Aufbau, Formen, Typografie, Schriften) und `--farbe 1–10` (Farbpalette), alternativ die Felder
„Design“ und „Farbe“ im Blatt Grunddaten der Excel. Standard: Design 1, Farbe 1.
`--alle-designs` erzeugt die Kundenauswahl `designauswahl.html`/`.pdf`: Teil A die 10 Designs (im gewählten
Farbkonzept), Teil B die 10 Farbkonzepte (im gewählten Design), je mit Startseite und Leistungsseite; Varianten
unter `vorschau/<salon>/designs/` (Bilder geteilt, Klick öffnet die komplette Seite).

Die Designs und Farbkonzepte sind aus 262 Startseiten Münchner Friseure abgeleitet (Verzeichnis Gelbe Seiten,
November 2026): die dort häufigsten Stilrichtungen und Farbfamilien, nachempfunden, keine Kopie einzelner Seiten.

| Nr. | Design | Startbereich | Formen / Details | Schriften |
|---|---|---|---|---|
| 1 | Klassik Vollbild | Salonfoto vollflächig, dunkler Verlauf, Text links | feine Linien, eckig | Playfair Display / Open Sans |
| 2 | Hell & Luftig | zentrierter Text, Foto als breites Band unten | viel Weißraum, Versalien, nur Linien | Josefin Sans / Lato |
| 3 | Modern Split | Text links, Foto rechts | rund, weiche Schatten | Montserrat / Open Sans |
| 4 | Typo-Statement | Vollbild-Foto, riesige Großbuchstaben | kräftige Rahmen, Akzentbalken | Oswald / Roboto |
| 5 | Editorial Schwarz-Weiß | große Magazin-Schrift, kleines S/W-Foto | nur Linien, S/W-Bilder | Bodoni Moda / Inter |
| 6 | Boutique Handschrift | Foto im Torbogen, Salonname in Schreibschrift | Bögen, Pillen-Schaltflächen, ✦ | Cormorant Garamond / Lato / Great Vibes |
| 7 | Barbershop | dunkles Vollbild, Abzeichen, Barber-Streifen | Slab-Schrift, ✂, Streifen | Alfa Slab One / Roboto |
| 8 | Natur & Bio | Foto in fließender Form, Farbfleck | organische Bildformen, ❧ | Lora / Nunito |
| 9 | Luxus Gerahmt | Vollbild-Foto im Doppelrahmen, zentriert | Doppelrahmen, ◆-Ornamente, Versalien | Cinzel / Montserrat |
| 10 | Freundlich & Nah | Vollbild-Foto mit heller Textkarte | Etiketten, runde Karten, Farbkante | Poppins / Open Sans |

Farbkonzepte: 1 Schwarz-Weiß, 2 Nude & Champagner, 3 Bordeaux, 4 Cognac & Creme, 5 Salbei & Leinen, 6 Marineblau,
7 Beere & Rosé, 8 Gold Noir, 9 Anthrazit & Kupfer, 10 Petrol & Mint.

Erweitern in `generator/designs.py`: Designs sind CSS-Ergänzungen (`design.css`, wird zuletzt geladen; `{HERO_IMG}` =
Titelbild = erstes Galeriebild), Farbkonzepte sind Paletten (Akzent muss stark zum Hintergrund kontrastieren).

## Online-Terminbuchung
Im Excel-Blatt Grunddaten „Buchungslink“ (z. B. eTermin-Buchungsseite), „Buchungs-Anbieter“ und optional den
Datenschutz-Link des Anbieters eintragen. Dann führen alle „Termin buchen“-Schaltflächen zum Anbieter (neuer Tab),
`termin.html` leitet weiter, und die Datenschutzerklärung erhält einen Abschnitt zur Online-Terminbuchung.
Ohne Buchungslink bleibt das eigene Anfrageformular. Eingebunden wird bewusst als Link, nicht als eingebettetes
Fenster: So lädt die Seite nichts vom Anbieter, und es ist dafür kein Cookie-Banner nötig.

## Salon-Daten per Excel
- Leere Vorlage: `generator/salon_daten_vorlage.xlsx` (neu erzeugen mit `.venv/bin/python generator/excel_daten.py vorlage`).
- Pro Salon eine Kopie ausfüllen; Fotos in denselben Ordner legen und den Dateinamen eintragen.
- Blätter: Grunddaten, Impressum (Schlüssel/Wert), Öffnungszeiten, Team, Leistungen, Galerie, Kennzahlen, Bewertungen.
- Ausgefüllte Werte überschreiben Google-Daten; leere Felder bleiben bei Google bzw. Platzhalter. Listen-Blätter
  ersetzen die Liste ganz, sobald eine Zeile ausgefüllt ist.
- Leistungen: Bereich (schnitt/farbe/pflege/braut oder eigener), Spalte links/rechts, entweder „Preis“ oder
  „Varianten“ im Format `kurz: ab 45 €; lang: ab 65 €`.

Ergebnis in `vorschau/<salon>/` (nicht im Git, siehe `.gitignore`):
- komplette Webseite auf Basis dieser Vorlage mit eigener `config.js` (Name, Adresse, Telefon, Öffnungszeiten,
  Bewertungen, bis zu 6 Fotos aus Google), für Suchmaschinen gesperrt (`noindex`)
- Schriften lokal in `fonts/` (keine Verbindung zu Google beim Besuch)
- `angebot.pdf` mit den Paketen aus `generator/angebot.json`

Beides öffnet sich am Ende automatisch (macOS).

## Einrichtung
1. Google Cloud: Projekt anlegen, **Places API (New)** aktivieren, API-Schlüssel erstellen (auf diese API beschränken).
2. `generator/angebot.json`: Absenderzeile, Preise, Umsatzsteuer-Hinweis (Kleinunternehmer ja/nein) anpassen.
3. Python-Umgebung: `python3 -m venv .venv && .venv/bin/pip install requests openpyxl`; Google Chrome (für das PDF).

Ohne Schlüssel kommen die Daten nur aus Link-Name und Excel; Fehlendes bleibt Platzhalter.

## Vor der Übergabe an den Kunden
- Fotos und Texte vom Salon verwenden: Google-Fotos und -Bewertungen dürfen nur mit Quellenangabe gezeigt und nicht
  dauerhaft gespeichert werden – sie sind nur für die Vorschau gedacht.
- Leistungen/Preise, Team, E-Mail, Instagram/Facebook in `config.js` mit den echten Angaben füllen.
- Impressum (Inhaber, Rechtsform, Kammer, USt-ID) und Datenschutzerklärung vervollständigen.
- Google-Karte nur nach Einwilligung laden (Cookie-/Consent-Lösung) oder durch einen Link ersetzen.
- `noindex` aus den HTML-Dateien entfernen, wenn die Seite live geht.

## Kunden ansprechen
Werbe-E-Mails und -Anrufe ohne vorherige Einwilligung sind in Deutschland auch gegenüber Firmen unzulässig (UWG § 7).
Erlaubt: persönlicher Besuch, Brief mit Vorschau-Link/QR-Code, Anzeigen, Empfehlungen.
