// REST /wp/v2/settings: POST gm_ values as admin (cookie + nonce), print response and stored option; anonymous checks too
// usage: node rest-settings.mjs <port> <key> <value> [<key> <value> ...]
import { launch, base, login, wp, INST } from './lib.mjs';
const [port, ...kv] = process.argv.slice(2);
const B = base(port), inst = INST[port];
const b = await launch();
const ctx = await b.newContext();
await login(ctx, B);
const p = await ctx.newPage();
await p.goto(B + '/wp-admin/');
const nonce = await p.evaluate(async (B) => (await fetch(B + '/wp-admin/admin-ajax.php?action=rest-nonce')).text(), B);
const res = [];
for (let i = 0; i < kv.length; i += 2) {
  const key = kv[i], val = kv[i + 1];
  const before = wp(inst, `option get ${key}`);
  const r = await p.evaluate(async ({ B, nonce, key, val }) => { const x = await fetch(B + '/wp-json/wp/v2/settings', { method: 'POST', headers: { 'X-WP-Nonce': nonce, 'Content-Type': 'application/json' }, body: JSON.stringify({ [key]: val }) }); const j = await x.json(); return { status: x.status, value: j[key], code: j.code }; }, { B, nonce, key, val });
  res.push({ key, sent: val, before, status: r.status, returned: r.value, code: r.code, stored: wp(inst, `option get ${key}`) });
}
const anon = await b.newContext(); const ap = await anon.newPage();
const ag = await ap.evaluate(async (B) => { const x = await fetch(B + '/wp-json/wp/v2/settings'); return x.status; }, B).catch(async () => { await ap.goto(B + '/'); return ap.evaluate(async (B) => (await fetch(B + '/wp-json/wp/v2/settings')).status, B); });
console.log(JSON.stringify({ port, res, anonGet: ag }, null, 1));
await b.close();
