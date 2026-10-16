import { launch, newCtx, WP, V2 } from './lib.mjs'
const b = await launch()
const sections = [['bar', '.top'], ['hero', '#top'], ['about', '#about'], ['head', '#creators'], ['stories', '#stories'], ['follow', '#follow'], ['footer', 'footer']]
for (const [w, h] of [[320, 568], [360, 740], [390, 844]]) for (const [name, url] of [['wp', WP], ['v2', V2]]) {
  const ctx = await newCtx(b, { w, h }); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(800)
  const g = await p.evaluate(sections => Object.fromEntries(sections.map(([k, s]) => [k, Math.round(document.querySelector(s).getBoundingClientRect().height)]).concat([['page', document.documentElement.scrollHeight], ['where', Math.round(document.querySelector('.where').getBoundingClientRect().height)], ['footerLines', [...document.querySelectorAll('footer p')].map(p => Math.round(p.getBoundingClientRect().height)).join('/')]])), sections)
  console.log(w, name, JSON.stringify(g))
  await ctx.close()
}
await b.close()
