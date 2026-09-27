# 기타 DCC·CAD·텍스처 앱과 게임 엔진 MCP 총정리

> 기준일: 2026-09-27 · Blender 밖에서도 벤더 공식 MCP가 빠르게 늘었습니다(Fusion·SketchUp·Rhino·Adobe, Unreal 5.8·Roblox·PlayCanvas·Babylon.js·RTX Remix). 그래도 AAA 품질은 서버 하나에서 나오지 않습니다. "CAD로 정확한 형태 → DCC에서 게임용 정리 → Substance로 PBR → 엔진에서 조립·조명 → 캡처로 검증"이라는 분업과 검증 루프에서 나옵니다.

## 핵심 요약

- **공식 MCP 지도(2026-09)**: Claude 공식 크리에이티브 커넥터 9종 가운데 3D와 직접 관련된 것은 Blender·Autodesk Fusion·Trimble SketchUp입니다(2026-04-28 발표). 이 밖에 벤더가 직접 낸 것은 McNeel Rhino MCP Platform, Adobe for creativity(원격, 도구 67개, 2D 편집용), Epic의 UE 5.8 Unreal MCP(Experimental)와 공식 Claude Code 플러그인, Roblox Studio 내장 MCP, PlayCanvas Editor MCP, Babylon.js 공식 MCP 서버들, NVIDIA RTX Remix 내장 MCP입니다. **Maya·3ds Max·Cinema 4D·ZBrush·Substance 3D는 벤더 공식 MCP가 없어** 커뮤니티 서버를 씁니다. Houdini 22 공식 MCP는 보도만 있고 확인하지 못했습니다.
- **커뮤니티 서버 중 쓸 만한 것**: 3ds Max `3dsmax-mcp`(도구 160개, 메시 접촉·관통 검사, v1.7.3), Houdini `fxhoudinimcp`(도구 206개, Houdini 22.0.368까지 테스트), Rhino `rhinomcp`(1.1k★), FreeCAD `freecad-mcp`(2.5k★), Substance Painter `SubstancePainterMCP`(도구 79개), Substance Designer MCP(재질 레시피 79개), Unity `CoplayDev/unity-mcp`(14.5k★), Unreal `ChiR24/Unreal_mcp`(환경 도구가 가장 많음). Maya는 여러 저장소로 쪼개져 있고 ZBrush는 Pre-Alpha입니다.
- **형태 정확도는 모델보다 입력 방식에서 갈립니다.** Onshape MCP 실험(Claude Opus 4.7)에서 사람이 쓴 치수 사양을 주면 단순/복잡 부품 복합 점수가 1.000/0.615였고, 모델이 도면을 스스로 읽게 하면 0.533/0.000이었습니다(칸당 1회 실행). 가구·조형은 **치수를 텍스트로 주고**, "해석부터 보여 주고 아직 만들지 마"로 시작한 뒤, 측정 도구로 확인하세요.
- **배치 오류(부유·관통·스케일)를 잡는 도구가 DCC·엔진 쪽에도 있습니다.** 3dsmax-mcp 접촉 검사, RhinoMCP `measure_objects`·`section_profile`, Fusion 커뮤니티 서버의 간섭 검사, Pascal Editor의 furniture-fit 스킬, r3f-mcp 공간 질의, GenOrca의 액터 라벨 캡처, Unity `screenshot-isolated`가 그 예입니다. Blender에서는 이 저장소의 [`scene_audit.py`](../03_playbooks/scripts/README.md)를 쓰세요.
- **UE 5.8 공식 MCP**는 에디터 안에서 `127.0.0.1:8000/mcp`로 뜨고, **AllToolsets 플러그인을 켜지 않으면 도구가 하나도 노출되지 않습니다.** 8000 포트는 충돌이 잦으니 8123처럼 다른 포트로 옮기세요. Epic README가 직접 "Localhost is not a trust boundary", "`execute_tool_script`는 임의 Python을 실행한다"고 경고합니다.
- **분업 원칙**: 히어로 에셋의 형태·베벨·UV·트림시트는 Blender/DCC에서, 배치·PCG·폴리지·Lumen 조명·노출·포스트·카메라는 엔진에서 합니다. 엔진 MCP 운영의 3원칙은 **직렬 호출, 쓰기 후 재조회, 3앵글 스크린샷**입니다(6절).
- **공개 사례의 수준**: 가장 구체적인 기록은 per-simmons/unreal-agent-harness(Claude + UE 5.8 공식 MCP로 PCG 글래스 타워 49개, 파리 블록, 아르데코 블록 제작)이고, 작성자 결론도 "real but raw"입니다. 이 주제에서도 독립적으로 검증된 AAA급 결과물은 찾지 못했습니다.
- **보안·포트**: 대부분 DCC 안에서 코드를 실행하는 localhost 서버입니다. 예외로 dcc-mcp-maya sidecar는 LAN(59765)에도 gateway를 열고, oculairmedia Houdini 서버는 인증 없는 RPyC(18811)를 씁니다. **포트 9876**은 Blender MCP(공식·커뮤니티), capoomgit Houdini, faust-machines Fusion 서버가 모두 기본값으로 써서 함께 켜면 충돌합니다.
- **[한국 사용자]** Tencent Hunyuan3D 오픈웨이트 라이선스는 적용 지역에서 EU·영국·한국을 뺍니다. AI Forge MCP의 ForgeHunyuan처럼 Hunyuan3D를 로컬로 돌리는 경로는 한국에서 라이선스 밖이고, AI Forge README의 "MIT" 표기는 틀렸습니다. SketchUp 커넥터의 "무료 모델 30개" 한도는 보도 기준이며 원문으로 확인하지 못했습니다.
- **없거나 못 쓰는 것**: Womp(MCP 없음), Plasticity(Phase 0, 사용 불가), Spline(아카이브, 공개 API 없음), KeyShot·Onshape·Maxon 공식 MCP(확인 안 됨), CryEngine MCP(없음).

> **이 문서에 자주 나오는 약어**: DCC(Maya·3ds Max·Houdini 같은 3D 제작 앱), PCG(Procedural Content Generation, UE의 절차적 배치 프레임워크), PIE(Play In Editor, 에디터 안 플레이), MRQ(Movie Render Queue), PPV(PostProcessVolume), ISM(Instanced Static Mesh), HDA(Houdini Digital Asset), VSM(Virtual Shadow Maps), BP(Blueprint).

---

## 1. 먼저 보기: AAA 에셋 목적별 추천 조합

한 서버가 전부를 하지 못합니다. 아래 표는 조사한 서버를 목적별로 묶은 것입니다. 왼쪽부터 "형태 → 정리·텍스처 → 조립·렌더 → 검증" 순서로 읽으세요. Blender 부분은 [Blender MCP 가이드](02_blender_mcp.md)를 보세요.

| 목적 | 형태 만들기 | 정리·텍스처 | 조립·렌더 | 검증 도구 | 주의 |
|---|---|---|---|---|---|
| 치수가 정확해야 하는 가구·제품 | Rhino 공식 MCP 또는 RhinoMCP, Fusion 공식 커넥터. 무료로는 build123d-mcp·AgentCAD | STEP/OBJ/GLB → Blender·Maya·3ds Max에서 리토폴·UV·베벨 → Substance Painter MCP로 베이크·텍스처 | 엔진(UE/Unity) 또는 KeyShot·Marmoset·Corona | RhinoMCP `measure_objects`·`section_profile`·naked edge, Fusion 커뮤니티 서버 간섭 검사, build123d 측정, 이 저장소 `scene_audit.py` | 치수는 텍스트로([실측 치수표](../03_playbooks/05_reference_dimensions.md)). NURBS·B-rep은 게임용 메시로 바로 못 씀 |
| 같은 계열 가구의 크기·형태 변형 | Rhino GH2 "make this parametric", Onshape Variable Studios | 위와 같음 | USD 베리언트(dcc-mcp-openusd, openusd-mcp `set_variant`) | 슬라이더 극단값에서 토폴로지가 깨지는지 | 기존 오브젝트를 bake하지 않고 원시 도형에서 생성하는지 확인 |
| 건축 장식·반복 조형(아치, 리브 볼트, 몰딩, 트레이서리) | tanishqbhattad/rhino-mcp(건축 요소 도구), Grasshopper 브리지(Cordyceps, LAmbda MCP) | 메싱 → DCC | 엔진·DCC | post-condition 계약(바운딩박스·엔벨로프·워터타이트) | star가 적은 개인 프로젝트 |
| 유기적 조각·크리처 | AI 3D 생성([04 가이드](04_ai_3d_generation.md)) | ZBrush MCP(dcc-mcp-zbrush)는 서브툴 정리·리메시·OBJ 익스포트 같은 기술 작업 위주 | Blender·엔진 | `zbrush_see_viewport` 캡처 | ZBrush MCP는 Pre-Alpha. 브러시 조형은 LLM이 잘 못함 |
| 천·소프트 소품(커튼, 쿠션, 테이블보) | Marvelous Designer MCP(기존 패턴 불러오기 → 원단 지정 → 시뮬레이션) | DCC에서 리토폴 | — | 시뮬레이션 뒤 캡처 | 패턴을 처음부터 설계하는 능력은 제한적 |
| 절차적 환경·산포·시뮬·USD 조립 | Houdini fxhoudinimcp(SOP/LOP/PDG/COP, HDA화) | Houdini Copernicus 또는 Substance | Solaris 또는 엔진 PCG | cook 에러 진단, 네트워크 검증 | 도구 206개라 컨텍스트 부담이 큼 |
| 인테리어·아키비즈 스틸 | SketchUp 커넥터로 매싱, 가구는 3dsmax-mcp의 Chaos Cosmos 검색·임포트 | 3ds Max | Corona·V-Ray | 3dsmax-mcp 메시 접촉·관통·작은 틈 검사 | Windows 전용. SketchUp 결과는 저폴리 면 모델 |
| 방 레이아웃·가구 풋프린트 초안 | Pascal Editor(MCP + furniture-fit 스킬) | 결과를 DCC로 넘김 | DCC·엔진 | furniture-fit | 웹 에디터라 렌더 품질은 별도 |
| 타일링 PBR 재질(돌·금속·직물·지형) | Substance Designer MCP 레시피 | 텍스처 익스포트 | 엔진·DCC | 출력 채널(height/normal/roughness/AO/base color/metallic) 확인 | **한 번에 도구 하나만 호출** |
| 게임 레디 텍스처 세트 | — | Substance Painter MCP: 메시 로드 → 베이크 → Smart Material → 엔진 프리셋 익스포트 | UE/Unity | 엔진 임포트 뒤 캡처, 3dsmax-mcp 텍스처 역할 검사 | Painter를 `--enable-remote-scripting`으로 실행 |
| 포트폴리오·제품 렌더 | — | — | Marmoset(dcc-mcp-marmoset), KeyShot MCP, C4D Redshift/Octane | 렌더 비평 | KeyShot MCP는 장면 메타데이터가 모델 제공자에게 갈 수 있음 |
| 게임 레벨 조립(Unreal) | Blender에서 키트 제작 | Substance | UE 5.8 공식 MCP + Epic Claude Code 플러그인. 환경은 ChiR24, 머티리얼 그래프는 monolith | CaptureViewport 3앵글, GenOrca 라벨 캡처, UnrealEngine_Bridge | 직렬 호출, 쓰기 후 재조회(6절) |
| 게임 레벨 조립(Unity) | Sketchfab 임포트, Tripo/Meshy 생성(CoplayDev) | — | CoplayDev MCP for Unity | IvanMurzak `screenshot-isolated` | 조명·HDRP 전용 기능은 README에 명시되지 않음 |
| 웹 3D 제품 뷰어·컨피규레이터 | PlayCanvas Store·Sketchfab 임포트 | Babylon.js NME(노드 머티리얼)·NGE(절차 지오메트리) | PlayCanvas·Babylon·three.js | threejs-devtools-mcp, r3f-mcp 공간 질의 | 모든 오브젝트에 이름 붙이기 |
| 구형 게임 리마스터 | — | RTX Remix | RTX Remix 내장 MCP | — | DX8/9 게임 대상 |
| 여러 DCC를 한 에이전트로 | dcc-mcp gateway(9765) 또는 Flue CLI | | | gateway 감사 로그 | 어댑터 대부분이 pre-alpha. LAN 노출 설정 확인 |

**처음 시작한다면**: Blender + [Blender MCP](02_blender_mcp.md) → Substance Painter MCP → UE 5.8 공식 MCP(+Epic 플러그인) 또는 CoplayDev Unity로 시작하세요. 치수가 중요한 가구가 많으면 Rhino 공식 MCP(Rhino 라이선스 필요)나 build123d-mcp(무료)를 앞단에 붙이면 됩니다.

---

## 2. 벤더 공식 MCP 지도 (2026-09)

