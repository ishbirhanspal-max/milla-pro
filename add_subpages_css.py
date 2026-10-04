import glob, re

print("Adding subpages and modal CSS to style.css...")

subpages_css = """
/* ==========================================================================
   SUBPAGES & MODAL FORM STYLING
   (about, contact, faq, login, our-science, privacy, refund, shipping, terms)
   ========================================================================== */

.page-hero-banner {
  background: #FFFBEF;
  padding: 3.5rem 0 2rem;
  border-bottom: 1px solid rgba(18, 18, 18, 0.08);
  text-align: center;
}

.page-kicker {
  display: inline-block;
  background: #FFC107;
  color: #121212;
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  padding: 0.35rem 0.9rem;
  border-radius: 9999px;
  border: 1px solid #121212;
  margin-bottom: 0.75rem;
}

.page-title {
  font-family: 'Anton', 'Bebas Neue', system-ui, sans-serif;
  font-size: clamp(2.2rem, 5vw, 3.6rem);
  text-transform: uppercase;
  color: #121212;
  line-height: 1.1;
  margin-bottom: 0.75rem;
}

.page-desc {
  font-size: 1.05rem;
  color: rgba(18, 18, 18, 0.75);
  max-width: 680px;
  margin: 0 auto;
  line-height: 1.6;
}

.legal-page-section {
  padding: 3.5rem 0 5rem;
  background: #FAF7F2;
}

.contact-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2.5rem;
  max-width: 1040px;
  margin: 0 auto;
}

@media (min-width: 860px) {
  .contact-grid {
    grid-template-columns: 1.1fr 0.9fr;
    align-items: start;
  }
}

.contact-info-cards {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.contact-card-item {
  background: #FFF;
  border: 2px solid #121212;
  border-radius: 14px;
  padding: 1.5rem;
  display: flex;
  gap: 1.25rem;
  align-items: flex-start;
  box-shadow: 4px 4px 0 #121212;
}

.contact-icon {
  font-size: 1.6rem;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #FAF7F2;
  border: 1.5px solid #121212;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.contact-form-card {
  background: #FFF;
  border: 2px solid #121212;
  border-radius: 14px;
  padding: 2rem;
  box-shadow: 4px 4px 0 #121212;
}

.contact-highlight-box {
  background: #FFFDF5;
  border: 1.5px solid #D4942A;
  border-radius: 10px;
  padding: 1.25rem;
  margin-top: 1.5rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  font-size: 0.82rem;
  font-weight: 700;
  color: #121212;
  margin-bottom: 0.35rem;
}

.form-control {
  width: 100%;
  padding: 0.85rem 1rem;
  border: 1.5px solid rgba(18, 18, 18, 0.2);
  border-radius: 8px;
  font-family: inherit;
  font-size: 0.95rem;
  box-sizing: border-box;
}

.form-control:focus {
  outline: none;
  border-color: #D4942A;
}

.amino-matrix-wrap {
  overflow-x: auto;
  background: #FFF;
  border: 2px solid #121212;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 5px 5px 0 #121212;
  margin-top: 2rem;
}

.amino-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 500px;
}

.amino-table th, .amino-table td {
  padding: 0.85rem 1rem;
  text-align: left;
  border-bottom: 1px solid rgba(18, 18, 18, 0.1);
  font-size: 0.9rem;
}

.amino-table th {
  background: #FAF7F2;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 0.78rem;
}

.auth-container {
  max-width: 480px;
  margin: 3rem auto 5rem;
  padding: 0 1.5rem;
}

.auth-card {
  background: #FFF;
  border: 2px solid #121212;
  border-radius: 18px;
  padding: 2.25rem 2rem;
  box-shadow: 6px 6px 0 #121212;
}

.auth-header-area {
  text-align: center;
  margin-bottom: 1.5rem;
}

.auth-title {
  font-size: 2rem;
  text-transform: uppercase;
  margin-bottom: 0.35rem;
}

.auth-desc {
  font-size: 0.88rem;
  color: rgba(18, 18, 18, 0.7);
}

.auth-subtabs-row {
  display: flex;
  gap: 0.5rem;
  background: #FAF7F2;
  border-radius: 8px;
  padding: 4px;
  margin-bottom: 1.5rem;
}

.auth-subtab-btn {
  flex: 1;
  padding: 0.65rem;
  border: none;
  background: none;
  font-weight: 700;
  font-size: 0.85rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.auth-subtab-btn.active {
  background: #121212;
  color: #FFFBEF;
}

.auth-divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: 1.5rem 0;
  color: rgba(18, 18, 18, 0.4);
  font-size: 0.75rem;
  font-weight: 700;
}

.auth-divider::before, .auth-divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid rgba(18, 18, 18, 0.15);
}

.auth-divider:not(:empty)::before {
  margin-right: .75em;
}

.auth-divider:not(:empty)::after {
  margin-left: .75em;
}

.auth-method-panel {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.lab-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.lab-table th, .lab-table td {
  padding: 0.9rem 1rem;
  text-align: left;
  border-bottom: 1px solid rgba(18, 18, 18, 0.1);
  font-size: 0.9rem;
}

.lab-table th {
  background: #FAF7F2;
  font-weight: 800;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.lab-table .highlight-row td, .highlight-row td {
  background: rgba(255, 193, 7, 0.15);
  font-weight: 700;
}

.checkout-step-container {
  max-width: 540px;
  margin: 0 auto;
}

.checkout-address-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.co-label {
  font-size: 0.82rem;
  font-weight: 700;
  color: #121212;
  margin-bottom: 0.3rem;
  display: block;
}

.co-input {
  width: 100%;
  padding: 0.8rem;
  border: 1.5px solid rgba(18, 18, 18, 0.2);
  border-radius: 8px;
  font-family: inherit;
  font-size: 0.92rem;
  box-sizing: border-box;
}

.co-input:focus {
  outline: none;
  border-color: #D4942A;
}

.co-delivery-notice {
  background: #FFF9E6;
  border: 1px dashed #D4942A;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.8rem;
  color: #121212;
}

.co-continue-btn {
  width: 100%;
  background: #121212;
  color: #FFFBEF;
  border: none;
  padding: 0.95rem;
  border-radius: 9999px;
  font-weight: 800;
  font-size: 0.92rem;
  cursor: pointer;
  box-shadow: 0 4px 0 0 #FFC107;
  transition: transform 0.15s ease;
}

.co-continue-btn:hover {
  transform: translateY(-2px);
}

.checkout-back-link {
  font-size: 0.85rem;
  font-weight: 700;
  color: #D4942A;
  text-decoration: underline;
  cursor: pointer;
  display: inline-block;
  margin-top: 0.5rem;
}

.delivery-recap-card {
  background: #FFF;
  border: 1.5px solid #121212;
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.drc-details {
  font-size: 0.85rem;
  line-height: 1.5;
}

.drc-edit-btn {
  font-size: 0.78rem;
  font-weight: 700;
  color: #D4942A;
  cursor: pointer;
  float: right;
}

.checkout-success-view {
  text-align: center;
  padding: 2rem 1rem;
}

.order-success-card {
  background: #FFF;
  border: 2px solid #121212;
  border-radius: 16px;
  padding: 2.5rem;
  text-align: center;
  box-shadow: 6px 6px 0 #121212;
}

.form-group-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.footer-compliance-box {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 0.85rem 1rem;
  border-radius: 8px;
  margin-top: 1rem;
  font-size: 0.75rem;
  line-height: 1.6;
}
"""

with open('style.css', 'a', encoding='utf-8') as f:
    f.write(subpages_css)

print("Appended subpages CSS to style.css!")

# Update style version in all HTML files
for hf in glob.glob('*.html'):
    if hf in ['elementor-bundle.html', 'every_roti_section.html', 'milld_home.html', 'milld_product.html', 'milld_science_extracted.html']:
        continue
    content = open(hf, encoding='utf-8').read()
    updated = re.sub(r'style\.css(\?v=[0-9.]+)?', 'style.css?v=22.0', content)
    if updated != content:
        with open(hf, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f"Updated style.css version in {hf}")

