// Admin checks through the UI: Site Editor front page (invalid blocks), Settings > Generation Maine save, Creators list and edit.
//   node admin.mjs <outdir> <label> <baseurl> <wpver: 65|71> [slow]
import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
import fs from 'fs';
const [out, label, base, ver, slow] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const T = slow ? 240000 : 60000;
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const ctx = await b.newContext({ viewport: { width: 1440, height: 1000 } });
ctx.setDefaultTimeout(T); ctx.setDefaultNavigationTimeout(T);
const p = await ctx.newPage();
const errs = [], cons = [];
p.on('pageerror', e => errs.push(e.message.slice(0, 300)));
p.on('console', m => { const t = m.text(); if (m.type() === 'error' || /validation|invalid|deprecat/i.test(t)) cons.push(m.type() + ': ' + t.slice(0, 300)); });
p.on('response', r => { if (r.status() >= 400 && !r.url().includes('favicon')) errs.push(r.status() + ' ' + r.url()); });
const res = { label };
const log = (k, v) => { res[k] = v; console.log(k, JSON.stringify(v)); };

// login
if (slow) {
  await p.goto(base + '/', { waitUntil: 'load' });
  await p.goto(base + '/wp-admin/', { waitUntil: 'load' });
  if (p.url().includes('wp-login.php')) { await p.fill('#user_login', 'admin'); await p.fill('#user_pass', 'password'); await p.click('#wp-submit'); await p.waitForLoadState('load'); }
} else {
  await p.goto(base + '/wp-login.php', { waitUntil: 'load' });
  await p.fill('#user_login', 'admin'); await p.fill('#user_pass', 'adminpass'); await p.click('#wp-submit'); await p.waitForLoadState('load');
}
log('loggedIn', await p.evaluate(() => !!document.getElementById('wpadminbar')));

// Site Editor, front page template
const se = ver === '65'
  ? '/wp-admin/site-editor.php?postType=wp_template&postId=generation-maine%2F%2Ffront-page&canvas=edit'
  : '/wp-admin/site-editor.php?p=%2Fwp_template%2Fgeneration-maine%2F%2Ffront-page&canvas=edit';
const t0 = Date.now();
await p.goto(base + se, { waitUntil: 'load' });
await p.waitForFunction(() => window.wp && wp.data && wp.data.select('core/block-editor') && wp.data.select('core/block-editor').getClientIdsWithDescendants().length > 20, null, { timeout: T * 2 }).catch(e => log('seWaitErr', String(e).slice(0, 200)));
await p.waitForTimeout(slow ? 20000 : 6000);
log('seLoadMs', Date.now() - t0);
log('siteEditor', await p.evaluate(() => {
  const s = wp.data.select('core/block-editor');
  const ids = s.getClientIdsWithDescendants();
  const blocks = ids.map(id => s.getBlock(id)).filter(Boolean);
  const invalid = blocks.filter(bl => bl.isValid === false).map(bl => bl.name);
  const missing = blocks.filter(bl => bl.name === 'core/missing').map(bl => bl.attributes && bl.attributes.originalName);
  const types = {}; blocks.forEach(bl => { types[bl.name] = (types[bl.name] || 0) + 1; });
  const gmTypes = ['generation-maine/creators', 'generation-maine/follow', 'generation-maine/newsletter', 'generation-maine/site-footer', 'generation-maine/posts'].map(n => n + '=' + !!wp.blocks.getBlockType(n));
  return { count: blocks.length, invalid, missing, types, gmTypes };
}));
const canvas = p.frames().find(f => f.name() === 'editor-canvas');
log('canvas', canvas ? await canvas.evaluate(() => ({
  warnings: document.querySelectorAll('.block-editor-warning').length,
  warningText: [...document.querySelectorAll('.block-editor-warning')].map(e => e.textContent.trim().slice(0, 120)),
  ssrErrors: [...document.querySelectorAll('.components-placeholder, .block-editor-warning__message')].map(e => e.textContent.trim().slice(0, 120)).slice(0, 10),
  panels: document.querySelectorAll('.panel').length,
  heroFont: (() => { const h = document.querySelector('.hero h1'); return h ? getComputedStyle(h).fontFamily.split(',')[0] + ' ' + getComputedStyle(h).fontSize : null; })(),
  navFont: (() => { const a = document.querySelector('.top nav a'); return a ? getComputedStyle(a).fontFamily.split(',')[0] : null; })(),
  footer: !!document.querySelector('.site, footer'),
  fontCheck: ['800 40px "Bricolage Grotesque"', '400 16px "DM Sans"', '400 13px Michroma'].map(f => f + '=' + document.fonts.check(f)),
})) : 'no canvas iframe');
await p.screenshot({ path: `${out}/${label}-site-editor.png` });
// scroll canvas to creators and footer for a look
if (canvas) {
  await canvas.evaluate(() => { const e = document.querySelector('.stories, [data-type="generation-maine/creators"]'); if (e) e.scrollIntoView(); });
  await p.waitForTimeout(slow ? 8000 : 2000);
  await p.screenshot({ path: `${out}/${label}-site-editor-creators.png` });
  await canvas.evaluate(() => { const e = document.querySelector('[data-type="generation-maine/site-footer"], footer'); if (e) e.scrollIntoView(); });
  await p.waitForTimeout(slow ? 8000 : 2000);
  await p.screenshot({ path: `${out}/${label}-site-editor-footer.png` });
}

