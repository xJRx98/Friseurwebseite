"""Vorschau-Webseite + Angebots-PDF für einen Friseursalon aus einem Google-Maps-Link.

  python3 generator/erstelle_webseite.py "<Google-Maps-Link>"

- Daten über die offizielle Google Places API (New): Umgebungsvariable GOOGLE_MAPS_API_KEY. Ohne Schlüssel wird der
  Name aus dem Link übernommen und der Rest mit Platzhaltern gefüllt.
- Ergebnis: vorschau/<salon>/ (Kopie der Vorlage mit eigener config.js, für Suchmaschinen gesperrt) und
  vorschau/<salon>/angebot.pdf (Pakete aus generator/angebot.json). Öffnet beides am Ende.
Hinweis: Google-Fotos/-Bewertungen nur für die Vorschau (mit Quellenangabe); für die echte Seite liefert der Salon
eigene Fotos und Texte. Impressum/Datenschutz müssen mit den Angaben des Inhabers vervollständigt werden."""
import html, json, os, re, shutil, subprocess, sys, urllib.parse
from datetime import date

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import designs  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")
DAYS = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def resolve(link):
    """Kurzlinks auflösen; Name und Koordinaten aus der Maps-URL lesen."""
    url = link
    if "goo.gl" in link or "g.co" in link:
        url = requests.get(link, allow_redirects=True, timeout=20).url
        q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        url = q.get("continue", [url])[0]
    url = urllib.parse.unquote(url)
    name = re.search(r"/place/([^/@]+)", url)
    name = name.group(1).replace("+", " ") if name else ""
    m = re.search(r"!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)", url) or re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)", url)
    return name, (float(m.group(1)), float(m.group(2))) if m else None


def places(name, loc):
    h = {"X-Goog-Api-Key": KEY, "X-Goog-FieldMask": "places.id"}
    body = {"textQuery": name, "languageCode": "de"}
    if loc:
        body["locationBias"] = {"circle": {"center": {"latitude": loc[0], "longitude": loc[1]}, "radius": 300.0}}
    r = requests.post("https://places.googleapis.com/v1/places:searchText", headers=h, json=body, timeout=20)
    r.raise_for_status()
    pid = r.json()["places"][0]["id"]
    fields = ("id,displayName,formattedAddress,addressComponents,nationalPhoneNumber,internationalPhoneNumber,"
              "regularOpeningHours,rating,userRatingCount,reviews,photos,googleMapsUri,websiteUri")
    r = requests.get(f"https://places.googleapis.com/v1/places/{pid}", params={"languageCode": "de"},
                     headers={"X-Goog-Api-Key": KEY, "X-Goog-FieldMask": fields}, timeout=20)
    r.raise_for_status()
    return r.json()


def slugify(s):
    s = s.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:50] or "salon"


