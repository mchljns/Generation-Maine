// Editor open in one tab, Quick Edit Order in another tab, then Update in the editor tab (meta box change only, then title change)
import { launch, base, login, wp, INST, watch, metaDrawer, publishOrUpdate, openEditor } from './lib.mjs';
const [port, id] = process.argv.slice(2); const B = base(port), inst = INST[port];
const b = await launch(); const ctx = await b.newContext({ viewport: { width: 1440, height: 1000 } }); await login(ctx, B);
const db = () => wp(inst, `post get ${id} --field=menu_order`).split('\n').pop();
const a = await ctx.newPage(); const errs = []; watch(a, errs); await openEditor(a, B, id); await metaDrawer(a, true);
console.log('editor tab Place', await a.inputValue('#gm_order'), 'stored', db());
const q = await ctx.newPage(); await q.goto(B + '/wp-admin/edit.php?post_type=gm_creator'); const row = q.locator('#post-' + id); await row.hover(); await row.locator('button.editinline').click();
const o = q.locator('tr.inline-edit-row input[name="menu_order"]').first(); await o.click(); await q.keyboard.press('Control+A'); await q.keyboard.type('11'); await q.locator('tr.inline-edit-row button.save').first().click(); await q.waitForTimeout(2500);
console.log('after Quick Edit 11 in the other tab: stored', db());
await a.bringToFront(); await a.locator('#gm_hometown').click(); await a.keyboard.press('End'); await a.keyboard.type(' x');
console.log('update (hometown only)', JSON.stringify(await publishOrUpdate(a)), 'stored', db(), 'editor tab Place', await a.inputValue('#gm_order'));
await metaDrawer(a, false); const cv = a.frameLocator('iframe[name="editor-canvas"]'); await cv.locator('h1.wp-block-post-title').first().click(); await a.keyboard.press('End'); await a.keyboard.type('y'); await metaDrawer(a, true);
console.log('update (title)', JSON.stringify(await publishOrUpdate(a)), 'stored', db());
await a.locator('#gm_order').click(); await a.keyboard.press('Control+A'); await a.keyboard.type('4'); await a.keyboard.press('Tab');
console.log('update (Place 4)', JSON.stringify(await publishOrUpdate(a)), 'stored', db());
console.log('errors', JSON.stringify(errs.filter(e => !/CERT|favicon|^dialog/.test(e))));
await b.close();
