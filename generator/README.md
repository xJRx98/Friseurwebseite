# Vorschau-Webseite + Angebot aus einem Google-Maps-Link

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

| Nr. | Design | Startbereich | Formen / Details | Schriften |
|---|---|---|---|---|
| 1 | Klassik Elegant | Text auf Farbverlauf | feine Linien, eckig | Cormorant Garamond / Jost |
| 2 | Modern Split | Text links, Foto rechts | rund, weiche Schatten | Manrope / Inter |
| 3 | Bold Statement | Vollbild-Foto, zentriert, Großbuchstaben | kräftige Rahmen, Akzentbalken | Oswald / Barlow |
| 4 | Boutique Bogen | Foto im Torbogen | Bögen, Pillen-Schaltflächen, ✦ | Playfair Display / Lato |
| 5 | Minimal Editorial | große Magazin-Schrift, kleines S/W-Foto | nur Linien, S/W-Bilder | Bodoni Moda / Inter |
| 6 | Glass Soft | weichgezeichnetes Foto, Text auf Glasfläche | durchscheinende Karten, Unschärfe | Plus Jakarta Sans |
| 7 | Retro Salon | rundes Foto mit Ring, Streifen unten | dicke Rahmen, Pillen-Etiketten | Abril Fatface / Poppins |
| 8 | Brutalist | Raster, Foto im Kasten mit versetztem Schatten | harte Rahmen und Schatten, Markierung | Archivo Black / Space Grotesk |
| 9 | Luxus Gerahmt | Vollbild-Foto im Doppelrahmen, zentriert | Doppelrahmen, ◆-Ornamente, Versalien | Cinzel / Montserrat |
| 10 | Organisch Weich | Foto in fließender Form, Farbfleck | organische Bildformen, sehr rund | Quicksand / Nunito |

Farbkonzepte: 1 Gold Noir, 2 Champagner, 3 Rosé, 4 Salbei, 5 Schwarz-Weiß, 6 Midnight, 7 Anthrazit & Kupfer,
8 Smaragd, 9 Terracotta, 10 Lavendel.

Erweitern in `generator/designs.py`: Designs sind CSS-Ergänzungen (`design.css`, wird zuletzt geladen; `{HERO_IMG}` =
Titelbild = erstes Galeriebild), Farbkonzepte sind Paletten (Akzent muss stark zum Hintergrund kontrastieren).

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
