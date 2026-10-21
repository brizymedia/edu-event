# -*- coding: utf-8 -*-
"""
이벤트와 교육연구소 홈페이지 페이지 생성기.

  python tools/build_site.py

index · about · ceo · event · education · portfolio · contact · notice · 404 와 sitemap.xml · robots.txt · llms.txt 를 만든다.
글 · 사진 목록을 고칠 땐 이 파일(맨 위 「회사 정보」 「자료」)을 고치고 다시 돌릴 것. 결과 HTML 을 손으로 고치지 말 것.
공지사항은 assets/data/notices.json 만 고치면 된다.
"""
import os, json, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ════════════════════════ 회사 정보 ════════════════════════
NAME = '이벤트와 교육연구소'
NAME_EN = 'Event & Education institute'
CEO = '황윤수'
BIZNO = '578-03-01411'                       # 계약서(KB-20261009-273) 기준
ADDR = '인천광역시 남동구 문화서로62번길 17, 3층 302호'
TEL = '010-9189-5589'                        # 기존 시안의 대표 번호 — 대표 확인 필요
TEL_RAW = TEL.replace('-', '')
EMAIL = 'ihaha2040@gmail.com'                # 기존 시안의 대표 메일 — 대표 확인 필요
KAKAO = 'http://pf.kakao.com/_XVrSs/chat'
NBLOG = 'https://blog.naver.com/event_edu'
BASE = 'https://brizymedia.github.io/edu-event'   # 도메인을 정하면 여기만 바꾸고 다시 실행 (계약: 도메인 오픈 시점에 협의)
NOINDEX = True                               # 오픈 확정 뒤 False 로 바꾸고 다시 실행
VER = '1'
EDIT_HASH = '15537d4153185a776f0e6b1512f411d17593a40ebf0d3bc5a89f6ae8cffa6c4c'   # 사장님 직접 수정 열쇠의 sha256 (열쇠 자체는 어디에도 적지 않는다)
OG = BASE + '/assets/img/og.jpg'
MAP = 'https://map.naver.com/p/search/' + '%EC%9D%B8%EC%B2%9C%EA%B4%91%EC%97%AD%EC%8B%9C%20%EB%82%A8%EB%8F%99%EA%B5%AC%20%EB%AC%B8%ED%99%94%EC%84%9C%EB%A1%9C62%EB%B2%88%EA%B8%B8%2017'

NAV = [('about.html', '회사 소개'), ('event.html', '행사'), ('education.html', '교육'), ('portfolio.html', '포트폴리오'), ('contact.html', '견적 문의')]

# ════════════════════════ 자료 ════════════════════════
EVENT_CATS = [
    dict(id='kinder', name='유치원 · 어린이집', c='#FFD9D1', title='처음 만나는 운동회, 가장 즐거운 하루', img='g10', alt='어린이집 크리스마스 매직쇼 현장',
         intro='아이들의 첫 운동회와 첫 축제는 평생 기억에 남습니다. 연령에 맞는 쉽고 안전한 프로그램으로, 아이도 선생님도 학부모님도 함께 웃는 시간을 만듭니다.',
         prog=['명랑운동회', '버블쇼', '매직쇼', '어린이날 체험부스', '레크리에이션']),
    dict(id='school', name='초등학교', c='#CFE5A3', title='운동회부터 학교 축제까지', img='g01', alt='초등학교 체육대회 현장',
         intro='학년별 눈높이에 맞춘 운동회와 체육대회, 아이들이 주인공이 되는 학교 축제와 학예회까지. 진행부터 에어바운스, 음향 · 조명 장비까지 학교 행사의 모든 것을 준비합니다.',
         prog=['운동회', '체육대회', '레크리에이션', '에어바운스', '놀이체험', '매직쇼', '버블쇼', '학교축제', '학예회 음향 및 조명']),
    dict(id='corp', name='기업체 · 기관', c='#FBD9A8', title='순서와 격식이 중요한 행사', img='g08', alt='대학 홈커밍데이 매직쇼 무대',
         intro='조직의 분위기를 살리는 체육대회와 팀빌딩부터, 한 치의 실수도 허락되지 않는 기념식까지. 행사 성격에 맞는 진행과 연출로 품격 있는 자리를 완성합니다.',
         prog=['체육대회', '레크리에이션', '팀빌딩', '송년회', '신년회', '시상식', '이취임식', '기공식', '준공식', '오픈식', '전문 MC', '가수 섭외']),
    dict(id='local', name='지자체 · 축제', c='#C9E6F7', title='무대부터 사람까지', img=None, alt='',
         intro='지역 주민이 함께 즐기는 축제는 무대, 장비, 인력이 맞물려야 성공합니다. 기획부터 무대 설치, 공연 운영, 체험부스까지 축제 현장 전체를 책임지고 운영합니다.',
         prog=['지역축제', '공연행사 운영', '무대 · 음향 · 조명', '천막 · 테이블 · 장비 대여', '체험부스 운영']),
    dict(id='church', name='교회', c='#E3D6F6', title='온 교회가 함께 웃는 시간', img='g05', alt='성탄 축하 행사 매직쇼 무대',
         intro='주일학교 아이들부터 온 성도까지 한마음이 되는 행사를 만듭니다. 교회 공동체의 분위기에 맞춘 프로그램으로 즐거움과 은혜를 함께 나눕니다.',
         prog=['교회 체육대회', '여름성경학교 레크리에이션', '성탄 · 어린이주일 행사', '버블쇼', '매직쇼']),
]
AUD_SHORT = {
    'kinder': '아이도 선생님도 학부모님도 함께 웃는 첫 운동회',
    'school': '운동회, 체육대회, 학교 축제까지 한 번에',
    'corp': '체육대회부터 격식 있는 기념식까지',
    'local': '무대 · 장비 · 인력을 통째로 운영',
    'church': '주일학교부터 온 성도까지 한마음으로',
}
EDU = [
    dict(n='감정교육', who='유아 · 초등', c='#FFD9D1', ic='heart', fx='정서지능 향상, 또래 관계 개선',
         t='놀이를 통해 내 마음을 알아보고, 친구의 마음을 읽는 법을 배웁니다. 감정놀이 연구를 바탕으로 한 프로그램입니다.'),
    dict(n='임원 리더십', who='초등 · 청소년', c='#CFE5A3', ic='flag', fx='리더십, 자신감, 협동심',
         t='학급 · 학생회 임원이 갖춰야 할 소통, 책임감, 협력을 활동 중심으로 배웁니다.'),
    dict(n='발표회', who='초등 · 청소년', c='#FBD9A8', ic='mic', fx='발표력, 자기표현력',
         t='사람들 앞에서 말하는 두려움을 줄이고, 내 생각을 자신 있게 표현하는 방법을 익힙니다.'),
    dict(n='과학실험 마술수업', who='유치부 · 초등부', c='#C9E6F7', ic='flask', fx='과학 흥미, 탐구력',
         t='마술 속에 숨은 과학 원리를 직접 실험하며 배웁니다. 신기함이 호기심으로, 호기심이 탐구로 이어집니다.'),
    dict(n='직업체험', who='초중고', c='#E3D6F6', ic='brief', fx='직업 이해, 진로 동기',
         t='다양한 직업을 직접 체험하며 일의 의미와 나에게 맞는 일을 생각해 봅니다.'),
    dict(n='진로탐색 강의', who='초중고', c='#C7EBDD', ic='compass', fx='자기이해, 진로 설계',
         t='나의 흥미와 강점을 발견하고, 꿈을 구체적인 계획으로 연결합니다.'),
]
# 사진 번호 g01~g10 (assets/img/g*.webp) ↔ 제목 · 분류. 필터 slug: kinder school corp local church edu
WORKS = [
    ('g01', '초등학교 체육대회', '대형 공 굴리기 · 체육관', 'school', 'w t'),
    ('g10', '어린이집 크리스마스 매직쇼', '', 'kinder', ''),
    ('g03', '초등학교 명랑운동회', '낙하산 놀이', 'school', ''),
    ('g04', '초등학교 운동회', '운동장 단체 게임', 'school', 'w'),
    ('g05', '성탄 축하 행사 매직쇼', '', 'church', ''),
    ('g06', '운동회 에어바운스', '', 'school', ''),
    ('g07', '초등학교 체육대회', '체육관 단체 게임', 'school', 'w'),
    ('g08', '대학 홈커밍데이 매직쇼', '2018', 'corp', ''),
    ('g09', '비둘기 마술', '', 'corp', ''),
    ('g02', '유치원 매직쇼', '', 'kinder', ''),
]
PF_FILTERS = [('all', '전체'), ('kinder', '유치원 · 어린이집'), ('school', '초등학교'), ('corp', '기업체 · 기관'), ('local', '지자체 · 축제'), ('church', '교회'), ('edu', '교육')]
REVIEWS = [
    ('30년 이상 교직생활을 하면서 비슷한 종목도 있는데 이번처럼 재미있었던 적은 없었습니다. 내년 운동회 <mark>꼭 예약해 주세요!</mark>', '초등학교 선생님'),
    ('<mark>역대급 최고의 운동회</mark>였습니다! 예년에 해보지 못한 경기들이 있어서 학생들이 더 좋아했고, 학년별로 나눠 진행한 게 굿 초이스였습니다.', '초등학교 담당교사'),
    ('다양한 프로그램이 있어 너무 좋았습니다. <mark>학생들을 다루는 솜씨가 좋아서</mark> 학부모님들도 교직원들도 칭찬을 많이 하셨습니다.', '초등학교 교장선생님'),
    ('친구들과 다 같이 즐길 수 있어서 너무 좋았어요. 처음 해보는 <mark>산가지놀이랑 무궁화꽃이 피었습니다 놀이</mark>는 신기했어요.', '초등학교 6학년 학생'),
]
TIMELINE = [
    ('~2010', '#FA8A7A', 'MC · 마술사로 무대에', '이벤트비전 수석실장, 서울시립청소년직업체험센터 전문강사로 이벤트 MC와 마술 공연을 시작했습니다.'),
    ('2011', '#F4A55A', '학교 운동회 · 체육대회 진행', '인천 용정초 · 강화갑룡초 운동회, 위즈 한마음 체육대회 등 단체 체육행사를 본격적으로 맡았습니다.'),
    ('2013 ~ 2019', '#7DB55A', '서울 · 경기로 확장', '서울 · 경기 초등학교 운동회를 해마다 맡으며, 같은 학교에서 여러 해 연속 다시 불러주시는 일이 늘었습니다.'),
    ('현재', '#8CC3EA', '이벤트와 교육연구소', '운동회 · 레크리에이션 · 매직쇼에 더해 감정교육, 리더십, 진로교육까지 즐거움과 성장이 함께하는 현장을 만들고 있습니다.'),
]
TICKER = ['유치원 · 어린이집 행사', '초등학교 운동회', '버블쇼', '매직쇼', '명랑운동회', '체험부스', '기업체 체육대회', '시상식 · 기념식', '지역축제', '교회 행사', '감정교육', '임원 리더십', '과학실험 마술수업', '진로탐색 강의']
FAQ = [
    ('견적은 어떻게 받나요?', '행사 날짜, 장소, 예상 인원만 알려 주시면 됩니다. 아래 문의 양식, 전화, 카카오톡 어느 쪽이든 편하신 방법으로 연락 주세요. 항목을 직접 골라 요청서를 만들고 싶으시면 「자동 견적서」를 이용하세요.'),
    ('행사 날짜가 아직 안 정해졌어도 문의할 수 있나요?', '그럼요. 대략적인 시기와 규모만 알려 주셔도 프로그램 구성과 예산 방향을 함께 정리해 드립니다.'),
    ('사전 상담이나 현장 답사도 해 주시나요?', '행사 전에 공간과 인원을 확인하고 맞춤으로 기획합니다. 우천 등 돌발 상황에 대비한 실내 대체 프로그램도 함께 준비합니다.'),
    ('행사 후 사진을 받을 수 있나요?', '행사가 끝나면 현장 사진을 정리해 보내드립니다.'),
    ('교육 프로그램은 몇 회로 운영하나요?', '1회 특강부터 4회, 8회 과정까지 대상과 목적에 맞춰 구성합니다. 기관 일정과 공간에 맞춰 유연하게 조정할 수 있습니다.'),
]
SCHOOLS = json.load(open(os.path.join(ROOT, 'assets/data/schools.json'), encoding='utf-8'))
NOTICES = json.load(open(os.path.join(ROOT, 'assets/data/notices.json'), encoding='utf-8'))
NJ = html.escape(json.dumps(NOTICES, ensure_ascii=False), quote=True).replace("'", '&#39;')

