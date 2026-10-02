# 에이전트 워크플로·프롬프팅 가이드

> 기준일: 2026-09-27 · 결과 품질은 모델이나 프롬프트 한 줄보다 **단계와 게이트, 숫자 검사, 다각도 렌더 비평, 버전 저장**을 강제하는 운영 방식에서 갈립니다. 2026년 공개 Blender 스킬팩들과 학술 연구가 공통으로 도달한 방법을 설정값, 프롬프트, 비용까지 붙여 정리했습니다.

## 핵심 요약

- **공개 스킬팩은 같은 순서로 수렴했습니다.** 레퍼런스·스펙 → 실측 스케일 블록아웃 → 카메라·구도 고정 → 라이트 v1 → 1·2·3차 형태 → 재질(명도 먼저) → 라이트 v2 → 디테일 → 최종 렌더 → 합성 → 익스포트 검증. 단계마다 스크린샷이나 렌더로 확인하고 `.blend` 버전을 남깁니다(RobLe3 cc-blender-skill, elithril blender-kiln, arjun988 blender-skills, Bniya-cn blender-design-master). 사람의 승인 게이트는 스펙, 구도, 최종 판정 세 곳에 둡니다.
- **시각 피드백 루프 규칙**: 캡처 전에 피사체를 프레이밍하고, Material Preview로 바꾸고, 여러 각도에서 본 뒤, 스펙과 다른 점을 2~3문장(또는 3줄 표)으로 짧게 적습니다. 비평은 큰 구조 문제만 다룹니다. 여러 저장소가 똑같이 경고합니다. **숫자 검사를 전부 통과한 렌더도 완전히 틀려 보일 수 있습니다.**
- **숫자 먼저, 그다음 눈.** 먼저 [`scene_audit.py`](../03_playbooks/scripts/README.md)로 떠 있음·관통·스케일·치수를 0건으로 만들고, 그다음 [`review_views.py`](../03_playbooks/scripts/README.md) 4방향 렌더를 비평합니다. 연구 근거도 같습니다. LLM은 코드만 보고 결과 모양을 거의 상상하지 못하고(SGP-MNIST에서 모든 모델이 5.5~13.0%, 우연 수준 10%), VLM 판정과 사람 판정의 일치율은 사람끼리보다 낮습니다(0.66 대 0.79).
- **코드는 작고 멱등으로 짭니다.** `execute_blender_code`는 호출할 때마다 새 namespace에서 실행됩니다. 그래서 오브젝트를 이름으로 가져오거나 만들고(get-or-create), 한 호출에는 부품 하나나 단계 하나만 넣고, 마지막 줄에 요약을 print합니다. 재현이 필요한 빌드는 `scripts/build_*.py`를 원본으로 두고 headless `blender -b`로 다시 돌립니다.
- **버전 저장은 필수입니다.** Claude Code의 `/rewind`는 MCP로 바꾼 Blender 상태를 되돌리지 못합니다. `bpy.ops.wm.save_mainfile(incremental=True)`를 쓰세요(Blender 4.2.23 LTS·5.0.1에서 동작 확인, ahujasid safe mode도 통과).
- **API는 추측하지 말고 조회하게 합니다.** `bpy_api_lookup`·`describe_node_type`(ahujasid), `search_blender_docs`(newo-ether 포크), 공식 Blender Lab 서버의 문서 툴, Context7, `fake-bpy-module` 스텁을 씁니다. **[한국 사용자]** 한국어 UI에서는 노드 이름이 번역될 수 있습니다. 노드는 `type`으로 찾고 Preferences의 **New Data** 번역을 끄세요.
- **Claude Code 기능 배치**: CLAUDE.md는 200줄 이하로 짧게 쓰고, 단계별 레시피는 Skills(SKILL.md 500줄 이하)로 빼고, 채점은 읽기 전용 **비평가 subagent**에게 맡기고, 꼭 지켜야 할 규칙은 **hooks**로 강제하고, `/goal` 조건은 텍스트로 증명할 수 있게 씁니다. Codex는 AGENTS.md와 스킬(`$skill`)로, Gemini CLI는 GEMINI.md와 `includeTools`로 대응합니다. **Codex에서 GPT-6 Astra의 기본 effort는 low이므로 반드시 따로 지정하세요.**
- **비용 감각**: Claude 이미지 토큰은 ⌈w/28⌉×⌈h/28⌉입니다. ahujasid MCP의 기본 캡처(긴 변 1000px)는 약 756토큰이고, 1920×1080은 Opus 5.5에서 2,691토큰입니다. 툴 호출 60회 정도의 세션을 가정하면 Sonnet 5 약 $2.5, Opus 5.5 약 $4, Fable 5.1 약 $8.7로 추정됩니다(가정 기반 추정). 한 요청에 이미지가 20장을 넘으면 각 변을 2000px 이하로 줄여야 합니다.
- **타임아웃·조합·보안**: ahujasid 소켓 타임아웃은 180초이고 애드온의 `exec()`에는 제한이 없습니다. 오래 걸리는 렌더와 익스포트는 headless로 돌리세요. 여러 MCP를 붙일 때는 상태 확인 → 기존 에셋 우선 → 유료 생성 전 승인 → 임포트 직후 정리 → 라이선스 기록 순서를 지킵니다. 공식 서버와 ahujasid는 둘 다 `localhost:9876`을 써서 동시에 켤 수 없습니다. `BLENDER_MCP_SAFE_MODE=1`은 샌드박스가 아닙니다.
- **기대치**: 독립적으로 검증된 'AAA급' AI+MCP 결과물은 찾지 못했습니다(공개 점수가 붙은 최고 사례도 재질·시각 충실도 6/10, 조명 7/10). 에이전트는 기능적으로 맞는 오브젝트까지는 만들지만 곡면 가구나 다듬어진 실루엣 같은 미감은 사람이 맡는다고 스킬 저자들이 직접 밝힙니다. 현실적인 목표는 **[에셋·생성 모델 + 에이전트 조립 + 검증 루프 + 사람의 마무리]** 하이브리드입니다.

---

## 1. 전제: AI는 '감독이 필요한 협업자'

스킬팩 저자들이 직접 밝힌 한계부터 보겠습니다.

