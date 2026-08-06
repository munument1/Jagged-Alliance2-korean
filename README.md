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
3. PowerShell에서 다음 명령을 실행합니다.

```powershell
.\install.ps1 -GamePath "D:\jagged\Jagged Alliance 2"
```

설치기는 기존 `ja2.exe`와 `Ja2.ini`를 타임스탬프가 붙은 파일로 백업한 뒤 패치를 복사하고, 한국어 글꼴 설정만 갱신합니다.

수동 설치 시에는 `Patch` 폴더의 내용물을 게임 설치 폴더에 덮어쓴 다음 `Ja2.ini`에서 `USE_WINFONTS = 1`, `WIN_FONT_ADJUST = 0`을 설정해야 합니다.

## 알려진 사항

- Windows 창 모드는 16비트 색상 표면을 요구해 환경에 따라 DirectDraw 오류가 날 수 있습니다. 우선 전체 화면으로 실행하는 것을 권장합니다.
- 번역과 UI 배치는 계속 검수 중입니다. 일부 추가 콘텐츠에는 영어가 남아 있을 수 있습니다.
- 다른 JA2 1.13 리비전이나 다른 모드 조합에서는 호환성을 보장하지 않습니다.

## 글꼴

한국어 표시에 [Galmuri](https://github.com/quiple/galmuri)를 사용합니다. 글꼴 라이선스는 `Patch/Data/Fonts/LICENSE_GALMURI.md`를 참고하세요.

