// Renders identity v2 SVGs to PNG with the v2 fonts embedded.
// Run from the repo root: node brand/src/render_v2.mjs
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const fw = path.join(root, 'brand', 'v2', 'fonts-web');
const exe = fs.existsSync('/opt/pw-browsers/chromium-1194/chrome-linux/chrome') ? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' : undefined;
const b64 = (f) => `url(data:font/woff2;base64,${fs.readFileSync(path.join(fw, f)).toString('base64')})`;
const css = `
@font-face{font-family:'Instrument Sans';font-weight:400 700;src:${b64('instrument-sans.woff2')}}
@font-face{font-family:'Instrument Serif';font-style:italic;src:${b64('instrument-serif-italic.woff2')}}
@font-face{font-family:Anton;src:${b64('anton-400.woff2')}}
@font-face{font-family:'IBM Plex Mono';font-weight:400 700;src:${b64('plex-mono-500.woff2')}}
html,body{margin:0;background:transparent}svg{display:block}`;

const browser = await chromium.launch({ executablePath: exe });
const page = await browser.newPage();
async function render(file, out, width) {
  const src = fs.readFileSync(file, 'utf8');
  const m = src.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
  const vw = parseFloat(m[1]), vh = parseFloat(m[2]);
  const w = Math.round(width || vw), h = Math.round((vh / vw) * w);
  const sized = src.replace(/width="[\d.]+" height="[\d.]+"/, `width="${w}" height="${h}"`);
  await page.setViewportSize({ width: w, height: h });
  await page.setContent(`<!doctype html><html><head><style>${css}</style></head><body>${sized}</body></html>`);
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: out, omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
}
for (const dir of ['first-light', 'postmark']) {
  const logo = path.join(root, 'brand', 'v2', dir, 'logo');
  for (const f of fs.readdirSync(logo).filter((f) => f.endsWith('.svg'))) await render(path.join(logo, f), path.join(logo, f.replace('.svg', '-1024.png')), 1024);
  const social = path.join(root, 'brand', 'v2', dir, 'social');
  for (const f of fs.readdirSync(social).filter((f) => f.endsWith('.svg'))) await render(path.join(social, f), path.join(social, f.replace('.svg', '.png')));
}
await page.setViewportSize({ width: 1440, height: 900 });
await page.goto('file://' + path.join(root, 'brand', 'v2', 'identity-v2.html'));
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(6000);
await page.screenshot({ path: path.join(root, 'brand', 'v2', 'identity-v2-preview.png'), fullPage: true });
await browser.close();
console.log('v2 PNGs and preview written');
