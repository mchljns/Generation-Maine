// COM-N03 on WP 7.1: Add creator, open Meta Boxes (mouse or keyboard), measure drawer and canvas; next Add creator; drag the drawer
// usage: node drawer.mjs <port> <tag> <WxH> <mouse|keyboard> [drag]
import { launch, base, login, SHOTS, watch, dismissGuide } from './lib.mjs';
const [port, tag, size, how, drag] = process.argv.slice(2); const B = base(port);
const [vw, vh] = size.split('x').map(Number);
const b = await launch(); const ctx = await b.newContext({ viewport: { width: vw, height: vh } }); await login(ctx, B);
const p = await ctx.newPage(); const errs = []; watch(p, errs); p.setDefaultTimeout(60000);
const state = async (t) => {
  const s = await p.evaluate(() => { const r = e => { if (!e) return null; const b = e.getBoundingClientRect(); return [Math.round(b.top), Math.round(b.height)]; }; return { drawer: r(document.querySelector('.edit-post-meta-boxes-main')), canvas: r(document.querySelector('iframe[name="editor-canvas"]')), expanded: (document.querySelector('.edit-post-meta-boxes-main [aria-expanded]') || { getAttribute: () => null }).getAttribute('aria-expanded'), pref: wp.data.select('core/preferences').get('core/edit-post', 'metaBoxesMainOpenHeight'), placeVisible: (() => { const f = document.getElementById('gm_order'); if (!f) return null; const b = f.getBoundingClientRect(); return b.height > 0; })() }; });
  const c = p.frames().find(f => f.name() === 'editor-canvas');
  s.titleVisible = c ? await c.evaluate(() => { const t = document.querySelector('h1.wp-block-post-title, .editor-post-title__input'); if (!t) return false; const b = t.getBoundingClientRect(); return b.height > 0 && b.bottom > 0 && b.top < innerHeight && innerHeight > 40; }) : null;
  console.log(tag, t, JSON.stringify(s)); await p.screenshot({ path: `${SHOTS}/drawer-${tag}-${t}.png` });
};
const open = async () => { await p.goto(B + '/wp-admin/post-new.php?post_type=gm_creator', { waitUntil: 'load' }); await p.waitForSelector('#gm_creator_details', { state: 'attached' }); await p.waitForTimeout(3500); await dismissGuide(p); };
await open(); await state('first-open');
const btn = p.locator('.edit-post-meta-boxes-main button[aria-expanded]').first();
if (how === 'keyboard') { await btn.focus(); await p.keyboard.press('Enter'); } else { const bb = await btn.boundingBox(); await p.mouse.click(bb.x + 40, bb.y + bb.height / 2); }
await p.waitForTimeout(1500); await state('after-open');
// type a title with the drawer open
const c = p.frameLocator('iframe[name="editor-canvas"]');
await c.locator('h1.wp-block-post-title, .editor-post-title__input').first().click({ timeout: 10000 }).then(() => p.keyboard.type('Drawer Test')).catch(e => console.log(tag, 'title click failed', e.message.split('\n')[0]));
if (drag) {
  const h = p.locator('.edit-post-meta-boxes-main .components-resizable-box__handle, .edit-post-meta-boxes-main [role="separator"]').first();
  const hb = await h.boundingBox().catch(() => null);
  if (hb) { await p.mouse.move(hb.x + hb.width / 2, hb.y + hb.height / 2); await p.mouse.down(); await p.mouse.move(hb.x + hb.width / 2, hb.y - 200, { steps: 8 }); await p.mouse.up(); await p.waitForTimeout(1000); await state('after-drag-up-200'); }
  else console.log(tag, 'no resize handle found');
}
await open(); await state('next-add-creator');
console.log(tag, 'errors', JSON.stringify(errs.filter(e => !/CERT|favicon/.test(e))));
await b.close();
