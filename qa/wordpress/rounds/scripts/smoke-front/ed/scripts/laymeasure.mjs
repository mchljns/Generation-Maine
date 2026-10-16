// Measure every .t-* test block on a post or page as a visitor (1440, 390) and in the post editor canvas (1440):
// container box and computed layout, each child's box relative to the container, rows. Screenshots of the page and the editor.
// usage: node laymeasure.mjs <base> <url> <postId> <tag> [noeditor]
import { launch, login, save } from './lib.mjs';
const [base, url, pid, tag, noed] = process.argv.slice(2);
const OUTD = "/tmp/claude-0/wptest/work/smoke-front/ed";
const browser = await launch();
const M = () => {
  const kidsSel = (el) => {
    const c = el.classList;
    if (c.contains('wp-block-gallery')) return ':scope > figure.wp-block-image';
    if (c.contains('wp-block-buttons')) return ':scope > .wp-block-button';
    if (c.contains('wp-block-columns')) return ':scope > .wp-block-column';
    if (c.contains('wp-block-cover')) return ':scope > .wp-block-cover__inner-container';
    if (c.contains('wp-block-media-text')) return ':scope > .wp-block-media-text__media, :scope > .wp-block-media-text__content';
    return ':scope > *:not(.block-list-appender):not(.block-editor-block-list__insertion-point)';
  };
  const out = {};
  const seen = new Set();
  for (const el of document.querySelectorAll('[class*="t-"]')) {
    const t = [...el.classList].find(x => /^t-[a-z0-9-]+$/.test(x));
    if (!t || seen.has(t)) continue;
    seen.add(t);
    const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    const kids = [...el.querySelectorAll(kidsSel(el))].filter(k => getComputedStyle(k).display !== 'none' && k.getBoundingClientRect().width > 0).map(k => { const q = k.getBoundingClientRect(); return { x: Math.round(q.left - r.left), y: Math.round(q.top - r.top), w: Math.round(q.width), h: Math.round(q.height), t: k.textContent.trim().slice(0, 18) }; });
    const rows = []; for (const k of kids) { const row = rows.find(rr => Math.abs(rr.y - k.y) <= 3); if (row) row.n++; else rows.push({ y: k.y, n: 1 }); }
    out[t] = { box: [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)], display: cs.display, dir: cs.flexDirection, wrap: cs.flexWrap, ai: cs.alignItems, jc: cs.justifyContent, gap: cs.gap, gtc: cs.gridTemplateColumns, gtr: cs.gridTemplateRows, rows: rows.map(x => x.n), kids };
  }
  out._overflow = document.documentElement.scrollWidth - document.documentElement.clientWidth;
  return out;
};
const res = {};
for (const [w, h] of [[1440, 900], [390, 844]]) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, ...(w < 500 ? { isMobile: true, hasTouch: true, deviceScaleFactor: 2 } : {}) });
  const page = await ctx.newPage();
  const errs = []; page.on('pageerror', e => errs.push(String(e)));
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);
  res['front' + w] = await page.evaluate(M);
  res['front' + w]._errs = errs;
  await page.screenshot({ path: `${OUTD}/shots/${tag}-front-${w}.png`, fullPage: true });
  await ctx.close();
}
if (!noed) {
  const { page } = await login(browser, base);
  const errs = []; page.on('pageerror', e => errs.push(String(e)));
  await page.goto(`${base}/wp-admin/post.php?post=${pid}&action=edit`, { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => window.wp && wp.data && wp.data.select('core/editor').getCurrentPostId(), null, { timeout: 90000 });
  await page.waitForTimeout(4000);
  for (let i = 0; i < 3; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click().catch(() => {}); await page.waitForTimeout(400); } }
  const fh = await page.$('iframe[name="editor-canvas"]');
  const frame = fh ? await fh.contentFrame() : page.mainFrame();
  // scroll through the canvas so lazy parts render
  await frame.evaluate(async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } window.scrollTo(0, 0); });
  await page.waitForTimeout(1000);
  res.editor = await frame.evaluate(M);
  res.editor._errs = errs;
  res.editor._dirty = await page.evaluate(() => wp.data.select('core/editor').isEditedPostDirty());
  // full canvas screenshot: resize the iframe's scroll area into an image by stepping
  const H = await frame.evaluate(() => document.documentElement.scrollHeight);
  res.editor._height = H;
  await page.screenshot({ path: `${OUTD}/shots/${tag}-editor-1440.png` });
}
save(`${tag}-lay.json`, res);
console.log('saved', tag, Object.keys(res.front1440).length, 'blocks');
await browser.close();
