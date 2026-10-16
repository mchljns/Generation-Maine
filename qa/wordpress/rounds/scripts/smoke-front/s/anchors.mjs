import { launch, newCtx, WP, V2, dir, watch } from './lib.mjs'
const out = dir('anchors')
const run = process.argv[2] || 'r1'
const b = await launch()
const settle = async p => { let last = -1; for (let i = 0; i < 40; i++) { const y = await p.evaluate(() => scrollY); if (y === last) break; last = y; await p.waitForTimeout(120) } }
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const w of [1440, 390]) {
  const phone = w < 900
  const ctx = await newCtx(b, { w, h: phone ? 844 : 900 })
  const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(800)
  const links = phone ? ['sheet:#about', 'sheet:#creators', 'sheet:#follow', 'sheet:#newsletter', 'hero:#follow', 'foot:#about', 'foot:#newsletter'] : ['top:#about', 'top:#creators', 'top:#follow', 'cta:#newsletter', 'hero:#follow', 'foot:#about', 'foot:#creators', 'foot:#follow', 'foot:#newsletter']
  for (const l of links) {
    const [where, hash] = l.split(':')
    await p.evaluate(() => { history.replaceState(null, '', location.pathname); scrollTo(0, 0) }); await p.waitForTimeout(300)
    let sel
    if (where === 'top') sel = `.top nav a[href="${hash}"]`
    if (where === 'cta') sel = `.top .cta a[href="${hash}"], .top a.cta[href="${hash}"]`
    if (where === 'hero') sel = `.hero a[href="${hash}"]`
    if (where === 'foot') sel = `footer .flinks a[href="${hash}"]`
    if (where === 'sheet') { await p.tap('#menu'); await p.waitForTimeout(400); sel = `#sheet a[href="${hash}"]` }
    if (where === 'foot') { await p.locator(sel).first().scrollIntoViewIfNeeded(); await p.waitForTimeout(200) }
    if (phone) await p.locator(sel).first().tap(); else await p.locator(sel).first().click()
    await p.waitForTimeout(300); await settle(p)
    const r = await p.evaluate((hash) => {
      const bar = document.querySelector('.top').getBoundingClientRect()
      const t = document.querySelector(hash)
      const tr = t.getBoundingClientRect()
      const head = t.querySelector('h2,h3,.k') || t
      const hr = head.getBoundingClientRect()
      return { hash: location.hash, scrollY: Math.round(scrollY), barBottom: Math.round(bar.bottom), targetTop: Math.round(tr.top), headText: head.textContent.trim().slice(0, 30), headTop: Math.round(hr.top), hidden: hr.top < bar.bottom - 1, sheetOpen: document.getElementById('sheet').classList.contains('open'), bodyOverflow: document.body.style.overflow, atBottom: Math.round(innerHeight + scrollY) >= document.documentElement.scrollHeight - 2 }
    }, hash)
    console.log(name, w, l, JSON.stringify(r))
    await p.screenshot({ path: `${out}/${name}-${w}-${where}-${hash.slice(1)}-${run}.png` })
  }
  await ctx.close()
}
await b.close()
