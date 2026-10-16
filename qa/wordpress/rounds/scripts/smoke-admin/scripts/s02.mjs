// S02: long footer line, legal line, note and handle through Settings > Generation Maine; measure sideways overflow on the front
import { launch, base, login, SHOTS } from './lib.mjs';
const [port, tag] = process.argv.slice(2); const B = base(port);
const long = 'x'.repeat(300);
const sets = [
  ['email-lede', { gm_footer_line: 'Young Mainers on the rules that shape their lives. Write to generationmaineinformation@mainepolicyinstitute.org' }],
  ['300-lede', { gm_footer_line: long }],
  ['300-handle', { gm_instagram_handle: '@' + long, gm_instagram_url: 'https://www.instagram.com/generationmaine/' }],
  ['email-legal-note', { gm_footer_line: 'Short line.', gm_instagram_handle: '@generationmaine', gm_legal_line: 'Generation Maine, write to generationmaineinformation@mainepolicyinstitute.org', gm_newsletter_note: 'Questions? generationmaineinformation@mainepolicyinstitute.org', gm_newsletter_url: 'https://generationmaine.substack.com/subscribe' }],
  ['300-legal-note', { gm_legal_line: long, gm_newsletter_note: long }],
  ['300-tiktok-from-url', { gm_legal_line: 'Generation Maine.', gm_newsletter_note: 'Runs on Substack.', gm_tiktok_handle: '', gm_tiktok_url: 'https://www.tiktok.com/@' + 'y'.repeat(120) }],
];
const b = await launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 1400 } }); await login(ctx, B);
const p = await ctx.newPage(); const out = [];
for (const [name, vals] of sets) {
  await p.goto(B + '/wp-admin/options-general.php?page=generation_maine');
  for (const [k, v] of Object.entries(vals)) await p.fill('#' + k, v);
  await Promise.all([p.waitForNavigation(), p.click('#submit')]);
  const notice = (await p.locator('.notice, .updated, .error').allInnerTexts()).map(t => t.replace(/\s+/g, ' ').replace(' Dismiss this notice.', '')).filter(t => !/available/.test(t)).join(' | ');
  const row = { name, notice, widths: {} };
  for (const w of [320, 360, 390, 768, 901, 1280, 1440]) {
    const c = await b.newContext({ viewport: { width: w, height: 800 }, isMobile: w < 800, hasTouch: w < 800 }); const v = await c.newPage();
    await v.goto(B + '/?n=' + Date.now()); await v.waitForTimeout(300);
    const m = await v.evaluate(() => {
      const vw = document.documentElement.clientWidth;
      const over = [...document.querySelectorAll('footer *, .follow *, #newsletter *')].filter(e => { const r = e.getBoundingClientRect(); return r.width && (r.right > vw + 1 || r.left < -1); }).slice(0, 4).map(e => e.tagName + '.' + [...e.classList].join('.') + ' ' + Math.round(e.getBoundingClientRect().right));
      return { vw, sw: document.documentElement.scrollWidth, over };
    });
    row.widths[w] = m;
    if ((w === 320 || w === 1280) && /300|email-lede/.test(name)) { const el = name.includes('handle') || name.includes('tiktok') ? '.follow' : 'footer.site'; await v.locator(el).first().scrollIntoViewIfNeeded().catch(() => {}); await v.waitForTimeout(800); await v.screenshot({ path: `${SHOTS}/s02-${tag}-${name}-${w}.png` }); }
    await c.close();
  }
  out.push(row);
}
// restore
await p.goto(B + '/wp-admin/options-general.php?page=generation_maine');
for (const [k, v] of Object.entries({ gm_footer_line: '', gm_legal_line: '', gm_newsletter_note: 'Runs on Substack. Unsubscribe in one click.', gm_instagram_handle: '', gm_tiktok_handle: '', gm_tiktok_url: 'https://www.tiktok.com/@generationmaine' })) await p.fill('#' + k, v);
await Promise.all([p.waitForNavigation(), p.click('#submit')]);
console.log(JSON.stringify({ port, out }, null, 1)); await b.close();
