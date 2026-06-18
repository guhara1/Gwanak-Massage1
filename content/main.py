# 메인 페이지 — 허브 역할. 모든 키워드를 밀어 넣지 않고 상세 페이지로 연결한다.
# 실제 오프라인 사업장 주소가 없는 방문형 사이트이므로 LocalBusiness Schema는 사용하지 않는다.
from .site import BASE_URL, BRAND, PHONE, PHONE_DISPLAY
from .pricing import PRICING

_JSONLD = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{BRAND}",
  "telephone": "{PHONE}",
  "url": "{BASE_URL}/",
  "image": "{BASE_URL}/assets/og-image.png",
  "description": "서울 관악구 전지역 방문 출장마사지·홈타이 예약 안내",
  "areaServed": {{
    "@type": "AdministrativeArea",
    "name": "서울특별시 관악구"
  }},
  "contactPoint": {{
    "@type": "ContactPoint",
    "telephone": "{PHONE}",
    "contactType": "reservations",
    "areaServed": "KR",
    "availableLanguage": "Korean"
  }}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "관악구 전지역 방문이 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "봉천권, 신림권, 남현권으로 나누어 안내하며 예약 시간과 정확한 위치, 배정 상황에 따라 가능 여부가 달라집니다. 권역별 안내 페이지에서 행정동 기준으로 확인할 수 있습니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "신림역이나 서울대입구역 근처도 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "주요 역세권은 역 상세 페이지에서 주변 생활권과 함께 안내합니다. 신림역은 2호선과 신림선 환승역이지만 페이지는 하나로 운영하며, 정확한 가능 여부는 예약 시 위치를 기준으로 확인합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "봉천동·신림동은 왜 행정동으로 나뉘어 있나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "관악구는 봉천동·신림동·남현동 법정동이 보라매동, 청룡동, 낙성대동, 대학동 등 여러 행정동으로 세분되어 있습니다. 각 행정동의 생활권 특징이 달라 페이지를 나누어 안내합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "사당역 근처 남현동도 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "남현동은 관악구에 속하며 방문 가능합니다. 사당역 자체는 동작구·서초구 경계 성격이 강해 남현동 페이지 본문에서 인접 생활권으로 안내합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "홈타이와 출장마사지는 어떻게 다른가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "관악 홈타이는 자택, 숙소, 사무실 인근에서 예약 가능 여부를 먼저 확인한 뒤 이용하는 방문형 관리 서비스입니다. 출장마사지와 같은 방문 관리의 다른 표현으로 보시면 됩니다."
      }}
    }}
  ]
}}
</script>
"""

_HERO = f"""<section class="hero">
  <div class="hero-inner">
    <p class="hero-badge">Premium Visiting Spa · 관악구 전지역</p>
    <h1>관악 출장마사지·관악구 홈타이<br>지역별 예약 안내</h1>
    <p class="hero-lead">샵까지 갈 필요 없이, 계신 곳에서 받는 프리미엄 방문 관리.<br>봉천권·신림권·남현권 어디든 전화 한 통이면 예약이 끝납니다.</p>
    <div class="hero-actions">
      <a class="hero-btn primary" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
      <a class="hero-btn" href="/courses/">코스 안내 보기</a>
    </div>
    <ul class="hero-stats">
      <li><strong>3개</strong><span>대표 권역</span></li>
      <li><strong>21개</strong><span>행정동 안내</span></li>
      <li><strong>10개</strong><span>역세권 안내</span></li>
      <li><strong>24시간</strong><span>예약 상담</span></li>
    </ul>
  </div>
</section>
"""

_BODY = f"""
<section id="service">
<h2>관악 출장마사지·홈타이 서비스 안내</h2>
<p>관악 출장마사지를 찾는 분들은 대부분 현재 위치에서 가까운 방문 가능 지역을 먼저 확인합니다. 관악구는 서울 남부에 있는 자치구로, 신림역과 서울대입구역을 중심으로 한 2호선 생활권, 관악산과 서울대 인근을 연결하는 신림선 생활권, 남현동과 사당 인접 생활권이 함께 있는 지역입니다. 이 페이지는 관악구 전체 구조를 설명하는 허브 역할을 하며, 더 자세한 내용은 권역별·행정동별·역세권별·생활권별 안내 페이지에서 확인하실 수 있습니다. {BRAND}는 예약 확인부터 방문 관리까지 정해진 절차에 따라 진행하며, 처음 이용하시는 분도 어렵지 않게 예약할 수 있도록 각 단계를 명확하게 안내해 드립니다.</p>
</section>

