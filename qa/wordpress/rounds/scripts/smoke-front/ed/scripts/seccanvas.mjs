// About and Follow inserted in a page: the post editor canvas against the front page at the same width.
import { launch, login, save, shot } from './lib.mjs';
const [base, pid, tag] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
await page.goto(`${base}/wp-admin/post.php?post=${pid}&action=edit`, { waitUntil: 'domcontentloaded' });
await page.waitForFunction(() => window.wp && wp.data && wp.data.select('core/editor').getCurrentPostId(), null, { timeout: 90000 });
await page.waitForTimeout(4000);
for (let i = 0; i < 3; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click().catch(() => {}); await page.waitForTimeout(400); } }
const fh = await page.$('iframe[name="editor-canvas"]');
const fr = fh ? await fh.contentFrame() : page.mainFrame();
const M = () => {
  const pick = (sec) => { const s = document.querySelector(sec); if (!s) return null; const sr = s.getBoundingClientRect(); const g = (q) => { const e = s.querySelector(q); if (!e) return null; const c = getComputedStyle(e); const r = e.getBoundingClientRect(); return `${c.fontSize} mt=${c.marginTop} top+${Math.round(r.top - sr.top)} left=${Math.round(r.left - sr.left)}`; }; return { x: Math.round(sr.left), w: Math.round(sr.width), h: Math.round(sr.height), mt: getComputedStyle(s).marginTop, h2: g('h2'), lede: g('.lede'), k: g('.k'), big: g('.big'), bg: getComputedStyle(s).backgroundColor }; };
  return { vw: document.documentElement.clientWidth, about: pick('section.about, .about'), follow: pick('section.follow, .follow') };
};
const editor = await fr.evaluate(M);
await fr.locator('.follow').first().scrollIntoViewIfNeeded().catch(() => {});
await shot(page, `${tag}-seccanvas-editor`);
const p = await browser.newPage({ viewport: { width: editor.vw, height: 900 } });
await p.goto(base + '/', { waitUntil: 'networkidle' });
const front = await p.evaluate(M);
save(`${tag}-seccanvas.json`, { editor, front });
console.log(JSON.stringify({ editor, front }, null, 1));
await browser.close();
