// Network inventory: every request with size and type, at load and after a full scroll.
// usage: node net.mjs <label> <url> <WxH> <outdir>
import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
import fs from 'node:fs';

const [label, url, vp, outdir] = process.argv.slice(2);
const [W, H] = vp.split('x').map(Number);
const phone = W <= 900;
fs.mkdirSync(outdir, { recursive: true });

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const ctx = await browser.newContext({
  viewport: { width: W, height: H },
  deviceScaleFactor: phone ? 3 : 1,
  isMobile: phone, hasTouch: phone, reducedMotion: process.env.REDUCE ? 'reduce' : 'no-preference',
});
const page = await ctx.newPage();
const cdp = await ctx.newCDPSession(page);
await cdp.send('Network.enable');

let phase = 'load';
const reqs = new Map();
cdp.on('Network.requestWillBeSent', e => {
  if (reqs.has(e.requestId) && e.redirectResponse) { /* redirect */ }
  reqs.set(e.requestId, { id: e.requestId, url: e.request.url, method: e.request.method, type: e.type, phase, t: e.timestamp, priority: e.request.initialPriority, initiator: e.initiator && e.initiator.type, isLinkPreload: !!e.request.isLinkPreload });
});
cdp.on('Network.responseReceived', e => { const r = reqs.get(e.requestId); if (r) { r.status = e.response.status; r.mime = e.response.mimeType; r.fromCache = e.response.fromDiskCache || e.response.fromPrefetchCache; } });
cdp.on('Network.loadingFinished', e => { const r = reqs.get(e.requestId); if (r) r.bytes = e.encodedDataLength; });
cdp.on('Network.loadingFailed', e => { const r = reqs.get(e.requestId); if (r) { r.failed = e.errorText; r.canceled = e.canceled; } });

const consoleMsgs = [];
page.on('console', m => consoleMsgs.push({ type: m.type(), text: m.text() }));
page.on('pageerror', e => consoleMsgs.push({ type: 'pageerror', text: String(e) }));

const t0 = Date.now();
await page.goto(url, { waitUntil: 'load', timeout: 90000 });
const loadMs = Date.now() - t0;
await page.waitForTimeout(3000);
const atLoad = await page.evaluate(() => {
  const res = performance.getEntriesByType('resource').map(r => ({ name: r.name, type: r.initiatorType, transfer: r.transferSize, body: r.encodedBodySize, rb: r.renderBlockingStatus, start: Math.round(r.startTime), end: Math.round(r.responseEnd) }));
  const nav = performance.getEntriesByType('navigation')[0];
  const paints = performance.getEntriesByType('paint').map(p => ({ name: p.name, t: Math.round(p.startTime) }));
  const imgs = [...document.images].map(i => { const r = i.getBoundingClientRect(); return { cls: i.className, src: i.currentSrc || i.getAttribute('src') || '', dataSrc: i.dataset.src || '', wAttr: i.getAttribute('width'), hAttr: i.getAttribute('height'), loading: i.getAttribute('loading'), nw: i.naturalWidth, nh: i.naturalHeight, rw: Math.round(r.width), rh: Math.round(r.height), top: Math.round(r.top + scrollY), visible: r.width > 0 && r.height > 0 && getComputedStyle(i).visibility !== 'hidden' }; });
  const fonts = [...document.fonts].map(f => ({ family: f.family, weight: f.weight, status: f.status }));
  return { res, nav: { ttfb: Math.round(nav.responseStart), dcl: Math.round(nav.domContentLoadedEventEnd), load: Math.round(nav.loadEventEnd), transfer: nav.transferSize, body: nav.encodedBodySize }, paints, imgs, fonts, docH: document.documentElement.scrollHeight };
});
const shot1 = `${outdir}/${label}-load.png`;
await page.screenshot({ path: shot1 });

// full vertical scroll in half-screen steps
phase = 'scroll';
let y = 0;
for (let i = 0; i < 400; i++) {
  const done = await page.evaluate(() => { scrollBy(0, Math.round(innerHeight * 0.5)); return innerHeight + scrollY >= document.documentElement.scrollHeight - 2; });
  await page.waitForTimeout(250);
  if (done) break;
}
await page.waitForTimeout(3000);
const afterScroll = await page.evaluate(() => ({ imgs: [...document.images].map(i => ({ cls: i.className, src: i.currentSrc || i.getAttribute('src') || '', nw: i.naturalWidth, nh: i.naturalHeight, rw: Math.round(i.getBoundingClientRect().width), rh: Math.round(i.getBoundingClientRect().height) })) }));

// on a phone, also swipe the creators track card by card
let swipe = null;
if (phone) {
  phase = 'swipe';
  await page.evaluate(() => { const s = document.getElementById('stories'); if (s) s.scrollIntoView(); });
  await page.waitForTimeout(800);
  const n = await page.evaluate(() => document.querySelectorAll('.panel').length);
  for (let k = 1; k < n; k++) {
    await page.evaluate(k => { const p = document.getElementById('panels'), c = document.querySelectorAll('.panel')[k]; p.scrollTo({ left: c.offsetLeft - parseFloat(getComputedStyle(p).paddingLeft), behavior: 'auto' }); }, k);
    await page.waitForTimeout(700);
  }
  await page.waitForTimeout(2000);
  swipe = { panels: n };
}

const list = [...reqs.values()].map(r => ({ ...r, file: r.url.startsWith('data:') ? 'data:' + r.url.slice(5, 40) : r.url.replace(/^https?:\/\/[^/]+/, '') }));
fs.writeFileSync(`${outdir}/${label}.json`, JSON.stringify({ label, url, vp, phone, loadMs, atLoad, afterScroll, swipe, requests: list, console: consoleMsgs }, null, 1));
await browser.close();

const sum = ph => { const xs = list.filter(r => r.phase === ph && !r.url.startsWith('data:')); return { n: xs.length, bytes: xs.reduce((a, r) => a + (r.bytes || 0), 0) }; };
console.log(label, JSON.stringify({ load: sum('load'), scroll: sum('scroll'), swipe: sum('swipe'), console: consoleMsgs.filter(m => m.type !== 'log').length }));
