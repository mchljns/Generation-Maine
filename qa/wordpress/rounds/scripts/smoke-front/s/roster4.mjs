// Round 4, FR-R2 / FR-R3: the roster tiles in a page (or on the front page). At each width, for every tile: the number
// (.n) on one line and not squeezed, the name and town inside the tile, words broken mid-word (and whether the word could
// have fitted the column at all), plus the section's width and left edge against the viewport, and page overflow.
// usage: URL=... TAG=... node roster4.mjs <run>
import { launch, newCtx, dir } from './lib.mjs'
const out = dir('roster4'); const run = process.argv[2] || 'r1'
const url = process.env.URL, tag = process.env.TAG || 'wp'
const widths = (process.env.WIDTHS || '320x568,360x740,390x844,414x896,430x932,768x1024,844x390,1024x768,1440x900').split(',').map(s => s.split('x').map(Number))
const b = await launch()
let probs = 0
for (const [w, h] of widths) {
  const ctx = await newCtx(b, { w, h, phone: w < 900 }); const p = await ctx.newPage()
  const errs = []; p.on('pageerror', e => errs.push(e.message))
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(600)
  const r = await p.evaluate(() => {
    const sec = document.querySelector('section.roster, .roster'); if (!sec) return null
    const sr = sec.getBoundingClientRect()
    const lineSplits = el => { // words split across lines, and the longest unbreakable word width vs the element width
      const out = []; const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT)
      for (let n; (n = tw.nextNode());) { const re = /\S+/g; let m; while ((m = re.exec(n.data))) { const rg = document.createRange(); rg.setStart(n, m.index); rg.setEnd(n, m.index + 1); const a = rg.getClientRects()[0]; rg.setStart(n, m.index + m[0].length - 1); rg.setEnd(n, m.index + m[0].length); const z = rg.getClientRects()[0]; rg.setStart(n, m.index); const full = rg.getBoundingClientRect(); if (a && z && Math.abs(a.top - z.top) > 3) out.push(m[0]) } }
      return out }
    const tiles = [...sec.querySelectorAll('.tile')].map((t, i) => {
      const tr = t.getBoundingClientRect(), n = t.querySelector('.n'), nm = t.querySelector('.who b'), town = t.querySelector('.town')
      const nr = n.getBoundingClientRect(), br = nm ? nm.getBoundingClientRect() : null, twr = town ? town.getBoundingClientRect() : null
      const lh = parseFloat(getComputedStyle(n).lineHeight) || parseFloat(getComputedStyle(n).fontSize) * 1.3
      return { i: i + 1, text: t.innerText.replace(/\s*\n\s*/g, ' / '), tileW: Math.round(tr.width), n: [Math.round(nr.width), n.scrollWidth, Math.round(nr.height)], nStacked: nr.height > lh * 1.5, nSqueezed: n.scrollWidth > nr.width + 1,
        nameOut: br ? Math.round(Math.max(br.right - tr.right, tr.left - br.left, 0)) : 0, townOut: twr ? Math.round(Math.max(twr.right - tr.right, 0)) : 0,
        nameSplit: nm ? lineSplits(nm) : [], townSplit: town ? lineSplits(town) : [], nameW: br ? Math.round(br.width) : 0 }
    })
    return { secLeft: Math.round(sr.left), secW: Math.round(sr.width), vw: innerWidth, overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth, cols: getComputedStyle(sec.querySelector('.tiles') || sec).gridTemplateColumns, tiles }
  })
  if (!r) { console.log(tag, `${w}x${h}`, 'NO ROSTER'); await ctx.close(); continue }
  const bad = r.tiles.filter(t => t.nStacked || t.nSqueezed || t.nameOut > 1 || t.townOut > 1 || t.townSplit.length)
  probs += bad.length + (r.overflow > 0 ? 1 : 0)
  console.log(tag, `${w}x${h}`, `section ${r.secLeft}+${r.secW} of ${r.vw}, overflow ${r.overflow}, tiles ${r.tiles.length}, tile width ${r.tiles[0] && r.tiles[0].tileW}; numbers stacked ${r.tiles.filter(t => t.nStacked).length}, squeezed ${r.tiles.filter(t => t.nSqueezed).length}; names past tile ${r.tiles.filter(t => t.nameOut > 1).length}; towns past tile ${r.tiles.filter(t => t.townOut > 1).length}; town words split ${r.tiles.reduce((a, t) => a + t.townSplit.length, 0)}; name words split ${JSON.stringify(r.tiles.filter(t => t.nameSplit.length).map(t => t.i + ':' + t.nameSplit.join('+')))}${errs.length ? ' errors ' + errs.join(';') : ''}`)
  for (const t of bad) console.log('    PROBLEM', JSON.stringify(t))
  const long = r.tiles.filter(t => t.nameSplit.length || t.nameW > t.tileW * 0.6)
  for (const t of long) console.log('    long name', JSON.stringify(t))
  const y = await p.evaluate(() => { const e = document.querySelector('.roster'); return e ? e.getBoundingClientRect().top + scrollY - 80 : 0 })
  await p.evaluate(v => scrollTo(0, v), y); await p.waitForTimeout(400)
  await p.screenshot({ path: `${out}/${tag}-${w}x${h}-${run}.png` })
  // the last tile up close
  const last = p.locator('.roster .tile').last(); await last.scrollIntoViewIfNeeded(); await p.waitForTimeout(200)
  await last.screenshot({ path: `${out}/${tag}-tile-last-${w}-${run}.png` })
  await ctx.close()
}
console.log(tag, 'problem tiles (stacked or squeezed number, name or town past the tile, a town split mid-word) plus overflowing widths:', probs)
await b.close()