# ════════════════════════ 조각 ════════════════════════
esc = lambda s: html.escape(str(s), quote=True)
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ICONS = {
    'heart': '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
    'flag': '<path d="M6 21V4M6 5h11l-2 4 2 4H6"/>',
    'mic': '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21"/>',
    'flask': '<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.8 3h10.4a2 2 0 0 0 1.8-3l-5-9V3M8 15h8"/>',
    'brief': '<rect x="3" y="7" width="18" height="13" rx="2.5"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>',
    'compass': '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
}
CHECK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'


def btn(href, text, cls='', ext=False):
    t = ' target="_blank" rel="noopener"' if ext else ''
    return f'<a class="btn {cls}" href="{href}"{t}>{text}<span class="ar">{ARROW}</span></a>'


def header(cur):
    items = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h == cur else ""}>{t}</a>' for h, t in NAV)
    sheet = ''.join(f'<a class="m" href="{h}">{t}</a>' for h, t in NAV)
    return f'''<a class="skip" href="#main">본문으로 바로가기</a>
<header class="hdr"><div class="pill">
  <a class="logo" href="index.html" aria-label="{NAME} 처음으로"><img src="assets/img/logo-h.png" alt="{NAME} {NAME_EN}" width="243" height="36"></a>
  <nav aria-label="주 메뉴">{items}</nav>
  <a class="tel" href="tel:{TEL_RAW}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>{TEL}</a>
  <button class="mbtn" aria-label="메뉴 열기" aria-expanded="false" aria-controls="sheet"><i></i><i></i><i></i></button>
</div></header>
<div class="sheet" id="sheet">{sheet}
  <div class="sub"><a href="ceo.html">대표 소개</a><a href="notice.html">공지사항</a><a href="quote.html">자동 견적서</a><a href="{NBLOG}" target="_blank" rel="noopener">네이버 블로그</a></div>
  <div class="btns" style="margin-top:28px">{btn("tel:" + TEL_RAW, "전화 " + TEL, "coral")}</div>
</div>'''


def footer():
    return f'''<footer class="ft"><div class="wrap">
  <div class="grid">
    <div><img class="fl" src="assets/img/logo-h.png" alt="{NAME}" width="243" height="36">
      <div class="info"><b style="color:#fff">{NAME}</b> · 소장 {CEO}<br>사업자등록번호 {BIZNO}<br>{ADDR}<br>전화 <a href="tel:{TEL_RAW}" style="display:inline">{TEL}</a> · <a href="mailto:{EMAIL}" style="display:inline">{EMAIL}</a></div></div>
    <div><h4>회사</h4><a href="about.html">회사 소개</a><a href="ceo.html">대표 소개</a><a href="notice.html">공지사항</a><a href="contact.html">오시는 길</a></div>
    <div><h4>서비스</h4><a href="event.html">행사</a><a href="education.html">교육</a><a href="portfolio.html">포트폴리오</a><a href="quote.html">자동 견적서</a></div>
    <div><h4>문의</h4><a href="contact.html">견적 문의</a><a href="{KAKAO}" target="_blank" rel="noopener">카카오톡 상담</a><a href="{NBLOG}" target="_blank" rel="noopener">네이버 블로그</a></div>
  </div>
  <div class="copy"><span>© {datetime.date.today().year} {NAME}. All rights reserved.</span><span>즐거움을 기획하고, 성장을 교육합니다</span></div>
  <p class="src">이 사이트의 사진 · 글은 {NAME}가 직접 운영한 행사와 교육 자료입니다. 무단 복제를 금합니다.</p>
</div></footer>
<div class="dock"><a href="tel:{TEL_RAW}">전화 상담</a><a href="{KAKAO}" target="_blank" rel="noopener">카카오톡 상담</a></div>
<div class="lb" role="dialog" aria-label="사진 크게 보기"><button aria-label="닫기">×</button><div style="text-align:center"><img alt="" src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="><p></p></div></div>
<script src="assets/app.js?v={VER}"></script>
<script src="assets/edit.js?v={VER}" defer></script>
<script defer src="https://www.ai-make.co.kr/stats/stats.js" data-site="edu"></script>'''


