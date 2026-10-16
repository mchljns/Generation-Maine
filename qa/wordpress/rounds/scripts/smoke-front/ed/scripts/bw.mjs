import { launch } from './lib.mjs';
const [url] = process.argv.slice(2);
const browser = await launch();
for (const w of [1440, 390]) {
  const page = await browser.newPage({ viewport: { width: w, height: 900 } });
  await page.goto(url, { waitUntil: 'networkidle' });
  console.log(w, JSON.stringify(await page.evaluate(() => [...document.querySelectorAll('main .wp-block-buttons')].map(g => ({ w: Math.round(g.getBoundingClientRect().width), items: [...g.querySelectorAll('.wp-block-button')].map(b => { const r = b.getBoundingClientRect(); return [b.textContent.trim(), Math.round(r.left), Math.round(r.top), Math.round(r.width), getComputedStyle(b).width]; }) })))));
  await page.close();
}
await browser.close();
