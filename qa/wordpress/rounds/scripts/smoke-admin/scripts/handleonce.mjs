// CRE-N05: creators whose title is (or looks like) their handle, made in the editor; read the clip header on the page.
// usage: node handleonce.mjs <port> <tag> "<title>|<handle>" ...
import { launch, base, login, wp, INST, SHOTS, watch, metaDrawer, publishOrUpdate, dismissGuide } from './lib.mjs';
const [port, tag, ...cases] = process.argv.slice(2); const B = base(port), inst = INST[port];
const b = await launch(); const ctx = await b.newContext({ viewport: { width: 1440, height: 1000 } }); await login(ctx, B);
const errs = []; const made = [];
for (const c of cases) {
  const [title, handle] = c.split('|');
  const p = await ctx.newPage(); watch(p, errs);
  await p.goto(B + '/wp-admin/post-new.php?post_type=gm_creator'); await p.waitForSelector('#gm_creator_details', { state: 'attached', timeout: 60000 }); await p.waitForTimeout(3000); await dismissGuide(p);
  await metaDrawer(p, false);
  const hasFrame = await p.locator('iframe[name="editor-canvas"]').count(); const cv = hasFrame ? p.frameLocator('iframe[name="editor-canvas"]') : p;
  await cv.locator('h1.wp-block-post-title, .editor-post-title__input').first().click(); await p.keyboard.type(title); await p.keyboard.press('Enter'); await p.keyboard.type('Story for ' + title);
  await metaDrawer(p, true);
  await p.locator('#gm_handle').click(); await p.keyboard.type(handle);
  await p.locator('#gm_hometown').click(); await p.keyboard.type('Houlton');
  await p.locator('#gm_clip_url').click(); await p.keyboard.type(B + '/wp-content/uploads/2026/10/portrait-1.jpg');
  await p.locator('#gm_order').click(); await p.keyboard.press('Control+A'); await p.keyboard.type('-' + (cases.length - made.length));
  await p.keyboard.press('Tab');
  await publishOrUpdate(p);
  made.push({ title, handle, id: await p.evaluate(() => wp.data.select('core/editor').getCurrentPostId()) });
  await p.close();
}
const res = [];
for (const [w, h] of [[1440, 900], [320, 640]]) {
  const v = await (await b.newContext({ viewport: { width: w, height: h }, isMobile: w < 800, hasTouch: w < 800 })).newPage();
  await v.goto(B + '/?n=' + Date.now()); await v.waitForTimeout(800);
  const who = await v.evaluate(() => ({ stage: [...document.querySelectorAll('#stage .who, .stage .who')].map(e => e.innerText.replace(/\n/g, ' / ')), cards: [...document.querySelectorAll('.slide .who, .card .who')].map(e => e.innerText.replace(/\n/g, ' / ')), sw: document.documentElement.scrollWidth }));
  res.push({ w, who });
  await v.screenshot({ path: `${SHOTS}/handleonce-${tag}-${w}.png` });
}
const html = await (await fetch(B + '/?n=' + Date.now())).text();
const whos = [...html.matchAll(/<div class="who[^"]*">(?:<img[^>]*>|<svg[\s\S]*?<\/svg>)?<span>([\s\S]*?)<\/span><\/div>/g)].map(m => m[1]);
console.log(JSON.stringify({ made, whoMarkup: [...new Set(whos)].slice(0, 12), res, errors: errs.filter(e => !/CERT|favicon|^dialog/.test(e)) }, null, 1));
await b.close();
