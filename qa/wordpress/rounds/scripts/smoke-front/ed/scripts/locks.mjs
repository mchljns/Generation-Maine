// Locked theme blocks: Options menu, Ctrl+Shift+D, the inserter, copy and paste. Header part (Logo, Phone menu button) and
// Front Page (Creators, Follow List, Newsletter Signup via Edit pattern; the mural in the hero).
// usage: node locks.mjs <base> <tag> <v65 0|1> [save]
import { launch, login, save, shot, openTemplate, openListView, lvRows, watch } from './lib.mjs';
const [base, tag, v65s, doSave] = process.argv.slice(2);
const v65 = v65s === '1';
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
const log = []; watch(page, log);
const out = {};
const count = (name) => page.evaluate((n) => { const s = wp.data.select('core/block-editor'); return s.getClientIdsWithDescendants().filter(id => s.getBlockName(id) === n).length; }, name);
const selectByName = (name, attr) => page.evaluate(([n, a]) => { const s = wp.data.select('core/block-editor'); const id = s.getClientIdsWithDescendants().find(id => s.getBlockName(id) === n && (!a || s.getBlock(id).attributes.name === a)); if (id) wp.data.dispatch('core/block-editor').selectBlock(id); return !!id; }, [name, attr]);
const optItems = async () => {
  const o = page.locator('.block-editor-block-toolbar, .block-editor-block-contextual-toolbar').getByRole('button', { name: /^Options$/ });
  if (!(await o.count())) return 'no options button';
  await o.first().click(); await page.waitForTimeout(500);
  const it = (await page.locator('[role="menuitem"], [role="menuitemcheckbox"]').allInnerTexts()).map(s => s.split('\n')[0]);
  const dup = page.getByRole('menuitem', { name: /^Duplicate/ });
  const dupDisabled = (await dup.count()) ? await dup.first().getAttribute('aria-disabled') : null;
  await page.keyboard.press('Escape'); await page.waitForTimeout(200);
  return { items: it, dupDisabled };
};
async function probe(label, blockName, attr) {
  const r = {};
  r.selected = await selectByName(blockName, attr);
  await page.waitForTimeout(500);
  r.before = await count(blockName);
  r.options = await optItems();
  // keyboard: focus the selected block in the canvas and press Ctrl+Shift+D
  await selectByName(blockName, attr); await page.waitForTimeout(300);
  await page.keyboard.press('Control+Shift+D'); await page.waitForTimeout(800);
  r.afterShortcut = await count(blockName);
  // the menu item, if offered
  await selectByName(blockName, attr); await page.waitForTimeout(300);
  const o = page.locator('.block-editor-block-toolbar, .block-editor-block-contextual-toolbar').getByRole('button', { name: /^Options$/ });
  if (await o.count()) {
    await o.first().click(); await page.waitForTimeout(400);
    const dup = page.getByRole('menuitem', { name: /^Duplicate/ });
    if (await dup.count() && (await dup.first().getAttribute('aria-disabled')) !== 'true') { await dup.first().click().catch(() => {}); await page.waitForTimeout(800); r.clickedDuplicate = true; }
    else await page.keyboard.press('Escape');
  }
  r.afterMenu = await count(blockName);
  out[label] = r;
}
// A. Header part
await openTemplate(page, base, v65, 'header', 'wp_template_part');
await probe('Logo', 'generation-maine/part', 'logo');
await probe('Phone menu button', 'generation-maine/part', 'menu');
await shot(page, `${tag}-locks-header`);
out.headerDirty = await page.evaluate(() => wp.data.select('core').__experimentalGetDirtyEntityRecords().map(r => r.name + ':' + r.key));
out.headerParts = await page.evaluate(() => { const s = wp.data.select('core/block-editor'); return s.getClientIdsWithDescendants().filter(id => s.getBlockName(id) === 'generation-maine/part').map(id => s.getBlock(id).attributes.name); });
if (doSave && out.headerParts.length > 2) {
  await page.locator('.editor-header__settings button, .edit-site-header-edit-mode__actions button', { hasText: /^Save$/ }).first().click();
  await page.waitForTimeout(1500);
  const p2 = page.locator('.entities-saved-states__panel').getByRole('button', { name: /^Save$/ }); if (await p2.count()) await p2.first().click();
  await page.waitForTimeout(3000);
  out.headerSaved = true;
}
// B. Front Page sections
await openTemplate(page, base, v65);
// In WP 7 the sections are pattern sections: enter Edit pattern through the block toolbar or sidebar after selecting the section
async function editPatternFor(sectionClass) {
  const ok = await page.evaluate((c) => { const s = wp.data.select('core/block-editor'); const id = s.getClientIdsWithDescendants().find(id => s.getBlockName(id) === 'core/group' && (' ' + (s.getBlock(id).attributes.className || '') + ' ').includes(' ' + c + ' ')); if (id) wp.data.dispatch('core/block-editor').selectBlock(id); return !!id; }, sectionClass);
  await page.waitForTimeout(600);
  const b = page.getByRole('button', { name: /^Edit pattern$/ });
  const n = await b.count();
  if (n) { await b.first().click(); await page.waitForTimeout(1200); }
  return { found: ok, editPattern: n };
}
out.editFollow = await editPatternFor('follow');
await probe('Follow List', 'generation-maine/follow');
await probe('Newsletter Signup', 'generation-maine/newsletter');
out.editCreators = await editPatternFor('gm-creators');
await probe('Creators', 'generation-maine/creators');
out.editHero = await editPatternFor('hero');
await probe('Maine mural', 'generation-maine/part', 'mural');
await shot(page, `${tag}-locks-front`);
// inserter: search each block
const ins = page.locator('button[aria-label="Block Inserter"], button[aria-label="Toggle block inserter"], .editor-document-tools__inserter-toggle, .edit-site-header-edit-mode__inserter-toggle').first();
await ins.click(); await page.waitForTimeout(900);
out.inserter = {};
for (const q of ['Creators', 'Follow List', 'Newsletter Signup', 'Generation Maine Part', 'mural', 'Site Footer']) {
  await page.locator('.block-editor-inserter__search input, input[type="search"]').first().fill(q); await page.waitForTimeout(1200);
  out.inserter[q] = await page.locator('.block-editor-block-types-list__item').evaluateAll(es => es.map(e => e.innerText.trim() + (e.getAttribute('aria-disabled') === 'true' || e.disabled ? ' [disabled]' : '')));
}
await shot(page, `${tag}-locks-inserter`);
await page.keyboard.press('Escape');
// copy and paste the Creators block (Ctrl+C, Ctrl+V) and see what the editor says
await selectByName('generation-maine/creators'); await page.waitForTimeout(400);
out.frontDirtyBeforePaste = await page.evaluate(() => wp.data.select('core').__experimentalGetDirtyEntityRecords().map(r => r.name + ':' + r.key));
save(`${tag}-locks.json`, { out, log });
console.log(JSON.stringify(out, null, 1));
console.log(log.filter(l => !/CERT/.test(l)).join('\n'));
await browser.close();