def jsonld_biz():
    d = {
        '@context': 'https://schema.org', '@type': 'LocalBusiness', '@id': BASE + '/#business', 'name': NAME, 'alternateName': NAME_EN,
        'url': BASE + '/', 'image': OG, 'logo': BASE + '/assets/img/logo-arch.png', 'telephone': TEL, 'email': EMAIL,
        'description': '즐거움을 기획하고 성장을 교육하는 행사·교육 전문 기관. 학교·기업체·기관·교회 행사부터 감정교육·리더십·진로교육까지 함께합니다.',
        'address': {'@type': 'PostalAddress', 'addressCountry': 'KR', 'addressRegion': '인천광역시', 'addressLocality': '남동구', 'streetAddress': '문화서로62번길 17, 3층 302호'},
        'founder': {'@type': 'Person', 'name': CEO, 'jobTitle': '소장'},
        'areaServed': ['서울', '인천', '경기'], 'sameAs': [NBLOG],
        'knowsAbout': ['유치원 운동회', '초등학교 운동회', '레크리에이션', '매직쇼', '버블쇼', '기업체 체육대회', '지역축제', '감정교육', '리더십 교육', '진로교육'],
    }
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>'


def page(fn, title, desc, body, cur='', extra_head='', og_img=None):
    url = BASE + '/' + ('' if fn == 'index.html' else fn)
    robots = '<meta name="robots" content="noindex,nofollow">' if NOINDEX else ''
    og = og_img or OG
    EDIT_META = ('<meta name="edu-edit" content="' + EDIT_HASH + '">') if fn not in ('notice-admin.html', '404.html') else ''
    out = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<meta name="theme-color" content="#FFF9F1">
{EDIT_META}
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="apple-touch-icon" href="assets/img/favicon.png">
<meta property="og:type" content="website"><meta property="og:locale" content="ko_KR"><meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="assets/style.css?v={VER}">
{extra_head}
</head>
<body>
{header(cur)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
'''
    open(os.path.join(ROOT, fn), 'w', encoding='utf-8', newline='\n').write(out)
    print('wrote', fn)


def phead(crumb, eb, h1, lead=''):
    return f'''<section class="phead"><div class="wrap">
  <p class="crumb"><a href="index.html">홈</a> › {crumb}</p>
  <span class="eb"><i></i>{eb}</span>
  <h1 class="rv">{h1}</h1>
  {f'<p class="lead rv d1">{lead}</p>' if lead else ''}
</div></section>'''


def cta_band(title='행사 날짜가 정해지셨나요?', sub='지금 견적을 받아보세요. 날짜 · 장소 · 인원만 알려 주시면 됩니다.'):
    return f'''<section class="sec cta"><div class="wrap"><div class="box rv">
  <span class="eb"><i></i>CONTACT</span>
  <h2 style="margin-top:18px">{title}</h2>
  <p>{sub}</p>
  <a class="phone" href="tel:{TEL_RAW}">{TEL}</a>
  <div class="btns">{btn("contact.html", "견적 문의하기", "white")}{btn(KAKAO, "카카오톡 상담", "lime", True)}</div>
</div></div></section>'''


def gal_fig(w, cls=None, k=0):
    code, t, sub, cat, c = w
    c = cls if cls is not None else c
    return (f'<figure class="{c}" data-t="{esc(t + (" · " + sub if sub else ""))}"><img src="assets/img/{code}.webp" alt="{esc(t)}" loading="lazy" decoding="async">'
            f'<figcaption>{esc(t)}{f"<small>{esc(sub)}</small>" if sub else ""}</figcaption></figure>')


# ════════════════════════ 대문 ════════════════════════
def build_index():
    tick = ''.join(f'<span>{esc(t)}</span>' for t in TICKER)
    aud_cols = ['#FFD9D1', '#CFE5A3', '#FBD9A8', '#C9E6F7', '#E3D6F6']
    aud = ''.join(
        f'<a class="rv d{i % 4 + 1}" href="event.html#{c["id"]}" style="--c:{aud_cols[i]}"><span class="n">0{i + 1}</span><h3>{c["name"]}</h3><p>{AUD_SHORT[c["id"]]}</p><span class="more">자세히 보기 →</span></a>'
        for i, c in enumerate(EVENT_CATS))
    gal = ''.join(gal_fig(w) for w in [WORKS[0], WORKS[1], WORKS[2], WORKS[3], WORKS[7], WORKS[4]])
    rev = ''.join(f'<figure class="rv d{i + 1}"><p>{t}</p><cite>{who}</cite></figure>' for i, (t, who) in enumerate(REVIEWS[:3]))
    notes = ''.join(
        f'<li><a href="notice.html#n{i}"><time>{esc(n["d"])}</time><span class="t">{esc(n["t"])}{" <span class=new>NEW</span>" if n.get("n") else ""}</span></a></li>'
        for i, n in enumerate(NOTICES[:4]))
    body = f'''
<section class="hero" aria-label="이벤트와 교육연구소 소개">
  <a class="pane ev" href="event.html" aria-label="행사 보기">
    <img src="assets/img/hero-event.webp" alt="체육관을 가득 채운 아이들의 운동회 현장" width="1600" height="900" fetchpriority="high">
    <div class="cap"><span class="tag">EVENT</span><h2>행사로<br>마음을 모읍니다</h2><p>운동회 · 무대 · 축제 현장</p><span class="go">행사 보기<span>{ARROW}</span></span></div>
  </a>
  <div class="core">
    <div class="arch"><div class="w"><div class="l">
      <p class="brand">Event &amp; Education institute</p>
      <h1>즐거움을 기획하고,<br><em>성장을 교육</em>합니다</h1>
      <p class="sub">행사로 마음을 모으고, 교육으로 사람을 키웁니다</p>
      <p class="desc">학교, 기업체, 기관, 교회까지. 20년 현장 경험으로 기획부터 진행까지 책임지는 행사, 심리상담 전문성을 바탕으로 한 교육을 함께 만듭니다.</p>
      <div class="btns">{btn("event.html", "행사 보기", "coral")}{btn("education.html", "교육 보기", "")}{btn("contact.html", "견적 문의", "white")}</div>
    </div></div></div>
  </div>
  <a class="pane ed" href="education.html" aria-label="교육 보기">
    <img src="assets/img/hero-edu.webp" alt="아이들이 눈을 반짝이며 지켜보는 무대 수업 현장" width="1100" height="771">
    <div class="cap"><span class="tag">EDUCATION</span><h2>교육으로<br>사람을 키웁니다</h2><p>수업 · 강의 현장</p><span class="go">교육 보기<span>{ARROW}</span></span></div>
  </a>
  <div class="confetti" aria-hidden="true"></div>
  <div class="scrollcue" aria-hidden="true">SCROLL</div>
</section>

<div class="ticker" aria-hidden="true"><div class="tr">{tick}</div></div>

<section class="sec" id="numbers"><div class="wrap">
  <div class="sechead"><div><span class="eb lime"><i></i>BY THE NUMBERS</span><h2 class="h2 rv">숫자로 보는 <span class="hl">연구소</span></h2></div>
    <p class="lead rv" style="margin:0">운동장에서 강당까지, 같은 학교가 다시 불러주는 이유를 숫자로 담았습니다.</p></div>
  <div class="stats">
    <div class="stat rv d1"><b data-n="20">0<small>년</small></b><span>행사 · 레크리에이션 현장 경력</span></div>
    <div class="stat rv d2"><b data-n="94">0<small>곳</small></b><span>2011년부터 운동회를 맡긴 학교</span></div>
    <div class="stat rv d3"><b data-n="5">0<small>개</small></b><span>대상별 행사 (유치원 · 학교 · 기업 · 지자체 · 교회)</span></div>
    <div class="stat rv d4"><b data-n="6">0<small>개</small></b><span>교육 프로그램 (감정 · 리더십 · 진로 외)</span></div>
  </div>
</div></section>

<section class="sec sand" id="parts"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>TWO PARTS</span><h2 class="h2 rv">두 개의 <span class="hl">파트</span></h2></div></div>
  <div class="parts">
    <article class="bz part ev rv"><div class="in">
      <div class="ph"><img src="assets/img/g04.webp" alt="초등학교 운동회 운동장 단체 게임" loading="lazy" decoding="async"></div>
      <span class="eb"><i></i>EVENT</span>
      <h3>즐거움을 기획합니다</h3>
      <p>학교 운동회와 축제부터 기업체 행사, 기관의 격식 있는 기념식과 지역 축제, 교회 행사까지. 진행 MC, 공연, 무대 · 음향 · 조명, 장비와 인력까지 한 번에 맡겨주세요.</p>
      <ul class="chips"><li>운동회</li><li>체육대회</li><li>매직쇼 · 버블쇼</li><li>기념식 · 시상식</li><li>지역축제</li></ul>
      {btn("event.html", "행사 자세히 보기", "coral")}
    </div></article>
    <article class="bz part ed rv d2"><div class="in">
      <div class="ph"><img src="assets/img/g02.webp" alt="유치원 매직쇼 수업 무대" loading="lazy" decoding="async"></div>
      <span class="eb lime"><i></i>EDUCATION</span>
      <h3>성장을 교육합니다</h3>
      <p>심리치료상담을 전공한 소장이 직접 설계한 프로그램으로, 자신의 감정을 이해하고 함께 소통하고 스스로의 길을 찾아가도록 돕습니다. 즐거운 활동 속에서 배우기 때문에 오래 기억에 남습니다.</p>
      <ul class="chips"><li>감정교육</li><li>임원 리더십</li><li>발표회</li><li>과학실험 마술수업</li><li>진로탐색</li></ul>
      {btn("education.html", "교육 자세히 보기", "lime")}
    </div></article>
  </div>
</div></section>

<section class="sec" id="audience"><div class="wrap">
  <div class="sechead"><div><span class="eb lime"><i></i>FOR YOU</span><h2 class="h2 rv">어떤 <span class="hl">행사</span>를 준비하세요?</h2></div>
    <p class="lead rv" style="margin:0">대상을 고르면 그 대상에 맞춘 프로그램으로 바로 이동합니다.</p></div>
  <div class="aud">{aud}</div>
</div></section>

<section class="sec sand" id="ceo"><div class="wrap ceo">
  <div class="pic rv"><div class="arch"><img src="assets/img/ceo.webp" alt="이벤트와 교육연구소 소장 {CEO}" loading="lazy" width="496" height="870"></div></div>
  <div class="rv d1">
    <span class="eb"><i></i>CEO</span>
    <p class="quote" style="margin-top:18px">마음을 읽는 MC,<br><span class="hl">성장을 돕는 교육자</span></p>
    <ul class="cv">
      <li>이벤트와 교육연구소 소장 · 이벤트 PD · 레크리에이션 전문가</li>
      <li>인하대학교 교육대학원 석사 (심리치료상담 전공)</li>
      <li>저서 『메타버스, 즐기는 자가 먼저다』 · 논문 「감정놀이 프로그램이 유아의 정서지능에 미치는 영향」</li>
    </ul>
    {btn("ceo.html", "대표 소개 보기", "")}
  </div>
</div></section>

<section class="sec" id="gallery"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>PORTFOLIO</span><h2 class="h2 rv">최근 <span class="hl">행사</span> 갤러리</h2></div>{btn("portfolio.html", "포트폴리오 전체 보기", "line sm")}</div>
  <div class="gal rv">{gal}</div>
  <p class="lead" style="margin-top:22px">더 많은 현장 사진과 후기는 <a href="{NBLOG}" target="_blank" rel="noopener" style="color:var(--coral-ink);font-weight:700">네이버 블로그</a>에서 보실 수 있어요.</p>
</div></section>

<section class="sec sand" id="reviews"><div class="wrap">
  <div class="sechead"><div><span class="eb lime"><i></i>REVIEWS</span><h2 class="h2 rv">&ldquo;내년에도 <span class="hl">꼭 와주세요</span>&rdquo;</h2></div></div>
  <div class="rvs">{rev}</div>
</div></section>

<section class="sec" id="notice"><div class="wrap two">
  <div><span class="eb"><i></i>NOTICE</span><h2 class="h2 rv">공지사항</h2><p class="lead rv">행사 일정과 새 소식을 가장 먼저 알려 드립니다.</p><div style="margin-top:26px">{btn("notice.html", "공지 전체 보기", "line sm")}</div></div>
  <ul class="notes rv d1" data-live="index" data-max="4" data-static='{NJ}'>{notes}</ul>
</div></section>
{cta_band()}
'''
    page('index.html', f'{NAME} | 즐거움을 기획하고 성장을 교육합니다', '즐거움을 기획하고 성장을 교육하는 행사·교육 전문 기관. 유치원·초등학교 운동회, 기업체 행사, 지자체 축제, 교회 행사부터 감정교육·리더십·진로교육까지.',
         body, 'index.html', extra_head=jsonld_biz() + '\n<link rel="preload" as="image" href="assets/img/hero-event.webp">')


# ════════════════════════ 회사 소개 ════════════════════════
def build_about():
    vals = [('01', '마음을 읽는 진행', '심리상담 전공 소장이 아이들의 반응을 읽고 현장 분위기를 이끕니다.', '#FA8A7A'),
            ('02', '20년 현장 경험', '교실, 체육관, 운동장, 대형 무대까지 수많은 현장에서 쌓은 노하우.', '#7DB55A'),
            ('03', '원스톱 운영', '기획, 진행, 장비, 음향 · 조명, 인력까지 한 곳에서 책임집니다.', '#F4A55A')]
    why = [('대상과 연령에 맞춘 맞춤 프로그램', ''), ('기관 일정과 공간에 맞춘 유연한 구성', ''), ('안전을 최우선으로 한 장비 운영과 인력 배치', ''),
           ('사전 상담 · 현장 답사', '행사 전에 공간과 인원을 확인하고 맞춤으로 기획합니다.'),
           ('우천 · 돌발 상황 대비', '날씨나 일정 변경에 맞춘 실내 대체 프로그램을 준비합니다.'),
           ('행사 후 현장 사진 제공', '행사가 끝나면 현장 사진을 정리해 보내드립니다.'),
           ('소장 직접 진행', '상담부터 현장 진행까지 소장이 직접 책임집니다.')]
    v = ''.join(f'<div class="val rv d{i + 1}" style="--c:{c}"><div class="no">{n}</div><h3>{t}</h3><p>{d}</p></div>' for i, (n, t, d, c) in enumerate(vals))
    w = ''.join(f'<li class="rv"><span class="ck">{CHECK}</span><div><b>{t}</b>{f"<span>{d}</span>" if d else ""}</div></li>' for t, d in why)
    body = phead('회사 소개', 'ABOUT', '즐거움을 기획하고,<br><span class="hl">성장을 교육</span>합니다',
                 f'{NAME}는 학교, 기업체, 기관, 교회까지 사람이 모이는 모든 곳에서 즐거움을 기획하고 성장을 교육하는 행사 · 교육 전문 기관입니다.') + f'''
<section class="sec"><div class="wrap two">
  <div class="rv"><span class="eb"><i></i>INTRO</span><h2 class="h2">사람이 모이는 자리에는<br>언제나 두 가지가 필요합니다</h2></div>
  <div class="prose rv d1">
    <p>함께 웃을 수 있는 <strong>즐거움</strong>, 그리고 무언가를 얻어 가는 <strong>배움</strong>입니다.</p>
    <p>{NAME}는 지난 20년 동안 학교 운동회와 축제, 기업체 체육대회와 송년회, 기관의 기념식과 지역 축제, 교회 행사까지 수많은 현장에서 즐거움을 기획해 왔습니다. 그리고 심리치료상담을 전공한 소장의 전문성을 바탕으로 감정교육, 리더십, 진로교육처럼 사람의 성장을 돕는 교육을 이어 왔습니다.</p>
    <p>행사로 마음을 모으고, 교육으로 사람을 키웁니다. 아이부터 어른까지, 학교부터 지역사회까지. 즐거움과 성장이 함께하는 현장을 만들겠습니다.</p>
  </div>
</div></section>

<section class="sec sand"><div class="wrap">
  <div class="sechead"><div><span class="eb lime"><i></i>VISION &amp; MISSION</span><h2 class="h2 rv">우리가 <span class="hl">바라보는 곳</span></h2></div></div>
  <div class="vm">
    <div class="bz rv"><div class="in" style="background:linear-gradient(160deg,#fff 45%,var(--coral-bg))"><span class="k">VISION</span><h3>다음세대가 행복한 세상</h3><p style="color:var(--soft)">아이들이 행복하려면 그 곁의 어른과 공동체가 함께 즐겁고 성장해야 합니다. 그래서 우리는 학교와 기업체, 기관, 교회까지 공동체의 모든 현장에서 함께합니다.</p></div></div>
    <div class="bz rv d1"><div class="in" style="background:linear-gradient(160deg,#fff 45%,var(--lime-bg))"><span class="k" style="color:var(--lime-ink)">MISSION</span><h3>즐거움과 성장이 함께하는 현장</h3><p style="color:var(--soft)">행사로 마음을 모으고, 교육으로 사람을 키워 즐거움과 성장이 함께하는 현장을 만듭니다.</p></div></div>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>CORE VALUES</span><h2 class="h2 rv">핵심 <span class="hl">가치</span></h2></div></div>
  <div class="vals">{v}</div>
</div></section>

<section class="sec sand"><div class="wrap">
  <div class="sechead"><div><span class="eb lime"><i></i>WHY US</span><h2 class="h2 rv">왜 <span class="hl">우리</span>인가요?</h2></div></div>
  <ul class="why">{w}</ul>
</div></section>

<section class="sec" id="map"><div class="wrap two">
  <div class="rv"><span class="eb"><i></i>LOCATION</span><h2 class="h2">오시는 길</h2><p class="lead">방문 상담은 미리 연락 주시면 시간을 맞춰 드립니다.</p></div>
  <div class="rv d1 side"><div class="card"><h3>{NAME}</h3><p>{ADDR}</p><p style="margin-top:6px">전화 <a href="tel:{TEL_RAW}">{TEL}</a></p><p>이메일 <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <div class="maplink">{btn(MAP, "네이버 지도로 보기", "line sm", True)}</div></div></div>
</div></section>
{cta_band()}
'''
    page('about.html', f'회사 소개 | {NAME}', f'{NAME} — 즐거움을 기획하고 성장을 교육하는 행사·교육 전문 기관. 비전, 미션, 핵심 가치, 오시는 길.', body, 'about.html')


# ════════════════════════ 대표 소개 ════════════════════════
def build_ceo():
    tl = ''.join(f'<li class="rv" style="--c:{c}"><div class="yr">{y}</div><h3>{t}</h3><p>{d}</p></li>' for y, c, t, d in TIMELINE)
    body = phead('<a href="about.html">회사 소개</a> › 대표 소개', 'CEO', '마음을 읽는 MC,<br><span class="hl">성장을 돕는 교육자</span>') + f'''
<section class="sec"><div class="wrap ceo">
  <div class="pic rv"><div class="arch"><img src="assets/img/ceo.webp" alt="이벤트와 교육연구소 소장 {CEO}" width="496" height="870"></div></div>
  <div class="letter rv d1" style="margin:0">
    <span class="eb"><i></i>GREETING</span>
    <div class="prose" style="margin-top:22px;font-size:17.5px">
      <p>안녕하세요. {NAME} 소장 <strong>{CEO}</strong>입니다.</p>
      <p>저는 지난 20년 동안 운동회와 레크리에이션, 매직쇼 무대에 서 왔습니다. 유치원 운동장부터 학교 축제, 기업 체육대회, 교회 행사와 지역 축제까지 사람들이 함께 웃는 현장이 저의 일터였습니다.</p>
      <p>무대에서 가장 많이 배운 것은 <strong>사람은 즐거울 때 마음을 연다</strong>는 사실입니다. 심리치료상담을 공부하며 그 마음을 더 깊이 이해하게 되었고, 즐거움이 배움과 성장으로 이어질 수 있다고 믿게 되었습니다. 그래서 행사와 함께 감정교육, 리더십, 진로교육을 이어가고 있습니다.</p>
      <p>{NAME}는 즐거움을 기획하고, 성장을 교육합니다. 행사로 마음을 모으고, 교육으로 사람을 키우는 일. 그 끝에 다음세대가 행복한 세상이 있다고 믿습니다.</p>
      <p>믿고 맡길 수 있는 행사, 오래 기억에 남는 교육으로 보답하겠습니다. 감사합니다.</p>
    </div>
    <p class="sign">{NAME} 소장 {CEO}</p>
  </div>
</div></section>

<section class="sec sand"><div class="wrap">
  <div class="sechead"><div><span class="eb lime"><i></i>CAREER</span><h2 class="h2 rv">이력</h2></div></div>
  <div class="cvgrid">
    <div class="cvbox rv"><h3>현재</h3><ul><li>{NAME} 소장</li><li>이벤트 PD · 레크리에이션 전문가</li><li>인천광역시 동구 · 서구 진로체험센터 전문강사</li></ul></div>
    <div class="cvbox l rv d1"><h3>학력</h3><ul><li>인하대학교 교육대학원 석사 (심리치료상담 전공)</li></ul></div>
    <div class="cvbox rv"><h3>주요 경력</h3><ul><li>전) 감정놀이연구소 인천지사 대표</li><li>전) 한국디지털융합진흥원 부설 글로벌AI메타버스개발원 부원장</li><li>전) 이벤트비전 수석실장 (이벤트 MC, 마술사)</li><li>전) 서울시립청소년직업체험센터 전문강사 (MC, 마술사)</li><li>전) 생각과 마음 상담&amp;코칭센타 놀이아동상담사</li></ul></div>
    <div class="cvbox l rv d1"><h3>저서 · 논문</h3><ul><li>저서 『메타버스, 즐기는 자가 먼저다』</li><li>논문 「감정놀이 프로그램이 유아의 정서지능에 미치는 영향」</li></ul></div>
  </div>
