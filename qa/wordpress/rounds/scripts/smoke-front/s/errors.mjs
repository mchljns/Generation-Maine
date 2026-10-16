import { launch, newCtx, WP, dir, watch } from './lib.mjs'
const out = dir('errors')
const run = process.argv[2] || 'r1'
const b = await launch()
for (const [w, h] of [[1440, 900], [390, 844]]) {
  const ctx = await newCtx(b, { w, h })
  const p = await ctx.newPage()
  const log = watch(p)
  await p.goto(WP, { waitUntil: 'networkidle' }); await p.waitForTimeout(800)
  const H = await p.evaluate(() => document.documentElement.scrollHeight)
  for (let y = 0; y < H; y += 400) { await p.evaluate(y => window.scrollTo({ top: y, behavior: 'instant' }), y); await p.waitForTimeout(120) }
  if (w < 900) {
    await p.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' }))
    await p.tap('#menu'); await p.waitForTimeout(300); await p.keyboard.press('Escape')
    await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(400)
    await p.tap('#story-1 .pv'); await p.waitForTimeout(600)
    for (let i = 0; i < 9; i++) { await p.keyboard.press('ArrowRight'); await p.waitForTimeout(350) }
    await p.keyboard.press('Escape'); await p.waitForTimeout(400)
  }
  await p.waitForTimeout(800)
  // also hit the 404 page and a creator URL guess
  const uniq = [...new Set(log.requests)]
  const insecure = uniq.filter(u => u.startsWith('http:') && !u.startsWith('http://127.0.0.1:8901/'))
  const external = uniq.filter(u => !u.startsWith('http://127.0.0.1:8901/') && !u.startsWith('data:'))
  console.log(w, JSON.stringify({ requests: uniq.length, console: log.console, pageerrors: log.pageerrors, failed: log.failed, bad: log.bad, insecureExternal: insecure, external }, null, 1))
  await ctx.close()
}
// 404 page and favicon
const ctx = await newCtx(b, { w: 1440, h: 900 })
const p = await ctx.newPage(); const log = watch(p)
const r = await p.goto('http://127.0.0.1:8901/no-such-page/', { waitUntil: 'networkidle' })
console.log('404 page status', r.status(), JSON.stringify({ console: log.console, pageerrors: log.pageerrors, bad: log.bad.filter(x => !x.includes('no-such-page')), failed: log.failed }))
await p.screenshot({ path: `${out}/404-${run}.png`, fullPage: true })
await ctx.close()
await b.close()
