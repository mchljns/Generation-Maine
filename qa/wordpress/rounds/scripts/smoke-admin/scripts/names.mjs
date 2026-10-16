// AD-R2 / CRE-N05 / AD-R3: names and handles with 4x4, --, quotes and apostrophes, typed through the Creator editor and
// Settings; read every place they print: stage and card headers, panel h2, card captions, viewer, roster tiles, follow rows,
// social spans, segment aria-labels, data-name and the Next label, clip aria-labels.
//   node names.mjs <port> <tag> [nocreate]
import { launch, base, login, wp, INST, SHOTS, watch, metaDrawer, publishOrUpdate, dismissGuide } from './lib.mjs';
import fs from 'fs';
const [port, tag, nocreate] = process.argv.slice(2); const B = base(port), inst = INST[port];
const CASES = [
  // title | handle typed | expected one line?
  ['@4x4.maine', '@4x4.maine'],
  ['@gen--maine', '@@gen--maine'],
  ['Gen--Maine', ' @ gen--maine'],
  ['Jo\'s "Kid" 4x4', '@jo.4x4'],
  ['Kai 2x4 -- O\'Neil', ''],
  ['Lena', 'lena'],
  ['D\'Arcy', '＠darcy--4x4'],
];
const b = await launch(); const ctx = await b.newContext({ viewport: { width: 1440, height: 1000 } }); await login(ctx, B);
const errs = []; const made = [];
if (!nocreate) {
  for (const [i, [title, handle]] of CASES.entries()) {
    const p = await ctx.newPage(); watch(p, errs);
    await p.goto(B + '/wp-admin/post-new.php?post_type=gm_creator'); await p.waitForSelector('#gm_creator_details', { state: 'attached', timeout: 60000 }); await p.waitForTimeout(3000); await dismissGuide(p);
    await metaDrawer(p, false);
    const hasFrame = await p.locator('iframe[name="editor-canvas"]').count(); const cv = hasFrame ? p.frameLocator('iframe[name="editor-canvas"]') : p;
    await cv.locator('h1.wp-block-post-title, .editor-post-title__input').first().click(); await p.keyboard.type(title); await p.keyboard.press('Enter'); await p.keyboard.type('Story for ' + title + ', who says "it\'s home" -- 4x4.');
    await metaDrawer(p, true);
    if (handle) { await p.locator('#gm_handle').click(); await p.keyboard.type(handle); }
    await p.locator('#gm_hometown').click(); await p.keyboard.type('Houlton');
    await p.locator('#gm_clip_url').click(); await p.keyboard.type(B + '/wp-content/uploads/2026/10/small-a.gif');
    await p.locator('#gm_instagram').click(); await p.keyboard.type('https://www.instagram.com/case' + i + '/');
    await p.locator('#gm_order').click(); await p.keyboard.press('Control+A'); await p.keyboard.type('-' + (CASES.length - i));
    await p.keyboard.press('Tab');
    await publishOrUpdate(p);
    const id = await p.evaluate(() => wp.data.select('core/editor').getCurrentPostId());
    made.push({ title, handle, id, storedTitle: wp(inst, `post get ${id} --field=post_title`), storedHandle: wp(inst, `post meta get ${id} gm_handle`).split('\n').pop() });
    await p.close();
  }
  // settings: follow rows from a handle typed with 4x4 and --, and from an address
  const s = await ctx.newPage(); watch(s, errs);
  await s.goto(B + '/wp-admin/options-general.php?page=generation_maine');
  await s.fill('#gm_instagram_handle', '@maine.4x4'); await s.fill('#gm_instagram_url', 'https://www.instagram.com/maine.4x4/');
  await s.fill('#gm_tiktok_handle', ''); await s.fill('#gm_tiktok_url', 'https://www.tiktok.com/@generation--maine');
  await s.fill('#gm_youtube_handle', '@generation--maine'); await s.fill('#gm_youtube_url', 'https://www.youtube.com/@generation--maine');
  await Promise.all([s.waitForNavigation(), s.click('#submit')]);
  await s.close();
}
// a page with the roster
let rosterId = wp(inst, `post list --post_type=page --title="Roster r4" --field=ID`).split('\n').pop();
if (!/^\d+$/.test(rosterId)) rosterId = wp(inst, `post create --post_type=page --post_status=publish --post_title="Roster r4" --post_content='<!-- wp:generation-maine/creators {"layout":"roster"} /-->' --porcelain`).split('\n').pop();
const res = { made, rosterId };
for (const [w, h] of [[1440, 900], [320, 640]]) {
  const vc = await b.newContext({ viewport: { width: w, height: h }, isMobile: w < 800, hasTouch: w < 800 }); const v = await vc.newPage(); watch(v, errs);
  await v.goto(B + '/?n=' + Date.now()); await v.waitForTimeout(1000);
  const r = await v.evaluate(() => {
    const t = s => [...document.querySelectorAll(s)].map(e => e.innerText.replace(/\n/g, ' / '));
    const panels = [...document.querySelectorAll('article.panel')];
    return {
      stageWho: t('.stage .who, #stage .who').slice(0, 8), cardWho: t('.slide .who').slice(0, 8), panelH2: t('article.panel h2').slice(0, 8), capStrong: t('.slide .cap strong').slice(0, 8),
      soc: [...document.querySelectorAll('article.panel .soc a span')].slice(0, 8).map(e => e.textContent),
      segAria: [...document.querySelectorAll('[data-name]')].slice(0, 8).map(e => e.getAttribute('aria-label') + ' | data-name=' + e.dataset.name),
      pvAria: [...document.querySelectorAll('.pv[aria-label]')].slice(0, 8).map(e => e.getAttribute('aria-label')),
      next: (document.getElementById('wnext') || {}).textContent,
      follow: [...document.querySelectorAll('.follow .row')].map(r => (r.querySelector('.h') || {}).textContent),
      followHtml: [...document.querySelectorAll('.follow .row .h')].slice(0, 3).map(e => e.innerHTML),
      bdiStyle: (() => { const bd = document.querySelector('.follow .row .h bdi'); const sp = bd && bd.parentElement; if (!bd) return null; const a = getComputedStyle(bd), c = getComputedStyle(sp); return { bdi: [a.fontFamily, a.fontSize, a.letterSpacing, a.color, a.display, a.unicodeBidi].join(' ; '), span: [c.fontFamily, c.fontSize, c.letterSpacing, c.color].join(' ; ') }; })(),
      sw: document.documentElement.scrollWidth,
    };
  });
  // the Next label for the first creator and after moving to the second
  if (w < 800) {
    // open the viewer from card 1 and read its caption, then swipe/next to 2
    const card = v.locator('.slide .fr').first(); await card.scrollIntoViewIfNeeded().catch(() => {}); await card.click().catch(() => {}); await v.waitForTimeout(800);
    r.viewer = await v.evaluate(() => { const vw = document.getElementById('viewer'); return vw ? { open: !vw.hidden && getComputedStyle(vw).display !== 'none', cap: (vw.querySelector('.cap, .vcap') || {}).innerText, text: vw.innerText.replace(/\n/g, ' / ').slice(0, 300) } : null; });
    await v.screenshot({ path: `${SHOTS}/names-${tag}-${w}-viewer.png` });
    await v.keyboard.press('Escape'); await v.waitForTimeout(400);
  } else {
    // step to creator 2 on desktop by scrolling to its panel
    await v.evaluate(() => { const p = document.querySelectorAll('article.panel')[1]; if (p) p.scrollIntoView({ block: 'center' }); }); await v.waitForTimeout(1200);
    r.nextAt2 = await v.evaluate(() => [(document.getElementById('wnext') || {}).textContent]);
    r.nextHtml = await v.evaluate(() => { const n = document.querySelector('[data-next]'); return n ? n.outerHTML.slice(0, 200) : null; });
    await v.evaluate(() => { const p = document.querySelector('article.panel'); if (p) p.scrollIntoView({ block: 'center' }); }); await v.waitForTimeout(1200);
    r.nextAt1 = await v.evaluate(() => [(document.getElementById('wnext') || {}).textContent]);
    await v.screenshot({ path: `${SHOTS}/names-${tag}-${w}-stage.png` });
  }
  const q = await vc.newPage(); await q.goto(B + '/?page_id=' + rosterId); await q.waitForTimeout(600);
  r.roster = await q.evaluate(() => ({ tiles: [...document.querySelectorAll('.roster .tile')].slice(0, 8).map(e => e.innerText.replace(/\n/g, ' / ') + ' | aria=' + (e.getAttribute('aria-label') || '')), sw: document.documentElement.scrollWidth }));
  await q.screenshot({ path: `${SHOTS}/names-${tag}-${w}-roster.png` });
  res['w' + w] = r; await vc.close();
}
const html = await (await fetch(B + '/?n=' + Date.now())).text();
res.rawWho = [...new Set([...html.matchAll(/<div class="who[^"]*">(?:<img[^>]*>|<svg[\s\S]*?<\/svg>)?<span>([\s\S]*?)<\/span><\/div>/g)].map(m => m[1]))].slice(0, 10);
res.rawTexturized = (html.match(/&#215;|&#8211;|&#8212;|&#8217;|&#8220;|&#8221;|×|–/g) || []).length;
res.rawTexturizedSamples = [...html.matchAll(/.{60}(?:&#215;|&#8211;|&#8217;|&#8220;).{30}/g)].slice(0, 12).map(m => m[0]);
res.errors = errs.filter(e => !/CERT|favicon|^dialog/.test(e));
fs.writeFileSync(`/tmp/claude-0/wptest/work/smoke-admin/logs/names-${tag}.json`, JSON.stringify(res, null, 1));
console.log(JSON.stringify(res, null, 1));
await b.close();
