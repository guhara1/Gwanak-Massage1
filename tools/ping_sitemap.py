#!/usr/bin/env python3
"""사이트맵 핑(ping).

참고: 구글(2023.6)과 빙은 무인증 사이트맵 핑 엔드포인트를 폐지했다.
따라서 현재 가장 효과적인 즉시 통보 수단은 다음과 같다.
  - 빙·네이버·얀덱스 → IndexNow:  python tools/indexnow.py
  - 구글            → Indexing API: python tools/google_index.py
  - 그 외           → 서치콘솔/웹마스터도구에 sitemap.xml 1회 등록(이후 자동 재크롤)

이 스크립트는 아직 핑을 받는 일부 엔진(얀덱스 등)과의 호환을 위해 남겨둔다.
실패 코드가 떠도 정상이며, IndexNow 통보를 함께 실행하도록 안내한다.
"""
import os
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content.site import BASE_URL  # noqa: E402

SITEMAP = BASE_URL.rstrip("/") + "/sitemap.xml"

# 폐지되지 않은(또는 무해한) 핑 대상만. 폐지된 곳은 단순히 실패만 출력된다.
TARGETS = [
    "https://webmaster.yandex.com/ping?sitemap=",
]


def main():
    print(f"사이트맵: {SITEMAP}\n")
    for t in TARGETS:
        url = t + urllib.parse.quote(SITEMAP, safe="")
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                print(f"  {r.status} {t}")
        except Exception as e:  # noqa: BLE001
            print(f"  실패 {t} — {e}")
    print(
        "\n빠른 색인은 아래를 권장합니다:\n"
        "  python tools/indexnow.py        # 빙·네이버·얀덱스 즉시 통보\n"
        "  python tools/google_index.py    # 구글 Indexing API (서비스계정 필요)"
    )


if __name__ == "__main__":
    main()
