import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('zoom')
const run = process.argv[2] || 'r1'
const b = await launch()
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h] of [[640, 400], [640, 512]]) {
  // 1280x800 (and 1280x1024) at 200 percent zoom = 640 CSS px wide at device scale 2, desktop (no touch)
  const ctx = await newCtx(b, { w, h, phone: false, dsf: 2 })
  const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(1200)
  const r = await p.evaluate(() => {
    const vis = e => { for (let x = e; x && x.nodeType === 1; x = x.parentElement) { const cs = getComputedStyle(x); if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) < 0.05) return false } const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 }
    const els = [...document.querySelectorAll('main h1, main h2, main h3, main p, main .btn, main .wp-block-button__link, main .row, main .where, footer p, footer a, footer nav, .top a, .top button')].filter(vis).filter(e => !e.closest('.viewer') && !e.closest('.sheet'))
    const rects = els.map(e => { const r = e.getBoundingClientRect(); return { e, l: r.left, t: r.top + scrollY, r: r.right, b: r.bottom + scrollY } })
    const overlaps = []
    for (let i = 0; i < rects.length; i++) for (let j = i + 1; j < rects.length; j++) {
      const a = rects[i], c = rects[j]
      if (a.e.contains(c.e) || c.e.contains(a.e)) continue
      const ix = Math.min(a.r, c.r) - Math.max(a.l, c.l), iy = Math.min(a.b, c.b) - Math.max(a.t, c.t)
      if (ix > 2 && iy > 2) overlaps.push(`${a.e.tagName}.${a.e.className.toString().slice(0, 20)} "${a.e.textContent.trim().slice(0, 15)}" x ${c.e.tagName}.${c.e.className.toString().slice(0, 20)} "${c.e.textContent.trim().slice(0, 15)}" ${Math.round(ix)}x${Math.round(iy)}`)
    }
    const clipped = els.filter(e => e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).overflowX !== 'visible').map(e => e.tagName + '.' + e.className + ' "' + e.textContent.trim().slice(0, 20) + '" by ' + (e.scrollWidth - e.clientWidth))
    const offRight = els.filter(e => e.getBoundingClientRect().right > innerWidth + 1 && !e.closest('#panels')).map(e => e.tagName + ' "' + e.textContent.trim().slice(0, 20) + '" right=' + Math.round(e.getBoundingClientRect().right))
    return { docOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth, layout: getComputedStyle(document.getElementById('menu')).display !== 'none' ? 'phone' : 'desktop', overlaps: overlaps.slice(0, 15), clipped: clipped.slice(0, 10), offRight: offRight.slice(0, 10), pageH: document.documentElement.scrollHeight, barH: document.querySelector('.top').getBoundingClientRect().height }
  })
  console.log(name, `${w}x${h}@2`, JSON.stringify(r, null, 1))
  await p.screenshot({ path: `${out}/${name}-${w}x${h}-full-${run}.png`, fullPage: true })
  // stories in view and menu open
  await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(500)
  const st = await p.evaluate(() => { const pv = document.querySelector('.panel.on .pv').getBoundingClientRect(), where = document.querySelector('.where').getBoundingClientRect(), bar = document.querySelector('.top').getBoundingClientRect(); return { pvTop: Math.round(pv.top), pvBottom: Math.round(pv.bottom), pvH: Math.round(pv.height), whereTop: Math.round(where.top), whereBottom: Math.round(where.bottom), barBottom: Math.round(bar.bottom), ih: innerHeight } })
  console.log(name, `${w}x${h}@2 stories`, JSON.stringify(st))
  await p.screenshot({ path: `${out}/${name}-${w}x${h}-stories-${run}.png` })
  await p.click('#menu'); await p.waitForTimeout(500)
  const m = await p.evaluate(() => { const s = document.getElementById('sheet'), r = s.getBoundingClientRect(); const last = [...s.querySelectorAll('a')].pop().getBoundingClientRect(); return { sheetTop: r.top, sheetBottom: r.bottom, lastLinkBottom: Math.round(last.bottom), ih: innerHeight, sheetScrollable: s.scrollHeight > s.clientHeight, overflowY: getComputedStyle(s).overflowY } })
  console.log(name, `${w}x${h}@2 menu`, JSON.stringify(m))
  await p.screenshot({ path: `${out}/${name}-${w}x${h}-menu-${run}.png` })
  await ctx.close()
}
await b.close()
