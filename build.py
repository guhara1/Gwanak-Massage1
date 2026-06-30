#!/usr/bin/env python3
"""노원 블랙 마사지 — 정적 사이트 빌드 스크립트.

content/ 패키지의 페이지 정의를 읽어 정적 HTML을 생성한다.

규칙(자동 적용):
  - 본문 텍스트 2,000자 미만 페이지는 robots noindex 처리
  - sitemap.xml 에는 index 허용 페이지만 포함
  - 지역+역+테마 조합 경로는 생성 자체가 불가능한 구조
"""
import datetime
import html
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content import (PAGES, areas, dongs_bongcheon, dongs_sillim,
                     dongs_namhyeon, stations, livingareas, themes)
from content.site import (BASE_URL, BRAND, BRAND_MARK, INDEXNOW_KEY, NAV,
                          PHONE, PHONE_DISPLAY, REGION, REGION_FULL)
from content.reviews_data import (REVIEWS, AGG_VALUE, AGG_COUNT, AGG_BEST,
                                  AGG_WORST)

ROOT = os.path.dirname(os.path.abspath(__file__))
MIN_INDEX_CHARS = 2000

# ── 내부 링크 인벤토리 ─────────────────────────────────────────
# 지역·역·생활권·테마 페이지 묶음을 모듈별로 가져와 롱테일 앵커 링크를 만든다.
DONG_PAGES = dongs_bongcheon.PAGES + dongs_sillim.PAGES + dongs_namhyeon.PAGES
STATION_PAGES = stations.PAGES
LIVING_PAGES = livingareas.PAGES
THEME_PAGES = [p for p in themes.PAGES if p["path"] != "themes/"]
AREA_PAGES = [p for p in areas.PAGES if p["path"] != "gwanak/"]


def _label(page: dict) -> str:
    bc = page.get("breadcrumb") or []
    if bc and bc[-1][0]:
        return bc[-1][0]
    return page["h1"]


def _links(pages, suffix):
    """(href, 롱테일 앵커) 목록. 앵커 = 지역/역/테마명 + 주제어."""
    return [("/" + p["path"], f'{_label(p)} {suffix}'.strip()) for p in pages]


def _ul(pairs, cls="link-cloud"):
    lis = "".join(f'<li><a href="{h}">{a}</a></li>' for h, a in pairs)
    return f'<ul class="{cls}">{lis}</ul>'


def homepage_link_index() -> str:
    """메인 페이지에 싣는 전체 지역·역·생활권·테마 내부 링크 허브."""
    return (
        '<section id="area-index">'
        "<h2>관악구 동네별·역세권별·테마별 상세 안내</h2>"
        "<p>찾으시는 동네, 지하철역, 생활권, 관리 테마를 바로 선택하실 수 있도록 모든 안내 페이지를 한곳에 모았습니다. "
        "각 페이지는 해당 지역의 생활권 특징과 방문 조건, 도착 기준을 고유한 내용으로 설명합니다.</p>"
        "<h3>행정동별 출장마사지 안내</h3>" + _ul(_links(DONG_PAGES, "출장마사지")) +
        "<h3>지하철역별 출장마사지 안내</h3>" + _ul(_links(STATION_PAGES, "출장마사지")) +
        "<h3>생활권·주요 거점별 홈타이 안내</h3>" + _ul(_links(LIVING_PAGES, "홈타이")) +
        "<h3>테마별 관리 안내</h3>" + _ul(_links(THEME_PAGES, "마사지")) +
        "</section>"
    )


def related_block(path: str, idx: int) -> str:
    """지역·테마 상세 페이지마다 다른 조합으로 다는 '주변 지역·관련 안내' 내부 링크."""
    pool = (_links(AREA_PAGES, "출장마사지") + _links(DONG_PAGES, "출장마사지")
            + _links(STATION_PAGES, "출장마사지") + _links(LIVING_PAGES, "홈타이"))
    self_href = "/" + path
    n = len(pool)
    start, step, picks = (idx * 5) % n, 3, []
    i = start
    while len(picks) < 9 and len(picks) < n:
        cand = pool[i % n]
        if cand[0] != self_href and cand not in picks:
            picks.append(cand)
        i += step
    # 관련 테마 4개도 회전 추가
    tp = _links(THEME_PAGES, "마사지")
    m = len(tp)
    picks += [tp[(idx * 3 + k) % m] for k in range(4)]
    seen, uniq = set(), []
    for h, a in picks:
        if h == self_href or h in seen:
            continue
        seen.add(h)
        uniq.append((h, a))
    return (
        '<section class="related-areas"><h2>주변 지역·관련 안내</h2>'
        "<p>가까운 동네와 지하철역, 관리 테마도 함께 살펴보세요. 위치가 다르면 도착 시간과 준비 방식이 달라질 수 있어, "
        "정확한 위치는 예약 시 알려주시면 바로 확인해 드립니다.</p>"
        + _ul(uniq) + "</section>"
    )


