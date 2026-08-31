# JA2 r7609 Korean Patch v0.1.7-alpha

이번 릴리스는 I.M.P. 용병 대사 문제를 계기로 BASE 런타임 대사 파일을 다시 전수 대조해, 배포 패치에서 빠진 `MercEdt` 번역 파일을 복구하는 알파 핫픽스입니다.

## 핵심 변경

### BASE MercEdt 전체 세트 복구

- 먼저 `Patch/Data/MercEdt/051.EDT` ~ `056.EDT`를 복구해 남성 I.M.P. 프로필 51~53과 여성 I.M.P. 프로필 54~56의 한국어 전투 대사를 패키지에 포함했습니다.
- 이후 원본 번역 데이터와 `Patch/Data/MercEdt`를 다시 전수 대조한 결과, **43개 파일이 추가로 누락**되어 있음을 확인했습니다.
- 누락된 43개 파일을 모두 복구해 최종적으로 BASE `MercEdt` **70개 파일 전체**를 배포 패치에 포함했습니다.
- `017.edt`처럼 원본에서 확장자 대소문자가 다른 파일도 별도로 확인해 `017.EDT`로 정상 포함했습니다.
- 각 파일의 실제 바이트 크기와 480바이트 고정 레코드 구조를 검사하고, 복호화 후 한국어 문자열이 존재하는지 확인했습니다.

### 잔여 영어/혼합 표기 정리

재검수 과정에서 활성 런타임 대사에 남아 있던 항목도 함께 정리했습니다.

- `055.EDT` 67번: `It appears there's been a theft here. Stuff's missing.` → `여기 도둑이 든 것 같아요. 물건이 없어졌어요.`
- `009.EDT` 34번: 영어 문장을 한국어로 번역
- `024.EDT` 39번: `Hasta la vista, 엄마.` → `아스타 라 비스타, 베이비.`
- `025.EDT` 109번: `Charlene Higgens.` → `샬린 히긴스.`

## 2차 전수검수

누락 복구 후 원본 번역 데이터, 현재 `main`, 실제 GitHub Release ZIP을 다시 대조했습니다.

- BASE `Data/MercEdt`: 최상위 **70 / 70**, 누락 0, 추가 0, 원본 파일 크기 일치
- BASE `Data/MercEdt/snitch`: **1 / 1**
- `Data-1.13/MercEdt`: 최상위 **74 / 74**, 누락 0, 추가 0, 원본 파일 크기 일치
- `Data-1.13/MercEdt/snitch`: **9 / 9**
- `Data/BinaryData`: 번역 대상 EDT **8 / 8**
- `Data-1.13/BinaryData`: 번역 대상 EDT **3 / 3**
- `Data-1.13/NpcData`: 번역 EDT `159.EDT`, `229.EDT` **2 / 2**
- BASE 원본의 구형 `Data/NPCData/159.EDT`는 r7609 VFS에서 더 높은 우선순위의 `Data-1.13/NpcData/159.EDT`가 사용되므로 배포 필수 목록에서 제외했습니다.
- BASE/1.13 MercEdt 전체를 하위 `snitch` 폴더까지 재귀 검사해 480바이트 고정 레코드 구조와 한국어 문자열 존재를 확인했습니다.
- `Data`와 `Data-1.13`에 동시에 존재하는 MercEdt **11개**의 VFS 중복 목록도 고정 검증합니다.
- EnemyTaunts는 `Data`와 `Data-1.13`의 **29개 XML**이 동일하며 검열 태그/텍스트 구조가 정상임을 다시 확인했습니다.
- BASE civilian EDT 필수 세트 **41개**도 기존 런타임 QA를 통과했습니다.
- 실제 배포 ZIP을 다시 내려받아 압축 해제한 뒤 `Patch`, `README.md`, 릴리즈 노트, 설치기 파일이 현재 저장소와 동일함을 비교했습니다.

## 자동 검증 강화

- `tools/verify_localization_package.py`를 추가해 BASE/1.13 MercEdt, `snitch`, BinaryData, NPCData의 파일 수·크기·구조와 VFS 중복을 상시 검사합니다.
- `Runtime dialogue QA`가 위 패키지 검증을 함께 실행하도록 강화했습니다.
- 릴리즈 워크플로는 ZIP을 만든 뒤 다시 압축 해제해 스테이징 파일과 일치하는지 확인합니다.
- 업로드한 GitHub Release ZIP도 다시 다운로드해 빌드 산출물과 바이트 단위로 비교합니다.
- 기존 릴리즈를 갱신할 때 `v0.1.7-alpha` Git 태그도 검증된 `main` 커밋으로 강제 동기화해 GitHub의 자동 Source code ZIP/TAR가 과거 커밋을 가리키지 않도록 수정했습니다.

## 검증 결과

- `tools/verify_localization_package.py` 통과
- `tools/check_runtime_dialogue.py` 통과
- `tools/verify_runtime_dialogue_zero.py` 통과
- 최종 판정: `RUNTIME_UNTRANSLATED=0`
- BASE `MercEdt`: **70 / 70** + `snitch` **1 / 1**
- 1.13 `MercEdt`: **74 / 74** + `snitch` **9 / 9**
- 실제 릴리즈 ZIP ↔ 현재 패치 파일 비교 통과
- EDT 파일 크기 및 레코드 구조 검사 통과
- EDT 복호화 후 한국어 문자열 확인

## 기존 v0.1.6-alpha 수정 유지

이번 패키지는 누적 배포판입니다. v0.1.6-alpha의 다음 수정도 그대로 포함합니다.

- I.M.P. 한글 이름/별명 입력 지원
- Fleuropa 꽃집 배송지 클릭 영역 수정
- 기존 한국어 UI/WinFont 수정
- BASE NPC, MercEdt, EnemyTaunts, AIM/IMP/퀘스트/RIS 번역
- Galmuri 한국어 글꼴 설정 및 설치기

`Patch/ja2.exe`는 v0.1.6-alpha와 동일합니다.

- 크기: `8,407,552 bytes`
- SHA-256: `a3480fd92a6c5e4e184b367cf29705d52b8b129a616c6a6a80affd062ee77582`

## 설치

대상 버전은 **Jagged Alliance 2 v1.13 r7609 영어판**입니다.

1. `JA2_r7609_Korean_Patch_v0.1.7-alpha.zip`을 압축 해제합니다.
2. `install.bat`, `install.ps1`, `Patch` 폴더를 JA2 r7609 설치 폴더로 복사합니다.
3. `ja2.exe`와 `Ja2.ini`가 있는 게임 폴더에서 `install.bat`을 실행합니다.
4. 기존 실행 파일과 INI는 설치기가 자동으로 백업합니다.

## 확인 권장

데이터, 패키지, 자동 QA는 통과했습니다. 실제 게임에서는 여러 AIM/MERC 및 남성·여성 I.M.P. 용병을 사용하면서 상황별 전투 대사가 정상 한국어로 표시되는지 추가 확인을 권장합니다.

다른 JA2 1.13 리비전이나 대규모 모드 조합에서는 호환성을 보장하지 않습니다.
