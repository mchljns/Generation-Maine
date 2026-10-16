// Does opening the phone menu move the page? Scroll to the creators, then open the menu by tap, by focus+Enter, and by
// Tab to the menu button + Enter; read scrollY before, while open, and after Escape. Also the turn with the menu open.
import { launch, newCtx, WP, V2 } from './lib.mjs'
const b = await launch()
const y = p => p.evaluate(() => Math.round(scrollY))
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h, touch] of [[390, 844, true], [768, 1024, true], [768, 1024, false]]) for (const how of touch ? ['tap'] : ['focus', 'click']) {
  const ctx = await newCtx(b, { w, h, phone: touch }); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(500)
  await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(500)
  const y0 = await y(p)
  if (how === 'tap') await p.tap('#menu'); else if (how === 'click') await p.click('#menu'); else { await p.focus('#menu'); await p.waitForTimeout(200); var yf = await y(p); await p.keyboard.press('Enter') }
  await p.waitForTimeout(500); const y1 = await y(p)
  await p.keyboard.press('Escape'); await p.waitForTimeout(400); const y2 = await y(p)
  console.log(`${name} ${w}x${h} ${how}: scrollY ${y0}${how === 'focus' ? ' -> after focus() ' + yf : ''} -> open ${y1} -> after Escape ${y2}`)
  await ctx.close()
}
await b.close()
