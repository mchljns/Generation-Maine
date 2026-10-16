// Styles: the States menu on Paragraph and Button, and the Styles three-dots menu. 7.1 only.
import { launch, login, save, shot, guide } from './lib.mjs';
const [base, tag] = process.argv.slice(2);
const browser = await launch();
const { page } = await login(browser, base, { w: 1440, h: 1000 });
const out = {};
await page.goto(base + '/wp-admin/site-editor.php?p=%2Fstyles', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(6000); await guide(page);
// three dots
const more = page.getByRole('button', { name: /^(More|Options|Styles actions|More Styles actions)$/ });
out.moreButtons = await page.locator('button[aria-label]').evaluateAll(bs => bs.map(b => b.getAttribute('aria-label')).filter(Boolean));
for (let i = 0; i < await more.count(); i++) {
  const b = more.nth(i); if (!(await b.isVisible())) continue;
  await b.click(); await page.waitForTimeout(700);
  out['more' + i] = await page.locator('[role="menuitem"], [role="menuitemcheckbox"], [role="menuitemradio"]').allInnerTexts();
  await shot(page, `${tag}-styles-more${i}`);
  await page.keyboard.press('Escape'); await page.waitForTimeout(300);
}
await page.getByRole('button', { name: /^Blocks$/ }).first().click(); await page.waitForTimeout(1200);
for (const b of ['Paragraph', 'Button']) {
  const s = page.locator('input[type="search"]').first();
  await s.fill(b); await page.waitForTimeout(800);
  await page.getByRole('button', { name: new RegExp('^' + b + '$') }).first().click(); await page.waitForTimeout(1200);
  const st = page.getByRole('button', { name: /States/ }).first();
  if (await st.count()) { await st.click(); await page.waitForTimeout(700); out['states:' + b] = await page.locator('[role="menuitem"], [role="menuitemradio"], [role="menuitemcheckbox"], [role="option"]').allInnerTexts(); await shot(page, `${tag}-styles-states-${b}`); await page.keyboard.press('Escape'); }
  else out['states:' + b] = 'no States button';
  await page.getByRole('button', { name: /^(Back|Navigate to the previous view)$/ }).last().click(); await page.waitForTimeout(700);
}
save(`${tag}-statesmenu.json`, out);
console.log(JSON.stringify(out, null, 1));
await browser.close();
