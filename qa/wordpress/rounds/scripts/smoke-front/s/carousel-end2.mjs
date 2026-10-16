// Round 2, V04 steps as written: at 768x1024 and 844x390 (touch), tap segment 9; reload, focus the carousel and press
// ArrowRight nine times; reload, swipe left nine times. Record counter, next label and the aria-current segment.
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('carousel')
const run = process.argv[2] || 'r1'
const b = await launch()
const state = p => p.evaluate(() => {
  const pe = document.getElementById('panels')
  const cur = [...document.querySelectorAll('#segs button')].findIndex(x => x.getAttribute('aria-current') === 'true') + 1
  const vis = [...document.querySelectorAll('.panel')].map((x, i) => { const r = x.getBoundingClientRect(); return r.left >= pe.getBoundingClientRect().left - 1 && r.right <= innerWidth + 1 ? i + 1 : 0 }).filter(Boolean)
  return { wn: document.getElementById('wn').textContent, next: document.getElementById('wnext').textContent, currentSeg: cur, scrollLeft: Math.round(pe.scrollLeft), max: pe.scrollWidth - pe.clientWidth, fullyVisible: vis }
})
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h] of [[768, 1024], [844, 390]]) {
  const tag = `${name} ${w}x${h}`
  const fresh = async () => { const ctx = await newCtx(b, { w, h, phone: true }); const p = await ctx.newPage(); await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(700); await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(500); return [ctx, p] }
  // 1. tap segment 9
  let [ctx, p] = await fresh()
  await p.tap('#segs button:nth-child(9)'); await p.waitForTimeout(1300)
  console.log(tag, 'tap segment 9', JSON.stringify(await state(p)))
  await p.screenshot({ path: `${out}/${name}-${w}x${h}-seg9-${run}.png` })
  await ctx.close();
  // 2. ArrowRight x9 with focus on the carousel
  [ctx, p] = await fresh()
  await p.focus('#panels')
  const seq = []
  for (let i = 0; i < 9; i++) { await p.keyboard.press('ArrowRight'); await p.waitForTimeout(700); seq.push((await state(p)).wn.slice(0, 2)) }
  console.log(tag, 'ArrowRight x9 counter sequence', seq.join(' '), JSON.stringify(await state(p)))
  // and back one
  await p.keyboard.press('ArrowLeft'); await p.waitForTimeout(800)
  console.log(tag, 'then ArrowLeft', JSON.stringify(await state(p)))
  await ctx.close();
  // 3. swipe left nine times (CDP touch)
  [ctx, p] = await fresh()
  const cdp = await ctx.newCDPSession(p)
  const box = await p.locator('#panels').boundingBox(); const y = Math.round(box.y + 60)
  const x0 = Math.round(Math.min(w * 0.6, 300))
  const swipe = async () => { await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y }] }); for (let i = 1; i <= 12; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: Math.round(x0 - 200 * i / 12), y }] }); await p.waitForTimeout(16) } await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }) }
  const sw = []
  for (let i = 0; i < 9; i++) { await swipe(); await p.waitForTimeout(1100); const s = await state(p); sw.push(s.wn.slice(0, 2)) }
  console.log(tag, 'swipe x9 counter sequence', sw.join(' '), JSON.stringify(await state(p)))
  await p.screenshot({ path: `${out}/${name}-${w}x${h}-swipe9-${run}.png` })
  await ctx.close()
}
await b.close()
