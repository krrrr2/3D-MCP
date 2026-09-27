# 3D 도구 설치 안전 가이드: 악성 애드온·.blend·MCP·모델 파일

> 기준일: 2026-09-27 · 원자료: [`G12_tool_safety.gap.json`](../01_research/raw/G12_tool_safety.gap.json)(조사), [`G12_tool_safety.verify.json`](../01_research/raw/G12_tool_safety.verify.json)(원문 대조)
> 보안 업체 블로그·언론 기사는 조사 환경에서 직접 열 수 없어 검색 요약으로 확인했습니다. 이런 내용은 **(검색 요약)**으로 표시했습니다. GitHub의 보안 권고, 커밋, README는 직접 확인했습니다.

## 핵심 요약

- **`.blend`는 데이터 파일이 아니라 "실행될 수 있는 코드 묶음"입니다.** 2025년에 악성 `.blend` 사례가 세 번 이어졌습니다. 세 경우 모두 Blender의 **Auto Run Python Scripts**가 켜져 있으면 파일을 열기만 해도 감염됐습니다(검색 요약).
  - 가짜 커미션 의뢰로 받은 파일
  - 80.lv가 경고한 "무료 의자 모델"
  - CGTrader 무료 모델 속 `Rig_Ui.py` → StealC V2 인포스틸러
