# JA2 1.13 r7609 한국어 EXE 소스 복원 기록

이 문서는 `Patch/ja2.exe`를 다시 빌드할 수 있는 소스 기준점을 고정하고, 현재 확인된 런타임 버그 수정 사항을 소스와 배포 바이너리 수준에서 재현 가능하게 보존하기 위한 기록이다.

## 기준 소스

- Upstream: `1dot13/source`
- Commit: `af1f5c5e173382b5070494e3414bcf5145fd9a6b`
- SVN marker: `Build@7606`
- Commit date: 2014-10-24
- Visual Studio project: VS2013 / `v120` / Win32 Release

프로젝트 초기 조사 기록상 r7609 시점까지 소스 트렁크에서 확인되는 마지막 실제 소스 변경이 Build 7606이고 다음 소스 변경이 Build 7612이므로, r7609 실행 파일을 복원하기 위한 기준점으로 이 커밋을 사용한다.

현재 배포 한국어 EXE 안에는 다음 PDB 경로도 남아 있어 당시 실제 빌드 환경이 확인된다.

`D:\Translation\ja2-r7609-source\bin\VS2013\JA2_EN_Release.pdb`

## 소스 패치

`tools/apply_r7609_runtime_hotfixes.py`는 위 기준 커밋의 소스 트리에 다음 두 수정만 적용한다.

### 1. I.M.P. 한글 이름 입력

대상:

`Laptop/IMP Begin Screen.cpp`

원인은 이름 입력 처리부가 `CHAR16` 버퍼를 사용하면서도 실제 키 입력 검증 단계에서 영문자, 숫자와 일부 ASCII 기호만 허용하는 데 있다. 캐릭터 생성 완료 시 `pFullName`과 `pNickName`은 그대로 `gMercProfiles[].zName` 및 `zNickname`으로 복사되므로 프로필 저장 구조 자체를 바꿀 필요는 없다.

소스 패치는 기존 입력 허용 규칙을 유지하면서 다음 유니코드 범위를 추가한다.

- Hangul Jamo: `U+1100–U+11FF`
- Hangul Compatibility Jamo: `U+3130–U+318F`
- Hangul Syllables: `U+AC00–U+D7A3`

`MercProfiles.xml`의 `PGmale1`, `PGmale2`, `PGLady1` 같은 문자열은 I.M.P. 슬롯의 내부 기본 식별자이므로 번역하지 않는다.

### 2. Fleuropa 꽃집 배송지 선택

대상:

`Laptop/florist Order Form.cpp`

꽃집 배송지 드롭다운은 실제 마우스 영역을 `usPosY+4`부터 `usPosY+usFontHeight`까지만 잡는다. 반면 선택 강조 영역은 아래쪽으로 `usPosY+usFontHeight+4`까지 사용하며, Bobby Ray 배송지 드롭다운도 행의 아래쪽 여유를 더 크게 둔다.

WinFont 기반 한국어 빌드에서는 이 좁은 영역 때문에 글자가 보이는 위치와 실제 클릭 가능한 위치가 어긋날 수 있다. 패치는 배송지 행의 클릭 범위를 다음처럼 확장한다.

- 기존: `usPosY+4` ~ `usPosY+usFontHeight`
- 수정: `usPosY` ~ `usPosY+usFontHeight+4`

닫힌 배송지 선택 영역의 우선순위는 변경하지 않는다. 전체 화면 차단 영역은 드롭다운을 열기 전에는 비활성 상태이므로 별도 우선순위 조정이 필요하지 않은 것으로 확인했다.

배송지 목록, 배송비, Meduna 인덱스 등 게임 데이터는 변경하지 않는다. 주문 처리 코드는 `gubCurrentlySelectedFlowerLocation == 7`일 때 Deidranna 꽃다발 이벤트를 실행하므로 이스터에그 자체는 r7609 EXE에 정상적으로 존재한다.

## 현재 한국어 EXE 직접 패치

한국어 내장 UI 문자열과 기존 WinFont 좌표 수정의 원본 C++ 작업본이 현재 남아 있지 않기 때문에, 순정 소스를 새로 빌드하여 `Patch/ja2.exe`를 교체하면 기존 한국어 기능이 퇴행한다.

이를 피하기 위해 `tools/patch_current_korean_exe.py`는 현재 배포 EXE에 필요한 기계어만 직접 수정한다.

### 입력 바이너리 고정

- 원본 크기: `8,407,552 bytes`
- 원본 SHA-256: `5da88f00f4cc9087463c98dab7594cf14379cf1aa281ef835296bac0fcd10582`
- 원본 Git blob SHA: `d2e21a779bb739b144feb70cefc35cf6ed353857`

위 SHA-256과 파일 크기가 정확히 일치하지 않으면 패치 도구는 중단한다. 각 수정 위치의 원본 바이트도 별도로 검증한다.

