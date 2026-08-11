# JA2 r7609 Korean Patch v0.1.3-alpha

이번 릴리스는 게임 플레이 중 보고된 **영문 런타임 대사 잔여분을 제거하는 데 집중한 알파 업데이트**입니다.

## 핵심 수정

- 실제 런타임 EDT 전수 감사에서 발견된 미번역 대사 **239개를 한국어로 교체**했습니다.
  - `Data/MercEdt/017.edt`: 105개
  - `Data-1.13/MercEdt/251.EDT`: 44개
  - `Data-1.13/MercEdt/252.EDT`: 48개
  - snitch 대사: 15개
  - `Data/MercEdt/032.EDT`: 11개
  - `Data/MercEdt/149.EDT`: 11개
  - `175/181/187.EDT`: 4개
  - `MERCBIOS.EDT` John Kulba 소개: 1개
- 기존 `Data`에만 있던 한국어 용병 EDT 11개를 `Data-1.13/MercEdt`에도 동일하게 배치해 상위 VFS에서 영어 원본이 선택될 가능성을 제거했습니다.
- 적군 전투 대사 `EnemyTaunts*.xml` 29개를 `Data`와 `Data-1.13` 양쪽에 동일하게 배치했습니다.
- 잘못된 `szTextCensored` 태그와 중복 `szText` 구조를 정식 `szCensoredText` 구조로 수정했습니다.
- 초기 작업 중 생성됐던 가짜 주민 대사 `civ*.edt` placeholder 479개를 제거했습니다.
- 실제 한국어 주민 대사가 들어 있는 `civ52.edt`는 보존했습니다.
- `NpcData/229.EDT`는 480-byte 레코드 형식으로 별도 검증했으며 기존 27개 대사가 모두 한국어임을 확인했습니다.

## 최종 QA

릴리스 소스에서 다음 범위를 실제 JA2 EDT 복호화 규칙으로 다시 읽어 검사합니다.

- `Data/MercEdt`
- `Data-1.13/MercEdt`
- `Data/NPCData`
- `Data-1.13/NpcData`
- `Data-1.13/BinaryData/MERCBIOS.EDT`
- `Data/TableData/EnemyTaunts`
- `Data-1.13/TableData/EnemyTaunts`

현재 자동 검증 결과: **`RUNTIME_UNTRANSLATED=0`**

## 설치

대상 버전은 **Jagged Alliance 2 v1.13 r7609**입니다.

이전 알파 버전을 설치한 적이 있다면 단순 수동 덮어쓰기보다 릴리스에 포함된 `install.ps1` 사용을 권장합니다. 설치기가 과거 버전에 남아 있을 수 있는 가짜 CIV placeholder 파일을 식별해 정리합니다.

`Data-UB`는 기본 JA2 r7609용 패치에 포함하지 않습니다.

## 주의

이번 `RUNTIME_UNTRANSLATED=0` 판정은 현재 패치에서 실제로 활성화되는 **용병/NPC/주민/적군 전투 대사 계열**에 대한 자동 감사 결과입니다. 새로운 외부 리소스나 다른 모드가 추가되면 별도 번역이 필요할 수 있습니다.