- **Blender 개발진도 이 위험을 UI에 반영하고 있습니다.** 2026-09 Blender 커밋 [7054d325](https://github.com/blender/blender/commit/7054d3254ba0da2df9b240c41dc8d6926c749a01)의 변경 내용입니다. 어느 버전에 들어가는지는 미확인입니다.
  - 경고창에서 "자동 실행 영구 허용" 체크박스를 없앴습니다.
  - 버튼 문구를 "Run potentially unsafe scripts in this blend file" / "Continue Safely"로 바꿨습니다.
  - Auto Run을 켜 두면 환경설정에 "인터넷 등 신뢰할 수 없는 출처의 파일은 위험하다"는 경고를 띄웁니다.
- **공식 확장 플랫폼도 "위험을 줄일 뿐 보증은 아닙니다".** extensions.blender.org는 사람이 검토하고 난독화 코드를 금지합니다(검색 요약). 하지만 애드온이 선언하는 권한(파일·네트워크 등)은 실행 중에 강제되지 않고, Allow Online Access도 제3자 코드가 무시하면 Blender가 막지 못합니다.
- **가장 큰 감염 경로는 "공짜 유료 애드온"과 "가짜 AI 도구"입니다.** 두 가지를 조심하세요.
  - SDF.R, Chisel, Botaniq, Quad Remesher, Archipack, SceneCity 같은 유료 애드온의 크랙판이 검색 상위에 뜹니다(G10·G11 조사).
  - Claude·ComfyUI·AI 영상 생성기를 사칭한 설치 파일로 인포스틸러를 퍼뜨린 사례가 2025~2026년에 반복됐습니다(검색 요약).
- **MCP 서버도 공급망 공격 대상입니다(검색 요약).** GitHub Advisory DB에는 MCP 관련 악성 패키지 권고가 다수 등재돼 있습니다.
  - postmark-mcp: 정상 버전 15개로 신뢰를 쌓은 뒤 16번째 버전에 모든 메일을 공격자에게 몰래 전달하는 코드를 넣었습니다(2025-09).
  - 이름을 흉내 낸 npm 패키지 19개가 악성 MCP 서버를 설치했습니다(2026-02).
  - 가짜 GitHub 저장소 약 7,600개 중 800개 이상이 AI 스킬·MCP 서버로 위장했습니다(2026-07 공개).
- **Blender MCP 자체의 위험도 확인됐습니다.** 커뮤니티 서버 ahujasid MCP for Blender에 2026년 CVE 4건이 등재됐습니다([GHSA](https://github.com/advisories/GHSA-fx9q-x9g5-jgg6) 등, 직접 확인). 애드온 소켓에는 인증이 없습니다. 공식 Blender Lab 서버도 코드 실행 보호가 약합니다([Blender MCP 가이드 10절](02_blender_mcp.md)).
- **AI 모델 가중치 파일도 코드를 실행할 수 있습니다.** `.ckpt`·`.pt`·`.bin`·`.pth`(pickle)는 불러오기만 해도 코드가 돌 수 있습니다. **safetensors**를 우선 쓰고 PyTorch 2.6 이상을 유지하세요. Hugging Face 스캐너도 "100% 확실하지 않다"고 밝힙니다.
- **GitHub 별 수는 신뢰 지표가 아닙니다.** 가짜 별로 의심되는 사례가 약 600만 개 보고됐습니다(StarScout, ICSE 2026). AI 에이전트가 악성 저장소를 추천한 실험 결과도 있습니다(검색 요약). **에이전트가 찾아 준 설치 명령도 사람이 원 저장소에서 다시 확인하세요.**

---

## 1. 설치 전 점검표 (이것만 지켜도 대부분 막힘)

### 1.1 Blender 설정

| 설정 | 권장 | 이유 |
|---|---|---|
| Edit > Preferences > Save & Load > **Auto Run Python Scripts** | **끔**(기본값). 꼭 켜야 하면 다운로드·메신저 수신·압축 해제 폴더를 Excluded Paths에 넣음 | 2025년 악성 `.blend` 세 건 모두 이 설정이 켜져 있을 때 감염 |
| 파일을 열 때 스크립트 경고창 | 기본으로 **Ignore / Continue Safely** | 경고창의 "실행"은 그 파일의 코드를 믿는다는 뜻 |
| Preferences > System > **Allow Online Access** | 필요할 때만 켬. 새 애드온은 `--offline-mode`로 먼저 시험 | 온라인 접근 설정은 규칙일 뿐 강제력이 없음. 실제 차단·관찰은 OS 방화벽으로 |
| Blender 본체 | blender.org(또는 Steam·Microsoft Store·Snap 공식 채널)에서만 받음. 검색 광고 링크 클릭 금지 | Blender 사칭 검색 광고로 인포스틸러가 퍼진 전례(2023, 검색 요약) |

### 1.2 에셋 파일 (`.blend`, 에셋 팩)

- 출처가 불분명한 에셋은 `.blend` 대신 **스크립트가 없는 형식**(`.glb`/`.gltf`, `.fbx`, `.obj`, `.usd`)으로 받습니다.
- `.blend`가 꼭 필요하면 Auto Run을 끈 격리 환경에서 먼저 엽니다. 그다음 Text Editor의 텍스트 블록과 드라이버 표현식을 **읽기만** 해서 확인합니다.
  - 특히 Register가 체크된 블록을 보세요.
  - `Rig_Ui.py`, Rigify처럼 익숙한 이름을 흉내 낸 스크립트도 의심하세요.
- 텍스트 에디터에서 스크립트를 직접 실행하면 Auto Run 보호가 적용되지 않습니다.

### 1.3 애드온

1. **받는 곳은 다음 순서로만**: ① extensions.blender.org → ② 개발자 본인의 공식 판매 페이지(Superhive, Gumroad 등) → ③ 개발자의 원 GitHub 저장소.
2. **"무료/cracked/leaked/FULL" 버전과 Discord·텔레그램·구글 드라이브 zip은 받지 않습니다.**
3. zip을 설치하기 전에 **압축 목록을 봅니다.**
   - 이런 파일이 있으면 경고 신호입니다: `.exe`, `.dll`, `.pyd`, `.so`, `.dylib`, `.bat`, `.ps1`, `.vbs`, `.lnk`, `.pyc`, 알 수 없는 `.dat`, 함께 들어 있는 인터프리터, 길게 인코딩된 문자열(base64 + exec).
   - 네이티브 바이너리가 원래 필요한 애드온도 있습니다. 이런 것은 **원 저장소·공식 스토어 배포본만** 씁니다.
     - Modular Tree의 C++ 코어
     - QRemeshify의 QuadWild
     - SDF.R의 Rust 백엔드
     - IfcOpenShell 네이티브 라이브러리
4. `blender_manifest.toml`의 `[permissions]`에서 네트워크·파일 권한 선언을 봅니다. 선언은 참고용일 뿐 강제되지 않는다는 점을 기억하세요.

### 1.4 MCP 서버

1. **원 저장소, 정확한 패키지 이름, 버전 고정**으로 설치합니다(`uvx 패키지==버전`, `npx 패키지@버전`). 업데이트할 때는 변경 로그와 diff를 봅니다.
2. 설치 전에 GitHub Advisory DB에서 `type:malware 패키지이름`을 조회합니다.
3. 클라이언트 설정에 넣기 전에 **command와 args 전문을 읽습니다.** 신뢰도가 낮은 서버를 메일·GitHub·파일시스템 같은 민감한 서버와 같은 세션에 두지 않습니다. 도구 설명에 숨긴 지시문으로 다른 서버의 데이터를 빼내는 공격이 알려져 있습니다(Tool Poisoning, 검색 요약).
4. 코드 실행 도구(`execute_blender_code` 등)는 **자동 승인하지 않습니다.** 호출 전에 코드를 보고, 작업 전에 저장합니다.
5. Blender MCP는 **ahujasid/mcp-for-blender**(커뮤니티)나 **Blender Lab**(공식) 중 하나를 원 저장소에서 설치합니다.
   - 소켓은 localhost에만 엽니다.
   - 커뮤니티 서버는 `BLENDER_MCP_SAFE_MODE=1`, `DISABLE_TELEMETRY=true`로 씁니다.
   - 공식 서버의 HTTP 모드는 필요할 때만 켭니다.

### 1.5 AI 모델·생성기

- 웹 서비스는 **공식 도메인에서만** 씁니다. 광고·SNS의 "Pro/무료" 링크는 무시합니다. 웹 서비스인데 설치 파일을 요구하거나, 결과물이 `.exe`·이중 확장자이면 즉시 중단합니다.
- 가중치는 **safetensors 우선**입니다. pickle 계열은 신뢰할 수 있는 조직 것만 씁니다.
  - `torch.load`의 `weights_only`는 기본값(True)을 유지합니다(PyTorch 2.6 이상).
  - `trust_remote_code=True`는 코드를 읽고 revision을 커밋 해시로 고정한 뒤에만 씁니다.
- 연구 코드의 가중치가 구글 드라이브의 pickle로만 배포되는 경우가 많습니다(HouseDiffusion, GSDiff 등). 격리 환경에서 한 번만 불러와 안전한 형식으로 변환하세요.
- ComfyUI로 3D 생성 노드를 쓸 때는 ComfyUI-Manager의 security_level을 normal 이상으로 둡니다. 새 커스텀 노드는 별도 venv·VM에서 먼저 시험합니다.

### 1.6 처음 쓰는 도구는 "털려도 괜찮은 곳"에서

- VM, Windows Sandbox, 또는 관리자 권한이 없는 별도 OS 계정에서 시험합니다. 그 환경에는 브라우저에 저장된 비밀번호, 암호화폐 지갑, 클라우드 CLI 토큰, SSH 키가 없어야 합니다.
- 받은 zip·모델·설치 파일의 **SHA-256을 기록**해 공식 릴리스의 해시와 대조합니다. 프로젝트에는 lockfile(`uv.lock`, `package-lock.json`)을 커밋합니다.

### 1.7 감염이 의심되면

1. 네트워크를 끊습니다.
2. **깨끗한 다른 기기에서** 이메일, 브라우저 계정, Discord·Telegram, 클라우드, GitHub·npm 토큰의 비밀번호와 세션을 모두 교체하고 2단계 인증을 확인합니다. 인포스틸러는 실행 즉시 데이터를 가져가므로 백신 치료만으로는 부족합니다.
3. 감염된 PC는 검사하거나 재설치합니다.

---

## 2. 저장소 신뢰도 보는 법 (별 수 말고)

| 볼 것 | 경고 신호 |
|---|---|
| 계정 | 최근 생성, 다른 활동이 거의 없음, 비슷한 이름의 계정이 여럿 |
| 저장소 | "forked from" 표시, 커밋 1개이거나 README만 수정, 이슈·PR 활동 없음 |
| 릴리스 | 파이썬·노드 프로젝트인데 Windows ZIP·exe가 있음. README의 다운로드 버튼이 소스가 아니라 릴리스 ZIP을 가리킴 |
| 이름 | 공식 이름과 한두 글자 다름(타이포스쿼팅), "Pro", "Free", "Cracked", "Full" |
| 문서 | 사용자에게 백신 끄기, 서명 없는 DLL 다운로드, 관리자 권한 실행을 요구 |

이번 조사에서 실제로 확인한 주의 사례입니다(G10·G11).
- 커뮤니티 Revit MCP의 한 포크가 서명 없는 사전 빌드 DLL zip을 받게 안내함. 소스 빌드나 공식 Revit MCP를 쓰세요.
- blendergis.com은 BlenderGIS 저장소가 링크하지 않은 도메인임. GitHub 원 저장소를 쓰세요.
- HiFi Architecture Builder는 라이선스 표기가 확장 페이지와 GitHub에서 다름.
- 이름이 같은 포크가 많은 도구(Modular Tree, QRemeshify, IfcOpenShell, TopologicPy)가 있음. 원 저장소를 확인하세요.

---

## 3. 사건 정리 (2023~2026)

| 날짜 | 사건 | 경로 | 출처 |
|---|---|---|---|
| 2023 | Blender 사칭 검색 광고 → 인포스틸러 | 가짜 다운로드 사이트 | [Securelist](https://securelist.com/malvertising-through-search-engines/108996/)(검색 요약) |
| 2024-06 | ComfyUI 악성 커스텀 노드(ComfyUI_LLMVISION) → 자격증명·지갑 탈취 | 커스텀 노드 설치 | [GIGAZINE](https://gigazine.net/gsc_news/en/20240611-comfyui-llmvision-malware/)(검색 요약) |
| 2025 봄~06 | 가짜 커미션 의뢰 `.blend`, "무료 의자" `.blend` | Auto Run | [80.lv](https://80.lv/articles/blender-creators-watch-out-for-malware-hidden-in-fake-commission-requests), [80.lv 경고](https://80.lv/articles/warning-malware-discovered-in-blender-file-circulating-online)(검색 요약) |
| 2025-05 | 가짜 AI 영상 생성기(Noodlophile) | 광고 → 가짜 결과 파일 | [Morphisec](https://www.morphisec.com/blog/new-noodlophile-stealer-fake-ai-video-generation-platforms/)(검색 요약) |
| 2025-09 | postmark-mcp: 16번째 버전에 메일 가로채기 | npm 러그풀 | [Koi](https://www.koi.ai/blog/postmark-mcp-npm-malicious-backdoor-email-theft)(검색 요약) |
| 2025-11 | CGTrader 무료 `.blend` 속 `Rig_Ui.py` → StealC V2 | Auto Run | [Morphisec](https://www.morphisec.com/blog/morphisec-thwarts-russian-linked-stealc-v2-campaign-targeting-blender-users-via-malicious-blend-files/), [Kaspersky](https://www.kaspersky.com/blog/malicious-blender-model-files/54948/)(검색 요약) |
| 2026-02 | Oura MCP 서버 복제본 → StealC | 가짜 GitHub 저장소 | [Straiker](https://www.straiker.ai/blog/smartloader-clones-oura-ring-mcp-to-deploy-supply-chain-attack)(검색 요약) |
| 2026-04 | 가짜 "Claude" 설치 파일 → DLL 끼워 넣기 → 원격 제어 | 가짜 사이트 | [Malwarebytes](https://www.malwarebytes.com/blog/scams/2026/04/fake-claude-site-installs-malware-that-gives-attackers-access-to-your-computer)(검색 요약) |
| 2026-05 | OpenAI 사칭 Hugging Face 저장소가 로더로 인포스틸러 설치 | 모델 저장소 | [HiddenLayer](https://www.hiddenlayer.com/research/malware-found-in-trending-hugging-face-repository-open-oss-privacy-filter)(검색 요약) |
| 2026-06~07 | ahujasid MCP for Blender CVE 4건(코드 인젝션, SSRF, 인젝션, Poly Haven 다운로드 경로 조작 CVSS 6.0) | 서버 도구 | [GHSA-fx9q](https://github.com/advisories/GHSA-fx9q-x9g5-jgg6), [GHSA-4h8q](https://github.com/advisories/GHSA-4h8q-hh2j-755w)(직접 확인) |
| 2026-07 | 가짜 GitHub 저장소 약 7,600개, 그중 800개 이상이 AI 스킬·MCP 위장 | 저장소 README → ZIP | [Island](https://www.island.io/blog/agentbaiting-how-800-fake-ai-skills-and-mcp-servers-delivered-malware)(검색 요약) |
| 2026-09 | Blender가 자동 실행 경고 UI 강화 | — | [커밋 7054d325](https://github.com/blender/blender/commit/7054d3254ba0da2df9b240c41dc8d6926c749a01)(직접 확인) |

- 3D·Blender 전용 PyPI 사칭 패키지(bpy, trimesh, open3d, hunyuan 등)는 2026-09-27 GitHub Advisory DB에서 찾지 못했습니다. npm `gltf-blender-io-tests` 1건은 악성으로 등재돼 있습니다([GHSA-vh25](https://github.com/advisories/GHSA-vh25-q2fm-2v22)).
- extensions.blender.org에 악성 확장이 올라온 사례는 찾지 못했습니다. 이는 확인하지 못했다는 뜻이지, 없다는 뜻은 아닙니다.

## 4. 확인하지 못한 것

- 보안 업체 원문(Morphisec, Kaspersky 등)과 Blender 공식 문서(docs/developer.blender.org)는 차단돼 검색 요약으로만 확인했습니다.
- 커밋 7054d325가 들어가는 Blender 버전
- ahujasid `BLENDER_MCP_SAFE_MODE`의 실제 차단 범위와 우회 가능성
- AI 3D 생성기(Meshy, Tripo, Hunyuan3D, TRELLIS 등)를 직접 사칭한 설치 파일 캠페인. 비슷한 AI 영상 생성기 사례로 유추했습니다.
- 한국 기관(KISA 등)의 관련 권고

## 관련 문서

- [Blender MCP 가이드 10절 보안](02_blender_mcp.md) · [인체·유기물·건물 도구 가이드](13_humans_organic_buildings.md) · [에셋·라이선스](10_assets_pipeline_licensing.md) · [에이전트 워크플로(훅으로 파괴적 코드 막기)](09_agent_workflow_prompting.md)
