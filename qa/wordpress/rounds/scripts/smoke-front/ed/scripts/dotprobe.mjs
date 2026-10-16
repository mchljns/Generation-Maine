// The canvas dot after the headline: nothing selected, the Hero section selected, the headline selected, a lede selected.
import { launch, login, save, openTemplate } from './lib.mjs';
const [base, tag, v65s] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
await openTemplate(page, base, v65s === '1');
const f = await (await page.$('iframe[name="editor-canvas"]')).contentFrame();
const out = {};
const read = async (label) => {
  out[label] = await f.evaluate(() => { const h = document.querySelector('h1'); const a = getComputedStyle(h, '::after'); return { cls: h.className, content: a.content, display: a.display, vis: a.visibility, opacity: a.opacity, bg: a.backgroundColor, w: a.width, h: a.height, anim: a.animationName }; });
  await f.locator('h1').first().screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-dot-${label}.png` });
};
await page.evaluate(() => wp.data.dispatch('core/block-editor').clearSelectedBlock()); await page.waitForTimeout(800);
await read('none');
await page.evaluate(() => { const s = wp.data.select('core/block-editor'); const id = s.getClientIdsWithDescendants().find(id => s.getBlockName(id) === 'core/group' && / hero /.test(' ' + (s.getBlock(id).attributes.className || '') + ' ')); wp.data.dispatch('core/block-editor').selectBlock(id); }); await page.waitForTimeout(800);
await read('heroSelected');
await f.locator('.hero .lede').first().click(); await page.waitForTimeout(800);
await read('ledeSelected');
await f.locator('h1').first().click(); await page.waitForTimeout(800);
await read('h1Selected');
save(`${tag}-dotprobe.json`, out);
console.log(JSON.stringify(out, null, 1));
await browser.close();
