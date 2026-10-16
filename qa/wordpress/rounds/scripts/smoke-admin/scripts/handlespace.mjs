import { launch, base, login } from './lib.mjs';
const [port] = process.argv.slice(2); const B = base(port);
const b = await launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 1400 } }); await login(ctx, B); const p = await ctx.newPage(); const out = [];
for (const [ig, tt, yt] of [[' @ generationmaine', '@', '@@generationmaine'], ['generation maine', ' @generationmaine ', '＠generationmaine']]) {
  await p.goto(B + '/wp-admin/options-general.php?page=generation_maine');
  await p.fill('#gm_instagram_handle', ig); await p.fill('#gm_tiktok_handle', tt); await p.fill('#gm_youtube_handle', yt);
  await Promise.all([p.waitForNavigation(), p.click('#submit')]);
  const fields = [await p.inputValue('#gm_instagram_handle'), await p.inputValue('#gm_tiktok_handle'), await p.inputValue('#gm_youtube_handle')];
  const v = await (await b.newContext()).newPage(); await v.goto(B + '/?n=' + Date.now());
  out.push({ typed: [ig, tt, yt], stored: fields, rows: await v.$$eval('.follow .row .h', e => e.slice(0, 3).map(x => x.textContent)) });
}
await p.goto(B + '/wp-admin/options-general.php?page=generation_maine'); for (const k of ['instagram', 'tiktok', 'youtube']) await p.fill(`#gm_${k}_handle`, ''); await Promise.all([p.waitForNavigation(), p.click('#submit')]);
console.log(JSON.stringify(out, null, 1)); await b.close();
