/**
 * ============================================================
 *  SALON WEBSITE – ZENTRALE KONFIGURATION
 *  Automatisch generiert aus Webseite_Daten_komplett.xlsx
 *  Stand: 09.04.2026 14:10
 * ============================================================
 */

const SALON_CONFIG = {

  // ── GRUNDDATEN ──────────────────────────────────────────
  SALON_NAME:       "Max Hair Styling",
  TAGLINE:          "Style your life",
  GRUENDUNGSJAHR:   "2023",
  STADT:            "München",
  YEAR:             new Date().getFullYear(),

  // ── KONTAKT ─────────────────────────────────────────────
  ADDRESS_STREET:   "Musterstr. 1",
  ADDRESS_ZIP:      "80331",
  ADDRESS_CITY:     "München",
  PHONE:            "01234 56789",
  EMAIL:            "info@maxhair.de",
  WHATSAPP:         "15737221530",

  // ── SOCIAL MEDIA ─────────────────────────────────────────
  INSTAGRAM_HANDLE: "@maxhair",
  INSTAGRAM_URL:    "",
  FACEBOOK_URL:     "",

  // ── GOOGLE ───────────────────────────────────────────────
  GOOGLE_API_KEY:   "AIKey",
  PLACE_ID:         "ChIJ...",
  MAPS_EMBED_URL:   "",
  MAPS_LINK:        "",
  GOOGLE_REVIEWS_URL: "",
  GOOGLE_RATING:    "4.9",
  GOOGLE_REVIEW_COUNT: "",

  // ── ÖFFNUNGSZEITEN ───────────────────────────────────────
  HOURS: [
    {
        "day": "Montag",
        "time": "Geschlossen"
    },
    {
        "day": "Dienstag",
        "time": "9:00 – 18:00"
    },
    {
        "day": "Mittwoch",
        "time": "9:00 – 18:00"
    },
    {
        "day": "Donnerstag",
        "time": "9:00 – 20:00"
    },
    {
        "day": "Freitag",
        "time": "9:00 – 18:00"
    },
    {
        "day": "Samstag",
        "time": "9:00 – 15:00"
    },
    {
        "day": "Sonntag",
        "time": "Geschlossen"
    }
],

  // ── TEAM ─────────────────────────────────────────────────
  TEAM: [
    {
        "name": "Niko Hair",
        "role": "Meisterin / Inhaberin",
        "photo": "images/team1.jpg",
        "bio": "Testbio",
        "quote": "Ich bin eine Biene",
        "tags": [],
        "isOwner": true
    },
    {
        "name": "Alex Konstatnin",
        "role": "Stylistin",
        "photo": "images/team2.jpg",
        "bio": "",
        "quote": "",
        "tags": [],
        "isOwner": false
    },
    {
        "name": "Hasan Harom",
        "role": "Coloristin",
        "photo": "images/team3.jpg",
        "bio": "",
        "quote": "",
        "tags": [],
        "isOwner": false
    },
    {
        "name": "Imael Sibari",
        "role": "Auszubildende/r",
        "photo": "images/team4.jpg",
        "bio": "",
        "quote": "",
        "tags": [],
        "isOwner": false
    }
],

  // ── KENNZAHLEN ───────────────────────────────────────────
  STATS: [
    {
        "number": "10+",
        "label": "Jahre Erfahrung"
    },
    {
        "number": "4",
        "label": "Teammitglieder"
    },
    {
        "number": "200+",
        "label": "Zufriedene Gäste/Monat"
    },
    {
        "number": "4.9",
        "label": "Google-Bewertung"
    }
],

  // ── GOOGLE BEWERTUNGEN ───────────────────────────────────
  REVIEWS: [],

  // ── GALERIE-BILDER ───────────────────────────────────────
  GALLERY: [
    { src: "images/balayage.png",     alt: "Balayage",      category: "farbe",  tag: "Balayage"      },
    { src: "images/damenschnitt.png", alt: "Damenschnitt",  category: "schnitt",tag: "Damenschnitt"  },
    { src: "images/brautfrisur.png",  alt: "Brautfrisur",   category: "braut",  tag: "Braut"         },
    { src: "images/highlights.png",   alt: "Highlights",    category: "farbe",  tag: "Highlights"    },
    { src: "images/salon.png",        alt: "Salon",         category: "salon",  tag: "Salon"         },
    { src: "images/herrenschnitt.png",alt: "Herrenschnitt", category: "schnitt",tag: "Herren"        },
  ],

  // ── LEISTUNGEN & PREISE ──────────────────────────────────
  SERVICES: {
    schnitt: {
      icon: "✂️",
      title: "Schnitt & Styling",
      left:  [
        { name: "Damen – Waschen, Schneiden, Föhnen", variants: [{"label": "kurz", "price": "ab XX €"}, {"label": "mittel", "price": "ab XX €"}, {"label": "lang", "price": "ab XX €"}] },
        { name: "Herren – Waschen & Schneiden", price: "ab XX €" },
        { name: "Kinder (bis 12 Jahre)", price: "ab XX €" },
        { name: "Föhnen & Eindrehen", price: "ab XX €" }
      ],
      right: [
        { name: "Glätten (Glätteisen)", price: "ab XX €" },
        { name: "Lockenstab-Styling", price: "ab XX €" },
        { name: "Keratin-Glättung", price: "ab XX €" },
        { name: "Nur Föhnen", price: "ab XX €" },
        { name: "Waschen & Legen", price: "ab XX €" }
      ],
    },
    farbe: {
      icon: "🎨",
      title: "Colorationen & Farbtechniken",
      note: "* Preise zzgl. Schnitt & Styling. Aufpreise je nach Haarlänge möglich.",
      left:  [
        { name: "Vollcoloration", variants: [{"label": "kurz", "price": "ab XX €"}, {"label": "mittel", "price": "ab XX €"}, {"label": "lang", "price": "ab XX €"}] },
        { name: "Ansatzcoloration", price: "ab XX €" },
        { name: "Tönung / Glossing", price: "ab XX €" },
        { name: "Strähnen (klassisch)", price: "ab XX €" }
      ],
      right: [
        { name: "Balayage / Ombré", price: "ab XX €" },
        { name: "Highlights (komplett)", price: "ab XX €" },
        { name: "Highlights (teilweise)", price: "ab XX €" },
        { name: "Entfärbung", price: "auf Anfrage" },
        { name: "Blondierung", price: "ab XX €" }
      ],
    },
    pflege: {
      icon: "💆",
      title: "Haarpflege & Treatments",
      left:  [
        { name: "Tiefenpflege-Kur", price: "ab XX €" },
        { name: "Haarkur (intensiv)", price: "ab XX €" },
        { name: "Kopfmassage (10 Min.)", price: "XX €" }
      ],
      right: [
        { name: "Kopfhautbehandlung", price: "ab XX €" },
        { name: "Olaplex-Behandlung", price: "ab XX €" },
        { name: "Haarbotox", price: "auf Anfrage" },
        { name: "Protein-Treatment", price: "ab XX €" }
      ],
    },
    braut: {
      icon: "💍",
      title: "Braut & Festliches Styling",
      note: "Für Brauttermine empfehlen wir frühzeitige Buchung.",
      left:  [
        { name: "Brautfrisur (inkl. Probe)", price: "ab XX €" },
        { name: "Brautfrisur (ohne Probe)", price: "ab XX €" },
        { name: "Probestyling", price: "ab XX €" }
      ],
      right: [
        { name: "Hochsteckfrisur (Event)", price: "ab XX €" },
        { name: "Flechtfrisur", price: "ab XX €" },
        { name: "Hair-Extensions (Beratung)", price: "kostenlos" }
      ],
    },
  },

  // ── IMPRESSUM ────────────────────────────────────────────
  IMPRESSUM: {
    INHABER_NAME:      "",
    BERUFSBEZEICHNUNG: "Friseurmeister/in",
    KAMMER:            "",
    UST_ID:            "",
    REGISTERGERICHT:   "",
    REGISTERNUMMER:    "",
    STAND:             "",
  },

  // ── FOOTER ───────────────────────────────────────────────
  FOOTER_DESC: "",

  // ── TERMIN: STYLISTEN ────────────────────────────────────
  BOOKING_STYLISTS: ["Niko Hair", "Alex Konstatnin", "Hasan Harom", "Imael Sibari"],

  // ── BEWERBUNGS-E-MAIL ────────────────────────────────────
  JOBS_EMAIL: "info@maxhair.de",
};
