import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
import { execSync } from 'child_process';
export const W = '/tmp/claude-0/wptest/work/smoke-admin';
export const SHOTS = W + '/shots';
export const M = '/tmp/claude-0/wptest/media/';
export const INST = { 8952: 'sa71', 8962: 'sa65' };
export function base(port) { return 'http://127.0.0.1:' + port; }
export async function launch() { return chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); }
export function wp(inst, args) {
  try { return execSync(`wpt wp ${inst} ${args} 2>/dev/null`, { maxBuffer: 64 * 1024 * 1024 }).toString().trim(); } catch (e) { return 'ERR:' + (e.stdout ? e.stdout.toString() : '') + (e.stderr ? e.stderr.toString() : ''); }
}
export async function login(ctx, B, user = 'admin', pass = 'adminpass') {
  const p = await ctx.newPage();
  await p.goto(B + '/wp-login.php?redirect_to=' + encodeURIComponent(B + '/wp-admin/profile.php'));
  await p.fill('#user_login', user); await p.fill('#user_pass', pass);
  await p.click('#wp-submit');
  for (let i = 0; i < 240 && p.url().includes('wp-login.php'); i++) await p.waitForTimeout(250);
  await p.waitForLoadState('domcontentloaded').catch(() => {});
  const ok = !p.url().includes('wp-login.php');
  await p.close();
  if (!ok) throw new Error('login failed ' + user);
  return ok;
}
export async function dismissGuide(p) {
  for (let i = 0; i < 3; i++) {
    const btn = p.locator('.components-modal__frame button[aria-label="Close"]');
    if (await btn.count() && await btn.first().isVisible()) { await btn.first().click().catch(() => {}); await p.waitForTimeout(300); } else break;
  }
}
export function watch(p, errs) {
  p.on('pageerror', e => errs.push('pageerror: ' + e.message));
  p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  p.on('dialog', d => { errs.push('dialog: ' + d.message()); d.accept(); });
}
export async function metaDrawer(p, open) {
  const mb = p.getByRole('button', { name: /Meta Boxes/ });
  if (!(await mb.count())) return 'no-drawer-button';
  const cur = (await mb.first().getAttribute('aria-expanded')) === 'true';
  if (cur !== open) { await mb.first().click({ position: { x: 30, y: 10 } }); await p.waitForTimeout(900); }
  return (await mb.first().getAttribute('aria-expanded'));
}
export const sleep = ms => new Promise(r => setTimeout(r, ms));
export async function publishOrUpdate(p) {
  await p.locator('.components-snackbar').evaluateAll(els => els.forEach(e => e.remove())).catch(() => {});
  const upd = p.getByRole('button', { name: /^(Save|Update)$/ });
  if (await upd.count() && await upd.first().isVisible()) { await upd.first().click(); }
  else {
    const pub = p.getByRole('button', { name: /^(Publish|Submit for Review)$/ }).first();
    await pub.click();
    await p.waitForTimeout(1200);
    const pp = p.locator('.editor-post-publish-panel__header-publish-button button');
    if (await pp.count()) await pp.first().click();
  }
  await p.waitForSelector('.components-snackbar', { timeout: 30000 }).catch(() => {});
  await p.waitForFunction(() => !document.querySelector('.editor-post-publish-button.is-busy, .editor-post-saved-state.is-saving, .is-saving'), null, { timeout: 30000 }).catch(() => {});
  await p.waitForTimeout(2500);
  return await p.locator('.components-snackbar').allInnerTexts();
}
export async function openEditor(p, B, id) {
  await p.goto(B + '/wp-admin/post.php?post=' + id + '&action=edit');
  await p.waitForSelector('.editor-header, .edit-post-header', { timeout: 60000 });
  await p.waitForTimeout(2500); await dismissGuide(p);
}
