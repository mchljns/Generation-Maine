// fix4 WORD-JOINER-DOT: the shipped headline's geometry, HEAD against the fix, on the v2 page: at every width 320 to 1440 by
// 2px the h1 box, the gold word's box and the dot's box, at DSF 1, 2 and 3. Any difference over 0.5px is printed.
// usage: node geom.mjs ; env A (url, default http://127.0.0.1:8931/head/), B (default http://127.0.0.1:8931/new/), DSFS
import { launch } from './lib.mjs'
const A = process.env.A || 'http://127.0.0.1:8931/head/', B = process.env.B || 'http://127.0.0.1:8931/new/'
const dsfs = (process.env.DSFS || '1,2,3').split(',').map(Number)
const step = +(process.env.STEP || 2)
const b = await launch()
const measure = async (url, dsf) => {
  const ctx = await b.newContext({ viewport: { width: 320, height: 900 }, deviceScaleFactor: dsf }); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(1200)
  const out = {}
  for (let w = 320; w <= 1440; w += step) {
    await p.setViewportSize({ width: w, height: 900 }); await p.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))))
    out[w] = await p.evaluate(() => { const r = e => { const b = e.getBoundingClientRect(); return [b.left, b.top, b.width, b.height].map(v => Math.round(v * 100) / 100) }
      const h = document.querySelector('.hero h1'); return { h1: r(h), here: r(h.querySelector('.here')), dot: r(h.querySelector('.d')), lede: r(document.querySelector('.hero .lede')) } })
  }
  await ctx.close(); return out
}
let diffs = 0, total = 0
for (const dsf of dsfs) {
  const a = await measure(A, dsf), c = await measure(B, dsf)
  let n = 0
  for (const w of Object.keys(a)) { total++
    const d = []
    for (const k of ['h1', 'here', 'dot', 'lede']) { const m = a[w][k].map((v, i) => Math.abs(v - c[w][k][i])); if (Math.max(...m) > 0.5) d.push(`${k} ${JSON.stringify(a[w][k])} -> ${JSON.stringify(c[w][k])}`) }
    if (d.length) { n++; diffs++; if (n <= 8) console.log(`DSF ${dsf} ${w}: ${d.join('; ')}`) }
  }
  console.log(`DSF ${dsf}: ${Object.keys(a).length} widths, ${n} with a difference over 0.5px`)
}
console.log(`TOTAL ${total} width checks, ${diffs} differ`)
await b.close()
