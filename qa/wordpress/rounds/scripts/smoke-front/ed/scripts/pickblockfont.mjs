// Styles > Blocks > <block> > Font: pick a font and save (theme 3.1.0).
import { launch, login, save, shot, guide } from './lib.mjs';
const [base, tag, block, pick] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 1000 });
const out = {};
await page.goto(base + '/wp-admin/site-editor.php?p=%2Fstyles', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(6000); await guide(page);
await page.getByRole('button', { name: /^Blocks$/ }).first().click(); await page.waitForTimeout(1200);
await page.locator('input[type="search"]').first().fill(block); await page.waitForTimeout(800);
await page.getByRole('button', { name: new RegExp('^' + block + '$') }).first().click(); await page.waitForTimeout(1500);
out.panel = (await page.locator('body').innerText()).replace(/\s+/g, ' ').match(new RegExp(block + ' States.{0,300}'))?.[0];
const combo = page.getByRole('combobox').or(page.locator('button[aria-haspopup="listbox"]')).first();
out.combo = await combo.count();
if (out.combo) {
  await combo.click(); await page.waitForTimeout(600);
  out.options = await page.getByRole('option').allInnerTexts();
  await page.getByRole('option', { name: new RegExp(pick) }).first().click(); await page.waitForTimeout(800);
  await page.getByRole('button', { name: /^(Save|Review \d+ changes?…?)$/ }).first().click(); await page.waitForTimeout(1500);
  const p2 = page.locator('.entities-saved-states__panel').getByRole('button', { name: /^Save$/ }); if (await p2.count()) await p2.first().click();
  await page.waitForTimeout(3000);
}
await shot(page, `${tag}-blockfont`);
save(`${tag}-blockfont.json`, out);
console.log(JSON.stringify(out, null, 1));
await browser.close();
