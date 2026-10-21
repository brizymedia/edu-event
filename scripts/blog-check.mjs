/**
 * 이벤트와 교육연구소 블로그 글 검사 — 올리기 전에 반드시 통과해야 한다
 * ─────────────────────────────────────────────────────────────────
 *   node scripts/blog-check.mjs                 모든 글 검사
 *   node scripts/blog-check.mjs --new a.json …  지정한 글만 엄격히 검사하고, 다른 글 전부와 중복 비교
 *
 * 막는 것: 형식 · 분량이 틀린 글, 가격 · 후기 · 순위 · 연혁 · 경험 늘려 말하기, 회사가 하겠다고 한 적 없는 약속,
 * 목록에 없는 사진 · 사진 장소/연도 바꿔 쓰기, 근거 없는 효과 · 통계 · 연구 이야기, 손으로 만든 공식 출처 주소,
 * 없는 내부 링크, 서로 베낀 글. 실패하면 exit 1.
 * (HD기획 scripts/blog-check.mjs 를 이 사이트에 맞게 옮긴 것 — 지역 규칙은 빼고 주제 글 · 회사 사실 · 효과 주장 규칙을 더했다)
 */
import { existsSync, readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { 글읽기, 사진목록, 본문글, 글이미지들, 글자만, 분야표, 예약주소 } from './build-blog.mjs';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const 인자 = process.argv.slice(2);
const 새파일 = 인자[0] === '--new' ? 인자.slice(1) : null;
const 새글 = 새파일 ? new Set(새파일.map((f) => f.split(/[\\/]/).pop())) : null;

const 사진 = 사진목록(ROOT);
const posts = 글읽기(ROOT);
const 공식출처 = JSON.parse(readFileSync(resolve(ROOT, '_blog', 'sources.json'), 'utf8')).출처;
const 회사 = JSON.parse(readFileSync(resolve(ROOT, '_blog', 'company.json'), 'utf8'));
const 주제표 = JSON.parse(readFileSync(resolve(ROOT, '_blog', 'keywords.json'), 'utf8')).주제;
const 도메인 = (u) => { try { return new URL(u).hostname.replace(/^(www|m)\./, ''); } catch { return null; } };
const 공식도메인 = new Set(공식출처.map((s) => 도메인(s.url)));
const 오늘 = new Date(Date.now() + 9 * 3600e3).toISOString().slice(0, 10);

const 오류 = [];
const 경고 = [];
const 틀림 = (p, m) => 오류.push(`✗ ${p._파일}: ${m}`);
const 주의 = (p, m) => 경고.push(`△ ${p._파일}: ${m}`);
const 붙여 = (s) => String(s || '').replace(/\*\*/g, '').replace(/\s+/g, '');
const 글자수 = (s) => [...String(s || '')].length;
const 문장들 = (t) => String(t || '').split(/(?<=[.!?])\s+|\n+/).map((s) => s.trim()).filter(Boolean);
const 회사사실붙임 = 회사.사실.map(붙여);

/* 확인할 수 없는 자랑 · 가격 · 후기 · 효과 · 연구 이야기는 쓰지 않는다 */
const 금지 = [
  [/\d[\d,]*\s*(만|천|억)?\s*원(?=$|[\s.,)·~/]|대|이|을|은|부터|까지|씩|선|정도|가량|짜리)/, '가격(원) — 가격은 쓰지 않는다'],
  [/무료|공짜|당일\s*(회신|답변|견적)|즉시\s*(회신|답변)|최저가|할인/, '가격 · 무료 · 당일 회신 같은 약속 — 대표가 준 약속이 아니다'],
  [/업계\s*(최초|1위)|지역\s*1위|실적\s*1위|No\.?\s*1|넘버원|최고의\s*(업체|회사)/i, '확인할 수 없는 1위 · 최초 표현'],
  [/100\s*%|무조건|보장합니다|보장해\s*드립니다|반드시\s*성공/, '보장 · 100% 표현'],
  [/\d+\s*%|\d+\s*퍼센트/, '퍼센트 숫자 — 출처 없는 통계는 쓰지 않는다'],
  [/\d+\s*년\s*(경력|전통|노하우|업력)|설립\s*(연도|이래|이후)/, '회사 연혁 · 경력 연수 — 쓰지 않는다'],
  [/후기|고객님\s*말씀|만족도|별점|리뷰|호평|극찬|인기\s*(많|있)/, '후기 · 만족도 · 평판 — 대표 확인 전이라 쓰지 않는다'],
  [/\d[\d,]*\s*(건|회)\s*(이상|넘게|넘는)?\s*(의\s*)?(행사|진행|실적|공연)/, '행사 · 진행 건수 — 쓰지 않는다'],
  [/(대응해|맡아|진행해|운영해|해|도와|준비해|이끌어)\s*(왔|온\s*경험)/, "경험을 늘려 말하는 표현('~해 왔습니다') — 확인된 학교 수 · 이력으로만 말한다"],
  [/프로이벤트|나인엠씨|NINEMC|PRO\s*EVENT|경쟁\s*업체/i, '다른 회사 이름 · 비교 — 쓰지 않는다'],
  [/효과가\s*(있|입증|검증|탁월|뛰어)|향상(됩니다|시킵니다|시켜\s*줍니다|된다)|개선(됩니다|시킵니다|된다)|(?<!심리)치료|진단|처방|치유|(?:ADHD|우울증|불안장애)/, '근거 없는 효과 · 의학 표현 — 효과를 단정하지 않는다'],
  [/전문가들은|연구자들은|연구에\s*따르면|연구\s*결과|조사에\s*따르면|통계에\s*따르면|알려져\s*있습니다|밝혀졌|입증됐|입증되었/, '출처 없는 연구 · 통계 · 통설 — 쓰지 않는다(공식 출처가 있으면 sources 에 달고 그 범위 안에서)'],
  [/사진[은이]?\s*아직\s*없|(이\s*글|글|사진)[을은도]?\s*(바꿀|고칠|갱신할|보탤|더할|업데이트할)\s*예정|작성자용/, '작성자용 메모를 글에 옮겼거나 글을 나중에 고치겠다고 약속했다'],
];

