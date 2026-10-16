import { launch, newCtx, WP } from './lib.mjs'
const b = await launch()
for (const [w, h] of [[1440, 900], [390, 844]]) {
  const ctx = await newCtx(b, { w, h }); const p = await ctx.newPage()
  await p.goto(WP, { waitUntil: 'networkidle' }); await p.waitForTimeout(500)
  await p.evaluate(() => document.querySelector('#creators h2').scrollIntoView({ block: 'center', behavior: 'instant' })); await p.waitForTimeout(500)
  console.log(w, await p.evaluate(() => { const e = document.querySelector('#creators h2'), r = e.getBoundingClientRect(); const pts = [[0.1, 0.5], [0.5, 0.5], [0.9, 0.5], [0.5, 0.9]].map(([fx, fy]) => { const x = r.left + r.width * fx, y = r.top + r.height * fy; const t = document.elementFromPoint(x, y); return t === e || e.contains(t) ? 'self' : (t.tagName + '.' + t.className) }); const s = document.getElementById('stories').getBoundingClientRect(); return { h2: [Math.round(r.top), Math.round(r.bottom), Math.round(r.right)], pts, storiesTop: Math.round(s.top), color: getComputedStyle(e).color, sectionBg: getComputedStyle(document.getElementById('creators')).backgroundColor } }))
  await ctx.close()
}
await b.close()
