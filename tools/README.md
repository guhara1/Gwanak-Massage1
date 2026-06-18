# 색인 통보 도구 (tools/)

검색엔진에 새 글/변경을 가장 빠르게 알리는 스크립트 모음입니다.
모든 스크립트는 저장소 루트의 `sitemap.xml`(빌드 산출물)을 기준으로 동작합니다.

## 0. 빌드 먼저
```bash
python3 build.py
```
- `sitemap.xml`, `rss.xml`, `robots.txt`, IndexNow 키 파일(`<KEY>.txt`)이 생성됩니다.
- 배포(Cloudflare Pages) 후 `https://<도메인>/<KEY>.txt` 가 열려야 IndexNow 인증이 됩니다.

## 1. IndexNow — 빙·네이버·얀덱스 즉시 통보 ✅ 권장
```bash
python tools/indexnow.py                       # 전체 URL 일괄 통보(최초 1회)
python tools/indexnow.py https://도메인/글주소/  # 글 새로 올릴 때마다 그 URL만
```
- 한 번 제출하면 참여 검색엔진에 함께 전파됩니다.
- 별도 설치 불필요(표준 라이브러리).

## 2. 구글 Indexing API — 구글 즉시 통보
구글은 IndexNow 미참여라서 별도 API를 씁니다.
```bash
pip install google-auth google-auth-httplib2 requests
python tools/google_index.py                   # 전체
python tools/google_index.py https://도메인/글/  # 특정 URL
```
준비: ① Indexing API 활성화 ② 서비스 계정 JSON 키를 `tools/google-credentials.json`로 저장
③ 서치콘솔에 서비스 계정 이메일을 **소유자**로 추가. (키 파일은 `.gitignore` 처리됨)

## 3. 사이트맵 핑 (참고용)
```bash
python tools/ping_sitemap.py
```
구글·빙은 무인증 핑을 폐지했습니다. IndexNow + Indexing API 사용을 권장합니다.

## 글 올릴 때 권장 루틴
```bash
python3 build.py
git add -A && git commit -m "새 글" && git push       # 배포
python tools/indexnow.py https://도메인/새글주소/        # 빙·네이버 즉시
python tools/google_index.py https://도메인/새글주소/    # 구글 즉시(선택)
```

## 검색엔진 등록(최초 1회)
- 네이버 서치어드바이저: 사이트 등록 → 소유확인(메인페이지 메타 적용됨) → `sitemap.xml` 제출
- 구글 서치콘솔: 속성 추가 → 소유확인 → `sitemap.xml` 제출
- 빙 웹마스터도구: 서치콘솔에서 가져오기 또는 직접 등록 → `sitemap.xml` 제출
