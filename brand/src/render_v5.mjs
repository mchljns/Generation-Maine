// Screenshots the v5 website mock (desktop and mobile) and exports social PNGs.
// Run from the repo root: node brand/src/render_v5.mjs
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const exe = fs.existsSync('/opt/pw-browsers/chromium-1194/chrome-linux/chrome') ? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' : undefined;
const b = await chromium.launch({ executablePath: exe });
const site = 'file://' + path.join(root, 'brand', 'v5', 'site', 'index.html');
for (const [w, name] of [[1440, 'desktop'], [390, 'mobile']]) {
  const p = await b.newPage({ viewport: { width: w, height: 900 }, deviceScaleFactor: name === 'mobile' ? 2 : 1 });
  await p.emulateMedia({ reducedMotion: 'reduce' });
  await p.goto(site); await p.evaluate(() => document.fonts.ready);
  const over = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  console.log(name, 'horizontal overflow px:', over);
  await p.screenshot({ path: path.join(root, 'brand', 'v5', 'site', name + '.png'), fullPage: true });
  await p.close();
}
// Social PNGs, rendered inside a page that has the fonts.
const css = fs.readFileSync(path.join(root, 'brand', 'v5', 'site', 'index.html'), 'utf8').match(/@font-face[^}]+}/g).join('\n')
  .replace(/font-family:Bric/g, "font-family:'Bricolage Grotesque'");
const extra = css + "\n" + css.replace(/'Bricolage Grotesque'/g, 'Bric');
const p = await b.newPage();
for (const f of fs.readdirSync(path.join(root, 'brand', 'v5', 'social')).filter((f) => f.endsWith('.svg'))) {
  const src = fs.readFileSync(path.join(root, 'brand', 'v5', 'social', f), 'utf8');
  const m = src.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
  const w = Math.round(+m[1]), h = Math.round(+m[2]);
  await p.setViewportSize({ width: w, height: h });
  await p.setContent(`<!doctype html><html><head><style>${extra} html,body{margin:0;background:transparent}svg{display:block}</style></head><body>${src}</body></html>`);
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(root, 'brand', 'v5', 'social', f.replace('.svg', '.png')), omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
}
await b.close();
console.log('v5 rendered');
