import { B, W } from './lib2.mjs';
// Helpers that drive the WordPress 7.1 block editor for a Creator post the way a person would.
export async function openNewCreator(page) {
  await page.goto(B + '/wp-admin/post-new.php?post_type=gm_creator');
  await page.waitForSelector('#gm_handle', { timeout: 60000, state: 'attached' });
  await page.waitForTimeout(1500);
  const close = page.locator('.components-modal__frame button[aria-label="Close"]');
  if (await close.count()) { await close.first().click(); await page.waitForTimeout(400); }
  // WordPress 6.5 does not iframe the canvas when meta boxes are present
  const canvas = (await page.$('iframe[name="editor-canvas"]')) ? page.frameLocator('iframe[name="editor-canvas"]') : page;
  return canvas;
}
export async function openMetaBoxes(page) {
  if (!(await page.isVisible('#gm_handle'))) {
    const mb = page.locator('button:has-text("Meta Boxes")');
    if (await mb.count()) { await mb.first().click({ position: { x: 30, y: 12 } }).catch(async () => { await mb.first().focus(); await page.keyboard.press('Enter'); }); await page.waitForTimeout(800); }
  }
  if (!(await page.isVisible('#gm_handle'))) {
    const h = page.locator('#gm_creator_details .handlediv');
    if (await h.count()) { await h.first().click(); await page.waitForTimeout(500); }
  }
  return page.isVisible('#gm_handle');
}
export async function fillTitleAndBio(page, canvas, title, bio) {
  // a user who last used the code editor gets it again: use its title box and textarea
  if (await page.isVisible('textarea.editor-post-text-editor')) {
    await page.fill('textarea[placeholder="Add title"]', title);
    if (bio) await page.fill('textarea.editor-post-text-editor', '<!-- wp:paragraph -->\n<p>' + bio + '</p>\n<!-- /wp:paragraph -->');
    return;
  }
  const t = canvas.locator('[aria-label="Add title"]'); await t.click({ timeout: 5000 }).catch(() => t.focus());
  await page.keyboard.type(title);
  if (bio) {
    await page.keyboard.press('Enter');
    await page.waitForTimeout(300);
    await page.keyboard.type(bio);
  }
}
export async function fillMeta(page, fields) {
  for (const [k, v] of Object.entries(fields)) {
    if (k === 'gm_placeholder') { const cb = page.locator('input[name="gm_placeholder"]'); if (v) await cb.check(); else await cb.uncheck(); continue; }
    await page.fill('#' + k, String(v));
  }
}
export async function waitSaved(page) {
  await page.waitForFunction(() => {
    const e = wp.data.select('core/editor'); const ep = wp.data.select('core/edit-post');
    return !e.isSavingPost() && !e.isAutosavingPost() && !(ep.isSavingMetaBoxes && ep.isSavingMetaBoxes());
  }, null, { timeout: 60000 });
  await page.waitForTimeout(1500);
}
export async function saveDraft(page) {
  await page.click('button:has-text("Save draft")');
  await page.waitForTimeout(800); await waitSaved(page);
}
// Submit for Review (contributor) or Publish (author and up), through the pre-publish panel if it shows
export async function submit(page, label) {
  await page.click(`.editor-header__settings button:has-text("${label}"), .edit-post-header__settings button:has-text("${label}")`);
  await page.waitForTimeout(1000);
  const confirm = page.locator(`.editor-post-publish-panel__header-publish-button button, .editor-post-publish-panel button.editor-post-publish-button`);
  if (await confirm.count()) { await confirm.first().click(); }
  await page.waitForTimeout(1000); await waitSaved(page);
}
export async function currentId(page) { return page.evaluate(() => wp.data.select('core/editor').getCurrentPostId()); }
export async function currentStatus(page) { return page.evaluate(() => wp.data.select('core/editor').getEditedPostAttribute('status')); }
