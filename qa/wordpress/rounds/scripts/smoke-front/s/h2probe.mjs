import { launch, newCtx, WP, V2 } from './lib.mjs'
const b = await launch()
for (const [name, url] of [['wp', WP], ['v2', V2]]) {
  const ctx = await newCtx(b, { w: 1440, h: 900 }); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(800)
  console.log(name, JSON.stringify(await p.evaluate(() => [...document.querySelectorAll('.panel h2')].slice(0, 3).map(h => { const cs = getComputedStyle(h), r = h.getBoundingClientRect(); return { w: Math.round(r.width), h: Math.round(r.height), ff: cs.fontFamily.slice(0, 30), fs: cs.fontSize, fw: cs.fontWeight, ls: cs.letterSpacing, mw: cs.maxWidth, lh: cs.lineHeight, mt: cs.marginTop, mb: cs.marginBottom, txt: h.textContent } }))))
  console.log(name, 'nav', JSON.stringify(await p.evaluate(() => [...document.querySelectorAll('.top nav a')].map(a => { const r = a.getBoundingClientRect(), cs = getComputedStyle(a); return [Math.round(r.height), cs.display, cs.lineHeight, cs.paddingTop, a.parentElement.tagName] }))))
  await ctx.close()
}
await b.close()
