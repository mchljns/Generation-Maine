// Phone menu, logged-in view, and console errors on the WordPress front page.
import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
const out = process.argv[2], url = 'http://127.0.0.1:8080/';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
// phone menu, logged out
{
  const p = await b.newPage({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(600);
  await p.tap('#menu'); await p.waitForTimeout(400);
  const m = await p.evaluate(() => { const s = document.getElementById('sheet'); const links = [...s.querySelectorAll('a')]; return { open: s.classList.contains('open'), expanded: document.getElementById('menu').getAttribute('aria-expanded'), inBar: !!s.closest('.top'), links: links.map(a => [a.textContent.trim(), a.getAttribute('href'), Math.round(a.getBoundingClientRect().height)]), visible: getComputedStyle(s).opacity }; });
  await p.screenshot({ path: `${out}/menu-390.png` });
  await p.tap('#sheet a[href="#creators"]'); await p.waitForTimeout(900);
  const after = await p.evaluate(() => ({ open: document.getElementById('sheet').classList.contains('open'), y: Math.round(document.getElementById('creators').getBoundingClientRect().top) }));
  console.log('menu', JSON.stringify(m), '| after link tap', JSON.stringify(after), '| errors', errs);
  await p.close();
}
// logged in: the admin bar, the bar under it, the setup note in place of the form
{
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8080/wp-login.php'); await p.fill('#user_login', 'admin'); await p.fill('#user_pass', 'adminpass'); await p.click('#wp-submit'); await p.waitForLoadState('networkidle');
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(600);
  await p.evaluate(() => scrollTo(0, 1500)); await p.waitForTimeout(500);
  const r = await p.evaluate(() => ({ adminbar: !!document.getElementById('wpadminbar'), barTop: Math.round(document.querySelector('.top').getBoundingClientRect().top), adminH: Math.round((document.getElementById('wpadminbar') || { offsetHeight: 0 }).offsetHeight), note: (document.querySelector('.gm-newsletter-missing') || {}).textContent || null, form: !!document.getElementById('nl') }));
  await p.screenshot({ path: `${out}/admin-1440.png` });
  console.log('logged in', JSON.stringify(r), '| errors', errs);
  await ctx.storageState({ path: `${out}/auth.json` });
  await ctx.close();
}
await b.close();
