// Appearance > Themes > Add New Theme > Upload Theme with a zip whose theme is already installed: choose "Replace installed with
// uploaded" and report the result text.
import { launch, login, save, shot, watch } from './lib.mjs';
const [base, tag, zip] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base);
const log = []; watch(page, log);
await page.goto(base + '/wp-admin/theme-install.php', { waitUntil: 'domcontentloaded' });
await page.locator('button.upload-view-toggle, a.upload-view-toggle').first().click();
await page.setInputFiles('#themezip', zip);
await Promise.all([page.waitForNavigation({ timeout: 120000 }), page.click('#install-theme-submit')]);
const first = (await page.locator('#wpbody-content').innerText()).slice(0, 1500);
await shot(page, `${tag}-replace-compare`, { fullPage: true });
const rep = page.locator('a.update-from-upload-overwrite, a:has-text("Replace installed with uploaded"), a:has-text("Replace active with uploaded")').first();
let after = '';
if (await rep.count()) {
  await Promise.all([page.waitForNavigation({ timeout: 120000 }), rep.click()]);
  after = (await page.locator('#wpbody-content').innerText()).slice(0, 800);
}
save(`${tag}-replace.json`, { first, after, log });
console.log(first.replace(/\n+/g, ' | ').slice(0, 900));
console.log('AFTER:', after.replace(/\n+/g, ' | '));
await browser.close();
