import glob
import re

footer_template = """  <!-- MASTER FOOTER -->
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
              <li><a class="ft-col-link" href="index.html#whey-calculator">Whey Cost Calculator</a></li>
            </ul>
          </div>
          <div class="ft-col">
            <h4 class="ft-col-title">Brand</h4>
            <ul class="ft-col-list">
              <li><a class="ft-col-link" href="about.html">About Mission</a></li>
              <li><a class="ft-col-link" href="faq.html">FAQ &amp; Kneading Guide</a></li>
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
  </footer>"""

for hf in sorted(glob.glob('*.html')):
    if hf in ['elementor-bundle.html', 'every_roti_section.html', 'milld_home.html', 'milld_product.html', 'milld_science_extracted.html', 'index.html']:
        continue
    c = open(hf, encoding='utf-8').read()
    if '<footer' in c:
        c = re.sub(r'<footer[^>]*>.*?</footer>', footer_template, c, flags=re.DOTALL)
        with open(hf, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Standardized luxury footer in {hf}")
