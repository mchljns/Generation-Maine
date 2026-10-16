// Round 2: no-JS desktop stepper. Viewport screenshots at stories 2, 5 and 9, the computed opacity of each story's text,
// and what the phone cards show.
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('nojs'); const run = process.argv[2] || 'r1'
const b = await launch()
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h] of [[1440, 900], [1024, 768], [390, 844]]) {
  const ctx = await newCtx(b, { w, h, js: false }); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(1000)
  const ops = await p.evaluate(() => [...document.querySelectorAll('.panel')].map(pn => { const kids = [...pn.children].filter(c => !c.classList.contains('pv')); return Math.min(...kids.map(c => parseFloat(getComputedStyle(c).opacity))) }))
  const sec = await p.evaluate(() => { const s = document.getElementById('stories'); return { h: s.offsetHeight, menu: getComputedStyle(document.getElementById('menu')).display, pvClipsWithSrc: [...document.querySelectorAll('.panel .pv .clip')].filter(c => c.getAttribute('src')).length, pvShown: [...document.querySelectorAll('.panel .pv')].filter(x => getComputedStyle(x).display !== 'none').length } })
  console.log(name, w, 'lowest text opacity per story', JSON.stringify(ops), JSON.stringify(sec))
  for (const k of [2, 5, 9]) {
    await p.evaluate(k => document.getElementById('story-' + k).scrollIntoView({ behavior: 'instant', block: 'center' }), k); await p.waitForTimeout(400)
    await p.screenshot({ path: `${out}/${name}-${w}-nojs-story${k}-${run}.png` })
  }
  await ctx.close()
}
await b.close()