| 앱 | 만든 곳 | 방식 | 상태·날짜 | 할 수 있는 것 | 출처 |
|---|---|---|---|---|---|
| Autodesk Fusion | Autodesk, Inc. (Claude 커넥터, Anthropic 검증) | 로컬. Fusion에 내장된 MCP 서버 | 2026-04-28 발표, 디렉터리 등재 2026-05 | 스케치·피처·지오메트리 생성·수정·검사, 디자인 데이터 조회 | [커넥터](https://claude.com/connectors/autodesk-fusion) |
| Trimble SketchUp | Trimble (Claude 커넥터) | 원격 `https://api.sketchup.com/mcp/v1/sketchup/mcp` | 2026-04 등재 | `build_model`, `get_docs`, `save_model` | [커넥터](https://claude.com/connectors/sketchup) |
| Adobe for creativity | Adobe Inc. (Claude 커넥터, Anthropic 검증) | 원격 `https://adobe-creativity.adobe.io/mcp` | 2026-04-28 | 도구 67개, 대상 앱 9개(Acrobat, Photoshop, Lightroom, Illustrator, Firefly, Premiere, Express, InDesign, Stock). Substance 3D는 없음 | [커넥터](https://claude.com/connectors/adobe-creativity), [Adobe 블로그](https://blog.adobe.com/en/publish/2026/04/28/adobe-for-creativity-connector) |
| Rhino 8/9 + Grasshopper | Robert McNeel & Associates | 로컬 플러그인 + Claude Desktop용 `.mcpb` | 활성(기본 브랜치 rhino-9.x), MIT, 316★ | Rhino·GH2 직접 조작, 레시피·sketch-to-model·파라메트릭 역설계 문서 | [mcneel/RhinoAI](https://github.com/mcneel/RhinoAI) |
| Autodesk 개발자 샘플 | Autodesk Platform Services | 샘플 코드 | 2026-09 갱신 | AEC Data Model, Revit Automation MCP 예제, AU2026 MCP 워크숍. Maya·3ds Max용은 없음 | [APS 저장소](https://github.com/orgs/autodesk-platform-services/repositories?q=mcp) |
| Houdini 22 | SideFX(+NVIDIA) | — | SIGGRAPH 2026 미리보기 보도 **(미확인, 신뢰도 낮음)** | APEX Script 리깅 보조. SideFX Labs로 나온다는 보도 | [JPR 기사](https://www.jonpeddie.com/news/sidefx-and-nvidia-bring-mcp-powered-ai-agents-to-houdini-22s-rigging-workflow-at-siggraph-2026/)(검색 요약만) |
| OpenUSD / Kit | NVIDIA | 로컬 Docker, NVIDIA API 키 | Apache-2.0, 96★ | USD·Kit·OmniUI·Isaac Sim 문서와 코드 검색. **라이브 씬은 편집하지 않음** | [kit-usd-agents](https://github.com/NVIDIA-Omniverse/kit-usd-agents) |
| Unreal Engine 5.8 | Epic Games | 에디터 내장 `127.0.0.1:8000/mcp` | Experimental | Toolset Registry + AllToolsets로 액터·머티리얼·PCG·뷰포트 캡처 | 4.1절 |
| Unreal (Claude Code 플러그인) | Epic Games | Claude Code 플러그인 | MIT, 308★, 2026-04~09 활발 | 스킬, SessionStart hook, 에디터 재시작에도 세션을 유지하는 프록시 | [저장소](https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin) |
| Unity 6 | Unity (`com.unity.ai.assistant`) | 로컬 IPC + relay | 2.x pre-release **(세부 미확인)** | 씬·게임오브젝트 관리, 카메라 캡처 | 4.2절 |
| Unity 산업용 | Unity Technologies | Claude Code 플러그인 마켓 | 실험적, source-available | Asset Manager, Asset Transformer(Pixyz), Pipeline Automation | [industry-ai-workflows](https://github.com/Unity-Technologies/industry-ai-workflows) |
| Roblox Studio | Roblox | Studio 내장 | 권장 경로(오픈소스 Rust 서버는 2026-04-03 아카이브) | 데이터 모델 탐색, 스크립트, Luau 실행, 플레이테스트 | 4.4절 |
| PlayCanvas | PlayCanvas | 로컬 `npx`, WebSocket 52000 | MIT, 137★ | 엔티티·에셋·머티리얼 편집, Store·Sketchfab 검색·임포트 | [editor-mcp-server](https://github.com/playcanvas/editor-mcp-server) |
| Babylon.js | Babylon.js | npm `@babylonjs/mcp-servers` 9.28.0(2026-09-24) | Apache-2.0 | 노드 머티리얼·노드 지오메트리·파티클 등 그래프 저작 | [packages/tools](https://github.com/BabylonJS/Babylon.js/tree/master/packages/tools) |
| RTX Remix | NVIDIA | 실행 시 자동 기동 `127.0.0.1:18014/mcp/` | Apache-2.0 | REST API를 MCP 도구로 변환, rtx-remix-modding 스킬 동봉 | [learning-mcp.md](https://github.com/NVIDIAGameWorks/toolkit-remix/blob/main/docs/howto/learning-mcp.md) |

벤더 공식 MCP가 **없는** 앱: Maya(Maya 2027의 Autodesk Assistant는 문서 Q&A 도우미 수준, [도움말](https://help.autodesk.com/view/MAYAUL/2027/ENU/?guid=GUID-B126B0C2-A72E-498F-B46B-56DEEFA72478), 검색 요약만), 3ds Max, MotionBuilder, Cinema 4D·ZBrush(Maxon), Substance 3D(Adobe), Onshape(PTC), KeyShot. 2026-04 이후 Anthropic이 Rhino·Houdini·Unreal을 공식 커넥터 디렉터리에 추가했는지는 확인하지 못했습니다.

---

## 3. DCC·CAD·텍스처 앱 MCP

### 3.1 Claude 공식 커넥터 3종 (Fusion·SketchUp·Adobe)

[Claude for Creative Work](https://www.anthropic.com/news/claude-for-creative-work)(2026-04-28)에서 발표된 커넥터 9종은 Ableton, Adobe for creativity, Affinity by Canva, Autodesk Fusion, Blender, Resolume Arena, Resolume Wire, SketchUp, Splice입니다. Blender는 [02 가이드](02_blender_mcp.md)에서 다루고, 여기서는 나머지 3D·텍스처 관련 3종을 봅니다. "모든 Claude 플랜에서 쓸 수 있다"는 설명은 발표문에 없어 **확인하지 못했습니다.**

| 항목 | Autodesk Fusion | Trimble SketchUp | Adobe for creativity |
|---|---|---|---|
| 실행 위치 | 로컬(Fusion 실행 필요, Claude Desktop) | Trimble 클라우드 세션 | Adobe 클라우드 |
| 켜는 법 | Fusion **Preferences > General > API > Fusion MCP Server** 켜기 → Claude Desktop에 커넥터 추가, 포트 맞추기 | 커넥터 켜기 → Trimble ID 로그인 | 커넥터 켜기 → Adobe 계정 |
| 요금 | Fusion 구독 필요(발표문 확인) | 무료 entitlement로 모델 30개 저장, 이후 유료 **(보도 기준, 미확인)** | Adobe 계정(기능별 구독 조건 미확인) |
| 잘하는 것 | 파라메트릭 히스토리, 조인트·어셈블리. 치수 정확도가 높음 | 방·가구·사이트 매싱 초안. 평면도·스케치·치수를 첨부하면 치수를 반복 검증 | 참조 이미지 배경 제거, 리사이즈, 색보정, 생성형 편집 |
| 한계 | B-rep이라 게임용 토폴로지·UV는 후처리. "Fusion Data MCP"는 원문 확인 못 함 | 저폴리 면 모델이라 AAA 에셋에는 베벨·디테일·UV를 따로 작업 | 원격 API라 **데스크톱 Photoshop의 PSD 레이어·채널 제어는 기대하지 않는 편이 안전**(도구 이름이 `asset_*`, `document_*` 같은 클라우드 API. 추론). 레이어 단위 작업은 3.4절의 로컬 MCP |
| 식별자·날짜 | `ant.dir.gh.autodesk.fusion-mcp`, 디렉터리 표기 "Added May 2026" | 2026-04 등재 | 도구 67개(발표 당시 "50+") |

가구 프롬프트 예(Fusion): "상판 1200×600×30mm, 다리 4개 테이퍼, 5° 벌어짐"처럼 수치로 지시한 뒤 STEP/FBX/OBJ로 내보내 DCC에서 리토폴·UV를 합니다.

### 3.2 DCC (Maya·3ds Max·MotionBuilder·Houdini·Cinema 4D·ZBrush)

★와 날짜는 2026-09-26~27 조회 기준입니다. "성숙도"는 릴리스 빈도, 테스트, 사용자 규모를 보고 매긴 상대 평가입니다.

| 앱 | 서버 | 구분 | 핵심 기능 | 성숙도 | ★ · 최신 | 라이선스 | 추천 용도 |
|---|---|---|---|---|---|---|---|
| Maya | [GG_MayaMCP](https://github.com/GimbalGoats/GG_MayaMCP) | 커뮤니티 | commandPort 기반 타입 도구 71개(Scene, Mesh, Modeling 15개, Shading, Skin, Animation 등). raw 코드 실행은 기본 꺼짐(`MAYA_MCP_ENABLE_RAW_EXECUTION=true`로 켬). 서버 프로세스에 Maya import 없음 | 중 | 23★, PyPI [maya-mcp](https://pypi.org/project/maya-mcp/) 0.6.1(2026-07-20) | MIT | 보안이 중요한 Maya 자동화. Maya 2024+, Claude Desktop(.mcpb)·Claude Code·Codex CLI·VS Code |
| Maya | [dcc-mcp-maya](https://github.com/dcc-mcp/dcc-mcp-maya) | 커뮤니티(dcc-mcp) | 스킬 29개, 타입 도구 79개 이상, Streamable HTTP, sidecar 격리, 멀티 인스턴스 gateway | 초기~베타 | 56★, 0.9.31(2026-09-23) | MIT | 렌더·팜·크로스 DCC 파이프라인. **sidecar가 LAN에도 gateway를 엶** |
| Maya | [PatrickPalmer/MayaMCP](https://github.com/PatrickPalmer/MayaMCP) | 커뮤니티 | Command Port로 Python 실행하는 초기 레퍼런스 구현 | 정체 | 103★, 2025-05 이후 멈춤 | MIT | 학습용 |
| Maya | [chadrik/maya-mcp-server](https://github.com/chadrik/maya-mcp-server) | 커뮤니티 | 여러 Maya 세션 자동 발견, `write_module`로 재사용 함수 정의 | 소규모 | 42★ | MIT | 세션이 여럿인 스튜디오 |
| Maya | [abrahamADSK/maya-mcp](https://github.com/abrahamADSK/maya-mcp) | 커뮤니티(Autodesk와 무관 명시) | Maya API 문서 하이브리드 RAG(ChromaDB+BM25), 위험 패턴 탐지 | 실험 | 2★ | MIT | API 환각을 줄이는 설계 참고 |
| 3ds Max | [3dsmax-mcp](https://github.com/cl0nazepamm/3dsmax-mcp) | 커뮤니티 | 도구 160개: 모디파이어·모델링, PBR 텍스처 배치, MCG, tyFlow, 격리 멀티뷰 캡처, RailClone(stable)·Forest Pack(WIP), Corona·V-Ray·Octane. v1.7.0(2026-09-12) Corona VFB 미리보기와 Chaos Cosmos 모델·재질·HDRI 검색·임포트. v1.7.3(2026-09-23) 메시 접촉·관통·교차·작은 틈 검사, 텍스처 역할 검사 | **높음**(릴리스 매우 활발) | 274★, [v1.7.3](https://github.com/cl0nazepamm/3dsmax-mcp/releases) | MIT | 인테리어·아키비즈 스틸, 가구 배치 검증. Windows 전용, Max 2023–2027 인스톨러 |
| MotionBuilder | [dcc-mcp-mobu](https://github.com/dcc-mcp/dcc-mcp-mobu) 외 | 커뮤니티 | 씬·리그·포즈·테이크 검사(MotionBuilderBridge 4★, motionbuilder-mcp 0★도 있음) | 매우 미성숙 | 4★ | 대부분 MIT | 모캡 정리·테이크 검사 한정 |
| Houdini | [fxhoudinimcp](https://github.com/healkeiser/fxhoudinimcp) | 커뮤니티 | 도구 206개·23개 카테고리(README 기준): SOP, LOP/USD, DOP, PDG/TOP, COP, HDA, VEX, 버전별 Houdini 매뉴얼 전문 검색. 리소스 8, 프롬프트 9, 워크플로 가이드 31(pyro, vellum, destruction, solaris 등). cook 프로파일링·네트워크 검증 | **높음** | 254★, [v2.21.0](https://github.com/healkeiser/fxhoudinimcp/releases)(2026-09-23), Houdini 20.5.278~22.0.368 통합 테스트 | MIT | 절차적 모델링·산포·시뮬·Solaris 조립·HDA화의 1순위 |
| Houdini | [capoomgit/houdini-mcp](https://github.com/capoomgit/houdini-mcp) | 커뮤니티 | 노드 생성·수정, 코드 실행, 선택 사항으로 OPUS API(RapidAPI 유료) 절차적 에셋·가구 라이브러리 | 중 | 299★ (조사 기록상 2026-06 업데이트, 검증에서는 날짜 미확인) | MIT | 단순 구성, 절차적 가구 생성 연계. **포트 9876** |
| Houdini | [oculairmedia/houdini-mcp](https://github.com/oculairmedia/houdini-mcp) | 커뮤니티 | hrpyc 기반 도구 43개, 파라미터 스키마 검증, 쿼드뷰 렌더, 모든 pane 스크린샷, cook 에러 진단, 테스트 418개 | 중 | 76★ | MIT | 검증 중심 워크플로. **RPyC(18811)가 무인증 원격 Python 실행을 허용 → 네트워크에 노출 금지** |
| Houdini | [dcc-mcp-houdini](https://github.com/dcc-mcp/dcc-mcp-houdini) | 커뮤니티(dcc-mcp) | 스킬 43개, 도구 295개, Streamable HTTP, gateway 9765, 라이선스 Houdini Docker로 E2E CI | 초기 | 16★ | MIT | 멀티 DCC 통합 |
| Cinema 4D | [ttiimmaacc/cinema4d-mcp](https://github.com/ttiimmaacc/cinema4d-mcp) | 커뮤니티 | 소켓 플러그인. 프리미티브, 머티리얼·셰이더·라이트, Redshift 머티리얼 검사, MoGraph 클로너·이펙터·필드, 소프트·리지드 바디, 프레임 렌더·스냅샷 | 중 | 127★ | MIT | MoGraph 절차 배치, 모션그래픽. C4D 2024.0+ |
| Cinema 4D | [kumoproductions/mcp-cinema4d](https://github.com/kumoproductions/mcp-cinema4d) | 커뮤니티 | TypeScript 서버, 도구 68개(exec_python, call_command, undo 그룹 batch, Takes, 노드 머티리얼, Xpresso, MoGraph), 환경변수·토큰 보안 게이트 | 중 | 24★ | MIT | 보안·undo 설계가 좋은 C4D 자동화. C4D 2026.0.0+, Node 24+ |
| Cinema 4D | [sdimaging/cinema4d-mcp](https://github.com/sdimaging/cinema4d-mcp) | 포크 | 도구 93개, Scene Nodes 저작(패턴 22, 템플릿 802), Octane OSL 주입, 씬 스냅샷·diff | 초기 | 13★ | MIT | Scene Nodes·Octane. C4D 2024–2026 |
| ZBrush | [dcc-mcp-zbrush](https://github.com/dcc-mcp/dcc-mcp-zbrush) | 커뮤니티(dcc-mcp) | ZBrush 2026.1+ 공식 Python SDK(내장 CPython 3.11). 씬 검사, 서브툴, 브러시, 뷰포트 캡처(`zbrush_see_viewport`), OBJ 익스포트 | **Pre-Alpha** | 7★, PyPI [0.2.26](https://pypi.org/project/dcc-mcp-zbrush/)(2026-08-26) | MIT | 서브툴 관리, 리메시·디시메이션 같은 기술 작업, OBJ 익스포트. 브러시 조형은 비현실적 |

**참고**:
- 3ds Max 캡처·검사 흐름 예: Cosmos에서 가구를 가져와 배치 → 접촉 검사로 관통·부유 확인 → Corona로 미리보기 렌더.
- fxhoudinimcp는 v2.16.0부터 auto-layout이 기본 꺼짐(`FXHOUDINIMCP_AUTO_LAYOUT=0`)입니다. PyPI 요약에 남은 "179 tools"는 옛 값이니 README의 206개를 기준으로 삼으세요.
- Cinema 4D MCP(ttiimmaacc)는 큰 해상도 렌더에서 메모리 문제로 실패하고, 일부 빌드에서는 Redshift 모듈을 쓸 수 없습니다. 미리보기 해상도로 확인하고 최종 렌더는 수동이나 배치로 돌리세요.
- Maxon 공식 MCP는 확인하지 못했습니다. Maxon이 예고한 Tencent HY 3D 통합(2026년 말)은 MCP와 무관해 보이며, 출시되면 **한국에서 쓸 수 있는지 약관을 따로 확인**해야 합니다(오픈웨이트 라이선스는 한국 제외, 클라우드 API 약관은 별개로 미확인).
- newsbubbles/zbrush-mcp는 커밋 1개짜리 스캐폴드이고 SDK 요구 버전 주장이 dcc-mcp-zbrush README와 모순돼 근거로 쓰지 않았습니다(신뢰도 낮음).

### 3.3 CAD (Rhino·Grasshopper·Fusion·SketchUp·FreeCAD·OpenSCAD·build123d·Onshape)

| 앱 | 서버 | 구분 | 핵심 기능 | 성숙도 | ★ · 최신 | 라이선스 | 추천 용도 |
|---|---|---|---|---|---|---|---|
| Rhino+GH | [mcneel/RhinoAI](https://github.com/mcneel/RhinoAI) (Rhino MCP Platform) | **공식** | Rhino·Grasshopper(GH2) 조작. 문서: 레시피, sketch-to-model, make-this-parametric, bulk-file-processing, headless-render-farm, GH1→GH2 업그레이드 | 높음 | 316★, rhino-9.x | MIT(플러그인), Rhino 8/9 라이선스 | 가구·계단·조형 파라메트릭. Claude Desktop/Code, Copilot, Codex, Gemini CLI, LM Studio(로컬 LLM), Cursor |
| Rhino+GH | [jingcheng-chen/rhinomcp](https://github.com/jingcheng-chen/rhinomcp) | 커뮤니티 | Python(stdio) → TCP → RhinoCommon 플러그인. 불리언, loft/extrude/sweep, viewport capture, RhinoScript/C# 실행, `gh_*` 도구. 0.4.0(2026-09-09)에서 `get_modeling_guidance`(가이드 6종), `create_planar_region`, `measure_objects`(충돌, bbox gap), `section_profile`, naked edge 분석 개선 | 높음 | 1.1k★, [0.4.1.1](https://github.com/jingcheng-chen/rhinomcp/releases)(2026-09-14) | MIT | 치수 검증 루프가 필요한 가구. Rhino 8 Win/Mac. TCP 루프백 무인증 |
| Rhino | [tanishqbhattad/rhino-mcp](https://github.com/tanishqbhattad/rhino-mcp) | 커뮤니티 | 도구 123개를 lean/standard/full 프로필로 노출. post-condition 계약(bbox, 엔벨로프, 워터타이트), 아치·리브 볼트·트레이서리·몰딩 도구 | 초기 | 24★ | MIT | 건축 장식·조형, 로컬 LLM(lean). Windows Rhino 8 |
| Grasshopper | [Cordyceps](https://github.com/brookstalley/cordyceps) / [LAmbda MCP](https://github.com/gramaziokohler/lamcp) | 커뮤니티 | Cordyceps: GH 캔버스 관리·배선·스크립팅·렌더(도구 7개). LAmbda(ETH Zurich Gramazio Kohler): 캔버스 검사, 슬라이더 읽기·쓰기, 모듈 핫리로드 | 초기 | 105★ / 20★ | MIT | 슬라이더로 변형하는 조형·반복 패턴. Cordyceps는 Rhino 8.21+/.NET 8 |
| Fusion | 공식 Fusion MCP(3.1절) | **공식** | 스케치·피처·지오메트리·데이터 조회 | 높음 | 2026-05 등재 | Fusion 구독 | 가구·제품 치수 |
| Fusion | [faust-machines/fusion360-mcp-server](https://github.com/faust-machines/fusion360-mcp-server) | 커뮤니티 | 도구 93개: 스케치 구속·치수, extrude/revolve/sweep/loft/fillet/shell, 어셈블리·조인트, 판금, CAM·G-code, STL/STEP/F3D I/O, 거리·각도·물성·**간섭 검사**, 렌더 캡처 | 중 | 104★, 2026-09-16 | MIT | 공식 서버에 없는 간섭 검사·CAM·판금 보완. **TCP 9876** |
| Fusion | [frankhommers/autodesk-fusion-mcp](https://github.com/frankhommers/autodesk-fusion-mcp) | 커뮤니티 | 애드인 안에서 Streamable HTTP로 도구 14개(`call_autodesk_api`, `execute_python`, `capture_viewport`, `fetch_api_documentation`) | 초기 | 22★, v1.6.0 | MIT | API 문서 조회로 환각 줄이기. MCP 프로토콜 2026-07-28 지원 |
| Fusion | [AuraFriday MCP-Link](https://github.com/AuraFriday/Fusion-360-MCP-Server) | 상용 | 범용 API 호출, Python 실행. Autodesk App Store 등록 | 중 | 127★ | 독점 | 오픈소스가 필요 없을 때 |
| SketchUp | 공식 커넥터(3.1절) | **공식** | 클라우드에서 모델 생성·저장 | 높음 | 2026-04 | 보도 기준 무료 30개 | 매싱 초안 |
| SketchUp | [mhyrr/sketchup-mcp](https://github.com/mhyrr/sketchup-mcp) | 커뮤니티 | 로컬 SketchUp Ruby 확장. 컴포넌트 생성·변형·삭제, 재질, 익스포트, `eval_ruby`(임의 Ruby) | 중(업데이트 뜸함) | 466★, 2026-04-25 | MIT | 로컬 파일 직접 편집, 저장 한도 없음. 가구 조인트는 `eval_ruby`로 Ruby API 호출 |
| FreeCAD | [neka-nat/freecad-mcp](https://github.com/neka-nat/freecad-mcp) | 커뮤니티 | XML-RPC 애드온 + MCP 서버. 모델 생성·편집, Python 실행, FEM 해석, 헤드리스 실행, 스크린샷 피드백(텍스트만 받아 토큰 절약 가능) | 높음 | **2.5k★**, 307 forks, PyPI [0.1.25](https://pypi.org/project/freecad-mcp/)(2026-09-24) | MIT | 무료 CAD 자동화, FEM 구조 검토 |
| FreeCAD | [spkane/freecad-addon-robust-mcp-server](https://github.com/spkane/freecad-addon-robust-mcp-server) | 커뮤니티 | 11개 카테고리 도구 150개 이상, XML-RPC·JSON-RPC 소켓·임베디드 모드(임베디드는 Linux 전용, macOS·Windows에서 크래시) | 중 | 238★, PyPI [0.6.1](https://pypi.org/project/freecad-robust-mcp/)(2026-01-13) | MIT | 풍부한 도구가 필요할 때. FreeCAD 0.21+ |
| FreeCAD | [ghbalf/freecad-ai](https://github.com/ghbalf/freecad-ai) | 커뮤니티 | FreeCAD 안 AI 채팅 워크벤치(LLM 제공자 21종) + 구조화된 작업 50개를 외부 MCP 서버로 노출 | 중 | 524★ | LGPL-2.1 | 앱 내부 채팅과 외부 에이전트 병행. FreeCAD 1.0/1.1 |
| OpenSCAD | [jhacksman/OpenSCAD-MCP-Server](https://github.com/jhacksman/OpenSCAD-MCP-Server) | 커뮤니티 | mm 단위 사양 → SCAD/STL/CSG/3MF + 4방향 PNG 미리보기, 리비전 관리, 렌더 120초 타임아웃, Docker | 중 | 197★ | MIT | 결정적·재현 가능한 단순 부재. 유기 형태·필렛에 약함(RobertCoop/openscad-mcp 142★도 있음) |
| build123d | [pzfreo/build123d-mcp](https://github.com/pzfreo/build123d-mcp) | 커뮤니티 | 영속 세션에서 build123d 코드 실행. PNG/SVG/DXF 미리보기, 부피·면적·bbox·무게중심 측정, 구멍·보스 패턴 인식, 프린트 가능성 검사, STEP/STL/DXF/SVG 익스포트 | 중 | 95★, PyPI 0.3.90(2026-09-25) | Apache-2.0 | 측정 기반 치수 검증 루프 |
| build123d / CadQuery | [jdilla1277/agentcad](https://github.com/jdilla1277/agentcad) | 커뮤니티 | CAD CLI + MCP(`agentcad[mcp]`), STEP/STL/**GLB**/OBJ 익스포트, 치수 사양 검사, 버전 간 시각 diff, 라이브 뷰어 | 중 | 138★, PyPI 0.6.0(2026-09-11) | Apache-2.0 | GLB로 엔진·DCC에 바로 넘기기 |
| Onshape | [jarvis-onshape-mcp](https://github.com/ReshefElisha/jarvis-onshape-mcp) | 커뮤니티(Claude Code 플러그인) | 도구 약 60개: 스케치, 피처, 어셈블리 메이트, 간섭 검사, 면 법선·질량·bbox, 멀티뷰 PNG, 도면 치수 OCR, FeatureScript, Variable Studios. 벤치마크 문서 [RESEARCH.md](https://raw.githubusercontent.com/ReshefElisha/jarvis-onshape-mcp/main/RESEARCH.md) | 중 | 172★ | MIT | 브라우저 CAD, 크기 변형 시리즈 |
| Onshape | [hedless/onshape-mcp](https://github.com/hedless/onshape-mcp) | 커뮤니티 | 도구 45개, 테스트 471개, STL/STEP/PARASOLID/GLTF/OBJ 익스포트 | 중 | 145★ | MIT | 테스트가 탄탄한 대안 |

**Onshape 벤치마크 읽는 법** (jarvis-onshape-mcp RESEARCH.md, Claude Opus 4.7, 개인 실험)

| 조건 | 단순 부품(Model Mania 2025) | 복잡 부품(2021) |
|---|---|---|
| 사람이 쓴 사양 | 1.000 | 0.615 |
| 모델이 도면을 스스로 비전 분해 | 0.533 | 0.000 |

- 점수는 "정확도"가 아니라 6개 층(바디 존재, 부피, bbox, 토폴로지, IoU, Chamfer)을 합친 **복합 점수**이고, 각 칸은 **1회 실행(n=1)** 입니다. 복잡 부품 자율 실행의 0.000은 151턴 한도에 걸려 export하지 못한 결과입니다.
- 원문이 꼽은 실패 원인: 파생 윤곽(derived outline), 극성(돌출·함몰 혼동), 8~12px 치수 텍스트 판독. 원문 결론은 "Opus 4.7 executes CAD reliably. It does not yet read engineering drawings reliably."
- 개선책 중 feature를 먼저 나열하는 plan-from-render만 +0.04(노이즈 수준)였고 나머지는 오히려 나빠졌습니다.
- Opus 5.5나 GPT-6 Astra로 다시 측정한 자료는 없습니다. 모델이 좋아져도 **치수는 텍스트로 주는 것**이 싸고 확실합니다. 모델 선택은 [01 가이드](01_ai_models_and_clients.md)를 보세요.

### 3.4 텍스처·2D·룩뎁·천

| 앱 | 서버 | 구분 | 핵심 기능 | 성숙도 | ★ · 최신 | 라이선스 | 추천 용도 |
|---|---|---|---|---|---|---|---|
| Substance 3D Painter | [elliezu/SubstancePainterMCP](https://github.com/elliezu/SubstancePainterMCP) | 커뮤니티(Adobe와 무관) | v1.0.0, 도구 79개(검사·진단 23, 레이어 편집 27, 익스포트·고급 29): fill/paint 레이어, 절차 파라미터, 마스크, Smart Material/Mask, 배치 베이크, 엔진 프리셋 익스포트. 트랜잭션 레이어 생성과 자동 롤백, 승인된 루트로 임포트 샌드박싱, 임의 Python은 `SP_MCP_ALLOW_EXECUTE_PYTHON=1`일 때만 | **높음** | 36★, 2026-07-28 | MIT | 게임 레디 텍스처 세트의 핵심 단계 자동화. Painter 12.1.1(Python API 0.3.5)에서 실검증. Ultikynnys 저장소는 이 저장소의 fork |
| Substance 3D Painter | [diffdaff/substance-painter-mcp](https://github.com/diffdaff/substance-painter-mcp) | 커뮤니티 | 단일 파일 FastMCP, 도구 10개(`create_fill_layer`로 JSON PBR 채널 배선, 대화상자 없는 `configure_and_bake`, PBR/Unreal/Unity 프리셋 `export_textures`) | 초기 | 1★ | MIT | 가볍게 시작할 때. Painter 10.x/11.x |
| Substance 3D Painter | [dcc-mcp-substance3d-painter](https://github.com/dcc-mcp/dcc-mcp-substance3d-painter) | 커뮤니티(dcc-mcp) | Painter 안 Streamable HTTP, Qt 메인 스레드 라우팅, project/material/compositing/lighting 스킬 | 초기 | — | MIT | 멀티 DCC 통합 |
| Substance 3D Designer | [matthieuhuguet/substance-designer-mcp](https://github.com/matthieuhuguet/substance-designer-mcp) | 커뮤니티 | stdio → Python 브리지 → TCP 9881 → SD 플러그인. 돌·금속·직물·지형 **레시피 79개**, `build_material_graph`가 노드 37~44개짜리 완전한 PBR 그래프를 한 번에 생성, `build_heightmap_graph`. README 본문은 "16 tools"라 하지만 도구 표에는 23개가 있고, 그중 임의 Python 실행 `execute_sd_code`도 있음 | 중 | 43★, 2026-05-10 | MIT | 타일링 절차 재질. SD 15.0.3에서 테스트. SD 16(OpenPBR, SDF 노드)은 미검증이며 대안으로 MikeLi-28의 SD 16.0.3용 서버(5★)가 있음 |
| Photoshop 외 Adobe 데스크톱 | [mikechambers/adb-mcp](https://github.com/mikechambers/adb-mcp) | 커뮤니티(PoC, "not endorsed by nor supported by Adobe") | MCP 서버 → Node 프록시 → 각 앱 UXP 플러그인. Photoshop 26.0+, Premiere Pro 25.3+, InDesign, After Effects, Illustrator | PoC | 715★ | MIT | **데스크톱 Photoshop 레이어 직접 제어**. UXP Developer Tool 설정 필요 |
| Photoshop | [alisaitteke/photoshop-mcp](https://github.com/alisaitteke/photoshop-mcp) | 커뮤니티 | UXP 기반 도구 118~122개(원자 도구 약 106 + 원스텝 레시피 16): 배경 제거, 리터칭, 색보정, 배치 처리, 생성형 채우기(Adobe 계정 필요) | 중(활발) | 522★ | MIT | 텍스처 원본 정리(색 균일화, 이음매, 크기 규격화), 알파·마스크. Windows·macOS, Node 18+ |
| Photoshop | [loonghao/photoshop-python-api-mcp-server](https://github.com/loonghao/photoshop-python-api-mcp-server) | 커뮤니티 | Photoshop Python API(Windows COM) | 중 | 305★ | — | Windows 배치 편집 |
| Marmoset Toolbag | [dcc-mcp-marmoset](https://github.com/dcc-mcp/dcc-mcp-marmoset) | 커뮤니티(dcc-mcp) | 씬 검사, 임포트, PBR 슬롯(Albedo/Normal/Roughness/Metallic/Occlusion) 지정, 카메라 렌더. 쇼케이스: FBX 임포트 → 텍스처 지정 → 프레이밍 → 1920×1080 렌더 | 초기 | 2★ | MIT | 포트폴리오 룩뎁 자동 조립. 베이크·턴테이블은 문서에 없음. Toolbag 4.03+/5.x |
| KeyShot | [truman-t3/keyshot-mcp](https://github.com/truman-t3/keyshot-mcp) | 커뮤니티 | `keyshot_headless` 스크립팅, 도구 19개(`keyshot_product_render` 원콜 제품 렌더, 배치 렌더, 카메라·머티리얼·환경) | 초기 | 15★, npm [0.12.1](https://www.npmjs.com/package/keyshot-mcp)(2026-09-02) | MIT | CAD 결과물의 제품샷·턴테이블. Windows 11, KeyShot Studio 2025/14.1, Node 20+. **장면 메타데이터·미리보기가 모델 제공자에게 전송될 수 있음**(README 경고) |
| Marvelous Designer | [ysk424/marvelous-designer-mcp](https://github.com/ysk424/marvelous-designer-mcp) | 커뮤니티 | MD 내장 Python 3.11에서 실행(TCP 127.0.0.1:7421). `import_project`(.zprj/.zpac/.obj/.fbx), `list_patterns`, `assign_fabric`, `simulate(steps)`, `export_project` | 초기 | 8★ | MIT | 옷·커튼·쿠션·테이블보 드레이프. MD 2026 또는 CLO 2026 필요. 같은 머신에서만 동작 |
| ComfyUI | [Comfy-Org/comfy-mcp](https://github.com/Comfy-Org/comfy-mcp) | **ComfyUI 공식** | 로컬 ComfyUI 워크플로 실행 | 중 | 237★ | — | 텍스처 생성 도구 다수가 ComfyUI 위에서 돌아감 → [05 가이드](05_texturing_materials.md) |

**텍스처 작업에서 도구 고르는 기준**
- 참조 이미지 정리, 배경 제거, 간단한 생성형 편집: Adobe for creativity(설치 없음, 원격).
- PSD 레이어·채널을 직접 다루는 작업, 타일링 소스 정리: adb-mcp 또는 alisaitteke/photoshop-mcp(로컬).
- 노멀·러프니스 등 **PBR 채널 간 일관성**이 중요한 작업: Photoshop이 아니라 Substance Painter/Designer MCP.

### 3.5 USD 허브와 멀티 DCC 프레임워크

| 이름 | 성격 | 핵심 | ★ · 상태 | 라이선스 | 쓰는 곳 |
|---|---|---|---|---|---|
| [NVIDIA kit-usd-agents](https://github.com/NVIDIA-Omniverse/kit-usd-agents) | 벤더 공식(지식형) | USD Code MCP(도구 7), Kit MCP(12, `:9902/mcp`, Docker), OmniUI MCP(10), Isaac Sim MCP(5). **API·문서·코드 예제 검색 전용**, 실시간 편집은 Chat USD 확장 담당. NVIDIA API 키 필요, 외부 기여 안 받음 | 96★ | Apache-2.0 | USD 코드를 쓸 때 API 환각 줄이기 |
| [daslabhq/openusd-mcp](https://github.com/daslabhq/openusd-mcp) | 커뮤니티 | `pip install openusd-mcp`. `usd_inspect`, `get_prim`, `get_materials`, `get_transforms`, `list_variants`, `set_variant`, `export_mesh`(STL/OBJ), `scene_stats` | 10★ | MIT | USD 파일 검사, 베리언트 전환 |
| [dcc-mcp-openusd](https://github.com/dcc-mcp/dcc-mcp-openusd) | 커뮤니티(dcc-mcp) | project, stage, validate(USDZ 패키징), material, light-camera, animation, composition(서브레이어, 페이로드, 베리언트) 스킬 7개 | 초기 | MIT | 여러 DCC 결과를 USD로 조립·검증, 가구 색·크기 베리언트 관리 |
| [dcc-mcp-core](https://github.com/dcc-mcp/dcc-mcp-core) | 멀티 DCC 프레임워크 | "Skill-first, Rust-powered control plane". Gateway(`http://127.0.0.1:9765/mcp`)가 `search`/`describe`/`load_skill`/`call` 4개 래퍼만 노출해 도구 수 폭발을 막음. 스킬 계약은 SKILL.md + tools.yaml. [조직 저장소 91개](https://github.com/orgs/dcc-mcp/repositories)(Maya, Blender, Houdini, 3ds Max, Nuke, Katana, MotionBuilder, ZBrush, Photoshop, Substance, Marvelous, Marmoset, SpeedTree, Gaea, OpenUSD, Unreal, Unity, Godot, RenderDoc, Krita, GIMP 등) | core 47★, core/cli 0.20.35(2026-09-26), 커밋 2,684개 | MIT | 한 에이전트가 Maya → Substance → Marmoset → Unreal을 오가는 파이프라인. **1인 주도, 어댑터 대부분 pre-alpha~beta, [showcase](https://github.com/dcc-mcp/showcase)는 비어 있음(신뢰도 낮음: 0~1★ 어댑터가 일괄 생성된 조직이라는 검증 지적)** |
| [ArtClaw Bridge](https://github.com/IvanYangYangXi/artclaw_bridge) | 멀티 DCC 브리지 | DCC 에디터 안 채팅 패널 + MCP 브리지, 공식 스킬 47개(중·영 문서). 검증 환경: UE 5.7, Maya 2023, 3ds Max 2023, Blender 5.1, Substance Painter 11.0.1, Substance Designer, ComfyUI | 36★, Beta | MIT | 아티스트용 인에디터 채팅 |
| [VFX Agent Toolkit](https://github.com/sideshowroberto/vfx-agent-toolkit) | Claude Code 플러그인 마켓 | 리드 VFX 아티스트 제작. Nuke, Houdini, UE, Blender, ComfyUI, Maya 스킬·커넥터("skills teach the craft; connectors give it hands") | 9★ | MIT | 스킬과 실행 권한을 분리하는 설계 참고 |
| [Flue](https://github.com/SFKislev/Flue) | CLI 브리지(MCP 아님) | `pip install flue` → `flue setup`만으로 Photoshop, Illustrator, AE, Blender, Unity, Houdini, 3ds Max 제어 | 87★ | MIT | MCP 도구 스키마가 컨텍스트를 너무 차지할 때 |
| [AI Forge MCP](https://github.com/HurtzDonutStudios/ai-forge-mcp) | 상용 Early Access | MCP 서버 16개·도구 565개(UE5, Blender, Substance Painter/Designer, Maya, Houdini, UniRig, Hunyuan3D, Audio2Face 등) **(벤더 자체 보고)**. Founder 가격 Solo $35/월(MSRP $79), Duo $65, Studio $149 | 93★ | 상용 | 멀티 DCC 파이프라인 구성 참고용. **근거 자료로 쓰지 말 것**: "AI Legends MMO 제작"은 미검증 자기 주장이고, Hunyuan3D를 "MIT"라고 잘못 적었음. **한국에서 ForgeHunyuan 경로는 라이선스 밖** |
| [Pascal Editor](https://github.com/pascalorg/editor) | 오픈소스 건축 에디터 + MCP | 벽·슬래브·천장·지붕·가구 배치. `pascal-3d` 스킬(안전한 MCP 설정·씬 조작), `furniture-fit` 스킬(증거 기반 가구 풋프린트 판정). `npx @pascal-app/cli editor`(Node 22.13+) | **24.3k★**, npm [@pascal-app/cli 1.0.3](https://www.npmjs.com/package/@pascal-app/cli)(2026-09-24) | MIT | 방 레이아웃·가구 배치 초안 → [08 배치 가이드](08_scene_layout_placement.md) |

### 3.6 없거나 쓸 수 없는 것

| 앱 | 상태 | 대안 |
|---|---|---|
| Womp | GitHub 검색 결과에 Womp 3D용 MCP 없음(검색하면 결제 서비스 Wompi만 나옴) | STL/OBJ로 수동 내보낸 뒤 다른 MCP DCC에서 후처리 |
| Plasticity | [PlasticityMCP](https://github.com/ozymandi/PlasticityMCP): "Phase 0 — recon. Not yet usable.", 라이선스 TBD, 2026-04-28 이후 멈춤 | Plasticity → Blender 브리지 → Blender MCP로 우회 |
| Spline | [spline-mcp-server](https://github.com/aydinfer/spline-mcp-server): 아카이브. Spline에 공개 REST API가 없어 도구 약 130개가 동작하지 않고 `@splinetool/runtime` 코드 생성 도구 10개만 작동 | 임베드 코드는 MCP 없이 LLM에게 바로 쓰게 함 |
| KeyShot 공식 | 없음(커뮤니티 keyshot-mcp 1개뿐) | 3.4절 |
| Maya·3ds Max·MotionBuilder 공식 | Autodesk 공식 MCP 없음 | 3.2절 커뮤니티 |
| Substance 3D 공식 | Adobe 공식 MCP 없음. Sampler 단독 MCP도 AI Forge 구성 요소 외에는 못 찾음 | 3.4절 커뮤니티 |
| Maxon(C4D·ZBrush) 공식 | 확인되지 않음 | 3.2절 커뮤니티 |
| Onshape(PTC) 공식 | 확인되지 않음 | 3.3절 커뮤니티 |

### 3.7 설치·설정 요점

**Rhino (McNeel 공식, Claude Desktop 기준)**

```text
1) connector.mcpb 받기: mcneel/RhinoMCP 저장소 릴리스(connector-v0.1.3)
   https://github.com/mcneel/RhinoMCP/releases
2) Claude Desktop → Settings → Extensions → Advanced settings → Install Extension
3) Rhino 플러그인 설치: Rhino 안이 아니라 동봉된 Yak CLI로 실행(또는 Package Manager)
   macOS  : "/Applications/Rhino 8.app/Contents/Resources/bin/yak" install Rhino-MCP-Platform
   Windows: "C:\Program Files\Rhino 8\System\Yak.exe" install Rhino-MCP-Platform
4) Rhino 재시작 → 명령창에서 MCPStart
※ GH2 결과물이 필요하면 Rhino 9(WIP) 권장
```
근거: [connector.md](https://raw.githubusercontent.com/mcneel/RhinoAI/rhino-9.x/docs/content/docs/getting-started/connector.md). Claude Code, Codex, Gemini CLI, Cursor, LM Studio에서도 쓸 수 있습니다.

**Houdini (fxhoudinimcp)**

```bash
pip install fxhoudinimcp
python -m fxhoudinimcp install          # Houdini 패키지 파일 작성 + 설치된 MCP 클라이언트에 자동 등록
export FXHOUDINIMCP_PROJECT_ROOT=/path/to/project   # 파일 경로 샌드박스
```
자동 등록 대상: Claude Desktop/Code, Cursor, VS Code, Windsurf, Copilot CLI, Gemini CLI, Codex, Cline.

**Maya (GG_MayaMCP)**: `pip install maya-mcp`(또는 소스, Claude Desktop은 `.mcpb`). raw 코드 실행은 꼭 필요할 때만 `MAYA_MCP_ENABLE_RAW_EXECUTION=true`.

**dcc-mcp (멀티 DCC)**

```bash
uv tool install dcc-mcp-cli        # 또는 pipx install dcc-mcp-cli
pip install dcc-mcp-core
mayapy -m pip install dcc-mcp-maya # 어댑터 예시(Maya). 이후 Plug-in Manager에서 로드
export DCC_MCP_GATEWAY_REMOTE_PORT=0   # sidecar의 LAN gateway(59765) 끄기 — 스튜디오 네트워크에서 필수
```
MCP 클라이언트 설정은 gateway 하나만 등록합니다: `{"mcpServers": {"zbrush": {"url": "http://127.0.0.1:9765/mcp"}}}`(ZBrush README 예시).

**Cinema 4D (kumoproductions)**: 보안 게이트를 켠 상태로만 씁니다.

```bash
C4D_MCP_ENABLE_EXEC_PYTHON=1      # 서버와 플러그인 양쪽
C4D_MCP_ENABLE_PYTHON_OPS=1
C4D_MCP_TOKEN=<공유 비밀>
# C4D_MCP_ALLOW_REMOTE=1 은 원격 접속을 허용하므로 켜지 말 것
```

**Substance 3D Painter (SubstancePainterMCP)**: Painter를 `--enable-remote-scripting` 플래그로 실행하면 `localhost:60041` HTTP 엔드포인트가 열립니다. MCP 서버(Python 3.10+)를 등록한 뒤 메시 로드 → 베이크(노멀/AO/커버처/곡률) → Smart Material → 파라미터 조정 → Unreal/Unity 프리셋 익스포트 순서로 진행합니다.

**Substance 3D Designer**: 브리지는 Python 3.12+, Designer 내부는 3.11, 설치는 uv. 클라이언트에서 **병렬 도구 호출을 끄세요.**

**Onshape**: 서버마다 환경변수 이름이 다릅니다. 하나로 묶어 안내하면 틀립니다.

| 서버 | 키 |
|---|---|
| jarvis-onshape-mcp | `ONSHAPE_API_KEY` / `ONSHAPE_API_SECRET`(OS 키체인에 저장) |
| hedless/onshape-mcp | `ONSHAPE_ACCESS_KEY` / `ONSHAPE_SECRET_KEY` |

**그 밖의 한 줄 설치**

| 서버 | 명령·방법 |
|---|---|
| FreeCAD (neka-nat) | 애드온을 FreeCAD 애드온 디렉터리에 넣고, uvx로 MCP 서버를 Claude Desktop 설정에 등록 |
| FreeCAD Robust | `pip install freecad-robust-mcp`, 소스, 또는 Docker(Addon Manager 설치는 확인 못 함) |
| AgentCAD | `agentcad[mcp]` extra를 설치한 뒤 Claude Code·Cursor·Windsurf에 연결 |
| KeyShot | `npx -y keyshot-mcp@0.12.1`(Node 20+) |
| Pascal Editor | `npx @pascal-app/cli editor`(Node 22.13+) |
| Marvelous Designer | MD Python Editor에서 리스너(`md_listener.py`) 실행. C++ SDK 불필요. **리스너가 도는 동안 GUI가 멈추는 것이 정상** |
| adb-mcp | UXP Developer Tool로 플러그인 로드 → Node 프록시 실행 → Claude Desktop 또는 OpenAI Agent SDK 연결 |
| 3dsmax-mcp | Windows 인스톨러(Python, 의존성, 네이티브 브리지 포함) → Max 메뉴에서 MCP 시작 → Claude Desktop, Codex, Cursor, OpenCode 연결 |

---

## 4. 게임 엔진·실시간 3D MCP

### 4.1 Unreal Engine

#### 4.1.1 Epic 공식 Unreal MCP (UE 5.8, Experimental)

| 항목 | 내용 |
|---|---|
| 정체 | 에디터 프로세스 안에서 MCP 서버를 띄우는 1st-party 실험 플러그인 `ModelContextProtocol`(엔진 경로 `Engine/Plugins/Experimental/ModelContextProtocol`). 도구는 Toolset Registry와 **AllToolsets** 플러그인이 제공 |
| 기본 주소 | `http://127.0.0.1:8000/mcp`(localhost 바인딩) |
| 출시 | UE 5.8, 2026-06-17(Unreal Fest Chicago) **(보도 기준, Epic 원문 미확인)**. 커뮤니티 첫 실작업 기록이 2026-06-20이라 6월 중순 출시와 모순되지는 않음 |
| 확인된 툴셋 예 | SceneTools, ActorTools, ObjectTools, StaticMeshTools, MaterialTools, MaterialInstanceTools, PCGToolset, PCGSpatialToolset, EditorAppToolset(CaptureViewport) |
| 툴셋 규모 | **출처마다 다름**: per-simmons 약 28개, Epic README "30+ toolsets", UnrealEngine_Bridge "Epic MCP 830 tools", 백포트 키트 "40개 툴셋·414개 서브툴"(1★ 저장소). 한 숫자를 사실처럼 인용하지 마세요 |
| 호출 방식 | tool search 방식. `list_toolsets` → `describe_toolset` → `call_tool`. `toolset_name`(예: `"PCGToolset.PCGToolset"`)과 `tool_name`(예: `"AddNode"`)을 따로 넘김 |
| 커스텀 도구 | C++(`UModelContextProtocolToolLibrary`)나 Python으로 추가. **추가 뒤 에디터 완전 재시작 필요**(Live Coding으로 반영 안 됨) |
| 약점 | Experimental이라 API·포맷이 바뀔 수 있음. 인증 계층 없음(origin 검증만). 프로젝트를 바꾸면 이전 서버가 종료됨. 포스트프로세스·레이트레이싱·Megascans 전용 도구가 빈약. 프로젝트 전체를 한 번에 파악하지 못하고 호출 하나씩 탐색 |
| 문서 | [Epic 공식 문서](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor?lang=en-US)(조사 환경에서 열람 불가), [per-simmons 활성화 문서](https://github.com/per-simmons/unreal-agent-harness/blob/master/docs/UNREAL-MCP-ENABLE.md) |

**켜는 순서**

```text
1) .uproject에서 플러그인 활성화: ModelContextProtocol, AllToolsets
   (Toolset Registry는 자동으로 켜짐. PythonScriptPlugin도 켜라는 기록은 per-simmons 문서에만 있음)
   ※ UE 5.8에서 두 플러그인이 스스로 켜진다는 보고도 있어 환경마다 다를 수 있음
2) 에디터 콘솔:
   ModelContextProtocol.StartServer 8123            # 기본 8000은 다른 프로그램과 자주 충돌
   ModelContextProtocol.GenerateClientConfig ClaudeCode   # 또는 Codex → 프로젝트 루트에 .mcp.json 생성
3) 자동 시작: Saved/Config/<Platform>Editor/EditorPerProjectUserSettings.ini 에
   bAutoStartServer=True
   ServerPortNumber=8123
   ServerUrlPath=/mcp
4) 안전을 위해 DefaultEngine.ini 에 bRemoteExecution=False (per-simmons 권장)
5) 연결 확인: SceneTools.get_current_level 호출
```

**빌드 요구에 관한 상충 정보**: ibrews/ue5-mcp README는 공식 플러그인이 "requires a source build of the engine"이라고 적었지만, per-simmons는 Epic Games Launcher판 UE 5.8로 작업했습니다. ibrews 쪽은 프리뷰 시절 정보로 보입니다.

**`execute_tool_script`는 샌드박스가 아닙니다.** per-simmons 문서는 소스(허용 모듈 목록, AST 검사, import hook)를 근거로 이 스크립트에서 `unreal` 모듈을 쓸 수 없고 `json`, `math`, `datetime`, `copy`, `re`, `time`만 import된다고 적었습니다([programmatic-toolset-capabilities.md](https://github.com/per-simmons/unreal-agent-harness/blob/master/docs/programmatic-toolset-capabilities.md)). 하지만 Epic README는 "executes arbitrary Python … full access to every toolset API, the project on disk, the asset database"라고 경고합니다. 등록된 툴셋 API로 프로젝트 콘텐츠를 바꾸거나 지울 수 있는 **특권 연산**으로 다루세요.

**UE 5.7 이하에서 쓰려면**: [MC-Oruc/UE57-MCP-PortKit](https://github.com/MC-Oruc/UE57-MCP-PortKit)이 5.8 소스를 받아 플러그인을 프로젝트 로컬로 이식합니다(머티리얼 그래프 원자적 JSON 변경·롤백·컴파일 진단 포함). 1★·28커밋 규모라 수치 주장은 신뢰도 낮음으로 보세요. 커뮤니티 서버(ChiR24)가 더 무난합니다.

**UE6 계획**: Epic이 State of Unreal 2026에서 UE6에 Claude·Gemini를 MCP로 통합한다고 발표했고 Early Access는 2027년 말 목표라는 보도가 있습니다([The Next Web](https://thenextweb.com/news/epic-unreal-engine-6-ai-claude-gemini)). **1차 출처로 확인하지 못했습니다(미확인).** 방향만 참고하세요.

#### 4.1.2 Epic 공식 Claude Code 플러그인

[EpicGames/unreal-engine-skills-for-claude-code-plugin](https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin)(MIT, 308★, 커밋 53개, 2026-04~09 활발)

```text
/plugin install unreal-engine-skills-for-claude-code@claude-plugins-official
```

- 제공: `unreal-mcp` 스킬([SKILL.md](https://raw.githubusercontent.com/EpicGames/unreal-engine-skills-for-claude-code-plugin/main/skills/unreal-mcp/SKILL.md)), SessionStart hook, **에디터를 재시작해도 MCP 세션을 유지하는 실험적 프록시**(`Engine/Plugins/Experimental/ModelContextProtocol/Extras/Proxy`).
- 스킬 지침 요약: `list_toolsets`/`describe_toolset`으로 먼저 도구를 파악하고, 일괄 변경 전에 저장하고(MCP 편집은 항상 undo되지는 않음), 의존 호출은 순차로 실행하고, 도구가 실패해도 예외를 던지지 않는 경우가 많으니 결과를 검증합니다.
- 보안 경고(README 원문): "Localhost is not a trust boundary", `ProgrammaticToolset.execute_tool_script`는 임의 Python 실행.
- README·[setup.md](https://raw.githubusercontent.com/EpicGames/unreal-engine-skills-for-claude-code-plugin/main/skills/unreal-mcp/references/setup.md)에는 필요한 UE 버전이 적혀 있지 않습니다. "5.8부터"는 커뮤니티 자료 근거입니다.
- Codex용으로는 이 플러그인을 바탕으로 한 [WildCake/unreal-engine-mcp-codex](https://github.com/WildCake/unreal-engine-mcp-codex)가 있습니다(헤드리스 러너 로그는 `Saved/AgentRuns/`). Codex에서 GPT-6 Astra를 쓸 때는 기본 reasoning effort가 low이므로 effort를 직접 지정하세요([01 가이드](01_ai_models_and_clients.md)).

#### 4.1.3 커뮤니티 Unreal 서버

| 서버 | 핵심 | UE 버전 | ★ · 최신 | 라이선스 | 추천 용도 |
|---|---|---|---|---|---|
| [ChiR24/Unreal_mcp](https://github.com/ChiR24/Unreal_mcp) | TS 서버 + C++ `McpAutomationBridge`. v0.6.0-beta-a부터 단일 `unreal` 게이트웨이 도구(search/describe/execute/configure)로 재편(원래 canonical tool 23개). `build_environment`(landscape, foliage, 절차 지형, spline 도로·강·펜스), `manage_pcg`, `sculpt_landscape`, `paint_foliage`, `configure_sky_atmosphere`, 높이 안개, 볼류메트릭 클라우드, time-of-day, weather, `convert_to_nanite`, 스크린샷, PIE, Sequencer, MRQ. 기본 capability token 인증 + loopback 전용 | 5.0~5.8 | 888★, v0.6.0-beta-b(2026-09-25, npm beta 태그. stable은 0.5.30) | MIT | **환경 아트 도구가 가장 많음.** 공식 MCP의 빈틈 보완. 단 [로드맵](https://github.com/ChiR24/Unreal_mcp/blob/main/docs/Roadmap.md)상 post-process(노출·블룸·DOF·컬러그레이딩), 레이트레이싱, Lumen 반사, Megascans/Fab 임포트는 미구현 → Python 우회 |
| [flopperam/unreal-engine-mcp](https://github.com/flopperam/unreal-engine-mcp) | 현재 **Aura 소유**. 로컬판: `create_town`, `construct_mansion`, `create_castle_fortress`, `create_suspension_bridge`, `create_maze` 같은 월드빌딩 도구, BP 그래프, 머티리얼·액터 관리(TCP 소켓, C++ 플러그인 빌드) | 5.5~5.7 | 1.1k★, 97커밋, 릴리스 태그 없음 | MIT(로컬판) | **블록아웃·스케일 검토.** 결과가 프리미티브 조합이라 AAA 룩과는 거리가 멂. 호스팅판(`agent.flopperam.com/mcp`, 9개 도메인 50개 이상 도구, FlopAI Unreal 플러그인 필요)은 유료. "64개 중 46개 무료"는 미확인 |
| [chongdashu/unreal-mcp](https://github.com/chongdashu/unreal-mcp) | 원조 격. C++ TCP 서버(55557) + Python FastMCP. 액터·BP 클래스·노드 그래프·뷰포트 카메라. UE 5.5 스타터 프로젝트 포함 | 5.5+ | 2.1k★, 345 forks, 33커밋 | MIT | 학습·포크 기반. 5.6 호환(#31), 버전 불일치(#43), 연결 실패(#23, #32) 이슈가 쌓여 있고 머티리얼·조명 도구가 빈약 |
| [runreal/unreal-mcp](https://github.com/runreal/unreal-mcp) | **UE 플러그인 설치 불필요**. 내장 Python Remote Execution 사용. 도구 20개(에셋 검색·export, 액터 CRUD, 스크린샷·카메라, 콘솔 명령, Python 실행) | 5.4+ | 115★, 24커밋 | MIT | C++ 빌드가 어려운 Blueprint 전용 프로젝트. 에디터 전체 권한을 넘기는 구조 |
| [GenOrca/unreal-mcp](https://github.com/GenOrca/unreal-mcp) | 21개 도메인·253개 액션(도메인마다 도구 하나가 action/params를 받음). 뷰포트·임의 포즈 캡처에 **액터 라벨을 이미지 위에 찍어** MCP Image로 반환. `execute_python`. 엔진 버전별 사전 컴파일 릴리스, Fab 배포 | 5.6+ | 144★, 2026-07-07 | Apache-2.0 | **배치 수정 루프의 시각 피드백.** VLM이 화면 속 물체와 액터 이름을 정확히 연결 |
| [tumourlove/monolith](https://github.com/tumourlove/monolith) | UE용 MCP 플러그인. 머티리얼 그래프·인스턴스 읽기/쓰기, `material_query('compile')` 등(텍스처 주제 검증 단계에서 추가된 항목이라 세부 기능은 미검증) | 5.7/5.8 | 316★ | MIT | **엔진에서 최종 머티리얼 조립** |
| [IvanMurzak/Unreal-MCP](https://github.com/IvanMurzak/Unreal-MCP) | C++ 플러그인 + .NET 사이드카, 도구 61개(액터·컴포넌트 13, BP 11, 에셋 11, 리플렉션 9, 레벨 7, C++ 편집 6, 스크린샷 4). 도구별 on/off | 5.5+(CI 5.7·5.8) | 40★, Beta | Apache-2.0 | 도구를 골라 켜고 싶을 때 |
| [JosephOIbrahim/UnrealEngine_Bridge](https://github.com/JosephOIbrahim/UnrealEngine_Bridge) | ViewportPerception C++ 플러그인(`:30011`)의 `ue_viewport_percept`/`watch`/`diff`로 연속 시각 인지·스냅샷 diff. 공식 MCP(`:8000`)와 병행 운용 문서화 | 5.8 | — | — | 공식 MCP에 "눈" 달기 |
| [oliver-io/unreal-harness](https://github.com/oliver-io/unreal-harness) | 자체 TS/C++ MCP, 에디터 액션 약 285개, 스킬 20개 이상. 플레이 가능한 멀티플레이 게임(HOVERBALL) 제작 사례 포함 | 5.7 | — | — | 게임플레이까지 가는 하네스 참고 |
| [PeterTXPan/dsh-unreal-mcp](https://github.com/PeterTXPan/dsh-unreal-mcp) | UE 5.8 공식 MCP에 DeepSeek 연동 번들(2026-08-30) | 5.8 | — | — | Claude 외 모델로 공식 MCP 구동 |
| [ThePecerowski/UEBPCracker](https://github.com/ThePecerowski/UEBPCracker) | 계약 검증 기반 Blueprint 자동화(2026-09) | 5.8 | — | — | BP 자동화 |
| 기타 | [kvick-games/UnrealMCP](https://github.com/kvick-games/UnrealMCP)(UE 5.5 전용 초기 WIP, 612★), [UnrealGenAISupport](https://github.com/prajwalshettydev/UnrealGenAISupport)(UE 5.4~5.7, MCP 기능 개발 중단, 650★), unreal-ai-connection(UE 5.7, 도구 105개), ue5-automation(BP 노드, UFUNCTION 59개) | | | | 대부분 1인 프로젝트, 유지보수 리스크 |

상용 제품 StraySpark(“200+ tools”), Ludus AI, Aura는 판매자 홍보 글이나 경쟁사 블로그만 있어 **도구 수 등 주장을 검증하지 못했습니다**(벤더 자체 보고).

#### 4.1.4 스킬·하네스 (서버 위의 지식 레이어)

| 이름 | 내용 | 주의 |
|---|---|---|
| [ibrews/ue5-mcp](https://github.com/ibrews/ue5-mcp) (UE5 MCP Field Manual, [SKILL.md](https://github.com/ibrews/ue5-mcp/blob/main/SKILL.md)) | Claude Code/Cowork 스킬. 크래시 시그니처(MetaSound Audio 핀, 참조 중인 메시 삭제), 조용한 실패(PascalCase, `_C`, RootComponent), Sequencer 함정, Python 출력 우회. v3.3.0(2026-08-08), MIT, 서버 무관 | "왕복 검증을 하면 99%, 안 하면 80%"는 **정량 근거 없음**. SKILL.md의 "Lumen GI는 Movable 라이트만 반영"과 "MovieRenderGraph는 5.8 전용"은 **틀림**(6.2절) |
| [per-simmons/unreal-agent-harness](https://github.com/per-simmons/unreal-agent-harness) | Claude + UE 5.8 공식 MCP 제작 전 과정 문서(ue_qa.py 캡처 디코더, 3앵글 QA, 헤드리스 Blender, PCG 레시피, 조명 계획). 196★ | 4.1.6절의 정정 사항 참고 |
| [WildCake/unreal-engine-mcp-codex](https://github.com/WildCake/unreal-engine-mcp-codex) | 공식 MCP용 Codex 스킬(2026-06-20) | — |
| [mMo66666/Unreal-MCP-Skills](https://github.com/mMo66666/Unreal-MCP-Skills) | 레벨 디자인·시네마틱용 Codex 스킬(중국어) | — |

Claude Code는 `.claude/skills`에 넣습니다. Codex는 `~/.codex/skills`와 저장소의 `.agents/skills`가 모두 보고돼 있으니(공식 문서 미확인) 설치한 Codex 버전에서 인식되는 쪽을 확인하세요. 어느 쪽이든 작업 전에 스킬 문서를 읽으라고 지시합니다. 이 저장소의 [스킬 템플릿](../03_playbooks/templates/skills/blender-aaa-scene/SKILL.md)과 같은 방식입니다.

#### 4.1.5 Unreal 서버 고르는 기준

| 상황 | 주력 | 보강 |
|---|---|---|
| UE 5.8 이상, 새 프로젝트 | 공식 Unreal MCP + Epic Claude Code 플러그인 | 환경(landscape·foliage·하늘·날씨)은 ChiR24, 시각 인지는 GenOrca 또는 UnrealEngine_Bridge, 머티리얼 그래프는 monolith |
| UE 5.5~5.7 | ChiR24 | GenOrca(5.6+), IvanMurzak, 블록아웃은 flopperam(5.5~5.7), 공식 툴셋이 꼭 필요하면 PortKit |
| C++ 빌드가 어려움(Blueprint 전용) | runreal(플러그인 불필요) | ChiR24(C++ 클래스 하나 추가하면 컴파일 가능), GenOrca 사전 컴파일 릴리스 |
| 포스트프로세스·Lumen 반사·Megascans 임포트 | 전용 도구 없음 | Python 실행으로 우회, 조명 수치는 6.2절의 화이트리스트 안에서 |
| 게임플레이·BP까지 | 공식 MCP | ue5-automation, UEBPCracker, oliver-io 하네스 참고 |

#### 4.1.6 참고할 공개 기록 (정정 포함)

| 기록 | 내용 | 검증 결과 |
|---|---|---|
| [per-simmons/unreal-agent-harness](https://github.com/per-simmons/unreal-agent-harness) (2026-06~) | Claude + UE 5.8 공식 MCP. PCG로 글래스 grammar 타워 49개(7×7, ISM 147, 빈 스폰 0, 2026-06-21 ITER 5~7). 같은 날 ITER 8에서 글래스 타워 14개를 실제 City Sample 레벨(Small_City_LVL)에 배치. 파리 오스만 블록(파사드 변형 12, 톤 5, 가로수 20, 가로등 12, 벤치 6, 차량 5), 청동 장식이 들어간 아르데코 블록. 결론: "real but raw" | 49개 도시는 "City Sample 위"가 아니라 City Sample 프로젝트 안의 빈 Startup 맵(`/Game/Map/Startup/Startup`)에 있고, 벽돌이 아니라 글래스 타워입니다(벽돌은 ITER 2~3). **SF 실내는 계획만 있고 조립은 대기 상태**([ENVIRONMENTS.md](https://github.com/per-simmons/unreal-agent-harness/blob/master/docs/ENVIRONMENTS.md)). Cesium NYC는 "documented" 상태 **(개인 사례, n=1)** |
| [44-99/unreal-agent-benchmark](https://github.com/44-99/unreal-agent-benchmark) (2026-07-28) | Codex + UE 5.8 MCP로 "플레이 가능한 패키지 게임"을 만들 수 있는지 평가하는 과제 3개와 100점 채점표(플레이 루프 50, 엔지니어링 15, 패키징 10, 자율 복구 10, 시각 품질 10, 효율 5). 컴파일→PIE→저장 후 재오픈→Win64 패키징→패키지 실행→스모크 테스트 6개 게이트 | **점수 미발표.** 데모와 제품의 차이를 보는 비판적 기준으로 참고 |
| Chong-U 데모(2025-03) | Cursor + Claude + chongdashu/unreal-mcp로 Flappy Bird 클론 | 그래픽이 아니라 게임플레이 프로토타이핑 |
| flopperam 쇼케이스 | 마을·성·저택·미로 생성 | 블록아웃 수준 |

사례 전체는 [사례 모음](../04_case_studies/01_case_studies.md)에 정리돼 있습니다.

### 4.2 Unity

| 서버 | 구분 | 핵심 | 버전 | ★ · 최신 | 라이선스 | 추천 용도 |
|---|---|---|---|---|---|---|
| Unity MCP (`com.unity.ai.assistant`) | **공식** | Unity가 시작되면 MCP bridge가 로컬 IPC(Windows named pipe, macOS/Linux Unix socket)를 열고, 클라이언트는 `~/.unity/relay/`의 relay 바이너리를 MCP 서버로 실행. 도구 예: `Unity_ManageScene`, `Unity_ManageGameObject`, `Unity_Camera_Capture`, Game View 스크린샷. 설정: Edit > Project Settings > AI > Unity MCP에서 Unity Bridge가 Running인지 확인 | Unity 6 이상(정확한 최소 버전 **미확인**: 구버전 1.0.0-pre.12 [미러](https://github.com/needle-mirror/com.unity.ai.assistant)는 6000.2 요구) | 2.x pre-release | Unity 구독·AI 크레딧(**요금 미확인, 싣지 않음**) | Unity 6 신규 프로젝트. HDRP Volume·조명 전용 도구는 확인 못 함 |
| [CoplayDev/unity-mcp](https://github.com/CoplayDev/unity-mcp) (MCP for Unity) | 커뮤니티(Aura 후원) | 도구 엔트리포인트 47개(`manage_scene`, `manage_gameobject`, `manage_material`, `manage_asset`, `read_console` 등), VFX·애니메이션·UI·테스트 도구 그룹, 멀티 인스턴스 라우팅, Roslyn 스크립트 검증. v10부터 [에셋 생성](https://github.com/CoplayDev/unity-mcp/blob/main/docs/asset-gen-manual-verification.md): `generate_model(provider=tripo\|meshy, mode=text\|image, format=fbx\|glb)`, Sketchfab `import_model`(search/import), 2D는 fal.ai·OpenRouter | 2021.3 LTS~6.x | **14.5k★**, v10.2.0(2026-09-01) | MIT | **Unity 1순위.** "조달부터 배치까지" 한곳에서. 조명·HDRP·ProBuilder 전용 기능은 없어 일반 컴포넌트 조작으로 처리 |
| [IvanMurzak/Unity-MCP](https://github.com/IvanMurzak/Unity-MCP) (AI Game Developer) | 커뮤니티 | 도구 70개 이상, 에디터와 빌드된 런타임 모두 동작. `assets-material-create`, `assets-shader-list-all`, `assets-prefab-*`, `scene-*`, `screenshot-camera`/`game-view`/`scene-view`, **`screenshot-isolated`**(대상 오브젝트만 단독 렌더, 선택적 2×2 합성). C# 메서드에 속성 한 줄로 도구 추가 | — | 4.3k★, 3,088커밋 | Apache-2.0 | **가구·소품 하나를 떼어 형태 검수.** 프로젝트 경로에 공백 금지 |
| [german-krasnikov/unity-biome-mcp](https://github.com/german-krasnikov/unity-biome-mcp) | 커뮤니티 | 도구 160개(Shader Graph, 머티리얼, Timeline, 파티클), Game View 베이스라인 비교·diff, PlayTest DSL | Unity 6 | v2.1.0(2026-09-25), 소규모 | — | Shader Graph 편집, 스크린샷 회귀 검증 |
| [Unity-Technologies/industry-ai-workflows](https://github.com/Unity-Technologies/industry-ai-workflows) | **공식 실험** | Claude Code 플러그인 마켓: Asset Manager(uam-mcp), **Asset Transformer**(uat-mcp, Pixyz SDK 기반, 로컬 작업에 Pixyz 라이선스 좌석 필요), Pipeline Automation(upa-mcp) | — | 2★ | Unity ToS "Experimental / Evaluation Version"(source-available, 오픈소스 아님) | CAD·대용량 3D를 게임용으로 경량화 |
| 기타 | 커뮤니티 | [CoderGamester/mcp-unity](https://github.com/CoderGamester/mcp-unity), [patina-unity-mcp](https://github.com/taygunsavas/patina-unity-mcp)(Rust 서버 + C# 브리지, 명령 86개), unity-ai-bridge(파일 기반 IPC, 도구 62개), [Unity MCP Pro](https://unity-mcp.abyo.net/)(유료, "280+ tools"는 벤더 자체 보고) | | | | |

- Unity AI 오픈 베타(2026-05-04 보도)와 3D Mesh·Material·Texture 생성기, 외부 에이전트를 Assistant 창에서 쓰는 AI Gateway가 소개됐지만 공식 문서가 조사 환경에서 모두 차단돼 **요구 버전·설정 경로·요금·날짜를 1차 확인하지 못했습니다.** [Unity 공식 블로그](https://unity.com/blog/unity-ai-mcp-how-to-get-started)를 직접 확인하세요.
- 선택: Unity 6 + 공식 AI 기능을 쓸 계획이면 공식 MCP, 그 외(특히 2021.3~2023 LTS)는 CoplayDev, 형태 검수 루프에는 IvanMurzak을 곁들이세요.

**CoplayDev 설치**

```text
Package Manager → Add package from git URL:
  https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#main
Window → MCP for Unity → Configure All Detected Clients     (Python 3.10+ 필요)
3D 생성 키: Window → MCP for Unity → Asset Gen 탭 (OS 키체인에 저장)
```

### 4.3 Godot

| 서버 | 핵심 | 요구 | ★ · 최신 | 라이선스 | 추천 용도 |
|---|---|---|---|---|---|
| [Coding-Solo/godot-mcp](https://github.com/Coding-Solo/godot-mcp) | 경량 13개 기능: 에디터·프로젝트 실행, 디버그 출력, 씬 생성, 노드 추가, 3D 씬을 MeshLibrary(GridMap용)로 내보내기 | Node 18+, 필요하면 `GODOT_PATH` | 5.8k★, 2026-07 | MIT | 읽고 확장하기 쉬운 시작점. `claude mcp add godot -- npx @coding-solo/godot-mcp` |
| [hi-godot/godot-ai](https://github.com/hi-godot/godot-ai) | 도구 46개·연산 120개 이상: `material_manage`(visual shader 포함), `camera_manage`, `resource_manage`(environment, noise texture), `gridmap_manage`, `csg_manage`. `editor_screenshot`이 viewport/viewport_2d/**cinematic(Camera3D 렌더)**/game 모드 지원. Vision Routing(이미지를 텍스트 설명으로 변환). GDScript 파싱 검증·핫리로드 | Godot 4.7+ | 2.6k★, 4.2.3(2026-09-24) | MIT | **최종 카메라로 룩 검증.** C#은 텍스트 전용이라 컴파일 오류를 보고하지 못함. "CoplayDev 팀 제작·Aura 후원"이라는 설명은 확인되지 않음 |
| [youichi-uda/godot-mcp-pro](https://github.com/youichi-uda/godot-mcp-pro) (Godot MCP Pro) | 3D Scene, 에디터·게임 스크린샷 비교 등(도구 수가 README 제목 162, 상세 목록 187, 외부 목록 84로 제각각). WebSocket 6505 | — | — | 독점($15 일회성, 평생 업데이트. 공개 저장소에는 무료 애드온만) | 유료라도 기능이 많은 쪽 |
| [beckettlab/beckett-godot-mcp](https://github.com/beckettlab/beckett-godot-mcp) | Node·Python 사이드카 없이 GDScript 애드온이 Streamable HTTP로 직접 서빙 | Godot 4 | — | — | 설치가 가장 가벼움 |
| [buildepicshit/Wick](https://github.com/buildepicshit/Wick) | 네이티브 C# MCP, 도구 53개, Roslyn·MSBuild | — | — | — | C# 프로젝트(godot-ai의 C# 약점 보완) |
| [Erodenn/godot-mcp-runtime](https://github.com/Erodenn/godot-mcp-runtime) 외 | 런타임 제어(UDP 브리지, 입력 시뮬레이션, 스크린샷). better-godot-mcp(composite 도구 18개), godot-forge(테스트·LSP·스크린샷)도 있음 | — | — | — | 런타임 테스트 |

Godot 렌더러로 UE Lumen/Nanite급 포토리얼 룩을 내기는 상대적으로 어렵습니다. 스타일라이즈드나 인디 규모에 맞춰 기대치를 잡으세요.

### 4.4 Roblox

- **Studio 내장 MCP 서버가 공식 권장 경로**입니다. 기존 오픈소스 [Roblox/studio-rust-mcp-server](https://github.com/Roblox/studio-rust-mcp-server)(도구 6종: `run_code`, `insert_model`, `get_console_output`, `start_stop_play` 등)는 2026-04-03 아카이브됐고, README가 내장 서버를 권합니다. 발표 글 제목은 ["Assistant Updates: Studio Built-in MCP Server and Playtest Automation"](https://devforum.roblox.com/t/assistant-updates-studio-built-in-mcp-server-and-playtest-automation/4474643)입니다.
- 설정: Studio 최신 버전 → Assistant Settings → MCP Servers → "Enable Studio as MCP server" → Quick connect로 클라이언트 선택(stdio). **2차 출처 기준이라 [공식 문서](https://create.roblox.com/docs/studio/mcp)로 재확인이 필요합니다(미확인).** 내장 서버의 전체 도구 목록도 확인하지 못했습니다.
- 커뮤니티: [boshyxd/robloxstudio-mcp](https://github.com/boshyxd/robloxstudio-mcp)는 2026-06-06 아카이브됐고, 원작자가 유지보수 포크 [Chrrxs/robloxstudio-mcp](https://github.com/Chrrxs/robloxstudio-mcp)(258★: 런타임 Luau 실행·브레이크포인트, 플레이테스트 제어, Creator Store 검색·미리보기, 스크린샷·입력 주입, 읽기 전용 inspector 에디션)로 옮기라고 권합니다. [weppy-roblox-mcp](https://github.com/hope1026/weppy-roblox-mcp)는 terrain·lighting·assets를 다루는 AGPL-3.0 서버(Basic/Pro 구분, 도구 수는 README에서 확인 안 됨)입니다.
- Roblox는 렌더링 목표 자체가 AAA 포토리얼과 다릅니다.

### 4.5 NVIDIA Omniverse·OpenUSD·RTX Remix

| 서버 | 역할 | 주소·요구 | ★ | 라이선스 |
|---|---|---|---|---|
| [kit-usd-agents](https://github.com/NVIDIA-Omniverse/kit-usd-agents) ([Kit MCP README](https://github.com/NVIDIA-Omniverse/kit-usd-agents/blob/main/source/mcp/kit_mcp/README.md)) | USD Code·Kit·OmniUI·Isaac Sim의 **지식 제공만**(씬 편집 없음) | Kit MCP `:9902/mcp`, Docker, NVIDIA API 키 | 96★ | Apache-2.0 |
| RTX Remix Toolkit 내장 MCP ([learning-mcp.md](https://github.com/NVIDIAGameWorks/toolkit-remix/blob/main/docs/howto/learning-mcp.md)) | 실행하면 자동 기동. REST API를 MCP 도구로 변환, rtx-remix-modding 스킬 동봉. DX8/9 구형 게임의 에셋·조명 교체 리마스터 | Streamable HTTP `http://127.0.0.1:18014/mcp/`(사용 중이면 18019까지 순차 시도) | — | Apache-2.0 |
| [serionist/omniverse-mcp](https://github.com/serionist/omniverse-mcp) | Kit 앱 라이브 조작: USD prim, PBR 머티리얼, 세그멘테이션 스크린샷(도구 42개·14개 카테고리) | Isaac Sim 5.1+ | 0★ | MIT |
| [omni-mcp/isaac-sim-mcp](https://github.com/omni-mcp/isaac-sim-mcp) | Isaac Sim 제어 | Isaac Sim 4.2.0+ | 192★ | MIT |

OpenUSD는 DCC와 엔진 사이의 레이아웃 교환 허브로 쓸 수 있지만, 이 계열은 게임 레벨 제작보다 시뮬레이션·디지털 트윈 성격이 강합니다.

### 4.6 웹 3D (PlayCanvas·Babylon.js·three.js/R3F)

| 서버 | 구분 | 핵심 | 실행 | ★ | 주의 |
|---|---|---|---|---|---|
| [PlayCanvas Editor MCP](https://github.com/playcanvas/editor-mcp-server) | **공식** | Editor에 MCP 클라이언트 내장(확장 불필요). 엔티티·컴포넌트·스크립트·에셋(최대 512MiB)·머티리얼·템플릿·애니메이션 상태 그래프·씬 설정, 뷰포트 캡처, 런타임 스크린샷·로그, 입력 주입, 버전 관리, **Store 검색·임포트·라이선스 확인, Sketchfab 검색·임포트**. schema-safe 배치 편집, 일관된 `{data, meta}` 응답 | `npx -y @playcanvas/editor-mcp-server`(Node 22.18+) → Editor 하단 MCP 버튼에서 포트(기본 52000) 확인 → CONNECT | 137★, MIT | 한 번에 Editor 인스턴스 하나만 연결 |
| [Babylon.js MCP 서버들](https://github.com/BabylonJS/Babylon.js/tree/master/packages/tools) | **공식** | `packages/tools` 아래 [nme](https://github.com/BabylonJS/Babylon.js/tree/master/packages/tools/nme-mcp-server)(Node Material), [nge](https://github.com/BabylonJS/Babylon.js/tree/master/packages/tools/nge-mcp-server)(Node Geometry, 절차 지오메트리), npe(파티클), nrge(렌더 그래프), gui, flow-graph, smart-filters + mcp-server-core. 에디터 라이브 세션 브리지 | npm [@babylonjs/mcp-servers](https://registry.npmjs.org/@babylonjs/mcp-servers)(9.28.0, 2026-09-24). 배포 바이너리 이름은 `babylonjs-nme-mcp-server`, `babylonjs-nge-mcp-server` 등 | Apache-2.0 | 씬 레이아웃보다 그래프 저작 중심. 커뮤니티 [babylon-mcp](https://github.com/immersiveidea/babylon-mcp)는 문서 검색 전용 |
| [threejs-devtools-mcp](https://github.com/DmitriyGolub/threejs-devtools-mcp) | 커뮤니티 | 실행 중인 three.js/R3F 앱에 WebSocket 브리지를 주입, 도구 59개(오브젝트, 머티리얼, 셰이더, 텍스처, 애니메이션, 성능, 메모리, 코드 생성) | `npx threejs-devtools-mcp` → `localhost:9222` 브라우저 탭 | 109★, MIT | **탭을 닫으면 끊김.** 이름 없는 오브젝트는 "(unnamed)"로 보여 식별 불가 |
| [r3f-mcp](https://github.com/r3f-mcp/r3f-mcp) | 커뮤니티 | `<MCPProvider>`로 Canvas를 감싸 씬 그래프 조회, 트랜스폼·머티리얼 변경, **바운드·거리·프러스텀 공간 질의**, 스크린샷 | `npm install r3f-mcp` → `npx r3f-mcp-server --port 3333` | 1★, MIT | 초기 프로젝트 |
| [web3d-mcp-server](https://glama.ai/mcp/servers/dev261004/web3d-mcp-server) / [Three.js Resources MCP](https://threejsresources.com/mcp) | 커뮤니티 | Next.js용 R3F 컴포넌트 생성 / Three.js·WebGPU·TSL 가이드 검색 | — | — | 코드 생성 보조 |

Babylon NME 흐름: `create_material` → `add_block` → `connect_blocks` → `set_block_properties` → **`validate_material`** → `export_material_json` → Scene MCP `add_material`(지오메트리는 `add_node_geometry_mesh`). 검증 단계를 빼고 export하면 런타임에서 깨집니다. Needle Engine·Bevy용 MCP는 찾지 못했습니다.

### 4.7 O3DE와 기타 엔진

- [nickschuetz/o3de-mcp](https://github.com/nickschuetz/o3de-mcp): 도구 66개(에디터 자동화 40개: 엔티티·컴포넌트, 트랜스폼, 프리팹, 레벨, 뷰포트 카메라, 스크린샷, 지속형 Python 세션 / EBus 스키마 탐색 / **RenderDoc 프레임 캡처** / 프로젝트·Gem 생성, CMake 빌드, Asset Processor). 동반 o3de-ai-companion-gem이 씬 스냅샷·엔티티 트리·씬 검증 제공. Python 3.10+, 11★, Apache-2.0/MIT, 2026-09-09.
- CryEngine용 MCP는 찾지 못했습니다.

### 4.8 에셋 조달·부착 보조 MCP

| 서버 | 역할 | 비고 |
|---|---|---|
| [Tanshaydar/Quartermaster](https://github.com/Tanshaydar/Quartermaster) | Unity Asset Store·Fab·Quixel Megascans·Gumroad·Leartes Cosmos에서 **이미 보유한** 에셋을 로컬 DB로 인덱싱(FTS5 키워드 + ONNX 임베딩 + CLIP 이미지 검색). `search_owned_assets`, `validate_stack`(렌더 파이프라인 충돌 검사), `import_asset_to_project`, `get_stack_recommendations`. Megascans의 texel density·실측 치수 표시 | 2★, MIT, Windows 중심. "생성보다 검증된 스캔 에셋 먼저" 원칙을 자동화 |
| PlayCanvas MCP, CoplayDev `import_model` | Sketchfab·Store 검색·임포트 | 라이선스 확인은 [10 가이드](10_assets_pipeline_licensing.md) |
| [gripforgeai/mcp](https://github.com/gripforgeai/mcp) | 리그의 손 본을 찾아 소품을 손 크기에 맞게 스케일하고 주먹을 쥐게 한 뒤 엔진용 바인드를 돌려줌 | 소품 부착 정확도 |

Megascans/Fab 에셋을 MCP로 직접 검색·다운로드·임포트하는 공식 도구는 확인하지 못했습니다(ChiR24 로드맵에서도 미구현).

---

## 5. Blender에서 만들 것 vs 엔진에서 할 것

엔진 MCP의 메시 편집 도구는 빈약하거나 실험 단계이고, Blender MCP로는 Lumen·Nanite·엔진 조명 아래의 최종 룩을 볼 수 없습니다. 스케일과 머티리얼 문제는 **엔진 조명 아래에서 봐야** 판단할 수 있습니다. 그래서 형태와 씬을 나눕니다.

| 작업 | 어디서 | MCP·도구 | 이유 / 팁 |
|---|---|---|---|
| 히어로 에셋 모델링, 베벨, 하드서피스 | Blender(또는 Max·Maya), 치수가 중요하면 CAD 앞단 | Blender MCP, 헤드리스 Blender, Rhino/Fusion/build123d | 엔진 MCP에는 모델링 도구가 거의 없음 |
| 절차적 파사드·반복 키트 | Blender Geometry Nodes 또는 Houdini | Blender MCP, fxhoudinimcp | per-simmons는 헤드리스 Blender로 **폭 400cm, X 중심·하단 피벗** 파사드 키트를 만들어 UE로 넘김 |
| 트림시트·UV·LOD | Blender·DCC | Blender MCP | — |
| 베이크·PBR 텍스처 세트 | Substance Painter(또는 Blender) | SubstancePainterMCP | 엔진 프리셋으로 익스포트 |
| 익스포트 전 형태·스케일 검사 | Blender | 이 저장소 [`scene_audit.py`](../03_playbooks/scripts/README.md)(부유·관통·스케일 미적용·non-manifold·치수 범위), [`review_views.py`](../03_playbooks/scripts/README.md)(4방향 검토 렌더) | 엔진으로 넘긴 뒤 고치면 왕복 비용이 큼 |
| 임포트 검증 | 엔진 | UE `StaticMeshTools.import_file` → bounds 조회 | 단위 설정이 어긋나면 FBX가 100배로 들어옴(4m 타일이 400m) |
| 최종 머티리얼 인스턴스·톤 변주 | 엔진 | MaterialInstanceTools, monolith | 엔진 조명 아래에서 조정해야 정확 |
| 배치·산포·PCG·폴리지·지형 | 엔진 | 공식 PCGToolset, ChiR24 `build_environment`·`paint_foliage` | 대규모 월드는 엔진에서 조립 |
| 조명(Lumen)·노출·포스트·하늘·안개 | 엔진 | 공식 ObjectTools로 속성 설정, ChiR24 sky/fog/cloud | 6.2절 시작값 |
| 카메라·시네마틱 | 엔진 | Sequencer, MRQ(ChiR24) | — |
| 시각 QA | 둘 다 | Blender `review_views.py` / UE CaptureViewport 3앵글, GenOrca 라벨 캡처, Unity `screenshot-isolated`, Godot cinematic | — |
| 정지 이미지·영상이 최종 산출물 | **Blender(Cycles)에서 끝내는 편이 나음** | Blender MCP, 헤드리스 렌더 | 인터랙티브 레벨·대규모 월드면 엔진 |

**Blender → 엔진 넘길 때 체크**
- 멀티 머티리얼 메시는 익스포트 전에 슬롯별 `material_index`가 기대대로 남아 있는지 확인합니다. `me.materials.clear()`를 하면 인덱스가 조용히 0이 됩니다.
- 모듈 규격과 피벗을 먼저 정합니다. 예: 바닥 타일은 min Z=0·XY 중앙 피벗, 벽은 타일 경계, 천장은 벽 높이(per-simmons의 4m 그리드 SF 실내 계획. **조립은 하지 않은 계획 문서**라 검증된 교훈은 아님).
- 키트마다 폭 축이 다를 수 있습니다. City Sample chair-kit은 폭이 Y축이라 그대로 조립하면 들쭉날쭉해졌습니다(검증된 실패 사례).
- 가구 치수는 [실측 치수표](../03_playbooks/05_reference_dimensions.md)(한국·미국·유럽)를 기준으로 합니다.

---

## 6. 엔진·DCC MCP 운영 수칙

### 6.1 열두 가지 수칙

1. **직렬로 호출하세요.** 에디터는 게임 스레드(또는 메인 스레드)가 하나입니다. UE 공식 MCP도 요청을 게임 스레드로 넘겨 순서대로 실행하고, `ExecuteGraphInstance`를 동시에 부르면 에디터가 멈춥니다. PCG는 그래프 하나·볼륨 하나 단위로 순차 실행합니다. 에셋 준비(헤드리스 Blender 등)는 병렬, 에디터 변경은 직렬("One editor, one game thread → serialize every scene mutation"). DCC도 같습니다: Substance Designer MCP는 병렬 호출 시 멈추고, Houdini·Maya·Painter 브리지는 메인 스레드 디스패처를 씁니다.
2. **쓰기 후 반드시 다시 읽으세요.** UE는 에러 없이 실패하는 경우가 많습니다.
   - 속성 이름은 PascalCase: `auto_possess_ai`는 아무 일도 안 하고 `AutoPossessAI`가 맞습니다.
   - `Mobility`·`RelativeLocation`은 Actor가 아니라 **RootComponent**에 있습니다. Actor에 쓰면 성공으로 보이지만 아무 데도 기록되지 않습니다.
   - BP 클래스 경로에는 `_C`(`/Game/Path/BP_Foo.BP_Foo_C`), 에셋 경로에는 `.AssetName`(`/Game/.../Tower_01.Tower_01`)을 붙입니다.
   - 값 비교는 ImportText/ExportText로 정규화한 뒤 합니다(`(X=1,Y=2)`와 `(X=1.000000,Y=2.000000)`는 같은 값).
3. **3앵글 스크린샷으로 확인하세요.** MCP 응답이 success여도 화면은 틀린 경우가 많습니다. 스케일·겹침·노출·빈 스폰은 이미지로만 잡힙니다. 매 빌드 단계마다 항공(전체), 눈높이, 파사드 근접 또는 플레이어 시점을 캡처하고 "행동 → 캡처 → 판독 → 추론" 루프를 돕니다. 도구: UE `EditorAppToolset.CaptureViewport`, GenOrca 라벨 캡처, Unity `screenshot-isolated`, Godot `editor_screenshot(mode=cinematic)`, Blender는 `review_views.py`.
4. **수치 검사를 이미지보다 먼저 하세요.** bounds·접촉·간섭 검사(3dsmax-mcp contact check, RhinoMCP `measure_objects`, faust Fusion 간섭 검사, r3f-mcp 공간 질의, Blender `scene_audit.py`)로 부유·관통을 먼저 걸러 내면 이미지 비평 횟수가 줄어듭니다.
5. **위에 얹는 오브젝트는 bounds로 좌표를 계산해 별도 액터로 두세요.** 지붕·캡을 PCG grammar 안에서 풀려고 중간 편집하면 스폰이 조용히 0개가 될 수 있습니다. 건물마다 `get_actor_bounds().max.z` 위치에 지붕 액터를 스폰하면 결정적이고 검증하기 쉽습니다.
6. **undo와 저장을 믿지 마세요.** `Modify()` 없이 한 변경은 Undo 기록에 남지 않습니다(변경 전에 `RootComponent->Modify()`). PIE·MRQ 전에는 반드시 저장합니다(Niagara·MetaSound PIE 크래시는 마지막 디스크 저장 상태로 돌아감). 에셋을 지우기 전에 `get_asset_references`로 참조를 확인합니다(참조 중인 메시 삭제는 assertion 크래시). **Git이나 Perforce에 커밋한 뒤 에이전트 세션을 시작하세요.**
7. **UE Python의 `print()`는 MCP 클라이언트로 돌아오지 않습니다.** 결과를 임시 Note 액터의 tags에 써서 읽고 지우세요.

   ```python
   note = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.Note, unreal.Vector(0, 0, 9999))
   note.tags = [result[:200]]   # 속성 조회로 읽은 뒤 액터 삭제
   ```
8. **조명·렌더 설정에는 화이트리스트를 주세요.** 허용: DirectionalLight Intensity/LightColor/Temperature/Rotation/LightSourceAngle, SkyLight Intensity/SourceType, SkyAtmosphere Rayleigh·Mie, PPV ExposureMethod/Compensation/MinEV100·MaxEV100/bloom/vignette/color grading. 금지: 레이트레이싱 속성, 라이트 Mobility 변경, 기존 SkyLight의 `bRealTimeCapture` 토글, CesiumSunSky 추가. Lumen은 소프트웨어 방식만([lighting-safety-review.md](https://github.com/per-simmons/unreal-agent-harness/blob/master/docs/lighting-safety-review.md)).
9. **생성보다 조립.** City Sample, Megascans, Fab, Poly Haven, KitBash3D, Quaternius CC0처럼 검증된 에셋을 먼저 쓰고, 생성 텍스처는 마지막 수단으로 둡니다. 보유 에셋 검색은 Quartermaster, Sketchfab·Store는 PlayCanvas MCP나 CoplayDev `import_model`.
10. **도구 수를 줄이세요.** 150~300개짜리 서버(fxhoudinimcp 206, dcc-mcp-houdini 295, 3dsmax-mcp 160)는 도구 스키마가 컨텍스트를 크게 먹고 선택 오류를 부릅니다. lean 프로필(tanishqbhattad/rhino-mcp), gateway 래퍼(dcc-mcp), tool search(UE 공식, ChiR24 `unreal` 게이트웨이)를 쓰고, 한 세션에 필요한 서버만 켭니다.
11. **API는 추측하지 말고 조회하게 하세요.** DCC API(hou, pymxs, maya.cmds, FeatureScript)는 버전마다 달라 LLM이 없는 함수를 지어냅니다. 문서 검색 도구(fxhoudinimcp 매뉴얼 검색, frankhommers Fusion `fetch_api_documentation`, abrahamADSK Maya RAG, NVIDIA USD Code MCP, UE `describe_toolset`)를 먼저 쓰게 하세요.
12. **UI 언어는 영어로 두세요.** [한국 사용자] Blender에서는 한국어 UI의 새 데이터 이름 번역 때문에 `nodes['Principled BSDF']` 같은 코드가 깨지는 문제가 확인됐습니다([02 가이드 12절](02_blender_mcp.md)). 다른 DCC에서 같은 문제가 있는지는 조사하지 못했지만, 에이전트가 이름으로 노드·속성을 찾는 구조는 같으므로 영어 UI와 타입 기반 탐색이 안전합니다(일반 권장).

### 6.2 UE 조명·재질 시작값 (per-simmons 기록, 개인 사례)

아래 값은 per-simmons 하네스 문서에서 가져온 시작점입니다(**개인 사례, n=1**). 절대값이 아니라 AI가 엉뚱한 값을 넣지 않게 하는 출발선으로 쓰세요. 조명 원리는 [06 가이드](06_lighting_rendering_art_direction.md)를 보세요.

**골든아워 외부 조명**([golden-hour-lighting-plan.md](https://github.com/per-simmons/unreal-agent-harness/blob/master/docs/golden-hour-lighting-plan.md))

| 대상 | 값 |
|---|---|
| DirectionalLight | pitch -8°(-6~-12), yaw -55°, 4000K(3700~4300), Intensity 8(**legacy 단위**), shadow distance 50000cm, dynamic cascades 4 |
| SkyLight | 1.0(최대 1.5), real-time capture, Movable |
| PostProcessVolume | Unbound, priority 1000000, AEM_Manual, exposure bias 11 EV(9~13) |
| SkyAtmosphere | Mie 약 0.004, aerial perspective 1.5 |
| 호출 순서 | `ActorTools.set_actor_transform` → `ObjectTools.set_properties` → `SceneTools.add_to_scene_from_class`(PPV) → CaptureViewport |

legacy 단위를 쓰는 라이트에 물리 lux 값(50000 이상)을 넣으면 화면이 하얗게 클리핑됩니다.

**재질·사실감**([REALISM-GUIDE.md](https://github.com/per-simmons/unreal-agent-harness/blob/master/docs/REALISM-GUIDE.md))
- 노멀맵 강도는 **약 0.3**. 8이나 1.5는 사포처럼 보였습니다.
- 400cm 모듈에 UTiling/VTiling 약 2~3, 오브젝트별 톤 변주 5종 정도, 모든 하드 엣지에 베벨.
- 그을음: `BaseColor *= lerp(1.0, 0.40, soot.A * 0.5)`.
- 금속 장식은 `Metallic 1.0`만 주면 어둡게 보여서 밝은 tint(>1.0)와 emissive 약 0.15~0.2를 줬습니다. 가장 사실적으로 나온 것은 깊은 베벨 릴리프와 청동 장식(두 번째 머티리얼 슬롯)으로 돌·금속 대비를 준 아르데코 블록이었습니다.
- 데칼은 AI가 생성한 균열·그을음 이미지 대신 Megascans 같은 스캔 데칼을 은은하게 씁니다(생성 크랙 네트워크는 가짜처럼 보였음). DecalActor는 로컬 +X로 투영하므로 -Y를 바라보는 벽이면 yaw 90°, +Y면 -90°, 벽 앞 약 100cm에 decalSize.x 400 이상. PNG는 CompressionSettings를 `TC_EditorIcon`에서 `TC_Default`로 바꾸고 `MD_DeferredDecal`·`BLEND_Translucent`를 씁니다.

**정정된 커뮤니티 주장**(07 검증 결과)
- "Lumen GI는 Movable 라이트만 반영한다"는 **틀렸습니다.** Epic 문서는 Static 라이트만 지원하지 않는다고 적고, Stationary도 Lumen GI에 반영됩니다. 에이전트가 만든 라이트를 Movable로 두는 것 자체는 무해한 관행입니다(Nanite와 Stationary 라이트를 함께 쓰면 VSM 문서가 Movable을 권함).
- "emissive가 1.0을 넘어야 블룸이 생긴다"는 엔진 규칙이 아니라 경험칙입니다. 블룸은 PPV의 Threshold로 제어되고(-1이면 모든 색이 기여), 노출 설정에 따라 달라집니다. 작은 발광체는 "Emissive Light Source"를 켜야 Lumen Scene에서 컬링되지 않습니다.
- Niagara 스프라이트는 노멀이 불안정해 lit translucent보다 Unlit+emissive가 안전하다는 것이 ibrews의 실무 권장입니다.

### 6.3 PCG를 MCP로 다룰 때의 함정

([PCG-GUIDE.md](https://github.com/per-simmons/unreal-agent-harness/blob/master/docs/PCG-GUIDE.md))
- 스포너의 메시 팔레트는 파라미터가 아니라 **노드 설정**에 있습니다: `settingsInterface → meshSelectorParameters.DefaultSelectorInstance.meshEntries`. 배열은 **한 번에 1개씩 append**합니다.
- `overrideMaterials`를 바꾼 뒤에는 PCGVolume을 지우고 `SpawnGraphInstance`를 다시 해야 반영됩니다.
- 볼륨 컬링은 실행 순서에 따라 포인트 0개를 반환할 수 있습니다.
- 문서 앞부분의 파라미터(gridExtents 20000, cellSize 4000, KMeans 5, scale 18/18/8~26/26/40)는 초기 "cube-extrusion" 프록시 단계의 값입니다. 최종 49개 글래스 타워는 grammar 그래프·actor-grid·tier 방식이고 이후 데모는 gridExtents 29000/31000을 썼습니다. **두 단계의 값을 섞어 쓰지 마세요.**

---

## 7. 보안·포트 한눈에

대부분의 DCC·엔진 MCP는 DCC 안에서 Python/MEL/MAXScript/Ruby/Luau를 실행합니다. 프롬프트 인젝션이나 실수 하나로 씬·파일이 손상될 수 있으니 **임의 코드 실행은 기본으로 끄고, 루프백에만 바인딩하고, 원격 바인딩은 명시적으로 허용할 때만 여세요.**

| 서버 | 기본 포트·주소 | 인증·게이트 | 주의 |
|---|---|---|---|
| Blender MCP(공식·ahujasid) | TCP 9876 | — | [02 가이드](02_blender_mcp.md) |
| capoomgit Houdini | TCP 9876 | — | **Blender MCP와 충돌** |
| faust-machines Fusion | TCP 9876 | — | **Blender MCP와 충돌** |
| oculairmedia Houdini | hrpyc/RPyC 18811 | 없음 | 무인증 원격 Python. 네트워크 노출 금지 |
| RhinoMCP | TCP 루프백 | 없음 | 로컬 전용으로만 |
| dcc-mcp gateway | `127.0.0.1:9765/mcp` | — | dcc-mcp-maya sidecar는 **LAN `:59765`** 에도 노출 → `DCC_MCP_GATEWAY_REMOTE_PORT=0` |
| Substance Painter | HTTP `localhost:60041`(Painter 원격 스크립팅) | `SP_MCP_ALLOW_EXECUTE_PYTHON=1`일 때만 임의 Python | 임포트는 승인된 루트로 샌드박싱 |
| Substance Designer | TCP 9881 | — | `execute_sd_code`(임의 Python) 존재 |
| Marvelous Designer | TCP `127.0.0.1:7421` | — | 같은 머신 전용 |
| GG_MayaMCP | Maya commandPort | `MAYA_MCP_ENABLE_RAW_EXECUTION=true`일 때만 raw 실행 | localhost 전용 |
| kumoproductions C4D | — | `C4D_MCP_ENABLE_EXEC_PYTHON`, `C4D_MCP_TOKEN` | `C4D_MCP_ALLOW_REMOTE=1` 켜지 말 것 |
| fxhoudinimcp | — | `FXHOUDINIMCP_PROJECT_ROOT` 경로 샌드박스 | — |
| KeyShot MCP | — | — | 장면 메타데이터·미리보기가 모델 제공자에게 전송될 수 있음 |
| SketchUp·Adobe 커넥터 | 원격(클라우드) | 계정 로그인 | 데이터가 벤더 클라우드로 감 |
| UE 5.8 공식 | `127.0.0.1:8000/mcp`(→ 8123 권장) | origin 검증만 | "Localhost is not a trust boundary". `execute_tool_script`는 특권 연산. `bRemoteExecution=False` |
| ChiR24 Unreal | 네이티브 HTTP 3000, 브리지 WS 8091 | capability token 기본, loopback 전용 | — |
| chongdashu Unreal | TCP 55557 | — | — |
| runreal Unreal | UE Python Remote Execution | — | 에디터 전체 권한을 넘김 |
| UnrealEngine_Bridge | `:30011` | — | 공식 MCP와 병행 |
| RTX Remix | `127.0.0.1:18014/mcp/`(~18019) | — | — |
| NVIDIA Kit MCP | `:9902/mcp` | NVIDIA API 키 | — |
| PlayCanvas | WebSocket 52000 | — | Editor 하나만 |
| Godot MCP Pro | WebSocket 6505 | — | — |
| threejs-devtools-mcp | `localhost:9222` | — | 탭 유지 |
| r3f-mcp | `--port 3333` | — | — |

---

## 8. 프롬프트 예시

**가구를 치수로 지시 (McNeel 공식 레시피, [recipes.md](https://raw.githubusercontent.com/mcneel/RhinoAI/rhino-9.x/docs/content/docs/try-it-out/recipes.md))**

```text
Design a parametric coffee table. Top is 1200×600×30mm walnut.
Four tapered legs, 400mm tall, splayed outward 5°.
```

같은 요청을 부재별로 더 구체화하면(Onshape 실험의 교훈):

```text
상판 1200×600×30mm 월넛. 다리 4개, 길이 400mm, 바깥으로 5° 벌어짐,
다리 단면은 상단 45mm → 하단 30mm 테이퍼. 에이프런 높이 80mm·두께 20mm.
완성 후 전체 바운딩박스와 부재별 치수를 표로 보고하고, naked edge 수를 확인해.
```

**스케치를 줄 때: 해석 먼저 ([sketch-to-model.md](https://raw.githubusercontent.com/mcneel/RhinoAI/rhino-9.x/docs/content/docs/advanced/sketch-to-model.md))**

```text
Here's a sketch of a shelving unit I want to build. Read the proportions and structure
off the drawing, tell me what you think the key parameters are, and propose a parametric
model. Don't build anything yet. Show me your interpretation first so I can correct it.
```
원근이 헷갈리면 "this is the front elevation", 너무 문자 그대로 모델링하면 "treat sketch as intent"를 덧붙입니다. 모델이 추정한 비율은 "거의 맞지만 정확하지 않은" 경우가 많고, 재료 두께·조인트·공차는 모델이 지어냅니다. 비교는 `get_viewport_image`로 스케치 각도에 맞춰 합니다.

**수작업 모델을 파라메트릭으로 역설계 ([make-this-parametric.md](https://raw.githubusercontent.com/mcneel/RhinoAI/rhino-9.x/docs/content/docs/advanced/make-this-parametric.md))**

```text
I've modeled this stair by hand. Look at the geometry on layer `Stair`, work out the
construction recipe, and rebuild it as a GH2 definition driven by sliders for tread depth,
riser height, total rise, and number of treads.
```
확인할 것: 요청한 슬라이더 수가 맞는지, 기존 Rhino 오브젝트를 bake하지 않고 원시 도형에서 생성하는지, 극단값에서 토폴로지가 깨지지 않는지.

**산포(겹침 금지)**: McNeel 레시피에는 5×5m 영역에 구 200개를 겹치지 않게 무작위 산포하는 예가 있습니다. 가구 소품 산포도 "영역, 개수, 최소 간격, 겹침 금지, 완료 후 겹침 쌍 수 보고"를 같이 지시하세요.

**코드 CAD의 측정 루프 ([build123d-mcp](https://github.com/pzfreo/build123d-mcp))**

```text
Make a 60 mm x 40 mm x 6 mm mounting plate with two 5 mm through holes 40 mm apart.
Render it, measure it, then export STEP and STL.
```

**배치 검증 (3ds Max 접촉 검사)**

```text
의자 4개를 테이블 주변에 배치한 뒤, 각 의자와 바닥 사이 gap이 0~1mm인지,
테이블과 관통이 없는지 contact check로 보고해. 문제가 있으면 고치고 다시 검사해.
```

**Houdini (fxhoudinimcp README 예시)**

```text
Create a procedural rock generator with mountain displacement
Build a USD scene with a camera, dome light, and ground plane
Create an HDA from the selected subnet
Debug why my scene has cooking errors
```

**Substance Designer (레시피에서 시작해 파라미터만 조정)**

```text
Build a weathered steel material with surface oxidation
Create a cliff heightmap with high detail and disorder
```
→ 결과 그래프에서 스케일·거칠기 파라미터만 조정해 달라고 후속 지시합니다. 병렬 도구 호출은 끕니다.

**API 환각 방지 (공통)**

```text
코드를 쓰기 전에 문서 검색 도구로 해당 노드·파라미터 이름을 확인하고,
실제로 존재하는 파라미터만 사용해. 쓰고 난 뒤에는 값을 다시 읽어서 보고해.
```

**엔진 조립 (UE 공식 MCP)**

```text
작업 규칙: 에디터 변경 호출은 하나씩 순서대로 보낸다. 모든 쓰기 뒤에는 같은 속성을 다시 읽어
값이 바뀌었는지 확인한다(속성 이름은 PascalCase, Mobility·위치는 RootComponent).
각 단계가 끝나면 항공·눈높이·플레이어 시점 3앵글로 CaptureViewport를 찍어 스케일, 겹침,
노출, 빈 스폰을 점검한다. 조명은 허용 목록의 속성만 바꾼다.
```

더 많은 템플릿은 [프롬프트 템플릿 모음](../03_playbooks/03_prompt_templates.md)에 있습니다.

---

## 흔한 실수와 해결

| 증상 | 원인 | 해결 |
|---|---|---|
| UE MCP에 연결은 되는데 도구가 없음 | AllToolsets 플러그인 꺼짐 | AllToolsets 활성화(없으면 서버가 도구를 하나도 노출하지 않음) |
| `StartServer`가 실패하거나 엉뚱한 서버에 붙음 | 기본 8000 포트 충돌 | `ModelContextProtocol.StartServer 8123`, ini 자동 시작 설정 |
| 새로 만든 커스텀 도구가 안 보임 | Live Coding으로는 반영 안 됨 | 에디터 완전 재시작 |
| 프로젝트를 바꾸자 MCP가 끊김 | 이전 서버가 종료됨 | 다시 StartServer. Epic 플러그인의 세션 유지 프록시 사용 |
| "success"인데 화면이 그대로 | snake_case 속성, Actor에 Mobility·위치를 씀, `_C` 누락 | PascalCase, RootComponent, 경로 접미사 확인 후 **재조회** |
| PCG 실행 중 에디터가 멈춤 | 여러 그래프를 동시에 실행 | 그래프·볼륨 하나씩 직렬 실행 |
| PCG 스폰이 0개 | 볼륨 컬링 순서, grammar 중간 편집 | 실행 순서 점검, 지붕·캡은 bounds 기반 별도 액터 |
| 머티리얼을 바꿨는데 PCG 결과에 반영 안 됨 | `overrideMaterials` 변경 후 재생성 안 함 | PCGVolume 삭제 후 `SpawnGraphInstance` |
| Python 결과가 에이전트에게 안 옴 | UE `print()`는 로그로만 감 | Note 액터 tags로 우회(6.1절 7번) |
| Ctrl+Z로 AI 변경이 안 돌아감 | `Modify()` 없이 변경 | 변경 전 `Modify()`, 단계마다 저장, 커밋 후 세션 시작 |
| 임포트한 메시가 100배 크기 | Blender·익스포터 단위 불일치 | 익스포트 단위 확인, 임포트 직후 bounds 조회 |
| 조립한 키트가 들쭉날쭉 | 키트마다 폭 축이 다름(City Sample chair-kit은 Y) | 임포트 후 축·피벗 표준화 |
| 화면이 하얗게 날아감 | legacy 단위 라이트에 lux 값(50000+) | 단위 확인, 6.2절 시작값 |
| 벽이 사포처럼 보임 | 노멀 강도 과다(1.5~8) | 약 0.3에서 시작 |
| 데칼이 안 보이거나 반대로 붙음 | +X 투영 방향, 텍스처 압축 설정 | yaw 조정, `TC_Default`, `MD_DeferredDecal` |
| Substance Designer가 멈춤 | 병렬 호출, `SDUsage.sNew()`, 알 수 없는 노드 정의 | 한 번에 하나씩 호출, 레시피 사용 |
| SD에서 노드 연결이 전부 사라짐 | `arrange_nodes()` 호출 | 쓰지 않기 |
| Marvelous Designer GUI가 멈춤 | 리스너 대기 상태(정상) | 작업 후 리스너 종료 |
| C4D 렌더 실패 | 큰 해상도에서 메모리 부족 | 미리보기 해상도로 확인, 최종은 배치 렌더 |
| Blender MCP와 Houdini/Fusion MCP를 같이 켰더니 이상 동작 | 모두 9876 포트 | 한 번에 하나만 켜거나 포트 변경 |
| 스튜디오 네트워크에서 Maya가 원격 조작될 위험 | dcc-mcp-maya sidecar LAN gateway | `DCC_MCP_GATEWAY_REMOTE_PORT=0` |
| Onshape 인증 실패 | 서버마다 환경변수 이름이 다름 | 3.7절 표대로 설정 |
| 에이전트가 엉뚱한 도구를 고름 | 도구 150~300개 노출 | lean 프로필, gateway, tool search, 필요한 서버만 켜기 |
| 없는 함수를 지어냄 | 버전별 API 차이 | 문서 검색 도구로 먼저 조회 |
| 도면을 주면 형태가 틀림 | 비전 분해가 병목(치수 텍스트·극성 오독) | 치수를 텍스트 사양으로, "해석 먼저" |
| three.js 대상 오브젝트를 못 찾음 | 이름 없음 → "(unnamed)" | 모든 오브젝트에 이름 |
| PlayCanvas 두 번째 에디터가 안 붙음 | 한 번에 하나만 지원 | 인스턴스 하나만 연결 |
| IvanMurzak Unity-MCP 설치 실패 | 프로젝트 경로에 공백 | 공백 없는 경로 |
| chongdashu 서버가 UE 5.6에서 연결 안 됨 | 호환 이슈(#31, #43) | ChiR24 또는 공식 MCP |
| Spline MCP가 동작 안 함 | Spline에 공개 API 없음(아카이브) | 임베드 코드만 LLM으로 작성 |
| [한국] AI Forge·로컬 Hunyuan3D 경로 사용 | Hunyuan3D 라이선스가 한국 제외 | 다른 생성기 사용, [10 가이드](10_assets_pipeline_licensing.md) 참고 |

---

## 관련 문서

- [목적·범위](../00_purpose/purpose_and_scope.md) · [조사 방법·신뢰도 정책](../01_research/research_method.md) · [출처 카탈로그](../01_research/sources_catalog.md) · [검증 로그](../01_research/verification_log.md)
- [AI 모델 비교·MCP 클라이언트·비용](01_ai_models_and_clients.md): Codex(GPT-6 Astra) effort 지정, 모델별 단가
- [Blender MCP 생태계](02_blender_mcp.md): 공식 Blender Lab 서버 vs ahujasid, 포트 9876, 한국어 UI 문제
- [AI 3D 생성](04_ai_3d_generation.md) · [텍스처링·재질](05_texturing_materials.md) · [라이팅·렌더·아트디렉션](06_lighting_rendering_art_direction.md)
- [오브젝트·가구·조형 모델링](07_modeling_objects_furniture_sculpture.md) · [배치·레이아웃](08_scene_layout_placement.md)
- [에이전트 워크플로·프롬프팅](09_agent_workflow_prompting.md): 시각 피드백 루프, 스킬, 토큰 비용
- [에셋·파이프라인·라이선스](10_assets_pipeline_licensing.md): Hunyuan3D 지역 제외, 에셋 라이선스
- [학술 연구](11_research_papers.md)
- [빠른 시작](../03_playbooks/01_quickstart_setup.md) · [AAA 제작 플레이북](../03_playbooks/02_aaa_production_playbook.md) · [프롬프트 템플릿](../03_playbooks/03_prompt_templates.md) · [품질 체크리스트](../03_playbooks/04_quality_checklists.md) · [실측 치수표](../03_playbooks/05_reference_dimensions.md)
- [보조 스크립트 사용법](../03_playbooks/scripts/README.md): `scene_audit.py`, `placement_utils.py`, `review_views.py`(Blender 4.2.23 LTS·5.0.1·5.2.2 LTS 테스트 통과)
- [CLAUDE.md 템플릿](../03_playbooks/templates/CLAUDE.md) · [Blender 스킬 템플릿](../03_playbooks/templates/skills/blender-aaa-scene/SKILL.md)
- [사례 모음](../04_case_studies/01_case_studies.md) · [한국어 자료](../04_case_studies/02_korean_resources.md)

## 원자료

- [`01_research/raw/03_dcc-cad-mcp.research.json`](../01_research/raw/03_dcc-cad-mcp.research.json): 기타 DCC·CAD·텍스처 앱 MCP 조사(항목 42, 노하우 13, 사례 9)
- [`01_research/raw/03_dcc-cad-mcp.verify.json`](../01_research/raw/03_dcc-cad-mcp.verify.json): 독립 검증(판정 15, 항목 점검 22, 신뢰도 낮은 출처 5, 누락 항목 7)
- [`01_research/raw/04_engine-mcp.research.json`](../01_research/raw/04_engine-mcp.research.json): 게임 엔진·실시간 3D MCP 조사(항목 21, 노하우 18, 사례 7)
- [`01_research/raw/04_engine-mcp.verify.json`](../01_research/raw/04_engine-mcp.verify.json): 독립 검증(판정 15, 항목 점검 17, 신뢰도 낮은 출처 8, 누락 항목 10)
- 교차 참조: [`06_texturing-materials.verify.json`](../01_research/raw/06_texturing-materials.verify.json)(monolith, Comfy-Org/comfy-mcp, dcc-mcp 신뢰도 지적), [`07_aaa-rendering-lighting.verify.json`](../01_research/raw/07_aaa-rendering-lighting.verify.json)(Lumen Movable 주장 반박, Epic 플러그인 UE 버전 표기), [`10_agent-workflow.verify.json`](../01_research/raw/10_agent-workflow.verify.json)(Epic 플러그인 설치 명령·보안 경고), [`G4_licensing_pricing.verify.json`](../01_research/raw/G4_licensing_pricing.verify.json)(Adobe 커넥터 대상 앱), [`G5_aaa_practice.gap.json`](../01_research/raw/G5_aaa_practice.gap.json)(UE 5.8 출시일 보도)
