// Change the hero lede in the Site Editor and save; print the Hero pattern description the sidebar shows for a hero block.
import { launch, login, save, shot, openTemplate } from './lib.mjs';
const [base, tag, text] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
const f = await openTemplate(page, base, false);
const out = {};
const lede = f.locator('.hero p.lede').first();
await lede.click(); await page.waitForTimeout(400);
const side = page.locator('.interface-complementary-area').first();
if (!(await side.count())) { await page.locator('.editor-header__settings').getByRole('button', { name: 'Settings', exact: true }).click().catch(() => {}); await page.waitForTimeout(600); }
out.sidebarBefore = (await side.innerText().catch(() => '')).replace(/\s+/g, ' ').slice(0, 700);
if (text) {
  await page.keyboard.press('Control+a'); await page.keyboard.type(text); await page.waitForTimeout(300);
  await page.locator('.editor-header__settings button', { hasText: /^Save$/ }).first().click();
  await page.waitForTimeout(1200);
  const p2 = page.locator('.entities-saved-states__panel').getByRole('button', { name: /^Save$/ }); if (await p2.count()) await p2.first().click();
  await page.waitForFunction(() => wp.data.select('core').__experimentalGetDirtyEntityRecords().length === 0, null, { timeout: 30000 }).catch(() => {});
  out.snack = await page.locator('.components-snackbar').allInnerTexts();
}
await shot(page, `${tag}-hero-sidebar`);
save(`${tag}-ledeedit.json`, out);
console.log(JSON.stringify(out, null, 1));
await browser.close();
