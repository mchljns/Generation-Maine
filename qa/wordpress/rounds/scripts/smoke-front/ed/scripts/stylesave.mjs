// Styles: open revisions, then set Typography > Text > Text alignment Left and save; dump REST and stored post after.
import { launch, login, save, shot, guide, watch } from './lib.mjs';
const [base, tag] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 1000 });
const log = []; watch(page, log);
const out = {};
out.restBefore = await page.evaluate(async () => { const r = await fetch('/wp-json/wp/v2/global-styles/themes/generation-maine?context=edit', { headers: { 'X-WP-Nonce': wpApiSettings.nonce } }).catch(() => null); return r ? r.status : null; }).catch(() => 'n/a');
await page.goto(base + '/wp-admin/site-editor.php?p=%2Fstyles', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(6000); await guide(page);
out.userConfig = await page.evaluate(async () => { const id = wp.data.select('core').__experimentalGetCurrentGlobalStylesId(); const r = await wp.apiFetch({ path: '/wp/v2/global-styles/' + id + '?context=edit' }); const rev = await wp.apiFetch({ path: '/wp/v2/global-styles/' + id + '/revisions?context=edit' }).catch(e => ({ err: e.message })); return { id, item: JSON.stringify({ s: r.styles, t: r.settings }).slice(0, 800), revisions: Array.isArray(rev) ? rev.map(x => JSON.stringify({ s: x.styles, t: x.settings }).slice(0, 300)) : rev }; });
// revisions screen
const revBtn = page.getByRole('button', { name: /Revisions/ }).first();
if (await revBtn.count()) { await revBtn.click(); await page.waitForTimeout(2500); out.revScreen = (await page.locator('body').innerText()).replace(/\s+/g, ' ').match(/Revisions.{0,400}/)?.[0]; await shot(page, `${tag}-styles-revisions`); await page.goto(base + '/wp-admin/site-editor.php?p=%2Fstyles', { waitUntil: 'domcontentloaded' }); await page.waitForTimeout(5000); await guide(page); }
await page.getByRole('button', { name: /^Typography/ }).first().click(); await page.waitForTimeout(1200);
await page.getByRole('button', { name: /^(Aa )?Text$/ }).first().click(); await page.waitForTimeout(1200);
const left = page.getByRole('radio', { name: /Align text left/i }).or(page.getByRole('button', { name: /Align text left/i })).first();
out.left = await left.count();
if (out.left) await left.click();
await page.waitForTimeout(800);
await page.getByRole('button', { name: /^(Save|Review \d+ changes?…?)$/ }).first().click(); await page.waitForTimeout(1500);
const p2 = page.locator('.entities-saved-states__panel').getByRole('button', { name: /^Save$/ }); if (await p2.count()) await p2.first().click();
await page.waitForTimeout(3500);
out.snack = await page.locator('.components-snackbar').allInnerTexts();
save(`${tag}-stylesave.json`, { out, log });
console.log(JSON.stringify(out, null, 1));
await browser.close();
