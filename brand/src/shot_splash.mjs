// Screenshots of the splash page at desktop and phone widths, scrolled so every section has entered the view.
import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
import path from 'node:path';
const [,, src, outPrefix] = process.argv;
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
for (const [name, w, h] of [['desktop', 1440, 900], ['phone', 390, 844]]) {
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  const errors = []; p.on('pageerror', e => errors.push(e.message)); p.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  await p.goto('file://' + path.resolve(src)); await p.addStyleTag({ content: 'html{scroll-behavior:auto!important}' }); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(1600);
  await p.screenshot({ path: `${outPrefix}-${name}-hero.png` });
  const H = await p.evaluate(() => document.body.scrollHeight);
  for (let y = 0; y < H; y += h * 0.7) { await p.evaluate(yy => scrollTo(0, yy), y); await p.waitForTimeout(350); }
  await p.evaluate(() => scrollTo(0, 0)); await p.addStyleTag({ content: '.top{position:static}' }); await p.waitForTimeout(400);
  await p.screenshot({ path: `${outPrefix}-${name}.png`, fullPage: true });
  const overflow = await p.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
  console.log(name, 'height', H, 'overflow', overflow, 'errors', errors);
  await p.close();
}
await b.close();
