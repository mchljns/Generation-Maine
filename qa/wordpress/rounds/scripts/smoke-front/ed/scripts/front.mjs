// Load a URL as a visitor at 1440 and 390: overflow, h1 markup, gold word and dot, build stamp, errors. Optional screenshot crop of the hero.
import { launch, save, shot } from './lib.mjs';
const url = process.argv[2], tag = process.argv[3];
const browser = await launch();
const out = {};
for (const [w, h] of [[1440, 900], [390, 844]]) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, ...(w < 500 ? { isMobile: true, hasTouch: true, deviceScaleFactor: 2 } : {}) });
  const page = await ctx.newPage();
  const log = [];
  page.on('pageerror', e => log.push('pageerror: ' + e));
  page.on('console', m => { if (m.type() === 'error') log.push('console: ' + m.text().slice(0, 200)); });
  const r = await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1200);
  out[w] = await page.evaluate(() => {
    const h1 = document.querySelector('h1');
    const here = [...document.querySelectorAll('h1 .here')].map(s => { const c = getComputedStyle(s); return { text: s.textContent, color: c.color }; });
    const dot = document.querySelector('h1 .d');
    const lastText = h1 ? h1.innerText : '';
    return {
      overflow: document.documentElement.scrollWidth - innerWidth,
      h1html: h1 ? h1.innerHTML : null,
      h1text: lastText,
      here, dot: dot ? (() => { const r = dot.getBoundingClientRect(); return { w: r.width, h: r.height, bg: getComputedStyle(dot).backgroundColor }; })() : null,
      build: (document.body.innerText.match(/Build [0-9a-f]{7}/) || [])[0] || null,
      title: document.title,
    };
  });
  out[w].status = r.status();
  out[w].log = log;
  const h1 = page.locator('h1').first();
  if (await h1.count()) await h1.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-h1-${w}.png` }).catch(() => {});
  await ctx.close();
}
save(`${tag}-front.json`, out);
console.log(JSON.stringify(out, null, 1));
await browser.close();