def _inject_before_pricing(body: str, block: str) -> str:
    if '<section class="pricing">' in body:
        return body.replace('<section class="pricing">', block + '<section class="pricing">', 1)
    if '<section class="cta">' in body:
        return body.replace('<section class="cta">', block + '<section class="cta">', 1)
    return body + block


def _review_objs():
    out = []
    for r in REVIEWS:
        out.append({
            "@type": "Review",
            "author": {"@type": "Person", "name": r["author"]},
            "datePublished": r["date"],
            "reviewRating": {
                "@type": "Rating", "ratingValue": r["rating"],
                "bestRating": AGG_BEST, "worstRating": AGG_WORST,
            },
            "reviewBody": r["body"],
        })
    return out


def service_schema(canonical: str, path: str) -> str:
    """Service + Offer + AggregateRating(+후기 페이지엔 review 배열) JSON-LD."""
    base = BASE_URL.rstrip("/")
    service = {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": "출장마사지·홈타이 방문 관리",
        "name": "관악 출장마사지·홈타이",
        "description": "서울 관악구 전지역 방문 출장마사지·홈타이. 봉천권·신림권·남현권 전 행정동·역세권 예약 안내.",
        "provider": {
            "@type": "Organization", "name": BRAND,
            "telephone": PHONE, "url": base + "/",
        },
        "areaServed": {"@type": "AdministrativeArea", "name": REGION_FULL},
        "url": canonical,
        "offers": [
            {"@type": "Offer", "name": "60분 코스", "price": "90000", "priceCurrency": "KRW"},
            {"@type": "Offer", "name": "90분 코스", "price": "150000", "priceCurrency": "KRW"},
            {"@type": "Offer", "name": "120분 코스", "price": "180000", "priceCurrency": "KRW"},
        ],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": f"{AGG_VALUE:.1f}",
            "reviewCount": AGG_COUNT,
            "bestRating": AGG_BEST,
            "worstRating": AGG_WORST,
        },
    }
    if path == "reviews/":
        service["review"] = _review_objs()
    return ('<script type="application/ld+json">\n'
            + json.dumps(service, ensure_ascii=False, indent=2)
            + "\n</script>")


def text_length(body_html: str) -> int:
    """태그를 제거한 본문 글자수(공백 포함, 연속 공백은 1자).
    공통 요금 블록은 페이지 고유 본문이 아니므로 측정에서 제외한다."""
    text = re.sub(r'<section class="pricing">.*?</section>', " ", body_html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text)


def render_nav(current_path: str) -> str:
    items = []
    for label, href, children in NAV:
        active = " is-active" if href == "/" + current_path else ""
        if children:
            sub = "".join(
                f'<li><a href="{c_href}">{c_label}</a></li>'
                for c_label, c_href in children
            )
            items.append(
                f'<li class="nav-item has-sub{active}">'
                f'<a href="{href}">{label}</a>'
                f'<ul class="sub-menu">{sub}</ul></li>'
            )
        else:
            items.append(
                f'<li class="nav-item{active}"><a href="{href}">{label}</a></li>'
            )
    return "".join(items)


def render_breadcrumb(crumbs) -> str:
    if not crumbs:
        return ""
    parts = ['<nav class="breadcrumb" aria-label="현재 위치"><ol>']
    parts.append('<li><a href="/">홈</a></li>')
    for label, href in crumbs:
        if href:
            parts.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            parts.append(f"<li><span>{label}</span></li>")
    parts.append("</ol></nav>")
    return "".join(parts)


def inject_toc(body: str):
    """본문 섹션(h2)에 id를 보장하고 좌측 목차 데이터를 만든다."""
    items = []
    counter = [0]

    def repl(m):
        attrs, title = m.group(1), m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs)
        if idm:
            sid = idm.group(1)
            opening = f"<section{attrs}>"
        else:
            counter[0] += 1
            sid = f"sec-{counter[0]}"
            opening = f'<section id="{sid}"{attrs}>'
        label = re.sub(r"<[^>]+>", "", title).strip()
        items.append((sid, label))
        return f"{opening}<h2>{title}</h2>"

    body = re.sub(r"<section([^>]*)>\s*<h2>(.*?)</h2>", repl, body, flags=re.S)
    return body, items


