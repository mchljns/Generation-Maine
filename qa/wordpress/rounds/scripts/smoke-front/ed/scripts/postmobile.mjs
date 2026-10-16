// Post editor canvas in the Mobile preview: title and text inset and sizes, against the page at the same width.
import { launch, login, save, shot } from './lib.mjs';
const [base, pid, tag] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
await page.goto(`${base}/wp-admin/post.php?post=${pid}&action=edit`, { waitUntil: 'domcontentloaded' });
await page.waitForFunction(() => window.wp && wp.data && wp.data.select('core/editor').getCurrentPostId(), null, { timeout: 90000 });
await page.waitForTimeout(3000);
for (let i = 0; i < 3; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click().catch(() => {}); await page.waitForTimeout(400); } }
const v = page.locator('button[aria-label="View"], button[aria-label="Preview"]').first();
await v.click(); await page.waitForTimeout(500);
await page.getByRole('menuitemradio', { name: /^Mobile/ }).or(page.getByRole('menuitem', { name: /^Mobile/ })).first().click();
await page.waitForTimeout(2500); await page.keyboard.press('Escape');
const fr = await (await page.$('iframe[name="editor-canvas"]')).contentFrame();
const M = () => { const R = s => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); const c = getComputedStyle(e); return { x: Math.round(r.left), w: Math.round(r.width), fs: c.fontSize }; }; return { vw: document.documentElement.clientWidth, title: R('h1'), p: R('.is-root-container p, main .gm-entry p, .wp-block-post-content p'), overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth }; };
const editor = await fr.evaluate(M);
await shot(page, `${tag}-post-mobile-editor`);
const link = await page.evaluate(() => wp.data.select('core/editor').getCurrentPost().link);
const p = await browser.newPage({ viewport: { width: editor.vw, height: 800 } });
await p.goto(link, { waitUntil: 'networkidle' });
const front = await p.evaluate(M);
// back to Desktop for later runs
await v.click(); await page.waitForTimeout(400); await page.getByRole('menuitemradio', { name: /^Desktop/ }).or(page.getByRole('menuitem', { name: /^Desktop/ })).first().click().catch(() => {});
save(`${tag}-post-mobile.json`, { editor, front });
console.log(JSON.stringify({ editor, front }));
await browser.close();
