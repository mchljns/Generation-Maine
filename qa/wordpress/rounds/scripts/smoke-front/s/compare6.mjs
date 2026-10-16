// Round 3: WP against the local v2 at the six sizes, reduced motion for stable frames. Section geometry and screenshots.
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
import { writeFileSync } from 'node:fs'
const out = dir('compare6'); const run = process.argv[2] || 'r1'
const b = await launch()
const sections = [['bar', '.top'], ['hero', '#top'], ['about', '#about'], ['creators-head', '#creators'], ['stories', '#stories'], ['follow', '#follow'], ['footer', 'footer']]
const geo = {}
const sizes = (process.env.SIZES || '320x568,390x844,768x1024,844x390,1024x768,1440x900').split(',').map(s => s.split('x').map(Number))
for (const [w, h] of sizes) for (const [name, url] of [['wp', WP], ['v2', V2]]) {
  const ctx = await newCtx(b, { w, h, reduced: true }); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(1200)
  await p.evaluate(() => scrollTo({ top: document.documentElement.scrollHeight, behavior: 'instant' })); await p.waitForTimeout(700)
  await p.evaluate(() => scrollTo({ top: 0, behavior: 'instant' })); await p.waitForTimeout(700)
  geo[`${name}-${w}x${h}`] = await p.evaluate(sections => Object.fromEntries(sections.map(([k, s]) => { const e = document.querySelector(s); const r = e.getBoundingClientRect(); return [k, { top: Math.round(r.top + scrollY), h: Math.round(r.height) }] }).concat([['doc', document.documentElement.scrollHeight]])), sections)
  for (const [k, s] of sections) {
    if (k === 'stories') { await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(900); await p.screenshot({ path: `${out}/${name}-${w}x${h}-${k}-${run}.png` }); continue }
    await p.locator(s).first().scrollIntoViewIfNeeded(); await p.waitForTimeout(300)
    await p.locator(s).first().screenshot({ path: `${out}/${name}-${w}x${h}-${k}-${run}.png` }).catch(e => console.log('shot fail', k, e.message))
  }
  await ctx.close()
}
writeFileSync(`${out}/geo-${run}.json`, JSON.stringify(geo, null, 1))
for (const [w, h] of sizes) { const a = geo[`wp-${w}x${h}`], v = geo[`v2-${w}x${h}`]; console.log(`${w}x${h}`, Object.keys(a).map(k => k === 'doc' ? `doc ${a[k]}/${v[k]}` : `${k} ${a[k].h}/${v[k].h}${a[k].h !== v[k].h ? '*' : ''}`).join('  ')) }
await b.close()
