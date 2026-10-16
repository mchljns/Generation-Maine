// Settings > Reading through the UI: node reading.mjs <port> posts | <port> page "<front label or ->" "<posts label or ->"
import { launch, base, login, SHOTS } from './lib.mjs';
const [port, mode, front, posts] = process.argv.slice(2);
const B = base(port);
const b = await launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } }); await login(ctx, B);
const page = await ctx.newPage();
await page.goto(B + '/wp-admin/options-reading.php');
if (mode === 'posts') { await page.check('input[name=show_on_front][value=posts]'); }
else {
  await page.check('input[name=show_on_front][value=page]');
  await page.selectOption('#page_on_front', front === '-' ? { value: '0' } : { label: front });
  await page.selectOption('#page_for_posts', posts === '-' ? { value: '0' } : { label: posts });
}
await Promise.all([page.waitForNavigation(), page.click('#submit')]);
console.log('notice:', (await page.locator('.notice, .error').allInnerTexts()).map(t => t.split('\n')[0]).filter(t => !/available/.test(t)).join(' | '));
await page.screenshot({ path: `${SHOTS}/reading-${port}-${mode}-${(front || '').replace(/\W/g, '')}-${(posts || '').replace(/\W/g, '')}.png`, clip: { x: 0, y: 0, width: 1280, height: 520 } });
await b.close();
