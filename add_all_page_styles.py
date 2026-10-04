import re

all_page_styles = """
/* ==========================================================================
   COMPLETE COMPONENT STYLING FOR ALL SUBPAGES
   (our-science, products, login, about, faq, contact, policy pages)
   ========================================================================== */

/* Science Badges Strip */
.science-badges-strip {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.science-badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #FFF;
  border: 1.5px solid #121212;
  border-radius: 9999px;
  padding: 0.4rem 1rem;
  font-size: 0.8rem;
  font-weight: 700;
  color: #121212;
  box-shadow: 2px 2px 0 #121212;
}

.pill-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #D4942A;
}

.section-header {
  text-align: center;
  max-width: 720px;
  margin: 0 auto 3rem;
}

.section-kicker {
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

.section-title {
  font-family: 'Anton', 'Bebas Neue', system-ui, sans-serif;
  font-size: clamp(2.2rem, 5vw, 3.6rem);
  text-transform: uppercase;
  color: #121212;
  margin-bottom: 0.75rem;
}

.section-subtitle {
  font-size: 1.05rem;
  color: rgba(18, 18, 18, 0.75);
  line-height: 1.6;
}

/* Ingredients Cards Grid */
.ingredients-cards-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

@media (min-width: 900px) {
  .ingredients-cards-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.ingredient-card {
  background: #FFF;
  border: 2px solid #121212;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 6px 6px 0 #121212;
  display: flex;
  flex-direction: column;
}

.ingredient-img-frame {
  position: relative;
  height: 220px;
  background: #FAF7F2;
  overflow: hidden;
  border-bottom: 2px solid #121212;
}

.ingredient-img-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.ingredient-num-pill {
  position: absolute;
  top: 14px;
  left: 14px;
  background: #121212;
  color: #FFC107;
  font-family: 'Anton', 'Bebas Neue', sans-serif;
  font-size: 1.1rem;
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid #FFC107;
}

.ingredient-ratio-pill {
  position: absolute;
  top: 14px;
  right: 14px;
  background: #D4942A;
  color: #121212;
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 9999px;
  border: 1px solid #121212;
}

.ingredient-body {
  padding: 1.75rem 1.5rem;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.ingredient-title {
  font-size: 1.35rem;
  text-transform: uppercase;
  margin-bottom: 0.35rem;
}

.ingredient-tagline {
  font-size: 0.85rem;
  font-weight: 700;
  color: #D4942A;
  margin-bottom: 0.85rem;
}

.ingredient-desc {
  font-size: 0.9rem;
  line-height: 1.6;
  color: rgba(18, 18, 18, 0.8);
  margin-bottom: 1.25rem;
}

.ingredient-specs-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: auto;
  border-top: 1px dashed rgba(18, 18, 18, 0.15);
  padding-top: 1rem;
}

.ingredient-specs-list li {
  font-size: 0.82rem;
  color: rgba(18, 18, 18, 0.75);
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.ingredient-specs-list li::before {
  content: '✓';
  color: #2E7D32;
  font-weight: 800;
}

/* Legal & Policy Page Content Cards */
.legal-content-card {
  background: #FFF;
  border: 2px solid #121212;
  border-radius: 18px;
  padding: 2.5rem 2rem;
  box-shadow: 6px 6px 0 #121212;
  margin: 0 auto;
  max-width: 900px;
}

.legal-content-card h2 {
  font-size: 1.5rem;
  text-transform: uppercase;
  margin: 1.75rem 0 0.5rem;
}

.legal-content-card p, .legal-content-card li {
  font-size: 0.95rem;
  line-height: 1.65;
  color: rgba(18, 18, 18, 0.8);
}

.report-spec-table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
}

.report-spec-table th, .report-spec-table td {
  padding: 0.75rem 1rem;
  border: 1px solid rgba(18, 18, 18, 0.15);
  font-size: 0.88rem;
}

.report-spec-table th {
  background: #FAF7F2;
  font-weight: 700;
}

/* Order Receipt & Modal Cards */
.order-receipt-card, .order-success-card {
  background: #FFF;
  border: 2px solid #121212;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 6px 6px 0 #121212;
}

.orc-row {
  display: flex;
  justify-content: space-between;
  padding: 0.6rem 0;
  border-bottom: 1px solid rgba(18, 18, 18, 0.08);
  font-size: 0.88rem;
}

.order-success-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #E8F5E9;
  color: #2E7D32;
  font-size: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.25rem;
}

.payment-options-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin: 1rem 0;
}

.payment-opt-card {
  background: #FFF;
  border: 1.5px solid rgba(18, 18, 18, 0.2);
  border-radius: 10px;
  padding: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.payment-opt-card.active, .payment-opt-card:hover {
  border-color: #D4942A;
  background: #FFFDF5;
}

.payment-opt-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 700;
  font-size: 0.9rem;
}

.rp-amount-bar {
  background: #FAF7F2;
  border-radius: 8px;
  padding: 0.85rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  font-size: 0.85rem;
}

.rp-badge {
  background: #2E7D32;
  color: #FFF;
  font-size: 0.7rem;
  font-weight: 800;
  padding: 3px 8px;
  border-radius: 9999px;
}

.rp-footer {
  margin-top: 1rem;
  text-align: center;
  font-size: 0.72rem;
  color: rgba(18, 18, 18, 0.5);
}

.rp-total-amount {
  font-family: 'Anton', 'Bebas Neue', sans-serif;
  font-size: 1.2rem;
  color: #D4942A;
}

/* Order Success Card Components for Shop Page */
.osc-box {
  background: #FAF7F2;
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1.5rem 0;
  text-align: left;
}

.osc-title {
  font-size: 1.1rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
}

.osc-sub {
  font-size: 0.85rem;
  color: rgba(18, 18, 18, 0.7);
  margin-bottom: 1rem;
}

.osc-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  padding: 0.35rem 0;
}

.osc-btn {
  background: #121212;
  color: #FFFBEF;
  border: none;
  padding: 0.85rem 1.5rem;
  border-radius: 9999px;
  font-weight: 800;
  cursor: pointer;
  width: 100%;
  margin-top: 1rem;
}

.osc-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

/* Login Page Specific Elements */
.google-signin-btn {
  width: 100%;
  background: #FFF;
  color: #121212;
  border: 1.5px solid rgba(18, 18, 18, 0.25);
  border-radius: 9999px;
  padding: 0.85rem 1.25rem;
  font-size: 0.9rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  cursor: pointer;
  transition: all 0.15s ease;
  box-shadow: 2px 2px 0 rgba(18, 18, 18, 0.1);
}

.google-signin-btn:hover {
  border-color: #121212;
  box-shadow: 3px 3px 0 #121212;
}

.email-toggle-row {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.et-btn {
  flex: 1;
  padding: 0.6rem;
  background: #FAF7F2;
  border: 1px solid rgba(18, 18, 18, 0.15);
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.8rem;
  cursor: pointer;
}

.et-btn.active {
  background: #121212;
  color: #FFFBEF;
  border-color: #121212;
}

.otp-box {
  background: #FFFDF5;
  border: 1.5px solid #D4942A;
  border-radius: 10px;
  padding: 1.25rem;
  margin-top: 1rem;
}

.otp-input-group {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  margin: 1rem 0;
}

.otp-digit {
  width: 44px;
  height: 48px;
  text-align: center;
  font-size: 1.3rem;
  font-weight: 800;
  border: 2px solid rgba(18, 18, 18, 0.25);
  border-radius: 8px;
}

.otp-digit:focus {
  outline: none;
  border-color: #D4942A;
}

/* Footer aliases */
.footer-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2.5rem;
}

@media (min-width: 900px) {
  .footer-grid {
    grid-template-columns: 1.2fr 1.8fr;
  }
}

.footer-heading {
  font-size: 0.72rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.22em;
  color: #FFC107 !important;
  margin-bottom: 1.25rem;
}

.logo-title {
  font-family: 'Anton', 'Bebas Neue', system-ui, sans-serif !important;
  font-size: 2rem !important;
  color: #121212;
}

.logo-accent {
  color: #D4942A !important;
}
"""

with open('style.css', 'a', encoding='utf-8') as f:
    f.write(all_page_styles)

print("Successfully added all component styles to style.css!")
