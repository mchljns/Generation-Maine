// Roster layout through the editor: page with the Creators block set to Roster; then the page at 320, 390 and 1440, and the log
import { launch, base, login, SHOTS, watch, dismissGuide, publishOrUpdate } from './lib.mjs';
const [port, tag] = process.argv.slice(2); const B = base(port);
const b = await launch(); const ctx = await b.newContext({ viewport: { width: 1440, height: 1000 } }); await login(ctx, B);
const p = await ctx.newPage(); const errs = []; watch(p, errs);
await p.goto(B + '/wp-admin/post-new.php?post_type=page'); await p.waitForSelector('.editor-header, .edit-post-header', { timeout: 60000 }); await p.waitForTimeout(3000); await dismissGuide(p);
const hasFrame = await p.locator('iframe[name="editor-canvas"]').count(); const cv = hasFrame ? p.frameLocator('iframe[name="editor-canvas"]') : p;
await cv.locator('h1.wp-block-post-title, .editor-post-title__input').first().click(); await p.keyboard.type('Roster test ' + tag); await p.keyboard.press('Enter');
await p.keyboard.type('/creators', { delay: 80 }); await p.waitForTimeout(1200); await p.keyboard.press('Enter'); await p.waitForTimeout(3000);
const sel = p.locator('.block-editor-block-inspector select').first();
const opts = await sel.locator('option').allInnerTexts(); await sel.selectOption({ label: opts.find(o => /Roster/.test(o)) }); await p.waitForTimeout(3000);
const editorTiles = await cv.locator('.roster .tile').count();
await p.screenshot({ path: `${SHOTS}/roster-${tag}-editor.png` });
console.log('editor preview tiles', editorTiles, 'publish', JSON.stringify(await publishOrUpdate(p)));
const link = await p.evaluate(() => wp.data.select('core/editor').getPermalink());
for (const [w, h] of [[1440, 900], [390, 844], [320, 568]]) {
  const v = await (await b.newContext({ viewport: { width: w, height: h }, isMobile: w < 800, hasTouch: w < 800 })).newPage(); const ve = []; watch(v, ve);
  await v.goto(link); await v.waitForTimeout(1000);
  const r = await v.evaluate(() => { const tiles = [...document.querySelectorAll('.roster .tile')]; const vw = document.documentElement.clientWidth; return { tiles: tiles.length, linkTiles: tiles.filter(t => t.tagName === 'A').map(t => t.href.slice(0, 60) + ' ' + t.target + ' ' + t.rel), ariaLabels: tiles.filter(t => t.hasAttribute('aria-label')).length, firstTexts: tiles.slice(0, 3).map(t => t.innerText.replace(/\n/g, ' | ')), broken: tiles.filter(t => { const tn = t.querySelector('.town'); return tn && tn.scrollWidth > tn.clientWidth + 1; }).length, sw: document.documentElement.scrollWidth, vw }; });
  console.log(w, JSON.stringify(r), 'errors', JSON.stringify(ve.filter(e => !/CERT|favicon/.test(e))));
  await v.screenshot({ path: `${SHOTS}/roster-${tag}-${w}.png`, fullPage: true });
}
console.log('editor errors', JSON.stringify(errs.filter(e => !/CERT|favicon|^dialog/.test(e))));
await b.close();
