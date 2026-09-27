# AI + MCP로 AAA급 3D 만들기 — 조사·정리 저장소

> 기준일: 2026-09-27 · GPT-6 Astra, Claude Fable 5.1, Claude Opus 5.5 같은 AI를 MCP로 Blender·게임엔진·CAD에 연결해서 **예쁜 모델링·텍스처, 올바른 가구·오브젝트·조형, 자연스러운 배치**를 만드는 방법을 최대한 모아 정리했습니다.

- 조사 규모: 13개 주제 조사 + 주제별 독립 교차검증 + 7개 공백 보완 조사 → 항목 약 550개, 사례 약 180건, 실측 치수 136행, 고유 출처 URL 약 1,500개
- 문서의 모든 외부 링크는 원자료에 실제로 있는 URL인지 스크립트로 확인했습니다([`check_docs.py`](01_research/tools/check_docs.py)).
- 함께 들어 있는 [보조 스크립트](03_playbooks/scripts/README.md)(형태·배치 검사, 건축 상식 검사, 배치 함수, 검토 렌더)는 Blender 4.2.23 LTS와 5.0.1에서 테스트를 통과했습니다.

---

## 먼저 결론

1. **'아스트라' = OpenAI GPT-6 Astra**(2026-09-03), **'페이블' = Claude Fable 5.1**(2026-09-01), **Opus 5.5**(2026-09-22)입니다. 셋 중 절대 1위는 없습니다. 모델 비교는 대부분 개인 테스트(n=1)이고 결과가 엇갈립니다. 공간·치수·CAD·사진 재구성은 Astra, 긴 장면 빌드·룩뎁·정밀 배치는 Opus 5.5, 가장 어려운 계획은 Fable 5.1 식으로 **작업별로 고르세요.** effort는 꼭 직접 지정합니다(Codex의 Astra 기본값은 low). → [AI 모델 가이드](02_guides/01_ai_models_and_clients.md)
2. **독립적으로 'AAA급'이라고 검증된 AI+MCP 결과물은 아직 없습니다.** 공개 점수가 붙은 최고 사례도 재질·시각 충실도 6/10 수준입니다. 좋은 결과는 **[검증된 에셋·생성 모델] + [AI의 조립·배치·세팅] + [숫자·렌더 검증 루프] + [사람의 마무리]** 조합에서 나왔습니다. → [사례 모음](04_case_studies/01_case_studies.md)
3. **Blender MCP는 두 종류입니다.** Claude 공식 커넥터는 Blender Lab(Blender 개발진)이 만든 서버(Blender 5.1+, GPL)이고, 커뮤니티 표준은 ahujasid의 MCP for Blender(약 29.4k stars, 36개 tool, 에셋·AI 생성 연동)입니다. 둘 다 포트 9876을 써서 **동시에 켜면 안 됩니다.** → [Blender MCP 가이드](02_guides/02_blender_mcp.md)
4. **LLM이 좌표를 직접 찍으면 배치가 망가집니다.** 한 비교에서 충돌률이 LLM 직접 좌표(LayoutGPT) 40.8%, 제약+솔버(Holodeck) 12.7%, 렌더→평가→수정 루프(SceneReVis) 4.5%였습니다. LLM은 "벽에 붙여, 소파를 바라보게" 같은 **관계 제약**만 쓰고, 좌표는 솔버·스크립트가 풀고, 충돌·부유 검사 후 위에서 본 렌더로 비평하는 구조가 정답으로 수렴했습니다. → [배치 가이드](02_guides/08_scene_layout_placement.md)
5. **가구·오브젝트는 '스펙 먼저'**: 부품별 치수 JSON → 부품 단위 코드 → 숫자 검사 → 렌더 검사 순서입니다. 치수는 추측하지 말고 [실측 치수표](03_playbooks/05_reference_dimensions.md)의 mm 값을 넘기세요(한국 천장고 2300/2400~2500, 싱크대 850, 매트리스 Q 1500×2000 등). → [모델링 가이드](02_guides/07_modeling_objects_furniture_sculpture.md)
6. **유기체·조형·캐릭터는 AI가 코드로 직접 빚기 어렵습니다.** Rodin·Tripo·Meshy·TRELLIS.2 같은 **이미지→3D 생성기**로 형태를 만들고, 에이전트는 정리·리토폴·UV·배치를 맡깁니다. 입력 이미지 품질(단일 물체, 단색 배경, 3/4 뷰)이 결과의 절반입니다. → [AI 3D 생성 가이드](02_guides/04_ai_3d_generation.md)
7. **'싸구려 CG'의 원인은 대부분 숫자로 고칠 수 있습니다**: 색관리(AgX), 실측 스케일, 광원 크기 0 금지, 모든 모서리에 베벨, roughness 변화, 순흑·순백 금지, 카메라 높이·초점거리. 이 규칙을 에이전트 규칙 파일에 숫자로 넣으세요. → [라이팅·렌더 가이드](02_guides/06_lighting_rendering_art_direction.md), [텍스처 가이드](02_guides/05_texturing_materials.md)
8. **품질은 모델보다 '하네스'에서 올라갑니다**: 작은 코드 조각 실행 → 스크린샷/4방향 렌더 → 숫자 게이트 → 한 번에 한 가지 수정, `.blend` 버전 저장, 비평 전용 에이전트 분리. → [에이전트 워크플로 가이드](02_guides/09_agent_workflow_prompting.md), [규칙 템플릿](03_playbooks/templates/CLAUDE.md)
9. **[한국 사용자 필수] Tencent Hunyuan3D 계열 오픈웨이트**(2.0/2.1/Omni/Part, HY-World, HY-Motion)는 라이선스 적용 지역에서 **대한민국을 제외**하고 출력물 사용도 제한합니다. 한국어 UI에서는 노드 이름이 번역돼 코드가 깨질 수 있으니 영어 UI를 쓰거나 노드를 type으로 찾게 하세요. → [라이선스 가이드](02_guides/10_assets_pipeline_licensing.md)
10. **"컴퓨터 유즈로 직접 모델링하는 게 낫다"는 대체로 오해입니다.** Astra 공식 사례도 bpy 스크립트로 만들고 컴퓨터 유즈는 화면 확인에 썼고, 화면 클릭 CAD 벤치마크 최고 성공률은 17.5%입니다. 만드는 건 스크립트·MCP, 확인과 API 없는 조작은 컴퓨터 유즈로 나누세요. → [컴퓨터 유즈 vs MCP vs 스크립트](02_guides/12_computer_use_and_other_methods.md)
11. **"사람이 만든 건물 같은가"도 자동 검사합니다.** 문이 벽에 안 뚫림·열면 벽·허공으로 나감·가구가 막음, 창턱 높이 제각각·실내 창, 문 없는 방·창 없는 거실·복도처럼 길쭉한 빈 방의 반복 같은 **백룸식 기묘함**을 [`building_audit.py`](03_playbooks/scripts/README.md)가 잡고 위험도를 매깁니다. **실제 AI가 만든 건물 9개**(GPT-6 Astra 재구성 공간, 같은 아파트를 Fable·GPT-6가 각각 만든 8개)로 검증해 오탐을 고쳤습니다 → [검증 기록](03_playbooks/scripts/validation/README.md)
12. **보안**: `execute_blender_code`는 임의 Python 실행 권한입니다. 작업 전 저장, `DISABLE_TELEMETRY=true`, 신뢰하는 서버만 쓰세요(safe mode는 샌드박스가 아님). → [빠른 시작](03_playbooks/01_quickstart_setup.md)

