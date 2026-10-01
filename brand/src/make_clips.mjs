// Placeholder creator clips, recorded from an HTML animation in the brand's language: a field of lines,
// the spoken line arriving as captions, the brand bug in the corner. The creator's avatar and handle sit on top of the clip in the page, so the clip carries no name. 9:16, six seconds, loops cleanly.
import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
import fs from 'node:fs'; import path from 'node:path';
const ROOT = '/home/user/Generation-Maine';
const CARDS = JSON.parse(process.argv[2]);
const font = fs.readFileSync(path.join(ROOT, 'generation-maine/assets/fonts/inter-var.woff2')).toString('base64');
const bug = fs.readFileSync(path.join(ROOT, 'brand/identity/logo-maine/signature/bug.svg'), 'utf8').replace('role="img"', '').replace('<svg ', '<svg style="height:18px;width:auto;display:block" ');
const TONES = { t1: ['#3D6F58', '#F4F0E6'], t2: ['#5F4F44', '#F4F0E6'], t3: ['#104836', '#F4F0E6'], t4: ['#6B5A4E', '#F4F0E6'], t5: ['#0B2B21', '#F4F0E6'], t6: ['#5E6A63', '#F4F0E6'] };
function html(c) {
  const [bg, fg] = TONES[c.tone];
  const words = c.cap.split(' ');
  return `<!doctype html><meta charset="utf-8"><style>
  @font-face{font-family:Inter;font-weight:100 900;src:url(data:font/woff2;base64,${font}) format('woff2')}
  html,body{margin:0;width:540px;height:960px;overflow:hidden;background:${bg};color:${fg};font-family:Inter,sans-serif}
  canvas{position:absolute;inset:0}
  .tag{position:absolute;top:28px;left:28px;font:600 11px/1 Inter;letter-spacing:.08em;text-transform:uppercase;opacity:.75}
  .cap{position:absolute;left:28px;right:28px;bottom:150px;font:600 34px/1.2 Inter;letter-spacing:-.01em}
  .cap span{display:inline-block;opacity:0;transform:translateY(10px);transition:opacity .35s,transform .5s cubic-bezier(.2,.7,.2,1);margin-right:.26em}
  .cap span.on{opacity:1;transform:none}
  .lt{position:absolute;left:28px;bottom:36px;right:28px;display:flex;justify-content:space-between;align-items:flex-end}
  .lt b{display:block;font:600 15px/1.3 Inter}.lt small{display:block;font:400 14px/1.3 Inter;opacity:.8}
  .d{display:inline-block;width:.2em;height:.2em;border-radius:50%;background:#EFB443;margin-left:.08em;vertical-align:baseline}
  </style><canvas id=c width=1080 height=1920 style="width:540px;height:960px"></canvas>
  <p class=cap id=cap>${words.map(w => `<span>${w}</span>`).join('')}</p>
  <div class=lt><div></div>${bug}</div>
  <script>
  const cv=document.getElementById('c'),ctx=cv.getContext('2d');ctx.scale(2,2);
  const L=[];for(let i=0;i<9;i++){const t=i/8;L.push({y:640+t*230,w:1.4+2.2*t,ph:i*1.3});}
  const t0=performance.now();
  function f(now){const T=(now-t0)/1000;ctx.clearRect(0,0,540,960);ctx.strokeStyle='${fg}';ctx.globalAlpha=.22;ctx.lineCap='round';
    for(const l of L){ctx.lineWidth=l.w;ctx.beginPath();for(let x=0;x<=540;x+=6){const y=l.y+3*Math.sin(T*.6+l.ph+x/540*2.4);x?ctx.lineTo(x,y):ctx.moveTo(x,y);}ctx.stroke();}
    ctx.globalAlpha=1;requestAnimationFrame(f);}
  requestAnimationFrame(f);
  const sp=[...document.querySelectorAll('#cap span')];sp.forEach((s,i)=>setTimeout(()=>s.classList.add('on'),600+i*140));
  </script>`;
}
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
for (let i = 0; i < CARDS.length; i++) {
  const ctx = await b.newContext({ viewport: { width: 540, height: 960 }, recordVideo: { dir: '/tmp/claude-0/clips', size: { width: 540, height: 960 } } });
  const p = await ctx.newPage(); await p.setContent(html(CARDS[i])); await p.waitForTimeout(6000);
  const v = p.video(); await ctx.close(); const src = await v.path();
  fs.copyFileSync(src, path.join(ROOT, 'brand/identity/splash/media', `creator-${i + 1}.webm`));
  console.log('clip', i + 1, Math.round(fs.statSync(src).size / 1024) + 'KB');
}
await b.close();
