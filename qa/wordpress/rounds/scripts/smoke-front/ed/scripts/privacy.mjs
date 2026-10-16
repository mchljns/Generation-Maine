// README step 5: Settings > Privacy > Use This Page, open the page in the block editor, publish, then compare canvas with the page.
import { launch, login, watch, save, shot } from './lib.mjs';
const [base, tag, widthArg] = process.argv.slice(2);
const W = +(widthArg || 1440);
const log = [];
const browser = await launch();
const { page, ctx } = await login(browser, base, { w: W, h: 900 });
watch(page, log);
await page.goto(base + '/wp-admin/options-privacy.php', { waitUntil: 'domcontentloaded' });
const use = page.locator('#set-page');
if (await use.count()) { await Promise.all([page.waitForNavigation(), use.click()]); }
const pid = await page.evaluate(() => { const s = document.querySelector('#page_for_privacy_policy'); return s ? s.value : null; });
await page.goto(`${base}/wp-admin/post.php?post=${pid}&action=edit`, { waitUntil: 'domcontentloaded' });
await page.waitForFunction(() => window.wp && wp.data && wp.data.select('core/editor').getCurrentPostId(), null, { timeout: 90000 });
await page.waitForTimeout(3500);
for (let i = 0; i < 3; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click().catch(() => {}); await page.waitForTimeout(400); } }
const status = await page.evaluate(() => wp.data.select('core/editor').getCurrentPost().status);
if (status !== 'publish') {
  await page.locator('.editor-post-publish-button__button, .editor-post-publish-panel__toggle').first().click();
  await page.waitForTimeout(1200);
  const confirm = page.locator('.editor-post-publish-panel__header-publish-button button, .editor-post-publish-panel__header-publish-button .components-button').first();
  if (await confirm.count()) await confirm.click();
  await page.waitForFunction(() => { const s = wp.data.select('core/editor'); return !s.isSavingPost() && s.getCurrentPost().status === 'publish'; }, null, { timeout: 60000 });
  await page.reload({ waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => window.wp && wp.data && wp.data.select('core/editor').getCurrentPostId(), null, { timeout: 90000 });
  await page.waitForTimeout(3500);
}
const M = () => {
  const R = e => { if (!e) return null; const r = e.getBoundingClientRect(); const c = getComputedStyle(e); return { x: Math.round(r.left), w: Math.round(r.width), fs: c.fontSize, ff: c.fontFamily.split(',')[0], lh: c.lineHeight, color: c.color }; };
  const title = document.querySelector('h1.gm-title, .editor-post-title, h1.wp-block-post-title');
  const h2 = [...document.querySelectorAll('h2')].filter(h => /Who we are|Comments|Media/.test(h.textContent))[0];
  const p = [...document.querySelectorAll('p')].filter(p => /Suggested text/.test(p.textContent))[0] || [...document.querySelectorAll('main p, .is-root-container p')][0];
  const vw = document.documentElement.clientWidth;
  return { vw, title: R(title), titleText: title && title.textContent.trim(), h2: R(h2), p: R(p), pText: p && p.textContent.slice(0, 40) };
};
const fh = await page.$('iframe[name="editor-canvas"]');
const frame = fh ? await fh.contentFrame() : page.mainFrame();
const editor = await frame.evaluate(M);
const mode = await page.evaluate(() => { const s = wp.data.select('core/editor'); return s.getRenderingMode ? s.getRenderingMode() : 'n/a'; });
await shot(page, `${tag}-privacy-editor-${W}`);
const link = await page.evaluate(() => wp.data.select('core/editor').getCurrentPost().link);
const p2 = await ctx.newPage();
await p2.goto(link, { waitUntil: 'networkidle' });
const front = await p2.evaluate(M);
await p2.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-privacy-front-${W}.png` });
save(`${tag}-privacy-${W}.json`, { pid, link, mode, editor, front, log });
console.log(JSON.stringify({ pid, link, mode, iframe: !!fh, editor, front }, null, 1));
await browser.close();
