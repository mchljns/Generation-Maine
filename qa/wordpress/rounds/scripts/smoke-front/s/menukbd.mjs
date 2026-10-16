// Round 3, VIS-N04 variations: keyboard in the open phone menu at 320x568, 768x1024 and 844x390 (no touch), Shift+Tab wrap,
// Escape, and a mouse click on the page area behind the sheet.
import { launch, newCtx, WP, V2 } from './lib.mjs'
const b = await launch()
for (const [name, url] of [['wp', WP], ['v2', V2]]) for (const [w, h, dsf] of [[320, 568, 2], [768, 1024, 1], [844, 390, 2], [390, 844, 3]]) {
  const ctx = await newCtx(b, { w, h, phone: false, dsf }); const p = await ctx.newPage()
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(700)
  const where = () => p.evaluate(() => { const s = document.getElementById('sheet'), a = document.activeElement, r = a.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2, on = cy >= 0 && cy < innerHeight, hit = on ? document.elementFromPoint(Math.max(0, Math.min(innerWidth - 1, cx)), cy) : null
    return (a.id ? '#' + a.id : a.tagName) + ':' + (a.textContent || a.getAttribute('aria-label') || '').trim().slice(0, 12) + (s.contains(a) ? '[sheet]' : '') + (!s.contains(a) && hit && s.contains(hit) ? '[HIDDEN]' : '') + (r.width === 0 ? '[ZERO]' : '') + (s.classList.contains('open') ? '' : '[closed]') + '@' + Math.round(scrollY) })
  // bar tab order before opening
  await p.keyboard.press('Tab'); const pre = [await where()]; for (let i = 0; i < 4; i++) { await p.keyboard.press('Tab'); await p.waitForTimeout(80); pre.push(await where()) }
  await p.focus('#menu'); await p.keyboard.press('Enter'); await p.waitForTimeout(400)
  const seq = []; for (let i = 0; i < 6; i++) { await p.keyboard.press('Tab'); await p.waitForTimeout(150); seq.push(await where()) }
  await p.focus('#menu'); await p.waitForTimeout(100)
  const back = []; for (let i = 0; i < 6; i++) { await p.keyboard.press('Shift+Tab'); await p.waitForTimeout(150); back.push(await where()) }
  await p.keyboard.press('Escape'); await p.waitForTimeout(300); const esc = await where()
  // reopen and click on the page below the sheet (if any space is left), then on the bar's logo area
  await p.focus('#menu'); await p.keyboard.press('Enter'); await p.waitForTimeout(400)
  const sb = await p.evaluate(() => Math.round(document.getElementById('sheet').getBoundingClientRect().bottom))
  let clickBelow = 'no room below the sheet'
  if (sb < h - 10) { await p.mouse.click(Math.round(w / 2), Math.min(h - 5, sb + 20)); await p.waitForTimeout(400); clickBelow = await where() }
  console.log(name, `${w}x${h}`, 'bar before open:', pre.join(' > '), '\n   open, Tab x6:', seq.join(' > '), '\n   from Menu Shift+Tab x6:', back.join(' > '), '\n   Escape:', esc, '| sheet bottom', sb, 'click below:', clickBelow)
  await ctx.close()
}
await b.close()
