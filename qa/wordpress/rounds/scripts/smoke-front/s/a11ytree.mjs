import { launch, newCtx, WP, V2, dir } from './lib.mjs'
import { writeFileSync } from 'node:fs'
const out = dir('a11y')
const run = process.argv[2] || 'r1'
const b = await launch()
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h] of [[1440, 900], [390, 844]]) {
  const ctx = await newCtx(b, { w, h }); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(800)
  const snap = await p.locator('body').ariaSnapshot()
  writeFileSync(`${out}/${name}-${w}-aria-${run}.yaml`, snap)
  const h2 = (snap.match(/heading "[^"]*" \[level=2\]/g) || [])
  const bios = ['I grew up here', 'I wanted to sell coffee', 'Half of my graduating', 'Forty minutes', 'I moved back in', 'First lease', 'One job pays', 'I am finishing', 'Landscaping stops'].filter(t => snap.includes(t)).length
  const live = await p.evaluate(() => [...document.querySelectorAll('[aria-live],[role=status],[role=log]')].map(e => e.id || e.className))
  console.log(name, w, 'level-2 headings in a11y tree:', h2.length, h2.join(' | '), '| creator bios exposed:', bios, '/9 | live regions:', JSON.stringify(live))
  await ctx.close()
}
await b.close()
