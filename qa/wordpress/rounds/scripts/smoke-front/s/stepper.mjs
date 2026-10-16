import { launch, newCtx, WP, V2, dir } from './lib.mjs'
const out = dir('stepper')
const run = process.argv[2] || 'r1'
const b = await launch()
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h] of [[1440, 900], [1024, 768]]) {
  const ctx = await newCtx(b, { w, h })
  const p = await ctx.newPage()
  const gifs = []
  p.on('request', r => { const m = r.url().match(/creator-(\d)\.gif/); if (m) gifs.push(+m[1]) })
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(800)
  console.log(name, w, 'gifs at load', JSON.stringify(gifs))
  const geo = await p.evaluate(() => { const s = document.getElementById('stories'); return { top: s.offsetTop, h: s.offsetHeight, ih: innerHeight } })
  const total = geo.h - geo.ih
  const rows = []
  for (let k = 0; k < 9; k++) {
    const y = Math.round(geo.top + (k + 0.5) / 9 * total)
    await p.evaluate(y => window.scrollTo({ top: y, behavior: 'instant' }), y)
    await p.waitForTimeout(900)
    const r = await p.evaluate(() => {
      const vis = e => { const cs = getComputedStyle(e); return cs.visibility !== 'hidden' && parseFloat(cs.opacity) > 0.01 }
      const stageClips = [...document.querySelectorAll('#stage .clip')]
      const visibleClips = stageClips.map((c, i) => vis(c) ? i : -1).filter(i => i >= 0)
      const loaded = stageClips.map((c, i) => c.getAttribute('src') ? i : -1).filter(i => i >= 0)
      const panelOn = [...document.querySelectorAll('.panel')].map((c, i) => c.classList.contains('on') ? i : -1).filter(i => i >= 0)
      const visPanels = [...document.querySelectorAll('.panel')].map((c, i) => vis(c) ? i : -1).filter(i => i >= 0)
      const whoOn = [...document.querySelectorAll('#stage .who')].map((c, i) => vis(c) ? i : -1).filter(i => i >= 0)
      const segOn = [...document.querySelectorAll('#segs button')].map((c, i) => c.getAttribute('aria-current') === 'true' ? i : -1).filter(i => i >= 0)
      const vidr = document.querySelector('#stage').getBoundingClientRect(), bar = document.querySelector('.top').getBoundingClientRect()
      const ph = document.querySelector('.panel.on h2'), pr = ph.getBoundingClientRect()
      const where = document.querySelector('.where').getBoundingClientRect()
      return { wn: document.getElementById('wn').textContent, next: document.getElementById('wnext').textContent, dur: document.getElementById('dur').textContent, visibleClips, loaded, panelOn, visPanels, whoOn, segOn, h2: ph.textContent, stageTop: Math.round(vidr.top), stageBottom: Math.round(vidr.bottom), barBottom: Math.round(bar.bottom), whereBottom: Math.round(where.bottom), ih: innerHeight, h2Top: Math.round(pr.top) }
    })
    rows.push(r)
    console.log(name, w, 'step', k, JSON.stringify(r))
    if (k === 0 || k === 4 || k === 8) await p.screenshot({ path: `${out}/${name}-${w}-step${k + 1}-${run}.png` })
  }
  console.log(name, w, 'gif requests in order', JSON.stringify(gifs))
  // segment click back to 3
  await p.click('#segs button:nth-child(3)'); await p.waitForTimeout(1500)
  console.log(name, w, 'after seg3 click', await p.evaluate(() => ({ wn: document.getElementById('wn').textContent, h2: document.querySelector('.panel.on h2').textContent })))
  // keyboard on segment
  await p.focus('#segs button:nth-child(7)'); await p.keyboard.press('Enter'); await p.waitForTimeout(1500)
  console.log(name, w, 'after seg7 Enter', await p.evaluate(() => ({ wn: document.getElementById('wn').textContent, h2: document.querySelector('.panel.on h2').textContent, focused: document.activeElement.getAttribute('aria-label') })))
  await ctx.close()
}
await b.close()
