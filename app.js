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

  /* ---------- keyboard access for every tooltip ---------- */
  function wireTips() {
    document.querySelectorAll("[data-tip]").forEach(function (el) {
      if (!el.hasAttribute("tabindex") && !el.matches("a,button,input,select,textarea")) {
        el.setAttribute("tabindex", "0");
      }
      if (!el.hasAttribute("role")) el.setAttribute("role", "note");
    });
  }

  function init() { wireToggle(); wireReveal(); wireTips(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
