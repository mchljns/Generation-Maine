// Renders brand SVGs to PNG with Playwright (Chromium), plus the favicon and share card.
// Run from the repo root: node brand/src/render.mjs
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const fontsDir = path.join(root, 'brand', 'fonts');
const exe = fs.existsSync('/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
  ? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' : undefined;

const b64 = (f) => `url(data:font/ttf;base64,${fs.readFileSync(path.join(fontsDir, f)).toString('base64')})`;
const fontCss = `
@font-face{font-family:'Bricolage Grotesque';font-weight:800;src:${b64('BricolageGrotesque-ExtraBold.ttf')}}
@font-face{font-family:Inter;font-weight:400;src:${b64('Inter-Regular.ttf')}}
@font-face{font-family:Inter;font-weight:600;src:${b64('Inter-SemiBold.ttf')}}
html,body{margin:0;padding:0;background:transparent}svg{display:block}`;

const browser = await chromium.launch({ executablePath: exe });
const page = await browser.newPage();

async function render(svgFile, outFile, width) {
  const src = fs.readFileSync(svgFile, 'utf8');
  const m = src.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
  const vw = parseFloat(m[1]), vh = parseFloat(m[2]);
  const w = width || vw;
  const h = Math.round((vh / vw) * w);
  const sized = src.replace(/width="[\d.]+" height="[\d.]+"/, `width="${w}" height="${h}"`);
  await page.setViewportSize({ width: w, height: h });
  await page.setContent(`<!doctype html><html><head><style>${fontCss}</style></head><body>${sized}</body></html>`);
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: outFile, omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
}

const logoDir = path.join(root, 'brand', 'logo');
for (const f of fs.readdirSync(logoDir).filter((f) => f.endsWith('.svg'))) {
  const base = f.replace('.svg', '');
  for (const w of [512, 1024]) await render(path.join(logoDir, f), path.join(logoDir, `${base}-${w}.png`), w);
}
for (const w of [16, 32, 48, 192, 512]) await render(path.join(logoDir, 'icon.svg'), path.join(logoDir, `favicon-${w}.png`), w);

const socialDir = path.join(root, 'brand', 'social');
for (const f of fs.readdirSync(socialDir).filter((f) => f.endsWith('.svg') && !f.includes('-blank'))) {
  await render(path.join(socialDir, f), path.join(socialDir, f.replace('.svg', '.png')));
  // Blank background for Canva and CapCut: same file with every [placeholder] text slot removed.
  const src = fs.readFileSync(path.join(socialDir, f), 'utf8');
  if (src.includes('>[')) {
    const blank = src.replace(/<text[^>]*>\[[^<]*<\/text>/g, '');
    const tmp = path.join(socialDir, f.replace('.svg', '-blank.svg'));
    fs.writeFileSync(tmp, blank);
    await render(tmp, path.join(socialDir, f.replace('.svg', '-blank.png')));
    fs.unlinkSync(tmp);
  }
}

// Theme fallback favicon and apple touch icon.
const img = path.join(root, 'generation-maine', 'assets', 'img');
await render(path.join(logoDir, 'icon.svg'), path.join(img, 'icon-192.png'), 192);
await render(path.join(logoDir, 'icon.svg'), path.join(img, 'icon-180.png'), 180);
await browser.close();

// ICO and JPG via Pillow.
execFileSync('python3', ['-c', `
from PIL import Image
d='${logoDir}'
im=Image.open(d+'/favicon-48.png').convert('RGBA')
im.save(d+'/favicon.ico', sizes=[(16,16),(32,32),(48,48)])
im.save('${img}/favicon.ico', sizes=[(16,16),(32,32),(48,48)])
Image.open('${socialDir}/og-share-card-1200x630.png').convert('RGB').save('${img}/share-card.jpg', quality=86, optimize=True)
Image.open('${socialDir}/og-share-card-1200x630.png').convert('RGB').save('${socialDir}/og-share-card-1200x630.jpg', quality=86, optimize=True)
`]);
console.log('PNGs, favicon.ico and share-card.jpg written');
