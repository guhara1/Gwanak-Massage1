#!/usr/bin/env python3
"""구글 Indexing API 즉시 색인 통보.

구글은 IndexNow 에 참여하지 않으므로, 구글에 즉시 통보하려면 이 API 를 쓴다.
공식 지원 범위는 JobPosting·BroadcastEvent 이지만, URL_UPDATED 통보는 일반
페이지에도 색인 발견을 앞당기는 데 실무적으로 쓰인다.

준비물:
  1) Google Cloud 프로젝트에서 "Indexing API" 활성화
  2) 서비스 계정 생성 → JSON 키 다운로드 → tools/google-credentials.json 로 저장
     (이 파일은 .gitignore 에 포함되어 커밋되지 않음)
  3) 서치콘솔에서 해당 서비스 계정 이메일을 사이트 '소유자'로 추가
  4) 의존성 설치:
       pip install google-auth google-auth-httplib2 requests

사용법:
    python tools/google_index.py                 # sitemap.xml 전체
    python tools/google_index.py URL [URL ...]    # 지정 URL만
    python tools/google_index.py --delete URL     # 색인 삭제 통보(URL_DELETED)
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRED = os.path.join(os.path.dirname(os.path.abspath(__file__)), "google-credentials.json")
SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"


def sitemap_urls():
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        sys.exit("sitemap.xml 이 없습니다. 먼저 `python3 build.py` 를 실행하세요.")
    with open(path, encoding="utf-8") as f:
        return re.findall(r"<loc>([^<]+)</loc>", f.read())


def main():
    args = sys.argv[1:]
    notif = "URL_UPDATED"
    if "--delete" in args:
        notif = "URL_DELETED"
        args = [a for a in args if a != "--delete"]
    urls = args or sitemap_urls()

    if not os.path.exists(CRED):
        sys.exit(
            f"서비스 계정 키가 없습니다: {CRED}\n"
            "  1) Indexing API 활성화 → 서비스 계정 JSON 키 생성\n"
            "  2) tools/google-credentials.json 로 저장\n"
            "  3) 서치콘솔에 서비스 계정 이메일을 소유자로 추가"
        )
    try:
        from google.oauth2 import service_account
        import google.auth.transport.requests
        import requests
    except ImportError:
        sys.exit("의존성 필요: pip install google-auth google-auth-httplib2 requests")

    creds = service_account.Credentials.from_service_account_file(CRED, scopes=SCOPES)
    creds.refresh(google.auth.transport.requests.Request())
    headers = {"Authorization": f"Bearer {creds.token}",
               "Content-Type": "application/json"}

    ok = 0
    # 일별 쿼터(기본 200) 주의
    for url in urls:
        body = {"url": url, "type": notif}
        r = requests.post(ENDPOINT, json=body, headers=headers, timeout=30)
        tag = "OK " if r.status_code == 200 else f"{r.status_code}"
        print(f"  {tag} {url}")
        if r.status_code == 200:
            ok += 1
    print(f"\n{ok}/{len(urls)} 통보 완료 ({notif}).")


if __name__ == "__main__":
    main()
