// Round 4: axe-core (WCAG 2.2 AA plus best practice) on the front page at the eight sizes, closed; with the menu open at
// phone and tablet sizes; the viewer open at 390. WP and the local v2 page.
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
import { writeFileSync } from 'node:fs'
const AXE = '/home/user/Generation-Maine/node_modules/axe-core/axe.min.js'
const out = dir('axe8'); const run = process.argv[2] || 'r1'
const sizes = (process.env.SIZES || '320x568,390x844,414x896,430x932,768x1024,844x390,1024x768,1440x900').split(',').map(s => s.split('x').map(Number))
const targets = (process.env.TARGETS || 'wp,v2').split(',')
const b = await launch()
const tags = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice']
for (const name of targets) for (const [w, h] of sizes) for (const state of (w <= 900 ? (w === 390 ? ['closed', 'menu', 'viewer'] : ['closed', 'menu']) : ['closed'])) {
  const url = name === 'wp' ? WP : V2
  const ctx = await newCtx(b, { w, h, phone: w <= 900 }); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(1500)
  if (state === 'menu') { await p.tap('#menu'); await p.waitForTimeout(500) }
  if (state === 'viewer') { await p.locator('#story-1 .pv').scrollIntoViewIfNeeded(); await p.tap('#story-1 .pv'); await p.waitForTimeout(800) }
  await p.addScriptTag({ path: AXE })
  const res = await p.evaluate(async (tags) => {
    const r = await axe.run(document, { runOnly: { type: 'tag', values: tags }, resultTypes: ['violations', 'incomplete'] })
    const m = v => ({ id: v.id, impact: v.impact, help: v.help, nodes: v.nodes.map(n => ({ target: n.target.join(' '), html: n.html.slice(0, 160), summary: (n.failureSummary || '').slice(0, 300) })) })
    return { violations: r.violations.map(m), incomplete: r.incomplete.map(m) }
  }, tags)
  const key = `${name}-${w}x${h}-${state}`
  writeFileSync(`${out}/${key}-${run}.json`, JSON.stringify(res, null, 1))
  console.log(key, 'violations', JSON.stringify(res.violations.map(v => `${v.id}(${v.impact},${v.nodes.length}: ${v.nodes.map(n => n.target).join(' ; ').slice(0, 120)})`)), 'incomplete', JSON.stringify(res.incomplete.map(v => `${v.id}(${v.nodes.length})`)))
  await ctx.close()
}
await b.close()
