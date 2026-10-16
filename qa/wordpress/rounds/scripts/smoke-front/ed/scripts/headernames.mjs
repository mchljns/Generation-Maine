// Header via Edit original (WP 7) or the Header part (6.5): rename the three labels (one with an apostrophe) and the button,
// save, then check the bar, the phone menu and the footer on the front page and on a post, at 1440 and 390.
import { launch, login, save, shot, openTemplate, canvas, watch } from './lib.mjs';
const [base, tag, v65s, postPath = '/hello-world/'] = process.argv.slice(2);
const v65 = v65s === '1';
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
const log = []; watch(page, log);
let f;
if (v65) {
  f = await openTemplate(page, base, true, 'header', 'wp_template_part');
} else {
  f = await openTemplate(page, base, false);
  await f.locator('header.wp-block-template-part').first().click({ position: { x: 400, y: 20 } });
  await page.waitForTimeout(600);
  await page.getByRole('button', { name: /Edit original/ }).first().click();
  await page.waitForTimeout(3500);
  f = await canvas(page);
  await page.waitForTimeout(1200);
}
const labels = { About: 'Mission', Creators: 'Who’s here', Follow: 'Channels' };
for (const [from, to] of Object.entries(labels)) {
  const a = f.locator('nav a', { hasText: from }).first();
  await a.click(); await page.waitForTimeout(200);
  await page.keyboard.press('Control+a');
  await page.keyboard.type(to);
  await page.waitForTimeout(300);
}
const cta = f.locator('.cta a, .cta .wp-block-button__link').first();
await cta.click(); await page.keyboard.press('Control+a'); await page.keyboard.type('Join the list');
await page.waitForTimeout(500);
const navHtml = await f.locator('nav').first().evaluate(n => [...n.querySelectorAll('a')].map(a => a.getAttribute('href') + '|' + a.textContent));
await page.locator('.editor-header__settings button, .edit-site-header-edit-mode__actions button', { hasText: /^Save$/ }).first().click();
await page.waitForTimeout(1200);
const p2 = page.locator('.entities-saved-states__panel').getByRole('button', { name: /^Save$/ }); if (await p2.count()) await p2.first().click();
await page.waitForFunction(() => wp.data.select('core').__experimentalGetDirtyEntityRecords().length === 0, null, { timeout: 30000 }).catch(() => {});
await page.waitForTimeout(1000);
const snack = await page.locator('.components-snackbar').allInnerTexts();
const res = {};
for (const path of ['/', postPath]) for (const w of [1440, 390]) {
  const c = await browser.newContext({ viewport: { width: w, height: 900 }, ...(w < 500 ? { isMobile: true, hasTouch: true } : {}) });
  const p = await c.newPage();
  await p.goto(base + path, { waitUntil: 'networkidle' });
  const r = await p.evaluate(() => ({
    bar: [...document.querySelectorAll('.gm-bar nav a')].map(a => a.textContent.trim() + ' -> ' + a.getAttribute('href')),
    cta: [...document.querySelectorAll('.gm-bar .cta a')].map(a => a.textContent.trim() + ' -> ' + a.getAttribute('href')),
    sheet: [...document.querySelectorAll('#gm-menu a, .sheet a, [id*="menu"] nav a')].map(a => a.textContent.trim() + ' -> ' + a.getAttribute('href')),
    footer: [...document.querySelectorAll('footer a, .site a')].filter(a => /Mission|Who|Channels|Join|About|Creators|Follow/.test(a.textContent)).map(a => a.textContent.trim() + ' -> ' + a.getAttribute('href')),
  }));
  if (w === 390) {
    const m = p.locator('.gm-bar .menu').first();
    if (await m.isVisible()) { await m.tap(); await p.waitForTimeout(600); r.sheetVisible = await p.evaluate(() => [...document.querySelectorAll('a')].filter(a => { const s = getComputedStyle(a); const rr = a.getBoundingClientRect(); return /Mission|Who|Channels/.test(a.textContent) && rr.width > 0 && s.visibility !== 'hidden' && rr.top < innerHeight; }).map(a => a.textContent.trim())); await p.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-names-sheet-${path.replace(/\W/g, '_')}.png` }); }
  }
  res[path + '@' + w] = r;
  await c.close();
}
save(`${tag}-headernames.json`, { navHtml, snack, res, log });
console.log(JSON.stringify({ navHtml, snack, res }, null, 1));
await browser.close();
