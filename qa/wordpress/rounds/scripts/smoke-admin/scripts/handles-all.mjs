// SET-N03: handles worked out from channel addresses of every shape. Each round saves the three addresses (handles cleared)
// through Settings > Generation Maine, then reads the follow rows on the front page as a visitor at 1280 and 320.
import { launch, base, login, INST, SHOTS, watch } from './lib.mjs';
const [port, tag] = process.argv.slice(2);
const B = base(port);
const IG0 = ['https://www.instagram.com/generationmaine/', 'https://www.instagram.com/generationmaine/reels/', 'https://www.instagram.com/generationmaine/?hl=en', 'https://www.instagram.com/p/Cx1AbC2dE3f/', 'https://www.instagram.com/reel/Cx1AbC2dE3f/?igsh=abc', 'https://www.instagram.com/stories/generationmaine/3212345678901234567/', 'https://instagram.com/generation.maine_', 'https://www.instagram.com/@generationmaine', 'https://www.instagram.com/explore/tags/maine/', 'https://www.instagram.com/', 'https://www.instagram.com/generationmaine/tagged/', 'https://www.instagram.com/GenerationMaine', 'https://www.instagram.com/accounts/login/?next=/generationmaine/'];
const TT0 = ['https://www.tiktok.com/@generationmaine', 'https://www.tiktok.com/@generationmaine/video/7312345678901234567', 'https://www.tiktok.com/@generationmaine?lang=en', 'https://www.tiktok.com/@generationmaine/', 'https://vm.tiktok.com/ZMabcdef/', 'https://www.tiktok.com/t/ZTabc123/', 'https://www.tiktok.com/generationmaine', 'https://m.tiktok.com/@generation.maine', 'https://www.tiktok.com/@generationmaine/video/7312345678901234567?is_from_webapp=1&sender_device=pc', 'https://www.tiktok.com/', 'https://www.tiktok.com/@generationmaine/photo/7312345678901234567', 'https://www.tiktok.com/%40generationmaine', 'https://www.tiktok.com/@'];
const YT0 = ['https://www.youtube.com/@generationmaine', 'https://www.youtube.com/@generationmaine/videos', 'https://www.youtube.com/@GenerationMaine/featured', 'https://www.youtube.com/@generationmaine/shorts', 'https://www.youtube.com/shorts/abc123XYZ_-', 'https://www.youtube.com/channel/UC1a2B3c4D5e6F7g8H9i0J', 'https://www.youtube.com/c/GenerationMaine', 'https://www.youtube.com/user/GenerationMaine', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'https://youtu.be/dQw4w9WgXcQ', 'https://m.youtube.com/@generationmaine?si=xyz', 'https://www.youtube.com/%40generationmaine', 'https://www.youtube.com/@generationmaine/community?lang=en'];

const IGX = ['https://www.instagram.com/s/aGlnaGxpZ2h0OjE3OTMxMTI0MDY0MDc3MTY5?story_media_id=321&igsh=abc', 'https://www.instagram.com/share/BAabc123/', 'https://www.instagram.com/about/', 'https://www.instagram.com/generationmaine/followers/', 'https://www.instagram.com/_u/generationmaine', 'https://www.instagram.com/generationmaine/p/Cx1AbC2dE3f/', 'https://www.instagram.com/stories/highlights/17912345/', 'https://www.instagram.com/generationmaine/reel/Cx1AbC2dE3f/?igsh=x', 'https://www.instagram.com/maine.4x4/', 'https://instagram.com/generation--maine'];
const TTX = ['https://www.tiktok.com/@gen%20maine', 'https://www.tiktok.com/@generationmaine/live', 'https://vt.tiktok.com/ZSabc123/', 'https://www.tiktok.com/@generation--maine', 'https://www.tiktok.com/@maine.4x4/video/7312345678901234567', 'https://www.tiktok.com/music/original-sound-7312345678901234567', 'https://www.tiktok.com/tag/maine', 'https://www.tiktok.com/discover/maine', 'https://www.tiktok.com/@GenerationMaine?_t=8abc&_r=1', 'https://www.tiktok.com/embed/v2/7312345678901234567'];
const YTX = ['https://www.youtube.com/@generation--maine', 'https://www.youtube.com/live/abcDEF12345', 'https://www.youtube.com/playlist?list=PL1234567890', 'https://www.youtube.com/@4x4maine/streams', 'https://music.youtube.com/channel/UC1a2B3c4D5e6F7g8H9i0J', 'https://youtube.com/@GenerationMaine?feature=shared', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=GenerationMaine', 'https://www.youtube.com/hashtag/maine', 'https://www.youtube.com/@generationmaine/about', 'https://youtube.com/shorts/abc123XYZ_-?si=xyz'];
const IG = IG0.concat(IGX), TT = TT0.concat(TTX), YT = YT0.concat(YTX);
const b = await launch();
const ctx = await b.newContext({ viewport: { width: 1280, height: 1400 } });
await login(ctx, B);
const p = await ctx.newPage(); const errs = []; watch(p, errs);
const vis = await b.newContext({ viewport: { width: 1280, height: 900 } });
const phone = await b.newContext({ viewport: { width: 320, height: 640 }, isMobile: true, hasTouch: true });
const rows = async (c) => { const q = await c.newPage(); await q.goto(B + '/?n=' + Date.now()); const r = await q.evaluate(() => ({ rows: [...document.querySelectorAll('.follow .row')].map(r => ({ tag: r.tagName, h: (r.querySelector('.h') || {}).textContent })), sw: document.documentElement.scrollWidth })); await q.close(); return r; };
const out = [];
for (let i = 0; i < IG.length; i++) {
  await p.goto(B + '/wp-admin/options-general.php?page=generation_maine');
  for (const k of ['instagram', 'tiktok', 'youtube']) await p.fill(`#gm_${k}_handle`, '');
  await p.fill('#gm_instagram_url', IG[i]); await p.fill('#gm_tiktok_url', TT[i]); await p.fill('#gm_youtube_url', YT[i]);
  await Promise.all([p.waitForNavigation(), p.click('#submit')]);
  const notices = (await p.locator('.notice, .error, .updated').allInnerTexts()).map(t => t.replace(/\s+/g, ' ').replace(' Dismiss this notice.', '').trim()).filter(t => t && !/is available/.test(t));
  const stored = [await p.inputValue('#gm_instagram_url'), await p.inputValue('#gm_tiktok_url'), await p.inputValue('#gm_youtube_url')];
  const d = await rows(vis); const m = await rows(phone);
  out.push({ ig: IG[i], tt: TT[i], yt: YT[i], notices, stored, desktop: d.rows.slice(0, 3).map(r => r.tag + ' ' + r.h), phone: m.rows.slice(0, 3).map(r => r.h), phoneScrollWidth: m.sw });
}
console.log(JSON.stringify({ port, out, errors: errs.filter(e => !/CERT/.test(e)) }, null, 1));
await b.close();
