// A strip of viewport shots, one per section, so the page background change on scroll can be seen in a still.
import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
import path from 'node:path';
const [,, src, out] = process.argv;
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: 1200, height: 760 }, deviceScaleFactor: 1 });
await p.goto('file://' + path.resolve(src)); await p.addStyleTag({ content: 'html{scroll-behavior:auto!important}' }); await p.waitForTimeout(1400);
const ids = ['top', 'about', 'creators', 'words', 'news', 'follow'];
const shots = [];
for (const id of ids) { await p.evaluate(i => { const el = document.getElementById(i); scrollTo(0, el.offsetTop - 40); }, id); await p.waitForTimeout(1300); shots.push(await p.screenshot()); }
await b.close();
const { default: sharp } = await import('/home/user/Generation-Maine/node_modules/sharp/lib/index.js').catch(() => ({ default: null }));
import fs from 'node:fs';
shots.forEach((s, i) => fs.writeFileSync(`${out}-${i}.png`, s));
console.log('shots', shots.length);
