import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('compare')
const run = process.argv[2] || 'r1'
const b = await launch()
const sections = [['bar', '.top'], ['hero', '#top'], ['about', '#about'], ['creators-head', '#creators'], ['stories', '#stories'], ['follow', '#follow'], ['footer', 'footer']]
const geo = {}
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h] of [[1440, 900], [390, 844]]) {
  const ctx = await newCtx(b, { w, h, reduced: true })
  const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(1500)
  // load the first clip on the stage, then trigger the footer draw, then return to top
  await p.evaluate(() => window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'instant' })); await p.waitForTimeout(600)
  await p.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' })); await p.waitForTimeout(800)
  await p.screenshot({ path: `${out}/${name}-${w}-full-${run}.png`, fullPage: true })
  geo[`${name}-${w}`] = await p.evaluate((sections) => Object.fromEntries(sections.map(([k, s]) => { const e = document.querySelector(s); const r = e.getBoundingClientRect(); return [k, { top: Math.round(r.top + scrollY), h: Math.round(r.height) }] })), sections)
  for (const [k, s] of sections) {
    if (k === 'stories') { await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(800); await p.screenshot({ path: `${out}/${name}-${w}-${k}-${run}.png` }); continue }
    await p.locator(s).first().screenshot({ path: `${out}/${name}-${w}-${k}-${run}.png` }).catch(e => console.log('shot fail', k, e.message))
  }
  await ctx.close()
}
console.log(JSON.stringify(geo, null, 0))
await b.close()
