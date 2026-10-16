// The bar in a narrow Site Editor canvas: settings open, List View open, inserter open, Tablet and Mobile previews, at two
// window widths. For each: canvas width, the bar's box, each label and the button (inside the bar?), the menu button.
// usage: node barcanvas.mjs <base> <tag> <v65 0|1> [slug] [type]
import { launch, login, save, shot, openTemplate } from './lib.mjs';
const [base, tag, v65s, slug = 'front-page', type = 'wp_template'] = process.argv.slice(2);
const v65 = v65s === '1';
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
await openTemplate(page, base, v65, slug, type);
const frame = async () => (await page.$('iframe[name="editor-canvas"]')).contentFrame();
const measure = async () => {
  const f = await frame();
  return f.evaluate(() => {
    const bar = document.querySelector('.gm-bar');
    const br = bar.getBoundingClientRect();
    const box = (e) => { if (!e) return null; const r = e.getBoundingClientRect(); const c = getComputedStyle(e); return { t: e.textContent.trim(), x: Math.round(r.left), y: Math.round(r.top - br.top), w: Math.round(r.width), h: Math.round(r.height), disp: c.display, vis: c.visibility, inside: r.width > 0 && r.top >= br.top - 0.5 && r.bottom <= br.bottom + 0.5 && r.left >= br.left - 0.5 && r.right <= br.right + 0.5 }; };
    const hero = document.querySelector('.hero');
    const heroK = document.querySelector('.hero .k');
    return {
      canvasW: document.documentElement.clientWidth,
      bar: { w: Math.round(br.width), h: Math.round(br.height), top: Math.round(br.top) },
      labels: [...bar.querySelectorAll('nav a')].map(box),
      button: box(bar.querySelector('.cta .wp-block-button__link, .cta a')),
      logo: box(bar.querySelector('.logo, a[aria-label*="home"]')),
      menu: (() => { const m = bar.querySelector('.menu'); return m ? getComputedStyle(m).display : null; })(),
      heroTopVsBarBottom: hero ? Math.round(hero.getBoundingClientRect().top - br.bottom) : null,
      kickerTopVsBarBottom: heroK ? Math.round(heroK.getBoundingClientRect().top - br.bottom) : null,
      wOverflow: (() => { const w = bar.querySelector('.w'); return w ? w.scrollWidth - w.clientWidth : null; })(),
    };
  });
};
const res = {};
const toggle = async (re) => { const b = page.getByRole('button', { name: re }).first(); await b.click(); await page.waitForTimeout(1500); };
const device = async (name) => {
  // 7.1: the View / Preview dropdown; 6.5: "View" dropdown with Desktop / Tablet / Mobile
  const v = page.locator('button[aria-label="View"], button[aria-label="Preview"], button[aria-label="Device preview"]').first();
  if (!(await v.count())) return false;
  await v.click(); await page.waitForTimeout(500);
  const it = page.getByRole('menuitemradio', { name: new RegExp('^' + name) }).or(page.getByRole('menuitem', { name: new RegExp('^' + name) })).first();
  if (!(await it.count())) { await page.keyboard.press('Escape'); return false; }
  await it.click(); await page.waitForTimeout(2500);
  await page.keyboard.press('Escape').catch(() => {});
  return true;
};
for (const W of [1440, 1024]) {
  await page.setViewportSize({ width: W, height: 900 }); await page.waitForTimeout(1500);
  res[`${W} default`] = await measure();
  await toggle(/^(Document Overview|List View)$/);
  res[`${W} list view`] = await measure();
  await shot(page, `${tag}-${slug}-bar-${W}-listview`, { clip: { x: 0, y: 0, width: W, height: 360 } });
  await toggle(/^(Document Overview|List View|Close)$/);
  await page.locator('button[aria-label="Block Inserter"], button[aria-label="Toggle block inserter"], .editor-document-tools__inserter-toggle, .edit-site-header-edit-mode__inserter-toggle').first().click(); await page.waitForTimeout(2000);
  res[`${W} inserter`] = await measure();
  await shot(page, `${tag}-${slug}-bar-${W}-inserter`, { clip: { x: 0, y: 0, width: W, height: 360 } });
  await page.locator('button[aria-label="Block Inserter"], button[aria-label="Toggle block inserter"], .editor-document-tools__inserter-toggle, .edit-site-header-edit-mode__inserter-toggle').first().click(); await page.waitForTimeout(1000);
}
await page.setViewportSize({ width: 1440, height: 900 }); await page.waitForTimeout(1000);
for (const d of ['Tablet', 'Mobile']) {
  let ok = false; try { ok = await Promise.race([device(d), new Promise(r => setTimeout(() => r(false), 8000))]); } catch (e) { ok = false; }
  if (ok) { await page.waitForTimeout(1500); res[d] = await measure(); await shot(page, `${tag}-${slug}-bar-${d}`); }
  else res[d] = 'no device menu';
}
await Promise.race([device('Desktop').catch(() => {}), new Promise(r => setTimeout(r, 8000))]);
save(`${tag}-${slug}-barcanvas.json`, res);
for (const [k, v] of Object.entries(res)) {
  if (typeof v === 'string') { console.log(k, v); continue; }
  const bad = [...v.labels, v.button].filter(x => !x || !x.inside).map(x => x ? `${x.t}@${x.x},${x.y} ${x.w}x${x.h} ${x.disp}` : 'missing');
  console.log(`${k.padEnd(18)} canvas=${v.canvasW} bar=${v.bar.w}x${v.bar.h} menu=${v.menu} kickerGap=${v.kickerTopVsBarBottom} overflow=${v.wOverflow} labels=${v.labels.map(l => `${l.t}@${l.x},${l.y}`).join(' ')} button=${v.button ? v.button.t + '@' + v.button.x + ',' + v.button.y + ' ' + v.button.w + 'x' + v.button.h + ' ' + v.button.disp : 'none'} NOT INSIDE: ${bad.join('; ') || '-'}`);
}
await browser.close();
