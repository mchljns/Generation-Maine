// Round 3, VIS-N02 variations: rotate with the menu open at other sizes, with the keyboard inside the sheet, with the viewer
// open, and phone portrait to phone landscape (stays the phone layout, so the sheet may stay open but must fit and scroll).
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('rotate'); const run = process.argv[2] || 'r1'
const b = await launch()
const st = p => p.evaluate(() => { const s = document.getElementById('sheet'), m = document.getElementById('menu'), a = document.activeElement, r = s.getBoundingClientRect()
  return { open: s.classList.contains('open'), inert: s.inert, expanded: m.getAttribute('aria-expanded'), bodyOverflow: document.body.style.overflow, sheetDisp: getComputedStyle(s).display, sheetVis: getComputedStyle(s).visibility, menuDisp: getComputedStyle(m).display, sheetBottom: Math.round(r.bottom), sheetScrollable: s.scrollHeight > s.clientHeight, ih: innerHeight, active: (a.id ? '#' + a.id : a.tagName) + ':' + (a.textContent || '').trim().slice(0, 14), y: Math.round(scrollY), vopen: document.documentElement.classList.contains('vopen') } })
for (const [name, url] of [['wp', WP], ['v2', V2]]) {
  // 1. touch: open the menu, rotate, wheel/scroll, rotate back, for several tablet and phone pairs
  for (const [w, h] of [[768, 1024], [820, 1180], [834, 1194], [390, 844], [430, 932]]) {
    const ctx = await newCtx(b, { w, h, phone: true }); const p = await ctx.newPage()
    const errs = []; p.on('pageerror', e => errs.push(e.message))
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(600)
    await p.tap('#menu'); await p.waitForTimeout(500)
    const a = await st(p)
    await p.setViewportSize({ width: h, height: w }); await p.waitForTimeout(800)
    const b1 = await st(p)
    await p.mouse.move(Math.round(h / 2), Math.round(w / 2)); await p.mouse.wheel(0, 600); await p.waitForTimeout(800)
    const b2 = await st(p)
    // last sheet link reachable in landscape? (phone landscape keeps the sheet)
    const lastLink = await p.evaluate(() => { const l = [...document.querySelectorAll('#sheet a')].pop(); const r = l.getBoundingClientRect(); return { top: Math.round(r.top), bottom: Math.round(r.bottom), ih: innerHeight } })
    await p.setViewportSize({ width: w, height: h }); await p.waitForTimeout(800)
    const c = await st(p)
    await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(300)
    if (c.open) await p.tap('#menu'); await p.waitForTimeout(300)
    await p.tap('#menu'); await p.waitForTimeout(400); const d = await st(p)
    await p.keyboard.press('Escape'); await p.waitForTimeout(300); const e = await st(p)
    console.log(name, `touch ${w}x${h} -> ${h}x${w} -> back`, JSON.stringify({ open: [a.open, b1.open, c.open], bodyOverflow: [a.bodyOverflow, b1.bodyOverflow, b2.bodyOverflow, c.bodyOverflow], landscape: { sheetDisp: b1.sheetDisp, menuDisp: b1.menuDisp, yAfterWheel: b2.y, sheetBottom: b1.sheetBottom, ih: b1.ih, scrollable: b1.sheetScrollable, lastLink }, back: { expanded: c.expanded, inert: c.inert }, reopen: [d.open, d.bodyOverflow], escape: [e.open, e.bodyOverflow], errs }))
    await p.setViewportSize({ width: h, height: w }); await p.waitForTimeout(300)
    await ctx.close()
  }
  // 2. keyboard: open with Enter, Tab to the second sheet link, rotate to desktop: where is focus, can Tab continue?
  {
    const ctx = await newCtx(b, { w: 768, h: 1024, phone: false }); const p = await ctx.newPage()
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(600)
    await p.focus('#menu'); await p.keyboard.press('Enter'); await p.waitForTimeout(300); await p.keyboard.press('Tab'); await p.keyboard.press('Tab'); await p.waitForTimeout(200)
    const a = await st(p)
    await p.setViewportSize({ width: 1024, height: 768 }); await p.waitForTimeout(800)
    const b1 = await st(p)
    await p.keyboard.press('Tab'); await p.waitForTimeout(300)
    const b2 = await st(p)
    const vis = await p.evaluate(() => { const r = document.activeElement.getBoundingClientRect(); return { top: Math.round(r.top), h: Math.round(r.height), visible: r.height > 0 && r.top >= 0 && r.bottom <= innerHeight } })
    console.log(name, 'keyboard 768x1024 focus on 2nd sheet link -> 1024x768', JSON.stringify({ before: a.active, afterRotate: [b1.open, b1.active, b1.bodyOverflow], nextTab: b2.active, nextVis: vis }))
    await ctx.close()
  }
  // 3. viewer open on a tablet, rotate to desktop and back
  {
    const ctx = await newCtx(b, { w: 768, h: 1024, phone: true }); const p = await ctx.newPage()
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(600)
    await p.locator('#story-1 .pv').scrollIntoViewIfNeeded(); await p.tap('#story-1 .pv'); await p.waitForTimeout(900)
    const y0 = await p.evaluate(() => Math.round(scrollY))
    const a = await st(p)
    await p.setViewportSize({ width: 1024, height: 768 }); await p.waitForTimeout(900)
    const b1 = await st(p)
    const vv = await p.evaluate(() => { const v = document.querySelector('.viewer'); return v ? { cls: v.className, disp: getComputedStyle(v).display, htmlOverflow: getComputedStyle(document.documentElement).overflow } : null })
    await p.mouse.move(500, 400); await p.mouse.wheel(0, 600); await p.waitForTimeout(800)
    const b2 = await st(p)
    console.log(name, 'viewer open 768x1024 -> 1024x768', JSON.stringify({ y0, vopen: [a.vopen, b1.vopen], viewer: vv, yAfterWheel: b2.y }))
    await ctx.close()
  }
}
await b.close()
