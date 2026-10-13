import { chromium } from '/home/user/Generation-Maine/node_modules/playwright/index.mjs';
const url = process.env.URL || 'file:///home/user/Generation-Maine/brand/identity/splash-lean-a/index.html';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
for (const [w, h] of [[320, 568], [360, 740], [375, 667], [390, 844], [430, 932], [844, 390], [768, 1024]]) {
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const reqs = []; p.on('request', r => { if (/media\//.test(r.url())) reqs.push(r.url().split('/').pop()); });
  await p.goto(url); await p.waitForTimeout(900);
  const r = await p.evaluate(() => {
    const q = s => document.querySelector(s), qa = s => [...document.querySelectorAll(s)];
    const R = e => { const b = e.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.width), Math.round(b.height)]; };
    const st = q('#stories'), tr = q('#panels'), panels = qa('.panel'), where = q('#where');
    const soc = panels[0].querySelector('.soc') || document.createElement('div'); const socLinks = [...soc.querySelectorAll('a')];
    const segs = qa('#segs button');
    return {
      docOverflow: document.documentElement.scrollWidth - innerWidth,
      bg: getComputedStyle(st).backgroundColor,
      track: R(tr), trackPad: getComputedStyle(tr).paddingLeft, scrollW: tr.scrollWidth, panel: R(panels[0]), panelLast: R(panels[8]),
      pv: R(panels[0].querySelector('.pv')), h2: R(panels[0].querySelector('h2')), bio: R(panels[0].querySelector('.bio')), bioLines: Math.round(panels[0].querySelector('.bio').getBoundingClientRect().height / parseFloat(getComputedStyle(panels[0].querySelector('.bio')).lineHeight)),
      socRows: new Set(socLinks.map(a => Math.round(a.getBoundingClientRect().top))).size, socLink: socLinks[0] ? R(socLinks[0]) : null, socOverflow: soc.scrollWidth - soc.clientWidth,
      who: R(panels[0].querySelector('.who')), whoText: panels[0].querySelector('.who span').scrollWidth - panels[0].querySelector('.who span').clientWidth, dur: R(panels[0].querySelector('.dur')),
      where: R(where), wn: R(q('#wn')), seg: R(segs[0]), segsBox: R(q('#segs')), next: R(q('#wnext')), nextText: q('#wnext').textContent, whereOverflow: where.scrollWidth - where.clientWidth,
      panelHeights: [...new Set(panels.map(p => Math.round(p.getBoundingClientRect().height)))],
      h2Overflow: panels.map(p => p.querySelector('h2').scrollWidth - p.querySelector('h2').clientWidth).filter(x => x > 0).length,
      headBottom: Math.round(q('.stories-head') ? q('.stories-head').getBoundingClientRect().bottom : -1),
      stageVids: qa('.stage video, .stage img').length, stageVidPreload: qa('.stage video').map(v => v.preload),
      firstClipLoading: panels[0].querySelector('img.clip')?.loading, tabindex: tr.getAttribute('tabindex'),
    };
  });
  // snap test: scroll to each panel using snap and read index + scrollLeft
  const snaps = [];
  for (let i = 0; i < 9; i++) {
    const s = await p.evaluate(i => { const tr = document.getElementById('panels'), pn = document.querySelectorAll('.panel')[i]; pn.scrollIntoView({ inline: 'center', block: 'nearest' }); return 0; }, i);
    await p.waitForTimeout(350);
    snaps.push(await p.evaluate(i => { const tr = document.getElementById('panels'), pn = document.querySelectorAll('.panel')[i].getBoundingClientRect(); return { i, sl: Math.round(tr.scrollLeft), shown: document.querySelector('#wn').textContent.slice(0, 2), on: [...document.querySelectorAll('.panel')].findIndex(p => p.classList.contains('on')), left: Math.round(pn.left), right: Math.round(pn.right - innerWidth), bg: document.getElementById('stories').style.backgroundColor }; }, i));
  }
  // mark click
  await p.evaluate(() => document.querySelectorAll('#segs button')[4].click()); await p.waitForTimeout(700);
  const click = await p.evaluate(() => ({ sl: Math.round(document.getElementById('panels').scrollLeft), wn: document.querySelector('#wn').textContent, p4left: Math.round(document.querySelectorAll('.panel')[4].getBoundingClientRect().left) }));
  console.log(`\n=== ${w}x${h}`); console.log(JSON.stringify(r, null, 0)); console.log('snaps', JSON.stringify(snaps)); console.log('click mark 5 ->', JSON.stringify(click)); console.log('media requested:', reqs.length, reqs.slice(0, 12).join(' '));
  await p.evaluate(() => document.querySelectorAll('.panel')[0].scrollIntoView({ inline: 'center' })); await p.waitForTimeout(300);
  await p.evaluate(() => document.getElementById('stories').scrollIntoView()); await p.waitForTimeout(300);
  await p.screenshot({ path: `${process.env.OUT || '.'}/qa-${w}.png` });
  await p.close();
}
await b.close();
