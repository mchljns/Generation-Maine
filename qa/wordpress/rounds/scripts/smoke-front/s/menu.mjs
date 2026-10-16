import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('menu')
const run = process.argv[2] || 'r1'
const b = await launch()
const st = p => p.evaluate(() => {
  const s = document.getElementById('sheet'), m = document.getElementById('menu'), a = document.activeElement
  const cs = getComputedStyle(s)
  let desc = a ? (a.tagName + (a.id ? '#' + a.id : '') + (a.getAttribute('href') ? '[' + a.getAttribute('href') + ']' : '') + ' ' + (a.textContent || '').trim().slice(0, 20)) : null
  const inSheet = a && s.contains(a), inTop = a && document.querySelector('.top').contains(a)
  const ar = a && a.getBoundingClientRect ? a.getBoundingClientRect() : null
  return { open: s.classList.contains('open'), ariaHidden: s.getAttribute('aria-hidden'), expanded: m.getAttribute('aria-expanded'), opacity: cs.opacity, bodyOverflow: document.body.style.overflow, active: desc, inSheet, inTop, activeVisible: ar ? (ar.width > 0 && getComputedStyle(a).visibility !== 'hidden' && !(inSheet && cs.opacity === '0')) : null, activeTop: ar ? Math.round(ar.top) : null, scrollY: Math.round(scrollY) }
})
for (const [name, url] of [['wp', WP], ['v2', V2]]) {
  const ctx = await newCtx(b, { w: 390, h: 844 })
  const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(800)
  const log = (k, v) => console.log(name, k, JSON.stringify(v))
  log('initial', await st(p))
  await p.tap('#menu'); await p.waitForTimeout(400)
  log('tap open', await st(p))
  await p.screenshot({ path: `${out}/${name}-open-${run}.png` })
  await p.tap('#menu'); await p.waitForTimeout(400)
  log('tap menu again (close)', await st(p))
  await p.tap('#menu'); await p.waitForTimeout(400)
  await p.keyboard.press('Escape'); await p.waitForTimeout(400)
  log('escape', await st(p))
  // keyboard: focus the menu button and press Enter
  await p.focus('#menu'); await p.keyboard.press('Enter'); await p.waitForTimeout(400)
  log('kbd enter open', await st(p))
  const seq = []
  for (let i = 0; i < 6; i++) { await p.keyboard.press('Tab'); await p.waitForTimeout(80); const s = await st(p); seq.push(`${s.active} inSheet=${s.inSheet} vis=${s.activeVisible} top=${s.activeTop}`) }
  log('tab x6 after open', seq)
  await p.screenshot({ path: `${out}/${name}-open-tab6-${run}.png` })
  await p.keyboard.press('Escape'); await p.waitForTimeout(400)
  log('escape after tabbing', await st(p))
  // shift-tab from menu button when open
  await p.focus('#menu'); await p.keyboard.press('Enter'); await p.waitForTimeout(300)
  const seq2 = []
  for (let i = 0; i < 3; i++) { await p.keyboard.press('Shift+Tab'); await p.waitForTimeout(80); const s = await st(p); seq2.push(`${s.active} inSheet=${s.inSheet}`) }
  log('shift-tab x3 after open', seq2)
  await p.keyboard.press('Escape'); await p.waitForTimeout(300)
  // focus in sheet, then Escape: where is focus?
  await p.focus('#menu'); await p.keyboard.press('Enter'); await p.waitForTimeout(300)
  await p.focus('#sheet a[href="#follow"]'); await p.keyboard.press('Escape'); await p.waitForTimeout(400)
  log('escape while focus on sheet link', await st(p))
  // link tap
  await p.evaluate(() => { document.activeElement && document.activeElement.blur(); scrollTo(0, 0) }); await p.waitForTimeout(300)
  await p.tap('#menu'); await p.waitForTimeout(400)
  await p.tap('#sheet a[href="#creators"]'); await p.waitForTimeout(1500)
  log('link tap', await st(p))
  // closed menu, tabbing from top: does focus enter invisible sheet links?
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(600)
  const seq3 = []
  for (let i = 0; i < 9; i++) { await p.keyboard.press('Tab'); await p.waitForTimeout(80); const s = await st(p); seq3.push(`${s.active} inSheet=${s.inSheet} vis=${s.activeVisible}`) }
  log('closed: tab x9 from top', seq3)
  await p.screenshot({ path: `${out}/${name}-closed-tab-${run}.png` })
  // open when scrolled to mid page: sheet top and page behind
  await p.evaluate(() => scrollTo(0, 1500)); await p.waitForTimeout(400)
  await p.tap('#menu'); await p.waitForTimeout(400)
  const geo = await p.evaluate(() => { const r = document.getElementById('sheet').getBoundingClientRect(); return { top: r.top, bottom: r.bottom, barBottom: document.querySelector('.top').getBoundingClientRect().bottom } })
  log('open mid page geo', geo)
  await p.mouse.wheel(0, 400); await p.waitForTimeout(400)
  log('wheel while open', await st(p))
  await ctx.close()
}
await b.close()
