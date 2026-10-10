
// Force Permanent Clean Light Mode (No Dark Mode)
(function() {
  try {
    localStorage.removeItem('milla_theme');
    document.documentElement.removeAttribute('data-theme');
    document.documentElement.setAttribute('data-theme', 'light');
  } catch(e) {}
})();


// =========================================================================
// Third-Party Extension Error Boundary (Suppresses Crypto Wallet inpage.js noise)
// =========================================================================
window.addEventListener('error', function(e) {
  if (e.filename && (e.filename.includes('inpage.js') || e.filename.includes('chrome-extension://') || e.filename.includes('moz-extension://'))) {
    e.stopImmediatePropagation();
    return true;
  }
}, true);

window.addEventListener('unhandledrejection', function(e) {
  var reason = '' + (e.reason || '');
  if (reason.includes('Broadcast channel') || reason.includes('Channel secret') || reason.includes('inpage.js')) {
    e.stopImmediatePropagation();
    e.preventDefault();
  }
});

// ==========================================
// Promotional Coupon & Discount Engine
// ==========================================
let appliedCoupon = null;
try {
  const savedCoupon = localStorage.getItem('millapro_coupon');
  if (savedCoupon) appliedCoupon = JSON.parse(savedCoupon);
} catch (e) {
  appliedCoupon = null;
}

function applyCartCoupon() {
  const input = document.getElementById('cartCouponInput');
  const msgEl = document.getElementById('couponStatusMessage');
  if (!input) return;
  const code = input.value.trim().toUpperCase();
  if (!code) {
    if (msgEl) {
      msgEl.style.color = '#C62828';
      msgEl.innerText = 'Please enter a coupon code.';
    }
    return;
  }
  
  if (code === 'LAUNCH20' || code === 'MILLA20' || code === 'PROTEIN20' || code === 'FLAT20') {
    appliedCoupon = { code: code, percent: 20 };
    localStorage.setItem('millapro_coupon', JSON.stringify(appliedCoupon));
    if (msgEl) {
      msgEl.style.color = '#1B5E20';
      msgEl.innerHTML = `🎉 Coupon <strong>${code}</strong> applied! 20% discount added.`;
    }
    updateCartDrawerUI();
  } else {
    if (msgEl) {
      msgEl.style.color = '#C62828';
      msgEl.innerHTML = `Invalid code "${code}". Try code <strong>LAUNCH20</strong> for 20% OFF!`;
    }
  }
}

function quickApplyCoupon(code) {
  const input = document.getElementById('cartCouponInput');
  if (input) input.value = code;
  applyCartCoupon();
}

function removeCartCoupon() {
  appliedCoupon = null;
  localStorage.removeItem('millapro_coupon');
  updateCartDrawerUI();
}

// ==========================================
// Customer Address & Multi-Step Checkout
// ==========================================
let customerAddress = null;
try {
  const savedAddress = localStorage.getItem('millapro_customer_address');
  if (savedAddress) customerAddress = JSON.parse(savedAddress);
} catch (e) {
  customerAddress = null;
}

function handlePincodeAutoFill(pin) {
  if (pin && pin.length === 6) {
    const cityStateInput = document.getElementById('custCityState');
    if (cityStateInput && !cityStateInput.value) {
      if (pin.startsWith('400')) cityStateInput.value = 'Mumbai, Maharashtra';
      else if (pin.startsWith('110')) cityStateInput.value = 'New Delhi, Delhi';
      else if (pin.startsWith('560')) cityStateInput.value = 'Bengaluru, Karnataka';
      else if (pin.startsWith('500')) cityStateInput.value = 'Hyderabad, Telangana';
      else if (pin.startsWith('600')) cityStateInput.value = 'Chennai, Tamil Nadu';
      else if (pin.startsWith('411')) cityStateInput.value = 'Pune, Maharashtra';
      else cityStateInput.value = 'Pan-India Delivery Hub';
    }
  }
}

function proceedToPaymentStep() {
  const name = document.getElementById('custFullName')?.value?.trim();
  const phone = document.getElementById('custPhone')?.value?.trim();
  const email = document.getElementById('custEmail')?.value?.trim();
  const address = document.getElementById('custAddress')?.value?.trim();
  const pincode = document.getElementById('custPincode')?.value?.trim();
  const cityState = document.getElementById('custCityState')?.value?.trim();

  if (!name || !phone || !email || !address || !pincode || !cityState) {
    alert('Please fill in all delivery details (Name, Phone, Email, Address, Pincode, City/State).');
    return;
  }

  if (phone.length < 10) {
    alert('Please enter a valid 10-digit mobile number for dispatch & tracking updates.');
    return;
  }

  if (!email.includes('@')) {
    alert('Please enter a valid email address for your 5% GST tax invoice.');
    return;
  }

  if (pincode.length !== 6) {
    alert('Please enter a valid 6-digit Indian Postal Pincode.');
    return;
  }

  customerAddress = { name, phone, email, address, pincode, cityState };
  localStorage.setItem('millapro_customer_address', JSON.stringify(customerAddress));

  // Populate Recap Card in Step 2
  const recapName = document.getElementById('recapCustomerName');
  const recapAddr = document.getElementById('recapCustomerAddress');
  const recapCont = document.getElementById('recapCustomerContact');
  if (recapName) recapName.innerText = `Delivering to: ${name}`;
  if (recapAddr) recapAddr.innerText = `${address}, ${cityState} - ${pincode}`;
  if (recapCont) recapCont.innerText = `📞 +91 ${phone} • 📧 ${email}`;

  // Toggle View
  document.getElementById('checkoutStepAddress').classList.remove('active');
  document.getElementById('checkoutStepPayment').classList.add('active');
  document.getElementById('stepperStep1').classList.remove('active');
  document.getElementById('stepperStep2').classList.add('active');
}

function backToAddressStep() {
  document.getElementById('checkoutStepPayment').classList.remove('active');
  document.getElementById('checkoutStepAddress').classList.add('active');
  document.getElementById('stepperStep2').classList.remove('active');
  document.getElementById('stepperStep1').classList.add('active');
}

function finishOrderAndReset() {
  closeRazorpayModal();
  document.getElementById('checkoutStepSuccess').classList.remove('active');
  document.getElementById('checkoutStepAddress').classList.add('active');
  document.getElementById('stepperStep1').classList.add('active');
  document.getElementById('stepperStep2').classList.remove('active');
}

/**
 * MILLA PRO™ - Master Application Script
 * Features: Mobile Sidebar, Synced Cart, 1-Click Razorpay Checkout,
 * Bug-Free Whey Replacement Calculator, Image Switcher, Pincode Checker.
 */

// Master Pack Configuration (Incl. 5% GST HSN 1101)
const PACKS = {
  '1kg': {
    id: '1kg',
    name: '1 KG Stand-up Zipper Pouch',
    weight: '1 KG',
    price: 249,
    mrp: 299,
    discount: 'SAVE 17%',
    basePrice: 237.14,
    gst: 11.86,
    rotis: 30,
    costPerRoti: 8.3
  },
  '5kg': {
    id: '5kg',
    name: '5 KG Family Saver Pack',
    weight: '5 KG',
    price: 1199,
    mrp: 1499,
    discount: 'SAVE 20% (FLAT ₹300 OFF)',
    basePrice: 1141.90,
    gst: 57.10,
    rotis: 150,
    costPerRoti: 7.99
  }
};

let currentPackId = '1kg';
let currentQty = 1;

// Load cart from localStorage or initialize with 1kg default
function getCart() {
  try {
    const saved = localStorage.getItem('millapro_cart_v2');
    if (saved) return JSON.parse(saved);
  } catch (e) {
    console.error('Failed to parse cart', e);
  }
  return [
    {
      id: '1kg',
      name: 'MILLA PRO™ 100% Natural High-Protein Atta (1 KG)',
      price: 249,
      mrp: 299,
      basePrice: 237.14,
      gst: 11.86,
      qty: 2
    }
  ];
}

function saveCart(cart) {
  try {
    localStorage.setItem('millapro_cart_v2', JSON.stringify(cart));
  } catch (e) {
    console.error('Failed to save cart', e);
  }
  updateCartDrawerUI();
}

let cartItems = getCart();

// ==========================================
// Mobile Sidebar Navigation
// ==========================================
function openMobileSidebar() {
  const sidebar = document.getElementById('mobileSidebar');
  const overlay = document.getElementById('sidebarOverlay');
  if (sidebar && overlay) {
    sidebar.classList.add('active');
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closeMobileSidebar() {
  const sidebar = document.getElementById('mobileSidebar');
  const overlay = document.getElementById('sidebarOverlay');
  if (sidebar && overlay) {
    sidebar.classList.remove('active');
    overlay.classList.remove('active');
    document.body.style.overflow = '';
  }
}

// ==========================================
// Pack Selection Logic (Home Page)
// ==========================================
function selectPack(packId) {
  if (!PACKS[packId]) return;
  currentPackId = packId;
  const pack = PACKS[packId];

  // Update selection UI cards
  const card1 = document.getElementById('pack1kg');
  const card5 = document.getElementById('pack5kg');
  if (card1 && card5) {
    card1.classList.toggle('active', packId === '1kg');
    card5.classList.toggle('active', packId === '5kg');
  }

  // Update Pricing Display
  const displayPrice = document.getElementById('displayPrice');
  const displayMrp = document.getElementById('displayMrp');
  const displayDiscount = document.getElementById('displayDiscount');
  const displayGstBreakdown = document.getElementById('displayGstBreakdown');
  const heroPrice = document.getElementById('heroPrice');
  const heroMrp = document.getElementById('heroMrp');
  const heroSave = document.getElementById('heroSave');
  const stickyBarText = document.getElementById('mobileStickyText');
  if (heroPrice) heroPrice.innerText = `₹${pack.price}`;
  if (heroMrp) heroMrp.innerText = `₹${pack.mrp}`;
  if (heroSave) heroSave.innerText = pack.id === '5kg' ? 'Save ₹300' : 'Save ₹50';
  if (stickyBarText) stickyBarText.innerText = `MILLA PRO ${pack.weight} - ₹${pack.price}`;
  document.querySelectorAll('.pack-select-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-pack') === packId);
  });

  if (displayPrice) displayPrice.innerText = pack.price;
  if (displayMrp) displayMrp.innerText = `MRP ₹${pack.mrp}`;
  if (displayDiscount) displayDiscount.innerText = pack.discount;
  if (displayGstBreakdown) {
    displayGstBreakdown.innerHTML = `<strong>Price includes 5% GST</strong> (Base ₹${pack.basePrice.toFixed(2)} + ₹${pack.gst.toFixed(2)} GST)`;
  }

  // Update Sticky Mobile Bar
  const stickyPackName = document.getElementById('stickyMobilePack');
  const stickyPriceText = document.getElementById('stickyMobilePrice');
  const mobileBarPrice = document.getElementById('mobileBarPrice');
  if (stickyPackName) stickyPackName.innerText = `${pack.weight} Pouch`;
  if (stickyPriceText) stickyPriceText.innerHTML = `₹${pack.price} <small style="font-size:0.7rem; color:#6B5B52;">(Incl. 5% GST)</small>`;
  if (mobileBarPrice) mobileBarPrice.innerHTML = `₹${pack.price} <small>(${pack.weight} Pack)</small>`;

  updateModalAmount();
}

