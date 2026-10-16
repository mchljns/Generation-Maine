import { launch, newCtx, WP, V2 } from './lib.mjs'
const b = await launch()
for (const url of [WP, V2]) for (const w of [390, 1440]) {
  const ctx = await newCtx(b, { w, h: w < 900 ? 844 : 900 })
  const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' })
  await p.waitForTimeout(500)
  const r = await p.evaluate(() => {
    const vis = e => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' }
    const out = []
    for (const e of document.querySelectorAll('h1,h2,h3,p,a,button,span,li,b,strong,input,label')) {
      if (!vis(e)) continue
      const ff = getComputedStyle(e).fontFamily
      if (/^"?Arial|^sans-serif|^system-ui|^-apple/i.test(ff)) out.push([e.tagName + '.' + e.className, (e.textContent || '').trim().slice(0, 30), ff])
    }
    const loaded = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight + ' ' + f.style)
    return { out: out.slice(0, 20), loaded, all: [...document.fonts].map(f => f.family + ' ' + f.weight + ' ' + f.status) }
  })
  console.log(url, w, JSON.stringify(r, null, 1))
  await ctx.close()
}
await b.close()
