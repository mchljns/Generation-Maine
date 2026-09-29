// QA runner: screenshots, overflow checks and axe-core for both creator states.
// Needs the Playground server from README (port 9400) with qa/mu-plugins mounted.
// Usage: node qa/run-qa.mjs [baseUrl]
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import fs from 'node:fs';
import path from 'node:path';

const base = process.argv[2] || 'http://127.0.0.1:9400';
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname));
const shots = path.join(root, 'screenshots');
fs.mkdirSync(shots, { recursive: true });
const exe = fs.existsSync('/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
  ? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' : undefined;

const browser = await chromium.launch({ executablePath: exe });
// The Playground auto-login cookie flag without an auth cookie gives an anonymous visitor.
const ctx = await browser.newContext();
await ctx.addCookies([{ name: 'playground_auto_login_already_happened', value: '1', url: base }]);
const page = await ctx.newPage();
const consoleErrors = [];
page.on('console', (m) => { if (m.type() === 'error') consoleErrors.push(m.text()); });
page.on('pageerror', (e) => consoleErrors.push(String(e)));

const results = { states: {} };
for (const [state, n] of [['0-creators', 0], ['12-creators', 12]]) {
  await page.goto(`${base}/?gm_seed=${n}`, { waitUntil: 'networkidle' });
  const r = { widths: {}, axe: null };
  for (const w of [375, 768, 1440]) {
    await page.setViewportSize({ width: w, height: 900 });
    await page.goto(base + '/', { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    const html = await page.content();
    const phpProblems = (html.match(/(Fatal error|Warning<\/b>|Notice<\/b>|Deprecated<\/b>)/g) || []).length;
    const overflow = await page.evaluate(() => {
      const docW = document.documentElement.clientWidth;
      const wide = [];
      document.querySelectorAll('body *').forEach((el) => {
        const b = el.getBoundingClientRect();
        if (b.width && (b.right > docW + 1 || b.left < -1)) {
          const cs = getComputedStyle(el);
          if (cs.position !== 'fixed' && !el.closest('.screen-reader-text, .gm-skip-link')) wide.push(el.tagName.toLowerCase() + '.' + [...el.classList].slice(0, 2).join('.'));
        }
      });
      return { scrollWidth: document.documentElement.scrollWidth, clientWidth: docW, offenders: [...new Set(wide)].slice(0, 10) };
    });
    const brokenImages = await page.evaluate(() => [...document.images].filter((i) => i.complete && i.naturalWidth === 0).map((i) => i.src));
    const attribution = await page.evaluate(() => {
      const t = document.body.innerText;
      const firstScreen = [...document.querySelectorAll('.gm-hero *')].some((e) => /initiative of Maine Policy Institute/i.test(e.textContent));
      return { heroLine: firstScreen, section: !!document.querySelector('#maine-policy'), footer: /initiative of Maine Policy Institute/i.test(document.querySelector('footer')?.innerText || ''), count: (t.match(/Maine Policy Institute/g) || []).length };
    });
    const file = path.join(shots, `${state}-${w}.png`);
    await page.screenshot({ path: file, fullPage: true });
    r.widths[w] = { phpProblems, overflow, brokenImages, attribution, screenshot: path.relative(root, file) };
  }
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto(base + '/', { waitUntil: 'networkidle' });
  const axe = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice']).analyze();
  await page.setViewportSize({ width: 375, height: 800 });
  const axeMobile = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice']).analyze();
  const summarize = (a) => a.violations.map((v) => ({ id: v.id, impact: v.impact, nodes: v.nodes.length, help: v.help, targets: v.nodes.slice(0, 3).map((n) => n.target.join(' ')) }));
  r.axe = { desktop: summarize(axe), mobile: summarize(axeMobile) };
  results.states[state] = r;
}
results.consoleErrors = [...new Set(consoleErrors)];
fs.writeFileSync(path.join(root, 'qa-results.json'), JSON.stringify(results, null, 2));
await browser.close();

for (const [s, r] of Object.entries(results.states)) {
  console.log(`\n== ${s}`);
  for (const [w, x] of Object.entries(r.widths)) {
    console.log(`  ${w}px php=${x.phpProblems} scroll=${x.overflow.scrollWidth}/${x.overflow.clientWidth} offenders=${x.overflow.offenders.join(',') || '-'} broken=${x.brokenImages.length} attribution=${JSON.stringify(x.attribution)}`);
  }
  for (const k of ['desktop', 'mobile']) {
    console.log(`  axe ${k}: ` + (r.axe[k].map((v) => `${v.impact}:${v.id}(${v.nodes}) ${v.targets.join(' | ')}`).join('\n    ') || 'no violations'));
  }
}
console.log('\nconsole errors:', results.consoleErrors);
