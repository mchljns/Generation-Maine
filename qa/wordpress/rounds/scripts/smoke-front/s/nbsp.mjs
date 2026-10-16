// ED-R5 risk: a pasted run of 9000 no-break spaces in the headline. Page overflow, h1 height and the dot at 390 and 1440.
import { launch, newCtx, WP, dir } from './lib.mjs'
const out = dir('nbsp'); const run = process.argv[2] || 'r1'
const b = await launch()
for (const [w, h] of [[390, 844], [1440, 900]]) {
  const ctx = await newCtx(b, { w, h, phone: w < 900 }); const p = await ctx.newPage()
  await p.goto(WP + '?gmh=nbsp9000', { waitUntil: 'networkidle' }); await p.waitForTimeout(1200)
  const r = await p.evaluate(() => { const h1 = document.querySelector('.hero h1'), r = h1.getBoundingClientRect(); return { overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth, h1h: Math.round(r.height), heroH: Math.round(document.querySelector('.hero').getBoundingClientRect().height), dots: h1.querySelectorAll('.d').length, gold: [...h1.querySelectorAll('.here')].map(s => s.textContent) } })
  console.log(w, JSON.stringify(r))
  await p.screenshot({ path: `${out}/nbsp9000-${w}-${run}.png` })
  await ctx.close()
}
await b.close()
