// The hero video for Bark & Sky: the five scene plates from make_hero_real.py, a slow constant drift with a gentle push in or
// pull out on each, dissolving one into the next, drawn on a canvas and encoded in the browser as a muted 1920 by 1080 WebM.
// The loop point is seamless: the file opens on the first setting at rest and closes on it in the same pose. The poster is
// the first frame.
// python3 brand/src/make_hero_real.py && node brand/src/make_hero_video.mjs
import pkg from '/home/user/Generation-Maine/node_modules/playwright/index.js';
import fs from 'node:fs';
import path from 'node:path';
const { chromium } = pkg;
const root = '/home/user/Generation-Maine';
const media = process.env.OUT || path.join(root, 'brand', 'identity', 'splash-bark-sky', 'media');
const fd = path.join(root, 'brand', 'content', 'photos', 'hero-frames');
const W = +process.env.W || 1920, H = +process.env.H || 1080;
const HOLD = +process.env.HOLD || 2600;      // each setting is on screen this long
const XF = +process.env.XF || 900;         // and dissolves into the next over this long, inside the hold
const DRIFT = +process.env.DRIFT || 1;      // scales how far each setting travels and how much it pushes in
const FPS = 30, KBPS = +process.env.KBPS || 2600;
// per setting: drift direction across the spare width and height, and the scale from start to end (push in or pull out)
const MOVES = [
  { dx: 1, dy: -0.2, z0: 1.00, z1: 1.06 },  // Katahdin: drift right, push toward the summit
  { dx: -1, dy: 0.3, z0: 1.08, z1: 1.00 },  // Aroostook: drift left, pull out over the fields
  { dx: 1, dy: 0.2, z0: 1.00, z1: 1.07 },   // Cadillac: drift right, push toward the islands
  { dx: -1, dy: -0.2, z0: 1.06, z1: 1.00 }, // Head Light: drift left, pull out to the sea
  { dx: 1, dy: 0.0, z0: 1.00, z1: 1.06 },   // Old Port: drift right along the waterfront
];
const files = fs.readdirSync(fd).filter(f => /^scene-\d+\.jpg$/.test(f)).sort();
const imgs = files.map(f => 'data:image/jpeg;base64,' + fs.readFileSync(path.join(fd, f)).toString('base64'));
const html = `<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#141110}</style></head>
<body><canvas id="c" width="${W}" height="${H}"></canvas>
${imgs.map((g, i) => `<img id="i${i}" src="${g}" hidden>`).join('')}
<script>
const MV=${JSON.stringify(MOVES)}, HOLD=${HOLD}, XF=${XF}, W=${W}, H=${H}, DRIFT=${DRIFT};
const smooth=t=>t*t*(3-2*t);
const c=document.getElementById('c'), g=c.getContext('2d'); g.imageSmoothingQuality='high';
const im=MV.map((_,i)=>document.getElementById('i'+i)); const N=im.length;
function draw(i,t,alpha){ // t 0..1 through the hold: a near constant drift with the gentlest ease at the ends
  const m=MV[i],pw=im[i].naturalWidth,ph=im[i].naturalHeight,sx=pw-W,sy=ph-H;
  const e=0.15*smooth(t)+0.85*t, z=m.z0+(m.z1-m.z0)*e*DRIFT;
  const x=-(sx/2)-m.dx*(sx/2)*(2*e-1)*0.7*DRIFT, y=-(sy/2)-m.dy*(sy/2)*(2*e-1)*DRIFT;
  g.save(); g.globalAlpha=alpha; g.translate(W/2,H/2); g.scale(z,z); g.translate(-W/2,-H/2); g.drawImage(im[i],x,y); g.restore(); }
function paint(T){ const i=Math.floor(T/HOLD)%N, u=(T-Math.floor(T/HOLD)*HOLD)/HOLD, nxt=(i+1)%N, into=T-Math.floor(T/HOLD)*HOLD-(HOLD-XF);
  g.fillStyle='#141110'; g.fillRect(0,0,W,H); draw(i,u,1); if(into>0) draw(nxt,0,smooth(into/XF)); }
window.go=()=>new Promise(res=>{
  paint(0); window.poster=c.toDataURL('image/jpeg',0.86);
  const stream=c.captureStream(${FPS}); const chunks=[];
  const rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp9',videoBitsPerSecond:${KBPS}*1000});
  rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data)};
  rec.onstop=()=>{const b=new Blob(chunks,{type:'video/webm'});const r=new FileReader();r.onload=()=>res(r.result.split(',')[1]);r.readAsDataURL(b);};
  let t0=null; const total=N*HOLD;
  function frame(now){ if(t0===null){t0=now; rec.start(250);} const T=now-t0;
    if(T>=total){ paint(0); setTimeout(()=>rec.stop(),120); return; }
    paint(T); requestAnimationFrame(frame); }
  requestAnimationFrame(frame); });
</script></body></html>`;
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const p = await b.newPage({ viewport: { width: W, height: H } });
await p.setContent(html);
await p.waitForFunction(() => [...document.images].every(i => i.complete && i.naturalWidth > 0));
const b64 = await p.evaluate(() => window.go());
const poster = await p.evaluate(() => window.poster);
await b.close();
// MediaRecorder leaves the Segment's Duration out, so players read the length as unknown; write it into the Info element.
function withDuration(buf, ms) {
  const vint = (pos) => { let len = 1, mask = 0x80; while (len <= 8 && !(buf[pos] & mask)) { len++; mask >>= 1; } let v = buf[pos] & (mask - 1); for (let i = 1; i < len; i++) v = v * 256 + buf[pos + i]; return { len, v }; };
  const idLen = (pos) => vint(pos).len; // IDs keep their marker bit, only the length matters here
  let pos = 0;
  // EBML header
  let l = idLen(pos); let sz = vint(pos + l); pos += l + sz.len + sz.v;
  // Segment: id, unknown size
  l = idLen(pos); sz = vint(pos + l); pos += l + sz.len;
  // children until Info (0x1549A966)
  for (;;) {
    l = idLen(pos); const id = buf.subarray(pos, pos + l).toString('hex'); sz = vint(pos + l);
    if (id === '1549a966') {
      const infoStart = pos, bodyStart = pos + l + sz.len, bodyEnd = bodyStart + sz.v;
      const dur = Buffer.alloc(11); dur[0] = 0x44; dur[1] = 0x89; dur[2] = 0x88; dur.writeDoubleBE(ms, 3);
      const newSize = sz.v + dur.length;
      const sizeBytes = Buffer.alloc(8); sizeBytes[0] = 0x01; sizeBytes.writeUIntBE(newSize, 2, 6); // 8-byte size vint
      return Buffer.concat([buf.subarray(0, infoStart + l), sizeBytes, buf.subarray(bodyStart, bodyEnd), dur, buf.subarray(bodyEnd)]);
    }
    pos += l + sz.len + sz.v;
    if (pos >= buf.length) throw new Error('no Info element');
  }
}
fs.writeFileSync(path.join(media, 'hero.webm'), withDuration(Buffer.from(b64, 'base64'), HOLD * files.length));
fs.writeFileSync(path.join(media, 'hero-poster.jpg'), Buffer.from(poster.split(',')[1], 'base64'));
console.log('hero.webm', files.length, 'settings,', (HOLD * files.length / 1000).toFixed(1), 's,', Math.round(fs.statSync(path.join(media, 'hero.webm')).size / 1024), 'KB; poster', Math.round(fs.statSync(path.join(media, 'hero-poster.jpg')).size / 1024), 'KB');
