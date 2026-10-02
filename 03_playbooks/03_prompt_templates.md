# 프롬프트 템플릿: 복사해서 쓰는 3D 에이전트 지시문

> 기준일: 2026-09-27 · 킥오프부터 게임레디 변환·비용 제한까지 템플릿 14개. 공개된 스킬·프롬프트 원문과 교차검증 결과를 근거로 만들었고, 코드 조각은 pip `bpy` 4.2.23 LTS와 5.0.1에서 실행해 확인했습니다.

## 핵심 요약

- **한 번에 다 시키지 말고 단계별로 끊어서 씁니다.** 킥오프(T01) → 해석 확인(T02) → 스펙(T03·T05) → 빌드(T04) → 검사(T06) → 4뷰 비평(T07) → 재질·조명·렌더(T08~T10) → 에셋 조달·정리·변환(T11~T13) 순서입니다. 비용·중단 조건(T14)은 첫 메시지에 같이 붙입니다.
- **형용사 대신 숫자와 절차를 씁니다.** '예쁘게', '자연스럽게' 대신 치수(m), 색온도(K), 비율, 허용 오차를 넣고, 출력 형식(JSON, 표, `NEEDS_FIX` 한 줄)을 고정해 기계적으로 검사할 수 있게 합니다. 로컬 9B 모델 실험에서도 "품질 형용사 대신 절차 제약" 원칙을 적용하자 시각 검증을 5/5 세션에서 스스로 수행했다고 보고합니다(작성자 보고, [roo-blendermcp-jp-rules](https://github.com/hideki711014/roo-blendermcp-jp-rules)).
- **멈춤 지점을 명시합니다.** 템플릿마다 `STATUS: WAITING_FOR_…` 한 줄로 끝나게 해서 사람이 G1(스펙), G2(블록아웃·구도), G3(최종 렌더), G4(익스포트)와 유료 호출 직전에 확인합니다. 사람 판단은 초반에 넣을수록 쌉니다.
- **좌표는 모델이 쓰지 않습니다.** 가구는 부품 스펙 JSON(T03), 방은 관계 제약 JSON(T05)만 쓰게 하고, 좌표는 [`placement_utils.py`](scripts/README.md)나 솔버가 계산합니다.
- **숫자 검사가 먼저, 그림 검사는 그다음입니다.** [`scene_audit.py`](scripts/README.md) → [`review_views.py`](scripts/README.md) 4뷰 → 체크리스트형 비평(큰 구조 문제만, `NEEDS_FIX: YES/NO`) 순서로 돌립니다. 숫자가 통과해도 그림이 틀리면 실패이고, 그림이 그럴듯해도 숫자가 틀리면 실패입니다.
- **이미지 입력 규칙:** 이미지를 텍스트보다 먼저 넣고 `Image 1:`처럼 라벨을 붙입니다. 검토용 스크린샷은 긴 변 1000px 안팎이면 충분하고, 한 요청에 이미지가 20장을 넘으면 각 변을 2000px 이하로 줄여야 합니다([Claude vision 문서](https://platform.claude.com/docs/en/build-with-claude/vision)).
- **모델 설정:** Codex에서 GPT-6 Astra의 기본 effort는 low이니 반드시 명시하세요. Opus 5.5의 기본 effort는 medium이라 스펙·레이아웃 설계 턴에서만 올리면 됩니다. 모델 비교는 대부분 개인 테스트(n=1)이므로 템플릿은 특정 모델에 기대지 않게 썼습니다([AI 모델 가이드](../02_guides/01_ai_models_and_clients.md)).
- **[한국 사용자]** 치수는 `REGION=KR` 프리셋([치수표](05_reference_dimensions.md) 10절), 오브젝트 이름은 **영어 snake_case**(한국어 이름은 `scene_audit` 치수 규칙이 인식하지 못함. 종류 단어 `chair`·`sofa` 등을 넣을 것), 노드는 **type**으로 찾기(한국어 UI에서 노드 이름이 번역될 수 있음), Tencent Hunyuan3D 계열은 호출 금지(라이선스 적용 지역에서 대한민국 제외, 출력물 사용도 제한).
- **기대치:** 독립적으로 검증된 'AAA급' AI+MCP 결과물은 아직 찾지 못했습니다. 이 템플릿들은 에이전트를 "감독이 필요한 협업자"로 두고 사람이 마무리하는 운영을 전제로 합니다.

---

## 0. 쓰는 법

### 0.1 템플릿 지도

| ID | 템플릿 | [플레이북](02_aaa_production_playbook.md) 단계 | 끝나는 방식 | 주 근거 |
|---|---|---|---|---|
| T01 | 프로젝트 킥오프·스펙시트 | 0 | `WAITING_FOR_G1` | kiln BRIEF, blender-research spec_sheet, RobLe3 pro-workflow |
| T02 | 해석만 먼저 보여 주기 | 0, 큰 작업 전 | `WAITING_FOR_APPROVAL` | kiln BRIEF, unreal-home-wizard 사진 재현 모드 |
| T03 | 가구 스펙 JSON | 0, 5 | JSON + 멈춤 | PartNet 계층, Holodeck '크기 먼저' |
| T04 | 부품 단위 빌드 | 1, 5 | 부품마다 `done:` 한 줄 | RobLe3 청크 규칙, build123d-mcp 측정 순서, ProfRino 조립 규칙 |
| T05 | 레이아웃 관계 제약 JSON | 6 | JSON + 멈춤 | Holodeck, SAGE, LayoutVLM |
| T06 | 배치 후 검사·수정 | 6, 9 | DONE 조건 표 | SceneSmith, SAGE, SceneEval |
| T07 | 4뷰 비평(체크리스트형, 큰 문제만) | 전 단계 | `NEEDS_FIX: YES/NO` | 3DCodeBench 비평 프롬프트, CADCodeVerify, SceneSmith critic |
| T08 | 재질 지정(PBR 규칙) | 7 | PBR 감사 표 | scenario texturing, RobLe3 materials |
| T09 | 라이팅 셋업 | 3, 8 | 조명 보고 표 | scenario lighting, RobLe3 lighting, Blender 소스 |
| T10 | 최종 렌더 | 10 | 렌더 경로 + 게이트 | Blender 소스, scenario, MCP for Blender #61 |
| T11 | 이미지→3D용 레퍼런스 이미지 생성 | 4 | 후보 이미지 + 승인 대기 | kiln 규칙, codex-blender-higgsfield |
| T12 | 에셋 임포트 정리 | 4, 5 | 정규화 보고 + provenance | kiln 규칙, 배치 조사의 정규화 교훈 |
| T13 | 게임레디 변환 | 11 | 8항목 체크 표 | kiln export 체크리스트 |
| T14 | 비용 제한·중단 조건 | 전체 | `STOP_REASON` 보고 | claude-3d-harness 프로필, SceneSmith 설정, Claude Code 문서 |

### 0.2 공통 약속

- `{{변수}}`는 채워 넣을 자리입니다. 각 템플릿의 변수 표에 예시 값을 적었습니다.
- 프로젝트 루트에 [CLAUDE.md 템플릿](templates/CLAUDE.md)(Codex·Gemini CLI는 AGENTS.md)을 깔아 두었다고 가정합니다. 단계 루프 전체는 [blender-aaa-scene 스킬](templates/skills/blender-aaa-scene/SKILL.md)로도 쓸 수 있습니다.
- 파일 배치는 플레이북 1.3절을 따릅니다: `spec/spec_sheet.json`, `spec/relations.json`, `spec/acceptance.yaml`, `scripts/build_<asset>.py`, `versions/`, `review/v###/`, `provenance/assets.csv`, `PROGRESS.md`.
- 예시 값은 한국 주거 기준입니다. 다른 지역이면 `REGION`을 바꾸고 [치수표](05_reference_dimensions.md)의 해당 줄을 씁니다.
- 코드 블록 첫 줄에 `# 실행 확인:`이 있는 것은 bpy 4.2.23 LTS와 5.0.1에서 두 번씩 실행해(멱등성 확인) 결과를 확인한 코드입니다. 없는 것은 작성 예시입니다.

### 0.3 CLAUDE.md 없이 쓸 때 앞에 붙이는 공통 블록

ChatGPT·Codex 앱처럼 규칙 파일을 쓰지 않는 환경에서는 템플릿 앞에 이 블록을 붙이세요.

```text
[공통 규칙]
- Blender {{BLENDER_VERSION}}, 영어 UI. 1 BU = 1 m, Z-up, 원점 = 바닥 중앙, 가구·제품 정면 = -Y.
- 가구 1개 = 부모 Empty 1개(유닛) + 자식 부품. 이름은 영어 snake_case(dining_chair_01, dining_chair_01_seat).
- 치수는 추측하지 말고 REGION={{REGION}} 치수표 값을 쓴다. 단위를 항상 붙인다.
- execute_blender_code 1회 = 부품 1개 또는 단계 1개. 이름으로 get-or-create, 마지막 줄에 print("done:...").
- 노드는 type으로 찾는다(BSDF_PRINCIPLED). API가 불확실하면 조회 툴을 먼저 쓴다.
- 내가 만들지 않은 오브젝트는 수정·삭제 금지. orphans_purge·공장 초기화 금지. 유료 호출은 승인 후.
- 단계가 끝나면 .blend 버전 저장 → 숫자 검사 → 4뷰 렌더 확인. 증거(수치, 렌더 경로) 없이 완료라고 말하지 않는다.
```

### 0.4 서버마다 다른 툴 이름

같은 템플릿을 어느 서버에서든 쓰도록 역할로 적었습니다. 한 Blender에는 서버를 **하나만** 연결하세요(공식·커뮤니티 모두 localhost:9876).

| 역할 | MCP for Blender(서버 이름 `blender`) | Blender Lab 공식(서버 이름 `blender-lab`) | 헤드리스 |
|---|---|---|---|
| 씬 요약 | `get_scene_info`(오브젝트 최대 10개, 치수 없음) → `scene_audit` 권장 | `get_objects_summary` | `scene_audit.py --out audit.json` |
| 오브젝트 상세 | `get_object_info`(`world_bounding_box` 포함) | `get_object_detail_summary` | — |
| 스크린샷 | `get_viewport_screenshot`(MCP 툴 기본 `max_size` 1000) | `get_screenshot_of_area_as_image` | `review_views.py` |
| 코드 실행 | `execute_blender_code` | `execute_blender_code`, `execute_blender_code_for_cli` | `blender -b … --python-exit-code 1 -P` |
| API 조회 | `bpy_api_lookup`, `describe_node_type` | `get_python_api_docs`, `search_api_docs`·`search_manual_docs`(번들 5.1 문서 AND 검색, 실측) | fake-bpy-module 스텁 |

툴 이름 대응은 cc-blender-skill에 올라온 제3자 PR(병합 안 됨, [PR #1](https://github.com/RobLe3/cc-blender-skill/pull/1))과 공식 서버 미러([bpype/blender_mcp](https://github.com/bpype/blender_mcp))로 확인했습니다. 서버별 설치는 [빠른 시작](01_quickstart_setup.md)을 보세요.

---

## T01. 프로젝트 킥오프·스펙시트

- **용도:** 세션의 첫 메시지입니다. 목표·제약·예산·절차·멈춤 지점을 한 번에 주고, 에이전트가 **스펙시트와 합격 기준 파일만** 쓰게 합니다.
- **언제:** 플레이북 단계 0, 게이트 G1 직전.
- **출력:** `spec/spec_sheet.json`, `spec/acceptance.yaml`, 질문 목록 → 멈춤.

| 변수 | 뜻 | 예 |
|---|---|---|
| `{{RUNTIME}}` | 연결 방식 | MCP for Blender / Blender Lab 공식 커넥터 / 헤드리스 bpy |
| `{{MODEL_SETUP}}` | 모델과 effort | Claude Opus 5.5 effort high / Codex GPT-6 Astra `model_reasoning_effort = "high"` |
| `{{GOAL}}` | 무엇을, 어디에 쓰나 | 한국 구축 아파트 거실, 저녁 실용광, 포트폴리오 스틸 |
| `{{DELIVERABLES}}` | 산출물 | 스틸 3컷(1920×1080) + 편집 가능한 `.blend` |
| `{{REFS}}` | 레퍼런스 이미지와 라벨 | Image 1: 무드, Image 2: 소파 정면 사진 |
| `{{REGION}}` | 치수 프리셋 | KR |
| `{{PROFILE}}` | 품질 프로필 | fast / standard / cinematic |
| `{{BUDGET}}` | 트라이·텍스처·유료 한도 | 히어로 ≤ 8k tri, 2K PBR, 유료 생성 0회 |

```text
[모델] {{MODEL_SETUP}}
[역할] 너는 Blender {{BLENDER_VERSION}}(영어 UI)를 {{RUNTIME}}로 조작하는 시니어 테크니컬 아티스트다.
       프로젝트 규칙은 CLAUDE.md(또는 AGENTS.md)를 따른다.
[입력] (이미지는 이 글보다 먼저 첨부했다) {{REFS}}
[목표] {{GOAL}}
[산출물] {{DELIVERABLES}}
[제약] 1 BU = 1 m, Z-up, 원점 = 바닥 중앙, 가구 정면 -Y.
       치수는 REGION={{REGION}} 치수표(03_playbooks/05_reference_dimensions.md 10절)에서 가져오고 추측하지 않는다.
       기존 오브젝트 수정·삭제 금지. 유료 API·에셋 다운로드는 내 승인 후에만. 이름은 영어 snake_case.
[예산] 품질 프로필 {{PROFILE}}, {{BUDGET}}. 비용·중단 조건은 아래 [예산·중단] 블록을 따른다(T14).
[이번 턴] Blender를 조작하지 말고 아래 세 가지만 작성해서 보여 줘.
 1) spec/spec_sheet.json
    meta{name, style, use, region, profile, poly_budget, texture_res}
    camera{lens_mm, height_m, angle, aspect}
    lighting_intent{time_of_day, key_kelvin, mood}
    palette[{name, srgb_hex}]
    objects[{id, category, dims_m:[w,d,h], count, source:"library|generate|code",
             hero:true|false, material_intent, notes}]
    치수마다 근거를 적는다: "치수표 1장 식탁의자" / "Image 2" / "추정".
 2) spec/acceptance.yaml  (G1 승인 뒤에는 수정하지 않는다)
    hard: scene_audit(floating 0, below_floor 0, sunk_into 0, above_ceiling 0, interpenetration 0,
          unapplied_scale 0, size_out_of_range 0), 방·건물이면 building_audit errors 0
          관계 치수(예: 식탁 상판 − 의자 좌판 0.25~0.305 m), 주동선 ≥ 0.9 m
    soft: 비평 기준(NEEDS_FIX: NO 2회 연속), 렌더 기준(발광체 외 클리핑 ≤ 0.5%)
    limits: 단계별 최대 수정 라운드, 유료 호출 한도
    allowed_exceptions: 의도적으로 떠 있는 것(벽걸이, 천장등) 목록
 3) [uncertain] 항목과 질문(최대 5개, 선택지나 예/아니오로)
[멈춤] 끝에 "STATUS: WAITING_FOR_G1" 한 줄만 쓰고 멈춰. 승인 전에는 MCP 툴을 호출하지 마.
```

**왜 이렇게 쓰나**

- "의자 하나 만들어줘"에는 치수·부품·재질이 비어 있어 모델이 임의로 채웁니다. 스펙을 먼저 만들고 확인받는 구조는 [blender-research 스킬](https://raw.githubusercontent.com/Gaius114/blender-claude-mcp/main/skill/blender-research/SKILL.md)의 spec_sheet 단계와 [blender-kiln](https://raw.githubusercontent.com/elithril/blender-kiln/main/SKILL.md)의 BRIEF 단계(이해한 내용을 다시 정리하고 확인받음)에서 가져왔습니다.
- 치수 추측 금지는 RobLe3 오케스트레이터의 "Do not guess"와 같습니다([text-to-blender](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/text-to-blender/SKILL.md)). 크기를 먼저 정하게 하는 패턴은 AI2 Holodeck이 LLM에게 크기를 `[length, width, height]` cm로 먼저 답하게 한 방식과 같습니다([prompts.py](https://raw.githubusercontent.com/allenai/Holodeck/main/ai2holodeck/generation/prompts.py)).
- 사람 확인을 초반에 두는 이유: 이미지 선택 → 승인 게이트([3D-lab-skills](https://github.com/LumosLab-Innovation/3D-lab-skills), 신뢰도 낮음), 단계별 승인([pipeline-kit](https://github.com/pradhankukiran/pipeline-kit)), 해시에 묶인 사람 리뷰([blender-art-factory](https://github.com/ErikBurdett/blender-art-factory))가 모두 같은 방향입니다.
- 증기기관차 도면을 오브젝트 3,295개로 만든 Tom Krcha는 "Naive prompts will fail, refined systematic prompts written by an expert succeed"라고 정리했습니다([X 게시물](https://x.com/tomkrcha/status/2095598645190291775), 원문 미열람·큐레이션 목록 경유).

---

## T02. 해석만 먼저 보여 주기: "아직 만들지 마"

- **용도:** 에이전트가 무엇을 이해했는지, 무엇을 가정했는지, 어떤 툴을 몇 번 부를지를 **실행 전에** 드러내게 합니다. 잘못 이해한 채로 10분짜리 빌드를 돌리는 것을 막습니다.
- **언제:** 새 장면·새 에셋·큰 수정(재배치, 재질 전면 교체, 유료 생성) 직전. T01 이후 단계마다 다시 써도 됩니다.

| 변수 | 예 |
|---|---|
| `{{REQUEST}}` | 거실에 3인 소파, 커피테이블, TV장, 암체어 1개를 배치해 줘 |
| `{{READONLY_TOOLS}}` | `get_scene_info`, `get_object_info`, `get_viewport_screenshot`(공식 서버는 0.4절 표의 대응 툴) |

```text
아직 아무것도 만들지 마.
허용: 읽기 전용 조회({{READONLY_TOOLS}})와 파일 읽기. 금지: execute_blender_code, 생성·다운로드 툴, 파일 쓰기.

요청: {{REQUEST}}
(레퍼런스: Image 1 … Image N)

아래 형식으로 네가 이해한 것만 보여 줘.
1. 한 문장 요약
2. 요구사항 표: 항목 | 이해한 값(단위 포함) | 근거(내 말 인용 / Image N / 치수표 / 추정)
3. 가정과 [uncertain]: 결과에 미치는 영향이 큰 것부터
4. 이번에 만들지 않을 것(범위 밖)
5. 계획: 단계 | 쓸 툴 | 예상 호출 수 | 유료 여부와 예상 크레딧
6. 완료 판정 기준(숫자로)
7. 질문 최대 5개(선택지나 예/아니오로)
마지막 줄: STATUS: WAITING_FOR_APPROVAL
```

**사진·도면을 재현할 때 덧붙이는 블록**

```text
[재현 모드] 레퍼런스에 보이지 않는 공간·가구·장식을 지어내지 마.
보이지 않는 부분은 [not in reference]로 표시하고 어떻게 처리할지 나에게 묻는다.
형상을 맞추기 전에 카메라(초점거리, 높이, 기울기)부터 추정한다.
스케일은 알려진 치수 하나로 맞춘다(예: 방문 높이 2.0~2.1 m). 그 값을 모르면 나에게 묻는다.
```

**왜 이렇게 쓰나**

- [unreal-home-wizard](https://raw.githubusercontent.com/amirmushichge/unreal-home-wizard/main/skills/unreal-home-wizard/SKILL.md)는 매물 사진 20장으로 UE 워크스루를 만들 때 "사진 재현 모드(임의 재디자인 금지)"를 두고, 천장고나 문 폭 같은 알려진 치수 하나를 사용자에게 묻습니다. "사용자는 1차 버그 탐지자가 아니다"가 이 스킬의 원칙입니다(Codex용 스킬).
- "사진에 맞추려고 형상을 비틀기 전에 카메라와 렌즈부터 푼다"는 규칙은 [blender-production](https://raw.githubusercontent.com/per-simmons/blender-production/master/SKILL.md)에서 왔습니다(커밋 1개의 미검증 저장소, 원문 문구는 확인됨).
- 이미지는 글보다 먼저 넣고 `Image 1:` 라벨을 붙이는 편이 결과가 좋습니다([vision 문서](https://platform.claude.com/docs/en/build-with-claude/vision)).

---

## T03. 가구 스펙 JSON 생성

- **용도:** 가구·소품 하나를 코드로 만들기 전에 부품·치수·결합·검사 기준을 JSON으로 고정합니다. 좌표를 코드 안에서 즉흥적으로 계산하다 부품이 뜨거나 파묻히는 문제를 줄입니다.
- **언제:** 플레이북 단계 0(스펙)과 단계 5(히어로 모델링) 직전.

| 변수 | 예 |
|---|---|
| `{{FURNITURE}}` | 한국 아파트 4인 식탁용 원목 의자 |
| `{{UNIT_NAME}}` | `dining_chair_01` |
| `{{STYLE}}` | 미드센추리, 오크 원목, 좌판 앞 모서리 R 5 mm |

```text
{{FURNITURE}}의 부품 스펙을 JSON으로만 출력해. 코드는 아직 쓰지 마. 스타일: {{STYLE}}
규칙
- 단위 m, Z-up, 원점 = 바닥 접점 중앙, 정면 -Y. REGION={{REGION}} 치수표 값을 쓰고 값마다 source를 단다.
- 부품은 PartNet 계층을 체크리스트로 쓴다.
  의자: chair_back(back_surface, back_frame, back_connector) / chair_seat(seat_surface, seat_frame)
        / chair_base(leg, bar_stretcher, runner, foot) / chair_arm
  테이블: tabletop / leg / apron / stretcher / drawer
  쓰지 않는 부품은 omitted에 이유와 함께 적는다.
- 부품마다 실제 두께를 준다. 모르면 범위로 쓰고 uncertain에 넣는다.
- 같은 유닛 안의 부품은 접합부에서 5~15 mm 겹쳐 이음새를 숨긴다(joints에 적는다). 다른 유닛과의 관통은 금지.
- 관계 치수를 checks에 넣는다(예: 식탁 상판 − 좌판 0.25~0.305 m).
- 제조 모서리마다 bevel 폭을 재질에 맞춰 적는다.
- 정점을 직접 나열하지 않는다. 곡면은 단면 프로파일(20점 이하)이나 커브 반경을 숫자로 적는다.
스키마
{"unit": "{{UNIT_NAME}}", "units": "m", "region": "{{REGION}}", "front": "-Y",
 "overall": {"w": 0, "d": 0, "h": 0},
 "parts": [{"name": "{{UNIT_NAME}}_seat", "partnet": "chair_seat/seat_surface",
            "shape": "box|cylinder|profile_extrude|curve_sweep|sdf",
            "size": [0, 0, 0], "center": [0, 0, 0], "rotation_deg": [0, 0, 0],
            "attach_to": {"part": "", "face": "top|bottom|front|back|left|right"},
            "material": "M_wood_oak", "bevel_m": 0.002, "source": ""}],
 "joints": [{"a": "", "b": "", "type": "overlap|mortise_tenon|screw|weld", "overlap_mm": 10}],
 "checks": {"seat_top_z": [0.43, 0.48]},
 "omitted": [{"partnet": "chair_arm", "reason": ""}],
 "uncertain": []}
출력 뒤 "STATUS: WAITING_FOR_SPEC_APPROVAL"로 끝내.
```

**채운 예(요지)** — 한국 식탁 의자. 좌판 윗면 0.45 m(KR 450, 범위 430~480 mm), 전체 높이 0.84 m(813~965 mm 안).

```json
{"unit": "dining_chair_01", "units": "m", "region": "KR", "front": "-Y",
 "overall": {"w": 0.44, "d": 0.42, "h": 0.84},
 "parts": [
  {"name": "dining_chair_01_seat", "partnet": "chair_seat/seat_surface", "shape": "box",
   "size": [0.44, 0.42, 0.03], "center": [0, 0, 0.435], "material": "M_wood_oak", "bevel_m": 0.002,
   "source": "치수표 1장: 식탁의자 좌판 450(430~480), 깊이 430(406~457)"},
  {"name": "dining_chair_01_leg_FL", "partnet": "chair_base/leg", "shape": "box",
   "size": [0.035, 0.035, 0.43], "center": [-0.185, -0.175, 0.215], "attach_to": {"part": "dining_chair_01_seat", "face": "bottom"},
   "material": "M_wood_oak", "bevel_m": 0.0015, "source": "경험치 0.035~0.045"},
  {"name": "dining_chair_01_leg_BL", "partnet": "chair_base/leg", "shape": "box",
   "size": [0.035, 0.035, 0.84], "center": [-0.185, 0.175, 0.42],
   "material": "M_wood_oak", "bevel_m": 0.0015, "source": "뒷다리가 등받이까지 이어지는 일체형"},
  {"name": "dining_chair_01_back_rail", "partnet": "chair_back/back_surface", "shape": "box",
   "size": [0.36, 0.02, 0.10], "center": [0, 0.175, 0.76], "attach_to": {"part": "dining_chair_01_leg_BL", "face": "right"},
   "material": "M_wood_oak", "bevel_m": 0.0015, "source": "추정"}],
 "joints": [{"a": "dining_chair_01_leg_FL", "b": "dining_chair_01_seat", "type": "overlap", "overlap_mm": 10},
            {"a": "dining_chair_01_back_rail", "b": "dining_chair_01_leg_BL", "type": "overlap", "overlap_mm": 12}],
 "checks": {"seat_top_z": [0.43, 0.48], "overall_h": [0.813, 0.965], "table_top_minus_seat_top": [0.25, 0.305]},
 "omitted": [{"partnet": "chair_arm", "reason": "식탁 의자"}, {"partnet": "chair_base/bar_stretcher", "reason": "스타일상 생략, 필요 시 추가"}],
 "uncertain": ["등받이 기울기(뒤로 약 8°) 적용 여부"]}
```

(FR·BR 다리는 대칭이라 생략. 이 치수로 만든 의자는 T04 코드로 조립해 `scene_audit` 결과 issues 0을 확인했습니다.)

**참고 수치** (근거와 신뢰도는 [모델링 가이드](../02_guides/07_modeling_objects_furniture_sculpture.md), 치수는 [치수표](05_reference_dimensions.md))

| 항목 | 값 | 비고 |
|---|---|---|
| 부재 두께 | 원목 식탁 상판 0.025~0.04, 에이프런 높이 0.07~0.10 × 두께 0.02~0.025(상판 끝에서 0.03~0.05 안쪽), 의자 다리 0.035~0.045, 좌판 0.02~0.035(쿠션 0.05~0.10), 판재 18 mm, 뒤판 3~6 mm, 문·서랍 틈 2~3 mm | 경험치(원문 미확인) |
| bevel 폭 | 원목 1~3 mm, 도장 MDF 0.5~1.5 mm, 금속 0.3~1 mm, 석재 2~5 mm, 사출 플라스틱 0.5~2 mm, 패브릭 쿠션 10~30 mm. 모르면 최대 치수의 0.5% | 경험치. 0.5% 기본값은 [scenario hard-surface](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/dcc/blender/scenario-blender-hard-surface/SKILL.md) 저자가 덧붙인 값 |
| Infinigen 의자 파라미터 | 좌판 윗면이 약 0.47~0.54 m | **표준이 아니라 랜덤 생성 범위**라서 치수 근거로 쓰지 않습니다(검증 정정) |

**왜 이렇게 쓰나**

- PartNet의 [Chair 계층](https://raw.githubusercontent.com/daerduoCarey/partnet_dataset/master/stats/after_merging_label_ids/Chair-hier.txt)은 24개 카테고리 모델 26,671개의 부품 주석에서 나온 어휘라 가로대·에이프런 같은 누락 부품을 줄여 줍니다.
- 접합부 겹침: RobLe3는 5~15 mm([modeling 스킬](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-modeling/SKILL.md)), ProfRino 조립 스킬은 최소 5 mm와 "코드 전에 연결 지도"를 요구합니다([Blender-MCP-Assembly-Skill](https://raw.githubusercontent.com/ProfRino/Blender-MCP-Assembly-Skill/main/SKILL.md)). 유닛 안 겹침은 허용하고 유닛 사이 관통은 금지하는 방식이 `scene_audit`(유닛끼리만 관통 검사)와 맞습니다.
- 정점 직접 나열 금지: 메시를 텍스트로 생성하는 LLaMA-Mesh·MeshLLM 계열은 저폴리에 머물러, 코드로 구성하는 경로가 현실적이라는 것이 08 조사 결론입니다.

---

## T04. 부품 단위 빌드

- **용도:** T03 스펙을 부품 하나씩 코드로 짓고, 부품마다 치수와 접촉을 숫자로 확인합니다.
- **언제:** 플레이북 단계 1(블록아웃)과 5(히어로 모델링).

```text
spec/{{SPEC_FILE}}의 부품을 하나씩 만든다.
- execute_blender_code 1회 = 부품 1개. 매 호출은 새 네임스페이스이므로 import부터 다시 하고,
  helper(unit_root, box_part, world_bbox, aabb_gap)를 매번 같이 보낸다.
- get-or-create: 이름으로 찾고 없을 때만 만든다. 같은 코드를 두 번 돌려도 결과가 같아야 한다.
- 크기는 메시 정점으로 만들고 오브젝트 scale은 (1,1,1)로 둔다. 회전한 부품은 world bbox로 축을 다시 확인한다.
- 순서: 받쳐 주는 부품부터(다리 → 좌판 → 등받이 기둥 → 등받이 → 가로대 → 하드웨어).
- 부품마다 한 줄로 보고: done:<name> min=… max=… 붙는 부품과의 aabb_gap 최댓값(m).
  최댓값 > 0.001(떠 있음)이거나 겹침이 spec의 overlap_mm 범위를 벗어나면 다음 부품으로 가지 말고 고친다.
- 유닛을 다 만들면 scene_audit(floor_z=0)을 돌려 issues 0을 확인하고 versions/에 저장한다.
- 같은 오류가 3번 나면 기능을 줄인 최소 버전으로 전략을 바꾸고 보고한다.
- 최종 코드는 scripts/build_{{UNIT_NAME}}.py에 파라미터 함수로 모아 둔다(뷰포트에서 고친 내용도 반영).
```

```python
# 실행 확인: bpy 4.2.23 LTS / 5.0.1 (두 번 실행해도 오브젝트 수 동일, scene_audit issues 0)
import bpy, bmesh
from mathutils import Vector

COL = "COL_Hero"

def get_col(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    return c

def unit_root(name, loc=(0.0, 0.0, 0.0)):
    """유닛(가구 1개) = 최상위 Empty. 원점 = 바닥 중앙, 정면 = -Y."""
    o = bpy.data.objects.get(name)
    if o is None:
        o = bpy.data.objects.new(name, None)
        get_col(COL).objects.link(o)
    o.location = loc
    return o

def box_part(name, size, center, parent, bevel=0.002):
    """size=(x,y,z) m, center = 부모 기준 중심. 부를 때마다 메시를 새로 만든다(멱등)."""
    o = bpy.data.objects.get(name)
    if o is None:
        o = bpy.data.objects.new(name, bpy.data.meshes.new(name))
        get_col(COL).objects.link(o)
    bm = bmesh.new()
    bm.loops.layers.uv.new("UVMap")
    bmesh.ops.create_cube(bm, size=1.0, calc_uvs=True)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    bm.to_mesh(o.data)
    bm.free()
    o.parent = parent
    o.location, o.rotation_euler, o.scale = center, (0.0, 0.0, 0.0), (1.0, 1.0, 1.0)
    bev = o.modifiers.get("Bevel") or o.modifiers.new("Bevel", "BEVEL")
    bev.width, bev.segments, bev.limit_method, bev.harden_normals = bevel, 3, "ANGLE", True
    wn = o.modifiers.get("WeightedNormal") or o.modifiers.new("WeightedNormal", "WEIGHTED_NORMAL")
    wn.keep_sharp = True  # Weighted Normal은 스택 맨 끝
    return o

def world_bbox(o):
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    pts = []
    for m in [o] + list(o.children_recursive):
        if m.type == "MESH":
            ev = m.evaluated_get(dg)
            pts += [ev.matrix_world @ Vector(c) for c in ev.bound_box]
    return (Vector([min(p[i] for p in pts) for i in range(3)]),
            Vector([max(p[i] for p in pts) for i in range(3)]))

def aabb_gap(a, b):
    """축별 간격(m). 음수는 겹침 깊이. max(...) > 0.001 이면 떨어져 있음."""
    (amn, amx), (bmn, bmx) = world_bbox(a), world_bbox(b)
    return [round(max(bmn[i] - amx[i], amn[i] - bmx[i]), 4) for i in range(3)]

# --- 이번 호출에서 만들 부품 1개 ---
root = unit_root("dining_chair_01")
seat = box_part("dining_chair_01_seat", (0.44, 0.42, 0.03), (0.0, 0.0, 0.435), root)
mn, mx = world_bbox(seat)
print(f"done:{seat.name} min={tuple(round(v, 3) for v in mn)} max={tuple(round(v, 3) for v in mx)}")
```

- 다음 호출에서 다리를 만들면 `aabb_gap(leg, seat)`가 `[-0.0525, -0.0525, -0.01]`처럼 나옵니다. 최댓값 -0.01은 10 mm 겹침이라 spec의 `overlap_mm: 10`과 맞습니다.
- 정밀 조인트(장부, 도브테일, 레일)가 필요하면 build123d-mcp로 만들고 Blender로 가져옵니다. 이 서버의 기본 프롬프트는 "(1) After every execute() call measure(); (2) After assembly positioning call compare(); (3) Only after (1) and (2) pass call render_view()" 순서를 강제합니다([default_prompt.md](https://raw.githubusercontent.com/pzfreo/build123d-mcp/main/default_prompt.md)). CAD는 기본 단위가 mm이라 가져올 때 0.001배 후 스케일을 적용합니다.
- 부품 단위 조립 검사 전체(`check_assembly()`)는 [모델링 가이드](../02_guides/07_modeling_objects_furniture_sculpture.md) 2.4절에 있습니다.

**왜 이렇게 쓰나**

- `execute_blender_code`는 호출마다 새 네임스페이스라 Python 변수가 남지 않고, 상태는 `bpy.data`에만 남습니다. 서버 도움말도 "Make sure to do it step-by-step by breaking it into smaller chunks"라고 적습니다([server.py](https://raw.githubusercontent.com/ahujasid/blender-mcp/main/src/blender_mcp/server.py)). `exec()`에는 타임아웃이 없고 소켓 타임아웃은 180초라 큰 루프는 Blender를 멈춥니다.
- `obj.dimensions`는 스케일은 반영하지만 **로컬 축 기준이라 회전을 반영하지 않습니다**(검증 정정). 그래서 위치 계산은 `matrix_world @ bound_box`의 world AABB로 합니다. 오브젝트를 옮긴 직후에는 `view_layer.update()`를 해야 `matrix_world`가 갱신됩니다.
- 파라미터 함수로 쓰고 부품마다 bbox를 print해 접촉·부유를 스스로 검사하게 하는 방식은 3DCodeBench 시스템 프롬프트의 절차적 구성 요구와 같습니다([text_to_3d_system_prompt](https://raw.githubusercontent.com/gaoypeng/3dcodebench/main/prompts/text_to_3d_system_prompt.txt)). 실행 오류는 traceback을 돌려주고 3회 안팎 재시도하는 것이 이 벤치마크의 표준입니다.

---

## T05. 레이아웃 관계 제약 JSON

- **용도:** 방 하나의 가구 배치를 **좌표 없이** 관계 제약으로만 쓰게 합니다. 좌표는 [배치 가이드](../02_guides/08_scene_layout_placement.md) 4.4절의 `grid_solver.py`나 `placement_utils`가 계산합니다.
- **언제:** 플레이북 단계 6. 방 구조(벽, 문, 창)가 확정된 뒤.

| 변수 | 예 |
|---|---|
| `{{ROOM}}` | 4.2 × 3.6 m, 천장 2.3 m(한국 구축 아파트) |
| `{{OPENINGS}}` | 문: 남쪽 벽 x 0.2~1.1 m / 창: 동쪽 벽 y 0.8~2.8 m, 바닥까지 |
| `{{FURNITURE_LIST}}` | 3인 소파, TV장, 커피테이블, 암체어, 사이드테이블, 플로어 램프 |
| `{{STORY}}` | 퇴근 후 혼자 영화 보는 저녁 |

```text
방: {{ROOM}}. 개구부: {{OPENINGS}}. 가구: {{FURNITURE_LIST}}. 장면 이야기: {{STORY}}.
좌표(x, y, z)는 쓰지 마. 아래 순서로 생각을 적고 마지막에 JSON만 따로 출력해.
1) 초점 1개를 정한다(TV 벽 / 창 전망 / 벽난로).
2) 기능 그룹(대화, 독서, 식사, 작업, 수면)과 그룹마다 앵커 1개, 멤버를 나열한다.
3) 주동선(폭 ≥ 0.9 m)과 금지 영역을 먼저 적는다: 문 앞 = 문 폭 × 문 폭 사각형, 창 앞 0.6 m.
4) objects와 relations를 JSON으로 쓴다.
   - size는 실측 m [폭, 깊이, 높이], REGION={{REGION}} 치수표 근거. id는 영어 snake_case.
   - 어휘는 against_wall(벽), wall_center(벽), facing(대상), in_front_of(대상), center_aligned(대상),
     distance(대상, min, max) 6개만. distance는 가장자리 사이 최단 거리(m).
   - 앵커는 벽 관련 제약만 쓴다. 뒤에 나오는 객체는 앞에 나온 객체에만 의존한다. 객체당 제약 3~5개.
   - 책·컵 같은 표면 위 소품은 넣지 않는다(배치 후 drop_to_surface와 물리 안착으로 따로 처리).
스키마
{"units": "m",
 "room": {"size": [W, D], "ceiling": H, "region": "{{REGION}}",
          "doors": [{"wall": "S", "x": [x0, x1]}], "windows": [{"wall": "E", "y": [y0, y1], "sill": 0.0}],
          "keep_out": [[x0, y0, x1, y1]]},
 "focal_point": "tv_stand",
 "groups": {"conversation": ["sofa", "coffee_table", "tv_stand"]},
 "objects": [{"id": "sofa", "size": [w, d, h], "front": "-Y", "relations": [["against_wall", "N"], ["wall_center", "N"]]}]}
끝에 "STATUS: WAITING_FOR_LAYOUT_APPROVAL".
```

**참고 간격**(출처별 값이 다르면 겹치는 구간을 기본값으로, 전체 표는 [치수표](05_reference_dimensions.md) 6절)

| 관계 | 기본값 | 출처별 값 |
|---|---|---|
| 소파–커피테이블 | 0.35~0.45 m | [SceneSmith 프롬프트](https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/prompts/data/furniture_agent/designer_agent.yaml) 0.3~0.5, [Infinigen home.py](https://raw.githubusercontent.com/princeton-vl/infinigen/v1.16.0/infinigen_examples/constraints/home.py) hinge(0.45, 0.6), 인테리어 가이드 356~457 mm |
| 소파–TV장 | 2.0~3.0 m | Infinigen hinge(2, 3) |
| 주동선 | ≥ 0.9 m | SceneSmith 0.7~1.0, [SAGE](https://raw.githubusercontent.com/NVlabs/sage/main/server/objects/object_placement_planner.py) 0.6~0.9, 치수표 KR 기본 900 |
| near / far | 0.5~1.5 m / 1.5 m 이상 | [Holodeck](https://raw.githubusercontent.com/allenai/Holodeck/main/ai2holodeck/generation/prompts.py) |
| 가구 점유율 | 30~40% | SAGE 프롬프트 |

**왜 이렇게 쓰나**

- LLM이 좌표를 직접 찍으면 충돌·부유·방향 오류가 반복됩니다. Holodeck, LayoutVLM, Infinigen, SAGE는 모두 "LLM은 관계, 솔버는 좌표"로 나눴습니다. 어휘를 수치로 못박지 않으면 모델마다 해석이 달라집니다([LayoutVLM 제약 7종](https://raw.githubusercontent.com/sunfanyunn/LayoutVLM/main/prompts/layoutvlm/base_prompt.py)).
- "앵커는 global 제약만, 큰 것부터, 뒤의 것은 앞의 것에만 의존"은 Holodeck 프롬프트 지침이고, SAGE 프롬프트는 "객체당 4~5개 제약이 planner를 크게 돕는다"고 적었습니다.
- 초점과 기능 그룹을 먼저 정하지 않으면 가구가 벽을 따라 흩어진 '대기실' 배치가 됩니다. Infinigen은 `focus_score`(소파가 TV를 향함)로 이를 최적화합니다.
- SAGE의 "문 회전반경 약 90 cm"는 프롬프트 문구이고, 실제 솔버는 문 폭 × 문 폭 정사각형을 막습니다(검증 정정). 템플릿은 솔버 쪽 정의를 따랐습니다.

---

## T06. 배치 후 검사·수정

- **용도:** T05 결과를 Blender에 적용한 뒤 관통·부유·방향·간격을 숫자로 검사하고, 위반만 고치게 합니다.
- **언제:** 플레이북 단계 6과 9(소품·디테일 뒤).

```text
spec/relations.json의 배치를 적용했다. 이제 검사하고 고친다. 한 호출에 오브젝트 1~3개만 다룬다.
1) 숫자 검사를 돌려 결과를 표로 보여 줘:
   - scene_audit(floor_z=0, ceiling_z={{CEILING_Z}}, collection="{{ROOM_COLLECTION}}", size_rules={{SIZE_RULES}}):
     floating, below_floor, sunk_into, above_ceiling, interpenetration(가구–벽·천장 포함), size_out_of_range
   - check_clearances({{CLEARANCE_RULES}})
   - facing: 정면(-Y)과 대상 방향의 수평 내적 ≥ 0.9
   - 문 앞 금지 영역, 주동선 폭 ≥ 0.9 m. 벽·문·창이 있으면 building_audit로 door_blocked·window_blocked 확인
2) DONE 조건: interpenetrations == [] AND floating == [](acceptance의 허용 예외 제외)
   AND 동선·문 막힘 0 AND clearance 위반 0 AND facing 전부 통과.
   하나라도 어기면 DONE이라고 말하지 마. 해결할 수 없는 충돌이면 그 오브젝트를 빼자고 제안한다.
3) 고치는 방법은 증상별로 정해져 있다:
   떠 있음 → snap_to_floor / drop_to_surface   벽에서 뜸 → place_against_wall(gap 0.01~0.05)
   관통 → 접촉면까지 이동(0.01 m 스텝으로 다가가다 충돌하면 한 스텝 후퇴)   방향 → face_towards
   간격 위반 → relations의 distance를 고치고 다시 푼다(좌표를 손으로 맞추지 않는다).
   location을 직접 바꿨다면 face_towards 전에 bpy.context.view_layer.update()를 호출한다.
4) 위반이 0이 되면 자연 노이즈를 준다: 벽붙이 가구 yaw ±1°, 위치 σ 0.03 m, 소품 yaw ±3~8°.
   식탁 의자 1~2개는 5~10 cm 빼 둔다. 모든 표면을 소품으로 채우지 않는다.
5) 다시 1)을 돌려 0건인지 확인하고, review_views 4뷰로 넘어간다(T07).
출력: 위반 표(object | 검사 | 값 | 기준 | 조치) → 조치 후 재검사 표 → 한 줄 요약.
```

```python
# 실행 확인: bpy 4.2.23 LTS / 5.0.1 — 검사 부분 (배치는 placement_utils 함수 사용)
import sys, importlib, bpy
from mathutils import Vector
sys.path.append(r"{{REPO}}/03_playbooks/scripts")   # 이 저장소를 받은 절대 경로
import scene_audit, placement_utils as pu
importlib.reload(scene_audit); importlib.reload(pu)

def facing_ok(obj, target, min_dot=0.9):
    """정면(-Y)이 target 쪽을 보는지. 수평 성분만 비교."""
    bpy.context.view_layer.update()
    f = obj.matrix_world.to_3x3() @ Vector((0.0, -1.0, 0.0))
    d = target.matrix_world.translation - obj.matrix_world.translation
    f.z = d.z = 0.0
    return f.normalized().dot(d.normalized()) >= min_dot

O = bpy.data.objects
rep = scene_audit.audit_scene(floor_z=0.0)   # 방이면 ceiling_z=2.30, collection="Room" 추가
print("audit:", rep["summary"], [(u["name"], u["issues"]) for u in rep["units"] if u["issues"]], rep["interpenetrations"])
print("clearance:", pu.check_clearances([("sofa", "coffee_table", 0.35, 0.45), ("sofa", "tv_stand", 2.0, 3.0)]))
print("facing:", {n: facing_ok(O[n], O[t]) for n, t in [("sofa", "tv_stand"), ("armchair", "coffee_table")]})
```

- 한국 프리셋 `size_rules`와 `ceiling_z`(구축 2.30)는 [치수표](05_reference_dimensions.md) 11절의 `KR_SIZE_RULES` 예시를 그대로 넘기세요. 이름은 단어 단위로 맞춥니다. `CoffeeTable`·`coffee_table_01`은 `coffee_table` 규칙에 걸리고, `table_lamp`·`door_handle`처럼 부속품 단어가 뒤에 붙거나 `turntable`처럼 단어 일부만 같으면 걸리지 않습니다. 폭·깊이는 가구 자체 방향 기준이라 회전한 가구도 오탐하지 않습니다.
- 방 안 가구와 건물 외관이 한 장면에 있으면 `collection=`으로 나눠 검사하세요. 천장 규칙이 건물 기둥 같은 외관 오브젝트에 잘못 걸리지 않습니다([스크립트 README](scripts/README.md)).
- 소품 물리 안착(2~5 cm 띄워 두고 rigid body로 떨어뜨린 뒤 변환 확정, 1 m 이상 이동하거나 45° 이상 기울면 실패)은 [배치 가이드](../02_guides/08_scene_layout_placement.md) 4.7절 코드를 쓰세요.

**왜 이렇게 쓰나**

- SceneSmith 디자이너 프롬프트는 "check_physics로 충돌 0을 확인하기 전에는 작업을 끝내지 말고, 해결 못 하는 충돌은 객체를 지우는 편이 낫다"고 적습니다([designer_agent.yaml](https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/prompts/data/furniture_agent/designer_agent.yaml)). 방향도 시각 판단 대신 전용 검사로 확인하게 합니다.
- '다가가다 충돌하면 한 스텝 후퇴(0.01 m 스텝, 0.01 m 마진)'는 SceneSmith [snapping_helpers.py](https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/furniture_agents/tools/snapping_helpers.py)의 방식이고, 노이즈 σ 0.03 m / 1°(가구)는 [base_furniture_agent.yaml](https://raw.githubusercontent.com/nepfaff/scenesmith/main/configurations/furniture_agent/base_furniture_agent.yaml) 값입니다.
- 검사 항목은 [SceneEval](https://github.com/3dlg-hcvc/SceneEval)의 비VLM 지표(Collision, Navigability, Out of Bounds, Opening Clearance)와 같게 맞췄습니다. 나머지 6개(개수, 속성, 관계, 받침, 접근성 등)는 T07 비평이 봅니다.
- 이번 작성 중 확인한 함정: `obj.location`을 직접 바꾼 뒤 `view_layer.update()` 없이 `face_towards()`를 부르면 이전 위치 기준으로 회전해 내적이 0.96 정도로 어긋납니다(bpy 5.0.1). `placement_utils`의 이동 함수들은 내부에서 갱신하므로 문제없습니다.

---

## T07. 4뷰 비평: 체크리스트형, 큰 문제만

- **용도:** `review_views.py`가 만든 위·정면·측면·3/4 렌더를 보고, 큰 구조 문제만 골라 수치 있는 수정안으로 돌려줍니다. 사소한 미감을 두고 끝없이 반복하는 것을 막습니다.
- **언제:** 모든 단계의 루프 안(숫자 검사 통과 뒤). 가능하면 빌더와 다른 컨텍스트(읽기 전용 비평가 subagent)에서 돌립니다.

먼저 렌더를 만듭니다. 출력 폴더는 **절대 경로**로 넘기세요(`//review/`를 그대로 넘기면 루트 아래에 폴더가 생김).

```python
# GUI(MCP)에서는 Workbench가 가장 빠름. 헤드리스·GPU 없는 서버는 CYCLES.
import sys, bpy; sys.path.append(r"{{REPO}}/03_playbooks/scripts")
from review_views import render_review_views
print(render_review_views(bpy.path.abspath("//review/v{{N}}"), engine="BLENDER_WORKBENCH", res=768))
```

```text
너는 이 장면을 만들지 않은 리뷰어다. 코드와 대화 이력이 아니라 결과만 본다.
[입력] Image 1: top(위 정사영, 화면 위쪽 = +Y)  Image 2: front(-Y 쪽에서 봄)
       Image 3: side(+X 쪽에서 봄)  Image 4: persp(3/4 원근)  — 오브젝트마다 다른 색으로 칠해져 있다.
       기준: spec/spec_sheet.json, spec/acceptance.yaml. 숫자 검사 요약: {{AUDIT_SUMMARY}}
[절차]
1) 요청 충족 여부를 판정할 예/아니오 질문을 8~12개 먼저 만든다
   (부품 수, 접촉, 비율, 대칭, 두께, 방향, 동선, 모서리, 재질 경계 중에서).
2) 질문마다 [예 | 아니오 | 불확실] + 근거(Image 번호와 위치)로 답한다. 근거 이미지 없이 불만을 적지 않는다.
3) '아니오'만 모아 큰 구조 문제로 정리한다: 누락 부품, 떠 있는 지오메트리, 관통, 비율 오류, 정렬·방향 오류, 형태 오류.
   취향, 미세한 색감, 조명 미세 조정은 적지 않는다.
4) 문제마다 한 줄: object | 문제 | 근거(Image N) | 수정안(이동 m, 회전 °, 치수 m). 최대 3개, 영향이 큰 순.
5) (선택) 0~10점: Realism, Functionality, Layout, Completeness, Prompt Following, Reachability.
   숫자 검사에 관통이 1건이라도 있으면 Realism은 4점 이하.
6) 전체 100단어 이내. 마지막 줄: 큰 구조 문제가 없으면 NEEDS_FIX: NO, 있으면 NEEDS_FIX: YES
```

**종료 규칙**(T14와 같음): `NEEDS_FIX: NO`가 2회 연속 나오거나 루프가 최대 5회에 이르면 멈춥니다. 점수를 쓰면 모든 항목 9점 이상에서 조기 종료하고, 한 항목이 2점 이상 또는 총점이 1점 이상 떨어지면 직전 버전 복원을 **검토**합니다(자동 아님).

**왜 이렇게 쓰나**

- 3DCodeBench의 [비평 프롬프트](https://raw.githubusercontent.com/gaoypeng/3dcodebench/main/prompts/visual_critique_system_prompt_text.txt)는 누락 부품·떠 있는 지오메트리·비율·정렬·형태 오류만 100단어 이하로 적고 `NEEDS_FIX: NO/YES`로 끝내게 하며, 사소한 미감을 두고 반복하지 말라고 명시합니다. "2회 연속 또는 최대 5회"는 조사자가 제안한 종료 조건입니다.
- 예/아니오 질문을 먼저 만들고 답하게 하는 방식은 [CADCodeVerify](https://github.com/Kamel773/CAD_Code_Generation)(ICLR 2025)에서 왔습니다. 막연히 "잘 됐는지 봐 줘"라고 하면 VLM이 관대하게 통과시킵니다.
- 6개 항목, 9점 조기 종료, 관통 시 Realism ≤ 4, 점수 하락 시 롤백 검토는 SceneSmith [critic](https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/prompts/data/furniture_agent/stateful_critic_agent.yaml)·[planner](https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/prompts/data/furniture_agent/stateful_planner_agent.yaml) 설정입니다.
- 만든 에이전트가 자기 작업을 채점하지 않게 하려면 도구를 읽기 전용으로 제한한 subagent를 쓰세요([sub-agents 문서](https://code.claude.com/docs/en/sub-agents)). 출하 전 판정을 SHIP / SHIP WITH NOTES / NO-SHIP으로 받고 싶으면 [arjun988 qa-review](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/qa-review/SKILL.md)의 Blocker/Major/Minor 분류를 붙이면 됩니다. 비평가 정의 예시는 [에이전트 워크플로 가이드](../02_guides/09_agent_workflow_prompting.md) 8.3절에 있습니다.

---

## T08. 재질 지정 (PBR 규칙 포함)

- **용도:** 오브젝트별 재질을 PBR 규칙 안에서 지정하고, 규칙 위반을 표로 보고하게 합니다.
- **언제:** 플레이북 단계 7. 카메라와 라이트 v1이 고정된 뒤(평평한 조명에서 맞춘 재질은 실제 조명에서 틀려 보입니다).

```text
spec의 material_intent대로 재질을 만든다. 재질 1개 = 호출 1회.
PBR 규칙
- 재질 하나 = Material Output 1개 + Principled BSDF 1개. 노드를 비우고 다시 만든다(반복 실행해도 같게).
- 노드는 type으로, 소켓은 identifier로 찾는다(한국어 UI에서 이름이 번역될 수 있음).
- Metallic은 0 또는 1. 칠 벗겨짐 같은 전환부만 마스크로 섞는다.
- 비금속 albedo는 sRGB 30~240 안(순수 검정·흰색·원색 금지), 금속 Base Color는 밝게.
- Roughness는 슬라이더 값 하나로 두지 않는다. 노이즈·맵으로 공간 변화를 주고 0은 쓰지 않는다(최소 0.02).
- 이미지 텍스처 색공간: Base Color·Emission만 sRGB, 나머지(Roughness, Metallic, Normal 등)는 Non-Color.
  Normal은 Normal Map 노드를 거친다. albedo에 그림자·하이라이트(조명)를 굽지 않는다.
- Principled v2 입력명: Specular IOR Level, Coat Weight, Transmission Weight, Subsurface Weight, Sheen Weight, Emission Color.
- 유리: Transmission Weight 1, IOR 1.5, Cycles transmission bounces 16 이상. 래커: Coat Weight 0.8, Coat Roughness 0.05.
  벨벳: Sheen Weight 0.5. 기준 반사값은 02_guides/05_texturing_materials.md 표에서 가져온다.
끝나면 재질 표를 보여 줘: 재질 | 적용 오브젝트 | Base(linear) | Metallic | Roughness 범위 | 이미지 색공간 | 규칙 위반.
그다음 Material Preview(또는 짧은 렌더)로 확인한다. Solid 모드 스크린샷으로 판단하지 않는다.
```

```python
# 실행 확인: bpy 4.2.23 LTS / 5.0.1 (use_nodes 폐기 경고 없음, 두 번 실행해도 재질 3개)
import bpy

def sock(sockets, ident):
    """identifier로 소켓 찾기. UI 번역·비활성 소켓과 무관하게 동작."""
    for s in sockets:
        if s.identifier == ident:
            return s
    raise KeyError(ident)

def pbr_material(name, base_linear, metallic, roughness, rough_var=0.08, noise_scale=8.0, **extra):
    """get-or-create. metallic은 0 또는 1. rough_var = roughness 공간 변화 폭(±)."""
    assert metallic in (0, 1), "Metallic은 0 또는 1"
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if bpy.app.version < (5, 0, 0):
        mat.use_nodes = True            # 5.0+는 항상 노드를 쓰고 이 속성은 폐기 예고
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    nt.links.new(sock(bsdf.outputs, "BSDF"), sock(out.inputs, "Surface"))
    sock(bsdf.inputs, "Base Color").default_value = (*base_linear, 1.0)
    sock(bsdf.inputs, "Metallic").default_value = float(metallic)
    for ident, val in extra.items():                  # 예: Coat_Weight=0.8
        sock(bsdf.inputs, ident.replace("_", " ")).default_value = val
    noise = nt.nodes.new("ShaderNodeTexNoise")
    sock(noise.inputs, "Scale").default_value = noise_scale
    mr = nt.nodes.new("ShaderNodeMapRange")
    sock(mr.inputs, "To Min").default_value = max(0.02, roughness - rough_var)
    sock(mr.inputs, "To Max").default_value = min(1.0, roughness + rough_var)
    nt.links.new(sock(noise.outputs, "Fac"), sock(mr.inputs, "Value"))   # 5.0 표시 이름은 Factor, identifier는 Fac
    nt.links.new(sock(mr.outputs, "Result"), sock(bsdf.inputs, "Roughness"))
    return mat

pbr_material("M_wood_oak", (0.30, 0.17, 0.08), 0, 0.55)
pbr_material("M_steel_brushed", (0.56, 0.57, 0.58), 1, 0.25)          # RobLe3 materials 값
pbr_material("M_lacquer_black", (0.05, 0.05, 0.06), 0, 0.30, Coat_Weight=0.8, Coat_Roughness=0.05)
print("done: 3 materials")
```

**왜 이렇게 쓰나**

- Metallic 스위치, 코트·유리·벨벳 값, 유리 bounces 16 이상은 [RobLe3 materials](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-materials/SKILL.md) 값입니다("Metallic is a switch, not a slider").
- albedo sRGB 30~240(범위 밖 픽셀 2% 미만), roughness 맵 표준편차 > 0.01 같은 감사 기준은 [scenario texturing-shading](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/dcc/blender/scenario-blender-texturing-shading/SKILL.md) 스킬의 값입니다. 업계 표준이 아니라 해당 스킬의 자체 기준입니다.
- 비활성 소켓(예: `Subsurface IOR`)은 문자열 키로 접근하면 KeyError가 납니다(검증에서 bpy 5.0.1로 확인). 그래서 목록을 돌며 identifier로 찾습니다. 5.0의 Noise 출력은 표시 이름이 `Factor`로 바뀌었지만 identifier는 `Fac`입니다(이번 작성 중 확인). 한국어 UI에서는 Preferences > Interface > Translation의 New Data(`use_translate_new_dataname`)가 켜져 있으면 새 노드 이름이 번역될 수 있는데, pip `bpy` 공장 기본값이 5.0.1에서는 켜짐, 4.2.23에서는 꺼짐이었습니다(이번 작성 중 확인, 실제 번역 동작은 미확인).
- 재질 수치의 기준표와 PBR 자동 감사 코드(`pbr_audit`)는 [텍스처링·재질 가이드](../02_guides/05_texturing_materials.md)에 있습니다.

---

## T09. 라이팅 셋업

- **용도:** 색관리 → 키 → 필 → 림 순서로 조명을 세우고, 광원마다 존재 이유(색온도, 크기, 거리)를 적게 합니다.
- **언제:** 플레이북 단계 3(라이트 v1: 무채색·형태 확인용)과 8(라이트 v2: 색온도·비율).

```text
조명을 새로 세운다. 기존 라이트는 숨긴 컬렉션으로 옮겨 두고(삭제 금지) 검정에서 시작한다.
1) 색관리 먼저: View Transform = AgX, Look = "AgX - Medium High Contrast".
   색 정확도가 중요한 제품샷이면 Khronos PBR Neutral. Standard는 쓰지 않는다.
   전체 밝기는 램프 세기가 아니라 view_settings.exposure로 조절한다(광량비 보존).
2) 광원은 하나씩 추가하고, 추가할 때마다 이유를 한 줄로 쓴다: 이름 | 역할 | K | 크기 m | 거리 m | W.
   색은 RGB를 추측하지 말고 켈빈으로: 촛불 1800, 텅스텐 3200, 주광 5500, 흐림 6500, 달빛 8000 이상.
   광원 크기는 0으로 두지 않는다(크기가 곧 그림자 부드러움). 태양 각도: 선명 0.5°, 부드럽게 2~5°.
3) 키: 카메라–피사체 축에서 수평 40°, 위로 35°, 거리 = 피사체 반경 × 3, 크기 = 피사체 반경.
   카메라 축에서 20° 안쪽의 정면 키는 금지(평평해짐).
4) 비율: 기본 key:fill 3~4:1로 시작하고 레퍼런스의 그림자 밀도에 맞춰 조정한다.
   재질별 출발점(key:fill:rim): 금속 4:1:2, 유리 3:1:1.2, 나무 4:1:1.5, 패브릭 3:1:0.5, 피부 4:1:1, 제품 5:1:1.5.
5) 실내: World(HDRI) 기여는 작게(스킬 기준 10% 미만), 실용광(스탠드·펜던트)을 주광원으로.
   HDRI를 쓰면 strength 0.5~2.0에서 시작한다.
6) 확인: View Transform을 잠시 False Color로 바꿔 노출을 보고(발광체 외 클리핑 ≤ 0.5%) 다시 AgX로.
   AgX는 클리핑을 부드럽게 숨기므로 표시 이미지만 보고 판단하지 않는다.
보고: 조명 표, exposure 값, False Color 판정, 짧은 렌더 경로. 끝에 "STATUS: WAITING_FOR_LOOK_CHECK".
```

```python
# 실행 확인: bpy 4.2.23 LTS / 5.0.1 (키가 카메라 축에서 수평 40°, 피사체를 정확히 겨눔)
import bpy, math
from mathutils import Vector, Matrix

def area_light(name, kelvin, energy_w, size_m):
    ld = bpy.data.lights.get(name) or bpy.data.lights.new(name, "AREA")
    ld.energy, ld.size = energy_w, size_m
    if hasattr(ld, "use_temperature"):           # 5.x: 켈빈 직접 지정 (4.2에는 속성 없음)
        ld.use_temperature, ld.temperature = True, kelvin
        ld.color = (1.0, 1.0, 1.0)               # 켈빈을 켜면 color는 곱해지는 틴트가 됨
    ob = bpy.data.objects.get(name) or bpy.data.objects.new(name, ld)
    if ob.name not in bpy.context.scene.collection.all_objects:
        bpy.context.scene.collection.objects.link(ob)
    return ob

def aim_from_camera(light_ob, target, cam_loc, az_deg, el_deg, dist):
    """카메라→피사체 축에서 수평 az°, 위로 el° 돌린 방향으로 dist m 떨어뜨리고 피사체를 겨눔."""
    t, c = Vector(target), Vector(cam_loc)
    h = c - t; h.z = 0.0; h.normalize()
    h = Matrix.Rotation(math.radians(az_deg), 3, "Z") @ h
    d = h * math.cos(math.radians(el_deg)); d.z = math.sin(math.radians(el_deg))
    light_ob.location = t + d * dist
    light_ob.rotation_euler = (t - light_ob.location).to_track_quat("-Z", "Y").to_euler()

TARGET, CAM, R = (0.0, 0.0, 0.45), (2.2, -2.6, 1.1), 0.5    # 피사체 중심, 카메라 위치, 피사체 반경(m)
K, F, RIM = 4, 1, 1.5                                       # 나무 출발점 4:1:1.5
dist = 3 * R
key_w = 100 * (dist / 1.5) ** 2                              # 거리 기반 에너지 공식(RobLe3)
aim_from_camera(area_light("LGT_key", 3200, key_w, R), TARGET, CAM, 40, 35, dist)
aim_from_camera(area_light("LGT_fill", 5500, key_w * F / K, 2 * R), TARGET, CAM, -60, 15, dist * 1.3)
aim_from_camera(area_light("LGT_rim", 6500, key_w * RIM / K, R), TARGET, CAM, 160, 40, dist)
vs = bpy.context.scene.view_settings
vs.view_transform, vs.look, vs.exposure = "AgX", "AgX - Medium High Contrast", 0.0
print("done: LGT_key/fill/rim", round(key_w), "W key")
```

- Blender 4.2 LTS에는 라이트 켈빈 속성(`use_temperature`)이 없어서 위 코드는 색을 기본 흰색으로 둡니다(이번 작성 중 확인). 4.x에서는 RGB로 직접 지정하세요.
- bpy로 새로 만든 라이트의 기본 반경(`radius`)은 0이라 점·스폿 라이트는 칼 같은 그림자가 나옵니다(검증: DNA 기본값). Look 이름은 `AgX - Medium High Contrast`처럼 접두사까지 써야 합니다(`Medium High Contrast`만 쓰면 오류).

**왜 이렇게 쓰나**

- 키 40°/35°/반경 3배, 정면 키 20° 경고, 실내 World 10% 미만, 클리핑 ≤ 0.5%, exposure로 밝기 조절, AgX가 선형 4.0을 0.91로 보여 클리핑을 숨긴다는 점은 [scenario lighting-rendering](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/dcc/blender/scenario-blender-lighting-rendering/SKILL.md) 스킬에서 왔습니다(Blender 5.2.1 테스트 명시, 게이트 수치는 스킬 자체 정의).
- 재질별 비율과 에너지 공식은 [RobLe3 lighting](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-lighting/SKILL.md), 켈빈 표와 HDRI strength는 [arjun988 lighting](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/lighting/SKILL.md)입니다. 필 비율은 소스마다 다르므로 "기본값 + 레퍼런스에 맞춰 조정"으로 적었습니다.
- 켈빈 속성과 기본값(6500K, radius 0, 태양 0.526°)은 Blender 소스([properties_data_light.py v5.2.2](https://raw.githubusercontent.com/blender/blender/v5.2.2/scripts/startup/bl_ui/properties_data_light.py))로 검증됐고, 뷰 목록(AgX, ACES 1.3/2.0, Khronos PBR Neutral, False Color)은 [config.ocio v5.2.2](https://raw.githubusercontent.com/blender/blender/v5.2.2/release/datafiles/colormanagement/config.ocio)에 있습니다. ACES 2.0은 4.2에 없습니다.
- 더 자세한 조명·아트디렉션 규칙은 [라이팅·렌더 가이드](../02_guides/06_lighting_rendering_art_direction.md)에 있습니다.

---

## T10. 최종 렌더

- **용도:** 뷰포트 스크린샷이 아니라 **실제 렌더 파일**로 최종 판단하게 하고, 렌더 설정·출력 형식·게이트를 고정합니다.
- **언제:** 플레이북 단계 10, 게이트 G3 직전.

```text
최종 렌더를 준비한다. 긴 렌더를 MCP로 돌리지 않는다(커뮤니티 서버 소켓 타임아웃 180초, Claude Code 유휴 타임아웃 stdio 30분·HTTP 서버 5분).
1) 렌더 전 점검: scene.camera 존재, 카메라·구도 G2 이후 변경 없음, scene_audit 0건, 색관리 AgX 유지.
2) Cycles 설정: 기본 상한(samples 4096) + adaptive threshold 0.01, 디노이즈 OIDN(입력 Albedo+Normal, prefilter Accurate).
   유리가 많으면 transmission bounces 16 이상. 실용광이 많은 실내는 max bounces 16 이상.
3) 출력: OpenEXR MultiLayer 16-bit DWAA(마스터) + 확인용 PNG. PNG에는 뷰 변환이 구워진다.
4) 실행: 설정을 저장한 .blend를 헤드리스로 렌더한다.
   blender -b versions/{{FILE}}.blend --python-exit-code 1 -P scripts/render_final.py -- --out renders/{{SHOT}}
5) 렌더 파일을 직접 열어 본다. 렌더를 보지 않고 완료라고 말하지 않는다.
6) 게이트: 발광체 외 클리핑 ≤ 0.5%, 카메라 축 20° 이내 정면 키 없음, T07 비평 NEEDS_FIX: NO.
   EEVEE로 반복했다면 Cycles 레퍼런스 한 장과 비교한다.
보고: 렌더 경로, 해상도, 샘플, 소요 시간, 파일 크기, 게이트 결과, 남은 결함. 끝에 "STATUS: WAITING_FOR_G3".
```

```python
# 실행 확인: bpy 4.2.23 LTS / 5.0.1 (scripts/render_final.py 안에 두는 설정 부분)
import bpy

def final_cycles(scene, samples=4096, glass=False, practicals=False):
    scene.render.engine = "CYCLES"
    c = scene.cycles
    c.samples, c.use_adaptive_sampling, c.adaptive_threshold = samples, True, 0.01
    c.use_denoising, c.denoiser = True, "OPENIMAGEDENOISE"
    c.denoising_input_passes, c.denoising_prefilter = "RGB_ALBEDO_NORMAL", "ACCURATE"
    if glass:
        c.transmission_bounces = max(c.transmission_bounces, 16)
    if practicals:
        c.max_bounces = max(c.max_bounces, 16)

def exr_multilayer(scene):
    ims = scene.render.image_settings
    if hasattr(ims, "media_type"):           # 5.0+: media_type을 먼저 바꿔야 멀티레이어 포맷이 선택지에 나타남
        ims.media_type = "MULTI_LAYER_IMAGE"
    ims.file_format, ims.color_depth, ims.exr_codec = "OPEN_EXR_MULTILAYER", "16", "DWAA"

sc = bpy.context.scene
assert sc.camera is not None, "카메라 없음"
final_cycles(sc, glass=True)
exr_multilayer(sc)
print("done:", sc.render.engine, sc.cycles.samples, sc.render.image_settings.file_format)
```

- **Blender 5.0 함정(이번 작성 중 확인):** `image_settings.file_format = "OPEN_EXR_MULTILAYER"`는 `media_type = "MULTI_LAYER_IMAGE"`를 먼저 설정하지 않으면 "enum not found" 오류가 납니다. 4.2에는 `media_type` 속성이 없습니다.
- `--python-exit-code 1`을 빼면 스크립트가 예외를 내도 종료 코드가 0이라 에이전트가 성공으로 오인합니다([yardstake-ux #151](https://github.com/captproton/yardstake-ux/issues/151)).
- EEVEE 식별자는 5.0부터 `BLENDER_EEVEE`, 4.2~4.5는 `BLENDER_EEVEE_NEXT`입니다. 레거시 `use_bloom`·`use_ssr`·`use_gtao`는 없으니 bloom은 컴포지터 Glare 노드로 만듭니다. Glare는 4.4부터 소켓 방식이라 Strength·Size 0~1, Iterations 2~5 범위를 씁니다(옛 튜토리얼의 Mix −0.7, Size 8~9는 입력 불가, [glare 소스 v5.2.2](https://raw.githubusercontent.com/blender/blender/v5.2.2/source/blender/nodes/composite/nodes/node_composite_glare.cc)).
- Unreal로 마무리한다면 MRQ·Path Tracer 설정은 [라이팅·렌더 가이드](../02_guides/06_lighting_rendering_art_direction.md)를 보세요.

**왜 이렇게 쓰나**

- MCP for Blender에는 전용 렌더 툴이 없습니다(요청 [#61](https://github.com/ahujasid/blender-mcp/issues/61)은 not planned로 닫힘). 뷰포트 스크린샷은 최종 색관리·GI·DOF와 다르므로 실제 렌더를 파일로 저장해 읽어야 합니다. `BLENDER_MCP_SAFE_MODE=1`에서도 bpy를 통한 렌더·저장은 허용됩니다(검증).
- Cycles 기본값(4096 samples, adaptive 0.01, OIDN + Albedo/Normal, Accurate prefilter)은 이미 프로덕션급입니다([properties.py v5.2.2](https://raw.githubusercontent.com/blender/blender/v5.2.2/intern/cycles/blender/addon/properties.py)). 장면 유형에 따라 bounces만 올리면 됩니다.
- "렌더를 직접 보지 않고 완료 보고 금지"와 EEVEE–Cycles 비교는 [scenario-blender-expert](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/dcc/blender/scenario-blender-expert/SKILL.md)·lighting 스킬 규칙입니다.

---

## T11. 이미지→3D용 레퍼런스 이미지 생성

- **용도:** 유기체·조형물·복잡한 소품처럼 코드로 만들기 어려운 대상을 image-to-3D로 만들 때, 입력 이미지를 생성기에 맞는 조건으로 만들고 사람이 고르게 합니다.
- **언제:** 플레이북 단계 4(에셋 조달 결정)에서 '생성'을 고른 경우. 가구·하드서피스처럼 단순한 형태는 코드 모델링(T03·T04)이 치수와 토폴로지 모두 정확합니다.

```text
[레퍼런스 이미지 → 3D 입력용]
대상: {{DESCRIPTION}}  목표 치수: {{W×D×H m}}  용도: {{USE}}
1) 영어 이미지 프롬프트로 바꾼다. 반드시 포함: single object, centered, plain light-grey background,
   three-quarter view, soft even studio lighting, realistic shading, no text, no logo, no props.
   캐릭터면 T-pose 또는 A-pose. 바닥·배경·환경은 생성하지 않는다.
2) 실존 브랜드·디자이너·작품 이름은 쓰지 않고 형태·재료·시대로만 묘사한다.
3) 멀티뷰를 쓰는 생성기라면 필요한 장수와 순서를 스키마에서 먼저 확인해 적는다(모델마다 다름).
4) 후보 {{N}}장 생성 계획과 예상 크레딧을 먼저 보여 주고 멈춘다: STATUS: WAITING_FOR_COST_APPROVAL
5) 승인 후 생성하고 후보를 Image 1..N으로 보여 준다. 내가 하나를 고르기 전에는 3D 생성을 호출하지 않는다.
6) 3D 생성 호출 시 모델 버전을 명시하고, 크기 옵션(bbox·height 등)이 있으면 목표 치수를 넘긴다.
   결과는 받자마자 로컬에 저장하고 T12로 정리한다.
금지: Hunyuan3D 계열(로컬 실행, 클라우드 경유, MCP 서버의 연동 기능 모두), 라이선스를 모르는 이미지 모델,
      NoAI 태그가 붙은 이미지를 입력으로 쓰기.
```

**왜 이렇게 쓰나**

- kiln 규칙: 컨셉 이미지는 배경이 없거나 흰 배경의 단일 뷰, 캐릭터는 T-pose, 바닥·환경은 AI로 생성하지 않음, 에셋은 한 번에 하나([blender-kiln](https://raw.githubusercontent.com/elithril/blender-kiln/main/SKILL.md)).
- 유료 생성 전 매번 승인: Codex + Higgsfield 사례의 규칙 "Higgsfield kostet Credits, frag vor jeder Generierung"([codex-blender-higgsfield](https://github.com/Arnie936/codex-blender-higgsfield)). MCP for Blender의 Tripo 생성은 유료 Premium 전용입니다(검증).
- 조명이 구워진 텍스처는 새 조명 아래에서 광원이 두 개인 것처럼 보이므로 고른 스튜디오 조명을 요구합니다. Hunyuan3D 2.1이 RGB 텍스처에서 PBR 파이프라인으로 옮긴 이유이기도 합니다.
- **[한국 사용자]** Tencent Hunyuan3D 2.0/2.1/Omni/Part, HY-World, HY-Motion 오픈웨이트 라이선스는 적용 지역에서 EU·영국·대한민국을 빼고, 그 밖에서의 사용과 출력물 사용을 무허가로 규정합니다([Hunyuan3D-2.1 LICENSE](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/LICENSE)). Tencent Cloud API 약관은 별개이며 원문을 확인하지 못했습니다(미확인).
- 생성기별 선택, 배경 제거 가중치의 라이선스 함정, 멀티뷰 순서 표는 [AI 3D 생성 가이드](../02_guides/04_ai_3d_generation.md) 4~5장에 있습니다.

---

## T12. 에셋 임포트 정리

- **용도:** 라이브러리나 생성기에서 가져온 에셋을 배치 가능한 상태(이름·스케일·원점·정면·메시·출처)로 정규화합니다. 배치 품질의 절반이 여기서 갈립니다.
- **언제:** 플레이북 단계 4~5. 에셋을 가져올 때마다(한 번에 하나).

```text
방금 가져온 {{ASSET}}을 정리한다. 한 번에 에셋 하나만 다룬다.
1) 출처 기록: source_url, author, license, tool과 model_version, date를 커스텀 프로퍼티(prov_*)와
   provenance/assets.csv에 쓴다. 라이선스를 확인할 수 없으면 여기서 멈추고 보고한다.
   CC-BY 에셋은 저작자 표기 문자열을 지우지 않는다.
2) 이름: 규약대로 즉시 바꾼다. 유닛 {{unit_name}}(영어 snake_case, 카테고리 단어 포함), 부품 {{unit_name}}_<part>, 재질 M_<type>_<variant>.
3) 트랜스폼: 회전·스케일을 적용한다. 목표 치수 {{DIMS_M}}에는 최대 축 기준 **균등** 스케일로 맞춘다(비균등 금지).
4) 원점 = bbox 바닥 중앙, 정면 = -Y. 정면이 불확실하면 4방향 렌더를 보고
   서랍·좌면·화면이 보이는 쪽을 고른 뒤 Z 회전만 바꾼다.
5) 메시: merge by distance 0.0001 m, 노멀 재계산, non-manifold 개수 보고.
6) 재질: albedo에 그림자·하이라이트가 구워져 있으면(생성 에셋에서 흔함) 보고하고 PBR 재질 교체를 제안한다.
7) 검증: scene_audit(해당 유닛 issues), review_views top/front, 치수(m)·삼각형 수·재질 수를 표로 보고한다.
끝에 "done:<unit_name> dims=… tris=… license=…" 한 줄.
```

- 정규화 코드는 두 곳에 실행 확인된 버전이 있습니다: 생성 에셋용은 [AI 3D 생성 가이드](../02_guides/04_ai_3d_generation.md) 6.2절, 배치용은 [배치 가이드](../02_guides/08_scene_layout_placement.md) 4.1절.
- MCP for Blender로 Poly Pizza 에셋을 받으면 약 69%가 CC-BY라 저작자 표기 문자열이 커스텀 프로퍼티로 저장됩니다. `licence='CC0'` 필터로 표기 의무를 피할 수 있고, `normalize_size`·`target_size`로 크기를 맞출 수 있습니다([server.py](https://raw.githubusercontent.com/ahujasid/blender-mcp/main/src/blender_mcp/server.py)).

**왜 이렇게 쓰나**

- kiln 규칙: 가져온 에셋은 출처와 상관없이 즉시 규약대로 이름을 바꾸고(Rule 25), 라이선스와 출처를 로그로 남깁니다(Rule 17)([blender-kiln](https://raw.githubusercontent.com/elithril/blender-kiln/main/SKILL.md)). kiln의 규칙은 모두 31개(core 26 + batch 5)입니다(검증 정정).
- 정면·스케일 정규화 실패는 배치 연구에서 반복된 문제입니다: 에셋 정면 정렬 혼란([Holodeck #92](https://github.com/allenai/Holodeck/issues/92)), 메시 스케일·회전 정규화 문제([LayoutVLM #9](https://github.com/sunfanyunn/LayoutVLM/issues/9)), 정면 규약 불일치를 +π로 보정하고 비균등 스케일로 비율을 왜곡한 코드([I-Design place_in_blender.py](https://raw.githubusercontent.com/atcelen/IDesign/main/place_in_blender.py)).
- glTF 원본의 정면은 +Z이고 Blender로 가져오면 -Y가 됩니다([glTF 2.0 스펙](https://raw.githubusercontent.com/KhronosGroup/glTF/main/specification/2.0/Specification.adoc)). 규약을 -Y로 통일하면 이 변환이 그대로 맞습니다.

---

## T13. 게임레디 변환

- **용도:** 렌더용으로 만든 에셋을 게임 엔진이나 웹에서 쓰는 GLB/FBX로 바꾸고, 형상이 망가지지 않았는지 확인합니다.
- **언제:** 플레이북 단계 11, 게이트 G4 직전.

| 변수 | 예 |
|---|---|
| `{{ENGINE}}` | Unreal 5.8 / Godot / 웹(three.js) |
| `{{TRI}}` | 게임 소품 3k~8k, 일반 에셋 10k~50k |
| `{{TEX}}` | 2048(로우폴리 1024) |

```text
{{ASSET}}을 {{ENGINE}}용으로 변환한다. 원본 .blend는 versions/에 두고 사본에서 작업한다.
목표: 삼각형 ≤ {{TRI}}, 텍스처 {{TEX}}, 포맷 {{GLB|FBX}}, LOD {{있음|없음}}.
1) 절차적 요소 정리: Bevel 셰이더 노드, Noise·Voronoi·ColorRamp 같은 절차적 텍스처는 이미지로 bake한다.
   지오메트리 노드는 export 전에 직접 적용한다(glTF export가 조용히 버린다).
2) 감량·삭제는 "제안 → before/after 렌더 비교 → 내 선택" 순서로만 한다. auto 모드에서도 같다.
3) 8항목 체크를 표로 보고한다:
   ① 모든 재질이 Principled BSDF ② Base Color/Normal/Roughness/Metallic 텍스처 포함
   ③ UV 겹침·늘어짐 ④ 모든 transform 적용 ⑤ merge by distance 0.0001 m ⑥ 노멀 재계산
   ⑦ 쓰지 않는 데이터는 이름을 지정해 명시적으로 삭제(orphans_purge 금지) ⑧ 임시 GLB 크기(웹 기준 50 MB 넘으면 경고)
4) export: 최적화는 gltf-transform의 개별 명령(dedup → weld → 텍스처 resize/WebP → Draco)으로 하고,
   optimize 한 방은 쓰지 않는다(simplify가 형상을 망가뜨림). LOD는 gltfpack으로 따로 만든다.
   MCP export가 타임아웃되면 헤드리스 CLI로 전환한다.
5) 검증: 다시 가져와서 메시 수·재질 슬롯·이름 접두사 확인 → review_views 4뷰로 원본과 비교 → 엔진 import 테스트.
보고: 원본/결과 삼각형, 파일 크기, 텍스처 목록, 8항목 결과, 남은 문제. 끝에 "STATUS: WAITING_FOR_G4".
```

**왜 이렇게 쓰나**

- 8항목 체크, `gltf-transform optimize` 금지, 지오노드 사전 적용(kiln은 `export_apply=False`로 두고 직접 적용), 파괴적 작업의 제안·비교·선택, MCP 타임아웃 시 헤드리스 전환은 모두 [blender-kiln](https://raw.githubusercontent.com/elithril/blender-kiln/main/SKILL.md) 규칙입니다. kiln은 대화형 MCP 경로와 헤드리스 경로의 결과가 바이트 단위로 같았다고 보고합니다(111.9 kB GLB, 2,202 tris). 15개 에셋 갤러리는 1,456 kB에서 133 kB로 91% 줄었습니다(작성자 보고).
- Bevel 셰이더 노드는 Cycles 전용이라 게임 export 전에 bake해야 합니다([scenario texturing-shading](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/dcc/blender/scenario-blender-texturing-shading/SKILL.md)).
- 삼각형 예산 참고: arjun988 스킬팩 예시는 사실적 소품 3k tris, 캐릭터 15k([blender-skills](https://github.com/arjun988/blender-skills)). 더 자세한 예산·LOD·충돌체 기준은 [AI 3D 생성 가이드](../02_guides/04_ai_3d_generation.md) 7장, 라이선스·provenance는 [에셋·라이선스 가이드](../02_guides/10_assets_pipeline_licensing.md)를 보세요.

---

## T14. 비용 제한·중단 조건

- **용도:** 킥오프 메시지 끝에 붙여서 에이전트가 스스로 멈출 조건과 돈을 쓰기 전 확인 절차를 정합니다.
- **언제:** 세션 시작 시 한 번. 긴 무인 실행(`/goal`, auto mode) 전에는 반드시.

| 변수 | 예 |
|---|---|
| `{{PROFILE}}` | fast(체크포인트 1회, 수정 1회, 최대 1280×720) / standard(블록아웃·조명·재질 뒤 체크포인트, 수정 2회, 1920×1080) / cinematic(모든 단계 게이트, 수정 4회) |
| `{{MAX_CALLS}}` | 툴 호출 80회 |
| `{{PAID_LIMIT}}` | 유료 생성 0회 또는 크레딧 한도 |

```text
[예산·중단]
- 품질 프로필: {{PROFILE}}. 단계마다 수정 라운드는 프로필 상한까지, 전체 루프는 최대 5회.
- 툴 호출 상한 {{MAX_CALLS}}회. 80%에 이르면 남은 계획을 보여 주고 계속할지 묻는다.
- 스크린샷은 긴 변 1000px 이하. 최종 판정에만 큰 렌더를 쓴다. 한 요청에 이미지가 20장을 넘으면 각 변 2000px 이하.
- 유료 호출(3D·이미지 생성, 유료 에셋): 호출마다 예상 크레딧과 누적 합계를 먼저 보여 주고 승인을 기다린다.
  누적이 {{PAID_LIMIT}}에 닿으면 멈춘다.
- 멈춤 조건(하나라도 해당하면 STOP하고 보고):
  a) 같은 결함이 두 번 고쳐도 남는다
  b) 비평 점수가 한 항목 2점 이상 또는 총점 1점 이상 떨어졌다 → 직전 버전 복원을 제안한다
  c) 실행 오류가 같은 원인으로 3번 났다
  d) 180초 타임아웃이 두 번 났다 → 헤드리스 전환을 제안한다
  e) 라이선스를 모르는 에셋, 파괴적 작업(삭제·decimate·remesh), 새 유료 서비스가 필요하다
  f) 호출 상한 또는 유료 한도에 닿았다
- 성공 종료: acceptance 하드 게이트 전부 통과 AND 비평 NEEDS_FIX: NO 2회 연속 AND 해당 게이트 승인.
- STOP 보고 형식: STOP_REASON | 현재 버전 파일 | audit 요약 | 남은 결함 상위 3개 | 다음에 할 일 제안.
```

**긴 무인 실행용 `/goal` 예시(Claude Code)**

```text
/goal blender-critic 서브에이전트가 NEEDS_FIX: NO를 2회 연속 출력하고, scene_audit 요약에서
units_with_issues 0과 interpenetrating_pairs 0이 출력되고, versions/에 최신 .blend 저장 로그가 출력될 것.
20턴이 지나면 중단.
```

`/goal` 평가자는 파일을 읽거나 명령을 실행하지 않고 대화에 드러난 내용만 봅니다. 그래서 수치와 판정을 **텍스트로 출력**하게 조건을 씁니다([/goal 문서](https://code.claude.com/docs/en/goal), 조건 최대 4,000자, 기본 평가 모델 Haiku).

**컨텍스트가 오염됐을 때 재개 프롬프트**

```text
같은 문제를 두 번 고쳤는데도 남아 있다. PROGRESS.md에 다음을 적고 멈춰:
spec 경로, 현재 단계, 최신 버전 파일, 오브젝트 인덱스(유닛 이름·치수), 결함 원장(미해결만), 시도한 방법과 실패 이유.
(사람이 /clear 한 뒤) → "PROGRESS.md를 읽고 {{STAGE}} 단계부터 재개. 실패한 방법은 다시 쓰지 마."
```

**비용 감(가정 기반 추정)**

| 항목 | 값 | 근거 |
|---|---|---|
| 세션 비용 | 툴 호출 60회, 평균 컨텍스트 80k 가정에서 Sonnet 5 약 $2.5, Opus 5.5 약 $4.0, Fable 5.1 약 $8.7 | [pricing](https://platform.claude.com/docs/en/about-claude/pricing) 단가로 계산(검증에서 산술 확인, 실측 아님) |
| 단가(입력/출력, 1M 토큰) | Opus 5.5 $4/$20, Sonnet 5 $2/$10, Fable 5.1 $10/$50 | 같은 문서 |
| 이미지 토큰 | ⌈w/28⌉×⌈h/28⌉. 1000×563 약 756토큰, 1920×1080은 Opus 5.5에서 2,691토큰 | [vision 문서](https://platform.claude.com/docs/en/build-with-claude/vision) |
| 툴 스키마 | MCP for Blender 스키마 약 6,928토큰(툴 28개 시점 측정, 현재 36개라 더 클 가능성) | [issue #347](https://github.com/ahujasid/blender-mcp/issues/347) |
| 참고 | Claude Code 기업 평균은 활동일 기준 개발자 1인당 약 $13 | [costs 문서](https://code.claude.com/docs/en/costs) |

**왜 이렇게 쓰나**

- 품질 프로필 3단계는 [claude-3d-harness](https://github.com/MAX-786/claude-3d-harness)가 체크포인트 수·수정 횟수·해상도로 품질과 비용을 수치화한 방식입니다(fast 64spp, standard 256spp, cinematic 512spp).
- 점수 하락 롤백 기준은 SceneSmith 설정이고, 롤백은 자동이 아니라 planner가 "강하게 고려"하는 방식입니다(검증 정정).
- "같은 문제로 두 번 교정했다면 컨텍스트가 실패한 시도로 오염된 상태이니 새로 시작하라"는 Claude Code 공식 권고입니다([best-practices](https://code.claude.com/docs/en/best-practices)). `/rewind`는 MCP로 바꾼 Blender 상태를 되돌리지 못하므로 `.blend` 버전 저장이 필수입니다.
- MCP 출력이 10,000토큰을 넘으면 경고, 기본 한도는 25,000토큰(`MAX_MCP_OUTPUT_TOKENS`)입니다. 긴 렌더는 유휴 타임아웃(`CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`, 기본값 stdio 서버 30분·HTTP 서버 5분)에 걸릴 수 있습니다([MCP 문서](https://code.claude.com/docs/en/mcp)).
- Codex에서 GPT-6 Astra를 effort 지정 없이 돌리면 기본값 low로 실행되어 비교가 무효가 됩니다([AI 모델 가이드](../02_guides/01_ai_models_and_clients.md)).

---

## 15. 공개된 실제 프롬프트·스킬 문구 (원문)

템플릿을 고칠 때 원래 표현을 확인할 수 있게 모았습니다. 원문이 영어면 그대로 적었습니다.

| 문구 | 출처 | 쓰인 템플릿 |
|---|---|---|
| "Make sure to do it step-by-step by breaking it into smaller chunks" | MCP for Blender `execute_blender_code` 설명([server.py](https://raw.githubusercontent.com/ahujasid/blender-mcp/main/src/blender_mcp/server.py)) | T04 |
| 항상 `get_scene_info` 먼저, 변경 전후 `get_viewport_screenshot`(내장 프롬프트 `asset_creation_strategy`의 요지) | 같은 파일 | 0.3, T06 |
| 노드는 type으로 찾고 enum을 하드코딩하지 말 것, `diffuse_color`는 뷰포트 전용(서버 instructions 요지) | 같은 파일 | T08 |
| "ALWAYS save your work before using it" | [MCP for Blender README](https://github.com/ahujasid/blender-mcp) | 0.3, T14 |
| 예시 프롬프트 "Create a beach vibe using HDRIs, textures, and models like rocks and vegetation", "Fill this room with low-poly furniture from Poly Pizza" | 같은 README | — |
| "Validate the blockout reads. Don't proceed to modeling/lighting until composition is locked" / "A perfect material tuned in flat lighting will look wrong once real lighting goes in." | [RobLe3 pro-workflow](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-pro-workflow/SKILL.md) | T08, T09 |
| "A render passing every numerical check can still look completely wrong." / "If the render is obviously wrong, do NOT report success." | [RobLe3 text-to-blender](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/text-to-blender/SKILL.md) | T07, T10 |
| "Use $create-3d-model to create a low-poly desk lamp from my description. Inspect the current scene first and do not delete existing objects. Capture and inspect screenshots after the blockout and final version. Export a GLB and preserve a versioned Blender source." | [CheshireJCat Codex 스킬 README](https://raw.githubusercontent.com/CheshireJCat/create-3d-model-skill/main/README.md) | T01(Codex 호출 예) |
| "get_scene_info() does NOT carry dimensions"(Rule 24) | [blender-kiln](https://raw.githubusercontent.com/elithril/blender-kiln/main/SKILL.md) | 0.4 |
| "A passing technical validator does not mean an asset looks good." | [blender-art-factory](https://github.com/ErikBurdett/blender-art-factory) | T07 |
| "(1) After every execute() call measure(); (2) After assembly positioning call compare(); (3) Only after (1) and (2) pass call render_view()" | [build123d-mcp default_prompt](https://raw.githubusercontent.com/pzfreo/build123d-mcp/main/default_prompt.md) | T04 |
| "Plausible mesh bevels provide real highlight surfaces on manufactured edges" | [blender-production realism.md](https://raw.githubusercontent.com/per-simmons/blender-production/master/references/realism.md)(미검증 저장소) | T03 |
| 비평은 큰 구조 문제만, 사소한 미감 반복 금지, `NEEDS_FIX: NO/YES` | [3DCodeBench 비평 프롬프트](https://raw.githubusercontent.com/gaoypeng/3dcodebench/main/prompts/visual_critique_system_prompt_text.txt) | T07 |
| check_physics로 충돌 0 확인 전 완료 금지, 못 풀면 객체 삭제 | [SceneSmith designer](https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/prompts/data/furniture_agent/designer_agent.yaml) | T06 |
| "Analyze the scene and list the outliers: objects with highest polygon count but smaller size from the camera point of view" | [Blender Lab MCP 페이지](https://www.blender.org/lab/mcp-server/)(검색 요약으로만 확인) | 분석용 첫 프롬프트 |
| "Always use Context7 when I need library/API documentation, code generation, setup or configuration steps without me having to explicitly ask." | [Context7 README](https://github.com/upstash/context7) | CLAUDE.md |
| "Higgsfield kostet Credits, frag vor jeder Generierung" | [codex-blender-higgsfield](https://github.com/Arnie936/codex-blender-higgsfield) | T11, T14 |
| "Localhost is not a trust boundary" | [Epic Claude Code 플러그인](https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin) | 보안 |

---

## 흔한 실수와 해결

| 증상 | 원인 | 해결 |
|---|---|---|
| "의자 만들어 줘" 한 줄에 비율이 이상한 결과 | 치수·부품·재질을 모델이 추측 | T01·T03으로 스펙부터, 치수표 값과 근거를 적게 함 |
| '고급스럽게'를 넣었는데 달라지지 않음 | 형용사는 코드로 번역되지 않음 | 치수, bevel 폭, 켈빈, 비율 같은 숫자로 바꿈 |
| 한 번에 방 전체를 만들다 180초 타임아웃·반쯤 만들어진 장면 | 긴 코드 한 방 | 호출 1회 = 부품 1개(T04), 긴 렌더·export는 헤드리스 |
| 가구가 떠 있거나 파묻힘, 방향이 180° 틀림 | 모델이 좌표·yaw를 직접 계산 | T05 관계 JSON + `placement_utils` + T06 검사 |
| `face_towards` 뒤에도 방향이 약간 틀림 | location을 바꾼 뒤 `view_layer.update()` 없이 호출 | 갱신 후 호출(T06) |
| 비평이 사소한 지적으로 끝나지 않음 | 종료 조건 없음, 리뷰어의 과잉 보고 | T07 큰 문제만 + `NEEDS_FIX` + 2회 연속/최대 5회 |
| 비평가가 늘 합격을 줌 | 만든 에이전트가 자기 작업을 채점 | 읽기 전용 subagent, 예/아니오 질문 먼저 |
| 재질을 넣었는데 스크린샷에 색이 안 보임 | 뷰포트가 Solid 모드 | Material Preview 또는 렌더로 확인 |
| `scene_audit` 치수 규칙이 엉뚱하게 걸리거나 안 걸림 | 한국어 이름, 종류 단어 없는 이름(`thing_01`), 이름이 `_wall`로 끝남(구조물로 분류) | 영어 snake_case + 종류 단어, [치수표](05_reference_dimensions.md) 11절 `KR_SIZE_RULES` |
| `KeyError: 'Principled BSDF'` | 한국어 UI에서 노드 이름 번역 | 노드는 type, 소켓은 identifier(T08 코드) |
| 5.0에서 EXR 멀티레이어 설정 오류 | `media_type`을 먼저 바꾸지 않음 | T10 코드 |
| 스크린샷 루프가 길어지자 요청 오류 | 이미지 20장 초과 시 치수 제한 강화 | 긴 변 1000px, 각 변 2000px 이하 |
| Codex에서 Astra 결과가 거칠고 비교에서 불리 | 기본 effort low | effort를 명시 |
| 유료 크레딧이 예상보다 많이 나감 | 승인 없는 재시도, 타임아웃 후 재제출 | T14 유료 호출 규칙, 타임아웃이면 job id로 상태 조회 |
| 한국에서 Hunyuan3D로 만든 에셋을 씀 | 라이선스 적용 지역에서 한국 제외 | T11 금지 목록, 다른 생성 소스 |
| 에이전트가 "완성했다"고 했는데 렌더를 보면 이상함 | 증거 없는 완료 보고 | 보고에 audit 요약·렌더 경로 요구, 렌더를 직접 보게 함 |

---

## 관련 문서

- [목적·범위](../00_purpose/purpose_and_scope.md) · [조사 방법·신뢰도 정책](../01_research/research_method.md) · [출처 카탈로그](../01_research/sources_catalog.md) · [검증 로그](../01_research/verification_log.md)
- [AI 모델 비교·클라이언트·비용](../02_guides/01_ai_models_and_clients.md): 모델별 effort, Codex 설정
- [Blender MCP 생태계](../02_guides/02_blender_mcp.md): 공식 서버 vs MCP for Blender, safe mode, 버전 함정 전체 표
- [기타 DCC·CAD·게임엔진 MCP](../02_guides/03_other_mcp_dcc_cad_engines.md) · [AI 3D 생성](../02_guides/04_ai_3d_generation.md) · [텍스처링·재질](../02_guides/05_texturing_materials.md) · [라이팅·렌더·아트디렉션](../02_guides/06_lighting_rendering_art_direction.md)
- [오브젝트·가구·조형 모델링](../02_guides/07_modeling_objects_furniture_sculpture.md) · [배치·레이아웃](../02_guides/08_scene_layout_placement.md) · [에이전트 워크플로·프롬프팅](../02_guides/09_agent_workflow_prompting.md)
- [에셋·파이프라인·라이선스](../02_guides/10_assets_pipeline_licensing.md) · [학술 연구](../02_guides/11_research_papers.md)
- [빠른 시작](01_quickstart_setup.md) · [AAA 제작 플레이북](02_aaa_production_playbook.md) · [품질 체크리스트](04_quality_checklists.md) · [실측 치수표](05_reference_dimensions.md)
- [CLAUDE.md 템플릿](templates/CLAUDE.md) · [blender-aaa-scene 스킬](templates/skills/blender-aaa-scene/SKILL.md) · [보조 스크립트](scripts/README.md)
- [사례 모음](../04_case_studies/01_case_studies.md) · [한국어 자료](../04_case_studies/02_korean_resources.md)

## 원자료

- [`01_research/raw/10_agent-workflow.research.json`](../01_research/raw/10_agent-workflow.research.json), [`10_agent-workflow.verify.json`](../01_research/raw/10_agent-workflow.verify.json): 킥오프·스펙시트·비평가·hooks·비용 규칙. 반영한 정정: safe mode는 bpy 저장·렌더 허용(샌드박스 아님), 스크린샷 기본 1000px, `dimensions`는 회전 미반영, kiln 규칙 31개, `save_mainfile(incremental=True)` 존재, 이미지 20장 초과 제한, Tripo Premium 전용
- [`01_research/raw/08_modeling-objects.research.json`](../01_research/raw/08_modeling-objects.research.json), [`08_modeling-objects.verify.json`](../01_research/raw/08_modeling-objects.verify.json): 부품 스펙 JSON, PartNet 계층, 두께·bevel, build123d-mcp 순서. 반영한 정정: Infinigen 값은 랜덤 범위, ProfRino 5 mm 겹침 규칙, 연구 코드 비상업 라이선스, Hunyuan3D-Part 한국 제외
- [`01_research/raw/09_scene-layout.research.json`](../01_research/raw/09_scene-layout.research.json), [`09_scene-layout.verify.json`](../01_research/raw/09_scene-layout.verify.json): 관계 제약 어휘, SceneSmith·SAGE 수치, SceneEval 지표. 반영한 정정: SAGE 문 차단은 문 폭 × 문 폭, 롤백은 자동 아님, Infinigen 커피테이블 거리 병기
- [`01_research/raw/07_aaa-rendering-lighting.research.json`](../01_research/raw/07_aaa-rendering-lighting.research.json), [`07_aaa-rendering-lighting.verify.json`](../01_research/raw/07_aaa-rendering-lighting.verify.json): 색관리·조명·렌더 규칙. 반영한 정정: 5.x Glare 소켓 범위, 켈빈 사용 시 color 흰색, EEVEE 식별자 버전 분기, hyperrealism 스킬 수치 제외
- [`01_research/raw/02_blender-mcp.research.json`](../01_research/raw/02_blender-mcp.research.json), [`02_blender-mcp.verify.json`](../01_research/raw/02_blender-mcp.verify.json): 서버별 툴 이름, 타임아웃 180초, 헤드리스 `--python-exit-code`. 반영한 정정: 공식 서버 툴 목록은 미러 기준(포크 전용 툴 제외), cc-blender-skill의 공식 서버 이전은 병합 안 된 PR
- 보조: [`01_research/raw/13_research-papers.research.json`](../01_research/raw/13_research-papers.research.json), [`13_research-papers.verify.json`](../01_research/raw/13_research-papers.verify.json)(3DCodeBench 비평 프롬프트, CADCodeVerify)
- 코드 조각(T04 부품 빌더, T06 검사, T08 재질, T09 조명, T10 렌더 설정)은 작성 중 pip `bpy` 4.2.23 LTS와 5.0.1(헤드리스)에서 각각 두 번 실행해 결과를 확인했습니다. T05·T11~T14의 텍스트 템플릿과 `/goal` 예시는 실행 검증하지 않은 작성 예시입니다.
