// Round 2: what a screen reader gets from the pause control (Chromium accessibility tree via CDP), before and after
// toggling with the keyboard, in both motion modes; and where it sits in the Tab order from the top of the page.
import { launch, newCtx, WP, V2 } from './lib.mjs'
const b = await launch()
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h] of [[1440, 900], [390, 844]]) for (const reduced of [false, true]) {
  const tag = `${name} ${w} ${reduced ? 'reduce' : 'motion'}`
  const ctx = await newCtx(b, { w, h, reduced }); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(800)
  const cdp = await ctx.newCDPSession(p)
  const ax = async () => {
    const { root } = await cdp.send('DOM.getDocument', { depth: 0 })
    const { nodeId } = await cdp.send('DOM.querySelector', { nodeId: root.nodeId, selector: '#cpause' })
    const { nodes } = await cdp.send('Accessibility.getPartialAXTree', { nodeId, fetchRelatives: false })
    const n = nodes[0]; const prop = k => { const x = (n.properties || []).find(pp => pp.name === k); return x ? x.value.value : undefined }
    return { role: n.role && n.role.value, name: n.name && n.name.value, pressed: prop('pressed'), focusable: prop('focusable'), ignored: n.ignored }
  }
  console.log(tag, 'initial', JSON.stringify(await ax()))
  // Tab order from the top: how many presses to reach the pause button, and what comes just before and after
  await p.evaluate(() => scrollTo(0, 0))
  const seen = []; let at = -1
  for (let i = 1; i <= 60; i++) { await p.keyboard.press('Tab'); const d = await p.evaluate(() => { const a = document.activeElement; return (a.id ? '#' + a.id : a.tagName) + ' ' + (a.getAttribute('aria-label') || a.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 20) }); seen.push(d); if (d.startsWith('#cpause')) { at = i; break } }
  console.log(tag, 'Tab presses from top to reach the pause button:', at, '| previous stops:', seen.slice(-4, -1).join(' > '))
  await p.keyboard.press('Tab'); console.log(tag, 'next stop after pause:', await p.evaluate(() => { const a = document.activeElement; return (a.id ? '#' + a.id : a.tagName) + ' ' + (a.getAttribute('aria-label') || '').slice(0, 30) }))
  await p.keyboard.press('Shift+Tab')
  const vis = await p.evaluate(() => { const a = document.activeElement, r = a.getBoundingClientRect(), bar = document.querySelector('.top').getBoundingClientRect(); return { id: a.id, top: Math.round(r.top), bottom: Math.round(r.bottom), barBottom: Math.round(bar.bottom), ih: innerHeight, onScreen: r.top >= bar.bottom && r.bottom <= innerHeight, focusVisible: a.matches(':focus-visible') } })
  console.log(tag, 'pause focused by Tab, on screen:', JSON.stringify(vis))
  await p.keyboard.press('Space'); await p.waitForTimeout(500)
  console.log(tag, 'after Space', JSON.stringify(await ax()))
  await p.keyboard.press('Enter'); await p.waitForTimeout(500)
  console.log(tag, 'after Enter', JSON.stringify(await ax()))
  await ctx.close()
}
await b.close()
