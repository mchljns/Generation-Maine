// The phone menu and the scroll position. Scroll to a section, wait (control: does scrollY move by itself?), then open
// the menu by tap and record scrollY per frame; close by tapping Menu again, by Escape. Isolation: set body overflow
// hidden by hand without the menu; open the menu with the stylesheet's scroll-behavior and scroll-padding noted.
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('menuscroll'); const run = process.argv[2] || 'r1'
const b = await launch()
const y = p => p.evaluate(() => Math.round(scrollY))
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h] of [[390, 844], [768, 1024]]) for (const where of ['about', 'stories', 'follow']) {
  const ctx = await newCtx(b, { w, h, phone: true }); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(500)
  await p.evaluate(id => document.getElementById(id).scrollIntoView({ behavior: 'instant' }), where); await p.waitForTimeout(800)
  const y0 = await y(p); await p.waitForTimeout(800); const yc = await y(p)
  // isolation: body overflow hidden by hand
  await p.evaluate(() => { document.body.style.overflow = 'hidden' }); await p.waitForTimeout(300); const yh = await y(p)
  await p.evaluate(() => { document.body.style.overflow = '' }); await p.waitForTimeout(300); const yh2 = await y(p)
  await p.evaluate(id => document.getElementById(id).scrollIntoView({ behavior: 'instant' }), where); await p.waitForTimeout(500); const y00 = await y(p)
  await p.evaluate(() => { window.__ys = []; const t0 = performance.now(); const f = () => { window.__ys.push(Math.round(scrollY)); if (performance.now() - t0 < 700) requestAnimationFrame(f) }; requestAnimationFrame(f) })
  await p.tap('#menu'); await p.waitForTimeout(800)
  const ys = await p.evaluate(() => [...new Set(window.__ys)]), y1 = await y(p)
  await p.screenshot({ path: `${out}/${name}-${w}-${where}-open-${run}.png` })
  await p.tap('#menu'); await p.waitForTimeout(500); const y2 = await y(p)
  await p.screenshot({ path: `${out}/${name}-${w}-${where}-closed-${run}.png` })
  const sec = await p.evaluate(() => { const c = innerHeight / 2; return [...document.querySelectorAll('main > *, main section')].map(s => [s.id || s.className.split(' ')[0], s.getBoundingClientRect()]).filter(([, r]) => r.top <= c && r.bottom >= c).map(([n]) => n).join(',') })
  console.log(`${name} ${w}x${h} at #${where}: scrollY ${y0}, after 0.8s idle ${yc}; body overflow hidden by hand ${yh}, cleared ${yh2} | menu tap: ${y00} -> frames ${ys.join(',')} -> open ${y1} -> closed by Menu ${y2} (mid-screen now: ${sec})`)
  await ctx.close()
}
await b.close()
