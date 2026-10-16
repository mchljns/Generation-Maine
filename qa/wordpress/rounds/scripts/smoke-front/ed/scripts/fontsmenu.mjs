// Appearance > Fonts on WP 7.1: what it offers with the theme's font library switch off.
import { launch, login, save, shot, watch } from './lib.mjs';
const [base, tag] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base);
const log = []; watch(page, log);
await page.goto(base + '/wp-admin/themes.php', { waitUntil: 'domcontentloaded' });
const href = await page.locator('#menu-appearance a', { hasText: /^Fonts$/ }).getAttribute('href').catch(() => null);
console.log('menu href', href);
if (href) {
  await page.goto(new URL(href, base + '/wp-admin/').href, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(5000);
  await shot(page, `${tag}-fonts-page`);
  const txt = await page.locator('#wpbody-content, .font-library-modal, body').first().innerText();
  console.log(txt.slice(0, 1500));
  const tabs = await page.getByRole('tab').allInnerTexts();
  console.log('tabs', tabs);
}
save(`${tag}-fonts-page.json`, { href, log });
console.log(log.join('\n'));
await browser.close();
