// Round 3, E01: the roster layout on the front end. For each tile: number, name and town, their client and scroll widths,
// display, white-space, text-shadow and overflow; screenshots. URL is the page holding a Roster Creators block.
import { launch, newCtx, dir } from './lib.mjs'
const out = dir('roster'); const run = process.argv[2] || 'r1'
const url = process.env.URL; const tag = process.env.TAG || 'wp'
const b = await launch()
for (const [w, h] of [[1440, 900], [1024, 768], [768, 1024], [844, 390], [700, 900], [390, 844], [320, 568]]) {
  const ctx = await newCtx(b, { w, h, phone: w <= 900 }); const p = await ctx.newPage()
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()) })
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(600)
  const r = await p.evaluate(() => {
    const tiles = [...document.querySelectorAll('.roster .tile')]
    const clipped = []; const shadows = new Set(); const disp = new Set(); const rows = []
    for (const t of tiles) {
      const spans = [...t.querySelectorAll('.who span, .who b, .n, .town')]
      for (const s of spans) { const cs = getComputedStyle(s); shadows.add(cs.textShadow); disp.add(s.className + ':' + cs.display + '/' + cs.whiteSpace + '/' + cs.overflow)
        if (s.scrollWidth > s.clientWidth + 1 || s.scrollHeight > s.clientHeight + 1 && cs.overflow === 'hidden') clipped.push(`${s.className || s.tagName}:"${s.textContent}" ${s.clientWidth}/${s.scrollWidth}`) }
      const town = t.querySelector('.town'); const tr = town ? town.getBoundingClientRect() : null, rr = t.getBoundingClientRect()
      // does any word break mid-word? compare rendered lines: get the text of each line via range rects
      let midword = false
      if (town) { const range = document.createRange(); const tn = town.firstChild; if (tn && tn.nodeType === 3) { let lastTop = null, lineStart = 0; for (let i = 0; i < tn.length; i++) { range.setStart(tn, i); range.setEnd(tn, i + 1); const rc = range.getClientRects()[0]; if (!rc) continue; if (lastTop !== null && Math.abs(rc.top - lastTop) > 2) { const prev = tn.data[i - 1], cur = tn.data[i]; if (/\w/.test(prev) && /\w/.test(cur)) midword = true } lastTop = rc.top } } }
      rows.push({ text: t.innerText.replace(/\n/g, ' | '), townW: tr ? Math.round(tr.width) : 0, townH: tr ? Math.round(tr.height) : 0, tileW: Math.round(rr.width), outside: tr ? (tr.right > rr.right + 1 || tr.left < rr.left - 1) : false, midword })
    }
    return { n: tiles.length, overflowX: document.documentElement.scrollWidth - innerWidth, clipped, shadows: [...shadows], disp: [...disp], rows, cols: getComputedStyle(document.querySelector('.roster .tiles, .roster') ).gridTemplateColumns }
  })
  console.log(tag, `${w}x${h}`, `tiles ${r.n} overflowX ${r.overflowX} clipped ${r.clipped.length} midword ${r.rows.filter(x => x.midword).length} outside ${r.rows.filter(x => x.outside).length}`, JSON.stringify({ clipped: r.clipped.slice(0, 6), shadows: r.shadows, disp: r.disp, cols: r.cols, errs }))
  console.log('   ', r.rows.map(x => `${x.text} [town ${x.townW}x${x.townH}${x.midword ? ' MIDWORD' : ''}]`).join(' ;; '))
  const y = await p.evaluate(() => { const e = document.querySelector('.roster'); return e ? e.getBoundingClientRect().top + scrollY - 80 : 0 })
  await p.evaluate(v => scrollTo(0, v), y); await p.waitForTimeout(500)
  await p.screenshot({ path: `${out}/${tag}-${w}x${h}-${run}.png`, fullPage: false })
  await ctx.close()
}
await b.close()
