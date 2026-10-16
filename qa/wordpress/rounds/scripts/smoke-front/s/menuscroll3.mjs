// Is the page scroll on opening the menu real or a Playwright artifact, and does the FR-R4 focus move scroll the page?
// A: a finger tap through CDP touch events at the Menu button's position (no scroll-into-view by the test tool).
// B: element.focus() on the Menu button and on a bar link while scrolled down, with and without preventScroll.
// C: menu opened by a CDP finger tap while at the creators, then the tablet turns (768x1024 -> 1024x768): scrollY before and
//    after, as served, and with HTMLElement.focus patched to preventScroll (diagnosis only).
// D: keyboard: menu open with focus in the sheet, Escape (the page focuses Menu again): scrollY.
import { launch, newCtx, WP, V2 } from './lib.mjs'
const b = await launch()
const y = p => p.evaluate(() => Math.round(scrollY))
const ftap = async (ctx, p, sel) => { const cdp = await ctx.newCDPSession(p); const bx = await p.evaluate(s => { const r = document.querySelector(s).getBoundingClientRect(); return [Math.round(r.left + r.width / 2), Math.round(r.top + r.height / 2)] }, sel); await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: bx[0], y: bx[1] }] }); await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }) }
for (const [name, url] of [['wp', WP], ['v2', V2]]) {
  for (const [w, h] of [[390, 844], [768, 1024]]) { // A
    const ctx = await newCtx(b, { w, h, phone: true }); const p = await ctx.newPage()
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(500)
    await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(600)
    const y0 = await y(p); await ftap(ctx, p, '#menu'); await p.waitForTimeout(700); const y1 = await y(p), open = await p.evaluate(() => document.getElementById('sheet').classList.contains('open'))
    await ftap(ctx, p, '#menu'); await p.waitForTimeout(700); const y2 = await y(p)
    console.log(`${name} A ${w}x${h} finger tap on Menu at the creators: scrollY ${y0} -> open(${open}) ${y1} -> tap again ${y2}`)
    await ctx.close()
  }
  for (const sel of ['#menu', '.top nav a']) for (const ps of [false, true]) { // B
    const w = sel === '#menu' ? 768 : 1024, h = sel === '#menu' ? 1024 : 768
    const ctx = await newCtx(b, { w, h, phone: false }); const p = await ctx.newPage()
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(500)
    await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(600)
    const y0 = await y(p); await p.evaluate(([s, ps]) => document.querySelector(s).focus({ preventScroll: ps }), [sel, ps]); await p.waitForTimeout(900); const y1 = await y(p)
    console.log(`${name} B ${w}x${h} ${sel}.focus({preventScroll:${ps}}) at the creators: scrollY ${y0} -> ${y1}`)
    await ctx.close()
  }
  for (const patch of [false, true]) { // C
    const ctx = await newCtx(b, { w: 768, h: 1024, phone: true }); const p = await ctx.newPage()
    if (patch) await ctx.addInitScript(() => { const f = HTMLElement.prototype.focus; HTMLElement.prototype.focus = function (o) { return f.call(this, Object.assign({}, o || {}, { preventScroll: true })) } })
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(500)
    await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(600)
    const y0 = await y(p); await ftap(ctx, p, '#menu'); await p.waitForTimeout(600); const y1 = await y(p)
    const act0 = await p.evaluate(() => document.activeElement.id || document.activeElement.tagName)
    await p.setViewportSize({ width: 1024, height: 768 }); await p.waitForTimeout(1200)
    const r = await p.evaluate(() => ({ y: Math.round(scrollY), act: (document.activeElement.textContent || document.activeElement.tagName).trim().slice(0, 12), storiesTop: Math.round(document.getElementById('stories').getBoundingClientRect().top) }))
    console.log(`${name} C 768x1024 finger tap Menu at the creators, turn to 1024x768${patch ? ' (focus patched to preventScroll)' : ''}: scrollY ${y0} -> open ${y1} (focus ${act0}) -> after turn ${r.y}, focus ${r.act}, stories top ${r.storiesTop}`)
    await ctx.close()
  }
  { // C2 control: no menu, same turn
    const ctx = await newCtx(b, { w: 768, h: 1024, phone: true }); const p = await ctx.newPage()
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(500)
    await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(600)
    const y0 = await y(p); await p.setViewportSize({ width: 1024, height: 768 }); await p.waitForTimeout(1200)
    const r = await p.evaluate(() => ({ y: Math.round(scrollY), storiesTop: Math.round(document.getElementById('stories').getBoundingClientRect().top) }))
    console.log(`${name} C2 control, no menu, turn 768x1024 -> 1024x768 at the creators: scrollY ${y0} -> ${r.y}, stories top ${r.storiesTop}`)
    await ctx.close()
  }
  { // D keyboard Escape from inside the sheet while scrolled down (menu opened by a finger tap, then keyboard)
    const ctx = await newCtx(b, { w: 768, h: 1024, phone: true }); const p = await ctx.newPage()
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(500)
    await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(600)
    const y0 = await y(p); await ftap(ctx, p, '#menu'); await p.waitForTimeout(500); await p.keyboard.press('Tab'); await p.waitForTimeout(200); const y1 = await y(p)
    await p.keyboard.press('Escape'); await p.waitForTimeout(900); const y2 = await y(p), act = await p.evaluate(() => document.activeElement.id)
    console.log(`${name} D 768x1024 finger tap Menu, Tab into the sheet, Escape: scrollY ${y0} -> ${y1} -> after Escape ${y2} (focus #${act})`)
    await ctx.close()
  }
}
await b.close()
