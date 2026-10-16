import { launch, login, openTemplate } from './lib.mjs';
const [base, v65s] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
for (const [slug, type] of [['header', 'wp_template_part'], ['front-page', 'wp_template']]) {
  const f = await openTemplate(page, base, v65s === '1', slug, type);
  console.log(slug, JSON.stringify(await f.evaluate(() => { const w = document.querySelector('.gm-bar .w'); const c = getComputedStyle(w); return { bar: Math.round(document.querySelector('.gm-bar').getBoundingClientRect().height), w: { h: Math.round(w.getBoundingClientRect().height), pad: c.paddingTop + ' ' + c.paddingBottom, minH: c.minHeight, height: c.height, wrap: c.flexWrap }, kids: [...w.children].map(k => { const r = k.getBoundingClientRect(); return (k.dataset.type || k.className.slice(0, 40)) + ' ' + Math.round(r.height) + ' ' + getComputedStyle(k).display + ' mt=' + getComputedStyle(k).marginTop + ' mb=' + getComputedStyle(k).marginBottom; }) }; })));
}
await browser.close();
