// S01/SET-N02: per field, save each value through Settings > Generation Maine; read notice, field, stored option and the front.
// usage: node settings-matrix.mjs <port> <tag>
import { launch, base, login, wp, INST, SHOTS, watch } from './lib.mjs';
const [port, tag] = process.argv.slice(2);
const B = base(port), inst = INST[port];
const cases = [
  ['gm_contact_url', 'https://mainepolicy.org/contact-a/'],
  ['gm_contact_url', 'mailto:info@mainepolicy.org'],
  ['gm_contact_url', 'MailTo:Info@MainePolicy.org?subject=Hi&body=x'],
  ['gm_contact_url', 'mailto:info@mainepolicy'],
  ['gm_contact_url', 'mailto:info@mainepolicy.org?subject=<b>x</b>"onclick=1'],
  ['gm_contact_url', 'http://mainepolicy.org/contact-b/'],
  ['gm_contact_url', 'ftp://mainepolicy.org/'],
  ['gm_instagram_url', 'mailto:info@mainepolicy.org'],
  ['gm_instagram_url', 'http://www.instagram.com/generationmaine/'],
  ['gm_instagram_url', 'javascript:alert(1)'],
  ['gm_tiktok_url', 'mailto:info@mainepolicy.org'],
  ['gm_tiktok_url', 'HTTP://www.tiktok.com/@generationmaine'],
  ['gm_tiktok_url', 'data:text/html,x'],
  ['gm_youtube_url', 'mailto:info@mainepolicy.org'],
  ['gm_youtube_url', 'http://www.youtube.com/@generationmaine'],
  ['gm_youtube_url', 'ftp://www.youtube.com/'],
  ['gm_newsletter_url', 'mailto:info@mainepolicy.org'],
  ['gm_newsletter_url', 'http://generationmaine.substack.com/subscribe'],
  ['gm_newsletter_url', 'javascript:alert(1)'],
];
const b = await launch();
const ctx = await b.newContext({ viewport: { width: 1280, height: 1400 } });
await login(ctx, B);
const p = await ctx.newPage(); const errs = []; watch(p, errs);
const vis = await b.newContext({ viewport: { width: 1280, height: 900 } });
const front = async () => { const q = await vis.newPage(); await q.goto(B + '/?n=' + Date.now()); const r = await q.evaluate(() => ({ contact: [...document.querySelectorAll('a')].filter(a => /^contact$/i.test(a.textContent.trim())).map(a => a.getAttribute('href')), follow: [...document.querySelectorAll('.follow .row')].map(r => ({ tag: r.tagName, href: r.getAttribute('href'), h: (r.querySelector('.h') || {}).textContent })), form: (document.querySelector('form.nl, form[action*=substack], #newsletter form') || {}).action || null, probes: document.querySelectorAll('b,[onclick]').length })); await q.close(); return r; };
const out = [];
for (const [key, val] of cases) {
  await p.goto(B + '/wp-admin/options-general.php?page=generation_maine');
  const before = await p.inputValue('#' + key);
  await p.fill('#' + key, val);
  await Promise.all([p.waitForNavigation(), p.click('#submit')]);
  const notices = (await p.locator('.notice, .error, .updated').allInnerTexts()).map(t => t.replace(/\s+/g, ' ').replace(' Dismiss this notice.', '').trim()).filter(t => t && !/is available/.test(t));
  const after = await p.inputValue('#' + key);
  const stored = wp(inst, `option get ${key}`);
  const f = await front();
  out.push({ key, typed: val, before, notices, fieldAfter: after, stored, front: f });
}
console.log(JSON.stringify({ port, out, errors: errs.filter(e => !/CERT/.test(e)) }, null, 1));
await b.close();
