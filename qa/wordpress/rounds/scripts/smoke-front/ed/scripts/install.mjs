// Upload the zip through Appearance > Themes > Add New Theme > Upload Theme, then activate it from the result page or the theme card.
import { launch, login, watch, save, shot, ZIP, OUT } from './lib.mjs';
const base = process.argv[2];
const tag = process.argv[3];
const log = [];
const browser = await launch();
const { ctx, page } = await login(browser, base);
watch(page, log);
if (process.argv[4] === 'activate-only') {
  await page.goto(base + '/wp-admin/themes.php', { waitUntil: 'domcontentloaded' });
  await page.locator('.theme[data-slug="generation-maine"]').hover();
  await page.waitForTimeout(500);
  const a = page.locator('.theme[data-slug="generation-maine"] a.activate');
  await Promise.all([page.waitForNavigation({ timeout: 60000 }), a.click()]);
} else {
await page.goto(base + '/wp-admin/theme-install.php', { waitUntil: 'domcontentloaded' });
await page.locator('button.upload-view-toggle, a.upload-view-toggle').first().click();
await page.setInputFiles('#themezip', ZIP);
await Promise.all([page.waitForNavigation({ timeout: 120000 }), page.click('#install-theme-submit')]);
await page.waitForLoadState('load');
}
const body = await page.locator('#wpbody-content').innerText();
const links = await page.locator('#wpbody-content a').evaluateAll(as => as.map(a => ({ t: a.textContent.trim(), h: a.href })));
await shot(page, `${tag}-upload-result`, { fullPage: true });
// activate
if (process.argv[4] !== 'activate-only') {
const act = page.locator('#wpbody-content a', { hasText: /^Activate/ }).first();
await Promise.all([page.waitForNavigation({ timeout: 60000 }), act.click()]);
}
const after = await page.locator('#wpbody-content .notice, #message').allInnerTexts().catch(() => []);
const active = await page.locator('.theme.active .theme-name').innerText().catch(() => '');
// theme details overlay
await page.goto(base + '/wp-admin/themes.php?theme=generation-maine', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(1500);
const details = await page.locator('.theme-overlay').innerText().catch(() => '');
await shot(page, `${tag}-theme-details`);
save(`${tag}-install.json`, { body, links, after, active, details, log });
console.log(JSON.stringify({ body: body.slice(0, 600), links: links.map(l => l.t), after, active, details: details.slice(0, 800), log }, null, 1));
await browser.close();
