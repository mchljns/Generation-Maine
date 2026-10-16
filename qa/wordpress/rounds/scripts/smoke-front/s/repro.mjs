// Fix round 2, visitor group: reproduce/verify VIS-N02 (rotate with the menu open), VIS-N04 (Tab past the open menu),
// VIS-N03 (pause control name and pressed state), VIS-N08 (animations while paused). WP and the local v2 page.
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('repro'); const run = process.argv[2] || 'before'
const only = process.env.ONLY || ''
const b = await launch()
for (const [name, url] of [['wp', WP], ['v2', V2]]) {
  if (only && only !== name) continue
  // N02: open the menu at 768x1024 (touch), rotate to 1024x768, wheel, rotate back
  {
    const ctx = await newCtx(b, { w: 768, h: 1024, phone: true }); const p = await ctx.newPage()
    const errs = []; p.on('pageerror', e => errs.push(e.message))
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(600)
    await p.tap('#menu'); await p.waitForTimeout(500)
    const before = await p.evaluate(() => ({ open: document.getElementById('sheet').classList.contains('open'), bodyOverflow: document.body.style.overflow }))
    await p.setViewportSize({ width: 1024, height: 768 }); await p.waitForTimeout(800)
    await p.mouse.move(500, 400); await p.mouse.wheel(0, 900); await p.waitForTimeout(900)
    const after = await p.evaluate(() => ({ open: document.getElementById('sheet').classList.contains('open'), bodyOverflow: document.body.style.overflow, inert: document.getElementById('sheet').inert, expanded: document.getElementById('menu').getAttribute('aria-expanded'), scrollY: Math.round(scrollY) }))
    await p.setViewportSize({ width: 768, height: 1024 }); await p.waitForTimeout(800)
    const back = await p.evaluate(() => ({ open: document.getElementById('sheet').classList.contains('open'), bodyOverflow: document.body.style.overflow, expanded: document.getElementById('menu').getAttribute('aria-expanded'), vis: getComputedStyle(document.getElementById('sheet')).visibility }))
    // and the menu still works after the round trip
    await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(300)
    await p.tap('#menu'); await p.waitForTimeout(500)
    const reopen = await p.evaluate(() => ({ open: document.getElementById('sheet').classList.contains('open'), bodyOverflow: document.body.style.overflow }))
    await p.tap('#menu'); await p.waitForTimeout(500)
    const reclose = await p.evaluate(() => ({ open: document.getElementById('sheet').classList.contains('open'), bodyOverflow: document.body.style.overflow }))
    console.log(name, 'N02', JSON.stringify({ before, after, back, reopen, reclose, errs }))
    await ctx.close()
  }
  // N04: open the menu with the keyboard and press Tab 7 times, then Shift+Tab 3 times, then Escape
  for (const [w, h, phone, dsf] of [[390, 844, true, 2], [390, 844, false, 1], [640, 400, false, 2]]) {
    const tag = `${name} N04 ${w}x${h} ${phone ? 'touch' : 'kbd'}`
    const ctx = await newCtx(b, { w, h, phone, dsf }); const p = await ctx.newPage()
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(700)
    await p.focus('#menu'); await p.keyboard.press('Enter'); await p.waitForTimeout(400)
    const where = () => p.evaluate(() => { const s = document.getElementById('sheet'), a = document.activeElement, r = a.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2, on = cy >= 0 && cy < innerHeight, hit = on ? document.elementFromPoint(Math.max(0, Math.min(innerWidth - 1, cx)), cy) : null
      return (a.id ? '#' + a.id : a.tagName) + ':' + (a.textContent || '').trim().slice(0, 12) + (s.contains(a) ? '[sheet]' : '') + (!s.contains(a) && hit && s.contains(hit) ? '[HIDDEN]' : '') + (s.classList.contains('open') ? '' : '[closed]') + '@' + Math.round(scrollY) })
    const seq = []
    for (let i = 0; i < 7; i++) { await p.keyboard.press('Tab'); await p.waitForTimeout(250); seq.push(await where()) }
    const back = []
    for (let i = 0; i < 3; i++) { await p.keyboard.press('Shift+Tab'); await p.waitForTimeout(250); back.push(await where()) }
    await p.keyboard.press('Escape'); await p.waitForTimeout(300)
    const esc = await where()
    console.log(tag, 'Tab:', seq.join(' > '), '| Shift+Tab:', back.join(' > '), '| Escape:', esc)
    await ctx.close()
  }
  // N03 + N08: the pause control in the accessibility tree, and the running animations, playing and paused
  for (const reduced of [false, true]) {
    const ctx = await newCtx(b, { w: 1440, h: 900, reduced }); const p = await ctx.newPage()
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(2200)
    const cdp = await ctx.newCDPSession(p)
    const ax = async () => { const { root } = await cdp.send('DOM.getDocument', { depth: 0 }); const { nodeId } = await cdp.send('DOM.querySelector', { nodeId: root.nodeId, selector: '#cpause' }); const { nodes } = await cdp.send('Accessibility.getPartialAXTree', { nodeId, fetchRelatives: false }); const n = nodes[0]; const pr = (n.properties || []).find(x => x.name === 'pressed'); return `${n.role.value} "${n.name.value}" pressed=${pr ? pr.value.value : '-'}` }
    const anims = () => p.evaluate(() => document.getAnimations().filter(a => a.playState === 'running' && a.effect && a.effect.getTiming().iterations === Infinity).map(a => a.animationName || a.constructor.name).join(','))
    const s0 = await ax(), a0 = await anims()
    await p.focus('#cpause'); await p.keyboard.press('Space'); await p.waitForTimeout(400)
    const s1 = await ax(), a1 = await anims()
    await p.keyboard.press('Enter'); await p.waitForTimeout(400)
    const s2 = await ax(), a2 = await anims()
    console.log(name, 'N03/N08', reduced ? 'reduce' : 'motion', JSON.stringify({ load: [s0, a0], space: [s1, a1], enter: [s2, a2] }))
    await ctx.close()
  }
}
await b.close()