def render_toc(items) -> str:
    if len(items) < 3:
        return ""
    links = "".join(
        f'<li><a href="#{sid}">{label}</a></li>' for sid, label in items
    )
    return (
        '<aside class="page-toc"><nav aria-label="페이지 목차">'
        '<p class="toc-title">목차</p>'
        f"<ul>{links}</ul></nav></aside>"
    )


def render_page(page: dict) -> str:
    path = page["path"]
    title = page["title"]
    desc = page["desc"]
    h1 = page["h1"]
    body = page["body"]
    crumbs = page.get("breadcrumb") or []
    extra_head = page.get("extra_head", "")
    hero = page.get("hero", "")

    chars = text_length(body)
    noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
    robots = (
        '<meta name="robots" content="noindex,follow">'
        if noindex
        else '<meta name="robots" content="index,follow">'
    )
    canonical = BASE_URL.rstrip("/") + "/" + path

    # WebPage + BreadcrumbList 구조화 데이터 (페이지 공통)
    base = BASE_URL.rstrip("/")
    schema_blocks = [
        '<script type="application/ld+json">\n'
        "{\n"
        '  "@context": "https://schema.org",\n'
        '  "@type": "WebPage",\n'
        f'  "name": {json.dumps(title, ensure_ascii=False)},\n'
        f'  "description": {json.dumps(desc, ensure_ascii=False)},\n'
        f'  "url": "{canonical}",\n'
        '  "inLanguage": "ko-KR",\n'
        '  "isPartOf": {\n'
        '    "@type": "WebSite",\n'
        f'    "name": {json.dumps(BRAND, ensure_ascii=False)},\n'
        f'    "url": "{base}/"\n'
        "  }\n"
        "}\n"
        "</script>"
    ]
    crumb_items = [("홈", base + "/")]
    for label, href in crumbs:
        crumb_items.append((label, base + href if href else canonical))
    if crumbs:
        li = ",\n".join(
            "    {\n"
            f'      "@type": "ListItem", "position": {i + 1},\n'
            f'      "name": {json.dumps(lbl, ensure_ascii=False)}, "item": "{url}"\n'
            "    }"
            for i, (lbl, url) in enumerate(crumb_items)
        )
        schema_blocks.append(
            '<script type="application/ld+json">\n'
            "{\n"
            '  "@context": "https://schema.org",\n'
            '  "@type": "BreadcrumbList",\n'
            '  "itemListElement": [\n'
            f"{li}\n"
            "  ]\n"
            "}\n"
            "</script>"
        )
    # Service·Offer·AggregateRating(후기 별점) — 법무(noindex) 페이지 제외 전 페이지 부착
    if not page.get("noindex", False):
        schema_blocks.append(service_schema(canonical, path))

    # 메인 페이지: WebSite 노드(사이트명·검색엔진 인식 강화)
    if path == "":
        website = {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": BRAND,
            "url": base + "/",
            "inLanguage": "ko-KR",
            "publisher": {"@type": "Organization", "name": BRAND, "url": base + "/"},
        }
        schema_blocks.append('<script type="application/ld+json">\n'
                             + json.dumps(website, ensure_ascii=False, indent=2)
                             + "\n</script>")

    jsonld = "\n".join(schema_blocks) + "\n"

    # 히어로가 있는 페이지(메인)는 H1을 히어로 안에서 출력한다.
    if hero:
        page_head = hero
    else:
        page_head = ""

    h1_html = "" if hero else f"<h1>{h1}</h1>"

    body, toc_items = inject_toc(body)
    toc_html = render_toc(toc_items)
    layout_cls = "page-layout has-toc" if toc_html else "page-layout"

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{canonical}">
<link rel="alternate" type="application/rss+xml" title="{BRAND} 매거진" href="{base}/rss.xml">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#0a101f">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link rel="stylesheet" href="/assets/style.css">
{jsonld}{extra_head}</head>
<body>
<header class="site-header">
  <div class="header-accent" aria-hidden="true"></div>
  <div class="header-top">
    <div class="header-inner">
      <a class="brand" href="/"><span class="brand-mark">{BRAND_MARK}</span> <span class="brand-text">{BRAND}</span></a>
      <p class="header-tagline"><span class="tag-gem">◆</span> {REGION} 전지역 방문 관리 <span class="tag-gem">◆</span> 24시간 상담</p>
      <a class="header-call" href="tel:{PHONE}"><span class="call-label">예약전화</span> {PHONE_DISPLAY}</a>
      <button class="nav-toggle" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="main-nav" aria-label="주 메뉴">
    <div class="nav-inner"><ul class="nav-list">{render_nav(path)}</ul></div>
  </nav>
