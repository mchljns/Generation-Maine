import { launch, newCtx, WP, dir } from './lib.mjs'
const out = dir('viewer')
const run = process.argv[2] || 'r1'
const b = await launch()
for (const [w, h] of [[320, 568], [390, 844], [430, 932], [844, 390], [768, 1024]]) {
  const ctx = await newCtx(b, { w, h }); const p = await ctx.newPage()
  await p.goto(WP, { waitUntil: 'networkidle' }); await p.waitForTimeout(500)
  await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(400)
  await p.tap('.panel.on .pv'); await p.waitForTimeout(800)
  const r = await p.evaluate(() => { const g = s => { const r = document.querySelector(s).getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)] }; return { vw: innerWidth, vh: innerHeight, close: g('#vclose'), vn: g('#vn'), fr: g('#vtrack .slide .fr'), cap: g('#vtrack .slide .cap'), ratio: +(document.querySelector('#vtrack .slide .fr').getBoundingClientRect().width / document.querySelector('#vtrack .slide .fr').getBoundingClientRect().height).toFixed(3) } })
  const fits = r.fr[1] >= 0 && r.fr[3] <= r.vh && r.cap[3] <= r.vh && r.close[3] <= r.vh && r.fr[0] >= 0 && r.fr[2] <= r.vw
  console.log(`${w}x${h}`, JSON.stringify(r), 'fits', fits)
  await p.screenshot({ path: `${out}/size-${w}x${h}-${run}.png` })
  await ctx.close()
}
await b.close()
