// Shared helpers for the visitor tests. One browser at a time.
import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs'
import { readFileSync, existsSync, mkdirSync } from 'node:fs'
import { extname } from 'node:path'

export const WP = process.env.WPURL || 'http://127.0.0.1:8951/'
export const V2 = process.env.V2URL || 'http://127.0.0.1:8961/'
export const OUT = '/tmp/claude-0/wptest/work/smoke-front'
const V2DIR = '/home/user/Generation-Maine/brand/identity/splash-lean-a/'
const TYPES = { '.html': 'text/html', '.gif': 'image/gif', '.jpg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml', '.webm': 'video/webm', '.mp4': 'video/mp4' }

export async function launch() {
  return chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--ignore-certificate-errors-spki-list=PS48cX347wDVcRynzq+DFqswl2PLNE1sG6uQvxMCOS0='] })
}

// The v2 page is served from the byte-identical local copy (Chromium here does not trust the egress proxy CA),
// under its real https origin, so relative media paths and the origin match the published page.
export async function routeV2(ctx) {
  if (!process.env.LOCALV2) return // round 2: load the live v2 page
  await ctx.route('https://mchljns.github.io/**', async route => {
    const u = new URL(route.request().url())
    let p = u.pathname.replace(/^\/Generation-Maine\/v2\/?/, '')
    if (!p) p = 'index.html'
    const f = V2DIR + p
    if (existsSync(f)) return route.fulfill({ status: 200, body: readFileSync(f), contentType: TYPES[extname(f)] || 'application/octet-stream' })
    return route.fulfill({ status: 404, body: 'not in local copy' })
  })
}

export async function newCtx(browser, { w = 1440, h = 900, phone = w < 900, reduced = false, js = true, storageState, dsf } = {}) {
  const opts = { viewport: { width: w, height: h }, isMobile: phone, hasTouch: phone, deviceScaleFactor: dsf || (phone ? 2 : 1), javaScriptEnabled: js }
  if (reduced) opts.reducedMotion = 'reduce'
  if (storageState) opts.storageState = storageState
  const ctx = await browser.newContext(opts)
  await routeV2(ctx)
  return ctx
}

export function dir(name) { const d = `${OUT}/${name}`; mkdirSync(d, { recursive: true }); return d }

export function watch(page) {
  const log = { console: [], pageerrors: [], failed: [], bad: [], requests: [] }
  page.on('console', m => { if (['error', 'warning'].includes(m.type())) log.console.push(m.type() + ': ' + m.text()) })
  page.on('pageerror', e => log.pageerrors.push(String(e.message)))
  page.on('requestfailed', r => log.failed.push(r.url() + ' ' + (r.failure() && r.failure().errorText)))
  page.on('response', r => { if (r.status() >= 400) log.bad.push(r.status() + ' ' + r.url()) })
  page.on('request', r => log.requests.push(r.url()))
  return log
}
