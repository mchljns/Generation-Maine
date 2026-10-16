// Round 2: a creator with no avatar while the clips are paused (reduced motion), desktop stage, phone card and viewer
import { launch, newCtx, WP, dir } from './lib.mjs'
const out = dir('pause'); const run = process.argv[2] || 'r1'
const b = await launch()
for (const [w, h] of [[1440, 900], [390, 844]]) {
  const ctx = await newCtx(b, { w, h, reduced: true }); const p = await ctx.newPage()
  await p.goto(WP, { waitUntil: 'networkidle' }); await p.waitForTimeout(800)
  if (w > 900) { const g = await p.evaluate(() => { const s = document.getElementById('stories'); return { top: s.offsetTop, total: s.offsetHeight - innerHeight } }); await p.evaluate(({ y }) => scrollTo({ top: y, behavior: 'instant' }), { y: Math.round(g.top + 3.5 / 9 * g.total) }) }
  else { await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.tap('#segs button:nth-child(4)') }
  await p.waitForTimeout(1500)
  const sel = w > 900 ? '#stage' : '#story-4 .pv'
  const r = await p.evaluate(sel => { const c = document.querySelector(sel).querySelector(w => 0) ; return 0 }, sel).catch(() => 0)
  const s = await p.evaluate(sel => { const box = document.querySelector(sel); const c = w => w; const clip = sel === '#stage' ? box.querySelector('.clip.on') : box.querySelector('.clip'); return { wn: document.getElementById('wn').textContent, pressed: document.getElementById('cpause').getAttribute('aria-pressed'), src: clip.getAttribute('src'), hasStill: 'still' in clip.dataset, alt: clip.getAttribute('alt') } }, sel)
  console.log(w, 'reduce, creator 4 without avatar', JSON.stringify(s))
  await p.locator(sel).screenshot({ path: `${out}/noavatar-${w}-paused-${run}.png` })
  if (w < 900) { await p.tap('#story-4 .pv'); await p.waitForTimeout(900); await p.screenshot({ path: `${out}/noavatar-${w}-viewer-${run}.png` }); console.log(w, 'viewer src', await p.evaluate(() => document.querySelector('#vtrack .slide:nth-child(4) .clip').getAttribute('src'))) }
  await ctx.close()
}
await b.close()
