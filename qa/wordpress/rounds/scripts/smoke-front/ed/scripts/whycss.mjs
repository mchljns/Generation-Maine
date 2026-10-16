// Print the CSS rules that match an element (CDP), for one property. usage: node whycss.mjs <url> <selector> <prop> [width]
import { launch } from './lib.mjs';
const [url, sel, prop, w = '1440'] = process.argv.slice(2);
const browser = await launch();
const ctx = await browser.newContext({ viewport: { width: +w, height: 900 } });
const page = await ctx.newPage();
await page.goto(url, { waitUntil: 'networkidle' });
const cdp = await ctx.newCDPSession(page);
await cdp.send('DOM.enable'); await cdp.send('CSS.enable');
const { root } = await cdp.send('DOM.getDocument', { depth: -1 });
const { nodeId } = await cdp.send('DOM.querySelector', { nodeId: root.nodeId, selector: sel });
const m = await cdp.send('CSS.getMatchedStylesForNode', { nodeId });
for (const r of m.matchedCSSRules) {
  const decl = r.rule.style.cssProperties.filter(p => p.name === prop || p.name.startsWith(prop));
  if (decl.length) console.log(r.rule.origin, '|', r.rule.selectorList.text.slice(0, 200), '|', (r.rule.media || []).map(x => x.text).join(','), '|', decl.map(d => d.name + ':' + d.value).join('; '));
}
const comp = await page.$eval(sel, (e, p) => getComputedStyle(e)[p], prop.replace(/-([a-z])/g, (_, c) => c.toUpperCase()));
console.log('computed', prop, comp);
await browser.close();
