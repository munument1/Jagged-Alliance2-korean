# JA2 r7609 Korean Patch v0.1.8-alpha

이번 버전은 **BASE SLF 폴백 텍스트 재검수**에서 발견된 누락을 보완하는 런타임 현지화 안정화 릴리스입니다.

## 핵심 수정

- 노트북 보험 사이트 본문이 깨진 문자로 출력되던 문제 수정
  - `Data/BinaryData/INSURANCEMULTI.EDT`
  - `Data/BinaryData/INSURANCESINGLE.EDT`
- BASE SLF에만 존재해 번역 파일이 없으면 원본 데이터로 폴백하던 용병 대사 7개를 한국어 오버라이드로 추가
  - `063.EDT`, `066.EDT`, `067.EDT`, `068.EDT`, `069.EDT`, `070.EDT`, `072.EDT`
- 추가 BASE 웹/문서 리소스 번역
  - `ALUMNAME.EDT` — A.I.M. 동문 이름
  - `CREDITS.EDT` — 크레딧 역할/표제
  - `FILES.EDT` — 인터셉트 수배 문서
  - `FLOWERCARD.EDT` — 꽃집 카드 문구
  - `FLOWERDESC.EDT` — 꽃집 상품명/설명
- 기존 v0.1.7의 BASE/1.13 MercEdt 복구, NPC 번역, EnemyTaunts, 실행 파일 핫픽스는 그대로 유지합니다.

## 특수/레거시 리소스 분류

전체 EDT 대조에서 남은 다음 6개는 일반 고정 레코드 EDT와 형식 또는 런타임 역할이 달라, 누락됐다는 이유만으로 일반 EDT 인코더를 적용하지 않았습니다.

- `MercEdt/200.EDT` — 비표준 형식
- `NPCData/56.EDT` — 비표준 형식
- `BinaryData/BRAYDESC.EDT` — 1.13에서 레거시 계열
- `BinaryData/ITEMDESC.EDT` — 1.13 TableData/XML 계열 사용
- `BinaryData/FLWRDESC.EDT` — 레거시 꽃집 설명 리소스
- `BinaryData/CREDITS_MOD.EDT` — 원본 데이터가 공란

이 파일들은 형식과 실제 r7609 런타임 참조 경로를 별도로 확인한 뒤 필요할 경우 처리합니다.

## QA 강화

- BASE `Data/MercEdt` 필수 최상위 파일 수를 **70 → 77**로 확장
- BASE MercEdt 재귀 검사: **78개(최상위 77 + snitch 1)**
- `Data-1.13/MercEdt`: **74 + snitch 9** 유지
- 새 BASE BinaryData 7개의 파일 크기를 배포 manifest에 고정
- 보험/수배 문서/꽃집/동문 이름 리소스를 영어 잔존 검사 대상에 추가
- `FLOWERDESC.EDT`의 160/160/640 바이트 복합 필드를 별도 스캔
- BASE/1.13 MercEdt 전체 480바이트 레코드 구조와 한글 포함 여부 검사
- Windows에서 충돌할 수 있는 대소문자 중복 경로 검사
- 릴리스 전 `RUNTIME_UNTRANSLATED=0` 자동 검증
- Release ZIP 생성 후 압축 해제본과 빌드 스테이지 비교
- 게시된 GitHub Release ZIP을 다시 내려받아 빌드 ZIP과 바이트 단위 비교

## 호환성

- 대상: **Jagged Alliance 2 v1.13 r7609 영어판**
- 기존 v0.1.7-alpha 설치 환경에서는 `install.bat`으로 덮어설치하는 것을 권장합니다.
- 다른 1.13 리비전이나 별도 모드 조합은 보장하지 않습니다.