const 링크들 = (글) => [...String(글 || '').matchAll(/\[([^\]]+)\]\(([^)\s]*)\)/g)].map((m) => m[2]);
const 허브주소 = new Set(['/blog/', ...Object.keys(분야표).map((k) => `/blog/${k}/`)]);
const 글주소들 = new Set(posts.flatMap((p) => [`/blog/${p.slug}/`, `/blog/${encodeURIComponent(p.slug)}/`]));
function 내부주소있나(u) {
  const 경로 = u.split('#')[0].split('?')[0];
  if (허브주소.has(경로) || 글주소들.has(경로)) return true;
  if (경로.startsWith('/blog/')) return false;
  if (경로 === '/') return true;
  return existsSync(resolve(ROOT, '.' + decodeURIComponent(경로)));
}

/* 글자 4개씩 묶어 겹치는 비율 — 서로 베낀 글을 잡는다 */
function 조각들(p) {
  const t = 본문글(p).replace(/[\s\d.,·—\-()［\]\[/:%~]+/g, '');
  const s = new Set();
  for (let i = 0; i + 4 <= t.length; i++) s.add(t.slice(i, i + 4));
  return s;
}
const 겹침 = (a, b) => { let n = 0; for (const x of a) if (b.has(x)) n++; return n / (a.size + b.size - n || 1); };

const 슬러그수 = new Map(); posts.forEach((p) => 슬러그수.set(p.slug, (슬러그수.get(p.slug) || 0) + 1));
const 주제수 = new Map(); posts.forEach((p) => 주제수.set(p.topic, (주제수.get(p.topic) || 0) + 1));
const 검사대상 = posts.filter((p) => (새글 ? 새글.has(p._파일) : true));
const 비교대상 = 검사대상;
if (새글 && 검사대상.length !== 새글.size) 오류.push(`✗ --new 로 준 파일 중 _blog/posts 에 없는 것이 있다: ${[...새글].join(', ')}`);

