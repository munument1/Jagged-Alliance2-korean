# Jagged Alliance 2 v1.13 r7609 한국어 패치

Jagged Alliance 2 v1.13 **r7609 영어판**을 대상으로 제작 중인 한국어 패치입니다.

현재 저장소에는 다음 항목이 포함됩니다.

- r7609 내장 UI 한국어 실행 파일
- `Data`, `Data-1.13`의 한국어 XML/EDT 데이터
- AIM, IMP, 동문회, 기록 일지, 퀘스트, RIS 문서 번역
- 한국어 메인 메뉴 로고
- 유니코드 한글 출력을 위한 Galmuri 비트맵 글꼴

# 설치 방법

## 권장 설치 — install.bat 더블클릭

1. GitHub Releases에서 `JA2_r7609_Korean_Patch_v0.1.7-alpha.zip`을 다운로드합니다.
2. ZIP의 압축을 풉니다.
3. 압축을 풀면 다음과 같은 구조가 나옵니다.

```text
JA2_r7609_Korean_Patch_v0.1.7-alpha\
├─ install.bat
├─ install.ps1
├─ Patch\
├─ README.md
└─ RELEASE_NOTES_v0.1.7-alpha.md
```

4. **`install.bat`, `install.ps1`, `Patch` 폴더**를 Jagged Alliance 2 v1.13 r7609 설치 폴더로 복사합니다.
5. 설치 폴더는 **`ja2.exe`와 `Ja2.ini`가 들어 있는 폴더**입니다.

예시:

```text
D:\Games\Jagged Alliance 2\
├─ ja2.exe
├─ Ja2.ini
├─ install.bat
├─ install.ps1
├─ Patch\
├─ Data\
└─ Data-1.13\
```

6. Jagged Alliance 2가 실행 중이라면 종료합니다.
7. 위 게임 폴더에서 **`install.bat`을 더블클릭**합니다.
8. 게임 경로를 따로 입력할 필요는 없습니다. BAT가 자신이 있는 폴더를 자동으로 게임 설치 경로로 사용합니다.
9. 설치가 정상적으로 끝나면 `Installation completed successfully.` 메시지가 표시됩니다.
10. 설치 창을 닫고 `ja2.exe`를 실행합니다.

### 권한 오류가 나는 경우

게임이 `Program Files`처럼 쓰기 권한이 제한되는 위치에 설치되어 있다면 `install.bat`을 우클릭하고 **관리자 권한으로 실행**하세요.

### 자동 설치기가 하는 일

- 현재 폴더에 `ja2.exe`, `Ja2.ini`, `Patch`가 있는지 확인
- 기존 `ja2.exe`와 `Ja2.ini`를 타임스탬프가 붙은 백업 파일로 보존
- `Patch` 안의 한국어 파일을 게임 폴더에 덮어쓰기
- 이전 알파 버전이 남긴 가짜 CIV placeholder EDT만 선별 제거
- EnemyTaunts 번역 파일을 `Data-1.13` 우선 VFS 계층에도 적용
- Galmuri 한국어 글꼴 설정 적용

**이전 알파 버전을 설치한 적이 있다면 `install.bat` 사용을 특히 권장합니다.** 일반적인 파일 덮어쓰기만으로는 예전 알파에서 생성된 삭제 대상 파일이 남을 수 있습니다.

## 수동 설치

BAT를 사용하지 않으려면 압축을 푼 뒤 `Patch` 폴더 **안의 내용물**을 JA2 r7609 설치 폴더로 복사하고 덮어씁니다.

```text
Patch\
├─ Data\
├─ Data-1.13\
├─ ja2.exe
└─ Ja2.ini
```

즉 `Patch` 폴더 자체를 게임 폴더 안에 넣는 것이 아니라, **`Patch` 안의 `Data`, `Data-1.13`, `ja2.exe`, `Ja2.ini`가 기존 게임 폴더의 같은 항목과 합쳐지도록 복사**하면 됩니다.

수동 설치 전에는 기존 `ja2.exe`와 `Ja2.ini`를 직접 백업하는 것을 권장합니다. 이전 알파 설치 환경은 구형 CIV 더미 파일이 남을 수 있으므로 수동 설치보다는 `install.bat`을 권장합니다.

`v0.1.1-alpha`부터 r7609 실행 파일이 요구하는 INI 기본값을 함께 제공하므로, 이전 알파에서 나타났던 시작 화면의 붉은 INI 경고 없이 실행할 수 있습니다.

## v0.1.7-alpha BASE 용병 대사 배포 누락 복구

v0.1.7-alpha에서는 I.M.P. 대사 문제를 계기로 BASE `Data/MercEdt`를 원본 번역 데이터와 다시 전수 대조했습니다.

- I.M.P. 프로필 `051.EDT` ~ `056.EDT`를 복구했습니다.
- 이후 재검수에서 BASE `MercEdt` 파일 **43개가 추가로 배포 패치에서 누락**된 것을 확인해 모두 복구했습니다.
- 최종적으로 원본 번역 데이터의 BASE `MercEdt` **70개 파일 전체**가 `Patch/Data/MercEdt`에 포함됩니다.
- 누락 파일의 크기와 480바이트 고정 레코드 구조를 검사하고, EDT 복호화 후 한국어 문자열이 정상적으로 들어 있는지 확인했습니다.
- 재검수 중 남아 있던 영어/혼합 표기 3건(`009.EDT`, `024.EDT`, `025.EDT`)과 기존 `055.EDT` 영어 대사 1건도 정리했습니다.
- 전체 활성 런타임 대사 검사 결과는 `RUNTIME_UNTRANSLATED=0`입니다.

