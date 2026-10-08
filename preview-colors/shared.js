// Scroll reveal — respects reduced motion via CSS fallback
(function () {
  var els = document.querySelectorAll('.rv:not(.in)');
  if (!('IntersectionObserver' in window)) {
    els.forEach(function (e) { e.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.16 });
  els.forEach(function (e) { io.observe(e); });
})();
