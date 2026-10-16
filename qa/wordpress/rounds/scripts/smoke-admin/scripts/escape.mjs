// Regression: markup in every creator field through the editor; then the front page as a visitor at 1440 and 320 (stage, cards, viewer)
import { launch, base, login, SHOTS, watch, metaDrawer, publishOrUpdate, dismissGuide } from './lib.mjs';
const [port, tag] = process.argv.slice(2); const B = base(port);
const b = await launch(); const ctx = await b.newContext({ viewport: { width: 1440, height: 1000 } }); await login(ctx, B);
const p = await ctx.newPage(); const errs = []; watch(p, errs);
await p.goto(B + '/wp-admin/post-new.php?post_type=gm_creator'); await p.waitForSelector('#gm_creator_details', { state: 'attached', timeout: 60000 }); await p.waitForTimeout(3000); await dismissGuide(p);
await metaDrawer(p, false); const cv = p.frameLocator('iframe[name="editor-canvas"]'); const hasFrame = await p.locator('iframe[name="editor-canvas"]').count();
await (hasFrame ? cv : p).locator('h1.wp-block-post-title, .editor-post-title__input').first().click();
await p.keyboard.type(`<img src=x onerror="window.__x=1"> "Q" & 'A' <b>B</b>`); await p.keyboard.press('Enter'); await p.keyboard.type(`Story <script>window.__y=1</script> & more`);
await metaDrawer(p, true);
const fill = async (sel, v) => { await p.locator(sel).click(); await p.keyboard.press('Control+A'); await p.keyboard.type(v); };
await fill('#gm_handle', `@h"><svg onload=window.__z=1>`); await fill('#gm_hometown', `<i data-gmprobe=1>Town</i>`); await fill('#gm_clip_len', `0:1<b>0</b>`);
await fill('#gm_clip_url', `javascript:alert(1)`); await fill('#gm_instagram', `https://www.instagram.com/x/"onmouseover="window.__w=1`); await fill('#gm_order', '-20');
await p.keyboard.press('Tab');
console.log('save', JSON.stringify(await publishOrUpdate(p)));
const out = {};
for (const [w, h] of [[1440, 900], [320, 640]]) {
  const v = await (await b.newContext({ viewport: { width: w, height: h }, isMobile: w < 800, hasTouch: w < 800 })).newPage(); const ve = []; watch(v, ve);
  await v.goto(B + '/?n=' + Date.now()); await v.waitForTimeout(1500);
  if (w < 800) { const c = v.locator('.slide .fr, .slide [tabindex="0"][aria-label]').first(); await c.scrollIntoViewIfNeeded().catch(() => {}); await c.click().catch(() => {}); await v.waitForTimeout(1200); }
  out[w] = await v.evaluate(() => ({ flags: [window.__x, window.__y, window.__z, window.__w], probes: document.querySelectorAll('[data-gmprobe], main svg[onload], img[onerror]').length, firstName: (document.querySelector('#panels h2, .panel h2') || {}).textContent, firstWho: (document.querySelector('.who') || {}).innerText, viewerOpen: !(document.getElementById('viewer') || {}).hidden, broken: [...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.getAttribute('src')).map(i => i.getAttribute('src')).slice(0, 5), sw: document.documentElement.scrollWidth }));
  out[w].errors = ve.filter(e => !/CERT|favicon/.test(e));
  await v.screenshot({ path: `${SHOTS}/escape-${tag}-${w}.png` });
}
console.log(JSON.stringify(out, null, 1)); console.log('editor errors', JSON.stringify(errs.filter(e => !/CERT|favicon|^dialog/.test(e))));
await b.close();
