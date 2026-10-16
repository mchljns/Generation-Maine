// Round 2 passed checks for in-place edits on the Front Page: lede, hero button text and link, About photo (Replace > Upload),
// aim and note, creators heading, follow heading and lede, newsletter label and heading. Save, reload (0 invalid blocks), then
// read the page at 1440 and 390.
import { launch, login, save, shot, openTemplate, watch } from './lib.mjs';
const [base, tag, v65s] = process.argv.slice(2);
const v65 = v65s === '1';
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
const log = []; watch(page, log);
const f = await openTemplate(page, base, v65);
const K = page.keyboard;
const edit = async (sel, text) => { const el = f.locator(sel).first(); await el.scrollIntoViewIfNeeded(); await el.click(); await K.press('Control+a'); await K.type(text); await page.waitForTimeout(300); };
const out = {};
await edit('.hero p.lede', 'A test lede from the editor, about the rules people live with in Maine.');
await edit('.hero .wp-block-button__link', 'See the clips');
// link popover: Edit link, type the new anchor
const editLink = page.getByRole('button', { name: 'Edit link' }).first();
if (await editLink.count()) {
  await editLink.click(); await page.waitForTimeout(400);
  const input = page.locator('.block-editor-link-control input').first();
  await input.fill('#creators');
  const apply = page.locator('.block-editor-link-control').getByRole('button', { name: /^(Save|Apply|Submit)$/ });
  if (await apply.count()) await apply.first().click(); else await K.press('Enter');
  await page.waitForTimeout(500);
  out.linkEdited = true;
} else {
  // older UI: Ctrl+K on the button opens the link control
  await K.press('Control+k'); await page.waitForTimeout(500);
  const input = page.locator('.block-editor-link-control input').first();
  if (await input.count()) { await input.fill('#creators'); await K.press('Enter'); out.linkEdited = 'ctrl+k'; }
}
// About photo: Replace > Upload
const fig = f.locator('.about figure').first();
await fig.scrollIntoViewIfNeeded(); await fig.click({ force: true }); await page.waitForTimeout(600);
const rep = page.locator('.block-editor-block-toolbar').getByRole('button', { name: 'Replace' });
if (await rep.count()) {
  await rep.first().click(); await page.waitForTimeout(500);
  const [chooser] = await Promise.all([page.waitForEvent('filechooser'), page.getByRole('menuitem', { name: /Upload/ }).first().click()]);
  await chooser.setFiles('/tmp/claude-0/wptest/media/sample-portrait.jpg');
  for (let i = 0; i < 60; i++) { const src = await f.locator('.about figure img').first().getAttribute('src').catch(() => ''); if (src && /uploads/.test(src)) break; await page.waitForTimeout(500); }
  out.photo = await f.locator('.about figure img').first().getAttribute('src');
}
await edit('.about p.big', 'We want young people to stay in Maine and to say what it costs them.');
await edit('.about p.note', 'Edited note from the editor test.');
await edit('.stories-head h2, .gm-creators h2', 'The people');
await edit('.follow .head h2', 'Find us here');
await edit('.follow .head p.lede', 'Edited follow lede.');
await edit('.nl p.k', 'Weekly email');
await edit('.nl h3', 'Get the paperwork');
await page.locator('.editor-header__settings button, .edit-site-header-edit-mode__actions button', { hasText: /^Save$/ }).first().click();
await page.waitForTimeout(1200);
const p2 = page.locator('.entities-saved-states__panel').getByRole('button', { name: /^Save$/ }); if (await p2.count()) await p2.first().click();
await page.waitForFunction(() => wp.data.select('core').__experimentalGetDirtyEntityRecords().length === 0, null, { timeout: 60000 }).catch(() => { out.saveTimeout = true; });
await page.waitForTimeout(1000);
out.snack = await page.locator('.components-snackbar').allInnerTexts();
// reload and count invalid blocks
await openTemplate(page, base, v65);
out.afterReload = await page.evaluate(() => { const s = wp.data.select('core/block-editor'); let n = 0; const bad = []; const walk = ids => ids.forEach(id => { const b = s.getBlock(id); n++; if (b.isValid === false) bad.push(b.name); walk(s.getBlockOrder(id)); }); walk(s.getBlockOrder('')); return { n, bad, dirty: wp.data.select('core').__experimentalGetDirtyEntityRecords().length }; });
out.recovery = await page.locator('text=/Attempt recovery|Attempt Block Recovery|unexpected or invalid content/').count();
for (const w of [1440, 390]) {
  const c = await browser.newContext({ viewport: { width: w, height: 900 }, ...(w < 500 ? { isMobile: true, hasTouch: true } : {}) });
  const p = await c.newPage();
  await p.goto(base + '/', { waitUntil: 'networkidle' });
  out['front' + w] = await p.evaluate(() => {
    const t = s => { const e = document.querySelector(s); return e ? e.textContent.trim() : null; };
    const img = document.querySelector('.about img');
    return { lede: t('.hero p.lede'), btn: t('.hero .wp-block-button__link'), btnHref: document.querySelector('.hero .wp-block-button__link').getAttribute('href'), aim: t('.about p.big'), note: t('.about p.note'), photo: img && img.getAttribute('src'), photoSize: img && [img.width, img.height], photoLoading: img && img.getAttribute('loading'), creatorsH: t('#creators h2'), followH: t('.follow .head h2'), followLede: t('.follow .head p.lede'), nlK: t('.nl p.k'), nlH: t('.nl h3'), overflow: document.documentElement.scrollWidth - innerWidth };
  });
  await c.close();
}
save(`${tag}-edits.json`, { out, log });
console.log(JSON.stringify(out, null, 1));
await browser.close();
