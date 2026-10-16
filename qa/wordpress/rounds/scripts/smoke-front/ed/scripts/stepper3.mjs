// Creators block: Layout Stepper, Most creators to show 3, the two labels; save; read the stepper on the page at 1440.
import { launch, login, save, openTemplate } from './lib.mjs';
const [base, tag, v65s] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
await openTemplate(page, base, v65s === '1');
await page.evaluate(() => { const s = wp.data.select('core/block-editor'); const id = s.getClientIdsWithDescendants().find(id => s.getBlockName(id) === 'core/group' && / gm-creators /.test(' ' + (s.getBlock(id).attributes.className || '') + ' ')); wp.data.dispatch('core/block-editor').selectBlock(id); });
await page.waitForTimeout(600);
const ep = page.getByRole('button', { name: /^Edit pattern$/ }); if (await ep.count()) { await ep.first().click(); await page.waitForTimeout(1200); }
await page.evaluate(() => { const s = wp.data.select('core/block-editor'); const id = s.getClientIdsWithDescendants().find(id => s.getBlockName(id) === 'generation-maine/creators'); wp.data.dispatch('core/block-editor').selectBlock(id); });
await page.waitForTimeout(800);
const side = page.locator('.interface-complementary-area').first();
const bt = side.getByRole('tab', { name: 'Block' }); if (await bt.count()) await bt.first().click();
await side.getByLabel('Layout').selectOption('stepper'); await page.waitForTimeout(600);
const lim = side.getByRole('spinbutton', { name: /Most creators/ }); await lim.fill('3'); await lim.press('Tab');
await side.getByLabel('Label before the next name').fill('Up next: ');
await side.getByLabel('Label on the last creator').fill('That is all');
await page.waitForTimeout(2500);
const panel = (await side.innerText()).replace(/\s+/g, ' ').slice(0, 500);
await page.locator('.editor-header__settings button, .edit-site-header-edit-mode__actions button', { hasText: /^Save$/ }).first().click();
await page.waitForTimeout(1200);
const p2 = page.locator('.entities-saved-states__panel').getByRole('button', { name: /^Save$/ }); if (await p2.count()) await p2.first().click();
await page.waitForFunction(() => wp.data.select('core').__experimentalGetDirtyEntityRecords().length === 0, null, { timeout: 30000 }).catch(() => {});
const p = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await p.goto(base + '/', { waitUntil: 'networkidle' });
const front = await p.evaluate(() => ({ stories: [...document.querySelectorAll('[id^="story-"]')].map(e => e.id), next: [...document.querySelectorAll('.wnext, [id="wnext"], .where')].map(e => e.textContent.replace(/\s+/g, ' ').trim()).slice(0, 2), counter: (document.querySelector('.count, .where .n') || {}).textContent, segs: document.querySelectorAll('.segs button, .segs i, #segs > *').length }));
save(`${tag}-stepper3.json`, { panel, front });
console.log(JSON.stringify({ panel, front }, null, 1));
await browser.close();
