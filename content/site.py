# 사이트 공통 설정
# 배포 도메인 확정 후 BASE_URL 을 실제 도메인으로 변경하세요.
BASE_URL = "https://gwanak-massage1.pages.dev"

BRAND = "바로GO"
BRAND_MARK = "GO"          # 헤더 로고 원형 마크 글자
PHONE = "0508-202-4719"
PHONE_DISPLAY = "0508-202-4719"

REGION = "관악구"           # 행정구역명
REGION_SHORT = "관악"        # 키워드 축약형
REGION_FULL = "서울특별시 관악구"

# 상단 메뉴 — 하위 메뉴에는 키워드를 대량 나열하지 않고 권역·역명만 간결히 표시한다.
NAV = [
    ("홈", "/", []),
    ("관악 출장마사지", "/massage/", [
        ("출장마사지 안내", "/massage/#service"),
        ("홈타이 안내", "/massage/#hometai"),
        ("전지역 방문 안내", "/massage/#coverage"),
        ("역세권 인근 안내", "/massage/#stations"),
        ("예약 가능 시간", "/massage/#hours"),
        ("코스 선택 안내", "/massage/#course"),
        ("이용 전 확인사항", "/massage/#check"),
        ("위생·안전 안내", "/massage/#safety"),
        ("자주 묻는 질문", "/massage/#faq"),
    ]),
    ("권역·행정동", "/gwanak/", [
        ("관악구 전지역", "/gwanak/"),
        ("봉천권", "/gwanak/bongcheon-area-chuljangmassage/"),
        ("신림권", "/gwanak/sillim-area-chuljangmassage/"),
        ("남현권", "/gwanak/namhyeon-area-chuljangmassage/"),
    ]),
    ("역세권 안내", "/gwanak/sillim-station-chuljangmassage/", [
        ("신림역", "/gwanak/sillim-station-chuljangmassage/"),
        ("서울대입구역", "/gwanak/seoul-national-univ-station-chuljangmassage/"),
        ("낙성대역", "/gwanak/nakseongdae-station-chuljangmassage/"),
        ("봉천역", "/gwanak/bongcheon-station-chuljangmassage/"),
        ("신대방역", "/gwanak/sindaebang-station-chuljangmassage/"),
        ("당곡역", "/gwanak/danggok-station-chuljangmassage/"),
        ("서원역", "/gwanak/seowon-station-chuljangmassage/"),
        ("서울대벤처타운역", "/gwanak/seoul-venture-town-station-chuljangmassage/"),
        ("관악산역", "/gwanak/gwanaksan-station-chuljangmassage/"),
        ("보라매병원역", "/gwanak/boramae-hospital-station-chuljangmassage/"),
    ]),
    ("생활권 안내", "/gwanak/sillim-station-area-chuljangmassage/", [
        ("신림역 상권", "/gwanak/sillim-station-area-chuljangmassage/"),
        ("서울대입구 생활권", "/gwanak/seoul-national-univ-area-chuljangmassage/"),
        ("낙성대 생활권", "/gwanak/nakseongdae-area-chuljangmassage/"),
        ("봉천동 생활권", "/gwanak/bongcheon-area-guide-chuljangmassage/"),
        ("신림동 고시촌", "/gwanak/sillim-gosichon-area-chuljangmassage/"),
        ("서울대벤처타운 생활권", "/gwanak/seoul-venture-town-area-chuljangmassage/"),
        ("관악산 입구 생활권", "/gwanak/gwanaksan-entrance-area-chuljangmassage/"),
        ("난곡·난향 생활권", "/gwanak/nangok-nanhyang-area-chuljangmassage/"),
        ("보라매병원 인근", "/gwanak/boramae-hospital-area-chuljangmassage/"),
        ("남현동·사당 인접", "/gwanak/namhyeon-sadang-area-chuljangmassage/"),
    ]),
    ("테마별 안내", "/themes/", [
        ("전체 테마", "/themes/"),
        ("스웨디시", "/themes/swedish/"),
        ("로미로미", "/themes/lomilomi/"),
        ("타이마사지", "/themes/thai/"),
        ("중국마사지", "/themes/chinese/"),
        ("아로마테라피", "/themes/aroma/"),
        ("홈케어", "/themes/homecare/"),
        ("호텔식마사지", "/themes/hotel-style/"),
        ("발마사지", "/themes/foot/"),
        ("스포츠·경락", "/themes/sports/"),
        ("스킨케어", "/themes/skincare/"),
        ("왁싱", "/themes/waxing/"),
        ("커플 관리", "/themes/couple/"),
        ("24시간", "/themes/24hours/"),
        ("수면 가능", "/themes/overnight/"),
    ]),
    ("코스안내", "/courses/", [
        ("전체 코스", "/courses/"),
        ("피로 회복 관리", "/courses/#recovery"),
        ("아로마 관리", "/courses/#aroma"),
        ("스포츠 관리", "/courses/#sports"),
        ("홈타이 코스", "/courses/#hometai"),
        ("커플·가족 방문 관리", "/courses/#couple"),
        ("기업·단체 방문 관리", "/courses/#group"),
        ("가격 안내", "/courses/#price"),
        ("코스 선택 가이드", "/courses/#guide"),
    ]),
    ("예약안내", "/reservation/", [
        ("예약 방법", "/reservation/#how"),
        ("예약 가능 시간", "/reservation/#hours"),
        ("방문 가능 장소", "/reservation/#place"),
        ("결제 안내", "/reservation/#payment"),
        ("변경·취소 안내", "/reservation/#change"),
        ("예약 전 체크사항", "/reservation/#check"),
    ]),
    ("이용가이드", "/guide/", [
        ("처음 이용하시는 분", "/guide/#first"),
        ("방문 전 준비사항", "/guide/#prepare"),
        ("위생 및 안전 기준", "/guide/#hygiene"),
        ("관리 후 주의사항", "/guide/#after"),
        ("금지행위 안내", "/guide/#prohibited"),
        ("이용 FAQ", "/guide/#faq"),
    ]),
    ("매거진", "/magazine/", [
        ("전체 글", "/magazine/"),
        ("마사지 비교 가이드", "/magazine/swedish-vs-thai/"),
        ("처음 이용 가이드", "/magazine/first-time-guide/"),
        ("수면과 마사지", "/magazine/sleep-and-massage/"),
        ("운동 후 회복", "/magazine/post-workout-timing/"),
        ("어깨·목 결림 관리", "/magazine/neck-shoulder-care/"),
        ("부모님 선물 가이드", "/magazine/parents-gift/"),
    ]),
    ("후기", "/reviews/", [
        ("전체 후기", "/reviews/"),
        ("지역별 후기", "/reviews/#area"),
        ("역세권 후기", "/reviews/#station"),
        ("후기 작성 안내", "/reviews/#write"),
    ]),
    ("고객센터", "/support/", [
        ("공지사항", "/support/#notice"),
        ("자주 묻는 질문", "/support/#faq"),
        ("1:1 문의", "/support/#contact"),
        ("제휴·기업 문의", "/support/#biz"),
        ("개인정보처리방침", "/support/privacy/"),
        ("이용약관", "/support/terms/"),
    ]),
]
