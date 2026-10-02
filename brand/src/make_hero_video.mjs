// The hero video for Bark & Sky: the five scene plates from make_hero_real.py, a slow two second move on each, recorded as a
// muted 1920 by 1080 WebM that loops. Moves alternate: a drift left with a slight push in, then a drift right.
// python3 brand/src/make_hero_real.py && node brand/src/make_hero_video.mjs
import pkg from '/home/user/Generation-Maine/node_modules/playwright/index.js';
import fs from 'node:fs';
import path from 'node:path';
const { chromium } = pkg;
const root = '/home/user/Generation-Maine';
const media = path.join(root, 'brand', 'identity', 'splash-bark-sky', 'media');
const fd = path.join(root, 'brand', 'content', 'photos', 'hero-frames');
const W = 1920, H = 1080, PER = 2000;
const files = fs.readdirSync(fd).filter(f => /^scene-\d+\.jpg$/.test(f)).sort();
const imgs = files.map(f => 'data:image/jpeg;base64,' + fs.readFileSync(path.join(fd, f)).toString('base64'));
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:${W}px;height:${H}px;overflow:hidden;background:#26201C}
.s{position:absolute;inset:0;opacity:0}.s.on{opacity:1}
.s img{position:absolute;top:0;left:0;display:block;transform-origin:50% 50%;will-change:transform}
</style></head><body>${imgs.map((g, i) => `<div class="s" id="s${i}"><img src="${g}"></div>`).join('')}
<script>
const ss=[...document.querySelectorAll('.s')];let i=0;
function ease(t){return .5-.5*Math.cos(t*Math.PI)}
function run(){ss.forEach((s,k)=>s.classList.toggle('on',k===i));const img=ss[i].querySelector('img');
 const pw=img.naturalWidth,ph=img.naturalHeight,sx=pw-${W},sy=ph-${H};const t0=performance.now();const dir=i%2===0?1:-1;
 function f(now){const t=Math.min(1,(now-t0)/${PER});const e=ease(t);
  // drift across the spare width, settle a little down, push in two percent
  const x=-(sx/2)-dir*(sx/2)*(2*e-1)*0.9, y=-(sy/2)-(sy/2)*(2*e-1)*0.35, z=1+0.02*e;
  img.style.transform='translate('+x+'px,'+y+'px) scale('+z+')';
  if(t<1)requestAnimationFrame(f);else{i=(i+1)%ss.length;run();}}
 requestAnimationFrame(f);}
Promise.all(ss.map(s=>new Promise(r=>{const im=s.querySelector('img');im.complete?r():im.onload=r;}))).then(()=>setTimeout(run,100));
</script></body></html>`;
const dir = '/tmp/claude-0/hero'; fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const ctx = await b.newContext({ viewport: { width: W, height: H }, recordVideo: { dir, size: { width: W, height: H } } });
const p = await ctx.newPage(); await p.setContent(html); await p.waitForTimeout(PER * files.length + 150);
await ctx.close(); await b.close();
const f = fs.readdirSync(dir).find(x => x.endsWith('.webm'));
fs.copyFileSync(path.join(dir, f), path.join(media, 'hero.webm'));
console.log('hero.webm', files.length, 'scenes', Math.round(fs.statSync(path.join(media, 'hero.webm')).size / 1024), 'KB');
