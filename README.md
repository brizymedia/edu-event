# 이벤트와 교육연구소 홈페이지

큰길브리지 계약 **KB-20261009-273** (회사형 · 1,100,000원 부가세 포함, 2026-10-10 서명, 오픈 예정 2026-10-20) 납품물.
콘텐츠 기획안(`Desktop\큰길브리지\이벤트와교육연구소\이벤트와 교육연구소 홈페이지 콘텐츠 기획안.docx`)의 사이트 구조 · 문구를 그대로 옮겼다.
서버 없이 정적 파일로 돈다(문의 · 공지 · 사진 업로드만 구글 앱스 스크립트).

```
index.html       대문: 히어로(행사|교육 2분할 + 가운데 로고 아치) → 숫자 → 두 개의 파트 → 대상별 5 → 대표 요약 → 갤러리 6 → 후기 3 → 공지 → 문의
about.html       회사 소개 (소개문 · 비전 · 미션 · 핵심 가치 3 · 왜 우리인가요 7 · 오시는 길)
ceo.html         대표 소개 (인사말 · 이력 · 운동장에서 보낸 20년)
event.html       행사 5개 대상(유치원·어린이집 / 초등학교 / 기업체·기관 / 지자체·축제 / 교회) — 타이틀 · 소개문 · 프로그램 · 견적 문의 단추
education.html   교육 6개(감정교육 · 임원 리더십 · 발표회 · 과학실험 마술수업 · 직업체험 · 진로탐색 강의) — 대상 · 소개문 · 기대효과
portfolio.html   분류 필터 + 현장 사진 + 운동회 실적 학교 94곳(지역별) + 후기(카톡 캡처 포함)
contact.html     견적 문의 폼 + 전화 · 카카오톡 · 자동 견적서 · 오시는 길 + FAQ(FAQPage)
notice.html      공지사항 · notice-admin.html 공지 관리자(서버 연결 뒤)
quote · contract · statement · schedule · upload · office .html   업무 도구(큰길이벤트 원본에서 이식, `tools/port_docs.py`)
assets/          style.css · app.js · edit.js(사장님 직접 수정) · img/ · data/(schools.json · notices.json)
tools/           build_site.py(페이지 생성) · port_docs.py(업무 도구 이식) · apply_edits.py(사장님 수정 반영) · admin_gate.py
apps-script/     contract(전자계약 서버) · gallery(사진 업로드 + 공지 서버) — 형님 구글 계정으로 배포
```

## 보기

```
python -m http.server 8820 --directory C:/Users/gilau/Documents/edu-event
```
→ http://localhost:8820 (`.claude/launch.json` 의 `edu-event`). `file://` 로 열면 글꼴 · 스크립트가 안 나온다.

## 고치는 법 (중요)

- 페이지 HTML(`index · about · ceo · event · education · portfolio · contact · notice · notice-admin · 404`)과 sitemap · robots · llms.txt 는 **`python tools/build_site.py` 가 만든다.** 글 · 사진 목록은 그 파일 맨 위(`회사 정보` · `자료`)에서 고치고 다시 돌린다.
- 업무 도구 HTML(`quote · contract · statement · schedule · upload · office`)은 `python tools/port_docs.py` 가 만든다. 회사 설정은 그 파일 맨 위.
- **사장님이 직접 수정 모드(`?edit=열쇠`)로 고친 내용을 `tools/apply_edits.py` 로 HTML 에 반영한 뒤에는 build_site.py 를 다시 돌리면 그 수정이 덮어써진다.** 그때부터는 HTML 을 원본으로 보고, 새 글 · 사진은 HTML 에서 고치거나 반영한 내용을 build_site.py 에도 같이 옮길 것.
- 공지사항: 서버 연결 전에는 `assets/data/notices.json` 을 고치고 build_site.py. 연결 뒤에는 `notice-admin.html` 에서 대표님이 직접(비밀번호 = 사진 올리기 비밀번호).

## 회사 정보 (계약서 · 기존 시안 기준)

