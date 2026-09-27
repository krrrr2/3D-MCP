# AAA 제작 플레이북: 장면 하나를 처음부터 끝까지

> 기준일: 2026-09-27 · 스펙 → 블록아웃 → 구도 → 조명 → 에셋 조달 → 모델링 → 배치 → 재질 → 조명 → 디테일 → 렌더 → 익스포트까지 12단계를, 단계마다 "누가, 무엇을 넣고, 무엇을 지시하고, 어떤 숫자를 넘어야 다음으로 가는지"로 정리한 실행 절차서

## 핵심 요약

- **기대치부터 맞추세요.** 독립적으로 검증된 'AAA급' AI+MCP 결과물은 찾지 못했습니다. 공개 점수가 있는 최고 사례인 Claude Fable 5.1 에이전트 스웜의 Union Square 디지털 트윈도 재질 6/10, 시각 충실도 6/10, 조명 7/10이었습니다(목표 8.5, [FINAL_QA_REPORT](https://raw.githubusercontent.com/PhiloLabs/fable51-worlds/main/union-square-sf/FINAL_QA_REPORT.md)). 고품질은 **[에셋·생성 모델 + 에이전트 조립 + 검증 루프 + 사람의 마무리]** 조합에서 나옵니다.
- **순서를 고정합니다.** 공개 스킬팩들은 같은 순서로 수렴합니다: 레퍼런스·스펙 → 실측 블록아웃 → 카메라 고정 → 무채색 조명 → 형태 → 재질(명도 먼저) → 조명 v2 → 디테일 → 렌더 → 합성 → 익스포트. 이유는 하나입니다. *"A perfect material tuned in flat lighting will look wrong once real lighting goes in."*([RobLe3 pro-workflow](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-pro-workflow/SKILL.md))
- **게이트 4개에서 사람이 멈춰 봅니다.** G1 스펙, G2 블록아웃·구도, G3 최종 렌더, G4 익스포트. 유료 생성 직전에도 비용 승인을 받습니다. 사람 판단은 초반에 넣을수록 쌉니다.
- **모든 단계 안에서 같은 루프를 돌립니다.** 작은 멱등 코드 → `.blend` 증분 저장 → **숫자 검사**([`scene_audit.py`](scripts/README.md)) → **렌더**([`review_views.py`](scripts/README.md)) → **다른 컨텍스트의 비평가** → 결함 하나만 수정. *"A passing technical validator does not mean an asset looks good."*([blender-art-factory](https://github.com/ErikBurdett/blender-art-factory)) 반대로 그림이 그럴듯해도 숫자가 틀리면 실패입니다.
- **좌표는 솔버와 스크립트가, LLM은 관계와 제약만.** 배치는 관계 제약 JSON → 솔버 → [`placement_utils.py`](scripts/README.md)로 붙이기 → 검사 → 4방향 렌더 채점 순서로 합니다([SceneSmith](https://github.com/nepfaff/scenesmith), [SAGE](https://raw.githubusercontent.com/NVlabs/sage/main/server/objects/object_placement_planner.py)).
- **처음부터 만들지 말고 먼저 고르세요.** 배경·반복 요소는 CC0 라이브러리와 모듈러 키트, 히어로 하드서페이스·가구는 스펙 기반 파라메트릭 코드, 유기체·조각은 이미지→3D 생성 후 리토폴로지. 재질도 "생성보다 선택"입니다.
- **모델 역할 분담(제안):** 계획은 Fable 5.1 또는 Opus 5.5, 빌드는 GPT-6 Astra(Codex, effort 명시) 또는 Opus 5.5, 비평은 빌더와 분리한 읽기 전용 에이전트, 대량 반복은 Sonnet 5. 모델 비교는 대부분 개인 테스트(n=1)라서 **절대 순위가 아니라 작업 유형별 선택**입니다.
- **[한국 사용자]** Tencent Hunyuan 계열 오픈웨이트(3D 2.0/2.1/Omni/Part, HY-World, HY-Motion)는 라이선스 적용 지역에서 대한민국이 빠져 있고 출력물 사용도 제한됩니다. 한국어 UI에서는 노드 이름이 번역될 수 있으니 코드에서 노드를 **type**으로 찾게 하세요. 치수는 [한국 프리셋](05_reference_dimensions.md)을 쓰세요.

---

## 0. 이 플레이북을 쓰는 법

### 0.1 예시 장면 3종

각 단계에 장면 유형별 차이를 따로 적었습니다.

| 기호 | 장면 | 예시 스펙 | 주요 산출물 |
|---|---|---|---|
| **A** | 인테리어 방 | 한국 아파트 거실 4.2 × 3.6 m, 천장 2.3 m, 저녁 실용광 | 스틸 렌더 2~3컷 + 편집 가능한 `.blend` |
| **B** | 제품·소품 히어로 | 미드센추리 원목 라운지 체어, 게임용 삼각형 ≤ 8k, 2K PBR | 히어로 렌더 + GLB |
| **C** | 야외 환경 | 숲길 한 구간(골든아워), 나무·바위·풀 산포 | 스틸 렌더 + 엔진용 인스턴스 배치 |

### 0.2 전체 흐름과 게이트

```text
[0 목표·레퍼런스·스펙] ─G1─▶ [1 스케일 블록아웃] ─▶ [2 카메라·구도 고정] ─G2─▶ [3 라이트 v1]
      ─▶ [4 에셋 조달 결정] ─(유료 생성 비용 승인)─▶ [5 히어로 모델링] ─▶ [6 배치]
      ─▶ [7 재질·텍스처] ─▶ [8 라이트 v2] ─▶ [9 디테일·스토리·마모]
      ─▶ [10 최종 렌더·합성] ─G3─▶ [11 익스포트·검증·provenance] ─G4─▶ 완료

모든 단계 안: 작은 코드 → 증분 저장 → 숫자 검사 → 검토 렌더 → 비평 → 결함 1개 수정 (3장)
```

| # | 단계 | 핵심 산출물 | 통과 게이트 요지 | 주 도구 |
|---|---|---|---|---|
| 0 | 목표·레퍼런스·스펙시트 | `spec_sheet.json`, `acceptance.yaml`, 레퍼런스 보드 | **G1** 사람이 스펙 승인 | 계획 모델, 이미지 모델 |
| 1 | 스케일 블록아웃 | 실측 프리미티브 씬 `v001.blend` | 전체 치수 ±3%, 떠 있음·관통 0 | 빌더, `scene_audit.py` |
| 2 | 카메라·구도 고정 | `CAM_Hero`(잠금), 후보 비교 시트 | 썸네일 가독성, **G2** 사람 승인 | 빌더, 테스트 렌더 |
| 3 | 라이트 v1 | 색관리 설정 + 무채색 조명 | False Color 피사체 ≈ 0 EV, 클리핑 ≤ 0.5% | 빌더, 렌더 |
| 4 | 에셋 조달 결정 | `asset_manifest.csv` | 모든 에셋에 출처·라이선스·비용, 유료 생성 승인 | 계획 모델, 사람 |
| 5 | 히어로 모델링 | 부품 단위 히어로 에셋 | 실루엣 IoU ≥ 0.90, 부품 수 일치, 감사 0건 | 빌더, 비평가 |
| 6 | 배치 | `relations.json` + 배치된 씬 | 충돌 0, 부유 0, 동선 ≥ 0.9 m, 채점 통과 | 솔버, `placement_utils.py` |
| 7 | 재질·텍스처 | PBR 재질 세트 | PBR 규칙 위반 0, 명도 구분, 라이선스 기록 | 빌더, 라이브러리 MCP |
| 8 | 라이트 v2 | 색온도·비율을 준 조명 | 수치 게이트 + 비평 통과 | 빌더, 비평가 |
| 9 | 디테일·스토리텔링·마모 | 드레싱·웨더링 | 히어로 존 과밀 없음, 감사 재통과 | 빌더, 비평가 |
| 10 | 최종 렌더·합성 | EXR 마스터 + 최종 이미지 | 비평가 SHIP, **G3** 사람 승인 | headless 렌더 |
| 11 | 익스포트·검증·provenance | GLB/FBX, credits, provenance | 8항목 + 검증기 오류 0, **G4** 사람 SHIP | 검증기, 스크립트 |

### 0.3 품질 프로필: 검증을 얼마나 할까

작업 규모에 맞춰 고릅니다([claude-3d-harness](https://github.com/MAX-786/claude-3d-harness) 프로필).

| 프로필 | 체크포인트 | 수정 라운드 | 검토 렌더 | 쓰는 곳 |
|---|---|---|---|---|
| fast | 1회 | 1회 | 최대 1280×720, 64spp | 아이디어 확인, 배경 소품 |
| standard | 블록아웃·조명·재질 뒤 | 2회 | 1920×1080, 256spp | 일반 에셋 |
| cinematic | 모든 단계 | 4회 | 512spp | 히어로 에셋, 포트폴리오 샷 |

실제 사례에서도 수정은 보통 2라운드였고([Vizuara](https://github.com/VizuaraAI/fable-visual-learning-pipeline)), 사람이 10시간 동안 21번 수정을 지시한 경우도 있었습니다(SpenserFX 빈티지 체육관, 2차 요약, 미검증).

---

## 1. 시작 전 준비

### 1.1 모델 역할 분담 (제안)

아래 구성은 원자료의 사례와 도구 문서를 근거로 한 **제안**이며, 효과가 측정된 구성은 아닙니다. 먼저 한 모델로 effort만 바꿔 보고, 부족한 단계만 떼어 내세요. 모델을 섞으면 캐시를 공유하지 못해 비용이 늘어납니다.

| 역할 | 맡는 일 | 추천 (2026-09) | 근거 (신뢰도) |
|---|---|---|---|
| **감독 (사람)** | 스펙·구도 승인, 미감 판단, 최종 SHIP | — | 공개된 고품질 사례 대부분에서 사람이 결함 목록을 주고 2~21회 반복 수정했습니다 |
| **계획** | spec_sheet, 부품 분해, 에셋 목록, 관계 제약, 합격 기준 | Claude Fable 5.1 또는 Opus 5.5 (effort high) | "기획·코드는 Fable 5.1, Blender는 Astra"로 나눈 사례(개인 테스트, n=1, 2차 요약). Fable 5.1은 $10/$50라 계획에만 씁니다 |
| **빌더** | bpy 코드, MCP 조작, 배치 적용, 익스포트 | GPT-6 Astra (Codex, **effort를 high 이상으로 명시**) 또는 Claude Opus 5.5 | 같은 Blender 과제에서 Astra가 토큰을 덜 썼다는 보고와 Opus 5.5가 두께·기울기 비례에서 나았다는 보고가 엇갈립니다(모두 n=1, [2차 요약](https://github.com/yangqiong/gpt6-astra-3d), 미검증) |
| **비평가** | 렌더 판정, 결함 목록, 수정안 | 빌더와 **다른 컨텍스트**의 읽기 전용 에이전트. Opus 5.5 권장 | Anthropic은 Opus 5.5를 "vision과 computer use에 가장 좋은 Opus"로 소개합니다([Opus](https://www.anthropic.com/claude/opus), 벤더 자체 보고). 새 컨텍스트의 리뷰어는 결과물을 만든 추론을 보지 않고 평가합니다([subagents](https://code.claude.com/docs/en/sub-agents)) |
| **대량 반복** | 소품 수백 개 재질 파라미터, 네이밍, 렌더 설정 | Claude Sonnet 5 ($2/$10) | 단가([pricing](https://platform.claude.com/docs/en/about-claude/pricing)). 공간 판단은 맡기지 말고 결과를 스크립트로 검사 |
| **스킬 회귀 테스트** | 스킬·규칙 수정 후 재검증 | 테스트는 Haiku, 패치는 Opus | RobLe3가 이 조합이 약 10배 저렴했다고 보고([cc-blender-skill](https://github.com/RobLe3/cc-blender-skill), 저자 보고) |

- **effort 명시:** Codex의 GPT-6 Astra 기본 reasoning은 low입니다. 스펙·비평·배치 제약처럼 판단이 필요한 단계는 high 이상으로 지정하세요. Opus 5.5의 기본 effort는 medium입니다. 자세한 비교는 [AI 모델 가이드](../02_guides/01_ai_models_and_clients.md)를 보세요.
- **'GPT-6 Astra 3D'는 OpenAI 제품이 아닙니다.** Scenario 문서에만 나오는 Scenario 자체 3D 파이프라인 이름으로 보입니다([scenario-3d SKILL](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/scenario-3d/SKILL.md), 단일 출처). LLM(Astra·Fable·Opus)과 3D 생성기의 역할을 구분하세요.
- Anthropic은 Opus 5.5가 "Fable 5.1 수준 성능에 Opus 5 대비 운영 비용 40% 절감"이라고 밝혔습니다([Anthropic 뉴스](https://www.anthropic.com/news), 벤더 자체 보고).

### 1.2 도구·MCP 구성

| 용도 | 1순위 | 대안 | 반드시 알아 둘 것 |
|---|---|---|---|
| Blender 실시간 조작 | 커뮤니티 표준 [MCP for Blender](https://github.com/ahujasid/blender-mcp)(PyPI `mcp-for-blender` [2.1.0](https://pypi.org/project/mcp-for-blender/), 2026-09-25, MIT, 36개 tool) 또는 Claude 공식 [Blender 커넥터](https://claude.com/connectors/blender)(Blender Lab 제작, v1.0.1, 애드온 최소 Blender 5.1.0, GPL-3.0-or-later) | [newo-ether 포크](https://github.com/newo-ether/blender-mcp)(노드 그래프를 패치 방식으로 편집), blend-ai(186 tools, 임의 코드 차단, AGPL) | **공식·커뮤니티 둘 다 `localhost:9876`** 이라 동시에 켜면 충돌합니다. 커뮤니티 서버의 Tripo 생성은 유료 Premium 전용입니다 |
| 재현 가능한 빌드·최종 렌더 | headless `blender -b --python build.py` | — | MCP 도구 호출은 소켓 타임아웃(커뮤니티 서버 180초)이나 유휴 타임아웃(stdio 30분·HTTP 서버 5분)에 걸릴 수 있습니다([Claude Code MCP](https://code.claude.com/docs/en/mcp)). 긴 렌더는 headless로 |
| mm 정밀 부품(조인트·하드웨어) | [build123d-mcp](https://github.com/pzfreo/build123d-mcp)(Apache-2.0) | OpenSCAD 계열 MCP | 성능 개선 수치(0.360 → 0.457)는 도구 저자 자체 보고입니다 |
| 3D 생성 | 로컬: [TRELLIS.2](https://github.com/microsoft/TRELLIS.2)·[Pixal3D](https://github.com/TencentARC/Pixal3D)(MIT, ComfyUI 본체 지원 [nodes_trellis2](https://github.com/comfyanonymous/ComfyUI/blob/master/comfy_extras/nodes_trellis2.py)) / 상용: [Meshy MCP](https://github.com/meshy-dev/meshy-mcp-server), [Rodin CLI](https://raw.githubusercontent.com/DeemosTech/hyper3d-cli/main/README.md), Tripo SDK | [Step1X-3D](https://github.com/stepfun-ai/Step1X-3D)(Apache-2.0이지만 텍스처 모듈에 Hunyuan 코드 포함 — 검토 필요) | 4단계의 라이선스 표를 먼저 보세요 |
| 재질·텍스처 | Poly Haven(MCP의 `set_texture`), ambientCG, [Substance 3D Painter MCP](https://github.com/elliezu/SubstancePainterMCP) | [Comfy-Org 공식 ComfyUI MCP](https://github.com/Comfy-Org/comfy-mcp), RTX Remix 내장 MCP([CHANGELOG](https://raw.githubusercontent.com/NVIDIAGameWorks/toolkit-remix/main/CHANGELOG.md)) | Poly Haven 연동은 2026-09-21 [PR #367](https://github.com/ahujasid/blender-mcp/pull/367) 이후 버전을 쓰세요 |
| 엔진 마무리 | UE 5.8 공식 실험적 Unreal MCP(`http://127.0.0.1:8000/mcp`, AllToolsets 필요) + [Epic Claude Code 플러그인](https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin) | — | 4장 참고 |
| API 문서 조회 | MCP의 `bpy_api_lookup`, `describe_node_type`, [fake-bpy-module](https://github.com/nutti/fake-bpy-module) | Context7, 공식 커넥터의 문서 기능 | 모델 학습 데이터에는 구버전 bpy 코드가 많습니다 |

**Blender 버전:** 안정판은 5.2.2(2026-09-14)이고 4.5 LTS·4.2 LTS가 병행 유지됩니다([태그](https://github.com/blender/blender/tags)). 공식 커넥터 애드온은 5.1.0 이상이 필요하고, 이 저장소 스크립트는 4.2.23 LTS·5.0.1에서 테스트했습니다. PyPI `bpy` 5.1 이상은 Python 3.13 전용(5.0은 3.11)입니다. Blender main 브랜치는 5.3 alpha라서 5.2용 규칙의 근거는 v5.2.2 태그 소스로 확인하세요.

설치·연결 절차와 보안 설정은 [빠른 시작](01_quickstart_setup.md), 서버별 차이는 [Blender MCP 가이드](../02_guides/02_blender_mcp.md), 엔진·기타 DCC는 [기타 MCP 가이드](../02_guides/03_other_mcp_dcc_cad_engines.md)를 보세요.

### 1.3 프로젝트 골격과 규약

"Git에 있는 설정과 Blender Python이 원본이고 MCP는 점검 레이어"라는 원칙을 따릅니다. MCP로 뷰포트에서 고친 내용은 반드시 스크립트에도 반영합니다([Codex-and-Blender](https://github.com/danielsobrado/Codex-and-Blender): *MCP edits require durable source equivalents*).

```text
project/
  CLAUDE.md                      ← templates/CLAUDE.md 복사 (Codex·Gemini는 AGENTS.md로)
  .claude/skills/blender-aaa-scene/SKILL.md
  .claude/agents/blender-critic.md   ← 읽기 전용 비평가 (3.2)
  spec/spec_sheet.json  spec/relations.json  spec/acceptance.yaml   ← acceptance는 G1 이후 수정 금지
  ref/                           ← 레퍼런스 (Image 1, Image 2 … 라벨)
  scripts/build_<asset>.py       ← 파라미터화된 멱등 빌더
  versions/scene_v###.blend
  review/v###/                   ← top/front/side/persp.png, beauty.png, falsecolor.png, audit.json
  export/  provenance/assets.csv  PROGRESS.md
```

| 규약 | 값 | 이유 |
|---|---|---|
| 단위·축 | 1 Blender unit = 1 m, Z-up | 스케일이 틀리면 DOF·광량 감쇠·텍스처 밀도가 모두 틀어집니다 |
| 원점 | 오브젝트 바닥 중앙 | 바닥 스냅·배치 계산이 단순해집니다 |
| 정면 | 가구·제품의 앞면은 **-Y** | [`placement_utils.face_towards()`](scripts/README.md)가 이 규약을 씁니다. glTF 원본 정면은 +Z이며 임포트 후 Blender -Y가 됩니다([glTF 스펙](https://raw.githubusercontent.com/KhronosGroup/glTF/main/specification/2.0/Specification.adoc)) |
| 묶음 | 가구 하나 = 부모(Empty) 1개 + 자식 부품 | `scene_audit.py`가 부모 기준 "유닛"으로 판정합니다 |
| 이름 | 영어 + 접두사(예: `SM_`, `M_`, `LGT_`, `CAM_`, 컬렉션 `COL_Blockout/COL_Hero/COL_Props/COL_Lights/COL_Cameras`) | 호출마다 네임스페이스가 새로 만들어지므로 이름이 곧 상태 핸들입니다. 치수 규칙도 이름 키워드(`chair`, `sofa`…)로 동작합니다 |
| 버전 | 단계마다 `versions/scene_v###.blend` | Claude Code의 `/rewind`는 MCP로 바꾼 Blender 상태를 되돌리지 못합니다([best-practices](https://code.claude.com/docs/en/best-practices)) |

### 1.4 이 저장소에서 가져다 쓰는 것

| 자산 | 어느 단계에서 | 쓰는 법 |
|---|---|---|
| [`scripts/scene_audit.py`](scripts/README.md) | 1, 5, 6, 9, 11 | 떠 있음·바닥 관통·유닛 간 관통·스케일 미적용·음수 스케일·non-manifold·재질/UV 없음·치수 범위 이탈을 JSON으로 보고 (Blender 4.2.23 LTS·5.0.1 테스트 통과) |
| [`scripts/placement_utils.py`](scripts/README.md) | 6, 9 | `snap_to_floor`, `drop_to_surface`, `place_next_to`, `place_against_wall`, `face_towards`, `check_clearances` |
| [`scripts/review_views.py`](scripts/README.md) | 1, 2, 5, 6, 9 | 위 정사영·정면·측면·3/4 원근 4장, 오브젝트별 랜덤 색 |
| [`templates/CLAUDE.md`](templates/CLAUDE.md) | 준비 | 프로젝트 규칙(단위, 금지 작업, 루프, 버전 저장) |
| [`templates/skills/blender-aaa-scene/SKILL.md`](templates/skills/blender-aaa-scene/SKILL.md) | 전 단계 | 스펙 → 빌드 → 감사 → 검토 루프를 스킬로 |
| [프롬프트 템플릿](03_prompt_templates.md) | 전 단계 | 이 문서의 "지시 요지"를 완성형 프롬프트로 |
| [품질 체크리스트](04_quality_checklists.md) | 게이트마다 | 모델링·재질·조명·배치·익스포트 체크 항목 |
| [실측 치수표](05_reference_dimensions.md) | 0, 1, 5, 6 | 한국·미국·유럽 치수와 간격, 에이전트용 압축 블록 |
| 가이드 속 코드 | 3, 5, 6, 7, 10, 11 | `review_render()`([조명 가이드](../02_guides/06_lighting_rendering_art_direction.md) 2.3절), 부품 단위 조립 검사 `check_assembly()`([모델링 가이드](../02_guides/07_modeling_objects_furniture_sculpture.md) 2.4절), `grid_solver.py`([배치 가이드](../02_guides/08_scene_layout_placement.md) 4.4절), `pbr_audit`([재질 가이드](../02_guides/05_texturing_materials.md) 4.7절), 생성 에셋 정규화([AI 3D 생성](../02_guides/04_ai_3d_generation.md) 6.2절), provenance 기록([에셋·라이선스](../02_guides/10_assets_pipeline_licensing.md) 5.4절) |

MCP로 스크립트를 쓰는 방법은 두 가지입니다: `sys.path`에 `03_playbooks/scripts`를 추가해 import하거나, 파일 내용을 `execute_blender_code`에 그대로 붙여 넣습니다([사용법](scripts/README.md)). `BLENDER_MCP_SAFE_MODE=1`은 bpy를 통한 저장·렌더는 허용하지만(검증 결과) 외부 모듈 import 방식이 허용되는지는 확인되지 않았습니다. 막히면 붙여 넣기 방식을 쓰세요.

### 1.5 [한국 사용자] 시작 전 점검

1. **UI 언어:** 현지화 UI에서는 새로 만든 노드 이름도 번역될 수 있습니다. 일본어 UI에서 `Principled BSDF`가 `プリンシプルBSDF`로 만들어져 스크립트가 깨진 사례가 있습니다([roo-blendermcp-jp-rules](https://github.com/hideki711014/roo-blendermcp-jp-rules)). 한국어 UI에도 같은 원리가 적용될 가능성이 높습니다(추정). 영어 UI를 쓰거나 Preferences > Interface > Translation에서 **New Data** 번역을 끄세요(속성 `use_translate_new_dataname`는 bpy 5.0.1에 있음. 번역 동작 자체는 미확인). 코드에서는 `n.type == 'BSDF_PRINCIPLED'`처럼 type으로 찾게 합니다.
2. **라이선스:** Hunyuan3D 2.0/2.1/Omni/Part, HY-World 2.0, HunyuanWorld 1.0, HY-Motion 1.0의 라이선스는 EU·영국·대한민국을 적용 지역에서 빼고, 그 밖에서 **출력물**을 쓰는 것도 금지합니다([Hunyuan3D-2.1 LICENSE](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/LICENSE)). MCP for Blender의 Hunyuan 로컬 연동도 같은 문제를 안고 있습니다. Tencent Cloud API 약관은 별개이며 원문을 확인하지 못했습니다(미확인).
3. **치수:** 한국 아파트 천장고, 주방 상판 높이, 매트리스 규격은 미국·유럽과 다릅니다. 스펙 단계에서 `REGION=KR`을 명시하고 [치수표](05_reference_dimensions.md)의 한국 프리셋을 쓰세요.
4. **경로:** Windows에서 스크립트 경로를 넘길 때는 `r"C:\..."` 형태의 절대 경로를 씁니다. 검토 렌더 출력 폴더도 절대 경로로 넘깁니다.

---

## 2. 단계별 절차

각 단계는 같은 틀로 적었습니다: **목적 / 누가 / 입력 / 할 일 / 에이전트 지시 요지 / 통과 게이트 / 산출물 / 장면별 차이 / 흔한 실패**. "지시 요지"는 핵심만 담은 것이고, 완성형 프롬프트는 [프롬프트 템플릿](03_prompt_templates.md)에 있습니다.

### 단계 0 — 목표·레퍼런스·스펙시트

- **목적**: 모델이 빈칸을 임의로 채우지 못하게 합니다. "의자 하나 만들어 줘"에는 치수·부품·재질이 비어 있습니다.
- **누가**: 계획 모델이 초안을 쓰고, 사람이 승인합니다(G1). 레퍼런스가 없으면 이미지 모델로 만듭니다.
- **입력**: 요청 문장, 레퍼런스 사진·스케치·평면도·스캔, 대상 지역(KR/US/EU), 용도(스틸 렌더/게임 에셋/둘 다).

**할 일**

1. **레퍼런스 보드**를 만듭니다. 무드, 팔레트, 계절·시간대, "복제할 특징 목록"을 적고 히어로를 한 문장으로 정합니다.
2. 레퍼런스 이미지는 **텍스트보다 앞에**, `Image 1:`, `Image 2:` 라벨을 붙여 줍니다([Claude vision 문서](https://platform.claude.com/docs/en/build-with-claude/vision)). 여러 뷰를 주면 뷰마다 역할과 불일치 해소 규칙을 지정합니다(예: 전체 비율은 측면, 폭은 정면).
3. **spec_sheet**를 코드보다 먼저 씁니다([Gaius114 blender-research](https://raw.githubusercontent.com/Gaius114/blender-claude-mcp/main/skill/blender-research/SKILL.md) 방식). 부품은 [PartNet 계층](https://raw.githubusercontent.com/daerduoCarey/partnet_dataset/master/stats/after_merging_label_ids/Chair-hier.txt)을 체크리스트로 씁니다(chair_back / chair_seat / chair_base(leg, bar_stretcher) / chair_arm).
4. **합격 기준**을 생성 전에 `acceptance.yaml`로 고정합니다. *"a result is scored, not admired"*([scenario-model-comparison](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/scenario-model-comparison/SKILL.md)). 이후 에이전트가 이 파일을 고치지 못하게 합니다.
5. 예산을 적습니다: 삼각형(모바일 소품 3k~8k, 일반 게임 에셋 10k~50k), 텍스처 해상도, 렌더 해상도, 유료 생성 크레딧 상한.

**에이전트 지시 요지**

```text
모델링 전에 spec_sheet(JSON)만 써라.
- meta: 이름, 스타일, 용도(스틸/게임), REGION=KR, 폴리 예산, 텍스처 해상도
- dims_m: 전체 W/D/H, 핵심 관계 치수(예: 식탁 상판과 의자 좌면 차 0.27~0.30)
- parts[]: name, 방법(primitive/코드/라이브러리/생성), size_m, position_m(바닥 중앙 기준), 재질(linear 색, roughness, metallic 0|1)
- 생략한 PartNet 부품과 이유, 불확실한 치수는 범위로
- camera/lighting 의도(시간대, 켈빈), acceptance(숫자 기준)
작성 후 멈추고 내 승인을 기다려. 치수는 추측하지 말고 근거를 대라.
```

**통과 게이트 (G1)**

- [ ] 히어로가 한 문장으로 정의되어 있다
- [ ] 전체 치수와 관계 치수가 숫자이고, 지역 프리셋이 명시되어 있다
- [ ] 부품 목록이 PartNet 계층 대비 누락 없이 검토되었다
- [ ] 폴리·텍스처·렌더 예산과 출력 형식이 있다
- [ ] 합격 기준(수치 + 렌더 기준)이 `acceptance.yaml`에 있다
- [ ] 라이선스 제약(상업 여부, 한국 제외 모델)이 적혀 있다
- [ ] **사람이 OK**

**산출물** `spec/spec_sheet.json`, `spec/acceptance.yaml`, `ref/` 보드, `PROGRESS.md` 첫 항목.

**장면별 차이**

- **A 실내:** 방 폴리곤, 천장 높이, 문·창 위치와 크기, 초점(TV 벽·창 전망), 기능 그룹(대화·식사·작업)을 스펙에 넣습니다. 스캔이나 평면도가 있으면 "근거가 있는 공간만 만들고 불확실한 곳은 기록"하게 합니다([realsee-astra-blender](https://github.com/realsee-developer/realsee-astra-blender)).
- **B 제품:** 정면·측면 정사영 레퍼런스를 준비합니다. 이미지로 레퍼런스를 만들 때는 "단일 오브젝트, 단색 배경, 3/4 뷰, 부드러운 조명, 텍스트 없음"으로 씁니다([asset-studio](https://github.com/zorrobyte/asset-studio)).
- **C 야외:** 면적, 경로, 랜드마크, 밀도 구역(전경·중경·배경), 시드(seed)를 정합니다. 실제 장소라면 모델의 기억 대신 지도·표고 데이터를 쓰게 합니다([per-simmons 가이드](https://raw.githubusercontent.com/per-simmons/unreal-agent-harness/master/AGENTIC-GAMEDEV-GUIDE.md)).

**흔한 실패**

- 스펙 없이 바로 모델링 → 부품이 떠 있거나 관통합니다. 스펙 단계에서 치수표 검사와 부품 누락 검사를 먼저 하면 코드 단계 오류가 줄어듭니다.
- 형용사만 있는 지시("고급스럽게") → 수치 제약과 금지 목록으로 바꿉니다. 소형 모델일수록 "품질 형용사 대신 절차 제약"이 효과적이었습니다([roo-blendermcp-jp-rules](https://github.com/hideki711014/roo-blendermcp-jp-rules)).
- 같은 물건인데 자료마다 치수가 다름(문 0.8×2.0 m 대 0.9×2.1 m) → 프로젝트 기준을 하나로 정해 `CLAUDE.md`에 적습니다.

---

### 단계 1 — 스케일 블록아웃

- **목적**: 실측 스케일과 전체 비율을 가장 싼 형태(프리미티브)로 먼저 확정합니다. 스케일 오류는 이후 모든 것을 조용히 망가뜨립니다.
- **누가**: 빌더 모델 + `scene_audit.py`. 비평가는 4방향 렌더만 봅니다.
- **입력**: 승인된 spec_sheet, [치수표](05_reference_dimensions.md).

**할 일**

1. 단위를 Metric, `scale_length = 1.0`으로 확인합니다.
2. 스펙의 부품마다 프리미티브를 **실측 치수**로 만듭니다. 원점은 바닥 중앙, 스케일은 즉시 적용합니다. 큐브는 `size=2`로 만들어 scale 값이 반폭(half-extent)과 같게 하면 치수 계산 실수가 줄어듭니다([ProfRino Assembly Skill](https://github.com/ProfRino/Blender-MCP-Assembly-Skill)).
3. **스케일 기준물**을 둡니다: 1.75~1.8 m 인체 더미, 문틀(최종 렌더에서는 숨김).
4. 코드는 부품 하나, 단계 하나씩 **멱등**으로 씁니다(3.1 참고).
5. `scene_audit.audit_scene(floor_z=0.0)`을 돌리고, `render_review_views()`로 4방향을 봅니다.
6. `versions/scene_v001.blend`로 저장합니다.

**에이전트 지시 요지**

```text
spec_sheet의 부품을 실측 치수의 프리미티브로만 만들어라. 디테일·베벨·재질 금지.
원점은 바닥 중앙, 스케일 즉시 적용, 부품은 부모 Empty 아래에.
끝나면 scene_audit 결과 요약과 유닛별 dimensions_m 표(스펙 대비 오차 %)를 보고하고,
review_views 4장을 찍어 비율을 레퍼런스와 비교해라. 오차가 3%를 넘는 부품만 고쳐라.
```

**통과 게이트**

- [ ] 전체 치수가 스펙 ±3% 이내(레퍼런스가 있으면 blockout 실루엣 IoU ≥ 0.85, 비율 오차 ≤ 5%. [blender-image-to-3d](https://raw.githubusercontent.com/majidmanzarpour/blender-game-skills/main/skills/blender-image-to-3d/SKILL.md) 기준, 커뮤니티 스킬)
- [ ] `scene_audit`: `floating_or_wall_mounted`(의도한 벽걸이 제외), `below_floor`, `interpenetrations`, `unapplied_scale`, `negative_scale`, `size_out_of_range`가 모두 0
- [ ] 스케일 기준물과 비교했을 때 이상 없음(눈 검사)
- [ ] `v001.blend` 저장 로그

**산출물** `versions/scene_v001.blend`, `review/v001/*.png`, `review/v001/audit.json`.

**장면별 차이**

- **A 실내:** 벽·바닥·천장·문·창 개구부를 먼저 만들고, 가구는 크기가 맞는 박스로 둡니다(구조 → 주요 가구 → 소품 순서, [realsee](https://github.com/realsee-developer/realsee-astra-blender)). 최종을 Unreal Lumen으로 가져갈 계획이면 벽 두께를 10 cm 이상으로 잡습니다([Lumen 기술 문서 미러](https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/lumen-technical-details-in-unreal-engine.md), 비공식 미러). 저장 후 다시 열어 벽 한 구간과 문 하나를 실제로 편집해 보는 확인도 권합니다.
- **B 제품:** 부품별 박스와 실린더(좌판, 등받이, 다리 4개)만 둡니다. 참고값: 라운지 체어 좌면 높이 0.40~0.43 m, 식탁 의자 좌면 0.45 m(치수표 참조).
- **C 야외:** 지형, 경로 커브, 랜드마크 매스, 밀도 구역 마스크를 만듭니다. 넓은 지역은 50×50 m 셀로 나누고 seed를 고정하면 재현됩니다([astra-blender-forest](https://github.com/octopus7/astra-blender-forest), 한국 개발자로 추정되는 사례).

**흔한 실패**

- `obj.dimensions`만 보고 배치 → `dimensions`는 스케일은 반영하지만 **회전은 반영하지 않는 로컬 축 기준**입니다. 배치에는 `matrix_world @ bound_box`로 구한 월드 AABB를 쓰세요(`placement_utils.world_bbox`).
- `get_scene_info`로 전체 파악 → 이 도구는 객체를 최대 10개만, 치수 없이 반환합니다([addon.py](https://raw.githubusercontent.com/ahujasid/blender-mcp/main/addon.py)). `scene_audit` JSON을 씬 목록으로 씁니다.
- 원점이 형상 중심 → 바닥에 반쯤 묻힙니다. 원점을 바닥 중앙으로 옮기고 `snap_to_floor`를 씁니다.

---

### 단계 2 — 카메라·구도 고정

- **목적**: 조명과 디테일은 시점에 의존합니다. 카메라를 먼저 잠가야 프레임 밖이나 흐려질 곳에 시간을 쓰지 않습니다.
- **누가**: 빌더가 후보를 렌더하고, 비평가가 비교하고, 사람이 고릅니다(G2).
- **입력**: 블록아웃 씬, 레퍼런스 보드, 스펙의 카메라 의도.

**할 일**

1. 후보 카메라 6~7개를 저품질로 렌더해 한 장의 비교 시트로 만듭니다([hyperrealism 08장](https://raw.githubusercontent.com/Bartindigital/blender-hyperrealism-skill/main/references/08-composition-workflow.md), 커뮤니티 규칙집·미검증).
2. 초점거리와 높이를 의도에 맞춥니다. 커뮤니티 스킬 기준: 와이드 18~28 mm, 스토리·제품 35~50 mm, 인물·히어로 85~135 mm, 사람 눈높이 1.6~1.7 m([arjun988 camera](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/camera-cinematography/SKILL.md)). 기본 50 mm를 무심코 쓰는 것은 AI 결과물의 흔한 티입니다.
3. 건축·실내는 카메라를 수평으로 두고 Shift Y로 수직선을 보정합니다.
4. 구도 규칙: 한 뷰에 히어로 하나, 전경·중경·배경 레이어, 삼분할, 프레임 가장자리 접선 피하기.
5. 고른 카메라를 `CAM_Hero`로 이름 짓고 위치·회전을 잠급니다.

**에이전트 지시 요지**

```text
후보 카메라 6개를 만들어 저해상도로 렌더하고 한 장의 비교 시트로 보여 줘.
카메라마다 초점거리, 높이, 의도를 한 줄로 적어라. 기본 50mm를 그대로 쓰지 마라.
내가 고르면 CAM_Hero로 이름 짓고 transform을 잠가라. 이후 단계에서 CAM_Hero를 움직이지 마라.
```

**통과 게이트 (G2)**

- [ ] 썸네일 크기에서도 히어로가 읽힌다(squint 테스트)
- [ ] 수직선이 곧다(의도한 경우 제외)
- [ ] 초점거리·높이가 기록되어 있다
- [ ] `CAM_Hero` 잠금
- [ ] **사람이 OK**: 블록아웃 스크린샷 1장 + 3줄 요약을 보고 승인

**산출물** `CAM_Hero`(+ 필요 시 보조 카메라 1~2개), `review/v002/camera_sheet.png`, `v002.blend`.

**장면별 차이**

- **A 실내:** 눈높이 1.6 m 문 쪽 시점을 기본으로, 과한 광각을 피합니다. 배치 검토용으로 탑다운 정사영 카메라를 따로 둡니다(렌더용 아님).
- **B 제품:** 3/4 뷰, 망원 쪽. 게임 에셋이면 정면·측면 정사영 검토 카메라를 레퍼런스에 맞춰 둡니다([reference-analysis-validator](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/reference-analysis-validator/SKILL.md)).
- **C 야외:** establishing 샷, 전경 프레이밍 요소(잎, 바위) 자리를 비워 둡니다. 3분할 교차점에 히어로 클러스터 자리를 표시합니다.

**흔한 실패**

- 조명·재질을 만든 뒤 카메라를 바꿈 → 조명을 처음부터 다시 잡게 됩니다. G2 이후 카메라는 고정입니다.
- 스케일이 틀린 상태에서 DOF → 미니어처처럼 보입니다. 1단계 게이트를 먼저 통과시키세요.

---

### 단계 3 — 라이트 v1 (색관리 먼저)

- **목적**: 색 없는 조명으로 형태가 읽히는지 확인합니다. 조명값은 뷰 변환에 맞춰 잡기 때문에 색관리를 가장 먼저 고정합니다.
- **누가**: 빌더 + 렌더 + 수치 게이트([`review_render()`](../02_guides/06_lighting_rendering_art_direction.md)).
- **입력**: 고정된 `CAM_Hero`, 블록아웃(재질은 회색 clay).

**할 일**

1. **색관리:** View Transform AgX + Look `AgX - Medium High Contrast`(또는 Punchy). 제품 색 재현이 중요하면 `Khronos PBR Neutral`([Khronos](https://github.com/KhronosGroup/ToneMapping/tree/main/PBR_Neutral)). Standard는 쓰지 않습니다. OCIO 파일 자체의 기본값은 Standard이므로([config.ocio v5.2.2](https://raw.githubusercontent.com/blender/blender/v5.2.2/release/datafiles/colormanagement/config.ocio)), 씬을 새로 만들거나 factory-startup으로 실행했으면 반드시 확인합니다.
2. **검정에서 시작:** World 0, 램프 모두 끈 상태에서 HDRI → 키 → (필·림) 순으로 하나씩 추가하고, 하나를 조정할 때 나머지는 숨깁니다.
3. **키 배치(시작값):** 카메라 축에서 40°, 위로 35°, 피사체 반경의 3배 거리, 광원 크기 = 피사체 반경. 카메라 축 20° 미만의 정면 키는 금지([scenario lighting](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/dcc/blender/scenario-blender-lighting-rendering/SKILL.md), 툴킷 자체 정의 값).
4. **광원 크기 0 금지:** bpy로 새로 만든 라이트는 radius 기본값이 0이라 칼 같은 그림자가 납니다([DNA 기본값](https://raw.githubusercontent.com/blender/blender/main/source/blender/makesdna/DNA_light_types.h): radius 0, energy 10, temperature 6500K, sun angle 0.526°).
5. **밝기는 `view_settings.exposure`로** 조절합니다. 램프를 하나씩 스케일하면 광량비가 깨지고 에이전트가 값을 오가며 진동합니다.
6. False Color로 노출을 판정합니다. AgX는 클리핑을 부드럽게 숨기므로 표시 이미지만 보면 속습니다.

**에이전트 지시 요지**

```text
색관리를 AgX(Medium High Contrast)로 설정하고 World를 0으로 시작해라.
무채색 키 하나를 카메라 축에서 40°, 위 35°, 피사체 반경 3배 거리, 크기 = 반경으로 두고
필과 림은 약하게 하나씩 추가해라. 밝기는 exposure로만 조절하고 램프 비율은 고정해라.
review_render로 beauty + False Color + 수치(clip_pct, value_range)를 저장하고 이미지를 직접 본 뒤 보고해라.
```

**통과 게이트**

- [ ] `view_transform`이 Standard가 아니다
- [ ] 회색 clay 상태에서 명암만으로 형태가 읽힌다
- [ ] 키가 카메라 축에서 20° 이상 떨어져 있고, 모든 광원 크기 > 0
- [ ] False Color에서 피사체가 회색(≈ 0 EV)이고, 발광체를 뺀 클리핑 ≤ 0.5%, value range ≥ 0.30(scenario 게이트, 자체 정의 값)

**산출물** 색관리 설정, `LGT_Key_Main` 등 조명 v1, `review/v003/beauty.png`, `falsecolor.png`, `stats.json`.

**장면별 차이**

- **A 실내:** 창 방향 HDRI나 Sun + 실용광 자리 표시. 실내에서 World 기여는 10% 미만을 목표로 합니다(scenario 게이트, Light Group으로 분리 측정).
- **B 제품:** 키·필·림 3점. 크고 부드러운 키가 기본입니다.
- **C 야외:** Sun + HDRI 두 개로 시작합니다. 태양 각지름은 실제값 약 0.53°, 더 부드럽게 하려면 2~5°([조명 가이드](../02_guides/06_lighting_rendering_art_direction.md) 3.3절).

**흔한 실패**

- 조명으로 스케일·형태 문제를 가림 → blender-production 규칙대로 *보정용 조명·재질로 결함을 숨기지 말고 원인을 고친 뒤 같은 뷰로 비교*합니다([blender-production](https://raw.githubusercontent.com/per-simmons/blender-production/master/SKILL.md), 성숙도 낮은 저장소).
- 뷰포트 스크린샷으로 조명 판정 → 뷰포트는 최종 색관리·GI·DOF와 다릅니다. MCP for Blender에는 전용 렌더 도구가 없으니([#61](https://github.com/ahujasid/blender-mcp/issues/61), not planned) `execute_blender_code`로 실제 렌더를 파일로 저장해 봅니다.

---

### 단계 4 — 에셋 조달 결정 (라이브러리 / AI 생성 / 직접 모델링)

- **목적**: 블록아웃의 박스마다 "어디서 가져올지"를 정합니다. 에이전트의 모델링 품질 한계를 우회하는 가장 현실적인 결정입니다.
- **누가**: 계획 모델이 표를 만들고, 사람이 비용·라이선스를 승인합니다.
- **입력**: 블록아웃 유닛 목록, 예산, 라이선스 조건.

**결정표**

| 대상 | 1순위 | 2순위 | 피할 것 | 근거 |
|---|---|---|---|---|
| 흔한 배경·자연물(바위, 나무, HDRI) | CC0 라이브러리(Poly Haven, ambientCG), BlenderKit | AI 생성 | 처음부터 직접 모델링 | 5가지 방식을 비교한 결과 CC0 키트가 "가장 깨끗한 실제 건물"이었고, 이미지→3D는 일회성 소품에만 맞았습니다([per-simmons](https://raw.githubusercontent.com/per-simmons/unreal-agent-harness/master/AGENTIC-GAMEDEV-GUIDE.md)) |
| 반복 요소(파사드, 벽 키트, 나무 군락) | 모듈러 키트 + **인스턴싱** | Geometry Nodes 절차 생성 | 이미지→3D로 하나씩 | 메시 127개를 16,573번 인스턴싱한 숲([astra-blender-forest](https://github.com/octopus7/astra-blender-forest)) |
| 히어로 하드서페이스·가구·제품 | **스펙 기반 파라메트릭 코드**(bpy, mm 정밀 부품은 build123d) | AI 생성 → 파트 bbox만 따서 코드로 재모델링 | 통짜 AI 메시를 그대로 | 부품 단위 코드가 편집성과 정확도를 함께 올립니다([모델링 가이드](../02_guides/07_modeling_objects_furniture_sculpture.md)) |
| 유기체·캐릭터·조각 | 이미지→3D 생성 → 리메시·UV·베이크 | SDF·메타볼 코드([fogleman/sdf](https://github.com/fogleman/sdf)) | LLM이 정점을 직접 나열 | 같은 일러스트에서 얼굴·옷 디테일은 Meshy 7이 Astra 직접 모델링보다 나았다는 보고(n=1, 2차 요약) |
| 실제 장소·건물 | 지도·표고·스캔 데이터 + 키트 | — | 모델의 기억 | 데이터 없이 만든 집은 "찌그러진 회색 플라스틱 모형" 같았다는 사례(2차 요약) |

**라이선스 확인표 (상업 작업 기준, 2026-09)**

| 도구·에셋 | 라이선스 | 판단 |
|---|---|---|
| Hunyuan3D 2.0/2.1/Omni/Part, HY-World 2.0, HY-Motion | Tencent Community License | **[한국] 적용 지역 밖. 출력물 포함 사용하지 않음** |
| TRELLIS.2 | 코드·모델 MIT. 단 nvdiffrast는 NVIDIA 비상업, 이미지 인코더는 DINOv3 License, 파이프라인 기본 배경 제거기 RMBG-2.0은 비상업 | 법무 검토 필요. 배경 제거한 알파 PNG를 직접 넣으세요 |
| Pixal3D | MIT(추론 시 DINOv3 로드) | 인코더 라이선스 확인 필요 |
| Step1X-3D | 코드 Apache-2.0. 단 텍스처 모듈에 Hunyuan3D 2.0 라이선스 코드가 섞여 있고 nvdiffrast(비상업)에 의존 | **텍스처 단계는 법률 검토 전 보류**. 형상만 쓰는 경우도 검토 필요([10 가이드](../02_guides/10_assets_pipeline_licensing.md)) |
| SAM 3D Objects | SAM License(상업 허용, 금지 용도 제외), VRAM 32GB 이상 | 가능 |
| PartCrafter | MIT | 가능 |
| PartPacker, Roblox Cube, CHORD | 비상업·연구 전용 | 상업 불가 |
| Poly Haven, ambientCG, PBRify 모델 | CC0 | 가능. Poly Haven live API는 크레딧 표기 요청 |
| Poly Pizza | 약 69%가 CC-BY | 표기 필요. `licence='CC0'` 필터로 피할 수 있음 |
| Meshy, Tripo, Rodin | 유료 플랜 약관 | 플랜별 상업권이 다름([에셋·라이선스 가이드](../02_guides/10_assets_pipeline_licensing.md)) |

**할 일**

1. 블록아웃 유닛마다 위 결정표로 경로를 정하고 `asset_manifest.csv`에 적습니다(유닛, 경로, 후보 출처, 라이선스, 예상 비용, 표기 의무).
2. 생성할 것은 **이미지 먼저, 그다음 3D**로 갑니다. 이미지 프롬프트는 "단일 오브젝트, 중앙, 단색 배경, 3/4 뷰, 부드러운 조명, 텍스트 없음"으로 다시 씁니다([asset-studio](https://github.com/zorrobyte/asset-studio)). TRELLIS.2는 배경이 있으면 구멍과 아티팩트가 심합니다([#65](https://github.com/microsoft/TRELLIS.2/issues/65)).
3. 반사가 강한 레퍼런스는 delight 옵션을 켭니다(Rodin `--texture-delight`, [hyper3d-cli](https://raw.githubusercontent.com/DeemosTech/hyper3d-cli/main/README.md)).
4. 치수를 생성 단계에서 넣습니다: Rodin `bbox_condition`·`height`, Tripo `auto_size`.
5. **버전을 고정합니다.** Tripo SDK 기본값은 아직 `v2.5-20250123`이므로 `v3.1-20260211`이나 `P1-20260311`을 명시합니다([client.py](https://raw.githubusercontent.com/VAST-AI-Research/tripo-python-sdk/master/tripo3d/client.py)).
6. **무료 픽스처로 파이프라인을 끝까지 먼저 검증**한 뒤 유료 생성을 씁니다. Robo Open은 이렇게 해서 Meshy 크레딧을 30크레딧만 썼고, 에이전트가 제안한 400크레딧 상한을 사람이 승인했습니다([Robo Open](https://github.com/az9713/gpt-6-astra-tennis-game)).
7. 비동기 작업 규칙: 타임아웃이 나도 **다시 제출하지 않고** 상태를 조회합니다. Rodin 결과 URL은 10분 뒤 만료되므로 바로 받습니다([rodin3d-skills](https://github.com/DeemosTech/rodin3d-skills/blob/main/skills/rodin3d-skill/SKILL.md)).
8. 비용 레버: 형태를 싸게 확정한 뒤 텍스처를 입힙니다(텍스처와 8K 옵션이 비용 대부분).

**에이전트 지시 요지**

```text
블록아웃 유닛마다 [라이브러리 / 모듈러+인스턴싱 / 파라메트릭 코드 / AI 생성 / 데이터] 중 하나를 고르고
asset_manifest.csv(유닛, 경로, 후보 출처 URL, 라이선스, 예상 크레딧, 표기 의무)를 만들어라.
한국 사용이므로 Hunyuan 계열 로컬 웨이트는 후보에서 뺀다.
유료 생성은 호출 전에 항목별 비용과 합계를 보여 주고 내 승인을 받아라. 타임아웃이 나도 재제출 금지.
```

**통과 게이트 (비용 승인)**

- [ ] 모든 유닛에 경로·출처·라이선스·비용이 있다
- [ ] 한국에서 쓸 수 없는 모델이 목록에 없다
- [ ] 무료 픽스처로 임포트 → 정규화 → 익스포트까지 한 번 통과했다
- [ ] 유료 생성 합계와 크레딧 상한을 **사람이 승인**

**산출물** `asset_manifest.csv`, 생성 레퍼런스 이미지, (승인 후) 원본 에셋 `assets/raw/`.

**장면별 차이**

- **A 실내:** 가구는 히어로 1~2점만 코드로, 나머지는 라이브러리. 소품은 라이브러리 우선.
- **B 제품:** 히어로 자체는 코드 경로가 기본입니다. 곡면이 많은 제품은 생성 → 파트 bbox 추출 → 코드 재모델링 하이브리드.
- **C 야외:** 식생·바위는 라이브러리와 인스턴싱, 히어로 바위나 쓰러진 나무만 고유 모델.

**흔한 실패**

- 버전 미지정으로 구모델 사용, 타임아웃 후 재제출로 크레딧 이중 소모.
- 생성 메시를 그대로 사용 → 5단계의 정리 절차를 반드시 거칩니다.
- 3D QA census의 "TRELLIS.2 출력 91.1% non-watertight" 수치를 근거로 인용 → 원저자가 철회한 초기 측정(n=101)입니다. 인용하지 말고 직접 검사하세요.

---

### 단계 5 — 히어로 모델링 (스펙 우선)

- **목적**: 시선이 머무는 히어로 에셋의 형태·비율·부품 구조를 맞춥니다.
- **누가**: 빌더가 부품 단위 코드를 쓰고, 비평가가 정사영 비교와 예/아니오 질문으로 판정합니다.
- **입력**: 승인된 부품 스펙, 레퍼런스, 블록아웃 프록시.

**할 일 — 코드 경로(하드서페이스·가구·제품)**

1. **부품 명세 JSON**을 코드보다 먼저 확정합니다: 부품별 `size`, `location`, `attach_to`(부모 면), 결합 방식, 허용 관입.
2. 부품 하나에 함수 하나(`build_seat()`, `build_leg(pos)`)로 `scripts/build_<asset>.py`를 쓰고, 대화형 루프에서는 이 함수를 `execute_blender_code`로 부릅니다.
3. **형태 1·2·3차:** 1차 큰 덩어리 → 2차 곡률·테이퍼·접합부 → 3차 베벨·이음새.
4. **모디파이어 순서:** Mirror → Array → Solidify → Bevel → Subdivision Surface. Bevel과 SubSurf 순서가 바뀌면 핀칭이 생깁니다([RobLe3 modeling](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-modeling/SKILL.md)). Weighted Normal은 스택 맨 끝입니다.
5. **베벨:** 크기를 모를 때 최대 치수의 0.5% 폭, 렌더 3 segments / 게임 1~2, angle 30°, Harden Normals([scenario hard-surface](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/dcc/blender/scenario-blender-hard-surface/SKILL.md), 스킬 저자 추가 기본값). 스케일을 적용한 뒤에 넣습니다. Auto Smooth는 Blender 4.1에서 제거됐으니 Smooth by Angle을 씁니다.
6. **결합 규칙을 정합니다.** 연결부를 5~15 mm 서로 파고들게 해 이음새를 숨기는 관행(RobLe3, ProfRino)과 "관입은 `JOINT_` 접두사만 허용"하는 검사 규칙은 서로 충돌합니다. [모델링 가이드](../02_guides/07_modeling_objects_furniture_sculpture.md)는 **연결 맵에 적은 쌍만 5~15 mm 겹침을 허용하고 나머지 겹침은 실패**로 정리했고, 이를 `check_assembly()`(같은 가이드 2.4절)로 검사합니다. `scene_audit.py`는 유닛끼리만 검사하고 같은 유닛 안의 부품끼리는 일부러 검사하지 않으므로 두 검사를 함께 씁니다.
7. 방향이 있는 부재(다리, 봉)는 Euler 회전 대신 bmesh로 두 점 사이를 잇습니다(실린더 회전 오류 방지, [ProfRino](https://github.com/ProfRino/Blender-MCP-Assembly-Skill)).
8. **결정적 검사 먼저, 렌더는 그다음**: build123d-mcp 규칙은 *"After every execute() call measure(); ... Only after (1) and (2) pass call render_view()"*입니다([default_prompt](https://raw.githubusercontent.com/pzfreo/build123d-mcp/main/default_prompt.md)).
9. **정사영 비교:** 레퍼런스 뷰에 맞춘 정사영 카메라로 실루엣 마스크를 렌더해 비교합니다. 같은 종류끼리 비교해야 합니다(와이어 대 셰이딩 렌더는 IoU가 낮게 나옴).
10. **예/아니오 검증 질문:** 비평가가 요청 충족 여부를 판정할 질문 8~12개를 먼저 만들고, 4방향 렌더를 보고 근거와 함께 답하게 합니다. "아니오"만 수정 지시로 바꿉니다([CADCodeVerify](https://github.com/Kamel773/CAD_Code_Generation) 방식).
11. **측면 두께 확인:** 정면 레퍼런스로 만든 모델은 옆에서 보면 얇기 쉽습니다(몸통 깊이를 1.45배로 고친 사례, [modeling-playground](https://github.com/mizchi/modeling-playground)).
12. 결함 원장에 기록하고 **가장 큰 결함 하나만** 고칩니다(3.3 참고).

**할 일 — 생성 메시 경로(유기체·조각·복잡한 곡면)**

1. 임포트 직후 bounds로 실측합니다. 생성 결과가 약 1.4 m로 작게, Y-up으로 들어온 사례가 있습니다.
2. 목표 높이 기준 **균일 스케일**(비균일 금지) → 원점 바닥 중앙 → transform 적용 → merge by distance 0.0001 m → 노멀 재계산.
3. voxel remesh → decimate 순서(순서가 형상 보존에 중요, [image-to-3dlab](https://github.com/Bingeljell/image-to-3dlab)) → 새 UV → 고해상도 master에서 color·metal-rough·normal 베이크 → LOD(50%, 25%) → 콜리전.
4. 참고 수치(작성자 보고): asset-studio는 상자 954,901 → 7,998 tris(오차 1.4%)에 11.1분, 펌프 997,520 → 19,803 tris(2.3%)에 15.6분, 예산만 바꾼 재최적화는 약 80초였습니다([asset-studio](https://github.com/zorrobyte/asset-studio)).
5. 파트가 필요하면 파트 단위 생성(PartCrafter 최대 16파트)이나 생성 후 파트 bbox만 뽑아 코드로 재모델링합니다.

**에이전트 지시 요지**

```text
부품 명세 JSON을 확정한 뒤, 부품 하나당 멱등 함수 하나로 build_<asset>.py를 써라.
각 부품을 만들 때마다 연결 맵 기준으로 부모와 붙었는지·과하게 겹치는지 check_assembly()로 확인하고 다음 부품으로 넘어가라.
모든 제조 모서리에 베벨(스케일 적용 후), Weighted Normal은 스택 끝.
끝나면 정사영 front/side/top + 3/4 렌더를 1.75 m 인체 더미와 함께 제출하고,
유닛별 삼각형 수, 부품 수(스펙 대비), 결함 원장을 보고해라. 숫자가 통과해도 이미지가 틀리면 실패다.
```

**통과 게이트**

- [ ] 부품 단위 `check_assembly()` 결과에 틈·과도한 겹침·계획에 없는 관통·떨어진 부품 0, 유닛 단위 `scene_audit` issue 0(non-manifold 포함)
- [ ] 부품 수가 스펙과 정확히 같다
- [ ] 레퍼런스가 있으면 실루엣 IoU ≥ 0.90, 비율 오차 ≤ 2%(forms 단계, blender-image-to-3d 기준. 가구 최종은 IoU ≥ 0.92 제안)
- [ ] 제조 모서리가 모두 하이라이트를 받는다(렌더로 확인)
- [ ] 삼각형 예산 이내
- [ ] 비평가 예/아니오 질문에서 "아니오"가 Minor만 남았다

**산출물** `scripts/build_<asset>.py`, 히어로 에셋(부품별 오브젝트), 결함 원장, `review/v005/`.

**장면별 차이**

- **A 실내:** 히어로는 1~2점(소파, 식탁 세트 등). 한국 4인 식탁 예: 1.40 × 0.80 × 0.74 m, 의자 좌면 0.45 m(치수표 확인).
- **B 제품:** 이 단계가 작업의 대부분입니다. cinematic 프로필(수정 4회)을 씁니다.
- **C 야외:** 히어로 바위·쓰러진 나무·표지판 정도. 조형물은 생성 메시 경로, 받침대는 하드서페이스로 따로 모델링합니다.

**흔한 실패**

- 한 번에 통째로 모델링 → 부품 계획을 먼저 검증하는 2단계 게이트가 실패를 줄입니다([Gaius114](https://github.com/Gaius114/blender-claude-mcp)).
- 떠 있는 부품 검사를 bbox 중심 한 줄 레이로 함 → 다리 위 좌판처럼 "중심 아래가 빈" 부품은 거의 항상 오탐합니다. 부모 기준 유닛 판정(`scene_audit`)이나 최근접 거리로 검사합니다.
- 곡면 가구·프로파일 컷·다듬어진 실루엣 → 스킬 저자 스스로 "미적 완성도는 범위 밖"이라고 밝힌 영역입니다([cc-blender-skill](https://github.com/RobLe3/cc-blender-skill)). 사람이 마무리하거나 생성 경로를 섞습니다.
- 얇고 반짝이는 물체(안경테 등) → 스펙큘러 플레어가 미해결로 남은 영역입니다. 조명(탑다운 소프트박스)이나 크롭으로 우회합니다.

---

### 단계 6 — 배치 (제약 + 솔버 + 검사)

- **목적**: 가구·소품이 물리적으로 말이 되고, 동선과 초점이 있는 배치를 만듭니다.
- **누가**: 계획 모델이 관계 제약을 쓰고, **솔버와 스크립트가 좌표를 정하고**, 비평가가 4방향 렌더를 채점합니다.
- **입력**: 방 스펙(폴리곤, 문·창), 정규화된 에셋(원점 바닥 중앙, 정면 -Y, 실측 m), [치수·간격표](05_reference_dimensions.md).

**할 일**

1. **에셋 정규화**를 먼저 합니다: 원점 바닥 중앙, 정면 축 통일(-Y), 균일 스케일, 회전·스케일 적용. 정면이 불확실한 생성 에셋은 4방향 렌더를 VLM에 보여 주고 "서랍·좌석·화면이 보이는 뷰"를 고르게 합니다.
2. **금지 영역**을 먼저 깝니다: 문 앞(예: 0.9 × 0.9 m), 창 앞, 주동선 스트립(폭 0.9 m).
3. **초점과 기능 그룹**을 정합니다(TV 벽/창 전망, 대화·식사·작업 그룹). 초점이 없으면 가구가 벽을 따라 흩어진 '대기실' 배치가 됩니다.
4. **관계 제약 JSON**: 객체당 3~5개, 앵커 → 큰 가구 → 작은 가구 순서, 뒤의 객체는 앞의 것에만 의존합니다. 어휘는 7~10개로 고정하고 수치로 정의합니다(예: near 50~150 cm, far 150 cm 이상, [Holodeck prompts](https://raw.githubusercontent.com/allenai/Holodeck/main/ai2holodeck/generation/prompts.py)).
5. **솔버**로 (x, y, yaw)를 풉니다([배치 가이드](../02_guides/08_scene_layout_placement.md) 4.4절의 `grid_solver.py`).
6. `placement_utils`로 적용합니다: `snap_to_floor` → `place_against_wall` → `place_next_to` → `face_towards` → (소품) `drop_to_surface`.
7. **검사:** `scene_audit`(관통·부유), `check_clearances`(간격 규칙), 문·통로 막힘.
8. **소품 안착:** 쌓기·기대기는 rigid body로 떨어뜨려 안착시킨 뒤 변환을 굳힙니다. 소품 ACTIVE/Convex Hull, 가구·바닥 PASSIVE/Mesh, 2~5 cm 띄워 약 120프레임 진행 → `visual_transform_apply` → rigid body 제거. 1 m 이상 이동하거나 45° 이상 기울면 실패로 보고 재배치합니다(SceneSmith 기준).
9. **자연 노이즈:** 그리드 스냅 뒤 소량의 흔들림을 줍니다. SceneSmith Natural 프로파일은 가구 XY σ 0.03 m·yaw σ 1°, 소품 XY σ 0.01 m·yaw σ 3°입니다([base_furniture_agent.yaml](https://raw.githubusercontent.com/nepfaff/scenesmith/main/configurations/furniture_agent/base_furniture_agent.yaml)). 식탁 의자 몇 개를 5~10 cm 빼 두면 사용 중인 느낌이 납니다.
10. **4방향 렌더 채점:** 탑다운 정사영(좌표 읽기에 가장 좋음) + 측면들. 루브릭 6항목(Realism, Functionality, Layout, Completeness, Prompt Following, Reachability) 0~10점([critic yaml](https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/prompts/data/furniture_agent/stateful_critic_agent.yaml)).

**수치 기준 (출처별로 다를 수 있어 병기)**

| 항목 | 값 | 출처 |
|---|---|---|
| 소파–커피테이블 | 0.3~0.5 m / hinge(0.45, 0.6) | [SceneSmith designer](https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/prompts/data/furniture_agent/designer_agent.yaml) / [Infinigen home.py](https://raw.githubusercontent.com/princeton-vl/infinigen/v1.16.0/infinigen_examples/constraints/home.py) |
| 주동선 | 0.7~1.0 m | SceneSmith |
| 주요 가구 사이 | 60~90 cm, 가구 점유율 30~40% | SAGE 프롬프트 문구([planner](https://raw.githubusercontent.com/NVlabs/sage/main/server/objects/object_placement_planner.py)). 문 회전반경 90 cm도 프롬프트 문구일 뿐 솔버 수치는 아님 |
| 소파–TV장 | 2~3 m (soft cost) | Infinigen |
| 조명 사이 | ≥ 1 m (hard) | Infinigen |
| 벽 그림·거울 중심 | 1.4~1.7 m, 가구 상단 위 20~40 cm | SceneSmith |
| 관통 판정 | 1 mm | SceneSmith |

[한국] 한국 주거 프리셋(주방 상판 높이, 천장고, 식탁 뒤 여유)은 [치수표](05_reference_dimensions.md)와 [배치 가이드](../02_guides/08_scene_layout_placement.md) 6.3절을 쓰세요.

**에이전트 지시 요지**

```text
좌표를 직접 쓰지 마라. 먼저 초점 1개와 기능 그룹, 주동선을 정하고,
객체마다 관계 제약 3~5개를 relations.json으로 써라(앵커→큰 것→작은 것, 뒤는 앞에만 의존).
솔버로 푼 뒤 placement_utils로 적용하고 scene_audit와 check_clearances를 돌려라.
DONE 조건: interpenetrations == [] AND 의도하지 않은 floating == [] AND 막힌 문 없음 AND 최소 동선 ≥ 0.9 m.
하나라도 어기면 DONE을 선언하지 말고 고치거나 그 객체를 빼라.
검증 캡처: 탑다운 정사영, 눈높이 1.6 m 문 쪽, 로우앵글 0.6 m.
```

**통과 게이트**

- [ ] `interpenetrations` 0, 의도하지 않은 `floating_or_wall_mounted` 0, `below_floor` 0
- [ ] `check_clearances` 위반 0, 문·창·통로 막힘 0, 최소 동선 ≥ 0.9 m(또는 스펙 값)
- [ ] 정면 방향 검증: 정면(-Y) 벡터와 대상 방향의 내적 > 0.9
- [ ] 보이는 모든 오브젝트에 지지·부착 근거가 있다(떠 있는 쿠션, 지지 없는 조명 없음. "사용자는 1차 버그 탐지자가 아니다", [unreal-home-wizard](https://github.com/amirmushichge/unreal-home-wizard))
- [ ] 비평 6항목 모두 ≥ 9 또는 최대 라운드 도달(아래 3.3 종료 규칙)

**산출물** `spec/relations.json`, 배치된 씬 `v006.blend`, `review/v006/`(top·front·side·persp + audit.json).

**장면별 차이**

- **A 실내:** 거실 순서 예: 러그 → 소파(초점 벽 맞은편 벽에 붙임) → TV장 → 커피테이블 → 암체어 → 사이드테이블 → 플로어 램프 → 벽 그림 → 천장 조명 → 소품. 층 단위로 나누면(바닥 가구 → 벽걸이 → 천장 → 표면 위 소품) 단계마다 롤백할 수 있습니다.
- **B 제품:** 받침면·배경 소품 3~5개만. 제품이 바닥·받침에 정확히 닿는지(`drop_to_surface`)만 확인하면 됩니다.
- **C 야외:** LLM이 수천 개 좌표를 찍을 수 없습니다. Geometry Nodes **Distribute Points on Faces**(Poisson Disk, Distance Min, Density Factor)의 파라미터만 LLM이 조정하게 합니다([노드 소스](https://raw.githubusercontent.com/blender/blender/main/source/blender/nodes/geometry/nodes/node_geo_distribute_points_on_faces.cc)). 경로에서 0~1.5 m는 밀도 0, 1.5~4 m는 풀·관목, 4 m 이상은 나무처럼 거리 마스크를 쓰고, 스케일 0.8~1.2·Z 회전 랜덤, 바위는 표면 법선 정렬 + 10~20% 묻기(실무 경험치, 미검증). 히어로 클러스터는 3·5개 단위.

**흔한 실패**

- 에셋 정면 규약 불일치 → 180°·90° 오류. 연구 코드에서도 z 회전에 +π를 더하는 보정이 흔적으로 남아 있습니다. 규약은 한 곳에서만 관리합니다.
- `obj.location` 직후 `matrix_world`를 읽음 → `view_layer.update()` 전에는 갱신되지 않습니다.
- 모든 표면을 채운 "균일한 잡동사니" → 9단계의 스토리 클러스터 규칙으로 해결합니다.
- 롤백을 자동으로 기대 → SceneSmith에서도 롤백은 planner가 "강하게 고려"하는 판단 사항이지 자동이 아닙니다. 체크포인트 저장과 롤백 기준을 프롬프트에 명시합니다.

---

### 단계 7 — 재질·텍스처

- **목적**: 물리적으로 가능한 표면 값을 주고, 명도 → 색 → 변화 순서로 사실감을 쌓습니다.
- **누가**: 빌더 + 라이브러리 MCP. 대량 파라미터 수정은 대량 반복 모델에 맡길 수 있습니다.
- **입력**: 부위별로 나뉜 에셋, 스펙의 재질 의도, [physicallybased.info 값](https://raw.githubusercontent.com/AntonPalmqvist/physically-based-api/main/deploy/v2/materials.json)(CC0).

**할 일**

1. **생성보다 선택:** 부위를 분류(면 노멀·높이 비율 또는 VLM 렌더 분석)하고, 부위별로 검증된 라이브러리 재질을 찾아 할당합니다. 없을 때만 절차적 레시피나 AI 텍스처를 씁니다([NVIDIA Material Agent](https://github.com/NVIDIA-Omniverse/usd-content-agents)도 이 방식).
2. **PBR 규칙:** Metallic은 0 또는 1(전환부 마스크만 중간값), 유전체 albedo는 sRGB 약 30~240(scenario 감사 30~243), 금속 base color는 밝게, Roughness는 정확히 0 금지(최소 0.01~0.05), Specular IOR Level 0.5(= IOR 1.5)가 기본. 색 텍스처만 sRGB, 나머지 맵은 Non-Color.
3. **명도 먼저:** 그레이스케일 렌더에서도 재질끼리 구분되게 명도를 먼저 잡고, 색은 나중에 줍니다.
4. **roughness에 공간 변화**를 줍니다(맵 표준편차 > 0.01, scenario 게이트). 균일한 roughness는 CG의 가장 큰 티입니다.
5. **Poly Haven:** 노드를 손으로 짜지 말고 `set_texture`를 쓰고, 1k~2k로 받고 히어로만 4k. 텍스처 실측 크기로 Mapping Scale을 맞춥니다(바닥 6 m, 텍스처 2 m면 3). 다운로드는 메인 스레드라 Blender가 멈춥니다.
6. **재질 코드는 멱등:** `nodes.clear()` 후 Output 1개 + Principled 1개를 새로 만듭니다. 중복 노드로 뷰포트는 맞는데 렌더가 회색이 된 사례가 있습니다([#190](https://github.com/ahujasid/blender-mcp/issues/190)).
7. **API 함정:** Principled v2 소켓 이름(`Specular IOR Level`, `Coat Weight`, `Transmission Weight`, `Subsurface Weight`, `Emission Color`), 비활성 소켓은 문자열 키로 접근 불가, Musgrave 노드는 4.1에서 제거(Noise fBM 사용), 5.0부터 `Material.use_nodes` 폐기 예고. 모르면 `describe_node_type`으로 먼저 조회합니다.
8. **AI 텍스처:** 이미지 모델에 노멀·roughness 맵을 "그려 달라"고 하지 않습니다. albedo만 생성하고 데이터 맵은 전용 추정기나 height 베이크로 만듭니다. Meshy retexture는 `enable_pbr=true`(기본 false), `remove_lighting=true`, `enable_original_uv=true`를 명시하고, 4k/8k를 지정해도 PBR 맵은 2K로 남는다는 점을 기억하세요([postprocessing.ts](https://raw.githubusercontent.com/meshy-dev/meshy-mcp-server/main/src/schemas/postprocessing.ts)).
9. **UV와 텍셀 밀도:** 하드서페이스는 Smart UV(`angle_limit`은 **라디안**, 66°), 유기체·생성 메시는 SLIM이나 PartUV. 게임용이면 씬 전체 텍셀 밀도를 통일합니다(콘솔·PC 10.24~20.48 px/cm, 커뮤니티 문서 값, [Texel Density Checker](https://github.com/mrven/Blender-Texel-Density-Checker)).
10. 후보를 2~3개 만들어 같은 조명에서 렌더하고 레퍼런스와 가장 가까운 것을 고르게 합니다(생성 + 시각 평가 반복이 한 번 생성보다 잘 수렴, [BlenderAlchemy](https://github.com/ianhuang0630/BlenderAlchemyOfficial)).

**에이전트 지시 요지**

```text
모든 재질은 Principled BSDF 하나. Metallic ∈ {0,1}. Base Color는 physicallybased.info 값 우선.
Roughness는 0 금지, 맵이나 노이즈로 변화를 줘라. 색 텍스처만 sRGB, 나머지는 Non-Color.
노드는 이름이 아니라 type으로 찾고, 소켓 이름이 불확실하면 describe_node_type으로 먼저 조회해라.
재질을 다시 만들 때는 nodes.clear() 후 새로 구성해라.
끝나면 재질별 Base Color / Metallic / Roughness 표와 규칙 위반 여부, 텍스처 출처·라이선스를 보고해라.
```

**통과 게이트**

- [ ] PBR 감사(`pbr_audit`, [재질 가이드](../02_guides/05_texturing_materials.md) 4.7절) 위반 0
- [ ] 그레이스케일 렌더에서 재질끼리 명도가 구분된다
- [ ] roughness 변화(표준편차 > 0.01), 카메라 거리에서 타일링 반복이 안 보인다
- [ ] AI 텍스처 albedo에 구워진 그림자·하이라이트가 없다
- [ ] Cycles 전용 마스크를 쓴 경우 Cycles 렌더로 확인했다(아래 흔한 실패 참고)
- [ ] 텍스처마다 출처·라이선스가 `asset_manifest`에 있다

**산출물** 재질 세트(`M_Wood_Oak` 식 이름), 텍스처 폴더, 재질 보고 표, `v007.blend`.

**장면별 차이**

- **A 실내:** 바닥·벽·패브릭은 라이브러리 스캔 재질, 목재 가구는 결 방향 스트레치가 있는 나무 레시피([재질 가이드](../02_guides/05_texturing_materials.md) 4.4절). 같은 의자 10개가 완전히 같은 색이면 즉시 CG처럼 보이니 Object Info Random으로 개체별 변화를 줍니다.
- **B 제품:** 색 재현이 중요하므로 3단계에서 Khronos PBR Neutral을 골랐다면 유지합니다. 게임 에셋이면 이 단계에서 베이크까지 계획합니다.
- **C 야외:** 지형은 triplanar나 여러 재질 블렌딩으로 타일링을 숨기고, displacement는 16-bit 소스와 약한 강도로 씁니다.

**흔한 실패**

- EEVEE 뷰포트로 웨더링 확인 → Pointiness는 EEVEE에서 상수 0.5, Bevel 노드는 노멀을 그대로 통과시킵니다([GPU 셰이더 소스](https://raw.githubusercontent.com/blender/blender/main/source/blender/gpu/shaders/material/gpu_shader_material_geometry.bsl.hh)). 에이전트가 "마모가 안 보인다"며 값을 과하게 올립니다. AO 노드는 EEVEE에서도 동작하지만 화면 공간 방식이라 결과가 다릅니다.
- 구버전 MCP로 Poly Haven 적용 → 2026-09-21 이전에는 normal·displacement가 연결되지 않거나 타일링이 뒤집힌 경로가 있었습니다(2 m 텍스처가 4 m 면에서 1.993회 대신 0.509회 반복, [PR #367](https://github.com/ahujasid/blender-mcp/pull/367)).
- Infinigen 레시피를 그대로 복사 → 연구용 랜덤화로 metallic 0.37 같은 비물리 값이 섞여 있습니다. 0/1 마스크로 재구성합니다.

---

### 단계 8 — 라이트 v2

- **목적**: 색온도·광량비·그림자 모양으로 분위기와 형태를 완성합니다.
- **누가**: 빌더 + 비평가 + 수치 게이트.
- **입력**: 재질이 입혀진 씬, 조명 v1, 레퍼런스의 그림자 밀도.

**할 일**

1. **켈빈으로 색 지정:** `light.use_temperature = True`로 켜면 `color`가 곱셈 틴트로 바뀌므로 color를 흰색(1,1,1)으로 되돌립니다(검증 결과). 기준값: 촛불 약 1500~1850K, 백열 2000~2500K, 실용광 기본 2700K, 텅스텐 3200K, 주광 5500~6500K. 네온·SF 광원만 RGB로 줍니다.
2. **광량비는 "기본값 + 레퍼런스로 조정":** key:fill 3~4:1로 시작해 레퍼런스 사진의 그림자 밀도에 맞춥니다. 재질별 시작값(커뮤니티 스킬): 금속 4:1:2, 유리 3:1:1.2, 나무 4:1:1.5, 패브릭 3:1:0.5, 피부 4:1:1, 제품 5:1:1.5(key:fill:rim, [RobLe3 lighting](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-lighting/SKILL.md)). 고정 비율 자체를 부정하는 실무자 견해도 있으니 레퍼런스가 우선입니다.
3. **실용광 장면:** World 0.10~0.20, 작은 메시 전구 emission 800~3000, max bounces 16 이상(같은 스킬 값).
4. **빛에 사연 주기:** 창살·나뭇잎 그림자(고보), 부분적으로 가려진 빛. 빛줄기는 World Volume이 아니라 볼륨 재질 큐브로, 밀도는 아주 낮게 둡니다.
5. **Light Group(Cycles 전용)** 으로 역할별(key, fill, rim, window) 패스를 나눠 한 번 렌더한 뒤 합성에서 비율을 조정합니다. EEVEE는 Light Linking(Object > Shading > Light Linking, 오브젝트 속성)으로 대체합니다([properties_object.py v5.2.2](https://raw.githubusercontent.com/blender/blender/v5.2.2/scripts/startup/bl_ui/properties_object.py)).
6. 한 번에 한 변수만 바꾸고 태그를 올려 이전 버전과 나란히 비교합니다.

**에이전트 지시 요지**

```text
광원마다 존재 이유(켈빈·크기·거리)를 한 줄로 적어라. RGB 추측 금지, use_temperature 후 color는 흰색.
key:fill은 3~4:1로 시작해 레퍼런스 그림자 밀도에 맞춰라. 밝기는 exposure로만.
Cycles면 Light Group을 역할별로 나눠라. 한 번에 한 변수만 바꾸고 v###를 올려 이전과 나란히 보여 줘라.
```

**통과 게이트**

- [ ] 모든 광원에 존재 이유가 있고 크기 > 0
- [ ] 수치 게이트 재통과: 클리핑 ≤ 0.5%, value range ≥ 0.30, 키 각도 ≥ 20°, 실내 World 기여 < 10%
- [ ] 비평가가 조명 항목에서 Blocker/Major 없음
- [ ] v1 대비 A/B 비교 이미지가 있다

**산출물** 조명 v2, Light Group 설정, `review/v008/`.

**장면별 차이**

- **A 실내:** 따뜻한 실용광(2700K)과 차가운 하늘 필의 대비. 창 쪽은 Light Portal이나 Path Guiding(CPU)을 검토합니다. Unreal로 갈 경우 실용광이 많으면 MegaLights(5.7 Beta, [문서 미러](https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/megalights-in-unreal-engine.md))를 씁니다.
- **B 제품:** 재질별 비율표를 시작값으로, 얇은 금속 하이라이트는 탑다운 소프트박스로 다룹니다.
- **C 야외:** 골든아워 태양(낮은 고도, 따뜻한 색온도) + 하늘 필, 대기 원근감은 Mist 패스나 낮은 밀도 볼륨.

**흔한 실패**

- 필을 쌓아 그림자를 없앰 → 초보의 대표적인 티입니다. 그림자는 없애는 것이 아니라 모양을 잡는 대상입니다.
- 램프 세기를 하나씩 스케일해 밝기 조절 → 비율이 깨집니다. exposure를 쓰세요.

---

### 단계 9 — 디테일·스토리텔링·마모

- **목적**: "사람이 사는 흔적"과 불완전성을 논리적인 위치에만 더합니다.
- **누가**: 빌더 + 비평가. 미감 판단은 사람이 합니다.
- **입력**: 조명까지 끝난 씬, 레퍼런스의 복제할 특징 목록.

**할 일**

1. **Attention budget:** 디테일은 시선이 머무는 곳에만. 히어로 존은 "의도는 높게, 잡음은 낮게", 배경은 실루엣만 남깁니다.
2. **스토리 비트:** 비트(먹다 만 식사, 쓰던 작업대 등)마다 소품 3~7개와 마모·데칼 단서 1~2개, 그리고 멈출 줄 압니다([arjun988 set-dressing](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/set-dressing/SKILL.md), 근거 데이터 없는 체크리스트 수준).
3. **반복 인스턴스 변주:** 회전 ±3~8°, 스케일 ±5% 정도의 지터(6단계 자연 노이즈와 같은 원리).
4. **웨더링은 물리적 원인에 맞는 채널로, 레이어 하나에 결함 하나:** 긁힘은 Normal/Bump, 지문·기름은 Roughness만, 먼지는 월드 노멀 Z 마스크, 틈새 때는 AO 기반. 위치는 "왜 거기가 닳았나"를 따라야 합니다.
5. **4단 구성:** 베이스 + 개체별 변화 + 마모 + 오염.
6. 드레싱 뒤 `scene_audit`와 `check_clearances`를 다시 돌립니다(소품이 표면을 관통하거나 동선을 막지 않았는지).

**에이전트 지시 요지**

```text
히어로 존에 스토리 비트 2개를 정하고 비트마다 소품 3~7개, 마모·데칼 1~2개만 추가해라.
모든 표면을 채우지 마라. 배경은 실루엣만.
마모는 물리적 원인을 한 줄로 적고 맞는 채널(normal/roughness/color)에 넣어라.
드레싱 후 scene_audit와 check_clearances를 다시 돌려 0건인지 보고해라.
```

**통과 게이트**

- [ ] 히어로가 여전히 한눈에 읽힌다(squint, 그레이스케일)
- [ ] 균일하게 깔린 잡동사니가 없고, 동선·문이 막히지 않았다
- [ ] `scene_audit` 재통과(소품 관통·부유 0)
- [ ] 마모 위치마다 원인이 설명된다
- [ ] 완벽하게 같은 방향·간격으로 정렬된 반복 소품이 없다

**산출물** 드레싱된 씬 `v009.blend`, 스토리 비트 목록, `review/v009/`.

**장면별 차이**

- **A 실내:** 쿠션·담요·책·컵처럼 생활 흔적. 벽걸이는 `floating_or_wall_mounted`로 표시되니 의도한 것인지 확인합니다.
- **B 제품:** 모서리 마모, 손이 닿는 부위의 광택 변화, 지문은 클로즈업일 때만.
- **C 야외:** 쓰러진 나무·표지판·발자국 같은 흔적 클러스터를 3분할 교차점에. 바위는 이끼·먼지를 월드 노멀 기준으로.

**흔한 실패**

- 모든 곳에 균일한 디테일 → 모델이 버티지 못할 정밀 검사를 부르고 토큰·시간을 낭비합니다.
- 지문을 bump로 넣는 식의 채널 착오 → 오히려 가짜처럼 보입니다.

---

### 단계 10 — 최종 렌더·합성

- **목적**: 깨끗하게 렌더한 뒤, 합성은 절제해서 "사진을 재구성"합니다.
- **누가**: headless 렌더 + 비평가(SHIP 판정) + 사람(G3).
- **입력**: 완성 씬, `CAM_Hero`, 품질 프로필.

**할 일**

1. **Cycles 기본값을 먼저 이해:** Blender 5.2.2 기준 samples 4096, adaptive threshold 0.01, max bounces 12(diffuse 4, glossy 4, transmission 12, volume 0, transparent 8), clamp indirect 10, OIDN + Albedo/Normal 패스([properties.py v5.2.2](https://raw.githubusercontent.com/blender/blender/v5.2.2/intern/cycles/blender/addon/properties.py)).
2. **장면별 조정:** 유리가 많으면 transmission 16 이상, 울퉁불퉁한 유리는 glossy 20~40, 유색 액체는 volume 약 12, 겹친 알파 잎은 transparent를 크게. 파이어플라이는 clamp indirect를 낮추거나 Filter Glossy로 잡습니다(스킬 권고값).
3. **출력:** OpenEXR Multilayer(Half Float, DWAA)를 마스터로. PNG에는 뷰 변환이 구워집니다.
4. **EEVEE 최종이라면:** 엔진 식별자는 5.x에서 `BLENDER_EEVEE`(4.2~4.5는 `BLENDER_EEVEE_NEXT`), `use_bloom`·`use_ssr`·`use_gtao`는 없습니다. 레이트레이싱 켜기(팩토리 씬은 꺼짐), 해상도 1:1, Fast GI step 16 등으로 설정하고 같은 장면의 Cycles 레퍼런스와 약 30% 이내인지 비교합니다(scenario 기준).
5. **합성 순서(커뮤니티 권고, 미검증):** 디노이즈 → (AO) → 색 보정(CDL) → Glare → 약한 렌즈 효과 → 비네트 → 그레인 마지막. 렌더 노이즈를 그레인 대용으로 쓰지 않습니다.
6. **Glare 노드는 5.x 소켓 방식:** Strength·Size 0~1(Size 기본 0.5), Iterations 2~5, Streaks 1~16, Fade 0.75~1, 기본 Type은 **Streaks**(Bloom 아님)입니다. 구버전 자료의 "Size 8~9, mix -0.7" 같은 값은 입력할 수 없습니다([node_composite_glare.cc v5.2.2](https://raw.githubusercontent.com/blender/blender/v5.2.2/source/blender/nodes/composite/nodes/node_composite_glare.cc)). 효과를 분명히 보이게 올렸다가 의식되지 않을 때까지 내립니다.
7. **최종 렌더는 headless로:** `blender -b scene.blend --python render_final.py`. MCP 호출로 긴 렌더를 돌리면 소켓 타임아웃(커뮤니티 서버 180초)이나 유휴 타임아웃(stdio 30분·HTTP 서버 5분)에 걸릴 수 있습니다.
8. **렌더를 직접 보고 판정:** 뷰포트 스크린샷은 최종 판단 근거가 아닙니다. *"렌더를 직접 보지 않고는 완료를 보고하지 말라"*([scenario expert](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/dcc/blender/scenario-blender-expert/SKILL.md)).
9. **비평가 판정:** CG 티 체크리스트(Standard 뷰 변환, 기본 50 mm, 크기 0 광원, 정면 조명, 날카로운 90° 모서리, 균일 roughness·순수 흑백·원색, 보이는 타일링, 축 정렬 등간격 배치, 틀린 스케일, 과한 CA·글로우, 구워진 조명, 먼지·마모 부재. [조명 가이드](../02_guides/06_lighting_rendering_art_direction.md) 7절)를 항목별로 "통과/문제(근거 뷰)"로 답하게 하고, Blocker/Major/Minor/Note로 분류해 SHIP / SHIP WITH NOTES / NO-SHIP으로 결론 냅니다([arjun988 qa-review](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/qa-review/SKILL.md)).

**에이전트 지시 요지**

```text
render_final.py를 headless로 실행해 EXR 마스터와 PNG를 만들어라(샘플은 프로필 값, adaptive 0.01, OIDN).
렌더 이미지를 직접 열어 보고, 수치 게이트와 CG 티 체크리스트를 항목별로 판정해라.
합성은 효과를 끈 버전과 A/B로 보여 줘라. "좋아졌는데 무엇을 했는지 안 보임"이 목표다.
blender-critic의 SHIP 판정과 내 승인 전에는 다음 단계로 가지 마라.
```

**통과 게이트 (G3)**

- [ ] 최종 렌더 파일을 직접 열어 확인했다(뷰포트 아님)
- [ ] 수치 게이트(클리핑, value range, 순흑·순백·채도 100% 픽셀 ≈ 0) 통과
- [ ] 비평가 SHIP(제안 기준: 항목 평균 ≥ 8, 최저 ≥ 7. 공개 사례 최고점이 6~7.5였다는 점을 감안해 프로젝트별로 조정)
- [ ] 합성 A/B에서 과한 효과가 없다
- [ ] **사람이 OK**

**산출물** `render/final_v###.exr`, 최종 PNG/JPG, 판정 보고서, `v010.blend`.

**장면별 차이**

- **A 실내:** 노이즈가 많은 간접광 장면이라 샘플을 넉넉히, 창은 클리핑 허용 여부를 의도적으로 정합니다.
- **B 제품:** 흰 배경 제품샷이면 순백 배경은 "의도한 클리핑"으로 게이트에서 제외합니다. 턴테이블이 필요하면 카메라 레시피를 고정합니다.
- **C 야외:** 식생 알파 때문에 transparent bounces를 늘리고, 대기 원근과 전경 프레이밍 잎을 확인합니다.

**흔한 실패**

- 레거시 EEVEE 속성을 쓰는 커뮤니티 스킬 코드 → 5.x에서는 AttributeError입니다(RobLe3·arjun988의 렌더 스킬에 남아 있음).
- 합성으로 결함을 덮음 → 결함은 앞 단계에서 고칩니다.

---

### 단계 11 — 익스포트·검증·provenance

- **목적**: 다른 도구·엔진에서 그대로 열리는 파일과, 나중에 권리를 증명할 기록을 남깁니다.
- **누가**: 빌더 + 검증 스크립트 + 사람(G4).
- **입력**: 최종 씬, `asset_manifest.csv`, 대상 엔진·포맷.

**할 일**

1. **익스포트 전 8항목**([blender-kiln](https://raw.githubusercontent.com/elithril/blender-kiln/main/SKILL.md)): ① 모든 재질이 Principled BSDF(절차 노드는 베이크) ② Base Color/Normal/Roughness/Metallic 텍스처 임베드 ③ UV 겹침·늘어짐 ④ 모든 transform 적용 ⑤ merge by distance 0.0001 m ⑥ 노멀 재계산 ⑦ 고아 데이터 정리(`orphans_purge` 대신 명시적 삭제) ⑧ 임시 GLB 크기 확인(웹 기준 50MB 이상 경고).
2. **glTF 규칙:** metallic은 B, roughness는 G 채널(같은 이미지), AO는 `glTF Material Output` 이름의 커스텀 노드 그룹의 Occlusion 입력으로만 나갑니다. Normal Map은 Tangent Space만([glTF-Blender-IO 문서](https://raw.githubusercontent.com/KhronosGroup/glTF-Blender-IO/main/docs/blender_docs/scene_gltf2.rst)). Displacement·SSS·절차 노드는 조용히 사라지므로 노멀·컬러로 베이크합니다. 베이크는 활성 이미지 노드가 없는 재질 슬롯을 오류 없이 **건너뛰기** 때문에 일부만 구워질 수 있습니다.
3. **최적화:** `gltf-transform optimize`는 simplify 단계가 형상을 망가뜨리므로 쓰지 않고, dedup → weld → 텍스처 리사이즈·압축 → Draco를 따로 실행합니다. LOD는 gltfpack으로 따로([에셋 가이드](../02_guides/10_assets_pipeline_licensing.md) 2.5절).
4. **FBX 스케일:** 100배 스케일 오류가 서로 무관한 사례에서 반복됐습니다(Unity에 2 m 로봇이 200 m로 들어옴). Blender FBX 익스포트에서 `apply_scale_options='FBX_SCALE_UNITS'`를 지정하고, 크기를 아는 픽스처로 먼저 시험합니다([Robo Open](https://github.com/az9713/gpt-6-astra-tennis-game)).
5. **재임포트 검증:** 내보낸 파일을 새 씬에 다시 불러와 `scene_audit`(치수가 원본과 같은지)와 `review_views`를 돌립니다. glTF 검증기로 오류 0을 확인하고([에셋 가이드](../02_guides/10_assets_pipeline_licensing.md) 2.6절), 만든 맵과 GLB에 실제로 채워진 슬롯을 비교합니다.
6. **Provenance:** 에셋마다 출처 유형(라이브러리/생성/직접), 생성기와 버전, 플랜, 입력 이미지 해시, 파라미터, 컴포넌트별 라이선스(배경 제거기·텍스트→이미지 모델까지), 사람이 편집한 내용, 표기 문구를 남깁니다. 커스텀 프로퍼티 → `credits.csv` → GLB extras 코드는 [에셋 가이드](../02_guides/10_assets_pipeline_licensing.md) 5.4절에 있습니다.
7. **승인을 파일 해시에 묶습니다.** 파일이 바뀌면 승인도 무효입니다([blender-art-factory](https://github.com/ErikBurdett/blender-art-factory)).

**에이전트 지시 요지**

```text
익스포트 전 8항목을 하나씩 확인하고 결과를 표로 보여 줘라. 절차 노드·displacement는 먼저 베이크해라.
GLB를 내보낸 뒤 새 씬에 재임포트해 scene_audit 치수를 원본과 비교하고, 검증기 종료 코드가 0이 될 때까지 고쳐라.
만든 맵 목록과 GLB에 채워진 슬롯을 비교해라.
asset_manifest를 기준으로 provenance와 credits.csv를 만들고, 파일 해시와 함께 내 SHIP 승인을 요청해라.
```

**통과 게이트 (G4)**

- [ ] 8항목 통과, glTF 검증기 오류 0
- [ ] 재임포트 후 치수·부품 수·재질 슬롯이 원본과 같다
- [ ] 대상 엔진 임포트 테스트(스케일·축·재질 연결)
- [ ] 모든 에셋에 provenance와 라이선스, 필요한 표기가 있다
- [ ] [한국] 쓸 수 없는 모델의 출력물이 섞이지 않았다
- [ ] **사람이 SHIP** (파일 해시 기록)

**산출물** `export/*.glb|fbx`, `provenance/assets.csv`, `credits.csv`, 검증 로그, 승인 기록.

**장면별 차이**

- **A 실내:** 씬 전체 대신 가구별 GLB + 배치 매니페스트로 나누면 재사용이 쉽습니다.
- **B 제품:** LOD(50%/25%)와 콜리전을 함께. 게임 엔진 규칙(삼각형 상한, 전방축, 콜리전)을 프롬프트에 숫자로 넣습니다.
- **C 야외:** 반복 에셋은 에셋 ID별 인스턴스(Unreal이면 HISM)로, 고유 오브젝트만 개별 액터로 내보냅니다([astra-blender-forest](https://github.com/octopus7/astra-blender-forest)).

**흔한 실패**

- Poly Haven 재질의 일부 맵만 GLB에 남음 → blender-kiln 측정에서 7개 맵 중 3개만 남은 사례(PR #367 이전 동작 기준)가 있습니다. 만든 맵 대 채워진 슬롯 감사를 자동화하세요.
- 에셋 라이선스를 나중에 추적 → 생성 시점의 플랜·버전을 모르면 상업권을 증명할 수 없습니다.

---

## 3. 단계 안에서 도는 루프

### 3.1 루프 한 바퀴

1. **상태 확인:** 씬 요약(`scene_audit` JSON이나 압축 씬 요약)과 `PROGRESS.md`를 읽습니다.
2. **작은 코드:** 호출 하나에 부품 하나나 단계 하나. `execute_blender_code`는 호출마다 새 네임스페이스라 Python 변수가 남지 않으니, 이름으로 가져오거나 만들고(get-or-create), 모듈을 다시 import하고, 마지막 줄에 한 줄 요약을 print합니다([RobLe3 text-to-blender](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/text-to-blender/SKILL.md)). `exec()`에는 타임아웃이 없으므로 큰 루프는 Blender를 멈춥니다.
3. **저장:** `bpy.ops.wm.save_mainfile(incremental=True)` 또는 `save_as_mainfile(copy=True)`로 버전을 남깁니다(둘 다 Blender 5.0.1에 있고 MCP for Blender의 SAFE_MODE 검사를 통과함, 검증 결과).
4. **숫자 검사:** `scene_audit`(유닛 단위), `check_assembly()`(부품 단위), `check_clearances`, PBR 감사, 수치 게이트.
5. **눈 검사:** 피사체를 프레이밍하고 Material Preview(또는 실제 렌더)로 여러 각도를 봅니다. 배치·비율은 `review_views`, 조명·재질은 `review_render`.
6. **비평:** 비평가가 스펙 대비 차이를 "부품 / 기대값 / 관찰값 / 수정안" 표로 최대 3줄 씁니다.
7. **수정:** 결함 원장의 가장 큰 결함 하나만 고치고 1로 돌아갑니다.

GUI(MCP)에서 Material Preview로 바꾸는 코드(RobLe3 기반):

```python
import bpy
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for s in area.spaces:
            if s.type == 'VIEW_3D':
                s.shading.type = 'MATERIAL'
                s.shading.use_scene_lights = True
                s.shading.use_scene_world = True
```

Solid 모드에서는 재질 색이 보이지 않아 검증이 무의미해집니다. 프레이밍하지 않은 뷰에서는 소품이 몇 픽셀로 찍힙니다(kiln Rule 22).

### 3.2 비평가 설정

- 빌더와 **다른 컨텍스트**에서 돌리고, 도구는 읽기 전용(스크린샷·씬 정보·파일 읽기)만 줍니다([subagents](https://code.claude.com/docs/en/sub-agents)). *"빌더는 자기 작업을 채점하지 않는다"*는 원칙으로 리뷰어 9명을 둔 사례는 벽 와인딩 반전, 미러링된 도로 마킹, 떠 있는 옥상 박스, 환경맵 이중 계산으로 인한 과노출을 잡았습니다([fable51-worlds](https://github.com/PhiloLabs/fable51-worlds)).
- 생성기와 검증기를 분리하고 검증에 연산을 더 쓰면 성능이 오른다는 것이 벤치마크의 교훈입니다([BlenderGym](https://github.com/richard-guyunqi/BlenderGym-Open)).
- 리뷰어는 문제를 과잉 보고하는 경향이 있으니 "스펙이나 품질에 영향이 없는 취향 문제는 적지 말라"고 지시합니다([best-practices](https://code.claude.com/docs/en/best-practices)).

```text
# .claude/agents/blender-critic.md 요지 (전체는 templates/skills 참고)
너는 이 씬을 만들지 않은 시니어 아트 디렉터다. spec_sheet와 acceptance.yaml, 레퍼런스를 기준으로
3/4 히어로·정면 오쏘·측면 오쏘·탑다운을 본다. 실루엣·스케일·비율·떠 있음·관통·셰이딩·재질 사실감·조명·구도를
1~10점으로 매기고, 문제마다 근거가 되는 뷰를 적는다. Blocker/Major/Minor로 분류하고 수치가 들어간 수정안은 최대 3개.
판정은 SHIP / SHIP WITH NOTES / NO-SHIP.
```

### 3.3 결함 원장과 종료·롤백 규칙

결함 원장(blender-production 방식)은 한 줄에 하나씩 적습니다.

| # | 뷰 | 결함 | 증거 | 추정 원인 | 변경 | 검증 |
|---|---|---|---|---|---|---|
| 1 | side | 등받이가 좌면 뒤에서 12 mm 떨어져 있음 | `check_assembly`: chair_back–chair_seat 틈(GAP) 0.012 m | location.y 계산 오류 | y = 좌면 뒤 모서리 | 재검사 0건, 같은 카메라 재렌더 |

종료·롤백 규칙(SceneSmith 설정을 바탕으로 한 제안):

| 규칙 | 값 |
|---|---|
| 조기 종료 | 모든 채점 항목 ≥ 9 |
| 최대 라운드 | 프로필별(fast 1, standard 2, cinematic 4). SceneSmith 가구 단계는 3, 소품 단계는 2 |
| 반복 실패 | 같은 문제가 2회 이상 반복되면 중단하고 사람에게 보고 |
| 롤백 | 한 항목이 2점 이상 또는 총점이 1점 이상 떨어지면 직전 버전으로 되돌리기를 **검토**(자동 아님) |
| 물리 충돌 | 관통 보고가 비어 있지 않으면 Realism 점수 최대 4 |

`/goal`을 쓸 때는 평가자가 파일을 읽지 않고 대화만 본다는 점을 기억하세요. 이미지를 봤다는 사실보다 수치와 판정을 텍스트로 출력하게 해야 합니다([/goal 문서](https://code.claude.com/docs/en/goal), 조건 최대 4,000자).

### 3.4 컨텍스트·비용 위생

- **스크린샷 크기:** MCP for Blender의 `get_viewport_screenshot` 기본 `max_size`는 1000입니다(16:9면 약 1000×563, Claude 이미지 약 756토큰). 1920×1080은 Opus 5.5 high-res tier에서 2,691토큰입니다([vision 문서](https://platform.claude.com/docs/en/build-with-claude/vision)). 검토용은 긴 변 약 1000px이면 충분하고, 최종 판정에만 큰 렌더를 씁니다.
- **이미지 20개 규칙:** 한 요청에 이미지가 20개를 넘으면(이전 턴과 tool_result 속 스크린샷 포함) 이미지당 치수 제한이 더 엄격해집니다. 각 변을 2000px 이하로 줄이세요.
- **MCP 출력:** Claude Code의 `MAX_MCP_OUTPUT_TOKENS` 기본값은 25,000이고 10,000을 넘으면 경고합니다([MCP 문서](https://code.claude.com/docs/en/mcp)). 큰 씬 정보는 요약 JSON으로 받습니다.
- **같은 문제로 두 번 교정했다면** 컨텍스트가 실패한 시도로 오염된 상태입니다. `PROGRESS.md`(스펙, 현재 단계, 최신 버전 파일, 미해결 결함)를 남기고 `/clear` 후 "PROGRESS.md를 읽고 단계 N부터 재개"로 시작합니다.
- **배칭:** 같은 변환 50개를 개별 호출하면 1,949토큰, 배치 한 번이면 1,018토큰이었습니다(페이로드만 측정, 전체 비용이 그만큼 줄지는 않음, [blender-astra-mcp](https://github.com/mohakmalviya/blender-astra-mcp)).
- **세션 비용 감(가정 기반 추정):** 툴 호출 60회, 평균 컨텍스트 80k 가정에서 Sonnet 5 약 $2.5, Opus 5.5 약 $4.0, Fable 5.1 약 $8.7([pricing](https://platform.claude.com/docs/en/about-claude/pricing) 단가 기준 계산).

### 3.5 안전장치

| 위험 | 대응 |
|---|---|
| `execute_blender_code`는 임의 Python을 타임아웃 없이 실행 | 작업 전 저장·git 커밋. MCP for Blender README도 *"ALWAYS save your work"*를 경고합니다([README](https://github.com/ahujasid/blender-mcp)) |
| `BLENDER_MCP_SAFE_MODE=1`을 샌드박스로 오해 | 직접 파일 I/O(`open`, `os`), 프로세스, 네트워크, 핸들러·타이머·드라이버, 외부 `.blend` append/link를 막지만 **bpy를 통한 저장·열기·import/export·렌더는 허용**합니다. 검사는 MCP 경로에만 걸리고 애드온 소켓은 로컬 프로세스의 raw 코드를 받으므로 샌드박스가 아닙니다 |
| 텔레메트리 | 익명 사용 기록은 **기본 수집**, 콘텐츠(프롬프트·코드·스크린샷)는 opt-in이며 AI 학습에 쓰일 수 있다고 적혀 있습니다. 끄려면 `DISABLE_TELEMETRY=true` |
| 파괴적 코드 | `orphans_purge`, 공장 초기화, 새 파일 열기 금지. 내가 만들지 않은 오브젝트 수정 금지. Claude Code Hooks의 PreToolUse(`mcp__blender__execute_blender_code` matcher, exit 2로 차단)로 강제할 수 있습니다([hooks](https://code.claude.com/docs/en/hooks)) |
| 권한 우회 | `--dangerously-skip-permissions`를 쓰지 않습니다. Epic도 "Localhost is not a trust boundary"라고 경고합니다 |
| 포트 충돌 | 공식 Blender 커넥터·MCP for Blender·Scenario 플러그인이 모두 9876을 씁니다. 하나만 켭니다 |

---

## 4. Unreal Engine으로 마무리할 때의 차이

Blender에서 형태·배치를 끝내고 UE 5.8에서 조명·렌더를 마무리하는 경우입니다. UE 문서는 비공식 미러로 확인한 내용입니다.

| 단계 | UE에서 달라지는 점 |
|---|---|
| 준비 | 공식 Unreal MCP는 실험 기능이고 ModelContextProtocol + AllToolsets(도구가 보이려면 필요) 플러그인을 켜야 합니다. Epic 플러그인: `/plugin install unreal-engine-skills-for-claude-code@claude-plugins-official`, 에디터에서 `ModelContextProtocol.StartServer`, `ModelContextProtocol.GenerateClientConfig ClaudeCode`. 기본 포트 8000이 다른 앱과 충돌해 8123으로 바꾼 사례가 있습니다([per-simmons](https://raw.githubusercontent.com/per-simmons/unreal-agent-harness/master/AGENTIC-GAMEDEV-GUIDE.md), 원문 "cost an hour") |
| 루프 | 대량 변경 전후로 저장(MCP 편집이 항상 undo되지는 않음), 같은 에셋에 대한 의존 호출은 직렬화, 결과는 읽기 전용 호출로 재확인(예외 없이 status만 돌려주는 도구가 많음), PIE 중인지 확인([Epic unreal-mcp SKILL](https://raw.githubusercontent.com/EpicGames/unreal-engine-skills-for-claude-code-plugin/main/skills/unreal-mcp/SKILL.md)). `CaptureViewport`의 base64 PNG는 파일로 빼서 작은 PNG로 디코드합니다 |
| 1 블록아웃 | 벽·바닥·천장은 분리된 모듈 메시, 벽 두께 10 cm 이상(누광 방지, Software RT 문맥의 권고) |
| 3·8 조명 | Lumen은 Static만 미지원이고 Stationary도 반영됩니다(커뮤니티 스킬의 "Movable만 반영"은 틀림, [Lumen GI 문서 미러](https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine.md)). 작은 발광체는 Emissive Light Source. 로컬 라이트 Source Radius 기본 0 → 칼 그림자이니 실제 크기로. 실용광이 많으면 MegaLights. 거울·크롬끼리 비치는 장면은 Lumen 반사 바운스(기본 1)를 올립니다(HWRT Hit Lighting 필요) |
| 7 재질 | Substrate는 5.7부터 새 프로젝트 기본이지만 기본 GBuffer가 Blendable이라 다층 재질이 단순화됩니다. AAA 다층 재질이면 Adaptive로([Substrate 문서 미러](https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/overview-of-substrate-materials-in-unreal-engine.md)) |
| 10 렌더 | Path Tracer + Movie Render Queue. Spatial × Temporal 샘플의 **곱**이 8을 넘으면 AA를 None으로 하거나 `r.TemporalAASamples`를 맞춥니다([품질 설정 미러](https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/cinematic-rendering-image-quality-settings-in-unreal-engine.md)). diffuse Base Color는 0.8 미만으로([Path Tracer 미러](https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/path-tracer-in-unreal-engine.md)) |
| 11 익스포트 | `StaticMeshTools.import_file`은 FBX/OBJ만 받고 GLB는 안 된다는 기록이 있습니다. 787 메시가 100배로 들어온 사례는 `RelativeScale3D=0.01`로 보정했습니다([BUILD-LOG](https://raw.githubusercontent.com/per-simmons/unreal-agent-harness/master/BUILD-LOG.md)) |

Unity·Godot·Roblox 경로는 [기타 MCP 가이드](../02_guides/03_other_mcp_dcc_cad_engines.md)를 보세요.

---

## 5. 시간·비용 참고값 (대부분 작성자 자기 보고)

| 사례 | 모델·도구 | 결과 | 시간·비용 | 신뢰도 |
|---|---|---|---|---|
| 펠리컨 자전거 씬 3회 반복 | GPT-6 Astra(Medium), headless Blender | 토이풍 일러스트 품질 | 2분39초 / 3분51초 / 5분59초 | 작성자 원문([TIL](https://github.com/simonw/til/blob/main/llms/blender-coding-agents-macos.md)) |
| 원프롬프트 3D 게임 | Fable 5.1(effort high), Blender headless | 1라운드 통과, 에셋을 직접 보고 수락 | 24분, $9.90, 75턴, 출력 95,832토큰 | 작성자 보고([저장소](https://github.com/Nipale-ai/fable-5-1-one-prompt-game)) |
| Robo Open 테니스 | Astra(Codex) + Blender + Meshy + Unity | 프로토타입 수준 | 프로토타입 52분, 세션 4시간23분, Meshy 30크레딧, 기록된 실패 22건 | 작성자 보고 |
| 교육 영상 5편 | Fable 5.1 + Blender 5.2 | 수정 보통 2라운드 | 심장 챕터 약 11,000프레임을 A10G 약 50대로 84분 | 작성자 보고 |
| Union Square 디지털 트윈 | Fable 5.1 에이전트 스웜 | 재질 6, 시각 충실도 6, 조명 7, 성능 6 (/10) | — | 조정하지 않은 리뷰어 점수 |
| 6날 조리개 비교 | Astra 대 Fable 5.1, 같은 동결 프롬프트 | 둘 다 작동했지만 기계적 결함(겹침, 핀 구멍 없음) | — | 사전 등록 비교, 과제 1개([iris](https://github.com/teshnizi2/astra-fable-3d-iris)) |
| Blender 과제 A/B | Opus 5.5 대 Astra | 품질 비슷, 토큰은 Astra가 적었다는 보고 | 예: Opus 5.5 35분·199.6k 대 Astra 28분·56.6k | 개인 테스트(n=1), 2차 요약, 미검증 |

교훈: "형상이 움직이는 것처럼 보이는 것"과 "기계적으로 맞는 것"은 다릅니다. 품질 차이는 모델보다 **파이프라인(스펙·검사·비평 루프)** 에서 더 크게 납니다.

---

## 흔한 실수와 해결

| 증상 | 원인 | 해결 (단계) |
|---|---|---|
| 가구가 장난감처럼 작거나 거대함 | 스케일 추측, 임포트 단위(cm/m, 100배) | 치수표 강제, 임포트 직후 bounds 실측, FBX_SCALE_UNITS (1, 11) |
| 의자가 "분해되어" 보임 | 부품 좌표 즉흥 계산, 실린더 Euler 회전 | 부품 명세 JSON + 연결 맵, bmesh로 두 점 잇기, `check_assembly()` 검사 (5) |
| 소품이 떠 있거나 파묻힘 | 원점 위치, `obj.location`을 버텍스 위치로 착각 | 원점 바닥 중앙, `snap_to_floor`/`drop_to_surface`, 월드 AABB (1, 6) |
| 배치가 대기실 같음 | 초점·그룹 없이 벽 따라 배치 | 초점 1개 + 기능 그룹 + 동선 먼저, 관계 제약 (6) |
| 너무 깔끔하고 CG 같음 | 균일 roughness, 날카로운 모서리, 완벽 정렬 | roughness 변화, 모든 제조 모서리 베벨, 자연 노이즈, 스토리 비트 (5, 7, 9) |
| 렌더가 밋밋함 | 카메라 축 정면 키, 필 과다, Standard 뷰 | 키 ≥ 20°, 검정에서 시작, AgX + exposure (3, 8) |
| 하이라이트가 하얗게 날아감(또는 AgX가 가림) | 노출 판정을 표시 이미지로만 | False Color·EXR 수치로 판정 (3, 10) |
| 재질 코드가 한국어 UI에서 실패 | 노드 이름 번역 | type으로 찾기, 영어 UI 또는 New Data 번역 끄기 (준비) |
| 노드 소켓 KeyError·AttributeError | 3.x 시절 이름, 레거시 EEVEE 속성 | Principled v2 이름, `describe_node_type` 조회, 5.x 엔진 식별자 (7, 10) |
| 뷰포트는 맞는데 렌더가 회색 | Material Output·Principled 중복 | `nodes.clear()` 후 재구성 (7) |
| 웨더링이 안 보여 값을 과하게 올림 | EEVEE에서 Pointiness·Bevel 미지원 | Cycles로 확인하거나 베이크 (7, 9) |
| GLB에서 AO·displacement가 사라짐 | glTF가 절차 노드·displacement를 안 내보냄 | 베이크, `glTF Material Output` 그룹, 슬롯 감사 (11) |
| 긴 렌더가 도중에 끊김 | 소켓 타임아웃 180초 / MCP 유휴 타임아웃(stdio 30분·HTTP 5분) | 최종 렌더는 headless (10) |
| 같은 수정이 계속 반복됨 | 컨텍스트 오염, 여러 곳 동시 수정 | 결함 하나씩, 2회 실패 시 `/clear` + PROGRESS.md (3) |
| "완료했다"는데 결과가 다름 | 증거 없는 완료 보고 | 렌더·감사 JSON 첨부를 완료 조건으로, 비평가 분리 (3) |
| 한국에서 쓸 수 없는 모델 출력이 섞임 | Hunyuan 계열 라이선스 확인 누락 | 4단계 라이선스 표, provenance 컴포넌트 기록 (4, 11) |
| MCP 서버가 연결되지 않음 | 공식·커뮤니티·Scenario 서버가 모두 9876 사용 | 하나만 켜기 (준비) |

---

## 관련 문서

- [README](../README.md) — 저장소 개요와 읽는 순서
- [목적·범위](../00_purpose/purpose_and_scope.md), [조사 방법·신뢰도](../01_research/research_method.md)
- [AI 모델·클라이언트 선택](../02_guides/01_ai_models_and_clients.md) — 역할 분담, effort, 비용
- [Blender MCP 생태계](../02_guides/02_blender_mcp.md) — 공식 커넥터와 MCP for Blender, 보안, API 함정
- [기타 DCC·CAD·엔진 MCP](../02_guides/03_other_mcp_dcc_cad_engines.md)
- [AI 3D 생성](../02_guides/04_ai_3d_generation.md) — 4단계 생성·정규화·후처리
- [텍스처링·재질](../02_guides/05_texturing_materials.md) — 7단계 PBR 규칙·레시피·`pbr_audit`
- [라이팅·렌더·아트디렉션](../02_guides/06_lighting_rendering_art_direction.md) — 3·8·10단계 수치 게이트와 `review_render()`
- [오브젝트·가구·조형 모델링](../02_guides/07_modeling_objects_furniture_sculpture.md) — 5단계 스펙 우선 모델링
- [배치·레이아웃](../02_guides/08_scene_layout_placement.md) — 6단계 제약·솔버·물리 안착
- [에이전트 워크플로·프롬프팅](../02_guides/09_agent_workflow_prompting.md) — 루프, CLAUDE.md·스킬·훅
- [에셋·파이프라인·라이선스](../02_guides/10_assets_pipeline_licensing.md) — 11단계 익스포트·provenance
- [학술 연구](../02_guides/11_research_papers.md)
- [빠른 시작](01_quickstart_setup.md), [프롬프트 템플릿](03_prompt_templates.md), [품질 체크리스트](04_quality_checklists.md), [실측 치수표](05_reference_dimensions.md)
- [CLAUDE.md 템플릿](templates/CLAUDE.md), [blender-aaa-scene 스킬 템플릿](templates/skills/blender-aaa-scene/SKILL.md), [보조 스크립트](scripts/README.md)
- [사례 모음](../04_case_studies/01_case_studies.md), [한국어 자료](../04_case_studies/02_korean_resources.md)

## 원자료

- `01_research/raw/10_agent-workflow.research.json`, `10_agent-workflow.verify.json` — 단계 순서, 게이트, 루프 규칙, 비평가, 비용·보안
- `01_research/raw/07_aaa-rendering-lighting.research.json`, `07_aaa-rendering-lighting.verify.json` — 색관리, 조명, 카메라, 렌더·합성, Unreal
- `01_research/raw/08_modeling-objects.research.json`, `08_modeling-objects.verify.json` — 스펙 우선 모델링, 부품 분해, 검사, 라이선스
- `01_research/raw/09_scene-layout.research.json`, `09_scene-layout.verify.json` — 관계 제약, 솔버, 물리 안착, 채점·종료 규칙
- `01_research/raw/06_texturing-materials.research.json`, `06_texturing-materials.verify.json` — PBR 규칙, 라이브러리 선택, 베이크·glTF
- `01_research/raw/05_ai-3d-generation.research.json`, `05_ai-3d-generation.verify.json` — 생성 모델 선택, 레퍼런스 준비, 후처리, 한국 라이선스
- `01_research/raw/11_case-studies.research.json`, `11_case-studies.verify.json` — 사례, 실패 패턴, 시간·비용, 모델 비교
