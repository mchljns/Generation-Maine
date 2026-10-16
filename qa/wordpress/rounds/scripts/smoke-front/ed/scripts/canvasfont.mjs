// Fonts in the Site Editor canvas (Front Page) and in the post editor (a paragraph's Typography panel offers Font?).
import { launch, login, save, shot, openTemplate } from './lib.mjs';
const [base, tag, v65, pid] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
const out = {};
const f = await openTemplate(page, base, v65 === '1');
out.canvas = await f.evaluate(() => { const g = s => { const e = document.querySelector(s); return e ? getComputedStyle(e).fontFamily.split(',')[0] : null; }; return { h1: g('h1'), lede: g('.hero .lede, .hero p.lede'), aboutGoal: g('.about .goal'), nav: g('.gm-bar nav a'), body: g('body') }; });
await shot(page, `${tag}-canvas-font`);
if (pid) {
  await page.goto(`${base}/wp-admin/post.php?post=${pid}&action=edit`, { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => window.wp && wp.data && wp.data.select('core/editor').getCurrentPostId(), null, { timeout: 90000 });
  await page.waitForTimeout(3000);
  for (let i = 0; i < 3; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click().catch(() => {}); await page.waitForTimeout(400); } }
  const fh = await page.$('iframe[name="editor-canvas"]');
  const fr = fh ? await fh.contentFrame() : page.mainFrame();
  out.postCanvas = await fr.evaluate(() => { const g = s => { const e = document.querySelector(s); return e ? getComputedStyle(e).fontFamily.split(',')[0] : null; }; return { title: g('h1'), p: g('.is-root-container p'), h2: g('.is-root-container h2') }; });
  // select the intro paragraph and open its Typography options
  await fr.locator('.is-root-container p').first().click();
  await page.waitForTimeout(800);
  const side = page.locator('.interface-complementary-area');
  if (!(await side.count())) { await page.getByRole('button', { name: 'Settings', exact: true }).first().click(); await page.waitForTimeout(600); }
  const bt = page.getByRole('tab', { name: 'Block' }); if (await bt.count()) await bt.first().click();
  await page.waitForTimeout(600);
  out.blockPanels = (await page.locator('.block-editor-block-inspector').innerText().catch(() => '')).replace(/\s+/g, ' ').slice(0, 600);
  const opt = page.locator('.block-editor-block-inspector').getByRole('button', { name: /Typography options/ });
  if (await opt.count()) { await opt.first().click(); await page.waitForTimeout(600); out.typographyMenu = await page.getByRole('menuitemcheckbox').allInnerTexts(); await shot(page, `${tag}-para-typography-menu`); await page.keyboard.press('Escape'); }
}
save(`${tag}-canvasfont.json`, out);
console.log(JSON.stringify(out, null, 1));
await browser.close();
