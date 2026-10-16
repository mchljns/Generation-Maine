// Round 2: the duration chip over a clip (derived from chip.mjs). For each story, hide the text, capture the pixels
// behind the text box, and work out the contrast of the white text against the lightest and the median pixel.
import { launch, newCtx, WP, V2, dir } from './lib.mjs'
import { writeFileSync } from 'node:fs'
const out = dir('durchip')
const run = process.argv[2] || 'r1'
const b = await launch()
const lum = (r, g, bl) => { const f = c => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4) }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(bl) }
const cr = (a, c) => (Math.max(a, c) + 0.05) / (Math.min(a, c) + 0.05)
const rows = []
async function measure(p, sel, label) {
  const box = await p.evaluate(sel => {
    const span = document.querySelector(sel); if (!span) return null
    const who = span; const r = span.getBoundingClientRect(), wr = who.getBoundingClientRect(), cs = getComputedStyle(who), ss = getComputedStyle(span)
    const st = document.createElement('style'); st.id = 'hidetext'; st.textContent = '.dur{color:transparent!important;text-shadow:none!important}'; document.head.appendChild(st)
    const fr = who.parentElement.getBoundingClientRect()
    return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height), chip: [Math.round(wr.left), Math.round(wr.top), Math.round(wr.width), Math.round(wr.height)], bg: cs.backgroundColor, color: ss.color, frameW: Math.round(fr.width), chipRightGap: Math.round(fr.right - wr.right), lines: Math.round(r.height), text: span.textContent.trim().replace(/\s+/g, ' ') }
  }, sel)
  if (!box) return null
  const buf = await p.screenshot({ clip: { x: box.x + 1, y: box.y + 1, width: Math.max(1, box.w - 2), height: Math.max(1, box.h - 2) } }) // 1px inset: the chip sits at fractional pixels
  await p.evaluate(() => document.getElementById('hidetext').remove())
  const px = await p.evaluate(async b64 => { const img = new Image(); img.src = 'data:image/png;base64,' + b64; await img.decode(); const c = document.createElement('canvas'); c.width = img.width; c.height = img.height; const x = c.getContext('2d'); x.drawImage(img, 0, 0); return Array.from(x.getImageData(0, 0, c.width, c.height).data) }, buf.toString('base64'))
  const L = []; for (let i = 0; i < px.length; i += 4) L.push(lum(px[i], px[i + 1], px[i + 2]))
  L.sort((a, c) => a - c)
  const white = 1, worst = cr(white, L[L.length - 1]), med = cr(white, L[Math.floor(L.length / 2)])
  const row = { label, text: box.text, bg: box.bg, worst: +worst.toFixed(2), median: +med.toFixed(2), chip: box.chip, frameW: box.frameW, chipRightGap: box.chipRightGap }
  rows.push(row); console.log(JSON.stringify(row))
  return row
}
for (const [name, url] of [['wp', WP], ['v2', V2]]) {
  // desktop stage at 1440 and 1024, three frames per story
  for (const [w, h] of [[1440, 900], [1024, 768]]) {
    const ctx = await newCtx(b, { w, h, dsf: 1 }); const p = await ctx.newPage()
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(600)
    const geo = await p.evaluate(() => { const s = document.getElementById('stories'); return { top: s.offsetTop, total: s.offsetHeight - innerHeight } })
    for (let k = 1; k <= 9; k++) {
      await p.evaluate(({ y }) => window.scrollTo({ top: y, behavior: 'instant' }), { y: Math.round(geo.top + (k - 0.5) / 9 * geo.total) }); await p.waitForTimeout(1300)
      for (let f = 0; f < 3; f++) { await measure(p, '#stage .dur', `${name} ${w} stage story ${k} frame ${f}`); await p.waitForTimeout(500) }
      if (k === 5) await p.locator('#stage').screenshot({ path: `${out}/${name}-${w}-stage-5-${run}.png` })
    }
    await ctx.close()
  }
  // phone cards and the viewer at 390 and 320
  for (const [w, h] of [[390, 844], [320, 568]]) {
    const ctx = await newCtx(b, { w, h, dsf: 1 }); const p = await ctx.newPage()
    await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(600)
    for (let k = 1; k <= 9; k++) {
      await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.tap(`#segs button:nth-child(${k})`); await p.waitForTimeout(1300)
      for (let f = 0; f < 3; f++) { await measure(p, `#story-${k} .pv .dur`, `${name} ${w} card story ${k} frame ${f}`); await p.waitForTimeout(500) }
      if (k === 5) await p.locator('#story-5 .pv').screenshot({ path: `${out}/${name}-${w}-card-5-${run}.png` })
    }
    for (const k of [2, 5]) {
      await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.tap(`#segs button:nth-child(${k})`); await p.waitForTimeout(1200)
      await p.tap('.panel.on .pv'); await p.waitForTimeout(900)
      for (let f = 0; f < 3; f++) { await measure(p, `#vtrack .slide:nth-child(${k}) .fr .dur`, `${name} ${w} viewer story ${k} frame ${f}`); await p.waitForTimeout(500) }
      await p.screenshot({ path: `${out}/${name}-${w}-viewer-${k}-${run}.png` })
      await p.keyboard.press('Escape'); await p.waitForTimeout(800)
    }
    await ctx.close()
  }
}
writeFileSync(`${out}/dur-${run}.json`, JSON.stringify(rows, null, 1))
const summary = {}
for (const r of rows) { const k = r.label.split(' story')[0]; summary[k] = summary[k] || { min: 99, n: 0 }; summary[k].min = Math.min(summary[k].min, r.worst); summary[k].n++ }
console.log('SUMMARY worst-pixel contrast per group', JSON.stringify(summary))
await b.close()
