// Control for the rotate test: scroll to the creators with the menu closed, turn 768x1024 -> 1024x768, read scrollY.
// Tells whether the scrollY change seen with the menu open comes from the turn itself or from the focus move.
import { launch, newCtx, WP, V2 } from './lib.mjs'
const b = await launch()
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const menu of [false, true]) {
  const ctx = await newCtx(b, { w: 768, h: 1024, phone: false }); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(500)
  await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(400)
  if (menu) { await p.focus('#menu'); await p.keyboard.press('Enter'); await p.waitForTimeout(300); await p.keyboard.press('Tab'); await p.keyboard.press('Tab') }
  const y0 = await p.evaluate(() => Math.round(scrollY)), t0 = await p.evaluate(() => { const e = document.querySelector('.panel.on h2') || document.getElementById('stories'); return e.textContent.trim().slice(0, 20) })
  await p.setViewportSize({ width: 1024, height: 768 }); await p.waitForTimeout(800)
  const r = await p.evaluate(() => ({ y: Math.round(scrollY), storiesTop: Math.round(document.getElementById('stories').getBoundingClientRect().top), wn: document.getElementById('wn').textContent }))
  console.log(`${name} menu ${menu ? 'open, focus Creators' : 'closed'}: scrollY ${y0} -> ${r.y}; stories top after ${r.storiesTop}; counter ${r.wn}`)
  await ctx.close()
}
await b.close()
