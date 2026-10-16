// Round 2: the new pause control for the clips. Keyboard, accessible name and state, still images when paused,
// reduced motion starting paused, GIF downloads while paused, and the viewer while paused.
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
import { writeFileSync } from 'node:fs'
const out = dir('pause')
const run = process.argv[2] || 'r1'
const b = await launch()
const st = p => p.evaluate(() => {
  const btn = document.getElementById('cpause'), r = btn.getBoundingClientRect(), cs = getComputedStyle(btn)
  const wn = document.getElementById('wn').getBoundingClientRect(), segs = document.getElementById('segs').getBoundingClientRect()
  const phone = matchMedia('(max-width: 900px)').matches
  const clip = phone ? document.querySelector('.panel.on .pv .clip') : document.querySelector('#stage .clip.on')
  const short = s => s ? s.replace(/^.*\//, '') : s
  const hit = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2)
  const svgVisible = [...btn.querySelectorAll('svg')].map(s => s.getAttribute('class') + ':' + getComputedStyle(s).display)
  return { pressed: btn.getAttribute('aria-pressed'), label: btn.getAttribute('aria-label'), rect: [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)], color: cs.color, icon: svgVisible.join(' '), hitIsBtn: !!(hit && hit.closest('#cpause')), wnRect: [Math.round(wn.left), Math.round(wn.right)], segsRect: [Math.round(segs.left), Math.round(segs.top), Math.round(segs.right)], overlapsWn: r.left < wn.right && r.right > wn.left && r.top < wn.bottom && r.bottom > wn.top, overlapsSegs: r.left < segs.right && r.right > segs.left && r.top < segs.bottom && r.bottom > segs.top, clipSrc: clip ? short(clip.getAttribute('src')) : null, clipTag: clip ? clip.tagName : null, natural: clip && clip.naturalWidth ? [clip.naturalWidth, clip.naturalHeight] : null, rendered: clip ? [Math.round(clip.getBoundingClientRect().width), Math.round(clip.getBoundingClientRect().height)] : null, dpr: devicePixelRatio, wn: document.getElementById('wn').textContent }
})
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h] of [[1440, 900], [390, 844]]) for (const reduced of [false, true]) {
  const phone = w < 900
  const tag = `${name}-${w}-${reduced ? 'reduce' : 'motion'}`
  const ctx = await newCtx(b, { w, h, reduced })
  const p = await ctx.newPage()
  const gifs = []
  p.on('request', r => { const m = r.url().match(/creator-(\d)\.gif/); if (m) gifs.push(+m[1]) })
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(800)
  const L = (k, v) => console.log(tag, k, typeof v === 'string' ? v : JSON.stringify(v))
  const geo = await p.evaluate(() => { const s = document.getElementById('stories'); return { top: s.offsetTop, total: s.offsetHeight - innerHeight } })
  const goStep = async k => { if (phone) { await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.tap(`#segs button:nth-child(${k})`) } else await p.evaluate(({ y }) => window.scrollTo({ top: y, behavior: 'instant' }), { y: Math.round(geo.top + (k - 0.5) / 9 * geo.total) }); await p.waitForTimeout(1500) }
  await goStep(1)
  L('at load', await st(p))
  L('aria', await p.locator('#cpause').ariaSnapshot())
  const sel = phone ? '.panel.on .pv' : '#stage'
  await p.locator(sel).screenshot({ path: `${out}/${tag}-load-a-${run}.png` }); await p.waitForTimeout(1700)
  await p.locator(sel).screenshot({ path: `${out}/${tag}-load-b-${run}.png` })
  await p.locator('.where').screenshot({ path: `${out}/${tag}-where-${run}.png` })
  // keyboard: Tab from the top until the pause button has focus
  await p.evaluate(() => { document.activeElement && document.activeElement.blur && document.activeElement.blur() })
  await p.focus('#segs button:nth-child(1)'); await p.keyboard.press('Shift+Tab'); await p.waitForTimeout(200)
  const focused = await p.evaluate(() => { const a = document.activeElement, cs = getComputedStyle(a); return { id: a.id, outline: `${cs.outlineStyle} ${cs.outlineWidth} ${cs.outlineColor} offset ${cs.outlineOffset}`, focusVisible: a.matches(':focus-visible') } })
  L('Shift+Tab from segment 1 lands on', focused)
  await p.locator('.where').screenshot({ path: `${out}/${tag}-where-focus-${run}.png` })
  const before = (await st(p)).pressed
  await p.keyboard.press('Space'); await p.waitForTimeout(800)
  const s1 = await st(p); L('after Space', s1)
  L('aria after Space', await p.locator('#cpause').ariaSnapshot())
  await p.locator(sel).screenshot({ path: `${out}/${tag}-space-a-${run}.png` }); await p.waitForTimeout(1700)
  await p.locator(sel).screenshot({ path: `${out}/${tag}-space-b-${run}.png` })
  await p.keyboard.press('Enter'); await p.waitForTimeout(800)
  const s2 = await st(p); L('after Enter', s2)
  L('aria after Enter', await p.locator('#cpause').ariaSnapshot())
  await p.locator(sel).screenshot({ path: `${out}/${tag}-enter-a-${run}.png` }); await p.waitForTimeout(1700)
  await p.locator(sel).screenshot({ path: `${out}/${tag}-enter-b-${run}.png` })
  // make sure we are paused, then move on to story 4 and 5: do GIFs download while paused, and does the new clip show its still?
  if ((await st(p)).pressed !== 'true') { await p.click('#cpause'); await p.waitForTimeout(500) }
  const g0 = gifs.length
  await goStep(4); const s4 = await st(p); L('paused, story 4', s4)
  await goStep(5); const s5 = await st(p); L('paused, story 5', s5)
  L('GIF requests while paused (story 4, 5)', gifs.slice(g0))
  await p.locator(sel).screenshot({ path: `${out}/${tag}-paused5-a-${run}.png` }); await p.waitForTimeout(1700)
  await p.locator(sel).screenshot({ path: `${out}/${tag}-paused5-b-${run}.png` })
  if (phone) {
    // the viewer while paused
    await p.tap('.panel.on .pv'); await p.waitForTimeout(900)
    const v = await p.evaluate(() => { const sl = [...document.querySelectorAll('#vtrack .slide')]; const c = document.querySelector('#vtrack').getBoundingClientRect(); const cur = sl.findIndex(s => { const r = s.getBoundingClientRect(); return Math.abs(r.left - c.left) < 5 }); const clip = sl[cur].querySelector('.clip'); const r = clip.getBoundingClientRect(); return { vn: document.getElementById('vn').textContent, cur, src: (clip.getAttribute('src') || '').replace(/^.*\//, ''), natural: clip.naturalWidth ? [clip.naturalWidth, clip.naturalHeight] : null, rendered: [Math.round(r.width), Math.round(r.height)], pauseInViewer: !!document.querySelector('#viewer .cpause, #viewer [aria-pressed]'), viewerButtons: [...document.querySelectorAll('#viewer button')].map(b => b.getAttribute('aria-label') || b.textContent.trim()) } })
    L('viewer opened while paused', v)
    await p.screenshot({ path: `${out}/${tag}-viewer-paused-${run}.png` })
    await p.keyboard.press('Escape'); await p.waitForTimeout(800)
  }
  // play again
  await p.click('#cpause'); await p.waitForTimeout(1200)
  const s6 = await st(p); L('after play again', s6)
  L('GIF requests total', gifs)
  await ctx.close()
}
await b.close()
