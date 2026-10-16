// Check the cause: set --wp--style--block-gap to 0px (with a unit) on the page and re-measure the gallery.
import { launch } from './lib.mjs';
const [url] = process.argv.slice(2);
const browser = await launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await page.goto(url, { waitUntil: 'networkidle' });
const m = () => page.evaluate(() => [...document.querySelectorAll('.wp-block-gallery')].map(g => [...g.querySelectorAll('figure.wp-block-image')].map(f => { const r = f.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.width)]; })));
console.log('as shipped', JSON.stringify(await m()));
await page.addStyleTag({ content: 'body{--wp--style--block-gap:0px}' });
console.log('block-gap 0px', JSON.stringify(await m()));
await page.addStyleTag({ content: 'main.gm-page .wp-block-gallery.is-layout-flex{gap:var(--wp--style--unstable-gallery-gap)}' });
console.log('+ gallery gap = its variable', JSON.stringify(await m()));
await browser.close();