</div></section>

<section class="sec"><div class="wrap two">
  <div><span class="eb"><i></i>STORY</span><h2 class="h2 rv">운동장에서 보낸 <span class="hl">20년</span></h2>
    <figure class="rv" style="margin:28px 0 0"><img src="assets/img/story-2011.webp" alt="2011 위즈 한마음 체육대회 현장" loading="lazy" style="border-radius:24px;box-shadow:var(--shadow)"><figcaption style="font-size:14px;color:var(--soft);margin-top:10px">2011 위즈 한마음 체육대회</figcaption></figure></div>
  <ol class="tl">{tl}</ol>
</div></section>
{cta_band('소장과 직접 상담하세요', '상담부터 현장 진행까지 소장이 직접 책임집니다.')}
'''
    page('ceo.html', f'대표 소개 | {NAME} 소장 {CEO}', f'마음을 읽는 MC, 성장을 돕는 교육자. {NAME} 소장 {CEO}의 인사말과 이력 — 인하대학교 교육대학원 심리치료상담 전공, 20년 행사 진행 경력.', body, 'about.html')


# ════════════════════════ 행사 ════════════════════════
def build_event():
    tabs = ''.join(f'<a href="#{c["id"]}">{c["name"]}</a>' for c in EVENT_CATS)
    blocks = ''
    for i, c in enumerate(EVENT_CATS):
        if c['img']:
            ph = f'<div class="ph rv"><img src="assets/img/{c["img"]}.webp" alt="{esc(c["alt"])}" loading="lazy" decoding="async"></div>'
        else:
            ph = f'<div class="ph pending rv" style="background:linear-gradient(160deg,{c["c"]},#fff)"><div><img src="assets/img/logo-mark.png" alt="" style="width:84px;margin:0 auto 14px"><b style="font-size:18px;color:var(--ink)">축제 현장 사진을 준비하고 있어요</b><br>행사 사진이 정리되는 대로 이 자리에 실립니다.</div></div>'
        chips = ''.join(f'<li>{esc(p)}</li>' for p in c['prog'])
        ex = ''
        if c['id'] == 'kinder':
            ex = '''<div class="ex rv"><h4>프로그램 구성 예시 (명랑운동회)</h4><ol><li><b>10:00</b>개회식</li><li><b>10:20</b>준비운동</li><li><b>10:40</b>학년별 경기 · 놀이</li><li><b>…</b>실제 시간표는 기관 일정과 공간에 맞춰 함께 짭니다</li></ol></div>'''
        blocks += f'''<article class="cat" id="{c["id"]}">
  {ph}
  <div class="rv d1"><span class="no">0{i + 1}</span><h3>{c["title"]}</h3><p class="i"><b style="color:var(--ink)">{c["name"]}</b> — {c["intro"]}</p>
    <div class="plist"><h4>프로그램</h4><ul class="chips">{chips}</ul></div>{ex}
    <div style="margin-top:22px">{btn("contact.html?type=" + c["name"].replace(" ", "%20") + "#form", "이 행사 견적 문의", "coral")}</div></div>
