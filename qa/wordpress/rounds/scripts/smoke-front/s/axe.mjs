import { launch, newCtx, WP, V2, dir } from './lib.mjs'
import { writeFileSync } from 'node:fs'
const AXE = '/home/user/Generation-Maine/node_modules/axe-core/axe.min.js'
const out = dir('axe')
const run = process.argv[2] || 'r1'
const b = await launch()
const tags = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice']
const summary = {}
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const w of [390, 1440]) for (const state of (w < 900 ? ['closed', 'menu', 'viewer'] : ['closed'])) {
  const ctx = await newCtx(b, { w, h: w < 900 ? 844 : 900 })
  const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' })
  await p.waitForTimeout(1500)
  if (state === 'menu') { await p.tap('#menu'); await p.waitForTimeout(500) }
  if (state === 'viewer') { await p.locator('#story-1 .pv').scrollIntoViewIfNeeded(); await p.tap('#story-1 .pv'); await p.waitForTimeout(800) }
  await p.addScriptTag({ path: AXE })
  const res = await p.evaluate(async (tags) => {
    const r = await axe.run(document, { runOnly: { type: 'tag', values: tags }, resultTypes: ['violations', 'incomplete'] })
    const m = v => ({ id: v.id, impact: v.impact, tags: v.tags.filter(t => /wcag|best/.test(t)).join(','), help: v.help, nodes: v.nodes.map(n => ({ target: n.target.join(' '), html: n.html.slice(0, 160), summary: (n.failureSummary || '').slice(0, 300) })) })
    return { violations: r.violations.map(m), incomplete: r.incomplete.map(m) }
  }, tags)
  const key = `${name}-${w}-${state}`
  writeFileSync(`${out}/${key}-${run}.json`, JSON.stringify(res, null, 1))
  await p.screenshot({ path: `${out}/${key}-${run}.png` })
  summary[key] = { violations: res.violations.map(v => `${v.id}(${v.impact},${v.nodes.length})`), incomplete: res.incomplete.map(v => `${v.id}(${v.nodes.length})`) }
  await ctx.close()
}
console.log(JSON.stringify(summary, null, 1))
await b.close()
