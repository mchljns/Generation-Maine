// The long-gap pages as a visitor at 1440 and 390: is every gold-word heading there, with its gold word and dot?
import { launch, save } from './lib.mjs';
const [base, tag, ...paths] = process.argv.slice(2);
const browser = await launch();
const out = {};
for (const path of paths) for (const w of [1440, 390]) {
  const p = await browser.newPage({ viewport: { width: w, height: 900 } });
  const r = await p.goto(base + path, { waitUntil: 'networkidle' });
  out[path + '@' + w] = await p.evaluate(() => ({ headings: [...document.querySelectorAll('main h2.gm-here')].map(h => ({ cls: h.className.replace('wp-block-heading gm-here ', ''), len: h.innerHTML.length, gold: [...h.querySelectorAll('.here')].map(s => s.textContent), dots: h.querySelectorAll('.d').length, height: Math.round(h.getBoundingClientRect().height) })), overflow: document.documentElement.scrollWidth - innerWidth }));
  out[path + '@' + w].status = r.status();
  await p.close();
}
save(`${tag}-longgap.json`, out);
for (const [k, v] of Object.entries(out)) console.log(k, v.status, 'overflow', v.overflow, JSON.stringify(v.headings));
await browser.close();
