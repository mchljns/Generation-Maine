// Round 3: axe-core (WCAG 2.2 AA + best practice) at the six sizes, WP and v2. Phones: closed, menu open, viewer open, paused.
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
import { writeFileSync } from 'node:fs'
const AXE = '/home/user/Generation-Maine/node_modules/axe-core/axe.min.js'
const out = dir('axe'); const run = process.argv[2] || 'r1'
const b = await launch()
const tags = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice']
const summary = {}
const sizes = [[320, 568], [390, 844], [768, 1024], [844, 390], [1024, 768], [1440, 900]]
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h] of sizes) {
  const phone = w <= 900
  for (const state of (phone ? ['closed', 'menu', 'viewer', 'paused'] : ['closed', 'paused', 'stage5'])) {
    const ctx = await newCtx(b, { w, h, phone }); const p = await ctx.newPage()
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(1200)
    if (state === 'menu') { await p.tap('#menu'); await p.waitForTimeout(500) }
    if (state === 'viewer') { await p.locator('#story-1 .pv').scrollIntoViewIfNeeded(); await p.tap('#story-1 .pv'); await p.waitForTimeout(800) }
    if (state === 'paused') { await p.locator('#cpause').scrollIntoViewIfNeeded(); await p.locator('#cpause').click(); await p.waitForTimeout(500) }
    if (state === 'stage5') { await p.evaluate(() => { const s = document.getElementById('stories'); scrollTo(0, s.offsetTop + 4.5 / 9 * (s.offsetHeight - innerHeight)) }); await p.waitForTimeout(1000) }
    await p.addScriptTag({ path: AXE })
    const res = await p.evaluate(async (tags) => {
      const r = await axe.run(document, { runOnly: { type: 'tag', values: tags }, resultTypes: ['violations', 'incomplete'] })
      const m = v => ({ id: v.id, impact: v.impact, help: v.help, nodes: v.nodes.map(n => ({ target: n.target.join(' '), html: n.html.slice(0, 160), summary: (n.failureSummary || '').slice(0, 300) })) })
      return { violations: r.violations.map(m), incomplete: r.incomplete.map(m) }
    }, tags)
    const key = `${name}-${w}x${h}-${state}`
    writeFileSync(`${out}/${key}-${run}.json`, JSON.stringify(res, null, 1))
    summary[key] = { v: res.violations.map(v => `${v.id}(${v.impact},${v.nodes.length}: ${v.nodes.map(n => n.target).join(' ; ').slice(0, 80)})`), inc: res.incomplete.map(v => `${v.id}(${v.nodes.length})`) }
    console.log(key, JSON.stringify(summary[key]))
    await ctx.close()
  }
}
await b.close()