// Settings > Generation Maine
await p.goto(base + '/wp-admin/options-general.php?page=generation_maine', { waitUntil: 'load' });
log('settingsPage', await p.evaluate(() => ({ h1: (document.querySelector('.wrap h1') || {}).textContent, fields: [...document.querySelectorAll('.form-table input')].map(i => i.name + ':' + i.type), sections: [...document.querySelectorAll('.wrap h2')].map(h => h.textContent) })));
const stamp = 'compat' + Date.now().toString().slice(-5);
await p.fill('#gm_instagram_handle', '@' + stamp);
await p.fill('#gm_instagram_url', 'https://www.instagram.com/' + stamp + '/');
await p.fill('#gm_newsletter_url', 'https://' + stamp + '.substack.com/subscribe');
await Promise.all([p.waitForNavigation({ waitUntil: 'load' }), p.click('#submit')]);
log('settingsSaved', await p.evaluate(() => ({ url: location.search, notice: [...document.querySelectorAll('.notice, .updated, .error, #setting-error-settings_updated')].map(n => n.textContent.trim()).join(' | '), handle: document.getElementById('gm_instagram_handle').value, nl: document.getElementById('gm_newsletter_url').value })));
log('stamp', stamp);
await p.screenshot({ path: `${out}/${label}-settings-saved.png`, fullPage: true });

