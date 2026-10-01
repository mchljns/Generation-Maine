/* Generation Maine: the page's motion. One file, no dependencies.
   The hero mural draws the mark; the period pulses like a place; the page scrubs from green to white with the scroll;
   the bar folds into a capsule; the creators step through while pinned; rules and rows arrive as sections enter.
   Everything respects prefers-reduced-motion. Every piece checks for its element so any section can be removed. */
(function () {
	var D = window.GMDATA || { rows: [], towns: [] };
	var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
	var $ = function (s, r) { return (r || document).querySelector(s); };
	var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
	document.documentElement.classList.add('js');

	// Headings marked .gm-dot end in the Marigold period: the last word and the dot stay together on one line.
	$$('.gm-dot').forEach(function (h) {
		if ($('.d', h)) { return; }
		var walker = document.createTreeWalker(h, NodeFilter.SHOW_TEXT), last = null, n;
		while ((n = walker.nextNode())) { if (n.nodeValue.trim()) { last = n; } }
		if (!last) { return; }
		var text = last.nodeValue.replace(/\s+$/, ''), i = text.lastIndexOf(' ');
		var head = i >= 0 ? text.slice(0, i + 1) : '', word = i >= 0 ? text.slice(i + 1) : text;
		var b = document.createElement('b'); b.className = 'nw'; b.textContent = word;
		var d = document.createElement('i'); d.className = 'd' + (h.classList.contains('gm-pulse') ? ' pulse' : ''); b.appendChild(d);
		last.nodeValue = head; last.parentNode.insertBefore(b, last.nextSibling);
	});

	// The hero: headline, lede and buttons rise in.
	var rises = $$('.hero .rise');
	if (!reduced && rises.length) {
		rises.forEach(function (el) { el.classList.add('pre'); });
		requestAnimationFrame(function () { requestAnimationFrame(function () { rises.forEach(function (el, k) { setTimeout(function () { el.classList.remove('pre'); }, k * 120); }); }); });
	}

	// The mural: the logo's sixteen lines at hero scale, drawing in from the top.
	var m = $('#mural');
	if (m && D.rows && D.rows.length) {
		var ns = 'http://www.w3.org/2000/svg', svg = document.createElementNS(ns, 'svg'); svg.setAttribute('viewBox', '0 0 720 720');
		D.rows.forEach(function (row, i) { row.runs.forEach(function (r) { var p = document.createElementNS(ns, 'path'); p.setAttribute('d', 'M' + r[0] + ' ' + row.y + ' L' + r[1] + ' ' + row.y); p.setAttribute('stroke', '#FFFFFF'); p.setAttribute('stroke-width', row.w); p.setAttribute('stroke-linecap', 'round'); p.setAttribute('fill', 'none'); p.setAttribute('pathLength', '1'); p.style.transitionDelay = (i * 45) + 'ms'; svg.appendChild(p); }); });
		m.appendChild(svg);
		new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { m.classList.add('on'); } }); }, { threshold: 0.2 }).observe(m);
	}

	// The page color, worked out on every frame from scroll position: green under the hero, scrubbing to white as the about
	// section rises, then whatever the section at the middle of the screen asks for (data-bg, or a bg-* class).
	var aboutEl = $('.about'), bgs = $$('[data-bg], [class*="bg-"]'), bgNow = '';
	var canMix = window.CSS && CSS.supports && CSS.supports('color', 'color-mix(in oklab, red, blue)');
	function bgOf(el) { if (el.dataset.bg) { return el.dataset.bg; } var mm = /(?:^|\s)bg-([a-z]+)/.exec(el.className); return mm ? 'var(--' + mm[1] + ')' : 'var(--bi)'; }
	function paint() {
		var c = 'var(--bi)', t = 1;
		if (aboutEl) {
			var top = aboutEl.getBoundingClientRect().top, start = top + scrollY, end = innerHeight * 0.6;
			t = Math.min(1, Math.max(0, (start - top) / (start - end)));
			aboutEl.classList.toggle('lit', t >= 0.4);
			document.body.classList.toggle('scrub', t > 0 && aboutEl.getBoundingClientRect().bottom > 0);
		}
		if (t <= 0) { c = 'var(--sp)'; }
		else if (t < 1) { c = canMix ? 'color-mix(in oklab, var(--sp), var(--bi) ' + (t * 100).toFixed(1) + '%)' : (t < 0.4 ? 'var(--sp)' : 'var(--bi)'); }
		else { var mid = innerHeight / 2; bgs.forEach(function (el) { if (el.getBoundingClientRect().top <= mid) { c = bgOf(el); } }); }
		if (c !== bgNow) { bgNow = c; document.body.style.background = c; }
	}

	// The creators: one pinned clip and one set of details that step with the scroll.
	var stage = $('#stage'), stageVids = stage ? $$('video, img.clip', stage) : [], whos = stage ? $$('.who', stage) : [], marks = $$('#segs button'), dur = $('#dur'), wn = $('#wn'), wnext = $('#wnext');
	var panels = $$('.panel'), panelsEl = $('#panels'), storiesEl = $('#stories'), cur = -1;
	function show(i) {
		if (i === cur || !panels[i]) { return; }
		var back = i < cur;
		panels.forEach(function (p, k) { p.classList.toggle('on', k === i); p.classList.toggle('prev', back ? k > i : k < i); });
		cur = i;
		stageVids.forEach(function (v, k) { var on = k === i; v.classList.toggle('on', on); if (!v.play) { return; } if (on) { var pr = v.play(); if (pr && pr.catch) { pr.catch(function () {}); } } else { v.pause(); } });
		whos.forEach(function (w, k) { w.classList.toggle('on', k === i); });
		marks.forEach(function (mk, k) { mk.classList.toggle('on', k === i); mk.classList.toggle('done', k < i); });
		if (dur && stageVids[i]) { dur.textContent = stageVids[i].dataset.dur || ''; dur.hidden = !stageVids[i].dataset.dur; }
		if (wn) { wn.textContent = String(i + 1).replace(/^(\d)$/, '0$1') + ' / ' + String(panels.length).replace(/^(\d)$/, '0$1'); }
		if (wnext) { var nx = marks[i + 1]; wnext.textContent = nx ? (wnext.dataset.next || 'Next: ') + nx.dataset.name : (wnext.dataset.last || 'Last one'); }
	}
	var stageEl = $('.stage');
	function fit() { if (!panelsEl) { return; } if (matchMedia('(min-width: 901px)').matches) { panelsEl.style.height = ''; if (stageEl) { stageEl.style.removeProperty('--stageh'); } return; } var h = 0; panels.forEach(function (p) { h = Math.max(h, p.scrollHeight); }); panelsEl.style.height = (h + 6) + 'px'; if (stageEl) { var top = 16, row = 28 + 12, room = innerHeight - top - (h + 6) - 14 * 2 - row - 12, colw = stageEl.clientWidth || (innerWidth - 32); stageEl.style.setProperty('--stageh', Math.round(Math.max(200, Math.min(innerHeight * 0.66, colw * 16 / 9, room))) + 'px'); } }
	function step() { if (!storiesEl || !panels.length) { return; } var total = storiesEl.offsetHeight - innerHeight; var t = total > 0 ? Math.min(1, Math.max(0, (scrollY - storiesEl.offsetTop) / total)) : 0; show(Math.min(panels.length - 1, Math.floor(t * panels.length))); }
	marks.forEach(function (mk, k) { mk.addEventListener('click', function () { var total = storiesEl.offsetHeight - innerHeight; scrollTo({ top: storiesEl.offsetTop + (k + 0.5) / panels.length * total }); }); });
	if (reduced) { stageVids.forEach(function (v) { if (v.play) { v.controls = true; } }); }
	fit(); step(); if (cur < 0 && panels.length) { show(0); }
	if (document.fonts && document.fonts.ready) { document.fonts.ready.then(function () { fit(); step(); }); }
	addEventListener('load', fit);

	// The bar: folds into the capsule on the first scroll, hides on the way down past the hero, returns on the way up.
	var bar = $('#topbar'), heroEl = $('.hero'), prog = $('#prog'), lastY = scrollY, ticking = false;
	var links = bar ? $$('nav a', bar) : [];
	links.forEach(function (l) { var hsh = (l.getAttribute('href') || '').split('#')[1]; if (hsh) { l.dataset.for = hsh; } });
	var ao = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { links.forEach(function (l) { l.classList.toggle('on', l.dataset.for === e.target.id); }); } }); }, { rootMargin: '-40% 0px -55% 0px', threshold: 0 });
	links.forEach(function (l) { var el = l.dataset.for && document.getElementById(l.dataset.for); if (el) { ao.observe(el); } });
	addEventListener('scroll', function () {
		if (ticking) { return; } ticking = true;
		requestAnimationFrame(function () {
			var y = scrollY, dy = y - lastY;
			if (bar) {
				bar.classList.toggle('scrolled', y > 12);
				var hh = heroEl ? heroEl.offsetHeight : 0;
				if (y > hh && dy > 6) { bar.classList.add('hide'); } else if (dy < -6 || y <= hh) { bar.classList.remove('hide'); }
				var max = document.documentElement.scrollHeight - innerHeight; if (prog) { prog.style.width = (Math.min(1, y / max) * 100).toFixed(1) + '%'; }
			}
			lastY = y; paint(); step(); ticking = false;
		});
	}, { passive: true });
	addEventListener('resize', function () { fit(); step(); paint(); });
	paint();

	// The phone menu: the sheet takes a copy of the bar's links, with the dot after each.
	var sheet = $('#sheet'), menu = $('#menu');
	if (sheet && menu && bar) {
		var sn = $('nav', sheet);
		if (sn && !sn.children.length) { links.forEach(function (l) { var a = document.createElement('a'); a.href = l.getAttribute('href'); a.textContent = l.textContent; var d = document.createElement('i'); d.className = 'd'; a.appendChild(d); sn.appendChild(a); }); }
		var setMenu = function (o) { sheet.classList.toggle('open', o); bar.classList.toggle('open', o); sheet.setAttribute('aria-hidden', String(!o)); menu.setAttribute('aria-expanded', String(o)); document.body.style.overflow = o ? 'hidden' : ''; };
		menu.addEventListener('click', function () { setMenu(!sheet.classList.contains('open')); });
		$$('a', sheet).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
		addEventListener('keydown', function (e) { if (e.key === 'Escape') { setMenu(false); } });
	}

	// Sections: marked before they enter, released as they do. The footer mark draws in and its dot pings.
	var secs = $$('.reveal'); secs.forEach(function (sc) { sc.classList.add('pre'); });
	var so = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.remove('pre'); so.unobserve(e.target); } }); }, { threshold: 0.18 });
	secs.forEach(function (sc) { so.observe(sc); });
	var site = $('.site'); if (site) { new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { site.classList.add('on'); } }); }, { threshold: 0.3 }).observe(site); }

	// The signup form hands off to Substack; the page shows its own line.
	$$('form.gm-newsletter').forEach(function (f) {
		f.addEventListener('submit', function (ev) {
			var em = $('input[type=email]', f), ok = $('.gm-newsletter__ok', f), btn = $('button', f);
			if (em && !em.checkValidity()) { ev.preventDefault(); em.focus(); em.setAttribute('aria-invalid', 'true'); return; }
			if (em) { em.removeAttribute('aria-invalid'); }
			if (ok && f.dataset.confirm) { ok.textContent = f.dataset.confirm; ok.hidden = false; requestAnimationFrame(function () { ok.classList.add('show'); }); }
			if (btn) { btn.disabled = true; }
		});
	});
})();