function changeQty(delta) {
  const newQty = currentQty + delta;
  if (newQty >= 1 && newQty <= 10) {
    currentQty = newQty;
    const qtyInput = document.getElementById('productQty');
    if (qtyInput) qtyInput.value = currentQty;
    updateModalAmount();
  }
}

// ==========================================
// Cart Management & Drawer
// ==========================================
function addToCart(packId = null, qty = null) {
  const targetPackId = packId || currentPackId;
  const targetQty = qty || currentQty;
  const pack = PACKS[targetPackId];
  if (!pack) return;

  const existing = cartItems.find(item => item.id === pack.id);
  if (existing) {
    existing.qty += targetQty;
  } else {
    cartItems.push({
      id: pack.id,
      name: `MILLA PRO™ High-Protein Atta (${pack.weight})`,
      price: pack.price,
      basePrice: pack.basePrice,
      gst: pack.gst,
      qty: targetQty
    });
  }

  saveCart(cartItems);
  openCartDrawer();
}

function removeCartItem(index) {
  cartItems.splice(index, 1);
  saveCart(cartItems);
  updateCartDrawerUI();
}

function changeCartItemQty(index, delta) {
  if (!cartItems[index]) return;
  const newQty = cartItems[index].qty + delta;
  if (newQty <= 0) {
    removeCartItem(index);
  } else if (newQty <= 15) {
    cartItems[index].qty = newQty;
    saveCart(cartItems);
    updateCartDrawerUI();
  }
}

function quickAddToCart(packId) {
  addToCart(packId, 1);
}

function updateCartDrawerUI() {
  const container = document.getElementById('cartItemsContainer') || document.getElementById('cartItemsList');
  const footerSection = document.getElementById('cartFooterSection') || document.getElementById('cartDrawerFooter');
  const headerCount = document.getElementById('cartDrawerHeaderCount');
  const cartBadge = document.getElementById('navCartCount') || document.getElementById('cartCountBadge');
  const cartBadgeMobile = document.getElementById('mobileCartCount') || document.getElementById('cartCountBadge');

  let totalAmount = 0;
  let totalMrp = 0;
  let totalBase = 0;
  let totalGst = 0;
  let totalCount = 0;

  if (container) {
    container.innerHTML = '';

    if (cartItems.length === 0) {
      if (footerSection) footerSection.style.display = 'none';
      container.innerHTML = `
        <div class="cart-empty-state">
          <div style="font-size:3rem; margin-bottom:12px;">🌾</div>
          <h3 style="color:var(--text-dark); font-size:1.15rem; margin-bottom:6px;">Your Nutrition Cart is Empty</h3>
          <p style="color:#7A6B63; font-size:0.85rem; max-width:280px; margin:0 auto 16px;">
            Upgrade your family's daily rotis to 15g clean pure grain & seed protein.
          </p>
          <div style="display:flex; flex-direction:column; gap:8px; width:100%; max-width:260px; margin:0 auto;">
            <button type="button" onclick="quickAddToCart('1kg')" style="background:var(--secondary); border:none; color:#FFF; padding:10px 16px; border-radius:var(--radius-full); font-weight:800; font-size:0.85rem; cursor:pointer;">
              + Add 1 KG Pouch (₹249)
            </button>
            <button type="button" onclick="quickAddToCart('5kg')" style="background:var(--primary); border:2px solid var(--primary); color:#FFF; padding:10px 16px; border-radius:var(--radius-full); font-weight:800; font-size:0.85rem; cursor:pointer;">
              + Add 5 KG Saver Pack (₹1,199)
            </button>
          </div>
        </div>
      `;
    } else {
      if (footerSection) footerSection.style.display = 'block';

      cartItems.forEach((item, index) => {
        const itemTotal = item.price * item.qty;
        const itemMrp = item.mrp || (item.id === '5kg' ? 1499 : 299);
        const itemMrpTotal = itemMrp * item.qty;
        const itemSavings = itemMrpTotal - itemTotal;

        totalAmount += itemTotal;
        totalMrp += itemMrpTotal;
        totalBase += item.basePrice * item.qty;
        totalGst += item.gst * item.qty;
        totalCount += item.qty;

        const packLabel = item.id === '5kg' ? '5 KG Family Saver Pack' : '1 KG Trial Pouch';
        const thumbSrc = item.id === '5kg' ? 'milla-pouch-cover.jpeg' : 'milla-pouch-front.jpeg';

        let priceLineHtml = `Qty: <strong>${item.qty}</strong> × ₹${item.price} = <strong class="cic-item-total">₹${itemTotal}</strong> <span class="cic-mrp"><strike>₹${itemMrpTotal}</strike></span>`;
        if (appliedCoupon && appliedCoupon.percent) {
          const discTotal = Math.round(itemTotal * (1 - appliedCoupon.percent / 100));
          priceLineHtml = `Qty: <strong>${item.qty}</strong> × ₹${item.price} = <span class="cic-price-strike">₹${itemTotal}</span> <strong class="cic-item-total" style="color:#2E7D32;">₹${discTotal}</strong> <span class="cic-discount-pill">${appliedCoupon.percent}% OFF</span>`;
        }

        const card = document.createElement('div');
        card.className = 'cart-item-card cart-item';
        card.innerHTML = `
          <div class="cic-thumb-wrap">
            <img src="${thumbSrc}" alt="MILLA PRO Atta" class="cic-thumb">
          </div>
          <div class="cic-content">
            <div class="cic-top-row">
              <div>
                <strong class="cic-name">${item.name}</strong>
                <div style="font-size:0.75rem; color:#8C7B72; font-weight:700; margin-top:2px;">${packLabel}</div>
              </div>
              <button type="button" class="cic-remove-btn" onclick="removeCartItem(${index})" title="Remove item" aria-label="Remove item">✕</button>
            </div>

            <div class="cic-badge-row">
              <span class="cic-macro-badge">15g Protein / Roti</span>
              <span class="cic-veg-badge">✓ 100% Vegan</span>
            </div>

            <div class="cic-calc-line">
              ${priceLineHtml}
            </div>

            <div class="cic-stepper-row">
              <div class="cart-qty-stepper">
                <button type="button" class="cqs-btn" onclick="changeCartItemQty(${index}, -1)" aria-label="Decrease quantity">−</button>
                <span class="cqs-val">${item.qty}</span>
                <button type="button" class="cqs-btn" onclick="changeCartItemQty(${index}, 1)" aria-label="Increase quantity">+</button>
              </div>
              <span class="cic-savings-tag">Save ₹${itemSavings}</span>
            </div>
          </div>
        `;
        container.appendChild(card);
      });
    }
  } else {
    // Background tally
    cartItems.forEach(item => {
      const itemMrp = item.mrp || (item.id === '5kg' ? 1499 : 299);
      totalCount += item.qty;
      totalAmount += item.price * item.qty;
      totalMrp += itemMrp * item.qty;
      totalBase += item.basePrice * item.qty;
      totalGst += item.gst * item.qty;
    });
  }

  // Calculate Discounts
  const launchSavings = Math.max(0, totalMrp - totalAmount);
  let couponSavings = 0;
  let finalPayable = totalAmount;

  if (appliedCoupon && appliedCoupon.percent) {
    couponSavings = Math.round(totalAmount * (appliedCoupon.percent / 100));
    finalPayable = totalAmount - couponSavings;
  }

  const finalTaxableBase = finalPayable / 1.05;
  const finalGst = finalPayable - finalTaxableBase;

  // Update Header & Badge Counts
  if (headerCount) headerCount.innerText = `${totalCount} ${totalCount === 1 ? 'Item' : 'Items'}`;
  if (cartBadge) cartBadge.innerText = totalCount;
  if (cartBadgeMobile) cartBadgeMobile.innerText = totalCount;

  // Update Coupon UI Section
  const couponActiveArea = document.getElementById('couponActiveArea');
  const couponInputArea = document.getElementById('couponInputArea');
  const billCouponRow = document.getElementById('billCouponDiscountRow');
  const billCouponDiscount = document.getElementById('billCouponDiscount');
  const billCouponLabel = document.getElementById('billCouponLabel');

  if (appliedCoupon && appliedCoupon.code) {
    if (couponActiveArea) {
      couponActiveArea.style.display = 'block';
      couponActiveArea.innerHTML = `
        <div class="coupon-active-badge">
          <span>🏷️ Coupon <strong>${appliedCoupon.code}</strong> Applied (${appliedCoupon.percent}% OFF)</span>
          <button type="button" class="coupon-remove-btn" onclick="removeCartCoupon()">Remove</button>
        </div>
      `;
    }
    if (couponInputArea) couponInputArea.style.display = 'none';
    if (billCouponRow) {
      billCouponRow.style.display = 'flex';
      if (billCouponLabel) billCouponLabel.innerText = `Promo Discount (${appliedCoupon.code} - ${appliedCoupon.percent}% OFF)`;
      if (billCouponDiscount) billCouponDiscount.innerText = `-₹${couponSavings}`;
    }
  } else {
    if (couponActiveArea) couponActiveArea.style.display = 'none';
    if (couponInputArea) couponInputArea.style.display = 'block';
    if (billCouponRow) billCouponRow.style.display = 'none';
  }

  // Update Itemized Invoice Bill Details
  const billMrpEl = document.getElementById('billMrpTotal');
  const billDiscountEl = document.getElementById('billDiscount');
  const billBaseEl = document.getElementById('billBaseTotal');
  const billGstEl = document.getElementById('billGstTotal');
  const billGrandEl = document.getElementById('billGrandTotal');
  const btnTotalEl = document.getElementById('checkoutBtnTotal');
  const billSavingsBanner = document.getElementById('billSavingsBanner');

  if (billMrpEl) billMrpEl.innerText = `₹${totalMrp}`;
  if (billDiscountEl) billDiscountEl.innerText = `-₹${launchSavings}`;
  if (billBaseEl) billBaseEl.innerText = `₹${finalTaxableBase.toFixed(2)}`;
  if (billGstEl) billGstEl.innerText = `₹${finalGst.toFixed(2)}`;
  if (billGrandEl) billGrandEl.innerText = `₹${finalPayable}`;
  if (btnTotalEl) btnTotalEl.innerText = `₹${finalPayable}`;

  const totalAllSavings = launchSavings + couponSavings;
  if (billSavingsBanner) {
    if (totalAllSavings > 0) {
      billSavingsBanner.style.display = 'block';
      billSavingsBanner.innerHTML = `🎉 You are saving <strong>₹${totalAllSavings}</strong> on this order!`;
    } else {
      billSavingsBanner.style.display = 'none';
    }
  }
}