def build_config(name, p, out):
    comp = {t: c.get("longText", "") for c in p.get("addressComponents", []) for t in c.get("types", [])}
    street = (comp.get("route", "") + " " + comp.get("street_number", "")).strip()
    city = comp.get("locality", "")
    hours = []
    for line in p.get("regularOpeningHours", {}).get("weekdayDescriptions", []):
        d, _, t = line.partition(": ")
        hours.append({"day": d, "time": t.replace("Geschlossen", "Geschlossen")})
    hours = hours or [{"day": d, "time": "bitte ergänzen"} for d in DAYS]
    intl = re.sub(r"\D", "", p.get("internationalPhoneNumber", ""))
    rating, count = str(p.get("rating", "")), str(p.get("userRatingCount", ""))
    reviews = []
    for rv in p.get("reviews", [])[:3]:
        n = rv.get("authorAttribution", {}).get("displayName", "Gast").split()
        reviews.append({"text": (rv.get("text") or {}).get("text", "")[:400],
                        "name": n[0] + (f" {n[-1][0]}." if len(n) > 1 else ""),
                        "date": rv.get("relativePublishTimeDescription", ""), "stars": int(rv.get("rating", 5))})
    gallery = []
    for i, ph in enumerate(p.get("photos", [])[:6]):
        try:
            img = requests.get(f"https://places.googleapis.com/v1/{ph['name']}/media",
                               params={"maxWidthPx": 1600, "key": KEY}, timeout=30).content
            fn = f"images/google_{i + 1}.jpg"
            open(os.path.join(out, fn), "wb").write(img)
            gallery.append({"src": fn, "alt": f"{name} (Foto: Google)", "category": "salon", "tag": "Salon"})
        except Exception:
            pass
    maps_q = urllib.parse.quote(p.get("formattedAddress", name))
    cfg = {
        "SALON_NAME": name, "TAGLINE": "Ihr Friseur in " + (city or "Ihrer Nähe") + ".", "GRUENDUNGSJAHR": "vielen Jahren",
        "STADT": city, "ADDRESS_STREET": street, "ADDRESS_ZIP": comp.get("postal_code", ""), "ADDRESS_CITY": city,
        "PHONE": p.get("nationalPhoneNumber", ""), "EMAIL": "", "WHATSAPP": intl if intl.startswith("491") else "",
        "INSTAGRAM_HANDLE": "", "INSTAGRAM_URL": "#", "FACEBOOK_URL": "#",
        "MAPS_EMBED_URL": f"https://www.google.com/maps?q={maps_q}&output=embed",
        "MAPS_LINK": p.get("googleMapsUri", f"https://maps.google.com/?q={maps_q}"),
        "GOOGLE_REVIEWS_URL": p.get("googleMapsUri", ""), "GOOGLE_RATING": rating, "GOOGLE_REVIEW_COUNT": count,
        "HOURS": hours,
        "TEAM": [{"name": "Unser Team", "role": "Friseurinnen & Friseure", "photo": "images/team.png",
                  "bio": f"Bei {name} nehmen wir uns Zeit für Ihre Beratung – vom klassischen Schnitt bis zur Farbe.",
                  "quote": "Wir freuen uns auf Ihren Besuch.", "tags": ["Schnitt", "Farbe", "Styling"], "isOwner": True}],
        "STATS": [{"number": rating or "–", "label": "Google-Bewertung"}, {"number": count or "–", "label": "Bewertungen"},
                  {"number": str(sum(1 for h in hours if "Geschlossen" not in h["time"])), "label": "Tage geöffnet"},
                  {"number": "1", "label": "Salon in " + (city or "der Stadt")}],
        "REVIEWS": reviews or [{"text": "Hier erscheinen Ihre Google-Bewertungen.", "name": "", "date": "", "stars": 5}],
        "IMPRESSUM": {"INHABER_NAME": "[Inhaber ergänzen]", "BERUFSBEZEICHNUNG": "[ergänzen]", "KAMMER": "[ergänzen]",
                      "UST_ID": "[ergänzen]", "REGISTERGERICHT": "", "REGISTERNUMMER": "", "STAND": date.today().strftime("%m/%Y")},
        "FOOTER_DESC": f"{name} – Ihr Friseursalon in {city}.", "BOOKING_STYLISTS": ["Unser Team"], "JOBS_EMAIL": "",
        "GALLERY": gallery or None,          # None = Bilder der Vorlage
        "SERVICES": None,                    # None = Leistungen der Vorlage (Beispielpreise)
    }
    return cfg


def finalize(cfg, google, changed):
    """Abgeleitete Felder nach dem Einlesen der Excel neu setzen (Karte, Texte mit Ort)."""
    city = cfg.get("ADDRESS_CITY") or cfg.get("STADT", "")
    cfg["STADT"] = cfg.get("STADT") or city
    addr = ", ".join(x for x in (cfg.get("ADDRESS_STREET", ""), f"{cfg.get('ADDRESS_ZIP', '')} {city}".strip()) if x)
    if addr and (not google or "ADDRESS_STREET" in changed):
        q = urllib.parse.quote(f"{cfg['SALON_NAME']}, {addr}")
        cfg["MAPS_EMBED_URL"] = f"https://www.google.com/maps?q={q}&output=embed"
        cfg["MAPS_LINK"] = f"https://maps.google.com/?q={q}"
    if "FOOTER_DESC" not in changed:
        cfg["FOOTER_DESC"] = f"{cfg['SALON_NAME']} – Ihr Friseursalon in {city}." if city else f"{cfg['SALON_NAME']} – Ihr Friseursalon."
    if "TAGLINE" not in changed and city:
        cfg["TAGLINE"] = f"Ihr Friseur in {city}."
    for st in cfg.get("STATS", []):
        if st.get("label", "").startswith("Salon in"):
            st["label"] = "Salon in " + (city or "der Stadt")


