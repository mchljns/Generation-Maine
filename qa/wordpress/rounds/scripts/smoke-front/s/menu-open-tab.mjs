// Round 2: with the phone menu open, keep pressing Tab past the last menu link. Where does focus go, can it be seen,
// and does the page scroll behind the open sheet?
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('menu')
const run = process.argv[2] || 'r1'
const b = await launch()
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h, phone, dsf] of [[390, 844, true, 2], [390, 844, false, 1], [640, 400, false, 2]]) {
  const tag = `${name}-${w}x${h}-${phone ? 'touch' : 'kbd'}`
  const ctx = await newCtx(b, { w, h, phone, dsf })
  const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(800)
  await p.focus('#menu'); await p.keyboard.press('Enter'); await p.waitForTimeout(500)
  const seq = []
  for (let i = 1; i <= 7; i++) {
    await p.keyboard.press('Tab'); await p.waitForTimeout(500)
    const g = await p.evaluate(() => {
      const s = document.getElementById('sheet'), a = document.activeElement, ar = a.getBoundingClientRect()
      const cx = ar.left + ar.width / 2, cy = ar.top + ar.height / 2
      const onScreen = cy >= 0 && cy < innerHeight
      const hit = onScreen ? document.elementFromPoint(Math.max(0, Math.min(innerWidth - 1, cx)), cy) : null
      return { active: a.tagName + (a.id ? '#' + a.id : '') + ' ' + (a.getAttribute('aria-label') || a.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 22), inSheet: s.contains(a), top: Math.round(ar.top), onScreen, hiddenBehindSheet: !s.contains(a) && !!(hit && s.contains(hit)), sheetOpen: s.classList.contains('open'), scrollY: Math.round(scrollY) }
    })
    seq.push(g)
    console.log(tag, 'Tab', i, JSON.stringify(g))
    if (i === 5) await p.screenshot({ path: `${out}/${tag}-open-tab5-${run}.png` })
  }
  await ctx.close()
}
await b.close()
