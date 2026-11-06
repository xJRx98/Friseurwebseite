"""10 Designs (Aufbau, Formen, Typografie, Schriften) x 10 Farbkonzepte für die Friseur-Vorlage,
abgeleitet aus den Webseiten Münchner Friseure.

Angewendet auf eine Kopie der Webseite, die Vorlage selbst bleibt unverändert:
  - Farbkonzept: ersetzt die Farbvariablen und die festen Farbwerte der Vorlage (Gold mit Transparenz, Linien,
    Navigations- und Hero-Hintergrund). Regel: Akzent und Hintergrund kontrastieren stark, weil Text auf
    Schaltflächen die Hintergrundfarbe (--dark) nutzt.
  - Design: ersetzt die Schriften und hängt design.css an (nach allen anderen Styles, gewinnt also), die Aufbau und
    Formen ändert. {HERO_IMG} wird durch das Titelbild ersetzt (erstes Galerie-Bild bzw. images/salon.png)."""
import os
import re

# Abgeleitet aus 262 Startseiten Münchner Friseure (Gelbe Seiten, November 2026): Hintergrund 44 % weiß, 16 % hell
# getönt, 17 % dunkel; Akzente nach Häufigkeit: keiner (Schwarz-Weiß), Bordeaux, Nude/Champagner, Kupfer/Cognac, Navy,
# Grün/Salbei, Beere/Magenta, Petrol.
FARBEN = [
    dict(key="schwarz-weiss", name="Schwarz-Weiß", text_de="Weiß mit Schwarz – der häufigste Münchner Salon-Look, klar und zeitlos.",
         mode="light", black="#f2f2f2", dark="#ffffff", mid="#ebebeb", text="#111111", muted="#666666",
         accent="#111111", accent_light="#444444", accent_dark="#000000"),
    dict(key="nude", name="Nude & Champagner", text_de="Warmes Creme mit Nude-Braun – weich, hell und hochwertig.", mode="light",
         black="#f2ebe2", dark="#faf6f1", mid="#ece2d6", text="#2e2620", muted="#75685c",
         accent="#86664b", accent_light="#b39577", accent_dark="#664c36"),
    dict(key="bordeaux", name="Bordeaux", text_de="Weiß mit Weinrot – elegant, etabliert, gern bei Meisterbetrieben.", mode="light",
         black="#f4eeec", dark="#fcfaf9", mid="#f0e6e3", text="#2a1d1d", muted="#73605f",
         accent="#7c2234", accent_light="#a5525f", accent_dark="#5a1624"),
    dict(key="cognac", name="Cognac & Creme", text_de="Creme mit Cognac und Kupfer – warm, handwerklich, gemütlich.", mode="light",
         black="#efe6da", dark="#f8f3ec", mid="#eadcca", text="#33261c", muted="#77665a",
         accent="#9a5527", accent_light="#c08458", accent_dark="#743f1b"),
    dict(key="salbei", name="Salbei & Leinen", text_de="Leinen mit Salbeigrün – natürlich, ideal für Natur- und Biofriseure.",
         mode="light", black="#e9ece3", dark="#f6f6f1", mid="#e2e6da", text="#26302a", muted="#5f6b62",
         accent="#4c6a50", accent_light="#7f9c82", accent_dark="#3a553e"),
    dict(key="marine", name="Marineblau", text_de="Weiß mit Marineblau – seriös, frisch und modern.", mode="light",
         black="#eef1f6", dark="#f9fafc", mid="#e6eaf2", text="#1b2238", muted="#5f6880",
         accent="#2e4677", accent_light="#5d77a8", accent_dark="#1f3157"),
    dict(key="beere", name="Beere & Rosé", text_de="Zartes Rosé mit Beerenton – feminin und modisch.", mode="light",
         black="#f6eaee", dark="#fdf8f9", mid="#f2e2e8", text="#33202a", muted="#7a6470",
         accent="#8c2a5c", accent_light="#b85d8a", accent_dark="#681d43"),
    dict(key="gold-noir", name="Gold Noir", text_de="Schwarz mit Gold – edel, für Premium-Salons und Abendstimmung.", mode="dark",
         black="#0f0e0d", dark="#181614", mid="#2a2724", text="#ece6dc", muted="#a39b91",
         accent="#c9a96e", accent_light="#e8d5b0", accent_dark="#9a7a4a"),
    dict(key="anthrazit-kupfer", name="Anthrazit & Kupfer", text_de="Anthrazit mit Kupfer – markant, typisch für Barbershops.",
         mode="dark", black="#0e0e0e", dark="#171717", mid="#262626", text="#ededed", muted="#9a9a9a",
         accent="#d07a45", accent_light="#e8a77d", accent_dark="#a65a2c"),
    dict(key="petrol", name="Petrol & Mint", text_de="Tiefes Petrol mit Mint – ruhig, frisch und eigenständig.", mode="dark",
         black="#0a1d21", dark="#10282d", mid="#1a3a40", text="#e7f1f0", muted="#98b3b2",
         accent="#86cbbd", accent_light="#b6e2d8", accent_dark="#5aa595"),
]

