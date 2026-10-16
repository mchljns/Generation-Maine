// Header and Footer parts: reach the Header through the canvas (click the bar, Edit original) and read the sidebar's Content
// list; open the Footer part and read its Content list. WP 7.1 only (6.5 has no Content panel).
import { launch, login, save, shot, openTemplate, guide, canvas, watch } from './lib.mjs';
const [base, tag] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
const log = []; watch(page, log);
const out = {};
const f = await openTemplate(page, base, false);
// click the bar's logo area (the part's empty space), then Edit original
await f.locator('header.wp-block-template-part').first().click({ position: { x: 400, y: 20 } });
await page.waitForTimeout(800);
const editOrig = page.getByRole('button', { name: /Edit original/ }).or(page.getByRole('menuitem', { name: /Edit original/ }));
out.editOriginalVisible = await editOrig.count();
if (!out.editOriginalVisible) {
  // toolbar options menu
  const opts = page.locator('.block-editor-block-toolbar').getByRole('button', { name: /Options/ }).first();
  if (await opts.count()) { await opts.click(); await page.waitForTimeout(500); out.optionsMenu = await page.getByRole('menuitem').allInnerTexts(); }
}
await editOrig.first().click();
await page.waitForTimeout(4000);
await guide(page);
out.url = page.url();
const side = page.locator('.interface-complementary-area').first();
if (!(await side.count())) { await page.locator('.editor-header__settings').getByRole('button', { name: 'Settings', exact: true }).click().catch(() => {}); await page.waitForTimeout(800); }
const tpTab = side.getByRole('tab', { name: /Template Part/ });
if (await tpTab.count()) { await tpTab.first().click(); await page.waitForTimeout(800); }
out.headerSidebar = (await side.innerText()).replace(/\n+/g, ' | ').slice(0, 900);
out.headerContentItems = await side.locator('.block-editor-block-quick-navigation__item, .editor-post-content-information, [class*="quick-navigation"] button').allInnerTexts();
await shot(page, `${tag}-header-part-sidebar`);
// footer part
await page.goto(base + '/wp-admin/site-editor.php?p=%2Fwp_template_part%2Fgeneration-maine%2F%2Ffooter&canvas=edit', { waitUntil: 'domcontentloaded' });
await canvas(page); await page.waitForTimeout(3000); await guide(page);
const side2 = page.locator('.interface-complementary-area').first();
if (!(await side2.count())) { await page.locator('.editor-header__settings').getByRole('button', { name: 'Settings', exact: true }).click().catch(() => {}); await page.waitForTimeout(800); }
const tpTab2 = side2.getByRole('tab', { name: /Template Part/ });
if (await tpTab2.count()) { await tpTab2.first().click(); await page.waitForTimeout(800); }
out.footerSidebar = (await side2.innerText()).replace(/\n+/g, ' | ').slice(0, 900);
out.footerContentItems = await side2.locator('.block-editor-block-quick-navigation__item, [class*="quick-navigation"] button').allInnerTexts();
await shot(page, `${tag}-footer-part-sidebar`);
const sf = side2.getByRole('button', { name: /Site Footer/ });
if (await sf.count()) { await sf.first().click(); await page.waitForTimeout(800); out.afterClickSiteFooter = (await side2.innerText()).replace(/\n+/g, ' | ').slice(0, 500); await shot(page, `${tag}-footer-part-sitefooter-click`); }
save(`${tag}-parts-content.json`, { out, log });
console.log(JSON.stringify(out, null, 1));
await browser.close();
