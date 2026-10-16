// Before/after for the rotation scroll: the same finger-tap-and-turn on WordPress, with the page script as served (this build)
// and with the round 3 build's site.js (git 3672e10) swapped in through a route. Only the script differs.
import { launch, newCtx, WP } from './lib.mjs'
import { readFileSync } from 'node:fs'
const old = readFileSync('/tmp/claude-0/wptest/work/r4-front/site-r3build.js', 'utf8')
const b = await launch()
const ftap = async (ctx, p, sel) => { const cdp = await ctx.newCDPSession(p); const bx = await p.evaluate(s => { const r = document.querySelector(s).getBoundingClientRect(); return [Math.round(r.left + r.width / 2), Math.round(r.top + r.height / 2)] }, sel); await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: bx[0], y: bx[1] }] }); await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }) }
for (const which of ['this build', 'round 3 build']) for (const r of [1, 2]) {
  const ctx = await newCtx(b, { w: 768, h: 1024, phone: true })
  if (which !== 'this build') await ctx.route('**/assets/js/site.js*', route => route.fulfill({ status: 200, contentType: 'text/javascript', body: old }))
  const p = await ctx.newPage(); await p.goto(WP, { waitUntil: 'networkidle' }); await p.waitForTimeout(500)
  await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(600)
  const y0 = await p.evaluate(() => Math.round(scrollY)); await ftap(ctx, p, '#menu'); await p.waitForTimeout(600)
  await p.setViewportSize({ width: 1024, height: 768 }); await p.waitForTimeout(1200)
  const s = await p.evaluate(() => ({ y: Math.round(scrollY), open: document.getElementById('sheet').classList.contains('open'), focus: (document.activeElement.textContent || document.activeElement.tagName).trim().slice(0, 12), storiesTop: Math.round(document.getElementById('stories').getBoundingClientRect().top), held: typeof held }))
  await p.screenshot({ path: `/tmp/claude-0/wptest/work/r4-front/rot4/turn-scroll-${which.replace(/ /g, '')}-r${r}.png` })
  console.log(`${which} run ${r}: at the creators scrollY ${y0}, finger tap Menu, turn 768x1024 -> 1024x768: scrollY ${s.y}, sheet open ${s.open}, focus ${s.focus}, stories top ${s.storiesTop}`)
  await ctx.close()
}
await b.close()
