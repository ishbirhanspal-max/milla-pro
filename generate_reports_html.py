import os

print("Generating updated reports.html with Envirocare Labs NABL certificate and data...")

reports_html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, viewport-fit=cover">
  <title>Official NABL Lab Test Reports | MILLA PRO™</title>
  <meta name="description" content="Official laboratory test certificates and quality reports for MILLA PRO™ High-Protein Atta from Envirocare Labs Pvt. Ltd. (NABL Accredited). 44.1g Protein, 13.1g Dietary Fiber.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anton&family=Caveat:wght@400;600;700&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css?v=21.0">
</head>
<body>

  <!-- 1. Top Ultra-Thin Moving Marquee Ticker -->
  <div class="top-ticker-bar">
    <div class="ticker-scroll-track">
      <div class="ticker-scroll-content">
        <span>✨ <strong>PAN-INDIA DELIVERY IN 10–15 DAYS</strong></span>
        <span class="ticker-dot">•</span>
        <span>⚡ <strong>15G PROTEIN PER ROTI</strong></span>
        <span class="ticker-dot">•</span>
        <span>🔬 <strong>NABL CERTIFIED LAB TESTED (44.1G / 100G)</strong></span>
        <span class="ticker-dot">•</span>
        <span>🌿 <strong>100% CLEAN PLANT FRACTIONS</strong></span>
        <span class="ticker-dot">•</span>
        <span>🛡️ <strong>INCL. 5% GST</strong></span>
        <span class="ticker-dot">•</span>
      </div>
      <div class="ticker-scroll-content" aria-hidden="true">
        <span>✨ <strong>PAN-INDIA DELIVERY IN 10–15 DAYS</strong></span>
        <span class="ticker-dot">•</span>
        <span>⚡ <strong>15G PROTEIN PER ROTI</strong></span>
        <span class="ticker-dot">•</span>
        <span>🔬 <strong>NABL CERTIFIED LAB TESTED (44.1G / 100G)</strong></span>
        <span class="ticker-dot">•</span>
        <span>🌿 <strong>100% CLEAN PLANT FRACTIONS</strong></span>
        <span class="ticker-dot">•</span>
        <span>🛡️ <strong>INCL. 5% GST</strong></span>
        <span class="ticker-dot">•</span>
      </div>
    </div>
  </div>

  <!-- 2. Authentic Sticky Master Header -->
  <header class="master-header">
    <div class="container header-inner">
      <a href="index.html" class="brand-logo">
        <span class="logo-main">MILLA <span>PRO</span>™</span>
        <span class="logo-sub">15G PROTEIN ATTA</span>
      </a>

      <nav class="desktop-nav">
        <a href="index.html">Home</a>
        <a href="products.html" class="shop-pill-nav">Shop Products</a>
        <a href="our-science.html">Our Science</a>
        <a href="index.html#whey-calculator">Whey Calculator</a>
        <a href="reports.html" class="active">NABL Reports</a>
        <a href="index.html#faq">FAQ</a>
        <a href="contact.html">Contact</a>
      </nav>

      <div class="header-actions">
        <a href="login.html" class="icon-btn" title="Account" aria-label="Account">
          <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        </a>
        <button type="button" class="icon-btn" onclick="openCartDrawer()" title="View Cart" aria-label="Cart">
          <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/></svg>
          <span class="cart-badge-count" id="cartCountBadge">1</span>
        </button>
        <button type="button" class="mobile-menu-btn" onclick="openMobileSidebar()" title="Menu" aria-label="Open Menu">
          <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </button>
      </div>
    </div>
  </header>

  <!-- Mobile Sidebar & Cart Drawers -->
  <div id="sidebarOverlay" class="sidebar-overlay" onclick="closeMobileSidebar()"></div>
  <aside id="mobileSidebar" class="mobile-sidebar" aria-label="Navigation Menu">
    <div class="sidebar-header">
      <a href="index.html" class="brand-logo" onclick="closeMobileSidebar()">
        <span class="logo-main">MILLA <span>PRO</span>™</span>
        <span class="logo-sub">15G PROTEIN ATTA</span>
      </a>
      <button type="button" class="cart-close-btn" onclick="closeMobileSidebar()" aria-label="Close Menu">✕</button>
    </div>
    <a href="products.html" class="mobile-shop-cta-btn" onclick="closeMobileSidebar()">
      <span>⚡ SHOP NOW — 15G PROTEIN ATTA</span>
      <span style="font-size:1.15rem;">&rarr;</span>
    </a>
    <nav class="mobile-nav-links">
      <a href="index.html" onclick="closeMobileSidebar()"><span>🌾 Home</span><span class="nav-arrow">&rarr;</span></a>
      <a href="products.html" onclick="closeMobileSidebar()"><span>🛒 Shop Packs (1KG &amp; 5KG)</span><span class="nav-arrow">&rarr;</span></a>
      <a href="our-science.html" onclick="closeMobileSidebar()"><span>🔬 Our Science &amp; Fractions</span><span class="nav-arrow">&rarr;</span></a>
      <a href="index.html#whey-calculator" onclick="closeMobileSidebar()"><span>🧮 Whey vs Atta Calculator</span><span class="nav-arrow">&rarr;</span></a>
      <a href="reports.html" onclick="closeMobileSidebar()"><span>📊 NABL Lab Reports</span><span class="nav-arrow">&rarr;</span></a>
      <a href="about.html" onclick="closeMobileSidebar()"><span>🌿 About Mission</span><span class="nav-arrow">&rarr;</span></a>
      <a href="index.html#faq" onclick="closeMobileSidebar()"><span>❓ FAQ</span><span class="nav-arrow">&rarr;</span></a>
      <a href="contact.html" onclick="closeMobileSidebar()"><span>📞 Contact</span><span class="nav-arrow">&rarr;</span></a>
    </nav>
  </aside>

  <div id="cartOverlay" class="cart-overlay" onclick="closeCartDrawer()"></div>
  <aside id="cartDrawer" class="cart-drawer" aria-label="Shopping Cart">
    <div class="cart-drawer-header">
      <div style="display:flex; align-items:center; gap:8px;">
        <span style="font-size:1.2rem;">🛒</span>
        <span class="cart-drawer-title">YOUR CART (<span id="cartDrawerHeaderCount">1</span>)</span>
      </div>
      <button type="button" class="cart-close-btn" onclick="closeCartDrawer()" aria-label="Close Cart">✕</button>
    </div>
    <div class="cart-items-container" id="cartItemsList"></div>
    <div class="cart-drawer-footer" id="cartDrawerFooter">
      <button type="button" class="cart-checkout-btn" onclick="triggerRazorpayCheckout()">
        <span>PROCEED TO CHECKOUT • <span id="checkoutBtnTotal">₹249</span></span>
        <span>&rarr;</span>
      </button>
    </div>
  </aside>

  <!-- Page Banner -->
  <section style="background:#FFFBEF; padding:3.5rem 0 2rem; border-bottom:1px solid rgba(18,18,18,0.08); text-align:center;">
    <div class="container">
      <span style="display:inline-block; background:#FFC107; color:#121212; font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:0.12em; padding:0.35rem 0.9rem; border-radius:9999px; border:1px solid #121212; margin-bottom:1rem;">
        🔬 100% VERIFIED BY THIRD-PARTY NABL LAB
      </span>
      <h1 style="font-family:var(--font-heading); font-size:clamp(2.2rem, 5vw, 3.8rem); text-transform:uppercase; color:#121212; line-height:1.08; margin:0 0 1rem;">
        Official Lab Test Reports
      </h1>
      <p style="font-size:1.1rem; color:rgba(18,18,18,0.75); max-width:680px; margin:0 auto; line-height:1.6;">
        Tested by <strong>Envirocare Labs Private Limited</strong>. Complete nutritional profile, chemical screening, and purity certifications.
      </p>
    </div>
  </section>

  <!-- Certificate Details & Scans -->
  <section style="padding:3.5rem 0;">
    <div class="container">

      <!-- Certificate Header Card -->
      <div style="background:#FFF; border:2px solid #121212; border-radius:18px; padding:2rem; box-shadow:6px 6px 0 #121212; margin-bottom:3rem;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1.5rem; border-bottom:2px dashed rgba(18,18,18,0.15); padding-bottom:1.5rem; margin-bottom:1.5rem;">
          <div>
            <span style="font-size:0.8rem; font-weight:800; color:var(--color-accent); text-transform:uppercase; letter-spacing:0.05em;">Certificate of Analysis</span>
            <h2 style="font-family:var(--font-heading); font-size:1.85rem; text-transform:uppercase; color:#121212; margin:4px 0 6px;">Envirocare Labs Test Report</h2>
            <div style="font-size:0.85rem; color:rgba(18,18,18,0.7); line-height:1.5;">
              <strong>Report No:</strong> 01/ETHFD2609015 &bull; <strong>ULR No:</strong> TC0828426000063499F<br>
              <strong>Date of Issue:</strong> 29 Sep 2026 &bull; <strong>Sample:</strong> High Protein Atta<br>
              <strong>Manufacturer / Client:</strong> A K FOODS, Chembur, Mumbai - 400074
            </div>
          </div>
          <div style="display:flex; flex-direction:column; gap:8px;">
            <a href="lab report.pdf" target="_blank" download class="lab-btn-pdf" style="text-align:center;">
              <span>📄 Download Official PDF (2 Pages)</span>
            </a>
          </div>
        </div>

        <!-- Verified Table -->
        <h3 style="font-family:var(--font-heading); font-size:1.3rem; text-transform:uppercase; margin:0 0 1rem;">NABL Verified Test Parameters</h3>
        <table class="lab-table" style="margin-bottom:2rem;">
          <thead>
            <tr>
              <th>Parameter</th>
              <th>Test Protocol</th>
              <th>Certified Value</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr class="highlight-row">
              <td><strong>Crude Protein (N x 6.25)</strong></td>
              <td>EL/SOP/549</td>
              <td><strong>44.1 g / 100g</strong></td>
              <td><span style="color:#2E7D32; font-weight:800;">✓ PASSED</span></td>
            </tr>
            <tr class="highlight-row">
              <td><strong>Total Dietary Fibre</strong></td>
              <td>AOAC 985.29</td>
              <td><strong>13.1 g / 100g</strong></td>
              <td><span style="color:#2E7D32; font-weight:800;">✓ PASSED</span></td>
            </tr>
            <tr>
              <td>Available Carbohydrates</td>
              <td>IS 1656</td>
              <td>43.1 g / 100g</td>
              <td><span style="color:#2E7D32; font-weight:800;">✓ PASSED</span></td>
            </tr>
            <tr>
              <td>Total Fat</td>
              <td>AOAC 996.06</td>
              <td>1.2 g / 100g</td>
              <td><span style="color:#2E7D32; font-weight:800;">✓ PASSED</span></td>
            </tr>
            <tr>
              <td>Energy Value</td>
              <td>By Calculation</td>
              <td>359.6 kcal / 100g</td>
              <td><span style="color:#2E7D32; font-weight:800;">✓ PASSED</span></td>
            </tr>
            <tr>
              <td>Saturated Fatty Acids</td>
              <td>AOAC 996.06</td>
              <td>0.48 g / 100g</td>
              <td><span style="color:#2E7D32; font-weight:800;">✓ PASSED</span></td>
            </tr>
            <tr>
              <td>Monounsaturated Fatty Acids (MUFA)</td>
              <td>AOAC 996.06</td>
              <td>0.34 g / 100g</td>
              <td><span style="color:#2E7D32; font-weight:800;">✓ PASSED</span></td>
            </tr>
            <tr>
              <td>Polyunsaturated Fatty Acids (PUFA)</td>
              <td>AOAC 996.06</td>
              <td>0.38 g / 100g</td>
              <td><span style="color:#2E7D32; font-weight:800;">✓ PASSED</span></td>
            </tr>
            <tr>
              <td>Trans Fatty Acids</td>
              <td>AOAC 996.06</td>
              <td>BLQ (Below Limit of Quantification)</td>
              <td><span style="color:#2E7D32; font-weight:800;">✓ ZERO TRANS FAT</span></td>
            </tr>
            <tr>
              <td>Cholesterol</td>
              <td>EL/SOP/520</td>
              <td>BLQ (0 mg)</td>
              <td><span style="color:#2E7D32; font-weight:800;">✓ ZERO CHOLESTEROL</span></td>
            </tr>
            <tr>
              <td>Sodium</td>
              <td>ICP-OES</td>
              <td>15.07 mg / 100g</td>
              <td><span style="color:#2E7D32; font-weight:800;">✓ LOW SODIUM</span></td>
            </tr>
            <tr>
              <td>Added Sugars</td>
              <td>FSSAI Manual</td>
              <td>4.4 g / 100g</td>
              <td><span style="color:#2E7D32; font-weight:800;">✓ PASSED</span></td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Scanned Certificate Pages -->
      <h3 style="font-family:var(--font-heading); font-size:1.75rem; text-transform:uppercase; text-align:center; margin-bottom:2rem;">Original NABL Certificate Scans</h3>
      
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:2rem; margin-bottom:3rem;">
        
        <div style="background:#FFF; border:2px solid #121212; border-radius:16px; padding:1.25rem; box-shadow:6px 6px 0 #121212;">
          <div style="font-weight:800; font-size:0.9rem; text-transform:uppercase; margin-bottom:0.75rem; display:flex; justify-content:space-between;">
            <span>Page 1 of 2</span>
            <span style="color:#2E7D32;">✓ NABL Stamp</span>
          </div>
          <a href="envirocare-lab-report-p1.png" target="_blank" title="Click to view full size">
            <img src="envirocare-lab-report-p1.png" alt="Envirocare Labs NABL Report Page 1" style="width:100%; border:1px solid #E2E8F0; border-radius:8px;">
          </a>
        </div>

        <div style="background:#FFF; border:2px solid #121212; border-radius:16px; padding:1.25rem; box-shadow:6px 6px 0 #121212;">
          <div style="font-weight:800; font-size:0.9rem; text-transform:uppercase; margin-bottom:0.75rem; display:flex; justify-content:space-between;">
            <span>Page 2 of 2</span>
            <span style="color:#2E7D32;">✓ Signatures &amp; Methods</span>
          </div>
          <a href="envirocare-lab-report-p2.png" target="_blank" title="Click to view full size">
            <img src="envirocare-lab-report-p2.png" alt="Envirocare Labs NABL Report Page 2" style="width:100%; border:1px solid #E2E8F0; border-radius:8px;">
          </a>
        </div>

      </div>

      <div style="text-align:center;">
        <a href="products.html" class="mh-btn-shop" style="display:inline-flex; align-items:center; gap:0.75rem; border-radius:9999px; background:#121212; padding:0.85rem 2rem; color:#FFF; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; box-shadow:0 6px 0 #FFC107;">
          <span>Shop Certified Atta Packs &rarr;</span>
        </a>
      </div>

    </div>
  </section>

  <!-- Footer -->
  <footer class="ft-footer">
    <div class="ft-container">
      <div class="ft-grid">
        <div class="ft-brand">
          <div class="logo-main" style="margin-bottom:0.5rem;">MILLA <span>PRO</span>™</div>
          <p class="ft-brand-text">
            India's trusted 100% natural high-protein chakki atta delivering 15g protein in every single roti without synthetic whey or chemical preservatives.
          </p>
          <div style="font-size:0.75rem; color:rgba(18,18,18,0.7); margin:1rem 0;">
            A K FOODS, Chembur, Mumbai - 400074 &bull; FSSAI Lic. 21526007002971
          </div>
        </div>
        <div class="ft-nav-grid">
          <div class="ft-col">
            <h4 class="ft-col-title">Shop</h4>
            <ul class="ft-col-list">
              <li><a class="ft-col-link" href="products.html">1 KG Trial Pouch (₹249)</a></li>
              <li><a class="ft-col-link" href="products.html">5 KG Saver Pack (₹1,199)</a></li>
            </ul>
          </div>
          <div class="ft-col">
            <h4 class="ft-col-title">Learn</h4>
            <ul class="ft-col-list">
              <li><a class="ft-col-link" href="our-science.html">Our Science</a></li>
              <li><a class="ft-col-link" href="reports.html">NABL Reports</a></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </footer>

  <script src="script.js?v=21.0"></script>
</body>
</html>
'''

with open('reports.html', 'w', encoding='utf-8') as f:
    f.write(reports_html)

print("Generated reports.html successfully!")
