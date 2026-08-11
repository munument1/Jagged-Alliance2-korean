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
- `install.bat`을 추가해 게임 설치 폴더에서 더블클릭만으로 설치할 수 있게 했습니다.

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

# 설치 방법

대상 버전은 **Jagged Alliance 2 v1.13 r7609 영어판**입니다.

## 권장 설치 — install.bat 사용

1. GitHub Releases에서 `JA2_r7609_Korean_Patch_v0.1.3-alpha.zip`을 받습니다.
2. ZIP의 압축을 풉니다.
3. 압축을 풀면 다음 항목이 보입니다.

```text
JA2_r7609_Korean_Patch_v0.1.3-alpha\
├─ install.bat
├─ install.ps1
├─ Patch\
├─ README.md
└─ RELEASE_NOTES_v0.1.3-alpha.md
```

4. 이 중 **`install.bat`, `install.ps1`, `Patch` 폴더**를 Jagged Alliance 2 r7609 설치 폴더로 복사합니다.
5. 올바른 위치는 **`ja2.exe`와 `Ja2.ini`가 있는 바로 그 폴더**입니다.

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

6. 게임을 완전히 종료합니다.
7. 게임 폴더의 **`install.bat`을 더블클릭**합니다.
8. 별도의 게임 경로 입력은 필요하지 않습니다. `install.bat`이 자신이 있는 현재 폴더를 자동으로 JA2 설치 경로로 사용합니다.
9. 설치가 끝나면 `Installation completed successfully.` 메시지가 표시됩니다.
10. 이후 `ja2.exe`를 실행하면 됩니다.

### 권한 오류가 나는 경우

게임이 `Program Files` 등 쓰기 권한이 제한된 위치에 설치되어 있다면 `install.bat`을 우클릭하고 **관리자 권한으로 실행**하세요.

### install.bat이 하는 일

- 현재 폴더에 `ja2.exe`, `Ja2.ini`, `Patch`가 있는지 확인
- 기존 `ja2.exe`와 `Ja2.ini` 자동 백업
- `Patch`의 한국어 파일을 게임 폴더에 덮어쓰기
- 과거 알파 버전에 남아 있을 수 있는 가짜 CIV placeholder EDT만 선별 제거
- EnemyTaunts를 `Data-1.13` 우선 VFS 계층에도 적용
- 한국어 Galmuri 글꼴 설정 적용

특히 **이전 알파 버전을 설치했던 사용자는 `install.bat` 사용을 권장**합니다. 일반 파일 덮어쓰기만으로는 예전 버전에서 생성된 삭제 대상 파일이 남을 수 있습니다.

## 수동 설치

자동 설치를 사용하지 않으려면 `Patch` 폴더 **안의 내용물**을 JA2 r7609 설치 폴더에 복사하고 모두 덮어씁니다.

즉 다음 항목이 게임 폴더의 같은 이름 항목과 합쳐지도록 복사하면 됩니다.

```text
Patch\
├─ Data\
├─ Data-1.13\
├─ ja2.exe
└─ Ja2.ini
```

수동 설치 전에는 기존 `ja2.exe`와 `Ja2.ini`를 직접 백업하는 것을 권장합니다.

이전 알파 버전을 설치했던 환경은 구형 CIV 더미 파일이 남을 수 있으므로 **수동 설치보다 `install.bat`을 권장합니다.**

`Data-UB`는 기본 JA2 r7609용 패치에 포함하지 않습니다.

## 주의

이번 `RUNTIME_UNTRANSLATED=0` 판정은 현재 패치에서 실제로 활성화되는 **용병/NPC/주민/적군 전투 대사 계열**에 대한 자동 감사 결과입니다. 새로운 외부 리소스나 다른 모드가 추가되면 별도 번역이 필요할 수 있습니다.