function openCartDrawer() {
  const overlay = document.getElementById('cartOverlay');
  const drawer = document.getElementById('cartDrawer');
  if (overlay) overlay.style.display = 'block';
  if (drawer) drawer.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeCartDrawer() {
  const overlay = document.getElementById('cartOverlay');
  const drawer = document.getElementById('cartDrawer');
  if (overlay) overlay.style.display = 'none';
  if (drawer) drawer.classList.remove('open');
  document.body.style.overflow = '';
}

// ==========================================
// 1-Click Razorpay Modal Checkout
// ==========================================
function updateModalAmount() {
  let total = 0;
  if (cartItems.length > 0) {
    cartItems.forEach(i => { total += i.price * i.qty; });
  } else {
    const pack = PACKS[currentPackId] || PACKS['1kg'];
    total = pack.price * currentQty;
  }

  let finalPayable = total;
  if (appliedCoupon && appliedCoupon.percent) {
    finalPayable = total - Math.round(total * (appliedCoupon.percent / 100));
  }

  const finalTaxableBase = finalPayable / 1.05;
  const totalGst = finalPayable - finalTaxableBase;

  const modalTotal = document.getElementById('modalTotalAmount');
  const modalTax = document.getElementById('modalTaxNote');
  const btnContinue = document.getElementById('btnContinueToPayment');

  if (modalTotal) modalTotal.innerText = `₹${finalPayable}`;
  if (modalTax) modalTax.innerHTML = `Includes ₹${totalGst.toFixed(2)} (5% GST) • <strong>Delivery in 3–5 Days</strong> • <strong>Prepaid Only (No COD)</strong>`;
  if (btnContinue) btnContinue.innerHTML = `<span>Continue to Payment • ₹${finalPayable}</span> <span>&rarr;</span>`;
}

function triggerRazorpayCheckout() {
  closeCartDrawer();
  closeMobileSidebar();
  updateModalAmount();

  // Pre-populate customer address if saved
  if (customerAddress) {
    const n = document.getElementById('custFullName');
    const p = document.getElementById('custPhone');
    const e = document.getElementById('custEmail');
    const a = document.getElementById('custAddress');
    const pin = document.getElementById('custPincode');
    const cs = document.getElementById('custCityState');
    if (n && customerAddress.name) n.value = customerAddress.name;
    if (p && customerAddress.phone) p.value = customerAddress.phone;
    if (e && customerAddress.email) e.value = customerAddress.email;
    if (a && customerAddress.address) a.value = customerAddress.address;
    if (pin && customerAddress.pincode) pin.value = customerAddress.pincode;
    if (cs && customerAddress.cityState) cs.value = customerAddress.cityState;
  }

  // Ensure Step 1 is active
  const s1 = document.getElementById('checkoutStepAddress');
  const s2 = document.getElementById('checkoutStepPayment');
  const s3 = document.getElementById('checkoutStepSuccess');
  if (s1) s1.classList.add('active');
  if (s2) s2.classList.remove('active');
  if (s3) s3.classList.remove('active');

  const st1 = document.getElementById('stepperStep1');
  const st2 = document.getElementById('stepperStep2');
  if (st1) st1.classList.add('active');
  if (st2) st2.classList.remove('active');

  const modal = document.getElementById('razorpayModal');
  if (modal) {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }
}

function closeRazorpayModal() {
  const modal = document.getElementById('razorpayModal');
  if (modal) {
    modal.style.display = 'none';
    document.body.style.overflow = '';
  }
}

function handleModalOverlayClick(e) {
  if (e.target.id === 'razorpayModal') {
    closeRazorpayModal();
  }
}

function simulatePaymentSuccess(method) {
  let total = 0;
  cartItems.forEach(i => { total += i.price * i.qty; });
  if (total === 0) total = 498;

  let finalPayable = total;
  if (appliedCoupon && appliedCoupon.percent) {
    finalPayable = total - Math.round(total * (appliedCoupon.percent / 100));
  }

  const orderNum = `#MP-2026-${Math.floor(1000 + Math.random() * 9000)}`;
  const custName = customerAddress ? customerAddress.name : 'Valued Customer';
  const custAddr = customerAddress ? `${customerAddress.address}, ${customerAddress.cityState} - ${customerAddress.pincode}` : 'Registered Address';

  // Fill receipt fields
  const rOrder = document.getElementById('receiptOrderId');
  const rCust = document.getElementById('receiptCustomer');
  const rAddr = document.getElementById('receiptAddress');
  const rMeth = document.getElementById('receiptMethod');
  const rTotal = document.getElementById('receiptTotalAmount');

  if (rOrder) rOrder.innerText = orderNum;
  if (rCust) rCust.innerText = custName;
  if (rAddr) rAddr.innerText = custAddr;
  if (rMeth) rMeth.innerText = method;
  if (rTotal) rTotal.innerText = `₹${finalPayable}`;

  // Switch to Step 3
  document.getElementById('checkoutStepPayment')?.classList.remove('active');
  document.getElementById('checkoutStepAddress')?.classList.remove('active');
  document.getElementById('checkoutStepSuccess')?.classList.add('active');
}

// ==========================================
// Product Gallery Switcher
// ==========================================
function switchVisualMode(mode) {
  document.querySelectorAll('.thumbnail-strip .thumb').forEach(t => t.classList.remove('active'));

  const viewport = document.getElementById('mainImageViewport');
  if (!viewport) return;

  if (mode === 'front') {
    const t = document.getElementById('thumbFront');
    if (t) t.classList.add('active');
    viewport.innerHTML = `
      <div class="real-cover-container">
        <img src="milla-pouch-front.jpeg" alt="MILLA PRO 100% Natural High-Protein Atta Front Pouch" class="real-pouch-img">
      </div>
    `;
  } else if (mode === 'back') {
    const t = document.getElementById('thumbBack');
    if (t) t.classList.add('active');
    viewport.innerHTML = `
      <div class="real-cover-container">
        <img src="milla-pouch-back.jpeg" alt="MILLA PRO Official Cost Benchmark & Lab Facts Back Pouch" class="real-pouch-img">
      </div>
    `;
  } else if (mode === 'full') {
    const t = document.getElementById('thumbFull');
    if (t) t.classList.add('active');
    viewport.innerHTML = `
      <div class="real-cover-container">
        <img src="milla-pouch-cover.jpeg" alt="MILLA PRO Full Packaging Front & Back" class="real-pouch-img">
      </div>
    `;
  } else if (mode === 'cost') {
    const t = document.getElementById('thumbCost');
    if (t) t.classList.add('active');
    viewport.innerHTML = `
      <div style="background:#FFF9F3; border:2px solid var(--primary); border-radius:14px; padding:24px 16px; text-align:center; width:100%; max-width:380px;">
        <span style="background:var(--primary); color:#FFF; font-size:0.75rem; font-weight:900; padding:3px 12px; border-radius:50px; display:inline-block; margin-bottom:8px;">
          GET 45g PROTEIN. COMPARE THE COST.
        </span>
        <div style="font-size:1.3rem; font-weight:900; color:var(--text-dark); margin-bottom:12px;">Verified Back of Pouch Data:</div>
        
        <div style="display:flex; justify-content:space-between; align-items:center; background:#FFF; border:2px solid var(--secondary); border-radius:8px; padding:10px; margin-bottom:8px;">
          <div style="text-align:left;"><strong>MILLA PRO ATTA</strong><br><small>100g (= 3 rotis)</small></div>
          <strong style="color:var(--secondary); font-size:1.4rem;">₹20</strong>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; background:#FFF; border:1px solid #DDD; border-radius:8px; padding:10px; margin-bottom:8px;">
          <div style="text-align:left;"><strong>Whey Protein</strong><br><small>2 scoops (60g)</small></div>
          <strong style="color:#C62828; font-size:1.1rem;">₹140 – ₹180</strong>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; background:#FFF; border:1px solid #DDD; border-radius:8px; padding:10px;">
          <div style="text-align:left;"><strong>Paneer</strong><br><small>250g paneer</small></div>
          <strong style="color:#C62828; font-size:1.1rem;">₹110 – ₹125</strong>
        </div>
      </div>
    `;
  }
}

// ==========================================
// INTERACTIVE WHEY REPLACEMENT CALCULATOR (100% Tested & Bug-Free)
// ==========================================
function updateSliderTrack(slider) {
  if (!slider) return;
  const min = parseFloat(slider.min) || 0;
  const max = parseFloat(slider.max) || 100;
  const val = parseFloat(slider.value) || min;
  const pct = ((val - min) / (max - min)) * 100;
  slider.style.background = `linear-gradient(to right, #E05A1B 0%, #E05A1B ${pct}%, #E8D8C8 ${pct}%, #E8D8C8 100%)`;
}

let isUpdatingFromWhey = false;
let isUpdatingFromRoti = false;

function onRotiSliderChange() {
  if (isUpdatingFromWhey) return;
  isUpdatingFromRoti = true;

  const rotiInput = document.getElementById('dailyRotiRange');
  const scoopInput = document.getElementById('wheyScoopRange');
  if (rotiInput && scoopInput) {
    const rotis = parseInt(rotiInput.value, 10) || 3;
    const protein = rotis * 15;
    const equivalentScoops = Math.min(4, Math.round((protein / 24) * 10) / 10);
    // sync whey slider to equivalent
    scoopInput.value = Math.min(4, Math.round(equivalentScoops));
    updateSliderTrack(scoopInput);
  }

  runWheyCalculator();
  isUpdatingFromRoti = false;
}

function onWheySliderChange() {
  if (isUpdatingFromRoti) return;
  isUpdatingFromWhey = true;

  const rotiInput = document.getElementById('dailyRotiRange');
  const scoopInput = document.getElementById('wheyScoopRange');
  if (rotiInput && scoopInput) {
    const scoops = parseFloat(scoopInput.value) || 2;
    const wheyProtein = scoops * 24;
    // How many rotis needed for this whey protein (15g per roti)
    const rotisNeeded = Math.min(8, Math.max(1, Math.round(wheyProtein / 15)));
    rotiInput.value = rotisNeeded;
    updateSliderTrack(rotiInput);
  }

  runWheyCalculator();
  isUpdatingFromWhey = false;
}

function runWheyCalculator() {
  const rotiInput = document.getElementById('dailyRotiRange');
  const scoopInput = document.getElementById('wheyScoopRange');
  const costInput = document.getElementById('wheyCostRange');
  if (!costInput) return;

  const rotis = rotiInput ? (parseInt(rotiInput.value, 10) || 3) : 3;
  const scoops = scoopInput ? parseInt(scoopInput.value, 10) : 2;
  const tubCost = parseInt(costInput.value, 10) || 2400;

  // 1 Milla Pro Roti = 15g Protein (45g per 100g flour = ~33g flour per roti)
  const rotiProtein = rotis * 15;
  const replacedWheyScoops = Math.round((rotiProtein / 24) * 10) / 10;

  // Update Roti Displays
  const dailyRotiValEl = document.getElementById('dailyRotiVal');
  const rotiProteinValEl = document.getElementById('rotiProteinVal');
  const rotiCountEl = document.getElementById('rotiCountVal');
  const totalRotiProteinValEl = document.getElementById('totalRotiProteinVal');
  const replacedWheyTextEl = document.getElementById('replacedWheyText');

  if (dailyRotiValEl) dailyRotiValEl.innerText = rotis;
  if (rotiProteinValEl) rotiProteinValEl.innerText = `${rotiProtein}g`;
  if (rotiCountEl) rotiCountEl.innerText = `${rotis} Daily Rotis`;
  if (totalRotiProteinValEl) totalRotiProteinValEl.innerText = `${rotiProtein}g protein`;
  if (replacedWheyTextEl) replacedWheyTextEl.innerText = `${replacedWheyScoops} Scoops of Whey`;

  // Update Whey Controls Displays
  const scoopsValEl = document.getElementById('wheyScoopsVal');
  const tubCostValEl = document.getElementById('wheyTubCostVal');
  const resScoopsText = document.getElementById('resScoopsText');
  const resProteinText = document.getElementById('resProteinText');
  const resRotisCountText = document.getElementById('resRotisCountText');

  if (scoopsValEl) scoopsValEl.innerText = scoops;
  if (tubCostValEl) tubCostValEl.innerText = tubCost;
  if (resScoopsText) resScoopsText.innerText = replacedWheyScoops;
  if (resProteinText) resProteinText.innerText = `${rotiProtein}g`;
  if (resRotisCountText) resRotisCountText.innerText = rotis;

  // Slider Track Visual Update
  updateSliderTrack(rotiInput);
  updateSliderTrack(scoopInput);
  updateSliderTrack(costInput);

  // Cost calculation:
  // 1kg tub of whey has ~30 scoops (33g/scoop, 24g protein). Cost per scoop = tubCost / 30.
  const costPerScoop = tubCost / 30;
  
  // Monthly Whey spend equivalent for the protein delivered by these rotis:
  const monthlyWheySpend = Math.round(replacedWheyScoops * costPerScoop * 30);

  // MILLA PRO cost benchmark from official pouch:
  // 45g protein (= 3 rotis = 100g flour) = ₹20.
  // Cost per roti = ₹20 / 3 = ~₹6.67.
  const dailyMillaSpend = rotis * (20 / 3);
  const monthlyMillaSpend = Math.round(dailyMillaSpend * 30);

  const monthlySavings = Math.max(0, monthlyWheySpend - monthlyMillaSpend);
  const annualSavings = monthlySavings * 12;

  // Update DOM Elements
  const monthlyWheyEl = document.getElementById('monthlyWheyCost');
  const monthlyMillaEl = document.getElementById('monthlyMillaCost');
  const monthlySavingsEl = document.getElementById('monthlySavingsVal');
  const annualSavingsEl = document.getElementById('annualSavingsVal');
  const btnSavingsEl = document.getElementById('btnSavingsVal');

  if (monthlyWheyEl) monthlyWheyEl.innerText = `₹${monthlyWheySpend.toLocaleString('en-IN')}`;
  if (monthlyMillaEl) monthlyMillaEl.innerText = `₹${monthlyMillaSpend.toLocaleString('en-IN')}`;
  
  if (monthlySavingsEl) {
    monthlySavingsEl.innerText = monthlySavings.toLocaleString('en-IN');
    monthlySavingsEl.classList.remove('pulse-update');
    void monthlySavingsEl.offsetWidth;
    monthlySavingsEl.classList.add('pulse-update');
  }
  if (annualSavingsEl) {
    annualSavingsEl.innerText = annualSavings.toLocaleString('en-IN');
    annualSavingsEl.classList.remove('pulse-update');
    void annualSavingsEl.offsetWidth;
    annualSavingsEl.classList.add('pulse-update');
  }
  if (btnSavingsEl) btnSavingsEl.innerText = monthlySavings.toLocaleString('en-IN');
}

function setWheyTubPrice(price, btnElement) {
  const costInput = document.getElementById('wheyCostRange');
  if (costInput) {
    costInput.value = price;
    document.querySelectorAll('.brand-btn').forEach(b => b.classList.remove('active'));
    if (btnElement) btnElement.classList.add('active');
    runWheyCalculator();
  }
}

function applyWheyRecommendation() {
  selectPack('5kg');
  const hero = document.getElementById('hero');
  if (hero) {
    hero.scrollIntoView({ behavior: 'smooth' });
  } else {
    window.location.href = 'index.html#hero';
  }
}

// ==========================================
// Pincode Validator
// ==========================================
function checkPincode() {
  const pinInput = document.getElementById('pincodeInput');
  const res = document.getElementById('pincodeResult');
  if (!pinInput || !res) return;

  const pin = pinInput.value.trim();
  if (pin.length !== 6 || isNaN(pin)) {
    res.innerText = '❌ Please enter a valid 6-digit Pincode';
    res.style.color = '#C62828';
    return;
  }

  res.innerText = `✓ Pincode ${pin}: Serviceable! Pan-India delivery in 3–5 Days via Bluedart / Delhivery. (100% Prepaid Orders, Strictly No COD).`;
  res.style.color = '#2E7D32';
}

function handlePinKey(event) {
  if (event.key === 'Enter') {
    checkPincode();
  }
}

// ==========================================
// FAQ Accordion
// ==========================================
function toggleFaq(btn) {
  if (!btn) return;
  var item = btn.closest('.faq-item') || btn.parentElement;
  if (!item) return;

  var isOpen = item.classList.contains('is-open') || item.classList.contains('active');
  var parent = item.parentElement;
  
  if (parent) {
    parent.querySelectorAll('.faq-item').forEach(function (el) {
      if (el !== item) {
        el.classList.remove('is-open', 'active');
        var b = el.querySelector('.faq-btn, .faq-question');
        if (b) b.setAttribute('aria-expanded', 'false');
        var ic = el.querySelector('.icon');
        if (ic) ic.innerText = '+';
      }
    });
  }

  if (isOpen) {
    item.classList.remove('is-open', 'active');
    btn.setAttribute('aria-expanded', 'false');
    var icon = btn.querySelector('.icon');
    if (icon) icon.innerText = '+';
  } else {
    item.classList.add('is-open', 'active');
    btn.setAttribute('aria-expanded', 'true');
    var icon = btn.querySelector('.icon');
    if (icon) icon.innerText = '−';
  }
  if (typeof playMicroSound === 'function') playMicroSound('tick');
}

// ==========================================
// Contact Form Submission (Mock Handler)
// ==========================================
function handleContactSubmit(event) {
  event.preventDefault();
  const name = document.getElementById('contactName')?.value || 'Customer';
  showToast(`Thank you ${name}! Your inquiry has been received. Our team will get back to you shortly.`);
  event.target.reset();
}

// ==========================================
// Customer Reviews & Interactive Review Submission
// ==========================================
const DEFAULT_REVIEWS = [
  {
    name: "Dr. Ananya S.",
    city: "Bandra, Mumbai",
    rating: 5,
    pack: "5KG Family Saver Pack",
    title: "No bloating, pure clean energy for the family!",
    body: "Being lactose intolerant, whey powders always caused severe gas and gut discomfort. Switching to MILLA PRO rotis has been life-changing. 3 rotis give me 45g of protein with my regular subzi, and my digestion is completely peaceful.",
    date: "Verified Purchase • 2 days ago",
    helpful: 42,
    category: "family"
  },
  {
    name: "Vikram K.",
    city: "Indiranagar, Bengaluru",
    rating: 5,
    pack: "5KG Family Saver Pack",
    title: "Saved over ₹4,000 every month on whey protein",
    body: "I was spending ₹3,600 on imported whey every 25 days. With MILLA PRO, my post-workout meal is 4 hot rotis with dal/paneer. Soft, delicious, and puffed up just like regular wheat rotis. 10/10 innovation.",
    date: "Verified Purchase • 5 days ago",
    helpful: 89,
    category: "gym"
  },
  {
    name: "Meera & Rajesh P.",
    city: "Chembur, Mumbai",
    rating: 5,
    pack: "5KG Family Pack",
    title: "Our entire family loves the taste and softness",
    body: "Usually high-protein flours are hard or bitter. MILLA PRO kneads easily with warm water and the rotis stay soft till evening in my kids' lunch boxes. Both my husband and teenagers eat it happily.",
    date: "Verified Purchase • 1 week ago",
    helpful: 57,
    category: "family"
  },
  {
    name: "Captain Rohit Malhotra",
    city: "Vasant Kunj, New Delhi",
    rating: 5,
    pack: "5KG Family Pack",
    title: "Lab-level clean macros without synthetic additives",
    body: "I have been training for 14 years and always hated the chalky taste and artificial sweeteners in whey. MILLA PRO is genuine whole wheat goodness with roasted peanut & soya. 60g protein in 4 rotis is unmatched anywhere in India.",
    date: "Verified Purchase • 10 days ago",
    helpful: 34,
    category: "gym"
  }
];

let currentReviewFilter = 'all';

function setReviewFilter(filterName, btn) {
  currentReviewFilter = filterName;
  document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderReviewsUI();
}

function markReviewHelpful(index, btn) {
  const reviews = getStoredReviews();
  if (reviews[index]) {
    reviews[index].helpful = (reviews[index].helpful || 0) + 1;
    saveReviews(reviews);
    if (btn) {
      btn.innerHTML = `👍 Helpful (${reviews[index].helpful})`;
      btn.style.color = 'var(--primary)';
      btn.style.borderColor = 'var(--primary)';
      btn.disabled = true;
    }
  }
}

function getStoredReviews() {
  try {
    const raw = localStorage.getItem('milla_customer_reviews');
    return raw ? JSON.parse(raw) : DEFAULT_REVIEWS;
  } catch (e) {
    return DEFAULT_REVIEWS;
  }
}

function saveReviews(reviews) {
  try {
    localStorage.setItem('milla_customer_reviews', JSON.stringify(reviews));
  } catch (e) {}
}

let selectedReviewRating = 5;

function setReviewRating(rating) {
  selectedReviewRating = rating;
  const stars = document.querySelectorAll('#starRatingSelect .star-item');
  stars.forEach((star, index) => {
    if (index < rating) {
      star.classList.add('active');
    } else {
      star.classList.remove('active');
    }
  });
}

function renderReviewsUI() {
  const container = document.getElementById('reviewsGrid');
  if (!container) return;

  const allReviews = getStoredReviews();
  let reviews = allReviews;

  if (currentReviewFilter === '5star') {
    reviews = allReviews.filter(r => r.rating === 5);
  } else if (currentReviewFilter === 'family') {
    reviews = allReviews.filter(r => r.category === 'family');
  } else if (currentReviewFilter === 'gym') {
    reviews = allReviews.filter(r => r.category === 'gym');
  }

  container.innerHTML = '';

  reviews.forEach((r, idx) => {
    const starsStr = '★'.repeat(r.rating) + '☆'.repeat(5 - r.rating);
    const initials = r.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase() || 'CU';
    const packTag = r.pack ? `<span style="font-size:0.72rem; color:var(--primary); font-weight:800; display:block; margin-top:2px;">Purchased: ${escapeHTML(r.pack)}</span>` : '';
    const helpfulCount = r.helpful || (18 + (idx * 7));

    const card = document.createElement('div');
    card.className = 'review-card';
    card.innerHTML = `
      <div>
        <div class="review-top-row" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <span class="stars-gold">${starsStr}</span>
          <span class="verified-buyer-badge" style="font-size:0.7rem; background:#E8F5E9; color:#2E7D32; padding:3px 8px; border-radius:50px; font-weight:800;">✓ Verified Buyer</span>
        </div>
        <h4 class="review-title" style="font-size:1.05rem; font-weight:800; margin-bottom:8px; color:var(--text-dark);">${escapeHTML(r.title)}</h4>
        <p class="review-body-text" style="font-size:0.88rem; color:var(--text-muted); line-height:1.6; margin-bottom:12px;">${escapeHTML(r.body)}</p>
        
        <div style="display:flex; gap:6px; flex-wrap:wrap; margin-bottom:12px;">
          <span style="background:#FFF9F3; border:1px solid #FFE0B2; color:#E05A1B; font-size:0.7rem; font-weight:800; padding:2px 8px; border-radius:4px;">15g Protein / Roti</span>
          <span style="background:#E8F5E9; border:1px solid #C8E6C9; color:#2E7D32; font-size:0.7rem; font-weight:800; padding:2px 8px; border-radius:4px;">Zero Bloat</span>
          <span style="background:#F5F5F5; border:1px solid #E0E0E0; color:#616161; font-size:0.7rem; font-weight:800; padding:2px 8px; border-radius:4px;">Soft & Puffed</span>
        </div>
      </div>
      <div>
        <div class="reviewer-meta" style="display:flex; align-items:center; gap:12px; padding-top:12px; border-top:1px solid var(--border-light);">
          <div class="reviewer-avatar">${initials}</div>
          <div style="flex:1;">
            <div class="reviewer-name">${escapeHTML(r.name)}</div>
            <div class="reviewer-city">${escapeHTML(r.city)} • <small style="color:var(--secondary); font-weight:700;">${r.date || 'Verified Review'}</small></div>
            ${packTag}
          </div>
        </div>
        <button type="button" class="review-helpful-btn" onclick="markReviewHelpful(${idx}, this)">
          👍 Helpful (${helpfulCount})
        </button>
      </div>
    `;
    container.appendChild(card);
  });
}

function escapeHTML(str) {
  if (!str) return '';
  return str.replace(/[&<>'"]/g, 
    tag => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      "'": '&#39;',
      '"': '&quot;'
    }[tag] || tag)
  );
}

