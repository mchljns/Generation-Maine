import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
const [out, auth] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const ctx = await b.newContext({ viewport: { width: 1440, height: 1000 }, storageState: auth });
const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
for (const [label, path] of [['template', '/wp-admin/site-editor.php?p=%2Fwp_template%2Fgeneration-maine%2F%2Ffront-page&canvas=edit'], ['creator', '/wp-admin/post.php?post=' + process.argv[4] + '&action=edit'], ['settings', '/wp-admin/options-general.php?page=generation_maine']]) {
  await p.goto('http://127.0.0.1:8080' + path, { waitUntil: 'networkidle' }).catch(() => {});
  await p.waitForTimeout(label === 'settings' ? 800 : 7000);
  const frame = p.frames().find(f => f.name() === 'editor-canvas' || (f.url() || '').includes('blob:')) || p.mainFrame();
  const info = await frame.evaluate(() => ({
    invalid: document.querySelectorAll('.block-editor-warning, .block-editor-block-list__block.has-warning').length,
    blocks: document.querySelectorAll('[data-type]').length,
    types: [...new Set([...document.querySelectorAll('[data-type]')].map(e => e.dataset.type))].slice(0, 30),
    heroFont: (() => { const h = document.querySelector('.hero h1, h1'); return h ? getComputedStyle(h).fontFamily.split(',')[0] + ' ' + getComputedStyle(h).fontSize : null; })(),
    navFont: (() => { const a = document.querySelector('.top nav a'); return a ? getComputedStyle(a).fontFamily.split(',')[0] : null; })(),
  })).catch(e => ({ err: String(e).slice(0, 200) }));
  const admin = await p.evaluate(() => ({ adminBodyFont: getComputedStyle(document.body).fontFamily.split(',')[0], h1: (document.querySelector('.wrap h1') || {}).textContent || null, fields: document.querySelectorAll('.form-table input').length }));
  await p.screenshot({ path: `${out}/editor-${label}.png` });
  console.log(label, JSON.stringify(info), JSON.stringify(admin));
}
console.log('page errors', JSON.stringify(errs.slice(0, 5)));
await b.close();
