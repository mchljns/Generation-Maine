// fix4: does the editor canvas's CSS dot (.gm-here::after, assets/css/editor.css) still wrap alone? A static copy of the
// hero markup with editor.css, swept 320 to 1440 by 2px: the h1's height with the dot against its height with gm-nodot.
// A taller h1 with the dot means the dot went onto a line of its own. usage: node edtest.mjs
import { launch } from './lib.mjs'
import { writeFileSync } from 'node:fs'
const dir = '/tmp/claude-0/wptest/work/fix4-front/edtest'
const heads = { shipped: 'Young Mainers<br>on building<br>a life here', long7: 'Young Mainers<br>on homeownership', emdashless: 'Young Mainers on what it costs to stay', url: 'Young Mainers<br>at generationmaine.org', long5: 'Young Mainers<br>on building<br>a life independently' }
const b = await launch()
for (const [k, h] of Object.entries(heads)) {
  writeFileSync(`${dir}/${k}.html`, `<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="assets/css/editor.css"><body><div class="hero"><div class="w"><div class="col"><h1 class="wp-block-heading rise gm-here" id="a">${h}</h1><h1 class="wp-block-heading rise gm-here gm-nodot" id="b" style="position:absolute;visibility:hidden">${h}</h1></div><div class="mural"></div></div></div>`)
  const ctx = await b.newContext({ viewport: { width: 320, height: 900 } }); const p = await ctx.newPage()
  await p.goto(`file://${dir}/${k}.html`); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300)
  const alone = []
  for (let w = 320; w <= 1440; w += 2) {
    await p.setViewportSize({ width: w, height: 900 })
    const r = await p.evaluate(() => { const a = document.getElementById('a'), b = document.getElementById('b'); b.style.width = a.getBoundingClientRect().width + 'px'; return [a.getBoundingClientRect().height, b.getBoundingClientRect().height] })
    if (r[0] > r[1] + 1) alone.push(w)
  }
  console.log(`${k}: CSS dot alone at ${alone.length} widths${alone.length ? ' (' + alone.slice(0, 12).join(',') + (alone.length > 12 ? ',...' : '') + ')' : ''}`)
  await ctx.close()
}
await b.close()