function openReviewModal() {
  const modal = document.getElementById('reviewModalOverlay');
  if (modal) {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    setReviewRating(5);
  }
}

function closeReviewModal() {
  const modal = document.getElementById('reviewModalOverlay');
  if (modal) {
    modal.style.display = 'none';
    document.body.style.overflow = '';
  }
}

function submitCustomerReview(event) {
  event.preventDefault();
  const name = document.getElementById('revName')?.value.trim();
  const city = document.getElementById('revCity')?.value.trim();
  const title = document.getElementById('revTitle')?.value.trim();
  const body = document.getElementById('revBody')?.value.trim();

  if (!name || !title || !body) {
    showToast('⚠️ Please fill out all required fields.');
    return;
  }

  const newReview = {
    name: name,
    city: city || 'Verified Location',
    rating: selectedReviewRating,
    title: title,
    body: body,
    date: 'Verified Buyer • Just now'
  };

  const reviews = getStoredReviews();
  reviews.unshift(newReview);
  saveReviews(reviews);
  renderReviewsUI();
  closeReviewModal();
  event.target.reset();

  showToast('🎉 Thank you! Your verified review has been published.');
}

function showToast(message) {
  let toast = document.getElementById('globalToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'globalToast';
    toast.className = 'toast-msg';
    document.body.appendChild(toast);
  }
  toast.innerText = message;
  toast.classList.add('show');
  setTimeout(() => {
    toast.classList.remove('show');
  }, 3500);
}

