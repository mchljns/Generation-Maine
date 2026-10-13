import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
const url = process.env.URL || 'file:///home/user/Generation-Maine/brand/identity/splash-lean-a/index.html', out = process.env.OUT || '.';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
for (const [w, h] of [[375, 667], [390, 844], [320, 568]]) {
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(url); await p.waitForTimeout(500);
  await p.evaluate(() => { document.documentElement.style.scrollBehavior = 'auto'; scrollTo(0, document.getElementById('creators').offsetTop - 56); }); await p.waitForTimeout(300);
  const y0 = await p.evaluate(() => scrollY);
  // nudge to card 2, then tap its clip
  await p.evaluate(() => document.getElementById('panels').scrollBy({ left: 200, behavior: 'auto' })); await p.waitForTimeout(600);
  await p.tap('.panel[data-i="1"] .pv'); await p.waitForTimeout(500);
  const o = await p.evaluate(() => { const v = document.getElementById('viewer'), fr = document.querySelector('.slide[data-i="1"] .fr').getBoundingClientRect(), cl = document.getElementById('vclose').getBoundingClientRect(); return { hidden: v.hidden, cls: v.className, vn: document.getElementById('vn').textContent, frame: [Math.round(fr.left), Math.round(fr.top), Math.round(fr.width), Math.round(fr.height)], ratio: (fr.width / fr.height).toFixed(3), close: [Math.round(cl.width), Math.round(cl.height)], focus: document.activeElement.id, locked: document.documentElement.classList.contains('vopen'), srcs: [...document.querySelectorAll('.slide img.clip')].map(i => i.src ? 1 : 0).join(''), docOverflow: document.documentElement.scrollWidth - innerWidth }; });
  console.log(`\n${w}x${h} open card 2 ->`, JSON.stringify(o));
  await p.screenshot({ path: `${out}qa4-${w}-open.png` });
  // swipe to the next slide
  await p.evaluate(() => document.getElementById('vtrack').scrollBy({ left: innerWidth, behavior: 'auto' })); await p.waitForTimeout(500);
  console.log(' after swipe:', await p.evaluate(() => document.getElementById('vn').textContent + ' srcs=' + [...document.querySelectorAll('.slide img.clip')].map(i => i.src ? 1 : 0).join('')));
  // close with the button; the carousel should land on card 3
  await p.tap('#vclose'); await p.waitForTimeout(700);
  console.log(' after close:', await p.evaluate(() => ({ hidden: document.getElementById('viewer').hidden, wn: document.getElementById('wn').textContent, card3left: Math.round(document.querySelector('.panel[data-i="2"]').getBoundingClientRect().left), locked: document.documentElement.classList.contains('vopen'), focus: document.activeElement.className })), 'scrollY same:', (await p.evaluate(() => scrollY)) === y0);
  await p.screenshot({ path: `${out}qa4-${w}-closed.png` });
  // Escape and backdrop close, history back
  await p.tap('.panel[data-i="2"] .pv'); await p.waitForTimeout(400); await p.keyboard.press('Escape'); await p.waitForTimeout(400);
  const esc = await p.evaluate(() => document.getElementById('viewer').hidden);
  await p.tap('.panel[data-i="2"] .pv'); await p.waitForTimeout(400); await p.goBack(); await p.waitForTimeout(500);
  const back = await p.evaluate(() => ({ hidden: document.getElementById('viewer').hidden, url: location.href.split('/').pop() }));
  await p.tap('.panel[data-i="2"] .pv'); await p.waitForTimeout(400); await p.tap('#vtrack', { position: { x: 5, y: 5 } }); await p.waitForTimeout(400);
  const bd = await p.evaluate(() => document.getElementById('viewer').hidden);
  console.log(' Escape closes:', esc, '| back button closes:', JSON.stringify(back), '| backdrop tap closes:', bd, '| page errors:', errs);
  await p.close();
}
const d = await b.newPage({ viewport: { width: 1400, height: 900 } }); await d.goto(url); await d.waitForTimeout(400);
console.log('\ndesktop: viewer display =', await d.evaluate(() => getComputedStyle(document.getElementById('viewer')).display), '| pv click opens?', await d.evaluate(() => { document.querySelector('.panel .pv') && document.querySelector('.panel .pv').click(); return !document.getElementById('viewer').hidden; }));
await b.close();
