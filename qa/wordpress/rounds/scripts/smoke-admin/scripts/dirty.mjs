// PL-R2: a change made only in Creator details marks the post dirty, Ctrl+S saves it (both requests), and leaving warns.
// One editor session as admin on a creator owned by another account and placed at a known Place; after each Ctrl+S the
// stored values are read with WP-CLI. Ends by checking that the author and the place were kept.
//   GMB=<base> GMI=<instance> node dirty.mjs <run> <creatorId>
import { browser, login, B, W, wp } from './lib2.mjs';
import { openMetaBoxes, waitSaved } from './editor-lib2.mjs';
import fs from 'fs';
const [run, idS] = process.argv.slice(2); const id = +idS;
const out = { run, id, before: { author: wp(`post get ${id} --field=post_author`), place: wp(`post get ${id} --field=menu_order`), clip: wp(`post meta get ${id} gm_clip_id`) }, steps: {} };
const b = await browser(); const ctx = await b.newContext({ viewport: { width: 1400, height: 1000 } }); const page = await login(ctx, 'admin', 'adminpass');
const errs = []; page.on('pageerror', e => errs.push(e.message));
const reqs = []; page.on('request', r => { if (['POST', 'PUT'].includes(r.method()) && /wp-json|post\.php|rest_route/.test(r.url())) reqs.push(r.method() + ' ' + r.url().replace(B, '').replace(/[?&]_locale=user/, '').replace(/meta-box-loader-nonce=\w+/, 'nonce').slice(0, 90)); });
const dirty = () => page.evaluate(() => wp.data.select('core/editor').isEditedPostDirty());
async function open() {
  await page.goto(B + `/wp-admin/post.php?post=${id}&action=edit`); await page.waitForSelector('#gm_hometown', { state: 'attached', timeout: 60000 }); await page.waitForTimeout(2000);
  for (let i = 0; i < 3; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click(); await page.waitForTimeout(400); } }
  await openMetaBoxes(page);
}
async function ctrlS(name, act, key) {
  reqs.length = 0;
  await act();
  const d = await dirty();
  await page.keyboard.press('Control+s'); await page.waitForTimeout(2500); await waitSaved(page);
  out.steps[name] = { dirtyBeforeCtrlS: d, requests: [...reqs], stored: wp(`post meta get ${id} ${key}`), dirtyAfter: await dirty() };
  console.log(name, JSON.stringify(out.steps[name]));
}
const type = (sel, v) => async () => { await page.click(sel, { clickCount: 3 }); await page.keyboard.press('Control+a'); await page.keyboard.type(v); };
await open();
// opening the editor and clicking around Creator details without changing anything leaves the post clean
await page.click('#gm_handle'); await page.click('#gm_hometown'); await page.click('#gm_creator_details .description >> nth=0'); await page.waitForTimeout(500);
out.cleanAfterClicks = !(await dirty());
await ctrlS('handle', type('#gm_handle', '@ctrl.handle' + run), 'gm_handle');
await ctrlS('hometown', type('#gm_hometown', 'Ctrl Town ' + run), 'gm_hometown');
await ctrlS('clipLink', type('#gm_clip_url', 'https://example.org/ctrl-clip-' + run + '.gif'), 'gm_clip_url');
await ctrlS('instagram', type('#gm_instagram', 'https://www.instagram.com/ctrl.ig' + run + '/'), 'gm_instagram');
await ctrlS('clipLength', type('#gm_clip_len', '0:33'), 'gm_clip_len');
await ctrlS('removeClip', async () => { await page.click('#gm_clip_clear'); await page.waitForTimeout(300); }, 'gm_clip_id');
// choose a clip in the media library: the hidden field changes without an event of its own
let picked = '';
await ctrlS('chooseClip', async () => {
  await page.click('#gm_clip_pick'); await page.waitForSelector('.media-modal', { state: 'visible', timeout: 20000 }); await page.waitForTimeout(1500);
  await page.locator('.media-modal:visible .media-router button, .media-modal:visible .media-menu-item', { hasText: 'Media Library' }).first().click().catch(() => {});
  await page.waitForSelector('.media-modal:visible .attachments .attachment', { timeout: 30000 }); await page.waitForTimeout(1000);
  const a = page.locator('.media-modal:visible .attachments .attachment').first(); picked = await a.getAttribute('data-id'); await a.click(); await page.waitForTimeout(400);
  await page.click('.media-modal .media-button-select'); await page.waitForTimeout(600);
}, 'gm_clip_id');
out.steps.chooseClip.picked = picked;
await ctrlS('untickPlaceholder', async () => { await page.uncheck('input[name="gm_placeholder"]'); }, 'gm_placeholder');
await ctrlS('tickPlaceholder', async () => { await page.check('input[name="gm_placeholder"]'); }, 'gm_placeholder');
// a change typed back to the saved value leaves nothing to save
await page.click('#gm_hometown', { clickCount: 3 }); await page.keyboard.type('Temp'); out.dirtyAfterTyping = await dirty();
await page.click('#gm_hometown', { clickCount: 3 }); await page.keyboard.press('Control+a'); await page.keyboard.type('Ctrl Town ' + run); out.cleanAfterTypingBack = !(await dirty());
// Place on the page still saves with Ctrl+S
reqs.length = 0; await page.click('#gm_order', { clickCount: 3 }); await page.keyboard.type(String(+out.before.place + 1));
const dPlace = await dirty(); await page.keyboard.press('Control+s'); await page.waitForTimeout(2500); await waitSaved(page);
out.steps.place = { dirtyBeforeCtrlS: dPlace, requests: [...reqs], stored: wp(`post get ${id} --field=menu_order`) };
// values WordPress cleans on save (a trailing space, an address with no https://) do not leave the post changed afterwards
await ctrlS('trailingSpace', type('#gm_hometown', 'Spaced town '), 'gm_hometown');
await ctrlS('noScheme', type('#gm_youtube', 'youtube.com/@noscheme'), 'gm_youtube');
await page.click('#gm_handle'); await page.click('#gm_clip_len'); await page.mouse.click(600, 200); await page.waitForTimeout(600);
out.cleanAfterCleanedSave = !(await dirty());
// leaving with an unsaved Creator details change warns
await page.click('#gm_tiktok', { clickCount: 3 }); await page.keyboard.type('https://www.tiktok.com/@leave' + run);
const dialogs = []; const h = async d => { dialogs.push(d.type()); await d.dismiss(); }; page.on('dialog', h);
await page.goto(B + '/wp-admin/edit.php?post_type=gm_creator', { timeout: 8000 }).catch(e => dialogs.push('stayed: ' + String(e).split('\n')[0].slice(0, 60)));
await page.waitForTimeout(800); page.off('dialog', h);
out.leave = { dialogs, url: page.url().replace(B, ''), tiktokStored: wp(`post meta get ${id} gm_tiktok`) };
out.after = { author: wp(`post get ${id} --field=post_author`), place: wp(`post get ${id} --field=menu_order`) };
out.authorKept = out.after.author === out.before.author;
out.errors = errs;
fs.writeFileSync(`${W}/dirty-${run}.json`, JSON.stringify(out, null, 1)); console.log(JSON.stringify({ cleanAfterCleanedSave: out.cleanAfterCleanedSave, cleanAfterClicks: out.cleanAfterClicks, dirtyAfterTyping: out.dirtyAfterTyping, cleanAfterTypingBack: out.cleanAfterTypingBack, place: out.steps.place, leave: out.leave, before: out.before, after: out.after, errors: errs }, null, 1));
await b.close();
