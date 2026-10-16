// Post editor with "Show template" turned on from the View/preview menu: title and text position against the page.
import { launch, login, save, shot } from './lib.mjs';
const [base, pid, tag] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
await page.goto(`${base}/wp-admin/post.php?post=${pid}&action=edit`, { waitUntil: 'domcontentloaded' });
await page.waitForFunction(() => window.wp && wp.data && wp.data.select('core/editor').getCurrentPostId(), null, { timeout: 90000 });
await page.waitForTimeout(3000);
for (let i = 0; i < 3; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click().catch(() => {}); await page.waitForTimeout(400); } }
// the device preview / View menu holds "Show template"
const view = page.locator('button[aria-label="View"], button[aria-label="Preview"]').first();
let toggled = false, menu = [];
if (await view.count()) {
  await view.click(); await page.waitForTimeout(600);
  menu = await page.locator('[role="menuitem"], [role="menuitemcheckbox"], [role="menuitemradio"]').allInnerTexts();
  const st = page.getByRole('menuitemcheckbox', { name: /Show template/ });
  if (await st.count()) { await st.click(); toggled = true; await page.waitForTimeout(2500); }
  await page.keyboard.press('Escape');
}
const mode = await page.evaluate(() => { const s = wp.data.select('core/editor'); return s.getRenderingMode ? s.getRenderingMode() : 'n/a'; });
const fh = await page.$('iframe[name="editor-canvas"]');
const frame = fh ? await fh.contentFrame() : page.mainFrame();
await page.waitForTimeout(1500);
const m = await frame.evaluate(() => {
  const R = e => { if (!e) return null; const r = e.getBoundingClientRect(); const c = getComputedStyle(e); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), fs: c.fontSize, pl: c.paddingLeft }; };
  const pc = document.querySelector('.wp-block-post-content');
  return { vw: document.documentElement.clientWidth, title: R(document.querySelector('h1')), postContent: R(pc), postContentCls: pc && pc.className, p: R(document.querySelector('.wp-block-post-content p')), h2: R(document.querySelector('.wp-block-post-content h2')), bar: R(document.querySelector('.gm-bar, header')) };
});
await shot(page, `${tag}-showtemplate`);
save(`${tag}-showtemplate.json`, { toggled, menu, mode, m });
console.log(JSON.stringify({ toggled, menu, mode, m }, null, 1));
// restore the mode so later checks start from the default
if (toggled) { await view.click(); await page.waitForTimeout(500); const st = page.getByRole('menuitemcheckbox', { name: /Show template/ }); if (await st.count()) await st.click(); }
await browser.close();