</header>
{page_head}<main class="site-main">
  <div class="container {layout_cls}">
    {toc_html}
    <article class="page-content">
      {render_breadcrumb(crumbs)}
      {h1_html}
      {body}
    </article>
  </div>
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-col footer-about">
      <p class="footer-brand">{BRAND}</p>
      <p class="footer-desc">{REGION} 전지역 방문 출장마사지·홈타이 안내 사이트입니다. 모든 서비스는 안내된 관리 범위와 위생·안전 기준 안에서만 제공됩니다.</p>
      <address class="footer-contact">
        <span class="footer-contact-row"><span class="footer-label">예약전화</span> <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></span>
        <span class="footer-contact-row"><span class="footer-label">상담시간</span> 연중무휴 24시간</span>
        <span class="footer-contact-row"><span class="footer-label">서비스 지역</span> {REGION_FULL} 전지역</span>
      </address>
    </div>
    <nav class="footer-col" aria-label="서비스 안내">
      <p class="footer-title">서비스</p>
      <ul>
        <li><a href="/massage/">관악 출장마사지</a></li>
        <li><a href="/gwanak/">권역·행정동 안내</a></li>
        <li><a href="/gwanak/sillim-station-chuljangmassage/">역세권 안내</a></li>
        <li><a href="/themes/">테마별 안내</a></li>
        <li><a href="/courses/">코스안내</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="이용 안내">
      <p class="footer-title">이용 안내</p>
      <ul>
        <li><a href="/reservation/">예약안내</a></li>
        <li><a href="/guide/">이용가이드</a></li>
        <li><a href="/reviews/">이용 후기</a></li>
        <li><a href="/support/">고객센터</a></li>
        <li><a href="/support/#faq">자주 묻는 질문</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="정책 및 기준">
      <p class="footer-title">정책</p>
      <ul>
        <li><a href="/about/">운영자 소개</a></li>
        <li><a href="/support/privacy/">개인정보처리방침</a></li>
        <li><a href="/support/terms/">이용약관</a></li>
        <li><a href="/guide/#hygiene">위생·안전 기준</a></li>
        <li><a href="/guide/#prohibited">금지행위 안내</a></li>
        <li><a href="/support/#biz">제휴·기업 문의</a></li>
      </ul>
    </nav>
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-inner">
      <p class="footer-copy">&copy; {BRAND}. All rights reserved.</p>
      <p class="footer-note">건전한 방문 관리 서비스를 운영하며, 불법적인 요청은 어떤 경우에도 응하지 않습니다.</p>
      <div class="footer-tg">
        <a class="tg-btn" href="https://t.me/googleseolab" target="_blank" rel="noopener nofollow"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.94 4.6 18.6 20.3c-.25 1.1-.9 1.38-1.83.86l-5.05-3.72-2.44 2.35c-.27.27-.5.5-1.01.5l.36-5.13L17.97 6.6c.41-.36-.09-.56-.63-.2L6.2 13.36l-5.06-1.58c-1.1-.34-1.12-1.1.23-1.62l19.78-7.62c.92-.34 1.72.2 1.42 1.66z"/></svg>웹사이트 제작문의</a>
        <a class="tg-btn" href="https://t.me/googleseolab" target="_blank" rel="noopener nofollow"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.94 4.6 18.6 20.3c-.25 1.1-.9 1.38-1.83.86l-5.05-3.72-2.44 2.35c-.27.27-.5.5-1.01.5l.36-5.13L17.97 6.6c.41-.36-.09-.56-.63-.2L6.2 13.36l-5.06-1.58c-1.1-.34-1.12-1.1.23-1.62l19.78-7.62c.92-.34 1.72.2 1.42 1.66z"/></svg>제휴문의</a>
      </div>
    </div>
  </div>
</footer>
<a class="call-fab" href="tel:{PHONE}" aria-label="전화 예약 {PHONE_DISPLAY}">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
  <span class="call-fab-label">예약 전화</span>
