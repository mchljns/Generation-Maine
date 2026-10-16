// A page holding pasted Logo and mural Part blocks: the post editor (notes, rendering mode) and the page.
import { launch, login, save, shot } from './lib.mjs';
const [base, tag, pid, url] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
const out = {};
await page.goto(`${base}/wp-admin/post.php?post=${pid}&action=edit`, { waitUntil: 'domcontentloaded' });
await page.waitForFunction(() => window.wp && wp.data && wp.data.select('core/editor').getCurrentPostId(), null, { timeout: 90000 });
await page.waitForTimeout(5000);
for (let i = 0; i < 3; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click().catch(() => {}); await page.waitForTimeout(400); } }
out.mode = await page.evaluate(() => { const s = wp.data.select('core/editor'); return s.getRenderingMode ? s.getRenderingMode() : 'n/a'; });
const fr = await (await page.$('iframe[name="editor-canvas"]')).contentFrame();
out.notes = await fr.evaluate(() => [...document.querySelectorAll('.block-editor-warning')].map(w => w.innerText.replace(/\s+/g, ' ')));
out.logosInEditor = await fr.evaluate(() => document.querySelectorAll('.is-root-container a[aria-label*="home"], .wp-block-post-content a[aria-label*="home"]').length);
out.partsEditor = await page.evaluate(() => { const s = wp.data.select('core/block-editor'); return s.getClientIdsWithDescendants().filter(id => s.getBlockName(id) === 'generation-maine/part').map(id => s.getBlock(id).attributes.name); });
await shot(page, `${tag}-pasted-editor`);
const p = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await p.goto(url, { waitUntil: 'networkidle' });
out.page = await p.evaluate(() => { const ids = [...document.querySelectorAll('[id]')].map(e => e.id); return { dupIds: [...new Set(ids.filter((x, i) => ids.indexOf(x) !== i))], logos: document.querySelectorAll('a[aria-label*="home"]').length, logosInEntry: document.querySelectorAll('.gm-entry a[aria-label*="home"]').length, murals: document.querySelectorAll('svg.mural, .mural').length }; });
await p.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-pasted-page.png` });
save(`${tag}-pastedparts.json`, out);
console.log(JSON.stringify(out, null, 1));
await browser.close();
