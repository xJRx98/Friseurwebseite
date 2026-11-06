# Vorschau-Webseite + Angebot aus einem Google-Maps-Link

```
cd ~/Programmieren/Friseurwebseite
GOOGLE_MAPS_API_KEY=<Schlüssel> .venv/bin/python generator/erstelle_webseite.py "<Google-Maps-Link>" --excel <salon.xlsx>
```
Link und Excel sind jeweils optional (mindestens eins von beiden). `--nicht-oeffnen` unterdrückt das automatische Öffnen.

## Designs (10 zur Auswahl)
`--design <1–10 oder Name>` wählt ein Design (oder Feld „Design“ im Blatt Grunddaten der Excel), Standard 1.
`--alle-designs` erzeugt zusätzlich alle 10 Varianten unter `vorschau/<salon>/designs/` (Bilder geteilt) sowie
`designauswahl.html` und `designauswahl.pdf` mit Vorschaubildern (Startseite + Leistungen) zum Vorlegen beim Kunden.

| Nr. | Design | Stil | Schriften |
|---|---|---|---|
| 1 | Gold Noir | dunkel, Gold (Original) | Cormorant Garamond / Jost |
| 2 | Champagner Hell | Creme, dunkles Gold | Cormorant Garamond / Jost |
| 3 | Rosé Blush | Rosé, feminin | Playfair Display / Lato |
| 4 | Salbei Natur | Salbeigrün, natürlich | Lora / Nunito Sans |
| 5 | Nordic Minimal | Schwarz-Weiß, reduziert | Manrope / Inter |
| 6 | Midnight Blau | Nachtblau, heller Akzent | DM Serif Display / DM Sans |
| 7 | Barber Industrial | Anthrazit, Kupfer (Barbershop) | Oswald / Barlow |
| 8 | Smaragd Luxus | Smaragdgrün, Gold | Cinzel / Montserrat |
| 9 | Terracotta Boho | Sand, Terrakotta | Fraunces / Work Sans |
| 10 | Lavendel Modern | Lavendel, kreativ | Josefin Sans / Karla |

Neue Designs: Eintrag in `generator/designs.py` ergänzen (Akzentfarbe muss stark zum Hintergrund kontrastieren,
weil Text auf Schaltflächen die Hintergrundfarbe nutzt).

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
