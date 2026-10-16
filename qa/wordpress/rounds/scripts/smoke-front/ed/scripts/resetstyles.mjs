// Styles > More (three dots) > Reset styles, then save; print the stored global styles.
import { launch, login, save, shot, guide } from './lib.mjs';
const [base, tag] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 1000 });
await page.goto(base + '/wp-admin/site-editor.php?p=%2Fstyles', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(6000); await guide(page);
const more = page.getByRole('button', { name: /^(More|Styles actions|Options)$/ }).first();
await more.click(); await page.waitForTimeout(600);
const items = await page.getByRole('menuitem').allInnerTexts();
await page.getByRole('menuitem', { name: /Reset/ }).first().click(); await page.waitForTimeout(1000);
const dlg = page.locator('[role="dialog"]').getByRole('button', { name: /^(Reset|Confirm)/ }); if (await dlg.count()) { await dlg.first().click(); await page.waitForTimeout(800); }
const saveBtn = page.getByRole('button', { name: /^(Save|Review \d+ changes?…?)$/ }).first();
await saveBtn.click(); await page.waitForTimeout(1500);
const p2 = page.locator('.entities-saved-states__panel').getByRole('button', { name: /^Save$/ }); if (await p2.count()) await p2.first().click();
await page.waitForTimeout(3000);
save(`${tag}-resetstyles.json`, { items });
console.log(JSON.stringify(items.filter(i => !/Menu|About|WordPress|Get Inv|Docum|Learn|Support|Feedback|Visit|Ctrl|^0|New|Post|Media|Page|Creator|User|Database|Howdy|admin|Log Out/.test(i))));
await browser.close();
