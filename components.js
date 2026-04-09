/**
 * ============================================================
 *  SALON WEBSITE – GEMEINSAME UI-KOMPONENTEN
 *  Wird von allen Seiten geladen. Rendert Nav + Footer
 *  aus SALON_CONFIG (config.js).
 * ============================================================
 */

// ── NAVIGATION ───────────────────────────────────────────────
function renderNav(activePage) {
  const pages = [
    { href: "index.html",      label: "Home" },
    { href: "leistungen.html", label: "Leistungen & Preise" },
    { href: "team.html",       label: "Team" },
    { href: "galerie.html",    label: "Galerie" },
    { href: "kontakt.html",    label: "Kontakt" },
  ];

  const links = pages.map(p =>
    `<li><a href="${p.href}"${p.href === activePage ? ' class="active"' : ''}>${p.label}</a></li>`
  ).join('\n      ');

  return `<nav>
    <a href="index.html" class="nav-logo">${SALON_CONFIG.SALON_NAME}</a>
    <ul class="nav-links" id="navLinks">
      ${links}
      <li><a href="termin.html" class="nav-cta${activePage === 'termin.html' ? ' active' : ''}">Termin buchen</a></li>
    </ul>
    <button class="hamburger" onclick="document.getElementById('navLinks').classList.toggle('open')" aria-label="Menü">
      <span></span><span></span><span></span>
    </button>
  </nav>`;
}

// ── FOOTER ────────────────────────────────────────────────────
function renderFooter() {
  return `<footer>
    <div class="footer-grid">
      <div>
        <span class="footer-logo">${SALON_CONFIG.SALON_NAME}</span>
        <p class="footer-desc">${SALON_CONFIG.FOOTER_DESC}</p>
        <div style="display:flex; gap:1rem; margin-top:1.5rem;">
          <a href="${SALON_CONFIG.INSTAGRAM_URL}" style="color:var(--text-muted); text-decoration:none; font-size:0.78rem; transition:color 0.3s;" onmouseover="this.style.color='var(--gold)'" onmouseout="this.style.color='var(--text-muted)'">Instagram</a>
          <a href="${SALON_CONFIG.FACEBOOK_URL}"  style="color:var(--text-muted); text-decoration:none; font-size:0.78rem; transition:color 0.3s;" onmouseover="this.style.color='var(--gold)'" onmouseout="this.style.color='var(--text-muted)'">Facebook</a>
        </div>
      </div>
      <div>
        <div class="footer-title">Navigation</div>
        <ul class="footer-links">
          <li><a href="index.html">Home</a></li>
          <li><a href="leistungen.html">Leistungen & Preise</a></li>
          <li><a href="team.html">Team</a></li>
          <li><a href="galerie.html">Galerie</a></li>
          <li><a href="kontakt.html">Kontakt</a></li>
        </ul>
      </div>
      <div>
        <div class="footer-title">Kontakt</div>
        <ul class="footer-links">
          <li><a href="tel:${SALON_CONFIG.PHONE}">${SALON_CONFIG.PHONE}</a></li>
          <li><a href="mailto:${SALON_CONFIG.EMAIL}">${SALON_CONFIG.EMAIL}</a></li>
          <li style="color:var(--text-muted); font-size:0.85rem; margin-top:0.4rem;">${SALON_CONFIG.ADDRESS_STREET}<br>${SALON_CONFIG.ADDRESS_ZIP} ${SALON_CONFIG.ADDRESS_CITY}</li>
        </ul>
      </div>
      <div>
        <div class="footer-title">Rechtliches</div>
        <ul class="footer-links">
          <li><a href="impressum.html">Impressum</a></li>
          <li><a href="datenschutz.html">Datenschutz</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© ${SALON_CONFIG.YEAR} ${SALON_CONFIG.SALON_NAME} · Alle Rechte vorbehalten</span>
      <span>Mit ♥ gestaltet in ${SALON_CONFIG.STADT}</span>
    </div>
  </footer>`;
}

// ── ÖFFNUNGSZEITEN-TABELLE ────────────────────────────────────
function renderHoursTable() {
  const todayIndex = new Date().getDay(); // 0=So, 1=Mo …
  // Config-Array beginnt bei Montag (Index 0 = Montag)
  // JS-Wochentag: 0=So → config-Index 6, 1=Mo → 0 …
  const configIndex = todayIndex === 0 ? 6 : todayIndex - 1;

  return SALON_CONFIG.HOURS.map((h, i) => `
    <tr${i === configIndex ? ' class="today"' : ''}>
      <td>${h.day}</td>
      <td style="text-align:right">${h.time}</td>
    </tr>`).join('');
}

// ── SCROLL-ANIMATION ──────────────────────────────────────────
function initScrollAnimations() {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
  }, { threshold: 0.1 });
  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
}