def prepare_pages(target, cfg, design, farbe):
    """config.js schreiben, Vorschau sperren (noindex), Design + Farbkonzept anwenden, Schriften lokal einbinden."""
    write_config(cfg, target)
    for f in os.listdir(target):
        if f.endswith(".html"):
            fp = os.path.join(target, f)
            s = open(fp, encoding="utf-8").read()
            if 'name="robots"' not in s:
                s = s.replace("<head>", '<head>\n  <meta name="robots" content="noindex,nofollow">', 1)
            open(fp, "w", encoding="utf-8").write(s)
    hero = (cfg.get("GALLERY") or [{"src": "images/salon.png"}])[0]["src"]
    designs.apply(target, design, farbe, hero)
    localize_fonts(target)


def shot(html_file, png, size="1280,1700"):
    """Bildschirmfoto; Einblend-Animationen dafür abgeschaltet (temporäre Kopie der Seite)."""
    tmp = os.path.join(os.path.dirname(html_file), "_shot_" + os.path.basename(html_file))
    s = open(html_file, encoding="utf-8").read().replace(
        "</head>", "<style>.fade-in{opacity:1!important;transform:none!important}"
                   "*{animation-delay:0s!important;animation-duration:0s!important}</style></head>", 1)
    open(tmp, "w", encoding="utf-8").write(s)
    try:
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars", f"--window-size={size}",
                        "--virtual-time-budget=4000", f"--screenshot={png}", "file://" + tmp],
                       capture_output=True, timeout=120)
    finally:
        os.remove(tmp)


def _variant(out, base, name, cfg, design, farbe):
    v = os.path.join(base, name)
    os.makedirs(v)
    for f in os.listdir(ROOT):
        if f.endswith((".html", ".css", ".js")):
            shutil.copy(os.path.join(ROOT, f), v)
    os.symlink(os.path.relpath(os.path.join(out, "images"), v), os.path.join(v, "images"))
    prepare_pages(v, cfg, design, farbe)
    png, png2 = os.path.join(base, name + ".png"), os.path.join(base, name + "-leistungen.png")
    shot(os.path.join(v, "index.html"), png, "1280,820")
    shot(os.path.join(v, "leistungen.html"), png2, "1280,1400")
    return os.path.relpath(png, out), os.path.relpath(png2, out), os.path.relpath(os.path.join(v, "index.html"), out)


