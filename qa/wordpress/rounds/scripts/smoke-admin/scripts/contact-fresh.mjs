// SET-N01 / SEC-N02 / S01: on a site where Contact was never saved, type a value into Contact link and save through the UI.
// usage: node contact-fresh.mjs <port> <tag> <value> [<value> ...]   (each value is saved in turn, same session)
import { launch, base, login, wp, INST, SHOTS, watch } from './lib.mjs';
const [port, tag, ...values] = process.argv.slice(2);
const B = base(port), inst = INST[port];
const b = await launch();
const out = { port, inst, steps: [] };
const vis = await b.newContext({ viewport: { width: 1280, height: 900 } });
const footer = async () => { const p = await vis.newPage(); await p.goto(B + '/?nocache=' + Date.now()); const r = await p.evaluate(() => [...document.querySelectorAll('footer a, .site-footer a, .ffine a')].map(a => ({ t: a.textContent.trim(), h: a.getAttribute('href') })).filter(x => /contact/i.test(x.t))); await p.close(); return r; };
out.footerBefore = await footer();
const ctx = await b.newContext({ viewport: { width: 1280, height: 1100 } });
await login(ctx, B);
const p = await ctx.newPage(); const errs = []; watch(p, errs);
await p.goto(B + '/wp-admin/options-general.php?page=generation_maine');
out.fieldInitial = await p.inputValue('#gm_contact_url');
out.optionRowInitial = wp(inst, 'option get gm_contact_url');
for (const v of values) {
  const s = { typed: v };
  await p.goto(B + '/wp-admin/options-general.php?page=generation_maine');
  s.fieldBefore = await p.inputValue('#gm_contact_url');
  await p.fill('#gm_contact_url', v);
  await Promise.all([p.waitForNavigation(), p.click('#submit')]);
  s.notices = (await p.locator('.notice, .error, .updated').allInnerTexts()).map(t => t.replace(/\s+/g, ' ').trim()).filter(Boolean);
  s.fieldAfter = await p.inputValue('#gm_contact_url');
  s.option = wp(inst, 'option get gm_contact_url');
  s.footer = await footer();
  await p.screenshot({ path: `${SHOTS}/${tag}-${values.indexOf(v)}.png` });
  out.steps.push(s);
}
out.errors = errs;
console.log(JSON.stringify(out, null, 1));
await b.close();
