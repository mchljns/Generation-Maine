import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('reduced')
const run = process.argv[2] || 'r1'
const b = await launch()
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h] of [[1440, 900], [390, 844]]) {
  const ctx = await newCtx(b, { w, h, reduced: true })
  const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(300)
  const r = await p.evaluate(() => {
    const anims = document.getAnimations().map(a => ({ name: a.animationName || a.transitionProperty || a.constructor.name, target: (a.effect && a.effect.target) ? (a.effect.target.className && a.effect.target.className.baseVal !== undefined ? a.effect.target.className.baseVal : a.effect.target.className) + (a.effect.pseudoElement || '') : '', iterations: a.effect && a.effect.getTiming().iterations, state: a.playState }))
    const infinite = anims.filter(a => a.iterations === Infinity && a.state === 'running')
    const paths = [...document.querySelectorAll('#mural path')]
    const mural = { paths: paths.length, offsets: [...new Set(paths.map(p => getComputedStyle(p).strokeDashoffset))].slice(0, 5), transitions: [...new Set(paths.map(p => getComputedStyle(p).transitionDuration))].slice(0, 3) }
    const dot = document.querySelector('.hero .d'), da = dot ? getComputedStyle(dot, '::after').animationName : null, db = dot ? getComputedStyle(dot).animationName : null
    const hiddenText = [...document.querySelectorAll('main h1, main h2, main h3, main p, main a, footer p, footer a')].filter(e => { const cs = getComputedStyle(e); const r = e.getBoundingClientRect(); return r.width > 0 && (parseFloat(cs.opacity) < 0.99 || cs.visibility === 'hidden') && !e.closest('.panel:not(.on)') && !e.closest('.viewer') && !e.closest('#stage .who:not(.on)') }).map(e => e.tagName + '.' + e.className + ' op=' + getComputedStyle(e).opacity + ' "' + e.textContent.trim().slice(0, 20) + '"')
    const rise = [...document.querySelectorAll('.rise')].map(e => getComputedStyle(e).opacity + '/' + getComputedStyle(e).transform)
    const smooth = getComputedStyle(document.documentElement).scrollBehavior
    return { anims: anims.length, infinite, mural, dotAnim: [db, da], rise, hiddenText: hiddenText.slice(0, 10), smooth }
  })
  console.log(name, w, JSON.stringify(r, null, 0))
  // after scrolling to the end: footer mark drawn, panel content visible
  await p.evaluate(() => window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'instant' })); await p.waitForTimeout(400)
  const f = await p.evaluate(() => { const ps = [...document.querySelectorAll('.site .lk path[stroke]')]; return { footerPaths: ps.length, offsets: [...new Set(ps.map(p => getComputedStyle(p).strokeDashoffset))], infinite: document.getAnimations().filter(a => a.effect.getTiming().iterations === Infinity && a.playState === 'running').length } })
  console.log(name, w, 'footer', JSON.stringify(f))
  await p.screenshot({ path: `${out}/${name}-${w}-footer-${run}.png` })
  await p.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' })); await p.waitForTimeout(200)
  await p.screenshot({ path: `${out}/${name}-${w}-hero-${run}.png` })
  await ctx.close()
}
// and no-preference for contrast
for (const [name, url] of [['wp', WP]]) {
  const ctx = await newCtx(b, { w: 1440, h: 900 })
  const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(2500)
  console.log(name, 'no-preference infinite anims', JSON.stringify(await p.evaluate(() => document.getAnimations().filter(a => a.effect.getTiming().iterations === Infinity).map(a => (a.animationName || '') + ' on ' + a.effect.target.className + (a.effect.pseudoElement || '')))))
  await ctx.close()
}
await b.close()
