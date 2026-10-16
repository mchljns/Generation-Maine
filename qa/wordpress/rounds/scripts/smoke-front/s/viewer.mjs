import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('viewer')
const run = process.argv[2] || 'r1'
const b = await launch()
const st = p => p.evaluate(() => {
  const v = document.getElementById('viewer'), a = document.activeElement
  const vt = document.getElementById('vtrack')
  return { hidden: v.hidden, vopen: document.documentElement.classList.contains('vopen'), htmlOverflow: getComputedStyle(document.documentElement).overflow, vn: document.getElementById('vn').textContent, vtScroll: Math.round(vt.scrollLeft), active: a ? (a.tagName + (a.id ? '#' + a.id : '') + ' ' + (a.getAttribute('aria-label') || '')).trim() : null, scrollY: Math.round(scrollY), wn: document.getElementById('wn').textContent, histLen: history.length, loaded: [...document.querySelectorAll('#vtrack .clip')].map((c, i) => c.getAttribute('src') ? i : -1).filter(i => i >= 0) }
})
for (const [name, url] of [['wp', WP], ['v2', V2]]) {
  const ctx = await newCtx(b, { w: 390, h: 844 })
  const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(800)
  const cdp = await ctx.newCDPSession(p)
  const swipe = async (x0, x1, y) => { await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y }] }); for (let i = 1; i <= 12; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: Math.round(x0 + (x1 - x0) * i / 12), y }] }); await p.waitForTimeout(16) } await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }) }
  const L = (k, v) => console.log(name, k, JSON.stringify(v))
  // go to story 3 via swipes so a non-first clip is opened
  await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(400)
  const pb = await p.locator('#panels').boundingBox()
  await swipe(312, 117, pb.y + 80); await p.waitForTimeout(900); await swipe(312, 117, pb.y + 80); await p.waitForTimeout(900)
  await p.evaluate(() => window.scrollBy({ top: -30, behavior: 'instant' })); await p.waitForTimeout(300)
  const before = await st(p); L('before open', before)
  // 1. open by tap, close by X
  await p.tap('#story-3 .pv'); await p.waitForTimeout(700)
  const o1 = await st(p); L('open by tap', o1)
  await p.screenshot({ path: `${out}/${name}-open-${run}.png` })
  const fr = await p.evaluate(() => { const r = document.querySelector('#vtrack .slide:nth-child(3) .fr').getBoundingClientRect(); const c = document.querySelector('#vtrack .slide:nth-child(3) .clip'); return { w: Math.round(r.width), h: Math.round(r.height), ratio: +(r.width / r.height).toFixed(3), clipFit: getComputedStyle(c).objectFit } })
  L('frame', fr)
  // try wheel scroll of page while open (scroll lock)
  await p.mouse.wheel(0, 600); await p.waitForTimeout(500)
  L('wheel while open scrollY', (await st(p)).scrollY)
  // swipe between creators
  const vb = await p.locator('#vtrack').boundingBox()
  await swipe(330, 60, vb.y + vb.height / 2); await p.waitForTimeout(900)
  L('swipe left in viewer', await st(p))
  await swipe(330, 60, vb.y + vb.height / 2); await p.waitForTimeout(900)
  L('swipe left again', await st(p))
  await swipe(60, 330, vb.y + vb.height / 2); await p.waitForTimeout(900)
  L('swipe right', await st(p))
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(900)
  L('ArrowRight in viewer', await st(p))
  await p.tap('#vclose'); await p.waitForTimeout(800)
  L('close by X', await st(p))
  await p.screenshot({ path: `${out}/${name}-after-x-${run}.png` })
  // 2. open, close by Escape
  const y2 = (await st(p)).scrollY
  await p.tap('.panel.on .pv'); await p.waitForTimeout(700)
  await p.keyboard.press('Escape'); await p.waitForTimeout(800)
  L('close by Escape (y before ' + y2 + ')', await st(p))
  // 3. backdrop tap: tap outside frame within viewer
  await p.tap('.panel.on .pv'); await p.waitForTimeout(700)
  const free = await p.evaluate(() => { const v = document.getElementById('viewer').getBoundingClientRect(); const pts = []; for (let y = v.top + 5; y < v.bottom; y += 10) for (let x = 5; x < v.width; x += 10) { const e = document.elementFromPoint(x, y); if (e && !e.closest('.fr, .vbar, .cap')) { pts.push([x, y, e.className]); } } return pts.slice(0, 3).concat(pts.length ? [['count', pts.length]] : []) })
  L('backdrop points', free)
  if (free.length && free[0][0] !== 'count') { await p.tap(`#viewer`, { position: { x: free[0][0], y: free[0][1] } }).catch(e => L('tap err', e.message)); await p.waitForTimeout(800) }
  L('close by backdrop', await st(p))
  // 4. back button
  const y4 = (await st(p)).scrollY
  await p.tap('.panel.on .pv'); await p.waitForTimeout(700)
  L('open again', await st(p))
  await p.goBack(); await p.waitForTimeout(900)
  L('close by back (y before ' + y4 + ')', await st(p))
  L('url after back', p.url())
  // 5. keyboard open via Enter on .pv and focus return
  await p.focus('.panel.on .pv'); await p.keyboard.press('Enter'); await p.waitForTimeout(700)
  L('kbd open', await st(p))
  const tabs = []
  for (let i = 0; i < 3; i++) { await p.keyboard.press('Tab'); await p.waitForTimeout(80); tabs.push((await st(p)).active) }
  L('tab x3 inside viewer', tabs)
  await p.keyboard.press('Escape'); await p.waitForTimeout(800)
  L('kbd escape', await st(p))
  await ctx.close()
}
await b.close()
