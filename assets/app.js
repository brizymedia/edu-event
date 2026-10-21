/* 이벤트와 교육연구소 — 공통 스크립트 (외부 라이브러리 없음) */
(function () {
  'use strict';
  var d = document, de = d.documentElement;
  var FORM_ENDPOINT = 'https://script.google.com/macros/s/AKfycbwvQ4UJRZklRX7bZB6C0s1yZgSvBAMCVccT580L_1BtiVDyh0DIxShCAvN9McZIB0b7FA/exec';   // 큰길브리지 공용 문의 서버 → 대표 메일 + 큰길브리지
  var SMS_TO = '010-9189-5589';
  var COMPANY = '이벤트와 교육연구소';
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || d).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || d).querySelectorAll(s)); };
  de.classList.add('js');

  /* ── 머리글 · 모바일 메뉴 ── */
  var hdr = $('.hdr'), sheet = $('.sheet'), mbtn = $('.mbtn');
  function onScroll() { if (hdr) hdr.classList.toggle('solid', (window.scrollY || 0) > 30); }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  function setMenu(o) {
    if (!sheet) return;
    sheet.classList.toggle('open', o); hdr.classList.toggle('open', o);
    mbtn.setAttribute('aria-expanded', o ? 'true' : 'false');
    d.body.style.overflow = o ? 'hidden' : '';
  }
  if (mbtn) {
    mbtn.addEventListener('click', function () { setMenu(!sheet.classList.contains('open')); });
    $$('a', sheet).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
  }

  /* ── 등장 효과 (IntersectionObserver + 안전장치) ── */
  var rvs = $$('.rv');
  function show(el) { el.classList.add('in'); }
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { show(e.target); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    rvs.forEach(function (el) { io.observe(el); });
    var chk = function () { rvs.forEach(function (el) { if (!el.classList.contains('in')) { var r = el.getBoundingClientRect(); if (r.top < innerHeight * 0.96 && r.bottom > 0) show(el); } }); };
    addEventListener('scroll', chk, { passive: true }); setTimeout(chk, 400); setTimeout(chk, 1500);
    setTimeout(function () { rvs.forEach(function (el) { if (!el.classList.contains('in') && el.getBoundingClientRect().top < innerHeight * 3) show(el); }); }, 6000);
  } else { rvs.forEach(show); }

  /* ── 히어로: 색종이 + 포인터에 따라 사진이 살짝 움직임 ── */
  var hero = $('.hero');
  if (hero && !reduce) {
    var cf = $('.confetti', hero);
    if (cf) {
      var cols = ['#FA8A7A', '#CFE5A3', '#F4A55A', '#A8D8C4', '#FFFFFF', '#F6C2C0'], h = '';
      var n = innerWidth < 700 ? 16 : 30;
      for (var i = 0; i < n; i++) {
        var w = 8 + Math.random() * 12, sq = Math.random() > .55, c = cols[i % cols.length];
        h += '<i style="left:' + (Math.random() * 100).toFixed(1) + '%;width:' + w.toFixed(0) + 'px;height:' + (sq ? w : w * 0.42).toFixed(0) + 'px;background:' + c + ';border-radius:' + (Math.random() > .5 ? '50%' : '3px') + ';animation-duration:' + (9 + Math.random() * 11).toFixed(1) + 's;animation-delay:-' + (Math.random() * 18).toFixed(1) + 's;--dx:' + ((Math.random() - .5) * 160).toFixed(0) + 'px;--rot:' + (Math.round(Math.random() * 900) - 300) + 'deg"></i>';
      }
      cf.innerHTML = h;
    }
    if (matchMedia('(hover:hover) and (min-width:901px)').matches) {
      var imgs = $$('.pane img', hero), tx = 0, ty = 0, cx = 0, cy = 0, run = false;
      hero.addEventListener('pointermove', function (e) {
        var r = hero.getBoundingClientRect(); tx = ((e.clientX - r.left) / r.width - .5); ty = ((e.clientY - r.top) / r.height - .5);
        if (!run) { run = true; requestAnimationFrame(tick); }
      });
      function tick() {
        cx += (tx - cx) * .08; cy += (ty - cy) * .08;
        imgs.forEach(function (im, i) { im.style.transform = 'translate3d(' + (-cx * 26 * (i ? -1 : 1) - cx * 8).toFixed(1) + 'px,' + (-cy * 18).toFixed(1) + 'px,0)'; });
        if (Math.abs(tx - cx) > .001 || Math.abs(ty - cy) > .001) requestAnimationFrame(tick); else run = false;
      }
    }
  }

  /* ── 숫자 올라가기 ── */
  var cnts = $$('[data-n]');
  if (cnts.length) {
    var done = false;
    var go = function () {
      if (done) return; done = true;
      cnts.forEach(function (el) {
        var n = +el.getAttribute('data-n'), sm = el.querySelector('small'), tail = sm ? sm.outerHTML : '', t0 = performance.now();
        (function step(t) { var k = reduce ? 1 : Math.min(1, (t - t0) / 1500); el.innerHTML = Math.round(n * (1 - Math.pow(1 - k, 3))) + tail; if (k < 1) requestAnimationFrame(step); })(t0);
      });
    };
    var box = cnts[0].closest('.stats') || cnts[0];
    if ('IntersectionObserver' in window) { new IntersectionObserver(function (es, o) { if (es[0].isIntersecting) { o.disconnect(); go(); } }, { threshold: .3 }).observe(box); setTimeout(function () { if (box.getBoundingClientRect().top < innerHeight) go(); }, 1200); } else go();
  }

  /* ── 띠 글자 이어붙이기 ── */
  var tr = $('.ticker .tr'); if (tr) tr.innerHTML += tr.innerHTML;

  /* ── 포트폴리오: 필터 + 확대 ── */
  var pf = $('.pf'), figs = [];
  function applyFilter(b) {
    var f = b.getAttribute('data-f'), cnt = 0, emp = $('#pfEmpty');
    $$('.filters button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
    figs = $$('figure', pf);
    figs.forEach(function (fg) { var ok = f === 'all' || (fg.getAttribute('data-c') || '').split(' ').indexOf(f) > -1; fg.hidden = !ok; if (ok) cnt++; });
    if (emp) emp.hidden = cnt > 0;
    history.replaceState(null, '', f === 'all' ? location.pathname : '#' + f);
  }
  function bindFilter(b) { b.addEventListener('click', function () { applyFilter(b); }); }
  if (pf) {
    $$('.filters button').forEach(bindFilter);
    var h0 = (location.hash || '').slice(1), b0 = h0 && $('.filters button[data-f="' + h0 + '"]'); if (b0) applyFilter(b0);
  }
  /* 대표님이 upload.html 로 올린 사진(photos 가지의 photos.json)을 포트폴리오 앞에 붙인다 */
  var UP_LIST = 'https://raw.githubusercontent.com/brizymedia/edu-event/photos/photos/photos.json';
  var UP_IMG = 'https://cdn.jsdelivr.net/gh/brizymedia/edu-event@photos/';
  var UP_CAT = { kinder: '유치원 · 어린이집', school: '초등학교', corp: '기업체 · 기관', local: '지자체 · 축제', church: '교회', edu: '교육' };
  function esc(t) { return String(t == null ? '' : t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  if (pf && location.protocol.indexOf('http') === 0) {
    fetch(UP_LIST + '?t=' + Math.floor(Date.now() / 300000), { cache: 'no-store' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (j) {
      if (!j || !j.photos || !j.photos.length) return;
      var html = '', chips = $('.filters');
      j.photos.filter(function (x) { return x && x.path; }).forEach(function (x) {
        var cat = UP_CAT[x.cat] ? x.cat : 'school', src = UP_IMG + x.path.split('/').map(encodeURIComponent).join('/'), t = x.event || '행사 현장';
        html += '<figure data-c="' + cat + '" data-t="' + esc(t) + '"><div class="im"><img src="' + src + '" alt="' + esc(t) + '" loading="lazy" decoding="async"></div><figcaption><b>' + esc(t) + '</b><span>' + UP_CAT[cat] + (x.place ? ' · ' + esc(x.place) : '') + (x.date ? ' · ' + esc(x.date) : '') + '</span></figcaption></figure>';
        if (chips && !$('button[data-f="' + cat + '"]', chips)) { var b = d.createElement('button'); b.setAttribute('data-f', cat); b.setAttribute('aria-pressed', 'false'); b.textContent = UP_CAT[cat]; chips.appendChild(b); bindFilter(b); }
      });
      pf.insertAdjacentHTML('afterbegin', html); figs = $$('figure', pf);
    }).catch(function () { });
  }
  var lb = $('.lb');
  if (lb) {
    var li = $('img', lb), lp = $('p', lb);
    var openFig = function (fg) { var im = $('img', fg); li.src = im.getAttribute('data-full') || im.src; li.alt = im.alt; lp.textContent = (fg.getAttribute('data-t') || im.alt); lb.classList.add('on'); };
    $$('.gal,.pf').forEach(function (box) {
      box.addEventListener('click', function (e) { var fg = e.target.closest('figure'); if (fg) openFig(fg); });
      box.addEventListener('keydown', function (e) { var fg = e.target.closest && e.target.closest('figure'); if (fg && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); openFig(fg); } });
      $$('figure', box).forEach(function (fg) { fg.tabIndex = 0; });
    });
    lb.addEventListener('click', function () { lb.classList.remove('on'); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape') lb.classList.remove('on'); });
  }

  /* ── 공지: 관리자 페이지(notice-admin.html)로 올린 공지를 정적 목록 앞에 붙인다 ── */
  var NOTICE_URL = 'https://raw.githubusercontent.com/brizymedia/edu-event/photos/photos/notices.json';
  var nls = $$('.notes[data-live]');
  if (nls.length && location.protocol.indexOf('http') === 0) {
    fetch(NOTICE_URL + '?t=' + Math.floor(Date.now() / 120000), { cache: 'no-store' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (j) {
      if (!j || !j.notices || !j.notices.length) return;
      nls.forEach(function (ul) {
        var st = []; try { st = JSON.parse(ul.getAttribute('data-static') || '[]'); } catch (x) { }
        var list = j.notices.concat(st), max = +ul.getAttribute('data-max') || 99, page = ul.getAttribute('data-live') === 'page', h = '';
        list.slice(0, max).forEach(function (n, i) {
          var tag = n.n ? ' <span class="new">NEW</span>' : '';
          if (page) h += '<li id="n' + i + '"><div class="row"><time>' + esc(n.d) + '</time><div><span class="t">' + esc(n.t) + tag + '</span>' + (n.b ? '<span class="d">' + esc(n.b) + '</span>' : '') + '</div></div></li>';
          else h += '<li><a href="notice.html#n' + i + '"><time>' + esc(n.d) + '</time><span class="t">' + esc(n.t) + tag + '</span></a></li>';
        });
        ul.innerHTML = h;
      });
    }).catch(function () { });
  }

  /* ── 문의 폼 ── */
  var form = $('#qform');
  if (form) {
    var qs = new URLSearchParams(location.search), tp = qs.get('type');
    if (tp) { var sel = $('select[name=type]', form); if (sel) { for (var k = 0; k < sel.options.length; k++) if (sel.options[k].text.indexOf(tp) > -1 || sel.options[k].value === tp) { sel.selectedIndex = k; break; } } }
    var ok = $('#qdone');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var fd = new FormData(form), v = {}; fd.forEach(function (val, key) { v[key] = String(val).trim(); });
      if (v.website) return;                                    // 허니팟
      if (!v.name || !v.tel) { alert('성함(기관명)과 연락처를 적어 주세요.'); return; }
      if (!form.agree.checked) { alert('개인정보 수집 · 이용에 동의해 주세요.'); return; }
      var text = [
        '■ 문의 종류: ' + (v.type || '-'), '■ 기관 · 단체: ' + (v.org || '-'), '■ 담당자: ' + v.name, '■ 연락처: ' + v.tel, '■ 이메일: ' + (v.email || '-'),
        '■ 날짜: ' + (v.date || '미정'), '■ 장소: ' + (v.place || '-'), '■ 예상 인원: ' + (v.people || '-'), '', v.memo || ''
      ].join('\n');
      var local = function () {
        try { navigator.clipboard.writeText('[' + COMPANY + ' 문의]\n' + text); } catch (x) { }
        if (/Android|iPhone|iPad/i.test(navigator.userAgent)) location.href = 'sms:' + SMS_TO.replace(/-/g, '') + '?body=' + encodeURIComponent('[' + COMPANY + ' 문의]\n' + text);
        else alert('문의 내용을 복사했습니다. 전화 ' + SMS_TO + ' 또는 카카오톡으로 붙여넣어 보내 주세요.');
      };
      if (!FORM_ENDPOINT) { local(); return; }
      var body = { name: v.name + (v.org ? ' (' + v.org + ')' : ''), phone: v.tel, email: v.email, service: '[' + COMPANY + '] ' + (v.type || '문의'), message: text, page: location.href, at: new Date().toLocaleString('ko-KR', { timeZone: 'Asia/Seoul' }), website: '' };
      var btn = $('button[type=submit]', form); if (btn) btn.disabled = true;
      fetch(FORM_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(body) })
        .then(function (r) { return r.json(); })
        .then(function (j) { if (j && j.ok) { ok.classList.add('on'); form.reset(); ok.scrollIntoView({ behavior: 'smooth', block: 'center' }); } else local(); })
        .catch(local)
        .then(function () { if (btn) btn.disabled = false; });
    });
  }

  /* ── 관리자 모드 입구 (바닥글 맨 끝) ── */
  var ft = $('.ft');
  if (ft && !$('.admin-entry', ft)) {
    var base = (d.currentScript && d.currentScript.src || '').replace(/assets\/app\.js.*$/, '');
    var a = d.createElement('div'); a.className = 'admin-entry'; a.style.cssText = 'text-align:center;padding:14px 0 0;font-size:12px';
    a.innerHTML = '<a href="' + base + 'office.html" rel="nofollow" style="display:inline-flex;gap:5px;align-items:center;opacity:.5;padding:0"><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>관리자 모드</a>';
    ft.querySelector('.wrap').appendChild(a);
  }
})();
