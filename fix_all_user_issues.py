import os
import re

print("Applying comprehensive fixes for the 4 issues...")

# ==============================================================================
# 1. FIX INDEX.HTML
# ==============================================================================
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# A. Add 'is-shown' to all bc-card-outer elements so they are never empty/invisible
html = html.replace('class="bc-card-outer"', 'class="bc-card-outer is-shown"')

# B. Move the yellow tilted marquee OUT of mh-copy and make it full screen edge-to-edge
# Find the hero section structure
# In index.html, the marquee is currently inside mh-copy
marquee_pattern = re.compile(r'<!-- Tilted Marquee Strip Under Roti -->\s*<div style="margin-left:-1\.5rem;.*?</div>\s*</div>\s*</div>', re.DOTALL)

# Let's extract the clean full-width marquee
full_screen_marquee = """    <!-- FULL-SCREEN EDGE-TO-EDGE TILTED MARQUEE STRIP -->
    <div class="hero-full-marquee-wrap">
      <div class="hero-full-marquee-inner">
        <div class="ms-track">
          <span class="ms-text">Loved by 30,000+ families</span>
          <span class="ms-icon"><svg viewBox="0 0 28 28" class="milld-marquee-icon"><path d="M14 2.2c5.8.2 11.6 4.4 11.8 11.6.2 6.4-5.4 12-12 12-6.4 0-12-5.4-11.8-12C2.2 7.4 7.6 2 14 2.2z" fill="#d4942a"></path></svg></span>
          <span class="ms-text">100% Plant Based</span>
          <span class="ms-icon"><svg viewBox="0 0 28 28" class="milld-marquee-icon"><path d="M14 2.2c5.8.2 11.6 4.4 11.8 11.6.2 6.4-5.4 12-12 12-6.4 0-12-5.4-11.8-12C2.2 7.4 7.6 2 14 2.2z" fill="#d4942a"></path></svg></span>
          <span class="ms-text">ZERO Preservatives</span>
          <span class="ms-icon"><svg viewBox="0 0 28 28" class="milld-marquee-icon"><path d="M14 2.2c5.8.2 11.6 4.4 11.8 11.6.2 6.4-5.4 12-12 12-6.4 0-12-5.4-11.8-12C2.2 7.4 7.6 2 14 2.2z" fill="#d4942a"></path></svg></span>
          <span class="ms-text">NABL LAB Tested (44.1g Protein)</span>
          <span class="ms-icon"><svg viewBox="0 0 28 28" class="milld-marquee-icon"><path d="M14 2.2c5.8.2 11.6 4.4 11.8 11.6.2 6.4-5.4 12-12 12-6.4 0-12-5.4-11.8-12C2.2 7.4 7.6 2 14 2.2z" fill="#d4942a"></path></svg></span>
          <span class="ms-text">Low GI 42 (Diabetic Friendly)</span>
          <span class="ms-icon"><svg viewBox="0 0 28 28" class="milld-marquee-icon"><path d="M14 2.2c5.8.2 11.6 4.4 11.8 11.6.2 6.4-5.4 12-12 12-6.4 0-12-5.4-11.8-12C2.2 7.4 7.6 2 14 2.2z" fill="#d4942a"></path></svg></span>
          <span class="ms-text">0% Whey Bloat</span>
          <span class="ms-icon"><svg viewBox="0 0 28 28" class="milld-marquee-icon"><path d="M14 2.2c5.8.2 11.6 4.4 11.8 11.6.2 6.4-5.4 12-12 12-6.4 0-12-5.4-11.8-12C2.2 7.4 7.6 2 14 2.2z" fill="#d4942a"></path></svg></span>
        </div>
      </div>
    </div>"""

# Remove old trapped marquee from inside mh-copy if present
old_marquee_marker = '<!-- Tilted Marquee Strip Under Roti -->'
if old_marquee_marker in html:
    start_m = html.find(old_marquee_marker)
    end_m = html.find('<!-- CTA Buttons -->')
    if start_m != -1 and end_m != -1:
        html = html[:start_m] + html[end_m:]
        print("Removed trapped marquee from inside hero copy column!")

