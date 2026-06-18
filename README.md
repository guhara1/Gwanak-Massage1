# 바로GO — 관악 출장마사지·관악구 홈타이 안내 사이트

서울 관악구 전지역 방문 관리(출장마사지·홈타이) 안내용 정적 사이트입니다.
예약전화: **0508-202-4719**

## 구조

- 정적 HTML 사이트 — 어느 호스팅(GitHub Pages, Netlify, 일반 웹서버)에서든 그대로 서빙 가능
- `build.py` + `content/` 패키지에서 페이지를 생성하는 빌드 방식
- 생성물(각 디렉터리의 `index.html`, `sitemap.xml`, `robots.txt`)도 저장소에 포함

```
build.py            # 빌드 스크립트 (레이아웃·글자수 검사·WebPage/BreadcrumbList JSON-LD·sitemap)
content/
  site.py           # 상호(바로GO)·전화·BASE_URL·메뉴 구조
  main.py           # 메인 페이지 (+ Organization/FAQPage JSON-LD, LocalBusiness 미사용)
  areas.py          # 권역 허브: 관악구 전지역(/gwanak/) + 봉천권·신림권·남현권
  dongs_bongcheon.py# 봉천권 행정동 9개
  dongs_sillim.py   # 신림권 행정동 11개
  dongs_namhyeon.py # 남현권 행정동(남현동) 1개
  stations.py       # 역세권: 2호선·신림선 10개 역
  livingareas.py    # 생활권·주요 거점 10개
  themes.py         # 테마별: 허브 + 14개 테마
  info.py           # 출장마사지 안내·코스·예약·가이드·후기·고객센터·약관
  magazine.py       # 매거진 글 6편 + 허브
  about.py          # 운영자 소개(E-E-A-T)
assets/             # CSS(프리미엄 팔레트·Pretendard), 모바일 내비 JS
```

## 빌드

```bash
python3 build.py
```

빌드 시 페이지별 본문 글자수 리포트가 출력됩니다.

## SEO 운영 원칙 (빌드에 강제됨)

- 본문 **2,000자 미만 페이지는 자동 `noindex`** 처리되고 sitemap에서 제외
- 지역은 봉천권·신림권·남현권 권역 + 21개 행정동으로 구성, 권역이 중간 허브 역할
- 역은 역 1개당 페이지 1개 — 신림역 등 환승역도 URL 하나, 노선별·출구별 페이지 없음
- 사당역·보라매역처럼 행정구역 경계가 애매한 역은 단독 페이지 대신 인접 생활권 본문에서 보조 설명
- **지역+역+테마 조합 페이지 없음** (도어웨이 방지) — 테마는 독립 페이지로만 운영
- 실제 오프라인 사업장 주소가 없는 방문형 사이트이므로 **LocalBusiness Schema 미사용** (Organization·WebPage·BreadcrumbList 사용)
- 상단/하위 메뉴와 푸터에 키워드·지역명·역명 대량 나열 없음
- 모든 페이지 본문은 페이지별 고유 작성 (지역명만 바꾼 복붙 없음 = scaled content abuse 회피)

## 배포 전 해야 할 일

1. `content/site.py`의 `BASE_URL`을 실제 도메인으로 변경
2. `python3 build.py` 재실행 (canonical·sitemap·robots.txt에 반영됨)
3. Google Search Console에 `sitemap.xml` 제출
