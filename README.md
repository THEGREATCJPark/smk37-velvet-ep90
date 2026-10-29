# Velvet EP 90 — SMK-37 Pro

90년대 R&B 발라드의 벨 어택·따뜻한 몸통·타건 표현을 목표로 만든 **오리지널 FM EP 8개**와 커스텀 펌웨어.

**v0.1.0-alpha.1 / 실기 미검증.** PC 빌드·DSP·패키지 검사는 통과했지만 실제 기기 설치/지연/오디오 출력은 검증하지 않았습니다. 특정 Babyface 녹음이나 Triton/DX7 공장 패치의 복제품이 아닙니다.

- [Pro 펌웨어](dist/velvet-ep90-smk37-pro-v0.1.0-alpha.1.fwsc)
- [16개 WAV 데모](dist/demos/) — 같은 자체 5음 코드, velocity64/112. 실제 펌웨어 C DSP 사용; 하드웨어 녹음 아님.
- [8개 SysEx](dist/presets/) — FX 미포함, 호환 소프트웨어 FM 신스로 먼저 테스트 가능
- [체크섬](dist/SHA256SUMS) · [완전한 수정 소스](dist/velvet-ep90-corresponding-source.tar.gz)
- [설치/복구/빌드](docs/GUIDE.md) · [조사와 튜닝 근거](docs/research/README.md) · [검증 로그](docs/verification-output.md)

| 슬롯 | 프리셋 | 목표 |
|---|---|---|
| F1 | Velvet 90 | 균형 잡힌 메인 EP |
| F2 | Glass Ballad | 밝고 유리 같은 어택 |
| F3 | Midnight Soft | 부드러운 발라드 |
| F4 | Silk Chorus | 넓은 코드 질감 |
| F5 | Studio Dry | FX 없는 믹싱 출발점 |
| F6 | Warm Tines | 따뜻한 몸통 |
| F7 | Bell Touch | 강한 타건의 선명한 벨 |
| F8 | Slow Jam | 느린 코드 진행용 |

Skiff 고정 소스의 FM6 bank를 교체합니다. 새 프로젝트 첫 트랙은 Velvet 90입니다. 기존 저장 프로젝트는 자체 패치를 유지할 수 있습니다. **FM 트랙당 최대6음**, 전체 트랙과 음성 예산 공유. 페달로 코드를 겹치면 이전 음이 끊길 수 있습니다.

FM6 preset browser에서 전환하세요. 엔진 knob 배열은 MOD LVL / MOD ENV / VEL MOD / PATCH입니다. MOD ENV는 변조 operator 시간이며 전체 음량 decay가 아닙니다. PATCH 슬롯만 바꾸면 FX는 유지되므로 완성 프리셋은 browser로 고릅니다. Chorus 버스는 모노이고, 스테레오 폭은 SPREAD로 코드의 음들을 좌우에 배치한 것입니다. 전용 새 UI/8패드 프리셋 모드는 구현하지 않았습니다.

상용 ROM·패치·곡 샘플은 포함하지 않았습니다. 파생 빌드에서 upstream 녹음 샘플/AI 루프를 제거하고 SLICE 필수 슬롯은 무음으로 대체했습니다. SAMPLE 기존 피아노/관악기와 SLICE break/funk용 빌드는 아닙니다.

조사 출처28개는 **대규모 커뮤니티 통계가 아닙니다**. 본문 열람10개/검색 발췌18개를 구분했습니다. 초기 탐색 데이터는 환경 정리로 소실되어, 복원 후 재검증한 [704조건 원시 지표](docs/measurements/)를 공개합니다. 실제 기준곡 A/B와 실기 튜닝은 남아 있습니다.

GPL-3.0-only. Upstream Skiff/Felucca, msfa 및 폰트 등의 원저작자/라이선스를 소스에 보존합니다. [라이선스/출처](docs/LICENSING.md). 브랜드·아티스트와 제휴 관계가 없습니다.
