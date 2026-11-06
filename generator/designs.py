"""10 Designs für die Friseur-Vorlage: Farbpalette + Schriftpaar, angewendet auf eine Kopie der Webseite.

Die Vorlage nutzt die Variablen --black/--dark/--mid nur als Hintergründe und --dark auch als Text auf der
Akzentfarbe (--gold). Deshalb gilt für jedes Design: Akzent und Hintergrund müssen stark kontrastieren. Feste Werte der
Vorlage (Gold mit Transparenz, weiße Linien, Navigations- und Hero-Hintergrund, Schriftnamen) werden mit ersetzt."""
import os
import re

DESIGNS = [
    dict(key="gold-noir", name="Gold Noir", text_de="Elegant und dunkel mit Gold – das Original.",
         mode="dark", black="#111010", dark="#1a1815", mid="#2e2b27", text="#e8e2d9", muted="#a09890",
         accent="#c9a96e", accent_light="#e8d5b0", accent_dark="#9a7a4a",
         head="Cormorant Garamond", body="Jost",
         gfonts="family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@300;400;500"),
    dict(key="champagner", name="Champagner Hell", text_de="Hell, edel und warm – Creme mit dunklem Gold.",
         mode="light", black="#f1ebe1", dark="#faf7f2", mid="#ece4d8", text="#2b2622", muted="#6f665c",
         accent="#8a6a3a", accent_light="#b8955f", accent_dark="#6b5029",
         head="Cormorant Garamond", body="Jost",
         gfonts="family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@300;400;500"),
    dict(key="rose", name="Rosé Blush", text_de="Zart und feminin – Rosé mit klassischer Serifenschrift.",
         mode="light", black="#f6eae8", dark="#fcf7f6", mid="#f1e0dd", text="#3a2a2a", muted="#7d6766",
         accent="#a8505a", accent_light="#c97b84", accent_dark="#843a43",
         head="Playfair Display", body="Lato",
         gfonts="family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Lato:wght@300;400;700"),
    dict(key="salbei", name="Salbei Natur", text_de="Natürlich und ruhig – Salbeigrün für Naturkosmetik-Salons.",
         mode="light", black="#e9ece3", dark="#f5f5f0", mid="#e2e6da", text="#26302a", muted="#5f6b62",
         accent="#4e6e52", accent_light="#7f9c82", accent_dark="#3a553e",
         head="Lora", body="Nunito Sans",
         gfonts="family=Lora:ital,wght@0,400;0,600;1,400&family=Nunito+Sans:wght@300;400;600"),
    dict(key="nordic", name="Nordic Minimal", text_de="Klar und reduziert – Schwarz-Weiß, moderne Grotesk.",
         mode="light", black="#f2f2f2", dark="#ffffff", mid="#ebebeb", text="#111111", muted="#666666",
         accent="#111111", accent_light="#444444", accent_dark="#000000",
         head="Manrope", body="Inter",
         gfonts="family=Manrope:wght@300;400;600;700&family=Inter:wght@300;400;500"),
    dict(key="midnight", name="Midnight Blau", text_de="Modern und seriös – Nachtblau mit hellem Akzent.",
         mode="dark", black="#0b1120", dark="#111a2e", mid="#1b2742", text="#e6ebf5", muted="#94a0b8",
         accent="#9cc3ff", accent_light="#c6dcff", accent_dark="#6f9de0",
         head="DM Serif Display", body="DM Sans",
         gfonts="family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500"),
    dict(key="barber", name="Barber Industrial", text_de="Kantig und markant – Anthrazit mit Kupfer, ideal für Barbershops.",
         mode="dark", black="#0e0e0e", dark="#171717", mid="#262626", text="#ededed", muted="#9a9a9a",
         accent="#d07a45", accent_light="#e8a77d", accent_dark="#a65a2c",
         head="Oswald", body="Barlow",
         gfonts="family=Oswald:wght@300;400;600&family=Barlow:wght@300;400;500"),
    dict(key="smaragd", name="Smaragd Luxus", text_de="Luxuriös – tiefes Smaragdgrün mit Gold.",
         mode="dark", black="#07130e", dark="#0d1f17", mid="#173129", text="#eaf2ec", muted="#9db5a7",
         accent="#d8b24a", accent_light="#ead18a", accent_dark="#a88626",
         head="Cinzel", body="Montserrat",
         gfonts="family=Cinzel:wght@400;600&family=Montserrat:wght@300;400;500"),
    dict(key="terracotta", name="Terracotta Boho", text_de="Warm und lebendig – Terrakotta und Sand.",
         mode="light", black="#f3e8dc", dark="#fbf6f0", mid="#eedfcf", text="#3b2a20", muted="#7d6253",
         accent="#a94d28", accent_light="#cf7b56", accent_dark="#843918",
         head="Fraunces", body="Work Sans",
         gfonts="family=Fraunces:ital,wght@0,300;0,500;1,300&family=Work+Sans:wght@300;400;500"),
    dict(key="lavendel", name="Lavendel Modern", text_de="Frisch und kreativ – Lavendel mit klarer, runder Schrift.",
         mode="light", black="#efeaf8", dark="#f9f7fd", mid="#e7e0f4", text="#2a2340", muted="#6e6585",
         accent="#5e43a0", accent_light="#8d75c9", accent_dark="#45307d",
         head="Josefin Sans", body="Karla",
         gfonts="family=Josefin+Sans:ital,wght@0,300;0,400;0,600;1,300&family=Karla:wght@300;400;500"),
]