</article>'''
    body = phead('행사', 'EVENT', '행사로<br><span class="hl">마음을 모읍니다</span>',
                 '학교 운동회와 축제부터 기업체 행사, 기관의 격식 있는 기념식과 지역 축제, 교회 행사까지. 대상과 목적에 꼭 맞는 행사를 기획하고 진행합니다. 진행 MC, 공연, 무대 · 음향 · 조명, 장비와 인력까지 한 번에 맡겨주세요.') + f'''
<section class="sec" style="padding-top:34px"><div class="wrap">
  <div class="tabs" aria-label="대상별 바로가기">{tabs}</div>
  {blocks}
</div></section>
<section class="sec sand"><div class="wrap two">
  <div><span class="eb lime"><i></i>HOW IT WORKS</span><h2 class="h2 rv">상담부터 <span class="hl">사진 전달</span>까지</h2></div>
  <ol class="why" style="grid-template-columns:1fr"><li class="rv"><span class="ck">{CHECK}</span><div><b>사전 상담 · 현장 답사</b><span>행사 전에 공간과 인원을 확인하고 맞춤으로 기획합니다.</span></div></li>
  <li class="rv"><span class="ck">{CHECK}</span><div><b>우천 · 돌발 상황 대비</b><span>날씨나 일정 변경에 맞춘 실내 대체 프로그램을 준비합니다.</span></div></li>
  <li class="rv"><span class="ck">{CHECK}</span><div><b>소장 직접 진행</b><span>상담부터 현장 진행까지 소장이 직접 책임집니다.</span></div></li>
  <li class="rv"><span class="ck">{CHECK}</span><div><b>행사 후 현장 사진 제공</b><span>행사가 끝나면 현장 사진을 정리해 보내드립니다.</span></div></li></ol>
