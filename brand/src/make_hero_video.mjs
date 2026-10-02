// A placeholder hero video for Bark & Sky: the nine portrait clips in a slow vertical montage, 4 by 5, muted, cool and quiet.
// Recorded with Playwright the way the story-card clips were. Real footage from the creators replaces media/hero.webm one for one.
// node brand/src/make_hero_video.mjs
import pkg from '/home/user/Generation-Maine/node_modules/playwright/index.js';
import fs from 'node:fs';
import path from 'node:path';
const { chromium } = pkg;
const root = '/home/user/Generation-Maine';
const media = path.join(root, 'brand', 'identity', 'splash-bark-sky', 'media');
const W = 880, H = 1100, PER = 3000, N = 9;
const gifs = Array.from({ length: N }, (_, i) => 'data:image/gif;base64,' + fs.readFileSync(path.join(media, `creator-${i + 1}.gif`)).toString('base64'));
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:${W}px;height:${H}px;overflow:hidden;background:#26201C}
.f{position:absolute;inset:0;opacity:0;transition:opacity .9s ease}
.f img{width:100%;height:100%;object-fit:cover;object-position:center 30%;display:block;filter:saturate(.9) contrast(1.04);transform:scale(1.04);transition:transform ${PER + 900}ms linear}
.f.on{opacity:1}.f.on img{transform:scale(1.12)}
.grade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(185,201,211,.10),rgba(38,32,28,.22));mix-blend-mode:multiply;pointer-events:none}
.tag{position:absolute;right:16px;bottom:16px;font:600 12px/1 ui-monospace,Menlo,monospace;letter-spacing:.06em;color:rgba(244,243,238,.9);background:rgba(38,32,28,.6);padding:7px 9px;border-radius:4px}
</style></head><body>${gifs.map((g, i) => `<div class="f" id="f${i}"><img src="${g}"></div>`).join('')}<div class="grade"></div><div class="tag">PLACEHOLDER</div>
<script>let i=0;const fs=[...document.querySelectorAll('.f')];function step(){fs.forEach((f,k)=>f.classList.toggle('on',k===i));i=(i+1)%fs.length}step();setInterval(step,${PER});</script></body></html>`;
const dir = '/tmp/claude-0/hero';
fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const ctx = await b.newContext({ viewport: { width: W, height: H }, recordVideo: { dir, size: { width: W, height: H } } });
const p = await ctx.newPage(); await p.setContent(html); await p.waitForTimeout(PER * N + 400);
await ctx.close(); await b.close();
const f = fs.readdirSync(dir).find(x => x.endsWith('.webm'));
fs.copyFileSync(path.join(dir, f), path.join(media, 'hero.webm'));
console.log('hero.webm', Math.round(fs.statSync(path.join(media, 'hero.webm')).size / 1024), 'KB');
