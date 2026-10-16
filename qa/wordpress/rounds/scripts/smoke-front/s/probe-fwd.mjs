// Trace one forward flick from card 7 (or FROM) frame by frame: scrollLeft, counter, and the page's scrollTo calls.
import { launch, newCtx, WP, V2 } from './lib.mjs'
const [w, h] = (process.env.SIZE || '390x844').split('x').map(Number); const from = +(process.env.FROM || 7); const url = process.env.T === 'v2' ? V2 : WP
const kind = process.env.KIND || 'flick'
const b = await launch()
const ctx = await newCtx(b, { w, h, phone: true })
await ctx.addInitScript(() => { window.__calls = []; const o = Element.prototype.scrollTo; Element.prototype.scrollTo = function (...a) { if (this.id === 'panels') window.__calls.push([Math.round(performance.now() - (window.__t0 || 0)), Math.round(a[0].left), a[0].behavior]); return o.apply(this, a) } })
const p = await ctx.newPage(); await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(700)
await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(500)
await p.tap(`#segs button:nth-child(${from})`); await p.waitForTimeout(1300)
const cdp = await ctx.newCDPSession(p); const box = await p.locator('#panels').boundingBox(); const y = Math.round(box.y + 60)
await p.evaluate(() => { window.__calls = []; window.__trace = []; const pe = document.getElementById('panels'), wn = document.getElementById('wn'); const t0 = performance.now(); window.__t0 = t0; const tick = () => { window.__trace.push([Math.round(performance.now() - t0), Math.round(pe.scrollLeft), wn.textContent.slice(0, 2)]); if (performance.now() - t0 < 3000) requestAnimationFrame(tick) }; requestAnimationFrame(tick) })
const dir = +(process.env.DIR || 1)
const [d, steps, dt] = kind === 'flick' ? [Math.round(w * 0.85), 4, 8] : kind === 'fling' ? [Math.round(w * 0.9), 3, 5] : [Math.round(w * 0.85), 30, 25]
const x0 = dir > 0 ? Math.round(w * 0.92) : Math.round(w * 0.08)
await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y }] })
for (let i = 1; i <= steps; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: Math.round(x0 - dir * d * i / steps), y }] }); await p.waitForTimeout(dt) }
await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] })
await p.waitForTimeout(3200)
const r = await p.evaluate(() => ({ tr: window.__trace, calls: window.__calls }))
let last = ''; console.log(`${process.env.T || 'wp'} ${w}x${h} ${kind} dir ${dir} from ${from}`)
console.log('frames (t ms, scrollLeft, counter), only changes:', r.tr.filter((x, i, a) => i === 0 || x[1] !== a[i - 1][1] || x[2] !== a[i - 1][2]).map(x => x.join(':')).join(' '))
console.log('script scrollTo calls:', JSON.stringify(r.calls))
await b.close()
