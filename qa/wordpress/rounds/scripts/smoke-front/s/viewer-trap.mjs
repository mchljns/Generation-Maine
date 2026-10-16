import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('viewer')
const run = process.argv[2] || 'r1'
const b = await launch()
for (const [name, url] of [['wp', WP], ['v2', V2]]) {
  const ctx = await newCtx(b, { w: 390, h: 844 })
  const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(800)
  await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(400)
  await p.focus('#story-5 .pv'); await p.keyboard.press('Enter'); await p.waitForTimeout(700)
  const seq = []
  for (let i = 0; i < 8; i++) {
    await p.keyboard.press('Tab'); await p.waitForTimeout(80)
    seq.push(await p.evaluate(() => { const a = document.activeElement, v = document.getElementById('viewer'); const r = a.getBoundingClientRect(); const top = document.elementFromPoint(Math.max(0, Math.min(innerWidth - 1, r.left + r.width / 2)), Math.max(0, Math.min(innerHeight - 1, r.top + r.height / 2))); return `${a.tagName}${a.id ? '#' + a.id : ''} "${(a.getAttribute('aria-label') || a.textContent || '').trim().slice(0, 24)}" inViewer=${v.contains(a)} onscreen=${r.bottom > 0 && r.top < innerHeight} coveredByViewer=${!!(top && v.contains(top) && !v.contains(a))}` }))
  }
  console.log(name, 'tab from close button inside open viewer:\n  ' + seq.join('\n  '))
  await p.screenshot({ path: `${out}/${name}-tab-escape-${run}.png` })
  await p.keyboard.press('Escape'); await p.waitForTimeout(600)
  // arrow to other creator then close: where is focus
  await p.focus('#story-5 .pv'); await p.keyboard.press('Enter'); await p.waitForTimeout(700)
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(800); await p.keyboard.press('ArrowRight'); await p.waitForTimeout(800)
  await p.keyboard.press('Escape'); await p.waitForTimeout(1200)
  console.log(name, 'after arrows+escape', await p.evaluate(() => { const a = document.activeElement, r = a.getBoundingClientRect(); return { active: a.getAttribute('aria-label'), left: Math.round(r.left), right: Math.round(r.right), vw: innerWidth, wn: document.getElementById('wn').textContent } }))
  await p.screenshot({ path: `${out}/${name}-focus-after-arrows-${run}.png` })
  await ctx.close()
}
await b.close()
