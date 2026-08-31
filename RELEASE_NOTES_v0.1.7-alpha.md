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

## 추가 누락 재검수

BASE 및 1.13의 주요 번역 EDT 계열도 다시 대조했습니다.

- `Data/BinaryData`: 번역 대상 EDT 8개 모두 존재 및 크기 일치
- `Data/NPCData`: 기존 BASE NPCData 완성본 유지
- `Data-1.13/BinaryData`: `AIMBIOS.EDT`, `EMAIL.EDT`, `MERCBIOS.EDT` 모두 존재 및 크기 일치
- `Data-1.13/MercEdt`: 원본 번역 폴더의 파일 세트가 패치에 포함되어 있음을 확인
- `Data-1.13/NpcData`: `159.EDT`, `229.EDT` 모두 존재 및 크기 일치
- `Data-UB`는 r7609 BASE 한국어 패치 배포 대상이 아니므로 기존처럼 패키지에서 제외합니다.

## 검증

- `tools/check_runtime_dialogue.py` 통과
- `tools/verify_runtime_dialogue_zero.py` 통과
- 최종 판정: `RUNTIME_UNTRANSLATED=0`
- BASE `MercEdt` 필수 세트: **70 / 70**
- 누락 파일: **0**
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

데이터와 자동 QA는 통과했습니다. 실제 게임에서는 여러 AIM/MERC 및 남성·여성 I.M.P. 용병을 사용하면서 상황별 전투 대사가 정상 한국어로 표시되는지 추가 확인을 권장합니다.

다른 JA2 1.13 리비전이나 대규모 모드 조합에서는 호환성을 보장하지 않습니다.