<section id="why">
<h2>관악구에서 출장마사지를 찾는 이유</h2>
<p>관악구는 1인 가구와 대학가, 고시촌, 직장 통근 세대가 두텁게 섞여 있는 지역입니다. 신림역 상권과 서울대입구역 생활권은 늦은 시간까지 활기가 돌고, 관악산 자락과 난곡·난향 주거권은 차분한 생활 리듬을 가집니다. 그만큼 샵을 직접 찾아가기보다 자택이나 숙소에서 받는 방문 관리를 선호하는 분이 많습니다. 관악 홈타이는 이동 시간을 아끼고 익숙한 공간에서 편하게 쉴 수 있다는 점에서 꾸준히 문의가 들어옵니다. 다만 관악구는 면적이 아주 큰 구는 아니어도 신림역 상권, 서울대입구역 생활권, 난곡·난향 주거권, 고시촌, 관악산 입구의 이동 기준이 서로 달라, 예약 전에 방문 가능 지역과 예상 도착 시간을 함께 확인하는 것이 좋습니다.</p>
</section>

<section id="coverage">
<h2>관악구 전지역 방문 가능 안내</h2>
<p>관악구는 봉천동, 신림동, 남현동이라는 큰 법정동 이름이 익숙하지만 실제 행정동은 보라매동, 은천동, 성현동, 중앙동, 청림동, 행운동, 청룡동, 낙성대동, 인헌동, 신림동, 신사동, 조원동, 미성동, 난곡동, 난향동, 서원동, 신원동, 서림동, 삼성동, 대학동, 남현동처럼 더 세분화되어 있습니다. 그래서 이 사이트는 단순히 ‘관악 전지역 가능’만 적는 방식보다 봉천권·신림권·남현권을 먼저 안내하고, 하위 페이지에서 행정동과 역세권을 연결하는 구조를 따릅니다. 방문 가능 여부는 행정동 경계가 아니라 실제 위치와 예약 시간으로 판단하므로, 권역과 행정동 안내는 위치를 설명하는 기준으로 활용해 주세요.</p>
</section>

<section id="areas">
<h2>봉천권·신림권·남현권 생활권 차이</h2>
<p>봉천권은 서울대입구역, 봉천역, 낙성대역을 중심으로 한 주거·상권 혼합 생활권입니다. 신림권은 신림역 상권과 고시촌, 서원·서울대벤처타운·관악산 신림선 생활권, 난곡·난향 주거권을 아우릅니다. 남현권은 사당역과 가까운 남현동 단일 생활권으로, 관악구 안에서 별도로 다룹니다. 같은 관악구라도 권역마다 주거 형태와 생활 리듬, 이동 기준이 다르므로 아래 권역 페이지에서 차이를 확인하신 뒤 세부 행정동으로 들어가시면 됩니다.</p>
<ul class="card-grid">
<li><a href="/gwanak/bongcheon-area-chuljangmassage/">봉천권 출장마사지</a></li>
<li><a href="/gwanak/sillim-area-chuljangmassage/">신림권 출장마사지</a></li>
<li><a href="/gwanak/namhyeon-area-chuljangmassage/">남현권 출장마사지</a></li>
</ul>
<p>관악구 전체 구조가 궁금하시면 <a href="/gwanak/">관악구 전지역 안내</a>에서 권역·행정동·역세권·생활권을 한눈에 확인하실 수 있습니다.</p>
</section>

<section id="dongs">
<h2>대표 행정동별 방문 가능 지역 안내</h2>
<p>행정동 페이지는 보라매동, 청룡동, 낙성대동, 신림동, 대학동, 난곡동처럼 세부 검색 의도를 담당합니다. 각 페이지에서는 해당 행정동의 생활권 특징, 가까운 역세권, 방문 전 확인사항, 예약 가능 시간을 동마다 고유한 내용으로 설명합니다. 가까운 행정동이라도 역세권과 생활권 설명을 다르게 작성해 중복을 줄였습니다.</p>
<ul class="card-grid">
<li><a href="/gwanak/sillim-dong-chuljangmassage/">신림동</a></li>
<li><a href="/gwanak/cheongnyong-dong-chuljangmassage/">청룡동</a></li>
<li><a href="/gwanak/nakseongdae-dong-chuljangmassage/">낙성대동</a></li>
<li><a href="/gwanak/daehak-dong-chuljangmassage/">대학동</a></li>
<li><a href="/gwanak/nangok-dong-chuljangmassage/">난곡동</a></li>
<li><a href="/gwanak/boramae-dong-chuljangmassage/">보라매동</a></li>
</ul>
</section>

