#!/usr/bin/env node
// Contrast of every visible text element against the background it sits on, per viewport.
// Flags under 4.5:1 for normal text and under 3:1 for large text (24px+, or 19px+ bold).
// The background is read from the nearest ancestor with a solid background-color; elements over
// images, video or gradients are listed separately as "over media" for a hand check against the
// brightest frame, since no CSS value tells you what pixel the glyph sits on.
//
//   node contrast.mjs <url-or-file> [--viewports 390x844,1440x900] [--selector css] [--all]
//
// Needs Playwright (npm i playwright). Set PW_CHROMIUM to a browser binary when needed.
import { createRequire } from 'node:module'
import { resolve } from 'node:path'
const require = createRequire(resolve(process.cwd(), 'noop.js'))
let chromium
try { ({ chromium } = require('playwright')) } catch { console.error('playwright not found: npm i playwright'); process.exit(2) }
const args = process.argv.slice(2)
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d }
const target = args.find((a, i) => !a.startsWith('--') && !['--viewports', '--selector'].includes(args[i - 1]))
if (!target) { console.error('usage: contrast.mjs <url-or-file> [--viewports WxH,...] [--selector css] [--all]'); process.exit(2) }
const url = /^https?:|^file:/.test(target) ? target : 'file://' + resolve(target)
const vps = opt('--viewports', '390x844,1440x900').split(',').map(s => s.split('x').map(Number))
const sel = opt('--selector', null); const all = args.includes('--all')
const browser = await chromium.launch(process.env.PW_CHROMIUM ? { executablePath: process.env.PW_CHROMIUM } : {})
let worst = 0
for (const [w, h] of vps) {
  const page = await browser.newPage({ viewport: { width: w, height: h }, isMobile: w < 900, hasTouch: w < 900 })
  await page.goto(url, { waitUntil: 'networkidle' }).catch(() => {})
  await page.waitForTimeout(500)
  const rows = await page.evaluate(({ sel, all }) => {
    const parse = c => { const m = c.match(/[\d.]+/g); if (!m) return null; const [r, g, b, a = 1] = m.map(Number); return { r, g, b, a } }
    const lum = ({ r, g, b }) => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4 }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b) }
    const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05) }
    const blend = (fg, bg) => ({ r: fg.r * fg.a + bg.r * (1 - fg.a), g: fg.g * fg.a + bg.g * (1 - fg.a), b: fg.b * fg.a + bg.b * (1 - fg.a), a: 1 })
    const vis = e => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && parseFloat(cs.opacity) > 0 }
    const root = sel ? document.querySelector(sel) : document.body
    const out = []
    const els = [...root.querySelectorAll('h1,h2,h3,h4,h5,h6,p,a,button,span,li,td,th,label,small,strong,b,em,i,figcaption,summary,legend,input,textarea,dt,dd,blockquote')]
    for (const e of els) {
      if (!vis(e)) continue
      const own = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1)
      if (!own) continue
      const cs = getComputedStyle(e)
      let fg = parse(cs.color); if (!fg) continue
      // walk up for the background
      let n = e, bg = null, media = false, layers = []
      while (n && n !== document.documentElement) {
        const s = getComputedStyle(n)
        if (s.backgroundImage && s.backgroundImage !== 'none') media = true
        if (n.tagName === 'VIDEO' || n.tagName === 'IMG' || n.tagName === 'CANVAS') media = true
        // a positioned sibling image/video under the text counts as media
        if (!media && n !== e) { const k = [...n.children].find(c => (c.tagName === 'VIDEO' || c.tagName === 'IMG' || c.tagName === 'CANVAS') && c !== e && vis(c) && !c.contains(e)); if (k) { const r1 = e.getBoundingClientRect(), r2 = k.getBoundingClientRect(); if (r1.left >= r2.left - 1 && r1.right <= r2.right + 1 && r1.top >= r2.top - 1 && r1.bottom <= r2.bottom + 1) media = true } }
        const c = parse(s.backgroundColor)
        if (c && c.a > 0) { layers.push(c); if (c.a >= 1) { break } }
        n = n.parentElement
      }
      bg = { r: 255, g: 255, b: 255, a: 1 }
      const bodyBg = parse(getComputedStyle(document.body).backgroundColor); if (bodyBg && bodyBg.a > 0 && !(layers.length && layers[layers.length - 1].a >= 1)) layers.push(bodyBg)
      for (const l of layers.reverse()) bg = l.a >= 1 ? l : blend(l, bg)
      if (fg.a < 1) fg = blend(fg, bg)
      const size = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight, 10) >= 700
      const large = size >= 24 || (size >= 18.66 && bold)
      const r = ratio(fg, bg), need = large ? 3 : 4.5
      const label = (e.getAttribute('aria-label') || e.textContent).trim().replace(/\s+/g, ' ').slice(0, 42)
      const rec = { el: label, tag: e.tagName.toLowerCase(), px: Math.round(size * 10) / 10, ratio: Math.round(r * 100) / 100, need, media }
      if (media || all || r < need) out.push(rec)
    }
    return out
  }, { sel, all })
  const fails = rows.filter(r => !r.media && r.ratio < r.need), over = rows.filter(r => r.media)
  console.log(`=== ${w}x${h}: ${fails.length} under target, ${over.length} over media (hand check)`)
  for (const r of fails) { console.log(`  FAIL ${r.ratio}:1 (need ${r.need}) ${r.px}px <${r.tag}> ${r.el}`); worst++ }
  for (const r of over.slice(0, 25)) console.log(`  over media ${r.ratio}:1 vs ancestor fill, ${r.px}px <${r.tag}> ${r.el}`)
  if (all) for (const r of rows.filter(x => !x.media && x.ratio >= x.need)) console.log(`  ok ${r.ratio}:1 ${r.px}px <${r.tag}> ${r.el}`)
  await page.close()
}
await browser.close()
process.exit(worst ? 1 : 0)
