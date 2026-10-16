// Measure core blocks on a page as a visitor (1440, 390) and in the block editor canvas (1440): buttons, columns, rows, stack,
// grid, gallery, quote, separator, table, title. axe color-contrast on the front. Keyboard focus ring and hover on a button.
// usage: node blocks-measure.mjs <base> <pageId> <tag>
import { launch, login, save, shot } from './lib.mjs';
const [base, pid, tag] = process.argv.slice(2);
const browser = await launch();
const M = (scope) => {
  const q = (s) => [...(scope || document).querySelectorAll(s)];
  const R = (e) => { if (!e) return null; const r = e.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const C = (e, props) => { if (!e) return null; const c = getComputedStyle(e); const o = {}; for (const p of props) o[p] = c[p]; return o; };
  const out = {};
  const title = document.querySelector('h1.gm-title, h1.wp-block-post-title, .editor-post-title, .editor-post-title__input');
  out.title = { ...R(title), ...C(title, ['fontSize', 'fontFamily', 'color']) };
  const firstP = q('p').find(p => /Intro paragraph/.test(p.textContent));
  out.introP = { ...R(firstP), ...C(firstP, ['fontSize', 'maxWidth']) };
  out.buttons = q('main .wp-block-buttons, .is-root-container .wp-block-buttons').map(g => ({ cls: g.className, box: R(g), ...C(g, ['display', 'flexWrap', 'justifyContent', 'gap']), items: [...g.querySelectorAll('.wp-block-button__link')].map(a => ({ text: a.textContent.trim(), box: R(a), ...C(a, ['color', 'backgroundColor', 'borderTopColor', 'borderTopWidth', 'borderTopLeftRadius', 'fontFamily', 'fontSize', 'textDecorationLine', 'display']) })) }));
  const cols = document.querySelector('.wp-block-columns');
  out.columns = cols ? { ...C(cols, ['display', 'columnGap', 'gap']), box: R(cols), cols: [...cols.children].filter(c => c.classList.contains('wp-block-column')).map(R) } : null;
  const row = (sel) => { const g = document.querySelector(sel); return g ? { cls: g.className, ...C(g, ['display', 'flexDirection', 'flexWrap', 'alignItems', 'justifyContent', 'gap', 'gridTemplateColumns']), box: R(g), kids: [...g.children].filter(k => !k.classList.contains('block-list-appender')).map(k => ({ t: k.textContent.trim().slice(0, 20), ...R(k) })) } : null; };
  out.row = row('.t-row'); out.rowTop = row('.t-row-top'); out.stack = row('.t-stack'); out.grid = row('.t-grid');
  const gal = document.querySelector('.wp-block-gallery');
  out.gallery = gal ? { cls: gal.className, ...C(gal, ['display', 'flexWrap', 'gap', 'columnGap']), box: R(gal), imgs: [...gal.querySelectorAll('figure.wp-block-image')].map(R), cap: (gal.querySelector('figcaption.blocks-gallery-caption, figcaption') || {}).textContent } : null;
  const bq = document.querySelector('.wp-block-quote');
  out.quote = bq ? { box: R(bq), ...C(bq, ['borderLeftWidth', 'borderLeftColor', 'paddingLeft', 'marginLeft']), cite: C(bq.querySelector('cite'), ['fontStyle', 'fontSize']) } : null;
  const hr = document.querySelector('hr.wp-block-separator');
  out.hr = hr ? { box: R(hr), ...C(hr, ['marginLeft', 'marginRight', 'borderTopWidth', 'borderTopColor', 'borderBottomWidth']) } : null;
  const tb = document.querySelector('.wp-block-table table');
  out.table = tb ? { box: R(tb), td: C(tb.querySelector('td'), ['borderTopWidth', 'borderTopStyle', 'padding']), cap: C(document.querySelector('.wp-block-table figcaption'), ['fontStyle', 'fontSize']) } : null;
  out.h2 = q('h2').slice(0, 2).map(h => ({ t: h.textContent.trim(), ...R(h), ...C(h, ['fontSize', 'marginTop', 'fontFamily']) }));
  out.overflow = document.documentElement.scrollWidth - document.documentElement.clientWidth;
  return out;
};
const res = {};
for (const [w, h] of [[1440, 900], [390, 844]]) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, ...(w < 500 ? { isMobile: true, hasTouch: true, deviceScaleFactor: 2 } : {}) });
  const page = await ctx.newPage();
  await page.goto(`${base}/?page_id=${pid}`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);
  res['front' + w] = await page.evaluate(M);
  await page.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-front-${w}.png`, fullPage: true });
  await page.addScriptTag({ path: '/home/user/Generation-Maine/node_modules/axe-core/axe.min.js' });
  const axe = await page.evaluate(async () => { const r = await axe.run(document, { runOnly: ['wcag2a', 'wcag2aa'] }); return r.violations.map(v => ({ id: v.id, impact: v.impact, n: v.nodes.length, nodes: v.nodes.slice(0, 4).map(n => n.target.join(' ') + ' :: ' + (n.any[0] ? n.any[0].message : '').slice(0, 160)) })); });
  res['axe' + w] = axe;
  if (w === 1440) {
    // keyboard focus and hover on the first button
    const first = page.locator('main .wp-block-button__link').first();
    await first.focus();
    await page.keyboard.press('Shift+Tab'); await page.keyboard.press('Tab');
    res.focus = await page.evaluate(() => { const a = document.activeElement; const c = getComputedStyle(a); return { el: a.className + ' ' + a.textContent.trim(), outline: c.outlineStyle + ' ' + c.outlineWidth + ' ' + c.outlineColor, offset: c.outlineOffset }; });
    await first.hover(); await page.waitForTimeout(400);
    res.hover = await first.evaluate(a => { const c = getComputedStyle(a); return { bg: c.backgroundColor, color: c.color }; });
    const outl = page.locator('main .is-style-outline .wp-block-button__link').first();
    if (await outl.count()) { await outl.hover(); await page.waitForTimeout(400); res.hoverOutline = await outl.evaluate(a => { const c = getComputedStyle(a); return { bg: c.backgroundColor, color: c.color, border: c.borderTopColor }; }); }
    await first.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-btn-hover.png` }).catch(() => {});
  }
  await ctx.close();
}
// editor canvas
const { page } = await login(browser, base);
await page.goto(`${base}/wp-admin/post.php?post=${pid}&action=edit`, { waitUntil: 'domcontentloaded' });
await page.waitForFunction(() => window.wp && wp.data && wp.data.select('core/editor').getCurrentPostId(), null, { timeout: 90000 });
await page.waitForTimeout(3500);
for (let i = 0; i < 3; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click().catch(() => {}); await page.waitForTimeout(400); } }
const fh = await page.$('iframe[name="editor-canvas"]');
const frame = fh ? await fh.contentFrame() : page.mainFrame();
res.editorIframe = !!fh;
res.renderingMode = await page.evaluate(() => { const s = wp.data.select('core/editor'); return s.getRenderingMode ? s.getRenderingMode() : 'n/a'; });
res.editor = await frame.evaluate(M);
res.editorRoot = await frame.evaluate(() => { const r = document.querySelector('.is-root-container'); const t = document.querySelector('.edit-post-visual-editor__post-title-wrapper, .editor-visual-editor__post-title-wrapper'); const R = e => e ? (({ left, width }) => ({ x: Math.round(left), w: Math.round(width) }))(e.getBoundingClientRect()) : null; return { rootCls: r && r.className, root: R(r), titleWrapCls: t && t.className, titleWrap: R(t), vw: document.documentElement.clientWidth }; });
await page.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-editor-1440.png` });
save(`${tag}-blocks.json`, res);
console.log(JSON.stringify(res, null, 1));
await browser.close();
