// Round 3, V05 variations: JavaScript off at the six sizes. Lowest text opacity per story, section height, menu button,
// stage and position row, visible stories; screenshots of stories 2, 5 and 9.
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('nojs6'); const run = process.argv[2] || 'r1'
const b = await launch()
const sizes = [[320, 568], [390, 844], [768, 1024], [844, 390], [1024, 768], [1440, 900]]
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h] of sizes) {
  const ctx = await newCtx(b, { w, h, js: false, phone: w <= 900 }); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(800)
  const r = await p.evaluate(() => {
    const panels = [...document.querySelectorAll('.panel')]
    const ops = panels.map(pn => { const kids = [...pn.querySelectorAll('h2,.bio,.k')]; return Math.min(...kids.map(c => { let o = 1; for (let e = c; e && e !== document.body; e = e.parentElement) o *= parseFloat(getComputedStyle(e).opacity); return +o.toFixed(2) })) })
    const vis = panels.map(pn => { const h2 = pn.querySelector('h2'), r = h2.getBoundingClientRect(); return r.height > 0 && getComputedStyle(h2).visibility !== 'hidden' ? 1 : 0 })
    const s = document.getElementById('stories')
    const overflowX = document.documentElement.scrollWidth - innerWidth
    const hiddenFoot = [...document.querySelectorAll('footer a, footer p')].filter(e => { const r = e.getBoundingClientRect(); return r.height === 0 || parseFloat(getComputedStyle(e).opacity) === 0 }).length
    const riseHidden = [...document.querySelectorAll('.rise')].filter(e => parseFloat(getComputedStyle(e).opacity) < 0.5).length
    const stillShown = [...document.querySelectorAll('.panel .pv')].filter(x => getComputedStyle(x).display !== 'none').length
    return { ops, vis: vis.join(''), storiesH: s.offsetHeight, docH: document.documentElement.scrollHeight, menu: getComputedStyle(document.getElementById('menu')).display, stage: document.getElementById('stage') ? getComputedStyle(document.getElementById('stage')).display : 'none', where: document.querySelector('.where') ? getComputedStyle(document.querySelector('.where')).display : '-', overflowX, hiddenFoot, riseHidden, pvShown: stillShown, h1: !!document.querySelector('h1').getBoundingClientRect().height }
  })
  console.log(name, `${w}x${h}`, JSON.stringify(r))
  for (const k of [2, 5, 9]) {
    await p.evaluate(k => document.getElementById('story-' + k).scrollIntoView({ behavior: 'instant', block: 'center' }), k); await p.waitForTimeout(300)
    await p.screenshot({ path: `${out}/${name}-${w}x${h}-story${k}-${run}.png` })
  }
  await ctx.close()
}
await b.close()
