// Run Theme Check through its admin screen (Appearance > Theme Check) and save the result text.
import { launch, login, save, shot } from './lib.mjs';
const base = process.argv[2], tag = process.argv[3];
const browser = await launch();
const { page } = await login(browser, base);
await page.goto(base + '/wp-admin/themes.php?page=themecheck', { waitUntil: 'domcontentloaded' });
const sel = page.locator('select[name="themename"]');
if (await sel.count()) await sel.selectOption('generation-maine');
await Promise.all([page.waitForNavigation({ timeout: 180000 }), page.locator('input[type="submit"], button[type="submit"]').filter({ hasText: /Check it|Check/ }).first().click().catch(async () => page.locator('#submit, input[name="submit"]').first().click())]);
const txt = await page.locator('#wpbody-content').innerText();
save(`${tag}-themecheck.txt`, txt);
const lines = txt.split('\n').filter(l => /REQUIRED|WARNING|RECOMMENDED|INFO|copyright|Author URI|passed/i.test(l));
console.log(lines.join('\n').slice(0, 4000));
await browser.close();
