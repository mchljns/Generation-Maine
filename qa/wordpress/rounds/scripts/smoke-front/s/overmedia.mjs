import { launch, newCtx, WP, dir } from './lib.mjs'
import { writeFileSync } from 'node:fs'
const out = dir('contrast')
const run = process.argv[2] || 'r1'
const b = await launch()
const res = []
for (const [w, h] of [[1440, 900], [390, 844]]) {
  const ctx = await newCtx(b, { w, h, dsf: 1 })
  const p = await ctx.newPage()
  await p.goto(WP, { waitUntil: 'networkidle' }); await p.waitForTimeout(500)
  const geo = await p.evaluate(() => { const s = document.getElementById('stories'); return { top: s.offsetTop, total: s.offsetHeight - innerHeight } })
  for (let k = 0; k < 9; k++) {
    if (w > 900) { await p.evaluate(({ y }) => window.scrollTo({ top: y, behavior: 'instant' }), { y: Math.round(geo.top + (k + 0.5) / 9 * geo.total) }) }
    else { await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.tap(`#segs button:nth-child(${k + 1})`) }
    await p.waitForTimeout(1500)
    const sel = w > 900 ? '#stage .who.on span' : `#story-${k + 1} .pv .who span`
    for (let f = 0; f < 3; f++) {
      const box = await p.evaluate(sel => { const e = document.querySelector(sel); const r = e.getBoundingClientRect(); e.closest('.who').style.visibility = 'hidden'; return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) } }, sel)
      const buf = await p.screenshot({ clip: { x: box.x, y: box.y, width: Math.max(1, box.w), height: Math.max(1, box.h) } })
      await p.evaluate(sel => { document.querySelector(sel).closest('.who').style.visibility = '' }, sel)
      writeFileSync(`${out}/bg-${w}-${k + 1}-${f}-${run}.png`, buf)
      res.push({ w, k: k + 1, f, file: `${out}/bg-${w}-${k + 1}-${f}-${run}.png` })
      await p.waitForTimeout(700)
    }
  }
  await ctx.close()
}
writeFileSync(`${out}/bg-index-${run}.json`, JSON.stringify(res))
await b.close()
