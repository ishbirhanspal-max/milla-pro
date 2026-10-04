
    var currentSelectedPack = '1kg';
    var currentPrice = 249;

    function switchShopThumb(imgSrc, btn) {
      document.getElementById('mainShopImg').src = imgSrc;
      document.querySelectorAll('.thumb-btn').forEach(function(b) { b.classList.remove('active'); });
      btn.classList.add('active');
    }

    function selectShopPack(pack, price, mrp, discount) {
      currentSelectedPack = pack;
      currentPrice = price;

      document.getElementById('packCard1kg').classList.toggle('active', pack === '1kg');
      document.getElementById('packCard5kg').classList.toggle('active', pack === '5kg');

      document.getElementById('shopPriceText').textContent = '₹' + price.toLocaleString('en-IN');
      document.getElementById('shopMrpText').textContent = '₹' + mrp.toLocaleString('en-IN');
      document.getElementById('shopDiscountText').textContent = 'SAVE ' + discount;

      // Update script.js?v=21.0 currentPackId if loaded
      if (typeof selectPack === 'function') {
        selectPack(pack);
      }
    }

    function stepQty(delta) {
      var input = document.getElementById('shopQtyInput');
      var val = parseInt(input.value, 10) || 1;
      val = Math.max(1, Math.min(10, val + delta));
      input.value = val;
      if (typeof currentQty !== 'undefined') {
        currentQty = val;
      }
    }

    function addShopToCart() {
      var qty = parseInt(document.getElementById('shopQtyInput').value, 10) || 1;
      if (typeof addToCart === 'function') {
        addToCart(currentSelectedPack, qty);
        openCartDrawer();
      } else {
        alert('Added ' + qty + ' × ' + currentSelectedPack.toUpperCase() + ' to cart!');
      }
    }

    function triggerShopCheckout() {
      var qty = parseInt(document.getElementById('shopQtyInput').value, 10) || 1;
      if (typeof addToCart === 'function' && typeof triggerRazorpayCheckout === 'function') {
        addToCart(currentSelectedPack, qty);
        triggerRazorpayCheckout();
      } else {
        window.location.href = 'login.html';
      }
    }

    function checkPin() {
      var pin = document.getElementById('pinInput').value.trim();
      var res = document.getElementById('pinResult');
      if (pin.length === 6 && /^\d+$/.test(pin)) {
        res.style.display = 'block';
        res.innerHTML = '✓ Pincode <strong>' + pin + '</strong> is serviceable. Delivery in 10–15 business days via Tracked Express Courier.';
      } else {
        res.style.display = 'block';
        res.style.color = '#C62828';
        res.innerHTML = '⚠ Please enter a valid 6-digit Indian Pincode.';
      }
    }

    function toggleShopAcc(btn) {
      var content = btn.nextElementSibling;
      var isOpen = content.classList.contains('open');
      document.querySelectorAll('.shop-acc-content').forEach(function(c) { c.classList.remove('open'); });
      document.querySelectorAll('.shop-acc-btn span:last-child').forEach(function(s) { s.textContent = '+'; });

      if (!isOpen) {
        content.classList.add('open');
        btn.querySelector('span:last-child').textContent = '−';
      }
    }
  