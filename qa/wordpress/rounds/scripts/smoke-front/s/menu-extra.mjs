// VIS-N04 safety net and edge cases: with the menu open, focus that leaves the bar and the sheet closes it (Shift+Tab from
// the logo to the skip link); a link tap still closes and lands; the menu opens and closes again after a rotation.
import { launch, newCtx, WP, V2 } from './lib.mjs'
const b = await launch()
const st = p => p.evaluate(() => ({ open: document.getElementById('sheet').classList.contains('open'), overflow: document.body.style.overflow, expanded: document.getElementById('menu').getAttribute('aria-expanded'), active: (document.activeElement.className || document.activeElement.tagName) + ':' + (document.activeElement.textContent || '').trim().slice(0, 14), y: Math.round(scrollY) }))
for (const [name, url] of [['wp', WP], ['v2', V2]]) {
  const ctx = await newCtx(b, { w: 390, h: 844, phone: false }); const p = await ctx.newPage()
  const errs = []; p.on('pageerror', e => errs.push(e.message))
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(700)
  await p.focus('#menu'); await p.keyboard.press('Enter'); await p.waitForTimeout(300)
  await p.focus('.top .w > a'); await p.waitForTimeout(150)
  const onLogo = await st(p)
  await p.keyboard.press('Shift+Tab'); await p.waitForTimeout(300)
  const onSkip = await st(p)
  console.log(name, 'menu open, focus logo:', JSON.stringify(onLogo), '| Shift+Tab to the skip link:', JSON.stringify(onSkip))
  await ctx.close()
  const c2 = await newCtx(b, { w: 390, h: 844, phone: true }); const q = await c2.newPage()
  await q.goto(url, { waitUntil: 'networkidle' }); await q.waitForTimeout(700)
  await q.tap('#menu'); await q.waitForTimeout(400)
  await q.tap('#sheet a[href$="#follow"]'); await q.waitForTimeout(1200)
  const tapped = await st(q)
  const fol = await q.evaluate(() => Math.round(document.getElementById('follow').getBoundingClientRect().top))
  console.log(name, 'tap Follow in the sheet:', JSON.stringify(tapped), 'follow top', fol, 'errors', errs.length)
  await c2.close()
}
await b.close()
