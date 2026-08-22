# JA2 1.13 r7609 한국어 EXE 소스 복원 기록

이 문서는 `Patch/ja2.exe`를 다시 빌드할 수 있는 소스 기준점을 고정하고, 현재 확인된 런타임 버그 수정 사항을 소스 수준에서 보존하기 위한 기록이다.

## 기준 소스

- Upstream: `1dot13/source`
- Commit: `af1f5c5e173382b5070494e3414bcf5145fd9a6b`
- SVN marker: `Build@7606`
- Commit date: 2014-10-24

프로젝트 초기 조사 기록상 r7609 시점까지 소스 트렁크에서 확인되는 마지막 실제 소스 변경이 Build 7606이고 다음 소스 변경이 Build 7612이므로, r7609 실행 파일을 복원하기 위한 기준점으로 이 커밋을 사용한다.

> 주의: 현재 저장소의 `Patch/ja2.exe`에는 한국어 내장 UI 문자열과 기존 WinFont UI 배치 수정이 이미 포함되어 있다. 아래 두 핫픽스만 적용한 순정 upstream 빌드로 `Patch/ja2.exe`를 바로 교체하면 기존 한국어 수정이 사라질 수 있으므로, 소스 복원이 끝날 때까지 배포 EXE는 교체하지 않는다.

## 자동 패치

`tools/apply_r7609_runtime_hotfixes.py`는 위 기준 커밋의 소스 트리에 다음 두 수정만 적용한다.

### 1. I.M.P. 한글 이름 입력

대상:

`Laptop/IMP Begin Screen.cpp`

원인은 이름 입력 처리부가 `CHAR16` 버퍼를 사용하면서도 실제 키 입력 검증 단계에서 영문자, 숫자와 일부 ASCII 기호만 허용하는 데 있다. 캐릭터 생성 완료 시 `pFullName`과 `pNickName`은 그대로 `gMercProfiles[].zName` 및 `zNickname`으로 복사되므로 프로필 저장 구조 자체를 바꿀 필요는 없다.

패치는 기존 입력 허용 규칙을 유지하면서 다음 유니코드 범위를 추가한다.

- Hangul Jamo: `U+1100–U+11FF`
- Hangul Compatibility Jamo: `U+3130–U+318F`
- Hangul Syllables: `U+AC00–U+D7A3`

`MercProfiles.xml`의 `PGmale1`, `PGmale2`, `PGLady1` 같은 문자열은 I.M.P. 슬롯의 내부 기본 식별자이므로 번역하지 않는다.

### 2. Fleuropa 꽃집 배송지 선택

대상:

`Laptop/florist Order Form.cpp`

꽃집 배송지 드롭다운은 표시 행의 글꼴 높이를 사용하면서 실제 마우스 영역을 `usPosY+4`부터 `usPosY+usFontHeight`까지만 잡는다. WinFont 환경에서는 시각적으로 보이는 행보다 클릭 가능한 영역이 지나치게 얇아질 수 있다.

패치는:

- 닫힌 배송지 선택 영역의 우선순위를 `MSYS_PRIORITY_HIGH+1`로 올린다.
- 각 배송지 행의 클릭 범위를 시각적 행 전체인 `usPosY` ~ `usPosY+usFontHeight+2`로 확장한다.
- 배송지 목록, 배송비, Meduna 인덱스 등 게임 데이터는 변경하지 않는다.

Bobby Ray 주문 화면은 같은 PostalService 데이터를 사용하지만 드롭다운 행의 클릭 영역을 더 넉넉하게 정의하고 있어 비교 기준으로 사용했다.

## 적용 방법

```powershell
git clone https://github.com/1dot13/source.git ja2-r7609-source
cd ja2-r7609-source
git checkout af1f5c5e173382b5070494e3414bcf5145fd9a6b

python <KOREAN_PATCH_REPO>/tools/apply_r7609_runtime_hotfixes.py .
python <KOREAN_PATCH_REPO>/tools/apply_r7609_runtime_hotfixes.py . --check
```

패치 도구는 예상한 기준 코드가 정확히 한 번 발견되지 않으면 중단한다. 다른 1.13 버전에 억지로 적용하지 않는다.

## 배포 EXE 교체 전 필수 복원 항목

현재 한국어 `ja2.exe`와 기능 동등성을 확보하려면 다음 작업이 추가로 필요하다.

1. `ja2.exe`에 컴파일된 한국어 UI 문자열 소스 복원
2. 기존 WinFont UI 좌표 수정 복원
   - 이메일 휴지통
   - 페이지 화살표 및 페이지 번호
   - 인사 관리자 팀 능력치 11개 행 배치
3. 기존 Galmuri/WinFont 설정과 동일한 빌드 확인
4. Release 빌드 후 현재 배포 EXE와 런타임 회귀 테스트

위 항목을 복원하기 전에는 `Patch/ja2.exe`를 새 빌드로 교체하지 않는다.

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

정품 Jagged Alliance 2 원본 데이터, 전체 설치본, SLF 원본 아카이브는 이 저장소에 추가하지 않는다. 공개 저장소에는 재배포 가능한 소스 패치, 번역 데이터, 도구와 문서만 보존한다.
