// Compare About and Follow inserted in a page with the same sections on the front page, at 1440 and 390.
import { launch, save } from './lib.mjs';
const [base, path, tag] = process.argv.slice(2);
const browser = await launch();
const res = {};
for (const vw of [1440, 390]) {
  const ctx = await browser.newContext({ viewport: { width: vw, height: 900 }, ...(vw < 500 ? { isMobile: true, hasTouch: true, deviceScaleFactor: 2 } : {}) });
  for (const [label, url] of [['front', '/'], ['page', path]]) {
    const page = await ctx.newPage();
    await page.goto(base + url, { waitUntil: 'networkidle' });
    res[`${label}-${vw}`] = await page.evaluate(() => {
      const pick = (sec) => {
        const s = document.querySelector(sec);
        if (!s) return null;
        const els = [...s.querySelectorAll('h2, p, .k, img, .row, a')].filter(e => e.getBoundingClientRect().height > 0).slice(0, 14);
        const sr = s.getBoundingClientRect();
        const cs = getComputedStyle(s);
        return { h: Math.round(sr.height), w: Math.round(sr.width), x: Math.round(sr.left), mt: cs.marginTop, mb: cs.marginBottom, bg: cs.backgroundColor, items: els.map(e => { const c = getComputedStyle(e); const r = e.getBoundingClientRect(); return `${e.tagName}.${(e.className && e.className.baseVal === undefined ? e.className : '').split(' ')[0]} "${(e.innerText || e.alt || '').slice(0, 18)}" ${c.fontFamily.split(',')[0]} ${c.fontSize}/${c.lineHeight} c=${c.color} mt=${c.marginTop} top+${Math.round(r.top - sr.top)} left=${Math.round(r.left)} w=${Math.round(r.width)} h=${Math.round(r.height)}`; }) };
      };
      const prev = document.querySelector('section.about') ? document.querySelector('section.about').previousElementSibling : null;
      return { about: pick('section.about'), follow: pick('section.follow'), overflow: document.documentElement.scrollWidth - innerWidth, prevGap: prev ? Math.round(document.querySelector('section.about').getBoundingClientRect().top - prev.getBoundingClientRect().bottom) : null };
    });
    await page.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-${label}-${vw}.png`, fullPage: true });
    await page.close();
  }
  await ctx.close();
}
save(`${tag}-cmpsec.json`, res);
let diffs = 0;
for (const k of ['about', 'follow']) for (const vw of [1440, 390]) {
  const f = res[`front-${vw}`][k], p = res[`page-${vw}`][k];
  console.log(`\n### ${k} ${vw}: front h=${f && f.h} w=${f && f.w} x=${f && f.x} | page h=${p && p.h} w=${p && p.w} x=${p && p.x} mt=${p && p.mt} mb=${p && p.mb}`);
  const n = Math.max(f ? f.items.length : 0, p ? p.items.length : 0);
  for (let i = 0; i < n; i++) { const a = f && f.items[i], b = p && p.items[i]; if (a !== b) { diffs++; console.log(`  F: ${a}\n  P: ${b}`); } }
}
console.log('\noverflow page', res['page-1440'].overflow, res['page-390'].overflow, 'gap above About', res['page-1440'].prevGap, res['page-390'].prevGap, 'differing lines', diffs);
await browser.close();
