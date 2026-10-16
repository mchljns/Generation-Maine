import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('contrast')
const run = process.argv[2] || 'r1'
const b = await launch()
for (const [name, url] of [['wp', WP], ['v2', V2]]) {
  const ctx = await newCtx(b, { w: 1440, h: 900, dsf: 2 })
  const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(500)
  const geo = await p.evaluate(() => { const s = document.getElementById('stories'); return { top: s.offsetTop, total: s.offsetHeight - innerHeight } })
  for (const k of [2, 3, 5]) {
    await p.evaluate(({ y }) => window.scrollTo({ top: y, behavior: 'instant' }), { y: Math.round(geo.top + (k - 0.5) / 9 * geo.total) }); await p.waitForTimeout(1500)
    const r = await p.evaluate(() => { const r = document.getElementById('stage').getBoundingClientRect(); return { x: r.left, y: r.top, width: r.width, height: 90 } })
    await p.screenshot({ path: `${out}/who-${name}-clip${k}-${run}.png`, clip: r })
  }
  await ctx.close()
}
await b.close()
