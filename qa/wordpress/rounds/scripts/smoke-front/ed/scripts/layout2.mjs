// The second blocks page: grid with 2 columns, a 2-image gallery, a 3-column gallery; front at 1440 and 390, editor at 1440.
import { launch, login, save } from './lib.mjs';
const [base, url, pid, tag] = process.argv.slice(2);
const browser = await launch();
const M = () => {
  const R = e => { const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)]; };
  const kids = (sel, k) => { const g = document.querySelector(sel); if (!g) return null; const c = getComputedStyle(g); return { display: c.display, gap: c.gap, gtc: c.gridTemplateColumns, box: R(g), items: [...g.querySelectorAll(k)].map(R) }; };
  return { grid2: kids('.t-grid2', ':scope > p'), gal2: kids('.t-gal2', 'figure.wp-block-image'), gal3: kids('.t-gal3', 'figure.wp-block-image') };
};
const res = {};
for (const [w, h] of [[1440, 900], [390, 844]]) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h } });
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: 'networkidle' });
  res['front' + w] = await page.evaluate(M);
  await page.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-front-${w}.png`, fullPage: true });
  await ctx.close();
}
const { page } = await login(browser, base);
await page.goto(`${base}/wp-admin/post.php?post=${pid}&action=edit`, { waitUntil: 'domcontentloaded' });
await page.waitForFunction(() => window.wp && wp.data && wp.data.select('core/editor').getCurrentPostId(), null, { timeout: 90000 });
await page.waitForTimeout(3500);
for (let i = 0; i < 3; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click().catch(() => {}); await page.waitForTimeout(400); } }
const fh = await page.$('iframe[name="editor-canvas"]');
const frame = fh ? await fh.contentFrame() : page.mainFrame();
res.editor = await frame.evaluate(M);
await page.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-editor-1440.png`, fullPage: false });
save(`${tag}-layout2.json`, res);
console.log(JSON.stringify(res));
await browser.close();
