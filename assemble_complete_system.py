import os
import re

print("Assembling complete system...")

# 1. Read files
with open('milld_components.css', 'r', encoding='utf-8') as f:
    milld_components_css = f.read()

with open('footer_styles.css', 'r', encoding='utf-8') as f:
    footer_css = f.read()

with open('style_ver_1995.css', 'r', encoding='utf-8') as f:
    ver_1995_css = f.read()

# Extract shop and modal styles from ver_1995_css
shop_start = ver_1995_css.find('/* 11. UN-CROWDED, SLEEK SHOP PAGE')
shop_css = ver_1995_css[shop_start:] if shop_start != -1 else ""

# Custom Overrides:
# - Remove hero roti photo styling
# - Ensure hero is centered on laptop and mobile
# - Clean lab reports details cards with link
# - Unified luxury dark footer for both .ft-footer and .master-footer
# - Complete Whey cost calculator styles
custom_overrides_css = """
/* ==========================================================================
   MILLA PRO™ HERO CENTERED OVERRIDE (NO ROTI IMAGE ON HOMEPAGE)
   PERFECT CENTERING ON LAPTOP & MOBILE
   ========================================================================== */
.milld-hs {
  position: relative !important;
  background-color: #FFFBEF !important;
  color: #121212 !important;
  padding: 3rem 0 2rem !important;
  overflow: hidden !important;
  text-align: center !important;
}

.milld-hs .mh-grid {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  text-align: center !important;
  max-width: 960px !important;
  margin: 0 auto !important;
  padding: 0 1.5rem !important;
  width: 100% !important;
}

.milld-hs .mh-copy {
  grid-column: auto !important;
  width: 100% !important;
  max-width: 860px !important;
  margin: 0 auto !important;
  text-align: center !important;
  position: relative !important;
  z-index: 10 !important;
  padding-top: 1rem !important;
  padding-bottom: 1rem !important;
}

.milld-hs .mh-badge {
  display: inline-flex !important;
  align-items: center !important;
  white-space: nowrap !important;
  border-radius: 9999px !important;
  border: 1.5px solid #121212 !important;
  background: #FFC107 !important;
  padding: 0.45rem 1.25rem !important;
  font-size: 11.5px !important;
  font-weight: 800 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.12em !important;
  color: #121212 !important;
  box-shadow: 0 4px 0 -1px rgba(18, 18, 18, 0.25) !important;
  margin-bottom: 1.5rem !important;
}

.milld-hs .mh-h1 {
  font-family: 'Anton', 'Bebas Neue', system-ui, sans-serif !important;
  text-transform: uppercase !important;
  line-height: 1.05 !important;
  letter-spacing: -0.01em !important;
  margin: 0 0 1.25rem !important;
  color: #121212 !important;
  font-weight: 400 !important;
  font-size: clamp(2.6rem, 6.5vw, 5.2rem) !important;
  text-align: center !important;
}

.milld-hs .mh-brush {
  background-image: linear-gradient(120deg, #FFC107 0%, #FFC107 100%) !important;
  background-repeat: no-repeat !important;
  background-size: 100% 38% !important;
  background-position: 0 84% !important;
  padding: 0 0.2em !important;
  color: #121212 !important;
  white-space: nowrap !important;
}

.milld-hs .mh-sub {
  margin: 1.25rem auto 2.25rem !important;
  max-width: 44rem !important;
  font-size: clamp(1.05rem, 2.2vw, 1.35rem) !important;
  line-height: 1.6 !important;
  color: rgba(18, 18, 18, 0.85) !important;
  text-align: center !important;
}

.milld-hs .mh-ctas {
  display: flex !important;
  flex-wrap: wrap !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 1.25rem !important;
  margin: 2.25rem auto 1.5rem !important;
}

.milld-hs .mh-stats {
  display: grid !important;
  grid-template-columns: repeat(3, 1fr) !important;
  gap: 1.25rem !important;
  max-width: 38rem !important;
  margin: 2.5rem auto 1rem !important;
  text-align: center !important;
}

/* ==========================================================================
   LAB DETAILS SECTION (VERIFIED NUMERIC PARAMETERS ON SITE + LINK TO CERTIFICATE)
   NO SCANNED IMAGES ON HOME PAGE
   ========================================================================== */
.lab-showcase-section, .lab-details-section {
  padding: 5rem 0;
  background: #FFFBEF;
}

.lab-showcase-container {
  max-width: 1140px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.lab-showcase-header {
  text-align: center;
  max-width: 780px;
  margin: 0 auto 3rem;
}

.lab-badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #FFC107;
  color: #121212;
  font-size: 10.5px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  padding: 0.35rem 1rem;
  border-radius: 9999px;
  border: 1.5px solid #121212;
  margin-bottom: 1rem;
}

.lab-showcase-title {
  font-size: clamp(2.4rem, 5vw, 4rem);
  text-transform: uppercase;
  margin-bottom: 1rem;
}

.lab-showcase-title .accent {
  color: #D4942A;
}

.lab-showcase-sub {
  font-size: 1.05rem;
  line-height: 1.65;
  color: rgba(18, 18, 18, 0.8);
}

.lab-details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 2.5rem;
}

@media (min-width: 768px) {
  .lab-details-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 1.25rem;
  }
}

.lab-detail-card {
  background: #FFF;
  border: 2px solid #121212;
  border-radius: 14px;
  padding: 1.25rem 1rem;
  text-align: center;
  box-shadow: 4px 4px 0 #121212;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.lab-detail-card.highlight {
  background: #FFFDF5;
  border-color: #D4942A;
  box-shadow: 4px 4px 0 #D4942A;
}

.lab-param-val {
  font-family: 'Anton', 'Bebas Neue', system-ui, sans-serif;
  font-size: 2.2rem;
  color: #121212;
  line-height: 1.1;
}

.lab-detail-card.highlight .lab-param-val {
  color: #D4942A;
}

.lab-param-name {
  font-size: 0.88rem;
  font-weight: 700;
  color: #121212;
  margin: 0.35rem 0 0.2rem;
}

.lab-param-method {
  font-size: 0.72rem;
  color: rgba(18, 18, 18, 0.55);
  font-weight: 600;
}

.lab-credentials-banner {
  background: #FFF;
  border: 2px solid #121212;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 6px 6px 0 #121212;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  align-items: center;
  justify-content: space-between;
}

@media (min-width: 900px) {
  .lab-credentials-banner {
    flex-direction: row;
  }
}

.lab-cred-text h3 {
  font-size: 1.5rem;
  text-transform: uppercase;
  margin-bottom: 0.4rem;
}

.lab-cred-text p {
  font-size: 0.88rem;
  color: rgba(18, 18, 18, 0.75);
  line-height: 1.5;
}

.lab-actions-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
}

.lab-btn-link {
  background: #121212;
  color: #FFFBEF;
  border: 1.5px solid #121212;
  border-radius: 9999px;
  padding: 0.85rem 1.6rem;
  font-size: 0.88rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  box-shadow: 0 4px 0 0 #FFC107;
  transition: transform 0.15s ease;
  text-decoration: none;
}

.lab-btn-link:hover {
  transform: translateY(-2px);
}

.lab-btn-pdf {
  background: #FFF;
  color: #121212;
  border: 2px solid #121212;
  border-radius: 9999px;
  padding: 0.85rem 1.6rem;
  font-size: 0.88rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  box-shadow: 3px 3px 0 #121212;
  transition: transform 0.15s ease;
  text-decoration: none;
}

.lab-btn-pdf:hover {
  transform: translateY(-2px);
  background: #FFFBEF;
}

/* ==========================================================================
   WHEY CALCULATOR & PROTEIN MATH STYLES
   ========================================================================== */
.pg-roti-slider {
  width: 100%;
  accent-color: #FFC107;
  cursor: pointer;
}

.pg-whey-card {
  background: #FFF;
  border: 2px solid #121212;
  border-radius: 20px;
  padding: 2.5rem 2rem;
  box-shadow: 6px 6px 0 #121212;
  margin-top: 2.5rem;
}

.pg-whey-header {
  text-align: center;
  max-width: 680px;
  margin: 0 auto 2rem;
}

.pg-whey-kicker {
  display: inline-block;
  background: #E8F5E9;
  color: #2E7D32;
  font-size: 10.5px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  padding: 0.35rem 0.85rem;
  border-radius: 9999px;
  margin-bottom: 0.75rem;
}

.pg-whey-title {
  font-size: clamp(1.8rem, 3.5vw, 2.6rem);
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.pg-whey-sub {
  font-size: 0.95rem;
  color: rgba(18, 18, 18, 0.75);
  line-height: 1.6;
}

.pg-whey-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

@media (min-width: 768px) {
  .pg-whey-grid {
    grid-template-columns: 1fr 1fr;
  }
}

.pg-whey-box {
  background: #FAF7F2;
  border: 1.5px solid rgba(18, 18, 18, 0.12);
  border-radius: 14px;
  padding: 1.75rem;
  text-align: center;
  position: relative;
}

.pg-whey-box.winner {
  background: #FFFDF5;
  border: 2px solid #D4942A;
  box-shadow: 4px 4px 0 #D4942A;
}

.pg-whey-box-badge {
  position: absolute;
  top: -12px;
  right: 18px;
  background: #2E7D32;
  color: #FFF;
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  padding: 3px 10px;
  border-radius: 9999px;
}

.pg-whey-box-title {
  font-size: 0.9rem;
  font-weight: 700;
  color: rgba(18, 18, 18, 0.75);
  margin-bottom: 0.5rem;
}

.pg-whey-box-price {
  font-family: 'Anton', 'Bebas Neue', system-ui, sans-serif;
  font-size: 2.6rem;
  color: #121212;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.pg-whey-box.winner .pg-whey-box-price {
  color: #D4942A;
}

.pg-whey-box-sub {
  font-size: 0.8rem;
  color: rgba(18, 18, 18, 0.6);
}

.pg-savings-banner {
  background: #121212;
  color: #FFFBEF;
  border-radius: 14px;
  padding: 1.25rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
  justify-content: space-between;
}

@media (min-width: 768px) {
  .pg-savings-banner {
    flex-direction: row;
  }
}

.pg-savings-text {
  font-size: 0.98rem;
}

.pg-savings-text strong {
  color: #FFC107;
  font-size: 1.15rem;
}

.pg-savings-btn {
  background: #FFC107;
  color: #121212;
  font-weight: 800;
  font-size: 0.85rem;
  text-transform: uppercase;
  padding: 0.75rem 1.5rem;
  border-radius: 9999px;
  white-space: nowrap;
  transition: transform 0.15s ease;
  text-decoration: none;
}

.pg-savings-btn:hover {
  transform: translateY(-2px);
}

/* ==========================================================================
   UNIFIED LUXURY DARK MASTER FOOTER
   APPLIES TO BOTH .ft-footer AND .master-footer
   ========================================================================== */
.ft-footer, .master-footer {
  position: relative !important;
  background-color: #121212 !important;
  color: #FFFBEF !important;
  padding: 5rem 0 2.5rem !important;
  border-top: 1px solid rgba(212, 148, 42, 0.3) !important;
}

.ft-footer *, .master-footer * {
  box-sizing: border-box;
}

.ft-logo, .footer-logo, .ft-brand .logo-main {
  font-family: 'Anton', 'Bebas Neue', system-ui, sans-serif !important;
  font-size: 2.2rem !important;
  letter-spacing: 0.02em !important;
  color: #FFFBEF !important;
  margin-bottom: 0.75rem !important;
  line-height: 1 !important;
}

.ft-logo span, .footer-logo span, .ft-brand .logo-main span {
  color: #D4942A !important;
}

.ft-brand-text, .footer-desc {
  font-size: 0.92rem !important;
  line-height: 1.65 !important;
  color: rgba(255, 251, 239, 0.75) !important;
  margin-bottom: 1.25rem !important;
  max-width: 32rem !important;
}

.ft-fssai-box, .footer-fssai {
  font-size: 0.78rem !important;
  line-height: 1.6 !important;
  color: rgba(255, 251, 239, 0.7) !important;
  background: rgba(255, 255, 255, 0.05) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  border-radius: 8px !important;
  padding: 0.85rem 1rem !important;
  margin-bottom: 1.25rem !important;
}

.ft-fssai-box strong, .footer-fssai strong {
  color: #FFC107 !important;
}

.ft-col-title, .footer-col-title {
  font-size: 0.72rem !important;
  font-weight: 800 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.22em !important;
  color: #FFC107 !important;
  margin-bottom: 1.25rem !important;
}

.ft-col-link, .footer-links a {
  font-size: 0.88rem !important;
  color: rgba(255, 251, 239, 0.7) !important;
  text-decoration: none !important;
  transition: color 0.15s ease !important;
}

.ft-col-link:hover, .footer-links a:hover {
  color: #FFFBEF !important;
}

.ft-bottom, .footer-bottom-bar, .footer-bottom {
  margin-top: 3.5rem !important;
  padding-top: 2rem !important;
  border-top: 1px solid rgba(255, 251, 239, 0.12) !important;
  font-size: 0.75rem !important;
  color: rgba(255, 251, 239, 0.5) !important;
}
"""

full_style_css = milld_components_css + "\n\n" + footer_css + "\n\n" + shop_css + "\n\n" + custom_overrides_css

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(full_style_css)

print(f"Generated unified style.css ({len(full_style_css)} bytes)")
