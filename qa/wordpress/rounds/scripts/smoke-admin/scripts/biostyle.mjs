// The story's look: computed style and box of each panel's p.bio (and the bdi inside it, if any) at 1440 and 390.
//   node biostyle.mjs <base> <tag>
import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
import fs from 'fs';
const [B, tag] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const out = {};
for (const [w, h] of [[1440, 900], [390, 844]]) {
  const ctx = await b.newContext({ viewport: { width: w, height: h } }); const page = await ctx.newPage();
  await page.goto(B + '/', { waitUntil: 'load' }); await page.waitForTimeout(1500);
  out[w] = await page.evaluate(() => [...document.querySelectorAll('.panel .bio')].map((p) => {
    const cs = getComputedStyle(p), inner = p.querySelector('bdi'), ics = inner ? getComputedStyle(inner) : null, r = p.getBoundingClientRect();
    const pick = (s) => s && { fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, lineHeight: s.lineHeight, color: s.color, letterSpacing: s.letterSpacing, overflowWrap: s.overflowWrap, unicodeBidi: s.unicodeBidi, direction: s.direction, display: s.display };
    return { text: p.textContent.slice(0, 40), p: { ...pick(cs), margin: cs.margin, maxWidth: cs.maxWidth, w: Math.round(r.width), h: Math.round(r.height) }, bdi: pick(ics) };
  }));
  out[w + 'scrollX'] = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  await ctx.close();
}
fs.writeFileSync(`/tmp/claude-0/wptest/work/smoke-admin/logs/biostyle-${tag}.json`, JSON.stringify(out, null, 1));
console.log(JSON.stringify({ p1440: out[1440][0], p390: out[390][0], n: out[1440].length, scrollX: [out['1440scrollX'], out['390scrollX']] }));
await b.close();
