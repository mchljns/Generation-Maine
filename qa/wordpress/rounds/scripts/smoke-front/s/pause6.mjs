// Round 3, VIS-N03 and VIS-N08 at the six sizes: the pause control's role, name and pressed state in the accessibility tree
// (load, tap or click, Space, Enter), the running infinite animations and the html.paused class, playing and paused.
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('pause6'); const run = process.argv[2] || 'r1'
const b = await launch()
const sizes = [[320, 568], [390, 844], [768, 1024], [844, 390], [1024, 768], [1440, 900]]
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h] of sizes) for (const reduced of [false, true]) {
  const phone = w <= 900
  const ctx = await newCtx(b, { w, h, phone, reduced }); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(2000)
  const cdp = await ctx.newCDPSession(p)
  const ax = async () => { const { root } = await cdp.send('DOM.getDocument', { depth: 0 }); const { nodeId } = await cdp.send('DOM.querySelector', { nodeId: root.nodeId, selector: '#cpause' }); const { nodes } = await cdp.send('Accessibility.getPartialAXTree', { nodeId, fetchRelatives: false }); const n = nodes[0]; const pr = (n.properties || []).find(x => x.name === 'pressed'); return `${n.role.value} "${n.name.value}" pressed=${pr ? pr.value.value : '-'}` }
  const anims = () => p.evaluate(() => document.getAnimations().filter(a => a.playState === 'running' && a.effect && a.effect.getTiming().iterations === Infinity).map(a => a.animationName).join(',') + (document.documentElement.classList.contains('paused') ? ' [html.paused]' : ''))
  const r = { load: [await ax(), await anims()] }
  await p.locator('#cpause').scrollIntoViewIfNeeded(); await p.waitForTimeout(300)
  if (phone) await p.tap('#cpause'); else await p.click('#cpause')
  await p.waitForTimeout(500); r.click = [await ax(), await anims()]
  await p.focus('#cpause'); await p.keyboard.press('Space'); await p.waitForTimeout(400); r.space = [await ax(), await anims()]
  await p.keyboard.press('Enter'); await p.waitForTimeout(400); r.enter = [await ax(), await anims()]
  // with the clips paused now (or playing), scroll to the top: the dot is a still gold dot
  await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(600)
  const dot = await p.evaluate(() => { const d = document.querySelector('h1 .d'); if (!d) return null; const cs = getComputedStyle(d), af = getComputedStyle(d, '::after'); const rr = d.getBoundingClientRect(); return { w: Math.round(rr.width), h: Math.round(rr.height), bg: cs.backgroundColor, afterAnim: af.animationName, afterOpacity: af.opacity } })
  r.dot = dot
  if (w === 1440 || w === 390) await p.locator('h1').screenshot({ path: `${out}/${name}-${w}x${h}-${reduced ? 'reduce' : 'motion'}-h1-${run}.png` })
  console.log(name, `${w}x${h}`, reduced ? 'reduce' : 'motion', JSON.stringify(r))
  await ctx.close()
}
await b.close()
