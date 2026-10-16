import { launch, newCtx, WP } from './lib.mjs'
const b = await launch(); const ctx = await newCtx(b, { w: +process.env.W || 480, h: 900, phone: false, dsf: 1 }); const p = await ctx.newPage()
await p.goto(WP + '?gmh=' + (process.env.K || 'url'), { waitUntil: 'networkidle' }); await p.waitForTimeout(1500)
console.log(JSON.stringify(await p.evaluate(() => { const h1 = document.querySelector('.hero h1'), r = h1.getBoundingClientRect(), c = h1.parentElement.getBoundingClientRect(); const d = h1.querySelector('.d').getBoundingClientRect(); const s = h1.querySelector('.here').getClientRects(); return { fs: getComputedStyle(h1).fontSize, h1: [r.left, r.right, r.width, r.height], col: [c.left, c.right], dot: [d.left, d.top, d.bottom], hereRects: [...s].map(x => [Math.round(x.left), Math.round(x.top), Math.round(x.right), Math.round(x.bottom)]), sw: h1.scrollWidth, vw: innerWidth } })))
await p.screenshot({ path: '/tmp/claude-0/wptest/work/r4-front/dotsweep/dbg-' + (process.env.K || 'url') + '-' + (process.env.W || 480) + '.png' })
await b.close()
