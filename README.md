# Jagged Alliance 2 v1.13 r7609 한국어 패치

Jagged Alliance 2 v1.13 **r7609 영어판**용 한국어 패치입니다.

현재 패치에는 r7609 내장 UI 한국어 실행 파일, `Data`/`Data-1.13` 한국어 XML·EDT 데이터, AIM/IMP/동문회/기록 일지/퀘스트/RIS 및 노트북 웹사이트 번역, 한국어 메인 메뉴 로고, Galmuri 비트맵 글꼴이 포함됩니다.

## 설치 방법

### 권장 설치 — `install.bat`

1. GitHub Releases에서 `JA2_r7609_Korean_Patch_v0.1.8-alpha.zip`을 받습니다.
2. ZIP을 압축 해제합니다.
3. `install.bat`, `install.ps1`, `Patch` 폴더를 JA2 v1.13 r7609 설치 폴더, 즉 `ja2.exe`와 `Ja2.ini`가 있는 폴더로 복사합니다.
4. 게임이 실행 중이면 종료합니다.
5. 게임 폴더의 `install.bat`을 실행합니다.
6. `Installation completed successfully.`가 표시되면 `ja2.exe`를 실행합니다.

`Program Files`처럼 쓰기 권한이 제한된 위치라면 `install.bat`을 관리자 권한으로 실행하세요.

자동 설치기는 기존 `ja2.exe`와 `Ja2.ini`를 백업하고, `Patch`의 한국어 파일을 알맞은 위치에 덮어쓰며, 과거 알파 버전이 남긴 삭제 대상 파일과 VFS 우선순위 문제를 정리합니다. 이전 알파 버전을 사용했다면 단순 수동 덮어쓰기보다 자동 설치기를 권장합니다.

### 수동 설치

`Patch` 폴더 **안의 내용물**을 게임 설치 폴더에 복사하여 기존 `Data`, `Data-1.13`, `ja2.exe`, `Ja2.ini`와 병합합니다. 수동 설치 전 기존 실행 파일과 INI를 직접 백업하세요.

## v0.1.8-alpha — BASE SLF 폴백 텍스트 보완

v0.1.7에서 BASE `MercEdt`를 복구한 뒤, 이번 버전에서는 **Loose Data에 없어서 BaseSLF로 폴백하는 텍스트 리소스까지 다시 추적**했습니다.

- 보험 사이트 본문 깨짐 수정: `INSURANCEMULTI.EDT`, `INSURANCESINGLE.EDT`
- BaseSLF 전용 용병 대사 7개 추가: `063`, `066`, `067`, `068`, `069`, `070`, `072.EDT`
- A.I.M. 동문 이름: `ALUMNAME.EDT`
- 인터셉트 수배 문서: `FILES.EDT`
- 꽃집 카드/상품 설명: `FLOWERCARD.EDT`, `FLOWERDESC.EDT`
- 크레딧 역할/표제: `CREDITS.EDT`

검증기도 함께 고쳐서 새 파일이 다음 배포에서 다시 빠지면 CI가 실패하도록 했습니다. 보험/수배 문서/꽃집/동문 이름은 영어 잔존 검사에도 포함됩니다.

`MercEdt/200.EDT`, `NPCData/56.EDT`처럼 일반 고정 레코드 EDT가 아닌 파일과, 1.13에서 XML/TableData 계열로 대체된 레거시 파일은 무작정 패치에 넣지 않고 별도 분류합니다.

상세 내용은 `RELEASE_NOTES_v0.1.8-alpha.md`를 참고하세요.

## v0.1.7-alpha — BASE 용병 대사 배포 누락 복구

- I.M.P. 프로필 `051.EDT`~`056.EDT` 복구
- BASE `MercEdt` 누락 파일 전수 복구
- 당시 Loose Data 기준 BASE MercEdt 최상위 70개 + `snitch/023.EDT` 검증
- `Data-1.13/MercEdt` 최상위 74개 + snitch 9개 검증
- 용병 대사의 480바이트 레코드 구조와 한글 문자열 검사
- EnemyTaunts 및 활성 런타임 대사의 영어 잔존 검사 강화

v0.1.8은 이 검사를 BaseSLF 폴백 리소스까지 확장한 버전입니다.

## v0.1.6-alpha — 런타임 핫픽스

- I.M.P. 캐릭터 생성 화면의 한글 이름/별명 입력 지원
- Fleuropa 꽃집 배송지 드롭다운 클릭 영역 보정
- 기존 한국어 실행 파일과 WinFont 수정사항 유지
- r7609 실행 파일 검증 SHA-256: `a3480fd92a6c5e4e184c367cf29705d52b8b129a616c6a6a80affd062ee77582`

## v0.1.4-alpha — BASE NPC 대사 완성

- BASE NPCData 한국어판 재구성
- 실제 영문 대사 3,233개 번역
- 원래 공란인 201개 레코드 보존
- 고정 레코드 크기와 전체 파일 크기 검증 및 역복호화 비교

## 런타임 대사/문서 리소스

- 용병 대사: `MercEdt/*.edt`
- 주민/NPC 대사: `NPCData/*.edt`, `CIV*.edt`, 섹터별 EDT
- 적군 전투 대사: `TableData/EnemyTaunts/*.xml`
- 용병 소개: `BinaryData/MERCBIOS.EDT`
- 노트북 웹/문서: `BinaryData/*.EDT`

저장소의 QA 도구는 패치에 포함된 활성 리소스의 구조, 파일 수, VFS 중복, 한글 포함 여부와 영어 잔존을 검사합니다. 별도 모드가 외부 데이터를 추가하면 그 리소스는 검사 범위 밖일 수 있습니다.

## 알려진 사항

- Windows 창 모드는 16비트 색상 표면을 요구하므로 환경에 따라 DirectDraw 오류가 날 수 있습니다. 문제가 있으면 전체 화면 실행을 먼저 권장합니다.
- 다른 JA2 1.13 리비전이나 별도 모드 조합의 호환성은 보장하지 않습니다.

## 글꼴

한국어 표시에 [Galmuri](https://github.com/quiple/galmuri)를 사용합니다. 글꼴 라이선스는 `Patch/Data/Fonts/LICENSE_GALMURI.md`를 참고하세요.
