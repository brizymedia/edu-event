/*
 * 이벤트와 교육연구소 — 견적 품목표와 견적 코드 읽기
 *
 * quote.html 과 schedule.html 이 함께 쓴다. 품목을 고칠 곳은 여기 하나뿐이다.
 * 견적서에는 서버가 없다 — 견적 하나가 주소 뒤 #q= 에 담기는 짧은 코드 하나다.
 * 그 코드를 푸는 규칙도 여기 둔다(두 화면이 같은 규칙으로 읽어야 하니까).
 */

const CATALOG = [
  { group:'행사 진행', items:[
    { id:'p1', name:'유치원 · 어린이집 행사',  spec:'명랑운동회 · 어린이날 체험부스 · 레크리에이션', unit:'식', price:null },
    { id:'p2', name:'초등학교 운동회 · 체육대회', spec:'학년별 종목 구성 · 진행 · 음향',           unit:'식', price:null },
    { id:'p3', name:'학교 축제 · 학예회',      spec:'진행 · 에어바운스 · 음향 · 조명',            unit:'식', price:null },
    { id:'p4', name:'기업체 · 기관 행사',      spec:'체육대회 · 팀빌딩 · 송년회 · 신년회',        unit:'식', price:null },
    { id:'p5', name:'기념식 · 시상식 · 이취임식', spec:'큐시트 · 의전 연출 · 전문 MC',            unit:'식', price:null },
    { id:'p6', name:'기공식 · 준공식 · 오픈식', spec:'시삽 · 테이프 커팅 · 축하 연출',             unit:'식', price:null },
    { id:'p7', name:'지자체 · 지역축제',       spec:'무대 · 공연 운영 · 체험부스 · 현장 스태프',  unit:'식', price:null },
    { id:'p8', name:'교회 행사',               spec:'체육대회 · 여름성경학교 · 성탄 · 어린이주일', unit:'식', price:null },
  ]},
  { group:'공연', items:[
    { id:'s1', name:'매직쇼',   spec:'30~40분 참여형 공연', unit:'회', price:null },
    { id:'s2', name:'버블쇼',   spec:'30~40분 공연 · 실내 · 실외', unit:'회', price:null },
    { id:'s3', name:'버블 + 매직 합동공연', spec:'60분 내외', unit:'회', price:null },
  ]},
  { group:'체험 · 놀이', items:[
    { id:'h1', name:'에어바운스',        spec:'공기주입식 놀이기구', unit:'동', price:null, qty:true },
    { id:'h2', name:'체험 부스',         spec:'만들기 · 놀이 체험 · 운영 인력 포함', unit:'동', price:null, qty:true },
    { id:'h3', name:'체육대회 게임도구', spec:'명랑운동회 · 팀빌딩 종목', unit:'식', price:null },
    { id:'h4', name:'레크리에이션 진행', spec:'단체 게임 · 응원전 · 댄스', unit:'식', price:null },
  ]},
  { group:'교육 프로그램', items:[
    { id:'e1', name:'감정교육',          spec:'유아 · 초등 · 놀이로 배우는 마음 읽기', unit:'회', price:null, qty:true },
    { id:'e2', name:'임원 리더십',       spec:'초등 · 청소년 · 소통 · 책임감 · 협력', unit:'회', price:null, qty:true },
    { id:'e3', name:'발표회 수업',       spec:'초등 · 청소년 · 발표력 · 자기표현',   unit:'회', price:null, qty:true },
    { id:'e4', name:'과학실험 마술수업', spec:'유치부 · 초등부 · 실험으로 배우는 과학', unit:'회', price:null, qty:true },
    { id:'e5', name:'직업체험',          spec:'초중고 · 직업 이해 · 진로 동기',       unit:'회', price:null, qty:true },
    { id:'e6', name:'진로탐색 강의',     spec:'초중고 · 흥미와 강점 발견',           unit:'회', price:null, qty:true },
  ]},
  { group:'음향 · 조명 · 장비', items:[
    { id:'a1', name:'음향 (소형)',       spec:'교실 · 강당 · 소규모 행사',     unit:'식', price:null },
    { id:'a2', name:'음향 (중형)',       spec:'체육관 · 운동장',               unit:'식', price:null },
    { id:'a3', name:'음향 (대형)',       spec:'야외 축제급',                   unit:'식', price:null },
    { id:'a4', name:'무선 마이크 추가',  spec:'핸드 / 핀 마이크',              unit:'개', price:null, qty:true },
    { id:'b1', name:'무대 · 조명',       spec:'크기 · 높이는 현장에 맞게',     unit:'식', price:null },
    { id:'b2', name:'LED 전광판',        spec:'실내외 · 크기 협의',            unit:'식', price:null },
    { id:'d3', name:'천막',              spec:'설치 · 철수',                   unit:'동', price:null, qty:true },
    { id:'d9', name:'테이블 · 의자',     spec:'행사 인원에 맞춰',              unit:'세트', price:null, qty:true },
  ]},
  { group:'MC · 섭외', items:[
    { id:'f1', name:'전문 MC · 사회자',  spec:'행사 성격에 맞춘 진행자',       unit:'명', price:null },
    { id:'f2', name:'가수 · 공연팀 섭외', spec:'트로트 · 대중가수 · 밴드',     unit:'팀', price:null },
    { id:'f5', name:'진행 스태프',       spec:'현장 안내 · 진행 보조',         unit:'명', price:null, qty:true },
  ]},
  { group:'기타', items:[
    { id:'g4', name:'사진 · 영상 기록',  spec:'행사 현장 촬영 · 전달',         unit:'식', price:null },
    { id:'g2', name:'운반 · 설치 인건비', spec:'상하차 · 설치 · 철수',         unit:'식', price:null },
    { id:'g3', name:'출장비',            spec:'인천 · 서울 · 경기 외 지역',    unit:'식', price:null },
  ]},
];
const BY_ID = {};
CATALOG.forEach(g => g.items.forEach(it => { BY_ID[it.id] = it; }));

