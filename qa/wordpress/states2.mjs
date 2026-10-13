import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
const [out, label, auth] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
for (const [w, h] of [[1440, 900], [390, 844]]) {
  const ctx = await b.newContext({ viewport: { width: w, height: h }, isMobile: w < 900, hasTouch: w < 900, ...(auth ? { storageState: auth } : {}) });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('http://127.0.0.1:8080/', { waitUntil: 'networkidle' }); await p.waitForTimeout(700);
  const s = await p.evaluate(() => ({ stories: !!document.getElementById('stories'), empty: (document.querySelector('.gm-empty p') || {}).textContent || null, form: !!document.getElementById('nl'), note: (document.querySelector('.gm-newsletter-missing') || {}).textContent || null,
    rows: [...document.querySelectorAll('.follow .row')].map(r => r.tagName.toLowerCase() + ':' + r.querySelector('.h').textContent + (r.href ? ' -> ' + r.href.replace(/\?.*/, '') : '')),
    clips: [...document.querySelectorAll('#stage .clip')].slice(0, 3).map(c => c.tagName.toLowerCase() + (c.getAttribute('src') ? ' loaded' : ' waiting')) }));
  if (s.stories) { await p.evaluate(() => { const st = document.getElementById('stories'); scrollTo(0, st.offsetTop + 10); }); await p.waitForTimeout(1500);
    s.playing = await p.evaluate(() => [...document.querySelectorAll('video.clip')].filter(v => !v.paused && v.currentTime > 0).map(v => (v.closest('.panel') ? 'panel' : v.closest('.slide') ? 'slide' : 'stage') + ' ' + v.dataset.src.split('/').pop())); }
  await p.screenshot({ path: `${out}/${label}-${w}.png` });
  console.log(label, w, JSON.stringify(s), 'errors', JSON.stringify(errs));
  await ctx.close();
}
await b.close();