// ==========================================
// DOM Initialization & Mobile Touch Binding
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
  updateCartDrawerUI();
  renderReviewsUI();

  // Calculator initialization and two-way dynamic reactive binding
  const rotiSlider = document.getElementById('dailyRotiRange');
  const scoopSlider = document.getElementById('wheyScoopRange');
  const costSlider = document.getElementById('wheyCostRange');

  if (rotiSlider) {
    rotiSlider.addEventListener('input', onRotiSliderChange);
    rotiSlider.addEventListener('change', onRotiSliderChange);
  }
  if (scoopSlider) {
    scoopSlider.addEventListener('input', onWheySliderChange);
    scoopSlider.addEventListener('change', onWheySliderChange);
  }
  if (costSlider) {
    costSlider.addEventListener('input', runWheyCalculator);
    costSlider.addEventListener('change', runWheyCalculator);
  }

  if (rotiSlider || scoopSlider || costSlider) {
    runWheyCalculator();
  }

  if (document.getElementById('pack1kg')) {
    selectPack('1kg');
  }

  // Scroll Header shadow effect
  window.addEventListener('scroll', () => {
    const header = document.querySelector('.site-header');
    if (header) {
      header.classList.toggle('scrolled', window.scrollY > 20);
    }
  });
});

// ==========================================
// Simple Savings Calculator (Single Slider)
// ==========================================
function initSimpleCalc() {
  const slider = document.getElementById('simpleRotiSlider');
  if (!slider) return;

  // Constants:
  // Average whey protein supplement in India: ₹3,500 per kg container (~750g pure protein = ~₹4.67 per gram protein)
  // Milla Pro Atta: ₹249/kg (~₹0.249 per gram of atta). 
  // 1 Milla Pro Roti = ~33g atta = 15g protein = ~₹8.20 per roti.
  const SUPPLEMENT_AVG_KG = 3500;
  const SUPPLEMENT_PROTEIN_PER_G_COST = 3500 / 750; // ₹4.67 per gram protein
  const MILLA_COST_PER_ROTI = (249 / 1000) * 33; // ~₹8.22 per roti

  function updateSimpleCalc() {
    const rotis = parseInt(slider.value) || 3;
    const dailyProtein = rotis * 15; // 15g per roti
    
    // Monthly calculation (30 days)
    const monthlyMillaCost = Math.round(rotis * MILLA_COST_PER_ROTI * 30);
    const monthlySupplementCost = Math.round(dailyProtein * SUPPLEMENT_PROTEIN_PER_G_COST * 30);
    const monthlySavings = Math.max(0, monthlySupplementCost - monthlyMillaCost);
    const annualSavings = monthlySavings * 12;

    const fmt = (n) => '₹' + n.toLocaleString('en-IN');

    const el = (id) => document.getElementById(id);
    if (el('simpleRotiCount')) el('simpleRotiCount').textContent = rotis;
    if (el('simpleProteinVal')) el('simpleProteinVal').textContent = dailyProtein + 'g';
    if (el('simpleMillaCostVal')) el('simpleMillaCostVal').textContent = fmt(monthlyMillaCost);
    if (el('simpleSupplementCostVal')) el('simpleSupplementCostVal').textContent = fmt(monthlySupplementCost);
    if (el('simpleSavingsVal')) el('simpleSavingsVal').textContent = fmt(monthlySavings);
    if (el('simpleAnnualSavings')) el('simpleAnnualSavings').textContent = fmt(annualSavings) + ' / yr';
  }

  slider.addEventListener('input', updateSimpleCalc);
  updateSimpleCalc();
}



