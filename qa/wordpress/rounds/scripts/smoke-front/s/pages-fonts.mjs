// Round 3, PER-N02/PER-N03/PER-N12 on every page type: requests for fonts and icons, preloads used or not (Chrome's
// "preloaded but not used" console warning), the computed families on the first screen, any TTF requested.
import { launch, newCtx, WP } from './lib.mjs'
const b = await launch()
const pages = (process.env.PAGES || '/,/hello-world/,/sample-page/,/no-such-page/,/?s=hello,/category/uncategorized/,/2026/').split(',')
for (const path of pages) for (const [w, h] of [[390, 844], [1440, 900]]) {
  const ctx = await newCtx(b, { w, h }); const p = await ctx.newPage()
  const reqs = [], warns = []
  p.on('request', r => { const u = r.url(); if (/\.(woff2?|ttf|otf|ico|svg|png)(\?|$)/.test(u) && /fonts|icon|favicon/.test(u)) reqs.push(u.replace(/^.*\//, '')) })
  p.on('console', m => { if (m.type() === 'warning' || m.type() === 'error') warns.push(m.type() + ': ' + m.text().slice(0, 160)) })
  const resp = await p.goto(WP.replace(/\/$/, '') + path, { waitUntil: 'networkidle' }); await p.waitForTimeout(3500)
  const fam = await p.evaluate(() => { const seen = new Set(); for (const e of document.querySelectorAll('body *')) { const r = e.getBoundingClientRect(); if (r.top > innerHeight || r.bottom < 0 || !r.width) continue; if (![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue; seen.add(getComputedStyle(e).fontFamily.split(',')[0].replace(/['"]/g, '')) } return [...seen] })
  const loaded = await p.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/['"]/g, '')))
  const preloads = await p.evaluate(() => [...document.querySelectorAll('link[rel=preload]')].map(l => l.href.replace(/^.*\//, '') + ' ' + l.type))
  console.log(path, w, resp.status(), JSON.stringify({ fontReqs: reqs.filter(x => /woff|ttf|otf/.test(x)), iconReqs: reqs.filter(x => !/woff|ttf|otf/.test(x)), ttf: reqs.filter(x => /ttf/.test(x)).length, preloads, firstScreenFamilies: fam, loaded, warns }))
  await ctx.close()
}
await b.close()
