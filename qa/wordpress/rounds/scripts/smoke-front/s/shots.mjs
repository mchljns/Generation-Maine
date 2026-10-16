// Screenshots for the record: the carousel's last three resting places at 768x1024 and 844x390 (VIS-N05), the duration
// chip over Maya's bright frame at 390 and on the 1440 stage (VIS-N06), the open menu after Tab wraps (VIS-N04).
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('shots')
const b = await launch()
for (const [name, url] of [['wp', WP], ['v2', V2]]) {
  for (const [w, h] of [[768, 1024], [844, 390]]) {
    const ctx = await newCtx(b, { w, h, phone: true }); const p = await ctx.newPage()
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(700)
    for (const k of [7, 8, 9]) {
      await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(300)
      await p.tap(`#segs button:nth-child(${k})`); await p.waitForTimeout(1300)
      await p.screenshot({ path: `${out}/${name}-${w}x${h}-card${k}.png` })
    }
    await ctx.close()
  }
  {
    const ctx = await newCtx(b, { w: 390, h: 844, phone: true }); const p = await ctx.newPage()
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(700)
    await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(1200)
    await p.locator('#story-1 .pv').screenshot({ path: `${out}/${name}-390-card1.png` })
    await ctx.close()
  }
  {
    const ctx = await newCtx(b, { w: 1440, h: 900 }); const p = await ctx.newPage()
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(700)
    const g = await p.evaluate(() => { const s = document.getElementById('stories'); return { top: s.offsetTop, total: s.offsetHeight - innerHeight } })
    await p.evaluate(({ y }) => scrollTo({ top: y, behavior: 'instant' }), { y: Math.round(g.top + 0.5 / 9 * g.total) }); await p.waitForTimeout(1300)
    await p.locator('#stage').screenshot({ path: `${out}/${name}-1440-stage1.png` })
    await ctx.close()
  }
  {
    const ctx = await newCtx(b, { w: 390, h: 844, phone: false }); const p = await ctx.newPage()
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(700)
    await p.focus('#menu'); await p.keyboard.press('Enter'); await p.waitForTimeout(400)
    for (let i = 0; i < 5; i++) { await p.keyboard.press('Tab'); await p.waitForTimeout(150) }
    await p.waitForTimeout(300)
    await p.screenshot({ path: `${out}/${name}-390-menu-tab5.png` })
    await ctx.close()
  }
}
await b.close()