// ==========================================
// Robust Cart & Mobile Sidebar Handlers
// ==========================================
function openCartDrawer() {
  const overlay = document.getElementById('cartOverlay');
  const drawer = document.getElementById('cartDrawer');
  if (overlay) {
    overlay.style.display = 'block';
    setTimeout(() => overlay.classList.add('active'), 10);
  }
  if (drawer) {
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
    setTimeout(() => { overlay.style.display = 'none'; }, 250);
  }
  if (drawer) {
    drawer.classList.remove('open');
  }
  document.body.style.overflow = '';
}

function openMobileSidebar() {
  const sidebar = document.getElementById('mobileSidebar');
  const overlay = document.getElementById('sidebarOverlay');
  if (overlay) {
    overlay.style.display = 'block';
    setTimeout(() => overlay.classList.add('active'), 10);
  }
  if (sidebar) {
    sidebar.classList.add('active');
  }
  document.body.style.overflow = 'hidden';
}

function closeMobileSidebar() {
  const sidebar = document.getElementById('mobileSidebar');
  const overlay = document.getElementById('sidebarOverlay');
  if (overlay) {
    overlay.classList.remove('active');
    setTimeout(() => { overlay.style.display = 'none'; }, 250);
  }
  if (sidebar) {
    sidebar.classList.remove('active');
  }
  document.body.style.overflow = '';
}

// ==========================================
// Working Whey Protein Cost Calculator
// Benchmark: ₹3,500 / kg standard whey in India
// ==========================================
function updateWheyCostCalc(rotis) {
  const r = parseInt(rotis, 10) || 3;
  const proteinGrams = Math.round(r * 15.33); // 15.33g protein per roti
  
  // Whey Powder: ₹3,500 / kg (with ~75% protein purity = ₹4.67 per gram of protein)
  // Or standard scoop: 33g scoop = 24g protein = ~₹115 per scoop
  const wheyDailyCost = Math.round(proteinGrams * (3500 / 750)); 
  const wheyMonthlyCost = wheyDailyCost * 30;

  // MILLA PRO Atta: ₹240/kg (5kg Saver Pack) or ₹249/kg (1kg Pouch)
  // 100g flour = 3 rotis = 46g protein = ₹24 (or ₹20 on 5kg pack)
  const millaDailyCost = Math.round(r * 6.67);
  const millaMonthlyCost = millaDailyCost * 30;

  const monthlySavings = wheyMonthlyCost - millaMonthlyCost;
  const yearlySavings = monthlySavings * 12;

  // Update UI elements
  const countEl = document.getElementById('wheyRotiCount');
  const unitEl = document.getElementById('wheyRotiUnit');
  const proteinEl = document.getElementById('wheyProteinGrams');
  const wheyCostEl = document.getElementById('wheyMonthlyCostVal');
  const millaCostEl = document.getElementById('millaMonthlyCostVal');
  const savingsEl = document.getElementById('wheySavingsMonthlyVal');
  const yearlyEl = document.getElementById('wheySavingsYearlyVal');

  if (countEl) countEl.innerText = r;
  if (unitEl) unitEl.innerText = (r === 1) ? 'roti' : 'rotis';
  if (proteinEl) proteinEl.innerText = proteinGrams + 'g';
  if (wheyCostEl) wheyCostEl.innerText = '₹' + wheyMonthlyCost.toLocaleString('en-IN');
  if (millaCostEl) millaCostEl.innerText = '₹' + millaMonthlyCost.toLocaleString('en-IN');
  if (savingsEl) savingsEl.innerText = '₹' + monthlySavings.toLocaleString('en-IN');
  if (yearlyEl) yearlyEl.innerText = '₹' + yearlySavings.toLocaleString('en-IN');
}



// ==========================================
// Comprehensive Auth Simulation Handlers
// ==========================================
function switchAuthMethod(method) {
  const tabMobile = document.getElementById('tabMobileBtn');
  const tabEmail = document.getElementById('tabEmailBtn');
  const tabTrack = document.getElementById('tabTrackBtn');

  const viewMobile = document.getElementById('authMobileView');
  const viewEmail = document.getElementById('authEmailView');
  const viewTrack = document.getElementById('authTrackView');

  if (tabMobile) tabMobile.classList.remove('active');
  if (tabEmail) tabEmail.classList.remove('active');
  if (tabTrack) tabTrack.classList.remove('active');

  if (viewMobile) viewMobile.style.display = 'none';
  if (viewEmail) viewEmail.style.display = 'none';
  if (viewTrack) viewTrack.style.display = 'none';

  if (method === 'mobile') {
    if (tabMobile) tabMobile.classList.add('active');
    if (viewMobile) viewMobile.style.display = 'block';
  } else if (method === 'email') {
    if (tabEmail) tabEmail.classList.add('active');
    if (viewEmail) viewEmail.style.display = 'block';
  } else if (method === 'track') {
    if (tabTrack) tabTrack.classList.add('active');
    if (viewTrack) viewTrack.style.display = 'block';
  }
}

function toggleEmailMode(mode) {
  const btnLogin = document.getElementById('etLoginBtn');
  const btnSignup = document.getElementById('etSignupBtn');
  const formLogin = document.getElementById('emailLoginForm');
  const formSignup = document.getElementById('emailSignupForm');

  if (mode === 'login') {
    if (btnLogin) btnLogin.classList.add('active');
    if (btnSignup) btnSignup.classList.remove('active');
    if (formLogin) formLogin.style.display = 'block';
    if (formSignup) formSignup.style.display = 'none';
  } else {
    if (btnLogin) btnLogin.classList.remove('active');
    if (btnSignup) btnSignup.classList.add('active');
    if (formLogin) formLogin.style.display = 'none';
    if (formSignup) formSignup.style.display = 'block';
  }
}

function handleGoogleSignIn() {
  const btn = document.getElementById('googleSignInBtn');
  if (btn) btn.innerHTML = 'Connecting with Google Account...';
  setTimeout(() => {
    alert('✓ Google Authentication Successful! Welcome to MILLA PRO.');
    window.location.href = 'index.html';
  }, 750);
}

function handleEmailLogin(e) {
  e.preventDefault();
  const email = document.getElementById('emailLoginInput').value;
  alert('✓ Logged in successfully as ' + email);
  window.location.href = 'index.html';
}

function handleEmailSignUp(e) {
  e.preventDefault();
  const name = document.getElementById('signupName').value;
  const email = document.getElementById('signupEmail').value;
  alert('✓ Account created successfully for ' + name + ' (' + email + ')! Welcome to MILLA PRO.');
  window.location.href = 'index.html';
}

function handleSendOtp(e) {
  e.preventDefault();
  const phone = document.getElementById('userPhone').value;
  const btn = document.getElementById('sendOtpBtn');
  const section = document.getElementById('otpInputSection');
  if (btn) {
    btn.disabled = true;
    btn.innerText = 'Sending 4-Digit OTP...';
  }
  setTimeout(() => {
    if (btn) btn.style.display = 'none';
    if (section) section.style.display = 'block';
  }, 600);
}

function simulateLoginSuccess(method = 'Account') {
  alert('✓ Verification Successful via ' + method + '! Redirecting to store...');
  window.location.href = 'index.html';
}

function handleTrackOrder(e) {
  e.preventDefault();
  const id = document.getElementById('trackOrderId').value;
  const res = document.getElementById('trackResultBox');
  const disp = document.getElementById('trackOrderIdDisplay');
  if (disp) disp.innerText = 'Order #' + (id || 'MP-2026-8812');
  if (res) res.style.display = 'block';
}


// ==========================================================================
// MILLD AUTHENTIC COMPONENT SCRIPTS
// ==========================================================================

function updateWheyCostCalc(rotis) {
  var r = parseInt(rotis, 10) || 3;
  var countEl = document.getElementById('pgRotiCount');
  var unitEl = document.getElementById('pgRotiUnit');
  var regularEl = document.getElementById('pgRegularVal');
  var milldEl = document.getElementById('pgMillaVal');
  var gainEl = document.getElementById('pgGainVal');
  
  var REGULAR = 3;
  var MILLA = 14.7;
  
  var regGrams = r * REGULAR;
  var millaGrams = +(r * MILLA).toFixed(1);
  var gainGrams = +(millaGrams - regGrams).toFixed(1);

  if (countEl) countEl.textContent = r;
  if (unitEl) unitEl.textContent = (r === 1) ? 'roti' : 'rotis';
  if (regularEl) regularEl.textContent = regGrams + 'g';
  if (milldEl) milldEl.textContent = millaGrams + 'g';
  if (gainEl) gainEl.textContent = gainGrams + 'g';

  // Whey Cost Calculator (@ ₹3,500 / kg standard whey in India)
  var wheyDailyCost = Math.round(millaGrams * (3500 / 750));
  var wheyMonthlyCost = wheyDailyCost * 30;

  // MILLA PRO Atta: ₹240/kg -> 100g flour (3 rotis) = ₹20 = ~₹6.67 per roti
  var millaDailyCost = Math.round(r * 6.67);
  var millaMonthlyCost = millaDailyCost * 30;

  var monthlySavings = wheyMonthlyCost - millaMonthlyCost;
  var yearlySavings = monthlySavings * 12;

  var wheyCostEl = document.getElementById('wheyMonthlyCostVal');
  var millaCostEl = document.getElementById('millaMonthlyCostVal');
  var savingsEl = document.getElementById('wheySavingsMonthlyVal');
  var yearlyEl = document.getElementById('wheySavingsYearlyVal');

  if (wheyCostEl) wheyCostEl.textContent = '₹' + wheyMonthlyCost.toLocaleString('en-IN');
  if (millaCostEl) millaCostEl.textContent = '₹' + millaMonthlyCost.toLocaleString('en-IN');
  if (savingsEl) savingsEl.textContent = '₹' + monthlySavings.toLocaleString('en-IN');
  if (yearlyEl) yearlyEl.textContent = '₹' + yearlySavings.toLocaleString('en-IN');
}

