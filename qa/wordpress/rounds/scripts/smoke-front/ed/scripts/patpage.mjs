// A new page through the editor: title, one paragraph, then About and Follow from Inserter > Patterns > Generation Maine. Publish.
// usage: node patpage.mjs <base> <tag> [Pattern names...]
import { launch, login, watch, save, shot } from './lib.mjs';
const [base, tag, ...pats] = process.argv.slice(2);
const want = pats.length ? pats : ['About', 'Follow'];
const log = [];
const browser = await launch();
const { page } = await login(browser, base);
watch(page, log);
await page.goto(base + '/wp-admin/post-new.php?post_type=page', { waitUntil: 'domcontentloaded' });
await page.waitForFunction(() => window.wp && wp.data && wp.data.select('core/editor') && wp.data.select('core/editor').getCurrentPostId(), null, { timeout: 90000 });
await page.waitForTimeout(2500);
for (let i = 0; i < 4; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click().catch(() => {}); await page.waitForTimeout(500); } else break; }
const hasIframe = await page.locator('iframe[name="editor-canvas"]').count();
const root = hasIframe ? page.frameLocator('iframe[name="editor-canvas"]') : page;
await root.locator('.editor-post-title__input, h1.wp-block-post-title').first().click();
await page.keyboard.type('Sections ' + want.join(' and '));
await page.keyboard.press('Enter');
await page.keyboard.type('A page with the sections inserted from Patterns.');
await page.keyboard.press('Enter');
const inserted = [];
for (const name of want) {
  await page.locator('button[aria-label="Block Inserter"], button[aria-label="Toggle block inserter"], .editor-document-tools__inserter-toggle, .edit-post-header-toolbar__inserter-toggle').first().click();
  await page.waitForTimeout(900);
  await page.getByRole('tab', { name: 'Patterns' }).click();
  await page.waitForTimeout(900);
  const cat = page.locator('.block-editor-inserter__category-panel, .block-editor-inserter__patterns-category-panel').first();
  const gm = page.getByRole('button', { name: /^Generation Maine/ }).or(page.getByRole('tab', { name: /^Generation Maine/ })).first();
  await gm.click();
  await page.waitForTimeout(1800);
  const items = page.locator('.block-editor-block-patterns-list__item');
  const n = await items.count();
  const labels = [];
  for (let i = 0; i < n; i++) labels.push(((await items.nth(i).getAttribute('aria-label')) || '') + '|' + (await items.nth(i).innerText()).trim());
  let hit = -1;
  for (let i = 0; i < n; i++) if (labels[i].split('|').some(s => s.trim() === name)) { hit = i; break; }
  inserted.push({ name, labels, hit });
  if (hit >= 0) await items.nth(hit).click();
  await page.waitForTimeout(1500);
  const close = page.locator('button[aria-label="Close Block Inserter"], button[aria-label="Close block inserter"], .block-editor-inserter__main-area ~ button, .editor-inserter-sidebar__header button').first();
  if (await page.locator('.block-editor-inserter__menu').count()) { await page.keyboard.press('Escape'); await page.waitForTimeout(300); }
  if (await page.locator('.block-editor-inserter__menu').count()) await close.click().catch(() => {});
  await page.waitForTimeout(500);
}
await shot(page, `${tag}-inserted`);
const blocks = await page.evaluate(() => wp.data.select('core/block-editor').getBlocks().map(b => b.name + (b.attributes.className ? '.' + b.attributes.className : '')));
await page.locator('.editor-post-publish-button__button, .editor-post-publish-panel__toggle').first().click();
await page.waitForTimeout(1200);
const confirm = page.locator('.editor-post-publish-panel__header-publish-button button, .editor-post-publish-panel__header-publish-button .components-button').first();
if (await confirm.count()) await confirm.click();
await page.waitForFunction(() => { const s = wp.data.select('core/editor'); return !s.isSavingPost() && s.getCurrentPost().status === 'publish'; }, null, { timeout: 60000 });
const info = await page.evaluate(() => { const p = wp.data.select('core/editor').getCurrentPost(); return { id: p.id, link: p.link }; });
save(`${tag}-patpage.json`, { info, inserted, blocks, log });
console.log(JSON.stringify({ info, inserted: inserted.map(i => [i.name, i.hit, i.labels.length]), blocks }));
await browser.close();
