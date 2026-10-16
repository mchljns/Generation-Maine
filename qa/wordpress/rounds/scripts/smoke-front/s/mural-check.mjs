// The mural with and without the inline JSON (?exp=nojson): same paths, same delays, same "on" class; and console errors.
import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
for (const vp of [[1440, 900], [390, 844]]) for (const u of ['http://127.0.0.1:8508/?exp=0', 'http://127.0.0.1:8508/?exp=nojson']) {
  const p = await b.newPage({ viewport: { width: vp[0], height: vp[1] } }); const errs = [];
  p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto(u); await p.waitForTimeout(1500);
  const r = await p.evaluate(() => { const m = document.getElementById('mural'); const ps = [...m.querySelectorAll('g path')]; return { on: m.classList.contains('on'), paths: ps.length, delays: ps.map(x => x.style.transitionDelay).join(','), json: !!document.getElementById('maine-data') }; });
  console.log(vp[0], u.split('?')[1], JSON.stringify(r), 'errors', errs.length);
  await p.close();
}
await b.close();
