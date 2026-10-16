import { launch, newCtx, WP, dir } from './lib.mjs'
import { existsSync } from 'node:fs'
const out = dir('admin')
const run = process.argv[2] || 'r1'
const b = await launch()
const AUTH = `${out}/auth.json`
{ // log in through the real form
  const ctx = await newCtx(b, { w: 1280, h: 800 })
  const p = await ctx.newPage()
  await p.goto(WP + 'wp-login.php', { waitUntil: 'networkidle' })
  await p.fill('#user_login', 'admin'); await p.fill('#user_pass', 'adminpass'); await p.click('#wp-submit')
  await p.waitForLoadState('networkidle')
  console.log('logged in at', p.url())
  await ctx.storageState({ path: AUTH }); await ctx.close()
}
const geo = p => p.evaluate(() => {
  const ab = document.getElementById('wpadminbar'), top = document.querySelector('.top'), sheet = document.getElementById('sheet')
  const a = ab ? ab.getBoundingClientRect() : null, t = top.getBoundingClientRect(), s = sheet.getBoundingClientRect()
  return { scrollY: Math.round(scrollY), adminBar: a ? [Math.round(a.top), Math.round(a.bottom), getComputedStyle(ab).position] : null, top: [Math.round(t.top), Math.round(t.bottom)], sheet: [Math.round(s.top), Math.round(s.bottom)], overlap: a ? Math.round(Math.max(0, Math.min(a.bottom, t.bottom) - Math.max(a.top, t.top))) : 0, gapBelowAdmin: a ? Math.round(t.top - a.bottom) : null }
})
for (const [w, h] of [[1440, 900], [1024, 768], [768, 1024], [390, 844]]) {
  const phone = w < 900
  const ctx = await newCtx(b, { w, h, storageState: AUTH })
  const p = await ctx.newPage()
  await p.goto(WP, { waitUntil: 'networkidle' }); await p.waitForTimeout(800)
  const L = (k, v) => console.log(w, k, JSON.stringify(v))
  L('top of page', await geo(p))
  await p.screenshot({ path: `${out}/${w}-top-${run}.png` })
  await p.evaluate(() => window.scrollTo({ top: 1200, behavior: 'instant' })); await p.waitForTimeout(400)
  L('scrolled 1200', await geo(p))
  await p.screenshot({ path: `${out}/${w}-scrolled-${run}.png` })
  // anchor landings with the admin bar
  for (const hash of ['#about', '#creators', '#follow', '#newsletter']) {
    await p.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' })); await p.waitForTimeout(200)
    if (phone) { await p.tap('#menu'); await p.waitForTimeout(400); await p.tap(`#sheet a[href="${hash}"]`) } else { await p.click(`.top a[href="${hash}"]`) }
    let last = -1; for (let i = 0; i < 40; i++) { const y = await p.evaluate(() => scrollY); if (y === last) break; last = y; await p.waitForTimeout(120) }
    const r = await p.evaluate(hash => { const t = document.querySelector(hash), head = t.querySelector('h2,h3,.k') || t; const hr = head.getBoundingClientRect(), bar = document.querySelector('.top').getBoundingClientRect(); return { head: head.textContent.trim().slice(0, 20), headTop: Math.round(hr.top), barBottom: Math.round(bar.bottom), hidden: hr.top < bar.bottom - 1 } }, hash)
    L('anchor ' + hash, r)
    if (r.hidden) await p.screenshot({ path: `${out}/${w}-anchor-${hash.slice(1)}-${run}.png` })
  }
  if (!phone) {
    // stepper stage vs bar
    await p.evaluate(() => { const s = document.getElementById('stories'); window.scrollTo({ top: s.offsetTop + 300, behavior: 'instant' }) }); await p.waitForTimeout(800)
    const sg = await p.evaluate(() => { const v = document.getElementById('stage').getBoundingClientRect(), bar = document.querySelector('.top').getBoundingClientRect(), wh = document.querySelector('.where').getBoundingClientRect(); return { stageTop: Math.round(v.top), barBottom: Math.round(bar.bottom), whereBottom: Math.round(wh.bottom), ih: innerHeight, stageHiddenPx: Math.max(0, Math.round(bar.bottom - v.top)) } })
    L('stepper stage', sg)
    await p.screenshot({ path: `${out}/${w}-stepper-${run}.png` })
  } else {
    // menu while scrolled, and viewer close button vs admin bar
    await p.evaluate(() => window.scrollTo({ top: 1200, behavior: 'instant' })); await p.waitForTimeout(300)
    await p.tap('#menu'); await p.waitForTimeout(500)
    L('menu open scrolled', await geo(p))
    await p.screenshot({ path: `${out}/${w}-menu-scrolled-${run}.png` })
    await p.keyboard.press('Escape'); await p.waitForTimeout(300)
    await p.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' })); await p.waitForTimeout(300)
    await p.tap('#menu'); await p.waitForTimeout(500)
    L('menu open at top', await geo(p))
    await p.screenshot({ path: `${out}/${w}-menu-top-${run}.png` })
    await p.keyboard.press('Escape'); await p.waitForTimeout(300)
    await p.evaluate(() => document.getElementById('stories').scrollIntoView({ behavior: 'instant' })); await p.waitForTimeout(400)
    await p.tap('.panel.on .pv'); await p.waitForTimeout(700)
    const vc = await p.evaluate(() => { const c = document.getElementById('vclose').getBoundingClientRect(); const ab = document.getElementById('wpadminbar'); const a = ab.getBoundingClientRect(); const hit = document.elementFromPoint(c.left + c.width / 2, c.top + c.height / 2); return { close: [Math.round(c.top), Math.round(c.bottom)], adminBar: [Math.round(a.top), Math.round(a.bottom)], hitIsClose: !!(hit && hit.closest('#vclose')), hit: hit ? hit.tagName + '#' + hit.id + '.' + hit.className : null } })
    L('viewer close vs admin bar', vc)
    await p.screenshot({ path: `${out}/${w}-viewer-${run}.png` })
    if (vc.hitIsClose) { await p.tap('#vclose'); } else { await p.keyboard.press('Escape') }
    await p.waitForTimeout(500)
  }
  // newsletter note
  await p.locator('#newsletter').scrollIntoViewIfNeeded(); await p.waitForTimeout(400)
  const note = await p.evaluate(() => { const n = document.querySelector('.gm-newsletter-missing'); if (!n) return null; const r = n.getBoundingClientRect(), cs = getComputedStyle(n); const a = n.querySelector('a'); return { text: n.textContent, w: Math.round(r.width), h: Math.round(r.height), color: cs.color, bg: getComputedStyle(n.closest('.follow')).backgroundColor, link: a && a.href, linkColor: a && getComputedStyle(a).color, overflow: n.scrollWidth > n.clientWidth } })
  L('newsletter note', note)
  await p.locator('#newsletter').screenshot({ path: `${out}/${w}-newsletter-note-${run}.png` })
  await ctx.close()
}
await b.close()
