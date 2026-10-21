/**
 * 이벤트와 교육연구소 블로그 — _blog/posts/*.json 을 홈페이지 글(/blog/)로 만든다
 * ──────────────────────────────────────────────────────────────────────────
 *   blog/index.html          글 목록 (최신순)
 *   blog/<분야>/             분야별 모음 (blog/event/ 행사, blog/edu/ 교육)
 *   blog/<글주소>/           글 하나
 *   rss.xml                  블로그 RSS
 *   sitemap.xml · llms.txt   블로그 부분을 이어서 갱신한다 (먼저 python tools/build_site.py 를 돌려 두면 일관된다)
 *
 * 사이트 공통 값(주소 BASE · noindex 여부 · 머리글 · 바닥글 · 상담 띠)은 tools/blog_shell.py 가
 * tools/build_site.py 에서 읽어 온다 — 여기에 도메인이나 전화번호를 적지 않는다.
 * 링크는 전부 상대 주소(../../)라서 로컬 미리보기 · GitHub Pages 하위 경로 · 나중의 자체 도메인 어디서나 맞는다.
 * blog/ 는 매번 지우고 새로 만든다 — 결과 HTML 을 손으로 고치지 말고 원본 JSON 이나 이 템플릿을 고친다.
 * (HD기획 scripts/build-blog.mjs 를 이 사이트의 디자인 · 주제 글 중심 구조에 맞게 옮긴 것)
 *
 * 실행:  python tools/build_site.py && node scripts/build-blog.mjs      규칙: _blog/GUIDE.md   검사: node scripts/blog-check.mjs
 */
import { readFileSync, readdirSync, writeFileSync, mkdirSync, rmSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

export const 분야표 = { event: '행사', edu: '교육' };
export const 예약주소 = new Set(['event', 'edu', 'page']);

export const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
export const 글자만 = (글) => String(글 ?? '').replace(/\*\*(.+?)\*\*/g, '$1').replace(/\[([^\]]+)\]\([^)]*\)/g, '$1');
export const 날짜글 = (d) => { const m = String(d || '').match(/^(\d{4})-(\d{2})-(\d{2})$/); return m ? `${m[1]}년 ${+m[2]}월 ${+m[3]}일` : String(d || ''); };
export const 글주소 = (slug) => `/blog/${encodeURIComponent(slug)}/`;

/** 사이트 공통 값 — python tools/blog_shell.py (build_site.py 의 BASE · header() · footer() 그대로) */
export function 사이트읽기(ROOT) {
  const out = execFileSync('python', [resolve(ROOT, 'tools', 'blog_shell.py')], { cwd: ROOT, encoding: 'buffer', maxBuffer: 1 << 26 });
  return JSON.parse(out.toString('utf8'));
}

/** 글 안에서는 **굵게** 와 [글자](주소) 만 쓴다. 주소는 / 로 시작하거나 https:// 여야 한다. R 은 이 쪽에서 사이트 루트까지의 상대 경로 */
export function 인라인(글, R = '/') {
  return esc(글)
    .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
    .replace(/\[([^\]]+)\]\(((?:\/|https:\/\/)[^)\s]*)\)/g, (m, t, u) =>
      u.startsWith('/') ? `<a href="${R}${u.slice(1)}">${t}</a>` : `<a href="${u}" target="_blank" rel="noopener">${t}</a>`);
}

/** photos.json 의 묶음을 사진 한 장씩 풀어 경로 → 정보 로 */
export function 사진목록(ROOT) {
  const j = JSON.parse(readFileSync(resolve(ROOT, '_blog', 'photos.json'), 'utf8'));
  const 표 = new Map();
  j.묶음.forEach((g, i) => { (g.path || []).forEach((p) => 표.set(p, { ...g, path: p, 묶음번호: i })); });
  return 표;
}

export function 글읽기(ROOT) {
  const 폴더 = resolve(ROOT, '_blog', 'posts');
  if (!existsSync(폴더)) return [];
  return readdirSync(폴더).filter((f) => f.endsWith('.json')).map((f) => {
    const p = JSON.parse(readFileSync(resolve(폴더, f), 'utf8'));
    Object.defineProperty(p, '_파일', { value: f, enumerable: false });
    return p;
  }).sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : a.slug < b.slug ? -1 : 1));
}

