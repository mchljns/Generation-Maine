// Round 4, FR-R4: rotation with the phone menu open, with and without keyboard focus in it. For each sheet item (and the
// menu button): focus before the turn, after it, whether it shows a focus ring, the next Tab and Shift+Tab, scrollY kept.
// Variations: page scrolled to the creators first; touch tap to open (no keyboard); turning back; the reverse turn with
// focus in the desktop bar; phone portrait to phone landscape (stays the phone layout).
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('rot4'); const run = process.argv[2] || 'r1'
const targets = (process.env.TARGETS || 'wp,v2').split(',')
const b = await launch()
const act = p => p.evaluate(() => { const a = document.activeElement, r = a.getBoundingClientRect(), s = document.getElementById('sheet')
  const where = s.contains(a) ? 'sheet' : a.closest('.top') ? 'bar' : a === document.body ? 'body' : 'page'
  let ring = false; try { ring = a.matches(':focus-visible') && getComputedStyle(a).outlineStyle !== 'none' && parseFloat(getComputedStyle(a).outlineWidth) > 0 } catch (e) {}
  return `${where}:${(a.textContent || a.getAttribute('aria-label') || a.tagName).replace(/\s+/g, ' ').trim().slice(0, 20)}${r.height > 0 && r.top >= 0 && r.bottom <= innerHeight ? '' : '(not visible)'}${ring ? '[ring]' : ''}` })
const st = p => p.evaluate(() => { const s = document.getElementById('sheet'); return { open: s.classList.contains('open'), inert: s.inert, exp: document.getElementById('menu').getAttribute('aria-expanded'), ov: document.body.style.overflow, y: Math.round(scrollY) } })
let bad = 0
for (const name of targets) {
  const url = name === 'wp' ? WP : V2
  const items = await (async () => { const ctx = await newCtx(b, { w: 768, h: 1024, phone: false }); const p = await ctx.newPage(); await p.goto(url, { waitUntil: 'networkidle' }); const r = await p.evaluate(() => ({ sheet: [...document.querySelectorAll('#sheet a, #sheet button')].map(a => a.textContent.trim()), bar: [...document.querySelectorAll('.top nav a, .top .cta a, .top a.cta')].map(a => a.textContent.trim()) })); await ctx.close(); return r })()
  console.log(`${name} sheet items ${JSON.stringify(items.sheet)} | bar links ${JSON.stringify(items.bar)}`)
  for (const [w, h] of [[768, 1024], [820, 1180], [834, 1194], [900, 1200]]) for (let steps = 0; steps <= items.sheet.length; steps++) for (const scrolled of [false, true]) {
    if (scrolled && !(w === 768 && (steps === 2 || steps === 0))) continue
    const ctx = await newCtx(b, { w, h, phone: false }); const p = await ctx.newPage()
    const errs = []; p.on('pageerror', e => errs.push(e.message))
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(500)
    if (scrolled) { await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(400) }
    await p.focus('#menu'); await p.keyboard.press('Enter'); await p.waitForTimeout(300)
    for (let i = 0; i < steps; i++) await p.keyboard.press('Tab')
    await p.waitForTimeout(150)
    const before = await act(p), s0 = await st(p)
    await p.setViewportSize({ width: h, height: w }); await p.waitForTimeout(700)
    const after = await act(p), s1 = await st(p)
    if (steps === 2 && w === 768 && !scrolled) await p.screenshot({ path: `${out}/${name}-kbd-tab2-after-${run}.png` })
    await p.keyboard.press('Tab'); await p.waitForTimeout(200); const next = await act(p)
    await p.keyboard.press('Shift+Tab'); await p.keyboard.press('Shift+Tab'); await p.waitForTimeout(200); const prev = await act(p)
    // expected: the same item in the bar (by text), or the bar's first link for the menu button
    const want = steps === 0 ? items.bar[0] : items.sheet[steps - 1]
    const ok = after.startsWith('bar:' + want) && !s1.open && s1.ov === '' && s1.y === s0.y
    if (!ok) bad++
    console.log(`${name} ${w}x${h}${scrolled ? ' scrolled' : ''} Tab x${steps}: before ${before} | after turn ${after}${ok ? '' : ' <<< expected bar:' + want} sheet open ${s1.open} inert ${s1.inert} expanded ${s1.exp} body overflow '${s1.ov}' scrollY ${s0.y}->${s1.y} | Tab ${next} | Shift+Tab x2 ${prev}${errs.length ? ' | errors ' + errs.join('; ') : ''}`)
    // turn back to portrait: menu closed, nothing odd
    if (steps === 2 && !scrolled) { await p.setViewportSize({ width: w, height: h }); await p.waitForTimeout(600); console.log(`   ${name} ${w}x${h} back to portrait: focus ${await act(p)} ${JSON.stringify(await st(p))}`) }
    await ctx.close()
  }
  // touch: open by tap (no keyboard), turn; then a tap opened menu, tap a link? no: just the turn
  for (const [w, h] of [[768, 1024], [820, 1180]]) {
    const ctx = await newCtx(b, { w, h, phone: true }); const p = await ctx.newPage()
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(500)
    await p.tap('#menu'); await p.waitForTimeout(400)
    const before = await act(p)
    await p.setViewportSize({ width: h, height: w }); await p.waitForTimeout(700)
    const after = await act(p), s1 = await st(p)
    await p.screenshot({ path: `${out}/${name}-touch-${w}-after-${run}.png`, clip: { x: 0, y: 0, width: h, height: 120 } })
    console.log(`${name} touch ${w}x${h} tap Menu -> ${h}x${w}: before ${before} | after ${after} ${JSON.stringify(s1)}`)
    await ctx.close()
  }
  // the reverse turn: keyboard focus on a desktop bar link, tablet turned to portrait (the bar links hide)
  for (const steps of [1, 2, 4]) {
    const ctx = await newCtx(b, { w: 1024, h: 768, phone: false }); const p = await ctx.newPage()
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(500)
    await p.keyboard.press('Tab'); for (let i = 0; i < steps; i++) await p.keyboard.press('Tab'); await p.waitForTimeout(150)
    const before = await act(p)
    await p.setViewportSize({ width: 768, height: 1024 }); await p.waitForTimeout(700)
    const after = await act(p)
    await p.keyboard.press('Tab'); await p.waitForTimeout(200); const next = await act(p)
    console.log(`${name} reverse 1024x768 -> 768x1024 focus ${before} | after ${after} | Tab ${next}`)
    await ctx.close()
  }
  // phone portrait to phone landscape: still the phone layout
  {
    const ctx = await newCtx(b, { w: 390, h: 844, phone: true }); const p = await ctx.newPage()
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(500)
    await p.focus('#menu'); await p.keyboard.press('Enter'); await p.waitForTimeout(300); await p.keyboard.press('Tab'); await p.keyboard.press('Tab'); await p.waitForTimeout(150)
    const before = await act(p)
    await p.setViewportSize({ width: 844, height: 390 }); await p.waitForTimeout(700)
    const after = await act(p), s1 = await st(p)
    await p.keyboard.press('Escape'); await p.waitForTimeout(200); const esc = await act(p), s2 = await st(p)
    if (!s1.open || !after.startsWith('sheet:')) bad++
    console.log(`${name} 390x844 -> 844x390 (phone layout) Tab x2: before ${before} | after ${after} ${JSON.stringify(s1)} | Escape ${esc} ${JSON.stringify(s2)}`)
    await ctx.close()
  }
}
console.log(`turns that did not land on the matching bar item (or changed scroll, or left the sheet open): ${bad}`)
await b.close()
