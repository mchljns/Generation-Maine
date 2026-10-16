// Round 3, new: the bare Creators block (Stepper) placed in a page. Width of the section, stage and panels at 1440 and
// 390, overflow, and whether the stepper still steps.
import { launch, newCtx, dir } from './lib.mjs'
const out = dir('stepperpage'); const run = process.argv[2] || 'r1'
const b = await launch()
for (const [w, h] of [[1440, 900], [1024, 768], [390, 844]]) {
  const ctx = await newCtx(b, { w, h, phone: w < 900 }); const p = await ctx.newPage()
  const errs = []; p.on('pageerror', e => errs.push(e.message))
  await p.goto(process.env.URL, { waitUntil: 'networkidle' }); await p.waitForTimeout(700)
  const g = await p.evaluate(() => { const s = document.getElementById('stories'); if (!s) return null; const r = s.getBoundingClientRect(); const st = document.querySelector('.stage'); const pr = document.getElementById('panels').getBoundingClientRect(); return { secLeft: Math.round(r.left), secW: Math.round(r.width), top: s.offsetTop, h: s.offsetHeight, stageW: st ? Math.round(st.getBoundingClientRect().width) : 0, panelsW: Math.round(pr.width), overflowX: document.documentElement.scrollWidth - innerWidth, maxW: getComputedStyle(s).maxWidth } })
  console.log(w, JSON.stringify(g), errs)
  if (g) { await p.evaluate(({ y }) => scrollTo({ top: y, behavior: 'instant' }), { y: Math.round(g.top + (w < 900 ? 0 : 0.3 * (g.h - h))) }); await p.waitForTimeout(1200); await p.screenshot({ path: `${out}/${w}-${run}.png` }) }
  await ctx.close()
}
await b.close()