<section id="stations">
<h2>신림역·서울대입구역·낙성대역·봉천역 역세권 안내</h2>
<p>지하철역 페이지는 관악 지역 안내에서 중요한 역할을 합니다. 신림역, 서울대입구역, 낙성대역, 봉천역처럼 실제 검색어와 가까운 제목으로 검색 의도를 분명히 하며, 같은 역을 노선별로 나누지 않습니다. 신림역은 2호선과 신림선이 만나는 환승역이지만 1개 페이지로만 운영하고 본문 안에서 환승 특징을 설명합니다. 사당역이나 보라매역처럼 행정구역 경계가 애매한 역은 단독 페이지 대신 인접 생활권 본문에서 보조로 다룹니다.</p>
<ul class="card-grid">
<li><a href="/gwanak/sillim-station-chuljangmassage/">신림역</a></li>
<li><a href="/gwanak/seoul-national-univ-station-chuljangmassage/">서울대입구역</a></li>
<li><a href="/gwanak/nakseongdae-station-chuljangmassage/">낙성대역</a></li>
<li><a href="/gwanak/bongcheon-station-chuljangmassage/">봉천역</a></li>
<li><a href="/gwanak/sindaebang-station-chuljangmassage/">신대방역</a></li>
<li><a href="/gwanak/boramae-hospital-station-chuljangmassage/">보라매병원역</a></li>
</ul>
</section>

<section id="sillim-line">
<h2>신림선 관악산·서울대벤처타운·서원 생활권 안내</h2>
<p>신림선은 관악산역에서 샛강역까지 이어지는 경전철로, 신림·서원·서울대벤처타운·관악산 생활권을 연결합니다. 당곡역, 서원역, 서울대벤처타운역, 관악산역, 보라매병원역이 관악구 내 신림선 역세권에 해당합니다. 역세권 페이지가 역 검색을 담당한다면, 생활권 페이지는 신림역 상권, 신림동 고시촌, 관악산 입구처럼 거점 단위 검색 의도를 담당합니다. 행정동·역세권·생활권의 역할을 나누어 같은 내용을 반복하지 않도록 구성했습니다.</p>
<ul class="card-grid">
<li><a href="/gwanak/danggok-station-chuljangmassage/">당곡역</a></li>
<li><a href="/gwanak/seowon-station-chuljangmassage/">서원역</a></li>
<li><a href="/gwanak/seoul-venture-town-station-chuljangmassage/">서울대벤처타운역</a></li>
<li><a href="/gwanak/gwanaksan-station-chuljangmassage/">관악산역</a></li>
<li><a href="/gwanak/sillim-gosichon-area-chuljangmassage/">신림동 고시촌</a></li>
<li><a href="/gwanak/gwanaksan-entrance-area-chuljangmassage/">관악산 입구 생활권</a></li>
</ul>
</section>

<section id="themes">
<h2>테마별 관리 안내</h2>
<p>테마별 안내에서는 관리 유형별 특징, 추천 대상, 예약 전 확인사항을 설명합니다. 테마는 각각 독립 페이지로 운영하며, 지역 페이지와 역 페이지에서는 관련 테마로 연결만 해 드립니다. 특정 역과 테마를 조합한 페이지는 운영하지 않으니, 원하시는 관리 유형을 먼저 고른 뒤 예약 시 위치를 알려주시면 됩니다.</p>
<ul class="card-grid">
<li><a href="/themes/swedish/">스웨디시</a></li>
<li><a href="/themes/thai/">타이마사지</a></li>
<li><a href="/themes/aroma/">아로마테라피</a></li>
<li><a href="/themes/homecare/">홈케어</a></li>
<li><a href="/themes/sports/">스포츠·경락</a></li>
<li><a href="/themes/overnight/">수면 가능</a></li>
</ul>
</section>

<section id="check">
<h2>관악 홈타이 예약 전 확인사항</h2>
<p>예약 전에는 방문 가능 지역, 예약 가능 시간, 추가 이동비, 결제 방식, 취소 기준, 서비스 범위를 먼저 확인해야 합니다. 특히 난곡동, 난향동, 대학동, 관악산 인접 지역은 차량 이동 시간이 달라질 수 있으므로 정확한 도로명 주소와 진입 방향을 알려주시면 도착 시간이 정확해집니다. 숙소나 오피스텔로 방문을 요청하실 때는 공동현관 출입 방법과 예약 시간대 연락 가능 여부를 함께 알려주세요. 준비사항 전체는 <a href="/guide/">이용가이드</a>에, 예약 절차는 <a href="/reservation/">예약안내</a>에 정리되어 있습니다.</p>
</section>

