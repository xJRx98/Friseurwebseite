"""10 Designs (Aufbau, Formen, Typografie, Schriften) x 10 Farbkonzepte für die Friseur-Vorlage.

Angewendet auf eine Kopie der Webseite, die Vorlage selbst bleibt unverändert:
  - Farbkonzept: ersetzt die Farbvariablen und die festen Farbwerte der Vorlage (Gold mit Transparenz, Linien,
    Navigations- und Hero-Hintergrund). Regel: Akzent und Hintergrund kontrastieren stark, weil Text auf
    Schaltflächen die Hintergrundfarbe (--dark) nutzt.
  - Design: ersetzt die Schriften und hängt design.css an (nach allen anderen Styles, gewinnt also), die Aufbau und
    Formen ändert. {HERO_IMG} wird durch das Titelbild ersetzt (erstes Galerie-Bild bzw. images/salon.png)."""
import os
import re

FARBEN = [
    dict(key="gold-noir", name="Gold Noir", text_de="Dunkel mit Gold – edel und klassisch.", mode="dark",
         black="#111010", dark="#1a1815", mid="#2e2b27", text="#e8e2d9", muted="#a09890",
         accent="#c9a96e", accent_light="#e8d5b0", accent_dark="#9a7a4a"),
    dict(key="champagner", name="Champagner", text_de="Creme mit dunklem Gold – hell und warm.", mode="light",
         black="#f1ebe1", dark="#faf7f2", mid="#ece4d8", text="#2b2622", muted="#6f665c",
         accent="#8a6a3a", accent_light="#b8955f", accent_dark="#6b5029"),
    dict(key="rose", name="Rosé", text_de="Zartes Rosé mit Beerenton – feminin.", mode="light",
         black="#f6eae8", dark="#fcf7f6", mid="#f1e0dd", text="#3a2a2a", muted="#7d6766",
         accent="#a8505a", accent_light="#c97b84", accent_dark="#843a43"),
    dict(key="salbei", name="Salbei", text_de="Salbeigrün und Leinen – natürlich und ruhig.", mode="light",
         black="#e9ece3", dark="#f5f5f0", mid="#e2e6da", text="#26302a", muted="#5f6b62",
         accent="#4e6e52", accent_light="#7f9c82", accent_dark="#3a553e"),
    dict(key="schwarz-weiss", name="Schwarz-Weiß", text_de="Reines Schwarz-Weiß – klar und zeitlos.", mode="light",
         black="#f2f2f2", dark="#ffffff", mid="#ebebeb", text="#111111", muted="#666666",
         accent="#111111", accent_light="#444444", accent_dark="#000000"),
    dict(key="midnight", name="Midnight", text_de="Nachtblau mit hellem Blau – modern und seriös.", mode="dark",
         black="#0b1120", dark="#111a2e", mid="#1b2742", text="#e6ebf5", muted="#94a0b8",
         accent="#9cc3ff", accent_light="#c6dcff", accent_dark="#6f9de0"),
    dict(key="anthrazit-kupfer", name="Anthrazit & Kupfer", text_de="Anthrazit mit Kupfer – markant, ideal für Barbershops.",
         mode="dark", black="#0e0e0e", dark="#171717", mid="#262626", text="#ededed", muted="#9a9a9a",
         accent="#d07a45", accent_light="#e8a77d", accent_dark="#a65a2c"),
    dict(key="smaragd", name="Smaragd", text_de="Tiefes Smaragdgrün mit Gold – luxuriös.", mode="dark",
         black="#07130e", dark="#0d1f17", mid="#173129", text="#eaf2ec", muted="#9db5a7",
         accent="#d8b24a", accent_light="#ead18a", accent_dark="#a88626"),
    dict(key="terracotta", name="Terracotta", text_de="Sand und Terrakotta – warm und lebendig.", mode="light",
         black="#f3e8dc", dark="#fbf6f0", mid="#eedfcf", text="#3b2a20", muted="#7d6253",
         accent="#a94d28", accent_light="#cf7b56", accent_dark="#843918"),
    dict(key="lavendel", name="Lavendel", text_de="Lavendel und Violett – frisch und kreativ.", mode="light",
         black="#efeaf8", dark="#f9f7fd", mid="#e7e0f4", text="#2a2340", muted="#6e6585",
         accent="#5e43a0", accent_light="#8d75c9", accent_dark="#45307d"),
]

