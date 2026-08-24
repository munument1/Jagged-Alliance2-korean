# JA2 r7609 Korean Patch v0.1.7-alpha

이번 릴리스는 I.M.P. 용병의 전투 대사 자막 리소스 누락을 수정하는 알파 핫픽스입니다.

## 핵심 변경

### I.M.P. 용병 대사 복구

- `Patch/Data/MercEdt/051.EDT` ~ `056.EDT`를 복구했습니다.
- 남성 I.M.P. 프로필 51~53과 여성 I.M.P. 프로필 54~56의 한국어 전투 대사가 패키지에 포함됩니다.
- 특히 여성 I.M.P. 생성 후 전투 대사가 깨지거나 정상 한국어로 표시되지 않던 문제를 수정합니다.
- 각 EDT는 57,600 bytes, 120개 고정 레코드 구조를 유지합니다.

### 남아 있던 영어 대사 1건 번역

`055.EDT`의 67번 대사에 남아 있던 다음 영어 문장을 번역했습니다.

- `It appears there's been a theft here. Stuff's missing.`
- → `여기 도둑이 든 것 같아요. 물건이 없어졌어요.`

## 검증

- `tools/check_runtime_dialogue.py` 통과
- `tools/verify_runtime_dialogue_zero.py` 통과
- 최종 판정: `RUNTIME_UNTRANSLATED=0`
- MercEdt 051~056 파일 크기 및 레코드 구조 확인
- EDT 복호화 후 한국어 문자열 정상 출력 확인

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

데이터와 자동 QA는 통과했습니다. 실제 게임에서는 남성/여성 I.M.P. 음성 슬롯별로 전투 대사가 정상 한국어로 표시되는지 추가 확인을 권장합니다.

다른 JA2 1.13 리비전이나 대규모 모드 조합에서는 호환성을 보장하지 않습니다.
