// Screenshot: type into Hometown, press the editor's Undo until the editor counts no change; the box still shows the text.
import { browser, login, B, wp } from './lib2.mjs';
import { openMetaBoxes } from './editor-lib2.mjs';
const [id, tag] = process.argv.slice(2);
const b = await browser(); const ctx = await b.newContext({ viewport: { width: 1400, height: 1000 } }); const page = await login(ctx, 'admin', 'adminpass');
await page.goto(B + `/wp-admin/post.php?post=${id}&action=edit`); await page.waitForSelector('#gm_hometown', { state: 'attached', timeout: 60000 }); await page.waitForTimeout(2000);
for (let i = 0; i < 3; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click(); await page.waitForTimeout(400); } }
await openMetaBoxes(page);
const saved = wp(`post meta get ${id} gm_hometown`);
await page.click('#gm_hometown'); await page.keyboard.press('End'); await page.keyboard.type(' Typed'); await page.waitForTimeout(300);
const undo = page.locator('button[aria-label="Undo"]').first();
for (let i = 0; i < 6; i++) { await undo.click(); await page.waitForTimeout(250); }
const st = await page.evaluate(() => ({ dirty: wp.data.select('core/editor').isEditedPostDirty(), box: document.getElementById('gm_hometown').value, saveLabel: (document.querySelector('.editor-post-publish-button, .editor-post-save-draft, .editor-post-saved-state') || {}).textContent }));
await page.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-admin/shots/undo-${tag}.png` });
const dialogs = []; page.on('dialog', async d => { dialogs.push(d.type()); await d.accept(); });
await page.goto(B + '/wp-admin/edit.php?post_type=gm_creator').catch(() => {});
console.log(JSON.stringify({ saved, ...st, leaveDialogs: dialogs, storedAfterLeave: wp(`post meta get ${id} gm_hometown`) }));
await b.close();
