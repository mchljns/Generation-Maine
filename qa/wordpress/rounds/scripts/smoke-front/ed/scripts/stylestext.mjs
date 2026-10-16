// Styles > Typography > each element: which controls show. Works on 7.1 (Design > Styles) and 6.5 (Styles sidebar).
import { launch, login, save, shot, guide } from './lib.mjs';
const [base, tag, v65] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 1000 });
const out = {};
await page.goto(base + (v65 ? '/wp-admin/site-editor.php?path=%2Fwp_global_styles' : '/wp-admin/site-editor.php?p=%2Fstyles'), { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(6000);
await guide(page);
if (v65) { const e = page.getByRole('button', { name: /^Edit styles/ }); if (await e.count()) { await e.first().click(); await page.waitForTimeout(3000); } }
const panel = () => page.locator('.edit-site-global-styles-sidebar__navigator-provider, .editor-global-styles-sidebar__navigator-provider, .edit-site-global-styles-sidebar, [class*="global-styles-sidebar"], .edit-site-sidebar-navigation-screen-global-styles__content, .edit-site-page-content').first();
const text = async () => (await page.locator('body').innerText()).replace(/\s+/g, ' ');
await page.getByRole('button', { name: /^Typography/ }).first().click(); await page.waitForTimeout(1500);
out.typography = (await text()).match(/Typography.{0,400}/)?.[0];
for (const el of ['Text', 'Links', 'Headings', 'Captions', 'Buttons']) {
  const b = page.getByRole('button', { name: new RegExp('^(Aa )?' + el + '$') }).first();
  if (!(await b.count())) { out[el] = 'not found'; continue; }
  await b.click(); await page.waitForTimeout(1500);
  const t = await text();
  out[el] = t.match(new RegExp(el + ' (Customize|Manage|Typography|Font|Text|Default|Aa|Upper|Lower|Size).{0,400}'))?.[0] || t.slice(t.indexOf(el), t.indexOf(el) + 400);
  out[el + '_font'] = await page.getByText(/^Font$|^Font family$/).count();
  out[el + '_fontcombo'] = await page.locator('select:near(:text("Font"))').count();
  await shot(page, `${tag}-styles-${el}`);
  await page.getByRole('button', { name: /^(Back|Navigate to the previous view)$/ }).last().click(); await page.waitForTimeout(800);
}
save(`${tag}-stylestext.json`, out);
console.log(JSON.stringify(out, null, 1));
await browser.close();
