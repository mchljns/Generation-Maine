// Undo with other edits around a Creator details change: the title, then Hometown, then Place; Undo and Redo with the top bar
// buttons and with Ctrl+Z in the canvas. Box and store must agree after every step; then Ctrl+S saves what the box shows.
//   GMB=<base> GMI=<instance> node undomix.mjs <creatorId>
import { browser, login, B, wp } from './lib2.mjs';
import { openMetaBoxes, waitSaved } from './editor-lib2.mjs';
const id = +process.argv[2];
const b = await browser(); const ctx = await b.newContext({ viewport: { width: 1400, height: 1000 } }); const page = await login(ctx, 'admin', 'adminpass');
const errs = []; page.on('pageerror', e => errs.push(e.message));
const reqs = []; page.on('request', r => { if (['POST', 'PUT'].includes(r.method()) && /wp-json|post\.php|rest_route/.test(r.url())) reqs.push(r.method() + ' ' + r.url().replace(B, '').slice(0, 60)); });
await page.goto(B + `/wp-admin/post.php?post=${id}&action=edit`); await page.waitForSelector('#gm_hometown', { state: 'attached', timeout: 60000 }); await page.waitForTimeout(2000);
for (let i = 0; i < 3; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click(); await page.waitForTimeout(400); } }
await openMetaBoxes(page);
const canvas = (await page.$('iframe[name="editor-canvas"]')) ? page.frameLocator('iframe[name="editor-canvas"]') : page;
const st = (label) => page.evaluate((label) => { const e = wp.data.select('core/editor'); const m = e.getEditedPostAttribute('meta') || {}; return { label, dirty: e.isEditedPostDirty(), title: e.getEditedPostAttribute('title'), box: document.getElementById('gm_hometown').value, store: m.gm_hometown, boxPlace: document.getElementById('gm_order').value, storePlace: e.getEditedPostAttribute('menu_order'), hasUndo: e.hasEditorUndo(), hasRedo: e.hasEditorRedo(), agree: document.getElementById('gm_hometown').value === m.gm_hometown }; }, label);
const undoBtn = page.locator('button[aria-label="Undo"]').first(); const redoBtn = page.locator('button[aria-label="Redo"]').first();
const click = async (btn) => btn.click({ timeout: 3000 }).then(() => 'clicked', () => 'disabled');
const out = [];
const saved = { title: wp(`post get ${id} --field=post_title`), town: wp(`post meta get ${id} gm_hometown`), place: wp(`post get ${id} --field=menu_order`) };
out.push(await st('open'));
// 1. title
const t = canvas.locator('h1.wp-block-post-title, [aria-label="Add title"]').first(); await t.click(); await page.keyboard.press('End'); await page.keyboard.type(' T'); await page.waitForTimeout(400);
out.push(await st('title typed'));
// 2. hometown
await page.click('#gm_hometown'); await page.keyboard.press('End'); await page.keyboard.type(' Mix'); await page.waitForTimeout(400);
out.push(await st('hometown typed'));
// 3. top bar Undo: the title goes back, the box keeps ' Mix'
out.push({ ...(await st('after Undo ' + (await click(undoBtn)))) });
out.push({ ...(await st('after Undo again ' + (await click(undoBtn)))) });
out.push({ ...(await st('after Redo ' + (await click(redoBtn)))) });
// 4. Place: typed in the box; Undo in the top bar puts the field back (the editor's own value, written into the box)
await page.click('#gm_order', { clickCount: 3 }); await page.keyboard.type('11'); await page.waitForTimeout(300);
await page.click('#gm_handle'); await page.waitForTimeout(300);
out.push(await st('place typed'));
out.push({ ...(await st('after Undo ' + (await click(undoBtn)))) });
out.push({ ...(await st('after Undo ' + (await click(undoBtn)))) });
// 5. Ctrl+Z with the cursor in the title (canvas)
await t.click(); await page.keyboard.press('Control+z'); await page.waitForTimeout(400);
out.push(await st('Ctrl+Z in the title'));
// 6. Ctrl+S saves what the box shows
reqs.length = 0; await page.keyboard.press('Control+s'); await page.waitForTimeout(2500); await waitSaved(page);
const after = { title: wp(`post get ${id} --field=post_title`), town: wp(`post meta get ${id} gm_hometown`), place: wp(`post get ${id} --field=menu_order`), author: wp(`post get ${id} --field=post_author`) };
out.push({ ...(await st('after Ctrl+S')), requests: [...reqs] });
console.log(JSON.stringify({ saved, after, steps: out, errs }).replace(/\},\{/g, '},\n{'));
await b.close();
