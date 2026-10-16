// Round 4, FR-R2 risk: the full-width rule uses calc(50% - 50vw). With classic (non-overlay) scrollbars, as on Windows,
// 100vw includes the scrollbar. Launch Chromium with its scrollbars shown and read, per page and width: the scrollbar
// width, page overflow, and where the full-width section sits against the visible area.
import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs'
import { dir } from './lib.mjs'
const out = dir('scrollbar'); const run = process.argv[2] || 'r1'
const base = process.env.BASE || 'http://127.0.0.1:8901/'
const pages = (process.env.PAGES || ',roster/,stepper/,roster-mixed/,stepper-mixed/,creators-pattern/,roster-group/').split(',')
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', ignoreDefaultArgs: ['--hide-scrollbars'] })
for (const path of pages) for (const [w, h] of [[1440, 900], [1024, 768]]) {
  const ctx = await b.newContext({ viewport: { width: w, height: h } }); const p = await ctx.newPage()
  await p.goto(base + path, { waitUntil: 'networkidle' }); await p.waitForTimeout(500)
  const r = await p.evaluate(() => {
    const de = document.documentElement, sb = innerWidth - de.clientWidth
    const sec = document.querySelector('.gm-entry > section, .gm-entry > .gm-creators, main > .hero') || document.querySelector('section.roster, section.stories')
    const sr = sec ? sec.getBoundingClientRect() : null
    const tiles = [...document.querySelectorAll('.roster .tile')], lastTile = tiles.length ? tiles[tiles.length - 1].getBoundingClientRect() : null
    return { scrollbar: sb, overflow: de.scrollWidth - de.clientWidth, sec: sec ? sec.className : null, secLeft: sr ? Math.round(sr.left) : null, secRight: sr ? Math.round(sr.right) : null, client: de.clientWidth, lastTileRight: lastTile ? Math.round(lastTile.right) : null, lastTileClipped: lastTile ? lastTile.right > de.clientWidth : null }
  })
  console.log(`/${path} ${w}x${h}`, JSON.stringify(r))
  await p.screenshot({ path: `${out}/${(path || 'front').replace(/\//g, '')}-${w}-${run}.png` })
  await ctx.close()
}
await b.close()
