// Locked blocks resist Delete and Backspace; delete the whole Follow section from List View, save, then insert the Follow pattern
// with nothing selected, save, and check #follow and #newsletter on the page.
import { launch, login, save, shot, openTemplate, openListView, lvRows, watch } from './lib.mjs';
const [base, tag, v65s] = process.argv.slice(2);
const v65 = v65s === '1';
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
const log = []; watch(page, log);
const out = {};
const count = n => page.evaluate(n => { const s = wp.data.select('core/block-editor'); return s.getClientIdsWithDescendants().filter(id => s.getBlockName(id) === n).length; }, n);
const saveIt = async () => {
  await page.locator('.editor-header__settings button, .edit-site-header-edit-mode__actions button', { hasText: /^Save$/ }).first().click();
  await page.waitForTimeout(1200);
  const p2 = page.locator('.entities-saved-states__panel').getByRole('button', { name: /^Save$/ }); if (await p2.count()) await p2.first().click();
  await page.waitForFunction(() => wp.data.select('core').__experimentalGetDirtyEntityRecords().length === 0, null, { timeout: 30000 }).catch(() => {});
  await page.waitForTimeout(800);
};
await openTemplate(page, base, v65);
// Delete/Backspace on each locked block (inside Edit pattern on WP 7)
for (const [sec, blk] of [['gm-creators', 'generation-maine/creators'], ['follow', 'generation-maine/follow'], ['follow', 'generation-maine/newsletter']]) {
  await page.evaluate(c => { const s = wp.data.select('core/block-editor'); const id = s.getClientIdsWithDescendants().find(id => s.getBlockName(id) === 'core/group' && (' ' + (s.getBlock(id).attributes.className || '') + ' ').includes(' ' + c + ' ')); wp.data.dispatch('core/block-editor').selectBlock(id); }, sec);
  await page.waitForTimeout(500);
  const ep = page.getByRole('button', { name: /^Edit pattern$/ }); if (await ep.count()) { await ep.first().click(); await page.waitForTimeout(1000); }
  await page.evaluate(n => { const s = wp.data.select('core/block-editor'); const id = s.getClientIdsWithDescendants().find(id => s.getBlockName(id) === n); wp.data.dispatch('core/block-editor').selectBlock(id); }, blk);
  await page.waitForTimeout(400);
  await page.keyboard.press('Delete'); await page.waitForTimeout(300); await page.keyboard.press('Backspace'); await page.waitForTimeout(300);
  out['afterDelete:' + blk] = await count(blk);
}
await openTemplate(page, base, v65);
// delete the Follow section from List View
await openListView(page);
const row = page.locator('.block-editor-list-view-tree tr').filter({ has: page.locator('.block-editor-list-view-block-select-button__title', { hasText: /^Follow$/ }) }).first();
await row.locator('a.block-editor-list-view-block-select-button').click(); await page.waitForTimeout(300);
await row.getByRole('button', { name: /Options/ }).click(); await page.waitForTimeout(400);
out.sectionMenu = (await page.getByRole('menuitem').allInnerTexts()).map(s => s.split('\n')[0]).filter(s => /Delete|Duplicate|Copy|Unlock|Detach/.test(s));
await page.getByRole('menuitem', { name: /^Delete/ }).click(); await page.waitForTimeout(600);
out.followAfterDelete = await count('generation-maine/follow');
await saveIt();
await openTemplate(page, base, v65);
await page.evaluate(() => wp.data.dispatch('core/block-editor').clearSelectedBlock());
await page.locator('button[aria-label="Block Inserter"], button[aria-label="Toggle block inserter"], .editor-document-tools__inserter-toggle, .edit-site-header-edit-mode__inserter-toggle').first().click(); await page.waitForTimeout(900);
await page.getByRole('tab', { name: 'Patterns' }).click(); await page.waitForTimeout(900);
await page.getByRole('button', { name: /^Generation Maine/ }).or(page.getByRole('tab', { name: /^Generation Maine/ })).first().click(); await page.waitForTimeout(2000);
const items = page.locator('.block-editor-block-patterns-list__item');
const n = await items.count(); out.patternList = [];
for (let i = 0; i < n; i++) out.patternList.push(((await items.nth(i).getAttribute('aria-label')) || '') + '|' + (await items.nth(i).innerText()).trim());
for (let i = 0; i < n; i++) if (out.patternList[i].split('|').some(s => s.trim() === 'Follow')) { await items.nth(i).click(); break; }
await page.waitForTimeout(2000);
await page.keyboard.press('Escape');
out.followAfterInsert = await count('generation-maine/follow');
out.topLevel = await page.evaluate(() => { const s = wp.data.select('core/block-editor'); const main = s.getBlockOrder('').map(id => s.getBlock(id)); return main.map(b => b.name + (b.attributes.className ? '.' + b.attributes.className : '') + ' [' + s.getBlockOrder(b.clientId).map(id => { const c = s.getBlock(id); return (c.attributes.metadata && c.attributes.metadata.name) || c.name; }).join(', ') + ']'); });
await saveIt();
const p = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await p.goto(base + '/', { waitUntil: 'networkidle' });
out.front = await p.evaluate(() => ({ follow: !!document.getElementById('follow'), newsletter: !!document.getElementById('newsletter'), followInMain: !!document.querySelector('main #follow'), followW: document.querySelector('.follow .w') ? Math.round(document.querySelector('.follow .w').getBoundingClientRect().width) : null, overflow: document.documentElement.scrollWidth - innerWidth }));
save(`${tag}-followreadd.json`, { out, log });
console.log(JSON.stringify(out, null, 1));
await browser.close();