def all_designs(out, cfg, design, farbe):
    """Auswahl für den Kunden: Teil A die Designs (im gewählten Farbkonzept), Teil B die 10 Farbkonzepte (im
    gewählten Design). Varianten unter out/designs/ (Bilder geteilt), Übersicht als HTML + PDF."""
    base = os.path.join(out, "designs")
    if os.path.exists(base):
        shutil.rmtree(base)
    os.makedirs(base)

    def card(nr, title, text, sub, imgs, swatches):
        img, img2, link = imgs
        sw = "".join(f"<span style=background:{c}></span>" for c in swatches)
        return (f"<div class='c'><a href='{link}'><img src='{img}'><img class='l' src='{img2}'></a>"
                f"<h2>{nr}. {html.escape(title)}</h2><p>{html.escape(text)}</p><p class='f'>{html.escape(sub)}</p>"
                f"<div class='sw'>{sw}</div></div>")

    part_a = []
    for i, d in enumerate(designs.DESIGNS, 1):
        imgs = _variant(out, base, f"design-{i}-{d['key']}", cfg, d, farbe)
        part_a.append(card(i, d["name"], d["text_de"], f"Schriften: {d['head']} / {d['body']}", imgs,
                           (farbe["dark"], farbe["mid"], farbe["accent"], farbe["text"])))
        print(f"  Design {i} {d['name']} fertig", flush=True)
    part_b = []
    for i, f in enumerate(designs.FARBEN, 1):
        imgs = _variant(out, base, f"farbe-{i:02d}-{f['key']}", cfg, design, f)
        part_b.append(card(i, f["name"], f["text_de"], "hell" if f["mode"] == "light" else "dunkel", imgs,
                           (f["dark"], f["mid"], f["accent"], f["text"])))
        print(f"  Farbkonzept {i:2d} {f['name']} fertig", flush=True)
    doc = f"""<!doctype html><html lang="de"><meta charset="utf-8"><title>Designauswahl {html.escape(cfg['SALON_NAME'])}</title>
<style>body{{font-family:Helvetica,Arial,sans-serif;margin:32px;color:#222}} h1{{margin:0 0 4px}} .sub{{color:#666;margin-bottom:20px}}
h3{{margin:28px 0 4px;font-size:16pt}} .part{{page-break-before:always}}
.g{{display:grid;grid-template-columns:1fr 1fr;gap:22px}} .c{{border:1px solid #ddd;border-radius:8px;padding:12px;page-break-inside:avoid}}
.c img{{width:100%;aspect-ratio:1280/820;object-fit:cover;object-position:top;border-radius:4px;border:1px solid #eee}}
.c img.l{{aspect-ratio:1280/520;object-position:0 70%;margin-top:6px}}
.c h2{{font-size:14pt;margin:8px 0 2px}} .c p{{margin:2px 0;font-size:10pt}} .f{{color:#777}}
.sw span{{display:inline-block;width:26px;height:16px;margin:6px 4px 0 0;border:1px solid #ccc;border-radius:3px}}</style>
<h1>Designauswahl für {html.escape(cfg['SALON_NAME'])}</h1>
<div class="sub">Wählen Sie <b>ein Design</b> (Aufbau, Formen, Schriften) und <b>ein Farbkonzept</b> – beides ist frei kombinierbar.
Bild anklicken für die Vorschau mit Ihren Inhalten. Bitte nennen Sie uns beide Nummern, z. B. „Design 2, Farbe 4“.</div>
<h3>A · {len(designs.DESIGNS)} Designs <span style="font-weight:normal;color:#777">(gezeigt im Farbkonzept {html.escape(farbe['name'])})</span></h3>
<div class="g">{''.join(part_a)}</div>
<div class="part"><h3>B · {len(designs.FARBEN)} Farbkonzepte <span style="font-weight:normal;color:#777">(gezeigt im Design {html.escape(design['name'])})</span></h3>
<div class="g">{''.join(part_b)}</div></div></html>"""
    sel = os.path.join(out, "designauswahl.html")
    open(sel, "w", encoding="utf-8").write(doc)
    pdf = os.path.join(out, "designauswahl.pdf")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}",
                    "--virtual-time-budget=3000", "file://" + sel], capture_output=True, timeout=120)
    return sel, pdf


def write_config(cfg, out):
    tpl = open(os.path.join(ROOT, "config.js"), encoding="utf-8").read()
    js = "/* Automatisch erzeugt (generator/erstelle_webseite.py) – VORSCHAU */\nconst SALON_CONFIG = {\n"
    for k, v in cfg.items():
        if k in ("GALLERY", "SERVICES") and v is None:
            continue
        js += f"  {k}: {json.dumps(v, ensure_ascii=False, indent=2)},\n"
    js += "  YEAR: new Date().getFullYear(),\n"
    if cfg.get("GALLERY") is None:
        js += "  " + tpl[tpl.index("GALLERY:"):tpl.index("],", tpl.index("GALLERY:")) + 2] + "\n"
    if cfg.get("SERVICES") is None:
        js += tpl[tpl.index("  SERVICES:"):tpl.index("  // ── IMPRESSUM")]
    js += "};\n"
    open(os.path.join(out, "config.js"), "w", encoding="utf-8").write(js)


