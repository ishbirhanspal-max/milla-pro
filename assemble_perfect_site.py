import os
import re

print("Building complete perfect site...")

# 1. Read base master CSS from build_master_css.py
from build_master_css import master_css

# 2. Read milld_components.css and footer_styles.css
with open('milld_components.css', 'r', encoding='utf-8') as f:
    milld_components_css = f.read()

with open('footer_styles.css', 'r', encoding='utf-8') as f:
    footer_css = f.read()

# Combine stylesheets
combined_css = master_css + "\n\n/* === MILLD COMPONENTS === */\n\n" + milld_components_css + "\n\n/* === FOOTER STYLES === */\n\n" + footer_css

# Write style.css
with open('style.css', 'w', encoding='utf-8') as f:
    f.write(combined_css)

print(f"Generated unified style.css: {len(combined_css)} bytes")

# 3. Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

# A. REMOVE HERO ROTI IMAGE (Hot, soft, high-protein roti broken open...)
# Looking for hero-visual-frame-wrap block
roti_hero_pattern = r'<!-- REAL FOOD HERO VISUAL.*?</div>\s*</div>\s*</div>'
if 'hero-visual-frame-wrap' in index_html:
    # Match the whole hero-visual-frame-wrap div
    start_tag = index_html.find('<div class="hero-visual-frame-wrap"')
    if start_tag != -1:
        # Find the matching closing div for hero-visual-frame-wrap
        # It contains hero-food-visual
        end_str = '<!-- Tilted Marquee Strip Under Roti -->'
        end_idx = index_html.find(end_str)
        if end_idx != -1:
            index_html = index_html[:start_tag] + index_html[end_idx:]
            print("Successfully removed hero roti image block!")
        else:
            print("Warning: Could not find end marker for hero roti image")
    else:
        print("hero-visual-frame-wrap not found by string")
else:
    print("hero-visual-frame-wrap not in index_html")

# B. REPLACE LAB REPORT SECTION
# Replace raw image and table with clean parameter cards and official certificate links
old_lab_section_start = index_html.find('<section class="lab-showcase-section" id="reports">')
old_lab_section_end = index_html.find('<!-- 8. COST COMPARISON TABLE SECTION (ss-section) -->')

new_lab_section = """    <!-- 7. INDEPENDENTLY CERTIFIED NABL NUTRITION (lab-showcase-section) -->
    <!-- Lab reports hidden behind official links; only verified nutrition details on site -->
    <section class="lab-showcase-section" id="reports">
      <div class="container lab-showcase-container">
        
        <div class="lab-showcase-header">
          <div class="lab-badge-pill">
            <span>🔬 OFFICIAL NABL ACCREDITED LABORATORY DATA</span>
          </div>
          <h2 class="lab-showcase-title">
            Independently Certified <span class="accent">Nutrition.</span>
          </h2>
          <p class="lab-showcase-sub">
            Every batch of MILLA PRO is tested by <strong>Envirocare Labs Private Limited</strong> (NABL Accredited Laboratory). Report No: <strong>01/ETHFD2609015</strong> &bull; ULR: <strong>TC0828426000063499F</strong>. 100% honest transparency.
          </p>
        </div>

        <!-- 8 Verified Parameter Detail Cards -->
        <div class="lab-details-grid">
          <div class="lab-detail-card highlight">
            <div class="lab-param-val">44.1g</div>
            <div class="lab-param-name">Crude Protein (N×6.25)</div>
            <div class="lab-param-method">EL/SOP/549 &bull; Per 100g</div>
          </div>

          <div class="lab-detail-card highlight">
            <div class="lab-param-val">13.1g</div>
            <div class="lab-param-name">Total Dietary Fibre</div>
            <div class="lab-param-method">AOAC 985.29 &bull; Prebiotic</div>
          </div>

          <div class="lab-detail-card">
            <div class="lab-param-val">43.1g</div>
            <div class="lab-param-name">Available Carbs</div>
            <div class="lab-param-method">IS 1656 &bull; Per 100g</div>
          </div>

          <div class="lab-detail-card">
            <div class="lab-param-val">359.6</div>
            <div class="lab-param-name">Calories / Energy</div>
            <div class="lab-param-method">Calculation &bull; kcal/100g</div>
          </div>

          <div class="lab-detail-card">
            <div class="lab-param-val">1.2g</div>
            <div class="lab-param-name">Total Healthy Fat</div>
            <div class="lab-param-method">AOAC 996.06 &bull; Low Fat</div>
          </div>

          <div class="lab-detail-card">
            <div class="lab-param-val">0g</div>
            <div class="lab-param-name">Trans Fat</div>
            <div class="lab-param-method">AOAC 996.06 &bull; BLQ Zero</div>
          </div>

          <div class="lab-detail-card">
            <div class="lab-param-val">0mg</div>
            <div class="lab-param-name">Cholesterol</div>
            <div class="lab-param-method">EL/SOP/520 &bull; 100% Plant</div>
          </div>

          <div class="lab-detail-card">
            <div class="lab-param-val">15.1mg</div>
            <div class="lab-param-name">Natural Sodium</div>
            <div class="lab-param-method">ICP-OES &bull; Per 100g</div>
          </div>
        </div>

        <!-- Official Certificate Links & Download Banner -->
        <div class="lab-credentials-banner">
          <div class="lab-cred-text">
            <h3>NABL Government Certified Batch</h3>
            <p>
              Sample: <strong>High Protein Atta</strong> &bull; Client: <strong>A K FOODS, Chembur, Mumbai</strong><br>
              Full chemical, nutritional, and microbial compliance certificates available for inspection.
            </p>
          </div>
          <div class="lab-actions-row">
            <a href="reports.html" class="lab-btn-link" title="View Full NABL Certificate">
              <span>📄 View Official NABL Certificate (Scans & PDF)</span>
              <span>&rarr;</span>
            </a>
            <a href="lab report.pdf" class="lab-btn-pdf" target="_blank" download title="Download NABL Lab Report PDF">
              <span>⬇️ Download Lab Report (PDF)</span>
            </a>
          </div>
        </div>

      </div>
    </section>

"""

