// Probe: type in Hometown, press Ctrl+Z inside the box, then Ctrl+Shift+Z; report box/store/dirty each step.
//   GMB=<base> GMI=<instance> node ctrlz.mjs <creatorId> [text]
import { browser, login, B, wp } from './lib2.mjs';
import { openMetaBoxes } from './editor-lib2.mjs';
const [idS, text = ' Typed'] = process.argv.slice(2); const id = +idS;
const b = await browser(); const ctx = await b.newContext({ viewport: { width: 1400, height: 1000 } }); const page = await login(ctx, 'admin', 'adminpass');
const errs = []; page.on('pageerror', e => errs.push(e.message));
await page.goto(B + `/wp-admin/post.php?post=${id}&action=edit`); await page.waitForSelector('#gm_hometown', { state: 'attached', timeout: 60000 }); await page.waitForTimeout(2000);
for (let i = 0; i < 3; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click(); await page.waitForTimeout(400); } }
await openMetaBoxes(page);
const st = (label) => page.evaluate((label) => { const e = wp.data.select('core/editor'); return { label, dirty: e.isEditedPostDirty(), box: document.getElementById('gm_hometown').value, store: (e.getEditedPostAttribute('meta') || {}).gm_hometown, hasUndo: e.hasEditorUndo(), hasRedo: e.hasEditorRedo(), focus: document.activeElement && document.activeElement.id }; }, label);
const out = [];
out.push(await st('open'));
await page.click('#gm_hometown'); await page.keyboard.press('End'); await page.keyboard.type(text); await page.waitForTimeout(300);
out.push(await st('typed'));
for (let i = 0; i < 3; i++) { await page.keyboard.press('Control+z'); await page.waitForTimeout(250); out.push(await st('ctrlz' + (i + 1))); }
await page.keyboard.press('Control+Shift+z'); await page.waitForTimeout(250); out.push(await st('redo1'));
for (let i = 0; i < 10; i++) { await page.keyboard.press('Control+z'); await page.waitForTimeout(150); }
out.push(await st('ctrlz x10 more'));
console.log(JSON.stringify({ saved: wp(`post meta get ${id} gm_hometown`), steps: out, errs }).replace(/\},\{/g, '},\n{'));
await b.close();
