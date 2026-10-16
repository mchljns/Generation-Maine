// Handles typed in Settings > Generation Maine that WordPress's typography filter rewrites (follow list on the front page)
import { launch, base, login } from './lib.mjs';
const [port] = process.argv.slice(2); const B = base(port);
const b = await launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 1400 } }); await login(ctx, B); const p = await ctx.newPage();
await p.goto(B + '/wp-admin/options-general.php?page=generation_maine');
await p.fill('#gm_instagram_handle', '@maine.4x4'); await p.fill('#gm_youtube_handle', '@generation--maine'); await p.fill('#gm_tiktok_handle', '@generationmaine');
await Promise.all([p.waitForNavigation(), p.click('#submit')]);
const v = await (await b.newContext()).newPage(); await v.goto(B + '/?n=' + Date.now());
console.log(JSON.stringify({ fields: [await p.inputValue('#gm_instagram_handle'), await p.inputValue('#gm_youtube_handle')], rows: await v.$$eval('.follow .row .h', e => e.map(x => x.textContent)) }));
await b.close();
