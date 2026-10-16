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
out.frontBefore = await front('before');
// A. Header part
await openTemplate(page, base, v65, 'header', 'wp_template_part');
out.headerStart = await parts();
await selPart('logo'); await page.waitForTimeout(400);
out.logoOptions = await optionsDup();
await selPart('menu'); await page.waitForTimeout(400);
await page.keyboard.press('Control+Shift+D'); await page.waitForTimeout(900);
out.headerAfter = await parts();
out.headerNotes = await notes();
await shot(page, `${tag}-dup-header-editor`);
await saveIt();
// B. Front page: hero mural
let f = await openTemplate(page, base, v65);
out.frontCanvasNotes = await notes();
await page.evaluate(() => { const s = wp.data.select('core/block-editor'); const id = s.getClientIdsWithDescendants().find(id => s.getBlockName(id) === 'core/group' && / hero /.test(' ' + (s.getBlock(id).attributes.className || '') + ' ')); wp.data.dispatch('core/block-editor').selectBlock(id); });
await page.waitForTimeout(500);
const ep = page.getByRole('button', { name: /^Edit pattern$/ }); out.editPattern = await ep.count(); if (out.editPattern) { await ep.first().click(); await page.waitForTimeout(1000); }
await selPart('mural'); await page.waitForTimeout(400);
await page.keyboard.press('Control+Shift+D'); await page.waitForTimeout(900);
out.frontAfter = await parts();
out.frontNotesAfter = await notes();
await shot(page, `${tag}-dup-front-editor`);
const fr = await (await page.$('iframe[name="editor-canvas"]')).contentFrame();
const muralCopy = fr.locator('.block-editor-warning').filter({ hasText: /mural/i }).first();
if (await muralCopy.count()) await muralCopy.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-mural-copy-note.png` }).catch(() => {});
await saveIt();
out.frontDup = await front('dup');
save(`${tag}-dupparts2.json`, { out, log });
console.log(JSON.stringify(out, null, 1));
await browser.close();