if old_lab_section_start != -1 and old_lab_section_end != -1:
    index_html = index_html[:old_lab_section_start] + new_lab_section + index_html[old_lab_section_end:]
    print("Successfully replaced lab report section with clean detail cards!")
else:
    print(f"Warning: Could not replace lab section. Start: {old_lab_section_start}, End: {old_lab_section_end}")

# C. UPDATE FOOTER IN INDEX.HTML
# Ensure footer has rich contrast, no black-on-black, and links are styled
old_footer_start = index_html.find('<!-- 11. MASTER FOOTER (ft-footer) -->')
old_footer_end = index_html.find('<!-- 12. SIMULATED RAZORPAY 2-STEP CHECKOUT MODAL -->')

new_footer = """  <!-- 11. MASTER FOOTER (ft-footer) -->
  <footer class="ft-footer">
    <div class="ft-container">
      <div class="ft-grid">
        
        <!-- Left: Brand + Info -->
        <div class="ft-brand">
          <div class="ft-logo">MILLA <span>PRO</span>™</div>
          <p class="ft-brand-text">
            India's trusted 100% natural high-protein chakki atta delivering 15g pure plant protein in every single roti without synthetic whey or chemical preservatives.
          </p>
          <div class="ft-fssai-box">
            <strong>MFG &amp; PACKED BY:</strong> A K FOODS<br>
            Gala No. 210, Daulat Udyog Bhavan, Wadhavali, CG Road, Chembur, Mumbai - 400074<br>
            <strong>FSSAI Lic. No:</strong> 21526007002971 &bull; GST 5% Included
          </div>
          <p class="ft-cta-note">
            ★ Loved by 30,000+ Indian families &amp; counting
          </p>
        </div>

        <!-- Right: Nav Columns -->
        <div class="ft-nav-grid">
          <div class="ft-col">
            <h4 class="ft-col-title">Shop</h4>
            <ul class="ft-col-list">
              <li><a class="ft-col-link" href="products.html">1 KG Trial Pouch (₹249)</a></li>
              <li><a class="ft-col-link" href="products.html">5 KG Saver Pack (₹1,199)</a></li>
              <li><a class="ft-col-link" href="products.html">Order Online</a></li>
            </ul>
          </div>
          <div class="ft-col">
            <h4 class="ft-col-title">Learn</h4>
            <ul class="ft-col-list">
              <li><a class="ft-col-link" href="our-science.html">Our Science &amp; Fractions</a></li>
              <li><a class="ft-col-link" href="reports.html">Official NABL Reports</a></li>
              <li><a class="ft-col-link" href="#whey-calculator">Whey Cost Calculator</a></li>
            </ul>
          </div>
          <div class="ft-col">
            <h4 class="ft-col-title">Brand</h4>
            <ul class="ft-col-list">
              <li><a class="ft-col-link" href="about.html">About Mission</a></li>
              <li><a class="ft-col-link" href="#faq">FAQ &amp; Kneading Guide</a></li>
              <li><a class="ft-col-link" href="contact.html">Contact Us</a></li>
            </ul>
          </div>
          <div class="ft-col">
            <h4 class="ft-col-title">Help &amp; Legal</h4>
            <ul class="ft-col-list">
              <li><a class="ft-col-link" href="shipping-policy.html">Shipping (10–15 Days)</a></li>
              <li><a class="ft-col-link" href="refund-policy.html">Refund Policy</a></li>
              <li><a class="ft-col-link" href="privacy-policy.html">Privacy Policy</a></li>
              <li><a class="ft-col-link" href="terms.html">Terms of Service</a></li>
            </ul>
          </div>
        </div>

      </div>

      <div class="ft-bottom">
        <div>&copy; 2026 MILLA PRO™ (A K FOODS). All rights reserved. Taxed @ 5% GST Included.</div>
        <div>Chembur, Mumbai, Maharashtra 400074 &bull; Pan-India Express Delivery</div>
      </div>
    </div>
  </footer>

"""

if old_footer_start != -1 and old_footer_end != -1:
    index_html = index_html[:old_footer_start] + new_footer + index_html[old_footer_end:]
    print("Successfully updated footer in index.html!")
else:
    print(f"Warning: Could not replace footer. Start: {old_footer_start}, End: {old_footer_end}")

# Write updated index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print("Updated index.html successfully!")
