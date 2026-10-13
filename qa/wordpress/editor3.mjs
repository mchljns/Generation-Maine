import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
const [auth, out] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const ctx = await b.newContext({ viewport: { width: 1440, height: 1000 }, storageState: auth });
const p = await ctx.newPage();
await p.goto('http://127.0.0.1:8080/wp-admin/site-editor.php?p=%2Fwp_template%2Fgeneration-maine%2F%2Ffront-page&canvas=edit', { waitUntil: 'networkidle' }).catch(() => {});
await p.waitForTimeout(6000);
const f = p.frames().find(f => f.name() === 'editor-canvas');
await p.screenshot({ path: `${out}/editor-hero.png` });
for (const [sel, name] of [['.about', 'about'], ['.stories-head', 'creators'], ['.follow', 'follow'], ['[data-type="generation-maine/site-footer"]', 'footer']]) {
  await f.evaluate(s => document.querySelector(s).scrollIntoView({ block: 'start' }), sel); await p.waitForTimeout(1500);
  await p.screenshot({ path: `${out}/editor-${name}.png` });
}
console.log('bars before:', await f.evaluate(() => { const cs = getComputedStyle(document.querySelector('.k-bars'), '::before'); return cs.display + ' ' + cs.width; }));
await b.close();