</div></section>
{cta_band()}
'''
    page('event.html', f'행사 | 유치원·초등학교·기업체·지자체·교회 행사 기획 진행 | {NAME}', '유치원·어린이집 운동회, 초등학교 운동회·학교 축제, 기업체 체육대회·기념식, 지자체 축제, 교회 행사까지 대상별 맞춤 기획·진행. MC·공연·무대·음향·조명·장비·인력을 한 번에.', body, 'event.html')


# ════════════════════════ 교육 ════════════════════════
def build_edu():
    cards = ''.join(
        f'''<article class="edu rv d{i % 3 + 1}" style="--c:{e["c"]}"><div class="ic"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[e["ic"]]}</svg></div><h3>{e["n"]}</h3><span class="tg">대상 {e["who"]}</span><p>{e["t"]}</p><div class="fx"><span>기대효과</span>{e["fx"]}</div>{btn("contact.html?type=" + "교육" + "#form", "교육 문의", "line sm")}</article>'''
        for i, e in enumerate(EDU))
    body = phead('교육', 'EDUCATION', '교육으로<br><span class="hl-l">사람을 키웁니다</span>',
                 '심리치료상담을 전공한 소장이 직접 설계한 프로그램으로, 자신의 감정을 이해하고, 함께 소통하고, 스스로의 길을 찾아가도록 돕습니다. 즐거운 활동 속에서 배우기 때문에 오래 기억에 남습니다.') + f'''
<section class="sec"><div class="wrap">
  <div class="sechead"><div><span class="eb lime"><i></i>PROGRAMS</span><h2 class="h2 rv">교육 <span class="hl">프로그램</span> 6가지</h2></div></div>
  <div class="edugrid">{cards}</div>
</div></section>
<section class="sec dark"><div class="wrap">
  <span class="eb"><i></i>COURSE</span><h2 class="h2 rv">회차는 <span class="hl-l">필요에 맞게</span></h2>
  <p class="lead rv">기관 일정과 대상, 목적에 맞춰 구성합니다. 수업 시간과 적정 인원, 준비물과 장소 조건은 상담할 때 함께 정리해 드립니다.</p>
  <div class="steps3" style="margin-top:36px"><div class="rv"><b>1회 특강</b><p>한 번의 만남으로 핵심을 체험하는 특강 형태.</p></div><div class="rv d1"><b>4회 과정</b><p>한 달 동안 주 1회, 배운 것을 이어가는 과정.</p></div><div class="rv d2"><b>8회 과정</b><p>한 학기 동안 깊이 있게 다루는 정기 수업.</p></div></div>
  <div style="margin-top:34px">{btn("contact.html?type=교육#form", "교육 문의하기", "lime")}</div>
</div></section>
{cta_band('우리 기관에 맞는 교육이 궁금하세요?', '대상과 인원, 일정만 알려 주시면 가장 알맞은 프로그램을 제안해 드립니다.')}
'''
    page('education.html', f'교육 | 감정교육·임원 리더십·발표회·과학실험 마술수업·진로탐색 | {NAME}', '심리치료상담 전공 소장이 설계한 교육 프로그램 6가지 — 감정교육, 임원 리더십, 발표회, 과학실험 마술수업, 직업체험, 진로탐색 강의. 유아·초등·청소년 대상.', body, 'education.html')


# ════════════════════════ 포트폴리오 ════════════════════════
def build_portfolio():
    cats_with = {w[3] for w in WORKS}
    filt = ''.join(f'<button data-f="{k}" aria-pressed="{"true" if k == "all" else "false"}">{n}</button>' for k, n in PF_FILTERS if k == 'all' or k in cats_with)
    catname = dict((k, n) for k, n in PF_FILTERS)
    figs = ''.join(
        f'<figure data-c="{w[3]}" data-t="{esc(w[1])}"><div class="im"><img src="assets/img/{w[0]}.webp" alt="{esc(w[1])}" loading="lazy" decoding="async"></div><figcaption><b>{esc(w[1])}</b><span>{catname[w[3]]}{" · " + esc(w[2]) if w[2] else ""}</span></figcaption></figure>'
        for w in WORKS)
    regs = ''.join(
        f'<details class="rv"><summary>{esc(r["region"])}<small>{esc(r["count"])}</small></summary><ul>' + ''.join(f'<li>{esc(a)}<small>{esc(b)}</small></li>' for a, b in r['schools']) + '</ul></details>'
        for r in SCHOOLS)
    rev = ''.join(f'<figure class="rv d{i % 3 + 1}"><p>{t}</p><cite>{who}</cite></figure>' for i, (t, who) in enumerate(REVIEWS))
    rev += '<figure class="rv shot d2"><img src="assets/img/review-kakao.webp" alt="운동회를 마친 학교 선생님과 나눈 실제 카카오톡 대화" loading="lazy"></figure>'
    body = phead('포트폴리오', 'PORTFOLIO', '저희가 <span class="hl">다녀온</span> 행사',
                 '운동장에서 체육관, 무대까지. 현장에서 직접 찍은 사진과 학교 선생님들의 후기를 모았습니다.') + f'''
<section class="sec" style="padding-top:40px"><div class="wrap">
  <div class="filters" role="group" aria-label="분류">{filt}</div>
  <div class="pf">{figs}</div>
  <div class="empty" id="pfEmpty" hidden>이 분류의 사진을 준비하고 있어요.</div>
  <p class="lead" style="margin-top:26px">더 많은 현장 사진은 <a href="{NBLOG}" target="_blank" rel="noopener" style="color:var(--coral-ink);font-weight:700">네이버 블로그</a>에서 보실 수 있어요.</p>
