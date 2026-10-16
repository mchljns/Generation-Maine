// SEC-N01: creators keep their author when another account saves them (Author, Contributor, Editor, Admin), block editor UI.
// usage: node author.mjs <port> <tag>
import { launch, base, login, wp, INST, SHOTS, watch, metaDrawer, publishOrUpdate, dismissGuide } from './lib.mjs';
const [port, tag] = process.argv.slice(2); const B = base(port), inst = INST[port];
const users = { admin: ['admin', 'adminpass'], editor1: ['editor1', 'editorpass'], author1: ['author1', 'authorpass'], author2: ['author2', 'authorpass'], contrib1: ['contrib1', 'contribpass'] };
const b = await launch(); const ctxs = {}; const errs = [];
async function as(u) { if (!ctxs[u]) { ctxs[u] = await b.newContext({ viewport: { width: 1440, height: 1000 } }); await login(ctxs[u], B, ...users[u]); } const p = await ctxs[u].newPage(); watch(p, errs); return p; }
const author = id => wp(inst, `post get ${id} --field=post_author`).split('\n').filter(l => /^\d+$/.test(l.trim())).join('');
const status = id => wp(inst, `post get ${id} --field=post_status`).split('\n').pop();
const meta = (id, k) => wp(inst, `post meta get ${id} ${k}`).split('\n').pop();
async function create(u, title, town, submit) {
  const p = await as(u);
  await p.goto(B + '/wp-admin/post-new.php?post_type=gm_creator'); await p.waitForSelector('#gm_creator_details', { state: 'attached', timeout: 60000 }); await p.waitForTimeout(3000); await dismissGuide(p);
  const c = p.frameLocator('iframe[name="editor-canvas"]');
  const hasFrame = await p.locator('iframe[name="editor-canvas"]').count();
  await (hasFrame ? c : p).locator('h1.wp-block-post-title, .editor-post-title__input').first().click(); await p.keyboard.type(title);
  await metaDrawer(p, true); await p.locator('#gm_hometown').click(); await p.keyboard.type(town);
  await p.locator('#gm_handle').click(); await p.keyboard.type('@' + title.toLowerCase().replace(/\W/g, ''));
  const notes = await publishOrUpdate(p);
  const id = +(new URL(p.url())).searchParams.get('post') || +(await p.evaluate(() => wp.data.select('core/editor').getCurrentPostId()));
  await p.close();
  return { id, notes };
}
async function edit(u, id, town, publish) {
  const p = await as(u);
  const r = await p.goto(B + '/wp-admin/post.php?post=' + id + '&action=edit');
  if (r.status() >= 400) { const t = (await p.locator('body').innerText()).slice(0, 80); await p.close(); return { status: r.status(), text: t }; }
  await p.waitForSelector('#gm_creator_details', { state: 'attached', timeout: 60000 }); await p.waitForTimeout(3000);
  let took = false; const to = p.locator('.components-modal__frame').getByText('Take over', { exact: true }); if (await to.count()) { await to.first().click(); took = true; await p.waitForTimeout(2500); }
  await dismissGuide(p);
  await metaDrawer(p, true); await p.locator('#gm_hometown').click(); await p.keyboard.press('Control+A'); await p.keyboard.type(town);
  let notes;
  if (publish) { await p.getByRole('button', { name: 'Publish', exact: true }).first().click(); await p.waitForTimeout(1200); const pp = p.locator('.editor-post-publish-panel__header-publish-button button'); if (await pp.count()) await pp.first().click(); await p.waitForTimeout(5000); notes = await p.locator('.components-snackbar').allInnerTexts(); }
  else notes = await publishOrUpdate(p);
  await p.close();
  return { status: r.status(), notes, tookOverLock: took };
}
const out = [];
const L = (step, id, extra) => { const o = { step, id, post_author: author(id), status: status(id), hometown: meta(id, 'gm_hometown'), ...extra }; out.push(o); console.log(JSON.stringify(o)); };
const a = await create('author1', 'Ada Author ' + tag, 'Bath'); L('author1 creates and publishes', a.id, { notes: a.notes });
L('admin edits hometown and updates', a.id, await edit('admin', a.id, 'Bath Admin'));
L('author1 opens own creator again and updates', a.id, await edit('author1', a.id, 'Bath Author'));
L('editor1 edits and updates', a.id, await edit('editor1', a.id, 'Bath Editor'));
L('author2 opens author1 creator', a.id, await edit('author2', a.id, 'Bath Author2'));
L('author1 opens own creator after the editor', a.id, await edit('author1', a.id, 'Bath Author Again'));
const c = await create('contrib1', 'Cora Contrib ' + tag, 'Belfast'); L('contrib1 creates and submits for review', c.id, { notes: c.notes });
L('admin publishes the pending creator', c.id, await edit('admin', c.id, 'Belfast Admin', true));
L('editor1 edits the published contributor creator', c.id, await edit('editor1', c.id, 'Belfast Editor'));
const c2 = await create('contrib1', 'Cole Contrib ' + tag, 'Lewiston'); L('contrib1 submits a second one', c2.id, { notes: c2.notes });
L('editor1 publishes the pending creator', c2.id, await edit('editor1', c2.id, 'Lewiston Editor', true));
const e = await create('editor1', 'Ed Editor ' + tag, 'Bangor'); L('editor1 creates and publishes', e.id, { notes: e.notes });
L('admin edits editor1 creator', e.id, await edit('admin', e.id, 'Bangor Admin'));
L('author1 opens editor1 creator', e.id, await edit('author1', e.id, 'Bangor Author'));
L('seeded creator (author 0) saved by admin', 8, await edit('admin', 8, 'Presque Isle'));
console.log('errors', JSON.stringify(errs.filter(x => !/CERT|favicon|^dialog/.test(x))));
await b.close();
