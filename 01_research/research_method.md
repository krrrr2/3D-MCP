# 조사 방법 · 한계 · 재현 방법

> 작성: 2026-09-27. 이 문서는 "이 자료를 얼마나 믿어도 되는가"를 판단하기 위한 기록입니다.

## 1. 조사 절차

| 단계 | 내용 | 규모 |
|---|---|---|
| 1차 조사 | 13개 주제를 병렬 조사 에이전트가 웹 검색 + 1차 출처(GitHub README·소스·이슈, 공식 문서, 논문 저장소)로 조사 | 에이전트 13개, 도구 호출 약 3,400회 |
| 1차 교차검증 | 주제마다 **독립된** 검증 에이전트가 핵심 주장(릴리스 날짜, 기능, 라이선스, 수치)을 다시 확인하고, 신뢰도 낮은 출처와 누락 항목을 지적 | 에이전트 13개 |
| 보완 조사 | 1차 조사의 공백(실측 치수, 한국어 자료, 영상·소셜 사례, 가격·라이선스, AAA 실무, 벤치마크)을 웹 검색으로 채움 | 에이전트 6개 |
| 보완 검증 | 수치가 그대로 쓰일 위험이 큰 두 주제(치수, 라이선스·가격)를 다시 독립 확인 | 에이전트 2개 |
| 정리 | 원자료를 주제별 가이드·플레이북·사례집으로 정리. 검증 결과를 우선 적용 | — |

1차 조사 결과 규모: 항목 381개, 노하우 286개, 사례 131개, 출처 535개(항목·사례 인용 포함 고유 URL 885개).

## 2. 주제 목록 (원자료 파일과 대응)

| 키 | 주제 | 원자료 |
|---|---|---|
| 01 | 프런티어 AI 모델 비교 (GPT-6 Astra, Claude Fable 5.1/Opus 5.5 등) | `raw/01_ai-models.*.json` |
| 02 | Blender MCP 생태계 | `raw/02_blender-mcp.*.json` |
| 03 | 기타 DCC·CAD·텍스처 앱 MCP | `raw/03_dcc-cad-mcp.*.json` |
| 04 | 게임 엔진·실시간 3D MCP | `raw/04_engine-mcp.*.json` |
| 05 | AI 3D 생성 (Text/Image-to-3D) | `raw/05_ai-3d-generation.*.json` |
| 06 | AI 텍스처링·PBR 재질 | `raw/06_texturing-materials.*.json` |
| 07 | AAA 라이팅·렌더·아트디렉션 | `raw/07_aaa-rendering-lighting.*.json` |
| 08 | 오브젝트·가구·조형 모델링 | `raw/08_modeling-objects.*.json` |
| 09 | 배치·레이아웃 | `raw/09_scene-layout.*.json` |
| 10 | 에이전트 워크플로·프롬프팅 | `raw/10_agent-workflow.*.json` |
| 11 | 사례 연구 | `raw/11_case-studies.*.json` |
| 12 | 에셋·파이프라인·라이선스 | `raw/12_assets-pipeline-licensing.*.json` |
| 13 | 학술 연구 | `raw/13_research-papers.*.json` |
| G1~G6 | 보완 조사 | `raw/G*.gap.json`, `raw/G*.verify.json` |
| G7 | 컴퓨터 유즈 vs MCP vs 스크립트 (메인 에이전트 직접 조사 + 독립 검증) | `raw/G7_computer_use.*.json` |
| G8 | 공식 Blender Lab MCP: 소스 정독 + **실제 구동 검증**(bpy 5.2.2 LTS에 공식 애드온·서버를 띄워 도구 호출) | `raw/G8_blender_lab_mcp.gap.json`, 응답 원본·재현 도구는 `handson/blender_lab_mcp/` |
| G9~G12 | 인체·캐릭터 / 유기물·자연 / 건물·건축·도시 / 3D 도구 보안. 하위 조사 에이전트 4개가 **읽기 전용**(다운로드·설치·실행 금지)으로 조사, 메인 에이전트가 GitHub·PyPI·LICENSE·로컬 bpy로 핵심 주장 대조 | `raw/G9_human_character.*`, `raw/G10_organic_nature.*`, `raw/G11_architecture.*`, `raw/G12_tool_safety.*` |

- `*.research.json` / `*.gap.json` = 조사 에이전트 원본 출력 (가공하지 않음)
- `*.verify.json` = 검증 에이전트 원본 출력
- `sources_catalog.md`, `verification_log.md` = 원자료에서 스크립트로 생성한 정리본
- `handson/` = 직접 실행해 확인한 기록. 검색·문서 조사가 아니라 실제 실행 결과이므로, 같은 내용이면 검색 요약보다 우선합니다

