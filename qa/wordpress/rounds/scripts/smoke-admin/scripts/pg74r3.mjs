// Round 3 changes on PHP 7.4 (pg74): handle cleaning and handles from addresses in Settings, a creator whose title is its
// handle with 4x4 and --, Ctrl+S in Creator details, the 10 MB box, then the front page as a visitor.
//   node pg74r3.mjs <outdir>
import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
import fs from 'fs';
const [out] = process.argv.slice(2); const base = 'http://127.0.0.1:9474'; const T = 300000;
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const ctx = await b.newContext({ viewport: { width: 1440, height: 1000 } }); ctx.setDefaultTimeout(T); ctx.setDefaultNavigationTimeout(T);
const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message.slice(0, 200)));
const res = {}; const log = (k, v) => { res[k] = v; console.log(k, JSON.stringify(v)); };
await p.goto(base + '/', { waitUntil: 'load' }); await p.goto(base + '/wp-admin/', { waitUntil: 'load' });
if (p.url().includes('wp-login.php')) { await p.fill('#user_login', 'admin'); await p.fill('#user_pass', 'password'); await p.click('#wp-submit'); await p.waitForLoadState('load'); }
// settings
await p.goto(base + '/wp-admin/options-general.php?page=generation_maine', { waitUntil: 'load' });
await p.fill('#gm_instagram_handle', ' @ maine.4x4'); await p.fill('#gm_instagram_url', 'https://www.instagram.com/maine.4x4/');
await p.fill('#gm_tiktok_handle', '@'); await p.fill('#gm_tiktok_url', 'https://www.tiktok.com/@generation--maine/video/7312345678901234567');
await p.fill('#gm_youtube_handle', ''); await p.fill('#gm_youtube_url', 'https://www.instagram.com/s/aGlnaGxpZ2h0OjE3?story_media_id=1&igsh=x');
await Promise.all([p.waitForNavigation({ waitUntil: 'load' }), p.click('#submit')]);
log('settings', await p.evaluate(() => ['gm_instagram_handle', 'gm_tiktok_handle', 'gm_youtube_handle', 'gm_youtube_url'].map(i => document.getElementById(i).value)));
// a creator titled with its handle
await p.goto(base + '/wp-admin/post-new.php?post_type=gm_creator', { waitUntil: 'load' });
await p.waitForSelector('#gm_creator_details', { state: 'attached', timeout: T }); await p.waitForTimeout(15000);
const g = await p.$('.components-modal__frame button[aria-label="Close"]'); if (g) { await g.click(); await p.waitForTimeout(800); }
const fr = (await p.$('iframe[name="editor-canvas"]')) ? p.frameLocator('iframe[name="editor-canvas"]') : p;
await fr.locator('h1.wp-block-post-title, .editor-post-title__input').first().click(); await p.keyboard.type('@4x4.maine'); await p.keyboard.press('Enter'); await p.keyboard.type('A story with "quotes" and an apostrophe\'s turn.');
if (!(await p.isVisible('#gm_handle'))) { const mb = p.locator('button:has-text("Meta Boxes")'); if (await mb.count()) { await mb.first().click({ position: { x: 30, y: 12 } }); await p.waitForTimeout(1500); } }
await p.fill('#gm_handle', '@@ 4x4.maine'); await p.fill('#gm_hometown', 'Old Town'); await p.fill('#gm_clip_url', base + '/wp-content/uploads/nope.gif?v=2');
await p.click('#gm_order', { clickCount: 3 }); await p.keyboard.type('-1');
await p.click('.editor-header__settings button:has-text("Publish"), .edit-post-header__settings button:has-text("Publish")'); await p.waitForTimeout(3000);
const conf = p.locator('.editor-post-publish-panel__header-publish-button button'); if (await conf.count()) await conf.first().click();
await p.waitForFunction(() => { const e = wp.data.select('core/editor'); const m = wp.data.select('core/edit-post'); return e.isCurrentPostPublished() && !e.isSavingPost() && !(m && m.isSavingMetaBoxes && m.isSavingMetaBoxes()); }, null, { timeout: T });
await p.waitForTimeout(8000);
const id = await p.evaluate(() => wp.data.select('core/editor').getCurrentPostId()); log('creatorId', id);
// Ctrl+S after a Creator details change only
await p.fill('#gm_hometown', 'Old Town Ctrl'); await p.waitForTimeout(500);
log('dirtyBeforeCtrlS', await p.evaluate(() => wp.data.select('core/editor').isEditedPostDirty()));
await p.locator('#gm_hometown').focus(); await p.keyboard.press('Control+s'); await p.waitForTimeout(4000);
await p.waitForFunction(() => { const e = wp.data.select('core/editor'); const m = wp.data.select('core/edit-post'); return !e.isSavingPost() && !(m && m.isSavingMetaBoxes && m.isSavingMetaBoxes()); }, null, { timeout: T });
await p.waitForTimeout(8000);
await p.reload({ waitUntil: 'load' }); await p.waitForSelector('#gm_hometown', { state: 'attached', timeout: T }); await p.waitForTimeout(8000);
log('afterReload', await p.evaluate(() => ({ hometown: document.getElementById('gm_hometown').value, handle: document.getElementById('gm_handle').value, link: document.getElementById('gm_clip_url').value, big: document.getElementById('gm_clip_big').hidden, dataLink: document.getElementById('gm_clip_big').getAttribute('data-link') })));
// front page as a visitor
const v = await (await b.newContext({ viewport: { width: 1440, height: 900 } })).newPage(); v.setDefaultTimeout(T); v.setDefaultNavigationTimeout(T);
const r = await v.goto(base + '/?n=' + Date.now(), { waitUntil: 'load' }); await v.waitForTimeout(3000);
log('front', { php: r.headers()['x-test-php'], build: await v.evaluate(() => (document.body.innerText.match(/Build \w+/) || [''])[0]), who: await v.evaluate(() => [...document.querySelectorAll('.stage .who, #stage .who')].slice(0, 2).map(e => e.innerHTML.replace(/<svg[\s\S]*?<\/svg>|<img[^>]*>/g, ''))), follow: await v.evaluate(() => [...document.querySelectorAll('.follow .row .h')].map(e => e.innerHTML)), h2: await v.evaluate(() => (document.querySelector('article.panel h2') || {}).innerHTML), sw: await v.evaluate(() => document.documentElement.scrollWidth) });
await v.screenshot({ path: `${out}/pg74r3-front-1440.png` });
log('errors', errs);
fs.writeFileSync(`${out}/pg74r3.json`, JSON.stringify(res, null, 1));
await b.close();
