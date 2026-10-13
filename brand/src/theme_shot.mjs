// The theme's screenshot.png for Appearance > Themes: the built page's first screen at 1200 by 900, after the mural settles.
//   node brand/src/theme_shot.mjs <in.html> <out.png>
import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
import path from 'node:path';
const [,, src, out] = process.argv;
const b = await chromium.launch({ executablePath: process.env.PW_CHROMIUM || '/opt/pw-browsers/chromium' });
const p = await b.newPage({ viewport: { width: 1200, height: 900 }, deviceScaleFactor: 1 });
await p.goto('file://' + path.resolve(src), { waitUntil: 'networkidle' });
await p.evaluate(() => document.fonts.ready);
await p.waitForTimeout(3000);
await p.screenshot({ path: out });
await b.close();
