// Round 4, word-joiner dot and ED-R5: for each headline variant (served by WordPress through gm_mark_here via ?gmh=key,
// or the v2 page as served), sweep the viewport width from 320 to 1440 in 2px steps and record, at each width: whether the
// dot sits on a line without the letter before it (alone), sideways page overflow, the h1 running past the hero or past its
// column, and whether the gold word is split across lines. usage: node dotsweep.mjs <run> ; env KEYS, TARGET (wp|v2), STEP,
// FROM, TO, DSF
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
import { writeFileSync } from 'node:fs'
const out = dir('dotsweep'); const run = process.argv[2] || 'r1'
const target = process.env.TARGET || 'wp'
const keys = (process.env.KEYS || 'shipped').split(',')
const step = +(process.env.STEP || 2), from = +(process.env.FROM || 320), to = +(process.env.TO || 1440), dsf = +(process.env.DSF || 1)
const b = await launch()
const all = {}
for (const key of keys) {
  const url = target === 'v2' ? V2 : `${WP}?gmh=${key}`
  const ctx = await newCtx(b, { w: from, h: 900, phone: false, dsf }); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(1500)
  // fix4: on v2, any key but 'shipped' puts the headline WordPress renders for that key into the v2 page's h1
  if (target === 'v2' && key !== 'shipped') { const src = await (await fetch(`${WP}?gmh=${key}`)).text(); const m = src.match(/<h1 class="wp-block-heading rise gm-here">([\s\S]*?)<\/h1>/); if (!m) throw new Error('no h1 for ' + key); await p.evaluate(h => { document.querySelector('.hero h1').innerHTML = h }, m[1]); await p.waitForTimeout(300) }
  const html = await p.evaluate(() => document.querySelector('.hero h1').innerHTML)
  const rows = []; const alone = [], over = [], past = [], split = new Set()
  for (let w = from; w <= to; w += step) {
    await p.setViewportSize({ width: w, height: 900 })
    await p.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))))
    const r = await p.evaluate(() => {
      const h1 = document.querySelector('.hero h1'), dot = h1.querySelector('.d'), fs = parseFloat(getComputedStyle(h1).fontSize)
      const heroR = document.querySelector('.hero').getBoundingClientRect(), colR = h1.parentElement.getBoundingClientRect(), hr = h1.getBoundingClientRect()
      const overflow = document.documentElement.scrollWidth - document.documentElement.clientWidth
      // every visible character's line (top) inside the gold word(s); the last letter before the dot
      const here = [...h1.querySelectorAll('.here')]
      const chars = []
      for (const s of here) { const tw = document.createTreeWalker(s, NodeFilter.SHOW_TEXT); for (let n; (n = tw.nextNode());) for (let i = 0; i < n.data.length; i++) { const ch = n.data[i]; if (ch === '⁠' || /\s/.test(ch)) continue; const rg = document.createRange(); rg.setStart(n, i); rg.setEnd(n, i + 1); const rc = rg.getClientRects()[0]; if (rc) chars.push([ch, Math.round(rc.top), Math.round(rc.right), Math.round(rc.bottom)]) } }
      const lines = [...new Set(chars.map(c => c[1]))]
      const res = { fs, overflow, h1Right: Math.round(hr.right), heroRight: Math.round(heroR.right), colRight: Math.round(colR.right), wordLines: lines.length }
      if (dot) { const dr = dot.getBoundingClientRect(), last = chars[chars.length - 1]; res.dot = [Math.round(dr.top), Math.round(dr.left), Math.round(dr.right)]; res.last = last; res.alone = !!last && dr.top >= last[3] - 1; res.dotPast = Math.round(dr.right - colR.right) }
      // the lines of the whole headline, as text
      const lt = []; const tw = document.createTreeWalker(h1, NodeFilter.SHOW_TEXT); let cur = null, top = null
      for (let n; (n = tw.nextNode());) for (let i = 0; i < n.data.length; i++) { const ch = n.data[i]; if (ch === '⁠') continue; const rg = document.createRange(); rg.setStart(n, i); rg.setEnd(n, i + 1); const rc = rg.getClientRects()[0]; if (!rc || rc.width === 0 && /\s/.test(ch)) { if (cur !== null) cur += ch; continue } if (top === null || Math.abs(rc.top - top) > fs * 0.5) { if (cur !== null) lt.push(cur.trim()); cur = ''; top = rc.top } cur += ch }
      if (cur !== null) lt.push(cur.trim())
      if (dot && res.alone) lt.push('•'); else if (dot && lt.length) lt[lt.length - 1] += '•'
      res.lines = lt
      return res
    })
    rows.push([w, r])
    if (r.alone) alone.push(w)
    if (r.overflow > 0) over.push(`${w}:${r.overflow}`)
    if (r.h1Right > r.heroRight || r.h1Right > r.colRight + 1 || (r.dotPast || 0) > 1) past.push(`${w}:h1 ${r.h1Right - r.colRight}/dot ${r.dotPast}`)
    if (r.wordLines > 1) split.add(w)
  }
  // line patterns: compress consecutive widths with the same lines
  const pats = []; for (const [w, r] of rows) { const k = r.lines.join(' | '); if (!pats.length || pats[pats.length - 1].k !== k) pats.push({ k, a: w, z: w }); else pats[pats.length - 1].z = w }
  all[key] = { html, alone, over, past, split: [...split], pats }
  console.log(`== ${target} ${key} (DSF ${dsf}) h1: ${html}`)
  console.log(`   dot alone at ${alone.length} widths${alone.length ? ': ' + alone.join(',') : ''}; page overflow at ${over.length}${over.length ? ': ' + over.slice(0, 20).join(',') : ''}; h1 or dot past its column at ${past.length}${past.length ? ': ' + past.slice(0, 12).join(',') : ''}; gold word split across lines at ${split.size} widths${split.size ? ' (' + [...split][0] + '..' + [...split][split.size - 1] + ')' : ''}`)
  for (const t of pats) console.log(`   ${String(t.a).padStart(4)}-${String(t.z).padEnd(4)} ${t.k}`)
  await ctx.close()
}
writeFileSync(`${out}/${target}-${keys.length > 3 ? 'many' : keys.join('_')}-dsf${dsf}-${run}.json`, JSON.stringify(all, null, 1))
await b.close()
