// Styles survey: the top level, Typography and its elements, Layout, Shadows, Blocks > Paragraph / Heading / Button / Group.
// Records the visible text of each screen. 7.1: Site Editor > Design > Styles. 6.5: Styles sidebar in the editor.
import { launch, login, save, shot, guide, openTemplate } from './lib.mjs';
const [base, tag, v65s] = process.argv.slice(2);
const v65 = v65s === '1';
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 1000 });
const out = {};
const T = async () => {
  const el = page.locator('.edit-site-global-styles-sidebar .components-navigator-screen, .editor-global-styles-sidebar .components-navigator-screen, [class*="global-styles"] .components-navigator-screen').first();
  if (await el.count()) return (await el.innerText()).replace(/\s+/g, ' ').slice(0, 900);
  return (await page.locator('body').innerText()).replace(/\s+/g, ' ').slice(0, 900);
};
const back = async () => { const b = v65 ? page.locator('.interface-complementary-area button[aria-label="Back"], .interface-complementary-area button[aria-label="Navigate to the previous view"]').last() : page.getByRole('button', { name: /^(Back|Navigate to the previous view)$/ }).last(); await b.click(); await page.waitForTimeout(700); };
const go = async (name) => { const scope = v65 ? page.locator('.interface-complementary-area').first() : page; const b = v65 ? page.locator(`.interface-complementary-area button[aria-label="${name} styles"], .interface-complementary-area button[aria-label="${name}"], .interface-complementary-area button[aria-label="${name} block styles"]`).first() : scope.getByRole('button', { name: new RegExp('^(Aa )?' + name + '( styles)?$') }).first(); if (!(await b.count())) return false; await b.click(); await page.waitForTimeout(1200); return true; };
if (v65) {
  await openTemplate(page, base, true);
  await page.getByRole('button', { name: /^Styles$/ }).first().click(); await page.waitForTimeout(2000); await guide(page); await page.waitForTimeout(800);
} else {
  await page.goto(base + '/wp-admin/site-editor.php?p=%2Fstyles', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(6000); await guide(page);
}
out.root = await T();
await shot(page, `${tag}-styles-root`);
if (await go('Typography')) {
  out.typography = await T(); await shot(page, `${tag}-styles-typography`);
  for (const el of ['Text', 'Links', 'Headings', 'Captions', 'Buttons']) { if (await go(el)) { out['typo:' + el] = await T(); await back(); } }
  if (await go('Font size presets')) { out.fontSizes = await T(); await shot(page, `${tag}-styles-fontsizes`); await back(); }
  await back();
}
for (const top of ['Colors', 'Background', 'Shadows', 'Layout']) { if (await go(top)) { out[top] = await T(); await shot(page, `${tag}-styles-${top}`); await back(); } else out[top] = 'not listed'; }
if (await go('Blocks')) {
  out.blocks = await T();
  for (const b of ['Paragraph', 'Heading', 'Button', 'Group', 'Quote', 'Table', 'Gallery']) {
    const s = page.locator('input[type="search"]').first();
    if (await s.count()) { await s.fill(b); await page.waitForTimeout(800); }
    const btn = v65 ? page.locator(`.interface-complementary-area button[aria-label="${b} block styles"], .interface-complementary-area button[aria-label="${b} styles"], .interface-complementary-area button[aria-label="${b}"]`).first() : page.getByRole('button', { name: new RegExp('^' + b + '$') }).first();
    if (await btn.count()) { await btn.click(); await page.waitForTimeout(1200); out['block:' + b] = await T(); await shot(page, `${tag}-styles-block-${b}`); await back(); } else out['block:' + b] = 'not found';
    if (await s.count()) await s.fill('');
  }
}
save(`${tag}-styles-survey.json`, out);
for (const [k, v] of Object.entries(out)) console.log(`--- ${k}\n${v}`);
await browser.close();
