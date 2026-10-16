// Create a post or page in the block editor from a markup file: parse it in the editor, rebuild any block the editor would flag
// (block recovery, as the "Attempt recovery" button does), insert, publish. Prints id, link and the blocks that needed recovery.
// usage: node mkpage2.mjs <base> <tag> <post|page> <title> <markup-file>
import fs from 'fs';
import { launch, login, watch, save, shot } from './lib.mjs';
const [base, tag, type, title, file] = process.argv.slice(2);
const log = [];
const browser = await launch();
const { page } = await login(browser, base);
watch(page, log);
await page.goto(base + '/wp-admin/post-new.php' + (type === 'page' ? '?post_type=page' : ''), { waitUntil: 'domcontentloaded' });
await page.waitForFunction(() => window.wp && wp.data && wp.data.select('core/editor') && wp.data.select('core/editor').getCurrentPostId(), null, { timeout: 90000 });
await page.waitForTimeout(2500);
for (let i = 0; i < 4; i++) {
  const c = page.locator('.components-modal__frame button[aria-label="Close"]');
  if (await c.count()) { await c.first().click().catch(() => {}); await page.waitForTimeout(500); } else break;
}
const markup = fs.readFileSync(file, 'utf8');
const res = await page.evaluate(([markup, title]) => {
  const recovered = [];
  const fix = (b) => {
    const inner = b.innerBlocks.map(fix);
    if (b.isValid === false) { recovered.push(b.name + ' ' + (b.attributes.className || '')); return wp.blocks.createBlock(b.name, b.attributes, inner); }
    return { ...b, innerBlocks: inner };
  };
  const blocks = wp.blocks.parse(markup).filter(b => b.name).map(fix);
  wp.data.dispatch('core/editor').editPost({ title });
  wp.data.dispatch('core/block-editor').resetBlocks(blocks);
  return { recovered, n: blocks.length };
}, [markup, title]);
await page.waitForTimeout(1500);
await page.evaluate(() => wp.data.dispatch('core/editor').editPost({ status: 'publish' }));
await page.evaluate(() => wp.data.dispatch('core/editor').savePost());
await page.waitForFunction(() => { const s = wp.data.select('core/editor'); return !s.isSavingPost() && s.getCurrentPost().status === 'publish'; }, null, { timeout: 60000 });
await page.waitForTimeout(800);
const invalid = await page.evaluate(() => { const s = wp.data.select('core/block-editor'); const out = []; const walk = ids => ids.forEach(id => { const b = s.getBlock(id); if (b.isValid === false) out.push(b.name); walk(s.getBlockOrder(id)); }); walk(s.getBlockOrder('')); return out; });
const info = await page.evaluate(() => { const p = wp.data.select('core/editor').getCurrentPost(); return { id: p.id, link: p.link, status: p.status }; });
save(`${tag}-mkpage2.json`, { info, res, invalid, log });
console.log(JSON.stringify({ info, res, invalid, log }));
await browser.close();
