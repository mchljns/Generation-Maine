// REST /wp/v2/gm_creator exposure, and the meta-box form's new post_author field under forgery (Author, Contributor)
import { launch, base, login, wp, INST } from './lib.mjs';
const [port, ownByAuthor, ownByContrib, otherId] = process.argv.slice(2); const B = base(port), inst = INST[port];
const b = await launch(); const out = {};
const anon = await (await b.newContext()).newPage(); await anon.goto(B + '/');
const draft = wp(inst, 'post list --post_type=gm_creator --post_status=draft,pending --field=ID').split('\n').filter(x => /^\d+$/.test(x))[0];
out.anon = await anon.evaluate(async ({ B, draft }) => { const j = async (u, o) => { const r = await fetch(B + u, o); let t = await r.text(); try { t = JSON.parse(t); } catch (e) {} return { s: r.status, t }; };
  const list = await j('/wp-json/wp/v2/gm_creator?per_page=100');
  const one = Array.isArray(list.t) ? list.t[0] : null;
  return { listStatus: list.s, count: Array.isArray(list.t) ? list.t.length : list.t, keys: one ? Object.keys(one).join(',') : null, metaKeys: one && one.meta ? Object.keys(one.meta).join(',') : null, hasAuthor: one ? 'author' in one : null,
    draftById: (await j('/wp-json/wp/v2/gm_creator/' + draft)).s, statusDraft: (await j('/wp-json/wp/v2/gm_creator?status=draft')).s, ctxEdit: (await j('/wp-json/wp/v2/gm_creator?context=edit')).s,
    post: (await j('/wp-json/wp/v2/gm_creator', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{"title":"x"}' })).s, settings: (await j('/wp-json/wp/v2/settings')).s }; }, { B, draft });
for (const [u, pw, own] of [['author1', 'authorpass', ownByAuthor], ['contrib1', 'contribpass', ownByContrib]]) {
  const ctx = await b.newContext(); await login(ctx, B, u, pw); const p = await ctx.newPage();
  const r = await p.goto(B + '/wp-admin/post.php?post=' + own + '&action=edit'); await p.waitForTimeout(4000);
  const nonce = await p.evaluate(async (B) => (await fetch(B + '/wp-admin/admin-ajax.php?action=rest-nonce')).text(), B);
  const mbUrl = await p.evaluate(() => window._wpMetaBoxUrl || (wp.data.select('core/edit-post').getMetaBoxesPerLocation ? null : null));
  const form = await p.evaluate(() => { const f = document.querySelector('form.metabox-base-form'); if (!f) return null; const d = new FormData(f); const o = {}; for (const [k, v] of d.entries()) o[k] = v; return o; });
  const before = wp(inst, `post get ${own} --field=post_author`).split('\n').pop();
  // forged meta-box POST: own creator, post_author set to the admin (1)
  const forged = form ? await p.evaluate(async ({ B, form, own }) => { const fd = new URLSearchParams({ ...form, post_author: '1', action: 'editpost', post_ID: own, post_type: 'gm_creator' }); const x = await fetch(window._wpMetaBoxUrl, { method: 'POST', body: fd, credentials: 'include' }); const t = await x.text(); const m = t.match(/<div class="wp-die-message">([\s\S]*?)<\/div>/) || t.match(/<p>([\s\S]*?)<\/p>/); return { s: x.status, msg: m ? m[1].replace(/<[^>]+>/g, '').trim().slice(0, 140) : t.slice(0, 80) }; }, { B, form, own }) : 'no form';
  const control = form ? await p.evaluate(async ({ B, form, own }) => { const fd = new URLSearchParams({ ...form, action: 'editpost', post_ID: own, post_type: 'gm_creator', gm_hometown: 'Control town' }); const x = await fetch(window._wpMetaBoxUrl, { method: 'POST', body: fd, credentials: 'include' }); return x.status; }, { B, form, own }) : null;
  const after = wp(inst, `post get ${own} --field=post_author`).split('\n').pop();
  const restOther = await p.evaluate(async ({ B, nonce, otherId }) => { const x = await fetch(B + '/wp-json/wp/v2/gm_creator/' + otherId, { method: 'POST', headers: { 'X-WP-Nonce': nonce, 'Content-Type': 'application/json' }, body: JSON.stringify({ menu_order: 99, meta: { gm_hometown: 'hacked' } }) }); return x.status; }, { B, nonce, otherId });
  const restOtherEdit = await p.evaluate(async ({ B, nonce, otherId }) => (await fetch(B + '/wp-json/wp/v2/gm_creator/' + otherId + '?context=edit', { headers: { 'X-WP-Nonce': nonce } })).status, { B, nonce, otherId });
  const restOwnOrder = await p.evaluate(async ({ B, nonce, own }) => { const x = await fetch(B + '/wp-json/wp/v2/gm_creator/' + own, { method: 'POST', headers: { 'X-WP-Nonce': nonce, 'Content-Type': 'application/json' }, body: JSON.stringify({ menu_order: 3 }) }); return x.status; }, { B, nonce, own });
  out[u] = { mbUrl, editStatus: r.status(), formFields: form ? Object.keys(form).filter(k => /author|nonce|gm_order/.test(k)).map(k => k + '=' + form[k]) : null, authorBefore: before, forged, authorAfter: after, controlOwnAuthor: control, controlHometown: wp(inst, `post meta get ${own} gm_hometown`).split('\n').pop(), restOther, restOtherEdit, restOwnOrder, ownOrderNow: wp(inst, `post get ${own} --field=menu_order`).split('\n').pop(), otherHometown: wp(inst, `post meta get ${otherId} gm_hometown`).split('\n').pop() };
  await ctx.close();
}
console.log(JSON.stringify(out, null, 1)); await b.close();
