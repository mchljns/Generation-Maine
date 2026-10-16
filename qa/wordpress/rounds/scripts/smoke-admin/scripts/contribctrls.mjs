// A Contributor's new creator: title, then Hometown and a clip link in Creator details, Ctrl+S saves the draft with both; then a
// Handle change alone, Ctrl+S again.
//   GMB=<base> GMI=<instance> node contribctrls.mjs <run>
import { browser, login, B, W, wp } from './lib2.mjs';
import { openNewCreator, fillTitleAndBio, openMetaBoxes, waitSaved, currentId } from './editor-lib2.mjs';
import fs from 'fs';
const run = process.argv[2] || '1';
const out = { run };
const b = await browser(); const ctx = await b.newContext({ viewport: { width: 1400, height: 1000 } }); const page = await login(ctx, 'contrib1', 'contribpass');
const errs = []; page.on('pageerror', e => errs.push(e.message)); page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text().slice(0, 120)); });
const reqs = []; page.on('response', r => { if (['POST', 'PUT'].includes(r.request().method()) && /wp-json\/wp\/v2\/gm_creator|meta-box-loader/.test(r.url())) reqs.push(r.status() + ' ' + r.url().replace(B, '').slice(0, 60)); });
const canvas = await openNewCreator(page); await fillTitleAndBio(page, canvas, 'Contrib draft ' + run, 'My words.');
await openMetaBoxes(page);
await page.fill('#gm_hometown', 'Bath'); await page.fill('#gm_clip_url', 'https://example.org/contrib-' + run + '.mp4');
await page.focus('#gm_clip_url'); await page.keyboard.press('Control+s'); await page.waitForTimeout(3000); await waitSaved(page);
const id = await currentId(page); out.id = id;
out.first = { requests: [...reqs], status: wp(`post get ${id} --field=post_status`), hometown: wp(`post meta get ${id} gm_hometown`), link: wp(`post meta get ${id} gm_clip_url`), author: wp(`post get ${id} --field=post_author`) };
reqs.length = 0;
await page.click('#gm_handle'); await page.keyboard.type('@contrib' + run);
out.dirty = await page.evaluate(() => wp.data.select('core/editor').isEditedPostDirty());
await page.keyboard.press('Control+s'); await page.waitForTimeout(3000); await waitSaved(page);
out.second = { requests: [...reqs], handle: wp(`post meta get ${id} gm_handle`), author: wp(`post get ${id} --field=post_author`) };
out.errors = errs;
fs.writeFileSync(`${W}/contribctrls-${run}.json`, JSON.stringify(out, null, 1)); console.log(JSON.stringify(out, null, 1));
await b.close();
