"""Standardisierte Excel-Datei für die Salon-Daten: Vorlage erzeugen und einlesen.

  python generator/excel_daten.py vorlage [Zieldatei.xlsx]    # leere Vorlage (mit Beispielen/Hinweisen)

Einlesen macht erstelle_webseite.py --excel <Datei>. Regeln:
  - Blatt „Grunddaten“/„Impressum“: nur ausgefüllte Werte überschreiben Google-Daten bzw. Platzhalter.
  - Listen-Blätter (Öffnungszeiten, Team, Leistungen, Galerie, Kennzahlen, Bewertungen): sobald mindestens eine Zeile
    ausgefüllt ist, ersetzt das Blatt die Liste vollständig; leere Blätter ändern nichts.
  - Bilder (Team/Galerie): Dateiname oder Pfad; relative Pfade gelten ab dem Ordner der Excel-Datei.
"""
import os
import sys

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

GRUNDDATEN = [  # (Schlüssel, Bezeichnung, Hinweis)
    ("DESIGN", "Design (Nummer 1–10)", "1 Gold Noir, 2 Champagner Hell, 3 Rosé Blush, 4 Salbei Natur, 5 Nordic Minimal, "
                                          "6 Midnight Blau, 7 Barber Industrial, 8 Smaragd Luxus, 9 Terracotta Boho, 10 Lavendel Modern"),
    ("SALON_NAME", "Name des Salons", "leer = Name aus Google"),
    ("TAGLINE", "Slogan", "z. B. „Schönheit beginnt mit dem richtigen Schnitt.“"),
    ("GRUENDUNGSJAHR", "Gründungsjahr", "z. B. 2014 – erscheint als „Seit 2014 …“"),
    ("STADT", "Stadt (für Texte)", "leer = aus der Adresse"),
    ("ADDRESS_STREET", "Straße und Hausnummer", "leer = aus Google"),
    ("ADDRESS_ZIP", "PLZ", "leer = aus Google"),
    ("ADDRESS_CITY", "Ort", "leer = aus Google"),
    ("PHONE", "Telefon", "leer = aus Google"),
    ("EMAIL", "E-Mail", "Kontakt-E-Mail des Salons"),
    ("WHATSAPP", "WhatsApp-Nummer", "nur Ziffern mit Ländervorwahl, z. B. 4917612345678"),
    ("INSTAGRAM_HANDLE", "Instagram-Name", "z. B. @salonname"),
    ("INSTAGRAM_URL", "Instagram-Link", "https://www.instagram.com/…"),
    ("FACEBOOK_URL", "Facebook-Link", "https://www.facebook.com/…"),
    ("JOBS_EMAIL", "E-Mail für Bewerbungen", "leer = Kontakt-E-Mail"),
    ("FOOTER_DESC", "Kurzbeschreibung (Fußzeile)", "1–2 Sätze"),
    ("GOOGLE_RATING", "Google-Bewertung", "leer = aus Google"),
    ("GOOGLE_REVIEW_COUNT", "Anzahl Bewertungen", "leer = aus Google"),
]
IMPRESSUM = [
    ("INHABER_NAME", "Inhaber/in (vollständiger Name)", "Pflicht"),
    ("BERUFSBEZEICHNUNG", "Berufsbezeichnung", "z. B. Friseurmeisterin"),
    ("KAMMER", "Zuständige Kammer", "z. B. Handwerkskammer für München und Oberbayern"),
    ("UST_ID", "USt-IdNr.", "falls vorhanden"),
    ("REGISTERGERICHT", "Registergericht", "nur bei Eintragung (GmbH, UG, e.K. …)"),
    ("REGISTERNUMMER", "Registernummer", "nur bei Eintragung"),
]
LISTS = {
    "Öffnungszeiten": (["Tag", "Zeit"], [[d, ""] for d in ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag",
                                                                "Samstag", "Sonntag"]],
                       "Zeit z. B. „9:00 – 18:00“ oder „Geschlossen“. Leer lassen = aus Google."),
    "Team": (["Name", "Rolle", "Foto (Datei)", "Kurzbeschreibung", "Zitat", "Schwerpunkte (Komma)", "Inhaber (ja/nein)"],
             [["Lisa Muster", "Friseurmeisterin & Inhaberin", "lisa.jpg", "Seit 15 Jahren …", "…", "Balayage, Brautstyling", "ja"]],
             "Beispielzeile überschreiben oder löschen. Foto: Datei im Ordner der Excel (oder voller Pfad)."),
    "Leistungen": (["Bereich", "Bereich-Titel", "Spalte (links/rechts)", "Leistung", "Preis",
                    "Varianten (z. B. kurz: ab 45 €; lang: ab 65 €)", "Hinweis zum Bereich"],
                   [["schnitt", "Schnitt & Styling", "links", "Herren – Waschen & Schneiden", "ab 29 €", "", ""]],
                   "Bereich: schnitt, farbe, pflege, braut (oder eigener). Preis ODER Varianten ausfüllen."),
    "Galerie": (["Bild (Datei)", "Beschreibung", "Kategorie", "Etikett"], [],
                "Kategorie z. B. schnitt, farbe, braut, salon. Leer = Google-Fotos bzw. Vorlagenbilder."),
    "Kennzahlen": (["Zahl", "Beschriftung"], [], "Genau 4 Zeilen empfohlen, z. B. „15+ | Jahre Erfahrung“."),
    "Bewertungen": (["Text", "Name", "Datum", "Sterne (1–5)"], [], "Leer = Google-Bewertungen."),
}
HEAD = PatternFill("solid", fgColor="C9A96E")