// Creators list
await p.goto(base + '/wp-admin/edit.php?post_type=gm_creator', { waitUntil: 'load' });
log('creatorsList', await p.evaluate(() => ({ h1: (document.querySelector('.wrap h1') || {}).textContent, rows: document.querySelectorAll('#the-list tr').length, titles: [...document.querySelectorAll('#the-list .row-title')].map(a => a.textContent), cols: [...document.querySelectorAll('thead th')].map(t => t.textContent.trim()).filter(Boolean), menu: (document.querySelector('#menu-posts-gm_creator .wp-menu-name') || {}).textContent })));
await p.screenshot({ path: `${out}/${label}-creators-list.png` });
const editHref = await p.getAttribute('#the-list tr:first-child .row-title', 'href');
// Edit screen
await p.goto(editHref.startsWith('http') ? editHref : base + '/wp-admin/' + editHref, { waitUntil: 'load' });
await p.waitForSelector('#gm_creator_details', { timeout: T * 2 }).catch(() => {});
await p.waitForTimeout(slow ? 15000 : 4000);
// dismiss welcome guide if any
const guide = await p.$('.components-modal__frame button[aria-label="Close"], .edit-post-welcome-guide button[aria-label="Close"]');
if (guide) { await guide.click(); await p.waitForTimeout(500); }
log('creatorEdit', await p.evaluate(() => {
  const s = wp.data && wp.data.select('core/block-editor');
  const ids = s ? s.getClientIdsWithDescendants() : [];
  return {
    title: wp.data.select('core/editor').getEditedPostAttribute('title'),
    metaBox: !!document.getElementById('gm_creator_details'),
    fields: [...document.querySelectorAll('#gm_creator_details input')].map(i => i.name + '=' + (i.type === 'checkbox' ? i.checked : i.value)),
    invalid: ids.map(id => s.getBlock(id)).filter(bl => bl && bl.isValid === false).length,
    featured: !!document.querySelector('.editor-post-featured-image img, .editor-post-featured-image__preview img'),
  };
}));
await p.screenshot({ path: `${out}/${label}-creator-edit.png` });
if (!(await p.isVisible('#gm_hometown'))) {
  const drawer = p.locator('button:has-text("Meta Boxes"), .edit-post-meta-boxes-main__presenter button').first();
  log('metaDrawer', await drawer.count());
  const bb = await drawer.boundingBox(); log('drawerBox', bb); await p.mouse.click(bb.x + 40, bb.y + bb.height / 2); await p.waitForTimeout(1500); if (!(await p.isVisible('#gm_hometown'))) { await drawer.focus(); await p.keyboard.press('Enter'); await p.waitForTimeout(1500); log('drawerViaKeyboard', true); }
}
// where is the Order field in this version?
log('orderField', await p.evaluate(() => { const l = [...document.querySelectorAll('label')].find(x => /^Order$/i.test(x.textContent.trim())); return l ? 'visible label' : 'not visible in sidebar'; }));
const parentBtn = await p.$('.editor-post-parent__panel-toggle, button:has-text("None")');
if (parentBtn) { await parentBtn.click().catch(() => {}); await p.waitForTimeout(800); log('orderAfterParentClick', await p.evaluate(() => [...document.querySelectorAll('.components-popover label, .components-dropdown__content label')].map(l => l.textContent.trim()))); await p.screenshot({ path: `${out}/${label}-creator-order.png` }); await p.keyboard.press('Escape'); await p.waitForTimeout(300); }
await p.evaluate(() => document.getElementById('gm_creator_details').scrollIntoView());
await p.fill('#gm_hometown', 'Compatville');
await p.screenshot({ path: `${out}/${label}-creator-edit-box.png` });
const saveBtn = await p.$('.editor-post-publish-button, .editor-post-publish-button__button, button.editor-post-save-draft');
await saveBtn.click();
await p.waitForFunction(() => { const e = wp.data.select('core/editor'); const m = wp.data.select('core/edit-post'); return !e.isSavingPost() && !(m && m.isSavingMetaBoxes && m.isSavingMetaBoxes()); }, null, { timeout: T * 2 });
await p.waitForTimeout(slow ? 10000 : 2500);
log('creatorSaved', await p.evaluate(() => ({ notices: wp.data.select('core/notices').getNotices().map(n => n.content), url: location.search })));
await p.reload({ waitUntil: 'load' }); await p.waitForSelector('#gm_hometown', { timeout: T * 2 }); await p.waitForTimeout(slow ? 8000 : 1500);
log('creatorAfterReload', await p.evaluate(() => document.getElementById('gm_hometown').value));
log('postId', await p.evaluate(() => wp.data.select('core/editor').getCurrentPostId()));

// 404
const r404 = await p.goto(base + '/no-such-page-' + stamp + '/', { waitUntil: 'load' });
log('404', { status: r404.status(), h1: await p.evaluate(() => (document.querySelector('h1') || {}).textContent), home: await p.evaluate(() => [...document.querySelectorAll('main a')].map(a => a.getAttribute('href'))) });
await p.screenshot({ path: `${out}/${label}-404.png` });

log('pageErrors', errs);
log('console', cons.slice(0, 30));
fs.writeFileSync(`${out}/${label}-admin.json`, JSON.stringify(res, null, 1));
await b.close();