for (const p of 검사대상) {
  /* 형식 */
  const 전 = 오류.length;
  for (const k of ['slug', 'date', 'category', 'topic', 'title', 'description', 'lead']) if (typeof p[k] !== 'string' || !p[k].trim()) 틀림(p, `${k} 없음`);
  if (!p.keyword || typeof p.keyword.main !== 'string') 틀림(p, 'keyword.main 없음');
  if (!Array.isArray(p.points) || p.points.length < 3 || p.points.length > 5) 틀림(p, 'points 는 3~5개');
  if (!Array.isArray(p.sections) || p.sections.length < 4 || p.sections.length > 8) 틀림(p, 'sections 는 4~8개');
  if (!Array.isArray(p.faq) || p.faq.length < 2 || p.faq.length > 6) 틀림(p, 'faq 는 2~6개');
  if (!Array.isArray(p.sources)) 틀림(p, 'sources 배열 없음(없으면 [])');
  if (오류.length > 전 && (!Array.isArray(p.sections) || !p.keyword)) continue;

  if (!/^[가-힣a-z0-9]+(-[가-힣a-z0-9]+)*$/.test(p.slug) || 글자수(p.slug) > 70) 틀림(p, 'slug 는 한글·영소문자·숫자와 - 만, 70자 이하');
  if (예약주소.has(p.slug)) 틀림(p, 'slug 가 예약된 주소와 같다');
  if (슬러그수.get(p.slug) > 1) 틀림(p, 'slug 가 다른 글과 같다');
  if (p._파일 !== `${p.date}-${p.slug}.json`) 틀림(p, `파일 이름은 ${p.date}-${p.slug}.json`);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(p.date) || p.date > 오늘) 틀림(p, `date 형식이 틀렸거나 오늘(${오늘})보다 뒤`);
  if (!분야표[p.category]) 틀림(p, `category 는 ${Object.keys(분야표).join(' · ')} 중 하나`);
  const 주제 = 주제표.find((t) => t.topic === p.topic);
  if (!주제) 틀림(p, `topic '${p.topic}' 은 _blog/keywords.json 에 없다`);
  else {
    if (주제.category !== p.category) 틀림(p, `topic '${p.topic}' 의 category 는 ${주제.category}`);
    if (p.keyword.main !== 주제.k) 틀림(p, `keyword.main 은 keywords.json 의 '${주제.k}' 그대로`);
  }
  if (주제수.get(p.topic) > 1) 틀림(p, `같은 topic 글이 둘 이상이다`);

  /* 제목 · 설명 · 키워드 */
  if (글자수(p.title) < 15 || 글자수(p.title) > 50) 틀림(p, `title 은 15~50자 (지금 ${글자수(p.title)})`);
  if (글자수(p.description) < 70 || 글자수(p.description) > 160) 틀림(p, `description 은 70~160자 (지금 ${글자수(p.description)})`);
  if (글자수(p.lead) < 80 || 글자수(p.lead) > 420) 틀림(p, `lead 는 80~420자 (지금 ${글자수(p.lead)})`);
  const 키 = 붙여(p.keyword.main);
  if (!붙여(p.title).includes(키)) 틀림(p, `title 에 핵심 키워드 '${p.keyword.main}' 가 없다`);
  if (!붙여(p.description).includes(키)) 틀림(p, `description 에 핵심 키워드가 없다`);
  if (!붙여(p.lead).includes(키)) 틀림(p, `lead(첫 문단)에 핵심 키워드가 없다`);
  const 본문 = 본문글(p);
  const 키횟수 = 붙여(본문).split(키).length - 1;
  if (키횟수 > 12) 주의(p, `핵심 키워드가 본문에 ${키횟수}번 — 억지로 넣은 느낌이 난다`);
  if (!p.sections.some((s) => 붙여(s.h2).includes(키))) 주의(p, '소제목(h2) 어디에도 핵심 키워드가 통째로 없다');

  /* 분량 · 구성 */
  const 길이 = 글자수(본문);
  if (길이 < 1800) 틀림(p, `본문이 짧다 (${길이}자, 1800자 이상)`);
  else if (길이 < 2500) 주의(p, `본문 ${길이}자 — 2500자 이상을 권한다`);
  const 블록들 = p.sections.flatMap((s) => s.blocks || []);
  p.sections.forEach((s, i) => { if (!s.h2 || !(s.blocks || []).length) 틀림(p, `sections[${i}] 에 h2 나 blocks 가 없다`); });
  if (!블록들.some((b) => b.table)) 틀림(p, '표(table)가 하나도 없다 — 체크리스트 표 1개 이상');
  블록들.forEach((b) => { if (b.table && (!Array.isArray(b.table.head) || !b.table.rows.every((row) => row.length === b.table.head.length))) 틀림(p, '표의 칸 수가 머리와 다르다'); });
  (p.faq || []).forEach((f, i) => { if (!f.q || !f.a) 틀림(p, `faq[${i}] 에 q 나 a 가 없다`); });

  /* 사진 — 없어도 된다. 쓰면 목록의 것만, 캡션은 포트폴리오 제목 그대로 */
  const 이미지 = 글이미지들(p);
  if (p.cover && (!p.cover.path)) 틀림(p, 'cover.path 없음');
  const 묶음 = new Set();
  for (const im of 이미지) {
    const 정보 = 사진.get(im.path);
    if (!정보) { 틀림(p, `사진 ${im.path} 은 _blog/photos.json 에 없다`); continue; }
    if (정보.제외) { 틀림(p, `사진 ${im.path} 은 쓰지 않는 사진 — ${정보.제외}`); continue; }
    if (묶음.has(정보.묶음번호)) 틀림(p, `사진 ${im.path} — 같은 사진을 한 글에 두 번 썼다`);
    묶음.add(정보.묶음번호);
    if (!existsSync(resolve(ROOT, '.' + im.path))) 틀림(p, `사진 파일이 없다: ${im.path}`);
    if (글자수(im.alt) < 8 || 글자수(im.alt) > 120) 틀림(p, `사진 ${im.path} alt 는 8~120자`);
    if (!im.caption) { 틀림(p, `사진 ${im.path} caption 없음`); continue; }
    if (!im.caption.includes(정보.제목)) 틀림(p, `사진 ${im.path} 캡션에 포트폴리오 제목 '${정보.제목}' 이 그대로 들어 있어야 한다 — 장소 · 학교 · 연도를 지어 쓰지 않는다`);
    const 설명 = `${im.alt} ${im.caption}`;
    const 허용연도 = `${정보.제목} ${정보.부제 || ''}`;
    for (const y of 설명.match(/(19|20)\d{2}/g) || []) if (!허용연도.includes(y)) 틀림(p, `사진 ${im.path} 설명에 연도 '${y}' — 목록에 없는 연도다`);
    const 학교 = 설명.match(/[가-힣]{2,}(초등학교|중학교|고등학교|대학교)/);
    if (학교) 틀림(p, `사진 ${im.path} 설명에 학교 이름처럼 보이는 '${학교[0]}' — 사진의 장소를 지어 쓰지 않는다`);
  }

  /* 표현 */
  const 캡션들 = 이미지.map((im) => `${im.alt} ${im.caption}`);
  const 전체글 = [p.title, p.description, 본문, ...캡션들].join('\n');
  for (const [식, 이유] of 금지) {
    const m = 전체글.match(식);
    if (!m) continue;
    if (이유.startsWith('출처 없는') && (p.sources || []).length) continue;   // 출처를 달았으면 그 범위 안에서 쓸 수 있다(사람이 확인)
    틀림(p, `${이유} — "${m[0]}"`);
  }
  /* 숫자 + 곳 은 확인된 학교 수만 */
  for (const m of 전체글.matchAll(/\d[\d,]*\s*곳/g)) if (!회사.허용숫자.includes(m[0].replace(/\s+/g, ''))) 틀림(p, `'${m[0]}' — 회사 사실에 없는 곳 수`);
  for (const m of 전체글.matchAll(/(19|20)\d{2}\s*년/g)) if (!회사.허용숫자.includes(m[0].replace(/\s+/g, ''))) 주의(p, `연도 '${m[0]}' — 근거가 있는 연도인지 확인`);

  /* 링크 */
  const 원문 = JSON.stringify(p);
  for (const u of 링크들(원문)) {
    if (u.startsWith('/')) { if (!내부주소있나(u)) 틀림(p, `없는 내부 주소 링크: ${u}`); }
    else if (!u.startsWith('https://')) 틀림(p, `링크는 / 또는 https:// 로 시작: ${u}`);
  }
  const 내부 = 링크들(원문).filter((u) => u.startsWith('/'));
  if (!내부.some((u) => u.startsWith('/contact.html') || u.startsWith('/quote.html'))) 틀림(p, '상담 링크(/contact.html 또는 /quote.html)가 없다');
  if (!내부.some((u) => /^\/(event|education)\.html/.test(u))) 틀림(p, '/event.html 또는 /education.html 링크가 없다');
  if (내부.length < 2) 틀림(p, '내부 링크가 2개 미만이다');

  /* 회사를 주어로 한 문장 — 대표가 준 약속 밖의 것을 약속하면 안 된다 */
  const 약속단위 = [...문장들(글자만([p.description, p.lead, ...(p.points || []), ...p.sections.flatMap((s) => (s.blocks || []).flatMap((b) => [b.p, b.tip, ...(b.ul || []), ...(b.ol || [])]))].filter(Boolean).join('\n'))),
    ...(p.faq || []).map((f) => 글자만(`${f.q} ${f.a}`))];
  for (const 단위 of 약속단위) {
    if (/(소장|저희|이벤트와\s*교육연구소|연구소)/.test(단위) && /(드립니다|드려요|해\s*줍니다|해드립|제공|지원합니다|가능합니다|보내|맡깁|맡아|책임집|책임지)/.test(단위)
        && !회사.약속키워드.some((k) => 붙여(단위).includes(붙여(k)))) {
      틀림(p, `회사가 하겠다고 한 적 없는 약속일 수 있다(허용: ${회사.약속키워드.join(' · ')}) — "${단위.slice(0, 70)}…"`);
    }
  }

  /* 출처 — 공식 기관 도메인은 사람이 확인한 주소(_blog/sources.json)만 */
  const 출처주소 = new Set();
  (p.sources || []).forEach((s, i) => {
    if (!s.name || !/^https:\/\//.test(s.url || '')) { 틀림(p, `sources[${i}] 는 name 과 https:// url 이 필요`); return; }
    출처주소.add(s.url);
    const d = 도메인(s.url);
    if (!d) 틀림(p, `sources[${i}] 주소 형식이 틀렸다: ${s.url}`);
    else if (!공식출처.some((o) => o.url === s.url)) 틀림(p, `sources[${i}] 는 _blog/sources.json 에 있는 주소만 쓴다: ${s.url}`);
  });
  if (/「[^」]*(법|규칙|기준)」|법\s*(제\s*\d|에\s*따라|상의?\s)|시행령|시행규칙|조례|기상청|고시|지침|소비자원|주의보|특보|인증/.test(본문) && !(p.sources || []).length) 틀림(p, '법 · 기준 · 기관 · 특보 이야기를 했는데 sources 가 비었다');

  /* 근거 — 글에 쓴 사실이 어디서 왔는지 */
  const 근거 = p.근거;
  if (!Array.isArray(근거) || 근거.length < 2) 틀림(p, '근거는 2개 이상 — { "내용": 본문에 그대로 있는 구절, "출처": "company.json" 또는 이 글 sources 의 주소 }');
  else {
    const 본문붙임 = 붙여([본문, ...캡션들, p.title, p.description].join(' '));
    let 회사근거 = 0, 출처근거 = 0;
    근거.forEach((g, i) => {
      if (!g || !g.내용 || !g.출처) { 틀림(p, `근거[${i}] 에 내용 · 출처가 없다`); return; }
      if (글자수(g.내용) < 4) 틀림(p, `근거[${i}] 내용이 너무 짧다`);
      if (!본문붙임.includes(붙여(g.내용))) 틀림(p, `근거[${i}] "${g.내용}" 이 본문에 그대로 없다`);
      if (g.출처 === 'company.json') {
        if (글자수(g.내용) > 45) 틀림(p, `근거[${i}] company.json 근거는 45자 이하 핵심 구절로`);
        if (!회사사실붙임.some((f) => f.includes(붙여(g.내용)))) 틀림(p, `근거[${i}] "${g.내용}" 은 _blog/company.json 사실 문장에 없다`);
        else 회사근거 += 1;
      } else if (!출처주소.has(g.출처)) 틀림(p, `근거[${i}] 출처는 'company.json' 이거나 이 글 sources 에 있는 주소여야 한다: ${g.출처}`);
      else 출처근거 += 1;
    });
    if (회사근거 < 1) 틀림(p, 'company.json 근거가 하나는 있어야 한다(글이 회사 사실을 말하는 자리)');
    if ((p.sources || []).length && 출처근거 < 1) 틀림(p, 'sources 를 달았으면 그 출처에서 가져온 구절을 근거로 하나 이상 적는다');
  }
  /* 글에 나온 회사 이력 고유명사는 company.json 에 있는 것만 */
  for (const m of 전체글.matchAll(/『[^』]+』|「[^」]+」/g)) {
    if (/(법|규칙|기준)」$/.test(m[0])) continue;
    if (!회사사실붙임.some((f) => f.includes(붙여(m[0])))) 주의(p, `${m[0]} — 회사 사실 목록에 없는 책 · 논문 · 법 이름이면 확인`);
  }
}

/* 서로 베낀 글 */
const 조각표 = new Map();
const 조각 = (p) => { if (!조각표.has(p)) 조각표.set(p, 조각들(p)); return 조각표.get(p); };
for (const p of 비교대상) {
  for (const o of posts) {
    if (o === p || (비교대상.includes(o) && o._파일 < p._파일)) continue;
    const v = 겹침(조각(p), 조각(o));
    if (v > 0.3) 틀림(p, `${o._파일} 와 본문이 ${(v * 100).toFixed(0)}% 겹친다`);
    else if (v > 0.2) 주의(p, `${o._파일} 와 본문이 ${(v * 100).toFixed(0)}% 겹친다`);
  }
}

console.log(`블로그 검사 — 글 ${posts.length}개 중 ${검사대상.length}개 검사`);
경고.forEach((m) => console.log(m));
오류.forEach((m) => console.log(m));
if (오류.length) { console.log(`실패 ${오류.length}건`); process.exit(1); }
console.log(`통과${경고.length ? ` (주의 ${경고.length}건)` : ''}`);