</a>
<script src="/assets/nav.js"></script>
</body>
</html>
"""


def build() -> None:
    report = []
    sitemap_urls = []
    rss_items = []
    base = BASE_URL.rstrip("/")
    today = datetime.date.today().isoformat()

    for idx, page in enumerate(PAGES):
        path = page["path"]  # "" 또는 "gwanak/sillim-dong-.../" 형태

        # 내부 링크 강화(롱테일 앵커): 메인=전체 지역·역·테마 인덱스, 지역/테마 상세=주변 관련 링크
        if path == "":
            page["body"] = _inject_before_pricing(page["body"], homepage_link_index())
        elif (path.startswith("gwanak/") and path != "gwanak/") or \
             (path.startswith("themes/") and path != "themes/"):
            page["body"] = _inject_before_pricing(page["body"], related_block(path, idx))

        out_dir = os.path.join(ROOT, path)
        os.makedirs(out_dir, exist_ok=True)
        html_out = render_page(page)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_out)

        chars = text_length(page["body"])
        noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
        if not noindex:
            url = base + "/" + path
            sitemap_urls.append((url, page.get("date", today), path))
            if path.startswith("magazine/") and path != "magazine/":
                rss_items.append(page)
        report.append((path or "/", chars, "noindex" if noindex else "index"))

    # sitemap.xml (lastmod·changefreq·priority 포함 — 색인 우선순위 신호)
    def _sm_meta(path):
        if path == "":
            return ("daily", "1.0")
        if path in ("gwanak/", "themes/", "massage/", "reviews/", "courses/", "magazine/"):
            return ("weekly", "0.9")
        if path.startswith("magazine/"):
            return ("monthly", "0.6")
        if path.startswith(("gwanak/", "themes/")):
            return ("weekly", "0.8")
        return ("monthly", "0.7")

    def _sm_row(u, d, path):
        cf, pr = _sm_meta(path)
        return (f"  <url><loc>{u}</loc><lastmod>{d}</lastmod>"
                f"<changefreq>{cf}</changefreq><priority>{pr}</priority></url>")

    urls = "\n".join(_sm_row(u, d, p) for u, d, p in sitemap_urls)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{urls}\n</urlset>\n"
        )

    # rss.xml — 매거진 글 피드 (네이버·구글·빙 신규 글 발견 가속)
    def _rfc822(d):
        try:
            dt = datetime.datetime.strptime(d, "%Y-%m-%d")
        except (ValueError, TypeError):
            dt = datetime.datetime.now()
        return dt.strftime("%a, %d %b %Y 09:00:00 +0900")

    rss_items.sort(key=lambda p: p.get("date", today), reverse=True)
    items_xml = []
    for p in rss_items:
        link = base + "/" + p["path"]
        items_xml.append(
            "    <item>\n"
            f"      <title>{html.escape(p['title'])}</title>\n"
            f"      <link>{link}</link>\n"
            f"      <guid isPermaLink=\"true\">{link}</guid>\n"
            f"      <description>{html.escape(p['desc'])}</description>\n"
            f"      <pubDate>{_rfc822(p.get('date', today))}</pubDate>\n"
            "    </item>"
        )
    build_date = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0900")
    with open(os.path.join(ROOT, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            "  <channel>\n"
            f"    <title>{html.escape(BRAND)} 매거진</title>\n"
            f"    <link>{base}/magazine/</link>\n"
            f'    <atom:link href="{base}/rss.xml" rel="self" type="application/rss+xml"/>\n'
            f"    <description>{REGION} 출장마사지·홈타이 — 마사지·휴식·컨디션 관리 가이드</description>\n"
            "    <language>ko-KR</language>\n"
            f"    <lastBuildDate>{build_date}</lastBuildDate>\n"
            f"{chr(10).join(items_xml)}\n"
            "  </channel>\n</rss>\n"
        )

    # robots.txt — 전체 허용 + 네이버(Yeti)·구글봇 명시 + sitemap/rss 안내(색인 가속)
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(
            "User-agent: *\nAllow: /\n\n"
            "User-agent: Yeti\nAllow: /\n\n"        # 네이버 검색 봇
            "User-agent: Googlebot\nAllow: /\n\n"
            "User-agent: Bingbot\nAllow: /\n\n"
            f"Sitemap: {base}/sitemap.xml\n"
            f"Sitemap: {base}/rss.xml\n"
        )

    # IndexNow 키 인증 파일 — https://host/{KEY}.txt 로 노출되어야 함
    with open(os.path.join(ROOT, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY + "\n")

    # .nojekyll (GitHub Pages)
    open(os.path.join(ROOT, ".nojekyll"), "w").close()

    width = max(len(p) for p, _, _ in report)
    print(f"{'PATH'.ljust(width)}  CHARS  ROBOTS")
    for p, c, r in sorted(report):
        flag = "" if (r == "noindex" or MIN_INDEX_CHARS <= c <= 2500) else "  ⚠"
        print(f"{p.ljust(width)}  {str(c).rjust(5)}  {r}{flag}")
    print(f"\n{len(report)} pages built, {len(sitemap_urls)} in sitemap.")
    print(f"rss.xml: {len(rss_items)} magazine items")
    print(f"IndexNow key file: {INDEXNOW_KEY}.txt")


if __name__ == "__main__":
    build()
