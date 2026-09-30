// Records the motion prototype: the load, then the pointer crossing the hero, then the mural drawing in.
// node brand/src/record_motion.mjs
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const out = path.join(root, 'brand', 'identity', 'motion', 'frames');
fs.rmSync(out, { recursive: true, force: true }); fs.mkdirSync(out, { recursive: true });
const exe = fs.existsSync('/opt/pw-browsers/chromium-1194/chrome-linux/chrome') ? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' : undefined;
const b = await chromium.launch({ executablePath: exe });
const p = await b.newPage({ viewport: { width: 1200, height: 680 }, deviceScaleFactor: 1 });
let n = 0;
const shot = async () => { await p.screenshot({ path: path.join(out, `f${String(n++).padStart(3, '0')}.png`) }); };
await p.goto('file://' + path.join(root, 'brand', 'identity', 'motion', 'hero.html'));
await p.evaluate(() => document.fonts.ready);
// the load: 1.3 s at 12 fps
for (let i = 0; i < 16; i++) { await shot(); await p.waitForTimeout(80); }
// the pointer crosses the hero on a gentle arc, 3 s
for (let i = 0; i <= 36; i++) { const t = i / 36; const x = 200 + 850 * t; const y = 330 + 120 * Math.sin(t * Math.PI * 1.2) - 60 * t; await p.mouse.move(x, y); await p.waitForTimeout(70); await shot(); }
await p.mouse.move(1300, 700); for (let i = 0; i < 6; i++) { await p.waitForTimeout(80); await shot(); }
// scroll to the mural and let it draw
await p.evaluate(() => document.getElementById('mural').scrollIntoView({ behavior: 'instant', block: 'start' }));
for (let i = 0; i < 22; i++) { await p.waitForTimeout(90); await shot(); }
await p.screenshot({ path: path.join(root, 'brand', 'identity', 'motion', 'hero-still.png') });
await p.evaluate(() => scrollTo(0, 0)); await p.mouse.move(640, 420); await p.waitForTimeout(600);
await p.screenshot({ path: path.join(root, 'brand', 'identity', 'motion', 'hero-pointer-still.png') });
await b.close();
console.log('frames', n);
