# 이용 후기 데이터 — 화면에 표시되는 후기 카드와 구조화 데이터(Review/AggregateRating)의 단일 출처.
# Google 구조화 데이터 정책: 별점·후기 스키마는 같은 페이지에 실제로 표시된 후기와 일치해야 한다.
# 따라서 이 목록 하나로 (1) 후기 페이지의 보이는 카드 (2) JSON-LD review 배열을 함께 생성한다.
import html
import json

# 각 후기: 표기명(개인정보 보호를 위해 일부만), 별점, 이용월, 지역(대표 동/역), 테마, 본문
REVIEWS = [
    {"author": "김O준", "rating": 5, "date": "2026-05-28", "area": "신림역", "theme": "스웨디시",
     "body": "야근 끝나고 밤 11시에 신림역 근처 오피스텔로 불렀는데 안내해준 시간에 정확히 도착했어요. 압도 처음에 맞춰주셔서 어깨 뭉친 게 확실히 풀렸습니다. 다음에 또 예약할게요."},
    {"author": "이O은", "rating": 5, "date": "2026-05-21", "area": "서울대입구역", "theme": "아로마테라피",
     "body": "서울대입구 쪽 자취방인데 좁아서 걱정했더니 매트 한 장이면 된다고 하셔서 편하게 받았습니다. 아로마 향이 은은해서 받다가 잠들었네요. 전화 상담도 친절했어요."},
    {"author": "박O호", "rating": 4, "date": "2026-05-15", "area": "봉천동", "theme": "타이마사지",
     "body": "홈타이 처음 받아봤는데 스트레칭 위주라 개운합니다. 도착이 10분 정도 늦은 건 아쉬웠지만 미리 연락 주셔서 괜찮았어요. 가격도 안내받은 그대로였습니다."},
    {"author": "최O린", "rating": 5, "date": "2026-05-09", "area": "낙성대역", "theme": "스포츠·경락",
     "body": "주말 농구 후에 종아리랑 허벅지가 너무 뭉쳤는데 부위별로 시간 배분해서 집중적으로 풀어주셨어요. 운동 자주 하는 분들께 추천합니다."},
    {"author": "정O아", "rating": 5, "date": "2026-04-30", "area": "대학동", "theme": "수면 가능",
     "body": "고시촌 원룸이라 망설였는데 조용히 진행해주시고 끝나고 바로 잘 수 있어서 좋았습니다. 결제도 시작 전에 끝나서 깔끔했어요."},
    {"author": "한O", "rating": 4, "date": "2026-04-22", "area": "남현동", "theme": "로미로미",
     "body": "사당 근처 남현동도 방문 가능하다고 해서 예약했어요. 깊은 압 좋아하는데 딱 맞게 해주셨습니다. 다만 주말이라 예약이 조금 빡빡했네요. 미리 예약하는 걸 추천."},
    {"author": "오O석", "rating": 5, "date": "2026-04-14", "area": "신림동", "theme": "커플 관리",
     "body": "여자친구랑 같이 받았는데 관리사 두 분이 동시에 진행해주셔서 시간 잘 맞았어요. 둘 다 다른 테마 골랐는데도 문제없이 진행됐습니다."},
    {"author": "윤O정", "rating": 5, "date": "2026-04-03", "area": "보라매병원역", "theme": "홈케어",
     "body": "부모님 선물로 예약했어요. 받는 분 압 선호를 몰라서 걱정했는데 시작하고 맞춰주신다고 해서 안심했습니다. 어머니가 너무 만족하셨어요."},
]

_ratings = [r["rating"] for r in REVIEWS]
AGG_VALUE = round(sum(_ratings) / len(_ratings) + 1e-9, 1)   # 실제 평균
AGG_COUNT = len(REVIEWS)
AGG_BEST = 5
AGG_WORST = 1


def _stars(n: int) -> str:
    return "★" * n + "☆" * (AGG_BEST - n)


def reviews_html() -> str:
    """후기 페이지에 표시되는 후기 카드 묶음."""
    cards = []
    for r in REVIEWS:
        cards.append(
            '<li class="review-card" itemscope itemtype="https://schema.org/Review">'
            '<div class="review-head">'
            f'<span class="review-author" itemprop="author">{html.escape(r["author"])}</span>'
            f'<span class="review-stars" aria-label="별점 {r["rating"]}점" '
            f'itemprop="reviewRating" itemscope itemtype="https://schema.org/Rating">{_stars(r["rating"])}'
            f'<meta itemprop="ratingValue" content="{r["rating"]}"><meta itemprop="bestRating" content="5">'
            "</span></div>"
            f'<p class="review-meta">{html.escape(r["area"])} · {html.escape(r["theme"])} · '
            f'<time itemprop="datePublished" datetime="{r["date"]}">{r["date"][:7].replace("-", ".")}</time></p>'
            f'<p class="review-body" itemprop="reviewBody">{html.escape(r["body"])}</p>'
            "</li>"
        )
    avg = f"{AGG_VALUE:.1f}"
    return (
        '<section id="list">'
        "<h2>실제 이용 후기</h2>"
        '<div class="review-summary">'
        f'<span class="review-avg">{avg}</span>'
        f'<span class="review-avg-stars">{_stars(round(AGG_VALUE))}</span>'
        f'<span class="review-count">이용자 평점 · 후기 {AGG_COUNT}건</span>'
        "</div>"
        f'<ul class="review-list">{"".join(cards)}</ul>'
        "<p>아래 후기는 이용이 확인된 예약 건에 한해 등록되며, 작성자 식별 정보는 가린 뒤 게재됩니다.</p>"
        "</section>"
    )


def review_jsonld_items() -> str:
    """Service 스키마에 넣을 review 배열(JSON 조각, 들여쓰기 포함)."""
    items = []
    for r in REVIEWS:
        obj = {
            "@type": "Review",
            "author": {"@type": "Person", "name": r["author"]},
            "datePublished": r["date"],
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": r["rating"],
                "bestRating": AGG_BEST,
                "worstRating": AGG_WORST,
            },
            "reviewBody": r["body"],
        }
        items.append(json.dumps(obj, ensure_ascii=False))
    return ",\n".join("      " + it for it in items)


def aggregate_rating_json() -> str:
    """AggregateRating JSON 조각."""
    obj = {
        "@type": "AggregateRating",
        "ratingValue": f"{AGG_VALUE:.1f}",
        "reviewCount": AGG_COUNT,
        "bestRating": AGG_BEST,
        "worstRating": AGG_WORST,
    }
    return json.dumps(obj, ensure_ascii=False)
