import { createRequire } from 'node:module'; const require = createRequire(import.meta.url);
import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: process.env.PROXY_SPKI ? ['--ignore-certificate-errors-spki-list=' + process.env.PROXY_SPKI] : [] });
const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
const t0 = Date.now(); const logs = []; p.on('console', m => logs.push(m.type() + ': ' + m.text().slice(0, 300))); p.on('pageerror', e => logs.push('pageerror: ' + e.message.slice(0, 300)));
await p.goto('https://mchljns.github.io/Generation-Maine/test/', { waitUntil: 'domcontentloaded', timeout: 120000 });
let ok = false, info = '';
for (let i = 0; i < 60; i++) {
  await p.waitForTimeout(5000);
  for (const f of p.frames()) {
    try {
      const r = await f.evaluate(() => ({ t: document.title, slides: document.querySelectorAll('.slide').length, clips: [...document.querySelectorAll('.clip')].map(c => c.getAttribute('data-src') || c.getAttribute('src') || '').filter(Boolean).length, h1: (document.querySelector('.hero h1') || {}).textContent || '' }));
      if (r.slides > 0 || /Generation Maine/.test(r.t)) { info = JSON.stringify(r); if (r.slides >= 9) ok = true; }
    } catch (e) {}
  }
  if (ok) break;
}
console.log(ok ? 'WORKS' : 'NOT YET', Math.round((Date.now() - t0) / 1000) + 's', p.url().slice(0, 80), info);
await p.screenshot({ path: (process.env.OUT || '.') + '/test-link.png' });
require('fs').writeFileSync(process.env.OUT ? process.env.OUT + '/console.txt' : 'console.txt', logs.join('\n')); await b.close();