---

## 목적별로 읽는 순서

| 하고 싶은 것 | 읽을 문서 |
|---|---|
| **오늘 바로 연결해서 써 보기** | [01 빠른 시작](03_playbooks/01_quickstart_setup.md) → [03 프롬프트 템플릿](03_playbooks/03_prompt_templates.md) |
| **어떤 AI·MCP를 쓸지 정하기** | [AI 모델](02_guides/01_ai_models_and_clients.md) → [Blender MCP](02_guides/02_blender_mcp.md) → [기타 MCP·엔진](02_guides/03_other_mcp_dcc_cad_engines.md) |
| **AAA급 장면 하나를 처음부터 끝까지** | [02 제작 플레이북](03_playbooks/02_aaa_production_playbook.md) + [04 품질 체크리스트](03_playbooks/04_quality_checklists.md) |
| **가구·오브젝트·조형이 제대로 나오게** | [모델링 가이드](02_guides/07_modeling_objects_furniture_sculpture.md) + [실측 치수표](03_playbooks/05_reference_dimensions.md) + [scene_audit.py](03_playbooks/scripts/README.md) |
| **배치가 자연스럽게** | [배치 가이드](02_guides/08_scene_layout_placement.md) + [placement_utils.py](03_playbooks/scripts/README.md) |
| **건물·방이 기묘하지 않게(백룸 방지)** | [building_audit.py](03_playbooks/scripts/README.md) (문·창·방·동선·계단 상식 검사) |
| **컴퓨터 유즈 vs MCP vs 스크립트 비교** | [컴퓨터 유즈와 다른 방법들](02_guides/12_computer_use_and_other_methods.md) |
| **텍스처·재질을 예쁘게** | [텍스처·재질 가이드](02_guides/05_texturing_materials.md) |
| **조명·렌더·구도** | [라이팅·렌더·아트디렉션](02_guides/06_lighting_rendering_art_direction.md) |
| **AI로 3D 에셋 생성** | [AI 3D 생성 가이드](02_guides/04_ai_3d_generation.md) |
| **다른 사람들은 어떻게 했나** | [사례 모음](04_case_studies/01_case_studies.md) · [한국어 자료](04_case_studies/02_korean_resources.md) |
| **상업적으로 써도 되나** | [에셋·파이프라인·라이선스](02_guides/10_assets_pipeline_licensing.md) |
| **연구 근거가 궁금하다** | [학술 연구 정리](02_guides/11_research_papers.md) |
| **AI 에이전트에게 규칙을 주고 싶다** | [templates/CLAUDE.md](03_playbooks/templates/CLAUDE.md)(Codex는 AGENTS.md로) · [Claude Code 스킬](03_playbooks/templates/skills/blender-aaa-scene/SKILL.md) |

