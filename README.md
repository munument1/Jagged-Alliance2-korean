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

1. GitHub Releases에서 `JA2_r7609_Korean_Patch_v0.1.3-alpha.zip`을 다운로드합니다.
2. ZIP의 압축을 풉니다.
3. 압축을 풀면 다음과 같은 구조가 나옵니다.

```text
JA2_r7609_Korean_Patch_v0.1.3-alpha\
├─ install.bat
├─ install.ps1
├─ Patch\
├─ README.md
└─ RELEASE_NOTES_v0.1.3-alpha.md
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
