// C06: what a paragraph's and a heading's Typography panel offers in the post editor (WordPress 6.5 and 7.1).
//   GMB=<base> node c06.mjs <run>
import { browser, login, B, W } from './lib2.mjs';
import fs from 'fs';
const run = process.argv[2] || '1';
const out = { run };
const b = await browser(); const ctx = await b.newContext({ viewport: { width: 1440, height: 1000 } }); const page = await login(ctx, 'admin', 'adminpass');
await page.goto(B + '/wp-admin/post-new.php'); await page.waitForFunction(() => window.wp && wp.data && wp.data.select('core/block-editor'), null, { timeout: 60000 }); await page.waitForTimeout(3000);
for (let i = 0; i < 3; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click(); await page.waitForTimeout(400); } }
out.version = await page.evaluate(() => document.body.className.match(/branch-[\d-]+/)?.[0]);
out.fontSizesSetting = await page.evaluate(() => {
  const s = wp.data.select('core/block-editor').getSettings();
  return { fontSizes: (s.fontSizes || []).map(f => f.name + ' ' + f.size), featuresFontSizes: s.__experimentalFeatures?.typography?.fontSizes };
});
for (const [name, block] of [['paragraph', 'core/paragraph'], ['heading', 'core/heading']]) {
  await page.evaluate(n => { const blk = wp.blocks.createBlock(n, { content: 'Test ' + n }); wp.data.dispatch('core/block-editor').insertBlocks(blk); wp.data.dispatch('core/block-editor').selectBlock(blk.clientId); }, block);
  await page.waitForTimeout(800);
  // open the settings sidebar on the block tab
  const settings = page.locator('button[aria-label="Settings"]').first();
  if ((await settings.getAttribute('aria-pressed')) !== 'true' && (await settings.getAttribute('aria-expanded')) !== 'true') { await settings.click(); await page.waitForTimeout(500); }
  const blockTab = page.locator('button[role="tab"]', { hasText: /^(Block|Paragraph|Heading)$/ }).first(); if (await blockTab.count()) { await blockTab.click().catch(() => {}); await page.waitForTimeout(400); }
  const r = {};
  r.panels = await page.$$eval('.block-editor-block-inspector .components-tools-panel-header h2, .block-editor-block-inspector .components-panel__body-title', h => h.map(x => x.textContent.trim()));
  const typo = page.locator('.block-editor-block-inspector .components-tools-panel', { hasText: 'Typography' }).first();
  r.typographyPanel = (await typo.count()) > 0;
  if (r.typographyPanel) {
    r.panelText = (await typo.innerText()).replace(/\s+/g, ' ').trim();
    r.fontSizePicker = await typo.locator('.components-font-size-picker, .block-editor-font-size-picker, input[type=number], [role=radiogroup], select').count();
    const menuBtn = typo.locator('.components-tools-panel-header button').first();
    await menuBtn.click(); await page.waitForTimeout(500);
    r.menuItems = await page.$$eval('.components-dropdown-menu__menu [role="menuitemcheckbox"], .components-dropdown-menu__menu [role="menuitem"], .components-tools-panel-header__menu .components-menu-item__button', els => els.map(e => [e.textContent.trim(), e.getAttribute('aria-checked'), e.getAttribute('aria-disabled') || String(e.disabled)]));
    await page.screenshot({ path: `${W}/shots/c06-${run}-${name}.png` });
    await page.keyboard.press('Escape'); await page.waitForTimeout(300);
  }
  out[name] = r;
}
fs.writeFileSync(`${W}/c06-${run}.json`, JSON.stringify(out, null, 1)); console.log(JSON.stringify(out, null, 1));
await b.close();