def _sheet_kv(wb, title, rows, intro):
    ws = wb.create_sheet(title)
    ws.append([intro]); ws["A1"].font = Font(italic=True, color="666666")
    ws.append(["Schlüssel", "Bezeichnung", "Wert", "Hinweis"])
    for c in ws[2]:
        c.font, c.fill = Font(bold=True), HEAD
    for k, label, hint in rows:
        ws.append([k, label, "", hint])
    for col, w in zip("ABCD", (20, 34, 48, 60)):
        ws.column_dimensions[col].width = w
    ws.column_dimensions["A"].hidden = False


def _sheet_list(wb, title, header, examples, intro):
    ws = wb.create_sheet(title)
    ws.append([intro]); ws["A1"].font = Font(italic=True, color="666666")
    ws.append(header)
    for c in ws[2]:
        c.font, c.fill = Font(bold=True), HEAD
        c.alignment = Alignment(wrap_text=True)
    for r in examples:
        ws.append(r)
    for i in range(len(header)):
        ws.column_dimensions[chr(65 + i)].width = 28 if i else 22
    return ws


def create_template(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Anleitung"
    for line in ["Salon-Daten für die Webseite", "",
                 "1. Pro Salon eine Kopie dieser Datei ausfüllen.",
                 "2. Nur ausfüllen, was bekannt ist – leere Felder werden aus Google übernommen oder bleiben Platzhalter.",
                 "3. Listen (Team, Leistungen, Galerie …): sobald eine Zeile ausgefüllt ist, ersetzt das Blatt die Liste ganz.",
                 "4. Fotos: Dateien in denselben Ordner wie diese Excel legen und den Dateinamen eintragen.",
                 "5. Aufruf: .venv/bin/python generator/erstelle_webseite.py \"<Maps-Link>\" --excel <diese Datei>",
                 "", "Die Spalte „Schlüssel“ bitte nicht ändern."]:
        ws.append([line])
    ws["A1"].font = Font(bold=True, size=14)
    ws.column_dimensions["A"].width = 110
    _sheet_kv(wb, "Grunddaten", GRUNDDATEN, "Nur die Spalte „Wert“ ausfüllen.")
    _sheet_kv(wb, "Impressum", IMPRESSUM, "Pflichtangaben für das Impressum (vom Inhaber).")
    for title, (header, examples, intro) in LISTS.items():
        ws = _sheet_list(wb, title, header, examples, intro)
        if title == "Leistungen":
            dv = DataValidation(type="list", formula1='"links,rechts"', allow_blank=True)
            ws.add_data_validation(dv); dv.add("C3:C200")
        if title == "Team":
            dv = DataValidation(type="list", formula1='"ja,nein"', allow_blank=True)
            ws.add_data_validation(dv); dv.add("G3:G50")
    wb.save(path)


def _rows(ws, ncols):
    out = []
    for row in ws.iter_rows(min_row=3, values_only=True):
        vals = [("" if v is None else str(v).strip()) for v in list(row)[:ncols]]
        vals += [""] * (ncols - len(vals))
        if any(vals):
            out.append(vals)
    return out


def _img(name, base, out, used):
    """Bild in images/ der Vorschau kopieren; Rückgabe des Pfads relativ zur Webseite (oder leer)."""
    import shutil
    if not name:
        return ""
    src = name if os.path.isabs(name) else os.path.join(base, name)
    if not os.path.exists(src):
        if os.path.exists(os.path.join(out, "images", os.path.basename(name))):
            return "images/" + os.path.basename(name)          # Bild der Vorlage
        print(f"  Bild nicht gefunden: {name}")
        return ""
    fn = os.path.basename(src)
    shutil.copy(src, os.path.join(out, "images", fn))
    used.append(fn)
    return "images/" + fn


def apply_excel(path, cfg, out):
    """Excel-Werte in cfg übernehmen (siehe Regeln oben). Gibt die Liste der geänderten Bereiche zurück."""
    wb = load_workbook(path, data_only=True)
    base, changed, used = os.path.dirname(os.path.abspath(path)), [], []
    for sheet, target in (("Grunddaten", cfg), ("Impressum", cfg["IMPRESSUM"])):
        if sheet in wb.sheetnames:
            for k, _, v, _ in _rows(wb[sheet], 4):
                if k and v:
                    target[k] = v
                    changed.append(k)
    if "Öffnungszeiten" in wb.sheetnames:
        rows = [r for r in _rows(wb["Öffnungszeiten"], 2) if r[1]]
        if rows:
            cfg["HOURS"] = [{"day": d, "time": t} for d, t in rows]
            changed.append("Öffnungszeiten")
    if "Team" in wb.sheetnames:
        rows = [r for r in _rows(wb["Team"], 7) if r[0]]
        if rows:
            cfg["TEAM"] = [{"name": n, "role": ro, "photo": _img(f, base, out, used) or "images/team.png", "bio": b,
                            "quote": q, "tags": [t.strip() for t in tg.split(",") if t.strip()],
                            "isOwner": own.lower() in ("ja", "j", "x", "1", "true")}
                           for n, ro, f, b, q, tg, own in rows]
            cfg["BOOKING_STYLISTS"] = [m["name"] for m in cfg["TEAM"]]
            changed.append("Team")
    if "Leistungen" in wb.sheetnames:
        rows = [r for r in _rows(wb["Leistungen"], 7) if r[3]]
        if rows:
            services = {}
            for key, title, side, name, price, variants, note in rows:
                key = (key or "weitere").lower()
                cat = services.setdefault(key, {"icon": {"schnitt": "✂️", "farbe": "🎨", "pflege": "💆", "braut": "💍"}.get(key, "✨"),
                                                 "title": title or key.capitalize(), "left": [], "right": []})
                if note:
                    cat["note"] = note
                item = {"name": name}
                if variants:
                    item["variants"] = [{"label": a.strip(), "price": b.strip()} for a, _, b in
                                        (v.partition(":") for v in variants.split(";")) if a.strip()]
                else:
                    item["price"] = price
                cat["right" if side.lower().startswith("r") else "left"].append(item)
            cfg["SERVICES"] = services
            changed.append("Leistungen")
    if "Galerie" in wb.sheetnames:
        rows = [r for r in _rows(wb["Galerie"], 4) if r[0]]
        gal = [{"src": s, "alt": d or "Bild", "category": c or "salon", "tag": t or (c or "Salon").capitalize()}
               for s, d, c, t in ((_img(f, base, out, used), d, c, t) for f, d, c, t in rows) if s]
        if gal:
            cfg["GALLERY"] = gal
            changed.append("Galerie")
    if "Kennzahlen" in wb.sheetnames:
        rows = [r for r in _rows(wb["Kennzahlen"], 2) if r[0]]
        if rows:
            cfg["STATS"] = [{"number": n, "label": l} for n, l in rows]
            changed.append("Kennzahlen")
    if "Bewertungen" in wb.sheetnames:
        rows = [r for r in _rows(wb["Bewertungen"], 4) if r[0]]
        if rows:
            cfg["REVIEWS"] = [{"text": t, "name": n, "date": d, "stars": int(float(s or 5))} for t, n, d, s in rows]
            changed.append("Bewertungen")
    if cfg.get("EMAIL") and not cfg.get("JOBS_EMAIL"):
        cfg["JOBS_EMAIL"] = cfg["EMAIL"]
    if cfg.get("ADDRESS_CITY") and not cfg.get("STADT"):
        cfg["STADT"] = cfg["ADDRESS_CITY"]
    return changed


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "vorlage":
        target = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                    "salon_daten_vorlage.xlsx")
        create_template(target)
        print("Vorlage erstellt:", target)
    else:
        print(__doc__)
