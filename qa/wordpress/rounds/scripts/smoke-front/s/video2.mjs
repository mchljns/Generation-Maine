// Round 2: video clips (three creators set to a WebM clip) with the pause control, reduced motion, and the viewer.
import { launch, newCtx, WP, dir } from './lib.mjs'
const out = dir('video')
const run = process.argv[2] || 'r1'
const b = await launch()
const vs = p => p.evaluate(() => {
  const f = sel => [...document.querySelectorAll(sel)].map((v, i) => v.tagName === 'VIDEO' ? `${i}:${v.getAttribute('src') ? 'src' : '-'}${v.paused ? 'P' : 'PLAY'}${v.controls ? 'C' : ''}` : null).filter(Boolean).join(' ')
  const btn = document.getElementById('cpause')
  return { stage: f('#stage .clip'), panels: f('.panel .clip'), viewer: f('#vtrack .clip'), wn: document.getElementById('wn').textContent, pressed: btn && btn.getAttribute('aria-pressed') }
})
for (const reduced of [false, true]) {
  const mode = reduced ? 'reduce' : 'motion'
  // desktop
  const ctx = await newCtx(b, { w: 1440, h: 900, reduced })
  const p = await ctx.newPage()
  await p.goto(WP, { waitUntil: 'networkidle' }); await p.waitForTimeout(500)
  const geo = await p.evaluate(() => { const s = document.getElementById('stories'); return { top: s.offsetTop, total: s.offsetHeight - innerHeight } })
  const go = async k => { await p.evaluate(({ y }) => window.scrollTo({ top: y, behavior: 'instant' }), { y: Math.round(geo.top + (k - 0.5) / 9 * geo.total) }); await p.waitForTimeout(1500) }
  for (const k of [1, 2, 3]) { await go(k); console.log(run, mode, 'desktop step', k, JSON.stringify(await vs(p))) }
  await p.click('#cpause'); await p.waitForTimeout(800)
  console.log(run, mode, 'desktop step 3 after pause button', JSON.stringify(await vs(p)))
  await go(2); console.log(run, mode, 'desktop step 2 after pause button', JSON.stringify(await vs(p)))
  await p.click('#cpause'); await p.waitForTimeout(800)
  console.log(run, mode, 'desktop step 2 after pause button again', JSON.stringify(await vs(p)))
  await ctx.close()
  // phone
  const c2 = await newCtx(b, { w: 390, h: 844, reduced })
  const q = await c2.newPage()
  await q.goto(WP, { waitUntil: 'networkidle' }); await q.waitForTimeout(500)
  await q.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await q.waitForTimeout(1500)
  console.log(run, mode, 'phone card 1', JSON.stringify(await vs(q)))
  await q.tap('#segs button:nth-child(2)'); await q.waitForTimeout(1500)
  console.log(run, mode, 'phone card 2', JSON.stringify(await vs(q)))
  await q.tap('.panel.on .pv'); await q.waitForTimeout(1500)
  console.log(run, mode, 'viewer open on 2', JSON.stringify(await vs(q)))
  await q.screenshot({ path: `${out}/viewer2-${mode}-${run}.png` })
  await q.keyboard.press('ArrowRight'); await q.waitForTimeout(1200)
  console.log(run, mode, 'viewer ArrowRight to 3', JSON.stringify(await vs(q)))
  await q.keyboard.press('Escape'); await q.waitForTimeout(1200)
  console.log(run, mode, 'viewer closed', JSON.stringify(await vs(q)))
  await q.tap('#cpause'); await q.waitForTimeout(800)
  console.log(run, mode, 'phone after pause button tap', JSON.stringify(await vs(q)))
  await q.tap('.panel.on .pv'); await q.waitForTimeout(1500)
  console.log(run, mode, 'viewer opened after pause button tap', JSON.stringify(await vs(q)))
  await q.keyboard.press('Escape'); await q.waitForTimeout(1200)
  await c2.close()
}
await b.close()
