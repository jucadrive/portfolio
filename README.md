# 주현준 백엔드 포트폴리오

HTML, CSS, JavaScript와 자체 제작 SVG로 구성한 정적 사이트입니다. 런타임 서버, 외부 CDN, 폰트 다운로드, npm 설치가 필요하지 않습니다. 홈과 네 개의 프로젝트 상세 페이지는 생성된 HTML로 제공됩니다.

## 로컬 미리보기

이 폴더에서 Python 3로 실행합니다.

```powershell
python -m http.server 4173 --bind 127.0.0.1
```

브라우저에서 [로컬 미리보기](http://127.0.0.1:4173/)를 엽니다. 서버 종료는 실행한 터미널에서 `Ctrl+C`입니다. `index.html`을 직접 열어도 본문·탭·SVG는 동작합니다. HTTP 미리보기는 배포 환경과 비슷한 상대 경로 검증에 권장됩니다.

## 구성

```text
index.html                 소개 / 경험 / 프로젝트 / 기술 / 교육·자격 / 연락처
projects/address.html      배송지 주소 조회 서비스 · 업무
projects/ams.html          AMS · 업무
projects/peaklog.html      PeakLog · 개인
projects/wms-lite.html     WMS-Lite · 개인
assets/style.css           반응형 스타일
assets/main.js             메뉴 / 탭 / 도식 확대
assets/*.svg               자체 제작 흐름도 18개 + favicon
404.html                   없는 페이지 안내
.nojekyll                  Jekyll 처리 비활성화
content.json               편집용 콘텐츠
tools/build.py             정적 HTML·SVG 생성 · Python 표준 라이브러리
tools/validate.py          파일·경로·링크·ARIA·공개 범위 검사
REVIEW.md                  근거와 확인이 필요한 항목
VALIDATION.md              이번 검증 결과와 한계
.github/workflows/pages.yml 수동 실행 전용 배포 워크플로
```

참고 사이트의 홈 타임라인, 카드, 상세 개요와 좌측 기능 메뉴·콘텐츠 패널 구조를 참고했습니다. 참고 인물의 문구·프로젝트·코드·이미지는 가져오지 않았습니다. 참고 주소는 [레이아웃 참고 사이트](https://sherlock0105.github.io/)입니다.

## 콘텐츠 수정

소개와 상세 본문은 개발자 본인의 경험을 채용 담당자에게 설명하는 문장으로 작성합니다. 자료를 읽은 과정, 출처 비교와 확인 한계는 `REVIEW.md`에서 관리하고 웹 본문에 넣지 않습니다.

1. `content.json`의 `profile`에서 이름·소개·연락처·교육을, `projects`에서 프로젝트 내용을 수정합니다.
2. 각 프로젝트의 `features`가 기능 탭이 됩니다. `flow`는 처리 흐름, `problem`·`solution`은 문제와 해결, `decisions`는 선택 이유와 비용, `validation`은 해당 기능의 구현 결과와 테스트입니다.
3. `architecture.nodes`와 `architecture.branch`로 개요 도식을 변경합니다. SVG는 텍스트와 화살표로 자동 생성합니다.
4. 아래 명령으로 다시 생성하고 점검합니다.

```powershell
python tools/build.py
python tools/validate.py
```

생성되는 HTML과 처리 흐름 SVG를 직접 수정하면 재생성할 때 덮어씁니다. 스타일은 `assets/style.css`, 동작은 `assets/main.js`, 공통 화면 구조는 `tools/build.py`에서 수정합니다. 현재 도식 생성기는 네 단계의 흐름을 기준으로 합니다.

`repository`는 **사용자가 제공한 실제 개인 저장소 URL**이 확인된 경우에만 추가합니다. 현재 WMS-Lite에 제공된 HomeLab URL만 사용했고 PeakLog에는 버튼이 없습니다. 업무 프로젝트에는 저장소 버튼을 넣지 않습니다. 새 URL을 추가할 경우 검사기의 허용 목록도 함께 검토합니다.

구현 완료·실험 중·향후 계획을 구분하고, 업무 수치와 개인 프로젝트의 실험 수치는 근거와 측정 조건을 유지하세요. 측정 환경과 근거 없이 담당 비율, 사용자 규모, 성능 수치를 추가하지 마세요. 자세한 범위는 `REVIEW.md`를 참고하세요.

## GitHub Pages 배포

이번 작업에서는 저장소 생성, 원격 푸시, 워크플로 실행, 공개 배포를 하지 않았습니다. 포함된 워크플로는 **수동 실행만 가능**하며 푸시만으로 배포하지 않습니다.

이 사이트 폴더만 별도 GitHub 저장소의 루트에 넣는 방식을 권장합니다. 업무 자료나 참고 프로젝트를 함께 올리지 마세요. 상위 작업 폴더 전체를 저장소로 공개하는 방식은 사용하지 않습니다.

1. 공개 내용을 검토한 뒤 별도 저장소에 사이트 소스만 올립니다. 이름이 `<사용자명>.github.io`이면 사용자 사이트, 그 외 이름이면 저장소 하위 경로의 프로젝트 사이트가 됩니다.
2. GitHub 저장소의 **Settings → Pages → Build and deployment → Source → GitHub Actions**를 선택합니다.
3. **Actions → Publish reviewed portfolio to GitHub Pages → Run workflow**를 직접 실행합니다.
4. 워크플로는 콘텐츠 재생성·정적 검사 후, 아래 허용 목록만 배포합니다. Pages의 기본 경로는 자동으로 전달되므로 프로젝트 사이트에서도 링크와 404 홈 복귀가 동작합니다.
5. 표시된 Pages URL에서 홈 → 상세 → 다른 상세 → 홈, 기능 탭, 도식 확대와 모바일 메뉴를 다시 확인합니다.

워크플로 파일은 이 사이트가 저장소 루트인 구성을 전제로 합니다. 상위 저장소 아래의 폴더로 배포하려면 모든 `run` 명령의 작업 디렉터리와 artifact 경로를 그 폴더에 맞게 지정해야 합니다. 원본 자료를 제외하는 허용 목록은 유지하세요.

브랜치 직접 배포를 원하면 웹 파일만 올린 별도 배포 브랜치의 루트를 Pages의 source로 선택할 수 있습니다. 프로젝트 사이트라면 `python tools/build.py --base-path /저장소이름/`으로 404 홈 링크를 생성합니다. 일반 페이지·CSS·JS·SVG 링크는 상대 경로이므로 기본 경로를 하드코딩하지 않습니다.

[GitHub 공식 배포 워크플로 문서](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)를 기준으로 작성했습니다.

## 공개 예정 파일

웹사이트 배포 대상은 다음만 포함합니다.

- `index.html`, `404.html`, `.nojekyll`
- `projects/`의 HTML 네 개
- `assets/`의 CSS, JavaScript, 자체 제작 SVG 19개

별도 소스 저장소를 공개하면 `content.json`, `tools/`, `README.md`, `REVIEW.md`, `VALIDATION.md`, `.gitignore`, `.github/workflows/pages.yml`도 열람 가능하므로 함께 검토하세요. 이 파일들에도 업무 원문·비밀 설정·운영 데이터·비공개 주소·로컬 절대 경로를 넣지 않았습니다.

`.local/`의 검증 화면, `_public/`, 로그와 Python 캐시는 저장소에 올리지 않으며 배포 artifact에서도 제외합니다. 공개용 이력서·PDF 원본, 개인 참고 프로젝트의 코드·설정은 복사하지 않았습니다. 이름과 이메일은 제공된 이력서에서 반영했으며 휴대전화·주소·사진·생년은 넣지 않았습니다.

## 검증 범위

```powershell
python tools/validate.py
```

HTML 링크·앵커·이미지·SVG 구문, 탭과 패널 연결, 업무 저장소 링크 금지, 외부 저장소 URL 허용 목록, 파일 종류와 대표적인 비밀값·내부 주소·로컬 경로 패턴을 검사합니다. 정규식 검사만으로 모든 비공개 정보를 판단할 수 없으므로 문구도 직접 검토했습니다. 이번 브라우저 검증의 크기와 결과는 `VALIDATION.md`에 기록했습니다.

백엔드 참고 프로젝트의 테스트는 실행하지 않았습니다. 참고 코드·설정·Git 상태를 변경하지 않기 위해 테스트 내용을 읽고 기존 실행 기록과 이번 확인을 구분했습니다.
