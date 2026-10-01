// Placeholder creator clips, recorded from HTML animations in the brand's language. Each clip is a story card:
// the fact at the heart of the story moves (three apartments become one, eleven signatures tally up, a clock runs
// forty minutes), the caption arrives word by word, the town signs off. 9:16, seven seconds, loops cleanly.
// No faces, no stock footage: these stand in until the creators film. Content comes from brand/content/creators-placeholder.json.
//   node brand/src/make_clips.mjs
import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
import fs from 'node:fs'; import path from 'node:path';
const ROOT = '/home/user/Generation-Maine';
const CREATORS = JSON.parse(fs.readFileSync(path.join(ROOT, 'brand/content/creators-placeholder.json'), 'utf8')).creators;
const font = fs.readFileSync(path.join(ROOT, 'brand/fonts/inter-var.woff2')).toString('base64');
const disp = fs.readFileSync(path.join(ROOT, 'generation-maine/assets/fonts/bricolage-grotesque-800.woff2')).toString('base64');
const bug = fs.readFileSync(path.join(ROOT, 'brand/identity/logo-maine/signature/bug.svg'), 'utf8').replace('role="img"', '').replace('<svg ', '<svg style="height:18px;width:auto;display:block" ');
const TONES = { t1: ['#3D6F58', '#FFFFFF'], t2: ['#5F4F44', '#FFFFFF'], t3: ['#104836', '#FFFFFF'], t4: ['#6B5A4E', '#FFFFFF'], t5: ['#0B2B21', '#FFFFFF'], t6: ['#5E6A63', '#FFFFFF'] };
const MG = '#EFB443';

// The moving fact for each story. Each returns markup plus a script that animates it over about five seconds.
const FACTS = {
	'Finding a place': () => ({
		html: '<div class="row">' + '<div class="box"></div>'.repeat(3) + '</div><p class="lbl"><b>3</b> apartments in town<br><span>1</span> I could afford</p>',
		js: "const b=[...document.querySelectorAll('.box')];b.forEach((x,i)=>setTimeout(()=>x.classList.add('on'),500+i*350));setTimeout(()=>{b[0].classList.add('off');b[2].classList.add('off');document.querySelector('.lbl span').classList.add('mg');},2600);",
	}),
	'Starting a shop': () => ({
		html: '<div class="tally">' + '<i></i>'.repeat(11) + '</div><p class="lbl"><b>11</b> signatures<br>one winter</p>',
		js: "[...document.querySelectorAll('.tally i')].forEach((x,i)=>setTimeout(()=>x.classList.add('on'),400+i*260));",
	}),
	'Who stays': () => ({
		html: '<div class="grid">' + '<i></i>'.repeat(20) + '</div><p class="lbl"><b>Half</b> of my class left<br><span>I stayed</span></p>',
		js: "const d=[...document.querySelectorAll('.grid i')];d.forEach((x,i)=>setTimeout(()=>x.classList.add('on'),300+i*60));setTimeout(()=>{d.forEach((x,i)=>{if(i%2)x.classList.add('off');});document.querySelector('.lbl span').classList.add('mg');},2400);",
	}),
	'The commute': () => ({
		html: '<p class="clock" id="clk">6:04</p><p class="lbl"><b>40</b> minutes<br>each way</p>',
		js: "let m=4;const el=document.getElementById('clk');const t=setInterval(()=>{m++;if(m>44){clearInterval(t);el.classList.add('mg');return;}el.textContent='6:'+String(m).padStart(2,'0');},95);",
	}),
	'Coming home': () => ({
		html: '<p class="big">26</p><div class="bars"><div class="bar"><i style="--w:92%"></i><span>rent</span></div><div class="bar"><i style="--w:58%"></i><span>take-home</span></div></div><p class="lbl">the math that<br><span>moved me back</span></p>',
		js: "setTimeout(()=>document.querySelectorAll('.bar i').forEach(x=>x.classList.add('on')),700);setTimeout(()=>document.querySelector('.lbl span').classList.add('mg'),2600);",
	}),
	'Moving out': () => ({
		html: '<div class="stack"><div>first month</div><div>deposit</div><div class="fee">surprise fee</div></div><p class="lbl">my <b>first</b> lease<br><span>and its fine print</span></p>',
		js: "[...document.querySelectorAll('.stack div')].forEach((x,i)=>setTimeout(()=>x.classList.add('on'),600+i*800));setTimeout(()=>document.querySelector('.lbl span').classList.add('mg'),3200);",
	}),
	'Two jobs': () => ({
		html: '<div class="bars tall"><div class="bar"><i style="--w:100%"></i><span>job one: the room</span></div><div class="bar"><i style="--w:100%"></i><span>job two: everything else</span></div></div><p class="lbl"><b>2</b> jobs<br><span>one life</span></p>',
		js: "const b=document.querySelectorAll('.bar i');setTimeout(()=>b[0].classList.add('on'),600);setTimeout(()=>b[1].classList.add('on'),1900);setTimeout(()=>document.querySelector('.lbl span').classList.add('mg'),3200);",
	}),
	'Doing the math': () => ({
		html: '<p class="big" id="sum">$0</p><div class="items"><div>exam fee</div><div>license</div><div>background check</div><div>gas to the test</div></div><p class="lbl">before the <b>first</b> paycheck</p>',
		js: "const el=document.getElementById('sum');const it=[...document.querySelectorAll('.items div')];const steps=[200,420,480,640];let total=0;steps.forEach((s,i)=>setTimeout(()=>{it[i].classList.add('on');const start=total,end=total+s,t0=performance.now();const f=n=>{const p=Math.min(1,(n-t0)/500);el.textContent='$'+Math.round(start+(end-start)*p);if(p<1)requestAnimationFrame(f);};requestAnimationFrame(f);total=end;},500+i*800));setTimeout(()=>el.classList.add('mg'),3900);",
	}),
	'Winter work': () => ({
		html: '<div class="months"><div>Nov</div><div>Dec</div><div>Jan</div><div>Feb</div><div>Mar</div><div class="on2">Apr</div></div><p class="lbl">landscaping stops<br><span>five months of what else</span></p>',
		js: "[...document.querySelectorAll('.months div')].forEach((x,i)=>setTimeout(()=>x.classList.add('on'),500+i*420));setTimeout(()=>document.querySelector('.lbl span').classList.add('mg'),3300);",
	}),
};

