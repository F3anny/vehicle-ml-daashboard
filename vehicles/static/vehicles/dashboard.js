document.getElementById('export-button').addEventListener('click', () => {
  const params = new URLSearchParams(window.location.search);
  params.set('export', 'csv');
  window.location.assign(`?${params.toString()}`);
});
const sections = document.querySelectorAll('section[id], article[id]');
const links = document.querySelectorAll('#dashboard-nav a');
const observer = new IntersectionObserver(entries => {
  const visible = entries.filter(entry => entry.isIntersecting);
  if (!visible.length) return;
  links.forEach(link => link.classList.toggle('active', link.hash === `#${visible[0].target.id}`));
}, { rootMargin: '-10% 0px -65% 0px', threshold: 0 });
sections.forEach(section => observer.observe(section));