def get(key_or_nr):
    k = str(key_or_nr or "").strip().lower().removesuffix(".0")
    if not k:
        return DESIGNS[0]
    if k.isdigit() and 1 <= int(k) <= len(DESIGNS):
        return DESIGNS[int(k) - 1]
    for d in DESIGNS:
        if k in (d["key"], d["name"].lower()):
            return d
    raise SystemExit(f"Design '{key_or_nr}' unbekannt. Verfügbar: " +
                     ", ".join(f"{i + 1}={d['key']}" for i, d in enumerate(DESIGNS)))


def _rgb(hex_):
    h = hex_.lstrip("#")
    return ",".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def apply(out, d):
    """Design d auf die Webseiten-Kopie in out anwenden (style.css, *.html, components.js)."""
    acc, dark, line = _rgb(d["accent"]), _rgb(d["dark"]), ("255,255,255" if d["mode"] == "dark" else "0,0,0")
    files = [f for f in os.listdir(out) if f.endswith((".html", ".css", ".js")) and f != "config.js"]
    for f in files:
        p = os.path.join(out, f)
        s = open(p, encoding="utf-8").read()
        s = re.sub(r"rgba\(\s*201\s*,\s*169\s*,\s*110\s*,", f"rgba({acc},", s)
        s = re.sub(r"rgba\(\s*255\s*,\s*255\s*,\s*255\s*,", f"rgba({line},", s)
        s = re.sub(r"rgba\(\s*26\s*,\s*24\s*,\s*21\s*,", f"rgba({dark},", s)
        s = s.replace("#0d0c0a", d["black"]).replace("#1e1b16", d["dark"]).replace("#2a2419", d["mid"])
        s = s.replace("'Cormorant Garamond'", f"'{d['head']}'").replace("'Jost'", f"'{d['body']}'")
        if f == "style.css":
            s = re.sub(r"@import url\('https://fonts\.googleapis\.com/css2\?[^']+'\);",
                       f"@import url('https://fonts.googleapis.com/css2?{d['gfonts']}&display=swap');", s)
            for var, val in (("gold", d["accent"]), ("gold-light", d["accent_light"]), ("gold-dark", d["accent_dark"]),
                             ("black", d["black"]), ("dark", d["dark"]), ("mid", d["mid"]), ("text", d["text"]),
                             ("text-muted", d["muted"]), ("cream", d["dark"] if d["mode"] == "light" else "#f5f0e8")):
                s = re.sub(rf"--{var}:\s*#[0-9a-fA-F]{{3,6}};", f"--{var}: {val};", s, count=1)
        open(p, "w", encoding="utf-8").write(s)
