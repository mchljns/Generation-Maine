// fix4 N2: the counter while the page itself scrolls the track: a tap on segment 9 from card 1 and back to 1, a tap on
// segment 5, ArrowRight and ArrowLeft with focus on the track, then a Tab from the track into the cards' buttons right after a
// tap (the counter must follow the card the browser scrolls to). Every frame: scrollLeft and the counter.
// usage: node glide.mjs ; env TARGETS, SIZES, REDUCED=1
import { launch, newCtx, WP, V2 } from './lib.mjs'
const targets = (process.env.TARGETS || 'wp,v2').split(',')
const sizes = (process.env.SIZES || '390x844,768x1024').split(',').map(s => s.split('x').map(Number))
const b = await launch()
let bad = 0
for (const name of targets) for (const [w, h] of sizes) {
  const ctx = await newCtx(b, { w, h, phone: true, reduced: !!process.env.REDUCED }); const p = await ctx.newPage()
  await p.goto(name === 'wp' ? WP : V2, { waitUntil: 'networkidle' }); await p.waitForTimeout(700)
  await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(500)
  const traced = async (fn, ms = 1600) => {
    await p.evaluate(ms => { window.__tr = []; const pe = document.getElementById('panels'), wn = document.getElementById('wn'), t0 = performance.now(); const tick = () => { window.__tr.push([Math.round(performance.now() - t0), Math.round(pe.scrollLeft), wn.textContent.slice(0, 2)]); if (performance.now() - t0 < ms) requestAnimationFrame(tick) }; requestAnimationFrame(tick) }, ms)
    await fn(); await p.waitForTimeout(ms + 200)
    const tr = await p.evaluate(() => window.__tr)
    const seq = tr.map(r => r[2]).filter((v, i, a) => i === 0 || v !== a[i - 1]), xs = tr.map(r => r[1])
    const moving = tr.filter((r, i) => i && r[1] !== tr[i - 1][1]), dur = moving.length ? moving[moving.length - 1][0] - moving[0][0] : 0
    return { seq, from: xs[0], to: xs[xs.length - 1], dur }
  }
  const state = () => p.evaluate(() => { const pe = document.getElementById('panels'), c = pe.getBoundingClientRect(), g = parseFloat(getComputedStyle(pe).paddingLeft) || 0, x = pe.scrollLeft, max = pe.scrollWidth - pe.clientWidth
    const snap = [...document.querySelectorAll('.panel')].map(el => Math.min(max, Math.max(0, el.getBoundingClientRect().left - c.left - g - (parseFloat(el.style.scrollMarginLeft) || 0) + x)))
    let card = 0, bd = Infinity; snap.forEach((s, k) => { const d = Math.abs(s - x); if (d < bd - 0.5) { bd = d; card = k } })
    return { n: +document.getElementById('wn').textContent.slice(0, 2), seg: [...document.querySelectorAll('#segs button')].findIndex(e => e.getAttribute('aria-current') === 'true') + 1, card: card + 1, act: document.activeElement.className || document.activeElement.id } })
  const line = async (label, r, want) => { const s = await state(); const ok = r.seq[r.seq.length - 1] === String(want).padStart(2, '0') && s.n === want && s.seg === want && s.card === want && (r.seq.length <= 2); if (!ok) bad++
    console.log(`${name} ${w}x${h}${process.env.REDUCED ? ' reduced' : ''} ${label}: x ${r.from} -> ${r.to} in ${r.dur} ms, counter ${r.seq.join(' ')}; now counter ${s.n} seg ${s.seg} card ${s.card}${ok ? '' : ' <<< BAD'}`) }
  await line('tap segment 9', await traced(() => p.tap('#segs button:nth-child(9)')), 9)
  await line('tap segment 1', await traced(() => p.tap('#segs button:nth-child(1)')), 1)
  await line('tap segment 5', await traced(() => p.tap('#segs button:nth-child(5)')), 5)
  await p.focus('#panels')
  await line('ArrowRight', await traced(() => p.keyboard.press('ArrowRight'), 1000), 6)
  await line('ArrowLeft', await traced(() => p.keyboard.press('ArrowLeft'), 1000), 5)
  // a tap on segment 2, then at once Tab from the track into the cards: the browser scrolls the focused card's button into view
  await p.tap('#segs button:nth-child(8)'); await p.waitForTimeout(1300)
  await p.focus('#panels')
  const r = await traced(async () => { await p.keyboard.press('ArrowLeft'); await p.waitForTimeout(60); await p.keyboard.press('Tab') }, 1600)
  const s = await state()
  console.log(`${name} ${w}x${h} ArrowLeft then Tab at once: x ${r.from} -> ${r.to}, counter ${r.seq.join(' ')}; now counter ${s.n} card ${s.card} focus ${s.act}${s.n === s.card ? '' : ' <<< BAD (counter is not the card on screen)'}`)
  if (s.n !== s.card) bad++
  await ctx.close()
}
console.log(`TOTAL bad ${bad}`)
await b.close()
