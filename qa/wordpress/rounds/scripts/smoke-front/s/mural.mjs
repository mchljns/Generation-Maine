// PER-N05: the mural on WordPress (server-drawn SVG, only the stagger printed) and on the static v2 page (built from the
// inline JSON): path count, transition delays, the "on" class, the data script size, console errors.
import { launch, WP, V2 } from './lib.mjs'
const b = await launch()
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const vp of [[1440, 900], [390, 844]]) {
  const p = await b.newPage({ viewport: { width: vp[0], height: vp[1] } }); const errs = []
  p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()) })
  await p.goto(url); await p.waitForTimeout(1500)
  const r = await p.evaluate(() => { const m = document.getElementById('mural'), ps = [...m.querySelectorAll('g path')], d = document.getElementById('maine-data'); return { on: m.classList.contains('on'), paths: ps.length, clip: !!m.querySelector('clipPath path'), delays: ps.map(x => x.style.transitionDelay).slice(0, 4).join(',') + ',...,' + ps[ps.length - 1].style.transitionDelay, offset: getComputedStyle(ps[ps.length - 1]).strokeDashoffset, json: d ? d.textContent.length : 0 } })
  console.log(name, vp[0], JSON.stringify(r), 'errors', errs.length, errs.join(' | '))
  await p.close()
}
await b.close()