## 3. 신뢰도 정책

1. **검증 결과가 조사 결과보다 우선**합니다. 반박(❌)된 주장은 정정값으로, 부분(🟡)은 조건을 붙여, 미확인(❔)은 "미확인"으로 표시해 가이드에 반영했습니다.
2. 2026년 자료에는 AI가 대량으로 만든 SEO 블로그가 많습니다(예: 모델 출시 직후 쏟아진 "OO + Blender MCP 6단계 가이드"류). 검증 에이전트가 지적한 출처는 `sources_catalog.md`에 ⚠로 표시했고, 가이드에서는 사례 근거로 쓰지 않거나 "미검증 주장"으로 표시했습니다.
3. 벤더가 자체 보고한 벤치마크(예: OpenAI의 BenchCAD 95.9%)와 독립 평가는 구분해서 적었습니다. 측정 조건이 다르면 직접 비교하지 않았습니다.
4. 대부분의 모델 비교는 개인 테스트(n=1)입니다. 가이드에서는 "절대 순위"가 아니라 "작업 유형별 선택 기준"으로만 사용했습니다.

## 4. 조사 환경의 한계 (중요)

이 조사는 클라우드 샌드박스에서 수행했고, 다음 제약이 있었습니다.

- **네트워크 정책 차단**: arxiv.org, youtube.com, reddit.com, huggingface.co, blender.org(docs/projects/developer 포함), dev.epicgames.com, docs.unity3d.com, polyhaven.com, openai.com, 각 AI 3D 벤더 사이트(meshy.ai, tripo3d.ai, hyper3d.ai 등), naver·velog 등 대부분의 도메인은 페이지를 직접 열 수 없었습니다. github.com, raw.githubusercontent.com, anthropic.com, claude.com, platform.claude.com, code.claude.com은 열 수 있었습니다.
  - 그래서 많은 사실을 **GitHub의 1차 자료**(공식 저장소 README, 소스코드, LICENSE, 이슈, 공식 문서 미러)로 확인했습니다. 오히려 SEO 블로그보다 신뢰도가 높은 경우가 많았습니다.
  - 차단된 사이트의 내용(영상, 논문 본문 수치, 벤더 가격표 등)은 **웹 검색 결과 요약**으로만 확인한 경우가 있고, 해당 항목은 신뢰도를 medium/low로 낮췄습니다.
- **웹 검색 할당량**: 세션 공용 검색 한도(약 200회)가 1차 조사 초반에 소진되어, 뒤쪽 주제 조사자는 검색 없이 GitHub 직접 조회로 진행했습니다. 보완 조사 단계에서 검색 한도가 다시 열려 한국어 자료·영상 사례·치수 표준·라이선스를 채웠습니다.
- **학술 수치**: arXiv 차단으로 논문 본문 수치 일부는 저장소 README·프로젝트 페이지 소스·검색 요약에 의존했습니다.

> 더 깊게 검증하려면: Claude Code on the web 환경 설정(세션 제목 표시줄의 클라우드 환경 메뉴 → Edit)에서 **Network access** 수준을 넓히거나 필요한 도메인(예: arxiv.org, docs.blender.org, dev.epicgames.com, youtube.com)을 허용 목록에 추가한 뒤, `05_handoff/status_and_next_steps.md`의 "다음 작업"을 이어서 수행하면 됩니다. 접근 수준 설명: <https://code.claude.com/docs/en/claude-code-on-the-web>

## 5. 재현·갱신 방법

```bash
# 원자료에서 출처 카탈로그와 검증 로그 다시 만들기
python3 01_research/tools/build_catalog.py

# 보조 스크립트 테스트 (Blender 설치 없이 pip bpy 모듈로)
python3 -m venv bpyenv && bpyenv/bin/pip install bpy==5.0.1
bpyenv/bin/python 03_playbooks/scripts/tests/test_scripts.py
```

- 새로운 조사 결과를 추가할 때는 `raw/`에 새 JSON 파일로 넣고(기존 파일 수정 금지) `build_catalog.py`를 다시 실행하세요.
- 이 분야는 매주 바뀝니다(모델 출시, MCP 서버 버전, 라이선스). 각 가이드의 "기준일"을 확인하고, 중요한 결정 전에는 1차 출처를 다시 확인하세요.
