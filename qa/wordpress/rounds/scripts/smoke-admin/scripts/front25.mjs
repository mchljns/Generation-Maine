// 25+ creators on the front page: counter, position row, overflow, errors; step to the last creator with the keyboard on the phone
import { launch, base, SHOTS, watch } from './lib.mjs';
const [port, tag] = process.argv.slice(2); const B = base(port);
const b = await launch(); const out = {};
for (const [w, h] of [[1440, 900], [390, 844], [320, 568]]) {
  const ctx = await b.newContext({ viewport: { width: w, height: h }, isMobile: w < 800, hasTouch: w < 800 }); const p = await ctx.newPage(); const errs = []; watch(p, errs);
  await p.goto(B + '/?n=' + Date.now()); await p.waitForTimeout(1500);
  const r = await p.evaluate(() => ({ count: (document.getElementById('wn') || {}).textContent, segsClass: (document.getElementById('segs') || {}).className, segs: document.querySelectorAll('#segs button, .segs button').length, progress: !!document.querySelector('.segs.bar, .progress, #segs.bar, .segs .bar, [class*="prog"]'), stories: document.querySelectorAll('#panels .panel, .panel').length, slides: document.querySelectorAll('.slide').length, sw: document.documentElement.scrollWidth, names: [...document.querySelectorAll('[data-name]')].length }));
  // keyboard: focus the carousel or stage and press ArrowRight many times
  let last = null;
  if (w < 800) {
    const track = p.locator('.slides, .track, #slides, .cards').first();
    await p.locator('#creators, .stories').first().scrollIntoViewIfNeeded();
    const tr = p.locator('section.stories [tabindex="0"]:not([aria-label])').first(); await tr.focus().catch(() => {});
    for (let i = 0; i < 30; i++) { await p.keyboard.press('ArrowRight'); await p.waitForTimeout(120); }
    await p.waitForTimeout(800);
    last = await p.evaluate(() => ({ count: (document.getElementById('wn') || {}).textContent, active: (document.activeElement || {}).className }));
  }
  await p.screenshot({ path: `${SHOTS}/front25-${tag}-${w}.png` });
  out[w] = { ...r, afterArrows: last, errors: errs.filter(e => !/CERT|favicon/.test(e)) };
  await ctx.close();
}
console.log(JSON.stringify(out, null, 1)); await b.close();