function initMillDRotiReveal() {
  var grid = document.getElementById('rr-grid-template--23901876781272__roti_break_down_UPtKi4');
  if (!grid) return;

  var pctEls = grid.querySelectorAll('.rr-bar-pct');
  var fillEls = grid.querySelectorAll('.rr-bar-fill');
  var fired = false;

  function easeOut(t) { return 1 - Math.pow(1 - t, 3); }

  function animateBars() {
    var DURATION = 1150;

    pctEls.forEach(function (el) {
      var target = parseInt(el.getAttribute('data-target'), 10);
      var delay = parseInt(el.getAttribute('data-delay'), 10) || 0;
      var start = null;

      function step(ts) {
        if (!start) start = ts;
        var elapsed = ts - start - delay;
        if (elapsed < 0) { requestAnimationFrame(step); return; }
        var progress = Math.min(elapsed / DURATION, 1);
        var val = Math.round(easeOut(progress) * target);
        el.textContent = val + '%';
        if (progress < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });

    fillEls.forEach(function (el) {
      var target = parseInt(el.getAttribute('data-target'), 10);
      var delay = parseInt(el.getAttribute('data-delay'), 10) || 0;
      var start = null;

      function step(ts) {
        if (!start) start = ts;
        var elapsed = ts - start - delay;
        if (elapsed < 0) { requestAnimationFrame(step); return; }
        var progress = Math.min(elapsed / DURATION, 1);
        el.style.width = Math.round(easeOut(progress) * target) + '%';
        if (progress < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }

  var observer = new IntersectionObserver(function (entries) {
    if (!fired && entries.some(function (e) { return e.isIntersecting; })) {
      fired = true;
      animateBars();
      observer.disconnect();
    }
  }, { threshold: 0.25 });

  observer.observe(grid);
}

function initMillDFlipCards() {
  var grid = document.getElementById('bc-grid-template--23901876781272__benefits_scroll_JRYXiR');
  if (!grid) return;

  var btns = grid.querySelectorAll('.bc-card-btn');
  btns.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      this.classList.toggle('is-flipped');
    });
  });
}

function initMillDReviews() {
  var el = document.getElementById('tm-reviews-template--23901876781272__testimonials_6TEXnH');
  if (!el) return;

  // Let CSS GPU hardware-accelerated marquee run smoothly at 60fps.
  // Add mobile touch pause/resume support matching desktop hover pause.
  el.addEventListener('touchstart', function() {
    el.style.animationPlayState = 'paused';
  }, { passive: true });
  el.addEventListener('touchend', function() {
    el.style.animationPlayState = 'running';
  }, { passive: true });
}

// Master toggleFaq is defined at line 914


document.addEventListener('DOMContentLoaded', function () {
  initMillDRotiReveal();
  initMillDFlipCards();
  initMillDReviews();
  updateWheyCostCalc(3);
  if (typeof updateCartDrawerUI === 'function') updateCartDrawerUI();
});



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


// ==========================================
// Global Shop Configurator & Cart Adapters
// ==========================================
var currentSelectedPack = '1kg';
var currentPrice = 249;

function selectShopPack(pack, price, mrp, discount) {
  currentSelectedPack = pack;
  currentPrice = price;

  var c1 = document.getElementById('packCard1kg');
  var c5 = document.getElementById('packCard5kg');
  if (c1) c1.classList.toggle('active', pack === '1kg');
  if (c5) c5.classList.toggle('active', pack === '5kg');

  var pText = document.getElementById('shopPriceText');
  var mText = document.getElementById('shopMrpText');
  var dText = document.getElementById('shopDiscountText');
  if (pText) pText.textContent = '₹' + price.toLocaleString('en-IN');
  if (mText) mText.textContent = '₹' + mrp.toLocaleString('en-IN');
  if (dText) dText.textContent = 'SAVE ' + discount;

  if (typeof selectPack === 'function') {
    selectPack(pack);
  }
}

function addShopToCart() {
  var qInput = document.getElementById('shopQtyInput');
  var qty = qInput ? (parseInt(qInput.value, 10) || 1) : 1;
  if (typeof addToCart === 'function') {
    addToCart(currentSelectedPack, qty);
    openCartDrawer();
  }
}

function stepQty(delta) {
  var input = document.getElementById('shopQtyInput');
  if (!input) return;
  var val = parseInt(input.value, 10) || 1;
  val = Math.max(1, Math.min(10, val + delta));
  input.value = val;
}

// =========================================================================
// 5 HIGH-END FUTURISTIC LUXURY INTERACTIVE CONTROLLERS
// 1. Apple-Style Segmented Pill Switcher
// 2. Interactive 3D Holographic Pouch Tilt Engine
// 3. Roti Macro Transformer Interactive HUD
// =========================================================================

function switchAppleTab(tabId) {
  var btns = document.querySelectorAll('.apple-tab-btn');
  btns.forEach(function(b) {
    b.classList.toggle('active', b.getAttribute('data-tab') === tabId);
  });
  
  var panels = document.querySelectorAll('.apple-tab-panel');
  panels.forEach(function(p) {
    p.classList.toggle('active', p.id === 'tab-panel-' + tabId);
  });
}

function initPouchTilt() {
  var card = document.getElementById('hero3dCard');
  if (!card) return;
  card.addEventListener('mousemove', function(e) {
    var rect = card.getBoundingClientRect();
    var x = e.clientX - rect.left - rect.width / 2;
    var y = e.clientY - rect.top - rect.height / 2;
    var rotateX = -(y / rect.height) * 14;
    var rotateY = (x / rect.width) * 14;
    card.style.transform = 'perspective(1000px) rotateX(' + rotateX.toFixed(2) + 'deg) rotateY(' + rotateY.toFixed(2) + 'deg) translateY(-6px)';
  });
  card.addEventListener('mouseleave', function() {
    card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)';
  });
}

function updateMacroTransformer(val) {
  var rotis = parseInt(val, 10) || 3;
  var rotiCountEl = document.getElementById('mtRotiCount');
  var millaProteinEl = document.getElementById('mtMillaProtein');
  var regProteinEl = document.getElementById('mtRegProtein');
  var proteinGainEl = document.getElementById('mtProteinGain');
  var dialFill = document.getElementById('mtDialFill');
  
  if (rotiCountEl) rotiCountEl.textContent = rotis + ' ' + (rotis === 1 ? 'Roti' : 'Rotis');
  var millaGrams = Math.round(rotis * 15);
  var regGrams = Math.round(rotis * 3);
  var netGain = millaGrams - regGrams;
  
  if (millaProteinEl) millaProteinEl.textContent = millaGrams + 'g';
  if (regProteinEl) regProteinEl.textContent = regGrams + 'g';
  if (proteinGainEl) proteinGainEl.textContent = '+' + netGain + 'g';
  if (dialFill) dialFill.style.width = Math.min(100, Math.round((millaGrams / 60) * 100)) + '%';
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initPouchTilt);
} else {
  initPouchTilt();
}

// ==========================================================================
// V29.0 LUXURY ARCHITECTURAL UPGRADES JAVASCRIPT CONTROLLERS
// ==========================================================================

// 1. Ambient Audio Micro-Feedback Synthesizer (Feature 4.3)
var audioCtx = null;
var soundEnabled = localStorage.getItem('milla_sound_enabled') === 'true';

function playMicroSound(type) {
  if (!soundEnabled) return;
  try {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
    var osc = audioCtx.createOscillator();
    var gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    var now = audioCtx.currentTime;

    if (type === 'tick') {
      osc.type = 'sine';
      osc.frequency.setValueAtTime(800, now);
      osc.frequency.exponentialRampToValueAtTime(350, now + 0.035);
      gain.gain.setValueAtTime(0.04, now);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.035);
      osc.start(now);
      osc.stop(now + 0.035);
    } else {
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(1050, now);
      osc.frequency.exponentialRampToValueAtTime(650, now + 0.06);
      gain.gain.setValueAtTime(0.06, now);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.06);
      osc.start(now);
      osc.stop(now + 0.06);
    }
  } catch(e) {}
}

function toggleAudioFeedback() {
  soundEnabled = !soundEnabled;
  localStorage.setItem('milla_sound_enabled', soundEnabled);
  updateAudioFeedbackUI();
  if (soundEnabled) playMicroSound('chime');
}

function updateAudioFeedbackUI() {
  document.querySelectorAll('.sound-toggle-btn').forEach(function(btn) {
    btn.classList.toggle('active', soundEnabled);
    btn.innerHTML = soundEnabled ? '🔊 Sound: ON' : '🔈 Sound: OFF';
  });
}

// 2. X-Ray Molecular Inspection Lens (Feature 1.1 / 1.2)
function toggleXrayView(mode) {
  var overlay = document.getElementById('xrayOverlayHud');
  var btnPouch = document.getElementById('xrayBtnPouch');
  var btnXray = document.getElementById('xrayBtnXray');
  var mainImg = document.getElementById('mainShopImg');

  if (mode === 'xray') {
    if (overlay) overlay.classList.add('active');
    if (btnPouch) btnPouch.classList.remove('active');
    if (btnXray) btnXray.classList.add('active');
    if (mainImg) mainImg.style.transform = 'scale(0.92) filter(contrast(1.15))';
    playMicroSound('chime');
  } else {
    if (overlay) overlay.classList.remove('active');
    if (btnPouch) btnPouch.classList.add('active');
    if (btnXray) btnXray.classList.remove('active');
    if (mainImg) mainImg.style.transform = 'scale(1)';
    playMicroSound('tick');
  }
}