### 결과 바이너리

- 결과 크기: `8,407,552 bytes` — 변경 없음
- 결과 SHA-256: `5087524fa181064a7c4646acee9b96cabb3ded68080a2662a6b242a021eb8ea1`
- 결과 Git blob SHA: `212863bcc18421ff5b9d13ecf225c559cdb1e414`
- 실제 변경 바이트 수: `27 bytes`

현재 hotfix 브랜치의 `Patch/ja2.exe`는 위 결과 바이너리와 동일하다.

### 바이너리 수정 위치

I.M.P. `HandleBeginScreenTextEvent()`는 현재 한국어 EXE에서 `0x0052C290`에 있다. ASCII 필터 부분만 같은 길이의 명령으로 교체하여:

- 기존 `A-Z`, `a-z`, `0-9`, `_`, `.`, 공백, `"`, `'` 입력을 그대로 유지하고
- compact한 바이너리 패치를 위해 UTF-16 코드 유닛 `U+0100` 이상도 통과시킨다.

따라서 한글 완성형/자모는 모두 입력 가능해진다. 소스 복원 시에는 위의 명시적 Hangul 범위 방식으로 유지한다.

Florist `CreateDestroyFlowerOrderDestDropDown()`은 `0x004F5990`에 있다. 세 개의 단일 바이트 수정으로 내부 Y 기준을 4픽셀 이동시키고, 마우스 영역의 top 계산에서 그 이동을 상쇄하며, 최종 드롭다운 높이에서도 같은 값을 상쇄한다. 결과적으로 화면의 도시 글자 위치와 전체 드롭다운 높이는 그대로 유지하면서 각 행의 클릭 bottom만 4픽셀 확장된다.

## 자동 바이너리 적용

`.github/workflows/apply-runtime-hotfix-binary.yml`은 hotfix 브랜치에서 다음 절차를 수행한다.

1. 기존 `Patch/ja2.exe`의 크기와 SHA 확인
2. `tools/patch_current_korean_exe.py` 실행
3. 결과 SHA-256이 고정값과 일치하는지 재검증
4. 변경된 `Patch/ja2.exe`만 브랜치에 커밋

알 수 없는 EXE에는 적용하지 않는다.

## 소스 적용 방법

```powershell
git clone https://github.com/1dot13/source.git ja2-r7609-source
cd ja2-r7609-source
git checkout af1f5c5e173382b5070494e3414bcf5145fd9a6b

python <KOREAN_PATCH_REPO>/tools/apply_r7609_runtime_hotfixes.py .
python <KOREAN_PATCH_REPO>/tools/apply_r7609_runtime_hotfixes.py . --check
```

패치 도구는 예상한 기준 코드가 정확히 한 번 발견되지 않으면 중단한다. 다른 1.13 버전에 억지로 적용하지 않는다.

## 장기 소스 복원 항목

바이너리 hotfix로 현재 배포본의 두 문제는 기존 한국어 기능을 보존한 채 수정할 수 있지만, 장기적으로는 다음 소스도 복원해 두는 것이 좋다.

1. `ja2.exe`에 컴파일된 한국어 UI 문자열 소스
2. 기존 WinFont UI 좌표 수정
   - 이메일 휴지통
   - 페이지 화살표 및 페이지 번호
   - 인사 관리자 팀 능력치 11개 행 배치
3. Galmuri/WinFont 빌드 설정
4. VS2013/v120 Release 재현 빌드 및 PDB 보존

## QA 체크리스트

### I.M.P.

- `홍길동`처럼 완성형 한글로 전체 이름 입력 가능
- 한글 별명 입력 가능
- 영문/숫자/기존 허용 기호 입력 회귀 없음
- 캐릭터 생성 완료 후 전술 화면에서 이름 정상 표시
- 전략 화면/인사 화면에서 이름 정상 표시
- 저장 후 재실행해도 이름 유지
- 복수 I.M.P. 슬롯에서도 정상 작동

### Fleuropa / 꽃다발 이스터에그

- 꽃집 주문서의 배송지 영역 클릭 가능
- 드롭다운이 정상적으로 열림
- 모든 보이는 배송지 행이 글자 위치와 관계없이 클릭 가능
- `Meduna` 선택 후 선택 문자열이 갱신됨
- 꽃다발 주문 및 배송 처리 정상
- Deidranna 대상 꽃다발 이벤트 진행 가능
- Bobby Ray 배송지 선택 기능 회귀 없음

## 공개 저장소 원칙

정품 Jagged Alliance 2 원본 데이터, 전체 설치본, SLF 원본 아카이브는 이 저장소에 추가하지 않는다. 공개 저장소에는 재배포 가능한 소스 패치, 번역 데이터, 패치된 실행 파일, 도구와 문서만 보존한다.
