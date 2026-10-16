// A creator whose chosen clip was deleted from the Media Library: the box shows no clip (it posts 0). Opening the editor and
// clicking around must not mark the post changed; a Hometown change saved with Ctrl+S also clears the stale clip id.
//   GMB=<base> GMI=<instance> node goneclip.mjs <run> <creatorId>
import { browser, login, B, W, wp } from './lib2.mjs';
import { openMetaBoxes, waitSaved } from './editor-lib2.mjs';
import fs from 'fs';
const [run, idS] = process.argv.slice(2); const id = +idS;
const out = { run, id, clipBefore: wp(`post meta get ${id} gm_clip_id`) };
const b = await browser(); const ctx = await b.newContext({ viewport: { width: 1400, height: 1000 } }); const page = await login(ctx, 'admin', 'adminpass');
const errs = []; page.on('pageerror', e => errs.push(e.message));
await page.goto(B + `/wp-admin/post.php?post=${id}&action=edit`); await page.waitForSelector('#gm_hometown', { state: 'attached', timeout: 60000 }); await page.waitForTimeout(2000);
for (let i = 0; i < 3; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click(); await page.waitForTimeout(400); } }
await openMetaBoxes(page);
out.boxClipField = await page.inputValue('#gm_clip_id');
out.storeClip = await page.evaluate(() => wp.data.select('core/editor').getEditedPostAttribute('meta').gm_clip_id);
await page.click('#gm_handle'); await page.click('#gm_instagram'); await page.click('#gm_order'); await page.mouse.click(700, 300); await page.waitForTimeout(500);
out.cleanAfterClicks = !(await page.evaluate(() => wp.data.select('core/editor').isEditedPostDirty()));
await page.click('#gm_hometown', { clickCount: 3 }); await page.keyboard.type('Gone clip town');
await page.keyboard.press('Control+s'); await page.waitForTimeout(2500); await waitSaved(page);
out.after = { hometown: wp(`post meta get ${id} gm_hometown`), clip: wp(`post meta get ${id} gm_clip_id`) };
out.errors = errs;
fs.writeFileSync(`${W}/goneclip-${run}.json`, JSON.stringify(out, null, 1)); console.log(JSON.stringify(out));
await b.close();
