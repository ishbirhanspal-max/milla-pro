import os
import re

print("Starting complete site build and styling unification...")

# ==============================================================================
# 1. BUILD MASTER STYLE.CSS (v22.0)
# ==============================================================================

master_css = """/* ==========================================================================
   MILLA PRO™ AUTHENTIC LUXURY DESIGN SYSTEM (v22.0)
   Typography: Anton (Impactful Display), Caveat (Script Callout), Inter (Ultra-Clean Body)
   Palette: #FFFBEF (Warm Cream), #D4942A (Golden Amber), #121212 (Ink Black), #FFC107 (Warm Yellow)
   ========================================================================== */

@import url('https://fonts.googleapis.com/css2?family=Anton&family=Caveat:wght@400;600;700&family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
  --color-background: #FFFBEF;
  --color-foreground: #121212;
  --color-accent: #D4942A;
  --color-yellow: #FFC107;
  --primary: #D4942A;
  --primary-hover: #B87C1D;
  --primary-light: #FFF5EE;
  --dark: #121212;
  --bg-cream: #FDF8EE;
  --bg-warm: #FFFBEF;
  --bg-light: #FEF8E9;
  --border-light: rgba(18, 18, 18, 0.12);
  --border-dark: #121212;
  --text-dark: #121212;
  --text-muted: rgba(18, 18, 18, 0.65);
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 20px;
  --radius-full: 9999px;
  --shadow-sm: 0 2px 8px rgba(18, 18, 18, 0.05);
  --shadow-md: 0 6px 20px rgba(18, 18, 18, 0.08);
  --shadow-lg: 0 12px 32px rgba(18, 18, 18, 0.12);
  --font-heading: 'Anton', 'Bebas Neue', system-ui, sans-serif;
  --font-script: 'Caveat', cursive;
  --font-body: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Universal Reset */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 16px;
  scroll-behavior: smooth;
  -webkit-text-size-adjust: 100%;
  overflow-x: hidden;
}

body {
  font-family: var(--font-body);
  background-color: var(--color-background);
  color: var(--color-foreground);
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow-x: hidden;
  width: 100%;
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading);
  letter-spacing: -0.01em;
  color: var(--color-foreground);
  margin-top: 0;
}

p, span, div, li, td, th {
  font-family: var(--font-body);
}

img, video, svg {
  max-width: 100%;
  height: auto;
  display: block;
}

a {
  color: inherit;
  text-decoration: none;
}

button {
  font-family: inherit;
  cursor: pointer;
}

.container {
  width: 100%;
  max-width: 1180px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* ==========================================================================
   1. Top Ultra-Thin Moving Marquee Ticker Bar
   ========================================================================== */
.top-ticker-bar {
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
}

.ticker-scroll-track {
  display: flex;
  width: max-content;
  animation: topTickerScroll 28s linear infinite;
}

.ticker-scroll-content {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding-right: 1.5rem;
  flex-shrink: 0;
}

.ticker-scroll-content span {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}

.ticker-dot {
  color: #D4942A;
  opacity: 0.7;
}

@keyframes topTickerScroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

/* ==========================================================================
   2. Sticky Master Header
   ========================================================================== */
.master-header {
  position: sticky;
  top: 0;
  z-index: 999;
  background: rgba(255, 251, 239, 0.96);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-bottom: 1px solid var(--border-light);
  height: 68px;
  transition: all 0.2s ease;
}

.header-inner {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
}

.brand-logo {
  text-decoration: none;
  display: flex;
  flex-direction: column;
  line-height: 1;
}

.brand-logo .logo-main {
  font-family: var(--font-heading);
  font-size: 1.95rem;
  letter-spacing: 0.02em;
  color: var(--color-foreground);
}

.brand-logo .logo-main span {
  color: var(--color-accent);
}

.brand-logo .logo-sub {
  font-family: var(--font-body);
  font-size: 0.62rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--text-muted);
  font-weight: 800;
  margin-top: 1px;
}

.desktop-nav {
  display: flex;
  align-items: center;
  gap: 1.75rem;
}

.desktop-nav a {
  text-decoration: none;
  color: var(--color-foreground);
  font-size: 0.86rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  transition: color 0.15s ease;
  position: relative;
}

.desktop-nav a:hover,
.desktop-nav a.active {
  color: var(--color-accent);
}

.desktop-nav .shop-pill-nav {
  background: #121212;
  color: #FFFBEF !important;
  padding: 0.45rem 1.15rem;
  border-radius: 9999px;
  font-weight: 700;
  box-shadow: 0 4px 0 -1px #FFC107;
  transition: transform 0.15s ease;
}

.desktop-nav .shop-pill-nav:hover {
  transform: translateY(-1px);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.icon-btn {
  background: none;
  border: 1.5px solid var(--border-light);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-foreground);
  position: relative;
  transition: all 0.15s ease;
  cursor: pointer;
}

.icon-btn:hover {
  border-color: var(--color-accent);
  color: var(--color-accent);
  background: rgba(212, 148, 42, 0.08);
}

.cart-badge-count {
  position: absolute;
  top: -4px;
  right: -4px;
  background: var(--color-accent);
  color: #121212;
  font-size: 0.65rem;
  font-weight: 900;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #FFFBEF;
}

.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  color: var(--color-foreground);
  cursor: pointer;
  padding: 4px;
}

@media (max-width: 900px) {
  .desktop-nav { display: none; }
  .mobile-menu-btn { display: block; }
}

/* ==========================================================================
   3. Mobile Sidebar Drawer & Cart Drawer
   ========================================================================== */
.sidebar-overlay, .cart-overlay, .modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(18, 18, 18, 0.65);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  z-index: 10000;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.25s ease;
}

.sidebar-overlay.active, .cart-overlay.active, .modal-overlay.active {
  opacity: 1;
  pointer-events: auto;
}

.mobile-sidebar {
  position: fixed;
  top: 0;
  right: 0;
  width: 320px;
  max-width: 85vw;
  height: 100vh;
  background: #FFFBEF;
  z-index: 10001;
  transform: translateX(100%);
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  flex-direction: column;
  box-shadow: -10px 0 30px rgba(18, 18, 18, 0.25);
  padding: 1.5rem;
}

.mobile-sidebar.active {
  transform: translateX(0);
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid var(--border-light);
}

.cart-close-btn {
  background: none;
  border: 1px solid var(--border-light);
  border-radius: 50%;
  width: 34px;
  height: 34px;
  font-size: 1rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--color-foreground);
}

.mobile-shop-cta-btn {
  background: #121212;
  color: #FFFBEF;
  border-radius: 9999px;
  padding: 0.85rem 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: 800;
  font-size: 0.85rem;
  letter-spacing: 0.05em;
  margin: 1.25rem 0;
  box-shadow: 0 4px 0 0 #FFC107;
  text-decoration: none;
}

.mobile-nav-links {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  overflow-y: auto;
  flex: 1;
}

.mobile-nav-links a {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 0.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--color-foreground);
  border-bottom: 1px solid rgba(18, 18, 18, 0.06);
}

.sidebar-trust-footer {
  margin-top: auto;
  padding-top: 1rem;
  border-top: 1px solid var(--border-light);
  font-size: 0.72rem;
  color: var(--text-muted);
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.cart-drawer {
  position: fixed;
  top: 0;
  right: 0;
  width: 420px;
  max-width: 90vw;
  height: 100vh;
  background: #FFFBEF;
  z-index: 10001;
  transform: translateX(100%);
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  flex-direction: column;
  box-shadow: -10px 0 35px rgba(18, 18, 18, 0.3);
}

.cart-drawer.active {
  transform: translateX(0);
}

.cart-drawer-header {
  padding: 1.25rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-light);
  background: #FFF;
}

.cart-drawer-title {
  font-family: var(--font-heading);
  font-size: 1.25rem;
  letter-spacing: 0.02em;
}

.cart-policy-strip {
  background: #FFF9E6;
  border-bottom: 1px solid rgba(212, 148, 42, 0.25);
  padding: 0.75rem 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-size: 0.75rem;
}

.cart-policy-item {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.cart-policy-item span:first-child {
  flex-shrink: 0;
}

.cart-policy-item div strong {
  display: block;
  color: #121212;
}

.cart-policy-item div span {
  color: rgba(18, 18, 18, 0.7);
}

.cart-items-container {
  flex: 1;
  overflow-y: auto;
  padding: 1.25rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.cart-item {
  display: flex;
  gap: 1rem;
  background: #FFF;
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  padding: 0.85rem;
  align-items: center;
}

.cart-item-img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: var(--radius-sm);
  background: #FAF7F2;
}

.cart-item-info {
  flex: 1;
}

.cart-item-title {
  font-weight: 700;
  font-size: 0.88rem;
  color: #121212;
}

.cart-item-price {
  font-family: var(--font-heading);
  font-size: 1.1rem;
  color: var(--color-accent);
}

.cart-drawer-footer {
  padding: 1.25rem 1.5rem;
  background: #FFF;
  border-top: 1px solid var(--border-light);
}

.bill-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.82rem;
  margin-bottom: 0.4rem;
  color: rgba(18, 18, 18, 0.75);
}

.bill-row.total-row {
  font-size: 1.1rem;
  font-weight: 800;
  color: #121212;
  border-top: 1px dashed var(--border-light);
  padding-top: 0.6rem;
  margin-top: 0.6rem;
}

.cart-checkout-btn {
  width: 100%;
  background: #121212;
  color: #FFFBEF;
  border: none;
  border-radius: var(--radius-full);
  padding: 0.95rem;
  font-size: 0.92rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 1rem;
  box-shadow: 0 4px 0 0 #FFC107;
  cursor: pointer;
  transition: transform 0.15s ease;
}

.cart-checkout-btn:hover {
  transform: translateY(-2px);
}

/* ==========================================================================
   4. Hero Section (.milld-hs) - CLEAN, CENTERED TYPOGRAPHIC HERO
   NO FOOD PHOTO AT THE TOP. PERFECT LAPTOP & MOBILE ALIGNMENT.
   ========================================================================== */
.milld-hs {
  position: relative;
  background-color: #FFFBEF;
  color: #121212;
  padding: 3rem 0 2rem;
  overflow: hidden;
  text-align: center;
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
  width: 100% !important;
  max-width: 860px !important;
  margin: 0 auto !important;
  text-align: center !important;
  position: relative;
  z-index: 10;
}

.milld-hs .mh-badge {
  display: inline-flex;
  align-items: center;
  white-space: nowrap;
  border-radius: 9999px;
  border: 1.5px solid #121212;
  background: #FFC107;
  padding: 0.45rem 1.25rem;
  font-size: 11.5px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: #121212;
  box-shadow: 0 4px 0 -1px rgba(18, 18, 18, 0.25);
  margin-bottom: 1.5rem;
}

.milld-hs .mh-h1 {
  font-family: var(--font-heading);
  text-transform: uppercase;
  line-height: 1.04;
  letter-spacing: -0.01em;
  margin: 0 0 1.25rem;
  color: #121212;
  font-weight: 400;
  font-size: clamp(2.6rem, 6.5vw, 5.2rem);
}

.milld-hs .mh-brush {
  background-image: linear-gradient(120deg, #FFC107 0%, #FFC107 100%);
  background-repeat: no-repeat;
  background-size: 100% 38%;
  background-position: 0 84%;
  padding: 0 0.2em;
  color: #121212;
  white-space: nowrap;
}

.milld-hs .mh-sub {
  margin: 1.25rem auto 2.25rem;
  max-width: 44rem;
  font-size: clamp(1.05rem, 2.2vw, 1.35rem);
  line-height: 1.6;
  color: rgba(18, 18, 18, 0.85);
}

.milld-hs .mh-sub strong {
  font-family: var(--font-script);
  font-size: 2rem;
  line-height: 1;
  font-weight: 700;
  color: #FFFBEF;
  background-image: linear-gradient(120deg, #D4942A 0%, #D4942A 100%);
  background-size: 100% 100%;
  background-repeat: no-repeat;
  padding: 0.08em 0.45em;
  border-radius: 4px;
  display: inline-block;
  margin-bottom: 0.4rem;
}

/* Tilted Marquee Strip */
.marquee-tilted-wrap {
  width: 100vw;
  position: relative;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
  margin-top: 1.75rem;
  margin-bottom: 2rem;
  overflow: hidden;
  padding: 0.75rem 0;
}

.marquee-tilted-inner {
  width: 110%;
  margin-left: -5%;
  transform: rotate(-1.5deg);
  background: #FFC107;
  border-top: 1.5px solid #121212;
  border-bottom: 1.5px solid #121212;
  box-shadow: 0 8px 24px -4px rgba(18, 18, 18, 0.15);
  overflow: hidden;
}

.ms-track {
  display: flex;
  align-items: center;
  white-space: nowrap;
  animation: milldMarquee 20s linear infinite;
  padding: 0.85rem 0;
}

.ms-text {
  flex-shrink: 0;
  margin: 0 1.5rem;
  font-family: var(--font-heading);
  font-size: 1.15rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #121212;
}

.ms-icon {
  display: inline-flex;
  align-items: center;
  flex-shrink: 0;
  width: 1.2rem;
  height: 1.2rem;
  margin: 0 1rem;
}

@keyframes milldMarquee {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

/* CTA Buttons */
.milld-hs .mh-ctas {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center !important;
  gap: 1.25rem;
  margin: 2.25rem auto 1.5rem;
}

.mh-btn-shop {
  display: inline-flex;
  align-items: center;
  gap: 0.85rem;
  border-radius: 9999px;
  background: #121212;
  padding: 0.85rem 1.5rem 0.85rem 2.25rem;
  color: #FFFBEF;
  text-decoration: none;
  box-shadow: 0 8px 0 -2px #FFC107;
  transition: transform 0.2s ease;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-size: 0.95rem;
}

.mh-btn-shop:hover {
  transform: translateY(-2px);
}

.mh-btn-icon {
  display: grid;
  place-items: center;
  width: 2.3rem;
  height: 2.3rem;
  border-radius: 50%;
  background: #FFC107;
  color: #121212;
  flex-shrink: 0;
}

.mh-btn-learn {
  font-size: 0.95rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #121212;
  text-decoration: underline;
  text-decoration-color: #FFC107;
  text-decoration-thickness: 4px;
  text-underline-offset: 5px;
  transition: color 0.15s ease;
}

.mh-btn-learn:hover {
  color: var(--color-accent);
}

/* 3 Macro Stat Badges */
.milld-hs .mh-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
  max-width: 38rem;
  margin: 2.5rem auto 1rem !important;
}

.mh-stat-box {
  background: #FFF;
  border: 1.5px solid #121212;
  border-radius: var(--radius-md);
  padding: 1rem 0.75rem;
  box-shadow: 4px 4px 0 #121212;
}

.milld-hs .mh-stat-n {
  font-family: var(--font-heading);
  font-size: 2.2rem !important;
  line-height: 1;
  color: #D4942A;
}

.mh-stat-label {
  margin-top: 0.4rem;
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: rgba(18, 18, 18, 0.7);
}

/* ==========================================================================
   5. Protein Gap & Whey Cost Calculator (.pg-section)
   ========================================================================== */
.pg-section {
  padding: 4.5rem 0;
  background: #FAF7F2;
  border-top: 1px solid var(--border-light);
  border-bottom: 1px solid var(--border-light);
}

.pg-container {
  max-width: 1140px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.pg-top-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

@media (min-width: 900px) {
  .pg-top-grid {
    grid-template-columns: 1.1fr 0.9fr;
    align-items: center;
  }
}

.pg-heading {
  font-size: clamp(2.2rem, 4.5vw, 3.8rem);
  line-height: 1.08;
  text-transform: uppercase;
}

.pg-heading-accent {
  color: #D4942A;
}

.pg-note-wrap {
  background: #FFF;
  border: 2px solid #121212;
  border-radius: var(--radius-md);
  padding: 1.5rem;
  box-shadow: 4px 4px 0 #121212;
  position: relative;
}

.pg-note-text {
  font-size: 1.05rem;
  line-height: 1.6;
  color: rgba(18, 18, 18, 0.85);
}

.pg-calc-wrap {
  margin-bottom: 2.5rem;
}

.pg-calc {
  background: #121212;
  color: #FFFBEF;
  border-radius: var(--radius-lg);
  padding: 2.5rem 2rem;
  position: relative;
  overflow: hidden;
  box-shadow: 0 12px 36px rgba(18, 18, 18, 0.15);
}

.pg-calc-inner {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

@media (min-width: 900px) {
  .pg-calc-inner {
    grid-template-columns: 1.1fr 0.9fr;
    align-items: center;
  }
}

.pg-calc-title {
  font-family: var(--font-heading);
  font-size: 1.75rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: #FFC107;
  margin-bottom: 1.25rem;
}

.pg-slider-box {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: var(--radius-md);
  padding: 1.5rem;
}

.pg-slider-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 1rem;
}

.pg-slider-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #FFFBEF;
}

.pg-slider-count {
  font-family: var(--font-heading);
  font-size: 1.85rem;
  color: #FFC107;
}

.pg-roti-slider {
  width: 100%;
  accent-color: #FFC107;
  cursor: pointer;
  height: 8px;
}

.pg-compare-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.pg-compare-box {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: var(--radius-md);
  padding: 1.25rem;
  text-align: center;
}

.pg-compare-milld {
  background: rgba(212, 148, 42, 0.2);
  border-color: #D4942A;
}

.pg-compare-label {
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: rgba(255, 251, 239, 0.7);
  margin-bottom: 0.25rem;
}

.pg-compare-label--milld {
  color: #FFC107;
}

.pg-compare-value {
  font-family: var(--font-heading);
  font-size: 2.2rem;
  color: #FFFBEF;
}

.pg-compare-value--milld {
  color: #FFC107;
}

.pg-result-box {
  margin-top: 1.25rem;
  background: rgba(255, 193, 7, 0.15);
  border: 1px solid #FFC107;
  border-radius: var(--radius-sm);
  padding: 0.85rem;
  text-align: center;
}

.pg-result-text {
  font-size: 0.95rem;
  font-weight: 700;
  color: #FFFBEF;
}

.pg-result-num {
  color: #FFC107;
  font-family: var(--font-heading);
  font-size: 1.3rem;
}

/* Whey Cost Calculator Card (@ ₹3,500/kg benchmark) */
.pg-whey-card {
  background: #FFF;
  border: 2px solid #121212;
  border-radius: var(--radius-lg);
  padding: 2.5rem 2rem;
  box-shadow: 6px 6px 0 #121212;
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
  border: 1.5px solid var(--border-light);
  border-radius: var(--radius-md);
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
  font-family: var(--font-heading);
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
  border-radius: var(--radius-md);
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
}

.pg-savings-btn:hover {
  transform: translateY(-2px);
}

/* ==========================================================================
   6. Every Roti Broken Down (.rr-section)
   ========================================================================== */
.rr-section {
  padding: 5rem 0;
  background: #FFFBEF;
}

.rr-container {
  max-width: 1140px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.rr-heading-wrap {
  text-align: center;
  margin-bottom: 3.5rem;
}

.rr-heading {
  font-size: clamp(2.4rem, 5vw, 4rem);
  text-transform: uppercase;
}

.rr-brush {
  background-image: linear-gradient(120deg, #FFC107 0%, #FFC107 100%);
  background-repeat: no-repeat;
  background-size: 100% 35%;
  background-position: 0 85%;
  padding: 0 0.2em;
}

.rr-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 3rem;
  align-items: center;
}

@media (min-width: 900px) {
  .rr-grid {
    grid-template-columns: 1fr 1fr;
  }
}

.rr-photo-col {
  position: relative;
  border: 2px solid #121212;
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: 6px 6px 0 #121212;
}

.rr-photo {
  width: 100%;
  height: auto;
  display: block;
}

.rr-badge {
  position: absolute;
  bottom: 20px;
  right: 20px;
  background: #121212;
  color: #FFFBEF;
  padding: 0.75rem 1.25rem;
  border-radius: var(--radius-md);
  text-align: center;
  border: 1px solid #FFC107;
}

.rr-badge-protein {
  font-family: var(--font-heading);
  font-size: 1.85rem;
  color: #FFC107;
  line-height: 1;
}

.rr-badge-label {
  font-size: 9px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: rgba(255, 251, 239, 0.7);
}

.rr-bars-col {
  display: flex;
  flex-direction: column;
}

.rr-bars-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.rr-bar-item {
  background: #FFF;
  border: 1.5px solid #121212;
  border-radius: var(--radius-md);
  padding: 1.25rem 1.5rem;
  box-shadow: 4px 4px 0 #121212;
}

.rr-bar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.6rem;
}

.rr-bar-name {
  font-weight: 700;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.rr-bar-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.rr-bar-pct {
  font-family: var(--font-heading);
  font-size: 1.4rem;
  color: #121212;
}

.rr-bar-track {
  height: 10px;
  background: #FAF7F2;
  border: 1px solid rgba(18, 18, 18, 0.15);
  border-radius: 9999px;
  overflow: hidden;
}

.rr-bar-fill {
  height: 100%;
  border-radius: 9999px;
  transition: width 1s ease-in-out;
}

/* ==========================================================================
   7. Three Fractions Cards (.bc-section)
   ========================================================================== */
.bc-section {
  padding: 5rem 0;
  background: #FAF7F2;
  border-top: 1px solid var(--border-light);
  border-bottom: 1px solid var(--border-light);
}

.bc-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.75rem;
}

@media (min-width: 640px) {
  .bc-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .bc-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.bc-card {
  background: #FFF;
  border: 2px solid #121212;
  border-radius: var(--radius-lg);
  padding: 2rem 1.5rem;
  box-shadow: 5px 5px 0 #121212;
  display: flex;
  flex-direction: column;
  position: relative;
}

.bc-badge {
  font-family: var(--font-heading);
  font-size: 1.75rem;
  color: #D4942A;
  margin-bottom: 0.5rem;
}

.bc-title {
  font-size: 1.35rem;
  text-transform: uppercase;
  margin-bottom: 0.75rem;
}

.bc-sub {
  font-size: 0.92rem;
  line-height: 1.6;
  color: rgba(18, 18, 18, 0.75);
}

/* ==========================================================================
   8. Verified Lab Reports Details Section (.lab-showcase-section)
   ONLY CLEAN DETAILS ON SITE. FULL REPORTS HIDDEN BEHIND LINK/MODAL.
   ========================================================================== */
.lab-showcase-section {
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

/* Lab Details Parameter Cards Grid */
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
  border-radius: var(--radius-md);
  padding: 1.25rem;
  text-align: center;
  box-shadow: 4px 4px 0 #121212;
  transition: transform 0.15s ease;
}

.lab-detail-card.highlight {
  background: #FFFDF5;
  border-color: #D4942A;
  box-shadow: 4px 4px 0 #D4942A;
}

.lab-param-val {
  font-family: var(--font-heading);
  font-size: 2.2rem;
  color: #121212;
  line-height: 1.1;
}

.lab-detail-card.highlight .lab-param-val {
  color: #D4942A;
}

.lab-param-name {
  font-size: 0.85rem;
  font-weight: 700;
  color: #121212;
  margin: 0.35rem 0 0.2rem;
}

.lab-param-method {
  font-size: 0.7rem;
  color: rgba(18, 18, 18, 0.55);
  font-weight: 600;
}

/* Lab Credentials Banner */
.lab-credentials-banner {
  background: #FFF;
  border: 2px solid #121212;
  border-radius: var(--radius-lg);
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
}

.lab-btn-pdf:hover {
  transform: translateY(-2px);
  background: #FFFBEF;
}

/* ==========================================================================
   9. Cost Comparison Table Section (.ss-section)
   ========================================================================== */
.ss-section {
  padding: 5rem 0;
  background: #FAF7F2;
  border-top: 1px solid var(--border-light);
}

.ss-container {
  max-width: 1140px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.ss-panel {
  background: #FFF;
  border: 2px solid #121212;
  border-radius: var(--radius-lg);
  padding: 3rem 2rem;
  box-shadow: 6px 6px 0 #121212;
}

.ss-panel-heading {
  text-align: center;
  font-size: clamp(2.2rem, 4.5vw, 3.5rem);
  text-transform: uppercase;
  margin-bottom: 2.5rem;
}

.ss-gold {
  color: #D4942A;
}

.ss-compare-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-top: 1.5rem;
}

.ss-compare-table th,
.ss-compare-table td {
  padding: 1.25rem 1rem;
  text-align: left;
  border-bottom: 1px solid rgba(18, 18, 18, 0.1);
  font-size: 0.95rem;
}

.ss-compare-table th {
  font-family: var(--font-heading);
  font-size: 1.15rem;
  text-transform: uppercase;
  background: #FAF7F2;
}

.ss-compare-table tr.highlight-row td {
  background: rgba(255, 193, 7, 0.12);
  font-weight: 700;
}

.ss-stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
  margin-top: 3rem;
}

@media (min-width: 900px) {
  .ss-stats-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

.ss-stat-card {
  background: #FAF7F2;
  border: 1.5px solid var(--border-light);
  border-radius: var(--radius-md);
  padding: 1.25rem;
  text-align: center;
}

.ss-stat-num {
  font-family: var(--font-heading);
  font-size: 2rem;
  color: #D4942A;
}

.ss-stat-label {
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  color: rgba(18, 18, 18, 0.65);
  margin-top: 0.35rem;
}

/* ==========================================================================
   10. Reviews & FAQ Sections (.tm-section & .faq-section)
   ========================================================================== */
.tm-section {
  padding: 5rem 0;
  background: #121212;
  color: #FFFBEF;
  overflow: hidden;
}

.tm-container {
  max-width: 1140px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.tm-heading {
  text-align: center;
  font-size: clamp(2.2rem, 4.5vw, 3.6rem);
  text-transform: uppercase;
  color: #FFFBEF;
  margin-bottom: 3rem;
}

.tm-heading span {
  color: #FFC107;
}

.tm-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .tm-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.tm-card {
  background: #1C1C1C;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: var(--radius-md);
  padding: 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.tm-stars {
  color: #FFC107;
  font-size: 1.1rem;
}

.tm-quote {
  font-size: 0.95rem;
  line-height: 1.6;
  color: rgba(255, 251, 239, 0.85);
  font-style: italic;
}

.tm-author {
  font-size: 0.85rem;
  font-weight: 700;
  color: #FFC107;
}

.tm-location {
  font-size: 0.75rem;
  color: rgba(255, 251, 239, 0.5);
}

.faq-section {
  padding: 5rem 0;
  background: #FFFBEF;
}

.faq-container {
  max-width: 820px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.faq-title {
  text-align: center;
  font-size: clamp(2.2rem, 4.5vw, 3.6rem);
  text-transform: uppercase;
  margin-bottom: 2.5rem;
}

.faq-accordion {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.faq-item {
  background: #FFF;
  border: 1.5px solid #121212;
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: 3px 3px 0 #121212;
}

.faq-btn {
  width: 100%;
  padding: 1.25rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: none;
  border: none;
  text-align: left;
  cursor: pointer;
}

.faq-question {
  font-weight: 700;
  font-size: 1.05rem;
  color: #121212;
}

.faq-icon {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
  color: #D4942A;
  transition: transform 0.2s ease;
}

.faq-body {
  display: none;
  padding: 0 1.5rem 1.25rem;
  border-top: 1px solid rgba(18, 18, 18, 0.08);
}

.faq-item.active .faq-body {
  display: block;
  padding-top: 1rem;
}

.faq-item.active .faq-icon {
  transform: rotate(45deg);
}

.faq-answer {
  font-size: 0.95rem;
  line-height: 1.6;
  color: rgba(18, 18, 18, 0.8);
}

/* ==========================================================================
   11. Unified Luxury Dark Master Footer (.ft-footer & .master-footer)
   NEVER PLAIN TEXT. HIGH CONTRAST, LUXURY GOLD HEADINGS, CLEAN COLUMNS.
   ========================================================================== */
.ft-footer, .master-footer {
  position: relative;
  background-color: #121212 !important;
  color: #FFFBEF !important;
  padding: 5rem 0 2.5rem;
  border-top: 1px solid rgba(212, 148, 42, 0.3);
  font-family: var(--font-body);
}

.ft-container, .master-footer .container {
  max-width: 1180px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.ft-grid, .footer-top-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 3rem;
}

@media (min-width: 900px) {
  .ft-grid, .footer-top-grid {
    grid-template-columns: 1.2fr 1.8fr;
    gap: 4rem;
    align-items: start;
  }
}

.ft-brand, .footer-brand-col {
  display: flex;
  flex-direction: column;
}

.ft-logo, .footer-logo {
  font-family: var(--font-heading);
  font-size: 2.2rem;
  letter-spacing: 0.02em;
  color: #FFFBEF !important;
  margin-bottom: 0.75rem;
  line-height: 1;
}

.ft-logo span, .footer-logo span {
  color: #D4942A !important;
}

.ft-brand-text, .footer-desc {
  font-size: 0.92rem;
  line-height: 1.65;
  color: rgba(255, 251, 239, 0.75) !important;
  margin-bottom: 1.25rem;
  max-width: 32rem;
}

.ft-fssai-box, .footer-fssai {
  font-size: 0.78rem;
  line-height: 1.6;
  color: rgba(255, 251, 239, 0.65) !important;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-sm);
  padding: 0.85rem 1rem;
  margin-bottom: 1.25rem;
}

.ft-fssai-box strong, .footer-fssai strong {
  color: #FFC107;
}

.ft-cta-note {
  font-family: var(--font-script);
  font-size: 1.35rem;
  font-weight: 600;
  color: #FFC107;
}

.ft-nav-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

@media (min-width: 640px) {
  .ft-nav-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 2rem;
  }
}

.ft-col, .footer-nav-col {
  display: flex;
  flex-direction: column;
}

.ft-col-title, .footer-col-title {
  font-size: 0.72rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.22em;
  color: #FFC107 !important;
  margin-bottom: 1.25rem;
}

.ft-col-list, .footer-links {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.ft-col-link, .footer-links a {
  font-size: 0.88rem;
  color: rgba(255, 251, 239, 0.7) !important;
  text-decoration: none;
  transition: color 0.15s ease;
}

.ft-col-link:hover, .footer-links a:hover {
  color: #FFFBEF !important;
}

.ft-bottom, .footer-bottom-bar, .footer-bottom {
  margin-top: 3.5rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 251, 239, 0.12);
  display: flex;
  flex-direction: column;
  gap: 1rem;
  font-size: 0.75rem;
  color: rgba(255, 251, 239, 0.5) !important;
}

@media (min-width: 640px) {
  .ft-bottom, .footer-bottom-bar, .footer-bottom {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}

/* ==========================================================================
   12. Complete Shop Page Styling (.shop-* classes for products.html)
   ========================================================================== */
.shop-hero-section {
  padding: 3.5rem 0 5rem;
  background: #FFFBEF;
}

.shop-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 3.5rem;
  align-items: start;
}

@media (min-width: 900px) {
  .shop-grid {
    grid-template-columns: 1.05fr 0.95fr;
  }
}

.shop-gallery-wrap {
  position: sticky;
  top: 88px;
}

.shop-main-img-card {
  background: #FFF;
  border: 2px solid #121212;
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  text-align: center;
  box-shadow: 6px 6px 0 #121212;
  margin-bottom: 1.25rem;
}

.shop-main-img-card img {
  max-width: 380px;
  width: 100%;
  border-radius: var(--radius-md);
  margin: 0 auto;
}

.shop-thumbs-row {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
}

.thumb-btn {
  background: #FFF;
  border: 1.5px solid #121212;
  border-radius: var(--radius-sm);
  padding: 0.5rem 1rem;
  font-size: 0.8rem;
  font-weight: 800;
  color: #121212;
  cursor: pointer;
  transition: all 0.15s ease;
  box-shadow: 2px 2px 0 #121212;
}

.thumb-btn.active, .thumb-btn:hover {
  background: #FFC107;
  border-color: #121212;
}

.shop-buy-panel {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.shop-product-title {
  font-size: clamp(2rem, 4vw, 3rem);
  text-transform: uppercase;
  line-height: 1.1;
}

.shop-product-tagline {
  font-size: 0.95rem;
  color: rgba(18, 18, 18, 0.75);
}

.shop-price-row {
  display: flex;
  align-items: baseline;
  gap: 1rem;
  padding: 1rem 0;
  border-top: 1px solid var(--border-light);
  border-bottom: 1px solid var(--border-light);
}

.shop-cur-price {
  font-family: var(--font-heading);
  font-size: 2.4rem;
  color: #121212;
}

.shop-mrp-strike {
  font-size: 1.1rem;
  color: rgba(18, 18, 18, 0.5);
  text-decoration: line-through;
}

.shop-discount-pill {
  background: #E8F5E9;
  color: #2E7D32;
  font-size: 0.78rem;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 9999px;
}

.shop-pack-selector {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.shop-pack-card {
  background: #FFF;
  border: 2px solid #121212;
  border-radius: var(--radius-md);
  padding: 1rem 1.25rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 3px 3px 0 #121212;
  transition: all 0.15s ease;
}

.shop-pack-card.active {
  background: #FFFDF5;
  border-color: #D4942A;
  box-shadow: 4px 4px 0 #D4942A;
}

.spc-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.spc-radio {
  width: 20px;
  height: 20px;
  border: 2px solid #121212;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.shop-pack-card.active .spc-radio {
  border-color: #D4942A;
}

.spc-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: transparent;
}

.shop-pack-card.active .spc-dot {
  background: #D4942A;
}

.spc-title {
  font-weight: 800;
  font-size: 1rem;
  color: #121212;
}

.spc-desc {
  font-size: 0.78rem;
  color: rgba(18, 18, 18, 0.65);
}

.spc-price {
  font-family: var(--font-heading);
  font-size: 1.4rem;
  color: #121212;
  text-align: right;
}

.spc-badge {
  font-size: 0.7rem;
  font-weight: 800;
  background: #E8F5E9;
  color: #2E7D32;
  padding: 2px 8px;
  border-radius: 4px;
  display: inline-block;
}

.shop-action-row {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.qty-stepper {
  display: flex;
  align-items: center;
  background: #FFF;
  border: 2px solid #121212;
  border-radius: var(--radius-full);
  padding: 4px;
}

.qty-btn {
  background: none;
  border: none;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.1rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.qty-btn:hover {
  background: #FAF7F2;
}

.qty-input {
  width: 40px;
  text-align: center;
  font-size: 1rem;
  font-weight: 800;
  border: none;
  background: none;
  color: #121212;
}

.buy-now-btn-main {
  flex: 1;
  background: #121212;
  color: #FFFBEF;
  border: none;
  border-radius: var(--radius-full);
  padding: 0.95rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 800;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  box-shadow: 0 4px 0 0 #FFC107;
  transition: transform 0.15s ease;
}

.buy-now-btn-main:hover {
  transform: translateY(-2px);
}

.add-cart-outline-btn {
  background: #FFF;
  color: #121212;
  border: 2px solid #121212;
  border-radius: var(--radius-full);
  padding: 0.9rem 1.5rem;
  font-size: 0.9rem;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 3px 3px 0 #121212;
  transition: all 0.15s ease;
}

.add-cart-outline-btn:hover {
  background: #FFFBEF;
  transform: translateY(-1px);
}

.shop-trust-points {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 1rem 0;
  border-top: 1px solid var(--border-light);
  font-size: 0.8rem;
  font-weight: 700;
  color: rgba(18, 18, 18, 0.7);
}

/* ==========================================================================
   13. Simulated Razorpay 2-Step Modal
   ========================================================================== */
.razorpay-simulated-modal {
  background: #FFF;
  border-radius: var(--radius-lg);
  max-width: 480px;
  width: 92%;
  margin: 5vh auto;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
}

.rp-header {
  background: #121212;
  color: #FFFBEF;
  padding: 1.25rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.rp-header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.rp-brand-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #FFC107;
  color: #121212;
  font-family: var(--font-heading);
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.rp-merchant-name {
  font-weight: 800;
  font-size: 0.95rem;
}

.rp-order-sub {
  font-size: 0.72rem;
  color: rgba(255, 251, 239, 0.7);
}

.rp-close {
  background: none;
  border: none;
  color: #FFFBEF;
  font-size: 1.25rem;
  cursor: pointer;
}

.rp-stepper-bar {
  display: flex;
  background: #FAF7F2;
  border-bottom: 1px solid var(--border-light);
}

.rp-step-item {
  flex: 1;
  padding: 0.75rem;
  font-size: 0.8rem;
  font-weight: 700;
  text-align: center;
  color: rgba(18, 18, 18, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
}

.rp-step-item.active {
  color: #121212;
  border-bottom: 2px solid #D4942A;
  background: #FFF;
}

.rp-step-num {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: rgba(18, 18, 18, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
}

.rp-step-item.active .rp-step-num {
  background: #D4942A;
  color: #FFF;
}

.rp-body {
  padding: 1.5rem;
}

.rp-form-group {
  margin-bottom: 1rem;
}

.rp-form-group label {
  display: block;
  font-size: 0.8rem;
  font-weight: 700;
  margin-bottom: 0.35rem;
  color: #121212;
}

.rp-input {
  width: 100%;
  padding: 0.75rem 0.85rem;
  border: 1.5px solid var(--border-light);
  border-radius: var(--radius-sm);
  font-size: 0.9rem;
  font-family: inherit;
}

.rp-input:focus {
  outline: none;
  border-color: #D4942A;
}

.rp-btn-primary {
  width: 100%;
  background: #121212;
  color: #FFFBEF;
  border: none;
  padding: 0.9rem;
  border-radius: var(--radius-sm);
  font-weight: 800;
  font-size: 0.92rem;
  cursor: pointer;
  margin-top: 0.75rem;
}

/* ==========================================================================
   14. Responsiveness for Mobile (393x852) & Laptop Alignment
   ========================================================================== */
@media (max-width: 600px) {
  .milld-hs {
    padding: 2rem 0 1.5rem;
  }
  .milld-hs .mh-stats {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
  .pg-calc {
    padding: 1.75rem 1.25rem;
  }
  .lab-details-grid {
    grid-template-columns: 1fr 1fr;
  }
}
"""

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(master_css)

print(f"Generated unified style.css (v22.0) ({len(master_css)} bytes)")
