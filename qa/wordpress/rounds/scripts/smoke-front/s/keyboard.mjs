import { launch, newCtx, WP, V2, dir } from './lib.mjs'
import { writeFileSync } from 'node:fs'
const out = dir('keyboard')
const run = process.argv[2] || 'r1'
const b = await launch()
const settle = async p => { let last = -1; for (let i = 0; i < 30; i++) { const y = await p.evaluate(() => scrollY + ',' + [...document.querySelectorAll('#panels')].map(e => e.scrollLeft).join()); if (y === last) break; last = y; await p.waitForTimeout(100) } }
const info = p => p.evaluate(() => {
  const a = document.activeElement
  if (!a || a === document.body) return { tag: 'BODY' }
  const r = a.getBoundingClientRect(), cs = getComputedStyle(a)
  const bar = document.querySelector('.top').getBoundingClientRect()
  const sheet = document.getElementById('sheet'), scs = getComputedStyle(sheet)
  const inHiddenSheet = sheet.contains(a) && (scs.display === 'none' || scs.opacity === '0')
  const hiddenAncestor = (() => { for (let e = a; e; e = e.parentElement) { const s = getComputedStyle(e); if (s.visibility === 'hidden' || s.display === 'none' || parseFloat(s.opacity) === 0) return e.className || e.tagName } return null })()
  const ring = (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0) ? `outline ${cs.outlineStyle} ${cs.outlineWidth} ${cs.outlineColor}` : (cs.boxShadow !== 'none' ? 'shadow ' + cs.boxShadow.slice(0, 40) : 'NONE')
  const isTop = document.querySelector('.top').contains(a)
  return { tag: a.tagName, id: a.id, label: (a.getAttribute('aria-label') || a.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 30), href: a.getAttribute('href'), top: Math.round(r.top), bottom: Math.round(r.bottom), w: Math.round(r.width), h: Math.round(r.height), ring, underBar: !isTop && r.top < bar.bottom - 1 && r.bottom > bar.top, offscreen: r.bottom <= 0 || r.top >= innerHeight || r.right <= 0 || r.left >= innerWidth, hiddenAncestor, inHiddenSheet }
})
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h] of [[1440, 900], [390, 844]]) {
  const ctx = await newCtx(b, { w, h, phone: false })  // keyboard user: no touch emulation, narrow window
  const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(800)
  const stops = []
  for (let i = 0; i < 80; i++) {
    await p.keyboard.press('Tab'); await p.waitForTimeout(60); await settle(p)
    const s = await info(p)
    stops.push(s)
    if (i > 2 && s.tag === 'BODY') break
    if (i > 2 && s.label === stops[0].label && s.tag === stops[0].tag) break
  }
  writeFileSync(`${out}/${name}-${w}-forward-${run}.json`, JSON.stringify(stops, null, 1))
  console.log(`== ${name} ${w}: ${stops.length} stops`)
  stops.forEach((s, i) => console.log(`${i + 1}. ${s.tag}${s.id ? '#' + s.id : ''} "${s.label}" ${s.href || ''} ${s.w}x${s.h} top=${s.top} ring=${s.ring}${s.underBar ? ' UNDER-BAR' : ''}${s.offscreen ? ' OFFSCREEN' : ''}${s.hiddenAncestor ? ' HIDDEN(' + s.hiddenAncestor + ')' : ''}`))
  // backward from the end
  const back = []
  for (let i = 0; i < 25; i++) { await p.keyboard.press('Shift+Tab'); await p.waitForTimeout(60); await settle(p); back.push(await info(p)) }
  const bad = back.filter(s => s.underBar || s.offscreen)
  console.log(`   shift-tab x25: underBar/offscreen stops: ${bad.map(s => s.label + '@' + s.top).join(', ') || 'none'}`)
  // skip link
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(600)
  await p.keyboard.press('Tab'); await p.waitForTimeout(100)
  await p.screenshot({ path: `${out}/${name}-${w}-skip-${run}.png` })
  await p.keyboard.press('Enter'); await p.waitForTimeout(400); await settle(p)
  const afterSkip = await p.evaluate(() => ({ hash: location.hash, active: document.activeElement.tagName + '#' + document.activeElement.id, scrollY: Math.round(scrollY) }))
  await p.keyboard.press('Tab'); await p.waitForTimeout(100); await settle(p)
  const next = await info(p)
  console.log(`   skip link: after Enter ${JSON.stringify(afterSkip)}; next Tab -> ${next.tag} "${next.label}" top=${next.top}`)
  await ctx.close()
}
await b.close()
