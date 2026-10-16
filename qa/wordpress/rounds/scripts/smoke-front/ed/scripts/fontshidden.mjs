// Appearance > Fonts hidden on 7.1: menu, direct visit, theme details overlay, command palette, Styles typography.
import { launch, login, save, shot, watch, guide } from './lib.mjs';
const [base, tag] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 1000 });
const log = []; watch(page, log);
const out = {};
await page.goto(base + '/wp-admin/themes.php', { waitUntil: 'domcontentloaded' });
out.appearanceMenu = await page.locator('#menu-appearance .wp-submenu a').allInnerTexts();
// theme details overlay
await page.goto(base + '/wp-admin/themes.php?theme=generation-maine', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2500);
out.overlayButtons = await page.locator('.theme-overlay .theme-actions a, .theme-overlay .theme-actions button').allInnerTexts();
out.overlayText = (await page.locator('.theme-overlay').innerText().catch(() => '')).replace(/\s+/g, ' ').slice(0, 600);
await shot(page, `${tag}-theme-details`);
// direct visit
const resp = await page.goto(base + '/wp-admin/font-library.php', { waitUntil: 'domcontentloaded' });
out.direct = { status: resp.status(), url: page.url(), title: await page.title(), text: (await page.locator('body').innerText()).slice(0, 400), links: await page.locator('a').evaluateAll(as => as.map(a => a.textContent.trim() + ' -> ' + a.getAttribute('href'))) };
await shot(page, `${tag}-fonts-direct`);
// with query args
const resp2 = await page.goto(base + '/wp-admin/font-library.php?tab=upload', { waitUntil: 'domcontentloaded' });
out.direct2 = resp2.status();
// command palette in the site editor
await page.goto(base + '/wp-admin/site-editor.php', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(5000); await guide(page);
await page.keyboard.press('Control+k'); await page.waitForTimeout(800);
await page.keyboard.type('Fonts'); await page.waitForTimeout(1500);
out.commandFonts = await page.locator('[cmdk-item], .commands-command-menu__container [role="option"]').allInnerTexts().catch(() => []);
await shot(page, `${tag}-command-fonts`);
await page.keyboard.press('Escape');
// dashboard command palette
await page.goto(base + '/wp-admin/index.php', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(2000);
await page.keyboard.press('Control+k'); await page.waitForTimeout(800);
await page.keyboard.type('Font'); await page.waitForTimeout(1500);
out.commandFontsDash = await page.locator('[cmdk-item], [role="option"]').allInnerTexts().catch(() => []);
await page.keyboard.press('Escape');
save(`${tag}-fontshidden.json`, { out, log });
console.log(JSON.stringify(out, null, 1));
await browser.close();
