import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
const [auth] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const ctx = await b.newContext({ viewport: { width: 1440, height: 1000 }, storageState: auth });
const p = await ctx.newPage();
await p.goto('http://127.0.0.1:8080/wp-admin/site-editor.php?p=%2Fwp_template%2Fgeneration-maine%2F%2Ffront-page&canvas=edit', { waitUntil: 'networkidle' }).catch(() => {});
await p.waitForTimeout(7000);
const f = p.frames().find(f => f.name() === 'editor-canvas');
const r = await f.evaluate(() => {
  const k = document.querySelector('.k-bars'); const cs = k ? getComputedStyle(k, '::before') : null;
  const img = document.querySelector('.about .ph img'); const fig = document.querySelector('.about .ph');
  const rules = [...document.styleSheets].flatMap(s => { try { return [...s.cssRules]; } catch (e) { return []; } }).map(r => r.cssText).filter(t => t.includes('k-bars')).map(t => t.slice(0, 160));
  return { kbars: k ? { content: cs.content, w: cs.width, bg: cs.backgroundImage.slice(0, 60), display: getComputedStyle(k).display } : null, rules,
    img: img ? { src: img.currentSrc.split('/').slice(-2).join('/'), natural: img.naturalWidth, box: [Math.round(img.getBoundingClientRect().width), Math.round(img.getBoundingClientRect().height)], pos: getComputedStyle(img).position, parent: img.parentElement.className.slice(0, 60) } : null,
    fig: fig ? [Math.round(fig.getBoundingClientRect().width), Math.round(fig.getBoundingClientRect().height)] : null };
});
console.log(JSON.stringify(r, null, 1));
await b.close();
