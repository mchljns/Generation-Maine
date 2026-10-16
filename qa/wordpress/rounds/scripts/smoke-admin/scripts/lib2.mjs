// Shared helpers for this attempt. Probes are inert markers (an <i> with a data-gmprobe attribute); a probe that shows up as
// a real element or attribute in the DOM means the value reached the page unescaped.
import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
import { execSync } from 'child_process';
export const B = process.env.GMB || 'http://127.0.0.1:8704';
export const W = process.env.GMW || '/tmp/claude-0/wptest/work/smoke-admin/logs';
export const browser = () => chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
export async function login(ctx, user, pass) {
  const page = await ctx.newPage();
  for (let i = 0; i < 3; i++) {
    await page.goto(B + '/wp-login.php', { waitUntil: 'load' });
    await page.fill('#user_login', user); await page.fill('#user_pass', pass);
    await page.click('#wp-submit');
    try { await page.waitForURL(u => !/wp-login\.php/.test(String(u)), { timeout: 30000 }); return page; } catch (e) { /* retry */ }
  }
  throw new Error('login failed for ' + user);
}
export const wp = args => { try { return execSync('wpt wp ' + (process.env.GMI || 'r3p71') + ' ' + args + ' 2>/dev/null', { encoding: 'utf8' }).trim(); } catch (e) { return '(missing: exit ' + e.status + ')'; } };
export function watch(page, log) {
  page.on('dialog', async d => { log.push('DIALOG ' + d.message()); await d.dismiss(); });
  page.on('pageerror', e => log.push('PAGEERROR ' + e.message));
}
// what a visitor's DOM holds: probe elements/attributes, unsafe schemes, blank targets without noopener, JSON-LD
export async function scan(page) {
  return page.evaluate(() => {
    const probeEls = [...document.querySelectorAll('[data-gmprobe]')].map(e => e.outerHTML.slice(0, 160));
    const probeAttrs = []; document.querySelectorAll('*').forEach(el => { for (const a of el.attributes) if (/gmprobe/i.test(a.name)) probeAttrs.push(el.tagName + ' ' + a.name); });
    const schemes = [...document.querySelectorAll('[href],[src],[action],[data-src],[poster],[data-still]')].flatMap(e => ['href', 'src', 'action', 'data-src', 'poster', 'data-still'].map(n => e.getAttribute(n))).filter(v => v && /^\s*(javascript|data|vbscript):/i.test(v));
    const blank = [...document.querySelectorAll('[target=_blank]')].filter(a => !/noopener|noreferrer/.test(a.getAttribute('rel') || '')).map(a => a.outerHTML.slice(0, 160));
    const ld = [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => { try { return JSON.parse(s.textContent); } catch (e) { return 'PARSE ERROR ' + e.message; } });
    const scripts = document.querySelectorAll('script').length;
    return { probeEls, probeAttrs, schemes, blank, ld, scripts, title: document.title };
  });
}
