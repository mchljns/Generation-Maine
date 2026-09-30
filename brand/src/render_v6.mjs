// Renders v6: website screenshots (desktop and mobile), an axe accessibility check, social PNGs,
// mark PNGs and the explorations sheet. Run from the repo root: node brand/src/render_v6.mjs
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const v6 = path.join(root, 'brand', 'v6');
const exe = fs.existsSync('/opt/pw-browsers/chromium-1194/chrome-linux/chrome') ? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' : undefined;
const b = await chromium.launch({ executablePath: exe });
const site = 'file://' + path.join(v6, 'site', 'index.html');
const axeSrc = fs.readFileSync(path.join(root, 'node_modules', 'axe-core', 'axe.min.js'), 'utf8');
const qa = { violations: 0, details: [] };
for (const [w, name] of [[1440, 'desktop'], [390, 'mobile']]) {
  const p = await b.newPage({ viewport: { width: w, height: 900 }, deviceScaleFactor: name === 'mobile' ? 2 : 1 });
  await p.emulateMedia({ reducedMotion: 'reduce' });
  await p.goto(site); await p.evaluate(() => document.fonts.ready);
  const over = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  await p.addScriptTag({ content: axeSrc });
  const res = await p.evaluate(async () => (await axe.run(document, { runOnly: ['wcag2a', 'wcag2aa', 'wcag21aa', 'best-practice'] })).violations.map((v) => ({ id: v.id, impact: v.impact, n: v.nodes.length, t: v.nodes.slice(0, 3).map((x) => x.target.join(' ')) })));
  qa.violations += res.length; qa.details.push({ name, overflow: over, res });
  console.log(name, 'overflow', over, 'axe violations', JSON.stringify(res));
  await p.screenshot({ path: path.join(v6, 'site', name + '.png'), fullPage: true });
  await p.close();
}
fs.writeFileSync(path.join(v6, 'site', 'qa.json'), JSON.stringify(qa, null, 2));
// Mobile contact sheet: the full-height mobile page split into columns.
{
  const img = 'data:image/png;base64,' + fs.readFileSync(path.join(v6, 'site', 'mobile.png')).toString('base64');
  const p = await b.newPage({ viewport: { width: 400, height: 400 } });
  await p.setContent(`<img id="i" src="${img}">`);
  const h = await p.evaluate(() => new Promise((r) => { const i = document.getElementById('i'); if (i.complete) r(i.naturalHeight); else i.onload = () => r(i.naturalHeight); }));
  const colH = 1560, cols = Math.ceil(h / 2 / colH);
  await p.setViewportSize({ width: cols * 410 - 20, height: colH });
  let html = '<body style="margin:0;background:#F4F0E6;display:flex;gap:20px">';
  for (let c = 0; c < cols; c++) html += `<div style="width:390px;height:${colH}px;overflow:hidden;position:relative"><img src="${img}" style="width:390px;position:absolute;top:${-c * colH}px"></div>`;
  await p.setContent(html + '</body>');
  await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(v6, 'site', 'mobile-sheet.png') });
  await p.close();
}
// Explorations sheet.
{
  const p = await b.newPage({ viewport: { width: 1100, height: 800 } });
  await p.goto('file://' + path.join(v6, 'explorations.html'));
  await p.screenshot({ path: path.join(v6, 'explorations.png'), fullPage: true });
  await p.close();
}
// Social and logo PNGs, rendered with the brand fonts available.
const css = fs.readFileSync(path.join(v6, 'site', 'index.html'), 'utf8').match(/@font-face\{[^}]+\}/g).join('\n');
const fonts = css + '\n' + css.replace(/font-family:Bric/g, "font-family:'Bricolage Grotesque'");
const p = await b.newPage();
for (const dir of ['social', 'logo']) {
  for (const f of fs.readdirSync(path.join(v6, dir)).filter((f) => f.endsWith('.svg'))) {
    const src = fs.readFileSync(path.join(v6, dir, f), 'utf8');
    const m = src.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
    const k = dir === 'logo' ? 4 : 1;
    const w = Math.round(+m[1] * k), h = Math.round(+m[2] * k);
    await p.setViewportSize({ width: w, height: h });
    await p.setContent(`<!doctype html><html><head><style>${fonts} html,body{margin:0;background:transparent}svg{display:block;width:${w}px;height:${h}px}</style></head><body>${src}</body></html>`);
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(v6, dir, f.replace('.svg', '.png')), omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
  }
}
await b.close();
console.log('v6 rendered');
