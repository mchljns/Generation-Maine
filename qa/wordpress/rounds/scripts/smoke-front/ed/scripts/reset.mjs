// README "Start over": Templates > Front Page > Actions > Reset; Patterns > Template Parts > Header > Reset (WP 7.1 UI).
import { launch, login, save, shot, guide } from './lib.mjs';
const [base, tag, which = 'front-page'] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
const out = { which };
if (which === 'front-page') {
  await page.goto(base + '/wp-admin/site-editor.php?p=%2Ftemplate', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(4000); await guide(page);
  const card = page.locator('.dataviews-view-grid__card, .dataviews-view-table__row, tr, li').filter({ hasText: 'Front Page' }).first();
  await card.hover();
  await card.getByRole('button', { name: /Actions|More actions/ }).first().click();
} else {
  await page.goto(base + '/wp-admin/site-editor.php?p=%2Fpattern&postType=wp_template_part&categoryId=all-parts', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(4000); await guide(page);
  const card = page.locator('.dataviews-view-grid__card, .dataviews-view-table__row, tr, li').filter({ hasText: new RegExp('^' + which, 'i') }).first();
  await card.hover();
  await card.getByRole('button', { name: /Actions|More actions/ }).first().click();
}
await page.waitForTimeout(600);
out.menu = await page.locator('[role="menuitem"]').allInnerTexts();
const reset = page.getByRole('menuitem', { name: /Reset|Clear customizations/ });
if (await reset.count()) {
  await reset.first().click(); await page.waitForTimeout(800);
  out.dialog = await page.locator('[role="dialog"]').allInnerTexts();
  const ok = page.locator('[role="dialog"]').getByRole('button', { name: /^(Reset|Confirm|Clear|Delete)/ });
  if (await ok.count()) await ok.first().click();
  await page.waitForTimeout(2500);
  out.snack = await page.locator('.components-snackbar').allInnerTexts();
}
save(`${tag}-reset-${which}.json`, out);
console.log(JSON.stringify(out));
await browser.close();
