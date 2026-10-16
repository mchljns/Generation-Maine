// Fonts on a post as a visitor and in the post editor, and on the front page and its Site Editor canvas.
import { launch, login, save, shot, openTemplate } from './lib.mjs';
const [base, tag, pid, url, v65] = process.argv.slice(2);
const browser = await launch();
const { page, ctx } = await login(browser, base, { w: 1440, h: 900 });
const out = {};
const F = () => { const g = s => { const e = document.querySelector(s); return e ? getComputedStyle(e).fontFamily.split(',')[0] + ' ' + getComputedStyle(e).fontWeight : null; }; return { h1: g('h1'), h2: g('h2'), aimBig: g('.about .big'), lede: g('.hero .lede'), goal: g('.about .goal'), body: g('body'), followLede: g('.follow .lede'), btn: g('.wp-block-button__link'), p1: g('p.has-label-font-family'), p2: g('p.has-dejavu-serif-font-family'), plain: [...document.querySelectorAll('p')].filter(p => /Plain paragraph/.test(p.textContent)).map(p => getComputedStyle(p).fontFamily.split(',')[0])[0] }; };
const p = await ctx.newPage(); await p.goto(base + '/', { waitUntil: 'networkidle' }); out.front = await p.evaluate(F);
await p.goto(url, { waitUntil: 'networkidle' }); out.post = await p.evaluate(F);
out.postFontCss = await p.evaluate(() => [...document.querySelectorAll('style')].map(s => s.textContent).join('\n').match(/[^}]{0,80}(dejavu|font-family--label)[^}]{0,80}/gi));
out.postFontFace = await p.evaluate(() => [...document.fonts].map(f => f.family + ' ' + f.status));
const f = await openTemplate(page, base, v65 === '1'); out.canvas = await f.evaluate(F);
await shot(page, `${tag}-fontstate-canvas`);
await page.goto(`${base}/wp-admin/post.php?post=${pid}&action=edit`, { waitUntil: 'domcontentloaded' });
await page.waitForFunction(() => window.wp && wp.data && wp.data.select('core/editor').getCurrentPostId(), null, { timeout: 90000 });
await page.waitForTimeout(3500);
for (let i = 0; i < 3; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click().catch(() => {}); await page.waitForTimeout(400); } }
const fh = await page.$('iframe[name="editor-canvas"]'); const fr = fh ? await fh.contentFrame() : page.mainFrame();
out.editor = await fr.evaluate(F);
out.editorSettingsFonts = await page.evaluate(() => { const s = wp.data.select('core/block-editor').getSettings(); return { lib: s.fontLibraryEnabled, fams: JSON.stringify(s.__experimentalFeatures && s.__experimentalFeatures.typography && s.__experimentalFeatures.typography.fontFamilies || null).slice(0, 300) }; });
await shot(page, `${tag}-fontstate-editor`);
save(`${tag}-fontstate.json`, out);
console.log(JSON.stringify(out, null, 1));
await browser.close();
