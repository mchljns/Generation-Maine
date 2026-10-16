// Under theme 3.1.0: Styles > Typography > Text > Font: pick "Michroma (labels)", save. Then read fonts on the page and canvas.
import { launch, login, save, shot, guide, openTemplate } from './lib.mjs';
const [base, tag, pick, el = 'Text'] = process.argv.slice(2);
const browser = await launch();
const { page, ctx } = await login(browser, base, { w: 1440, h: 1000 });
const out = {};
if (pick) {
  await page.goto(base + '/wp-admin/site-editor.php?p=%2Fstyles', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(6000); await guide(page);
  await page.getByRole('button', { name: /^Typography/ }).first().click(); await page.waitForTimeout(1200);
  await page.getByRole('button', { name: new RegExp('^(Aa )?' + el + '$') }).first().click(); await page.waitForTimeout(1200);
  const combo = page.getByRole('combobox').or(page.locator('button[aria-haspopup="listbox"]')).first();
  await combo.click(); await page.waitForTimeout(600);
  out.options = await page.getByRole('option').allInnerTexts();
  await page.getByRole('option', { name: new RegExp(pick) }).first().click(); await page.waitForTimeout(800);
  await page.getByRole('button', { name: /^(Save|Review \d+ changes?…?)$/ }).first().click(); await page.waitForTimeout(1500);
  const p2 = page.locator('.entities-saved-states__panel').getByRole('button', { name: /^Save$/ }); if (await p2.count()) await p2.first().click();
  await page.waitForTimeout(3000);
}
const F = () => { const g = s => { const e = document.querySelector(s); return e ? getComputedStyle(e).fontFamily.split(',')[0] : null; }; return { h1: g('h1'), aimBig: g('.about .big'), h2: g('.follow h2'), lede: g('.hero .lede'), goal: g('.about .goal'), body: g('body'), followLede: g('.follow .lede') }; };
const p = await ctx.newPage(); await p.goto(base + '/', { waitUntil: 'networkidle' }); out.front = await p.evaluate(F);
const f = await openTemplate(page, base, false); out.canvas = await f.evaluate(F);
// Styles > Typography > Text after: any font control left to undo it?
await page.goto(base + '/wp-admin/site-editor.php?p=%2Fstyles', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(6000); await guide(page);
await page.getByRole('button', { name: /^Typography/ }).first().click(); await page.waitForTimeout(1200);
await page.getByRole('button', { name: /^(Aa )?Text$/ }).first().click(); await page.waitForTimeout(1200);
out.textPanel = (await page.locator('body').innerText()).replace(/\s+/g, ' ').match(/Text Manage.{0,200}/)?.[0];
await shot(page, `${tag}-styles-text`);
save(`${tag}-pickfont310.json`, out);
console.log(JSON.stringify(out, null, 1));
await browser.close();
