#!/usr/bin/env node
// Measure a page instead of eyeballing it. For each viewport: horizontal overflow, tap targets under 44px,
// text that overflows its box, images missing alt, media requested at load, console errors, fonts in use,
// and a screenshot. Prints JSON per viewport and writes screenshots next to --out.
//
//   node measure.mjs <url-or-file> [--out dir] [--viewports 390x844,1400x900] [--full] [--selector css]
//
// Needs Playwright (npm i playwright) and a Chromium. Set PW_CHROMIUM to a browser binary when the
// bundled download is not available (for example /opt/pw-browsers/chromium in some sandboxes).
import { createRequire } from 'node:module'
import { mkdirSync } from 'node:fs'
import { resolve } from 'node:path'
const require = createRequire(resolve(process.cwd(), 'noop.js'))
let chromium
try { ({ chromium } = require('playwright')) } catch { console.error('playwright not found: npm i playwright (run from the project root)'); process.exit(2) }
const args = process.argv.slice(2)
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d }
const target = args.find(a => !a.startsWith('--') && !['--out', '--viewports', '--selector'].includes(args[args.indexOf(a) - 1]))
if (!target) { console.error('usage: measure.mjs <url-or-file> [--out dir] [--viewports WxH,...] [--full] [--selector css]'); process.exit(2) }
const url = /^https?:|^file:/.test(target) ? target : 'file://' + resolve(target)
const out = opt('--out', 'measure-out'); mkdirSync(out, { recursive: true })
const vps = opt('--viewports', '320x568,390x844,768x1024,1400x900').split(',').map(s => s.split('x').map(Number))
const full = args.includes('--full'); const sel = opt('--selector', null)
const browser = await chromium.launch(process.env.PW_CHROMIUM ? { executablePath: process.env.PW_CHROMIUM } : {})
for (const [w, h] of vps) {
  const phone = w < 900
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: phone ? 2 : 1, isMobile: phone, hasTouch: phone })
  const media = [], errors = []
  page.on('request', r => { if (/\.(gif|webm|mp4|jpe?g|png|webp|avif|woff2?|ttf)(\?|$)/i.test(r.url())) media.push(r.url().split('/').pop().split('?')[0]) })
  page.on('pageerror', e => errors.push(String(e.message)))
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()) })
  await page.goto(url, { waitUntil: 'networkidle' }).catch(e => errors.push('goto: ' + e.message))
  await page.waitForTimeout(600)
  const r = await page.evaluate(({ sel }) => {
    const root = sel ? document.querySelector(sel) : document.body
    const vis = e => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' }
    const label = e => (e.getAttribute('aria-label') || e.textContent || e.id || e.className || e.tagName).toString().trim().replace(/\s+/g, ' ').slice(0, 40)
    const targets = [...root.querySelectorAll('a[href],button,input,select,textarea,[role=button],[tabindex]:not([tabindex="-1"])')].filter(vis)
    const small = targets.map(e => { const r = e.getBoundingClientRect(); return { el: label(e), w: Math.round(r.width), h: Math.round(r.height) } }).filter(t => t.w < 44 || t.h < 44)
    const overflowText = [...root.querySelectorAll('h1,h2,h3,h4,p,a,button,span,li,td,th,label')].filter(vis).filter(e => e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).overflowX !== 'hidden').map(e => ({ el: label(e), by: e.scrollWidth - e.clientWidth })).slice(0, 20)
    const noAlt = [...root.querySelectorAll('img')].filter(i => !i.hasAttribute('alt')).map(i => (i.getAttribute('src') || i.getAttribute('data-src') || '').split('/').pop()).slice(0, 20)
    const fonts = [...new Set([...root.querySelectorAll('h1,h2,h3,p,a,button,span,li')].filter(vis).map(e => getComputedStyle(e).fontFamily.split(',')[0].replace(/"/g, '')))]
    const tiny = [...root.querySelectorAll('p,a,li,span,td,label,button')].filter(vis).filter(e => parseFloat(getComputedStyle(e).fontSize) < 12 && e.textContent.trim().length > 2).map(e => ({ el: label(e), px: parseFloat(getComputedStyle(e).fontSize) })).slice(0, 20)
    const h1s = root.querySelectorAll('h1').length
    const landmarks = ['main', 'nav', 'header', 'footer'].filter(t => root.querySelector(t) || root.querySelector(`[role=${t === 'main' ? 'main' : t === 'nav' ? 'navigation' : t === 'header' ? 'banner' : 'contentinfo'}]`))
    return { docOverflowPx: document.documentElement.scrollWidth - innerWidth, pageHeight: document.documentElement.scrollHeight, tapTargetsUnder44: small, textOverflow: overflowText, imagesWithoutAlt: noAlt, textUnder12px: tiny, fonts, h1Count: h1s, landmarks, title: document.title, metaDescription: !!document.querySelector('meta[name=description]'), viewportMeta: !!document.querySelector('meta[name=viewport]') }
  }, { sel })
  r.mediaRequestedAtLoad = { count: media.length, files: media.slice(0, 30) }
  r.errors = errors
  const shot = `${out}/${w}x${h}.png`
  await page.screenshot({ path: shot, fullPage: full })
  r.screenshot = shot
  console.log(`=== ${w}x${h}`); console.log(JSON.stringify(r, null, 1))
  await page.close()
}
await browser.close()
