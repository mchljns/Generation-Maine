import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
import fs from 'fs';
export const OUT = '/tmp/claude-0/wptest/work/smoke-front/ed';
export const ZIP = '/home/user/Generation-Maine/dist/generation-maine.zip';
export function save(name, data) {
  const p = `${OUT}/data/${name}`;
  fs.writeFileSync(p, typeof data === 'string' ? data : JSON.stringify(data, null, 2));
  return p;
}
export async function launch() {
  return chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
}
export function watch(page, sink, tag = '') {
  page.on('pageerror', e => sink.push(`${tag}pageerror: ${String(e).slice(0, 300)}`));
  page.on('console', m => { if (m.type() === 'error') sink.push(`${tag}console.error: ${m.text().slice(0, 300)}`); });
}
export async function login(browser, base, { w = 1440, h = 900, mobile = false } = {}) {
  const statePath = `${OUT}/data/state-${new URL(base).port}.json`;
  const ctxOpts = { viewport: { width: w, height: h } };
  if (mobile) Object.assign(ctxOpts, { isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  if (fs.existsSync(statePath)) ctxOpts.storageState = statePath;
  const ctx = await browser.newContext(ctxOpts);
  const page = await ctx.newPage();
  page.setDefaultTimeout(+process.env.PWTIMEOUT || 45000);
  await page.goto(base + '/wp-admin/', { waitUntil: 'domcontentloaded' });
  if (page.url().includes('wp-login.php')) {
    await page.fill('#user_login', 'admin');
    await page.fill('#user_pass', 'adminpass');
    await Promise.all([page.waitForURL(/wp-admin/), page.click('#wp-submit')]);
    await ctx.storageState({ path: statePath });
  }
  return { ctx, page };
}
export async function shot(page, name, opts = {}) {
  const p = `${OUT}/shots/${name}.png`;
  await page.screenshot({ path: p, ...opts });
  return p;
}
export async function canvas(page) {
  const h = await page.waitForSelector('iframe[name="editor-canvas"]', { timeout: 90000 });
  const f = await h.contentFrame();
  await f.waitForSelector('.is-root-container', { timeout: 90000 });
  return f;
}
export async function guide(page) {
  for (let i = 0; i < 5; i++) {
    const g = page.getByRole('button', { name: 'Get started' });
    if (await g.count()) { await g.first().click().catch(() => {}); await page.waitForTimeout(400); continue; }
    const c = page.locator('.components-modal__frame button[aria-label="Close"]');
    if (await c.count()) { await c.first().click().catch(() => {}); await page.waitForTimeout(400); continue; }
    break;
  }
}
export const FRONT71 = '/wp-admin/site-editor.php?p=%2Fwp_template%2Fgeneration-maine%2F%2Ffront-page&canvas=edit';
export const FRONT65 = '/wp-admin/site-editor.php?postType=wp_template&postId=generation-maine%2F%2Ffront-page&canvas=edit';
export async function wpver(page) {
  return page.evaluate(() => (document.body.className.match(/branch-(\d+-\d+)/) || [])[1] || '');
}
export async function openTemplate(page, base, v65, slug = 'front-page', type = 'wp_template') {
  const url = v65
    ? `${base}/wp-admin/site-editor.php?postType=${type}&postId=generation-maine%2F%2F${slug}&canvas=edit`
    : `${base}/wp-admin/site-editor.php?p=%2F${type}%2Fgeneration-maine%2F%2F${slug}&canvas=edit`;
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  const f = await canvas(page);
  await page.waitForTimeout(2500);
  await guide(page);
  await page.waitForTimeout(500);
  return f;
}
export async function saveSite(page) {
  const save = page.locator('.editor-header__settings button, .edit-site-header-edit-mode__actions button', { hasText: /^Save$/ }).first();
  await save.click();
  await page.waitForTimeout(1200);
  const panel = page.locator('.entities-saved-states__panel');
  let entities = [];
  if (await panel.count()) {
    entities = await panel.locator('.components-checkbox-control__label, label').allInnerTexts();
    await panel.getByRole('button', { name: /^Save$/ }).first().click();
  }
  for (let i = 0; i < 60; i++) {
    const dirty = await page.evaluate(() => wp.data.select('core').__experimentalGetDirtyEntityRecords().length + (wp.data.select('core').isSavingEntityRecord ? 0 : 0));
    const saving = await page.evaluate(() => { const s = wp.data.select('core'); return s.__experimentalGetEntitiesBeingSaved ? s.__experimentalGetEntitiesBeingSaved().length : 0; });
    if (!dirty && !saving) break;
    await page.waitForTimeout(300);
  }
  await page.waitForTimeout(1000);
  const snack = await page.locator('.components-snackbar').allInnerTexts().catch(() => []);
  return { entities, snack };
}
export async function openListView(page) {
  const lv = page.locator('.block-editor-list-view-tree');
  if (!(await lv.count())) {
    const b = page.getByRole('button', { name: /Document Overview|List View/ }).first();
    await b.click(); await page.waitForTimeout(800);
  }
  for (let i = 0; i < 8; i++) {
    const ex = page.locator('.block-editor-list-view-tree a[aria-expanded="false"] .block-editor-list-view__expander');
    const n = await ex.count();
    if (!n) break;
    for (let j = n - 1; j >= 0; j--) await ex.nth(j).click({ force: true }).catch(() => {});
    await page.waitForTimeout(300);
  }
}
export async function lvRows(page) {
  return page.$$eval('.block-editor-list-view-tree tr', trs => trs.map(t => ({ level: +t.getAttribute('aria-level'), label: (t.querySelector('.block-editor-list-view-block-select-button__title') || t).innerText.trim(), id: t.dataset.block })));
}
export async function tree(page) {
  return page.evaluate(() => {
    const s = wp.data.select('core/block-editor');
    const walk = (ids, d) => ids.map(id => { const b = s.getBlock(id); const a = b.attributes; return '  '.repeat(d) + b.name + (a.metadata && a.metadata.name ? ' "' + a.metadata.name + '"' : '') + (a.className ? ' .' + a.className : '') + (b.name === 'generation-maine/part' ? ' name=' + a.name : '') + (a.lock ? ' lock=' + JSON.stringify(a.lock) : '') + ' mode=' + (s.getBlockEditingMode ? s.getBlockEditingMode(id) : '?') + '\n' + walk(s.getBlockOrder(id), d + 1).join(''); });
    return walk(s.getBlockOrder(''), 0).join('');
  });
}
export async function fetchText(url) {
  const r = await fetch(url);
  return { status: r.status, text: await r.text() };
}