- [RobLe3/cc-blender-skill](https://github.com/RobLe3/cc-blender-skill)(v1.3.0, Blender 5.1.1에서 end-to-end 검증): 곡면 가구, 프로파일 컷, 다듬어진 실루엣 같은 **미적 완성도는 범위 밖**이라고 적었습니다. 프리미티브로 만든 얼굴은 '추상 아바타'처럼 보이고, 얇은 금속에는 스펙큘러 플레어가 생긴다고도 밝혔습니다. 실패한 렌더까지 저장소에 공개했습니다('no cherry-picking').
- [Bniya-cn/blender-design-master](https://github.com/Bniya-cn/blender-design-master): 멀티에이전트와 점수 게이트(평균 8점 이상)를 설계했지만, 실제 Codex 테스트(Level 0)에서 자기 Final Gate를 넘지 못했습니다(평균 7.4). 라이선스가 선언되지 않았으니 설계 참고용으로만 보세요.
- [bsantanna/roblox-flex-with-friends](https://github.com/bsantanna/roblox-flex-with-friends): "3D space can't be verified from code alone. A position that looks right numerically can float, clip, or face the wrong way."

그래서 역할을 이렇게 나누는 편이 현실적입니다.

| 작업 | 누가·무엇이 맡나 | 이유 |
|---|---|---|
| 스펙·치수·부품 분해 | AI가 초안 → 사람이 확인(게이트 G1) | 사람 판단이 가장 싸게 먹히는 지점이 초반입니다 |
| 하드서페이스·가구 형태 | AI가 파라메트릭 코드로 작성 + 검증 루프 | 부품 단위 함수가 정확도와 편집성을 함께 올립니다(14절) |
| 유기체·조각·캐릭터 | 3D 생성 모델, 에셋 라이브러리, 스컬프트 → AI는 정리·배치 | LLM이 메시를 직접 만들면 저폴리에 머뭅니다([AI 3D 생성](04_ai_3d_generation.md)) |
| 배치 좌표 | 솔버·스크립트([`placement_utils.py`](../03_playbooks/scripts/README.md)). LLM은 관계와 제약만 | 좌표를 직접 찍으면 충돌률이 높습니다(14절) |
| 재질 | PBR 라이브러리 매칭이나 절차적 노드 코드 | [텍스처링·재질](05_texturing_materials.md) |
| 품질 판정 | 숫자 검사 → VLM 비평 → 사람 최종 판정 | VLM 판정은 흔들립니다(5절) |
| 세밀한 룩뎁(그레이딩, 미감) | 사람 | 사소한 미감을 두고 반복하면 비효율적입니다(3DCodeBench 비평 규칙) |

---

## 2. 표준 파이프라인: 11단계와 게이트

### 2.1 공개 스킬팩 비교 (2026-09 기준)

| 스킬팩 | 규모·라이선스 | 단계 구조 | 쓸 만한 점 | 주의 |
|---|---|---|---|---|
| [RobLe3/cc-blender-skill](https://github.com/RobLe3/cc-blender-skill) | 30 skills, MIT, v1.3.0 | 오케스트레이터 text-to-blender → 서브스킬 체인, [11단계 pro order](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-pro-workflow/SKILL.md) | 실측 [치수표](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/text-to-blender/references/common-object-dimensions.md), 레퍼런스 IoU 검증, 트리거 평가(200개 이상 쿼리에서 TP 100%, FP 4%), 실패 렌더 공개 | 버전 호환 문서의 `use_auto_smooth` 제거 시점이 틀림(실제 4.1) |
| [elithril/blender-kiln](https://github.com/elithril/blender-kiln) | MIT, Iron Rules 31개(core 26 + batch 5) | CONFIG → BRIEF → SOURCE → IMPORT → CLEANUP → TEXTURING → OPTIMIZE → EXPORT | 대화형 MCP 경로와 headless 경로의 결과가 바이트 단위로 같음(111.9kB GLB, 2,202 tris). 15개 에셋 1,456.2kB → 132.7kB(91%) | Blender 4.4 하한 |
| [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | 94 skills, 참조 파일 175개 이상, MIT | director가 전문 스킬을 체인 로드. Reference → Camera match → Geometry tiers → Materials → Lighting → Screenshot compare | [qa-review](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/qa-review/SKILL.md): 5개 뷰, Blocker/Major/Minor/Note, SHIP 판정. [set-dressing](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/set-dressing/SKILL.md) | 스킬이 많아 라우팅이 틀어질 수 있음 |
| [Bniya-cn/blender-design-master](https://github.com/Bniya-cn/blender-design-master) | 에이전트 4종, 라이선스 미선언 | Brief → Visual Decomposition → Asset Strategy → Modeling Plan → Blockout → Diagnostic Review → Refinement → LookDev → Lighting/Camera → Final Render → Final Gate | 읽기 전용 visual-critic, 평균 8·최저 7 게이트, 증거를 SHA-256에 묶음, `.ai-blender/tasks/<id>/`로 세션 복구 | 설계 참고용(위 1절) |
| [Gaius114/blender-claude-mcp](https://github.com/Gaius114/blender-claude-mcp) | 11 skills + kernel | [research](https://raw.githubusercontent.com/Gaius114/blender-claude-mcp/main/skill/blender-research/SKILL.md)(spec_sheet) → plan_validator → execute → render → analyze → iterate | 형상을 만들기 전에 분해 계획부터 검증 | 자체 서버(HTTP 7234) |
| [jithinolickal/blender](https://github.com/jithinolickal/blender) | Apache-2.0 | Analysis → Construction → Verification(다각도) → Iteration | `four_angle_inspection`, `save_milestone`, [common-errors.md](https://raw.githubusercontent.com/jithinolickal/blender/main/skills/blender/references/common-errors.md) | 단일 스킬 |
| [CheshireJCat/create-3d-model-skill](https://github.com/CheshireJCat/create-3d-model-skill) | Codex용 | 씬 점검 → 블록아웃 체크포인트 → 최종 → GLB | 기존 오브젝트는 사용자 소유로 취급 | 규모가 작음 |
| [newo-ether/blender-mcp](https://github.com/newo-ether/blender-mcp) | MIT, 서버 포크 + [스킬](https://raw.githubusercontent.com/newo-ether/blender-mcp/main/skills/blender-mcp/SKILL.md) | Export → Validate → Apply → Read back | 노드 그래프 트랜잭션 편집, 문서 검색 툴 | 규모가 작음 |
| [MAX-786/claude-3d-harness](https://github.com/MAX-786/claude-3d-harness) | MIT, 5개 라이브러리의 SKILL.md 58개 통합 | 워크플로 6종 × 프로필 3종 | 품질·비용 트레이드오프를 프로필로 수치화 | 초기 단계 |

### 2.2 단계별 할 일과 게이트

순서를 고정하는 이유는 "라이팅이 정해지기 전에 맞춘 재질, 형태가 확정되기 전에 넣은 디테일은 대부분 다시 만들게 된다"는 데 있습니다(RobLe3: *"A perfect material tuned in flat lighting will look wrong once real lighting goes in."*).

| # | 단계 | 할 일 | 통과 조건(게이트) | 검증 수단 |
|---|---|---|---|---|
| 0 | 레퍼런스·스펙 | 레퍼런스 이미지 확보, spec_sheet 작성(3.1절) | **G1: 사람이 스펙 확인** | — |
| 1 | 블록아웃 | 실측 스케일의 프리미티브만 사용 | 전체 치수가 스펙 ±3% 이내, 떠 있음·관통 0건 | `scene_audit.py`, 4방향 캡처 |
| 2 | 카메라·구도 고정 | 카메라 배치, 저품질 테스트 렌더 | 썸네일 크기에서도 형태가 읽힘. **G2: 사람이 구도 확인** | 테스트 렌더 |
| 3 | 라이트 v1 | 색 없는 3점 조명 | 명암만으로 형태가 읽힘 | 그레이스케일 렌더 |
| 4 | 형태 1·2·3차 | 1차(큰 덩어리) → 2차(곡률, 테이퍼, 접합부) → 3차(베벨, 이음새) | 레퍼런스와 실루엣 비교(3.3절), 주요 부품 수 일치 | `review_views.py`, 오쏘 비교 |
| 5 | 재질 v1 | 명도 먼저, 색은 나중 | 그레이스케일에서도 재질이 구분됨 | Material Preview |
| 6 | 라이트 v2 | 색온도와 강도 비율(예: 키:필 약 3:1) | 비평가 지적 사항 해결 | 렌더 |
| 7 | 디테일 패스 | 마모, 데칼, 소품 | 히어로 존이 과밀하지 않음 | 4방향 캡처 |
| 8 | 최종 렌더 | 샘플 + 디노이즈 | 비평가 subagent SHIP 판정(8.3절) | 비평가 |
| 9 | 합성 | 그레이딩, glare, vignette | — | — |
| 10 | 익스포트 검증 | 8항목 체크, 재임포트 확인 | **G3: 사람의 SHIP 판정** | 재임포트 + 4방향 렌더 |

익스포트 8항목(kiln): ① 모든 재질이 Principled BSDF(Noise/Voronoi/ColorRamp 같은 절차적 노드는 베이크) ② Base Color/Normal/Roughness/Metallic 텍스처 임베드 ③ UV 겹침·늘어짐 ④ 모든 transform 적용 ⑤ merge by distance 0.0001 m ⑥ 노멀 재계산 ⑦ 고아 데이터 정리(`orphans_purge` 대신 명시적 삭제) ⑧ 임시 GLB 크기 확인(웹 기준 50MB 이상이면 경고). glTF로 내보낼 때 절차적 노드는 조용히 사라지고, `gltf-transform optimize`는 simplify 단계가 형상을 망가뜨리므로 resize·WebP·Draco를 따로 실행합니다. 세부는 [품질 체크리스트](../03_playbooks/04_quality_checklists.md)와 [에셋·파이프라인](10_assets_pipeline_licensing.md)을 보세요.

단계마다 쓰는 비평 기법(RobLe3): **squint**(썸네일에서도 읽히나), **greyscale**(명도 구분), **좌우 반전**(눈이 익숙해진 오류 찾기), **레퍼런스와 같은 스케일로 나란히 놓고 비교**.

### 2.3 사람 승인 게이트와 품질 프로필

비싼 단계 앞에 사람 게이트를 둡니다. 사람의 판단은 초반에 넣을수록 쌉니다. [3D-lab-skills](https://github.com/LumosLab-Innovation/3D-lab-skills)는 이미지 후보를 사용자가 고르게 하고, [pipeline-kit](https://github.com/pradhankukiran/pipeline-kit)은 단계별로 승인을 받고, [blender-art-factory](https://github.com/ErikBurdett/blender-art-factory)는 파일 해시에 묶인 사람 리뷰 없이는 퍼블리시하지 않습니다("A passing technical validator does not mean an asset looks good").

```text
게이트 G1(스펙·컨셉), G2(블록아웃·구도), G3(최종 렌더·익스포트 전)에서는
작업을 멈추고 스크린샷 1장과 3줄 요약을 보여 준 뒤 내 OK를 기다려.
```

이 저장소의 [제작 플레이북](../03_playbooks/02_aaa_production_playbook.md)·[프롬프트 템플릿](../03_playbooks/03_prompt_templates.md)·[CLAUDE.md 템플릿](../03_playbooks/templates/CLAUDE.md)은 위의 G3를 G3(최종 렌더)와 G4(익스포트)로 나눠 게이트를 네 곳에 둡니다.

작업 규모에 따라 검증 강도를 고릅니다([claude-3d-harness](https://github.com/MAX-786/claude-3d-harness) 프로필).

| 프로필 | 체크포인트 | 수정 횟수 | 렌더 | 용도 |
|---|---|---|---|---|
| fast | 1회 | 1회 | 최대 1280×720, 64spp | 아이디어 확인, 배경 소품 |
| standard | 블록아웃·라이팅·재질 후 | 2회 | 1920×1080, 256spp | 일반 에셋 |
| cinematic | 모든 단계 | 4회 | 512spp | 히어로 에셋, 포트폴리오 샷 |

---

## 3. 시작 전: 스펙시트와 레퍼런스

### 3.1 모호한 요청은 spec_sheet로 바꾼다

"의자 하나 만들어줘"에는 치수, 부품, 재질이 비어 있어서 모델이 알아서 채웁니다. Gaius114의 [blender-research](https://raw.githubusercontent.com/Gaius114/blender-claude-mcp/main/skill/blender-research/SKILL.md)와 kiln의 BRIEF 단계는 모델링에 들어가기 전에 스펙을 먼저 만들고 확인을 받습니다.

```text
모델링 전에 spec_sheet(Python dict)를 작성해.
필드: meta(이름, 스타일, 용도, 폴리 버짓),
      dims_cm(전체 W/D/H),
      parts[{name, primitive/기법, size_cm, position_cm(바닥 중앙 기준),
             color_linear, principled{metallic 0|1, roughness, ...}}],
      modeling_order, dependencies, notes.
치수는 실측 근거를 대고, 불확실하면 범위로 적어.
작성한 뒤에는 멈추고 내 확인을 기다려.
```

- 색은 sRGB를 linear로 바꿔 적게 합니다(예: #D2042D → (0.467, 0.009, 0.005)).
- 러프니스 기준값(Gaius114): 거울 0.00 / 연마 금속 0.05 / 과일 0.15 / 직물 0.75 / 콘크리트 0.80.
- 형용사보다 숫자가 결과를 안정시킵니다. 예: 모디파이어 순서 Mirror → Array → Solidify → Bevel → Subdivision Surface(Bevel과 SubSurf 순서가 바뀌면 핀칭이 생김), 부품 접합부는 5~15mm 서로 파고들게 해서 이음새를 숨김, Metallic은 0 또는 1(RobLe3 [modeling](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-modeling/SKILL.md)·[materials](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-materials/SKILL.md)). 재질 수치는 [텍스처링·재질](05_texturing_materials.md)에 모았습니다.

### 3.2 치수는 추측하지 않는다

- **1 Blender unit = 1 m, Z-up, origin은 바닥 중앙**을 프로젝트 규칙으로 고정합니다.
- 코드를 쓰기 전에 치수표를 참조하게 합니다(RobLe3 오케스트레이터: "Do not guess"). 한국·미국·유럽 기준은 [실측 치수표](../03_playbooks/05_reference_dimensions.md)에 있습니다. 같은 물건도 자료마다 값이 다르니(예: 문 80×200cm 대 0.9×2.1m) **프로젝트 기준을 하나로 정해 CLAUDE.md에 적으세요.** 한국 주거 공간이 배경이면 한국 치수를 기준으로 삼으라고 명시하세요.
- 실제 크기는 `get_object_info`가 돌려주는 **world bounding box**로 잽니다. ahujasid의 `get_scene_info`는 이름, 타입, 위치(소수 둘째 자리)만 주고 치수는 주지 않습니다.
- `obj.dimensions`는 스케일은 반영하지만 **회전은 반영하지 않습니다**(로컬 축 기준). 배치 계산에는 `matrix_world @ bound_box`로 구한 world AABB를 쓰세요. [`placement_utils.world_bbox()`](../03_playbooks/scripts/README.md)가 이 계산을 합니다.
- origin과 실제 버텍스 위치는 다릅니다. `obj.location.z = 0.45`처럼 origin만 옮기면 origin이 가운데인 오브젝트는 절반이 바닥에 묻힙니다. 바닥에 붙이는 일은 `pu.snap_to_floor()`에 맡기세요.

### 3.3 레퍼런스 이미지를 주는 법

- **이미지를 텍스트보다 앞에 두고, 여러 장이면 'Image 1:', 'Image 2:' 라벨을 붙입니다**([Claude vision 문서](https://platform.claude.com/docs/en/build-with-claude/vision)).
- 정면·측면 오쏘 레퍼런스가 있으면 같은 오쏘 카메라를 맞춰 놓고 실루엣끼리 비교합니다. 비교는 같은 종류끼리 합니다. 와이어프레임 마스크를 뷰티 렌더와 비교하면 IoU가 엉뚱하게 낮게 나옵니다.

```text
Image 1: 정면 레퍼런스, Image 2: 측면 레퍼런스.
두 이미지에서 전체 비율(H:W:D)과 주요 부품의 상대 위치를 먼저 표로 뽑고,
오쏘 카메라를 레퍼런스에 맞춘 다음 블록아웃해.
```

레퍼런스 일치 기준(RobLe3 [reference-analysis-validator](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/reference-analysis-validator/SKILL.md)):

| 지표 | 기준 |
|---|---|
| 실루엣 IoU | 강체·로고 ≥ 0.90, 마스코트 1차 ≥ 0.82 |
| bbox 중심 드리프트 | ≤ 12px (1024px 기준) |
| bbox 크기 드리프트 | ≤ 3% |
| 랜드마크 드리프트 | ≤ 2% |
| 주요 부품 수 | 정확히 일치 |

- **레퍼런스가 없으면 목표 이미지부터 만듭니다.** BlenderAlchemy는 텍스트 목표를 이미지 생성 모델로 그린 '상상 이미지'를 평가 기준으로 썼고, Scenethesis는 가이던스 이미지에서 씬 그래프와 포즈를 뽑았습니다. 추상적인 텍스트보다 이미지가 비평 기준으로 안정적입니다. 컨셉 이미지 2~3장 → 하나 선택 → 이후 비평 때마다 첨부하는 식으로 씁니다. 3D 생성용 이미지 준비는 [AI 3D 생성](04_ai_3d_generation.md)을 보세요.

---

## 4. 시각 피드백 루프

### 4.1 루프 한 바퀴

1. 코드 청크 하나를 실행합니다(6.1절).
2. 피사체를 프레이밍합니다.
3. 셰이딩을 Material Preview로 바꿉니다.
4. 여러 각도에서 캡처합니다(4.4절).
5. 스펙과 다른 점을 `부품 / 기대값 / 관찰값 / 수정안` 표로 최대 3줄 적습니다.
6. 차이가 있으면 고치고, 없으면 다음 단계로 넘어갑니다.
7. 단계가 끝나면 `.blend` 버전을 저장합니다(6.5절).

```text
각 단계가 끝나면 피사체를 프레이밍하고 4각도 스크린샷을 찍은 뒤,
스펙 대비 차이를 '부품 / 기대값 / 관찰값 / 수정안' 표로 최대 3줄 적어.
차이가 없으면 다음 단계로 넘어가.
```

### 4.2 루프 규칙

| 규칙 | 이유 | 출처 |
|---|---|---|
| 변경 전후로 스크린샷, 작업 전에 씬 정보 먼저 | 서버에 내장된 `asset_creation_strategy` 프롬프트가 이렇게 지시함 | [ahujasid server.py](https://raw.githubusercontent.com/ahujasid/blender-mcp/main/src/blender_mcp/server.py) |
| 캡처 전에 반드시 프레이밍 | 프레이밍하지 않으면 소품이 몇 픽셀로 찍혀 검증이 안 됨 | [kiln Rule 22](https://raw.githubusercontent.com/elithril/blender-kiln/main/SKILL.md) |
| Material Preview로 전환 | Solid 모드에서는 재질 색이 보이지 않아 검증이 무의미해짐(실제 실패 사례) | [roo-blendermcp-jp-rules](https://github.com/hideki711014/roo-blendermcp-jp-rules) |
| 한 각도만 보지 않기 | 떠 있음, 관통, 방향 오류는 한 각도에서 잘 안 보임 | [roblox-flex-with-friends](https://github.com/bsantanna/roblox-flex-with-friends) |
| 캡처는 구조 변경 1회 또는 배치 1회당 1장, 여러 단계를 묶은 작업이면 끝에서 1장 | 토큰 예산 | [blend-ai auto_critique_workflow](https://raw.githubusercontent.com/HoldMyBeer-gg/blend-ai/main/src/blend_ai/prompts/workflows.py) |
| 비평은 2~3문장, 또는 100단어 이하 bullet | 길게 쓰면 토큰만 늘고 판단은 나아지지 않음 | blend-ai, [3DCodeBench 비평 프롬프트](https://raw.githubusercontent.com/gaoypeng/3dcodebench/main/prompts/visual_critique_system_prompt_text.txt) |
| 큰 구조 문제만 지적하고 취향 문제는 적지 않기 | 사소한 미감을 두고 반복하면 비효율적이고, 리뷰어는 문제를 과잉 보고하는 경향이 있음 | 3DCodeBench, [Claude Code best practices](https://code.claude.com/docs/en/best-practices) |
| 본 것만 서술하고 결과를 과장하지 않기 | '결과 과장 서술'이 실제 실패 패턴으로 기록됨 | roo-blendermcp-jp-rules |
| **숫자가 통과해도 이미지가 틀리면 실패** | "A render passing every numerical check can still look completely wrong." | [RobLe3 text-to-blender](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/text-to-blender/SKILL.md), [blender-art-factory](https://github.com/ErikBurdett/blender-art-factory) |

### 4.3 Material Preview 전환 코드 (GUI 연결 시)

```python
import bpy
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for s in area.spaces:
            if s.type == 'VIEW_3D':
                s.shading.type = 'MATERIAL'
                s.shading.use_scene_lights = True
                s.shading.use_scene_world = True
print("shading=MATERIAL")
```

출처는 RobLe3 text-to-blender입니다. headless(`blender -b`)에는 뷰포트가 없으니 이 코드 대신 [`review_views.py`](../03_playbooks/scripts/README.md)로 렌더하세요.

### 4.4 어느 각도에서 볼까

| 상황 | 뷰 구성 | 출처 |
|---|---|---|
| 단일 오브젝트 기본 | 위(오쏘) / 정면 / 측면 / 3/4 원근. 오브젝트마다 다른 색으로 칠해 겹침과 간격이 잘 보임 | [`review_views.py`](../03_playbooks/scripts/README.md) (Blender 4.2.23 LTS·5.0.1·5.2.2 LTS 테스트 통과) |
| 파라메트릭 디자인 | 방위각/고도 = -45°/55°(레퍼런스), 0°/12°(측면), 225°/35°(앞-왼쪽), 5°/85°(탑다운) | [jithinolickal viewport_helpers.py](https://raw.githubusercontent.com/jithinolickal/blender/main/skills/blender/scripts/viewport_helpers.py) |
| 출하 전 QA | 3/4 히어로, 오쏘/프로파일, 와이어, 뷰티, 레퍼런스 비교(5개 뷰) | [arjun988 qa-review](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/qa-review/SKILL.md) |
| 인테리어·배치 | 탑다운 오쏘 1장 + 눈높이(1.6m) 1장 + 로우앵글(0.6m) 1장 | [arjun988 set-dressing](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/set-dressing/SKILL.md) |
| 배치를 VLM이 직접 판단할 때 | 탑다운 오쏘에 격자선과 라벨을 얹어 셀 단위로 지시(가구 0.3m, 소품 0.1m 격자) | [TreeSearchGen](https://github.com/dw-dengwei/TreeSearchGen) (CVPR 2025) |
| 레퍼런스 재현 | 레퍼런스와 같은 오쏘 카메라 | 3.3절 |

`review_views.py` 사용 팁: GPU가 없는 서버에서는 `engine="CYCLES"`(CPU)만 동작합니다. GUI에 연결된 상태라면 `engine="BLENDER_WORKBENCH"`가 가장 빠릅니다.

### 4.5 비평 프롬프트

**3DCodeBench 형식**(큰 구조 문제만, 짧게, 판정을 기계가 읽을 수 있게):

```text
설명(또는 참조 이미지)과 4방향 렌더를 비교해서
누락된 부품, 떠 있는 지오메트리, 비율 오류, 정렬 오류, 형태 오류만
100단어 이하 bullet로 적어. 사소한 미감은 적지 마.
큰 구조 문제가 없으면 마지막 줄에 NEEDS_FIX: NO,
있으면 NEEDS_FIX: YES와 수정 방향(수치 포함)을 적어.
```

**체크리스트를 먼저 만들게 하기**(CADCodeVerify 방식, [코드](https://github.com/Kamel773/CAD_Code_Generation)): 모델이 먼저 "다리가 4개인가?", "좌판 높이가 폭의 절반쯤으로 보이는가?" 같은 예/아니오 질문을 만들고, 렌더를 보고 답한 다음 수정합니다.

**종료 조건 예시**: `NEEDS_FIX: NO`가 2회 연속 나오거나 최대 5회 반복하면 멈춥니다. 세밀한 룩 개발(조명 미세 조정, 컬러 그레이딩)은 사람이 하거나 별도 단계로 뺍니다.

**판정 노이즈 줄이기**: VLM 판정은 흔들리므로, 후보 두 개를 비교할 때는 좌우 순서를 바꿔 두 번 물어보고 결과가 같을 때만 채택합니다(BlenderGym의 verifier 실험 결과를 바탕으로 한 권장).

---

## 5. '숫자 먼저, 그다음 눈' 검증

### 5.1 검증 순서

| 순서 | 무엇으로 | 목표 | 왜 이 순서인가 |
|---|---|---|---|
| ① 숫자 | [`scene_audit.py`](../03_playbooks/scripts/README.md): 떠 있음, 바닥 아래로 박힘(`below_floor`), 다른 물체 속으로 파고듦(`sunk_into`), 천장 위로 뚫림(`above_ceiling`, `ceiling_z`를 줄 때), 유닛 간 관통과 가구–벽·천장 관통, 스케일 미적용·음수 스케일, non-manifold, 재질·UV 없음, 이름 기준 치수 범위 이탈(가구 자체 방향 기준 폭 w·깊이 d·높이 z) → JSON. 간격은 `pu.check_clearances()`. 문·창·방 구조가 있으면 [`building_audit.py`](../03_playbooks/scripts/README.md)도 돌립니다 | `units_with_issues`와 `interpenetrating_pairs`가 0(의도한 벽걸이·천장 조명은 예외로 확인) | 싸고 결정적입니다. VLM이 놓치는 작은 관통(기본 허용 오차 5 mm 초과)도 잡습니다 |
| ② 눈 | [`review_views.py`](../03_playbooks/scripts/README.md) 4방향 렌더 → 비평가(8.3절) | NEEDS_FIX: NO 또는 SHIP | 숫자로 못 잡는 실루엣, 비율, 분위기를 봅니다 |
| ③ 사람 | 최종 렌더와 익스포트 결과 | G3 SHIP | VLM 판정과 사람 판정의 일치율은 0.66으로, 사람끼리의 0.79보다 낮습니다([BlenderGym](https://github.com/richard-guyunqi/BlenderGym-Open)) |
| ④ (선택) 물리 | 소품에 rigid body(active), 가구·바닥에 passive를 걸고 60프레임 시뮬레이션 → 2cm 이상 움직이거나 5° 이상 돌아간 오브젝트를 '불안정' 목록으로 반환 → 시뮬레이션 결과는 적용하지 않고 원위치로 복원 | 불안정 0건 | SceneSmith는 시뮬레이션 뒤 96%가 안정적이었습니다. 이 절차는 연구를 바탕으로 한 작성 예시이며 이 저장소에서 스크립트로 검증하지는 않았습니다 |

MCP로 연결된 Blender에서 돌리는 방법:

```python
import sys
sys.path.append(r"C:\path\to\3D-MCP\03_playbooks\scripts")   # 이 저장소를 받은 위치
import importlib, scene_audit
importlib.reload(scene_audit)
report = scene_audit.audit_scene(floor_z=0.0)
print(report["summary"])
for u in report["units"]:
    if u["issues"]:
        print(u["name"], u["issues"])
print(report["interpenetrations"])
```

- 방 안을 검사할 때는 천장 높이와 범위를 함께 줍니다: `audit_scene(floor_z=0.0, ceiling_z=2.30, collection="Room")`. `collection`을 주면 그 컬렉션의 유닛만 보고하고 천장 규칙도 그 유닛에만 적용하므로, 방 내부와 건물 외관이 한 장면에 있어도 따로 검사할 수 있습니다.
- headless: `blender -b scene.blend --python 03_playbooks/scripts/scene_audit.py -- --floor-z 0 --ceiling-z 2.3 --collection Room --out audit.json`.
- safe mode 때문에 외부 모듈 import가 막히면 파일 내용을 통째로 붙여 넣으세요(끝에서 자동 실행).
- 판정 규약은 [스크립트 README](../03_playbooks/scripts/README.md)에 있습니다. 요점: 최상위 부모 기준으로 '유닛'을 묶고, 가구 정면은 -Y입니다. 치수 규칙은 이름의 **단어**로 고릅니다(`CoffeeTable`·`coffee_table_01` → `coffee_table`, `table_lamp`·`turntable` → 규칙 없음). 구조물은 이름의 **마지막 핵심 단어**로 판정합니다(`Wall_N` → 구조물, `wall_shelf` → 가구).

### 5.2 `get_scene_info` 10개 제한을 피하는 압축 씬 요약

ahujasid의 `get_scene_info`는 오브젝트를 **최대 10개**만 돌려주고 치수도 없습니다(코드 주석 'Reduced from 20 to 10'). 가구가 수십 개인 방에서는 모델이 나머지를 모른 채 작업하게 됩니다. 아래 스크립트로 한 줄짜리 인덱스를 만들고, 필요한 오브젝트만 `get_object_info`로 자세히 조회하게 하세요. 오브젝트 100개면 대략 수천 토큰입니다.

```python
import bpy, json
from mathutils import Vector
rows = []
for o in bpy.context.scene.objects:
    if o.type not in {'MESH', 'LIGHT', 'CAMERA', 'EMPTY', 'CURVE'}:
        continue
    pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
    mn = [min(p[i] for p in pts) for i in range(3)]
    mx = [max(p[i] for p in pts) for i in range(3)]
    rows.append([o.name, o.type,
                 (o.users_collection[0].name if o.users_collection else ''),
                 [round(v, 3) for v in mn],                    # world bbox 최소점
                 [round(mx[i] - mn[i], 3) for i in range(3)]]) # world 크기(m)
print(json.dumps(rows, separators=(',', ':')))
```

이 문서를 쓰면서 bpy 5.0.1과 4.2.23 LTS에서 실행해 확인했습니다. MCP 결과가 10,000토큰을 넘으면 Claude Code가 경고하고, 25,000토큰(`MAX_MCP_OUTPUT_TOKENS` 기본값)을 넘는 텍스트 결과는 파일로 빠집니다([Claude Code MCP 문서](https://code.claude.com/docs/en/mcp)). 씬이 아주 크면 컬렉션 단위로 나눠 출력하세요.

### 5.3 완료 보고는 증거로

Claude Code 모범 사례도 성공을 주장하지 말고 증거(명령 출력, 스크린샷)를 보여 주라고 권합니다([best practices](https://code.claude.com/docs/en/best-practices)). 보고 형식을 정해 두세요(RobLe3 예시).

```text
Created:   GEO-sword_blade (1,240 verts), GEO-sword_grip (320 verts)
Materials: MAT-steel_brushed, MAT-leather_dark
Lights:    LGT-key (3200K), LGT-fill (5500K), LGT-rim
Rendered:  /tmp/sword_hero.png (1920×1080, 2.3MB, 38s, 256 samples + OptiX denoise)
Audit:     units_with_issues=0, interpenetrating_pairs=0
Remaining: (남은 결함 목록)
```

newo-ether 스킬은 여기에 '달성 여부, 수행한 변경, 검증 증거, 저장·미저장 상태'를 추가로 요구합니다.

---

## 6. 실행 방식: 코드를 어떻게 쪼개고 남기나

### 6.1 `execute_blender_code` 청크 규칙

| 규칙 | 이유 |
|---|---|
| 매 호출마다 필요한 모듈을 다시 import | 호출마다 새 namespace라서 Python 변수는 다음 호출까지 남지 않습니다. 상태는 `bpy.data`에만 남습니다 |
| 오브젝트는 **이름으로 가져오거나 만들기**(get-or-create) | 같은 코드를 다시 실행해도 중복이 생기지 않습니다(멱등) |
| 호출 하나에 부품 하나 또는 단계 하나 | ahujasid 툴 설명도 "breaking it into smaller chunks"를 요구합니다. 실패 지점을 찾기 쉽습니다 |
| 마지막 줄에 한 줄 요약 print | 모델이 결과를 텍스트로 확인하고 다음 판단에 씁니다 |
| 에셋은 한 번에 하나만 가져오기 | kiln Rule 3 |
| 큰 루프 금지, 해상도 상한 두기 | 애드온의 `exec()`에는 타임아웃이 없어 Blender가 멈추고, 서버 소켓은 180초에 끊깁니다. jithinolickal은 인터랙티브 작업에서 `profile_resolution` ≤ 140, 슬랫 수 ≤ 50으로 제한합니다 |
| 가능하면 `bpy.ops` 대신 데이터 API(`bpy.data`, `bmesh`) | view3d 오퍼레이터는 MCP 컨텍스트에서 poll 오류가 납니다(jithinolickal common-errors). 오퍼레이터로 프리미티브를 만들 때는 3D 커서 영향을 피하려고 `location=(0,0,0)`을 명시합니다(3DCodeBench) |

템플릿(RobLe3 규칙을 바탕으로 작성. 치수를 메시에 직접 구워 스케일이 1로 유지되므로 `scene_audit.py`의 '스케일 미적용' 경고가 나지 않습니다):

```python
import bpy, bmesh
from mathutils import Matrix

name = "GEO-seat"
obj = bpy.data.objects.get(name)
if obj is None:                                        # get-or-create: 다시 실행해도 하나만 생김
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0); bm.to_mesh(mesh); bm.free()
    mesh.transform(Matrix.Diagonal((0.45, 0.45, 0.04, 1.0)))   # 45×45×4cm를 메시에 굽기
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
obj.location = (0.0, 0.0, 0.45 - 0.02)                 # 좌면 윗면 높이 45cm (origin이 두께 중앙)
bpy.context.view_layer.update()
print(f"done:{name} dims={tuple(round(d,3) for d in obj.dimensions)} scale={tuple(obj.scale)}")
```

bpy 5.0.1과 4.2.23 LTS에서 두 번 연속 실행해 오브젝트가 하나만 생기고 `dims=(0.45, 0.45, 0.04) scale=(1.0, 1.0, 1.0)`이 출력되는 것을 확인했습니다.

### 6.2 오류가 나면

- 코드 실행 툴이 예외를 삼키지 않게 하고 **traceback 전체**를 모델에 돌려줍니다.
- 3DCodeBench의 멀티턴 설정은 이전 코드 + traceback으로 **3회**(T=3) 재시도하는 것을 표준으로 씁니다. 3회 실패하면 "기능을 줄인 최소 버전부터 다시"로 전략을 바꾸세요.
- 참고로 2024년 범용 모델의 Blender 스크립트 구문 오류율은 15.6~21.4%였고, 특화 모델 BlenderLLM은 3.4%였습니다([BlenderLLM](https://github.com/FreedomIntelligence/BlenderLLM)). 모델별 값은 두 검증 결과가 README 표를 다르게 읽어 어긋납니다([학술 연구 가이드](11_research_papers.md) 4.1절). BlenderLLM은 스스로 '기본 모델링만 가능'하다고 밝힙니다. 최신 모델의 오류율은 이 조사에서 측정되지 않았습니다.

### 6.3 headless 스크립트를 원본으로: 하이브리드 구조

대화형 MCP로만 만들면 과정이 대화 기록에만 남습니다. 다음 구성을 권합니다([kiln](https://github.com/elithril/blender-kiln), [little-prince-planet-world](https://github.com/MMMvinki/little-prince-planet-world), newo-ether의 방식을 종합).

1. `scripts/build_<asset>.py`에 파라미터화된 멱등 빌더 함수를 두고, 에이전트는 **이 파일을 편집**합니다.
2. 대화형 루프에서는 단계마다 해당 함수를 `execute_blender_code`로 호출하고 스크린샷을 찍습니다.
3. 최종 산출물과 CI는 `blender -b scene.blend --python scripts/build_chair.py`로 재현합니다. kiln은 두 경로의 결과가 바이트 단위로 같다고 보고했습니다.
4. 셰이더·Geometry Nodes 그래프는 구조화 툴로 다룹니다(6.4절).
5. MCP 익스포트가 타임아웃되면 headless CLI로 전환합니다(kiln Rule 21).

```text
project/
├─ CLAUDE.md            (Codex·Gemini용으로 AGENTS.md에도 같은 내용)
├─ spec/chair_spec.json (G1에서 확정한 spec_sheet)
├─ scripts/build_chair.py
├─ versions/            (chair1.blend, chair2.blend ...)
├─ review/              (top.png, front.png, side.png, persp.png)
├─ PROGRESS.md          (8.6절 작업 메모리)
└─ export/chair.glb + chair_log.md (라이선스·출처 기록)
```

참고로 Anthropic은 MCP 툴을 하나씩 호출하는 대신 코드 실행으로 중간 결과를 컨텍스트 밖에서 처리하면 토큰이 150,000에서 2,000으로 줄었다고 보고했습니다(98.7%, [2025-11-04](https://www.anthropic.com/engineering/code-execution-with-mcp)). 일반 MCP 사례의 수치이고 3D 작업에서 측정한 값은 아닙니다. '큰 스크립트 한 번'과 '작은 툴 호출 여러 번'을 3D에서 정량 비교한 자료는 찾지 못했습니다.

### 6.4 노드 그래프와 정형 작업은 구조화 툴로

| 방식 | 언제 | 예 |
|---|---|---|
| 트랜잭션 노드 패치 | 셰이더·Geometry Nodes 편집. 임의 Python으로 노드를 만들면 깨지기 쉬움 | [newo-ether](https://github.com/newo-ether/blender-mcp): `export_node_tree` → `validate_node_tree_patch` → `apply_node_tree_patch` → 다시 읽어 확인. 오래된 패치는 revision 체크로 거부. 우선순위는 전용 툴 → 검증된 패치 → 최소한의 `execute_blender_code` |
| typed operation + 레시피 | 제품샷, 턴테이블처럼 반복되는 작업 | [pipeline-kit](https://github.com/pradhankukiran/pipeline-kit): 검증되는 오퍼레이션 8개와 레시피 ID만 계획하게 하고, dependsOn DAG와 단계별 승인 게이트를 둠. 문법 환각이 사라지는 대신 레시피 밖 창작에는 약함 |
| 원자 연산 + 상태 JSON | 배치 편집 | [SceneReVis](https://github.com/Runder-sun/SceneReVis): add, move, rotate, scale, replace, remove 6개 연산만 쓰고 매 턴 '상태 JSON + 렌더 + 충돌 목록'을 돌려줌. [SceneAssistant](https://github.com/ROUJINN/SceneAssistant)도 매 스텝 미리보기 이미지와 JSON 상태를 함께 기록 |
| 카메라 연출 레시피 | 제품 영상 | [kevinbadi/blender-skills](https://github.com/kevinbadi/blender-skills): turntable, slow-zoom, dolly-rotate 등 6종을 레시피로 고정 |

### 6.5 `.blend` 증분 저장과 되돌리기

Claude Code 체크포인트는 "Claude의 파일 편집 도구로 바꾼 것만 추적하고, Bash나 외부 프로세스의 변경은 추적하지 않습니다"([best practices](https://code.claude.com/docs/en/best-practices)). MCP로 바꾼 Blender 씬은 `/rewind`로 돌아오지 않습니다. ahujasid도 "ALWAYS save your work before using it"이라고 경고합니다. Unreal도 MCP 편집이 항상 undo되지는 않습니다(Epic 스킬).

| 방법 | 동작 | 확인 |
|---|---|---|
| `bpy.ops.wm.save_mainfile(incremental=True)` | 현재 파일을 번호를 붙인 새 파일로 저장하고 그 파일로 작업을 이어 감(`chair.blend` → `chair1.blend` → `chair2.blend`). 먼저 한 번은 경로를 지정해 저장해 두세요 | bpy 5.0.1·4.2.23 LTS에서 동작 확인. ahujasid safe mode 검증기 통과(2026-09-25 커밋 기준) |
| `bpy.ops.wm.save_as_mainfile(filepath=..., copy=True)` | 사본만 저장하고 작업 파일 경로는 그대로 둠 | safe mode 통과. 아래 스니펫을 bpy 5.0.1·4.2.23 LTS에서 확인 |

```python
import bpy
base = bpy.path.abspath('//')
name = bpy.path.display_name_from_filepath(bpy.data.filepath) or 'untitled'
n = int(bpy.context.scene.get('ai_ver', 0)) + 1
bpy.context.scene['ai_ver'] = n
target = f"{base}{name}_v{n:03d}.blend"
bpy.ops.wm.save_as_mainfile(filepath=target, copy=True)   # 작업 파일은 그대로, 사본만 저장
print('saved', target)
```

- **safe mode는 bpy를 통한 저장·열기, import/export, 렌더를 막지 않습니다.** 막는 것은 `open()`·`os` 같은 직접 파일 I/O, 프로세스, 네트워크, handlers/timers/drivers, 외부 `.blend` append/link입니다(검증 결과로 정정된 내용).
- **되돌리기 전략**: BlenderAlchemy는 후보 편집 여러 개를 렌더해 비교하고, 나아지지 않으면 이전 가설로 되돌립니다(hypothesis reversion. 예제 config는 깊이 4 × 폭 8 트리, num_tries 4, [config](https://raw.githubusercontent.com/ianhuang0630/BlenderAlchemyOfficial/main/configs/wood_to_marble.yaml)). 실무에서는 편집 전에 저장하고, 비평 점수가 떨어지면 직전 버전 파일을 다시 여는 방식으로 씁니다.
- 파라미터는 한 번에 하나씩 바꾸고, 바꾸기 전에 마일스톤을 저장합니다(jithinolickal).

### 6.6 네이밍·단위·축 규약

이름이 곧 상태 핸들입니다. namespace가 매번 새로 만들어지기 때문입니다. 임포트한 에셋은 출처와 관계없이 바로 규약대로 이름을 바꿉니다(kiln Rule 25).

| 항목 | 옵션 A (Blender Studio식, RobLe3) | 옵션 B (게임 엔진식, kiln) |
|---|---|---|
| 오브젝트 | `GEO-`, `LGT-`, `CAM-`, `ARM-` | `SM_PascalCase`, 캐릭터 `CH_`, 리그 `RG_`, 애니메이션 `A_` |
| 메시 데이터 | — | `SM_Name_Mesh` |
| 재질 | `MAT-` | `M_Type_Variant` (예: `M_Wood_Oak`) |
| 컬렉션 | `COL-` | `COL_Blockout / COL_Hero / COL_Props / COL_Lights / COL_Cameras` |
| 익스포트 파일 | — | kebab-case (`wooden-chair_final.glb`, `wooden-chair_log.md`) |

공통: 1 BU = 1 m, Z-up, origin은 바닥 중앙, 가구 정면은 -Y(이 저장소 스크립트 규약. SceneSmith는 +Y forward로 정규화하니 외부 파이프라인과 섞을 때 확인하세요). **[한국 사용자] 대화는 한국어로 해도 되지만 오브젝트 이름은 영어로 짓게 하세요.** `scene_audit.py`의 치수 규칙이 `chair`, `table`, `sofa` 같은 영어 키워드로 동작합니다.

### 6.7 파괴적 작업 금지 목록

에이전트가 '깨끗하게 다시 시작'하려다 씬을 지우거나 재질을 날리는 사고가 반복됩니다. CLAUDE.md에 넣고, 가능하면 hook으로 강제하세요(8.4절).

- 기존 오브젝트와 데이터블록은 사용자 소유입니다. 내가 만든 것(접두사로 식별)만 고치거나 지웁니다(CheshireJCat).
- `orphans_purge` 금지. 재질이 사라집니다(jithinolickal).
- decimate, simplify, 삭제는 제안 → before/after 비교 → 사용자 선택 순서로 합니다. auto 모드에서도 같습니다(kiln Rule 6).
- 공장 초기화(`read_factory_settings`)나 새 파일 열기 금지.
- `.blend`를 덮어쓰거나 옮기는 일은 요청이 있을 때만 합니다(newo-ether). 버전 사본 저장은 예외로 허용합니다.
- 에셋 다운로드와 유료 생성은 확인을 받은 뒤에만 합니다.

---

## 7. API 문서 공급: 추측하지 말고 조회하게 하기

모델의 학습 데이터에는 2.8x~3.x 시절 코드가 많아서 4.x/5.x에서 KeyError나 AttributeError가 자주 납니다. 조회 툴을 주면 '추측 → 실패 → 재시도' 루프가 줄어듭니다. LL3M은 Blender API 문서 검색(BlenderRAG)을 붙여 BMesh, 모디파이어, 셰이더 노드 같은 고급 기능을 썼습니다.

### 7.1 조회 수단

| 수단 | 무엇 | 언제 쓰나 | 비고 |
|---|---|---|---|
| `bpy_api_lookup`, `describe_node_type` ([ahujasid](https://github.com/ahujasid/blender-mcp)) | RNA 시그니처 JSON, 노드 소켓 스키마 | 실행 중인 Blender 버전 그대로의 API 확인 | 가장 직접적입니다 |
| `search_blender_docs`, `get_blender_doc_page`, `search_geometry_node_types` ([newo-ether](https://github.com/newo-ether/blender-mcp)) | 공식 Manual/API 검색 | 버전에 민감한 API 사용 전 | 포크 서버 필요 |
| 공식 Blender Lab 서버의 문서 툴 ([Claude 커넥터](https://claude.com/connectors/blender)) | API·매뉴얼 문서 접근 | 공식 커넥터 사용자 | Blender 5.1+ ([Blender MCP 가이드](02_blender_mcp.md) 4절) |
| [Context7](https://github.com/upstash/context7) | 라이브러리 문서를 버전별로 가져와 주입(`resolve-library-id`, `query-docs`, 원격 `https://mcp.context7.com/mcp`) | 파이썬 일반 라이브러리, 웹·엔진 SDK | `npx ctx7 setup` 또는 `/plugin install context7@claude-plugins-official`. **Blender API 문서가 등록돼 있는지는 미확인** |
| [fake-bpy-module](https://github.com/nutti/fake-bpy-module) | 2.78~5.2 버전별 bpy 스텁 | 오프라인 확인, 생성한 스크립트를 pyright/mypy로 미리 검사 | `pip install fake-bpy-module-5.1`. 비활성 소켓이나 context poll 실패 같은 런타임 동작은 잡지 못함 |
| [3DCodeBench `blender_5_api_reference.txt`](https://raw.githubusercontent.com/gaoypeng/3dcodebench/main/prompts/blender_5_api_reference.txt) | LLM이 자주 틀리는 5.0 API 목록 | 시스템 프롬프트·스킬 reference로 첨부 | `use_auto_smooth`·Musgrave는 5.0이 아니라 **4.1**에서 제거된 것이니 이 부분은 고쳐서 쓰세요 |

Context7을 쓸 때 CLAUDE.md에 넣는 README 원문 규칙: `Always use Context7 when I need library/API documentation, code generation, setup or configuration steps without me having to explicitly ask.` 문서 서버는 코딩 단계에서만 켜 두는 편이 토큰에 유리합니다.

### 7.2 모델에게 줄 버전 함정 요약

전체 표는 [Blender MCP 가이드 11절](02_blender_mcp.md)에 있습니다. 스킬 reference에는 아래 정도만 넣어도 대부분의 실패를 막습니다.

| 함정 | 사실 (검증 반영) | 대응 |
|---|---|---|
| EEVEE 엔진 식별자 | 4.2~4.x `BLENDER_EEVEE_NEXT`, 5.0부터 `BLENDER_EEVEE` | 아래 스니펫처럼 enum에서 골라 쓰기 |
| `Mesh.use_auto_smooth` | **4.1에서 제거**(5.x가 아님) | `hasattr` 분기, smooth by angle 계열 사용 |
| Musgrave 텍스처 노드 | 4.1에서 제거 | Noise 텍스처로 대체 |
| Principled BSDF v2 입력명 | `Specular IOR Level`, `Coat Weight`, `Transmission Weight`, `Subsurface Weight`, `Emission Color`. `Subsurface Color`는 없음 | 이름을 조회한 뒤 사용 |
| 비활성 소켓 | `inputs["Subsurface IOR"]`처럼 문자열 키로 접근하면 KeyError | 아래 `set_input()`처럼 순회해서 찾기 |
| F-curve 접근 | 5.0에는 `action.fcurves`가 없음. `action.layers[].strips[].channelbags[].fcurves`(4.4+) | kiln은 4.4를 하한으로 잡음 |
| `Material/World.use_nodes` | 5.0에서 DeprecationWarning(6.0에서 제거 예정). 5.0.1에서는 새 재질에 이미 node_tree가 있음 | `if bpy.app.version < (5, 0, 0): mat.use_nodes = True` |
| Noise 텍스처 출력 | 5.0에서 표시 이름은 `Factor`, identifier는 여전히 `Fac` | 이름보다 identifier로 접근 |
| `bgl` 모듈 | 5.0에서 제거 | `gpu` 모듈 사용 |
| Geometry Nodes | 입력은 인덱스가 아니라 이름으로, CaptureAttribute는 `capture_items.new()` 필요 | 3DCodeBench 목록 |
| 렌더 전 카메라 | 카메라가 없으면 렌더 실패 | `ensure_camera` 확인 |
| PyPI `bpy` | 5.1+는 Python 3.13 전용, 5.0은 3.11 | headless 환경 구성 시 확인 |

```python
import bpy
# 엔진 식별자: 버전에 맞는 EEVEE를 enum에서 골라 쓴다
ids = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
bpy.context.scene.render.engine = 'BLENDER_EEVEE' if 'BLENDER_EEVEE' in ids else 'BLENDER_EEVEE_NEXT'

# 재질: 5.0부터 use_nodes 불필요(폐기 예고), 노드는 이름이 아니라 type으로 찾는다
mat = bpy.data.materials.get("M_Wood_Oak") or bpy.data.materials.new("M_Wood_Oak")
if bpy.app.version < (5, 0, 0):
    mat.use_nodes = True
bsdf = next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')

def set_input(node, name, value):
    """비활성 소켓도 찾을 수 있게 순회해서 설정한다."""
    for inp in node.inputs:
        if inp.name == name:
            inp.default_value = value
            return True
    return False

set_input(bsdf, "Roughness", 0.55)
set_input(bsdf, "Coat Weight", 0.0)
print("engine", bpy.context.scene.render.engine, "bsdf", bsdf.name)
```

엔진 선택, `use_nodes` 분기, type 기반 탐색, `set_input()`(비활성 소켓 `Subsurface IOR` 포함)을 bpy 5.0.1과 4.2.23 LTS에서 확인했습니다.

### 7.3 [한국 사용자] 한국어 UI에서 노드 이름이 바뀌는 문제

> **문제**: Blender UI를 현지화하면 새로 만든 데이터의 이름도 번역될 수 있습니다. 일본어 UI에서 'Principled BSDF' 노드가 'プリンシプルBSDF'로 만들어져 `nodes['Principled BSDF']` 코드가 실패한 사례가 [문서화되어 있습니다](https://github.com/hideki711014/roo-blendermcp-jp-rules). 한국어 UI도 같은 원리가 적용될 가능성이 높습니다(추정. 한국어 UI로 직접 재현하지는 못했습니다).
>
> **해결**
> 1. 코드에서는 노드를 **type으로 찾습니다**: `n.type == 'BSDF_PRINCIPLED'`, 출력 노드는 `n.type == 'OUTPUT_MATERIAL'`. 노드 타입은 언어 설정과 무관합니다. 이 저장소의 [보조 스크립트](../03_playbooks/scripts/README.md)도 이렇게 찾습니다.
> 2. Preferences > Interface > Translation에서 **New Data** 번역을 끕니다. 코드로는 `bpy.context.preferences.view.use_translate_new_dataname = False`입니다. 이 속성이 bpy 4.2.23 LTS·5.0.1에 있다는 것은 확인했지만, 번역이 실제로 적용되고 꺼지는 동작은 bpy 모듈에 번역 데이터가 없어 확인하지 못했습니다.
> 3. 가장 확실한 방법은 영어 UI입니다.
>
> CLAUDE.md에 넣을 문장: `노드와 소켓은 이름 대신 type과 identifier로 찾을 것. UI 번역 때문에 이름이 바뀔 수 있음.`

**작은 모델·로컬 모델일수록 규칙을 절차로 씁니다.** [roo-blendermcp-jp-rules](https://github.com/hideki711014/roo-blendermcp-jp-rules)(Ollama qwen3.5:9b, Blender 4.5.7 LTS 일본어 UI)는 '품질 형용사 대신 절차 제약', '실제 실패 코드 예시', '데이터가 필요한 작업은 조회한 뒤 수행' 원칙을 적용해 시각 검증 5/5 세션, 충돌 회피 2/2, Suzanne 인식 5/6을 보고했습니다(표본이 작음). 규칙은 "X하지 말 것"보다 "먼저 `get_object_info(name)`로 world_bounding_box를 읽고 그 값으로 location을 계산할 것. 실패 예: `obj.location.z = 0.45`(origin이 가운데면 반쯤 묻힘)"처럼 씁니다. Opus 5.5나 Fable 5.1 같은 프런티어 모델은 규칙을 덜 줘도 되지만, 검증 루프와 증거 요구는 똑같이 필요합니다.

---

## 8. Claude Code 활용

| 기능 | 여기에 넣을 것 | 크기·동작 | 공식 문서 |
|---|---|---|---|
| CLAUDE.md | 매번 지켜야 하는 짧은 규칙 | 매 세션 로드, **200줄 이하** 권장 | [costs](https://code.claude.com/docs/en/costs), [best practices](https://code.claude.com/docs/en/best-practices) |
| Skills | 단계별 레시피, 치수표, 버전 함정 | 설명만 항상 로드, 본문은 호출 시. **SKILL.md 500줄 이하** | [skills](https://code.claude.com/docs/en/skills) |
| Subagents | 비평가, 문서·에셋 조사 | 새 컨텍스트에서 시작 | [sub-agents](https://code.claude.com/docs/en/sub-agents) |
| Hooks | 반드시 지킬 규칙(파괴적 코드 차단, 스크린샷 리마인드) | 결정적으로 실행 | [hooks](https://code.claude.com/docs/en/hooks) |
| `/goal` | 장시간 작업의 완료 조건 | 매 턴 뒤 빠른 모델이 판정 | [goal](https://code.claude.com/docs/en/goal) |

### 8.1 CLAUDE.md: 짧게

CLAUDE.md는 매 세션 로드되고, 너무 길면 중요한 규칙이 묻혀 무시됩니다. 자주 쓰지 않는 워크플로는 Skills로 옮기세요. 완성 템플릿은 [templates/CLAUDE.md](../03_playbooks/templates/CLAUDE.md)에 있고(AGENTS.md로도 사용), 뼈대는 이 정도입니다.

```markdown
# Blender 3D 프로젝트 규칙
- 런타임: Blender 5.x(영어 UI), MCP 서버 이름 'blender'. 1 BU = 1 m, Z-up, origin은 바닥 중앙, 가구 정면 -Y.
- 치수 기준: 03_playbooks/05_reference_dimensions.md의 한국 기준. 추측 금지. 치수는 get_object_info(world bbox)로 확인.
- IMPORTANT: 내가 만들지 않은 오브젝트는 수정·삭제 금지. orphans_purge와 공장 초기화 금지.
- 단계 시작 전 씬 요약, 단계가 끝나면 save_mainfile(incremental=True).
- 이름: SM_/M_/LGT_/CAM_, 컬렉션 COL_Blockout/COL_Hero/COL_Props/COL_Lights/COL_Cameras. 이름은 영어로.
- execute_blender_code: 부품 또는 단계 1개, 멱등(get-or-create), 모듈 재import, 마지막 줄에 요약 print.
- 노드는 type으로 찾기(BSDF_PRINCIPLED). API가 불확실하면 bpy_api_lookup / describe_node_type 먼저.
- 순서: ref → spec → blockout → camera lock → light v1 → forms → materials → light v2 → detail → render → post → export 체크.
- 변경 후: scene_audit 0건 → 프레이밍 → Material Preview → 스크린샷 → 스펙 대비 차이 3줄.
- Compact 시 보존: spec_sheet, 현재 단계, 오브젝트 인덱스, 최신 버전 파일명, 미해결 결함 목록.
```

### 8.2 Skills: 오케스트레이터 + 단계별 서브스킬 + reference

- RobLe3와 arjun988은 오케스트레이터(director)가 의도를 판단해 서브스킬을 체인으로 불러오는 구조로 30~94개 스킬을 운용합니다.
- frontmatter 필드: `name`, `description`, `allowed-tools`, `context: fork`, `agent`, `model`, `effort`, `paths`. `allowed-tools`로 MCP 툴을 미리 승인할 수 있습니다.
- 본문에 `` !`cmd` ``를 쓰면 명령 실행 결과를 동적으로 주입합니다. 예: ``- Blender: !`blender --version | head -1` ``.
- 자동 compaction은 최근 호출한 스킬의 앞 5,000토큰씩을 합계 25,000토큰 예산 안에서 다시 붙입니다. 핵심 규칙은 SKILL.md 앞부분에 두세요.
- 트리거 평가 쿼리를 `evals/evals.json`으로 관리하면 스킬이 엉뚱할 때 불리는 것을 잡을 수 있습니다(RobLe3).

```markdown
---
name: text-to-blender
description: Drive Blender from natural language...
allowed-tools: Read Bash Glob Grep mcp__blender__execute_blender_code mcp__blender__get_scene_info mcp__blender__get_object_info mcp__blender__get_viewport_screenshot
---
```

폴더 구성 예: `SKILL.md`(규칙과 라우팅) + `references/`(assembly-order, 버전 함정, 치수표) + `scripts/` + `evals/evals.json`. 이 저장소의 [스킬 템플릿](../03_playbooks/templates/skills/blender-aaa-scene/SKILL.md)이 스펙 → 빌드 → 감사 → 검토 루프를 이 구조로 담고 있습니다.

### 8.3 비평가 subagent: 만든 쪽이 채점하지 않게

새 컨텍스트에서 시작하는 리뷰어는 결과물을 만든 추론 과정을 보지 않고 결과 자체로 판단합니다. subagent 정의에는 `tools` allowlist, `disallowedTools`, `model`, `mcpServers`, `skills`, `maxTurns`, `effort`를 쓸 수 있습니다. 모델은 Anthropic이 'vision과 computer use에 가장 좋은 Opus'로 소개한 Opus 5.5가 무난합니다(벤더 자체 소개. 모델 선택은 [AI 모델 가이드](01_ai_models_and_clients.md)).

`.claude/agents/blender-critic.md` (작성 예시):

```markdown
---
name: blender-critic
description: Read-only visual critic for Blender scenes. Use after blockout, after lighting/materials, and before export.
tools: mcp__blender__get_viewport_screenshot, mcp__blender__get_scene_info, mcp__blender__get_object_info, Read
model: opus
---
너는 이 씬을 만들지 않은 시니어 아트 디렉터다. spec_sheet와 레퍼런스(경로를 받음)를 기준으로
3/4 히어로, 정면 오쏘, 측면 오쏘, 탑다운을 캡처하라(또는 review/ 폴더의 4방향 렌더를 읽어라).
실루엣과 가독성, 스케일과 비율, 떠 있음과 관통, 노멀과 셰이딩 아티팩트,
재질 사실감(metallic 0/1, roughness 변화), 라이팅 비율과 구도를 각각 1~10점으로 매겨라.
결함은 Blocker/Major/Minor로 나누고, 수치가 들어간 수정안을 최대 3개 제시하라.
판정은 SHIP / SHIP WITH NOTES / NO-SHIP이다. 평균 8 미만이거나 어느 항목이든 7 미만이면 NO-SHIP.
스펙이나 품질에 영향이 없는 취향 문제는 적지 마라.
```

- 점수 게이트(평균 8, 최저 7)는 Bniya-cn의 설계에서, 심각도 분류와 SHIP 판정은 [arjun988 qa-review](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/qa-review/SKILL.md)에서 왔습니다.
- 리뷰어는 문제를 과잉 보고하는 경향이 있습니다. "요구사항에 영향이 있는 결함만"이라고 못 박으세요.
- 문서 조사나 에셋 검색도 subagent에 맡기면 메인 컨텍스트가 깨끗하게 유지됩니다.

### 8.4 Hooks: 권고가 아니라 강제

CLAUDE.md는 권고일 뿐이고 hook은 결정적으로 실행됩니다. matcher는 `mcp__<server>__<tool>` 형식입니다. PreToolUse에서 exit 2를 반환하면 호출이 막히고, PostToolUse에서는 JSON의 `additionalContext`로 Claude에게 메시지를 전달합니다. 핸들러 type은 command, http, mcp_tool, prompt, agent 다섯 가지입니다.

`.claude/settings.json` (작성 예시, 검증 필요):

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "mcp__blender__execute_blender_code",
        "hooks": [{ "type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/bpy-guard.sh" }] }
    ],
    "PostToolUse": [
      { "matcher": "mcp__blender__execute_blender_code",
        "hooks": [{ "type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/remind-shot.sh" }] }
    ]
  }
}
```

`.claude/hooks/bpy-guard.sh`:

```bash
#!/usr/bin/env bash
code=$(jq -r '.tool_input.code // empty')
if echo "$code" | grep -Eq 'orphans_purge|read_factory_settings|import (os|subprocess|shutil)|rmtree'; then
  echo 'Blocked: destructive bpy pattern. Delete objects explicitly by name.' >&2
  exit 2
fi
exit 0
```

`.claude/hooks/remind-shot.sh`:

```bash
#!/usr/bin/env bash
jq -n '{hookSpecificOutput:{hookEventName:"PostToolUse",additionalContext:"Code ran. Before the next mutation: frame the subject, switch to Material Preview, call get_viewport_screenshot, and state 3 concrete diffs vs spec_sheet."}}'
```

- 서버 이름(`blender`)과 코드 파라미터 이름(`code`)은 설정과 서버 버전에 따라 다를 수 있으니 한 번 확인하세요.
- 정규식 차단은 실수 방지용입니다. 보안 경계가 아닙니다(13절).

### 8.5 `/goal`: 텍스트로 증명할 수 있는 조건

`/goal`은 매 턴이 끝날 때 빠른 모델(기본 Haiku)이 조건을 판정하는 Stop 훅입니다. **평가자는 파일을 읽거나 명령을 실행하지 않고 대화에 드러난 내용만 봅니다.** 그래서 '이미지를 봤다'보다 수치와 판정을 텍스트로 출력하게 해야 합니다. 조건은 최대 4,000자입니다.

```text
/goal blender-critic 서브에이전트가 SHIP 판정(평균 ≥8, 최저 ≥7)을 텍스트로 출력하고,
scene_audit summary의 units_with_issues=0, interpenetrating_pairs=0이 출력되며,
versions/에 최신 버전 저장 로그가 출력될 것. 20턴이 지나면 중단.
```

auto mode와 함께 쓰면 무인 실행이 됩니다. 이때도 G1~G3 사람 게이트를 어디에 둘지 먼저 정하세요.

### 8.6 컨텍스트 위생과 작업 메모리

- 같은 문제로 두 번 넘게 교정했다면 컨텍스트가 실패한 시도로 오염된 상태입니다. 배운 점을 반영한 더 나은 프롬프트로 `/clear` 후 새로 시작하세요([best practices](https://code.claude.com/docs/en/best-practices)).
- 단계가 끝날 때마다 `PROGRESS.md`에 spec_sheet 위치, 오브젝트 인덱스, 결함 목록을 적습니다. VIGA는 계획, 코드 diff, 렌더 이력을 담은 메모리로 파인튜닝 없이 자기교정했습니다([VIGA](https://github.com/Fugtemypt123/VIGA)). 형식 예: `반복 n: 목표 / 변경 요약 / 코드 diff 경로 / 렌더 경로 / 남은 문제`. 매 턴 시작 때 최근 3회분만 읽게 합니다.
- 재개할 때: `/clear` → "PROGRESS.md를 읽고 Light v2 단계부터 재개".
- `/compact spec_sheet·현재 단계·버전 파일·미해결 결함만 보존`.
- 쓰지 않는 MCP 서버는 `/mcp`에서 끄고, `/context`로 점유량을 확인합니다.
- Opus 5.5 기본 effort는 medium입니다. 레이아웃·치수 설계처럼 어려운 턴만 올리세요([AI 모델 가이드](01_ai_models_and_clients.md)).

---

## 9. Codex·Gemini CLI 대응 기능

같은 규칙을 AGENTS.md로 공유하면 세 하네스에서 같은 운영 방식을 쓸 수 있습니다. Agent Skills 포맷(SKILL.md)과 [AGENTS.md](https://github.com/agentsmd/agents.md)가 사실상 공용 표준이 되었습니다.

> **Gemini CLI 주의**: 2026-06-18부터 무료·Google AI Pro·Ultra 사용자의 요청 처리를 멈추고 Antigravity CLI로 넘어갔습니다. 아래 Gemini CLI 설정은 유료 API 키나 Code Assist Standard/Enterprise 사용자에게만 해당합니다([AI 모델 가이드](01_ai_models_and_clients.md)).

| 기능 | Claude Code | Codex (GPT-6 Astra 등) | Gemini CLI |
|---|---|---|---|
| 프로젝트 규칙 파일 | CLAUDE.md | AGENTS.md | GEMINI.md 계층(글로벌 `~/.gemini/GEMINI.md`, 워크스페이스, JIT). `context.fileName`에 `["AGENTS.md","GEMINI.md"]` 지정 가능([문서](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md)) |
| MCP 추가 | `claude mcp add blender -- uvx mcp-for-blender` | `codex mcp add blender -- uvx mcp-for-blender` (설정 파일 `~/.codex/config.toml`) | settings.json의 `mcpServers`(command, args, env, timeout, trust, includeTools/excludeTools) |
| 스킬 | `.claude/skills/<name>/SKILL.md` | `~/.codex/skills/` 또는 저장소 안 `.agents/skills/`, 호출은 `$skill-name`. **공식 문서 미확인**이라 두 경로를 모두 적어 둠([codex docs/skills.md](https://github.com/openai/codex/blob/main/docs/skills.md)는 차단된 공식 사이트로 연결) | 이 조사 범위 밖 |
| 툴 노출 줄이기 | MCP 툴 정의 지연 로딩(tool search) 기본, `/mcp`로 서버 끄기 | (미확인) | `includeTools`/`excludeTools`(둘 다 있으면 exclude 우선) |
| 이미지 결과 | MCP 툴 이미지를 인라인으로 표시, 원본은 tool-results에 저장 | (미확인) | text/image/audio/resource 멀티파트 결과 |
| effort | Opus 5.5 기본 medium | **Astra 기본 low**(Codex models.json 기준, 6단계 low~ultra). `model_reasoning_effort`로 꼭 지정 | — |
| 비평가·훅·목표 | subagent, hooks, `/goal` | (대응 기능 미확인) | (대응 기능 미확인) |

Codex 스킬 호출 예([CheshireJCat](https://raw.githubusercontent.com/CheshireJCat/create-3d-model-skill/main/README.md)):

```text
Use $create-3d-model to create a low-poly desk lamp from my description.
Inspect the current scene first and do not delete existing objects.
Capture and inspect screenshots after the blockout and final version.
Export a GLB and preserve a versioned Blender source.
```

Gemini CLI 설정 예(필요한 툴만 노출, [MCP 문서](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md)):

```json
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["mcp-for-blender"],
      "includeTools": ["get_scene_info", "get_object_info", "get_viewport_screenshot", "execute_blender_code"],
      "timeout": 600000
    }
  }
}
```

- Codex 쪽 사례: [Arnie936/codex-blender-higgsfield](https://github.com/Arnie936/codex-blender-higgsfield)(이미지 생성 → Blender 씬, 생성마다 사용자 승인), [Bniya-cn](https://github.com/Bniya-cn/blender-design-master)(Codex에서만 실제 테스트).
- Codex의 타임아웃 키(`tool_timeout_sec` 등)와 effort 설정은 [AI 모델·클라이언트 가이드](01_ai_models_and_clients.md)를 보세요. Google Antigravity 설정은 비공식 개인 가이드만 있어 여기서는 다루지 않습니다(미검증).
- GPT-6 Astra와 Gemini의 이미지 토큰 산정 방식은 확인하지 못했습니다.

---

## 10. 컨텍스트·이미지 토큰·비용

### 10.1 이미지 토큰

Claude의 이미지 비용은 **⌈w/28⌉ × ⌈h/28⌉** 비주얼 토큰입니다. Claude 4.7 이후 모델은 high-res tier(긴 변 2576px, 최대 4,784토큰)로 처리됩니다([vision 문서](https://platform.claude.com/docs/en/build-with-claude/vision)).

| 이미지 | 계산 | 토큰 | 비고 |
|---|---|---|---|
| 800×450 | 29 × 17 | 493 | 애드온 함수 기본값(800) 기준 |
| **1000×563** | 36 × 21 | **756** | **ahujasid MCP `get_viewport_screenshot` 기본 캡처**(서버 기본 `max_size=1000`. docstring의 800은 틀림) |
| 768×768 | 28 × 28 | 784 | `review_views.py` 기본(res=768). 4장이면 약 3,136 |
| 1920×1080 | 69 × 39 | 2,691 (high-res tier, Opus 5.5) / 1,560 (standard tier 모델) | 최종 판정용 |

- **한 요청에 이미지가 20장을 넘으면**(이전 턴에서 다시 보내는 이미지와 tool_result 안의 스크린샷 포함) 이미지당 치수 제한이 더 엄격해집니다. 문서는 각 변을 **2000px 이하**로 줄이라고 권합니다. 2576px 렌더를 그대로 넣으면 `invalid_request_error`가 날 수 있습니다.
- 에이전트 루프는 매 요청마다 전체 이력을 다시 보냅니다(캐시 읽기로 과금). 초반에 찍은 스크린샷도 세션이 끝날 때까지 비용이 듭니다. 1000px 스크린샷 20장이면 약 15,000토큰이 이후 매 턴 컨텍스트에 남습니다.
- MCP 툴이 반환한 이미지는 인라인으로 보일 때 축소·압축될 수 있고, `MAX_MCP_OUTPUT_TOKENS` 한도에도 포함됩니다.

### 10.2 툴 스키마와 MCP 출력 한도

- ahujasid 서버의 툴 스키마만 **6,928토큰**입니다. 2026-08-19~09-03 사이에 5,462토큰에서 27% 늘었고(툴 25개 → 28개, [issue #347](https://github.com/ahujasid/blender-mcp/issues/347)), 지금 main의 `server.py`에는 툴이 36개라 더 클 가능성이 큽니다.
- Claude Code는 MCP 툴 정의를 기본적으로 지연 로딩하므로 이 비용을 처음부터 다 내지 않습니다. Claude Desktop이나 Cursor처럼 정의를 한꺼번에 올리는 클라이언트에서 부담이 큽니다.
- 툴이 많은 서버는 '점진적 공개'를 씁니다. [blender-mcp-pro](https://github.com/youichi-uda/blender-mcp-pro)(120개 이상, 유료)는 처음에 15개만 노출하고 `enable_tools(category)`로 필요할 때 켭니다. [blend-ai](https://github.com/HoldMyBeer-gg/blend-ai)는 186개 툴이라 스키마가 클 수 있습니다(추정).
- Claude Code의 MCP 출력 한도: `MAX_MCP_OUTPUT_TOKENS` 기본 25,000, 10,000을 넘으면 경고. 이미지가 없는 결과가 한도를 넘으면 파일로 빠집니다.

### 10.3 단가와 세션 비용 추정

단가(1M 토큰당, [Claude 가격 문서](https://platform.claude.com/docs/en/about-claude/pricing)):

| 모델 | 입력 | 출력 | 캐시 읽기 | 캐시 쓰기 |
|---|---|---|---|---|
| Claude Opus 5.5 | $4 | $20 | $0.20 (0.05×) | 5분 $5, 1시간 $8 |
| Claude Sonnet 5 | $2 | $10 | $0.20 | (9월 1일 예정이던 $3/$15 인상은 취소됨) |
| Claude Fable 5.1 | $10 | $50 | $0.25 (0.025×) | — |

세션 추정(**가정 기반 추정치**이며 실측 로그가 아닙니다): 툴 호출 60회, 평균 컨텍스트 80k → 캐시 읽기 480만 토큰, 새 입력 20만 토큰(5분 캐시 쓰기 1.25×), 출력 10만 토큰(사고 토큰 포함).

| 모델 | 캐시 읽기 | 새 입력 | 출력 | 합계 |
|---|---|---|---|---|
| Sonnet 5 | $0.96 | $0.50 | $1.00 | **약 $2.5** |
| Opus 5.5 | $0.96 | $1.00 | $2.00 | **약 $4.0** |
| Fable 5.1 | $1.20 | $2.50 | $5.00 | **약 $8.7** |

독립 검증에서 산술은 맞는 것으로 확인했습니다(Sonnet 5 ≈ $2.46, Opus 5.5 ≈ $3.96, Fable 5.1 ≈ $8.70). 참고로 Claude Code 기업 평균 비용은 활동일 기준 개발자 1인당 약 $13입니다([costs](https://code.claude.com/docs/en/costs)). GPT-6 Astra 단가와 실측 사례 비용은 [AI 모델 가이드](01_ai_models_and_clients.md)에 있습니다.

### 10.4 절약 수칙

1. 반복 루프의 뷰포트 캡처는 800~1000px이면 충분합니다. 1920px 렌더는 최종 판정에만 씁니다.
2. 숫자 검사(`scene_audit.py`)를 먼저 통과시키면 이미지 비평 횟수가 줄어듭니다.
3. 여러 단계를 묶은 작업은 끝에서 한 번만 캡처합니다.
4. 문서 조사·에셋 검색은 subagent로 보내 메인 컨텍스트를 가볍게 유지합니다.
5. 오래된 스크린샷이 쌓였으면 PROGRESS.md에 요약하고 `/clear`로 새로 시작합니다.
6. 쓰지 않는 MCP 서버는 끄고, Gemini는 `includeTools`로 필요한 툴만 노출합니다.

---

## 11. MCP 타임아웃 설정

긴 Cycles 렌더, 대용량 익스포트, 베이크는 여러 계층의 타임아웃에 걸립니다. **가장 짧은 값이 이깁니다.**

| 계층 | 기본값 | 설정 방법 | 메모 |
|---|---|---|---|
| ahujasid 서버 ↔ 애드온 소켓 | **180초** | 서버 내부 | 클라이언트 값을 늘려도 이 한도는 남습니다 |
| ahujasid 애드온 `exec()` | **제한 없음** | — | 무한 루프나 거대한 루프는 Blender 자체를 멈춥니다 |
| Claude Code 툴 타임아웃 `MCP_TOOL_TIMEOUT` | 설정하지 않으면 약 28시간 | 환경변수, 또는 `.mcp.json` 서버별 `"timeout"`(ms) | [MCP 문서](https://code.claude.com/docs/en/mcp) |
| Claude Code 유휴 타임아웃 `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT` | stdio 서버(ahujasid·공식 Blender 서버 기본) **30분**, HTTP·SSE·WebSocket·claude.ai 커넥터 **5분** (공식 문서 기준, 검토 단계에서 원문 확인) | 환경변수 | 진행 알림 없이 오래 걸리는 툴이 끊길 수 있습니다. 긴 렌더는 헤드리스로 분리하세요 |
| Gemini CLI | 600,000ms(10분) | settings.json `timeout` | |
| Codex | [AI 모델 가이드](01_ai_models_and_clients.md) 참고 | `~/.codex/config.toml` | 공식 문서를 직접 확인하지 못함 |
| headless QA 서버 [ellmos](https://github.com/ellmos-ai/ellmos-blender-use-mcp) `blender_run_script` | 최대 600,000ms(10분), 출력 tail 기본 8,000자(최대 50,000자) | — | README에 규모에 비해 과장된 문구가 많습니다(신뢰도 낮음). 채택 전에 동작을 확인하세요 |

`.mcp.json` 예:

```json
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["mcp-for-blender"],
      "timeout": 600000,
      "env": { "DISABLE_TELEMETRY": "true" }
    }
  }
}
```

**실무 규칙**: 1분 넘게 걸릴 작업(최종 Cycles 렌더, 대형 익스포트, 베이크)은 MCP로 부르지 말고 `blender -b scene.blend --python scripts/render_final.py`처럼 headless로 분리합니다. 대화형 루프에서는 해상도·샘플을 낮춘 미리보기만 돌립니다.

---

## 12. 멀티 MCP 조합 규칙

### 12.1 순서

1. **상태 확인**: `get_addon_status` → `get_polyhaven_status`·`get_sketchfab_status` 등으로 통합 상태를 봅니다(kiln).
2. **기존 에셋 우선**: 라이브러리에서 먼저 찾고, 없을 때만 생성합니다(ahujasid `asset_creation_strategy`).
3. **유료 생성 전 승인**: 크레딧을 확인하고 사용자 승인을 받습니다(Codex 사례: "Higgsfield kostet Credits, frag vor jeder Generierung"). ahujasid에서 **Tripo는 유료 [Premium](https://www.mcp-for-blender.com/premium) 전용**이고, Hyper3D Rodin과 Hunyuan3D는 자기 키(BYOK)나 Premium 키로 씁니다.
4. **컨셉 이미지 규칙**: 배경이 없거나 흰 배경인 단일 뷰, 캐릭터는 T-pose, 바닥과 환경은 AI로 생성하지 않습니다(kiln Rules 9, 11~13).
5. **임포트 직후 정리**: 규약대로 이름 변경 → 1 BU = 1 m 스케일 확인 → transform 적용 → merge by distance(0.0001 m) → 노멀 재계산. 방향은 가구 정면 규약에 맞춥니다.
6. **라이선스 기록**: 출처와 라이선스를 `_log.md`에 남깁니다(kiln Rule 17). Poly Pizza 에셋은 약 69%가 CC-BY라 저작자 표기 의무가 있고, ahujasid는 attribution 문자열을 커스텀 속성으로 저장합니다. `licence='CC0'` 필터로 표기 의무를 피할 수도 있습니다.
7. **문서 서버**(Context7 등)는 코딩 단계에서만 켭니다.

> **[한국 사용자] Hunyuan3D 로컬 사용 주의**: Tencent Hunyuan3D 계열 오픈웨이트(2.0/2.1/Omni/Part 등) 라이선스는 적용 지역에서 EU·영국·**대한민국**을 빼고, 출력물 사용도 제한합니다. 한국에서 로컬로 돌리는 것은 라이선스 범위 밖입니다. Tencent Cloud API 약관은 별개이며 원문을 확인하지 못했습니다. kiln처럼 Hunyuan3D를 소스로 쓰는 스킬을 그대로 가져오지 말고 생성 소스를 바꾸세요. 자세한 내용은 [에셋·라이선스](10_assets_pipeline_licensing.md)를 보세요.

### 12.2 포트·이름 충돌

| 서버 | 포트 | 주의 |
|---|---|---|
| 공식 Blender Lab 서버 | localhost:9876 | ahujasid와 같은 포트. 실행 파일 이름도 `blender-mcp` |
| ahujasid MCP for Blender | localhost:9876 | `uvx blender-mcp`는 호환 래퍼로 이 커뮤니티 서버를 실행 |
| Scenario for Blender 플러그인 내장 MCP | `http://127.0.0.1:9876/mcp` | 위 두 서버와 같은 포트. 셋 중 하나만 켜기 |
| blender-mcp-pro | 9877 | 유료 서버 |
| Gaius114 자체 애드온 | HTTP 7234 | `/screenshot`, `/render`가 base64 PNG 반환 |
| Epic Unreal MCP (UE 5.8) | `http://127.0.0.1:8000/mcp` | AllToolsets 필요 |

- **한 Blender에는 서버 하나만 붙이세요.** MCP 서버 인스턴스도 하나만 실행해야 합니다.
- 툴 이름에는 네임스페이스를 분명히 붙이는 것이 좋습니다(Anthropic [writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)). 여러 스킬 라이브러리를 섞으면 이름이 충돌하니, claude-3d-harness처럼 레지스트리에서 한 서버로 정리하는 방법도 있습니다.
- 설치 명령과 이름 혼동은 [Blender MCP 가이드 2.2절](02_blender_mcp.md)과 [빠른 시작](../03_playbooks/01_quickstart_setup.md)을 보세요.

### 12.3 조합 예시

| 목적 | 조합 |
|---|---|
| 단일 히어로 소품 | Blender MCP(1개) + 스킬팩 + `scene_audit.py`/`review_views.py` + 비평가 subagent. 최종 렌더·익스포트는 headless |
| 에셋 기반 인테리어 | Blender MCP의 Poly Haven/Sketchfab/Poly Pizza + 배치는 [`placement_utils.py`](../03_playbooks/scripts/README.md)와 [배치 가이드](08_scene_layout_placement.md)의 관계 제약 방식 |
| 유기체·조각 포함 씬 | 3D 생성 MCP(한국이면 Hunyuan3D 로컬 제외) → 리메시 → 코드로 스케일·origin·방향 정규화 → 배치 → 재질 |
| 치수 정확도가 중요한 부품 | CAD 코드 MCP(예: [build123d-mcp](https://github.com/pzfreo/build123d-mcp), Apache 2.0)로 만들고 측정한 뒤 STEP/STL로 Blender에 가져오기. 다른 CAD 앱은 [기타 DCC·CAD 가이드](03_other_mcp_dcc_cad_engines.md) |
| 이미지 생성 → 3D 씬 | 이미지 생성 CLI/MCP(생성마다 승인) → 레퍼런스로 Blender 씬 구성([codex-blender-higgsfield](https://github.com/Arnie936/codex-blender-higgsfield)) |
| 게임 엔진까지 | Blender에서 익스포트 → 엔진 MCP. Anthropic 크리에이티브 커넥터 9종 중 3D에 직접 관련된 것은 Blender, Autodesk Fusion, SketchUp입니다([발표](https://www.anthropic.com/news/claude-for-creative-work)) |

**툴 카드와 계획 먼저**: SceneWeaver는 여러 생성 방법(검색, 절차적 생성, 수정 도구)을 설명이 붙은 툴 카드로 등록해 에이전트가 골랐고, SceneOrchestra는 이 반복이 느리다고 보고 전체 툴 호출 순서를 먼저 예측했습니다. 실무에서는 MCP 서버마다 '언제 쓰는가, 입력, 출력, 한계'를 1~3줄 카드로 CLAUDE.md에 적고, 계획 단계에서 전체 호출 순서를 먼저 쓰게 한 뒤 렌더 검증은 단계 경계에서만 합니다.

### 12.4 Unreal Engine에서 에이전트 운용 규칙 (Epic 공식 스킬 기준)

설치는 `/plugin install unreal-engine-skills-for-claude-code@claude-plugins-official`, 에디터 콘솔에서 `ModelContextProtocol.StartServer`, `ModelContextProtocol.GenerateClientConfig ClaudeCode`(Codex는 `... Codex`)입니다. 확인은 `/mcp` 후 "List all actors in the current level"로 합니다([Epic 플러그인](https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin), [unreal-mcp SKILL.md](https://raw.githubusercontent.com/EpicGames/unreal-engine-skills-for-claude-code-plugin/main/skills/unreal-mcp/SKILL.md)).

- 대량 변경 전후로 저장과 커밋을 합니다(MCP 편집은 항상 undo되지 않음).
- 컴파일과 셰이더 작업이 끝날 때까지 기다린 뒤 호출합니다.
- 같은 에셋에 대한 의존 호출은 직렬화합니다.
- 결과는 읽기 전용 호출로 다시 확인합니다. 많은 툴이 예외 없이 status만 돌려줍니다.
- PIE(에디터 내 플레이) 중인지 확인합니다.
- 탐색 순서는 `list_toolsets` → `describe_toolset` → `call_tool`입니다. 프로젝트 스킬(`AgentSkillToolset.ListSkills`)이 일반 규칙보다 우선합니다.
- 빌드, 테스트, 쿡은 headless 커맨드라인을 우선하고 로그와 JSON 요약을 `Saved/AgentRuns/<kind>-<run-id>`에 남깁니다([Codex용 커뮤니티 스킬](https://github.com/WildCake/unreal-engine-mcp-codex)).
- 엔진 쪽 설정 전반은 [기타 DCC·CAD·게임엔진 가이드](03_other_mcp_dcc_cad_engines.md)를 보세요.

---

## 13. 보안 체크리스트

`execute_blender_code`는 Blender 권한으로 임의 Python을 실행하고 타임아웃도 없습니다. 사실상 OS 권한을 넘기는 것과 같습니다.

- [ ] **작업 전 저장과 git 커밋.**
- [ ] **`BLENDER_MCP_SAFE_MODE=1`을 켜되 샌드박스로 믿지 않기.** 막는 것: `open()`·`os` 같은 직접 파일 I/O, 프로세스 실행, 네트워크, handlers/timers/drivers, 외부 `.blend` append/link. 허용하는 것: bpy를 통한 저장·열기, import/export, 렌더. 검사는 **MCP 경로에만** 걸리고, 애드온 소켓은 로컬의 어떤 프로세스가 보낸 raw `execute_code`도 받습니다. 개발자도 "not a sandbox around Blender"라고 적었습니다.
- [ ] **`DISABLE_TELEMETRY=true`.** 콘텐츠(프롬프트, 코드, 스크린샷, 궤적)는 옵트인이지만, 익명 사용 기록(설치 ID, 세션 ID, 툴 이름, 성공 여부, 소요 시간, 버전, OS)은 **기본으로 수집**됩니다. README는 수집 데이터가 AI 모델 학습에 쓰일 수 있다고도 적었습니다. 서버 프롬프트는 사용자 수락·거절 내용을 `record_trajectory_feedback`으로 기록하라고 지시하니 동작을 이해하고 쓰세요.
- [ ] **localhost 바인딩 유지, 공유 머신에서 쓰지 않기.** Epic도 "Localhost is not a trust boundary"라고 경고하고, Unreal의 `ProgrammaticToolset.execute_tool_script`도 임의 Python을 실행합니다.
- [ ] **`--dangerously-skip-permissions` 금지**(Epic 명시). auto mode나 명시적 allow 규칙을 쓰세요.
- [ ] **프로젝트 `.mcp.json` 서버는 신뢰를 확인한 뒤 승인.** `claude -p` 비대화형 실행에서는 확인 없이 로드됩니다([security](https://code.claude.com/docs/en/security), [mcp](https://code.claude.com/docs/en/mcp)).
- [ ] **프롬프트 인젝션 주의.** 에셋 설명이나 웹 콘텐츠처럼 MCP가 가져오는 외부 텍스트는 지시가 아니라 데이터로 다룹니다.
- [ ] **다운로드한 `.blend`의 Python 자동 실행 끄기**(Preferences > Save & Load > Auto Run Python Scripts. blend-ai도 비활성화).
- [ ] **hooks로 파괴적 패턴 차단**(8.4절). 단 정규식은 실수 방지용입니다.
- [ ] **임의 코드를 아예 없애는 선택지**: [blend-ai](https://github.com/HoldMyBeer-gg/blend-ai)(허용 import 5개: bpy, bmesh, mathutils, math, json, 셰이더 노드 64종 allowlist, 텔레메트리 없음, 127.0.0.1 바인딩). 2026-10-02 확인: [blenderwright](https://github.com/HoldMyBeer-gg/blenderwright)로 이름이 바뀌었고 LICENSE는 **MIT**(이전 조사 시점 표기는 AGPL-3.0-or-later).
- [ ] **CI 검증은 포트가 열리지 않는 headless 경로로 분리**(`blender -b`, 또는 신뢰도를 확인한 headless QA 서버).
- [ ] **VM이나 dev container에서 실행하는 것도 고려.**
- [ ] **스킬·서버 라이선스 확인**: Bniya-cn blender-design-master는 라이선스가 없고, 공식 Blender Lab 서버는 GPL-3.0-or-later입니다(번들 배포 시 주의).

---

## 14. 연구가 뒷받침하는 원칙

확인한 학술 연구 대부분은 GPT-4o/GPT-4V/Claude 3.5~3.7/GPT-5 세대 모델로 실험했습니다. **GPT-6 Astra, Claude Fable 5.1, Opus 5.5를 직접 평가한 동료심사 논문은 찾지 못했습니다.** 수치는 방향을 잡는 근거로만 쓰세요. 논문별 주석은 [학술 연구 가이드](11_research_papers.md)에 있습니다.

| 원칙 | 근거(수치) | 실무 적용 |
|---|---|---|
| **LLM은 코드만 보고 결과를 상상하지 못한다** | [SGP-Bench](https://github.com/sgp-bench/sgp-bench)(ICLR 2025 Spotlight): GPT-4o가 렌더 없이 SVG 프로그램 의미를 맞힌 비율 64.8%(추론 문항 50.4%), CAD 72.9%. SGP-MNIST에서는 모든 모델이 5.5~13.0%(우연 수준 10%) | 매 수정 후 반드시 렌더나 스크린샷을 보여 줍니다 |
| **검증에 연산을 쓴다** | [BlenderGym](https://github.com/richard-guyunqi/BlenderGym-Open)(CVPR 2025 Highlight, 씬 245개·과제 5개): 검증 비율 0.33/0.62/0.73을 비교해 적정 비율이 있고, **총 연산이 클수록 검증 비중을 높이는 쪽이 유리**했습니다. '0.62~0.73이 최적'이라는 고정 범위는 과잉 해석이라 정정됐습니다. verifier 추론을 늘린 오픈 모델이 폐쇄 모델 verifier를 넘기도 했습니다 | 후보 2~3개를 만들고 렌더해서 비교 판정으로 고릅니다. 예산이 크면 생성보다 검증에 더 씁니다 |
| **VLM 판정은 사람만큼 믿을 수 없다** | BlenderGym: verifier와 사람의 일치율 Claude-3.5-Sonnet 0.66, 사람끼리 0.79 | 순서를 바꿔 두 번 판정하고, 숫자 검사를 먼저, 최종은 사람 |
| **폐루프가 표준** | SceneCraft, BlenderAlchemy, LL3M, [VIGA](https://github.com/Fugtemypt123/VIGA), CADCodeVerify, SceneReVis, SceneSmith가 모두 '코드 → 실행 → 렌더 → 비평 → 수정' 루프. 원샷은 기준선으로만 쓰임 | 4절의 루프 |
| **좌표는 솔버, LLM은 관계·제약** | [SceneReVis](https://github.com/Runder-sun/SceneReVis) 비교표(침실+거실 평균) 충돌률: LayoutGPT 40.8%, LayoutVLM 36.8%, I-Design 16.2%, [Holodeck](https://github.com/allenai/Holodeck)(DFS 제약 솔버) 12.7%, SceneReVis(멀티턴 RL) 4.5%. 경쟁 논문이 잰 값이고, 미분 최적화를 쓰는 LayoutVLM도 36.8%였으니 '솔버만 쓰면 해결'로 일반화하지는 마세요 | LLM은 `against_wall`, `in_front_of`, `face_to` 같은 관계를 JSON으로 쓰고, 좌표는 스크립트가 계산합니다([배치 가이드](08_scene_layout_placement.md), `placement_utils.py`) |
| **계층 단계로 만든다** | [SceneSmith](https://github.com/nepfaff/scenesmith)(ICML 2026 Spotlight): 평면도 → 가구 → 벽 부착물 → 천장 → 소품, 단계마다 designer/critic/orchestrator. 기존 대비 객체 수 3~6배, 객체 간 충돌 0(프로젝트 페이지 기준, arXiv 요약은 "2% 미만"), 시뮬레이션 뒤 96% 안정, 사용자 205명 연구에서 베이스라인 대비 평균 승률 realism 92%·faithfulness 91% | 단계마다 게이트, 소품은 지지면 목록을 먼저 뽑고 그 위에만 배치 |
| **처음부터 만들기보다 검색·재사용** | Holodeck(Objaverse), SceneSmith(HSSD/Objaverse/PartNet-Mobility, SAM3D·Hunyuan3D-2 생성), [SAGE](https://github.com/NVlabs/sage)(TRELLIS·재질 생성·레이아웃 솔버를 별도 서버로) | 유기체·조각은 생성하거나 라이브러리에서 가져오고, 코드는 배치·재질·조명을 맡음 |
| **파라메트릭 부품 코드** | [3D-GPT](https://github.com/Chuny1/3DGPT)(절차적 생성 함수의 파라미터만 추론), [Scene Language](https://github.com/zzyunzhi/scene-language)(loop·transform 프리미티브), [MeshCoder](https://github.com/InternRobotics/MeshCoder)(파트별 Blender 코드, 100만 쌍 학습), [Procedura](https://arxiv.org/abs/2608.26238)(2026-08: 파트별 파라메트릭 프로그램 + typed mate로 떠 있거나 파고드는 파트를 측정해 거부) | `def make_chair(seat_h=0.45, seat_w=0.5, leg_th=0.035, back_h=0.4)`처럼 함수부터 쓰고, 파트 이름을 붙이고, 파트마다 bbox를 print해 접촉·부유를 스스로 검사 |
| **API 문서를 검색해 붙인다** | LL3M의 BlenderRAG, 3DCodeBench의 Blender 5.0 API 함정 목록 | 7절 |
| **실행 오류는 traceback으로 3회 재시도** | [3DCodeBench](https://github.com/gaoypeng/3dcodebench)(2026-06, Blender 5.0, 212 카테고리, Claude Code/Codex/Gemini CLI 하네스, trial 82,042개와 에이전트 transcript 2,767개 공개): 멀티턴 설정 T=3 | 6.2절 |
| **비평은 큰 구조 문제만** | 3DCodeBench 비평 프롬프트: '사소한 미감에 대한 과도한 반복을 피하라' | 4.5절 종료 조건 |
| **작업 메모리를 파일로** | VIGA: 계획·코드 diff·렌더 이력 메모리로 파인튜닝 없이 자기교정 | PROGRESS.md(8.6절) |
| **후보 탐색과 되돌리기** | [BlenderAlchemy](https://github.com/ianhuang0630/BlenderAlchemyOfficial)(ECCV 2024): 후보 편집 여러 개 → VLM이 렌더 비교로 선택 → 나아지지 않으면 이전 가설로 복귀 | 편집 전 저장, 나빠지면 직전 버전으로(6.5절) |
| **목표를 이미지로 먼저** | BlenderAlchemy의 visual imagination, Scenethesis의 가이던스 이미지 | 3.3절 |
| **편집 연산을 줄이고 상태를 구조화** | SceneReVis 6개 원자 연산, SceneAssistant 매 스텝 이미지 + JSON 상태 | 6.4절 |
| **VLM에게는 격자 지도를** | TreeSearchGen: 이모지 격자, 가구 0.3m·소품 0.1m | 4.4절 |
| **모델 버전에 워크플로를 묶지 않는다** | LL3M은 논문에 쓴 Claude Sonnet 3.7이 retire되자(2026-02-19) 서버를 중단했습니다. Scene Language(기본 3.7 Sonnet)와 BlenderGym의 Claude 기준선도 원래 설정으로는 재현되지 않습니다([deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)) | 프롬프트·툴 정의는 모델 중립적으로 쓰고, 새 모델이 나오면 같은 과제 세트로 회귀 테스트(3DCodeBench 카테고리 일부 활용) |
| **특화 파인튜닝은 실행률을 올리지만 범위가 좁다** | BlenderLLM: 구문 오류율 3.4%(범용 모델 15.6~21.4%), 스스로 '기본 모델링만' | AAA 품질에는 프런티어 모델 + 렌더 루프가 현실적 |

참고로 LLM이 만든 씬 프로그램의 오류를 LLM 없이 프로그램 탐색으로 고치는 연구([SIGGRAPH Asia 2025](https://arxiv.org/abs/2510.16147))도 있어서, '좌표·제약 수정은 결정적 알고리즘에 맡긴다'는 방향을 뒷받침합니다. Geometry Nodes를 LLM이 편집할 수 있는 Python으로 바꾸는 [ProcFunc](https://github.com/princeton-vl/procfunc/blob/main/experiments/EXPERIMENTS.md)도 LLM/VLM 편집 실험을 함께 공개했습니다.

---

## 15. 실제로 이렇게 했다: 사례에서 나온 교훈

| 누가 | 무엇을·어떻게 | 결과 | 교훈 |
|---|---|---|---|
| [RobLe3](https://github.com/RobLe3/cc-blender-skill) (2026-05 전후, Claude Code) | 칼, 병, 의자, 선글라스, 데스크 램프, 아바타. 치수표 → 11단계 → 시각 검증 → IoU/bbox 수치 검증 → [quality-refinement-autoloop](https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/quality-refinement-autoloop/SKILL.md)로 실패 원인을 진단하고 스킬을 패치해 재빌드 | 실패 렌더까지 공개. 미감은 범위 밖이라고 명시 | 스킬 자체를 결과에 맞춰 고치는 루프 |
| [elithril blender-kiln](https://github.com/elithril/blender-kiln) (2026-08-27) | 텍스트 브리프 → 웹용 GLB 15종(주의: 갤러리 15종은 스킬·MCP 실행 결과가 아니라 `blender --background --python` 스크립트 경로 결과라고 README가 밝힘). 단계마다 씬 정보·스크린샷, 파괴적 작업은 제안 후 선택 | 1,456.2kB → 132.7kB(91%), MCP·headless 결과 동일 | 대화형으로 만들고 headless로 재현 |
| [bsantanna](https://github.com/bsantanna/roblox-flex-with-friends) (2026-07, Claude Code) | Roblox 게임(5개 존, Luau 모듈 100개 이상)을 며칠 만에 개발, Blender MCP로 공간 관계 측정·다각도 검증 | 플레이 가능한 게임 | 코드만으로 3D 공간을 검증할 수 없다 |
| [MMMvinki](https://github.com/MMMvinki/little-prince-planet-world) (2026-09-10) | 생성 스크립트를 파일로 보관해 행성 8개와 캐릭터·소품 제작, GLB 파싱 테스트로 구면 카메라 252곳 검증 | 모델링 마찰은 줄었지만 검증 인프라가 상당히 필요 | 스크립트를 원본으로 남기면 재현과 테스트가 됨 |
| [hideki711014](https://github.com/hideki711014/roo-blendermcp-jp-rules) (2026-05, qwen3.5:9b) | 일본어 UI Blender를 로컬 9B 모델로 제어. 관찰된 실패를 규칙에 실패 예시로 넣음 | 시각 검증 5/5, 충돌 회피 2/2 | 현지화 UI는 type 기반 탐색, 작은 모델은 절차 규칙 |
| [Gaius114](https://github.com/Gaius114/blender-claude-mcp) (2026, Claude Code) | 도넛, 에스프레소 잔, 와인병, 과일 바구니. spec_sheet → plan_validator로 분해 계획 검증 → 실행·렌더·분석 반복 | renders/ 폴더에 결과 | 형상 만들기 전 계획 검증 게이트 |
| [Arnie936](https://github.com/Arnie936/codex-blender-higgsfield) (2026-09-08, Codex) | 설치 자동화 → 테스트 씬 → 이미지 생성 크레딧 확인 → 생성마다 승인 → 씬 구성 | 정량 평가 없음 | 유료 생성은 매번 승인 |
| [Bniya-cn](https://github.com/Bniya-cn/blender-design-master) (2026-08-25, Codex) | 읽기 전용 비평가와 점수 게이트를 둔 멀티에이전트 | Level 0 테스트에서 Final Gate 평균 7.4로 미통과 | 게이트를 엄격히 두면 '통과 못 함'이 정상 결과일 수 있음 |

더 많은 사례는 [사례 모음](../04_case_studies/01_case_studies.md), 한국어 자료는 [한국어 자료 모음](../04_case_studies/02_korean_resources.md)에 있습니다.

---

## 16. 킥오프 프롬프트

재사용 템플릿 전체는 [프롬프트 템플릿](../03_playbooks/03_prompt_templates.md)에 있습니다. 여기서는 이 문서의 규칙을 한 번에 담은 두 가지를 싣습니다.

**단일 히어로 에셋(가구)**

```text
[역할] 너는 Blender 5.x를 MCP로 조작하는 시니어 테크니컬 아티스트다.
[입력] Image 1: 정면 레퍼런스, Image 2: 측면 레퍼런스(미드센추리 원목 라운지 체어).
[목표] 게임용 히어로 에셋 SM_LoungeChair. 삼각형 ≤ 8k, 텍스처 2K PBR, GLB로 전달.
[제약] 1 BU = 1 m, Z-up, origin 바닥 중앙, 정면 -Y. 좌면 높이 0.40~0.43 m.
       기존 오브젝트 삭제 금지. 유료 API는 내 승인 후에만. 이름은 영어로.
[절차]
 1) 씬 요약 → 경로를 지정해 versions/chair.blend로 저장
 2) spec_sheet 작성 후 멈추고 내 확인 대기 (G1)
 3) 실측 스케일 블록아웃 + 카메라(50mm, 높이 1.1 m, 3/4 뷰)
 4) scene_audit 0건 확인 → 4방향 캡처로 레퍼런스 비율(H:W:D) 오차 3% 이내까지 수정 → 멈추고 확인 (G2)
 5) 카메라 고정, 무채색 3점 조명 v1
 6) 1차 형태(좌판, 등판, 다리) → 2차(곡률, 테이퍼, 접합부 5~15mm 관통) → 3차(베벨 2~4mm, 이음새)
 7) 재질 v1(명도) → 색
 8) 조명 v2(키:필 약 3:1, 색온도)
 9) blender-critic 서브에이전트로 채점
10) 최종 렌더는 headless로, 익스포트 8항목 체크 → GLB → 멈추고 확인 (G3)
[검증] 매 단계: scene_audit → 프레이밍 → Material Preview → 스크린샷 → 스펙 대비 차이 3줄 → 수정
       → save_mainfile(incremental=True). 숫자가 통과해도 이미지가 틀리면 실패다.
[보고] 오브젝트별 트라이 수, 재질, 라이트(K), 렌더 경로와 시간, audit 요약, 남은 결함.
```

**인테리어 레이아웃**

```text
방 COL_Room: 4.0×3.2 m, 천장 2.4 m, 문은 남쪽 벽 중앙 0.9×2.1 m. (치수 기준: 한국 주거)
1) 가구 목록 표를 먼저 만들어: 이름 / 실측 footprint(W×D×H) / 벽과의 클리어런스 /
   기능 관계(예: 소파와 TV 2.0~2.5 m).
2) 좌표는 직접 찍지 말고 관계(against_wall, in_front_of, face_to, next_to)를 JSON으로 써.
   좌표는 placement_utils 함수로 계산해. 주 동선 폭은 0.8 m 이상.
3) 모든 오브젝트는 바닥에 스냅하고, 벽 쪽 가구는 벽 면에서 0.01~0.05 m 띄워.
4) scene_audit(floor_z=0, ceiling_z=2.4, collection="COL_Room")와 check_clearances 결과를 출력해
   (관통·박힘·천장 관통 0건이어야 함). 문·창을 만들었으면 building_audit로 문 막힘도 확인해.
5) 서사 클러스터 2개(예: '읽다 만 책과 식은 커피')에 소품 3~7개씩, 회전 ±7°, 스케일 ±5% 변주.
   모든 표면을 채우지 마. 동선과 카메라 경로는 비워 둬.
6) 검증 캡처: 탑다운 오쏘, 눈높이 1.6 m 문 쪽 시점, 로우앵글 0.6 m.
   떠 있음, 관통, 벽 뚫림을 점검해.
```

인테리어 연출 규칙의 근거는 arjun988 set-dressing입니다. 가장 흔한 실패는 모든 표면을 소품으로 채우는 'uniform clutter wallpaper'이고, 히어로 존은 'high intent, low noise', 배경은 실루엣만 살립니다. 간격 수치는 [실측 치수표](../03_playbooks/05_reference_dimensions.md), 배치 방법은 [배치 가이드](08_scene_layout_placement.md)를 보세요.

---

## 흔한 실수와 해결

| 증상 | 원인 | 해결 |
|---|---|---|
| 에이전트가 "완성했다"고 했는데 렌더를 보면 이상함 | 코드만 보고 결과를 상상함, 증거 없는 완료 보고 | 매 단계 렌더를 강제하고, 보고에 audit 수치와 렌더 경로를 요구(5.3절). `/goal`도 텍스트 증거로 |
| 재질을 넣었는데 스크린샷에 색이 안 보임 | 뷰포트가 Solid 모드 | Material Preview 전환(4.3절) |
| 소품이 스크린샷에 몇 픽셀로만 보임 | 프레이밍 없이 캡처 | 캡처 전 프레이밍, `review_views.py` 사용 |
| 가구가 떠 있거나 바닥에 반쯤 묻힘 | origin 기준으로 location 계산, 치수 추측 | world bbox 기준 `snap_to_floor()`, `scene_audit.py`로 확인 |
| `obj.dimensions`로 계산한 배치가 회전한 오브젝트에서 틀림 | dimensions는 로컬 축 기준이라 회전을 반영하지 않음 | `matrix_world @ bound_box`로 world AABB 사용 |
| 같은 코드를 다시 돌렸더니 오브젝트가 두 개 | get-or-create가 아님 | 이름으로 가져오고 없을 때만 생성(6.1절) |
| 모델이 방 안의 가구 일부를 모름 | `get_scene_info` 10개 제한 | 압축 씬 요약 스크립트(5.2절) |
| `KeyError: 'Principled BSDF'` | 한국어·일본어 UI에서 노드 이름 번역 | type으로 찾기, New Data 번역 끄기(7.3절) |
| `KeyError`/`AttributeError`가 반복됨 | 옛 API(EEVEE 식별자, `use_auto_smooth`, 비활성 소켓) | 조회 툴 먼저, 함정 표를 스킬 reference에(7절) |
| 5.0에서 `use_nodes` DeprecationWarning | 5.0에서 폐기 예고 | `bpy.app.version < (5,0,0)`일 때만 설정 |
| 실수로 씬이나 재질이 날아감 | `orphans_purge`, 공장 초기화, 덮어쓰기 | 금지 목록 + PreToolUse hook + 증분 저장 |
| `/rewind`했는데 Blender는 그대로 | 체크포인트는 Claude의 파일 편집만 추적 | `.blend` 증분 저장으로 되돌리기(6.5절) |
| 180초 뒤 실패하거나 Blender가 멈춤 | 긴 코드·렌더를 MCP로 실행, `exec()` 무제한 | 청크 분할, 미리보기 해상도, 최종은 headless(11절) |
| 스크린샷 루프가 길어지자 `invalid_request_error` | 이미지 20장 초과 시 치수 제한 강화 | 캡처 800~1000px, 각 변 2000px 이하 |
| 세션 비용이 예상보다 큼 | 스크린샷·툴 스키마가 매 턴 다시 전송됨, 모델·effort 선택 | 10.4절 절약 수칙, 오래된 이력은 PROGRESS.md로 넘기고 `/clear` |
| 비평이 사소한 취향 지적으로 끝나지 않음 | 종료 조건이 없음, 리뷰어 과잉 보고 | 큰 구조 문제만, `NEEDS_FIX: NO` 2회 연속 또는 최대 5회 |
| 만든 에이전트가 스스로 늘 합격을 줌 | 자기 채점 편향 | 읽기 전용 비평가 subagent(8.3절) |
| Codex에서 Astra 결과가 거칠고 비교에서 불리하게 나옴 | Codex 기본 effort low | effort 명시([AI 모델 가이드](01_ai_models_and_clients.md)) |
| 공식 커넥터와 커뮤니티 서버가 서로 간섭 | 둘 다 localhost:9876 | 한 Blender에는 서버 하나만 |
| 한국에서 Hunyuan3D 로컬로 만든 에셋 사용 | 라이선스 적용 지역에서 한국 제외 | 다른 생성 소스로 교체(12.1절) |
| 오래된 논문 코드가 안 돌아감 | 논문에 쓴 Claude 모델이 retire됨 | 모델 설정을 바꾸고, 워크플로를 특정 모델에 묶지 않기 |

---

## 관련 문서

- [목적·범위](../00_purpose/purpose_and_scope.md) · [조사 방법·신뢰도 정책](../01_research/research_method.md) · [출처 카탈로그](../01_research/sources_catalog.md) · [검증 로그](../01_research/verification_log.md)
- [AI 모델 비교·MCP 클라이언트·비용](01_ai_models_and_clients.md): 모델별 effort, Codex 설정, Astra 단가
- [Blender MCP 생태계](02_blender_mcp.md): 공식 서버 vs ahujasid, 설치, 버전 함정 전체 표, safe mode
- [기타 DCC·CAD·게임엔진 MCP](03_other_mcp_dcc_cad_engines.md): Unreal 5.8 공식 MCP, Fusion, SketchUp
- [AI 3D 생성](04_ai_3d_generation.md) · [텍스처링·재질](05_texturing_materials.md) · [라이팅·렌더·아트디렉션](06_lighting_rendering_art_direction.md)
- [오브젝트·가구·조형 모델링](07_modeling_objects_furniture_sculpture.md) · [배치·레이아웃](08_scene_layout_placement.md)
- [에셋·파이프라인·라이선스](10_assets_pipeline_licensing.md) · [학술 연구](11_research_papers.md)
- [빠른 시작](../03_playbooks/01_quickstart_setup.md) · [AAA 제작 플레이북](../03_playbooks/02_aaa_production_playbook.md) · [프롬프트 템플릿](../03_playbooks/03_prompt_templates.md) · [품질 체크리스트](../03_playbooks/04_quality_checklists.md) · [실측 치수표](../03_playbooks/05_reference_dimensions.md)
- [CLAUDE.md 템플릿](../03_playbooks/templates/CLAUDE.md) · [Blender 스킬 템플릿](../03_playbooks/templates/skills/blender-aaa-scene/SKILL.md)
- [보조 스크립트 사용법](../03_playbooks/scripts/README.md): `scene_audit.py`, `placement_utils.py`, `review_views.py`, `building_audit.py`
- [사례 모음](../04_case_studies/01_case_studies.md) · [한국어 자료](../04_case_studies/02_korean_resources.md)

## 원자료

- [`01_research/raw/10_agent-workflow.research.json`](../01_research/raw/10_agent-workflow.research.json): 에이전트 워크플로·프롬프팅 조사(항목 25, 노하우 32, 사례 8, 출처 46)
- [`01_research/raw/10_agent-workflow.verify.json`](../01_research/raw/10_agent-workflow.verify.json): 독립 검증(판정 23, 항목 점검 16, 신뢰도 낮은 출처 6, 누락 항목 10). 반영한 주요 정정: safe mode 범위(bpy 저장·렌더 허용, MCP 경로만 검사), 스크린샷 기본 1000px, `use_auto_smooth` 4.1 제거, `dimensions`는 회전 미반영, kiln Iron Rules 31개, ellmos 10분·문자 수, `save_mainfile(incremental=True)`, 이미지 20장 초과 제한, 텔레메트리 기본 수집, Tripo Premium 전용, blend-ai AGPL, Bniya 라이선스 없음
- [`01_research/raw/13_research-papers.research.json`](../01_research/raw/13_research-papers.research.json): 학술 연구 조사(항목 48, 노하우 18, 사례 7)
- [`01_research/raw/13_research-papers.verify.json`](../01_research/raw/13_research-papers.verify.json): 독립 검증(판정 15, 항목 점검 19). 반영한 주요 정정: BlenderGym VeriRatio 해석, LayoutVLM 충돌률 해석, LL3M 코드 비공개·서버 중단, Scene Language 기본 모델, `use_auto_smooth`·Musgrave 4.1 제거, Procedura 등 누락 연구
- 이 문서의 코드 스니펫 중 get-or-create 템플릿, 증분 저장 두 가지, 압축 씬 요약, 엔진 선택·`set_input()`·type 기반 노드 탐색·`use_translate_new_dataname` 속성 존재는 작성 중 pip `bpy` 5.0.1과 4.2.23 LTS(헤드리스)에서 실행해 확인했습니다. Material Preview 전환, hooks, subagent 정의, 물리 안정성 검사는 실행 검증을 하지 않은 작성 예시입니다.
