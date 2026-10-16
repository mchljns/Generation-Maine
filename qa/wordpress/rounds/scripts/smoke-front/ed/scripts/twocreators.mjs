// A page with two Creators blocks: the editor's warning on the second, and what the page renders.
import { launch, login, save, shot } from './lib.mjs';
const [base, pid, url, tag] = process.argv.slice(2);
const browser = await launch();
const { page, ctx } = await login(browser, base, { w: 1440, h: 900 });
await page.goto(`${base}/wp-admin/post.php?post=${pid}&action=edit`, { waitUntil: 'domcontentloaded' });
await page.waitForFunction(() => window.wp && wp.data && wp.data.select('core/editor').getCurrentPostId(), null, { timeout: 90000 });
await page.waitForTimeout(5000);
for (let i = 0; i < 3; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click().catch(() => {}); await page.waitForTimeout(400); } }
const fh = await page.$('iframe[name="editor-canvas"]');
const fr = fh ? await fh.contentFrame() : page.mainFrame();
const editor = await fr.evaluate(() => ({ blocks: document.querySelectorAll('[data-type="generation-maine/creators"]').length, warnings: [...document.querySelectorAll('.block-editor-warning')].map(w => { const r = w.getBoundingClientRect(); return { text: w.innerText.replace(/\s+/g, ' '), y: Math.round(r.top + scrollY) }; }) }));
await fr.locator('.block-editor-warning').first().scrollIntoViewIfNeeded().catch(() => {});
await fr.locator('[data-type="generation-maine/creators"]').nth(1).scrollIntoViewIfNeeded().catch(() => {});
await shot(page, `${tag}-editor-second`);
const p = await ctx.newPage();
const errs = []; p.on('pageerror', e => errs.push(String(e)));
await p.goto(url, { waitUntil: 'networkidle' });
const front = await p.evaluate(() => { const ids = [...document.querySelectorAll('[id]')].map(e => e.id); return { steppers: document.querySelectorAll('#stories, .stories .stage').length, rosters: document.querySelectorAll('.roster').length, tiles: document.querySelectorAll('.roster .tile').length, dupIds: [...new Set(ids.filter((x, i) => ids.indexOf(x) !== i))], overflow: document.documentElement.scrollWidth - innerWidth }; });
await p.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-front.png`, fullPage: true });
save(`${tag}-twocreators.json`, { editor, front, errs });
console.log(JSON.stringify({ editor, front, errs }, null, 1));
await browser.close();
