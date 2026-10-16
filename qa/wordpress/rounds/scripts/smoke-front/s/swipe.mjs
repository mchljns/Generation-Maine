// VIS-N05: swipe one card at a time (CDP touch, the tester's gesture) and back; print counter and scrollLeft per swipe.
// Sizes: tablets and phones in both orientations, the phone layout's full width range.
import { launch, newCtx, WP, V2 } from './lib.mjs'
const b = await launch()
const sizes = (process.env.SIZES || '768x1024,844x390,390x844,320x568,600x900,900x700,430x932').split(',').map(s => s.split('x').map(Number))
const only = process.env.ONLY || ''
const state = p => p.evaluate(() => { const pe = document.getElementById('panels'); return { n: document.getElementById('wn').textContent.slice(0, 2), x: Math.round(pe.scrollLeft), max: pe.scrollWidth - pe.clientWidth } })
let bad = 0
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h] of sizes) {
  if (only && only !== name) continue
  const ctx = await newCtx(b, { w, h, phone: true }); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(700)
  await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(500)
  const cdp = await ctx.newCDPSession(p)
  const box = await p.locator('#panels').boundingBox(); const y = Math.round(box.y + 60)
  const dist = Math.round(Math.min(200, w * 0.5)), x0 = Math.round(Math.min(w * 0.6, 300) + (w < 500 ? w * 0.2 : 0))
  const swipe = async dir => { const a = dir > 0 ? x0 : x0 - dist; await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: a, y }] }); for (let i = 1; i <= 12; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: Math.round(a - dir * dist * i / 12), y }] }); await p.waitForTimeout(16) } await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }) }
  const n = await p.evaluate(() => document.querySelectorAll('.panel').length)
  const fwd = [], back = []
  for (let i = 0; i < n; i++) { await swipe(1); await p.waitForTimeout(1100); const s = await state(p); fwd.push(s.n + '@' + s.x) }
  for (let i = 0; i < n; i++) { await swipe(-1); await p.waitForTimeout(1100); const s = await state(p); back.push(s.n + '@' + s.x) }
  const seqF = fwd.map(s => s.slice(0, 2)), seqB = back.map(s => s.slice(0, 2))
  const want = Array.from({ length: n - 1 }, (_, i) => String(i + 2).padStart(2, '0'))
  const okF = want.every((v, i) => seqF[i] === v), okB = want.slice().reverse().slice(1).concat(['01']).every((v, i) => seqB[i] === v)
  if (!okF || !okB) bad++
  console.log(name, `${w}x${h}`, okF && okB ? 'OK  ' : 'SKIP', 'forward', fwd.join(' '), '| back', back.join(' '), '| max', (await state(p)).max)
  await ctx.close()
}
console.log('sizes with a skipped card:', bad)
await b.close()
