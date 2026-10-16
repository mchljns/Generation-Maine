import { launch, base } from './lib.mjs';
const [port] = process.argv.slice(2); const B = base(port);
const b = await launch(); const q = await (await b.newContext()).newPage(); const out = [];
for (const v of ['1', '2', '3']) {
  const r = await q.goto(B + '/?gmprobe=' + v); const raw = await r.text(); const head = raw.split('</head>')[0];
  const d = await q.evaluate(() => ({ docTitle: document.title, titles: document.querySelectorAll('title').length, probes: [...document.querySelectorAll('[data-gmprobe]')].map(e => e.outerHTML), ogTitle: (document.querySelector('meta[property="og:title"]') || {}).content, desc: (document.querySelector('meta[name="description"]') || {}).content }));
  out.push({ v, rawTitle: (head.match(/<title>[\s\S]*?<\/title>/) || [''])[0], rawOgTitle: (head.match(/<meta property="og:title"[^>]*>/) || [''])[0], ...d });
}
console.log(JSON.stringify({ port, out }, null, 1)); await b.close();
