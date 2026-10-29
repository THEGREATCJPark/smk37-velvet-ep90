# 설치·복구·빌드

## 수령 후 설치: Pro만

실기 미검증 alpha입니다. 먼저 데모를 듣고 방향을 판단하세요. 트랙당6음 제한이 있습니다.

1. 모델이 SMK-37 Pro인지 확인합니다. Elite/MKE/Starrykey에 이 패키지를 사용하지 않습니다.
2. upstream 설치 조건은 공식 **V016**입니다. 다른 버전은 공식 경로에서 준비하고 버전 검사를 강제로 건너뛰지 않습니다.
3. [고정 소스의 백업 절차](../vendor/skiff/SMK37.md#back-up-first)로 1MiB flash를 두 번 읽어 동일한 SHA-256/크기1,048,576bytes를 확인하세요. 고유 calibration이 있으므로 개인적으로 두 사본을 보관합니다. Boot-mode 장치를 포맷하지 않습니다. 기존 Skiff 음악/사용자 preset도 별도 백업합니다.
4. 내려받은 파일을 dist/SHA256SUMS와 비교하고 안정된 USB 데이터/전원 연결에서 설치합니다.

```sh
python3 -m pip install mido python-rtmidi
python3 vendor/skiff/tools/fm1_install.py --info
python3 vendor/skiff/tools/fm1_install.py dist/velvet-ep90-smk37-pro-v0.1.0-alpha.1.fwsc
```

자동 최신파일 선택 웹페이지는 원본 Skiff를 설치할 수 있어 위 명시적 파일 경로를 사용합니다. `--force`로 모델/버전 검사를 우회하지 않습니다. 설치 명령은 실제 기기를 준비한 사용자가 실행하며 빌드 도구는 기기에 접속하지 않습니다.

처음에는 낮은 음량으로 F1–F8 단음/5음코드, 약/중/강 타건, 저음/고음, 페달 3음→3음코드, mono 합산, 저장/재시작을 검사하세요. '어택/몸통/타건/공간감'으로 피드백을 나누면 조정하기 쉽습니다. 기존 factory 번호를 쓰던 테마·즐겨찾기 의미는 바뀔 수 있습니다.

복구는 [고정 SMK37.md](../vendor/skiff/SMK37.md#if-it-does-not-start). UPDATE MODE는 동일 설치기를 다시 실행하는 upstream 절차를 따릅니다. 공식 복귀는 사용자가 확보한 변조하지 않은 V016 파일과 upstream 복귀 절차를 사용합니다. 부팅 부분 검사 거절을 우회하거나 타 기기 calibration으로 덮지 마세요. Skiff에서 제조사 자체 로더를 임의로 실행하면 보정영역에 영향을 줄 수 있다는 upstream 경고가 있습니다. 이 프로젝트는 실제 복구를 시험하지 않았습니다.

## 개발/재현

Linux x86_64, Python3.12+, cc, git, curl. Windows에서는 WSL을 사용할 수 있습니다.

```sh
git clone --recurse-submodules https://github.com/THEGREATCJPark/smk37-velvet-ep90.git
cd smk37-velvet-ep90
python3 -m pip install -r requirements.txt
python3 tools/velvet.py prepare
```

Skiff pin: `8eb0e273b62d964dc7f53ca78257c19fdc38bd9e`. JieLi Linux toolchain `20260730.1`, SDK commit `d179b4484759423312073f5fbb232501aa491047` / branch `AC79NN_SDK_V1.2.1_2023-12-13`. 다운로드와 설치는 [upstream BUILDING.md](../vendor/skiff/BUILDING.md). 이 빌드에서 사용한 toolchain archive SHA256은 `a1545cddbc451a06bac43eb5cd96d831470c42a97c5c0b1f98879a20fc7647bd`; clang SHA256은 `c45189ee624de0430deb0db02e6dce171fb5538e7fe323e3964dc8ac6236240f`. SDK3개 입력은 upstream build가 hash검사합니다.

```sh
export JIELI_TOOLCHAIN=/absolute/path/to/jieli-linux-toolchains-20260730.1
export AC79_SDK=/absolute/path/to/fw-AC79_AIoT_SDK
BOARD=smk37 MODEL=pro build/firmware/build.sh
python3 tools/verify.py
```

패키지: build/firmware/build/skiff-smk37.fwsc. UI VEP90-a1, updater identity SMK-37 Pro_700(개발용). 숫자identity만으로 원본 Skiff와 구별하지 말고 파일 checksum을 확인하세요.

`presets/designs.json`과 `tools/velvet.py`를 편집하고 prepare→build→verify 순으로 반복합니다. prepare는 build/firmware를 재생성합니다. 최종704조건 grid와16데모가 새로 생성됩니다. `tools/render.c`는 같은 firmware C DSP를 포함합니다. Dry float32는 voice full-scale 기준, wet PCM16은 FX/mixer 이후이며 loudness normalization은 없습니다.

소스 archive의 firmware/는 이미 overlay가 반영된 완전한 빌드 트리입니다. 그 안의 build.sh를 위 환경변수로 실행하면 submodule 없이 빌드할 수 있습니다. project/는 원래 overlay/원본 디자인/검증 도구입니다.
