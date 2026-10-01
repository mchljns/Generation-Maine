// Full-page screenshot of a local HTML file. node brand/src/shot.mjs <in.html> <out.png> [width] [scale]
import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
import path from 'node:path';
const [,, src, out, width = '1600', scale = '1.5'] = process.argv;
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: +width, height: 900 }, deviceScaleFactor: +scale });
await p.goto('file://' + path.resolve(src));
await p.evaluate(() => document.fonts.ready);
await p.waitForTimeout(500);
await p.screenshot({ path: out, fullPage: true });
await b.close();
