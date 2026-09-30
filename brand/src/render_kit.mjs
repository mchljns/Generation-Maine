// Exports the brand kit: every artboard in brand/kit/kit.html as a PNG (overlays with transparency),
// logo PNGs at several sizes, the avatar, favicons, and a full-page preview.
// Run from the repo root: node brand/src/render_kit.mjs
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const kit = path.join(root, 'brand', 'kit');
const exe = fs.existsSync('/opt/pw-browsers/chromium-1194/chrome-linux/chrome') ? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' : undefined;
const b = await chromium.launch({ executablePath: exe });
fs.mkdirSync(path.join(kit, 'mockups'), { recursive: true });
fs.mkdirSync(path.join(kit, 'assets', 'video'), { recursive: true });

// Artboards at 3x, so 360 x 640 exports at 1080 x 1920.
{
  const p = await b.newPage({ viewport: { width: 1400, height: 900 }, deviceScaleFactor: 3 });
  await p.goto('file://' + path.join(kit, 'kit.html')); await p.evaluate(() => document.fonts.ready);
  const ids = await p.evaluate(() => [...document.querySelectorAll('.ab')].map((e) => e.id));
  for (const id of ids) {
    const clear = id.startsWith('ov-');
    if (clear) await p.evaluate((i) => { const e = document.getElementById(i); e.style.background = 'transparent'; e.style.boxShadow = 'none'; }, id);
    else await p.evaluate((i) => { const e = document.getElementById(i); e.style.borderRadius = '0'; e.style.boxShadow = 'none'; }, id);
    const el = await p.$('#' + id);
    const dir = clear ? path.join(kit, 'assets', 'video') : path.join(kit, 'mockups');
    await el.screenshot({ path: path.join(dir, id + '.png'), omitBackground: clear, timeout: 120000 });
  }
  console.log('artboards', ids.length);
  await p.close();
}
// Full-page preview at 1x.
{
  const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  await p.goto('file://' + path.join(kit, 'kit.html')); await p.evaluate(() => document.fonts.ready);
  const h = await p.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0, i = 0; y < h; y += 2400, i++) await p.screenshot({ path: path.join(kit, `preview-${i}.png`), clip: { x: 0, y, width: 1400, height: Math.min(2400, h - y) }, fullPage: true, timeout: 120000 });
  await p.close();
}
// Logo PNGs, avatar and favicons.
const css = fs.readFileSync(path.join(kit, 'kit.html'), 'utf8').match(/@font-face\{[^}]+\}/g).join('\n');
const p = await b.newPage();
async function png(svgFile, out, w, h) {
  const src = fs.readFileSync(svgFile, 'utf8');
  await p.setViewportSize({ width: w, height: h });
  await p.setContent(`<!doctype html><html><head><style>${css} html,body{margin:0;background:transparent}svg{display:block;width:${w}px;height:${h}px}</style></head><body>${src}</body></html>`);
  await p.screenshot({ path: out, omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
}
const logo = path.join(kit, 'assets', 'logo');
for (const f of fs.readdirSync(logo).filter((f) => f.endsWith('.svg'))) {
  const m = fs.readFileSync(path.join(logo, f), 'utf8').match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
  const k = 2000 / Math.max(+m[1], +m[2]);
  await png(path.join(logo, f), path.join(logo, f.replace('.svg', '.png')), Math.round(+m[1] * k), Math.round(+m[2] * k));
}
fs.mkdirSync(path.join(kit, 'assets', 'social'), { recursive: true });
await png(path.join(logo, 'icon.svg'), path.join(kit, 'assets', 'social', 'avatar-1080.png'), 1080, 1080);
for (const s of [16, 32, 180, 512]) await png(path.join(logo, 'icon.svg'), path.join(kit, 'assets', 'social', `favicon-${s}.png`), s, s);
await b.close();
console.log('kit rendered');
