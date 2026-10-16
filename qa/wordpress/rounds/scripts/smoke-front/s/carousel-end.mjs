// Round 2: the end of the phone carousel at tablet and landscape widths. Swipe one card at a time and record the
// counter; with video clips, check whether creator 8's clip ever plays when the visitor only swipes.
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('carousel')
const run = process.argv[2] || 'r1'
const b = await launch()
const state = p => p.evaluate(() => {
  const pe = document.getElementById('panels'), g = parseFloat(getComputedStyle(pe).paddingLeft), edge = pe.getBoundingClientRect().left + g
  const vids = [...document.querySelectorAll('.panel .clip')].map((v, i) => v.tagName === 'VIDEO' ? `${i + 1}:${v.paused ? 'P' : 'PLAY'}` : null).filter(Boolean).join(' ')
  const vis = [...document.querySelectorAll('.panel')].map((x, i) => { const r = x.getBoundingClientRect(); return r.left >= pe.getBoundingClientRect().left - 1 && r.right <= innerWidth + 1 ? i + 1 : 0 }).filter(Boolean)
  return { scrollLeft: Math.round(pe.scrollLeft), max: pe.scrollWidth - pe.clientWidth, wn: document.getElementById('wn').textContent, next: document.getElementById('wnext').textContent, fullyVisibleCards: vis, vids }
})
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h] of [[768, 1024], [844, 390], [390, 844]]) {
  const ctx = await newCtx(b, { w, h, phone: true })
  const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(800)
  const cdp = await ctx.newCDPSession(p)
  await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(600)
  const box = await p.locator('#panels').boundingBox(); const y = Math.round(box.y + 60)
  const swipe = async (x0, x1) => { await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y }] }); for (let i = 1; i <= 12; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: Math.round(x0 + (x1 - x0) * i / 12), y }] }); await p.waitForTimeout(16) } await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }) }
  const seen = []
  for (let i = 0; i < 10; i++) {
    const s = await state(p); seen.push(s.wn.slice(0, 2))
    if (i === 0 || i >= 5) console.log(name, `${w}x${h}`, 'swipe', i, JSON.stringify(s))
    await swipe(Math.round(Math.min(w * 0.6, 300)), Math.round(Math.min(w * 0.6, 300)) - 200); await p.waitForTimeout(1100)
  }
  console.log(name, `${w}x${h}`, 'counter values seen while swiping one card at a time:', [...new Set(seen)].join(' '))
  await p.screenshot({ path: `${out}/${name}-${w}x${h}-end-swipe-${run}.png` })
  await p.tap('#segs button:nth-child(8)'); await p.waitForTimeout(1300)
  console.log(name, `${w}x${h}`, 'tap segment 8', JSON.stringify(await state(p)))
  await ctx.close()
}
await b.close()