def localize_fonts(out):
    """Google-Schriften herunterladen und lokal einbinden (Datenschutz: keine Verbindung zu Google beim Besuch)."""
    css_path = os.path.join(out, "style.css")
    css = open(css_path, encoding="utf-8").read()
    m = re.search(r"@import url\('(https://fonts\.googleapis\.com/[^']+)'\);", css)
    if not m:
        return False
    ua = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
    try:
        fcss = requests.get(m.group(1), headers=ua, timeout=20).text
        os.makedirs(os.path.join(out, "fonts"), exist_ok=True)
        for n, url in enumerate(sorted(set(re.findall(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", fcss)))):
            fn = f"font_{n + 1}.woff2"
            open(os.path.join(out, "fonts", fn), "wb").write(requests.get(url, timeout=30).content)
            fcss = fcss.replace(url, fn)
        open(os.path.join(out, "fonts", "fonts.css"), "w", encoding="utf-8").write(fcss)
        open(css_path, "w", encoding="utf-8").write(css.replace(m.group(0), "@import url('fonts/fonts.css');"))
        return True
    except requests.RequestException as e:
        print("Schriften nicht lokal eingebunden (bleiben bei Google):", e)
        return False


def offer_pdf(cfg, out):
    a = json.load(open(os.path.join(ROOT, "generator", "angebot.json"), encoding="utf-8"))
    rows = "".join(
        f"<div class='p'><h2>{html.escape(p['name'])}</h2><div class='price'>{html.escape(p['preis'])}</div>"
        f"<ul>{''.join(f'<li>{html.escape(x)}</li>' for x in p['leistungen'])}</ul></div>" for p in a["pakete"])
    addr = ", ".join(x for x in (cfg["ADDRESS_STREET"], f"{cfg['ADDRESS_ZIP']} {cfg['ADDRESS_CITY']}".strip()) if x)
    extras = "".join(f"<tr><td>{html.escape(e[0])}</td><td>{html.escape(e[1])}</td></tr>" for e in a["extras"])
    doc = f"""<!doctype html><html lang="de"><meta charset="utf-8"><style>
body{{font-family:Helvetica,Arial,sans-serif;color:#222;margin:40px;font-size:11pt}} h1{{color:#9a7a4a;margin:0}}
.sub{{color:#666;margin-bottom:24px}} .grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
.p{{border:1px solid #ddd;border-radius:8px;padding:14px;page-break-inside:avoid}} .p h2{{margin:0;font-size:14pt}}
.price{{font-size:15pt;font-weight:bold;color:#9a7a4a;margin:6px 0}} li{{margin:3px 0}} table{{width:100%;border-collapse:collapse}}
td{{border-bottom:1px solid #eee;padding:5px}} .small{{color:#666;font-size:9pt;margin-top:20px}}</style>
<p>{html.escape(a['anbieter'])}</p><h1>Angebot: Webseite für {html.escape(cfg['SALON_NAME'])}</h1>
<div class="sub">{html.escape(addr + " · " if addr else "")}Datum {date.today():%d.%m.%Y} · gültig {a['gueltig_tage']} Tage</div>
<p>Vielen Dank für Ihr Interesse. Eine Vorschau Ihrer neuen Webseite haben wir bereits erstellt (7 Seiten: Start, Leistungen
& Preise, Team, Galerie, Termin, Kontakt, Impressum/Datenschutz). Wählen Sie das passende Paket:</p>
<div class="grid">{rows}</div><h3>Zusatzleistungen</h3><table>{extras}</table>
<p class="small">{html.escape(a['hinweis'])}</p></html>"""
    h = os.path.join(out, "angebot.html")
    open(h, "w", encoding="utf-8").write(doc)
    pdf = os.path.join(out, "angebot.pdf")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}",
                    "file://" + h], capture_output=True, timeout=120)
    return pdf


def erstelle(link="", excel=None, design=None, farbe=None, alle=False, api_key=None, log=print):
    """Webseite (+ optional Kundenauswahl) erzeugen. farbe: Nummer/Name oder ein eigenes Farbkonzept (dict).
    Gibt ein dict mit den Pfaden zurück (out, index, angebot, auswahl, auswahl_pdf, name, design, farbe)."""
    global KEY
    if api_key is not None:
        KEY = api_key
    if not link and not excel:
        raise ValueError("Bitte einen Google-Maps-Link und/oder eine Excel-Datei angeben.")
    excel_name = ""
    if excel:
        from openpyxl import load_workbook
        ws = load_workbook(excel, data_only=True)["Grunddaten"]
        excel_name = next((str(r[2]).strip() for r in ws.iter_rows(min_row=3, values_only=True)
                           if r[0] == "SALON_NAME" and r[2]), "")
    name, loc = resolve(link) if link else ("", None)
    p = {}
    if KEY and link:
        p = places(name or link, loc)
        name = p.get("displayName", {}).get("text", name)
        log(f"Google-Daten geladen: {name}")
    else:
        log("Hinweis: keine Google-Daten (Schlüssel oder Link fehlt) – Name aus Link/Excel, Rest aus Excel oder Platzhalter.")
    name = excel_name or name or "Ihr Salon"
    out = os.path.join(ROOT, "vorschau", slugify(name))
    if os.path.exists(out):
        shutil.rmtree(out)
    shutil.copytree(ROOT, out, ignore=shutil.ignore_patterns(".git", "vorschau", "generator", "README.md", ".venv",
                                                            "*.command", ".gitignore"))
    cfg = build_config(name, p, out)
    if excel:
        from excel_daten import apply_excel
        changed = apply_excel(excel, cfg, out)
        log(f"Aus Excel übernommen: {', '.join(changed) if changed else 'nichts (Datei leer?)'}")
        finalize(cfg, google=bool(p), changed=changed)
    design = designs.get_design(design or cfg.get("DESIGN", ""))
    farbe = farbe if isinstance(farbe, dict) else designs.get_farbe(farbe or cfg.get("FARBE", ""))
    cfg.pop("DESIGN", None); cfg.pop("FARBE", None)
    prepare_pages(out, cfg, design, farbe)
    log(f"Design: {design['name']}, Farbkonzept: {farbe['name']}")
    pdf = offer_pdf(cfg, out)
    res = dict(out=out, index=os.path.join(out, "index.html"), angebot=pdf, name=name,
               design=design["name"], farbe=farbe["name"])
    if alle:
        res["auswahl"], res["auswahl_pdf"] = all_designs(out, cfg, design, farbe)
    return res


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Vorschau-Webseite + Angebot aus Google-Maps-Link und/oder Excel")
    ap.add_argument("link", nargs="?", default="", help="Google-Maps-Link des Salons (optional mit --excel)")
    ap.add_argument("--excel", help="ausgefüllte Salon-Daten (Vorlage: generator/excel_daten.py vorlage)")
    ap.add_argument("--nicht-oeffnen", action="store_true", help="Vorschau und PDF nicht automatisch öffnen")
    ap.add_argument("--design", help="Design 1–10 oder Name (Standard: aus Excel, sonst 1 Klassik Elegant)")
    ap.add_argument("--farbe", help="Farbkonzept 1–10, Name oder eigenes (aus eigene_farben.json)")
    ap.add_argument("--alle-designs", action="store_true",
                    help="Kundenauswahl: 10 Designs + 10 Farbkonzepte als Übersicht/PDF")
    args = ap.parse_args()
    link = args.link or ("" if args.excel else input("Google-Maps-Link: ").strip())
    try:
        res = erstelle(link, args.excel, args.design, args.farbe, args.alle_designs)
    except ValueError as e:
        sys.exit(str(e))
    print(f"Vorschau: {res['index']}\nAngebot:  {res['angebot']}")
    to_open = [res["index"], res["angebot"]]
    if args.alle_designs:
        print(f"Designauswahl: {res['auswahl']}\nDesignauswahl-PDF: {res['auswahl_pdf']}")
        to_open = [res["auswahl"], res["auswahl_pdf"], res["angebot"]]
    if sys.platform == "darwin" and not args.nicht_oeffnen:
        for f in to_open:
            if os.path.exists(f):
                subprocess.run(["open", f])


if __name__ == "__main__":
    main()
