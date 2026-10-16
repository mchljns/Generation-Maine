// Screenshot the hero headline for a variant at given widths, with the dot and last-letter geometry, and the same with
// overflow-wrap set to normal (diagnosis only, not a page change).
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('dotsweep'); const run = process.argv[2] || 'r1'
const key = process.env.K || 'long7', widths = (process.env.WS || '960,1440').split(',').map(Number), target = process.env.TARGET || 'wp', dsf = +(process.env.DSF || 1)
const b = await launch()
for (const w of widths) {
  const ctx = await newCtx(b, { w, h: 900, phone: w < 900, dsf }); const p = await ctx.newPage()
  await p.goto(target === 'v2' ? V2 : `${WP}?gmh=${key}`, { waitUntil: 'networkidle' })
  if (process.env.INJECT) await p.evaluate(h => { document.querySelector('.hero h1').innerHTML = h }, process.env.INJECT)
  await p.waitForTimeout(1500)
  const geo = async () => p.evaluate(() => { const h1 = document.querySelector('.hero h1'), d = h1.querySelector('.d').getBoundingClientRect(), hs = [...h1.querySelectorAll('.here')].flatMap(s => [...s.getClientRects()]); const c = h1.getBoundingClientRect(); return { ow: getComputedStyle(h1).overflowWrap, h1: [Math.round(c.left), Math.round(c.right), Math.round(c.height)], dot: [Math.round(d.left), Math.round(d.top)], here: hs.map(r => [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]) } })
  const g1 = await geo()
  const box = await p.locator('.hero h1').boundingBox()
  await p.screenshot({ path: `${out}/${target}-${key}-${w}-dsf${dsf}-${run}.png`, clip: { x: 0, y: Math.max(0, box.y - 20), width: w, height: box.height + 40 } })
  await p.evaluate(() => { document.querySelector('.hero h1').style.overflowWrap = 'normal' }); await p.waitForTimeout(100)
  const g2 = await geo()
  console.log(`${target} ${key} ${w} dsf${dsf}: as served ${JSON.stringify(g1)} | with overflow-wrap normal ${JSON.stringify(g2)}`)
  await ctx.close()
}
await b.close()