const 견적정보칸 = ['org','name','tel','email','title','date','place','people','memo'];
const 견적정보짧게 = { org:'o', name:'n', tel:'t', email:'e', title:'m', date:'d', place:'p', people:'c', memo:'x' };

const 견적b64u   = (s) => btoa(unescape(encodeURIComponent(s))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const 견적unb64u = (s) => {
  let t = String(s).replace(/-/g, '+').replace(/_/g, '/');
  while (t.length % 4) t += '=';
  return decodeURIComponent(escape(atob(t)));
};

/**
 * 견적 코드를 사람이 읽을 수 있는 모양으로 푼다.
 *   { 정보:{org,name,tel,…}, 줄:[{id,name,spec,qty,unit,days,price}], 할인 }
 * 못 읽으면 null.
 */
function 견적풀기(코드) {
  try {
    const s = JSON.parse(견적unb64u(코드));
    const 정보 = {};
    견적정보칸.forEach((k, idx) => {
      const i = s.i;
      if (!i) { 정보[k] = ''; return; }
      const v = Array.isArray(i) ? i[idx]
              : (i[견적정보짧게[k]] != null ? i[견적정보짧게[k]] : i[k]);
      정보[k] = v == null ? '' : String(v);
    });

    const 책 = (id) => BY_ID[id] || { name: '', spec: '', unit: '식' };
    const 줄 = (s.r || []).map((a) => {
      if (typeof a === 'string') {
        const c = 책(a);
        return { id: a, name: c.name, spec: c.spec, qty: 1, unit: c.unit, days: 1, price: null };
      }
      if (a.length <= 4) {
        const c = 책(a[0]);
        return { id: a[0], name: c.name, spec: c.spec,
                 qty: a[1] != null ? a[1] : 1, unit: c.unit,
                 days: a[2] != null ? a[2] : 1,
                 price: a[3] != null ? a[3] : null };
      }
      return { id: a[0], name: a[1], spec: a[2], qty: a[3], unit: a[4], days: a[5], price: a[6] };
    });

    return { 정보: 정보, 줄: 줄, 할인: +s.d || 0, 총액: +s.t || 0, 부가세: s.x === 'p' ? '포함' : '별도' };
  } catch (e) { return null; }
}

/* 견적 한 줄을 「300명 내외 · 스피커 4통 · 2개 · 2일」 같은 한 줄 설명으로 */
function 견적줄설명(r) {
  return [r.spec, (+r.qty > 1 ? r.qty + (r.unit || '') : ''), (+r.days > 1 ? r.days + '일' : '')]
    .filter(Boolean).join(' · ');
}
