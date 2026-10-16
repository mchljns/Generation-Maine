// Round 3, E01 original steps through the real UI: Site Editor > Front Page > select the Creators block (List View) >
// Layout: Roster, Most creators to show: 6 > Save. Then the front page shows the roster.
import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs'
const base = (process.env.WPURL || 'http://127.0.0.1:8901/').replace(/\/$/, '')
const out = '/tmp/claude-0/wptest/work/r4-front/roster'
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' })
const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } }); const p = await ctx.newPage(); p.setDefaultTimeout(45000)
const log = []; p.on('pageerror', e => log.push('pageerror ' + e.message))
await p.goto(base + '/wp-login.php'); await p.fill('#user_login', 'admin'); await p.fill('#user_pass', 'adminpass'); await p.click('#wp-submit'); await p.waitForURL(/wp-admin/)
await p.goto(base + '/wp-admin/site-editor.php?p=%2Fwp_template%2Fgeneration-maine%2F%2Ffront-page&canvas=edit', { waitUntil: 'domcontentloaded' })
const fh = await p.waitForSelector('iframe[name="editor-canvas"]', { timeout: 90000 }); const f = await fh.contentFrame()
await f.waitForSelector('.is-root-container', { timeout: 90000 }); await p.waitForTimeout(3000)
for (let i = 0; i < 4; i++) { const g = p.getByRole('button', { name: 'Get started' }); if (await g.count()) { await g.first().click().catch(() => {}); await p.waitForTimeout(400); continue } const c = p.locator('.components-modal__frame button[aria-label="Close"]'); if (await c.count()) { await c.first().click().catch(() => {}); await p.waitForTimeout(400); continue } break }
// select the Creators block in the canvas
const blk = f.locator('[data-type="generation-maine/creators"]').first()
await blk.scrollIntoViewIfNeeded(); await blk.click({ position: { x: 20, y: 20 } }); await p.waitForTimeout(800)
if (!(await p.locator('.interface-complementary-area').count())) { await p.locator('.editor-header__settings').getByRole('button', { name: 'Settings', exact: true }).click().catch(() => {}); await p.waitForTimeout(600) }
const tabBlock = p.getByRole('tab', { name: /^(Block|Creators)$/ }); if (await tabBlock.count()) await tabBlock.first().click().catch(() => {})
await p.waitForTimeout(500)
const layout = p.locator('.interface-complementary-area').getByLabel('Layout', { exact: true })
log.push('layout control count ' + await layout.count())
await layout.first().selectOption('roster'); await p.waitForTimeout(800)
const most = p.locator('.interface-complementary-area').getByLabel('Most creators to show')
if (await most.count()) { await most.first().fill('6'); await p.waitForTimeout(500) }
await p.screenshot({ path: `${out}/ui-editor-roster.png` })
await p.locator('.editor-header__settings button', { hasText: /^Save$/ }).first().click(); await p.waitForTimeout(1500)
const panel = p.locator('.entities-saved-states__panel'); if (await panel.count()) await panel.getByRole('button', { name: /^Save$/ }).first().click()
await p.waitForTimeout(4000)
log.push('snack: ' + (await p.locator('.components-snackbar').allInnerTexts().catch(() => [])).join(' | '))
console.log(log.join('\n'))
await b.close()
