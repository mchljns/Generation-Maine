// Round 3, VIS-N05 variations: long flings (CDP synthesized touch scroll gestures with fling, and fast flicks), then
// one-card swipes from wherever the fling stopped. After each gesture: counter, current segment, scrollLeft, and whether
// the current card is fully on screen and which card's left edge sits nearest the gutter.
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('fling'); const run = process.argv[2] || 'r1'
const b = await launch()
const sizes = (process.env.SIZES || '320x568,390x844,430x932,600x900,768x1024,844x390').split(',').map(s => s.split('x').map(Number))
const state = p => p.evaluate(() => {
  const pe = document.getElementById('panels'), g = parseFloat(getComputedStyle(pe).paddingLeft), c = pe.getBoundingClientRect()
  const panels = [...document.querySelectorAll('.panel')]
  const n = +document.getElementById('wn').textContent.slice(0, 2)
  const seg = [...document.querySelectorAll('#segs button')].findIndex(x => x.getAttribute('aria-current') === 'true') + 1
  const r = panels[n - 1].getBoundingClientRect()
  const full = r.left >= c.left - 1 && r.right <= innerWidth + 1
  const offs = panels.map(p => Math.round(p.getBoundingClientRect().left - c.left - g))
  const atGutter = offs.reduce((a, o, i) => Math.abs(o) < Math.abs(offs[a]) ? i : a, 0) + 1
  const playing = [...document.querySelectorAll('.panel .clip')].map((x, i) => x.classList.contains('on') || (x.tagName === 'VIDEO' && !x.paused) ? i + 1 : 0).filter(Boolean)
  return { n, seg, x: Math.round(pe.scrollLeft), max: pe.scrollWidth - pe.clientWidth, full, curOff: offs[n - 1], atGutter }
})
const fmt = s => `${String(s.n).padStart(2, '0')}${s.seg !== s.n ? '(seg' + s.seg + ')' : ''}@${s.x}${s.full ? '' : '[NOT FULLY VISIBLE off ' + s.curOff + ']'}`
let problems = 0
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h] of sizes) {
  const ctx = await newCtx(b, { w, h, phone: true }); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(700)
  await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(500)
  const cdp = await ctx.newCDPSession(p)
  const box = await p.locator('#panels').boundingBox(); const y = Math.round(box.y + 60)
  const rows = []
  const gesture = async (dx, speed, label) => {
    const x = dx < 0 ? Math.round(w * 0.85) : Math.round(w * 0.15)
    await cdp.send('Input.synthesizeScrollGesture', { x, y, xDistance: dx, yDistance: 0, speed, gestureSourceType: 'touch', preventFling: false, repeatCount: 1 })
    await p.waitForTimeout(1800)
    const s = await state(p); rows.push(`${label} ${fmt(s)}`); if (!s.full || s.seg !== s.n) problems++
    return s
  }
  const flick = async (dir, label) => { // a short fast flick: 3 moves of 60px in 24ms
    const x0 = dir > 0 ? Math.round(w * 0.7) : Math.round(w * 0.3)
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y }] })
    for (let i = 1; i <= 3; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: x0 - dir * 60 * i, y }] }); await p.waitForTimeout(8) }
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] })
    await p.waitForTimeout(1800)
    const s = await state(p); rows.push(`${label} ${fmt(s)}`); if (!s.full || s.seg !== s.n) problems++
    return s
  }
  const swipe = async (dir, label) => { const dist = Math.round(Math.min(200, w * 0.5)), a = dir > 0 ? Math.round(w * 0.6) : Math.round(w * 0.6) - dist
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: a, y }] }); for (let i = 1; i <= 12; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: Math.round(a - dir * dist * i / 12), y }] }); await p.waitForTimeout(16) } await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] })
    await p.waitForTimeout(1200); const s = await state(p); rows.push(`${label} ${fmt(s)}`); if (!s.full || s.seg !== s.n) problems++; return s }
  await gesture(-Math.round(w * 3), 4000, 'fling-left-long')
  await gesture(-Math.round(w * 3), 6000, 'fling-left-long2')
  await gesture(-Math.round(w * 3), 6000, 'fling-left-long3')
  // from the end: one card at a time back to the start, recording every counter value
  const back = []
  for (let i = 0; i < 9; i++) { const s = await swipe(-1, 'swipe-back'); back.push(String(s.n).padStart(2, '0')) }
  await gesture(Math.round(w * 4), 6000, 'fling-right-long')
  await flick(1, 'flick-left'); await flick(1, 'flick-left'); await flick(1, 'flick-left'); await flick(1, 'flick-left')
  const fwd = []
  for (let i = 0; i < 9; i++) { const s = await swipe(1, 'swipe-fwd'); fwd.push(String(s.n).padStart(2, '0')) }
  await flick(-1, 'flick-right'); await flick(-1, 'flick-right')
  await gesture(Math.round(w * 6), 8000, 'fling-right-to-start')
  console.log(`${name} ${w}x${h}`, rows.filter(r => !/^swipe/.test(r)).join(' | '))
  console.log(`${name} ${w}x${h}`, 'one-card swipes back from the fling end:', back.join(' '), '| forward after flicks:', fwd.join(' '))
  await p.screenshot({ path: `${out}/${name}-${w}x${h}-end-${run}.png` })
  await ctx.close()
}
console.log('gestures where the counter card is not fully visible or the segment disagrees:', problems)
await b.close()