- 상호 이벤트와 교육연구소 · 대표(소장) 황윤수 · 사업자등록번호 578-03-01411 · 인천광역시 남동구 문화서로 62번길 17, 3층 302호
- 계약 담당(서명자) 김필선 010-6342-5309 · filsun@naver.com
- **사이트에 넣은 전화 010-9189-5589 · 메일 ihahanara@gmail.com 은 기존 시안(`index.html`)에 있던 대표 번호 · 메일이다.** 계약서의 담당자 번호와 다르니 대표 확인 필요.
- 카카오톡 채널 pf.kakao.com/_XVrSs · 네이버 블로그 blog.naver.com/event_edu (기존 시안 기준)
- 로고 2종(아치형 · 가로형)은 받은 PNG 를 `assets/img/logo-arch.png` · `logo-h.png` 로 변환. 웃는 얼굴 마크는 가로형에서 잘라 `favicon.png` · `logo-mark.png`. 어두운 바탕용 `logo-h-white.png`.

## 납품 전에 꼭 확인할 것 (황윤수 소장 · 김필선 담당에게 물어볼 것)

1. **사진.** 2026-10-25 대표님이 폴더별로 보낸 사진 87장 + 영상 6개를 반영했다(`카카오톡 받은 파일/이벤트와교육연구소`: 초등학교 운동회 29 · 교회 체육대회 23 · 과학수업 12(+영상 5) · 마술공연 8(+영상 1) · 대학축제 6 · 관공서 체육대회 5 · 기업 레크리에이션 4).
   - 변환본은 `assets/img/p/<접두어>NN.webp`(긴 변 1400px), 영상은 `assets/video/`(+첫 화면 jpg). 포트폴리오 분류 · 순서는 `build_site.py` 의 `PHOTO_SETS` · `WORKS`. 원본 사진이 카톡 압축본(1280px)이라 히어로는 약간 부드럽다 — 원본 파일을 받으면 `hero-event.webp` · `hero-edu.webp` 교체.
   - 「교회 체육대회」 폴더 사진은 학교 운동장에서 열린 「전교인 명랑운동회」다(현수막 · 건물 이름이 사진에 보임). 폴더 이름대로 교회로 분류했고 캡션에 학교 이름은 쓰지 않았다.
   - 아이들 얼굴이 나오는 사진이 많다. 학교 · 학부모 공개 동의 여부를 대표님께 확인(일부는 이미 모자이크됨).
   - 「지자체 · 축제」 분류에는 대학 축제 사진 6장만 있다. 교육 사진은 과학수업(과학실험 마술수업)뿐 — 감정교육 · 리더십 등 다른 수업 사진은 아직 없다.
   - 기존 시안 사진 10장(`g01~g10`)은 그대로 두고 분류를 여러 개(예: 유치원 + 마술)로 달았다. 「성탄 축하 행사 매직쇼」를 교회로 분류한 것은 짐작이니 확인.
2. **숫자.** 대문 「20년」 · 「94곳」은 기존 시안의 학교 목록(`assets/data/schools.json`)과 이력 기준이다. 기획안의 「누적 행사 ○○회 · 함께한 기관 ○○곳」은 수치를 받지 못해 쓰지 않았다.
3. **후기 4개**와 카톡 캡처는 기존 시안의 것이다. 대표가 공개에 동의한 것인지, 학교 · 개인 정보가 가려졌는지 확인(카톡 캡처 `review-kakao.webp` 에 이름 · 사진이 보이지 않는지 한 번 더 확인).
4. **교회 프로그램**(기획안이 「실제 운영 프로그램으로 조정 필요」라 적은 곳) — 체육대회 · 여름성경학교 레크리에이션 · 성탄 · 어린이주일 행사 · 버블쇼 · 매직쇼를 그대로 넣었다.
5. **교육 상세**(회차 1회 / 4회 / 8회 구성, 수업 시간 · 적정 인원 · 준비물)는 기획안이 「업체 전달용 공통 항목」으로만 적어 두었고 내용이 없다. 지금은 회차 구성 안내만 넣었다.
6. **행사 상세**(프로그램 시간표 · 진행 인원 · 소요 시간)도 같다. 유치원 쪽에 기획안의 예시(10:00 개회식 → 10:20 준비운동)만 「구성 예시」로 넣었다.
7. **직인.** 대표 인감 PNG 를 `assets/img/stamp-edu.png` 로 넣으면 견적서 · 계약서 · 명세서에 찍힌다(없으면 「(인)」).
8. **입금 계좌 · 사업자 계좌**는 큰길브리지 기본값이 아니라 이 회사용으로 비워 두었다(`port_docs.py`). 대표 계좌를 받으면 넣는다.