ROUND = ".btn-primary,.btn-outline,.btn-dark,.nav-cta,.submit-btn,.btn-next,.time-slot"
BOXES = ".card,.review-card,.booking-panel,.sidebar-card"
IMGS = ".img-placeholder,.about-img-wrap,.gallery-img,.gallery-item,.team-member-img,.map-container"
LINE = "color-mix(in srgb, var(--gold) 25%, transparent)"
# Text auf Fotos ist immer hell, egal welches Farbkonzept
ON_PHOTO = """.hero-title,.hero-eyebrow{color:#fff}
.hero-title em,.hero-eyebrow{color:color-mix(in srgb,var(--gold) 50%,#fff)}
.hero-subtitle{color:rgba(255,255,255,.86)}
.hero-scroll{color:rgba(255,255,255,.7)}
.hero .btn-outline{color:#fff!important;border-color:rgba(255,255,255,.6)!important}"""

# 10 Stilrichtungen, die auf Münchner Friseur-Webseiten immer wieder vorkommen (nachempfunden, keine Kopie einzelner Seiten)
DESIGNS = [
    dict(key="klassik", name="Klassik Vollbild",
         text_de="Salonfoto über die ganze Breite mit dunklem Verlauf, Text links in Serifenschrift – der häufigste Münchner Stil.",
         head="Playfair Display", body="Open Sans",
         gfonts="family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400&family=Open+Sans:wght@400;500;600",
         css=f"""
.hero-bg{{background:linear-gradient(90deg,rgba(0,0,0,.78) 0%,rgba(0,0,0,.5) 50%,rgba(0,0,0,.12) 100%),url('{{HERO_IMG}}') center/cover}}
.hero-pattern,.hero-glow{{display:none}}
{ON_PHOTO}"""),
    dict(key="hell", name="Hell & Luftig",
         text_de="Viel Weißraum, zentrierter Text in feinen Großbuchstaben, Foto als breites Band – ruhig und modern.",
         head="Josefin Sans", body="Lato", gfonts="family=Josefin+Sans:wght@300;400;600&family=Lato:wght@400;700",
         css=f"""
.hero{{flex-direction:column;justify-content:flex-start;align-items:center;text-align:center;padding-top:calc(var(--nav-height) + 7vh)}}
.hero-bg{{background:var(--dark)}}
.hero-pattern,.hero-glow,.hero-scroll{{display:none}}
.hero-content{{margin:0 auto;max-width:860px}}
.hero-title{{font-size:clamp(2.2rem,4.2vw,3.4rem);font-weight:400;text-transform:uppercase;letter-spacing:.12em;line-height:1.2}}
.hero-title em{{font-style:normal;font-weight:600}}
.hero-subtitle{{margin-left:auto;margin-right:auto}}
.hero-actions{{justify-content:center}}
.hero::after{{content:"";position:absolute;left:5vw;right:5vw;bottom:0;height:33vh;background:url('{{HERO_IMG}}') center 35%/cover}}
nav{{border-bottom:1px solid {LINE}}}
.nav-logo{{text-transform:uppercase;letter-spacing:.3em;font-weight:400;font-size:1.2rem}}
.nav-links a{{text-transform:uppercase;letter-spacing:.14em;font-size:.8rem}}
.section-title{{text-transform:uppercase;letter-spacing:.1em;font-weight:400}}
.section-title em{{font-style:normal;font-weight:600}}
.section-label{{letter-spacing:.35em}}
.divider{{width:40px}}
{BOXES}{{background:transparent!important;border:none!important;border-bottom:1px solid {LINE}!important}}
{ROUND}{{letter-spacing:.24em!important;font-weight:400!important}}
.services-grid{{border:none!important;gap:0}}
.service-item{{border:none!important;border-bottom:1px solid {LINE}!important}}
@media (max-width:900px){{.hero::after{{height:28vh}}}}"""),
    dict(key="modern-split", name="Modern Split",
         text_de="Geteilter Startbereich: Text links, großes Foto rechts, runde Formen, weiche Schatten – freundlich und modern.",
         head="Montserrat", body="Open Sans", gfonts="family=Montserrat:wght@400;600;700;800&family=Open+Sans:wght@300;400;500;600",
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
    dict(key="statement", name="Typo-Statement",
         text_de="Vollbild-Foto, riesige zentrierte Großbuchstaben, kräftige Rahmen – selbstbewusst, für junge Salons.",
         head="Oswald", body="Roboto", gfonts="family=Oswald:wght@400;500;600&family=Roboto:wght@400;500;700",
         css=f"""
.hero{{justify-content:center;text-align:center}}
.hero-bg{{background:linear-gradient(rgba(0,0,0,.55),rgba(0,0,0,.7)),url('{{HERO_IMG}}') center/cover}}
.hero-pattern,.hero-glow{{display:none}}
.hero-content{{max-width:960px;margin:0 auto}}
.hero-title{{text-transform:uppercase;font-weight:600;letter-spacing:.02em;font-size:clamp(2.8rem,6vw,5rem)}}
.hero-title em{{font-style:normal}}
.hero-subtitle{{margin-left:auto;margin-right:auto}}
.hero-actions{{justify-content:center}}
{ON_PHOTO}
.section-title,.page-hero h1{{text-transform:uppercase;letter-spacing:.03em;font-weight:600}}
.section-title em{{font-style:normal}}
.section-label{{font-weight:600}}
{ROUND}{{border-width:2px!important;font-weight:600!important;letter-spacing:.14em!important}}
{BOXES}{{border:none!important;border-left:4px solid var(--gold)!important}}
.divider{{height:3px;width:90px}}
.service-item:hover{{background:var(--gold)!important}}
.service-item:hover .service-name,.service-item:hover .service-desc{{color:var(--dark)!important}}
.nav-logo{{text-transform:uppercase;letter-spacing:.12em;font-weight:500}}"""),
    dict(key="editorial", name="Editorial Schwarz-Weiß",
         text_de="Große Schrift wie in einem Modemagazin, Schwarz-Weiß-Porträt, nur feine Linien – reduziert und urban.",
         head="Bodoni Moda", body="Inter", gfonts="family=Bodoni+Moda:ital,wght@0,400;0,500;1,400&family=Inter:wght@300;400;500;600",
         css=f"""
.hero{{align-items:flex-end;padding-bottom:12vh}}
.hero-bg{{background:var(--dark)}}
.hero-pattern,.hero-glow,.hero-scroll{{display:none}}
.hero-content{{max-width:1100px}}
.hero-title{{font-size:clamp(3rem,6.5vw,5.8rem);line-height:1;letter-spacing:-0.03em;font-weight:400}}
.hero-title em{{color:var(--text);text-decoration:underline;text-decoration-color:var(--gold);
  text-decoration-thickness:3px;text-underline-offset:12px}}
.hero::after{{content:"";position:absolute;right:5vw;top:calc(var(--nav-height) + 6vh);width:20vw;aspect-ratio:3/4;
  background:url('{{HERO_IMG}}') center/cover;filter:grayscale(1)}}
nav{{border-bottom:1px solid var(--text)}}
.nav-links a{{color:var(--text)}}
.section-title{{font-size:clamp(2rem,3.6vw,3rem);letter-spacing:-0.02em;font-weight:400}}
.section-label{{font-weight:600;color:var(--text)}}
.divider{{display:none}}
{BOXES}{{background:transparent!important;border:none!important;border-top:1px solid var(--text)!important;padding-left:0;padding-right:0}}
.services-grid{{border:none!important;border-top:1px solid var(--text)!important;border-bottom:1px solid var(--text)!important}}
.btn-primary{{background:var(--text)!important;color:var(--dark)!important}}
.btn-outline{{border-color:var(--text)!important;color:var(--text)!important}}
.gallery-img img,.team-member-img img,.about-img-wrap img,.gallery-item img{{filter:grayscale(1);transition:filter .5s}}
.gallery-img:hover img,.team-member-img:hover img,.about-img-wrap:hover img,.gallery-item:hover img{{filter:none}}
@media (max-width:900px){{.hero::after{{display:none}}}}"""),
    dict(key="boutique", name="Boutique Handschrift",
         text_de="Salonname in Schreibschrift, Foto im Torbogen, Pillen-Schaltflächen – feminin und persönlich wie ein kleiner Salon.",
         head="Cormorant Garamond", body="Lato",
         gfonts="family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Lato:wght@400;700&family=Great+Vibes",
         css=f"""
.hero-pattern,.hero-glow{{display:none}}
.hero-content{{max-width:55%}}
.hero::after{{content:"";position:absolute;right:7vw;top:calc(var(--nav-height) + 7vh);bottom:9vh;width:min(32vw,440px);
  background:url('{{HERO_IMG}}') center/cover;border-radius:999px 999px 0 0;
  box-shadow:0 0 0 12px var(--dark),0 0 0 13px var(--gold)}}
.hero-title em,.section-title em{{font-family:'Great Vibes',cursive;font-style:normal;font-weight:400;font-size:1.3em;line-height:1}}
.nav-logo,.hero-title,.footer-logo{{font-family:'Great Vibes',cursive;letter-spacing:0;font-weight:400}}
.nav-logo{{font-size:2.1rem}}
.hero-title{{font-size:clamp(3.2rem,6vw,5.2rem);line-height:1.1}}
.about-img-wrap,.team-member-img,.gallery-item,.gallery-img{{border-radius:999px 999px 0 0;overflow:hidden}}
{BOXES}{{border-radius:28px}}
{ROUND}{{border-radius:999px!important}}
.section-label::before{{content:"✦  "}}
.divider{{width:140px;background:linear-gradient(to right,transparent,var(--gold),transparent)}}
.services-grid{{border:none;gap:1.5rem;padding:2.5rem 5vw}}
.service-item{{border:1px solid {LINE}!important;border-radius:200px 200px 28px 28px;padding-top:3rem}}
.map-container,input,select,textarea{{border-radius:18px!important}}
@media (max-width:900px){{.hero::after{{display:none}}.hero-content{{max-width:100%}}}}"""),
    dict(key="barber", name="Barbershop",
         text_de="Dunkles Foto, kräftige Slab-Schrift, Abzeichen und Barber-Streifen – kernig, für Herrenfriseure.",
         head="Alfa Slab One", body="Roboto", gfonts="family=Alfa+Slab+One&family=Roboto:wght@300;400;500;700",
         css=f"""
.hero{{justify-content:center;text-align:center}}
.hero-bg{{background:linear-gradient(rgba(0,0,0,.62),rgba(0,0,0,.8)),url('{{HERO_IMG}}') center/cover}}
.hero-pattern,.hero-glow{{display:none}}
.hero-content{{max-width:900px;margin:0 auto}}
.hero-eyebrow{{display:inline-block;border:2px solid currentColor;border-radius:999px;padding:.45rem 1.3rem}}
.hero-title{{text-transform:uppercase;font-weight:400;letter-spacing:.02em;font-size:clamp(2.8rem,6.5vw,5.4rem)}}
.hero-title em{{font-style:normal}}
.hero-subtitle{{margin-left:auto;margin-right:auto}}
.hero-actions{{justify-content:center}}
{ON_PHOTO}
.hero::after{{content:"";position:absolute;left:0;right:0;bottom:0;height:14px;
  background:repeating-linear-gradient(-45deg,var(--gold) 0 14px,#fff 14px 28px,var(--gold-dark) 28px 42px,#fff 42px 56px)}}
.nav-logo{{text-transform:uppercase;letter-spacing:.06em}}
.section-title,.page-hero h1{{text-transform:uppercase;font-weight:400;letter-spacing:.01em}}
.section-title em{{font-style:normal}}
.section-label{{font-weight:700}}
.section-label::before{{content:"✂  "}}
{BOXES}{{border:2px solid var(--gold)!important;border-radius:6px}}
{ROUND}{{border-radius:4px!important;font-weight:700!important;letter-spacing:.14em!important}}
{IMGS}{{border-radius:6px;overflow:hidden}}
.divider{{height:8px;width:96px;background:repeating-linear-gradient(-45deg,var(--gold) 0 8px,transparent 8px 16px)}}
.service-item:hover{{background:var(--gold)!important}}
.service-item:hover .service-name,.service-item:hover .service-desc{{color:var(--dark)!important}}"""),
    dict(key="natur", name="Natur & Bio",
         text_de="Bilder in fließenden Formen, weiche Farbflächen, warme Serifenschrift – herzlich, für Naturfriseure.",
         head="Lora", body="Nunito", gfonts="family=Lora:ital,wght@0,400;0,500;0,600;1,400&family=Nunito:wght@300;400;600",
         css=f"""
.hero-pattern,.hero-scroll{{display:none}}
.hero-bg{{background:var(--dark)}}
.hero-glow{{width:560px;height:560px;right:4vw;background:color-mix(in srgb,var(--gold) 18%,transparent);
  border-radius:42% 58% 63% 37% / 41% 44% 56% 59%}}
.hero-content{{max-width:55%}}
.hero::after{{content:"";position:absolute;right:8vw;top:calc(var(--nav-height) + 8vh);bottom:10vh;width:min(32vw,440px);
  background:url('{{HERO_IMG}}') center/cover;border-radius:62% 38% 46% 54% / 60% 44% 56% 40%;box-shadow:0 30px 60px rgba(0,0,0,.15)}}
.hero-title,.section-title{{font-weight:500;letter-spacing:-0.01em}}
.section-label{{text-transform:none;letter-spacing:.03em;font-weight:600;font-size:.9rem}}
.section-label::before{{content:"❧ "}}
{IMGS}{{border-radius:46% 54% 42% 58% / 52% 40% 60% 48%;overflow:hidden}}
.map-container{{border-radius:32px!important}}
{BOXES}{{border-radius:32px;border:none!important;background:var(--mid)}}
{ROUND}{{border-radius:999px!important}}
.divider{{height:6px;width:60px;border-radius:6px}}
.services-grid{{border:none!important;gap:1.2rem;padding:2.5rem 5vw}}
.service-item{{border:none!important;border-radius:36px;background:var(--mid)}}
input,select,textarea{{border-radius:16px!important}}
@media (max-width:900px){{.hero::after{{display:none}}.hero-content{{max-width:100%}}}}"""),
    dict(key="luxus-gerahmt", name="Luxus Gerahmt",
         text_de="Vollbild-Foto im Doppelrahmen, Ornamente, Versalien – wie ein Luxushotel, für Premium-Salons.",
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
.hero-actions{{justify-content:center}}
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
    dict(key="freundlich", name="Freundlich & Nah",
         text_de="Großes Foto mit heller Textkarte, Etiketten und runde Karten – nahbar, für den Salon um die Ecke.",
         head="Poppins", body="Open Sans", gfonts="family=Poppins:wght@400;500;600;700&family=Open+Sans:wght@400;500;600",
         css=f"""
.hero{{align-items:flex-end;padding-bottom:9vh}}
.hero-bg{{background:url('{{HERO_IMG}}') center/cover}}
.hero-pattern,.hero-glow,.hero-scroll{{display:none}}
.hero-content{{margin-left:5vw;padding:2.6rem 3rem;max-width:640px;background:var(--dark);border-radius:28px;
  box-shadow:0 30px 70px rgba(0,0,0,.28)}}
.hero-title{{font-size:clamp(2.3rem,4.4vw,3.7rem);font-weight:700;letter-spacing:-0.02em}}
.hero-title em,.section-title em{{font-style:normal}}
.hero-subtitle{{max-width:none}}
.section-title{{font-weight:700;letter-spacing:-0.02em}}
.hero-eyebrow,.section-label{{display:inline-block;background:color-mix(in srgb,var(--gold) 14%,transparent);padding:.3rem .95rem;
  border-radius:999px;text-transform:none;letter-spacing:.02em;font-weight:600;font-size:.85rem}}
.nav-links a{{text-transform:none;letter-spacing:0;font-size:.92rem;font-weight:500}}
nav{{border-bottom:none;box-shadow:0 2px 18px rgba(0,0,0,.08)}}
{ROUND}{{border-radius:12px!important;text-transform:none!important;letter-spacing:.02em!important;font-weight:600!important;font-size:.92rem!important}}
{BOXES}{{border-radius:20px;border:none!important;border-top:4px solid var(--gold)!important;box-shadow:0 10px 30px rgba(0,0,0,.08)}}
{IMGS}{{border-radius:20px;overflow:hidden}}
.services-grid{{border:none!important;gap:1rem;padding:2rem 5vw}}
.service-item{{border:none!important;border-radius:20px;background:var(--mid)}}
.divider{{height:4px;width:44px;border-radius:4px}}
input,select,textarea{{border-radius:12px!important}}
@media (max-width:900px){{.hero-content{{margin:0 4vw;padding:2rem 1.6rem}}}}"""),
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
