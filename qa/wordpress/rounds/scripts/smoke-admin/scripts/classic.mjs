// Classic Editor plugin: Place on the page vs Page Attributes > Order, change and back, several saves; author kept; clip picker
import { launch, base, login, wp, INST, SHOTS, watch } from './lib.mjs';
const [port, id, authorsId] = process.argv.slice(2); const B = base(port), inst = INST[port];
const b = await launch(); const ctx = await b.newContext({ viewport: { width: 1440, height: 1000 } }); await login(ctx, B);
const p = await ctx.newPage(); const errs = []; watch(p, errs); const log = (...a) => console.log(...a);
const db = x => wp(inst, `post get ${x} --field=menu_order`).split('\n').pop();
const open = async (x) => { await p.goto(B + '/wp-admin/post.php?post=' + x + '&action=edit'); await p.waitForSelector('#gm_order'); const t = p.locator('#post-lock-dialog:visible a', { hasText: 'Take over' }); if (await t.count()) { await t.first().click(); await p.waitForSelector('#gm_order'); await p.waitForTimeout(800); } };
const save = async () => { await Promise.all([p.waitForNavigation({ timeout: 60000 }), p.click('#publish')]); await p.waitForSelector('#gm_order'); return (await p.locator('#message').innerText().catch(() => '')).split('\n')[0]; };
const st = async (s) => log(`${s}: Place=${await p.inputValue('#gm_order')} was=${await p.inputValue('input[name=gm_order_was]')} PageAttrOrder=${await p.locator('#menu_order').count() ? await p.inputValue('#menu_order') : '(none)'} stored=${db(id)}`);
const type = async (sel, v) => { await p.locator(sel).click(); await p.keyboard.press('Control+A'); await p.keyboard.type(v); };
const ONLYAUTHOR = process.env.ONLYAUTHOR; if (!ONLYAUTHOR) { await open(id); await st('open');
await type('#gm_order', '9'); log(' save', await save()); await st('place 9 + save');
await type('#gm_order', '5'); log(' save', await save()); await st('place back 5 + save');
if (await p.locator('#menu_order').count()) { await type('#menu_order', '2'); log(' save', await save()); await st('PageAttr 2 + save'); await type('#gm_order', '7'); await type('#menu_order', '3'); log(' save', await save()); await st('place 7 and PageAttr 3 in one save'); }
await type('#gm_order', '5'); log(' save', await save()); await st('place 5 + save');
}
// author kept
await open(authorsId); log('author before', wp(inst, `post get ${authorsId} --field=post_author`).split('\n').pop());
await type('#gm_hometown', 'Bath Classic'); log(' save', await save()); log('author after admin classic save', wp(inst, `post get ${authorsId} --field=post_author`).split('\n').pop(), 'hometown', wp(inst, `post meta get ${authorsId} gm_hometown`).split('\n').pop());
// clip picker opens in the classic editor
await p.locator('#gm_clip_pick').focus(); await p.keyboard.press('Enter'); const modal = await p.waitForSelector('.media-modal', { state: 'visible', timeout: 10000 }).then(() => true).catch(() => false);
log('clip picker opens', modal, modal ? await p.locator('.media-modal:visible .media-frame-title h1').innerText().catch(() => '') : '');
await p.screenshot({ path: `${SHOTS}/classic-${port}.png` });
log('errors', JSON.stringify(errs.filter(e => !/CERT|favicon|^dialog/.test(e))));
await b.close();
