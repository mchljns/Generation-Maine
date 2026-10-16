// Round 4, FR-R1 / VIS-N05: a gesture matrix on the phone carousel. For each size: one-card swipes forward through all
// nine and back; then from cards 7, 8 and 9 back gestures (one card, half screen, slow drag, flick, long fling), and from
// cards 1, 5, 6, 7 and 8 forward gestures (one card, flick, long fling). Every frame for up to 3.2 s after release:
// scrollLeft and the counter. The page's own scrollTo calls on #panels are logged, so a forward move made by the script
// (settle) is told apart from the browser's snap. The card on screen is worked out independently: the card whose snap
// position (left edge minus gutter minus its scroll margin, clamped to the track) is nearest scrollLeft.
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('gestx'); const run = process.argv[2] || 'r1'
const sizes = (process.env.SIZES || '320x568,390x844,414x896,430x932,768x1024,844x390').split(',').map(s => s.split('x').map(Number))
const targets = (process.env.TARGETS || 'wp,v2').split(',')
const b = await launch()
const hook = () => {
  window.__calls = []
  const o = Element.prototype.scrollTo
  Element.prototype.scrollTo = function (...a) { if (this.id === 'panels') window.__calls.push([Math.round(performance.now()), Math.round(typeof a[0] === 'object' ? a[0].left : a[0])]); return o.apply(this, a) }
}
const state = p => p.evaluate(() => {
  const pe = document.getElementById('panels'), c = pe.getBoundingClientRect(), g = parseFloat(getComputedStyle(pe).paddingLeft) || 0
  const max = pe.scrollWidth - pe.clientWidth, x = pe.scrollLeft
  const panels = [...document.querySelectorAll('.panel')]
  const snap = panels.map(el => Math.min(max, Math.max(0, el.getBoundingClientRect().left - c.left - g - (parseFloat(el.style.scrollMarginLeft) || 0) + x)))
  let card = 0, bd = Infinity; snap.forEach((s, k) => { const d = Math.abs(s - x); if (d < bd - 0.5) { bd = d; card = k } })
  const n = +document.getElementById('wn').textContent.slice(0, 2)
  const seg = [...document.querySelectorAll('#segs button')].findIndex(e => e.getAttribute('aria-current') === 'true') + 1
  const r = panels[n - 1].getBoundingClientRect()
  return { n, seg, card: card + 1, off: Math.round(bd), x: Math.round(x), max, full: r.left >= c.left - 1 && r.right <= innerWidth + 1, snap: snap.map(Math.round) }
})
let total = 0, mism = 0, scriptFwdBack = 0, bigFwd = 0, skips = 0
const summary = []
for (const name of targets) for (const [w, h] of sizes) {
  const url = name === 'wp' ? WP : V2
  const ctx = await newCtx(b, { w, h, phone: true }); await ctx.addInitScript(hook); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(700)
  await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(500)
  const cdp = await ctx.newCDPSession(p)
  const box = await p.locator('#panels').boundingBox(); const y = Math.round(box.y + 60)
  const s0 = await state(p)
  console.log(`${name} ${w}x${h} snap positions ${s0.snap.join(',')} max ${s0.max}`)
  const drag = async (from, dx, steps, dt) => {
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: from, y }] })
    for (let i = 1; i <= steps; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: Math.round(from + dx * i / steps), y }] }); await p.waitForTimeout(dt) }
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] })
  }
  const traced = async (fn) => {
    await p.evaluate(() => { window.__calls = []; window.__trace = []; const pe = document.getElementById('panels'), wn = document.getElementById('wn'); const t0 = performance.now(); window.__t0 = t0; const tick = () => { window.__trace.push([Math.round(performance.now() - t0), Math.round(pe.scrollLeft), wn.textContent.slice(0, 2)]); if (performance.now() - t0 < 4500) requestAnimationFrame(tick) }; requestAnimationFrame(tick) })
    await fn()
    // wait until still for 700 ms (or 3.2 s)
    let last = -1, still = 0
    for (let i = 0; i < 64 && still < 10; i++) { await p.waitForTimeout(50); const x = await p.evaluate(() => Math.round(document.getElementById('panels').scrollLeft)); still = x === last ? still + 1 : 0; last = x }
    await p.waitForTimeout(300)
    return p.evaluate(() => ({ tr: window.__trace, calls: window.__calls.map(([t, l]) => [Math.round(t - window.__t0), l]) }))
  }
  const check = (s, label) => { total++; const bad = s.n !== s.card || s.seg !== s.n || !s.full; if (bad) mism++; return bad ? ` MISMATCH(counter ${s.n} seg ${s.seg} card ${s.card} off ${s.off}${s.full ? '' : ' not-fully-visible'})` : '' }
  // A. one-card swipes through all nine and back
  const dist = Math.round(Math.min(200, w * 0.5)), x0 = Math.round(Math.min(w * 0.6, 300) + (w < 500 ? w * 0.2 : 0))
  const fw = [], bk = []
  for (let i = 0; i < 9; i++) { await drag(x0, -dist, 12, 16); await p.waitForTimeout(1100); const s = await state(p); fw.push(String(s.n).padStart(2, '0') + check(s)) }
  for (let i = 0; i < 9; i++) { await drag(x0 - dist, dist, 12, 16); await p.waitForTimeout(1100); const s = await state(p); bk.push(String(s.n).padStart(2, '0') + check(s)) }
  const want = '02 03 04 05 06 07 08 09 09', wantB = '08 07 06 05 04 03 02 01 01'
  const okA = fw.join(' ') === want && bk.join(' ') === wantB; if (!okA) skips++
  console.log(`${name} ${w}x${h} ONE-CARD ${okA ? 'OK' : 'SKIP/MISMATCH'} forward ${fw.join(' ')} | back ${bk.join(' ')}`)
  summary.push(`${name} ${w}x${h} one-card ${okA ? 'OK' : 'BAD'}`)
  // B/C. gestures from a start card
  const kinds = {
    onecard: [dist, 12, 16], half: [Math.round(w * 0.5), 12, 16], slowdrag: [Math.round(w * 0.85), 30, 25], flick: [Math.round(w * 0.85), 4, 8], fling: [Math.round(w * 0.9), 3, 5],
  }
  const plan = []
  for (const from of [9, 8, 7]) for (const k of ['onecard', 'half', 'slowdrag', 'flick', 'fling']) plan.push([from, -1, k])
  for (const from of [1, 5, 6, 7, 8]) for (const k of ['onecard', 'half', 'slowdrag', 'flick', 'fling']) plan.push([from, 1, k])
  for (const [from, dirn, kind] of plan) {
    await p.tap(`#segs button:nth-child(${from})`); await p.waitForTimeout(1100)
    const st = await state(p)
    const [d, steps, dt] = kinds[kind]
    const start = dirn < 0 ? Math.round(w * 0.08) : Math.round(w * 0.92)
    const { tr, calls } = await traced(() => drag(start, dirn < 0 ? d : -d, steps, dt))
    const s = await state(p)
    const xs = tr.map(r => r[1]); const ext = dirn < 0 ? Math.min(...xs) : Math.max(...xs)
    const after = dirn < 0 ? s.x - ext : ext - s.x // movement against the gesture after its furthest point
    const seq = tr.map(r => r[2]).filter((v, i, a) => i === 0 || v !== a[i - 1])
    const scriptAgainst = calls.filter(([t, l]) => dirn < 0 ? l > ext + 2 : l < ext - 2)
    if (dirn < 0 && scriptAgainst.length) scriptFwdBack++
    if (after > 150) bigFwd++
    const m = check(s)
    console.log(`${name} ${w}x${h} ${dirn < 0 ? 'BACK' : 'FWD '} ${kind.padEnd(8)} from ${String(st.n).padStart(2, '0')}@${st.x}: furthest @${ext}, end ${String(s.n).padStart(2, '0')}@${s.x} (card ${s.card}); against-gesture ${after}px${after > 5 ? (scriptAgainst.length ? ' BY SCRIPT ' + JSON.stringify(scriptAgainst) : ' (browser snap)') : ''}; script calls ${JSON.stringify(calls)}; counter ${seq.join(' ')}${m}`)
  }
  await p.screenshot({ path: `${out}/${name}-${w}x${h}-end-${run}.png` })
  await ctx.close()
}
console.log(`TOTAL checks ${total}, counter/card mismatches ${mism}, back gestures moved forward by the script ${scriptFwdBack}, moves >150px against a gesture ${bigFwd}, one-card runs with a skip ${skips}`)
console.log(summary.join('\n'))
await b.close()
