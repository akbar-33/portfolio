/* Theme toggle, scroll reveal, animated funnel bars. No dependencies. */
(function () {
  "use strict";

  /* ---------- theme: dark is the default, choice is remembered ---------- */
  var root = document.documentElement;
  var KEY = "ak-theme";
  var stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) { /* private mode */ }
  if (stored === "light") root.setAttribute("data-theme", "light");

  function label(btn) {
    var light = root.getAttribute("data-theme") === "light";
    btn.setAttribute("aria-pressed", String(light));
    btn.setAttribute("aria-label", light ? "Switch to dark theme" : "Switch to light theme");
    var text = btn.querySelector(".label");
    if (text) text.textContent = light ? "Light" : "Dark";
  }

  function wireToggle() {
    var btn = document.querySelector(".theme-toggle");
    if (!btn) return;
    label(btn);
    btn.addEventListener("click", function () {
      var toLight = root.getAttribute("data-theme") !== "light";
      if (toLight) root.setAttribute("data-theme", "light");
      else root.removeAttribute("data-theme");
      try { localStorage.setItem(KEY, toLight ? "light" : "dark"); } catch (e) {}
      label(btn);
    });
  }

  /* ---------- scroll reveal, and funnel bars that grow on entry ---------- */
  function wireReveal() {
    var targets = document.querySelectorAll(".reveal, .visual");
    if (!("IntersectionObserver" in window)) {
      targets.forEach(function (el) { el.classList.add("is-in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-in");
        io.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    targets.forEach(function (el) { io.observe(el); });
  }

  /* ---------- tooltips ----------
     One floating node on <body>. The diagrams sit inside overflow-x:auto
     containers, which clip absolutely positioned children, so the tooltip
     cannot live inside them. Position is clamped to the viewport and flips
     below the target when there is no room above. */
  var tip = null, current = null;

  function ensureTip() {
    if (tip) return tip;
    tip = document.createElement("div");
    tip.className = "tip";
    tip.setAttribute("role", "tooltip");
    tip.id = "ak-tip";
    document.body.appendChild(tip);
    return tip;
  }

  function place(el) {
    var t = ensureTip();
    t.textContent = el.getAttribute("data-tip");
    t.style.maxWidth = "";           // let CSS decide, then measure
    t.classList.add("is-shown");

    var pad = 10;
    var r = el.getBoundingClientRect();
    var tr = t.getBoundingClientRect();
    var vw = document.documentElement.clientWidth;
    var vh = document.documentElement.clientHeight;

    // horizontal: centre on the target, then clamp inside the viewport
    var left = r.left + r.width / 2 - tr.width / 2;
    if (left < pad) left = pad;
    if (left + tr.width > vw - pad) left = Math.max(pad, vw - pad - tr.width);

    // vertical: above by default, below when the top would be cut off
    var top = r.top - tr.height - 8;
    if (top < pad) {
      top = r.bottom + 8;
      if (top + tr.height > vh - pad) top = Math.max(pad, vh - pad - tr.height);
    }

    t.style.left = Math.round(left) + "px";
    t.style.top = Math.round(top) + "px";
  }

  function show(el) {
    if (!el || !el.getAttribute("data-tip")) return;
    current = el;
    el.setAttribute("aria-describedby", "ak-tip");
    place(el);
  }

  function hide() {
    if (tip) tip.classList.remove("is-shown");
    if (current) current.removeAttribute("aria-describedby");
    current = null;
  }

  function wireTips() {
    var els = document.querySelectorAll("[data-tip]");
    els.forEach(function (el) {
      if (!el.hasAttribute("tabindex") && !el.matches("a,button,input,select,textarea")) {
        el.setAttribute("tabindex", "0");
      }
      el.addEventListener("mouseenter", function () { show(el); });
      el.addEventListener("mouseleave", hide);
      el.addEventListener("focus", function () { show(el); });
      el.addEventListener("blur", hide);
      // touch: no hover, so a tap toggles
      el.addEventListener("click", function (ev) {
        if (current === el) { hide(); return; }
        ev.stopPropagation();
        show(el);
      });
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") hide(); });
    document.addEventListener("click", function (e) {
      if (current && !current.contains(e.target)) hide();
    });
    // Follow the target on scroll rather than hiding: smooth scrolling keeps
    // firing events after the page settles, and hiding there makes the tooltip
    // feel broken. Drop it only once the target leaves the viewport.
    var queued = false;
    function reflow() {
      if (!current || queued) return;
      queued = true;
      requestAnimationFrame(function () {
        queued = false;
        if (!current) return;
        var r = current.getBoundingClientRect();
        var vh = document.documentElement.clientHeight;
        if (r.bottom < 0 || r.top > vh) { hide(); return; }
        place(current);
      });
    }
    window.addEventListener("scroll", reflow, { passive: true });
    window.addEventListener("resize", reflow);
    document.querySelectorAll(".visual").forEach(function (v) {
      v.addEventListener("scroll", reflow, { passive: true });
    });
  }

  function init() { wireToggle(); wireReveal(); wireTips(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
