import { launch } from './lib.mjs';
const [url, w = '1440'] = process.argv.slice(2);
const browser = await launch();
const ctx = await browser.newContext({ viewport: { width: +w, height: 900 } });
const page = await ctx.newPage();
await page.goto(url, { waitUntil: 'networkidle' });
console.log(JSON.stringify(await page.evaluate(() => {
  const g = document.querySelector('.wp-block-gallery'); const cs = getComputedStyle(g);
  return { gw: g.getBoundingClientRect().width, gap: cs.gap, gapVar: cs.getPropertyValue('--wp--style--unstable-gallery-gap'), styleTags: [...document.querySelectorAll('style')].map(s => s.textContent).filter(t => /gallery/.test(t)).map(t => t.slice(0, 300)), figs: [...g.querySelectorAll('figure')].map(f => { const c = getComputedStyle(f); return { w: f.getBoundingClientRect().width, basis: c.flexBasis, grow: c.flexGrow, minW: c.minWidth, ml: c.marginLeft, mr: c.marginRight, boxs: c.boxSizing, pl: c.paddingLeft, bl: c.borderLeftWidth }; }) };
}), null, 1));
await browser.close();
