// PL-R2 recheck: every Creator details field, the clip picker and Remove, each on its own: Ctrl+S saves it (and nothing is
// lost), and leaving with only that change warns. Then Undo after a details change. Creator owned by another account.
//   GMB=<base> GMI=<instance> node dirty4.mjs <run> <creatorId>
import { browser, login, B, W, wp } from './lib2.mjs';
import { openMetaBoxes, waitSaved } from './editor-lib2.mjs';
import fs from 'fs';
const [run, idS, only] = process.argv.slice(2); const id = +idS;
const out = { run, id, before: { author: wp(`post get ${id} --field=post_author`), place: wp(`post get ${id} --field=menu_order`) }, ctrlS: {}, leave: {}, undo: {} };
const b = await browser(); const ctx = await b.newContext({ viewport: { width: 1400, height: 1000 } }); const page = await login(ctx, 'admin', 'adminpass');
const errs = []; page.on('pageerror', e => errs.push(e.message));
const reqs = []; page.on('request', r => { if (['POST', 'PUT'].includes(r.method()) && /wp-json|post\.php|rest_route/.test(r.url())) reqs.push(r.method() + ' ' + r.url().replace(B, '').replace(/[?&]_locale=user/, '').replace(/meta-box-loader-nonce=\w+/, 'nonce').slice(0, 70)); });
let onDialog = 'accept'; const dialogs = [];
page.on('dialog', async d => { dialogs.push(d.type()); if (onDialog === 'accept') await d.accept(); else await d.dismiss(); });
const dirty = () => page.evaluate(() => wp.data.select('core/editor').isEditedPostDirty());
async function open() {
  onDialog = 'accept';
  await page.goto(B + `/wp-admin/post.php?post=${id}&action=edit`); await page.waitForSelector('#gm_hometown', { state: 'attached', timeout: 60000 }); await page.waitForTimeout(2000);
  for (let i = 0; i < 3; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click(); await page.waitForTimeout(400); } }
  await openMetaBoxes(page);
}
const type = (sel, v) => async () => { await page.click(sel, { clickCount: 3 }); await page.keyboard.press('Control+a'); await page.keyboard.type(v); };
async function pick(nth) {
  await page.locator('#gm_clip_pick').focus(); await page.keyboard.press('Enter');
  await page.waitForSelector('.media-modal', { state: 'visible', timeout: 20000 }); await page.waitForTimeout(1500);
  await page.locator('.media-modal:visible .media-router button, .media-modal:visible .media-menu-item', { hasText: 'Media Library' }).first().click().catch(() => {});
  await page.waitForSelector('.media-modal:visible .attachments .attachment', { timeout: 30000 }); await page.waitForTimeout(1000);
  const a = page.locator('.media-modal:visible .attachments .attachment').nth(nth); const pid = await a.getAttribute('data-id'); await a.click(); await page.waitForTimeout(400);
  // keyboard: Tab to "Use this clip" would be long; press it with Enter after focusing it
  await page.locator('.media-modal:visible .media-button-select').focus(); await page.keyboard.press('Enter'); await page.waitForTimeout(800);
  return pid;
}
let n = 0;
const mk = (sfx) => ({
  handle: [type('#gm_handle', '@r4.h' + run + sfx), 'post meta get ' + id + ' gm_handle'],
  hometown: [type('#gm_hometown', 'R4 Town ' + run + sfx), 'post meta get ' + id + ' gm_hometown'],
  clipLink: [type('#gm_clip_url', 'https://example.org/r4-' + run + sfx + '.gif'), 'post meta get ' + id + ' gm_clip_url'],
  clipLength: [type('#gm_clip_len', '0:4' + run + sfx), 'post meta get ' + id + ' gm_clip_len'],
  instagram: [type('#gm_instagram', 'https://www.instagram.com/r4ig' + run + sfx + '/'), 'post meta get ' + id + ' gm_instagram'],
  tiktok: [type('#gm_tiktok', 'https://www.tiktok.com/@r4tt' + run + sfx), 'post meta get ' + id + ' gm_tiktok'],
  youtube: [type('#gm_youtube', 'https://www.youtube.com/@r4yt' + run + sfx), 'post meta get ' + id + ' gm_youtube'],
  placeholder: [async () => { await page.locator('input[name="gm_placeholder"]').focus(); await page.keyboard.press('Space'); }, 'post meta get ' + id + ' gm_placeholder'],
  place: [type('#gm_order', String(+out.before.place + 3 + sfx.length)), 'post get ' + id + ' --field=menu_order'],
  chooseClip: [async () => { out.picked = await pick(sfx ? 3 : 1); }, 'post meta get ' + id + ' gm_clip_id'],
  removeClip: [async () => { await page.locator('#gm_clip_clear').focus(); await page.keyboard.press('Enter'); await page.waitForTimeout(300); }, 'post meta get ' + id + ' gm_clip_id'],
});
let fields = mk('');
const keys = only ? only.split(',') : Object.keys(fields);
// Ctrl+S, one field per fresh editor load
for (const k of keys) {
  await open(); reqs.length = 0;
  const [act, read] = fields[k];
  const was = wp(read); await act(); await page.waitForTimeout(400);
  const d = await dirty(); const boxed = await page.evaluate(() => ({ clip: document.getElementById('gm_clip_id').value, ph: document.querySelector('input[name="gm_placeholder"]').checked }));
  await page.keyboard.press('Control+s'); await page.waitForTimeout(2500); await waitSaved(page);
  out.ctrlS[k] = { was, dirtyBeforeCtrlS: d, box: boxed, requests: [...reqs], stored: wp(read), dirtyAfter: await dirty(), author: wp(`post get ${id} --field=post_author`) };
  console.log('ctrlS', k, JSON.stringify(out.ctrlS[k]));
}
fields = mk('L');
// leave warning, one field per fresh editor load: the change is not saved, the dialog shows, and staying keeps the edit
for (const k of keys) {
  await open();
  const [act, read] = fields[k];
  if (k === 'removeClip' && (await page.evaluate(() => document.getElementById('gm_clip_id').value)) === '0') { await pick(2); await page.keyboard.press('Control+s'); await page.waitForTimeout(2500); await waitSaved(page); }
  const was = wp(read); await act(); await page.waitForTimeout(400);
  const d = await dirty();
  dialogs.length = 0; onDialog = 'dismiss';
  let nav = 'left';
  await page.goto(B + '/wp-admin/edit.php?post_type=gm_creator', { timeout: 6000 }).catch(e => { nav = 'stayed'; });
  await page.waitForTimeout(600);
  out.leave[k] = { dirty: d, dialogs: [...dialogs], nav, url: page.url().replace(B, ''), storedUnchanged: wp(read) === was };
  console.log('leave', k, JSON.stringify(out.leave[k]));
}
// Undo after a Creator details change
await open();
const ht0 = wp('post meta get ' + id + ' gm_hometown');
await type('#gm_hometown', 'Undo town ' + run)(); await page.waitForTimeout(300);
out.undo.dirtyAfterTyping = await dirty();
const undoBtn = page.locator('button[aria-label="Undo"]').first();
out.undo.undoEnabled = await undoBtn.isEnabled().catch(() => 'none');
await undoBtn.click().catch(e => out.undo.undoErr = String(e).slice(0, 80)); await page.waitForTimeout(600);
out.undo.afterUndo = { dirty: await dirty(), box: await page.inputValue('#gm_hometown'), storeMeta: await page.evaluate(() => (wp.data.select('core/editor').getEditedPostAttribute('meta') || {}).gm_hometown) };
reqs.length = 0; await page.locator('#gm_hometown').focus(); await page.keyboard.press('Control+s'); await page.waitForTimeout(2500); await waitSaved(page);
out.undo.afterCtrlS = { requests: [...reqs], stored: wp('post meta get ' + id + ' gm_hometown'), storedBefore: ht0 };
dialogs.length = 0; onDialog = 'dismiss'; let nav2 = 'left';
await page.goto(B + '/wp-admin/edit.php?post_type=gm_creator', { timeout: 6000 }).catch(() => { nav2 = 'stayed'; });
out.undo.leave = { dialogs: [...dialogs], nav: nav2 };
// the Update/Save button after Undo
await open(); await type('#gm_hometown', 'Undo2 town ' + run)(); await page.waitForTimeout(300); await undoBtn.click().catch(() => {}); await page.waitForTimeout(600);
const saveBtn = page.locator('.editor-header__settings button.editor-post-publish-button, .edit-post-header__settings button.editor-post-publish-button').first();
out.undo.saveButton = { text: await saveBtn.innerText().catch(() => ''), disabled: await saveBtn.getAttribute('aria-disabled').catch(() => '') };
reqs.length = 0; await saveBtn.click().catch(() => {}); await page.waitForTimeout(2500); await waitSaved(page);
out.undo.afterButton = { requests: [...reqs], stored: wp('post meta get ' + id + ' gm_hometown'), box: await page.inputValue('#gm_hometown') };
// Undo back to the saved value: the box keeps the typed text, the editor no longer counts a change
await open(); const ht1 = wp('post meta get ' + id + ' gm_hometown');
await page.click('#gm_hometown'); await page.keyboard.press('End'); await page.keyboard.type('XYZ'); await page.waitForTimeout(300);
out.undo2 = { dirtyAfterTyping: await dirty() };
for (let i = 0; i < 3; i++) { await undoBtn.click().catch(() => {}); await page.waitForTimeout(300); }
out.undo2.afterUndos = { dirty: await dirty(), box: await page.inputValue('#gm_hometown'), storeMeta: await page.evaluate(() => (wp.data.select('core/editor').getEditedPostAttribute('meta') || {}).gm_hometown), undoStillEnabled: await undoBtn.getAttribute('aria-disabled') };
reqs.length = 0; await page.locator('#gm_hometown').focus(); await page.keyboard.press('Control+s'); await page.waitForTimeout(2500); await waitSaved(page);
out.undo2.ctrlS = { requests: [...reqs], stored: wp('post meta get ' + id + ' gm_hometown'), storedBefore: ht1 };
dialogs.length = 0; onDialog = 'dismiss'; let nav3 = 'left';
await page.goto(B + '/wp-admin/edit.php?post_type=gm_creator', { timeout: 6000 }).catch(() => { nav3 = 'stayed'; });
out.undo2.leave = { dialogs: [...dialogs], nav: nav3, stored: wp('post meta get ' + id + ' gm_hometown') };
onDialog = 'accept';
out.after = { author: wp(`post get ${id} --field=post_author`), place: wp(`post get ${id} --field=menu_order`) };
out.authorKept = out.after.author === out.before.author; out.errors = errs;
fs.writeFileSync(`${W}/dirty4-${run}.json`, JSON.stringify(out, null, 1));
console.log(JSON.stringify({ undo: out.undo, undo2: out.undo2, before: out.before, after: out.after, errors: errs }, null, 1));
await b.close();
