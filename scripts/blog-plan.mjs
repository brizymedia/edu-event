/** 아직 안 쓴 블로그 주제 보기:  node scripts/blog-plan.mjs  (주제 목록은 _blog/keywords.json) */
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { 글읽기 } from './build-blog.mjs';
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const 주제 = JSON.parse(readFileSync(resolve(ROOT, '_blog', 'keywords.json'), 'utf8')).주제;
const 쓴 = new Set(글읽기(ROOT).map((p) => p.topic));
const 남음 = 주제.filter((t) => !쓴.has(t.topic));
console.log(남음.length ? `아직 안 쓴 주제 ${남음.length}개` : '모든 주제를 썼습니다 — keywords.json 에 새 주제를 추가하세요');
남음.forEach((t) => console.log(`- [${t.category}] ${t.topic}: ${t.k}  (${t.s.join(' · ')})`));
