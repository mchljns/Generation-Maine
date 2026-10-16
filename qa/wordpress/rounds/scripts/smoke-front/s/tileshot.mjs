import { launch, newCtx, dir } from './lib.mjs'
const out = dir('roster'); const run = process.argv[2] || 'r1'
const b = await launch()
for (const [w, h] of [[320, 568], [390, 844], [1440, 900]]) {
  const ctx = await newCtx(b, { w, h, phone: w < 900 }); const p = await ctx.newPage()
  await p.goto(process.env.URL, { waitUntil: 'networkidle' }); await p.waitForTimeout(500)
  const t = p.locator('.roster .tile').nth(8); await t.scrollIntoViewIfNeeded(); await p.waitForTimeout(300)
  const info = await t.evaluate(e => { const n = e.querySelector('.n'), bb = e.querySelector('b'), tw = e.querySelector('.town'); const r = x => { const q = x.getBoundingClientRect(); return [Math.round(q.left), Math.round(q.width), Math.round(q.height)] }; return { tile: r(e), n: r(n), nScroll: n.scrollWidth, name: r(bb), town: r(tw), nameText: bb.textContent } })
  console.log(w, JSON.stringify(info))
  await t.screenshot({ path: `${out}/tile9-${process.env.TAG}-${w}-${run}.png` })
  await ctx.close()
}
await b.close()