<section id="guide">
<h2>관악 출장마사지 사이트 이용 가이드</h2>
<p>메인페이지는 관악구 전체 안내를 담당하고, 권역 페이지는 봉천권·신림권·남현권을 묶어주는 중간 허브 역할을 합니다. 행정동 페이지는 보라매동·청룡동·낙성대동·신림동·대학동·난곡동 같은 세부 검색을 담당하고, 역세권 페이지는 신림역·서울대입구역·낙성대역·봉천역·서울대벤처타운역·관악산역 검색 의도를 담당합니다. 생활권 페이지는 신림역 상권이나 신림동 고시촌처럼 거점 단위로 안내합니다. 거주 권역이 분명하면 권역 페이지부터, 가까운 역이 분명하면 역세권 페이지부터 살펴보시면 필요한 정보가 더 빨리 보입니다.</p>
</section>

<section id="safety">
<h2>위생 및 안전 안내</h2>
<p>건전하고 안전한 방문 관리를 위해 위생 기준, 예약 정보 확인, 개인정보 보호, 금지행위 안내를 명확히 제공합니다. 과장된 표현이나 허위 후기, 과도한 할인 문구는 사용하지 않으며, 불법적이거나 무리한 요청은 어떤 경우에도 진행하지 않습니다. 예약 정보는 관리 목적 외에 사용하지 않습니다. 자세한 기준은 <a href="/guide/#hygiene">위생·안전 기준</a>과 <a href="/support/privacy/">개인정보처리방침</a>에서 확인하실 수 있습니다.</p>
</section>

<section id="faq">
<h2>자주 묻는 질문</h2>
<div class="faq-item">
<h3>관악구 전지역 방문이 가능한가요?</h3>
<p>봉천권, 신림권, 남현권으로 나누어 안내하며 예약 시간과 정확한 위치, 배정 상황에 따라 가능 여부가 달라집니다. 권역별 안내 페이지에서 행정동 기준으로 확인할 수 있습니다.</p>
</div>
<div class="faq-item">
<h3>신림역이나 서울대입구역 근처도 가능한가요?</h3>
<p>주요 역세권은 역 상세 페이지에서 주변 생활권과 함께 안내합니다. 신림역은 2호선과 신림선 환승역이지만 페이지는 하나로 운영하며, 정확한 가능 여부는 예약 시 위치를 기준으로 확인합니다.</p>
</div>
<div class="faq-item">
<h3>사당역 근처 남현동도 가능한가요?</h3>
<p>남현동은 관악구에 속하며 방문 가능합니다. 사당역 자체는 동작구·서초구 경계 성격이 강해 남현동 페이지 본문에서 인접 생활권으로 안내합니다.</p>
</div>
<div class="faq-item">
<h3>당일 예약도 가능한가요?</h3>
<p>가능할 수 있지만 저녁 시간대와 주말은 문의가 많을 수 있어 사전 예약을 권장합니다.</p>
</div>
<div class="faq-item">
<h3>홈타이와 출장마사지는 어떻게 다른가요?</h3>
<p>관악 홈타이는 자택, 숙소, 사무실 인근에서 예약 가능 여부를 먼저 확인한 뒤 이용하는 방문형 관리 서비스입니다. 출장마사지와 같은 방문 관리의 다른 표현으로 보시면 됩니다.</p>
</div>
</section>

{PRICING}
<section id="contact" class="cta">
<h2>예약문의</h2>
<p>관악구 방문 관리 예약과 상담은 전화로 가장 빠르게 진행됩니다. 위치와 희망 시간을 알려주시면 가능 여부를 바로 확인해 드립니다.</p>
<a class="cta-phone" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
</section>
"""

PAGE = {
    "path": "",
    "title": "관악 출장마사지｜관악구 홈타이 지역별 예약 안내",
    "desc": "관악 출장마사지·홈타이 예약 전 행정동, 역세권, 이용 기준을 정리했습니다.",
    "h1": "관악 출장마사지 · 관악구 홈타이 지역별 예약 안내",
    "body": _BODY,
    "extra_head": _JSONLD,
    "breadcrumb": [],
    "hero": _HERO,
}
