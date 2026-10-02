// Exports every artboard in brand/identity/apply/apply.html as a PNG at 3x.
// node brand/src/render_apply.mjs
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const dir = path.join(root, 'brand', 'identity', process.argv[2] || 'apply');
const exe = fs.existsSync('/opt/pw-browsers/chromium-1194/chrome-linux/chrome') ? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' : undefined;
const b = await chromium.launch({ executablePath: exe });
fs.mkdirSync(path.join(dir, 'mockups'), { recursive: true });
const p = await b.newPage({ viewport: { width: 1400, height: 900 }, deviceScaleFactor: 3 });
await p.goto('file://' + path.join(dir, 'apply.html')); await p.evaluate(() => document.fonts.ready);
const ids = await p.evaluate(() => [...document.querySelectorAll('.ab')].map((e) => e.id));
for (const id of ids) {
  await p.evaluate((i) => { const e = document.getElementById(i); e.style.borderRadius = '0'; e.style.boxShadow = 'none'; }, id);
  const el = await p.$('#' + id);
  await el.screenshot({ path: path.join(dir, 'mockups', id + '.png'), timeout: 120000 });
}
await b.close();
console.log('artboards', ids.length);
