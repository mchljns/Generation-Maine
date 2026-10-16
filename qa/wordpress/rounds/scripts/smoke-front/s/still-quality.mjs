// Round 2: the still a paused clip shows. With reduced motion the clips start paused. Story 5 on 8512 has a 1080x1080
// avatar. Record the still's file, its natural size, the size it is drawn at in device pixels, and screenshot it.
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('still')
const run = process.argv[2] || 'r1'
const b = await launch()
const info = (p, sel) => p.evaluate(sel => { const c = document.querySelector(sel); const r = c.getBoundingClientRect(); const cs = getComputedStyle(c); return { src: (c.getAttribute('src') || '').replace(/^.*\//, ''), natural: [c.naturalWidth, c.naturalHeight], css: [Math.round(r.width), Math.round(r.height)], fit: cs.objectFit, dpr: devicePixelRatio, upscale: +(Math.max(r.width / c.naturalWidth, r.height / c.naturalHeight) * devicePixelRatio).toFixed(2) } }, sel)
for (const [name, url] of [['wp8512', 'http://127.0.0.1:8512/'], ['wp8502', WP], ['v2', V2]]) {
  // desktop 1440 at device scale 2
  let ctx = await newCtx(b, { w: 1440, h: 900, reduced: true, dsf: 2 }); let p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(600)
  const g = await p.evaluate(() => { const s = document.getElementById('stories'); return { top: s.offsetTop, total: s.offsetHeight - innerHeight } })
  await p.evaluate(({ y }) => scrollTo({ top: y, behavior: 'instant' }), { y: Math.round(g.top + 4.5 / 9 * g.total) }); await p.waitForTimeout(1500)
  console.log(name, '1440@2x stage story 5 paused', JSON.stringify(await info(p, '#stage .clip.on')), 'pressed', await p.getAttribute('#cpause', 'aria-pressed'))
  await p.locator('#stage').screenshot({ path: `${out}/${name}-1440-stage5-paused-${run}.png` })
  await ctx.close()
  // phone 390 at device scale 3
  ctx = await newCtx(b, { w: 390, h: 844, reduced: true, dsf: 3 }); p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(600)
  await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.tap('#segs button:nth-child(5)'); await p.waitForTimeout(1300)
  console.log(name, '390@3x card 5 paused', JSON.stringify(await info(p, '#story-5 .pv .clip')))
  await p.locator('#story-5 .pv').screenshot({ path: `${out}/${name}-390-card5-paused-${run}.png` })
  await p.tap('#story-5 .pv'); await p.waitForTimeout(900)
  console.log(name, '390@3x viewer 5 paused', JSON.stringify(await info(p, '#vtrack .slide:nth-child(5) .clip')))
  await p.screenshot({ path: `${out}/${name}-390-viewer5-paused-${run}.png` })
  await ctx.close()
}
await b.close()
