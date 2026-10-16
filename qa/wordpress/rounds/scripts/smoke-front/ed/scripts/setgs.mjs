// Write the user's global styles the way the Styles panel saves them (REST PUT), then read back.
import { launch, login, save } from './lib.mjs';
const [base, tag, json] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base);
await page.goto(base + '/wp-admin/site-editor.php', { waitUntil: 'domcontentloaded' });
await page.waitForFunction(() => window.wp && wp.apiFetch && wp.data && wp.data.select('core'), null, { timeout: 90000 });
await page.waitForTimeout(3000);
const out = await page.evaluate(async (j) => {
  const id = wp.data.select('core').__experimentalGetCurrentGlobalStylesId();
  const body = JSON.parse(j);
  const r = await wp.apiFetch({ path: '/wp/v2/global-styles/' + id, method: 'POST', data: { id, ...body } });
  return { id, styles: r.styles, settings: Object.keys(r.settings || {}) };
}, json);
save(`${tag}-setgs.json`, out);
console.log(JSON.stringify(out));
await browser.close();
