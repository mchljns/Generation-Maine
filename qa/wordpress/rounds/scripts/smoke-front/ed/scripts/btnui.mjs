// Button Width through the editor UI: add Buttons with two buttons, set each to 50% in the block sidebar, publish, measure.
import { launch, login, watch, save, shot } from './lib.mjs';
const [base, tag, pct = '50'] = process.argv.slice(2);
const log = []; const out = {};
const browser = await launch();
const { page } = await login(browser, base);
watch(page, log);
await page.goto(base + '/wp-admin/post-new.php', { waitUntil: 'domcontentloaded' });
await page.waitForFunction(() => window.wp && wp.data && wp.data.select('core/editor') && wp.data.select('core/editor').getCurrentPostId(), null, { timeout: 90000 });
await page.waitForTimeout(2500);
for (let i = 0; i < 4; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click().catch(() => {}); await page.waitForTimeout(500); } else break; }
const root = page.frameLocator('iframe[name="editor-canvas"]');
await root.locator('.editor-post-title__input, h1.wp-block-post-title').first().click();
await page.keyboard.type('Button width UI ' + pct);
await page.keyboard.press('Enter'); await page.waitForTimeout(500);
await page.keyboard.type('/buttons'); await page.waitForTimeout(900); await page.keyboard.press('Enter'); await page.waitForTimeout(900);
await page.keyboard.type('First'); await page.waitForTimeout(300);
await page.keyboard.press('End'); await page.keyboard.press('Enter'); await page.waitForTimeout(700);
let n = await page.evaluate(() => wp.data.select('core/block-editor').getGlobalBlockCount('core/button'));
if (n < 2) { await root.locator('.wp-block-buttons .block-list-appender button, .wp-block-buttons .block-editor-button-block-appender').first().click(); await page.waitForTimeout(700); }
await page.keyboard.type('Second'); await page.waitForTimeout(300);
out.count = await page.evaluate(() => wp.data.select('core/block-editor').getGlobalBlockCount('core/button'));
const ids = await page.evaluate(() => { const s = wp.data.select('core/block-editor'); return s.getClientIdsWithDescendants().filter(id => s.getBlockName(id) === 'core/button'); });
const side = page.locator('.interface-complementary-area');
if (!(await side.count())) { await page.getByRole('button', { name: 'Settings', exact: true }).first().click(); await page.waitForTimeout(600); }
out.controls = [];
for (const id of ids) {
  await page.evaluate(id => wp.data.dispatch('core/block-editor').selectBlock(id), id); await page.waitForTimeout(700);
  for (const tab of ['Settings', 'Block']) { const t = page.getByRole('tab', { name: tab, exact: true }); if (await t.count()) { await t.first().click().catch(() => {}); await page.waitForTimeout(400); } }
  const insp = page.locator('.block-editor-block-inspector');
  out.controls.push((await insp.innerText()).replace(/\s+/g, ' ').slice(0, 500));
  const rng = insp.locator('input[type="range"]');
  if (await rng.count()) { await rng.first().focus(); const steps = { '25': 1, '50': 2, '75': 3, '100': 4 }[pct]; for (let i = 0; i < steps; i++) { await page.keyboard.press('ArrowRight'); await page.waitForTimeout(250); } out.controls.push('range: ' + await rng.first().inputValue() + ' ' + (await rng.first().getAttribute('aria-valuetext'))); await shot(page, `${tag}-btnui-sidebar`); continue; }
  let opt = insp.getByRole('radio', { name: pct + '%' });
  if (!(await opt.count())) opt = insp.getByRole('button', { name: pct + '%' });
  if (!(await opt.count())) { const st = page.getByRole('tab', { name: 'Styles' }); if (await st.count()) { await st.first().click(); await page.waitForTimeout(500); } opt = insp.getByRole('radio', { name: pct + '%' }); if (!(await opt.count())) opt = insp.getByRole('button', { name: pct + '%' }); out.controls.push('styles tab: ' + (await insp.innerText()).replace(/\s+/g, ' ').slice(0, 500)); }
  out['clicked' + id.slice(0, 4)] = await opt.count();
  if (await opt.count()) { await opt.first().click(); await page.waitForTimeout(500); }
  await shot(page, `${tag}-btnui-sidebar`);
}
out.attrs = await page.evaluate(() => { const s = wp.data.select('core/block-editor'); return s.getClientIdsWithDescendants().filter(id => s.getBlockName(id) === 'core/button').map(id => s.getBlockAttributes(id)); });
out.saved = await page.evaluate(() => wp.data.select('core/editor').getEditedPostContent());
await page.evaluate(() => wp.data.dispatch('core/editor').editPost({ status: 'publish' }));
await page.evaluate(() => wp.data.dispatch('core/editor').savePost());
await page.waitForFunction(() => { const s = wp.data.select('core/editor'); return !s.isSavingPost() && s.getCurrentPost().status === 'publish'; }, null, { timeout: 60000 });
const fr = await (await page.$('iframe[name="editor-canvas"]')).contentFrame();
out.editorBoxes = await fr.evaluate(() => { const g = document.querySelector('.wp-block-buttons'); const r = g.getBoundingClientRect(); return { w: Math.round(r.width), kids: [...g.querySelectorAll(':scope > .wp-block-button')].map(k => Math.round(k.getBoundingClientRect().width)) }; });
const link = await page.evaluate(() => wp.data.select('core/editor').getCurrentPost().link);
out.link = link;
for (const w of [1440, 390]) {
  const ctx = await browser.newContext({ viewport: { width: w, height: 900 } }); const p = await ctx.newPage();
  await p.goto(link, { waitUntil: 'networkidle' });
  out['front' + w] = await p.evaluate(() => { const g = document.querySelector('main .wp-block-buttons'); const r = g.getBoundingClientRect(); return { w: Math.round(r.width), kids: [...g.querySelectorAll(':scope > .wp-block-button')].map(k => Math.round(k.getBoundingClientRect().width)), cls: [...g.querySelectorAll(':scope > .wp-block-button')].map(k => k.className) }; });
  await p.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-btnui-front-${w}.png` });
  await ctx.close();
}
save(`${tag}-btnui.json`, { out, log });
console.log(JSON.stringify(out, null, 1));
await browser.close();
