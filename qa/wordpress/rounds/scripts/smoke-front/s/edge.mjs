// Round 2 edge cases: (1) open the phone menu on a tablet, then rotate to landscape desktop width: can the page still
// scroll? (2) short desktop windows: does any story panel overflow and become its own scroll box or tab stop?
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('edge'); const run = process.argv[2] || 'r1'
const b = await launch()
for (const [name, url] of [['wp', WP], ['v2', V2]]) {
  const ctx = await newCtx(b, { w: 768, h: 1024, phone: true }); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(600)
  await p.tap('#menu'); await p.waitForTimeout(500)
  const before = await p.evaluate(() => ({ open: document.getElementById('sheet').classList.contains('open'), bodyOverflow: document.body.style.overflow }))
  await p.setViewportSize({ width: 1024, height: 768 }); await p.waitForTimeout(800)
  const y0 = await p.evaluate(() => scrollY)
  await p.mouse.wheel(0, 900); await p.waitForTimeout(800)
  const after = await p.evaluate(() => ({ open: document.getElementById('sheet').classList.contains('open'), sheetDisplay: getComputedStyle(document.getElementById('sheet')).display, bodyOverflow: document.body.style.overflow, computedOverflow: getComputedStyle(document.body).overflowY, menuDisplay: getComputedStyle(document.getElementById('menu')).display, scrollY: Math.round(scrollY) }))
  console.log(name, 'menu open at 768x1024, then rotated to 1024x768', JSON.stringify({ before, y0, after }))
  await p.screenshot({ path: `${out}/${name}-rotate-${run}.png` })
  // and back to portrait: is the sheet still open?
  await p.setViewportSize({ width: 768, height: 1024 }); await p.waitForTimeout(800)
  console.log(name, 'back to 768x1024', JSON.stringify(await p.evaluate(() => ({ open: document.getElementById('sheet').classList.contains('open'), bodyOverflow: document.body.style.overflow, expanded: document.getElementById('menu').getAttribute('aria-expanded') }))))
  await ctx.close()
  for (const [w, h] of [[1024, 600], [1280, 640], [1366, 768], [901, 700]]) {
    const c2 = await newCtx(b, { w, h }); const q = await c2.newPage()
    await q.goto(url, { waitUntil: 'networkidle' }); await q.waitForTimeout(800)
    const g = await q.evaluate(() => { const s = document.getElementById('stories'); return { top: s.offsetTop, total: s.offsetHeight - innerHeight } })
    const rows = []
    for (let k = 1; k <= 9; k++) {
      await q.evaluate(({ y }) => scrollTo({ top: y, behavior: 'instant' }), { y: Math.round(g.top + (k - 0.5) / 9 * g.total) }); await q.waitForTimeout(700)
      rows.push(await q.evaluate(() => { const pn = document.querySelector('.panel.on'), r = pn.getBoundingClientRect(), bar = document.querySelector('.top').getBoundingClientRect(), wh = document.querySelector('.where').getBoundingClientRect(), st = document.getElementById('stage').getBoundingClientRect(); return { k: pn.id, overflow: pn.scrollHeight - pn.clientHeight, top: Math.round(r.top), bottom: Math.round(r.bottom), whereBottom: Math.round(wh.bottom), stageTop: Math.round(st.top), barBottom: Math.round(bar.bottom), ih: innerHeight } }))
    }
    const worst = rows.reduce((a, r) => (r.overflow > a.overflow ? r : a), rows[0])
    const cut = rows.filter(r => r.whereBottom > r.ih || r.stageTop < r.barBottom)
    console.log(name, `${w}x${h}`, 'max panel overflow', JSON.stringify(worst), 'rows with stage under bar or position row off screen:', cut.length)
    if (worst.overflow > 0) await q.screenshot({ path: `${out}/${name}-${w}x${h}-overflow-${run}.png` })
    // keyboard: does Tab land on a panel?
    await q.evaluate(() => { const s = document.getElementById('stories'); scrollTo({ top: s.offsetTop - 200, behavior: 'instant' }) })
    await q.focus('.hero a[href$="#follow"]')
    const stops = []
    for (let i = 0; i < 4; i++) { await q.keyboard.press('Tab'); await q.waitForTimeout(80); stops.push(await q.evaluate(() => { const a = document.activeElement; return a.tagName + (a.id ? '#' + a.id : '') + (a.classList.contains('panel') ? '.panel' : '') })) }
    console.log(name, `${w}x${h}`, 'Tab after hero link:', stops.join(' > '))
    await c2.close()
  }
}
await b.close()
