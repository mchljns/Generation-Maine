// Give a seeded sample its own clip (chosen from the Media Library) and its own links, leave Placeholder ticked, Save.
//   GMB=<base> GMI=<instance> node editsample.mjs <creatorId>
import { browser, login, B, wp } from './lib2.mjs';
import { openMetaBoxes, waitSaved } from './editor-lib2.mjs';
const id = +process.argv[2];
const b = await browser(); const ctx = await b.newContext({ viewport: { width: 1400, height: 1000 } }); const page = await login(ctx, 'admin', 'adminpass');
await page.goto(B + `/wp-admin/post.php?post=${id}&action=edit`); await page.waitForSelector('#gm_hometown', { state: 'attached', timeout: 60000 }); await page.waitForTimeout(2000);
for (let i = 0; i < 3; i++) { const c = page.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click(); await page.waitForTimeout(400); } }
await openMetaBoxes(page);
await page.click('#gm_clip_pick'); await page.waitForSelector('.media-modal', { state: 'visible', timeout: 20000 }); await page.waitForTimeout(1500);
await page.locator('.media-modal:visible .media-router button, .media-modal:visible .media-menu-item', { hasText: 'Media Library' }).first().click().catch(() => {});
await page.waitForTimeout(1500); await page.locator('.media-modal:visible .attachment[aria-label="small-a"]').first().click(); await page.waitForTimeout(400);
await page.click('.media-modal .media-button-select'); await page.waitForTimeout(600);
await page.fill('#gm_instagram', 'https://www.instagram.com/real.person/'); await page.fill('#gm_tiktok', 'https://www.tiktok.com/@real.person'); await page.fill('#gm_handle', '@real.person');
await page.click('.editor-header__settings button:has-text("Save"), .edit-post-header__settings button:has-text("Update"), .editor-header__settings button:has-text("Update")'); await page.waitForTimeout(800); await waitSaved(page);
console.log(JSON.stringify({ id, clip: wp(`post meta get ${id} gm_clip_id`), ig: wp(`post meta get ${id} gm_instagram`), handle: wp(`post meta get ${id} gm_handle`), ph: wp(`post meta get ${id} gm_placeholder`), seeded: wp(`post meta get ${id} gm_seeded`) }));
await b.close();
