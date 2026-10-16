// fix4 N1: every focus() call in the page script, made while the page is scrolled down: does scrollY move, and where does
// focus land? A: Tab wraps in the open phone menu (last link -> Menu, Menu -> Shift+Tab -> last link). B: Escape from the
// sheet. C: the tablet turn with the menu open (focus in the sheet by keyboard, and by finger tap only). D: the viewer's Tab
// wrap. E: the newsletter's empty submit. usage: node focusjump.mjs ; env TARGETS=wp,v2
import { launch, newCtx, WP, V2 } from './lib.mjs'
const targets = (process.env.TARGETS || 'wp,v2').split(',')
const b = await launch()
const y = p => p.evaluate(() => Math.round(scrollY))
const act = p => p.evaluate(() => { const a = document.activeElement; const s = document.getElementById('sheet'); return (s && s.contains(a) ? 'sheet:' : a.closest('.top') ? 'bar:' : a.closest('#viewer') ? 'viewer:' : '') + (a.id ? '#' + a.id : (a.textContent || a.getAttribute('aria-label') || a.tagName).replace(/\s+/g, ' ').trim().slice(0, 18)) })
const ftap = async (ctx, p, sel) => { const cdp = await ctx.newCDPSession(p); const bx = await p.evaluate(s => { const r = document.querySelector(s).getBoundingClientRect(); return [Math.round(r.left + r.width / 2), Math.round(r.top + r.height / 2)] }, sel); await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: bx[0], y: bx[1] }] }); await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }) }
let moved = 0, n = 0
const rep = (name, label, y0, y1, extra = '') => { n++; if (Math.abs(y1 - y0) > 1) moved++; console.log(`${name} ${label}: scrollY ${y0} -> ${y1}${Math.abs(y1 - y0) > 1 ? ' MOVED ' + (y1 - y0) : ''} ${extra}`) }
const toCreators = async p => { await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(600) }
for (const name of targets) {
  const url = name === 'wp' ? WP : V2
  for (const [w, h] of [[390, 844], [768, 1024]]) {
    // A. Tab wraps inside the open menu
    { const ctx = await newCtx(b, { w, h, phone: true }); const p = await ctx.newPage(); await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(500); await toCreators(p)
      const y0 = await y(p); await ftap(ctx, p, '#menu'); await p.waitForTimeout(500)
      const nl = await p.evaluate(() => document.querySelectorAll('#sheet a[href], #sheet button').length)
      await p.focus('#menu'); const y1 = await y(p)
      for (let i = 0; i < nl; i++) await p.keyboard.press('Tab')
      await p.waitForTimeout(150); const atLast = await act(p), y2 = await y(p)
      await p.keyboard.press('Tab'); await p.waitForTimeout(300); const wrapped = await act(p), y3 = await y(p)
      await p.keyboard.press('Shift+Tab'); await p.waitForTimeout(300); const back = await act(p), y4 = await y(p)
      rep(name, `${w}x${h} A menu Tab to the last link (${atLast})`, y1, y2)
      rep(name, `${w}x${h} A menu Tab wraps to ${wrapped}`, y2, y3)
      rep(name, `${w}x${h} A menu Shift+Tab wraps to ${back}`, y3, y4, `(start ${y0})`)
      await ctx.close() }
    // B. Escape from inside the sheet
    { const ctx = await newCtx(b, { w, h, phone: true }); const p = await ctx.newPage(); await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(500); await toCreators(p)
      const y0 = await y(p); await ftap(ctx, p, '#menu'); await p.waitForTimeout(500); await p.keyboard.press('Tab'); await p.waitForTimeout(150); const y1 = await y(p), in1 = await act(p)
      await p.keyboard.press('Escape'); await p.waitForTimeout(900); rep(name, `${w}x${h} B Escape from ${in1}, focus ${await act(p)}`, y1, await y(p), `(start ${y0})`)
      await ctx.close() }
  }
  // C. the turn with the menu open: focus in the sheet by keyboard (Tab x2), on the Menu button (keyboard), and finger tap only
  for (const mode of ['tab2', 'menubtn', 'finger']) {
    const ctx = await newCtx(b, { w: 768, h: 1024, phone: true }); const p = await ctx.newPage(); await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(500); await toCreators(p)
    if (mode === 'finger') { await ftap(ctx, p, '#menu') } else { await p.focus('#menu'); await p.keyboard.press('Enter'); if (mode === 'tab2') { await p.keyboard.press('Tab'); await p.keyboard.press('Tab') } }
    await p.waitForTimeout(400); const y0 = await y(p), f0 = await act(p)
    await p.setViewportSize({ width: 1024, height: 768 }); await p.waitForTimeout(1200)
    const r = await p.evaluate(() => ({ open: document.getElementById('sheet').classList.contains('open'), top: Math.round(document.getElementById('stories').getBoundingClientRect().top) }))
    rep(name, `768x1024 C turn to 1024x768 (${mode}) focus ${f0} -> ${await act(p)}`, y0, await y(p), `sheet open ${r.open}, stories top ${r.top}`)
    await ctx.close()
  }
  // D. the viewer: open by a finger tap on the current card, Tab round, Shift+Tab round, Escape
  { const ctx = await newCtx(b, { w: 390, h: 844, phone: true }); const p = await ctx.newPage(); await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(500); await toCreators(p)
    const y0 = await y(p); await ftap(ctx, p, '.panel.on .pv'); await p.waitForTimeout(800)
    const open = await p.evaluate(() => !document.getElementById('viewer').hidden), y1 = await y(p), f1 = await act(p)
    const nf = await p.evaluate(() => [...document.getElementById('viewer').querySelectorAll('button, [href], [tabindex]:not([tabindex="-1"])')].filter(x => x.offsetParent !== null).length)
    const seq = []; for (let i = 0; i < nf + 1; i++) { await p.keyboard.press('Tab'); await p.waitForTimeout(80); seq.push(await act(p)) }
    const y2 = await y(p); await p.keyboard.press('Shift+Tab'); await p.keyboard.press('Shift+Tab'); await p.waitForTimeout(150); const y3 = await y(p)
    rep(name, `390x844 D viewer open(${open}) focus ${f1}, Tab x${nf + 1}: ${seq.join(' > ')}`, y1, y2, `(start ${y0})`)
    rep(name, `390x844 D viewer Shift+Tab x2 (${await act(p)})`, y2, y3)
    await p.keyboard.press('Escape'); await p.waitForTimeout(700); rep(name, `390x844 D viewer Escape, focus ${await act(p)}`, y0, await y(p))
    await ctx.close() }
  // E. the newsletter: empty submit by the button while the page is scrolled so the form is on screen, and while it is not
  for (const where of ['form', 'creators']) {
    const ctx = await newCtx(b, { w: 390, h: 844, phone: true }); const p = await ctx.newPage(); await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(500)
    if (!(await p.evaluate(() => !!document.getElementById('nl')))) { console.log(`${name} 390x844 E no newsletter form on this page`); await ctx.close(); continue }
    await p.evaluate(() => document.getElementById('nl').scrollIntoView({ block: 'center', behavior: 'instant' })); await p.waitForTimeout(400)
    const y0 = await y(p)
    if (where === 'form') await p.evaluate(() => document.getElementById('nl').requestSubmit()); else { await toCreators(p); await p.evaluate(() => document.getElementById('nl').requestSubmit()) }
    await p.waitForTimeout(700); const y1 = await y(p)
    console.log(`${name} 390x844 E empty submit (${where}): scrollY ${where === 'form' ? y0 : '(creators)'} -> ${y1}, focus ${await act(p)}, input on screen ${await p.evaluate(() => { const r = document.querySelector('#nl input[type=email], #nl [name=email]').getBoundingClientRect(); return r.top >= 68 && r.bottom <= innerHeight })}`)
    await ctx.close()
  }
}
console.log(`TOTAL ${n} checks, scrollY moved in ${moved}`)
await b.close()
