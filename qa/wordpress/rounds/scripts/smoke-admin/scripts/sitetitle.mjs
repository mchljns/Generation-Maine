// SET-N05 / SEC-N03: Site Title through Settings > General, then read the front head as a visitor (raw HTML and parsed DOM)
import { launch, base, login, SHOTS } from './lib.mjs';
const [port, title, tag] = process.argv.slice(2);
const B = base(port);
const b = await launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } }); await login(ctx, B);
const p = await ctx.newPage();
if (title !== '-') {
  await p.goto(B + '/wp-admin/options-general.php');
  await p.fill('#blogname', title);
  await Promise.all([p.waitForNavigation(), p.click('#submit')]);
}
const vis = await b.newContext(); const q = await vis.newPage();
const resp = await q.goto(B + '/?n=' + Date.now()); const raw = await resp.text();
const head = raw.split('</head>')[0];
const r = await q.evaluate(() => {
  const m = s => [...document.querySelectorAll(s)].map(e => e.getAttribute('content'));
  const ld = [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => { try { return JSON.parse(s.textContent); } catch (e) { return 'INVALID ' + e.message; } });
  return { docTitle: document.title, titleEls: document.querySelectorAll('title').length, ogSite: m('meta[property="og:site_name"]'), ogTitle: m('meta[property="og:title"]'), ogAlt: m('meta[property="og:image:alt"]'), desc: m('meta[name="description"]'), ld, probes: document.querySelectorAll('[data-gmprobe]').length, probeInHead: !!document.head.querySelector('[data-gmprobe]') };
});
r.rawTitle = (head.match(/<title>[\s\S]*?<\/title>/) || [''])[0];
r.rawLd = (raw.match(/<script type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/) || ['', ''])[1].slice(0, 300);
r.rawOgSite = (head.match(/<meta property="og:site_name"[^>]*>/) || [''])[0];
r.rawOgTitle = (head.match(/<meta property="og:title"[^>]*>/) || [''])[0];
console.log(JSON.stringify({ port, typed: title, ...r }, null, 1));
await b.close();
