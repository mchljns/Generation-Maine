// Styles > Typography > Text (and Headings): pick the uploaded font, save, then read the fonts on the page and in the editor.
import { launch, login, save, shot, guide, canvas } from './lib.mjs';
const [base, tag] = process.argv.slice(2);
const browser = await launch();
const { page, ctx } = await login(browser, base, { w: 1440, h: 1000 });
const out = {};
await page.goto(base + '/wp-admin/site-editor.php?p=%2Fstyles', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(6000); await guide(page);
await page.getByRole('button', { name: /^Typography/ }).first().click(); await page.waitForTimeout(1200);
for (const el of ['Text', 'Headings']) {
  await page.getByRole('button', { name: new RegExp('^(Aa )?' + el + '$') }).first().click(); await page.waitForTimeout(1200);
  const combo = page.getByRole('combobox').or(page.locator('button[aria-haspopup="listbox"]')).first();
  await combo.click(); await page.waitForTimeout(600);
  out[el + '_options'] = await page.getByRole('option').allInnerTexts();
  await page.getByRole('option', { name: /Liberation Serif/ }).first().click(); await page.waitForTimeout(800);
  await page.getByRole('button', { name: /^(Back|Navigate to the previous view)$/ }).last().click(); await page.waitForTimeout(800);
}
await shot(page, `${tag}-picked`);
const saveBtn = page.getByRole('button', { name: /^(Save|Review \d+ changes?…?)$/ }).first();
await saveBtn.click(); await page.waitForTimeout(1500);
const p2 = page.locator('.entities-saved-states__panel').getByRole('button', { name: /^Save$/ });
if (await p2.count()) await p2.first().click();
await page.waitForTimeout(3000);
const p = await ctx.newPage();
await p.goto(base + '/', { waitUntil: 'networkidle' });
out.front = await p.evaluate(() => { const f = s => { const e = document.querySelector(s); return e ? getComputedStyle(e).fontFamily.split(',')[0] : null; }; return { h1: f('h1'), lede: f('.hero .lede, .hero p:not(.k)'), aboutP: f('.about .goal'), aim: f('.about .big'), h2: f('section h2'), nav: f('.gm-bar nav a'), body: f('body') }; });
await p.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-front-after-font.png` });
await p.goto(base + (process.argv[4] || '/blocks-test/'), { waitUntil: 'networkidle' });
out.page = await p.evaluate(() => { const f = s => { const e = document.querySelector(s); return e ? getComputedStyle(e).fontFamily.split(',')[0] : null; }; return { title: f('h1'), h2: f('main h2'), p: f('main p') }; });
save(`${tag}-pickfont.json`, out);
console.log(JSON.stringify(out, null, 1));
await browser.close();
