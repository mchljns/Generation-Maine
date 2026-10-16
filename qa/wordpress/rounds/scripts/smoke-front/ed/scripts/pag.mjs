// Pagination on archive and search pages: each target's box, rows, gaps; tap a number at 390 with touch.
import { launch, save } from './lib.mjs';
const [base, tag, ...paths] = process.argv.slice(2);
const browser = await launch();
const out = {};
for (const path of paths) {
  for (const [w, h] of [[390, 844], [1440, 900], [320, 568]]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, ...(w < 500 ? { isMobile: true, hasTouch: true, deviceScaleFactor: 2 } : {}) });
    const page = await ctx.newPage();
    const r = await page.goto(base + path, { waitUntil: 'networkidle' });
    const nav = page.locator('.wp-block-query-pagination').first();
    if (!(await nav.count())) { out[path + '@' + w] = { status: r.status(), nav: null }; await ctx.close(); continue; }
    await nav.scrollIntoViewIfNeeded();
    await nav.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-pag-${path.replace(/\W+/g, '_')}-${w}.png` }).catch(() => {});
    const m = await page.evaluate(() => {
      const n = document.querySelector('.wp-block-query-pagination');
      const items = [...n.querySelectorAll('a, span.page-numbers')].map(e => { const r = e.getBoundingClientRect(); return { text: e.textContent.trim().replace(/\s+/g, ' '), cls: e.className, x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height), cx: r.left + r.width / 2, cy: r.top + r.height / 2 }; });
      // smallest distance between centers of neighboring targets, and overlap of 24px circles
      let minDist = Infinity;
      for (let i = 0; i < items.length; i++) for (let j = i + 1; j < items.length; j++) { const d = Math.hypot(items[i].cx - items[j].cx, items[i].cy - items[j].cy); if (d < minDist) minDist = d; }
      const rows = [...new Set(items.map(i => i.y))].length;
      const c = getComputedStyle(n);
      return { display: c.display, justify: c.justifyContent, rows, minCenterDist: Math.round(minDist), items, overflow: document.documentElement.scrollWidth - innerWidth };
    });
    m.status = r.status();
    out[path + '@' + w] = m;
    if (w === 390) {
      // tap the last number link and see where it goes
      const nums = page.locator('.wp-block-query-pagination-numbers a.page-numbers');
      if (await nums.count()) { const last = nums.last(); const t = await last.textContent(); await Promise.all([page.waitForNavigation(), last.tap()]); m.tapped = { text: t.trim(), url: page.url() }; }
    }
    await ctx.close();
  }
}
save(`${tag}-pag.json`, out);
for (const [k, v] of Object.entries(out)) console.log(k, v.nav === null ? 'NO NAV' : JSON.stringify({ display: v.display, rows: v.rows, minCenterDist: v.minCenterDist, overflow: v.overflow, items: v.items.map(i => `${i.text}[${i.x},${i.y} ${i.w}x${i.h}]`), tapped: v.tapped }));
await browser.close();
