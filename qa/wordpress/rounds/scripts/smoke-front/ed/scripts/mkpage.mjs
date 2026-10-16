// Create a page through the block editor UI: title, a Buttons block typed in with two buttons (slash command, Ctrl+K links),
// then the rest of the markup pasted through the Code editor (Ctrl+Shift+Alt+M), then Publish. Prints the page id and link.
// usage: node mkpage.mjs <base> <tag> <title> [markup-file] [--no-buttons]
import fs from 'fs';
import { launch, login, watch, save, shot } from './lib.mjs';
const [base, tag, title, file] = process.argv.slice(2);
const noButtons = process.argv.includes('--no-buttons');
const log = [];
const browser = await launch();
const { page } = await login(browser, base);
watch(page, log);
await page.goto(base + '/wp-admin/post-new.php?post_type=page', { waitUntil: 'domcontentloaded' });
await page.waitForFunction(() => window.wp && wp.data && wp.data.select('core/editor') && wp.data.select('core/editor').getCurrentPostId(), null, { timeout: 90000 });
await page.waitForTimeout(2500);
for (let i = 0; i < 4; i++) {
  const c = page.locator('.components-modal__frame button[aria-label="Close"], .components-modal__frame button:has-text("Close")');
  if (await c.count()) { await c.first().click().catch(() => {}); await page.waitForTimeout(500); } else break;
}
const ifr = page.frameLocator('iframe[name="editor-canvas"]');
const hasIframe = await page.locator('iframe[name="editor-canvas"]').count();
const root = hasIframe ? ifr : page;
const titleEl = root.locator('.editor-post-title__input, h1.wp-block-post-title').first();
await titleEl.click();
await page.keyboard.type(title);
await page.keyboard.press('Enter');
await page.waitForTimeout(500);
if (!noButtons) {
  await page.keyboard.type('/buttons');
  await page.waitForTimeout(900);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(900);
  await page.keyboard.type('First button');
  await page.keyboard.press('ControlOrMeta+k');
  await page.waitForTimeout(700);
  await page.keyboard.type('https://example.com/one');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(700);
  // second button: Enter at the end of a button's text adds the next button in recent versions; fall back to the appender
  await page.keyboard.press('Escape').catch(() => {});
  let n = await page.evaluate(() => wp.data.select('core/block-editor').getGlobalBlockCount('core/button'));
  const firstBtn = root.locator('.wp-block-button__link').first();
  await firstBtn.click();
  await page.keyboard.press('End');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(700);
  n = await page.evaluate(() => wp.data.select('core/block-editor').getGlobalBlockCount('core/button'));
  if (n < 2) {
    await firstBtn.click();
    await page.waitForTimeout(300);
    const app = root.locator('.wp-block-buttons .block-list-appender button, .wp-block-buttons .block-editor-button-block-appender').first();
    await app.click();
    await page.waitForTimeout(700);
  }
  await page.keyboard.type('Second button');
  await page.keyboard.press('ControlOrMeta+k');
  await page.waitForTimeout(700);
  await page.keyboard.type('https://example.com/two');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(700);
  log.push('buttons: ' + await page.evaluate(() => wp.data.select('core/block-editor').getGlobalBlockCount('core/button')));
}
if (file) {
  const extra = fs.readFileSync(file, 'utf8').replaceAll('__BASE__', base);
  await page.keyboard.press('ControlOrMeta+Shift+Alt+m');
  await page.waitForTimeout(1200);
  const ta = page.locator('textarea.editor-post-text-editor, textarea#post-content-0').first();
  const cur = await ta.inputValue();
  await ta.fill(cur + '\n\n' + extra);
  await page.waitForTimeout(500);
  await page.keyboard.press('ControlOrMeta+Shift+Alt+m');
  await page.waitForTimeout(1500);
  if (await ta.count()) {
    const exit = page.getByRole('button', { name: /Exit code editor/ });
    if (await exit.count()) { await exit.click(); await page.waitForTimeout(1200); }
  }
}
const invalid = await page.evaluate(() => { const s = wp.data.select('core/block-editor'); const out = []; const walk = ids => ids.forEach(id => { const b = s.getBlock(id); if (b.isValid === false) out.push(b.name); walk(s.getBlockOrder(id)); }); walk(s.getBlockOrder('')); return out; });
// publish
await page.locator('.editor-post-publish-button__button, .editor-post-publish-panel__toggle').first().click();
await page.waitForTimeout(1200);
const confirm = page.locator('.editor-post-publish-panel__header-publish-button button, .editor-post-publish-panel__header-publish-button .components-button').first();
if (await confirm.count()) await confirm.click();
await page.waitForFunction(() => { const s = wp.data.select('core/editor'); return !s.isSavingPost() && s.getCurrentPost().status === 'publish'; }, null, { timeout: 60000 });
await page.waitForTimeout(800);
const info = await page.evaluate(() => { const p = wp.data.select('core/editor').getCurrentPost(); return { id: p.id, link: p.link, status: p.status }; });
await shot(page, `${tag}-editor-after-publish`);
save(`${tag}-mkpage.json`, { info, invalid, log });
console.log(JSON.stringify({ info, invalid, log }));
await browser.close();
