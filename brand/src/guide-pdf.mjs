// Exports brand/brand-guide.html to brand/brand-guide.pdf (Letter landscape).
import { chromium } from 'playwright';
import path from 'node:path';
import fs from 'node:fs';
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const exe = fs.existsSync('/opt/pw-browsers/chromium-1194/chrome-linux/chrome') ? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' : undefined;
const b = await chromium.launch({ executablePath: exe });
const p = await b.newPage();
await p.goto('file://' + path.join(root, 'brand', 'brand-guide.html'), { waitUntil: 'load' });
await p.evaluate(() => document.fonts.ready);
await p.pdf({ path: path.join(root, 'brand', 'brand-guide.pdf'), width: '11in', height: '8.5in', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
await p.setViewportSize({ width: 1100, height: 900 });
await p.screenshot({ path: path.join(root, 'qa', 'screenshots', 'brand-guide-preview.png'), fullPage: true });
await b.close();
console.log('brand-guide.pdf written');
