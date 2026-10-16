import { launch, login, openTemplate } from './lib.mjs';
const [base] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
const f = await openTemplate(page, base, false, 'header', 'wp_template_part');
console.log(JSON.stringify(await f.evaluate(() => { const nav = document.querySelector('.gm-bar nav, .gm-bar [data-type="core/group"]:not(.w)'); const c = getComputedStyle(nav); return { tag: nav.tagName, cls: nav.className.slice(0, 120), disp: c.display, align: c.alignItems, h: nav.getBoundingClientRect().height, kids: [...nav.children].map(k => { const r = k.getBoundingClientRect(); const s = getComputedStyle(k); return k.tagName + '.' + k.className.slice(0, 60) + ' h=' + Math.round(r.height) + ' y=' + Math.round(r.top) + ' lh=' + s.lineHeight + ' fs=' + s.fontSize + ' pad=' + s.paddingTop + '/' + s.paddingBottom + ' minh=' + s.minHeight; }) }; }), null, 1));
await browser.close();
