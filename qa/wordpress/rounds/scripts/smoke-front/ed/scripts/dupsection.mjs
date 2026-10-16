// Duplicate whole sections (Creators, Follow) from List View > Options > Duplicate; what the editor says; save; the page.
import { launch, login, save, shot, openTemplate, openListView, watch } from './lib.mjs';
const [base, tag, v65s] = process.argv.slice(2);
const v65 = v65s === '1';
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
const log = []; watch(page, log);
const out = {};
const count = n => page.evaluate(n => { const s = wp.data.select('core/block-editor'); return s.getClientIdsWithDescendants().filter(id => s.getBlockName(id) === n).length; }, n);
const f = await openTemplate(page, base, v65);
await openListView(page);
for (const name of ['Creators', 'Follow']) {
  const row = page.locator('.block-editor-list-view-tree tr').filter({ has: page.locator('.block-editor-list-view-block-select-button__title', { hasText: new RegExp('^' + name + '$') }) }).first();
  await row.locator('a.block-editor-list-view-block-select-button').click(); await page.waitForTimeout(300);
  await row.getByRole('button', { name: /Options/ }).click(); await page.waitForTimeout(400);
  const dup = page.getByRole('menuitem', { name: /^Duplicate/ });
  out[name + ':dupOffered'] = await dup.count();
  if (await dup.count()) { await dup.first().click(); await page.waitForTimeout(1200); } else await page.keyboard.press('Escape');
}
out.counts = { creators: await count('generation-maine/creators'), follow: await count('generation-maine/follow'), newsletter: await count('generation-maine/newsletter') };
out.warnings = await f.evaluate(() => [...document.querySelectorAll('.block-editor-warning')].map(w => w.innerText.replace(/\s+/g, ' ')));
await shot(page, `${tag}-dupsection-editor`);
await page.locator('.editor-header__settings button, .edit-site-header-edit-mode__actions button', { hasText: /^Save$/ }).first().click();
await page.waitForTimeout(1200);
const p2 = page.locator('.entities-saved-states__panel').getByRole('button', { name: /^Save$/ }); if (await p2.count()) await p2.first().click();
await page.waitForFunction(() => wp.data.select('core').__experimentalGetDirtyEntityRecords().length === 0, null, { timeout: 30000 }).catch(() => {});
for (const w of [1440, 390]) {
  const p = await browser.newPage({ viewport: { width: w, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto(base + '/', { waitUntil: 'networkidle' });
  out['front' + w] = await p.evaluate(() => { const ids = [...document.querySelectorAll('[id]')].map(e => e.id); return { dupIds: [...new Set(ids.filter((x, i) => ids.indexOf(x) !== i))], steppers: document.querySelectorAll('.stage').length, rosters: document.querySelectorAll('.tile').length, follows: document.querySelectorAll('section.follow').length, forms: document.querySelectorAll('form').length, overflow: document.documentElement.scrollWidth - innerWidth }; });
  out['front' + w].errs = errs;
  await p.close();
}
save(`${tag}-dupsection.json`, { out, log });
console.log(JSON.stringify(out, null, 1));
await browser.close();
