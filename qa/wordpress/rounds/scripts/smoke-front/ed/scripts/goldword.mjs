// Hero headline cases typed in the Site Editor (Front Page), saved, then read on the page (1440, 390) and in the canvas.
// usage: node goldword.mjs <base> <tag> <v65 0|1> <case,case,...>
import { launch, login, save, shot, openTemplate, watch } from './lib.mjs';
const [base, tag, v65s, list] = process.argv.slice(2);
const v65 = v65s === '1';
const cases = list.split(',');
const browser = await launch();
const { page, ctx } = await login(browser, base, { w: 1440, h: 900 });
const log = []; watch(page, log);
const K = page.keyboard;
const typeSlow = async (s) => K.type(s, { delay: 5 });
const bold = async (s) => { await K.press('Control+b'); await typeSlow(s); await K.press('Control+b'); };
const link = async (url) => { await K.press('Control+k'); await page.waitForTimeout(700); await typeSlow(url); await K.press('Enter'); await page.waitForTimeout(700); };
const selectBack = async (n) => { for (let i = 0; i < n; i++) await K.press('Shift+ArrowLeft'); };
const spaces = async (n) => { for (let i = 0; i < n; i++) await K.press('Space'); };
const CASES = {
  plain: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('on staying here.'); },
  boldOut: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('on staying '); await bold('here'); await typeSlow('.'); },
  boldIn: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('on staying '); await bold('here.'); },
  linkOut: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('on staying here.'); await K.press('ArrowLeft'); await selectBack(4); await link('#about'); await K.press('End'); },
  linkIn: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('on staying here.'); await selectBack(5); await link('#about'); await K.press('End'); },
  boldInLink: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('on staying here.'); await K.press('ArrowLeft'); await selectBack(4); await K.press('Control+b'); await link('#about'); await K.press('End'); },
  question: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('why do we stay?'); },
  boldQuestion: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('why do we '); await bold('stay?'); },
  bang: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('we stay here!'); },
  questionSpaces: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('why do we stay?'); await spaces(6); },
  trailingSpaces: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('on staying here'); await spaces(7); },
  periodSpaces: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('on staying here.'); await spaces(5); },
  trailingBreak: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('on staying here'); await K.press('Shift+Enter'); },
  periodBreak: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('on staying here.'); await K.press('Shift+Enter'); },
  run400: async () => { await typeSlow('Alpha'); await spaces(400); await typeSlow('Omega here.'); },
  oneWord: async () => { await typeSlow('Here.'); },
  ellipsis: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('on staying here...'); },
  longword: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('on unaffordability.'); },
  url: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('at generationmaine.org.'); },
  nbsp40: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('on staying'); for (let i = 0; i < 40; i++) await K.press('Shift+Space'); await typeSlow('here.'); },
  linkThenBold: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('on staying here.'); await K.press('ArrowLeft'); await selectBack(4); await link('#about'); await K.press('ArrowLeft'); await K.press('ArrowRight'); await K.press('End'); await K.press('ArrowLeft'); await selectBack(4); await K.press('Control+b'); await K.press('End'); },
  quoted: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('on a place called "home."'); },
  quotedQ: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('on what "home" means?'); await K.press('Shift+Enter'); await K.press('Backspace'); },
  restore: async () => { await typeSlow('Young Mainers'); await K.press('Shift+Enter'); await typeSlow('on building'); await K.press('Shift+Enter'); await typeSlow('a life here.'); },
};
const results = {};
await openTemplate(page, base, v65);
const fh = await page.$('iframe[name="editor-canvas"]');
const f = await fh.contentFrame();
for (const c of cases) {
  const r = {};
  // click into the headline, select its text, type the case
  const h1 = f.locator('h1').first();
  await h1.click(); await page.waitForTimeout(400);
  await K.press('Control+a'); await page.waitForTimeout(200);
  await K.press('Delete'); await page.waitForTimeout(300);
  await CASES[c]();
  await page.waitForTimeout(800);
  r.stored = await page.evaluate(() => { const s = wp.data.select('core/block-editor'); const id = s.getClientIdsWithDescendants().find(id => s.getBlockName(id) === 'core/heading' && / gm-here /.test(' ' + (s.getBlock(id).attributes.className || '') + ' ')); const a = s.getBlock(id).attributes; return String(a.content); });
  r.canvas = await f.evaluate(() => { const h = document.querySelector('h1'); const a = getComputedStyle(h, '::after'); return { cls: h.className, after: a.content, afterBg: a.backgroundColor, afterW: a.width, text: h.innerText }; });
  await h1.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-${c}-canvas.png` }).catch(() => {});
  // save
  await page.locator('.editor-header__settings button, .edit-site-header-edit-mode__actions button', { hasText: /^Save$/ }).first().click();
  await page.waitForTimeout(1200);
  const p2 = page.locator('.entities-saved-states__panel').getByRole('button', { name: /^Save$/ }); if (await p2.count()) await p2.first().click();
  await page.waitForFunction(() => wp.data.select('core').__experimentalGetDirtyEntityRecords().length === 0, null, { timeout: 30000 }).catch(() => { r.saveTimeout = true; });
  await page.waitForTimeout(800);
  // page
  r.front = {};
  for (const [w, hh] of [[1440, 900], [390, 844], [320, 568]]) {
    const c2 = await browser.newContext({ viewport: { width: w, height: hh } });
    const p = await c2.newPage();
    await p.goto(base + '/', { waitUntil: 'networkidle' });
    await p.waitForTimeout(600);
    r.front[w] = await p.evaluate(() => { const h = document.querySelector('h1'); if (!h) return { missing: true }; return { overflow: document.documentElement.scrollWidth - innerWidth, h1right: Math.round(h.getBoundingClientRect().right), html: h.innerHTML, text: h.innerText, gold: [...h.querySelectorAll('.here')].map(s => [s.textContent, getComputedStyle(s).color]), dots: h.querySelectorAll('.d').length, height: Math.round(h.getBoundingClientRect().height) }; });
    await p.locator('h1').first().screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-${c}-front-${w}.png` }).catch(() => {});
    await c2.close();
  }
  results[c] = r;
  console.log('=== ' + c);
  console.log(' stored :', JSON.stringify(r.stored).slice(0, 300));
  console.log(' canvas :', r.canvas.cls.includes('gm-nodot') ? 'gm-nodot' : '', 'after=', r.canvas.after, r.canvas.afterBg);
  console.log(' front  :', JSON.stringify(r.front[1440].html || r.front[1440]).slice(0, 400));
  console.log(' overflow 1440/390/320:', r.front[1440].overflow, r.front[390].overflow, r.front[320].overflow);
  console.log(' gold   :', JSON.stringify(r.front[1440].gold), 'dots', r.front[1440].dots, '| 390 gold', JSON.stringify(r.front[390].gold), 'dots', r.front[390].dots);
}
save(`${tag}-goldword.json`, { results, log });
console.log(log.filter(l => !/CERT/.test(l)).join('\n'));
await browser.close();