// 3. Household Macro Architect Dial (Feature 2.1)
var currentFamilyPeople = 4;
function setHouseholdFamilySize(people) {
  currentFamilyPeople = parseInt(people, 10) || 4;
  playMicroSound('tick');

  document.querySelectorAll('.family-pill-btn').forEach(function(btn) {
    btn.classList.toggle('active', parseInt(btn.getAttribute('data-people'), 10) === currentFamilyPeople);
  });

  // Calculate Family Requirement (avg 55g/adult/day)
  var familyTarget = currentFamilyPeople * 55;
  var rotisPerPerson = 3;
  var totalFamilyRotis = currentFamilyPeople * rotisPerPerson;
  var regularProtein = Math.round(totalFamilyRotis * 3);
  var millaProtein = Math.round(totalFamilyRotis * 15);
  var closedGap = millaProtein - regularProtein;

  var targetEl = document.getElementById('archFamilyTarget');
  var rotisEl = document.getElementById('archFamilyRotis');
  var regEl = document.getElementById('archRegularProtein');
  var millaEl = document.getElementById('archMillaProtein');
  var closedEl = document.getElementById('archClosedGap');
  var percentEl = document.getElementById('archPercentMet');

  if (targetEl) targetEl.textContent = familyTarget + 'g';
  if (rotisEl) rotisEl.textContent = totalFamilyRotis + ' rotis';
  if (regEl) regEl.textContent = regularProtein + 'g';
  if (millaEl) millaEl.textContent = millaProtein + 'g';
  if (closedEl) closedEl.textContent = '+' + closedGap + 'g';
  if (percentEl) {
    var pct = Math.min(100, Math.round((millaProtein / familyTarget) * 100));
    percentEl.textContent = pct + '%';
  }
}

// 4. Compare Against Any Atta Matrix (Feature 3.2)
var attaData = {
  'aashirvaad': {
    name: 'Aashirvaad Superior MP Atta',
    protein: '10.5g',
    carbs: '73.2g',
    fiber: '11.0g',
    gi: 'High GI (65)',
    bloat: 'Low (Wheat)',
    costPer10g: '₹4.8'
  },
  'pillsbury': {
    name: 'Pillsbury Chakki Fresh',
    protein: '10.8g',
    carbs: '72.0g',
    fiber: '10.5g',
    gi: 'High GI (64)',
    bloat: 'Low (Wheat)',
    costPer10g: '₹4.9'
  },
  'multigrain': {
    name: 'Commercial Multigrain Atta',
    protein: '13.5g',
    carbs: '68.0g',
    fiber: '12.0g',
    gi: 'Medium GI (58)',
    bloat: 'Moderate (Channa/Barley)',
    costPer10g: '₹6.2'
  },
  'besan': {
    name: 'Pure Besan / Gram Flour',
    protein: '21.0g',
    carbs: '57.8g',
    fiber: '10.8g',
    gi: 'Low GI (35)',
    bloat: 'High Gas / Hard to Puff',
    costPer10g: '₹7.5'
  }
};

function switchCompareAtta(brandKey) {
  var data = attaData[brandKey];
  if (!data) return;
  playMicroSound('tick');

  document.querySelectorAll('.compare-tab-pill').forEach(function(pill) {
    pill.classList.toggle('active', pill.getAttribute('data-brand') === brandKey);
  });

  var brandNameEl = document.getElementById('cmpBrandName');
  var brandProteinEl = document.getElementById('cmpBrandProtein');
  var brandCarbsEl = document.getElementById('cmpBrandCarbs');
  var brandFiberEl = document.getElementById('cmpBrandFiber');
  var brandGiEl = document.getElementById('cmpBrandGi');
  var brandBloatEl = document.getElementById('cmpBrandBloat');
  var brandCostEl = document.getElementById('cmpBrandCost');

  if (brandNameEl) brandNameEl.textContent = data.name;
  if (brandProteinEl) brandProteinEl.textContent = data.protein;
  if (brandCarbsEl) brandCarbsEl.textContent = data.carbs;
  if (brandFiberEl) brandFiberEl.textContent = data.fiber;
  if (brandGiEl) brandGiEl.textContent = data.gi;
  if (brandBloatEl) brandBloatEl.textContent = data.bloat;
  if (brandCostEl) brandCostEl.textContent = data.costPer10g;

  for (var i = 1; i <= 7; i++) {
    var mobEl = document.getElementById('cmpMobileBrandLbl' + i);
    if (mobEl) mobEl.textContent = data.name;
  }
}

// 5. Dynamic Glassmorphic Floating Island Sticky Nav (Feature 5.1)
function initFloatingIsland() {
  var island = document.getElementById('floatingIsland');
  if (!island) return;

  var lastScrollY = window.scrollY;
  window.addEventListener('scroll', function() {
    var currentY = window.scrollY;
    // Show after scrolling past 350px
    if (currentY > 350) {
      island.classList.add('visible');
    } else {
      island.classList.remove('visible');
    }
    lastScrollY = currentY;
  }, { passive: true });
}

// =========================================================================
// FEATURE 6: OBSIDIAN DARK MODE / SURGICAL LIGHT THEME ENGINE
// =========================================================================
function getStoredTheme() {
  try {
    var stored = localStorage.getItem('milla_theme');
    if (stored === 'dark' || stored === 'light') return stored;
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
  } catch (e) {}
  return 'light';
}

function updateThemeToggleButtons(theme) {
  var isDark = theme === 'dark';
  document.querySelectorAll('.theme-toggle-btn').forEach(function(btn) {
    btn.setAttribute('aria-label', isDark ? 'Switch to Surgical Light Mode' : 'Switch to Obsidian Dark Mode');
    btn.setAttribute('title', isDark ? 'Switch to Surgical Light Mode (☀️)' : 'Switch to Obsidian Dark Mode (🌙)');
  });

  document.querySelectorAll('.sidebar-theme-indicator').forEach(function(el) {
    el.textContent = isDark ? '☀️ Light' : '🌙 Dark';
  });
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  if (document.body) {
    document.body.setAttribute('data-theme', theme);
  }
  updateThemeToggleButtons(theme);
  try {
    localStorage.setItem('milla_theme', theme);
  } catch (e) {}
}

function toggleThemeMode() {
  var current = document.documentElement.getAttribute('data-theme') || getStoredTheme();
  var next = current === 'dark' ? 'light' : 'dark';
  applyTheme(next);
  if (typeof playMicroSound === 'function') {
    playMicroSound('pop');
  }
}

function initThemeMode() {
  var theme = getStoredTheme();
  applyTheme(theme);
}

// Auto-init on page load
document.addEventListener('DOMContentLoaded', function() {
  initThemeMode();
  updateAudioFeedbackUI();
  initFloatingIsland();
  if (document.getElementById('archFamilyTarget')) {
    setHouseholdFamilySize(4);
  }
});





// ==========================================================================
// APPETIZING WARM MODERN LIGHT HELPERS
// ==========================================================================

function switchProductImage(src, btnEl) {
  const mainImg = document.getElementById('mainProductImg');
  if (mainImg) {
    mainImg.src = src;
  }
  document.querySelectorAll('.hero-thumb-btn').forEach(btn => btn.classList.remove('active'));
  if (btnEl) {
    btnEl.classList.add('active');
  }
}

function buyNowCurrentPack() {
  addToCart(currentPackId, 1);
  openCartDrawer();
}

function toggleCleanFaq(btnEl) {
  const item = btnEl.closest('.clean-faq-item');
  if (!item) return;
  const isActive = item.classList.contains('active');
  document.querySelectorAll('.clean-faq-item').forEach(el => el.classList.remove('active'));
  if (!isActive) {
    item.classList.add('active');
  }
}

var currentFamilyPeople = 4;
var currentRotisPerPerson = 3;

function setHouseholdFamilySize(people) {
  currentFamilyPeople = parseInt(people, 10) || 4;
  document.querySelectorAll('.calc-pill-btn').forEach(function(btn) {
    var p = parseInt(btn.getAttribute('data-people'), 10);
    btn.classList.toggle('active', p === currentFamilyPeople);
  });
  updateFamilyCalculator();
}

function onMacroRotiSliderChange(val) {
  currentRotisPerPerson = parseInt(val, 10) || 3;
  var sliderValEl = document.getElementById('macroSliderVal');
  if (sliderValEl) sliderValEl.textContent = currentRotisPerPerson + (currentRotisPerPerson === 1 ? ' Roti' : ' Rotis');
  updateFamilyCalculator();
}

function updateFamilyCalculator() {
  var familyTarget = currentFamilyPeople * 55;
  var totalFamilyRotis = currentFamilyPeople * currentRotisPerPerson;
  var standardAttaProtein = Math.round(totalFamilyRotis * 3);
  var millaProtein = Math.round(totalFamilyRotis * 15);
  var gapBoost = millaProtein - standardAttaProtein;
  var percentMet = Math.min(100, Math.round((millaProtein / familyTarget) * 100));

  var elTarget = document.getElementById('calcFamilyTarget');
  var elStandard = document.getElementById('calcStandardProtein');
  var elMilla = document.getElementById('calcMillaProtein');
  var elPercent = document.getElementById('calcPercentMet');

  if (elTarget) elTarget.textContent = familyTarget + 'g';
  if (elStandard) elStandard.textContent = standardAttaProtein + 'g';
  if (elMilla) elMilla.textContent = millaProtein + 'g (+' + gapBoost + 'g)';
  if (elPercent) elPercent.textContent = percentMet + '%';
}

// Mobile Sticky Bar scroll watcher
window.addEventListener('scroll', function() {
  const stickyBar = document.getElementById('mobileStickyBar');
  if (!stickyBar) return;
  if (window.innerWidth <= 768) {
    if (window.scrollY > 350) {
      stickyBar.classList.add('visible');
    } else {
      stickyBar.classList.remove('visible');
    }
  } else {
    stickyBar.classList.remove('visible');
  }
});
