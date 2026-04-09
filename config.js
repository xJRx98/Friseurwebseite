/**
 * ============================================================
 *  SALON WEBSITE – ZENTRALE KONFIGURATION
 *  Automatisch generiert aus Webseite_Daten_komplett.xlsx
 *  Stand: 09.04.2026 14:45
 * ============================================================
 */

const SALON_CONFIG = {

  // ── GRUNDDATEN ──────────────────────────────────────────
  SALON_NAME:       "Lisa's Hair Styling",
  TAGLINE:          "Schönheit beginnt mit dem richtigen Schnitt.",
  GRUENDUNGSJAHR:   "2014",
  STADT:            "München",
  YEAR:             new Date().getFullYear(),

  // ── KONTAKT ─────────────────────────────────────────────
  ADDRESS_STREET:   "Schleißheimer Str. 42",
  ADDRESS_ZIP:      "80797",
  ADDRESS_CITY:     "München",
  PHONE:            "089 46 24 83 50",
  EMAIL:            "info@lisas-hairstyling.de",
  WHATSAPP:         "4989462483550",

  // ── SOCIAL MEDIA ─────────────────────────────────────────
  INSTAGRAM_HANDLE: "@lisas.hairstyling",
  INSTAGRAM_URL:    "https://www.instagram.com/lisas.hairstyling",
  FACEBOOK_URL:     "https://www.facebook.com/lisashairstylingmuenchen",

  // ── GOOGLE ───────────────────────────────────────────────
  GOOGLE_API_KEY:   "AIzaSyD-BEISPIEL-KEY-123456789",
  PLACE_ID:         "ChIJN1t_tDeuEmsRUsoyG83frY4",
  MAPS_EMBED_URL:   "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2661.5!2d11.5620!3d48.1615",
  MAPS_LINK:        "https://maps.google.com/?q=Schleißheimer+Str.+42,+80797+München",
  GOOGLE_REVIEWS_URL: "https://g.page/r/lisas-hairstyling-muenchen/review",
  GOOGLE_RATING:    "4.9",
  GOOGLE_REVIEW_COUNT: "184",

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
        "name": "Lisa Hinrich",
        "role": "Friseurmeisterin & Inhaberin",
        "photo": "images/team1.jpg",
        "bio": "Lisa gründete den Salon 2014 nach ihrer Meisterausbildung in München. Mit über 15 Jahren Erfahrung ist sie spezialisiert auf Balayage und individuelle Beratung. Ihre Leidenschaft gilt modernen Schnitttechniken und der Arbeit mit feinem Haar.",
        "quote": "Haare sind die einzige Accessoire, die du nie ablegen kannst – also pflege sie mit Liebe.",
        "tags": [
            "Balayage",
            "Feine Haare",
            "Brautstyling"
        ],
        "isOwner": true
    },
    {
        "name": "Jessica Zuren",
        "role": "Stylistin",
        "photo": "images/team2.jpg",
        "bio": "Jessica ist seit 2018 im Team und hat ihre Ausbildung mit Auszeichnung abgeschlossen. Sie liebt es, mit Farbe zu experimentieren und ihren Kundinnen einen frischen Look zu geben. Besonders Colorationen und kreative Schnitte sind ihr Herzensthema.",
        "quote": "Jeder Mensch verdient einen Tag, an dem er sich unwiderstehlich fühlt.",
        "tags": [
            "Colorationen",
            "Kreativschnitte",
            "Beratung"
        ],
        "isOwner": false
    },
    {
        "name": "Hasan Harom",
        "role": "Colorist",
        "photo": "images/team3.jpg",
        "bio": "Hasan kam 2020 zu Lisa's Hair Styling und bringt frischen Wind aus der internationalen Friseurwelt mit. Er hat in Istanbul und Wien gearbeitet und ist Experte für Blondierungen und Strähnen-Techniken.",
        "quote": "Farbe ist Emotion – und ich helfe dir, die richtige zu finden.",
        "tags": [
            "Blondierung",
            "Highlights",
            "Herrenschnitte"
        ],
        "isOwner": false
    },
    {
        "name": "Imael Sibari",
        "role": "Auszubildende/r im 2. Lehrjahr",
        "photo": "images/team4.jpg",
        "bio": "Imael ist seit 2023 Auszubildende bei uns und bringt frische Energie und Begeisterung mit. Besonders das Styling mit Lockenstab und das Erlernen von Flechtfrisuren machen ihr große Freude.",
        "quote": "Ich lerne jeden Tag etwas Neues – und das ist das Schönste an diesem Beruf.",
        "tags": [
            "Styling",
            "Flechtfrisuren",
            "2. Lehrjahr"
        ],
        "isOwner": false
    }
],

  // ── KENNZAHLEN ───────────────────────────────────────────
  STATS: [
    {
        "number": "15+",
        "label": "Jahre Erfahrung"
    },
    {
        "number": "4",
        "label": "Teammitglieder"
    },
    {
        "number": "250+",
        "label": "Zufriedene Gäste/Monat"
    },
    {
        "number": "4.9",
        "label": "Google-Bewertung"
    }
],

  // ── GOOGLE BEWERTUNGEN ───────────────────────────────────
  REVIEWS: [
    {
        "text": "Ich bin seit Jahren Stammkundin und komme immer wieder gerne! Lisa hat ein unglaubliches Gespür für das, was zu einem passt. Der Salon ist gemütlich, das Team super herzlich – und mein Haar sieht danach jedes Mal traumhaft aus.",
        "name": "Sarah M.",
        "date": "März 2026",
        "stars": 5
    },
    {
        "text": "Hasan hat meine Blondierung perfekt hinbekommen – genau der Ton, den ich mir vorgestellt hatte. Professionelle Beratung, faire Preise und eine entspannte Atmosphäre. Absolute Empfehlung!",
        "name": "Thomas K.",
        "date": "Februar 2026",
        "stars": 5
    },
    {
        "text": "Jessica hat meine langen Haare mit einem Balayage in ein echtes Kunstwerk verwandelt. Ich hatte vorher schlechte Erfahrungen woanders gemacht, aber hier wurde ich von Anfang an super beraten. Ich komme nicht mehr woanders hin!",
        "name": "Melanie R.",
        "date": "Januar 2026",
        "stars": 5
    }
],

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
        { name: "Damen – Waschen, Schneiden, Föhnen", variants: [{"label": "kurz", "price": "ab 45 €"}, {"label": "mittel", "price": "ab 55 €"}, {"label": "lang", "price": "ab 65 €"}] },
        { name: "Herren – Waschen & Schneiden", price: "ab 29 €" },
        { name: "Kinder (bis 12 Jahre)", price: "ab 22 €" },
        { name: "Föhnen & Eindrehen", price: "ab 25 €" }
      ],
      right: [
        { name: "Glätten (Glätteisen)", price: "ab 20 €" },
        { name: "Lockenstab-Styling", price: "ab 22 €" },
        { name: "Keratin-Glättung", price: "ab 120 €" },
        { name: "Nur Föhnen", price: "ab 18 €" },
        { name: "Waschen & Legen", price: "ab 30 €" }
      ],
    },
    farbe: {
      icon: "🎨",
      title: "Colorationen & Farbtechniken",
      note: "* Preise zzgl. Schnitt & Styling. Aufpreise je nach Haarlänge möglich.",
      left:  [
        { name: "Vollcoloration", variants: [{"label": "kurz", "price": "ab 55 €"}, {"label": "mittel", "price": "ab 70 €"}, {"label": "lang", "price": "ab 90 €"}] },
        { name: "Ansatzcoloration", price: "ab 45 €" },
        { name: "Tönung / Glossing", price: "ab 35 €" },
        { name: "Strähnen (klassisch)", price: "ab 50 €" }
      ],
      right: [
        { name: "Balayage / Ombré", price: "ab 90 €" },
        { name: "Highlights (komplett)", price: "ab 80 €" },
        { name: "Highlights (teilweise)", price: "ab 55 €" },
        { name: "Entfärbung", price: "auf Anfrage" },
        { name: "Blondierung", price: "ab 75 €" }
      ],
    },
    pflege: {
      icon: "💆",
      title: "Haarpflege & Treatments",
      left:  [
        { name: "Tiefenpflege-Kur", price: "ab 18 €" },
        { name: "Haarkur (intensiv)", price: "ab 25 €" },
        { name: "Kopfmassage (10 Min.)", price: "15 €" }
      ],
      right: [
        { name: "Kopfhautbehandlung", price: "ab 30 €" },
        { name: "Olaplex-Behandlung", price: "ab 35 €" },
        { name: "Haarbotox", price: "auf Anfrage" },
        { name: "Protein-Treatment", price: "ab 28 €" }
      ],
    },
    braut: {
      icon: "💍",
      title: "Braut & Festliches Styling",
      note: "Für Brauttermine empfehlen wir frühzeitige Buchung.",
      left:  [
        { name: "Brautfrisur (inkl. Probe)", price: "ab 180 €" },
        { name: "Brautfrisur (ohne Probe)", price: "ab 120 €" },
        { name: "Probestyling", price: "ab 60 €" }
      ],
      right: [
        { name: "Hochsteckfrisur (Event)", price: "ab 55 €" },
        { name: "Flechtfrisur", price: "ab 40 €" },
        { name: "Hair-Extensions (Beratung)", price: "kostenlos" }
      ],
    },
  },

  // ── IMPRESSUM ────────────────────────────────────────────
  IMPRESSUM: {
    INHABER_NAME:      "Lisa Hinrich",
    BERUFSBEZEICHNUNG: "Friseurmeisterin",
    KAMMER:            "Handwerkskammer für München und Oberbayern",
    UST_ID:            "DE298374651",
    REGISTERGERICHT:   "Amtsgericht München",
    REGISTERNUMMER:    "HRB 234871",
    STAND:             "April 2026",
  },

  // ── FOOTER ───────────────────────────────────────────────
  FOOTER_DESC: "Ihr Friseursalon im Herzen Münchens – für Menschen, die Wert auf Stil, Pflege und persönliche Beratung legen.",

  // ── TERMIN: STYLISTEN ────────────────────────────────────
  BOOKING_STYLISTS: ["Lisa Hinrich", "Jessica Zuren", "Hasan Harom", "Imael Sibari"],

  // ── BEWERBUNGS-E-MAIL ────────────────────────────────────
  JOBS_EMAIL: "bewerbung@lisas-hairstyling.de",
};
