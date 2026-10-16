// Round 3, VIS-N01 / VIS-N07 / PER-N06: what a paused clip shows, per creator, on the desktop stage, the phone card and the
// viewer, with reduced motion (paused at load) and with the pause button. For each: the src, whether it decoded, its natural
// size against the size drawn in device pixels. STORIES lists the creators to visit (1-based).
import { launch, newCtx, WP, dir } from './lib.mjs'
const out = dir('still'); const run = process.argv[2] || 'r1'
const url = process.env.URL || WP; const tag = process.env.TAG || 'wp'
const stories = (process.env.STORIES || '1,4,5').split(',').map(Number)
const b = await launch()
const info = (p, sel) => p.evaluate(sel => { const c = document.querySelector(sel); if (!c) return { missing: sel }; const r = c.getBoundingClientRect(); const isV = c.tagName === 'VIDEO'
  const src = isV ? (c.currentSrc || c.getAttribute('src') || '') : (c.getAttribute('src') || '')
  return { tag: c.tagName, src: src.replace(/^.*\//, '') || '(none)', poster: isV ? (c.getAttribute('poster') || '').replace(/^.*\//, '') : undefined, still: (c.dataset.still || '').replace(/^.*\//, ''), complete: isV ? c.readyState : c.complete, natural: isV ? [c.videoWidth, c.videoHeight] : [c.naturalWidth, c.naturalHeight], broken: !isV && c.complete && c.getAttribute('src') && c.naturalWidth === 0, css: [Math.round(r.width), Math.round(r.height)], dpr: devicePixelRatio, paused: isV ? c.paused : undefined,
    scale: !isV && c.naturalWidth ? +(Math.max(r.width / c.naturalWidth, r.height / c.naturalHeight) * devicePixelRatio).toFixed(2) : null } }, sel)
const net = []
for (const mode of ['reduce', 'button']) {
  for (const [w, h, dsf] of [[1440, 900, 2], [1024, 768, 1]]) {
    const ctx = await newCtx(b, { w, h, reduced: mode === 'reduce', dsf }); const p = await ctx.newPage()
    p.on('response', r => { if (/uploads|still\.svg/.test(r.url())) net.push(`${mode} ${w} ${r.status()} ${r.url().replace(/^.*\//, '')}`) })
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(600)
    if (mode === 'button') { await p.locator('#cpause').scrollIntoViewIfNeeded(); await p.click('#cpause'); await p.waitForTimeout(400) }
    const g = await p.evaluate(() => { const s = document.getElementById('stories'); return { top: s.offsetTop, total: s.offsetHeight - innerHeight } })
    for (const k of stories) {
      await p.evaluate(({ y }) => scrollTo({ top: y, behavior: 'instant' }), { y: Math.round(g.top + (k - 0.5) / 9 * g.total) }); await p.waitForTimeout(1500)
      console.log(tag, mode, `${w}@${dsf}x stage story ${k}`, JSON.stringify(await info(p, '#stage .clip.on')), 'wn', await p.textContent('#wn'))
      await p.locator('#stage').screenshot({ path: `${out}/${tag}-${mode}-${w}-stage${k}-${run}.png` })
    }
    await ctx.close()
  }
  for (const [w, h, dsf] of [[390, 844, 3], [320, 568, 2], [768, 1024, 2]]) {
    const ctx = await newCtx(b, { w, h, reduced: mode === 'reduce', dsf, phone: true }); const p = await ctx.newPage()
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(600)
    await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(300)
    if (mode === 'button') { await p.tap('#cpause'); await p.waitForTimeout(400) }
    for (const k of stories) {
      await p.tap(`#segs button:nth-child(${k})`); await p.waitForTimeout(1400)
      console.log(tag, mode, `${w}@${dsf}x card ${k}`, JSON.stringify(await info(p, `#story-${k} .pv .clip`)))
      await p.locator(`#story-${k} .pv`).screenshot({ path: `${out}/${tag}-${mode}-${w}-card${k}-${run}.png` })
      if (w !== 768) {
        await p.tap(`#story-${k} .pv`); await p.waitForTimeout(1000)
        console.log(tag, mode, `${w}@${dsf}x viewer ${k}`, JSON.stringify(await info(p, `#vtrack .slide:nth-child(${k}) .clip`)))
        await p.screenshot({ path: `${out}/${tag}-${mode}-${w}-viewer${k}-${run}.png` })
        await p.keyboard.press('Escape'); await p.waitForTimeout(600)
      }
    }
    await ctx.close()
  }
}
console.log('still and upload responses:', [...new Set(net)].filter(x => / 4\d\d /.test(x) || /still|portrait-[0-9]+\.|huge|wide|big/.test(x)).join(' | '))
await b.close()
