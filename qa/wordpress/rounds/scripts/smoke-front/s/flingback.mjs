// Round 3, new: swiping back from the end of the phone carousel. Start on the last card (segment tap), then a fast flick
// or a slow long drag toward the start. Record every counter value and scrollLeft each frame for 2.5 s after release,
// the furthest point reached, where the track ends, and screenshots at the furthest point and at the end.
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('flingback'); const run = process.argv[2] || 'r1'
const b = await launch()
const sizes = (process.env.SIZES || '390x844,768x1024,844x390,320x568').split(',').map(s => s.split('x').map(Number))
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h] of sizes) for (const [kind, from] of [['flick', 9], ['slowdrag', 9], ['flick', 8], ['slowdrag', 8], ['flick', 7]]) {
  const ctx = await newCtx(b, { w, h, phone: true }); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(700)
  await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(400)
  await p.tap(`#segs button:nth-child(${from})`); await p.waitForTimeout(1300)
  const cdp = await ctx.newCDPSession(p)
  const box = await p.locator('#panels').boundingBox(); const y = Math.round(box.y + 60)
  await p.evaluate(() => { window.__trace = []; const pe = document.getElementById('panels'), wn = document.getElementById('wn'); const t0 = performance.now(); const tick = () => { window.__trace.push([Math.round(performance.now() - t0), Math.round(pe.scrollLeft), wn.textContent.slice(0, 2)]); if (performance.now() - t0 < 4000) requestAnimationFrame(tick) }; requestAnimationFrame(tick) })
  const x0 = Math.round(w * 0.08), dx = Math.round(w * 0.85)
  const [steps, dt] = kind === 'flick' ? [4, 8] : [30, 25]
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y }] })
  for (let i = 1; i <= steps; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: x0 + Math.round(dx * i / steps), y }] }); await p.waitForTimeout(dt) }
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] })
  // screenshot near the furthest point: poll until scrollLeft stops falling
  let last = 1e9, shotDone = false
  for (let i = 0; i < 40 && !shotDone; i++) { const x = await p.evaluate(() => document.getElementById('panels').scrollLeft); if (x >= last - 1 && i > 2) { await p.screenshot({ path: `${out}/${name}-${w}x${h}-${kind}-from${from}-furthest-${run}.png` }); shotDone = true } last = x; await p.waitForTimeout(30) }
  await p.waitForTimeout(2500)
  const tr = await p.evaluate(() => window.__trace)
  const end = tr[tr.length - 1], min = tr.reduce((a, r) => r[1] < a[1] ? r : a, tr[0])
  // counter values in order, collapsing repeats
  const seq = tr.map(r => r[2]).filter((v, i, a) => i === 0 || v !== a[i - 1])
  const backTravel = min[1] < end[1] - 5 ? `then moved FORWARD ${end[1] - min[1]}px back to ${end[2]} (from t=${min[0]}ms to ~${tr.find(r => r[0] > min[0] && Math.abs(r[1] - end[1]) < 2)?.[0]}ms)` : 'no return'
  console.log(`${name} ${w}x${h} ${kind} back from ${from}: start ${tr[0][2]}@${tr[0][1]}, furthest ${min[2]}@${min[1]} at t=${min[0]}ms, end ${end[2]}@${end[1]}; ${backTravel}; counter sequence ${seq.join(' ')}`)
  await p.screenshot({ path: `${out}/${name}-${w}x${h}-${kind}-from${from}-end-${run}.png` })
  await ctx.close()
}
await b.close()
