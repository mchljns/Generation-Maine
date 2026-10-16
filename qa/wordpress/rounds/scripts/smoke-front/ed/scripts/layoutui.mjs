// Row vertical alignment and Grid columns through the editor controls on the layout test page: live canvas, then save and view.
import { launch, login, watch, save, shot } from './lib.mjs';
const [base, pid, url, tag] = process.argv.slice(2);
const log = []; const out = {};
const browser = await launch();
const { page } = await login(browser, base);
watch(page, log);
await page.goto(`${base}/wp-admin/post.php?post=${pid}&action=edit`, { waitUntil: 'domcontentloaded' });
await page.waitForFunction(() => window.wp && wp.data && wp.data.select('core/editor').getCurrentPostId(), null, { timeout: 90000 });
await page.waitForTimeout(3500);
for (let i = 0; i < 3; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click().catch(() => {}); await page.waitForTimeout(400); } }
const fr = await (await page.$('iframe[name="editor-canvas"]')).contentFrame();
const sel = (cls) => page.evaluate(c => { const s = wp.data.select('core/block-editor'); const id = s.getClientIdsWithDescendants().find(id => (s.getBlockAttributes(id).className || '').split(' ').includes(c)); wp.data.dispatch('core/block-editor').selectBlock(id); return id; }, cls);
const kids = (cls) => fr.evaluate(c => { const g = document.querySelector('.' + c); const r = g.getBoundingClientRect(); g.scrollIntoView(); return { ai: getComputedStyle(g).alignItems, gtc: getComputedStyle(g).gridTemplateColumns, kids: [...g.children].filter(k => !k.classList.contains('block-list-appender')).map(k => { const q = k.getBoundingClientRect(); return [Math.round(q.left - r.left), Math.round(q.top - r.top), Math.round(q.width), Math.round(q.height)]; }) }; }, cls);
// Row: t-row-center -> bottom via the toolbar
await sel('t-row-center'); await page.waitForTimeout(800);
out.rowBefore = await kids('t-row-center');
const va = page.locator('.block-editor-block-toolbar').getByRole('button', { name: /vertical alignment/i }).first();
out.vaButton = await va.count();
if (out.vaButton) { await va.click(); await page.waitForTimeout(500); out.vaItems = await page.getByRole('menuitemradio').allInnerTexts(); await page.getByRole('menuitemradio', { name: /bottom/i }).first().click(); await page.waitForTimeout(800); }
out.rowAfter = await kids('t-row-center');
out.rowAttr = await page.evaluate(() => { const s = wp.data.select('core/block-editor'); const id = s.getSelectedBlockClientId(); return s.getBlockAttributes(id).layout; });
await shot(page, `${tag}-layoutui-row`);
// Grid: t-grid3 -> 4 columns through the Layout panel
await sel('t-grid3'); await page.waitForTimeout(800);
const side = page.locator('.interface-complementary-area');
if (!(await side.count())) { await page.getByRole('button', { name: 'Settings', exact: true }).first().click(); await page.waitForTimeout(600); }
const bt = page.getByRole('tab', { name: 'Block' }); if (await bt.count()) { await bt.first().click(); await page.waitForTimeout(400); }
out.gridBefore = await kids('t-grid3');
const insp = page.locator('.block-editor-block-inspector');
out.layoutPanel = (await insp.innerText()).replace(/\s+/g, ' ').slice(0, 400);
const num = insp.locator('input[type="number"]').first();
out.numInputs = await insp.locator('input[type="number"]').count();
if (out.numInputs) { await num.fill('4'); await num.press('Tab'); await page.waitForTimeout(800); }
out.gridAfter = await kids('t-grid3');
out.gridAttr = await page.evaluate(() => { const s = wp.data.select('core/block-editor'); const id = s.getSelectedBlockClientId(); return s.getBlockAttributes(id).layout; });
await shot(page, `${tag}-layoutui-grid`);
await page.evaluate(() => wp.data.dispatch('core/editor').savePost());
await page.waitForFunction(() => !wp.data.select('core/editor').isSavingPost(), null, { timeout: 60000 }); await page.waitForTimeout(1500);
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } }); const p = await ctx.newPage();
await p.goto(url, { waitUntil: 'networkidle' });
out.front = await p.evaluate(() => { const f = c => { const g = document.querySelector('.' + c); const r = g.getBoundingClientRect(); return { ai: getComputedStyle(g).alignItems, gtc: getComputedStyle(g).gridTemplateColumns, kids: [...g.children].map(k => { const q = k.getBoundingClientRect(); return [Math.round(q.left - r.left), Math.round(q.top - r.top), Math.round(q.width)]; }) }; }; return { row: f('t-row-center'), grid: f('t-grid3') }; });
save(`${tag}-layoutui.json`, { out, log });
console.log(JSON.stringify(out, null, 1));
await browser.close();
