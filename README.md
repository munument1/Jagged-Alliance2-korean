# Jagged Alliance 2 v1.13 r7609 한국어 패치

Jagged Alliance 2 v1.13 **r7609 영어판**을 대상으로 제작 중인 한국어 패치입니다.

현재 저장소에는 다음 항목이 포함됩니다.

- r7609 내장 UI 한국어 실행 파일
- `Data`, `Data-1.13`의 한국어 XML/EDT 데이터
- AIM, IMP, 동문회, 기록 일지, 퀘스트, RIS 문서 번역
- 한국어 메인 메뉴 로고
- 유니코드 한글 출력을 위한 Galmuri 비트맵 글꼴

## 설치

1. Jagged Alliance 2 v1.13 r7609 영어판을 준비합니다.
2. 게임을 종료합니다.
3. 릴리즈 ZIP의 압축을 풉니다.
4. 압축을 푼 폴더의 `Patch`, `install.bat`, `install.ps1`을 **`ja2.exe`가 있는 게임 설치 폴더에 놓습니다.**
5. 게임 설치 폴더에서 **`install.bat`을 더블클릭**합니다.

`install.bat`은 자신이 있는 현재 폴더를 자동으로 JA2 설치 경로로 사용하므로 별도의 경로 입력이 필요하지 않습니다. `ja2.exe`, `Ja2.ini`, `Patch` 폴더가 모두 있는지 먼저 확인한 뒤 PowerShell 설치기를 실행합니다.

자동 설치기는 기존 `ja2.exe`와 `Ja2.ini`를 타임스탬프가 붙은 파일로 백업한 뒤 `Patch`의 내용을 게임 폴더에 복사하고 한국어 글꼴 설정을 갱신합니다. 또한 이전 알파에서 설치된 것으로 확인되는 CIV 더미 EDT만 식별하여 제거하고, EnemyTaunts 번역 파일을 r7609의 `Data-1.13` 우선 VFS 계층에도 배치합니다.

게임이 `Program Files` 아래에 있어 쓰기 권한 오류가 발생하면 `install.bat`을 우클릭해 **관리자 권한으로 실행**하세요.

수동 설치가 필요하면 `Patch` 안에 있는 `Data`, `Data-1.13`, `ja2.exe`, `Ja2.ini`를 게임 설치 폴더에 그대로 복사하고 덮어쓸 수도 있습니다. 다만 이전 알파의 삭제 대상 파일은 남을 수 있으므로 업그레이드 설치에는 `install.bat` 사용을 권장합니다.

기존 `ja2.exe`와 `Ja2.ini`는 자동 설치 시 백업됩니다. 릴리즈의 `Ja2.ini`는 한국어 글꼴과 전체 화면 실행이 이미 설정되어 있습니다.

`v0.1.1-alpha`부터 r7609 실행 파일이 요구하는 INI 기본값을 함께 제공하므로, 이전 알파에서 나타났던 시작 화면의 붉은 INI 경고 없이 실행할 수 있습니다.

## v0.1.3-alpha 런타임 대사 수정

실제 게임이 읽는 EDT/XML을 다시 복호화·파싱해 기존 패치에서 영어로 남아 있던 런타임 대사를 전수 감사했습니다.

- 실제 미번역 런타임 대사 **239개를 한국어로 교체**했습니다.
- `Data/MercEdt`에만 있던 한국어 용병 EDT 11개를 `Data-1.13/MercEdt`에도 동일하게 배치해 상위 VFS에서 영어 원본이 다시 선택되는 문제를 막았습니다.
- 적군 전투 대사 `EnemyTaunts*.xml` 29개를 `Data`와 `Data-1.13` 양쪽에 동일하게 배치했습니다.
- 잘못된 `szTextCensored` 태그와 중복 `szText`를 정식 `szCensoredText` 구조로 수정했습니다.
- 초기 작업에서 생성됐던 가짜 주민 대사 `civ*.edt` placeholder 479개를 제거했습니다.
- 실제 한국어 주민 대사가 들어 있는 `civ52.edt`는 보존했습니다.
- `NpcData/229.EDT`는 별도 480-byte 레코드 형식으로 확인했으며 27개 대사가 모두 한국어였습니다.

자동 QA는 `MercEdt`, `NPCData`, `MERCBIOS.EDT`, `EnemyTaunts`를 실제 런타임 형식으로 검사하며 **`RUNTIME_UNTRANSLATED=0`**을 통과해야 합니다.

상세 변경 사항은 `RELEASE_NOTES_v0.1.3-alpha.md`를 참고하세요.

## 런타임 대사 리소스

- 용병 대사: `MercEdt/*.edt`
- 주민/NPC 대사: `NPCData/*.edt`, `CIV*.edt`, 섹터별 EDT
- 적군 전투 대사: `TableData/EnemyTaunts/*.xml`
- 용병 소개: `BinaryData/MERCBIOS.EDT`

이번 릴리스의 `RUNTIME_UNTRANSLATED=0` 판정은 위의 현재 활성 런타임 대사 계열을 대상으로 합니다. 다른 모드나 별도 외부 리소스를 추가하면 그쪽에 영어가 남아 있을 수 있습니다.

## 알려진 사항

- Windows 창 모드는 16비트 색상 표면을 요구해 환경에 따라 DirectDraw 오류가 날 수 있습니다. 우선 전체 화면으로 실행하는 것을 권장합니다.
- UI 배치와 추가 콘텐츠는 계속 검수 중입니다.
- 다른 JA2 1.13 리비전이나 다른 모드 조합에서는 호환성을 보장하지 않습니다.

## 글꼴

한국어 표시에 [Galmuri](https://github.com/quiple/galmuri)를 사용합니다. 글꼴 라이선스는 `Patch/Data/Fonts/LICENSE_GALMURI.md`를 참고하세요.
