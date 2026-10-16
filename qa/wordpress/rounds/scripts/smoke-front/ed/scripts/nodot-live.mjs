// EDI-N04 live: the canvas dot as the headline's last character changes (keyboard only): ? then Backspace, ! then a period.
import { launch, login, save, openTemplate } from './lib.mjs';
const [base, tag, v65s] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
const f = await openTemplate(page, base, v65s === '1');
const K = page.keyboard;
const st = () => f.evaluate(() => { const h = document.querySelector('h1'); const a = getComputedStyle(h, '::after'); return (h.className.includes('gm-nodot') ? 'nodot' : 'dot') + ' after=' + a.content + ' | ' + h.innerText.replace(/\n/g, ' / '); });
const out = [];
await f.locator('h1').first().click(); await K.press('Control+a'); await K.press('Delete');
await K.type('Young Mainers'); await K.press('Shift+Enter'); await K.type('why do we stay');
out.push(['typed "stay"', await st()]);
await K.type('?'); await page.waitForTimeout(300); out.push(['typed "?"', await st()]);
await K.press('Backspace'); await page.waitForTimeout(300); out.push(['Backspace', await st()]);
await K.type('!'); await page.waitForTimeout(300); out.push(['typed "!"', await st()]);
await K.press('Backspace'); await K.type('.'); await page.waitForTimeout(300); out.push(['"!" replaced by "."', await st()]);
await K.type('?'); await page.waitForTimeout(300); out.push(['typed "?" after the period', await st()]);
await K.press('Shift+Enter'); await page.waitForTimeout(300); out.push(['line break after "?"', await st()]);
await K.press('Control+z'); await K.press('Control+z'); await K.press('Control+z'); await page.waitForTimeout(300); out.push(['undo x3', await st()]);
// leave without saving: reload discards
save(`${tag}-nodot-live.json`, out);
for (const [a, b] of out) console.log(a.padEnd(30), b);
await browser.close();