ROUND = ".btn-primary,.btn-outline,.btn-dark,.nav-cta,.submit-btn,.btn-next,.time-slot"
BOXES = ".card,.review-card,.booking-panel,.sidebar-card"
IMGS = ".img-placeholder,.about-img-wrap,.gallery-img,.gallery-item,.team-member-img,.map-container"
LINE = "color-mix(in srgb, var(--gold) 25%, transparent)"

DESIGNS = [
    dict(key="klassik", name="Klassik Elegant",
         text_de="Text auf Farbverlauf, feine Linien, klassische Serifenschrift – zeitlos und edel.",
         head="Cormorant Garamond", body="Jost",
         gfonts="family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@300;400;500",
         css=""),
    dict(key="modern-split", name="Modern Split",
         text_de="Geteilter Startbereich mit großem Foto, runde Formen, weiche Schatten – freundlich und modern.",
         head="Manrope", body="Inter", gfonts="family=Manrope:wght@400;600;700;800&family=Inter:wght@300;400;500",
         css=f"""
.hero-pattern,.hero-glow,.hero-scroll{{display:none}}
.hero-bg{{background:var(--dark)}}
.hero-content{{max-width:52%}}
.hero::after{{content:"";position:absolute;right:0;top:calc(var(--nav-height) + 2rem);bottom:2rem;width:44%;
  background:url('{{HERO_IMG}}') center/cover;border-radius:32px 0 0 32px;box-shadow:0 30px 60px rgba(0,0,0,.18)}}
.hero-title,.section-title{{font-weight:800;letter-spacing:-0.03em}}
.hero-title em,.section-title em{{font-style:normal}}
.section-label{{text-transform:none;letter-spacing:.02em;font-weight:600;font-size:.85rem}}
nav{{border-bottom:none;box-shadow:0 4px 24px rgba(0,0,0,.08)}}
.nav-links a{{text-transform:none;letter-spacing:0;font-size:.92rem}}
{ROUND}{{border-radius:999px!important}}
{BOXES}{{border-radius:20px;border-color:transparent!important;box-shadow:0 12px 32px rgba(0,0,0,.10)}}
{IMGS}{{border-radius:20px;overflow:hidden}}
.services-grid{{border:none;gap:1rem;padding:2rem 5vw}}
.service-item{{border:none!important;border-radius:20px;background:var(--mid)}}
.divider{{height:4px;width:48px;border-radius:4px}}
input,select,textarea{{border-radius:12px!important}}
@media (max-width:900px){{.hero::after{{width:100%;border-radius:0;opacity:.18;top:0;bottom:0}}.hero-content{{max-width:100%}}}}"""),
    dict(key="bold", name="Bold Statement",
         text_de="Vollbild-Foto, zentrierte Großbuchstaben, kräftige Rahmen – selbstbewusst und markant.",
         head="Oswald", body="Barlow", gfonts="family=Oswald:wght@400;500;600&family=Barlow:wght@300;400;500;600",
         css=f"""
.hero{{justify-content:center;text-align:center}}
.hero-bg{{background:linear-gradient(rgba(0,0,0,.55),rgba(0,0,0,.7)),url('{{HERO_IMG}}') center/cover}}
.hero-pattern,.hero-glow{{display:none}}
.hero-content{{max-width:960px;margin:0 auto}}
.hero-title{{text-transform:uppercase;font-weight:600;letter-spacing:.02em;color:#fff;font-size:clamp(3rem,8vw,6.5rem)}}
.hero-title em{{font-style:normal;color:color-mix(in srgb, var(--gold) 55%, #fff)}}
.hero-eyebrow{{color:color-mix(in srgb, var(--gold) 55%, #fff)}}
.hero-subtitle{{margin-left:auto;margin-right:auto;color:rgba(255,255,255,.85)}}
.hero-scroll{{color:rgba(255,255,255,.7)}}
.section-title,.page-hero h1{{text-transform:uppercase;letter-spacing:.03em;font-weight:600}}
.section-title em{{font-style:normal}}
.section-label{{font-weight:600}}
{ROUND}{{border-width:2px!important;font-weight:600!important;letter-spacing:.14em!important}}
{BOXES}{{border:none!important;border-left:4px solid var(--gold)!important}}
.divider{{height:3px;width:90px}}
.service-item:hover{{background:var(--gold)!important}}
.service-item:hover .service-name,.service-item:hover .service-desc{{color:var(--dark)!important}}
.nav-logo{{text-transform:uppercase;letter-spacing:.12em;font-weight:500}}"""),
    dict(key="boutique", name="Boutique Bogen",
         text_de="Bilder in Torbogen-Form, Pillen-Schaltflächen, feine Verzierungen – verspielt und hochwertig.",
         head="Playfair Display", body="Lato", gfonts="family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Lato:wght@300;400;700",
         css=f"""
.hero-pattern,.hero-glow{{display:none}}
.hero-content{{max-width:55%}}
.hero::after{{content:"";position:absolute;right:7vw;top:calc(var(--nav-height) + 7vh);bottom:9vh;width:min(32vw,440px);
  background:url('{{HERO_IMG}}') center/cover;border-radius:999px 999px 0 0;
  box-shadow:0 0 0 12px var(--dark),0 0 0 13px var(--gold)}}
.hero-title em,.section-title em{{font-style:italic}}
.about-img-wrap,.team-member-img,.gallery-item,.gallery-img{{border-radius:999px 999px 0 0;overflow:hidden}}
{BOXES}{{border-radius:28px}}
{ROUND}{{border-radius:999px!important}}
.section-label::before{{content:"✦  "}}
.divider{{width:140px;background:linear-gradient(to right,transparent,var(--gold),transparent)}}
.services-grid{{border:none;gap:1.5rem;padding:2.5rem 5vw}}
.service-item{{border:1px solid {LINE}!important;border-radius:200px 200px 28px 28px;padding-top:3rem}}
.map-container,input,select,textarea{{border-radius:18px!important}}
@media (max-width:900px){{.hero::after{{display:none}}.hero-content{{max-width:100%}}}}"""),
    dict(key="editorial", name="Minimal Editorial",
         text_de="Große Schrift wie in einem Magazin, viel Weißraum, nur Linien, Schwarz-Weiß-Bilder – reduziert und modern.",
         head="Bodoni Moda", body="Inter", gfonts="family=Bodoni+Moda:ital,wght@0,400;0,500;1,400&family=Inter:wght@300;400;500;600",
         css=f"""
.hero{{align-items:flex-end;padding-bottom:12vh}}
.hero-bg{{background:var(--dark)}}
.hero-pattern,.hero-glow,.hero-scroll{{display:none}}
.hero-content{{max-width:1100px}}
.hero-title{{font-size:clamp(3.8rem,9vw,8.5rem);line-height:.95;letter-spacing:-0.03em;font-weight:400}}
.hero-title em{{color:var(--text);text-decoration:underline;text-decoration-color:var(--gold);
  text-decoration-thickness:3px;text-underline-offset:12px}}
.hero::after{{content:"";position:absolute;right:5vw;top:calc(var(--nav-height) + 6vh);width:20vw;aspect-ratio:3/4;
  background:url('{{HERO_IMG}}') center/cover;filter:grayscale(1)}}
nav{{border-bottom:1px solid var(--text)}}
.nav-links a{{color:var(--text)}}
.section-title{{font-size:clamp(2.4rem,5vw,4.2rem);letter-spacing:-0.02em;font-weight:400}}
.section-label{{font-weight:600;color:var(--text)}}
.divider{{display:none}}
{BOXES}{{background:transparent!important;border:none!important;border-top:1px solid var(--text)!important;padding-left:0;padding-right:0}}
.services-grid{{border:none!important;border-top:1px solid var(--text)!important;border-bottom:1px solid var(--text)!important}}
.btn-primary{{background:var(--text)!important;color:var(--dark)!important}}
.btn-outline{{border-color:var(--text)!important;color:var(--text)!important}}
.gallery-img img,.team-member-img img,.about-img-wrap img,.gallery-item img{{filter:grayscale(1);transition:filter .5s}}
.gallery-img:hover img,.team-member-img:hover img,.about-img-wrap:hover img,.gallery-item:hover img{{filter:none}}
@media (max-width:900px){{.hero::after{{display:none}}}}"""),
    dict(key="glass", name="Glass Soft",
         text_de="Weichgezeichnetes Foto, Inhalte auf Glasflächen, sanfte Unschärfe – leicht und zeitgemäß.",
         head="Plus Jakarta Sans", body="Plus Jakarta Sans", gfonts="family=Plus+Jakarta+Sans:wght@300;400;600;700;800",
         css=f"""
.hero{{justify-content:center;text-align:center}}
.hero-bg{{background:linear-gradient(color-mix(in srgb,var(--dark) 55%,transparent),color-mix(in srgb,var(--dark) 70%,transparent)),
  url('{{HERO_IMG}}') center/cover;filter:blur(5px);transform:scale(1.06)}}
.hero-pattern,.hero-scroll{{display:none}}
.hero-glow{{width:520px;height:520px;left:8%;right:auto;background:radial-gradient(circle,color-mix(in srgb,var(--gold) 45%,transparent) 0%,transparent 70%)}}
.hero-content{{max-width:820px;margin:0 auto;padding:3rem 3.5rem;border-radius:30px;
  background:color-mix(in srgb,var(--mid) 45%,transparent);backdrop-filter:blur(18px);
  border:1px solid color-mix(in srgb,var(--text) 18%,transparent);box-shadow:0 30px 80px rgba(0,0,0,.2)}}
.hero-subtitle{{margin:0 auto 1rem}}
.hero-title,.section-title{{font-weight:700;letter-spacing:-0.02em}}
.hero-title em,.section-title em{{font-style:normal}}
nav{{background:color-mix(in srgb,var(--dark) 60%,transparent)!important;backdrop-filter:blur(20px);border-bottom:1px solid color-mix(in srgb,var(--text) 10%,transparent)}}
.nav-links a{{text-transform:none;letter-spacing:0;font-size:.92rem}}
{BOXES}{{background:color-mix(in srgb,var(--mid) 60%,transparent)!important;backdrop-filter:blur(14px);border-radius:24px;
  border:1px solid color-mix(in srgb,var(--text) 12%,transparent)!important}}
{ROUND}{{border-radius:14px!important}}
{IMGS}{{border-radius:24px;overflow:hidden}}
.services-grid{{border:none;gap:1rem;padding:2rem 5vw}}
.service-item{{border:1px solid color-mix(in srgb,var(--text) 12%,transparent)!important;border-radius:22px;
  background:color-mix(in srgb,var(--mid) 55%,transparent)}}
input,select,textarea{{border-radius:12px!important}}"""),
    dict(key="retro", name="Retro Salon",
         text_de="Rundes Foto mit dickem Ring, Streifen und Pillen-Etiketten – fröhlich mit 70er-Charme.",
         head="Abril Fatface", body="Poppins", gfonts="family=Abril+Fatface&family=Poppins:wght@300;400;500;600",
         css=f"""
.hero-pattern,.hero-glow{{display:none}}
.hero-bg{{background:linear-gradient(to top,var(--gold) 0 14px,var(--mid) 14px 28px,var(--gold-light) 28px 42px,var(--dark) 42px)}}
.hero-content{{max-width:55%}}
.hero::after{{content:"";position:absolute;right:8vw;top:50%;transform:translateY(-42%);width:min(30vw,420px);aspect-ratio:1;
  border-radius:50%;background:url('{{HERO_IMG}}') center/cover;border:10px solid var(--gold);box-shadow:0 0 0 18px var(--mid)}}
.hero-title{{font-weight:400}}
.hero-title em,.section-title em{{font-style:normal;text-shadow:3px 3px 0 color-mix(in srgb,var(--gold) 30%,transparent)}}
.section-title{{font-weight:400}}
.section-label{{display:inline-block;background:var(--gold);color:var(--dark);padding:.25rem .9rem;border-radius:999px;font-weight:600}}
{ROUND}{{border-radius:999px!important;border:3px solid var(--gold)!important;font-weight:600!important}}
{BOXES}{{border-radius:28px;border:3px solid var(--gold)!important}}
{IMGS}{{border-radius:28px;overflow:hidden;border:3px solid var(--gold)}}
.divider{{height:10px;width:90px;background:repeating-linear-gradient(135deg,var(--gold) 0 6px,transparent 6px 12px)}}
.services-grid{{border:none!important;gap:1rem;padding:2rem 5vw}}
.service-item{{border:3px solid var(--gold)!important;border-radius:28px}}
@media (max-width:900px){{.hero::after{{display:none}}.hero-content{{max-width:100%}}}}"""),
    dict(key="brutalist", name="Brutalist",
         text_de="Harte Rahmen, versetzte Schatten, Raster und Markierungen – laut, mutig und unverwechselbar.",
         head="Archivo Black", body="Space Grotesk",
         gfonts="family=Archivo+Black&family=Space+Grotesk:wght@300;400;500;700&family=Space+Mono:wght@400;700",
         css=f"""
nav{{border-bottom:3px solid var(--text)}}
.hero-bg{{background:var(--dark)}}
.hero-glow,.hero-scroll{{display:none}}
.hero-pattern{{opacity:.09;background-image:linear-gradient(var(--text) 1px,transparent 1px),linear-gradient(90deg,var(--text) 1px,transparent 1px);background-size:48px 48px}}
.hero-content{{max-width:60%}}
.hero::after{{content:"";position:absolute;right:6vw;top:calc(var(--nav-height) + 9vh);width:28vw;aspect-ratio:4/5;
  background:url('{{HERO_IMG}}') center/cover;border:3px solid var(--text);box-shadow:14px 14px 0 var(--gold)}}
.hero-title,.section-title{{text-transform:uppercase;letter-spacing:-0.01em;line-height:.98;font-weight:400}}
.hero-title em,.section-title em{{font-style:normal;background:var(--gold);color:var(--dark);padding:0 .15em}}
.section-label,.hero-eyebrow{{font-family:'Space Mono',monospace;text-transform:uppercase;color:var(--text)}}
{BOXES}{{border:3px solid var(--text)!important;box-shadow:8px 8px 0 var(--text);border-radius:0}}
{ROUND}{{border:3px solid var(--text)!important;box-shadow:4px 4px 0 var(--text);border-radius:0!important}}
{IMGS}{{border:3px solid var(--text)}}
.services-grid{{border:3px solid var(--text)!important}}
.service-item{{border-right:3px solid var(--text)!important}}
.divider{{height:6px;width:100px}}
@media (max-width:900px){{.hero::after{{display:none}}.hero-content{{max-width:100%}}}}"""),
    dict(key="luxus-gerahmt", name="Luxus Gerahmt",
         text_de="Vollbild-Foto im Doppelrahmen, Ornamente, Versalien – wie ein Luxushotel.",
         head="Cinzel", body="Montserrat", gfonts="family=Cinzel:wght@400;500;600&family=Montserrat:wght@300;400;500",
         css=f"""
.hero{{justify-content:center;text-align:center}}
.hero-bg{{background:linear-gradient(color-mix(in srgb,var(--dark) 72%,transparent),color-mix(in srgb,var(--dark) 85%,transparent)),
  url('{{HERO_IMG}}') center/cover}}
.hero-pattern,.hero-glow{{display:none}}
.hero::before{{content:"";position:absolute;inset:calc(var(--nav-height) + 2.5rem) 2.5rem 2.5rem;border:1px solid var(--gold);
  outline:1px solid color-mix(in srgb,var(--gold) 45%,transparent);outline-offset:-10px;z-index:1;pointer-events:none}}
.hero-content{{margin:0 auto;max-width:860px}}
.hero-subtitle{{margin-left:auto;margin-right:auto}}
.hero-title{{text-transform:uppercase;letter-spacing:.06em;font-weight:400;font-size:clamp(2.6rem,6vw,5rem)}}
.hero-title em,.section-title em{{font-style:normal;color:var(--gold)}}
.section-title{{text-transform:uppercase;letter-spacing:.06em;font-weight:400}}
.divider{{width:160px;position:relative;overflow:visible}}
.divider::after{{content:"◆";position:absolute;left:50%;top:50%;transform:translate(-50%,-55%);color:var(--gold);
  background:var(--dark);padding:0 .5rem;font-size:.7rem;line-height:1}}
{IMGS}{{outline:1px solid var(--gold);outline-offset:8px}}
{BOXES}{{border:1px solid var(--gold)!important;outline:1px solid color-mix(in srgb,var(--gold) 35%,transparent);outline-offset:-8px}}
{ROUND}{{letter-spacing:.22em!important}}
.nav-logo{{text-transform:uppercase;letter-spacing:.14em}}
footer{{border-top:3px double var(--gold)!important}}"""),
    dict(key="organisch", name="Organisch Weich",
         text_de="Bilder in fließenden Formen, weiche Farbflecken, runde Schrift – natürlich und herzlich.",
         head="Quicksand", body="Nunito", gfonts="family=Quicksand:wght@400;500;600;700&family=Nunito:wght@300;400;600",
         css=f"""
.hero-pattern,.hero-scroll{{display:none}}
.hero-bg{{background:var(--dark)}}
.hero-glow{{width:560px;height:560px;right:4vw;background:color-mix(in srgb,var(--gold) 18%,transparent);
  border-radius:42% 58% 63% 37% / 41% 44% 56% 59%}}
.hero-content{{max-width:55%}}
.hero::after{{content:"";position:absolute;right:8vw;top:calc(var(--nav-height) + 8vh);bottom:10vh;width:min(32vw,440px);
  background:url('{{HERO_IMG}}') center/cover;border-radius:62% 38% 46% 54% / 60% 44% 56% 40%;box-shadow:0 30px 60px rgba(0,0,0,.15)}}
.hero-title,.section-title{{font-weight:700;letter-spacing:-0.01em}}
.hero-title em,.section-title em{{font-style:normal}}
.section-label{{text-transform:none;letter-spacing:.03em;font-weight:600;font-size:.9rem}}
{IMGS}{{border-radius:46% 54% 42% 58% / 52% 40% 60% 48%;overflow:hidden}}
.map-container{{border-radius:32px!important}}
{BOXES}{{border-radius:32px;border:none!important;background:var(--mid)}}
{ROUND}{{border-radius:999px!important}}
.divider{{height:6px;width:60px;border-radius:6px}}
.services-grid{{border:none!important;gap:1.2rem;padding:2.5rem 5vw}}
.service-item{{border:none!important;border-radius:36px;background:var(--mid)}}
input,select,textarea{{border-radius:16px!important}}
@media (max-width:900px){{.hero::after{{display:none}}.hero-content{{max-width:100%}}}}"""),
]


