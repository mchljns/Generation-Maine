// CRE-N01 / COM-N02: Place on the page vs WordPress's Order (Actions on 7.x, Post Attributes on 6.5) vs Quick Edit, one browser session.
// usage: node order.mjs <port> <tag> step step ...
//   open:ID  place:N (typed with the keyboard)  arrow:Up3|Down2  actions:N  attr:N  title:TEXT  hometown:TEXT  update  savekbd
//   reload  qe:ID:N (Quick Edit in the Creators list)  check
import { launch, base, login, wp, INST, SHOTS, watch, metaDrawer, publishOrUpdate, openEditor, dismissGuide } from './lib.mjs';
const [port, tag, ...steps] = process.argv.slice(2);
const B = base(port), inst = INST[port];
const b = await launch();
const ctx = await b.newContext({ viewport: { width: 1440, height: 1000 } });
await login(ctx, B);
const p = await ctx.newPage(); const errs = []; watch(p, errs);
let cur = 0; const log = (...a) => console.log(...a);
const db = (id) => wp(inst, `post get ${id} --field=menu_order`).split('\n').filter(l => /^-?\d+$/.test(l.trim())).join('');
const frontOrder = async () => { const r = await fetch(B + '/?n=' + Date.now()); const h = await r.text(); return [...h.matchAll(/data-name="([^"]+)"/g)].map(m => m[1]).join(','); };
async function listOrder() { const q = await ctx.newPage(); await q.goto(B + '/wp-admin/edit.php?post_type=gm_creator'); const r = await q.$$eval('#the-list tr', trs => trs.map(t => (t.querySelector('.row-title') || {}).textContent + ':' + ((t.querySelector('td.gm_order, td.column-gm_order') || {}).textContent || '').trim()).join(',')); await q.close(); return r; }
async function sidebarOrder() {
  const pa = p.getByRole('button', { name: 'Post Attributes' });
  if (await pa.count()) { if ((await pa.first().getAttribute('aria-expanded')) === 'false') { await pa.first().click(); await p.waitForTimeout(400); } const f = p.getByLabel('Order', { exact: true }); return (await f.count()) ? await f.first().inputValue() : '(none)'; }
  return '(no panel)';
}
async function state(s) {
  const onEditor = /post\.php|post-new\.php/.test(p.url());
  const place = onEditor && await p.locator('#gm_order').count() ? await p.inputValue('#gm_order') : '-';
  const edited = onEditor ? await p.evaluate(() => wp.data.select('core/editor').getEditedPostAttribute('menu_order')).catch(() => '?') : '-';
  log(`after ${s}: Place=${place} editorStore=${edited} sidebarOrder=${onEditor ? await sidebarOrder() : '-'} stored=${db(cur)} | list ${await listOrder()} | front ${await frontOrder()}`);
}
for (const s of steps) {
  const [cmd, ...rest] = s.split(':'); const arg = rest.join(':');
  if (cmd === 'open') { cur = +arg; await openEditor(p, B, cur); await metaDrawer(p, true); }
  else if (cmd === 'reload') { await openEditor(p, B, cur); await metaDrawer(p, true); }
  else if (cmd === 'place') { await p.locator('#gm_order').click(); await p.keyboard.press('Control+A'); await p.keyboard.type(arg, { delay: 60 }); await p.keyboard.press('Tab'); }
  else if (cmd === 'arrow') { const m = arg.match(/(Up|Down)(\d+)/); await p.locator('#gm_order').focus(); for (let i = 0; i < +m[2]; i++) await p.keyboard.press('Arrow' + m[1]); await p.keyboard.press('Tab'); }
  else if (cmd === 'actions') {
    await p.locator('.interface-complementary-area').getByRole('button', { name: 'Actions' }).click(); await p.waitForTimeout(500);
    await p.getByRole('menuitem', { name: 'Order' }).click(); await p.waitForTimeout(800);
    const dlg = p.getByRole('dialog').last(); const inp = dlg.locator('input').first();
    log('  actions dialog shows', await inp.inputValue());
    await inp.click(); await p.keyboard.press('Control+A'); await p.keyboard.type(arg, { delay: 50 });
    await dlg.getByRole('button', { name: /Save/ }).click(); await p.waitForTimeout(3000);
    log('  actions notices', JSON.stringify(await p.locator('.components-snackbar').allInnerTexts()));
  }
  else if (cmd === 'attr') { await sidebarOrder(); const f = p.getByLabel('Order', { exact: true }).first(); await f.click(); await p.keyboard.press('Control+A'); await p.keyboard.type(arg, { delay: 50 }); await p.keyboard.press('Tab'); await p.waitForTimeout(300); }
  else if (cmd === 'title') { const hasFrame = await p.locator('iframe[name="editor-canvas"]').count(); const canvas = hasFrame ? p.frameLocator('iframe[name="editor-canvas"]') : p; await metaDrawer(p, false); await canvas.locator('h1.wp-block-post-title, .editor-post-title__input').first().click(); await p.keyboard.press('End'); await p.keyboard.type(arg); await metaDrawer(p, true); }
  else if (cmd === 'hometown') { await p.locator('#gm_hometown').click(); await p.keyboard.press('Control+A'); await p.keyboard.type(arg); }
  else if (cmd === 'update') { log('  save', JSON.stringify(await publishOrUpdate(p))); }
  else if (cmd === 'savekbd') { await p.keyboard.press('Control+S'); await p.waitForTimeout(5000); log('  ctrl+s', JSON.stringify(await p.locator('.components-snackbar').allInnerTexts())); }
  else if (cmd === 'qe') {
    const [id, n] = arg.split(':'); cur = +id;
    await p.goto(B + '/wp-admin/edit.php?post_type=gm_creator');
    const row = p.locator('#post-' + id); await row.hover(); await row.locator('button.editinline').click();
    const qe = p.locator('tr.inline-edit-row').first(); const o = qe.locator('input[name="menu_order"]');
    log('  quick edit Order shows', await o.inputValue());
    await o.click(); await p.keyboard.press('Control+A'); await p.keyboard.type(n);
    await qe.locator('button.save').click(); await p.waitForTimeout(2500);
  }
  if (cmd !== 'open' || true) await state(s);
}
await p.screenshot({ path: `${SHOTS}/order-${tag}.png` });
log('errors', JSON.stringify(errs.filter(e => !/CERT|favicon/.test(e))));
await b.close();
