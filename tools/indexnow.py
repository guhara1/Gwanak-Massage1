#!/usr/bin/env python3
"""IndexNow 즉시 색인 통보 — 빙·네이버·얀덱스.

사용법:
    python tools/indexnow.py                # sitemap.xml 의 모든 URL 통보
    python tools/indexnow.py URL [URL ...]   # 지정한 URL만 통보 (글 새로 올릴 때)

IndexNow 는 한 번 제출하면 참여 검색엔진(빙·네이버·얀덱스·Seznam)에
함께 전파된다. 키 인증 파일이 사이트 루트에 노출되어 있어야 한다:
    https://<도메인>/<KEY>.txt   (빌드 시 자동 생성)

표준 라이브러리만 사용한다. 별도 설치 불필요.
"""
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content.site import BASE_URL, INDEXNOW_KEY  # noqa: E402

BASE = BASE_URL.rstrip("/")
HOST = re.sub(r"^https?://", "", BASE).split("/")[0]
KEY_LOCATION = f"{BASE}/{INDEXNOW_KEY}.txt"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 제출 엔드포인트 — 하나만 보내도 전파되지만, 네이버·빙에 직접도 함께 보낸다.
ENDPOINTS = [
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow",
    "https://searchadvisor.naver.com/indexnow",
]


def sitemap_urls():
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        sys.exit("sitemap.xml 이 없습니다. 먼저 `python3 build.py` 를 실행하세요.")
    with open(path, encoding="utf-8") as f:
        return re.findall(r"<loc>([^<]+)</loc>", f.read())


def submit(urls):
    payload = json.dumps({
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }).encode("utf-8")

    for ep in ENDPOINTS:
        req = urllib.request.Request(
            ep, data=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                print(f"  {resp.status} {resp.reason:12} {ep}")
        except urllib.error.HTTPError as e:
            # 200/202 외에도 일부 엔드포인트는 다른 코드를 줄 수 있다.
            print(f"  {e.code} {e.reason:12} {ep}")
        except Exception as e:  # noqa: BLE001
            print(f"  ERR  {ep} — {e}")


def main():
    urls = sys.argv[1:] or sitemap_urls()
    # IndexNow 1회 제출 최대 10,000개
    urls = urls[:10000]
    print(f"호스트: {HOST}")
    print(f"키 위치: {KEY_LOCATION}")
    print(f"통보 URL {len(urls)}개 제출 중...\n")
    submit(urls)
    print("\n완료. (202/200 = 접수됨, 색인은 검색엔진 판단에 따라 진행)")


if __name__ == "__main__":
    main()
