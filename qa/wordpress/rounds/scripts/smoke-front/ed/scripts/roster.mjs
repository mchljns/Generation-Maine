// Creators block > Layout: Roster (Front Page, Edit pattern, block sidebar), save; then the front at 1440/1024/390/320:
// town and name clipping, text-shadow, display; aria-labels; and the canvas preview.
// usage: node roster.mjs <base> <tag> <v65 0|1> <roster|stepper> [limit]
import { launch, login, save, shot, openTemplate, watch } from './lib.mjs';
const [base, tag, v65s, mode, limit = '9'] = process.argv.slice(2);
const v65 = v65s === '1';
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
const log = []; watch(page, log);
const f = await openTemplate(page, base, v65);
// select the Creators section, Edit pattern (WP 7), then the Creators block
await page.evaluate(() => { const s = wp.data.select('core/block-editor'); const id = s.getClientIdsWithDescendants().find(id => s.getBlockName(id) === 'core/group' && / gm-creators /.test(' ' + (s.getBlock(id).attributes.className || '') + ' ')); wp.data.dispatch('core/block-editor').selectBlock(id); });
await page.waitForTimeout(600);
const ep = page.getByRole('button', { name: /^Edit pattern$/ }); if (await ep.count()) { await ep.first().click(); await page.waitForTimeout(1200); }
await page.evaluate(() => { const s = wp.data.select('core/block-editor'); const id = s.getClientIdsWithDescendants().find(id => s.getBlockName(id) === 'generation-maine/creators'); wp.data.dispatch('core/block-editor').selectBlock(id); });
await page.waitForTimeout(800);
const side = page.locator('.interface-complementary-area').first();
if (!(await side.count())) { await page.getByRole('button', { name: 'Settings', exact: true }).first().click(); await page.waitForTimeout(600); }
const bt = side.getByRole('tab', { name: 'Block' }); if (await bt.count()) await bt.first().click();
await page.waitForTimeout(500);
const before = (await side.innerText()).replace(/\s+/g, ' ').slice(0, 600);
await side.getByLabel('Layout').selectOption(mode);
await page.waitForTimeout(800);
const lim = side.getByRole('spinbutton', { name: /Most creators/ });
if (await lim.count()) { await lim.fill(limit); await lim.press('Tab'); }
await page.waitForTimeout(3500);
const after = (await side.innerText()).replace(/\s+/g, ' ').slice(0, 600);
const canvas = await f.evaluate(() => { const e = document.querySelector('[data-type="generation-maine/creators"]'); return { tiles: e.querySelectorAll('.tile').length, labels: [...e.querySelectorAll('.tile[aria-label]')].map(t => t.getAttribute('aria-label')).slice(0, 3), towns: [...e.querySelectorAll('.tile .town')].map(t => `${t.textContent}:${t.clientWidth}/${t.scrollWidth}`).slice(0, 3) }; });
await f.locator('[data-type="generation-maine/creators"]').first().scrollIntoViewIfNeeded();
await shot(page, `${tag}-roster-canvas-${mode}`);
await page.locator('.editor-header__settings button, .edit-site-header-edit-mode__actions button', { hasText: /^Save$/ }).first().click();
await page.waitForTimeout(1200);
const p2 = page.locator('.entities-saved-states__panel').getByRole('button', { name: /^Save$/ }); if (await p2.count()) await p2.first().click();
await page.waitForFunction(() => wp.data.select('core').__experimentalGetDirtyEntityRecords().length === 0, null, { timeout: 30000 }).catch(() => {});
await page.waitForTimeout(1000);
const front = {};
for (const w of [1440, 1024, 390, 320]) {
  const p = await browser.newPage({ viewport: { width: w, height: 900 } });
  await p.goto(base + '/', { waitUntil: 'networkidle' });
  front[w] = await p.evaluate(() => {
    const tiles = [...document.querySelectorAll('.roster .tile')];
    return {
      n: tiles.length,
      ariaLabels: tiles.map(t => t.getAttribute('aria-label')).filter(Boolean),
      clipped: tiles.map(t => { const o = []; for (const s of t.querySelectorAll('.who span, .who b, .n, .town')) { if (s.scrollWidth > s.clientWidth + 1 || s.scrollHeight > s.clientHeight + 1) o.push(s.className + ':' + s.textContent + ' ' + s.clientWidth + '/' + s.scrollWidth); } return o; }).flat(),
      sample: tiles.slice(0, 3).map(t => { const tw = t.querySelector('.town'); const c = tw && getComputedStyle(tw); const r = tw && tw.getBoundingClientRect(); return tw ? `${tw.textContent} ${Math.round(r.width)}x${Math.round(r.height)} disp=${c.display} ws=${c.whiteSpace} shadow=${c.textShadow}` : t.innerText.slice(0, 60); }),
      overflow: document.documentElement.scrollWidth - innerWidth,
    };
  });
  const r = p.locator('.roster').first();
  if (await r.count()) await r.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-roster-front-${mode}-${w}.png` }).catch(() => {});
  await p.close();
}
save(`${tag}-roster-${mode}.json`, { before, after, canvas, front, log });
console.log(JSON.stringify({ after: after.slice(0, 300), canvas, front }, null, 1));
await browser.close();
