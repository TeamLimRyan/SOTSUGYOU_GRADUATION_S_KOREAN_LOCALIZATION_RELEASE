[버전 1.0 설치 ZIP 다운로드](https://github.com/TeamLimRyan/SOTSUGYOU_GRADUATION_S_KOREAN_LOCALIZATION_RELEASE/releases/tag/v1.0)

# 졸업 S 한국어 패치 1.0

SEGA Saturn 일본판 **T-20103G / V1.001**용 한국어 패치입니다. 게임 텍스트·한글 이름 입력·승인된 이미지/UI를 반영했습니다. 원본 음성은 유지합니다.

게임 디스크·BIOS·저장 파일은 포함하지 않습니다. 본인이 보유한 원본이 필요합니다.

## 적용

필요 도구: Python 3.10 이상, [MAME chdman](https://www.mamedev.org/release.html) (검증 버전 0.289). Windows용 xdelta3 3.2.0은 동봉했습니다. 다른 OS는 xdelta3를 설치하고 `--xdelta`로 지정합니다.

1. 릴리스 ZIP을 새 폴더에 풉니다.
2. 원본 CHD와 chdman 경로를 넣어 다음 명령을 실행합니다. 출력 폴더는 아직 존재하지 않는 경로여야 합니다.

```powershell
py -3 apply_patch.py "D:\Games\Sotsugyou - Graduation S (Japan).chd" "D:\Games\Graduation_S_Korean_1.0" --chdman "D:\Tools\chdman.exe"
```

3. 생성된 `Graduation_S_Korean_v1.0.cue`를 에뮬레이터에서 엽니다. 같은 폴더의 9개 BIN은 함께 보관합니다.

설치기는 원본 CHD와 추출한 9개 트랙의 SHA-256을 확인하고 Track 1에 xdelta를 적용합니다. 나머지 오디오 8개는 원본에서 가져오며, 최종 9개 트랙도 다시 검증합니다. 원본은 덮어쓰지 않습니다. 실패하면 임시 출력만 지우며, 다시 실행할 때는 새 출력 경로를 사용합니다. 제거는 생성된 출력 폴더를 지우면 됩니다. 원판 저장 데이터는 사본을 별도로 보관하세요.

원본 CHD: 402151193 bytes

```
3d3291adeff6c472c84d12501b2dca4c8d3897a03212107391e4181188d8515f
```

원본 Track 1 SHA-256:
```
57fdfedd22cd315dfc8d79d2b9752f2da7ba7f80ac309ad1989857a3e41e60e9
```

최종 Track 1 SHA-256:
```
931214ce852236450afda084a19ac21719d19f8943508c057d71dd86ec39f252
```

BIN/CUE 원본을 가진 경우 위 Track 1 해시가 정확히 같을 때만 xdelta를 직접 적용할 수 있습니다. 오디오 트랙과 CUE 구성은 원본 그대로 유지합니다.

```powershell
.\xdelta3.exe -d -s "original-track1.bin" "Graduation_S_Korean_v1.0.xdelta" "korean-track1.bin"
```

## 검증 범위와 제한

정적 검증: payload 786개, 활성 번역1907+대체4, 승인 이미지292, EDC/ECC, 원본부터 2회 빌드 일치. 실제 실행: 시작·한글 이름6종/최대10글자·교사 유형·확인창·수업/훈육·학생 메뉴·주간 일정·저장/로드 대표 경로. 최종 r17은 새 BRAM 시작 및 이름/유형/확인창까지 재확인했습니다.

모든 엔딩·분기·시험·일반 창1148개·이미지292개를 전부 실행한 것은 아닙니다. 음성/자막 동기화의 전수 비교와 실제 새턴 하드웨어 검증은 미수행입니다. 원판 저장 설명의 일본어는 사용자 승인 예외로 유지합니다. 문제 신고 시 장면, 재현 방법, 사용 에뮬레이터, 패치 버전과 화면을 첨부해 주세요.

## 라이선스와 출처

- 원작 게임의 권리는 각 권리자에게 있습니다. 비공식 팬 번역 패치입니다.
- 한글 글리프: [Galmuri 2.40.4](https://github.com/quiple/galmuri), Lee Minseo, SIL OFL 1.1. 게임용 글리프를 12×12 / 2bpp 형식으로 변환·배치했습니다. 파생 게임 폰트에 원본 예약 이름을 새 이름으로 사용하지 않습니다. `LICENSE-Galmuri-OFL.txt` 동봉.
- [xdelta3 3.2.0](https://github.com/jmacd/xdelta/releases/tag/v3.2.0), Joshua MacDonald, Apache 2.0. Windows 실행 파일와 `LICENSE-xdelta3.txt` 동봉. 소스: https://github.com/jmacd/xdelta/tree/v3.2.0
- 설치 스크립트는 MIT(`LICENSE-installer.txt`). chdman은 동봉하지 않으며 MAME 공식 배포처에서 준비합니다.
