// === SCRIPT 87 ===
(function () {
    var calc   = document.getElementById('pg-calc-template--23901876781272__protein_gap_fnpWcK');
    if (!calc) return;

    var slider     = calc.querySelector('.pg-roti-slider');
    var countEl    = calc.querySelector('.pg-roti-count');
    var regularEl  = calc.querySelector('.pg-regular-val');
    var milldEl    = calc.querySelector('.pg-milld-val');
    var gainEl     = calc.querySelector('.pg-gain-val');
    var unitEl     = calc.querySelector('.pg-slider-unit');

    var REGULAR = 4;   /* protein grams per roti — regular atta */
    var MILLD   = 15.333;  /* protein grams per roti — MillD atta   */

    function update() {
      var r  = parseInt(slider.value, 10);

      var re = r * REGULAR;
      var mi = Math.round(r * MILLD);

      countEl.textContent   = r;
      regularEl.textContent = re + 'g';
      milldEl.textContent   = mi + 'g';
      gainEl.textContent    = Math.round(mi - re) + 'g';
      if (unitEl) unitEl.textContent = (r === 1) ? 'roti' : 'rotis';
    }

    slider.addEventListener('input', update);
    update();
  })();

// === SCRIPT 88 ===
(function () {
    var grid = document.getElementById('rr-grid-template--23901876781272__roti_break_down_UPtKi4');
    if (!grid) return;

    var pctEls  = grid.querySelectorAll('.rr-bar-pct');
    var fillEls = grid.querySelectorAll('.rr-bar-fill');
    var fired   = false;

    function easeOut(t) { return 1 - Math.pow(1 - t, 3); }

    function animateBars() {
      var DURATION = 1150;

      pctEls.forEach(function (el) {
        var target = parseInt(el.getAttribute('data-target'), 10);
        var delay  = parseInt(el.getAttribute('data-delay'),  10);
        var start  = null;

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
        var delay  = parseInt(el.getAttribute('data-delay'),  10);
        var start  = null;

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
    }, { threshold: 0.3 });

    observer.observe(grid);
  })();

// === SCRIPT 89 ===
(function () {
    var grid = document.getElementById('bc-grid-template--23901876781272__benefits_scroll_JRYXiR');
    if (!grid) return;

    var cards  = grid.querySelectorAll('.bc-card-outer');
    var btns   = grid.querySelectorAll('.bc-card-btn');
    var fired  = false;
    var canHover = window.matchMedia('(hover: hover)').matches;

    /* ── Entry animation ── */
    var observer = new IntersectionObserver(function (entries) {
      if (!fired && entries.some(function (e) { return e.isIntersecting; })) {
        fired = true;
        cards.forEach(function (el) { el.classList.add('is-shown'); });
        observer.disconnect();
      }
    }, { threshold: 0.12 });
    observer.observe(grid);

    /* ── Flip behaviour ── */
    btns.forEach(function (btn) {
      if (canHover) {
        btn.addEventListener('mouseenter', function () { btn.classList.add('is-flipped'); });
        btn.addEventListener('mouseleave', function () { btn.classList.remove('is-flipped'); });
      } else {
        btn.addEventListener('click', function () { btn.classList.toggle('is-flipped'); });
      }
    });
  })();

// === SCRIPT 90 ===
(function () {
    function initAutoScroll(el, pxPerSec) {
      if (!el) return { pause: function(){}, resume: function(){} };
      var raf = 0, last = 0, paused = false, initialized = false, pauseTimer = null;
      var lockedByVideo = false;                      // held paused while a video plays
      var dragging = false, startX = 0, startLeft = 0;

      function tick(now) {
        var half = el.scrollWidth / 2;
        if (half > 0) {
          if (!initialized) {
            if (pxPerSec < 0) el.scrollLeft = half;
            initialized = true;
          }
          if (!paused) {
            if (!last) last = now;
            el.scrollLeft += (pxPerSec * (now - last)) / 1000;
            last = now;
            if (pxPerSec > 0 && el.scrollLeft >= half) el.scrollLeft -= half;
            if (pxPerSec < 0 && el.scrollLeft <= 0)  el.scrollLeft += half;
          } else {
            last = 0;
          }
        }
        raf = requestAnimationFrame(tick);
      }

      function scheduleResume() {
        if (lockedByVideo) return;            // don't auto-resume while video is playing
        if (pauseTimer) clearTimeout(pauseTimer);
        pauseTimer = setTimeout(function () { paused = false; }, 1500);
      }

      // ── Drag-to-scroll (mouse) ──
      el.addEventListener('pointerdown', function (e) {
        if (e.button !== 0) return;
        dragging  = true;
        paused    = true;
        startX    = e.clientX;
        startLeft = el.scrollLeft;
        el.setPointerCapture(e.pointerId);
        el.classList.add('is-dragging');
        if (pauseTimer) clearTimeout(pauseTimer);
      });

      el.addEventListener('pointermove', function (e) {
        if (!dragging) return;
        el.scrollLeft = startLeft - (e.clientX - startX);
      });

      function endDrag(e) {
        if (!dragging) return;
        dragging = false;
        el.classList.remove('is-dragging');
        try { el.releasePointerCapture(e.pointerId); } catch (_) {}
        scheduleResume();
      }

      el.addEventListener('pointerup',     endDrag);
      el.addEventListener('pointercancel', endDrag);

      // ── Touch ──
      el.addEventListener('touchstart', function () {
        if (!dragging) { paused = true; if (pauseTimer) clearTimeout(pauseTimer); }
      }, { passive: true });
      el.addEventListener('touchend',    function () { if (!dragging) scheduleResume(); });
      el.addEventListener('touchcancel', function () { if (!dragging) scheduleResume(); });

      // ── Mouse wheel ──
      el.addEventListener('wheel', function () { paused = true; scheduleResume(); }, { passive: true });

      raf = requestAnimationFrame(tick);

      // Return controls so mute logic can lock/unlock scrolling
      return {
        pause:  function () { lockedByVideo = true;  paused = true;  if (pauseTimer) clearTimeout(pauseTimer); },
        resume: function () { lockedByVideo = false; paused = false; }
      };
    }

    var reelsScroller   = initAutoScroll(document.getElementById('tm-reels-template--23901876781272__testimonials_6TEXnH'),    90);
    var reviewsScroller = initAutoScroll(document.getElementById('tm-reviews-template--23901876781272__testimonials_6TEXnH'), -80);

    // ── Mute / unmute — exclusive: unmuting one mutes all others ──
    document.querySelectorAll('.tm-reel-mute-btn').forEach(function (btn) {

      // Stop pointerdown from reaching the scroll container so setPointerCapture
      // never steals pointer events away from this button.
      btn.addEventListener('pointerdown', function (e) {
        e.stopPropagation();
      });

      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var isMuted = btn.getAttribute('data-muted') === 'true';

        if (isMuted) {
          // Unmuting this reel — first mute every other reel
          document.querySelectorAll('.tm-reel-mute-btn').forEach(function (other) {
            if (other === btn) return;
            other.setAttribute('data-muted', 'true');
            other.setAttribute('aria-label', 'Unmute');
            var vid = other.closest('.tm-reel').querySelector('.tm-reel-video');
            if (vid) vid.muted = true;
          });
          // Now unmute this one + stop reels auto-scroll while video plays
          btn.setAttribute('data-muted', 'false');
          btn.setAttribute('aria-label', 'Mute');
          var thisVid = btn.closest('.tm-reel').querySelector('.tm-reel-video');
          if (thisVid) { thisVid.muted = false; thisVid.play(); }
          if (reelsScroller) reelsScroller.pause();
        } else {
          // Muting this reel + resume auto-scroll
          btn.setAttribute('data-muted', 'true');
          btn.setAttribute('aria-label', 'Unmute');
          var thisVid = btn.closest('.tm-reel').querySelector('.tm-reel-video');
          if (thisVid) thisVid.muted = true;
          if (reelsScroller) reelsScroller.resume();
        }
      });
    });

    // ── Video lightbox — click a reel to pop its video up ──
    (function () {
      var section = document.getElementById('tm-section-template--23901876781272__testimonials_6TEXnH');
      var modal   = document.getElementById('tm-modal-template--23901876781272__testimonials_6TEXnH');
      if (!section || !modal) return;

      var wrap  = modal.querySelector('.tm-modal-video-wrap');
      var downX = 0, downY = 0, moved = false;

      function onKey(e) { if (e.key === 'Escape') closeModal(); }

      function closeModal() {
        modal.classList.remove('is-open');
        modal.setAttribute('aria-hidden', 'true');
        wrap.innerHTML = '';                     // stops & removes the cloned video
        if (reelsScroller) reelsScroller.resume();
        document.removeEventListener('keydown', onKey);
      }

      function openModal(srcVideo) {
        if (!srcVideo) return;
        var clone = srcVideo.cloneNode(true);    // keeps the <source> children
        clone.className = '';
        clone.removeAttribute('style');
        clone.muted    = false;
        clone.controls = true;
        clone.loop     = true;
        clone.setAttribute('playsinline', '');

        wrap.innerHTML = '';
        wrap.appendChild(clone);
        modal.classList.add('is-open');
        modal.setAttribute('aria-hidden', 'false');
        if (reelsScroller) reelsScroller.pause();

        var p = clone.play();
        if (p && p.catch) p.catch(function () {});
        document.addEventListener('keydown', onKey);
      }

      // The scroll container captures the pointer, which redirects the `click`
      // event away from the reel — so resolve the tap from pointerup instead.
      var tracking = false;

      section.addEventListener('pointerdown', function (e) {
        tracking = true; moved = false;
        downX = e.clientX; downY = e.clientY;
      });
      section.addEventListener('pointermove', function (e) {
        if (tracking && (Math.abs(e.clientX - downX) > 8 || Math.abs(e.clientY - downY) > 8)) moved = true;
      });
      section.addEventListener('pointerup', function (e) {
        if (!tracking) return;
        tracking = false;
        if (moved) return;                                    // was a drag/swipe, not a tap

        var el = document.elementFromPoint(e.clientX, e.clientY);
        if (!el || el.closest('.tm-reel-mute-btn')) return;   // let the mute button do its thing
        var reel = el.closest('.tm-reel');
        if (!reel) return;
        var vid = reel.querySelector('.tm-reel-video') || reel.querySelector('video');
        openModal(vid);
      });

      modal.querySelectorAll('[data-tm-close]').forEach(function (el) {
        el.addEventListener('click', closeModal);
      });
    })();

    // ── Header scroll-reveal ──
    var tmSection = document.getElementById('tm-section-template--23901876781272__testimonials_6TEXnH');
    if (tmSection) {
      var tmHeader = tmSection.querySelector('.tm-header');
      if (tmHeader) {
        var io = new IntersectionObserver(function (entries) {
          if (entries[0].isIntersecting) {
            tmHeader.classList.add('tm-header--visible');
            io.disconnect();
          }
        }, { threshold: 0.2 });
        io.observe(tmHeader);
      }
    }
  })();

// === SCRIPT 91 ===
(function () {
    var list = document.getElementById('faq-list-template--23901876781272__faq_dFVNJy');
    if (!list) return;

    list.addEventListener('click', function (e) {
      var btn = e.target.closest('.faq-btn');
      if (!btn) return;

      var item = btn.closest('.faq-item');
      var isOpen = item.classList.contains('is-open');

      /* close all */
      list.querySelectorAll('.faq-item.is-open').forEach(function (el) {
        el.classList.remove('is-open');
        el.querySelector('.faq-btn').setAttribute('aria-expanded', 'false');
      });

      /* open clicked one (unless it was already open) */
      if (!isOpen) {
        item.classList.add('is-open');
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  })();

