# -*- coding: utf-8 -*-
"""
블로그(scripts/build-blog.mjs)가 쓰는 사이트 공통 조각을 JSON 으로 내보낸다.

  python tools/blog_shell.py

BASE · NOINDEX · 머리글 · 바닥글 · 상담 띠는 tools/build_site.py 의 것을 그대로 쓴다(한 곳에서만 고친다).
build_site 를 import 해도 페이지는 다시 쓰이지 않는다(쓰기는 __main__ 에서만).
머리글 · 바닥글의 상대 주소(about.html …)는 앞에 @@R@@ 표시를 붙여 내보낸다. 블로그 빌더가 쪽 깊이에 맞는 ../ 로 바꾼다
(상대 주소라야 로컬 미리보기 · GitHub Pages 하위 경로 · 나중의 자체 도메인 어디서나 맞는다).
"""
import sys, os, re, json
from urllib.parse import urlparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_site as b

base_path = urlparse(b.BASE).path.rstrip('/')


def absolutize(h):
    def fix(m):
        attr, v = m.group(1), m.group(2)
        if re.match(r'^(https?:|tel:|mailto:|data:|#|/)', v):
            return m.group(0)
        return f'{attr}="@@R@@{v}"'
    return re.sub(r'\b(href|src)="([^"]*)"', fix, h)


out = {
    'base': b.BASE.rstrip('/'), 'basePath': base_path, 'noindex': bool(b.NOINDEX), 'ver': b.VER,
    'name': b.NAME, 'nameEn': b.NAME_EN, 'tel': b.TEL, 'email': b.EMAIL, 'nblog': b.NBLOG, 'ogImage': b.OG,
    'header': absolutize(b.header('blog/index.html')),
    'footer': absolutize(b.footer()),
    'cta': absolutize(b.cta_band('행사 · 교육 상담이 필요하신가요?', '날짜 · 장소 · 인원만 알려 주시면 됩니다.')),
}
sys.stdout.buffer.write(json.dumps(out, ensure_ascii=False).encode('utf-8'))
