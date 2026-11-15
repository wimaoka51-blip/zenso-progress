// 動き（DESIGN.md 8章）：スクロールで見えた時のフェード、03 の窯の口の写真のせり上がり、ペン画のふっと出る、FV の読み込み。
// 動きを減らす設定・?still・自動の撮影では止める（JS が動かなければ全部見える）
(() => {
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches || location.search.includes('still') || navigator.webdriver;
  if (still || !('IntersectionObserver' in window)) return;
  document.documentElement.classList.add('js-motion');
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } }), {rootMargin: '0px 0px -10% 0px'});
  document.querySelectorAll('[data-in]').forEach((el, i) => { el.style.transitionDelay = (i % 3) * 0.12 + 's'; io.observe(el); });
  document.querySelectorAll('[data-reveal],[data-ink]').forEach(el => io.observe(el));
  requestAnimationFrame(() => document.documentElement.classList.add('is-loaded'));
})();
