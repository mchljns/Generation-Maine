// The mural copy note in the Front Page canvas (7.1): what sits on top of its buttons, and what a click does.
import { launch, login, save, shot, openTemplate } from './lib.mjs';
const [base, tag] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
await openTemplate(page, base, false);
const cf = await (await page.$('iframe[name="editor-canvas"]')).contentFrame();
const note = cf.locator('.block-editor-warning').filter({ hasText: /mural/i }).first();
const out = { notes: await note.count() };
if (out.notes) {
  await note.scrollIntoViewIfNeeded();
  out.top = await note.evaluate(n => { const b = [...n.querySelectorAll('button')].map(b => { const r = b.getBoundingClientRect(); const e = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2); return { btn: b.textContent, topEl: e ? e.tagName + '.' + [...e.classList].slice(0, 4).join('.') + ' ' + (e.getAttribute('aria-label') || '') : null }; }); return b; });
  const box = await note.getByRole('button', { name: 'Remove' }).boundingBox();
  const ifr = await (await page.$('iframe[name="editor-canvas"]')).boundingBox();
  await page.mouse.click(ifr.x + box.x + box.width / 2, ifr.y + box.y + box.height / 2); await page.waitForTimeout(900);
  out.afterRealClick = await page.evaluate(() => { const s = wp.data.select('core/block-editor'); const id = s.getSelectedBlockClientId(); return { selected: id ? s.getBlockName(id) + ' ' + (s.getBlock(id).attributes.className || s.getBlock(id).attributes.name || '') : null, murals: s.getClientIdsWithDescendants().filter(x => s.getBlockName(x) === 'generation-maine/part' && s.getBlock(x).attributes.name === 'mural').length }; });
  await shot(page, `${tag}-noteprobe-after-click`);
  await page.mouse.click(ifr.x + box.x + box.width / 2, ifr.y + box.y + box.height / 2); await page.waitForTimeout(900);
  out.afterSecondClick = await page.evaluate(() => { const s = wp.data.select('core/block-editor'); const id = s.getSelectedBlockClientId(); return { selected: id ? s.getBlockName(id) + ' ' + (s.getBlock(id).attributes.className || s.getBlock(id).attributes.name || '') : null, murals: s.getClientIdsWithDescendants().filter(x => s.getBlockName(x) === 'generation-maine/part' && s.getBlock(x).attributes.name === 'mural').length }; });
  await shot(page, `${tag}-noteprobe-after-second-click`);
}
save(`${tag}-noteprobe.json`, out);
console.log(JSON.stringify(out, null, 1));
await browser.close();
