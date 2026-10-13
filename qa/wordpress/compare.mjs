// Renders the v2 page and the WordPress front page at the same sizes and saves matching shots.
//   node compare.mjs <outdir>
import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
const out = process.argv[2];
const pages = { v2: 'file:///home/user/Generation-Maine/brand/identity/splash-lean-a/index.html', wp: 'http://127.0.0.1:8080/' };
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
for (const [w, h] of [[1440, 900], [390, 844]]) {
  for (const [name, url] of Object.entries(pages)) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1, isMobile: w < 900, hasTouch: w < 900 });
    const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); }); p.on('requestfailed', r => errs.push('failed ' + r.url().split('/').pop()));
    await p.goto(url, { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(2600);
    await p.screenshot({ path: `${out}/${name}-${w}-top.png` });
    // section geometry for a numeric comparison
    const geo = await p.evaluate(() => ['.top', '.hero', '#about', '#creators', '#stories', '#follow', '#newsletter', '.site'].map(s => { const e = document.querySelector(s); if (!e) return [s, null]; const r = e.getBoundingClientRect(); return [s, Math.round(r.height)]; }));
    const fonts = await p.evaluate(() => ['.top nav a', '.hero h1', '.hero .lede', '.hero .k', '.btn,.wp-block-button__link', '.site .flinks a'].map(s => { const e = document.querySelector(s); return e ? s + ': ' + getComputedStyle(e).fontFamily.split(',')[0] + ' ' + getComputedStyle(e).fontSize : s + ': none'; }));
    await p.addStyleTag({ content: '.top{position:relative!important}html{scroll-behavior:auto!important}' });
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); });
    await p.waitForTimeout(800);
    await p.screenshot({ path: `${out}/${name}-${w}-full.png`, fullPage: true });
    console.log(`${name} ${w}: height ${await p.evaluate(() => document.documentElement.scrollHeight)} overflow ${await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth)} errors ${JSON.stringify(errs.slice(0, 5))}`);
    console.log('  sections', JSON.stringify(geo)); console.log('  fonts', fonts.join(' | '));
    await p.close();
  }
}
await b.close();
