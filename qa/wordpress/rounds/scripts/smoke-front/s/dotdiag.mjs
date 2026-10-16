// Diagnosis for the word-joiner dot: at given widths, is the dot alone on a line (a) as served, (b) with the word joiner
// taken out (the round 3 markup), (c) with the last letter and the dot wrapped in a white-space:nowrap span (a possible fix).
// Client-side markup changes only, for comparison. Also screenshots of (a). usage: K=key WS=... [TARGET=v2 INJECT=html] [PHONE=1 DSF=2]
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('dotdiag'); const run = process.argv[2] || 'r1'
const key = process.env.K || 'url', widths = (process.env.WS || '414').split(',').map(Number), target = process.env.TARGET || 'wp'
const dsf = +(process.env.DSF || 1), phone = !!process.env.PHONE
const b = await launch()
for (const w of widths) {
  const ctx = await newCtx(b, { w, h: phone ? 896 : 900, phone, dsf }); const p = await ctx.newPage()
  await p.goto(target === 'v2' ? V2 : `${WP}?gmh=${key}`, { waitUntil: 'networkidle' })
  if (process.env.INJECT) await p.evaluate(h => { document.querySelector('.hero h1').innerHTML = h }, process.env.INJECT)
  await p.waitForTimeout(1500)
  const alone = () => p.evaluate(() => { const h1 = document.querySelector('.hero h1'), d = h1.querySelector('.d').getBoundingClientRect(); let last = null
    for (const s of h1.querySelectorAll('.here')) { const tw = document.createTreeWalker(s, NodeFilter.SHOW_TEXT); for (let n; (n = tw.nextNode());) for (let i = 0; i < n.data.length; i++) { if (/[\s⁠]/.test(n.data[i])) continue; const rg = document.createRange(); rg.setStart(n, i); rg.setEnd(n, i + 1); const r = rg.getClientRects()[0]; if (r) last = r } }
    return { alone: d.top >= last.bottom - 1, h1h: Math.round(h1.getBoundingClientRect().height), html: h1.innerHTML.replace(/⁠/g, '&#8288;').replace(/<i class="d pulse" aria-hidden="true"><\/i>/, '•').slice(-80) } })
  const a = await alone()
  const box = await p.locator('.hero h1').boundingBox()
  await p.screenshot({ path: `${out}/${target}-${key}-${w}${phone ? '-phone' : ''}-dsf${dsf}-${run}.png`, clip: { x: 0, y: Math.max(0, box.y - 16), width: w, height: box.height + 32 } })
  await p.evaluate(() => { const h1 = document.querySelector('.hero h1'); const tw = document.createTreeWalker(h1, NodeFilter.SHOW_TEXT); for (let n; (n = tw.nextNode());) n.data = n.data.replace(/⁠/g, '') })
  const bb = await alone()
  await p.evaluate(() => { const d = document.querySelector('.hero h1 .d'); let t = d.previousSibling; while (t && t.nodeType === 3 && !t.data.length) t = t.previousSibling; if (t && t.nodeType === 3) { const last = t.data.slice(-1); t.data = t.data.slice(0, -1); const s = document.createElement('span'); s.style.whiteSpace = 'nowrap'; s.textContent = last; d.before(s); s.appendChild(d) } })
  const c = await alone()
  console.log(`${target} ${key} ${w}${phone ? ' phone' : ''} dsf${dsf}: as served alone=${a.alone} (h1 ${a.h1h}px) | no word joiner alone=${bb.alone} | last letter+dot nowrap alone=${c.alone} (h1 ${c.h1h}px) | ${a.html}`)
  await ctx.close()
}
await b.close()