## 오픈할 때 바꿀 것

1. 도메인: 계약 「오픈 시점에 협의」. 정해지면 `build_site.py` 의 `BASE` · `port_docs.py` 의 `HOME` 을 바꾸고 두 스크립트를 다시 실행 → CNAME 파일은 **DNS 가 살아난 뒤에** 커밋.
2. `NOINDEX = True` 를 `False` 로 바꾸고 build_site.py 재실행 → robots · 메타 noindex 가 풀린다(지금은 검색 차단 상태).
3. 레포 `brizymedia/edu-event` 만들기 → 푸시 → Pages(main 루트). **photos 고아 가지**(빈 `photos/photos.json` · `photos/notices.json`)를 같이 만들어 둔다(es-company 방식).
4. 서버 두 개 배포(형님 구글 계정): `apps-script/contract`(전자계약 · 견적서 저장함 · 관리자 암호) · `apps-script/gallery`(사진 업로드 + 공지). 각 README 참고. 배포 뒤 `/exec` 주소를 `tools/port_docs.py` 의 `CONTRACT_URL` · `GALLERY_URL` 에 넣고 `python tools/port_docs.py` 와 `python tools/build_site.py`. **그 전에는 관리자 화면(?admin=1)이 잠기지 않고 office.html 은 열리지 않는다.**
5. 문의 서버(`ai-make/문의폼-AppsScript-코드.gs`)에 이벤트와 교육연구소 수신 주소(대표 메일) 추가 — 지금은 문의가 큰길브리지 메일로만 간다.
6. 유입 현황판(`stats.js` data-site="edu")에 사이트 추가 — 현황판 쪽 SITE 목록.
7. 네이버 서치어드바이저 · 구글 서치콘솔 등록(소유 확인 태그를 받아 `<head>` 에 넣고 sitemap 제출). **build_site.py 가 `<head>` 를 새로 쓰므로 소유 확인 태그는 `EDIT_META` 옆에 넣어 둘 것.**

## 계약 항목 점검 (KB-20261009-273)

| 항목 | 상태 |
|---|---|
| 회사형 홈페이지 · 10페이지 구성 | ✅ 대문 · 회사소개 · 대표 · 행사 · 교육 · 포트폴리오 · 견적문의 · 공지 · 공지관리 + 블로그 |
| 브랜드 컨설팅 · 로고 리터치 | ✅ 받은 로고 PNG 를 웹용으로 변환(가로 · 아치 · 마크 · 흰색판). 로고 원본(.ai)은 받지 못함 |
| 공지 · 게시판 관리자 페이지 | ✅ `notice-admin.html` — 서버(gallery) 배포 뒤 작동 |
| 직접 수정 가능한 CMS 세팅 + 교육 | ✅ `?edit=열쇠` 글 · 사진 수정 모드(es-company 방식). 열쇠는 문자로 따로 |
| 도메인 등록 + 연결 | ⏳ 도메인 미정 |
| 갤러리 + 인스타 · 블로그 자동 연동 | ✅ `upload.html`(사진 올리기 + 블로그 · 인스타 글 자동 작성) — 서버 배포 뒤 |
| 네이버 · 구글 AI 검색 세팅 | ✅ 사이트맵 · llms.txt · JSON-LD(LocalBusiness · FAQPage) · robots / ⏳ 소유 확인 · 등록은 도메인 뒤 |
| 자동 계약서 작성 · 서명 | ✅ `contract.html` — 서버(contract) 배포 뒤 짧은 링크 |
| AI 검색 최적화 (블로그글 10개) | `blog/` 참고(아래) |
| 3D 무대시안 만들기 | ⏳ 이 폴더 밖 — 큰길이벤트.com/stage3d 서비스에서 따로 진행 |
| 모바일 명함 + 콜백 문자 | ⏳ 이 폴더 밖 — 큰길브리지 명함 만들기(ai-make.co.kr/card/)에서 따로 |
| 1개월 무상 유지보수 · 월 관리비 5만원(제9조) · 매월 블로그 홍보기사 10회 · AI 마케팅 강의 영상 | 운영 항목(사이트 밖) |
