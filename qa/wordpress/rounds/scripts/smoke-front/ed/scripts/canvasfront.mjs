// Front Page: canvas against the page at the same width; font family, size, weight, color, background, transform per element.
import { launch, login, save, openTemplate } from './lib.mjs';
const [base, tag, v65s] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
const f = await openTemplate(page, base, v65s === '1');
const SEL = ['.gm-bar nav a', '.gm-bar .cta a', '.hero .k', '.hero h1', '.hero .lede', '.hero .wp-block-button__link', '.about .k', '.about .big', '.about .note', '.about .goal', '#creators h2, .stories-head h2', '.follow h2', '.follow .lede', '.follow .row .name, .follow .row b', '.nl .k', '.nl h3'];
const M = (sels) => sels.map(s => { const e = document.querySelector(s); if (!e) return [s, null]; const c = getComputedStyle(e); return [s, [c.fontFamily.split(',')[0], c.fontSize, c.fontWeight, c.color, c.textTransform, c.letterSpacing, c.lineHeight].join(' ')]; });
const ed = await f.evaluate(M, SEL);
const vw = await f.evaluate(() => document.documentElement.clientWidth);
const p = await browser.newPage({ viewport: { width: vw, height: 900 } });
await p.goto(base + '/', { waitUntil: 'networkidle' });
const fr = await p.evaluate(M, SEL);
const diffs = ed.map((e, i) => e[1] === fr[i][1] ? null : { sel: e[0], editor: e[1], front: fr[i][1] }).filter(Boolean);
save(`${tag}-canvasfront.json`, { vw, ed, fr, diffs });
console.log('canvas width', vw, 'elements', SEL.length, 'differences', JSON.stringify(diffs, null, 1));
await browser.close();
