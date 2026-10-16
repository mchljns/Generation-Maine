// Duplicate the Logo and Phone menu button in the Header part and the mural in the hero (Ctrl+Shift+D), save, then look at the page.
import { launch, login, save, shot, openTemplate, watch } from './lib.mjs';
const [base, tag, v65s] = process.argv.slice(2);
const v65 = v65s === '1';
const browser = await launch();
const { page, ctx } = await login(browser, base, { w: 1440, h: 900 });
const log = []; watch(page, log);
const sel = (n, a) => page.evaluate(([n, a]) => { const s = wp.data.select('core/block-editor'); const id = s.getClientIdsWithDescendants().find(id => s.getBlockName(id) === n && (!a || s.getBlock(id).attributes.name === a)); if (id) wp.data.dispatch('core/block-editor').selectBlock(id); return !!id; }, [n, a]);
const saveIt = async () => {
  await page.locator('.editor-header__settings button, .edit-site-header-edit-mode__actions button', { hasText: /^Save$/ }).first().click();
  await page.waitForTimeout(1500);
  const p2 = page.locator('.entities-saved-states__panel').getByRole('button', { name: /^Save$/ }); if (await p2.count()) await p2.first().click();
  await page.waitForFunction(() => wp.data.select('core').__experimentalGetDirtyEntityRecords().length === 0, null, { timeout: 30000 }).catch(() => {});
  await page.waitForTimeout(1500);
};
await openTemplate(page, base, v65, 'header', 'wp_template_part');
for (const a of ['logo', 'menu']) { await sel('generation-maine/part', a); await page.waitForTimeout(300); await page.keyboard.press('Control+Shift+D'); await page.waitForTimeout(800); }
const headerParts = await page.evaluate(() => { const s = wp.data.select('core/block-editor'); return s.getClientIdsWithDescendants().filter(id => s.getBlockName(id) === 'generation-maine/part').map(id => s.getBlock(id).attributes.name); });
await saveIt();
await openTemplate(page, base, v65);
const ok = await page.evaluate(() => { const s = wp.data.select('core/block-editor'); const id = s.getClientIdsWithDescendants().find(id => s.getBlockName(id) === 'core/group' && / hero /.test(' ' + (s.getBlock(id).attributes.className || '') + ' ')); wp.data.dispatch('core/block-editor').selectBlock(id); return !!id; });
await page.waitForTimeout(500);
const ep = page.getByRole('button', { name: /^Edit pattern$/ }); if (await ep.count()) { await ep.first().click(); await page.waitForTimeout(1000); }
await sel('generation-maine/part', 'mural'); await page.waitForTimeout(300); await page.keyboard.press('Control+Shift+D'); await page.waitForTimeout(800);
const frontParts = await page.evaluate(() => { const s = wp.data.select('core/block-editor'); return s.getClientIdsWithDescendants().filter(id => s.getBlockName(id) === 'generation-maine/part').map(id => s.getBlock(id).attributes.name); });
await shot(page, `${tag}-dupparts-editor`);
await saveIt();
const res = {};
for (const [w, h] of [[1440, 900], [390, 844]]) {
  const c2 = await browser.newContext({ viewport: { width: w, height: h }, ...(w < 500 ? { isMobile: true, hasTouch: true } : {}) });
  const p = await c2.newPage();
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto(base + '/', { waitUntil: 'networkidle' });
  await p.waitForTimeout(1500);
  res[w] = await p.evaluate(() => {
    const ids = [...document.querySelectorAll('[id]')].map(e => e.id); const dup = ids.filter((x, i) => ids.indexOf(x) !== i);
    const vis = s => [...document.querySelectorAll(s)].map(e => { const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height), getComputedStyle(e).display]; });
    return { dupIds: [...new Set(dup)], logos: vis('.gm-bar .logo, header a.logo, .gm-bar a[aria-label*="home"]'), menus: vis('.gm-bar .menu, header button.menu'), murals: vis('.hero svg.mural, .hero .mural'), overflow: document.documentElement.scrollWidth - innerWidth };
  });
  res[w].errs = errs;
  await p.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-dupparts-front-${w}.png` });
  if (w === 390) {
    // tap each menu button: does the sheet open?
    const btns = p.locator('.gm-bar .menu, header button.menu');
    const n = await btns.count(); res.menuTaps = [];
    for (let i = 0; i < n; i++) { const b = btns.nth(i); if (!(await b.isVisible())) { res.menuTaps.push('hidden'); continue; } await b.tap(); await p.waitForTimeout(600); res.menuTaps.push(await p.evaluate(() => [...document.querySelectorAll('.gm-bar .menu, header button.menu')].map(b => b.getAttribute('aria-expanded')).join(','))); await p.keyboard.press('Escape'); await p.waitForTimeout(400); }
  }
  await c2.close();
}
save(`${tag}-dupparts.json`, { headerParts, frontParts, res, log });
console.log(JSON.stringify({ headerParts, frontParts, res }, null, 1));
await browser.close();
