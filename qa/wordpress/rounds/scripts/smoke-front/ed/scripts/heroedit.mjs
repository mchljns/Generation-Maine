// Hero headline editing in the Site Editor (Front Page): type a case, read the canvas while selected, click away (the lede),
// read again, Undo/Redo, then save and read the page. usage: node heroedit.mjs <base> <tag> <v65 0|1> <case,...> [undo]
import { launch, login, save, shot, openTemplate, watch } from './lib.mjs';
const [base, tag, v65s, list, undoFlag] = process.argv.slice(2);
const v65 = v65s === '1';
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 900 });
const log = []; watch(page, log);
const K = page.keyboard;
const T = async (s) => K.type(s, { delay: 5 });
const sp = async (n) => { for (let i = 0; i < n; i++) await K.press('Space'); };
const L1 = async () => { await T('Young Mainers'); await K.press('Shift+Enter'); };
const CASES = {
  trailingSpaces: async () => { await L1(); await T('on staying here'); await sp(7); },
  trailingBreak: async () => { await L1(); await T('on staying here'); await K.press('Shift+Enter'); },
  twoBreaks: async () => { await L1(); await T('on staying here'); await K.press('Shift+Enter'); await K.press('Shift+Enter'); },
  breakSpaces: async () => { await L1(); await T('on staying here'); await K.press('Shift+Enter'); await sp(3); },
  nbspTrail: async () => { await L1(); await T('on staying here'); await K.insertText('   '); },
  periodSpaces: async () => { await L1(); await T('on staying here.'); await sp(5); },
  breakThenWord: async () => { await L1(); await T('on staying here'); await K.press('Shift+Enter'); await T('now'); },
  boldTrail: async () => { await L1(); await T('on staying '); await K.press('Control+b'); await T('here   '); await K.press('Control+b'); },
  quoted: async () => { await L1(); await T('on a place called "home."'); },
  quotedQ: async () => { await L1(); await T('on what we call "home?"'); },
  quotedBang: async () => { await L1(); await T('on a place called "home!"'); },
  single: async () => { await L1(); await T("on a place called 'home.'"); },
  quotedOut: async () => { await L1(); await T('on a place called "home".'); },
  quotedSpaces: async () => { await L1(); await T('on a place called "home."'); await sp(4); },
  ellipsis: async () => { await L1(); await T('on staying here...'); },
  ellipsisChar: async () => { await L1(); await T('on staying here'); await K.insertText('…'); },
  ellipsisQuoted: async () => { await L1(); await T('on staying "here..."'); },
  twoDots: async () => { await L1(); await T('on staying here..'); },
  curlyTyped: async () => { await L1(); await T('on a place called '); await K.insertText('“home.”'); },
  questionQuoteBreak: async () => { await L1(); await T('on "home?"'); await K.press('Shift+Enter'); },
  restore: async () => { await L1(); await T('on building'); await K.press('Shift+Enter'); await T('a life here.'); },
};
const results = {};
await openTemplate(page, base, v65);
const f = await (await page.$('iframe[name="editor-canvas"]')).contentFrame();
const stored = () => page.evaluate(() => { const s = wp.data.select('core/block-editor'); const id = s.getClientIdsWithDescendants().find(id => s.getBlockName(id) === 'core/heading' && / gm-here /.test(' ' + (s.getBlock(id).attributes.className || '') + ' ')); return String(s.getBlock(id).attributes.content); });
const canvas = () => f.evaluate(() => { const h = document.querySelector('h1'); const a = getComputedStyle(h, '::after'); const r = h.getBoundingClientRect(); return { nodot: h.className.includes('gm-nodot'), after: a.content, afterDisplay: a.display, h: Math.round(r.height), text: JSON.stringify(h.innerText) }; });
const dirty = () => page.evaluate(() => wp.data.select('core').__experimentalGetDirtyEntityRecords().map(r => r.name + ':' + (r.key || '')));
const away = async () => { await f.locator('.hero p.lede, .hero .lede').first().click(); await page.waitForTimeout(900); };
for (const c of list.split(',')) {
  const r = {};
  const h1 = f.locator('h1').first();
  await h1.click(); await page.waitForTimeout(400);
  await K.press('Control+a'); await page.waitForTimeout(200); await K.press('Delete'); await page.waitForTimeout(300);
  await CASES[c](); await page.waitForTimeout(700);
  r.selStored = await stored(); r.selCanvas = await canvas();
  await h1.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-${c}-canvas-selected.png` }).catch(() => {});
  await away();
  r.awayStored = await stored(); r.awayCanvas = await canvas(); r.awayDirty = await dirty();
  await h1.screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-${c}-canvas-away.png` }).catch(() => {});
  if (undoFlag) {
    await K.press('Control+z'); await page.waitForTimeout(800); r.undo1 = await stored();
    await K.press('Control+Shift+z'); await page.waitForTimeout(800); r.redo1 = await stored();
    await away(); r.afterRedoAway = await stored();
  }
  await page.locator('.editor-header__settings button, .edit-site-header-edit-mode__actions button', { hasText: /^Save$/ }).first().click();
  await page.waitForTimeout(1200);
  const p2 = page.locator('.entities-saved-states__panel').getByRole('button', { name: /^Save$/ }); if (await p2.count()) await p2.first().click();
  await page.waitForFunction(() => wp.data.select('core').__experimentalGetDirtyEntityRecords().length === 0, null, { timeout: 30000 }).catch(() => { r.saveTimeout = true; });
  await page.waitForTimeout(800);
  r.front = {};
  for (const [w, hh] of [[1440, 900], [390, 844]]) {
    const c2 = await browser.newContext({ viewport: { width: w, height: hh } }); const p = await c2.newPage();
    await p.goto(base + '/', { waitUntil: 'networkidle' }); await p.waitForTimeout(500);
    r.front[w] = await p.evaluate(() => { const h = document.querySelector('h1'); const d = h.querySelector('.d'); const here = h.querySelector('.here'); let gap = null; if (d && here) { const rg = document.createRange(); const tn = [...here.childNodes].filter(n => n.nodeType === 3).pop(); if (tn) { rg.setStart(tn, Math.max(0, tn.length - 1)); rg.setEnd(tn, tn.length); const lr = rg.getBoundingClientRect(); const dr = d.getBoundingClientRect(); gap = { dx: Math.round(dr.left - lr.right), dy: Math.round(dr.top - lr.top), lastChar: JSON.stringify(tn.textContent.slice(-2)) }; } } return { html: h.innerHTML, text: h.innerText, dots: h.querySelectorAll('.d').length, gold: [...h.querySelectorAll('.here')].map(s => s.textContent), gap, overflow: document.documentElement.scrollWidth - innerWidth }; });
    await p.locator('h1').first().screenshot({ path: `/tmp/claude-0/wptest/work/smoke-front/ed/shots/${tag}-${c}-front-${w}.png` }).catch(() => {});
    await c2.close();
  }
  results[c] = r;
  console.log(`=== ${c}\n sel  : ${JSON.stringify(r.selStored)} nodot=${r.selCanvas.nodot} h=${r.selCanvas.h}\n away : ${JSON.stringify(r.awayStored)} nodot=${r.awayCanvas.nodot} h=${r.awayCanvas.h} dirty=${r.awayDirty}`);
  if (undoFlag) console.log(` undo : ${JSON.stringify(r.undo1)}\n redo : ${JSON.stringify(r.redo1)}\n redo+away: ${JSON.stringify(r.afterRedoAway)}`);
  console.log(` front: ${r.front[1440].html.slice(-160)} dots=${r.front[1440].dots} gold=${JSON.stringify(r.front[1440].gold)} gap=${JSON.stringify(r.front[1440].gap)} gap390=${JSON.stringify(r.front[390].gap)} ovf=${r.front[1440].overflow}/${r.front[390].overflow}`);
}
save(`${tag}-heroedit.json`, { results, log });
console.log(log.filter(l => !/CERT/.test(l)).join('\n'));
await browser.close();
