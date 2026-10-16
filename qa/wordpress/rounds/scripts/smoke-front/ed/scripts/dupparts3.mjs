// Duplicate the Logo and Phone menu button in the Header part and the mural in the hero (Options menu and Ctrl+Shift+D);
// read the editor notes; save; look at the page (ids, logos, menus, murals, menu taps); then Find original and Remove on
// each copy; save; look at the page again. usage: node dupparts2.mjs <base> <tag> <v65 0|1>
import { launch, login, save, shot, openTemplate, watch } from './lib.mjs';
const [base, tag, v65s] = process.argv.slice(2);
const v65 = v65s === '1';
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
const log = []; watch(page, log);
const out = {};
const parts = () => page.evaluate(() => { const s = wp.data.select('core/block-editor'); return s.getClientIdsWithDescendants().filter(id => s.getBlockName(id) === 'generation-maine/part').map(id => s.getBlock(id).attributes.name + (s.getBlock(id).attributes.lock && Object.keys(s.getBlock(id).attributes.lock).length ? '(locked)' : '')); });
const selPart = (name, nth = 0) => page.evaluate(([n, k]) => { const s = wp.data.select('core/block-editor'); const ids = s.getClientIdsWithDescendants().filter(id => s.getBlockName(id) === 'generation-maine/part' && s.getBlock(id).attributes.name === n); if (ids[k]) wp.data.dispatch('core/block-editor').selectBlock(ids[k]); return ids[k] || null; }, [name, nth]);
const selected = () => page.evaluate(() => wp.data.select('core/block-editor').getSelectedBlockClientId());
const notes = async () => { const f = await (await page.$('iframe[name="editor-canvas"]')).contentFrame(); return f.evaluate(() => [...document.querySelectorAll('.block-editor-warning')].map(w => w.innerText.replace(/\s+/g, ' '))); };
const saveIt = async () => {
  await page.locator('.editor-header__settings button, .edit-site-header-edit-mode__actions button', { hasText: /^Save$/ }).first().click();
  await page.waitForTimeout(1500);
  const p2 = page.locator('.entities-saved-states__panel').getByRole('button', { name: /^Save$/ }); if (await p2.count()) await p2.first().click();
  await page.waitForFunction(() => wp.data.select('core').__experimentalGetDirtyEntityRecords().length === 0, null, { timeout: 30000 }).catch(() => { out.saveTimeout = (out.saveTimeout || 0) + 1; });
  await page.waitForTimeout(1500);
};
const optionsDup = async () => {
  const o = page.locator('.block-editor-block-toolbar, .block-editor-block-contextual-toolbar').getByRole('button', { name: /^Options$/ });
  if (!(await o.count())) return 'no options';
  await o.first().click(); await page.waitForTimeout(500);
  const items = (await page.locator('[role="menuitem"], [role="menuitemcheckbox"]').allInnerTexts()).map(s => s.split('\n')[0]);
  const dup = page.getByRole('menuitem', { name: /^Duplicate/ });
  let clicked = false;
  if (await dup.count() && (await dup.first().getAttribute('aria-disabled')) !== 'true') { await dup.first().click(); clicked = true; await page.waitForTimeout(900); } else await page.keyboard.press('Escape');
  return { items, clicked };
};
const front = async (label) => {
  const r = {};
  for (const [w, h] of [[1440, 900], [390, 844]]) {
    const c2 = await browser.newContext({ viewport: { width: w, height: h }, ...(w < 500 ? { isMobile: true, hasTouch: true } : {}) });
    const p = await c2.newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e)));
    await p.goto(base + '/', { waitUntil: 'networkidle' }); await p.waitForTimeout(1200);
    r[w] = await p.evaluate(() => {
      const ids = [...document.querySelectorAll('[id]')].map(e => e.id); const dup = ids.filter((x, i) => ids.indexOf(x) !== i);
      const vis = s => [...document.querySelectorAll(s)].map(e => { const q = e.getBoundingClientRect(); return [Math.round(q.left), Math.round(q.top), Math.round(q.width), Math.round(q.height), getComputedStyle(e).display]; });
      return { dupIds: [...new Set(dup)], logos: vis('header a[aria-label*="home"]'), menus: vis('header button.menu'), murals: vis('.hero svg.mural, .hero .mural'), partWrappers: document.querySelectorAll('.wp-block-generation-maine-part, .gm-part').length, emptyParts: [...document.querySelectorAll('.wp-block-generation-maine-part, .gm-part')].filter(e => !e.innerHTML.trim()).length, overflow: document.documentElement.scrollWidth - innerWidth, barH: Math.round(document.querySelector('header').getBoundingClientRect().height) };
    });
    r[w].errs = errs;
    await p.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-${label}-front-${w}.png` });
    if (w === 390) {
      const b = p.locator('header button.menu').first();
      if (await b.count() && await b.isVisible()) { await b.tap(); await p.waitForTimeout(700); r.menuTap = await p.evaluate(() => ({ expanded: document.querySelector('header button.menu').getAttribute('aria-expanded'), sheetVisible: (() => { const s = document.getElementById('sheet'); return s ? getComputedStyle(s).visibility + '/' + Math.round(s.getBoundingClientRect().height) : 'no sheet'; })() })); }
    }
    await c2.close();
  }
  return r;
};

out.frontDup = await front('dup');
let f = await openTemplate(page, base, v65);
out.frontCanvasParts = await parts();
out.frontCanvasNotes = await notes();
await shot(page, `${tag}-dup-front-editor-reopen`);
const cf = await (await page.$('iframe[name="editor-canvas"]')).contentFrame();
const muralNote = cf.locator('.block-editor-warning').filter({ hasText: /mural/i }).first();
out.muralNote = await muralNote.count();
if (out.muralNote) await muralNote.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-mural-copy-note.png` }).catch(() => {});
const origId = await page.evaluate(() => { const s = wp.data.select('core/block-editor'); return s.getClientIdsWithDescendants().find(id => s.getBlockName(id) === 'generation-maine/part' && s.getBlock(id).attributes.name === 'mural'); });
// without Edit pattern first
const tryClick = async (loc) => { try { await loc.click({ timeout: 4000 }); return 'clicked'; } catch (e) { return 'blocked: ' + String(e.message).split('\n')[0].slice(0, 120); } };
out.findNoEdit = await tryClick(muralNote.getByRole('button', { name: 'Find original' }));
await page.waitForTimeout(700);
out.findSelectsOriginal = (await selected()) === origId;
out.selectedName = await page.evaluate(() => { const s = wp.data.select('core/block-editor'); const id = s.getSelectedBlockClientId(); return id ? s.getBlockName(id) + ' ' + (s.getBlock(id).attributes.name || s.getBlock(id).attributes.className || '') : null; });
let n0 = (await parts()).length;
out.removeNoEdit = await tryClick(muralNote.getByRole('button', { name: 'Remove' }));
await page.waitForTimeout(900);
out.removedNoEdit = n0 - (await parts()).length;
if (!out.removedNoEdit) {
  await page.evaluate(() => { const s = wp.data.select('core/block-editor'); const id = s.getClientIdsWithDescendants().find(id => s.getBlockName(id) === 'core/group' && / hero /.test(' ' + (s.getBlock(id).attributes.className || '') + ' ')); wp.data.dispatch('core/block-editor').selectBlock(id); });
  await page.waitForTimeout(500);
  const ep = page.getByRole('button', { name: /^Edit pattern$/ }); out.editPattern = await ep.count(); if (out.editPattern) { await ep.first().click(); await page.waitForTimeout(1000); }
  n0 = (await parts()).length;
  out.removeWithEdit = await tryClick(cf.locator('.block-editor-warning').filter({ hasText: /mural/i }).first().getByRole('button', { name: 'Remove' }));
  await page.waitForTimeout(900);
  out.removedWithEdit = n0 - (await parts()).length;
}
out.afterRemoveFront = await parts();
out.dirtyAfterRemove = await page.evaluate(() => wp.data.select('core').__experimentalGetDirtyEntityRecords().map(r => r.name + ':' + (r.key || '')));
await saveIt();
await openTemplate(page, base, v65, 'header', 'wp_template_part');
const hf = await (await page.$('iframe[name="editor-canvas"]')).contentFrame();
out.headerNotes = await notes();
const lnote = hf.locator('.block-editor-warning').first();
if (await lnote.count()) await lnote.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-header-copy-note.png` }).catch(() => {});
await shot(page, `${tag}-dup-header-reopen`);
out.headerFind = await tryClick(hf.getByRole('button', { name: 'Find original' }).first());
await page.waitForTimeout(600);
out.headerFindSelected = await page.evaluate(() => { const s = wp.data.select('core/block-editor'); const id = s.getSelectedBlockClientId(); const ids = s.getClientIdsWithDescendants().filter(x => s.getBlockName(x) === 'generation-maine/part'); return id ? s.getBlock(id).attributes.name + ' index ' + ids.indexOf(id) : null; });
out.headerRemoves = [];
for (let i = 0; i < 4; i++) { const rb = hf.getByRole('button', { name: 'Remove' }); if (!(await rb.count())) break; out.headerRemoves.push(await tryClick(rb.first())); await page.waitForTimeout(900); }
out.headerAfterRemove = await parts();
out.headerNotesAfterRemove = await notes();
await saveIt();
out.frontAfterRemove = await front('removed');
save(`${tag}-dupparts3.json`, { out, log });
console.log(JSON.stringify(out, null, 1));
await browser.close();