function html(c) {
	const [bg, fg] = TONES[c.tone];
	const words = c.caption.split(' ');
	const fact = (FACTS[c.story] || FACTS['Finding a place'])();
	return `<!doctype html><meta charset=utf-8><style>
	@font-face{font-family:Inter;src:url(data:font/woff2;base64,${font}) format('woff2');font-weight:100 900}
	@font-face{font-family:Bric;src:url(data:font/woff2;base64,${disp}) format('woff2');font-weight:800}
	html,body{margin:0;width:540px;height:960px;overflow:hidden;background:${bg};color:${fg};font-family:Inter}
	.fact{position:absolute;left:28px;right:28px;top:150px;height:440px;display:flex;flex-direction:column;justify-content:flex-end;gap:26px}
	.lbl{font:600 22px/1.3 Inter;margin:0;opacity:.92}.lbl b{font:800 40px/1 Bric;letter-spacing:-.02em}.lbl span{transition:color .5s}.mg{color:${MG}!important}
	.row{display:flex;gap:14px}.box{flex:1;height:170px;border:2.5px solid ${fg};border-radius:12px;opacity:0;transform:translateY(16px);transition:opacity .5s,transform .6s cubic-bezier(.2,.7,.2,1),border-color .5s}.box.on{opacity:1;transform:none}.box.off{opacity:.18}
	.tally{display:flex;flex-wrap:wrap;gap:12px 10px;width:380px}.tally i{display:block;width:6px;height:64px;border-radius:3px;background:${fg};opacity:0;transform:scaleY(0);transform-origin:bottom;transition:opacity .25s,transform .35s cubic-bezier(.2,.7,.2,1)}.tally i.on{opacity:1;transform:none}.tally i:nth-child(5n){transform:rotate(-70deg) scaleY(0);width:5px;height:150px;margin-left:-110px;margin-top:-40px}.tally i:nth-child(5n).on{transform:rotate(-70deg)}
	.grid{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;width:330px}.grid i{display:block;aspect-ratio:1;border-radius:50%;background:${fg};opacity:0;transform:scale(.4);transition:opacity .4s,transform .5s cubic-bezier(.3,1.3,.4,1)}.grid i.on{opacity:1;transform:none}.grid i.off{opacity:.15;transition:opacity .9s}
	.clock{font:800 150px/1 Bric;letter-spacing:-.04em;margin:0;font-variant-numeric:tabular-nums;transition:color .5s}
	.big{font:800 170px/1 Bric;letter-spacing:-.04em;margin:0;font-variant-numeric:tabular-nums;transition:color .5s}
	.bars{display:flex;flex-direction:column;gap:18px}.bar{position:relative;height:38px}.bar i{display:block;height:14px;width:var(--w);border-radius:7px;background:${fg};transform:scaleX(0);transform-origin:left;transition:transform 1.1s cubic-bezier(.2,.7,.2,1)}.bar i.on{transform:none}.bar span{position:absolute;left:0;top:22px;font:600 15px/1 Inter;opacity:.85}.tall .bar{height:60px}.tall .bar i{height:24px;border-radius:12px}.tall .bar span{top:34px}
	.stack{display:flex;flex-direction:column-reverse;gap:10px}.stack div{padding:18px 20px;border:2.5px solid ${fg};border-radius:12px;font:600 22px/1 Inter;opacity:0;transform:translateY(20px);transition:opacity .4s,transform .6s cubic-bezier(.2,.7,.2,1)}.stack div.on{opacity:1;transform:none}.stack .fee.on{border-color:${MG};color:${MG}}
	.items{display:flex;flex-direction:column;gap:8px}.items div{font:600 19px/1.3 Inter;opacity:0;transform:translateX(-10px);transition:opacity .35s,transform .45s;padding-left:18px;position:relative}.items div::before{content:"";position:absolute;left:0;top:11px;width:8px;height:2px;background:${fg}}.items div.on{opacity:.9;transform:none}
	.months{display:flex;gap:10px}.months div{flex:1;padding:70px 0 12px;border-top:3px solid ${fg};font:600 17px/1 Inter;text-align:center;opacity:0;transition:opacity .5s}.months div.on{opacity:.4}.months div.on2.on{opacity:1;border-color:${MG};color:${MG}}
	.cap{position:absolute;left:28px;right:28px;bottom:118px;margin:0;font:600 30px/1.22 Inter;letter-spacing:-.01em}
	.cap span{display:inline-block;opacity:0;transform:translateY(10px);transition:opacity .35s,transform .5s cubic-bezier(.2,.7,.2,1);margin-right:.26em}.cap span.on{opacity:1;transform:none}
	.lt{position:absolute;left:28px;bottom:36px;right:28px;display:flex;justify-content:space-between;align-items:flex-end}
	.lt small{font:600 13px/1 Inter;letter-spacing:.1em;text-transform:uppercase;opacity:0;transition:opacity .5s}.lt small.on{opacity:.85}
	.lt small::after{content:"";display:inline-block;width:7px;height:7px;border-radius:50%;background:${MG};margin-left:8px;vertical-align:middle}
	</style>
	<div class=fact>${fact.html}</div>
	<p class=cap id=cap>${words.map(w => `<span>${w}</span>`).join('')}</p>
	<div class=lt><small id=town>${c.town}, Maine</small>${bug}</div>
	<script>
	${fact.js}
	const sp=[...document.querySelectorAll('#cap span')];sp.forEach((s,i)=>setTimeout(()=>s.classList.add('on'),3600+i*110));
	setTimeout(()=>document.getElementById('town').classList.add('on'),5200);
	</script>`;
}

const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
for (let i = 0; i < CREATORS.length; i++) {
	const ctx = await b.newContext({ viewport: { width: 540, height: 960 }, recordVideo: { dir: '/tmp/claude-0/clips', size: { width: 540, height: 960 } } });
	const p = await ctx.newPage(); await p.setContent(html(CREATORS[i])); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(7000);
	const v = p.video(); await ctx.close(); const src = await v.path();
	fs.copyFileSync(src, path.join(ROOT, 'brand/identity/splash/media', `creator-${i + 1}.webm`));
	console.log('clip', i + 1, CREATORS[i].story, Math.round(fs.statSync(src).size / 1024) + 'KB');
}
await b.close();
