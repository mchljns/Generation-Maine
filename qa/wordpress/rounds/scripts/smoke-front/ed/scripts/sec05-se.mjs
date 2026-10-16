// SEC-N05 as an editor would hit it: in the Site Editor, paste a headline with a long run of spaces (or no-break spaces)
// into the hero headline, save, and check the page and the theme log.
import { launch, login, save, shot, openTemplate, watch } from './lib.mjs';
const [base, tag, v65s, kind = 'spaces', nStr = '9000'] = process.argv.slice(2);
const n = +nStr;
const browser = await launch();
const { page, ctx } = await login(browser, base, { w: 1440, h: 900 });
await ctx.grantPermissions(['clipboard-read', 'clipboard-write'], { origin: base });
const log = []; watch(page, log);
const f = await openTemplate(page, base, v65s === '1');
const gap = kind === 'nbsp' ? ' '.repeat(n) : kind === 'newlines' ? '\n'.repeat(n) : ' '.repeat(n);
const h1 = f.locator('h1').first();
await h1.click(); await page.waitForTimeout(300);
await page.keyboard.press('Control+a'); await page.keyboard.press('Delete');
await page.keyboard.type('Young Mainers');
await page.keyboard.press('Shift+Enter');
await page.keyboard.type('on staying');
// put the gap and the last word on the clipboard and paste (the editor's own paste handling)
await page.evaluate(async (t) => { await navigator.clipboard.writeText(t); }, gap + 'here.');
await page.keyboard.press('Control+v');
await page.waitForTimeout(2000);
const stored = await page.evaluate(() => { const s = wp.data.select('core/block-editor'); const id = s.getClientIdsWithDescendants().find(id => s.getBlockName(id) === 'core/heading' && / gm-here /.test(' ' + (s.getBlock(id).attributes.className || '') + ' ')); return String(s.getBlock(id).attributes.content); });
const storedInfo = { len: stored.length, spaces: (stored.match(/ /g) || []).length, nbspChars: (stored.match(/ /g) || []).length, nbspEnt: (stored.match(/&nbsp;/g) || []).length, br: (stored.match(/<br>/g) || []).length, head: stored.slice(0, 40), tail: stored.slice(-30) };
await page.locator('.editor-header__settings button, .edit-site-header-edit-mode__actions button', { hasText: /^Save$/ }).first().click();
await page.waitForTimeout(1200);
const p2 = page.locator('.entities-saved-states__panel').getByRole('button', { name: /^Save$/ }); if (await p2.count()) await p2.first().click();
await page.waitForFunction(() => wp.data.select('core').__experimentalGetDirtyEntityRecords().length === 0, null, { timeout: 60000 }).catch(() => {});
await page.waitForTimeout(1000);
const front = {};
for (const w of [1440, 390]) {
  const p = await browser.newPage({ viewport: { width: w, height: 900 } });
  await p.goto(base + '/', { waitUntil: 'networkidle' });
  front[w] = await p.evaluate(() => { const h = document.querySelector('h1'); return h ? { text: h.innerText.replace(/\s+/g, ' '), gold: [...h.querySelectorAll('.here')].map(s => s.textContent), dots: h.querySelectorAll('.d').length, h: Math.round(h.getBoundingClientRect().height) } : 'NO H1'; });
  front[w].overflow = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth);
  await p.locator('h1').first().screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-sec05-${kind}-front-${w}.png` }).catch(() => {});
  await p.close();
}
save(`${tag}-sec05-${kind}.json`, { storedInfo, front, log });
console.log(JSON.stringify({ storedInfo, front }, null, 1));
await browser.close();
