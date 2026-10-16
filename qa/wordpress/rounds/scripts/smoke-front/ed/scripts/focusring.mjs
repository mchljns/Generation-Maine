// Keyboard focus ring colors: a text link and a button in a page (navy expected), and links/inputs inside an inserted Follow
// section (navy background; gold expected), and the same section on the front page.
import { launch, save } from './lib.mjs';
const [base, tag, ...paths] = process.argv.slice(2);
const browser = await launch();
const out = {};
for (const path of paths) {
  const p = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto(base + path, { waitUntil: 'networkidle' });
  const rows = [];
  for (let i = 0; i < 40; i++) {
    await p.keyboard.press('Tab');
    const r = await p.evaluate(() => { const a = document.activeElement; if (!a || a === document.body) return null; const c = getComputedStyle(a); let bg = 'none'; for (let e = a; e; e = e.parentElement) { const b = getComputedStyle(e).backgroundColor; if (b && b !== 'rgba(0, 0, 0, 0)') { bg = b; break; } } return { el: a.tagName + '.' + (a.className || '').toString().split(' ')[0] + ' ' + (a.textContent || a.value || a.getAttribute('aria-label') || '').trim().slice(0, 24), inSection: !!a.closest('.follow, .about, .hero'), inMain: !!a.closest('main'), outline: c.outlineStyle + ' ' + c.outlineColor + ' ' + c.outlineWidth, bg }; });
    if (r) rows.push(r);
  }
  out[path] = rows.filter(r => r.inMain);
  await p.close();
}
save(`${tag}-focusring.json`, out);
for (const [k, v] of Object.entries(out)) { console.log('==', k); const seen = new Set(); for (const r of v) { const key = r.el + r.outline; if (seen.has(key)) continue; seen.add(key); console.log(' ', r.inSection ? '[section]' : '[content]', r.el.padEnd(40), r.outline, 'on', r.bg); } }
await browser.close();