## 폴더 구조

```
00_purpose/            목적·요구사항·범위 (모든 판단의 기준)
01_research/           조사 원자료와 검증 기록
  raw/                   조사·검증 에이전트 원본 출력 (JSON, 수정 금지)
  sources_catalog.md     전체 출처 목록 (자동 생성, 신뢰도 경고 표시)
  verification_log.md    교차검증 결과: 확인/부분/반박/미확인 (자동 생성)
  research_method.md     조사 방법·한계·신뢰도 정책
  tools/                 카탈로그 생성·문서 링크 검사 스크립트
02_guides/             주제별 가이드 12편 (분석·정리)
03_playbooks/          실전 적용: 빠른 시작, 제작 플레이북, 프롬프트, 체크리스트, 치수표
  templates/             에이전트 규칙(CLAUDE.md/AGENTS.md), Claude Code 스킬
  scripts/               Blender 검사·배치 스크립트 4종 + 테스트 (4.2 LTS·5.0 통과)
04_case_studies/       사례 모음, 한국어 자료
05_handoff/            진행 상태·결정 기록·다음 작업
```

## 믿고 쓰기 전에 알아 둘 것

- **매주 바뀌는 분야입니다.** 모델·MCP 서버 버전·가격·라이선스는 문서마다 날짜를 적었습니다. 중요한 결정 전에는 링크된 1차 출처를 다시 확인하세요.
- 조사 환경에서 arxiv·YouTube·Reddit·공식 벤더 사이트 등 여러 도메인을 직접 열 수 없었습니다. 그래서 GitHub 1차 자료(공식 저장소 README·소스·LICENSE)로 확인한 것이 많고, 검색 요약으로만 확인한 내용은 **(미확인)**, **(신뢰도 낮음)**, **(벤더 자체 보고)**, **(개인 테스트, n=1)** 로 표시했습니다. 자세한 내용은 [조사 방법](01_research/research_method.md)과 [검증 로그](01_research/verification_log.md)를 보세요.
- 인수인계·다음 작업: [05_handoff/status_and_next_steps.md](05_handoff/status_and_next_steps.md)

## 유지보수 명령

```bash
python3 01_research/tools/build_catalog.py     # 원자료 → 출처 카탈로그·검증 로그 재생성
python3 01_research/tools/check_docs.py        # 문서의 URL이 원자료에 있는지, 내부 링크가 살아 있는지 검사
python3 -m venv bpyenv && bpyenv/bin/pip install bpy==5.0.1 && bpyenv/bin/python 03_playbooks/scripts/tests/test_scripts.py
```
