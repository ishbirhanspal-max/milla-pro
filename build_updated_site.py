import os

print("Assembling complete updated style.css and index.html...")

# 1. Read base milld components and footer styles
with open('milld_components.css', 'r', encoding='utf-8') as f:
    milld_components_css = f.read()

with open('footer_styles.css', 'r', encoding='utf-8') as f:
    footer_css = f.read()

# 2. Build Updated Master style.css
updated_style_css = f"""/* ==========================================================================
   MILLA PRO™ x MillD Authentic Master Stylesheet (v22.0)
   Fonts: Anton, Caveat, Inter
   Palette: #FDF8EE (Warm Cream), #D4942A (Golden Amber), #121212 (Ink Black)
   ========================================================================== */

@import url('https://fonts.googleapis.com/css2?family=Anton&family=Caveat:wght@400;600;700&family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {{
  --color-background: #FDF8EE;
  --color-foreground: #121212;
  --color-accent: #D4942A;
  --color-yellow: #FFC107;
  --primary: #D4942A;
  --primary-dark: #B07A1F;
  --dark: #121212;
  --bg-cream: #FDF8EE;
  --bg-warm: #FFFBEF;
  --bg-light: #FEF8E9;
  --border-light: rgba(18, 18, 18, 0.12);
  --border-dark: #121212;
  --font-heading: 'Anton', 'Bebas Neue', system-ui, sans-serif;
  --font-script: 'Caveat', cursive;
  --font-body: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}}

/* Universal Reset */
*, *::before, *::after {{
  box-sizing: border-box;
}}

html {{
  font-size: 16px;
  scroll-behavior: smooth;
  -webkit-text-size-adjust: 100%;
  overflow-x: hidden;
}}

body {{
  margin: 0;
  padding: 0;
  font-family: var(--font-body);
  background-color: var(--color-background);
  color: var(--color-foreground);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow-x: hidden;
  width: 100%;
}}

h1, h2, h3, h4, h5, h6 {{
  font-family: var(--font-heading);
  letter-spacing: -0.01em;
  color: var(--color-foreground);
  margin-top: 0;
}}

p, span, div, li, td, th {{
  font-family: var(--font-body);
}}

img, video, svg {{
  max-width: 100%;
  height: auto;
  display: block;
}}

a {{
  color: inherit;
  text-decoration: none;
}}

button {{
  font-family: inherit;
  cursor: pointer;
}}

.container {{
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}}

/* ==========================================================================
   Top Ultra-Thin Moving Marquee Ticker Bar
   ========================================================================== */
.top-ticker-bar {{
  background: #121212;
  color: #FFFBEF;
  padding: 0.45rem 0;
  font-size: 0.72rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  overflow: hidden;
  white-space: nowrap;
  position: relative;
  z-index: 1000;
  border-bottom: 1px solid rgba(212, 148, 42, 0.3);
}}

.ticker-scroll-track {{
  display: flex;
  width: max-content;
  animation: topTickerScroll 28s linear infinite;
}}

.ticker-scroll-content {{
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding-right: 1.25rem;
}}

.ticker-dot {{
  color: var(--color-yellow);
  font-size: 0.85rem;
}}

@keyframes topTickerScroll {{
  0% {{ transform: translateX(0); }}
  100% {{ transform: translateX(-50%); }}
}}

/* ==========================================================================
   Authentic Sticky Master Header
   ========================================================================== */
.master-header {{
  position: sticky;
  top: 0;
  z-index: 990;
  background-color: rgba(253, 248, 238, 0.98);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(18, 18, 18, 0.08);
  transition: all 0.25s ease;
}}

.header-inner {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 68px;
}}

.brand-logo {{
  display: flex;
  flex-direction: column;
  line-height: 1;
  text-decoration: none;
}}

.logo-main {{
  font-family: var(--font-heading);
  font-size: 1.95rem;
  letter-spacing: 0.04em;
  color: var(--color-foreground);
}}

.logo-main span {{
  color: var(--color-accent);
}}

.logo-sub {{
  font-size: 0.62rem;
  font-weight: 800;
  letter-spacing: 0.22em;
  color: rgba(18, 18, 18, 0.6);
  margin-top: 1px;
}}

.desktop-nav {{
  display: flex;
  align-items: center;
  gap: 1.75rem;
}}

@media (max-width: 992px) {{
  .desktop-nav {{
    display: none;
  }}
}}

.desktop-nav a {{
  font-size: 0.9rem;
  font-weight: 700;
  color: rgba(18, 18, 18, 0.85);
  transition: color 0.15s ease;
}}

.desktop-nav a:hover, .desktop-nav a.active {{
  color: var(--color-accent);
}}

.desktop-nav .shop-pill-nav {{
  background: var(--color-yellow);
  color: #121212 !important;
  font-weight: 800;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.06em;
  padding: 0.5rem 1.15rem;
  border-radius: 9999px;
  border: 1.5px solid #121212;
  box-shadow: 0 3px 0 #121212;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}}

.desktop-nav .shop-pill-nav:hover {{
  transform: translateY(-1px);
  box-shadow: 0 4px 0 #121212;
}}

.header-actions {{
  display: flex;
  align-items: center;
  gap: 0.85rem;
}}

.icon-btn {{
  background: transparent;
  border: none;
  padding: 8px;
  border-radius: 50%;
  color: var(--color-foreground);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: background 0.15s ease;
}}

.icon-btn:hover {{
  background: rgba(18, 18, 18, 0.06);
}}

.cart-badge-count {{
  position: absolute;
  top: 0;
  right: 0;
  background: var(--color-accent);
  color: #FFF;
  font-size: 0.65rem;
  font-weight: 800;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1.5px solid var(--color-background);
}}

.mobile-menu-btn {{
  background: transparent;
  border: none;
  padding: 8px;
  color: var(--color-foreground);
  display: none;
  cursor: pointer;
}}

@media (max-width: 992px) {{
  .mobile-menu-btn {{
    display: flex;
    align-items: center;
    justify-content: center;
  }}
}}

/* ==========================================================================
   Mobile Navigation Sidebar Drawer
   ========================================================================== */
.sidebar-overlay {{
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 1100;
  opacity: 0;
  visibility: hidden;
  transition: all 0.25s ease;
}}

.sidebar-overlay.active {{
  opacity: 1;
  visibility: visible;
}}

.mobile-sidebar {{
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 86%;
  max-width: 340px;
  background: #FFFBEF;
  border-right: 2px solid #121212;
  z-index: 1200;
  transform: translateX(-100%);
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  flex-direction: column;
  box-shadow: 10px 0 30px rgba(0, 0, 0, 0.2);
  overflow-y: auto;
}}

.mobile-sidebar.active {{
  transform: translateX(0);
}}

.sidebar-header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.25rem 1rem;
  border-bottom: 1px solid rgba(18, 18, 18, 0.08);
}}

.mobile-shop-cta-btn {{
  margin: 1rem 1.25rem;
  background: #FFC107;
  color: #121212;
  padding: 0.85rem 1.25rem;
  border-radius: 9999px;
  border: 2px solid #121212;
  box-shadow: 0 4px 0 #121212;
  font-size: 0.88rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  display: flex;
  align-items: center;
  justify-content: space-between;
  text-decoration: none;
}}

.mobile-nav-links {{
  display: flex;
  flex-direction: column;
  padding: 0.5rem 0.75rem;
  flex: 1;
}}

.mobile-nav-links a {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.8rem 0.75rem;
  border-radius: 10px;
  font-size: 0.95rem;
  font-weight: 600;
  color: #121212;
  transition: background 0.15s ease;
}}

.mobile-nav-links a:hover {{
  background: rgba(212, 148, 42, 0.12);
}}

.nav-arrow {{
  color: rgba(18, 18, 18, 0.4);
}}

.sidebar-trust-footer {{
  padding: 1.25rem;
  background: #FDF8EE;
  border-top: 1px solid rgba(18, 18, 18, 0.08);
  font-size: 0.78rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  color: rgba(18, 18, 18, 0.7);
}}

.stf-item {{
  display: flex;
  align-items: center;
  gap: 8px;
}}

/* ==========================================================================
   Slide-out Cart Drawer
   ========================================================================== */
.cart-overlay {{
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 1100;
  opacity: 0;
  visibility: hidden;
  transition: all 0.25s ease;
}}

.cart-overlay.active {{
  opacity: 1;
  visibility: visible;
}}

.cart-drawer {{
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: 90%;
  max-width: 400px;
  background: #FFFBEF;
  border-left: 2px solid #121212;
  z-index: 1200;
  transform: translateX(100%);
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  flex-direction: column;
  box-shadow: -10px 0 30px rgba(0, 0, 0, 0.2);
}}

.cart-drawer.active {{
  transform: translateX(0);
}}

.cart-drawer-header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem;
  border-bottom: 1px solid rgba(18, 18, 18, 0.1);
  background: #FDF8EE;
}}

.cart-drawer-title {{
  font-family: var(--font-heading);
  font-size: 1.25rem;
  letter-spacing: 0.05em;
  color: #121212;
}}

.cart-close-btn {{
  background: transparent;
  border: none;
  font-size: 1.25rem;
  color: #121212;
  cursor: pointer;
  padding: 4px;
}}

.cart-policy-strip {{
  background: #FFF;
  border-bottom: 1px solid rgba(18, 18, 18, 0.08);
  padding: 0.75rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  font-size: 0.75rem;
}}

.cart-policy-item {{
  display: flex;
  align-items: flex-start;
  gap: 8px;
}}

.cart-policy-item strong {{
  display: block;
  color: #121212;
}}

.cart-policy-item span {{
  color: rgba(18, 18, 18, 0.65);
  font-size: 0.7rem;
}}

.cart-items-container {{
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}}

.cart-item-row {{
  background: #FFF;
  border: 1.5px solid #121212;
  border-radius: 12px;
  padding: 0.85rem;
  display: flex;
  gap: 0.75rem;
  align-items: center;
  box-shadow: 3px 3px 0 rgba(18, 18, 18, 0.1);
}}

.cir-img {{
  width: 54px;
  height: 54px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid rgba(18, 18, 18, 0.1);
}}

.cir-details {{
  flex: 1;
}}

.cir-title {{
  font-weight: 700;
  font-size: 0.85rem;
  color: #121212;
  margin-bottom: 2px;
}}

.cir-price {{
  font-size: 0.85rem;
  font-weight: 800;
  color: var(--color-accent);
}}

.cir-qty-ctrl {{
  display: flex;
  align-items: center;
  gap: 8px;
  background: #FDF8EE;
  border: 1px solid #121212;
  border-radius: 9999px;
  padding: 2px 8px;
}}

.cir-qty-btn {{
  background: transparent;
  border: none;
  font-weight: 800;
  font-size: 0.9rem;
  cursor: pointer;
  color: #121212;
}}

.cir-qty-val {{
  font-size: 0.8rem;
  font-weight: 700;
}}

.cart-drawer-footer {{
  padding: 1.25rem;
  background: #FDF8EE;
  border-top: 1px solid rgba(18, 18, 18, 0.1);
}}

.bill-row {{
  display: flex;
  justify-content: space-between;
  font-size: 0.82rem;
  margin-bottom: 0.35rem;
  color: rgba(18, 18, 18, 0.75);
}}

.bill-row.total-row {{
  font-size: 1rem;
  font-weight: 800;
  color: #121212;
  border-top: 1.5px dashed rgba(18, 18, 18, 0.2);
  padding-top: 0.5rem;
  margin-top: 0.5rem;
  margin-bottom: 1rem;
}}

.cart-checkout-btn {{
  width: 100%;
  background: #121212;
  color: #FFFBEF;
  border: none;
  border-radius: 9999px;
  padding: 0.9rem 1.25rem;
  font-size: 0.9rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  box-shadow: 0 4px 0 var(--color-yellow);
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  transition: transform 0.15s ease;
}}

.cart-checkout-btn:hover {{
  transform: translateY(-2px);
}}

/* ==========================================================================
   AUTHENTIC MILLD COMPONENT RULES
   ========================================================================== */
{milld_components_css}

/* ==========================================================================
   HERO CENTERING ON DESKTOP & LAPTOP (NO IMAGE SKEWING)
   ========================================================================== */
.milld-hs {{
  padding: 3.5rem 0 2rem !important;
}}

.milld-hs .mh-grid {{
  display: block !important;
  max-width: 920px !important;
  margin: 0 auto !important;
  padding: 0 1.5rem !important;
  text-align: center !important;
}}

.milld-hs .mh-copy {{
  width: 100% !important;
  text-align: center !important;
  grid-column: auto !important;
  padding: 1rem 0 !important;
}}

.milld-hs .mh-h1 {{
  font-size: clamp(2.5rem, 5.5vw, 4.5rem) !important;
  line-height: 1.05 !important;
  letter-spacing: -0.01em !important;
  margin-bottom: 1.5rem !important;
}}

.milld-hs .mh-sub {{
  margin: 1.5rem auto 0 !important;
  max-width: 42rem !important;
  font-size: 1.2rem !important;
  line-height: 1.6 !important;
}}

.milld-hs .mh-ctas {{
  justify-content: center !important;
  margin-top: 2.25rem !important;
}}

.milld-hs .mh-stats {{
  justify-content: center !important;
  margin: 2.5rem auto 1rem !important;
  max-width: 32rem !important;
}}

/* ==========================================================================
   NABL NUTRITION DETAILS CARD (IMAGE HIDDEN BEHIND LINK)
   ========================================================================== */
.lab-details-section {{
  position: relative;
  background-color: #FEF8E9;
  padding: 5rem 0;
  border-top: 2px solid rgba(18, 18, 18, 0.08);
  border-bottom: 2px solid rgba(18, 18, 18, 0.08);
}}

.lab-details-container {{
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 1.5rem;
}}

.lab-details-header {{
  text-align: center;
  max-width: 720px;
  margin: 0 auto 3rem;
}}

.lab-badge-pill {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #FFC107;
  color: #121212;
  font-size: 10.5px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 0.35rem 0.95rem;
  border-radius: 9999px;
  border: 1.5px solid #121212;
  box-shadow: 0 4px 0 -1px rgba(18, 18, 18, 0.25);
  margin-bottom: 1rem;
}}

.lab-details-title {{
  font-family: var(--font-heading);
  font-size: clamp(2.2rem, 4.5vw, 3.25rem);
  text-transform: uppercase;
  color: #121212;
  line-height: 1.1;
  margin: 0 0 1rem;
}}

.lab-details-title .accent {{
  color: #D4942A;
}}

.lab-details-sub {{
  font-size: 1.05rem;
  line-height: 1.6;
  color: rgba(18, 18, 18, 0.75);
  margin: 0;
}}

.lab-summary-card {{
  background: #FFF;
  border: 2px solid #121212;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 6px 6px 0 #121212;
}}

.lab-summary-top {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 1.25rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px dashed rgba(18, 18, 18, 0.15);
  margin-bottom: 2rem;
}}

.lab-summary-meta h3 {{
  font-family: var(--font-heading);
  font-size: 1.65rem;
  text-transform: uppercase;
  color: #121212;
  margin: 0 0 0.4rem;
}}

.lab-summary-meta p {{
  margin: 0;
  font-size: 0.88rem;
  color: rgba(18, 18, 18, 0.7);
  line-height: 1.5;
}}

.lab-params-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
  margin-bottom: 2.25rem;
}}

@media (max-width: 768px) {{
  .lab-params-grid {{
    grid-template-columns: 1fr;
    gap: 0.85rem;
  }}
}}

.lab-param-box {{
  background: #FDF8EE;
  border: 1.5px solid rgba(18, 18, 18, 0.15);
  border-radius: 14px;
  padding: 1.25rem;
  text-align: center;
  transition: transform 0.15s ease;
}}

.lab-param-box.featured {{
  background: #FFFBEF;
  border: 2px solid #D4942A;
  box-shadow: 0 4px 12px rgba(212, 148, 42, 0.15);
}}

.lab-param-val {{
  font-family: var(--font-heading);
  font-size: 2rem;
  color: #121212;
  line-height: 1;
  margin-bottom: 0.25rem;
}}

.lab-param-box.featured .lab-param-val {{
  color: #D4942A;
}}

.lab-param-name {{
  font-size: 0.85rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #121212;
  margin-bottom: 0.2rem;
}}

.lab-param-method {{
  font-size: 0.72rem;
  color: rgba(18, 18, 18, 0.55);
}}

.lab-cta-card-row {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
  background: #FFFBEF;
  border: 1.5px solid rgba(18, 18, 18, 0.15);
  border-radius: 14px;
  padding: 1.25rem 1.75rem;
}}

.lab-btn-view-cert {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #121212;
  color: #FFFBEF;
  font-size: 0.9rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 0.85rem 1.5rem;
  border-radius: 9999px;
  box-shadow: 0 4px 0 #FFC107;
  transition: transform 0.15s ease;
}}

.lab-btn-view-cert:hover {{
  transform: translateY(-2px);
}}

/* ==========================================================================
   WHEY PROTEIN COST CALCULATOR (INTEGRATED IN PG-SECTION)
   ========================================================================== */
.pg-whey-card {{
  margin-top: 2.5rem;
  background: #FFF;
  border: 2px solid #121212;
  border-radius: 20px;
  padding: 2.25rem;
  box-shadow: 6px 6px 0 #121212;
}}

.pg-whey-header {{
  text-align: center;
  margin-bottom: 1.5rem;
}}

.pg-whey-kicker {{
  display: inline-block;
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  background: #FFC107;
  color: #121212;
  padding: 0.3rem 0.8rem;
  border-radius: 9999px;
  border: 1px solid #121212;
  margin-bottom: 0.5rem;
}}

.pg-whey-title {{
  font-family: var(--font-heading);
  font-size: clamp(1.6rem, 3.5vw, 2.3rem);
  text-transform: uppercase;
  color: #121212;
  margin: 0 0 0.5rem;
}}

.pg-whey-sub {{
  font-size: 0.95rem;
  color: rgba(18, 18, 18, 0.7);
  max-width: 620px;
  margin: 0 auto;
}}

.pg-whey-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin: 1.75rem 0;
}}

@media (max-width: 640px) {{
  .pg-whey-grid {{
    grid-template-columns: 1fr;
    gap: 1rem;
  }}
}}

.pg-whey-box {{
  background: #FDF8EE;
  border: 1.5px solid rgba(18, 18, 18, 0.2);
  border-radius: 14px;
  padding: 1.5rem;
  text-align: center;
}}

.pg-whey-box.winner {{
  background: #FFFBEF;
  border: 2px solid #D4942A;
  box-shadow: 0 6px 20px rgba(212, 148, 42, 0.15);
  position: relative;
}}

.pg-whey-box-badge {{
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  background: #D4942A;
  color: #FFF;
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 2px 10px;
  border-radius: 9999px;
}}

.pg-whey-box-title {{
  font-size: 0.9rem;
  font-weight: 700;
  color: rgba(18, 18, 18, 0.75);
  margin-bottom: 0.5rem;
}}

.pg-whey-box-price {{
  font-family: var(--font-heading);
  font-size: 2.3rem;
  color: #121212;
  line-height: 1;
  margin-bottom: 0.25rem;
}}

.pg-whey-box.winner .pg-whey-box-price {{
  color: #2E7D32;
}}

.pg-whey-box-sub {{
  font-size: 0.78rem;
  color: rgba(18, 18, 18, 0.6);
}}

.pg-savings-banner {{
  background: linear-gradient(135deg, #121212, #241C16);
  color: #FFFBEF;
  border-radius: 14px;
  padding: 1.25rem 1.75rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}}

.pg-savings-text {{
  font-size: 1.05rem;
  line-height: 1.4;
}}

.pg-savings-text strong {{
  color: #FFC107;
  font-size: 1.3rem;
}}

.pg-savings-btn {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #FFC107;
  color: #121212;
  font-size: 0.88rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 0.75rem 1.35rem;
  border-radius: 9999px;
  text-decoration: none;
  box-shadow: 0 4px 0 #D4942A;
  transition: transform 0.15s ease;
}}

.pg-savings-btn:hover {{
  transform: translateY(-2px);
}}

/* ==========================================================================
   AUTHENTIC MILLD FOOTER STYLES
   ========================================================================== */
{footer_css}

/* ==========================================================================
   Simulated Razorpay 2-Step Checkout Modal
   ========================================================================== */
.modal-overlay {{
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(5px);
  z-index: 1500;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}}

.modal-overlay.active {{
  display: flex;
}}

.razorpay-simulated-modal {{
  background: #FFF;
  width: 100%;
  max-width: 480px;
  border-radius: 16px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.1);
}}

.rp-header {{
  background: #0C2340;
  color: #FFF;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}}

.rp-header-left {{
  display: flex;
  align-items: center;
  gap: 12px;
}}

.rp-brand-avatar {{
  width: 38px;
  height: 38px;
  background: var(--color-accent);
  color: #FFF;
  font-weight: 900;
  font-size: 1.2rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}}

.rp-merchant-name {{
  font-weight: 700;
  font-size: 0.95rem;
}}

.rp-order-sub {{
  font-size: 0.72rem;
  opacity: 0.75;
}}

.rp-close {{
  background: transparent;
  border: none;
  color: #FFF;
  font-size: 1.25rem;
  cursor: pointer;
  padding: 4px;
}}

.rp-stepper-bar {{
  display: flex;
  background: #F4F6F9;
  border-bottom: 1px solid #E2E8F0;
}}

.rp-step-item {{
  flex: 1;
  padding: 0.75rem;
  text-align: center;
  font-size: 0.78rem;
  font-weight: 700;
  color: #718096;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}}

.rp-step-item.active {{
  color: #0C2340;
  background: #FFF;
  border-bottom: 2px solid var(--color-accent);
}}

.rp-step-num {{
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #CBD5E0;
  color: #FFF;
  font-size: 0.7rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}}

.rp-step-item.active .rp-step-num {{
  background: var(--color-accent);
}}

.rp-body {{
  padding: 1.25rem;
  max-height: 70vh;
  overflow-y: auto;
}}

.rp-form-group {{
  margin-bottom: 0.85rem;
}}

.rp-form-group label {{
  display: block;
  font-size: 0.78rem;
  font-weight: 700;
  margin-bottom: 4px;
  color: #2D3748;
}}

.rp-input {{
  width: 100%;
  padding: 0.65rem 0.85rem;
  border: 1px solid #CBD5E0;
  border-radius: 8px;
  font-size: 0.88rem;
  transition: border 0.15s ease;
}}

.rp-input:focus {{
  outline: none;
  border-color: var(--color-accent);
}}

.rp-btn-primary {{
  width: 100%;
  background: #0C2340;
  color: #FFF;
  border: none;
  padding: 0.85rem;
  border-radius: 8px;
  font-weight: 800;
  font-size: 0.9rem;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: background 0.15s ease;
}}

.rp-btn-primary:hover {{
  background: #1A365D;
}}

/* ==========================================================================
   MOBILE VIEWPORT 393 × 852 STRICT COMPATIBILITY
   ========================================================================== */
@media (max-width: 500px) {{
  html, body {{
    width: 100vw;
    overflow-x: hidden !important;
  }}

  .container {{
    padding: 0 1rem !important;
  }}

  .header-inner {{
    height: 58px;
  }}

  .logo-main {{
    font-size: 1.55rem !important;
  }}

  .milld-hs {{
    padding: 2rem 0 1rem !important;
  }}

  .milld-hs .mh-h1 {{
    font-size: 11.5vw !important;
    line-height: 1.05 !important;
  }}

  .milld-hs .mh-sub {{
    font-size: 0.98rem !important;
    margin-top: 1.25rem !important;
  }}

  .milld-hs .mh-sub strong {{
    font-size: 1.45rem !important;
  }}

  .pg-section {{
    padding: 2.5rem 0 !important;
  }}

  .pg-heading {{
    font-size: 9.5vw !important;
  }}

  .pg-note-wrap {{
    padding: 1.25rem 1rem !important;
  }}

  .pg-calc {{
    padding: 1.25rem 1rem !important;
  }}

  .pg-calc-title {{
    font-size: 1.35rem !important;
  }}

  .pg-compare-value {{
    font-size: 1.85rem !important;
  }}

  .pg-whey-card {{
    padding: 1.25rem 1rem !important;
    border-radius: 16px !important;
  }}

  .pg-whey-title {{
    font-size: 1.4rem !important;
  }}

  .pg-whey-box-price {{
    font-size: 1.85rem !important;
  }}

  .pg-savings-banner {{
    padding: 1rem !important;
    flex-direction: column !important;
    text-align: center !important;
  }}

  .pg-savings-btn {{
    width: 100% !important;
    justify-content: center !important;
  }}

  .rr-section {{
    padding: 2.5rem 0 !important;
  }}

  .rr-heading {{
    font-size: 11vw !important;
  }}

  .rr-grid {{
    gap: 1.5rem !important;
  }}

  .bc-section {{
    padding: 2.5rem 0 !important;
  }}

  .bc-heading {{
    font-size: 11vw !important;
  }}

  .lab-details-section {{
    padding: 2.5rem 0 !important;
  }}

  .lab-details-title {{
    font-size: 9.5vw !important;
  }}

  .lab-summary-card {{
    padding: 1.5rem 1rem !important;
  }}

  .ss-section {{
    padding: 2.5rem 0 !important;
  }}

  .ss-panel-heading-mobile {{
    font-size: 10vw !important;
  }}

  .ss-cards-mobile {{
    gap: 0.75rem !important;
  }}

  .tm-section {{
    padding: 2.5rem 0 !important;
  }}

  .tm-heading {{
    font-size: 10vw !important;
  }}

  .faq-section {{
    padding: 2.5rem 0 !important;
  }}

  .faq-heading {{
    font-size: 11vw !important;
  }}

  .ft-footer {{
    padding: 3rem 0 1.5rem !important;
  }}

  .ft-grid {{
    gap: 2rem !important;
  }}
}}
"""

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(updated_style_css)

print(f"Generated style.css (v22.0) ({len(updated_style_css)} bytes)")
