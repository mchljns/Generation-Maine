import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('carousel')
const run = process.argv[2] || 'r1'
const b = await launch()
const state = p => p.evaluate(() => {
  const pe = document.getElementById('panels'), g = parseFloat(getComputedStyle(pe).paddingLeft)
  const edge = pe.getBoundingClientRect().left + g
  const offs = [...document.querySelectorAll('.panel')].map(x => Math.round(x.getBoundingClientRect().left - edge))
  const snapped = offs.some(o => Math.abs(o) <= 1)
  const loaded = [...document.querySelectorAll('.panel .clip')].map((c, i) => c.getAttribute('src') ? i : -1).filter(i => i >= 0)
  const segOn = [...document.querySelectorAll('#segs button')].map((c, i) => c.getAttribute('aria-current') === 'true' ? i : -1).filter(i => i >= 0)
  return { scrollLeft: Math.round(pe.scrollLeft), snapped, nearestOff: offs.reduce((a, o) => Math.abs(o) < Math.abs(a) ? o : a, 9999), wn: document.getElementById('wn').textContent, next: document.getElementById('wnext').textContent, segOn, loaded, tint: document.getElementById('stories').style.backgroundColor, on: [...document.querySelectorAll('.panel')].findIndex(x => x.classList.contains('on')) }
})
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h] of [[390, 844], [320, 568], [844, 390], [768, 1024]]) {
  const ctx = await newCtx(b, { w, h })
  const p = await ctx.newPage()
  const gifs = []
  p.on('request', r => { const m = r.url().match(/creator-(\d)\.gif/); if (m) gifs.push(+m[1]) })
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(800)
  const cdp = await ctx.newCDPSession(p)
  await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' }))
  await p.waitForTimeout(600)
  console.log(name, w, 'start', JSON.stringify(await state(p)), 'gifs', JSON.stringify(gifs))
  const box = await p.locator('#panels').boundingBox()
  const y = Math.round(box.y + 80)
  const swipe = async (x0, x1) => { await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y }] }); for (let i = 1; i <= 12; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: Math.round(x0 + (x1 - x0) * i / 12), y }] }); await p.waitForTimeout(16) } await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }) }
  for (let i = 0; i < 9; i++) {
    await swipe(Math.round(w * 0.8), Math.round(w * 0.3))
    await p.waitForTimeout(1000)
    console.log(name, w, 'swipe left', i + 1, JSON.stringify(await state(p)), 'gifs so far', gifs.length)
  }
  await p.screenshot({ path: `${out}/${name}-${w}-after-swipes-${run}.png` })
  await swipe(Math.round(w * 0.3), Math.round(w * 0.8))
  await p.waitForTimeout(900)
  console.log(name, w, 'swipe right', JSON.stringify(await state(p)))
  // segment taps
  for (const k of [9, 5, 1]) {
    await p.tap(`#segs button:nth-child(${k})`); await p.waitForTimeout(1200)
    console.log(name, w, 'tap seg', k, JSON.stringify(await state(p)))
  }
  // arrow keys
  await p.focus('#panels')
  for (const key of ['ArrowRight', 'ArrowRight', 'ArrowLeft']) { await p.keyboard.press(key); await p.waitForTimeout(900); console.log(name, w, key, JSON.stringify(await state(p))) }
  // to the end with arrow keys, then one more
  for (let i = 0; i < 9; i++) { await p.keyboard.press('ArrowRight'); await p.waitForTimeout(500) }
  console.log(name, w, 'ArrowRight x9', JSON.stringify(await state(p)))
  console.log(name, w, 'gif requests', JSON.stringify(gifs), 'count', gifs.length)
  await p.screenshot({ path: `${out}/${name}-${w}-end-${run}.png` })
  await ctx.close()
}
await b.close()
