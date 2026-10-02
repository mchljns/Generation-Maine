const topbar = document.getElementById('topbar');
const menuButton = document.querySelector('.menu-button');
const mobileNav = document.getElementById('mobile-nav');

function updateBar() {
  topbar.classList.toggle('scrolled', window.scrollY > 16);
}

function setMenu(open) {
  mobileNav.hidden = !open;
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
}

updateBar();
addEventListener('scroll', updateBar, { passive: true });
menuButton.addEventListener('click', () => setMenu(mobileNav.hidden));
mobileNav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false)));
addEventListener('keydown', event => { if (event.key === 'Escape') setMenu(false); });
addEventListener('click', event => { if (!mobileNav.hidden && !mobileNav.contains(event.target) && !menuButton.contains(event.target)) setMenu(false); });