### v0.1.7 2차 전수검수

누락 복구 후 배포 파일을 다시 한 번 원본 번역 데이터와 대조했습니다.

- BASE `MercEdt`: 최상위 **70 / 70**, `snitch` **1 / 1**
- `Data-1.13/MercEdt`: 최상위 **74 / 74**, `snitch` **9 / 9**
- `Data/BinaryData` 번역 EDT: **8 / 8**
- `Data-1.13/BinaryData` 번역 EDT: **3 / 3**
- `Data-1.13/NpcData`: 번역 EDT `159.EDT`, `229.EDT` **2 / 2**
- BASE 원본의 구형 `Data/NPCData/159.EDT`는 r7609 VFS에서 더 높은 우선순위의 `Data-1.13/NpcData/159.EDT`가 대신 사용되므로 배포 필수 파일에서 제외합니다.
- BASE/1.13 `MercEdt` 전체를 재귀 검사해 480바이트 레코드 구조와 한국어 문자열을 확인했습니다.
- `Data`와 `Data-1.13`에 함께 존재하는 MercEdt 11개도 VFS 중복 목록을 고정해 예기치 않은 덮어쓰기를 검사합니다.
- 실제 GitHub Release ZIP을 다시 내려받아 압축 해제한 뒤 `Patch`, README, 릴리즈 노트, 설치기가 현재 `main`과 동일한지 비교합니다.
- `tools/verify_localization_package.py`를 추가해 이후 커밋과 릴리즈에서도 위 파일 수·크기·구조를 자동 검사합니다.
- 릴리즈 워크플로는 기존 릴리즈를 갱신할 때도 `v0.1.7-alpha` Git 태그를 검증된 `main` 커밋과 동기화합니다.

상세 변경 사항은 `RELEASE_NOTES_v0.1.7-alpha.md`를 참고하세요.

## v0.1.6-alpha 런타임 핫픽스

이번 버전에서는 기존 한국어 실행 파일의 번역과 WinFont 수정사항을 유지한 채 두 가지 런타임 문제를 보정했습니다.

- I.M.P. 캐릭터 생성 화면에서 한글 이름과 별명을 입력할 수 있도록 Unicode 입력 필터 수정
- Fleuropa 꽃집 배송지 드롭다운의 클릭 영역을 WinFont 표시 영역에 맞게 확대
- Meduna / Deidranna 꽃다발 이스터에그 로직은 기존 r7609 데이터 그대로 유지
- 최종 `ja2.exe` SHA-256: `a3480fd92a6c5e4e184b367cf29705d52b8b129a616c6a6a80affd062ee77582`
- r7609 기준 소스와 재현 가능한 소스/바이너리 패치 도구를 저장소에 보존

상세 변경 사항은 `RELEASE_NOTES_v0.1.6-alpha.md`와 `R7609_SOURCE_RECOVERY.md`를 참고하세요.

## v0.1.4-alpha BASE NPC 대사 완성

기존 v0.1.3-alpha의 런타임 용병/적군 대사 수정에 이어, r7609 기본 `Data/NPCData`를 전수 정리했습니다.

- BASE NPCData **160개 EDT 파일**을 한국어판으로 재구성했습니다.
- 실제 영문 대사 **3,233개**를 모두 한국어로 반영했습니다.
- 원래 공란인 레코드 **201개**는 그대로 공란으로 보존했습니다.
- 총 **3,434개 레코드**의 순서, 고정 레코드 크기(320/480 bytes), 파일 크기를 검증했습니다.
- JA2 EDT 인코딩 규칙으로 재인코딩한 뒤 전 레코드 역복호화 비교를 수행해 번역 문자열과 1:1 일치를 확인했습니다.
- v0.1.3-alpha에서 적용한 용병 대사, EnemyTaunts, VFS 우선순위 보정, 설치기 수정은 그대로 유지됩니다.

상세 변경 사항은 `RELEASE_NOTES_v0.1.4-alpha.md`를 참고하세요.

## 런타임 대사 리소스

- 용병 대사: `MercEdt/*.edt`
- 주민/NPC 대사: `NPCData/*.edt`, `CIV*.edt`, 섹터별 EDT
- 적군 전투 대사: `TableData/EnemyTaunts/*.xml`
- 용병 소개: `BinaryData/MERCBIOS.EDT`

`RUNTIME_UNTRANSLATED=0` 판정은 위의 현재 활성 런타임 대사 계열을 대상으로 합니다. 다른 모드나 별도 외부 리소스를 추가하면 그쪽에 영어가 남아 있을 수 있습니다.

## 알려진 사항

- Windows 창 모드는 16비트 색상 표면을 요구해 환경에 따라 DirectDraw 오류가 날 수 있습니다. 우선 전체 화면으로 실행하는 것을 권장합니다.
- UI 배치와 추가 콘텐츠는 계속 검수 중입니다.
- 다른 JA2 1.13 리비전이나 다른 모드 조합에서는 호환성을 보장하지 않습니다.

## 글꼴

한국어 표시에 [Galmuri](https://github.com/quiple/galmuri)를 사용합니다. 글꼴 라이선스는 `Patch/Data/Fonts/LICENSE_GALMURI.md`를 참고하세요.
