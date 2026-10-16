import { launch } from './lib.mjs';
const [base, tag] = process.argv.slice(2);
const browser = await launch();
for (const w of [1440, 1024, 390, 320]) {
  const p = await browser.newPage({ viewport: { width: w, height: 900 } });
  await p.goto(base + '/', { waitUntil: 'networkidle' });
  const grid = p.locator('.tile').first().locator('xpath=..');
  await grid.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-roster-tiles-${w}.png` });
  console.log(w, await grid.evaluate(g => g.className + ' ' + Math.round(g.getBoundingClientRect().width) + 'x' + Math.round(g.getBoundingClientRect().height)));
  await p.close();
}
await browser.close();