# Now place the full-screen marquee right between the Hero copy/CTAs and section 4
hero_end_marker = '</section>'
first_hero_end = html.find(hero_end_marker)
# Find the exact hero section closing tag
sec4_start = html.find('<!-- 4. PROTEIN GAP & CALCULATOR SECTION')
if sec4_start != -1:
    # Insert marquee right before section 4
    html = html[:sec4_start] + full_screen_marquee + "\n\n    " + html[sec4_start:]
    print("Placed full-screen edge-to-edge marquee strip!")

# C. Clean hero layout in index.html to ensure centered presentation
html = html.replace('class="mh-grid" style="display:block; max-width:80rem; margin:0 auto; padding:0 1.5rem; gap:2.5rem;"',
                    'class="mh-grid"')
html = html.replace('class="mh-copy" style="position:relative; z-index:10; padding-top:1rem; padding-bottom:1rem; text-align:center; width:100%;"',
                    'class="mh-copy"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html successfully!")


# ==============================================================================
# 2. UPDATE SCRIPT.JS - UNIFY CART DRAWER & INITIALIZE PROPERLY
# ==============================================================================
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace all openCartDrawer and closeCartDrawer implementations with guaranteed robust functions
cart_functions = """
// ==========================================
// GUARANTEED WORKING CART & SIDEBAR HANDLERS
// ==========================================
function openCartDrawer() {
  const overlay = document.getElementById('cartOverlay');
  const drawer = document.getElementById('cartDrawer');
  if (overlay) {
    overlay.style.display = 'block';
    overlay.classList.add('active');
    overlay.classList.add('open');
  }
  if (drawer) {
    drawer.classList.add('active');
    drawer.classList.add('open');
  }
  document.body.style.overflow = 'hidden';
  if (typeof updateCartDrawerUI === 'function') {
    updateCartDrawerUI();
  }
}

function closeCartDrawer() {
  const overlay = document.getElementById('cartOverlay');
  const drawer = document.getElementById('cartDrawer');
  if (overlay) {
    overlay.classList.remove('active');
    overlay.classList.remove('open');
    setTimeout(() => { overlay.style.display = 'none'; }, 200);
  }
  if (drawer) {
    drawer.classList.remove('active');
    drawer.classList.remove('open');
  }
  document.body.style.overflow = '';
}

function openMobileSidebar() {
  const overlay = document.getElementById('sidebarOverlay');
  const sidebar = document.getElementById('mobileSidebar');
  if (overlay) {
    overlay.style.display = 'block';
    overlay.classList.add('active');
    overlay.classList.add('open');
  }
  if (sidebar) {
    sidebar.classList.add('active');
    sidebar.classList.add('open');
  }
  document.body.style.overflow = 'hidden';
}

function closeMobileSidebar() {
  const overlay = document.getElementById('sidebarOverlay');
  const sidebar = document.getElementById('mobileSidebar');
  if (overlay) {
    overlay.classList.remove('active');
    overlay.classList.remove('open');
    setTimeout(() => { overlay.style.display = 'none'; }, 200);
  }
  if (sidebar) {
    sidebar.classList.remove('active');
    sidebar.classList.remove('open');
  }
  document.body.style.overflow = '';
}
"""

# Append guaranteed functions at the end of script.js so they override any previous ones
js = js + "\n\n" + cart_functions

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated script.js successfully!")


# ==============================================================================
# 3. UPDATE STYLE.CSS - MASTER OVERRIDES AT THE VERY BOTTOM (WINS SPECIFICITY)
# ==============================================================================
master_overrides = """
/* ==========================================================================
   MASTER SPECIFICITY OVERRIDES (FIXING 1920px LAPTOP & CARTS)
   ========================================================================== */

/* 1. Ensure MILLA PRO Difference Cards are NEVER empty or hidden */
.bc-card-outer {
  opacity: 1 !important;
  transform: none !important;
  visibility: visible !important;
}

.bc-section {
  padding: 5rem 0 !important;
  background: #FAF7F2 !important;
}

.bc-container {
  max-width: 1200px !important;
  margin: 0 auto !important;
  padding: 0 2rem !important;
  width: 100% !important;
}

.bc-heading-wrap {
  text-align: center !important;
  margin-bottom: 3.5rem !important;
}

.bc-heading {
  font-family: 'Anton', 'Bebas Neue', system-ui, sans-serif !important;
  font-size: clamp(2.4rem, 5vw, 4rem) !important;
  text-transform: uppercase !important;
  color: #121212 !important;
  text-align: center !important;
}

.bc-heading-accent {
  color: #D4942A !important;
}

.bc-grid {
  display: grid !important;
  grid-template-columns: repeat(4, 1fr) !important;
  gap: 1.5rem !important;
  width: 100% !important;
  overflow: visible !important;
}

@media (max-width: 1023px) {
  .bc-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 1.5rem !important;
  }
}

@media (max-width: 640px) {
  .bc-grid {
    grid-template-columns: 1fr !important;
    gap: 1.5rem !important;
  }
}

.bc-card-btn {
  display: block !important;
  width: 100% !important;
  min-height: 420px !important;
  aspect-ratio: 5 / 7 !important;
  cursor: pointer !important;
  border-radius: 1.5rem !important;
  border: none !important;
  background: transparent !important;
  padding: 0 !important;
  text-align: left !important;
  perspective: 1600px !important;
}

.bc-face {
  position: absolute !important;
  inset: 0 !important;
  border-radius: 1.5rem !important;
  overflow: hidden !important;
  backface-visibility: hidden !important;
  -webkit-backface-visibility: hidden !important;
  border: 2px solid #121212 !important;
  box-shadow: 5px 5px 0 #121212 !important;
}

/* 2. Hero Section Centering on Laptop (1920x957 & 1280x800) */
@media (min-width: 1024px) {
  .milld-hs .mh-grid {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    max-width: 1200px !important;
    margin: 0 auto !important;
    padding: 0 2rem !important;
    width: 100% !important;
    grid-template-columns: none !important;
  }

  .milld-hs .mh-copy {
    grid-column: auto !important;
    width: 100% !important;
    max-width: 1000px !important;
    margin: 0 auto !important;
    text-align: center !important;
    padding: 1.5rem 0 !important;
  }

  .milld-hs .mh-h1 {
    font-size: clamp(3rem, 5.5vw, 5.4rem) !important;
    text-align: center !important;
    margin: 0 auto 1.25rem !important;
    line-height: 1.05 !important;
  }

  .milld-hs .mh-sub {
    margin: 1.5rem auto 2.5rem !important;
    max-width: 50rem !important;
    text-align: center !important;
    font-size: 1.35rem !important;
  }

  .milld-hs .mh-ctas {
    justify-content: center !important;
    margin: 2.5rem auto 1.5rem !important;
  }

  .milld-hs .mh-stats {
    display: grid !important;
    grid-template-columns: repeat(3, 1fr) !important;
    gap: 1.5rem !important;
    max-width: 38rem !important;
    margin: 2.5rem auto 1rem !important;
    text-align: center !important;
  }
}

/* 3. FULL-SCREEN EDGE-TO-EDGE TILTED MARQUEE STRIP */
.hero-full-marquee-wrap {
  width: 100vw !important;
  position: relative !important;
  left: 50% !important;
  right: 50% !important;
  margin-left: -50vw !important;
  margin-right: -50vw !important;
  overflow: hidden !important;
  padding: 1.5rem 0 !important;
  z-index: 25 !important;
}

.hero-full-marquee-inner {
  width: 110% !important;
  margin-left: -5% !important;
  transform: rotate(-1.85deg) !important;
  transform-origin: center !important;
  overflow: hidden !important;
  border-top: 2px solid #121212 !important;
  border-bottom: 2px solid #121212 !important;
  background: #FFC107 !important;
  box-shadow: 0 10px 30px -4px rgba(18, 18, 18, 0.2) !important;
  padding: 0.25rem 0 !important;
}

.hero-full-marquee-inner .ms-track {
  display: flex !important;
  align-items: center !important;
  white-space: nowrap !important;
  animation: milldMarquee 20s linear infinite !important;
}

.hero-full-marquee-inner .ms-text {
  font-family: 'Anton', 'Bebas Neue', system-ui, sans-serif !important;
  font-size: 1.35rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.06em !important;
  color: #121212 !important;
  margin: 0 2rem !important;
}

.hero-full-marquee-inner .ms-icon {
  width: 1.4rem !important;
  height: 1.4rem !important;
  display: inline-flex !important;
  align-items: center !important;
}

/* 4. GUARANTEED CART DRAWER & OVERLAY SLIDE-OUT */
.cart-overlay.active, .cart-overlay.open,
.sidebar-overlay.active, .sidebar-overlay.open {
  opacity: 1 !important;
  pointer-events: auto !important;
  display: block !important;
}

.cart-drawer.active, .cart-drawer.open {
  transform: translateX(0) !important;
  display: flex !important;
}

.mobile-sidebar.active, .mobile-sidebar.open {
  transform: translateX(0) !important;
  display: flex !important;
}

/* Cart Item Card Styling */
.cart-empty-state {
  text-align: center;
  padding: 3rem 1.5rem;
}

.cart-item-card {
  display: flex;
  gap: 12px;
  background: #FFF;
  border: 1.5px solid rgba(18, 18, 18, 0.15);
  border-radius: 12px;
  padding: 12px;
  align-items: center;
  margin-bottom: 10px;
}

.cic-thumb-wrap {
  width: 64px;
  height: 64px;
  border-radius: 8px;
  background: #FAF7F2;
  overflow: hidden;
  flex-shrink: 0;
  border: 1px solid rgba(18, 18, 18, 0.08);
}

.cic-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cic-content {
  flex: 1;
  min-width: 0;
}

.cic-top-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 4px;
}

.cic-name {
  font-size: 0.92rem;
  font-weight: 800;
  color: #121212;
}

.cic-remove-btn {
  background: none;
  border: none;
  color: rgba(18, 18, 18, 0.4);
  font-size: 0.9rem;
  cursor: pointer;
  padding: 2px 6px;
}

.cic-remove-btn:hover {
  color: #C62828;
}

.cic-badge-row {
  display: flex;
  gap: 6px;
  margin-bottom: 6px;
}

.cic-macro-badge {
  background: #FFF9E6;
  color: #D4942A;
  font-size: 10px;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: 4px;
}

.cic-veg-badge {
  background: #E8F5E9;
  color: #2E7D32;
  font-size: 10px;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: 4px;
}

.cic-calc-line {
  font-size: 0.82rem;
  margin-bottom: 6px;
  color: rgba(18, 18, 18, 0.75);
}

.cic-item-total {
  font-family: 'Anton', 'Bebas Neue', sans-serif;
  font-size: 1.1rem;
  color: #121212;
}

.cic-mrp strike {
  color: rgba(18, 18, 18, 0.4);
  font-size: 0.8rem;
  margin-left: 4px;
}

.cic-stepper-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.cart-qty-stepper {
  display: flex;
  align-items: center;
  background: #FAF7F2;
  border: 1px solid rgba(18, 18, 18, 0.15);
  border-radius: 9999px;
  padding: 2px 4px;
}

.cqs-btn {
  background: none;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
  font-weight: 800;
  font-size: 0.95rem;
}

.cqs-val {
  padding: 0 8px;
  font-size: 0.85rem;
  font-weight: 800;
}

/* Global 1920px container centering polish */
.container, .pg-container, .rr-container, .bc-container, .lab-showcase-container, .ss-container, .tm-container, .faq-container, .ft-container {
  max-width: 1200px !important;
  margin-left: auto !important;
  margin-right: auto !important;
  width: 100% !important;
}
"""

with open('style.css', 'a', encoding='utf-8') as f:
    f.write(master_overrides)

print("Appended master overrides to style.css successfully!")