</div></section>

<section class="sec sand" id="record"><div class="wrap">
  <div class="sechead"><div><span class="eb lime"><i></i>TRACK RECORD</span><h2 class="h2 rv">해마다 다시 <span class="hl">불러주시는</span> 학교들</h2></div>
    <p class="lead rv" style="margin:0">2011년부터 운동회를 맡겨주신 학교 94곳입니다. 숫자는 진행 연도예요.</p></div>
  <div class="regions">{regs}</div>
</div></section>

<section class="sec" id="reviews"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>REVIEWS</span><h2 class="h2 rv">선생님 · 학생 <span class="hl">후기</span></h2></div></div>
  <div class="rvs">{rev}</div>
</div></section>
{cta_band()}
'''
    page('portfolio.html', f'포트폴리오 | 운동회·체육대회·매직쇼 현장 | {NAME}', '유치원·어린이집·초등학교 운동회, 체육대회, 매직쇼, 기업체 행사 현장 사진과 학교 선생님 후기, 2011년부터 운동회를 맡긴 학교 94곳 실적.', body, 'portfolio.html')


# ════════════════════════ 견적 문의 ════════════════════════
def build_contact():
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    opts = ''.join(f'<option>{o}</option>' for o in ['유치원 · 어린이집 행사', '초등학교 운동회 · 행사', '기업체 · 기관 행사', '지자체 · 축제', '교회 행사', '교육 프로그램', '기타'])
    body = phead('견적 문의', 'CONTACT', '행사 날짜가 정해지셨나요?<br><span class="hl">지금 견적을 받아보세요</span>', '날짜 · 장소 · 인원만 알려 주시면 됩니다. 전화와 카카오톡으로도 바로 상담해 드립니다.') + f'''
<section class="sec" id="form" style="padding-top:40px"><div class="wrap cgrid">
  <div class="bz rv"><div class="in" style="padding:clamp(24px,4vw,44px)">
    <form class="f" id="qform" novalidate>
      <label>문의 종류<select name="type">{opts}</select></label>
      <div class="row"><label>담당자 성함 <em>*</em><input name="name" autocomplete="name" required></label><label>연락처 <em>*</em><input name="tel" type="tel" autocomplete="tel" placeholder="010-0000-0000" required></label></div>
      <div class="row"><label>기관 · 단체명<input name="org" autocomplete="organization"></label><label>이메일<input name="email" type="email" autocomplete="email"></label></div>
      <div class="row"><label>행사 날짜<input name="date" type="date"></label><label>예상 인원<input name="people" placeholder="예) 300명"></label></div>
      <label>장소<input name="place" placeholder="예) ○○초등학교 운동장"></label>
      <label>요청사항<textarea name="memo" placeholder="행사 성격, 원하는 프로그램, 예산 범위 등 알려주실 내용을 적어 주세요."></textarea></label>
      <input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
      <label class="agree"><input type="checkbox" name="agree"> 문의 답변을 위해 성함 · 연락처 · 문의 내용을 수집하며, 상담이 끝나면 파기하는 것에 동의합니다.</label>
      <div><button class="btn coral" type="submit">문의 보내기<span class="ar">{ARROW}</span></button></div>
    </form>
    <div class="done" id="qdone"><b>문의가 접수되었습니다.</b><br>확인 후 빠르게 연락드리겠습니다. 급하시면 전화 <a href="tel:{TEL_RAW}">{TEL}</a> 로 바로 연락 주세요.</div>
  </div></div>
  <aside class="side rv d1">
    <div class="card"><h3>전화 상담</h3><a class="big" href="tel:{TEL_RAW}">{TEL}</a><p style="color:var(--soft);font-size:15px;margin-top:4px">소장이 직접 상담합니다.</p></div>
    <div class="card"><h3>카카오톡 상담</h3><p style="color:var(--soft);font-size:15px;margin-bottom:12px">사진 · 자료를 함께 보내시기 편합니다.</p>{btn(KAKAO, "카카오톡 채널 열기", "lime sm", True)}</div>
    <div class="card"><h3>자동 견적서</h3><p style="color:var(--soft);font-size:15px;margin-bottom:12px">필요한 항목을 직접 골라 견적 요청서를 만들 수 있습니다.</p>{btn("quote.html", "자동 견적서 만들기", "line sm")}</div>
    <div class="card"><h3>오시는 길</h3><p style="font-size:15.5px">{ADDR}</p>{btn(MAP, "네이버 지도", "line sm", True)}</div>
  </aside>
</div></section>
<section class="sec sand"><div class="wrap two">
  <div><span class="eb lime"><i></i>FAQ</span><h2 class="h2 rv">자주 묻는 <span class="hl">질문</span></h2></div>
  <div class="faq rv d1">{faq}</div>
</div></section>
'''
    faqld = '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}, ensure_ascii=False) + '</script>'
    page('contact.html', f'견적 문의 | {NAME}', f'행사·교육 견적 문의 — 날짜·장소·인원만 알려 주세요. 전화 {TEL}, 카카오톡, 온라인 문의 모두 가능합니다.', body, 'contact.html', extra_head=faqld)


# ════════════════════════ 공지 ════════════════════════
def build_notice():
    rows = ''.join(
        f'<li id="n{i}"><div class="row"><time>{esc(n["d"])}</time><div><span class="t">{esc(n["t"])}{" <span class=new>NEW</span>" if n.get("n") else ""}</span>{f"<span class=d>{esc(n["b"])}</span>" if n.get("b") else ""}</div></div></li>'
        for i, n in enumerate(NOTICES))
    body = phead('공지사항', 'NOTICE', '새 소식과 <span class="hl">공지사항</span>', '행사 일정과 새 소식을 가장 먼저 알려 드립니다.') + f'''
