// Open the Front Page, click the headline and click away without typing: the template must stay clean. Also the Undo
// button state. Then select the headline and press Escape, Tab away.
import { launch, login, save, openTemplate, watch } from './lib.mjs';
const [base, tag, v65s] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
const log = []; watch(page, log);
const out = {};
await openTemplate(page, base, v65s === '1');
const f = await (await page.$('iframe[name="editor-canvas"]')).contentFrame();
const dirty = () => page.evaluate(() => wp.data.select('core').__experimentalGetDirtyEntityRecords().map(r => r.name + ':' + (r.key || '')));
const undo = () => page.evaluate(() => { const s = wp.data.select('core'); return s.hasUndo ? s.hasUndo() : (wp.data.select('core/editor').hasEditorUndo ? wp.data.select('core/editor').hasEditorUndo() : null); });
out.start = { dirty: await dirty(), undo: await undo() };
await f.locator('h1').first().click(); await page.waitForTimeout(500);
await f.locator('.hero .lede').first().click(); await page.waitForTimeout(900);
out.clickAway = { dirty: await dirty(), undo: await undo() };
await f.locator('h1').first().click(); await page.waitForTimeout(400);
await page.keyboard.press('End'); await page.waitForTimeout(200);
await page.keyboard.press('Escape'); await page.waitForTimeout(400);
await f.locator('.about').first().click({ position: { x: 5, y: 5 } }).catch(() => {}); await page.waitForTimeout(900);
out.escapeAway = { dirty: await dirty(), undo: await undo() };
save(`${tag}-cleanleave.json`, { out, log });
console.log(JSON.stringify(out));
await browser.close();