/** 본문 글자 — 읽는 시간 · 검사 · 중복 비교에 쓴다 */
export function 본문글(p) {
  const 조각 = [p.lead, ...(p.points || [])];
  for (const s of p.sections || []) {
    조각.push(s.h2);
    for (const b of s.blocks || []) {
      if (b.p) 조각.push(b.p);
      if (b.tip) 조각.push(b.tip);
      if (b.ul) 조각.push(...b.ul);
      if (b.ol) 조각.push(...b.ol);
      if (b.table) 조각.push(...(b.table.head || []), ...(b.table.rows || []).flat());
    }
  }
  for (const f of p.faq || []) 조각.push(f.q, f.a);
  return 조각.map(글자만).join('\n');
}

export function 글이미지들(p) {
  const 목록 = p.cover ? [p.cover] : [];
  for (const s of p.sections || []) for (const b of s.blocks || []) if (b.img) 목록.push(b.img);
  return 목록;
}

export function buildBlog({ ROOT }) {
  const S = 사이트읽기(ROOT);
  const SITE = S.base;
  const posts = 글읽기(ROOT);
  const 절대 = (path) => SITE + String(path).split('/').map((x, i) => (i ? encodeURIComponent(x) : x)).join('/');   // og · JSON-LD 용 절대 주소
  const 제이슨 = (o) => `<script type="application/ld+json">${JSON.stringify(o).replace(/</g, '\\u003c')}</script>`;
  const 바꿈 = (html, R) => html.split('@@R@@').join(R);

  rmSync(resolve(ROOT, 'blog'), { recursive: true, force: true });
  const 쓰기 = (폴더, html) => { const d = resolve(ROOT, 폴더); mkdirSync(d, { recursive: true }); writeFileSync(resolve(d, 'index.html'), html, 'utf8'); };

  /** 쪽 하나 — 깊이(R)에 맞춰 머리글 · 바닥글 · 링크를 맞춘다 */
  const 쪽 = ({ 제목, 설명, 경로, 깊이, 이미지, 종류 = 'website', 더넣기 = '', 색인 = true, 본문 }) => {
    const R = '../'.repeat(깊이);
    const 색인끄기 = S.noindex || !색인;
    const html = `<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>${esc(제목)}</title>
<meta name="description" content="${esc(설명)}">
${색인끄기 ? '<meta name="robots" content="noindex,nofollow">' : ''}
<meta name="theme-color" content="#FFF9F1">
<link rel="canonical" href="${SITE}${경로}">
<link rel="icon" type="image/png" href="@@R@@assets/img/favicon.png">
<link rel="alternate" type="application/rss+xml" title="${esc(S.name)} 블로그" href="@@R@@rss.xml">
<meta property="og:type" content="${종류}"><meta property="og:locale" content="ko_KR"><meta property="og:site_name" content="${esc(S.name)}">
<meta property="og:title" content="${esc(제목)}"><meta property="og:description" content="${esc(설명)}"><meta property="og:url" content="${SITE}${경로}"><meta property="og:image" content="${esc(이미지)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="@@R@@assets/style.css?v=${S.ver}">
<link rel="stylesheet" href="@@R@@assets/blog.css?v=${S.ver}">
${더넣기}
</head>
<body>
${S.header}
<main id="main">
${본문}
</main>
${S.footer}
</body>
</html>
`;
    return 바꿈(html, R);
  };

  const 썸네일 = (p, R) => p.cover
    ? `<img src="${R}${p.cover.path.slice(1)}" alt="${esc(p.cover.alt)}" loading="lazy" decoding="async" width="800" height="450">`
    : `<div class="bl-ph" aria-hidden="true"><span>${esc(분야표[p.category] || '')}</span></div>`;
  const 카드 = (p, R) => `<a class="bl-card" href="${R}blog/${encodeURIComponent(p.slug)}/">
      ${썸네일(p, R)}
      <div class="in"><div class="r">${esc(분야표[p.category] || '')} · ${esc(날짜글(p.date))}</div><div class="t">${esc(p.title)}</div><div class="s">${esc(p.description)}</div></div>
    </a>`;

  const 개수 = new Map(); posts.forEach((p) => 개수.set(p.category, (개수.get(p.category) || 0) + 1));
  const 칩 = (현재, R) => `<nav class="bl-chips" aria-label="분야별 글">
    <a href="${R}blog/index.html"${현재 === '' ? ' aria-current="page"' : ''}>전체<small>${posts.length}</small></a>
    ${Object.entries(분야표).filter(([k]) => 개수.get(k)).map(([k, v]) => `<a href="${R}blog/${k}/index.html"${현재 === k ? ' aria-current="page"' : ''}>${v}<small>${개수.get(k)}</small></a>`).join('\n    ')}
  </nav>`;

  const 이미지html = (im, 표지, R) => `<figure class="bl-fig${표지 ? ' cover' : ''}">
    <img src="${R}${im.path.slice(1)}" alt="${esc(im.alt)}" ${표지 ? 'fetchpriority="high"' : 'loading="lazy"'} decoding="async" width="1100" height="620">
    <figcaption>${인라인(im.caption, R)}</figcaption>
  </figure>`;
  const 블록 = (b, R) => {
    if (b.p) return `<p>${인라인(b.p, R)}</p>`;
    if (b.tip) return `<div class="bl-tip">${인라인(b.tip, R)}</div>`;
    if (b.ul) return `<ul>${b.ul.map((x) => `<li>${인라인(x, R)}</li>`).join('')}</ul>`;
    if (b.ol) return `<ol>${b.ol.map((x) => `<li>${인라인(x, R)}</li>`).join('')}</ol>`;
    if (b.table) return `<div class="bl-tbl"><table><thead><tr>${b.table.head.map((h) => `<th scope="col">${인라인(h, R)}</th>`).join('')}</tr></thead><tbody>${
      b.table.rows.map((row) => `<tr>${row.map((c) => `<td>${인라인(c, R)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
    if (b.img) return 이미지html(b.img, false, R);
    return '';
  };

  /* ── 글 페이지 ── */
  for (const p of posts) {
    const R = '../../';
    const 경로 = 글주소(p.slug);
    const 분 = Math.max(1, Math.round(본문글(p).length / 500));
    const 관련 = [...posts.filter((o) => o !== p && o.category === p.category), ...posts.filter((o) => o !== p && o.category !== p.category)].slice(0, 3);
    const 사진들 = 글이미지들(p);
    const ld = { '@context': 'https://schema.org', '@graph': [
      { '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: '홈', item: SITE + '/' },
        { '@type': 'ListItem', position: 2, name: '블로그', item: SITE + '/blog/' },
        { '@type': 'ListItem', position: 3, name: p.title, item: SITE + 경로 } ] },
      { '@type': 'BlogPosting', '@id': SITE + 경로, headline: p.title, description: p.description,
        ...(사진들.length ? { image: 사진들.map((im) => 절대(im.path)) } : { image: S.ogImage }),
        datePublished: p.date, dateModified: p.updated || p.date, inLanguage: 'ko',
        keywords: [p.keyword.main, ...(p.keyword.sub || [])].join(', '),
        author: { '@type': 'Organization', name: S.name, url: SITE + '/' },
        publisher: { '@id': SITE + '/#business' },
        mainEntityOfPage: { '@type': 'WebPage', '@id': SITE + 경로 } },
      ...((p.faq || []).length ? [{ '@type': 'FAQPage', '@id': SITE + 경로 + '#faq',
        mainEntity: p.faq.map((f) => ({ '@type': 'Question', name: f.q, acceptedAnswer: { '@type': 'Answer', text: 글자만(f.a) } })) }] : []),
    ] };
    const 본문 = `<section class="phead bl-head"><div class="wrap">
  <p class="crumb"><a href="@@R@@index.html">홈</a> › <a href="@@R@@blog/index.html">블로그</a> › <a href="@@R@@blog/${p.category}/index.html">${esc(분야표[p.category])}</a></p>
  <span class="eb"><i></i>${esc(분야표[p.category])} · ${esc(날짜글(p.date))}</span>
  <h1>${esc(p.title)}</h1>
  <p class="bl-meta">읽는 시간 약 ${분}분 · ${esc(S.name)}</p>
</div></section>
<article class="sec bl-sec"><div class="wrap bl-art">
  <p class="bl-lead">${인라인(p.lead, '@@R@@')}</p>
  ${p.cover ? 이미지html(p.cover, true, '@@R@@') : ''}
  <div class="bl-points"><b>이 글의 요점</b><ul>${p.points.map((x) => `<li>${인라인(x, '@@R@@')}</li>`).join('')}</ul></div>
  <nav class="bl-toc" aria-label="목차"><b>목차</b><ol>${p.sections.map((s, i) => `<li><a href="#s${i + 1}">${esc(s.h2)}</a></li>`).join('')}</ol></nav>
  <div class="bl-body">
${p.sections.map((s, i) => `<h2 id="s${i + 1}">${esc(s.h2)}</h2>\n${s.blocks.map((b) => 블록(b, '@@R@@')).join('\n')}`).join('\n')}
  </div>
  ${(p.faq || []).length ? `<section class="bl-faq" id="faq"><h2>자주 묻는 질문</h2>${p.faq.map((f) => `<details><summary>${esc(f.q)}</summary><p>${인라인(f.a, '@@R@@')}</p></details>`).join('')}</section>` : ''}
  ${(p.sources || []).length ? `<div class="bl-src"><b>확인한 자료</b> (${esc(날짜글(p.updated || p.date))} 기준)<ul>${p.sources.map((s) => `<li><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.name)}</a></li>`).join('')}</ul></div>` : ''}
</div></article>
${관련.length ? `<section class="sec bl-more"><div class="wrap"><h2>같이 보면 좋은 글</h2><div class="bl-cards">${관련.map((o) => 카드(o, '@@R@@')).join('\n')}</div></div></section>` : ''}
${S.cta}`;
    쓰기(`blog/${p.slug}`, 쪽({ 제목: `${p.title} | ${S.name}`, 설명: p.description, 경로, 깊이: 2, 이미지: p.cover ? 절대(p.cover.path) : S.ogImage, 종류: 'article',
      더넣기: `<meta property="article:published_time" content="${p.date}">\n${제이슨(ld)}`, 본문 }));
  }

  /* ── 목록 · 분야 모음 ── */
  const 목록쪽 = ({ 폴더, 경로, 깊이, 현재, 제목, 설명, eb, h1, 리드, 글들 }) => {
    const R = '@@R@@';
    const ld = { '@context': 'https://schema.org', '@graph': [
      { '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: '홈', item: SITE + '/' },
        { '@type': 'ListItem', position: 2, name: '블로그', item: SITE + '/blog/' },
        ...(현재 ? [{ '@type': 'ListItem', position: 3, name: h1, item: SITE + 경로 }] : []) ] },
      { '@type': 'Blog', '@id': SITE + 경로, name: h1, inLanguage: 'ko', publisher: { '@id': SITE + '/#business' },
        blogPost: 글들.map((p) => ({ '@type': 'BlogPosting', headline: p.title, url: SITE + 글주소(p.slug), datePublished: p.date })) } ] };
    const 본문 = `<section class="phead bl-head"><div class="wrap">
  <p class="crumb"><a href="${R}index.html">홈</a> › ${현재 ? `<a href="${R}blog/index.html">블로그</a> › ${esc(분야표[현재])}` : '블로그'}</p>
  <span class="eb"><i></i>${esc(eb)}</span>
  <h1>${esc(h1)}</h1>
  <p class="lead">${esc(리드)}</p>
</div></section>
<section class="sec bl-sec"><div class="wrap">
  ${칩(현재, R)}
  ${글들.length ? `<div class="bl-cards">${글들.map((p) => 카드(p, R)).join('\n')}</div>` : '<div class="bl-empty">첫 글을 준비하고 있습니다.</div>'}
</div></section>
${S.cta}`;
    쓰기(폴더, 쪽({ 제목, 설명, 경로, 깊이, 이미지: 글들[0]?.cover ? 절대(글들[0].cover.path) : S.ogImage, 색인: 글들.length > 0, 더넣기: 제이슨(ld), 본문 }));
  };
  목록쪽({ 폴더: 'blog', 경로: '/blog/', 깊이: 1, 현재: '', 제목: `블로그 — 행사 준비 체크리스트와 교육 이야기 | ${S.name}`,
    설명: '운동회 · 체험부스 · 매직쇼 · 체육대회 같은 행사 준비 체크리스트와 감정교육 · 리더십 · 발표 · 진로 교육 이야기를 담당자가 저장해 두고 볼 수 있게 정리합니다.',
    eb: 'BLOG', h1: '행사 준비 체크리스트, 교육 이야기', 리드: '행사를 맡은 담당자와 교육을 고민하는 선생님이 저장해 두고 볼 수 있게, 확인할 것을 순서대로 정리합니다.', 글들: posts });
  const 허브글 = [];
  for (const k of Object.keys(분야표)) {
    const 글들 = posts.filter((p) => p.category === k);
    if (!글들.length) continue;
    const 행사 = k === 'event';
    목록쪽({ 폴더: `blog/${k}`, 경로: `/blog/${k}/`, 깊이: 2, 현재: k, 제목: `${행사 ? '행사 준비 체크리스트' : '교육 프로그램 이야기'} — 블로그 | ${S.name}`,
      설명: 행사 ? '운동회 · 체험부스 · 에어바운스 · 매직쇼 · 체육대회 등 행사 준비 체크리스트 모음.' : '감정교육 · 임원 리더십 · 발표회 · 과학실험 마술수업 · 진로탐색 교육을 도입하기 전에 확인할 것 모음.',
      eb: 분야표[k], h1: 행사 ? '행사 준비 체크리스트' : '교육 프로그램 이야기', 리드: 행사 ? '운동회부터 체육대회까지, 행사 날 당황하지 않도록 미리 확인할 것을 정리했습니다.' : '교육을 도입하기 전에 구성과 확인할 것을 정리했습니다.', 글들 });
    허브글.push({ loc: `/blog/${k}/`, lastmod: 글들[0].updated || 글들[0].date });
  }

  /* ── sitemap.xml — 기존 항목은 두고 /blog/ 부분만 바꾼다 ── */
  const 블로그주소 = posts.length ? [{ loc: '/blog/', lastmod: posts[0].updated || posts[0].date }, ...허브글, ...posts.map((p) => ({ loc: 글주소(p.slug), lastmod: p.updated || p.date }))] : [];
  const sm = resolve(ROOT, 'sitemap.xml');
  if (existsSync(sm)) {
    let xml = readFileSync(sm, 'utf8');
    xml = xml.replace(/<url><loc>[^<]*\/blog\/[^<]*<\/loc>[^]*?<\/url>\s*/g, '');
    xml = xml.replace(/<\/urlset>\s*$/, 블로그주소.map((u) => `<url><loc>${SITE}${u.loc}</loc><lastmod>${u.lastmod}</lastmod></url>\n`).join('') + '</urlset>\n');
    writeFileSync(sm, xml, 'utf8');
  }

  /* ── llms.txt — 「## 블로그」 절을 다시 쓴다 ── */
  const ll = resolve(ROOT, 'llms.txt');
  if (existsSync(ll) && posts.length) {
    let t = readFileSync(ll, 'utf8').replace(/\r\n/g, '\n');
    const 절 = `## 블로그 (행사 준비 체크리스트 · 교육 이야기)\n- [블로그 목록](${SITE}/blog/)\n` + posts.map((p) => `- [${p.title}](${SITE}${글주소(p.slug)}): ${p.description}`).join('\n') + '\n';
    t = /^## 블로그[^]*?(?=^## |(?![^]))/m.test(t) ? t.replace(/^## 블로그[^]*?(?=^## |(?![^]))/m, 절) : t.trimEnd() + '\n\n' + 절;
    writeFileSync(ll, t, 'utf8');
  }

  /* ── rss.xml ── */
  const rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
<title>${esc(S.name)} 블로그</title><link>${SITE}/blog/</link><description>행사 준비 체크리스트와 교육 이야기</description><language>ko</language>
${posts.slice(0, 50).map((p) => `<item><title>${esc(p.title)}</title><link>${SITE}${글주소(p.slug)}</link><guid>${SITE}${글주소(p.slug)}</guid><description>${esc(p.description)}</description><pubDate>${new Date(p.date + 'T09:00:00+09:00').toUTCString()}</pubDate></item>`).join('\n')}
</channel></rss>
`;
  writeFileSync(resolve(ROOT, 'rss.xml'), rss, 'utf8');
  return { posts, 블로그주소 };
}

/* 혼자 실행할 때 */
const 이파일 = fileURLToPath(import.meta.url);
if (process.argv[1] && resolve(process.argv[1]) === 이파일) {
  const ROOT = resolve(dirname(이파일), '..');
  const { posts, 블로그주소 } = buildBlog({ ROOT });
  console.log(`blog/: 글 ${posts.length}개 · sitemap 항목 ${블로그주소.length}개 · rss.xml · llms.txt 갱신`);
}