def _pick(items, key_or_nr, label):
    k = str(key_or_nr or "").strip().lower().removesuffix(".0")
    if not k:
        return items[0]
    if k.isdigit() and 1 <= int(k) <= len(items):
        return items[int(k) - 1]
    for d in items:
        if k in (d["key"], d["name"].lower()):
            return d
    raise SystemExit(f"{label} '{key_or_nr}' unbekannt. Verfügbar: " +
                     ", ".join(f"{i + 1}={d['key']}" for i, d in enumerate(items)))


def get_design(v):
    return _pick(DESIGNS, v, "Design")


EIGENE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eigene_farben.json")


def eigene_farben():
    import json
    try:
        return json.load(open(EIGENE, encoding="utf-8"))
    except (OSError, ValueError):
        return []


def speichere_eigene(f):
    import json
    alle = [x for x in eigene_farben() if x["key"] != f["key"]] + [f]
    json.dump(alle, open(EIGENE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def get_farbe(v):
    k = str(v or "").strip().lower()
    for f in eigene_farben():
        if k in (f["key"], f["name"].lower()):
            return f
    return _pick(FARBEN, v, "Farbkonzept")


def _lum(hex_):
    r, g, b = (int(hex_.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lin = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def kontrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def _mix(a, b, t):
    ca = [int(a.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    cb = [int(b.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(ca, cb))


def eigene_farbe(name, hintergrund, text, akzent, abschnitt=None, flaeche=None, gedaempft=None):
    """Eigenes Farbkonzept aus 3 Grundfarben; Abstufungen werden abgeleitet, wenn nicht angegeben."""
    light = _lum(hintergrund) > 0.4
    key = "eigen-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    black = abschnitt or _mix(hintergrund, "#000000", 0.05 if light else 0.30)          # Abschnitte: etwas dunkler
    mid = flaeche or (_mix(hintergrund, "#000000", 0.08) if light else _mix(hintergrund, "#ffffff", 0.10))  # Karten
    return dict(key=key, name=name, text_de="Eigenes Farbkonzept.", mode="light" if light else "dark",
                dark=hintergrund, black=black, mid=mid, text=text,
                muted=gedaempft or _mix(text, hintergrund, 0.42), accent=akzent,
                accent_light=_mix(akzent, "#ffffff", 0.35), accent_dark=_mix(akzent, "#000000", 0.25))


def _rgb(hex_):
    h = hex_.lstrip("#")
    return ",".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def apply(out, design, farbe, hero_img="images/salon.png"):
    """Design + Farbkonzept auf die Webseiten-Kopie in out anwenden."""
    f = farbe
    acc, dark, line = _rgb(f["accent"]), _rgb(f["dark"]), ("255,255,255" if f["mode"] == "dark" else "0,0,0")
    for fn in os.listdir(out):
        if not fn.endswith((".html", ".css", ".js")) or fn in ("config.js", "design.css"):
            continue
        p = os.path.join(out, fn)
        s = open(p, encoding="utf-8").read()
        s = re.sub(r"rgba\(\s*201\s*,\s*169\s*,\s*110\s*,", f"rgba({acc},", s)
        s = re.sub(r"rgba\(\s*255\s*,\s*255\s*,\s*255\s*,", f"rgba({line},", s)
        s = re.sub(r"rgba\(\s*26\s*,\s*24\s*,\s*21\s*,", f"rgba({dark},", s)
        s = s.replace("#0d0c0a", f["black"]).replace("#1e1b16", f["dark"]).replace("#2a2419", f["mid"])
        s = s.replace("'Cormorant Garamond'", f"'{design['head']}'").replace("'Jost'", f"'{design['body']}'")
        if fn == "style.css":
            s = re.sub(r"@import url\('https://fonts\.googleapis\.com/css2\?[^']+'\);",
                       f"@import url('https://fonts.googleapis.com/css2?{design['gfonts']}&display=swap');", s)
            for var, val in (("gold", f["accent"]), ("gold-light", f["accent_light"]), ("gold-dark", f["accent_dark"]),
                             ("black", f["black"]), ("dark", f["dark"]), ("mid", f["mid"]), ("text", f["text"]),
                             ("text-muted", f["muted"]), ("cream", f["dark"] if f["mode"] == "light" else "#f5f0e8")):
                s = re.sub(rf"--{var}:\s*#[0-9a-fA-F]{{3,6}};", f"--{var}: {val};", s, count=1)
        if fn.endswith(".html") and 'href="design.css"' not in s:
            s = s.replace("</head>", '  <link rel="stylesheet" href="design.css">\n</head>', 1)
        open(p, "w", encoding="utf-8").write(s)
    css = f"/* Design: {design['name']} */\n" + design["css"].replace("{HERO_IMG}", hero_img)
    open(os.path.join(out, "design.css"), "w", encoding="utf-8").write(css)
