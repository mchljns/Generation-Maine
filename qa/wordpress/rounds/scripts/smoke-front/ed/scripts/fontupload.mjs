// Upload a font through Appearance > Fonts > Upload, then see where it shows: Styles > Typography and a paragraph's Typography panel.
import { launch, login, save, shot, watch, canvas, guide } from './lib.mjs';
const [base, tag] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 1000 });
const log = []; watch(page, log);
const out = {};
await page.goto(base + '/wp-admin/font-library.php', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(4000);
await page.getByRole('tab', { name: 'Upload' }).click();
await page.waitForTimeout(1000);
await page.locator('input[type="file"]').first().setInputFiles('/tmp/claude-0/wptest/work/r4-editor/fonts/LiberationSerif-Regular.ttf');
await page.waitForTimeout(6000);
out.afterUpload = (await page.locator('.components-notice, [role="status"], .font-library-modal__tabpanel-layout, .components-snackbar').allInnerTexts()).join(' | ').slice(0, 500);
await page.getByRole('tab', { name: 'Library' }).click();
await page.waitForTimeout(1500);
out.library = (await page.locator('body').innerText()).split('Library')[1]?.slice(0, 400);
await shot(page, `${tag}-fonts-after-upload`);
// Styles > Typography in the Site Editor
await page.goto(base + '/wp-admin/site-editor.php?p=%2Fstyles', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(6000);
await guide(page);
const typ = page.getByRole('button', { name: /^Typography/ }).first();
if (await typ.count()) { await typ.click(); await page.waitForTimeout(1500); }
out.stylesTypography = (await page.locator('.edit-site-global-styles-sidebar, .editor-global-styles-sidebar, .interface-complementary-area, [aria-label="Styles"]').first().innerText().catch(() => '')).slice(0, 800);
await shot(page, `${tag}-styles-typography-after-upload`);
const textEl = page.getByRole('button', { name: /^Text/ }).first();
if (await textEl.count()) { await textEl.click(); await page.waitForTimeout(1500); out.stylesText = (await page.locator('.edit-site-global-styles-sidebar, .editor-global-styles-sidebar, .interface-complementary-area').first().innerText().catch(() => '')).slice(0, 800); await shot(page, `${tag}-styles-text-after-upload`); }
save(`${tag}-fontupload.json`, { out, log });
console.log(JSON.stringify(out, null, 1));
await browser.close();
