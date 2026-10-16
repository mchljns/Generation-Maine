// Round 2 misc: footer small print at 360, and the stepper's live region at 1440 (CDP accessibility tree)
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('misc'); const run = process.argv[2] || 'r1'
const b = await launch()
for (const [name, url] of [['wp', WP], ['v2', V2]]) {
  const ctx = await newCtx(b, { w: 360, h: 740 }); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(600)
  await p.locator('footer .ffine').scrollIntoViewIfNeeded(); await p.waitForTimeout(500)
  await p.locator('footer .ffine').screenshot({ path: `${out}/${name}-360-ffine-${run}.png` })
  console.log(name, 360, 'ffine', JSON.stringify(await p.evaluate(() => [...document.querySelectorAll('footer .ffine > *')].map(e => ({ tag: e.tagName, h: Math.round(e.getBoundingClientRect().height), w: Math.round(e.getBoundingClientRect().width), text: e.textContent.trim().replace(/\s+/g, ' ').slice(0, 80) })))))
  await ctx.close()
  const c2 = await newCtx(b, { w: 1440, h: 900 }); const q = await c2.newPage()
  await q.goto(url, { waitUntil: 'networkidle' }); await q.waitForTimeout(800)
  const cdp = await c2.newCDPSession(q)
  const live = async () => { const { nodes } = await cdp.send('Accessibility.getFullAXTree'); const n = nodes.find(x => (x.properties || []).some(pp => pp.name === 'live')); const heads = nodes.filter(x => x.role && x.role.value === 'heading' && !x.ignored).map(x => x.name && x.name.value); return { liveNode: n ? { role: n.role.value, name: n.name && n.name.value, live: n.properties.find(pp => pp.name === 'live').value.value } : null, headings: heads.filter(h => ['Maya', 'Devin', 'Priya', 'Cole', 'Jess', 'Tyler', 'Amara', 'Noah', 'Sam'].includes(h)) } }
  console.log(name, 1440, 'before', JSON.stringify(await live()))
  await q.focus('#segs button:nth-child(2)'); await q.keyboard.press('Enter'); await q.waitForTimeout(1500)
  console.log(name, 1440, 'after Enter on segment 2', JSON.stringify(await live()), 'focus', await q.evaluate(() => document.activeElement.getAttribute('aria-label')))
  await c2.close()
}
await b.close()
