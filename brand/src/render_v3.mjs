// Screenshots the v3 concepts page and exports each concept's key pieces as PNG.
// Run from the repo root: node brand/src/render_v3.mjs
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const exe = fs.existsSync('/opt/pw-browsers/chromium-1194/chrome-linux/chrome') ? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' : undefined;
const b = await chromium.launch({ executablePath: exe });
const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
await p.goto('file://' + path.join(root, 'brand', 'v3', 'concepts.html'));
await p.evaluate(() => document.fonts.ready);
await p.screenshot({ path: path.join(root, 'brand', 'v3', 'concepts-preview.png'), fullPage: true });
for (const key of ['viewfinder', 'rings', 'woven']) {
  const sec = await p.$('#' + key);
  await sec.screenshot({ path: path.join(root, 'brand', 'v3', key, key + '-board.png') });
  const figs = await sec.$$('.apps figure svg');
  const names = ['avatar', 'endcard', 'lowerthird'];
  for (let i = 0; i < figs.length; i++) await figs[i].screenshot({ path: path.join(root, 'brand', 'v3', key, names[i] + '.png'), omitBackground: true });
}
await b.close();
console.log('v3 rendered');
