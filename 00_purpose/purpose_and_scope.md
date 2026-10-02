# 00. 목적 · 요구사항 · 범위

> 이 저장소의 모든 조사, 판단, 정리의 기준이 되는 문서입니다.
> 작성일: 2026-09-26

## 1. 사용자 요청 원문

> 혹시 아스트라든 페이블, 오푸스 5.5든 AI랑 MCP를 사용해서 모델링, 텍스쳐도 이쁘게 만들어서 AAA급 그래픽으로 만드는 노하우라든지 MCP 추천 자료 및 오브젝트나 가구, 조형, 배치 등이 제대로 만들어지기 위한 자료들을 최대한 많이 수집해서 어떻게 했는지 등의 자료를 체계적으로 조사 정리를 해볼래?

## 2. 실제 목적 (해석)

최신 AI 모델(OpenAI **GPT-6 Astra**, Anthropic **Claude Fable 5.1 / Opus 5.5** 등)을 **MCP(Model Context Protocol)** 로 3D 도구(Blender, 게임 엔진, CAD 등)에 연결해서 다음을 할 수 있게 하는 것:

1. 모델링 결과물이 **AAA급 품질**로 보이게 만들기 (조형, 텍스처, 재질, 조명, 렌더)
2. **오브젝트·가구·조형물**의 형태와 비율이 올바르게 나오게 만들기
3. **배치(레이아웃)** 가 자연스럽고 물리적으로 말이 되게 만들기

이 목적에는 "자료 목록"만이 아니라, **실제로 따라 할 수 있는 방법(노하우, 순서, 설정값, 프롬프트)** 까지 포함된다고 판단했습니다.

## 3. 핵심 요구사항

| # | 요구사항 | 이 저장소에서 다루는 곳 |
|---|---|---|
| R1 | AI + MCP로 모델링·텍스처를 예쁘게 만드는 노하우 | `02_guides/05_texturing_materials.md`, `02_guides/06_lighting_rendering_art_direction.md`, `02_guides/09_agent_workflow_prompting.md`, `03_playbooks/` 전체 |
| R2 | 추천 MCP 서버·도구 자료 | `02_guides/02_blender_mcp.md`, `02_guides/03_other_mcp_dcc_cad_engines.md`, `02_guides/04_ai_3d_generation.md` |
| R3 | 오브젝트·가구·조형이 제대로 만들어지기 위한 자료 | `02_guides/07_modeling_objects_furniture_sculpture.md`, `03_playbooks/05_reference_dimensions.md`, `03_playbooks/scripts/` |
| R4 | 배치(레이아웃)가 제대로 되기 위한 자료 | `02_guides/08_scene_layout_placement.md`, `03_playbooks/scripts/placement_utils.py`, 보조 도구 색인 `03_playbooks/06_placement_structure_helpers.md` |
| R5 | 다른 사람들이 **어떻게 했는지** (사례) | `04_case_studies/01_case_studies.md`, `04_case_studies/02_korean_resources.md` |
| R6 | **최대한 많이** 수집 | 13개 주제 병렬 조사 + 주제별 교차검증 + 6개 공백 보완 조사 (`01_research/`) |
| R7 | **체계적으로** 정리 | 번호 붙은 폴더 구조, 원자료/가공자료 분리, 검증 기록, 인수인계 문서 |
| (필요 요소) | 어떤 AI를 쓸지 | `02_guides/01_ai_models_and_clients.md` |
| (필요 요소) | 설치·연결 방법 | `03_playbooks/01_quickstart_setup.md` |
| (필요 요소) | 라이선스·상업적 이용 | `02_guides/10_assets_pipeline_licensing.md` |
| (추가 요청) | 건물·배치가 사람이 만든 것처럼 상식적인지(백룸 방지) | `03_playbooks/scripts/building_audit.py`, 실제 AI 건물 검증 `03_playbooks/scripts/validation/` |
| (추가 요청) | 컴퓨터 유즈 등 MCP 외 방법 총정리 | `02_guides/12_computer_use_and_other_methods.md` |
| (추가 요청) | 인체·유기물·건물 배치 전용 도구(평가 좋은 것·최신) | `02_guides/13_humans_organic_buildings.md`, 원자료 G9~G11 |
| (추가 요청) | 악성코드·DLL 등 설치 안전 | `02_guides/14_tool_install_safety.md`, 원자료 G12 |

## 4. 목적 달성에 필요한 기본 요소 (사용자가 명시하지 않았지만 필요한 것)

- **모델 선택 기준**: "어떤 AI를 어떤 작업에 쓰는가" (모델마다 코드 작성·공간 추론·이미지 비평 능력이 다름)
- **설치·연결 방법**: MCP 서버를 실제로 붙이는 절차
- **AI 3D 생성 도구**(이미지→3D 등): AAA급 결과물 대부분이 "AI가 직접 모델링"보다 "생성 도구 + 에셋 라이브러리 + AI 조립" 조합에서 나오기 때문
- **렌더링·조명 기본기**: 모델링이 좋아도 조명·색 관리가 틀리면 싸구려 CG처럼 보임
- **검증 루프**: 스크린샷/렌더 → 비평 → 수정의 반복 (AI 작업 품질을 좌우)
- **라이선스·상업적 이용 조건**: 특히 한국 사용자에게 적용되는 지역 제한 여부
- **실측 치수 기준표**: 가구·공간 치수가 틀리면 형태와 배치가 모두 어색해짐

## 5. 범위 밖 (의도적으로 제외)

- 특정 프로젝트용 실제 3D 에셋 제작 자체 (이번 작업은 조사·정리)
- 유료 도구의 실제 구매·계정 설정
- 캐릭터 리깅·애니메이션 심화 (언급은 하되 핵심 범위는 정적 오브젝트·환경·배치)

## 6. 조사 원칙

- 2026년 9월 기준 최신 정보를 우선하되, AI가 대량 생성한 SEO 블로그의 부정확한 내용은 1차 출처(공식 문서, GitHub, 논문, 제작자 원글)로 교차확인
- 확인되지 않은 내용은 "미확인"으로 표시하고 단정하지 않음
- 원자료(조사 에이전트 원본 결과)는 `01_research/raw/`에 가공 없이 보존하고, 정리된 가이드와 분리
