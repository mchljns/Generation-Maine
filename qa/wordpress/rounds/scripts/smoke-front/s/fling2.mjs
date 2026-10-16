// Round 3, VIS-N05 variations 2: fast flicks of several sizes from card 1 and from the middle, a slow long drag, and an
// overshooting drag inside the end stretch. After each: the counter, the card at the gutter / resting place, and whether
// the counter's card is fully on screen. Also every counter value shown while the track moved (sampled each frame).
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('fling'); const run = process.argv[2] || 'r1'
const b = await launch()
const sizes = (process.env.SIZES || '320x568,390x844,768x1024,844x390').split(',').map(s => s.split('x').map(Number))
const state = p => p.evaluate(() => {
  const pe = document.getElementById('panels'), c = pe.getBoundingClientRect(), panels = [...document.querySelectorAll('.panel')]
  const n = +document.getElementById('wn').textContent.slice(0, 2)
  const seg = [...document.querySelectorAll('#segs button')].findIndex(x => x.getAttribute('aria-current') === 'true') + 1
  const r = panels[n - 1].getBoundingClientRect(), full = r.left >= c.left - 1 && r.right <= innerWidth + 1
  const vids = window.__seen ? [...new Set(window.__seen)].join(',') : ''
  return { n, seg, x: Math.round(pe.scrollLeft), full, seen: vids }
})
const fmt = s => `${String(s.n).padStart(2, '0')}${s.seg !== s.n ? '(seg' + s.seg + ')' : ''}@${s.x}${s.full ? '' : '[NOT FULLY VISIBLE]'} seen[${s.seen}]`
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h] of sizes) {
  const ctx = await newCtx(b, { w, h, phone: true }); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(700)
  await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(500)
  await p.evaluate(() => { window.__seen = []; const wn = document.getElementById('wn'); new MutationObserver(() => window.__seen.push(wn.textContent.slice(0, 2))).observe(wn, { childList: true, characterData: true, subtree: true }) })
  const cdp = await ctx.newCDPSession(p)
  const box = await p.locator('#panels').boundingBox(); const y = Math.round(box.y + 60)
  const reset = () => p.evaluate(() => { window.__seen = [] })
  const touch = async (x0, dx, steps, dt) => { await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y }] }); for (let i = 1; i <= steps; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: Math.round(x0 + dx * i / steps), y }] }); await p.waitForTimeout(dt) } await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); await p.waitForTimeout(2000) }
  const rows = []
  const goSeg = async k => { await p.tap(`#segs button:nth-child(${k})`); await p.waitForTimeout(1200); await reset() }
  // big fast flick from 1
  await goSeg(1); await touch(Math.round(w * 0.9), -Math.round(w * 0.8), 4, 8); rows.push('bigflick-from-01 ' + fmt(await state(p)))
  await goSeg(1); await touch(Math.round(w * 0.6), -Math.round(w * 0.3), 3, 8); rows.push('smallflick-from-01 ' + fmt(await state(p)))
  await goSeg(4); await touch(Math.round(w * 0.9), -Math.round(w * 0.8), 4, 8); rows.push('bigflick-from-04 ' + fmt(await state(p)))
  // slow long drag of two and a half cards from 3
  await goSeg(3); const pitch = await p.evaluate(() => { const ps = document.querySelectorAll('.panel'); return ps[1].getBoundingClientRect().left - ps[0].getBoundingClientRect().left })
  await touch(Math.round(w * 0.95), -Math.round(Math.min(w * 0.9, pitch * 2.5)), 40, 30); rows.push(`slowdrag-${Math.round(Math.min(w * 0.9, pitch * 2.5))}px-from-03 ` + fmt(await state(p)))
  // in the end stretch: drag most of the screen, slowly, from 6 and from 7
  for (const k of [6, 7, 8]) { await goSeg(k); await touch(Math.round(w * 0.95), -Math.round(w * 0.85), 30, 25); rows.push(`longdrag-from-0${k} ` + fmt(await state(p))) }
  // back: big fast flick from 9
  await goSeg(9); await touch(Math.round(w * 0.1), Math.round(w * 0.8), 4, 8); rows.push('bigflick-back-from-09 ' + fmt(await state(p)))
  await goSeg(9); await touch(Math.round(w * 0.05), Math.round(w * 0.85), 30, 25); rows.push('longdrag-back-from-09 ' + fmt(await state(p)))
  console.log(`${name} ${w}x${h}`, rows.join(' | '))
  await ctx.close()
}
await b.close()
