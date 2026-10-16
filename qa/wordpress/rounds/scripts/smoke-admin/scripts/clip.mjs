// Clip box tests (X12, CRE-N04, CRE-N06): one session as one user. Steps:
//   as:USER  new:TITLE  open:ID  pick:FILE (upload through the picker, opened with the keyboard)  pickname:FILENAME (choose from library)
//   remove  link:URL|$UP  len:TEXT  update  reload  box  front:NAME  upload:FILE (Media > Add New, sets $UP)  delmedia:ID|$LASTPICK  shot:NAME
import { launch, base, login, wp, INST, SHOTS, M, watch, metaDrawer, publishOrUpdate, dismissGuide } from './lib.mjs';
const [port, tag, ...steps] = process.argv.slice(2); const B = base(port), inst = INST[port];
const MEDIA = '/tmp/claude-0/wptest/work/smoke-admin/media/';
const users = { admin: ['admin', 'adminpass'], editor1: ['editor1', 'editorpass'], author1: ['author1', 'authorpass'], contrib1: ['contrib1', 'contribpass'] };
const b = await launch(); let ctx, p; const errs = []; let cur = 0, UP = '', LASTPICK = '';
const log = (...a) => console.log(...a);
async function openEd(url) { await p.goto(url); await p.waitForSelector('#gm_creator_details', { state: 'attached', timeout: 60000 }); await p.waitForTimeout(3000); const to = p.locator('.components-modal__frame').getByText('Take over', { exact: true }); if (await to.count()) { await to.first().click(); await p.waitForTimeout(2000); } await dismissGuide(p); await metaDrawer(p, true); }
async function box() {
  const s = await p.evaluate(() => { const g = i => document.getElementById(i); const vis = e => !!e && !e.hidden && e.getBoundingClientRect().height > 0; return { clipId: g('gm_clip_id').value, name: g('gm_clip_name').textContent, removeVisible: vis(g('gm_clip_clear')), pickButton: !!g('gm_clip_pick'), noUploadNote: g('gm_clip_noupload') ? g('gm_clip_noupload').textContent : null, warning: vis(g('gm_clip_big')) ? g('gm_clip_big').textContent.trim() : null, link: g('gm_clip_url').value, help: [...document.querySelectorAll('#gm_creator_details .description')].map(d => d.textContent).find(t => /vertical video/.test(t)) }; });
  return s;
}
for (const s of steps) {
  const [cmd, ...rest] = s.split(':'); let arg = rest.join(':'); arg = arg.replace('$UP', UP).replace('$LASTPICK', LASTPICK);
  if (cmd === 'as') { if (ctx) await ctx.close(); ctx = await b.newContext({ viewport: { width: 1440, height: 1000 } }); await login(ctx, B, ...users[arg]); p = await ctx.newPage(); watch(p, errs); log('as', arg); continue; }
  if (cmd === 'new') {
    await openEd(B + '/wp-admin/post-new.php?post_type=gm_creator');
    await metaDrawer(p, false); const c = p.frameLocator('iframe[name="editor-canvas"]'); const hasFrame = await p.locator('iframe[name="editor-canvas"]').count();
    await (hasFrame ? c : p).locator('h1.wp-block-post-title, .editor-post-title__input').first().click(); await p.keyboard.type(arg); await p.keyboard.press('Enter'); await p.keyboard.type('A story for the clip test.');
    await metaDrawer(p, true); await p.locator('#gm_hometown').click(); await p.keyboard.type('Bath');
  }
  else if (cmd === 'open') { cur = +arg; await openEd(B + '/wp-admin/post.php?post=' + cur + '&action=edit'); }
  else if (cmd === 'reload') { await openEd(B + '/wp-admin/post.php?post=' + cur + '&action=edit'); }
  else if (cmd === 'pick' || cmd === 'pickname') {
    await p.locator('#gm_clip_pick').focus(); await p.keyboard.press('Enter');
    await p.waitForSelector('.media-modal', { state: 'visible', timeout: 10000 });
    if (cmd === 'pick') {
      await p.locator('.media-modal:visible .media-router button, .media-modal:visible .media-menu-item', { hasText: 'Upload files' }).first().click();
      await p.setInputFiles('.media-modal:visible input[type=file]', MEDIA + arg);
      await p.waitForSelector('.media-modal:visible .attachment.selected.save-ready', { timeout: 180000 });
    } else {
      await p.locator('.media-modal:visible .media-router button, .media-modal:visible .media-menu-item', { hasText: 'Media Library' }).first().click(); await p.waitForTimeout(2000);
      await p.locator(`.media-modal:visible .attachment[aria-label="${arg}"]`).first().click();
    }
    await p.waitForTimeout(1000);
    LASTPICK = await p.locator('.media-modal:visible .attachment.selected').first().getAttribute('data-id');
    await p.locator('.media-modal:visible .media-button-select').click(); await p.waitForSelector('.media-modal', { state: 'hidden' }); await p.waitForTimeout(600);
  }
  else if (cmd === 'remove') { await p.locator('#gm_clip_clear').focus(); await p.keyboard.press('Enter'); await p.waitForTimeout(300); }
  else if (cmd === 'link') { await p.locator('#gm_clip_url').click(); await p.keyboard.press('Control+A'); if (arg) await p.keyboard.type(arg); else await p.keyboard.press('Delete'); }
  else if (cmd === 'len') { await p.locator('#gm_clip_len').click(); await p.keyboard.press('Control+A'); await p.keyboard.type(arg); }
  else if (cmd === 'savekbd') { await p.locator('#gm_clip_len').focus(); await p.keyboard.press('Control+S'); await p.waitForTimeout(5000); log('  ctrl+s', JSON.stringify(await p.locator('.components-snackbar').allInnerTexts())); }
  else if (cmd === 'savepending') { await p.getByRole('button', { name: 'Save as pending' }).first().click(); await p.waitForTimeout(5000); log('  save as pending', JSON.stringify(await p.locator('.components-snackbar').allInnerTexts())); }
  else if (cmd === 'update') { log('  save', JSON.stringify(await publishOrUpdate(p))); if (!cur) cur = +(await p.evaluate(() => wp.data.select('core/editor').getCurrentPostId())); }
  else if (cmd === 'upload') {
    const q = await ctx.newPage(); await q.goto(B + '/wp-admin/media-new.php'); await q.waitForSelector('input[type=file]', { state: 'attached' });
    await q.setInputFiles('input[type=file]', MEDIA + arg);
    await q.waitForFunction(() => { const it = document.querySelectorAll('#media-items .media-item'); const l = it[it.length - 1]; return l && (l.querySelector('.copy-attachment-url') || /error|failed/i.test(l.textContent)); }, null, { timeout: 180000 });
    UP = await q.locator('#media-items .media-item').last().locator('.copy-attachment-url').getAttribute('data-clipboard-text').catch(() => '');
    log('  uploaded', UP); await q.close(); continue;
  }
  else if (cmd === 'delmedia') {
    const q = await ctx.newPage(); q.on('dialog', d => d.accept()); await q.goto(B + '/wp-admin/upload.php?mode=list');
    const row = q.locator('#post-' + arg); await row.hover(); await row.locator('.delete a, a.submitdelete').first().click(); await q.waitForTimeout(2500);
    log('  deleted media', arg, (await q.locator('#message').innerText().catch(() => '')).replace(/\s+/g, ' '), '| exists now:', wp(inst, `post exists ${arg}`)); await q.close(); continue;
  }
  else if (cmd === 'front') {
    const r = await fetch(B + '/?n=' + Date.now()); const h = await r.text();
    const i = h.indexOf('data-name="' + arg + '"'); const idx = [...h.matchAll(/data-name="([^"]+)"/g)].findIndex(m => m[1] === arg);
    const stage = h.split('id="stage"')[1] || h; const clips = [...stage.matchAll(/<(img|video|div) class="([^"]*)"[^>]*data-i="(\d+)"[^>]*>/g)].filter(m => +m[3] === idx).map(m => m[0].replace(/\s+/g, ' ').slice(0, 300));
    log(`  front ${arg} (index ${idx}):`, JSON.stringify(clips));
    continue;
  }
  else if (cmd === 'shot') { await p.locator('#gm_creator_details').screenshot({ path: `${SHOTS}/clip-${tag}-${arg}.png` }); continue; }
  else if (cmd === 'box') { }
  const st = await box();
  log(`after ${s}: ${JSON.stringify(st)} | stored clip_id=${cur ? wp(inst, `post meta get ${cur} gm_clip_id`).split('\n').pop() : '-'} clip_url=${cur ? wp(inst, `post meta get ${cur} gm_clip_url`).split('\n').pop() : '-'}`);
}
log('errors', JSON.stringify(errs.filter(e => !/CERT|favicon|^dialog|mediaelement/.test(e))));
await b.close();