<section class="sec" style="padding-top:30px"><div class="wrap" style="max-width:900px"><ul class="notes" data-live="page" data-static='{NJ}'>{rows}</ul></div></section>
{cta_band()}
'''
    page('notice.html', f'공지사항 | {NAME}', f'{NAME}의 새 소식과 공지사항.', body, '')


# ════════════════════════ 공지 관리자 ════════════════════════
def build_notice_admin():
    import re
    pd = open(os.path.join(ROOT, 'tools/port_docs.py'), encoding='utf-8').read()
    m = re.search(r"^GALLERY_URL\s*=\s*'([^']*)'", pd, re.M)
    gurl = m.group(1) if m else ''
    body = f"""<section class="phead" style="padding-bottom:50px"><div class="wrap"><span class="eb"><i></i>ADMIN</span><h1 style="font-size:clamp(30px,5vw,52px)">공지사항 관리</h1>
<p class="lead">공지를 쓰면 홈페이지 공지사항에 바로 올라갑니다(몇 분 안에). 사진 올리기와 같은 비밀번호를 씁니다.</p></div></section>
<section class="sec" style="padding-top:20px"><div class="wrap" style="max-width:900px">
<div id="setup" class="done on" hidden></div>
<form class="f" id="login" style="max-width:420px"><label>비밀번호<input type="password" id="pw" autocomplete="current-password"></label><div><button class="btn" type="submit">들어가기<span class="ar">{ARROW}</span></button></div><p id="lmsg" style="color:var(--coral-ink)"></p></form>
<div id="panel" hidden>
  <div class="bz"><div class="in" style="padding:clamp(20px,3vw,34px)">
  <form class="f" id="nf"><input type="hidden" id="nid">
    <div class="row"><label>날짜<input id="nd" placeholder="2026.10.20"></label><label>NEW 표시<select id="nn"><option value="1">표시함</option><option value="0">표시 안 함</option></select></label></div>
    <label>제목 <em>*</em><input id="nt" maxlength="120"></label>
    <label>내용 (선택)<textarea id="nb" maxlength="1500" placeholder="자세한 안내가 있으면 적어 주세요."></textarea></label>
    <div class="btns"><button class="btn coral" type="submit">저장하기<span class="ar">{ARROW}</span></button><button class="btn line" type="button" id="nreset">새로 쓰기<span class="ar">{ARROW}</span></button></div>
    <p id="nmsg" role="status"></p>
  </form></div></div>
  <h2 class="h2" style="font-size:26px;margin:40px 0 10px">올린 공지</h2>
  <ul class="notes" id="nlist"></ul>
</div>
</div></section>
<script>
(function(){{
  var SERVER = '{gurl}', KEY = 'edu-notice-pw';
  var $ = function(i){{ return document.getElementById(i); }};
  var pw = ''; try {{ pw = sessionStorage.getItem(KEY) || ''; }} catch(e) {{}}
  var list = [];
  function esc(t){{ return String(t==null?'':t).replace(/[&<>"]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c];}}); }}
  function call(body){{
    body.pw = pw;
    return fetch(SERVER, {{method:'POST', headers:{{'Content-Type':'text/plain;charset=utf-8'}}, body: JSON.stringify(body)}}).then(function(r){{return r.json();}});
  }}
  function today(){{ var d=new Date(); return d.getFullYear()+'.'+('0'+(d.getMonth()+1)).slice(-2)+'.'+('0'+d.getDate()).slice(-2); }}
  function reset(){{ $('nid').value=''; $('nd').value=today(); $('nt').value=''; $('nb').value=''; $('nn').value='1'; }}
  function draw(){{
    $('nlist').innerHTML = list.length ? list.map(function(n,i){{
      return '<li><div class="row" style="flex-wrap:wrap"><time>'+esc(n.d)+'</time><div style="flex:1;min-width:200px"><span class="t">'+esc(n.t)+(n.n?' <span class="new">NEW</span>':'')+'</span>'+(n.b?'<span class="d">'+esc(n.b)+'</span>':'')+'</div><span class="btns"><button class="btn sm line" data-e="'+i+'">수정</button><button class="btn sm" data-x="'+i+'">삭제</button></span></div></li>';
    }}).join('') : '<li><div class="row"><span class="t" style="color:var(--soft)">아직 이 화면으로 올린 공지가 없습니다. (처음 열 때 기본으로 보이는 공지는 홈페이지에 들어 있는 것입니다.)</span></div></li>';
  }}
  function open(){{
    $('login').hidden = true; $('panel').hidden = false; reset();
    call({{action:'notice-list'}}).then(function(j){{ if(j && j.ok){{ list=j.notices||[]; draw(); }} else {{ $('login').hidden=false; $('panel').hidden=true; $('lmsg').textContent=(j&&j.error)||'열 수 없습니다.'; }} }})
      .catch(function(){{ $('lmsg').textContent='서버에 연결하지 못했습니다.'; $('login').hidden=false; $('panel').hidden=true; }});
  }}
  if(!SERVER){{
    $('login').hidden = true;
    var s = $('setup'); s.hidden = false;
    s.innerHTML = '<b>아직 공지 서버가 연결되지 않았습니다.</b><br>큰길브리지가 사진 업로드 서버(apps-script/gallery)를 배포하고 주소를 넣으면 이 화면이 열립니다. 그 전에는 큰길브리지(1533-7295)에 공지 내용을 알려 주세요.';
  }}
  $('login').addEventListener('submit', function(e){{
    e.preventDefault(); pw = $('pw').value; if(!pw) return;
    try {{ sessionStorage.setItem(KEY, pw); }} catch(x) {{}}
    open();
  }});
  $('nf').addEventListener('submit', function(e){{
    e.preventDefault();
    var t = $('nt').value.trim(); if(!t){{ $('nmsg').textContent='제목을 적어 주세요.'; return; }}
    $('nmsg').textContent='저장하는 중…';
    call({{action:'notice-save', notice:{{id:$('nid').value, d:$('nd').value, t:t, b:$('nb').value, n:$('nn').value==='1'}}}})
      .then(function(j){{ if(j&&j.ok){{ list=j.notices; draw(); reset(); $('nmsg').textContent='저장했습니다. 홈페이지에는 몇 분 안에 보입니다.'; }} else $('nmsg').textContent=(j&&j.error)||'저장하지 못했습니다.'; }})
      .catch(function(){{ $('nmsg').textContent='서버에 연결하지 못했습니다.'; }});
  }});
  $('nreset').addEventListener('click', reset);
  $('nlist').addEventListener('click', function(e){{
    var b = e.target.closest('button'); if(!b) return;
    if(b.dataset.e){{ var n=list[+b.dataset.e]; $('nid').value=n.id; $('nd').value=n.d; $('nt').value=n.t; $('nb').value=n.b||''; $('nn').value=n.n?'1':'0'; scrollTo({{top:0,behavior:'smooth'}}); }}
    if(b.dataset.x && confirm('이 공지를 삭제할까요?')){{ var n2=list[+b.dataset.x]; call({{action:'notice-delete', id:n2.id}}).then(function(j){{ if(j&&j.ok){{ list=j.notices; draw(); }} else alert((j&&j.error)||'삭제하지 못했습니다.'); }}); }}
  }});
  if(SERVER && pw) open();
}})();
</script>"""
    page('notice-admin.html', f'공지사항 관리 | {NAME}', '공지사항 관리 화면', body, '', extra_head='<meta name="robots" content="noindex,nofollow">')


def build_404():
    body = f'''<section class="phead" style="min-height:70vh;display:grid;align-items:center"><div class="wrap"><span class="eb"><i></i>404</span><h1>페이지를 찾을 수 없어요</h1><p class="lead">주소가 바뀌었거나 없는 페이지입니다.</p><div style="margin-top:26px">{btn("index.html", "처음으로", "coral")}</div></div></section>'''
    page('404.html', f'페이지를 찾을 수 없습니다 | {NAME}', '페이지를 찾을 수 없습니다.', body, '')


# ════════════════════════ 사이트맵 · robots · llms ════════════════════════
def build_meta():
    pages = ['', 'about.html', 'ceo.html', 'event.html', 'education.html', 'portfolio.html', 'contact.html', 'notice.html', 'quote.html']
    today = datetime.date.today().isoformat()
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f'<url><loc>{BASE}/{p}</loc><lastmod>{today}</lastmod></url>\n' for p in pages) + '</urlset>\n'
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write(sm)
    rb = ('User-agent: *\nDisallow: /\n' if NOINDEX else
          'User-agent: *\nAllow: /\nDisallow: /contract.html\nDisallow: /statement.html\nDisallow: /office.html\nDisallow: /schedule.html\nDisallow: /upload.html\nDisallow: /notice-admin.html\n'
          'User-agent: GPTBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\n') + f'\nSitemap: {BASE}/sitemap.xml\n'
    open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8', newline='\n').write(rb)
    ll = f'''# {NAME} ({NAME_EN})

> 즐거움을 기획하고 성장을 교육하는 행사·교육 전문 기관. 학교·기업체·기관·교회 행사부터 감정교육·리더십·진로교육까지.

- 소장: {CEO} (이벤트 PD · 레크리에이션 전문가, 인하대학교 교육대학원 심리치료상담 석사)
- 주소: {ADDR}
- 전화: {TEL} · 이메일: {EMAIL}
- 블로그: {NBLOG}
- 활동 지역: 서울 · 인천 · 경기

## 행사 (대상별)
''' + ''.join(f'- {c["name"]}: {c["title"]} — 프로그램: {", ".join(c["prog"])}\n' for c in EVENT_CATS) + '\n## 교육\n' + ''.join(f'- {e["n"]} ({e["who"]}): {e["t"]} 기대효과: {e["fx"]}\n' for e in EDU) + f'''
## 페이지
- {BASE}/about.html 회사 소개 · 비전 · 핵심 가치
- {BASE}/ceo.html 대표 소개
- {BASE}/event.html 행사
- {BASE}/education.html 교육
- {BASE}/portfolio.html 포트폴리오 · 후기 · 운동회 실적 학교 94곳
- {BASE}/contact.html 견적 문의
'''
    open(os.path.join(ROOT, 'llms.txt'), 'w', encoding='utf-8', newline='\n').write(ll)


if __name__ == '__main__':
    build_index(); build_about(); build_ceo(); build_event(); build_edu(); build_portfolio(); build_contact(); build_notice(); build_notice_admin(); build_404(); build_meta()
