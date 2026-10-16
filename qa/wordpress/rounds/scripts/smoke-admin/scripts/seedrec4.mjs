// Seed 3.0.0 recognition. As an Administrator, through the block editor: make creators by hand, one of them typed to match a
// seed exactly (name, story, handle, hometown, Placeholder), and change some of the 3.0.0 seeds. Then the README's removal
// command runs outside this script (seed-creators.php 0) and dump.sh lists what is left.
//   GMB=<base> GMI=<instance> node seedrec.mjs <run> <seedIndexToCopy> <noahId> <devinId> <tylerId>
import { browser, login, B, W } from './lib2.mjs';
import { openNewCreator, fillTitleAndBio, openMetaBoxes, fillMeta, submit, currentId, waitSaved } from './editor-lib2.mjs';
import fs from 'fs';
const [run, idxS, noah, devin, tyler, maya, amara, sam] = process.argv.slice(2);
const idx = +idxS;
const J = JSON.parse(fs.readFileSync('/home/user/Generation-Maine/generation-maine/bin/creators-placeholder.json', 'utf8')).creators;
const out = { run, made: {}, changed: {} };
const b = await browser(); const ctx = await b.newContext({ viewport: { width: 1400, height: 1100 } });
const page = await login(ctx, 'admin', 'adminpass');
const make = async (key, title, bio, meta) => {
  const canvas = await openNewCreator(page); await fillTitleAndBio(page, canvas, title, bio);
  await openMetaBoxes(page); await fillMeta(page, meta);
  await submit(page, 'Publish'); out.made[key] = await currentId(page); console.log(key, out.made[key]);
  await page.screenshot({ path: `${W}/shots/seedrec-${run}-${key}.png` });
};
// a person types a creator that copies a seed (for example to keep a sample while waiting for a recruit)
await make('handCopyOfSeed', J[idx].name, J[idx].bio, { gm_handle: J[idx].handle, gm_hometown: J[idx].town, gm_placeholder: true });
// control: a person's own pending recruit marked Placeholder
await make('ownRecruit', 'Pending recruit ' + run, 'Coming soon.', { gm_handle: '@recruit' + run, gm_hometown: 'Bath', gm_placeholder: true });
const edit = async (id) => {
  await page.goto(B + `/wp-admin/post.php?post=${id}&action=edit`); await page.waitForSelector('#gm_hometown', { state: 'attached', timeout: 60000 }); await page.waitForTimeout(1500);
  for (let i = 0; i < 3; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click(); await page.waitForTimeout(400); } }
  await openMetaBoxes(page);
};
const save = async () => { await page.click('.editor-header__settings button:has-text("Save"), .edit-post-header__settings button:has-text("Update"), .editor-header__settings button:has-text("Update")'); await page.waitForTimeout(800); await waitSaved(page); };
// a 3.0.0 seed whose chosen clip the person removed and replaced with their own clip link, plus a real Instagram address
await edit(noah);
await page.click('#gm_clip_clear'); await page.fill('#gm_clip_url', 'https://example.org/own-clip-' + run + '.gif'); await page.fill('#gm_instagram', 'https://www.instagram.com/noah.own' + run + '/');
await save(); out.changed.noahClipRemovedLinkAdded = noah;
// a 3.0.0 seed whose handle the person changed (the README says this keeps it)
await edit(devin); await page.fill('#gm_handle', '@devin.real' + run); await save(); out.changed.devinHandleChanged = devin;
// a 3.0.0 seed the person only added a real Instagram address to
await edit(tyler); await page.fill('#gm_instagram', 'https://www.instagram.com/tyler.own' + run + '/'); await save(); out.changed.tylerInstagramAdded = tyler;
// a 3.0.0 seed opened and saved in the editor without any change
await edit(maya); await page.click('#gm_hometown'); await page.click('#gm_handle'); await save(); out.changed.mayaOpenedSaved = maya;
// a 3.0.0 seed given its own clip, uploaded through the picker
await edit(amara);
await page.locator('#gm_clip_pick').focus(); await page.keyboard.press('Enter'); await page.waitForSelector('.media-modal', { state: 'visible', timeout: 20000 });
await page.locator('.media-modal:visible .media-router button, .media-modal:visible .media-menu-item', { hasText: 'Upload files' }).first().click();
await page.setInputFiles('.media-modal:visible input[type=file]', '/tmp/claude-0/wptest/media/sample-clip.gif');
await page.waitForSelector('.media-modal:visible .attachment.selected.save-ready', { timeout: 180000 }); await page.waitForTimeout(800);
await page.locator('.media-modal:visible .media-button-select').click(); await page.waitForSelector('.media-modal', { state: 'hidden' }); await page.waitForTimeout(600);
await save(); out.changed.amaraOwnClip = amara;
// a 3.0.0 seed whose clip length the person changed
await edit(sam); await page.fill('#gm_clip_len', '0:19'); await save(); out.changed.samLengthChanged = sam;
fs.writeFileSync(`${W}/seedrec-${run}.json`, JSON.stringify(out, null, 1)); console.log(JSON.stringify(out));
await b.close();
