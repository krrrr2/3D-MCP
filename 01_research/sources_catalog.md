# 출처 카탈로그 (자동 생성)

> `01_research/raw/` 원본 조사 데이터에서 `tools/build_catalog.py` 로 생성한 파일입니다. 직접 수정하지 마세요.
> ⚠ 표시는 교차검증 에이전트가 신뢰도 문제(SEO성 AI 생성 글, 1차 출처와 모순 등)를 지적한 출처입니다.

## 목차

- [AI 모델 비교 (GPT-6 Astra / Claude / Gemini ...)](#01_ai-models) — 출처 38개
- [Blender MCP 생태계](#02_blender-mcp) — 출처 32개
- [기타 DCC·CAD·텍스처 앱 MCP](#03_dcc-cad-mcp) — 출처 35개
- [게임 엔진·실시간 3D MCP](#04_engine-mcp) — 출처 36개
- [AI 3D 생성 (Text/Image-to-3D)](#05_ai-3d-generation) — 출처 32개
- [AI 텍스처링·PBR 재질](#06_texturing-materials) — 출처 83개
- [AAA 라이팅·렌더·아트디렉션](#07_aaa-rendering-lighting) — 출처 31개
- [오브젝트·가구·조형 모델링](#08_modeling-objects) — 출처 63개
- [배치·레이아웃](#09_scene-layout) — 출처 50개
- [에이전트 워크플로·프롬프팅](#10_agent-workflow) — 출처 46개
- [사례 연구](#11_case-studies) — 출처 34개
- [에셋·파이프라인·라이선스](#12_assets-pipeline-licensing) — 출처 37개
- [학술 연구](#13_research-papers) — 출처 18개
- [[보완] 실측 치수 표준](#g1_dimensions) — 출처 57개
- [[보완] 한국어 자료](#g2_korean_resources) — 출처 31개
- [[보완] 영상·소셜 사례](#g3_videos_cases) — 출처 78개
- [[보완] 가격·라이선스·법규](#g4_licensing_pricing) — 출처 34개
- [[보완] AAA 실무·공식 변경사항](#g5_aaa_practice) — 출처 39개
- [[보완] 벤치마크·모델 비교](#g6_benchmarks_models) — 출처 40개

항목·사례에 인용된 URL까지 합친 고유 URL 수: **1469개**

<a id="01_ai-models"></a>
## AI 모델 비교 (GPT-6 Astra / Claude / Gemini ...)

주제 원문: MCP로 3D 툴을 구동하기 위한 프런티어 AI 모델 비교 (2026년 9월 기준): GPT-6 Astra, Claude Fable 5.1/Opus 5.5/Sonnet 5/Haiku 4.5, Gemini 3.x, Grok, 오픈웨이트 모델, MCP 클라이언트, 3D 벤치마크

| # | 제목 | 유형 | 날짜 | 왜 유용한가 | URL |
|---|---|---|---|---|---|
| 1 | Claude for Creative Work (Anthropic, 9종 커넥터 발표) | 공식 발표 | 2026-04-28 | Blender, SketchUp, Fusion을 포함한 9종 커넥터 목록과 3D 활용 문구를 담은 1차 자료 | <https://www.anthropic.com/news/claude-for-creative-work> |
| 2 | Claude Opus 5.5 모델 개요 (Claude Platform Docs) | 공식 문서 | 2026-09-22 | Fable 5.1, Opus 5.5, Sonnet 5, Haiku 4.5의 컨텍스트, 가격, effort 기본값 비교표 | <https://platform.claude.com/docs/en/models/opus-5-5/overview> |
| 3 | What's new in Claude Opus 5.5 | 공식 문서 | 2026-09-22 | 스크린샷·다이어그램 판독 개선, 컴퓨터 사용 도구 버전, forced tool use 불가 등 연동 주의점 | <https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5> |
| 4 | Prompting Claude Opus 5.5 | 공식 문서 | 2026-09 | effort 보정, 무인 실행 프롬프트, 복잡한 시각 입력용 crop 도구, 디자인 기본값 회피법 | <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5> |
| 5 | Introducing Claude Opus 5.5 | 공식 발표 | 2026-09-22 | Terminal-Bench 4.0, OSWorld 2.0, FrontierCode(Astra 53.3% 대비 54.4%) 수치 | <https://www.anthropic.com/claude-opus-5-5> |
| 6 | Claude Fable 5.1 개요 / 발표 | 공식 문서 | 2026-09-01 | 가격, 컨텍스트, 출시일, Mythos 5.1 관계 | <https://platform.claude.com/docs/en/models/fable-5-1/overview> |
| 7 | Introducing Claude Fable 5.1 and Claude Mythos 5.1 | 공식 발표 | 2026-09-01 | 캐시 가격 인하와 벤치마크 | <https://www.anthropic.com/claude-fable-and-mythos-5-1> |
| 8 | Claude Vision 문서 | 공식 문서 | 2026-09 | 고해상도 티어 2576px/4784토큰, 이미지 토큰 공식, 20장 초과 시 2000px 제한 | <https://platform.claude.com/docs/en/build-with-claude/vision> |
| 9 | Optimizing for cost and intelligence | 공식 문서 | 2026-09 | 어드바이저와 오케스트레이터 패턴 실측, effort별 비용 대비 성능 | <https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence> |
| 10 | Choosing the right model | 공식 문서 | 2026-09 | Anthropic이 공식으로 권하는 모델 선택 매트릭스 | <https://platform.claude.com/docs/en/about-claude/models/choosing-a-model> |
| 11 | Claude Code MCP 문서 | 공식 문서 | 2026-09 | claude mcp add 문법, MAX_MCP_OUTPUT_TOKENS, 타임아웃, 이미지 결과 처리 | <https://code.claude.com/docs/en/mcp> |
| 12 | Claude Code computer use | 공식 문서 | 2026-09 | GUI 전용 앱 제어 조건(macOS, Pro/Max)과 스크린샷 자동 축소 규칙 | <https://code.claude.com/docs/en/computer-use> |
| 13 | Claude Fable models on your plan | 공식 헬프센터 | 2026-09 | 플랜별 Fable 과금 방식(Pro 크레딧, Max 50%) | <https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan> |
| 14 | Claude 커넥터 페이지: Blender / SketchUp / Autodesk Fusion | 공식 디렉터리 | 2026-04~05 | 제작 주체(Blender Lab, Trimble, Autodesk), 도구 목록, 요구 사항 | <https://claude.com/connectors/blender> |
| 15 | GPT-6 Astra: A new generation of intelligence (OpenAI) | 공식 발표 (직접 열람 불가, 검색 요약으로 확인) | 2026-09-03 | Astra 1차 발표문. Blender, KiCad, UE 데모와 BenchCAD 수치의 출처 | <https://openai.com/index/gpt-6-astra/> |
| 16 | GPT-6 Astra vs Claude Fable 5.1: Benchmarks and Pricing (DataCamp) | 2차 분석 기사 | 2026-09 | BenchCAD, Terminal-Bench, OSWorld 비교와 비교 조건 차이 설명 | <https://www.datacamp.com/blog/gpt-6-astra-vs-claude-fable-5-1> |
| 17 | BenchCAD LEADERBOARD.md | 벤치마크 (GitHub) | 2026-06 | 재채점된 독립 수치. 벤더 보고와 조건 차이 확인용 | <https://github.com/BenchCAD/BenchCAD-main/blob/main/LEADERBOARD.md> |
| 18 | 3DCodeBench (GitHub, arXiv 2606.01057) | 벤치마크 / 논문 | 2026-06-01 | Blender 5.0 bpy 절차적 모델링 평가. 에러 피드백 효과와 하네스 비교 | <https://github.com/gaoypeng/3dcodebench> |
| 19 | 3DHarnessBench (GitHub, arXiv 2609.06535) | 벤치마크 / 논문 | 2026-09 | Astra, Kimi K3, Opus 5, Fable 5, Qwen3.8, Gemini 3.1 Pro의 에이전트형 3D→코드 평가 설계 | <https://github.com/llada60/3DHarnessBench> |
| 20 | BlenderGym (arXiv 2504.01786) | 논문 | 2025-04 | 배치, 조명, 머티리얼 등 5개 편집 과제와 검증 연산 배분 인사이트 | <https://arxiv.org/abs/2504.01786> |
| 21 | awesome-gpt-6-astra (데모 큐레이션) ⚠ | GitHub 큐레이션 | 2026-09 | Blender·3D 사례 24건의 원문 X 링크와 제작자 | <https://github.com/magiccreator-ai/awesome-gpt-6-astra> |
| 22 | awesome-claude-opus-5-5-demos | GitHub 큐레이션 | 2026-09 | Opus 5.5의 Blender와 게임 사례 | <https://github.com/magiccreator-ai/awesome-claude-opus-5-5-demos> |
| 23 | Codex-and-Blender (Astra + Blender 재현 가능한 워크플로) | GitHub 템플릿 | 2026-09 | YAML→bpy→CLI 정본 구조, 시각 평가기, 합격 기준 게이트 | <https://github.com/danielsobrado/Codex-and-Blender> |
| 24 | claude-3d-harness | GitHub 템플릿 | 2026 | Claude Code 스킬 58개 기반 렌더-검증 파이프라인 | <https://github.com/MAX-786/claude-3d-harness> |
| 25 | Gemini CLI → Antigravity CLI 전환 공지 | 공식 공지 (GitHub) | 2026-05-19 | 2026-06-18 소비자 티어 서비스 종료 사실 | <https://github.com/google-gemini/gemini-cli/discussions/27274> |
| 26 | Google releases three new Gemini models — but no 3.5 Pro (TechCrunch) | 뉴스 | 2026-07-21 | Gemini 3.5 Pro 지연과 3.6 Flash 출시 | <https://techcrunch.com/2026/07/21/google-releases-three-new-gemini-models-but-no-3-5-pro/> |
| 27 | Introducing Gemini 3.8 Flash and 3.8 Flash Cyber | 공식 발표 (검색 요약으로 확인) | 2026-09-02 | 최신 Gemini 워크호스 모델 정보 | <https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/> |
| 28 | Kimi K3 (GitHub) | 공식 저장소 | 2026-07 | 사양, 비전 지원, 라이선스, 벤더 벤치마크 | <https://github.com/MoonshotAI/Kimi-K3> |
| 29 | Stefan 3D AI: Opus 5.5 vs GPT-6 Astra 첫 3D 테스트 | X 게시물 (실측) | 2026-09 | 같은 프롬프트에서 시간, 토큰, 비용을 직접 비교한 수치 | <https://x.com/Stefan_3D_AI/status/2102471841046786153> |
| 30 | Hierarchy Agency: GPT-6 Astra vs Claude Fable 5.1 Blender 테스트 | 에이전시 블로그 (검색 요약으로 확인) | 2026-09 | 실사용 1주일 결론(공간은 Astra, 소프트웨어는 Fable) | <https://hierarchy.ch/en/news/gpt-6-astra-vs-claude-fable-5-1> |
| 31 | I Tested GPT Astra for 3D Modeling (SketchUp 농가 테스트) | YouTube (요약은 daily.dev로 확인) | 2026-09 | 건축 모델링의 치수 오차와 토큰 소모 한계 | <https://www.youtube.com/watch?v=SsBLhNgqTqQ> |
| 32 | GPT-6 Astra vs Meshy 7 (HackerNoon) | 2차 기사 | 2026-09 | 캐릭터·유기체 한계와 생성형 3D 분업 워크플로 | <https://hackernoon.com/gpt-6-astra-vs-meshy-7-for-3d-creation-what-three-creator-workflows-reveal> |
| 33 | Claude's Blender MCP Burned 60% of a $200/Month Plan on One Donut (MindStudio) ⚠ | 블로그 실측 | 2026 | 구독 한도 소진 실측과 실패 유형 | <https://www.mindstudio.ai/blog/claude-blender-mcp-60-percent-tokens-donut-test-results> |
| 34 | Blender AI Arena 리더보드 ⚠ | 커뮤니티 아레나 | 2026-09 | 블라인드 투표 결과(시즌 3 5자 동률) | <https://blenderai.org/leaderboard> |
| 35 | Opus 5.5 vs GPT-6 Astra 12 use cases (Geeky Gadgets 요약) ⚠ | 2차 기사 | 2026-09 | Nate Herk의 8-4 결과와 시간·비용 차이 | <https://www.geeky-gadgets.com/opus-5-5-vs-gpt-6-astra/> |
| 36 | GPT-6 아스트라 vs 클로드 페이블 5.1, 성능표만 보면 놓치는 차이 (AI매터스) | 국내 기사 | 2026-09 | 한국어 자료. 컴퓨터 사용 성공률의 의미와 사진 재구성 환각 지적 | <https://aimatters.co.kr/news-report/51830/> |
| 37 | Developer mode and MCP apps in ChatGPT (OpenAI Help) | 공식 헬프센터 (검색 요약으로 확인) | 2026 | ChatGPT 웹은 원격 MCP만 지원한다는 점과 지원 플랜 | <https://help.openai.com/en/articles/12584461-developer-mode-apps-and-full-mcp-connectors-in-chatgpt-beta> |
| 38 | Blender Lab MCP 서버 저장소 | 공식 저장소 (검색 요약으로 확인) | 2026 | Blender 5.1 이상 요구 사항과 공식 서버 구조 | <https://projects.blender.org/lab/blender_mcp> |

**⚠ 신뢰도 경고가 붙은 출처**

- <https://llm-stats.com/benchmarks/benchcad> — 'Opus 5.5 0.730 선두'는 BenchCAD 공식 리더보드 척도(IoU-score 최고 0.384, 벤더 보고 포함)와 크게 어긋납니다. 공식 표에 Opus 5.5는 없습니다. 집계 사이트 수치는 1차 근거로 쓰지 말아야 합니다.
- <https://blenderai.org/leaderboard> — Blender 재단(blender.org)과 무관한 커뮤니티 사이트로 보이며 운영 주체가 확인되지 않습니다. 참가자에 상용 제품(3D-Agent)이 있어 이해상충 가능성이 있고, 이번에 접속이 불가해 수치를 검증하지 못했습니다.
- <https://blendermcp.org/setup/ollama> — 프로젝트명과 비슷한 비공식 도메인입니다. ahujasid 프로젝트의 공식 사이트는 README상 mcp-for-blender.com이고, 공식 Blender Lab 서버와도 무관합니다. 설치 안내가 공식판과 커뮤니티판을 혼동시킬 위험이 있습니다.
- <https://mcp.film/mcps/blender-lab-mcp/> — MCP 디렉터리형 집계 사이트로 1차 자료가 아닙니다. Blender Lab 기능 설명은 projects.blender.org나 blender.org/lab으로 교차 확인해야 합니다.
- <https://codersera.com/blog/gpt-astra-vs-google-project-astra-2026/> — 대량 생산형 SEO 블로그 성격의 도메인입니다. 명칭 구분(GPT-6 Astra vs Project Astra)은 상식 수준이라 이 출처 없이도 서술할 수 있습니다.
- <https://www.winzheng.com/en/article/gpt-6-astra-plus-business-rollout-pricing-analysis> — 출처가 불명확한 재가공 기사 사이트입니다. 가격과 요금제(272k 초과 재과금, Plus 제한) 같은 핵심 수치를 이 사이트에 의존하면 안 되며 OpenAI 공식 가격표로 확인해야 합니다. 이번에 접속 불가였습니다.
- <https://runtimewire.com/article/gpt-6-astra-blender-scene-control-stefan-vaskevich> — X 게시물을 재가공한 2차 사이트로 보입니다. 원 게시물이나 OpenAI 발표로 대체해야 합니다.
- <https://se7en.ws/ai-claude-opus-5-5-surpasses-gpt-6-astra-in-unreal-engine-game-development/?lang=en> — 다국어 재게시·번역형 집계 사이트입니다. 조사자도 인정했듯 원본 영상(Brendan Jowett)을 확인하지 않은 3차 인용입니다. 'a million times better' 같은 과장 인용을 결론 근거로 쓰기에 부적합합니다.
- <https://ixbt.games/en/news/2026/09/25/438160-ii-claude-opus-55-obosel-gpt-6-astra-v-sozdanii-igr-na-unreal-engine.html> — se7en.ws와 같은 YouTube 영상을 재요약한 2차 보도로, 독립 출처로 셀 수 없습니다.
- <https://www.geeky-gadgets.com/opus-5-5-vs-gpt-6-astra/> — YouTube 영상 요약형 저품질 기사로 자주 지적되는 사이트입니다. Nate Herk 8 대 4 결과는 원 게시물로 확인해야 합니다.
- <https://www.mindstudio.ai/blog/claude-blender-mcp-60-percent-tokens-donut-test-results> — 자사 제품 홍보 목적의 벤더 블로그입니다. 모델 버전이 명시되지 않았고, 마젠타 화면을 컨텍스트 초과로 설명한 것은 Blender의 일반 동작(텍스처 누락 표시)과 어긋납니다. Fable 5.1 워크스루 글도 같은 벤더의 콘텐츠 마케팅입니다.
- <https://evolink.ai/blog/grok-4-7-release-date> — API 재판매 업체의 마케팅 블로그입니다. Grok 4.7 출시일과 가격은 docs.x.ai로 확인해야 합니다.
- <https://www.digitalapplied.com/blog/deepseek-v4-flash-vision-exp-launch-pricing> — 에이전시 SEO 블로그입니다. DeepSeek 모델 사양과 가격은 DeepSeek 공식 API 문서나 GitHub로 대체해야 합니다.
- <https://www.morphllm.com/best-open-source-coding-model-2026> — 자사 제품(코드 적용 모델) 판매사의 순위 글이라 이해상충이 있습니다. 오픈웨이트 순위 근거로 쓰기에 약합니다.
- <https://www.gradually.ai/en/llm-comparison/gpt-6-astra-vs-gpt-6-sol/> — 자동 생성형 비교 페이지로 보입니다. 'magnitude step up' 같은 정성 평가의 원출처가 불명확합니다.
- <https://github.com/magiccreator-ai/awesome-gpt-6-astra> — magiccreator.ai로 유입시키는 마케팅용 큐레이션입니다. 다만 항목마다 '제작자 보고, 미검증' 공개 문구가 있어 사례 색인으로는 쓸 만합니다. 수치는 원 게시물로 확인해야 합니다(awesome-claude-opus-5-5-demos도 동일).

<a id="02_blender-mcp"></a>
## Blender MCP 생태계

주제 원문: Blender MCP 생태계 심층 조사 (2026-09 기준): ahujasid MCP for Blender, Blender Lab 공식 MCP/Claude 커넥터, 대안 서버·포크·스킬, In-Blender AI 애드온, 헤드리스 방식, Blender+AI 실무 규칙과 함정

| # | 제목 | 유형 | 날짜 | 왜 유용한가 | URL |
|---|---|---|---|---|---|
| 1 | ahujasid/mcp-for-blender (구 blender-mcp) GitHub README | GitHub README (primary) | 2026-09-25 업데이트 | 설치(Claude Desktop/Code/Cursor/Codex/OpenCode/Antigravity/Docker), 환경변수, safe mode, 텔레메트리, 문제 해결 표, 예시 프롬프트 | <https://github.com/ahujasid/blender-mcp> |
| 2 | mcp-for-blender server.py (raw) | 소스 코드 (primary) | 2026-09 | 36개 tool 목록과 파라미터, 180초 소켓 타임아웃, FastMCP instructions(노드 type 조회, enum 하드코딩 금지), Premium 감지 방식 | <https://raw.githubusercontent.com/ahujasid/blender-mcp/main/src/blender_mcp/server.py> |
| 3 | mcp-for-blender addon.py (raw) | 소스 코드 (primary) | 2026-09 | get_scene_info의 10개 제한, GPUOffScreen 스크린샷, timer 큐, exec namespace, undo 처리 없음 확인 | <https://raw.githubusercontent.com/ahujasid/blender-mcp/main/addon.py> |
| 4 | PyPI mcp-for-blender | 패키지 레지스트리 | 2.1.0, 2026-09-25 | 최신 버전과 릴리스 이력, 이름 변경 공지 | <https://pypi.org/project/mcp-for-blender/> |
| 5 | PyPI blender-mcp (release history) | 패키지 레지스트리 | 0.1.0(2025-03-08) ~… | 전체 버전 연혁과 2.0.0 호환 래퍼 확인 | <https://pypi.org/project/blender-mcp/> |
| 6 | mcp-for-blender commits | GitHub 커밋 로그 | 2026-09-15~25 | opt-in 텔레메트리 전환(09-21), safe mode 추가, export_scene, Poly Pizza, premium 통합 | <https://github.com/ahujasid/blender-mcp/commits/main> |
| 7 | Anthropic — Claude for Creative Work | 공식 발표 | 2026-04-28 (2026-05… | Blender 개발자가 만든 공식 커넥터라는 점, 9개 커넥터 목록, Blender가 Development Fund 대신 일회성 기부를 택한 사실 | <https://www.anthropic.com/news/claude-for-creative-work> |
| 8 | Claude connectors — Blender | 공식 커넥터 디렉터리 | 2026-04 등록 | Provider가 'Blender Lab (Anthropic verified)'이고 애드온이 필요하다는 점 | <https://claude.com/connectors/blender> |
| 9 | Blender Lab MCP Server 페이지 | 공식 문서 (검색 요약으로 확인, 직접 열람 실패) | 2026 | Blender 5.1+ 요구, 2회 드래그 설치, 샘플 프롬프트, 로컬 LLM 안내 | <https://www.blender.org/lab/mcp-server/> |
| 10 | lab/blender_mcp 저장소 및 v1.0.0 릴리스 | 공식 저장소 (검색 요약으로 확인) | 2026-04-27 | 초기 릴리스 날짜(Dalai Felinto), MCPB 번들 | <https://projects.blender.org/lab/blender_mcp/releases/tag/v1.0.0> |
| 11 | bpype/blender_mcp (Blender Lab MCP GitHub 미러) | 미러 저장소 | 2026 | 공식 서버의 tool 목록, 아키텍처, 애드온 설정(host/port/polling/auto-start) | <https://github.com/bpype/blender_mcp> |
| 12 | bpy-dev/blender-mcp readme_tools.rst ⚠ | 파생 배포판 문서 | 2026 | search_api_docs/search_manual_docs/get_runtime_python_api_docs 등 공식 계열 tool 설명 | <https://github.com/bpy-dev/blender-mcp/blob/main/readme_tools.rst> |
| 13 | stefancrm/claude-blender-mcp-connector-setup-kit | 커뮤니티 설치 키트 | 2026 | 공식 서버를 Claude Code에 붙이는 구체적 ~/.claude.json 설정, null-byte 구분 JSON, 포트 9876, 26 tools | <https://github.com/stefancrm/claude-blender-mcp-connector-setup-kit> |
| 14 | scenario-labs/blender-plugin issue #3 (Blender Lab 라이선스) | GitHub 이슈 | 2026 | 공식 blender_mcp manifest의 GPL-3.0-or-later 확인과 아키텍처 비교 | <https://github.com/scenario-labs/blender-plugin/issues/3> |
| 15 | GHSA-qqw9-95ww-prfm / CVE-2026-10661 | 보안 권고 | 2026-06-02/03 | ahujasid blender-mcp 취약점의 범위, 심각도, 패치 커밋 | <https://github.com/advisories/GHSA-qqw9-95ww-prfm> |
| 16 | ahujasid issue #232 텔레메트리 opt-in 요구 | GitHub 이슈 | 2026-04-20 | 과거 기본 ON(consent default=True)과 Supabase 업로드 데이터 범위 | <https://github.com/ahujasid/blender-mcp/issues/232> |
| 17 | ahujasid issue #347 tool-schema 컨텍스트 비용 | GitHub 이슈 | 2026-09-05 | 5,462→6,928 토큰 측정치와 클라이언트별 영향 | <https://github.com/ahujasid/blender-mcp/issues/347> |
| 18 | ahujasid issues #339/#357/#219/#187 ⚠ | GitHub 이슈 | 2026-02~09 | Windows 타임아웃(프레이밍 불일치 의심), 불완전 JSON, WSL 스크린샷 경로 문제 | <https://github.com/ahujasid/blender-mcp/issues/339> |
| 19 | newo-ether/blender-mcp releases | GitHub 릴리스 | v1.19.0 2026-09-21 | 노드 트리 패치 tool 진화와 slim export 수치 | <https://github.com/newo-ether/blender-mcp/releases> |
| 20 | HoldMyBeer-gg/blend-ai | GitHub README | v1.6.0 2026-09-25 | 186 tools, 샌드박스, Blender 4.2+ 호환 정보 | <https://github.com/HoldMyBeer-gg/blend-ai> |
| 21 | PatrykIti/blender-ai-mcp | GitHub README | v3.3.0 2026-05 | goal-first 라우팅과 결정적 검증 설계 원칙 | <https://github.com/PatrykIti/blender-ai-mcp> |
| 22 | RobLe3/cc-blender-skill (modeling/lighting/text-to-blender SKILL.md) | Claude Code 스킬 저장소 | v1.3.0 2026 | 치수, 베벨, 모디파이어 순서, 조명 비율, 바운스, QA 게이트 등 수치 규칙 | <https://github.com/RobLe3/cc-blender-skill> |
| 23 | ra100/blender-claude-plugin | Claude Code 플러그인 | v1.3.0 2026 | 공식 MCP 전제의 Blender 5.x 스킬과 설치 명령 | <https://github.com/ra100/blender-claude-plugin> |
| 24 | sakalond/StableGen | GitHub README | 2026-06-12 | Blender 내 AI 투영 텍스처링과 TRELLIS.2, 버전 지원 범위 | <https://github.com/sakalond/StableGen> |
| 25 | ifBars/blender-agent-studio | GitHub README | 2026 | Codex 헤드리스 CLI 방식의 구체 사례 | <https://github.com/ifBars/blender-agent-studio> |
| 26 | captproton/yardstake-ux issue #151 (--python-exit-code) | GitHub 이슈 | 2026 | 헤드리스 실행에서 예외가 나도 exit 0이 되는 함정과 해결책 | <https://github.com/captproton/yardstake-ux/issues/151> |
| 27 | Blender 5.0 Python API release notes | 공식 릴리스 노트 (검색 요약으로 확인) | 2025-11 | EEVEE ID, action.fcurves, bgl, compositor 등 5.0 변경점 | <https://developer.blender.org/docs/release_notes/5.0/python_api/> |
| 28 | Blender 5.2 LTS Python API release notes | 공식 릴리스 노트 (검색 요약으로 확인) | 2026-07-14 | GN 모디파이어 properties.inputs API 변경 | <https://developer.blender.org/docs/release_notes/5.2/python_api/> |
| 29 | benrugg/AI-Render issue #171 / EverettFish issue #172 | GitHub 이슈 | 2025-2026 | scene.node_tree→compositing_node_group 실제 파손 사례와 호환 코드 | <https://github.com/benrugg/AI-Render/issues/171> |
| 30 | PyPI bpy | 패키지 레지스트리 | 5.2.2, 2026-09-15 | Blender를 Python 모듈로 쓰는 헤드리스 대안(Python 3.13 전용) | <https://pypi.org/project/bpy/> |
| 31 | dhakalnirajan/blender-open-mcp | GitHub README | 2026-09-04 | 로컬 LLM provider 전환형 MCP | <https://github.com/dhakalnirajan/blender-open-mcp> |
| 32 | Introducing Blender Lab / CG Channel 보도 | 뉴스 | 2025-11 | Blender Lab 출범과 MCP 서버를 AI/ML 첫 과제로 삼은 배경 | <https://www.cgchannel.com/2025/11/blender-foundation-launches-the-blender-lab/> |

**⚠ 신뢰도 경고가 붙은 출처**

- <https://www.mindstudio.ai/blog/claude-fable-5-1-blender-video-generation> — AI 에이전트 플랫폼 업체의 대량 SEO 블로그입니다. 원문은 차단돼 열람하지 못했고, 조사 결과도 '검색 요약으로만 확인'했다고 밝힙니다. '37초 시애틀 주택 워크스루'의 서버 종류와 재현 절차가 없으니 사례로 싣지 말거나 '미검증 주장'으로 명시해야 합니다.
- <https://www.mindstudio.ai/blog/claude-blender-mcp-real-world-performance> — 같은 업체 SEO 블로그이고 원문 확인이 불가능했습니다. '2시간, Max 플랜 세션 토큰 60%' 같은 수치의 출처와 측정 조건을 알 수 없습니다.
- <https://gamedevacademy.org/gpt-astra-blender-mcp-tutorial/> — egress가 차단돼 확인하지 못했습니다. 조사 결과는 모델명을 'GPT-6 Astra'로 적었지만, 1차 출처인 ahujasid 이슈 #351은 'GPT Astra'라고만 씁니다. 모델명과 사용 MCP(ahujasid 여부)는 검증되지 않았습니다.
- <https://3d-agent.com/> — 상용 제품의 자사 마케팅 사이트입니다(차단돼 열람 불가). 가격 정보가 서로 모순되고 조사자도 자사 SEO 비중이 크다고 지적했습니다. 독립적인 검증 전에는 추천 목록에서 빼는 편이 안전합니다.
- <https://blenderartists.org/t/from-blender-mcp-to-3d-agent-anthropic-partners-with-blender-claude-ai-connector-now-official/1639106> — 제목부터 'Blender MCP에서 3D Agent로'라고 해서 공식 커넥터와 커뮤니티 MCP, 상용 제품을 뒤섞는 홍보성 글로 보입니다. 공식 커넥터는 Blender Lab이 만들었다는 1차 출처(anthropic.com, claude.com)와 어긋날 소지가 있습니다(차단돼 원문 미확인).
- <https://github.com/bpy-dev/blender-mcp/blob/main/readme_tools.rst> — 비공식 포크(developer preview)의 문서인데 공식 Blender Lab 서버 tool 목록의 출처로 쓰였습니다. get_runtime_python_api_docs 같은 포크 전용 tool이 공식 목록에 섞여 들어간 원인으로 보입니다.
- <https://pypi.org/project/mcp-blender/> — RFingAdam README가 이 PyPI 이름을 가리키지만 실제 소유자는 brnv(Artem)의 다른 프로젝트(v0.1.0)입니다. 설치 출처로 인용하면 공급망 혼동이 생깁니다.
- <https://github.com/ahujasid/blender-mcp/issues/339> — 이슈 자체는 믿을 만하지만, 이슈에서 언급된 blender-mcp.com(및 blendermcp.org) 같은 비공식 사이트는 비공식 애드온을 배포하는 곳입니다. 설치 출처로 쓰면 안 됩니다.

<a id="03_dcc-cad-mcp"></a>
## 기타 DCC·CAD·텍스처 앱 MCP

주제 원문: MCP servers for other DCC, CAD and texturing apps (Maya, 3ds Max, MotionBuilder, Houdini, Cinema 4D, ZBrush, SketchUp, Rhino/Grasshopper, Fusion, FreeCAD, OpenSCAD, CadQuery/build123d, Onshape, Substance 3D, Photoshop, Marvelous Designer, Spline, Plasticity, Womp, KeyShot, OpenUSD), 2026-09 기준

| # | 제목 | 유형 | 날짜 | 왜 유용한가 | URL |
|---|---|---|---|---|---|
| 1 | Claude for Creative Work (Anthropic) | 공식 발표 | 2026-04-28 | 9개 크리에이티브 커넥터 목록과 각 기능(Fusion, SketchUp, Blender, Adobe) 원문 | <https://www.anthropic.com/news/claude-for-creative-work> |
| 2 | Autodesk Fusion connector \| Claude | 공식 커넥터 페이지 | 2026-05 | Fusion MCP 활성화 경로(Preferences > General > API > Fusion MCP Server), 로컬 전용, Autodesk 제작 | <https://claude.com/connectors/autodesk-fusion> |
| 3 | Trimble SketchUp connector \| Claude | 공식 커넥터 페이지 | 2026-04 | 도구명 build_model/get_docs/save_model, MCP 엔드포인트 URL | <https://claude.com/connectors/sketchup> |
| 4 | Blender connector \| Claude | 공식 커넥터 페이지 | 2026-04 | Blender Lab 제작, 애드온 필요(교차 주제) | <https://claude.com/connectors/blender> |
| 5 | mcneel/RhinoAI (Rhino MCP Platform) | 공식 GitHub | 2026-09 | McNeel 공식 Rhino MCP, 설치 절차, 지원 클라이언트, 레시피와 고급 워크플로 문서 | <https://github.com/mcneel/RhinoAI> |
| 6 | RhinoAI connector.md / sketch-to-model.md / recipes.md / make-this-parametric.md | 공식 문서 | 2026 | '해석 먼저' 프롬프트, 파라메트릭 역설계 등 실무 노하우 원문 | <https://raw.githubusercontent.com/mcneel/RhinoAI/rhino-9.x/docs/content/docs/advanced/sketch-to-model.md> |
| 7 | healkeiser/fxhoudinimcp | GitHub README/Releases | v2.21.0 2026-09-23 | Houdini MCP 중 가장 포괄적(도구 206개, Houdini 22 테스트) | <https://github.com/healkeiser/fxhoudinimcp> |
| 8 | capoomgit/houdini-mcp | GitHub | 2026-06 | 가장 인기 있는 Houdini MCP, OPUS 연동 | <https://github.com/capoomgit/houdini-mcp> |
| 9 | SideFX and Nvidia bring MCP-powered AI agents to Houdini 22 (JPR) | 뉴스 (검색 요약만 확인) | 2026-07 | SideFX 공식 MCP(APEX Script) 프리뷰 정보 | <https://www.jonpeddie.com/news/sidefx-and-nvidia-bring-mcp-powered-ai-agents-to-houdini-22s-rigging-workflow-at-siggraph-2026/> |
| 10 | cl0nazepamm/3dsmax-mcp + Releases | GitHub Releases | v1.7.3 2026-09-23 | 3ds Max 도구 160개, Corona/Chaos Cosmos, 접촉·관통 검사 | <https://github.com/cl0nazepamm/3dsmax-mcp/releases> |
| 11 | GimbalGoats/GG_MayaMCP | GitHub | 2026-08 | Maya 타입 도구 71개와 보안 설계 | <https://github.com/GimbalGoats/GG_MayaMCP> |
| 12 | PatrickPalmer/MayaMCP | GitHub | 2025-05 | Maya MCP 레퍼런스 구현 | <https://github.com/PatrickPalmer/MayaMCP> |
| 13 | dcc-mcp organization repositories | GitHub org | 2026-09-26 | Maya/Max/Houdini/MotionBuilder/ZBrush/Substance/MD/Marmoset/SpeedTree/Gaea/OpenUSD 어댑터 목록 | <https://github.com/orgs/dcc-mcp/repositories> |
| 14 | dcc-mcp/dcc-mcp-core | GitHub | 2026-09 | 멀티 DCC gateway 아키텍처와 스킬 계약 | <https://github.com/dcc-mcp/dcc-mcp-core> |
| 15 | dcc-mcp/dcc-mcp-zbrush | GitHub | 2026 | ZBrush 2026.1 Python SDK 기반 MCP | <https://github.com/dcc-mcp/dcc-mcp-zbrush> |
| 16 | ttiimmaacc/cinema4d-mcp | GitHub | 2026 | C4D MCP 대표 구현, MoGraph/Redshift | <https://github.com/ttiimmaacc/cinema4d-mcp> |
| 17 | kumoproductions/mcp-cinema4d | GitHub | 2026 | C4D 2026용 TypeScript MCP와 보안 게이트 | <https://github.com/kumoproductions/mcp-cinema4d> |
| 18 | jingcheng-chen/rhinomcp (Releases) | GitHub Releases | 0.4.1.1 2026-09-14 | 측정·단면·GH 도구의 변천 | <https://github.com/jingcheng-chen/rhinomcp/releases> |
| 19 | neka-nat/freecad-mcp | GitHub | 2026-09 | 가장 인기 있는 CAD MCP | <https://github.com/neka-nat/freecad-mcp> |
| 20 | pzfreo/build123d-mcp | GitHub | 2026-09 | 측정·렌더 검증 루프형 코드 CAD MCP | <https://github.com/pzfreo/build123d-mcp> |
| 21 | jdilla1277/agentcad | GitHub | 2026-09 | build123d/CadQuery CLI+MCP, GLB 익스포트, 시각 diff | <https://github.com/jdilla1277/agentcad> |
| 22 | ReshefElisha/jarvis-onshape-mcp RESEARCH.md | 실험 보고서 | 2026 | Opus 4.7 도면→CAD 정확도 정량 데이터 | <https://raw.githubusercontent.com/ReshefElisha/jarvis-onshape-mcp/main/RESEARCH.md> |
| 23 | elliezu/SubstancePainterMCP | GitHub | 2026-07 | Painter 12.1.1용 도구 79개, remote scripting 설정 | <https://github.com/elliezu/SubstancePainterMCP> |
| 24 | matthieuhuguet/substance-designer-mcp ⚠ | GitHub | 2026-05 | Designer PBR 그래프 생성 레시피와 제약 | <https://github.com/matthieuhuguet/substance-designer-mcp> |
| 25 | mikechambers/adb-mcp | GitHub | 2026 | 데스크톱 Photoshop/Premiere 등 UXP 기반 MCP | <https://github.com/mikechambers/adb-mcp> |
| 26 | alisaitteke/photoshop-mcp | GitHub | 2026-09 | Photoshop 도구 118~122개 | <https://github.com/alisaitteke/photoshop-mcp> |
| 27 | ysk424/marvelous-designer-mcp | GitHub | 2026-05 | MD 2026 Python 기반 천 시뮬레이션 MCP | <https://github.com/ysk424/marvelous-designer-mcp> |
| 28 | truman-t3/keyshot-mcp | GitHub | 2026-09 | KeyShot 헤드리스 렌더 MCP | <https://github.com/truman-t3/keyshot-mcp> |
| 29 | aydinfer/spline-mcp-server | GitHub | 아카이브 | Spline에 공개 API가 없다는 한계 확인 | <https://github.com/aydinfer/spline-mcp-server> |
| 30 | ozymandi/PlasticityMCP | GitHub | 2026-04 | Plasticity MCP 미동작 상태 확인 | <https://github.com/ozymandi/PlasticityMCP> |
| 31 | NVIDIA-Omniverse/kit-usd-agents | GitHub (NVIDIA) | 2026 | USD Code MCP 등 NVIDIA MCP | <https://github.com/NVIDIA-Omniverse/kit-usd-agents> |
| 32 | faust-machines/fusion360-mcp-server | GitHub | 2026-09-16 | Fusion 커뮤니티 도구 93개(간섭 검사, CAM 등) | <https://github.com/faust-machines/fusion360-mcp-server> |
| 33 | HurtzDonutStudios/ai-forge-mcp ⚠ | GitHub (상용) | 2026-04 | 게임 에셋 멀티 DCC 파이프라인 구성 예 | <https://github.com/HurtzDonutStudios/ai-forge-mcp> |
| 34 | pascalorg/editor | GitHub | 2026-09 | 가구 배치(furniture-fit skill) MCP, 교차 주제 | <https://github.com/pascalorg/editor> |
| 35 | Autodesk Maya 2027 Help — Introducing Autodesk Assistant | 공식 문서 (검색 요약만 확인) | 2026-03 | Maya 2027 Autodesk Assistant가 문서 도우미임을 확인 | <https://help.autodesk.com/view/MAYAUL/2027/ENU/?guid=GUID-B126B0C2-A72E-498F-B46B-56DEEFA72478> |

**⚠ 신뢰도 경고가 붙은 출처**

- <https://github.com/HurtzDonutStudios/ai-forge-mcp> — 상용 Early Access 제품의 자기 홍보 README다('AAA', '248,000+ lines', 'One prompt in, game-ready asset out'). Hunyuan3D를 'MIT License'라고 적었는데 이는 Tencent Hunyuan 3D Community License와 모순된다(EU, 영국, 한국 제외). 'AI Legends MMO 제작'도 검증되지 않은 자기 주장이라 1차 근거로 쓰면 안 된다.
- <https://github.com/newsbubbles/zbrush-mcp> — 커밋이 1개뿐인 스캐폴드성 저장소다. 'ZBrush 2024+ with Python SDK'라고 주장하지만, dcc-mcp-zbrush README는 공식 Python SDK가 ZBrush 2026.1+를 요구하며 이전 스캐폴드의 HTTP 서버 가정이 틀렸다고 적고 있다. AI가 생성한 미검증 코드일 가능성이 높다.
- <https://www.mindstudio.ai/blog/claude-mcp-adobe-vs-photoshop-premiere-what-it-does> — MindStudio(경쟁 에이전트 플랫폼)의 마케팅 블로그로 SEO형 제목을 달고 있고 프록시 차단으로 내용을 확인하지 못했다. Adobe 커넥터의 실제 성격(원격 엔드포인트 adobe-creativity.adobe.io, 도구 67개)은 Claude 커넥터 페이지라는 1차 출처로 대체해야 한다.
- <https://pypi.org/project/fxhoudinimcp/> — PyPI summary에 '179 tools'라는 오래된 수치가 남아 있어 README(206개)와 다르다. 도구 수는 README를 기준으로 인용해야 한다.
- <https://github.com/matthieuhuguet/substance-designer-mcp> — README 안에서 수치가 어긋난다('16 MCP tools'와 도구 표 23개). '최초의 SD MCP'도 자기 주장이다. 기능 설명은 표를 기준으로 인용해야 한다.

<a id="04_engine-mcp"></a>
## 게임 엔진·실시간 3D MCP

주제 원문: 게임 엔진·실시간 3D용 MCP 서버 (Unreal/Unity/Godot/Roblox/Omniverse·OpenUSD/웹 3D/O3DE): AAA급 씬을 AI로 구성하기 위한 서버 조사, 실전 노하우, 사례 (2026-09 기준)

| # | 제목 | 유형 | 날짜 | 왜 유용한가 | URL |
|---|---|---|---|---|---|
| 1 | Unreal MCP in Unreal Editor (UE 5.8 공식 문서) | 공식 문서 (접근 차단, 검색 스니펫만 확인) | 2026-06 | 공식 MCP 플러그인의 원문 문서 | <https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor?lang=en-US> |
| 2 | unreal-agent-harness UNREAL-MCP-ENABLE.md | GitHub 문서 | 2026 | UE 5.8 공식 MCP 활성화 절차, 콘솔 명령, ini 설정, 툴셋 이름 | <https://github.com/per-simmons/unreal-agent-harness/blob/master/docs/UNREAL-MCP-ENABLE.md> |
| 3 | unreal-agent-harness (README와 docs 전체) | GitHub 사례 저장소 | 2026-06~ | Claude + UE 5.8 MCP 도시·실내 제작 전 과정, PCG·조명·사실감 레시피 | <https://github.com/per-simmons/unreal-agent-harness> |
| 4 | REALISM-GUIDE.md | GitHub 문서 | 2026 | 노멀 강도, 타일링, 데칼, 베벨, 노출 등 포토리얼 수치 | <https://github.com/per-simmons/unreal-agent-harness/blob/master/docs/REALISM-GUIDE.md> |
| 5 | PCG-GUIDE.md | GitHub 문서 | 2026-06-21 | PCGToolset 호출 형식, 검증된 파라미터, 7가지 함정 | <https://github.com/per-simmons/unreal-agent-harness/blob/master/docs/PCG-GUIDE.md> |
| 6 | golden-hour-lighting-plan.md | GitHub 문서 | 2026 | 태양 각도, 색온도, 노출 EV 등 조명 수치와 MCP 호출 순서 | <https://github.com/per-simmons/unreal-agent-harness/blob/master/docs/golden-hour-lighting-plan.md> |
| 7 | ibrews/ue5-mcp SKILL.md (UE5 MCP Field Manual) | GitHub 스킬 문서 | 2026 | 크래시·조용한 실패·검증 패턴 체크리스트 | <https://github.com/ibrews/ue5-mcp/blob/main/SKILL.md> |
| 8 | ChiR24/Unreal_mcp README와 Roadmap | GitHub | 2026-09 | landscape, foliage, sky, PCG 도구 목록과 미구현 항목(post-process, Megascans) | <https://github.com/ChiR24/Unreal_mcp/blob/main/docs/Roadmap.md> |
| 9 | flopperam/unreal-engine-mcp | GitHub | 2026 | 월드빌딩 도구 목록, Aura 인수, 무료·유료 구분 | <https://github.com/flopperam/unreal-engine-mcp> |
| 10 | chongdashu/unreal-mcp | GitHub | 2025~2026 | 원조 Unreal MCP의 구조와 한계 | <https://github.com/chongdashu/unreal-mcp> |
| 11 | runreal/unreal-mcp | GitHub | 2026 | 플러그인 없이 Python Remote Execution을 쓰는 방식 | <https://github.com/runreal/unreal-mcp> |
| 12 | GenOrca/unreal-mcp | GitHub | 2026-07 | 액터 라벨이 찍힌 뷰포트 캡처 | <https://github.com/GenOrca/unreal-mcp> |
| 13 | MC-Oruc/UE57-MCP-PortKit ⚠ | GitHub | 2026 | UE 5.8 툴셋 규모(40개 툴셋, 414개 서브툴), 5.7 백포트, Material Graph DSL | <https://github.com/MC-Oruc/UE57-MCP-PortKit> |
| 14 | WildCake/unreal-engine-mcp-codex | GitHub 스킬 | 2026-06-20 | 공식 MCP 호출 흐름(list_toolsets, describe_toolset, call_tool)과 Codex 설정 | <https://github.com/WildCake/unreal-engine-mcp-codex> |
| 15 | JosephOIbrahim/UnrealEngine_Bridge | GitHub | 2026-07 | 뷰포트 인지와 diff, 공식 MCP와의 병행 운용 | <https://github.com/JosephOIbrahim/UnrealEngine_Bridge> |
| 16 | 44-99/unreal-agent-benchmark | GitHub 벤치마크 | 2026-07 | 데모 수준을 넘어선 비판적 평가 설계 | <https://github.com/44-99/unreal-agent-benchmark> |
| 17 | GitHub topic: unreal-mcp | GitHub 목록 | 2026-09 | UE 5.8 MCP 파생 프로젝트 현황 | <https://github.com/topics/unreal-mcp> |
| 18 | CoplayDev/unity-mcp | GitHub | 2026-09 | 가장 인기 있는 Unity MCP, 설치법과 버전 | <https://github.com/CoplayDev/unity-mcp> |
| 19 | CoplayDev asset-gen-manual-verification.md | GitHub 문서 | 2026 | Tripo·Meshy·Sketchfab 연계 도구 사양 | <https://github.com/CoplayDev/unity-mcp/blob/main/docs/asset-gen-manual-verification.md> |
| 20 | IvanMurzak/Unity-MCP default-mcp-tools.md | GitHub 문서 | 2026 | 스크린샷(격리 포함), 머티리얼, 프리팹 도구 이름 | <https://github.com/IvanMurzak/Unity-MCP/blob/main/docs/default-mcp-tools.md> |
| 21 | Unity MCP overview (com.unity.ai.assistant 2.18) | 공식 문서 (검색 스니펫) | 2026 | 공식 Unity MCP 구조(bridge, relay)와 요구사항 | <https://docs.unity3d.com/Packages/com.unity.ai.assistant@2.18/manual/integration/unity-mcp-overview.html> |
| 22 | Unity AI open beta (Unity Discussions) | 공식 포럼 (검색 스니펫) | 2026-05 | Unity AI 오픈 베타 공지 | <https://discussions.unity.com/t/unity-ai-s-open-beta-now-live-for-unity-6/1718560> |
| 23 | hi-godot/godot-ai (README, docs/TOOLS.md) | GitHub | 2026-09 | Godot 3D·머티리얼·시네마틱 스크린샷 도구 | <https://github.com/hi-godot/godot-ai> |
| 24 | Coding-Solo/godot-mcp | GitHub | 2026 | 경량 Godot MCP | <https://github.com/Coding-Solo/godot-mcp> |
| 25 | youichi-uda/godot-mcp-pro | GitHub | 2026 | 유료 Godot MCP의 도구 구성 | <https://github.com/youichi-uda/godot-mcp-pro> |
| 26 | Roblox/studio-rust-mcp-server (아카이브) | GitHub 공식 | 2026 | 내장 MCP 전환 확인, 기존 도구 목록 | <https://github.com/Roblox/studio-rust-mcp-server> |
| 27 | Connect to the Roblox Studio MCP server | 공식 문서 (검색 스니펫) | 2026 | 내장 MCP 설정 | <https://create.roblox.com/docs/studio/mcp> |
| 28 | NVIDIA-Omniverse/kit-usd-agents | GitHub 공식 | 2026 | Kit·USD·OmniUI·Isaac MCP의 범위(지식 전용) | <https://github.com/NVIDIA-Omniverse/kit-usd-agents> |
| 29 | RTX Remix: Using AI Agents with MCP (learning-mcp.md) | GitHub 공식 문서 | 2026 | RTX Remix 내장 MCP 엔드포인트와 포트, 번들 스킬 | <https://github.com/NVIDIAGameWorks/toolkit-remix> |
| 30 | playcanvas/editor-mcp-server | GitHub 공식 | 2026 | 웹 3D 공식 에디터 MCP, Sketchfab 연동 | <https://github.com/playcanvas/editor-mcp-server> |
| 31 | Babylon.js packages/tools (MCP 서버들) | GitHub 공식 | 2026 | NME·NGE 등 공식 MCP 서버의 존재와 흐름 | <https://github.com/BabylonJS/Babylon.js/tree/master/packages/tools> |
| 32 | DmitriyGolub/threejs-devtools-mcp | GitHub | 2026 | three.js·R3F 라이브 씬 편집 | <https://github.com/DmitriyGolub/threejs-devtools-mcp> |
| 33 | nickschuetz/o3de-mcp | GitHub | 2026-09 | O3DE MCP | <https://github.com/nickschuetz/o3de-mcp> |
| 34 | punkpeye/awesome-mcp-servers (Gaming 섹션) ⚠ | 큐레이션 목록 | 2026-09 | 게임 엔진 MCP 전수 목록(Quartermaster, weppy-roblox, unity-biome 등) | <https://github.com/punkpeye/awesome-mcp-servers> |
| 35 | Tanshaydar/Quartermaster | GitHub | 2026 | Fab·Megascans 보유 에셋 검색 MCP | <https://github.com/Tanshaydar/Quartermaster> |
| 36 | Unreal Engine 6 AI: Epic builds in Claude and Gemini (The Next Web) | 뉴스 (검색 스니펫) | 2026-06 | UE6 Claude·Gemini MCP 통합 발표 | <https://thenextweb.com/news/epic-unreal-engine-6-ai-claude-gemini> |

**⚠ 신뢰도 경고가 붙은 출처**

- <https://byteiota.com/unreal-engine-5-8-ships-mcp-server-ai-agents-can-now-drive-the-editor/> — UE 5.8 출시일 주장의 유일한 인용 출처인데 접근이 차단되어 확인할 수 없었습니다. 개발 뉴스를 재가공하는 블로그로 보이며, 출시일 같은 핵심 사실은 Epic 공식 릴리스 노트로 대체해야 합니다.
- <https://www.bitsminds.com/news/epic-unreal-engine-6-unified-mcp-claude-gemini-2026> — AI가 생성한 뉴스 집약 사이트로 의심됩니다. 1차 출처가 아니며 UE6 발표 내용(EA 2027년 말 등)의 근거로 쓰기 부적절합니다(접근도 차단).
- <https://www.summerengine.com/blog/best-godot-mcp-server> — 자사 제품을 파는 벤더 블로그의 '베스트 목록' 형식이라 편향 가능성이 있습니다. SEO성 비교 글이며 접근이 차단되어 검증하지 못했습니다.
- <https://forums.unrealengine.com/t/strayspark-unreal-mcp-server-200-ai-tools-for-ue5-editor-automation-via-mcp/2707474> — 판매자가 직접 올린 홍보 글('200+ tools')입니다. 도구 수 등 마케팅 수치는 독립적으로 검증되지 않았습니다.
- <https://ludusengine.com/blog/unreal-mcp-plugin-ue5-8-setup> — 경쟁 상용 제품(Ludus AI) 벤더의 블로그라 공식 MCP의 약점을 부각할 동기가 있습니다. 접근이 차단되어 검증하지 못했습니다.
- <https://github.com/MC-Oruc/UE57-MCP-PortKit> — 1 star, 28 commits 규모의 저장소입니다. '40 toolsets / 414 sub-tools'가 리서처 요약에서 공식 MCP 규모처럼 인용되었지만, Epic README(30+ toolsets), per-simmons(약 28), UnrealEngine_Bridge(830 tools)와 서로 맞지 않습니다.
- <https://github.com/punkpeye/awesome-mcp-servers> — 큐레이션 목록의 설명이 원 저장소와 다릅니다(unity-biome-mcp 47 tools 대 저장소 160, godot-mcp-pro 84 대 162/187). 발견용으로만 쓰고 수치는 원 저장소에서 가져와야 합니다.
- <https://github.com/ChiR24/Unreal_mcp/releases> — HTML 릴리스 페이지에는 연도가 빠져 있어 자동 요약 도구가 2024로 오독했습니다. 날짜는 releases.atom(ISO 타임스탬프)으로 확인해야 합니다.

<a id="05_ai-3d-generation"></a>
## AI 3D 생성 (Text/Image-to-3D)

주제 원문: Text/Image-to-3D 생성 모델·서비스 현황과 MCP 워크플로 활용법 (2026년 9월 기준)

| # | 제목 | 유형 | 날짜 | 왜 유용한가 | URL |
|---|---|---|---|---|---|
| 1 | microsoft/TRELLIS.2 GitHub (README, example.py, example_texturing.py, commits) | GitHub 공식 저장소 | 2025-12-16 공개, 2026… | 4B 파라미터, O-Voxel, PBR 속성, H100 속도, 24GB VRAM, to_glb 기본값, 텍스처링 파이프라인, MIT 라이선스 | <https://github.com/microsoft/TRELLIS.2> |
| 2 | microsoft/TRELLIS.2 Issue #181 – TRELLIS vs TRELLIS.2-4B geometry metrics (3D Arena 2,307… ⚠ | GitHub 이슈 (독립 평가) | 2026-08-04 | non-watertight 91.1%, non-manifold 14.9% 등 독립 기하 QA 수치 | <https://github.com/microsoft/TRELLIS.2/issues/181> |
| 3 | microsoft/TRELLIS.2 Issue #65 – artifacts without background removal | GitHub 이슈 | 2025-12-30 | 배경 제거가 필수라는 실사용 근거와 Hunyuan3D 2.1과의 비교 | <https://github.com/microsoft/TRELLIS.2/issues/65> |
| 4 | TencentARC/Pixal3D | GitHub 공식 저장소 | 2026-04~2026-09 | SIGGRAPH 2026, TRELLIS.2 backbone, MIT, 단일·multi-view 추론 명령어 | <https://github.com/TencentARC/Pixal3D> |
| 5 | Tencent-Hunyuan/Hunyuan3D-2.1 README와 LICENSE | GitHub 라이선스 원문 | 2025-06-13 | Territory에서 EU, 영국, 대한민국 제외와 출력물 사용 제한 조항 | <https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/blob/main/LICENSE> |
| 6 | Tencent-Hunyuan GitHub 3D 저장소 목록 | GitHub 조직 페이지 | 2026-08 기준 | HY-World 2.0, Buffalo1.0, WorldClaw, Omni, Part 등 최신 저장소와 날짜 | <https://github.com/orgs/Tencent-Hunyuan/repositories?q=3d> |
| 7 | Tencent-Hunyuan/HY-World-2.0 (README, License.txt) | GitHub 공식 저장소 | 2026-04-16 | mesh, 3DGS, point cloud 출력과 한국 제외 라이선스 | <https://github.com/Tencent-Hunyuan/HY-World-2.0> |
| 8 | DeemosTech/rodin3d-skills SKILL.md (Gen-2.5) | 공식 Agent Skill 문서 | 2026 | Gen-2.5 티어 용도, 면 수 매핑, credit, 이미지 제한, bbox, TAPose, HighPack | <https://github.com/DeemosTech/rodin3d-skills/blob/main/skills/rodin3d-skill/SKILL.md> |
| 9 | DeemosTech/hyper3d-cli README | 공식 CLI 문서 | 2026-09-23 | Raw/Quad 폴리곤 범위와 기본값, texture-delight, BANG --strength | <https://raw.githubusercontent.com/DeemosTech/hyper3d-cli/main/README.md> |
| 10 | ComfyUI comfy_api_nodes (nodes_rodin/tripo/meshy/hunyuan3d.py)와 커밋 이력 | 오픈소스 코드 (파트너 API 통합) | 2025-05~2026-09 | Rodin Gen-2.5, Tripo v3.1/P1/P2, Meshy 7/7.1, Hunyuan 3.0/3.1의 파라미터 범위와 출시 시점 교차 확인 | <https://github.com/comfyanonymous/ComfyUI/tree/master/comfy_api_nodes> |
| 11 | VAST-AI-Research/tripo-python-sdk client.py | 공식 SDK 코드 | v0.4.2 2026-07-01 | model_version 문자열(v3.1-20260211, P1-20260311 등)과 기본값 | <https://raw.githubusercontent.com/VAST-AI-Research/tripo-python-sdk/master/tripo3d/client.py> |
| 12 | meshy-dev/meshy-mcp-server (README, commits, releases) | 공식 MCP 서버 | v0.5.0 2026-08-11, … | 24개 도구, 모델별 credit 표, smart-topology, 설치 명령 | <https://github.com/meshy-dev/meshy-mcp-server> |
| 13 | mordor-forge/trident-mcp docs/MCP_TOOLS.md | 커뮤니티 MCP 문서 | 2026-07 | Tripo P1과 H3.1의 용도, 시간, credit 실측 | <https://github.com/mordor-forge/trident-mcp/blob/main/docs/MCP_TOOLS.md> |
| 14 | scenario-labs/skills (scenario-3d, 3d-worlds, sparc3d, rodin, meshy, model-comparison) | 상용 MCP 공식 Agent Skills | 2026-09 | GPT-6 Astra 3D, Sparc3D/Hitem3D, Marble 티어와 splat 출력, 레퍼런스 이미지 규칙, 흔한 실수 | <https://github.com/scenario-labs/skills> |
| 15 | ahujasid/blender-mcp (README, server.py, addon.py) | GitHub 오픈소스 MCP | 2026-09 기준 | Rodin, Hunyuan, Tripo 통합 도구 이름, 환경변수, 리전 설정, 검증 가이드 | <https://github.com/ahujasid/blender-mcp> |
| 16 | zorrobyte/asset-studio | 실사용 파이프라인 사례 (GitHub) | 2026-09 | 로컬 text-to-image-to-3D-to-Blender 전 과정의 수치, 프리셋, 교훈 | <https://github.com/zorrobyte/asset-studio> |
| 17 | Bingeljell/image-to-3dlab (README, info_and_credits.md) | 커뮤니티 비교 실험 (GitHub) | 2026 | Pixal3D, TRELLIS.2, Hunyuan-MLX, SF3D 정성 비교와 라이선스 정리 | <https://github.com/Bingeljell/image-to-3dlab> |
| 18 | facebookresearch/sam-3d-objects (README, LICENSE) | GitHub 공식 저장소 | 2025-11-19, 2026-06… | splat과 mesh 출력, 다중 객체 레이아웃, SAM License 상업 허용 | <https://github.com/facebookresearch/sam-3d-objects> |
| 19 | GeekatplayStudio/comfyui-hitem3d ⚠ | 커뮤니티 통합 코드 | 2026-01 | Hitem3D 모델 버전, 해상도(1536pro), face 범위, multi-view 순서 | <https://github.com/GeekatplayStudio/comfyui-hitem3d> |
| 20 | dcc-mcp/dcc-ai-hunyuan3d tools.yaml | 커뮤니티 MCP skill | 2026-08-25 | Tencent Cloud Hunyuan 3D 3.0/3.1 파라미터 | <https://raw.githubusercontent.com/dcc-mcp/dcc-ai-hunyuan3d/main/skill/hunyuan3d/tools.yaml> |
| 21 | stepfun-ai/Step1X-3D | GitHub 공식 저장소 | 2025-05-13 | Apache-2.0 오픈 대안의 스펙 | <https://github.com/stepfun-ai/Step1X-3D> |
| 22 | DreamTechAI/Direct3D-S2 | GitHub 공식 저장소 | 2025-05-30 | MIT 고해상도 shape 모델의 VRAM | <https://github.com/DreamTechAI/Direct3D-S2> |
| 23 | wgsxm/PartCrafter | GitHub 공식 저장소 | 2025-07-13 | part-aware 생성(MIT, 8GB) | <https://github.com/wgsxm/PartCrafter> |
| 24 | Roblox/cube (README, LICENSE) | GitHub 공식 저장소 | 2025-03~2026-05 | bbox conditioning, CubePart, research-only 라이선스 | <https://github.com/Roblox/cube> |
| 25 | Stability-AI/stable-point-aware-3d LICENSE.md | 라이선스 원문 | 2025 | 연매출 100만 달러 기준 Community License | <https://github.com/Stability-AI/stable-point-aware-3d/blob/main/LICENSE.md> |
| 26 | KaelNebula/rodin-via-blender ⚠ | 사례 (Claude Code skill) | 2026-05 | Rodin과 Blender MCP로 FRP 조형물을 만드는 실제 흐름 | <https://github.com/KaelNebula/rodin-via-blender> |
| 27 | AIWHOS/sketch-to-3d-codex ⚠ | 사례 (Codex skill) | 2026-09 | 사람 승인 게이트가 있는 스케치-to-Rodin 워크플로 | <https://github.com/AIWHOS/sketch-to-3d-codex> |
| 28 | aigeboku/blender-ai-3d-setup ⚠ | 사례 (Claude Desktop 설정 skill) | 2026-05 | Gemini, Hitem3D, Blender MCP로 가구를 배치한 사례 | <https://github.com/aigeboku/blender-ai-3d-setup> |
| 29 | elithril/blender-kiln | 사례 (Claude Code skill) | 2026-08 | 8단계 에셋 파이프라인과 glTF 주의사항 | <https://github.com/elithril/blender-kiln> |
| 30 | img2threejs/img2threejs | 오픈소스 에이전트 워크플로 | 2026-09-23 | procedural 코드 모델링과 단계별 quality gate 대안 | <https://github.com/img2threejs/img2threejs> |
| 31 | ziangcao0312/PhysX-Anything | GitHub 연구 저장소 | CVPR 2026 | 관절이 있는 가구와 URDF 생성 | <https://github.com/ziangcao0312/PhysX-Anything> |
| 32 | nv-tlabs/lyra | GitHub 공식 저장소 | 2026-04-15 (2.0) | NVIDIA 오픈 3D 월드 모델 현황 | <https://github.com/nv-tlabs/lyra> |

**⚠ 신뢰도 경고가 붙은 출처**

- <https://github.com/microsoft/TRELLIS.2/issues/181> — 벤더(Topoheal)가 올린 홍보성 이슈입니다. 인용된 생성기별 수치(TRELLIS.2 n=101)는 원 보고서에서 2026-09-01 'superseded'로 철회되었습니다. 독립 평가로 인용하면 안 됩니다.
- <https://github.com/alza123123/3dqa-benchmark> — 수치 표가 삭제되고 topoheal.com(접근 불가)으로 리다이렉트됩니다. 엔진(3dqa)은 source-available 비재배포 라이선스라서 독립 재현성과 개방성이 제한적입니다.
- <https://github.com/GeekatplayStudio/comfyui-hitem3d> — Hitem3D 공식이 아닌 커뮤니티 래퍼입니다(GITHUB_READY.md 등 자동 생성으로 보이는 문서가 다수 있음). 파라미터의 1차 출처로 삼으면 안 되고 Scenario Sparc3D skill 등으로 교차 확인이 필요합니다. 마지막 업데이트는 2026-01입니다.
- <https://github.com/AIWHOS/sketch-to-3d-codex> — README가 직접 '실제 Hyper3D 생성, import, 리깅, 렌더링을 테스트하지 않았다'고 밝힙니다. 커밋 1개짜리 저장소라 성공 사례 근거로 쓸 수 없습니다.
- <https://github.com/KaelNebula/rodin-via-blender> — 커밋 1개(2026-05-02)짜리 개인 skill이고 결과물 증빙이 없습니다. 워크플로 아이디어 참고용일 뿐 검증된 사례로 볼 수 없습니다.
- <https://github.com/aigeboku/blender-ai-3d-setup> — 커밋 1개(2026-05-16)짜리 설정 가이드이고 실제 결과 품질 증빙이 없습니다.
- <https://raw.githubusercontent.com/meshy-dev/meshy-mcp-server/main/README.md> — 공식 문서지만 'text-to-3D에 meshy-7 없음'이라는 기술이 ComfyUI 공식 파트너 노드(2026-08-24 meshy-7, 2026-09-20 meshy-7.1을 text-to-3D에 노출)와 충돌합니다. 모델 지원 범위는 Meshy 공식 API 문서로 재확인해야 합니다.
- <https://raw.githubusercontent.com/scenario-labs/skills/main/skills/scenario-3d/SKILL.md> — 'GPT-6 Astra 3D'의 유일한 출처입니다(2026-09-21 추가). 벤더 자체 문서라 성능 주장은 독립 검증이 없습니다. 단, 날조로 보이지는 않습니다(같은 저장소에 gpt-6-astra가 OpenAI Codex 모델명으로 등장).

<a id="06_texturing-materials"></a>
## AI 텍스처링·PBR 재질

주제 원문: AI 텍스처링 및 PBR 머티리얼: AI + MCP로 사실적이고 아름다운 텍스처/머티리얼 만들기 (2026-09 기준)

| # | 제목 | 유형 | 날짜 | 왜 유용한가 | URL |
|---|---|---|---|---|---|
| 1 | ahujasid/blender-mcp (mcp-for-blender) README | GitHub README | 2026-09 | Poly Haven, Sketchfab, Poly Pizza, Hunyuan, Rodin 통합, 해상도 권장, 메인 스레드 프리즈 경고 | <https://github.com/ahujasid/blender-mcp> |
| 2 | blender-mcp addon.py (Poly Haven 맵 테이블, 컬러스페이스 로직) | 소스코드 | 2026-09 | POLYHAVEN_TEXTURE_MAPS, 스킵 맵, sRGB/Non-Color 규칙 | <https://raw.githubusercontent.com/ahujasid/blender-mcp/main/addon.py> |
| 3 | blender-mcp server.py (MCP 도구 목록, asset_creation_strategy) | 소스코드 | 2026-09 | describe_node_type, bpy_api_lookup, get_viewport_screenshot, 텔레메트리 도구 확인 | <https://raw.githubusercontent.com/ahujasid/blender-mcp/main/src/blender_mcp/server.py> |
| 4 | Issue #361 Poly Haven integration is buggy | GitHub issue | 2026-09-14 | normal/displacement 미연결 등 실제 실패 원인 | <https://github.com/ahujasid/blender-mcp/issues/361> |
| 5 | PR #367 Fix the Poly Haven integration | GitHub PR | 2026-09-21 | Mapping POINT 수정, 실측 스케일, 49% 대역폭 감소, Blender 5.2.1 테스트 | <https://github.com/ahujasid/blender-mcp/pull/367> |
| 6 | Issue #190 duplicated Material Output / Principled BSDF | GitHub issue | 2026-08-09 | idempotent 머티리얼 리셋 패턴 | <https://github.com/ahujasid/blender-mcp/issues/190> |
| 7 | Issue/PR #343 texture an existing mesh with local Hunyuan3D-2 | GitHub PR | 2026-09-02 | MCP에서 기존 메시 재텍스처링 설계 | <https://github.com/ahujasid/blender-mcp/issues/343> |
| 8 | Tencent-Hunyuan/Hunyuan3D-2.1 | GitHub README | 2025-06-13 | Paint 2.1 PBR, VRAM 21GB/29GB, 코드 예시 | <https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1> |
| 9 | Hunyuan3D 2.1 LICENSE | 라이선스 | 2025 | EU/UK/한국 제외 조항 | <https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/LICENSE> |
| 10 | Tencent-Hunyuan/Hunyuan3D-2 | GitHub README | 2025 | Paint v2-0/Turbo, 2.5 발표일, blender_addon, api_server | <https://github.com/Tencent-Hunyuan/Hunyuan3D-2> |
| 11 | ZebinHe/MaterialMVP | GitHub README(ICCV 2025) | 2025-07 | 조명 불변 albedo + MR 생성, Paint-v2-1과의 관계 | <https://github.com/ZebinHe/MaterialMVP> |
| 12 | sakalond/StableGen | GitHub README | 2026-09 | 모드, 카메라 전략, PBR 분해, 요구사항 | <https://github.com/sakalond/StableGen> |
| 13 | StableGen Releases | GitHub releases | 2026-06-12 | 버전별 기능과 날짜 | <https://github.com/sakalond/StableGen/releases> |
| 14 | ubisoft/ubisoft-laforge-chord | GitHub README | 2025 | image→PBR, 연구 전용 라이선스 | <https://github.com/ubisoft/ubisoft-laforge-chord> |
| 15 | ubisoft/ComfyUI-Chord | GitHub README | 2025 | ComfyUI 워크플로 | <https://github.com/ubisoft/ComfyUI-Chord> |
| 16 | meshy-dev/meshy-mcp-server | GitHub README | 2026-09 | 공식 Meshy MCP 도구, 크레딧 | <https://github.com/meshy-dev/meshy-mcp-server> |
| 17 | Meshy MCP postprocessing.ts (retexture 스키마) | 소스코드 | 2026-09 | enable_pbr, remove_lighting, enable_original_uv 기본값 | <https://raw.githubusercontent.com/meshy-dev/meshy-mcp-server/main/src/schemas/postprocessing.ts> |
| 18 | Meshy MCP generation.ts | 소스코드 | 2026-09 | texture_prompt, texture_resolution | <https://raw.githubusercontent.com/meshy-dev/meshy-mcp-server/main/src/schemas/generation.ts> |
| 19 | Meshy MCP instructions.ts | 소스코드 | 2026-09 | 비용 확인, 스타일 입력 상호 배타 규칙 | <https://raw.githubusercontent.com/meshy-dev/meshy-mcp-server/main/src/instructions.ts> |
| 20 | Tripo Python SDK API.md | API 문서 | 2025~2026 | texture_model 파라미터 | <https://github.com/VAST-AI-Research/tripo-python-sdk/blob/master/docs/API.md> |
| 21 | microsoft/TRELLIS.2 | GitHub README | 2025~2026 | PBR 속성, texturing 모드, MIT, 24GB | <https://github.com/microsoft/TRELLIS.2> |
| 22 | huanngzh/MV-Adapter | GitHub README | 2025-06 | 형상 조건 멀티뷰 텍스처링 | <https://github.com/huanngzh/MV-Adapter> |
| 23 | MV-Adapter LICENSE | 라이선스 | - | Apache-2.0 확인 | <https://raw.githubusercontent.com/huanngzh/MV-Adapter/main/LICENSE> |
| 24 | 3DTopia/MaterialAnything | GitHub README | 2024-11 / CVPR 2025 | 임의 3D 오브젝트용 PBR 생성 | <https://github.com/3DTopia/MaterialAnything> |
| 25 | OpenTexture/Paint3D | GitHub README | CVPR 2024 | 조명 없는 2K UV 텍스처 | <https://github.com/OpenTexture/Paint3D> |
| 26 | LIU-Yuxin/SyncMVD | GitHub README | 2023~2024 | 동기화 멀티뷰 확산과 제약 | <https://github.com/LIU-Yuxin/SyncMVD> |
| 27 | daveredrum/Text2Tex | GitHub README | ICCV 2023 | 런타임과 VRAM | <https://github.com/daveredrum/Text2Tex> |
| 28 | CVMI-Lab/TEXGen | GitHub README | SIGGRAPH Asia 2024 | UV 도메인 feed-forward | <https://github.com/CVMI-Lab/TEXGen> |
| 29 | oakshy/RomanTex | GitHub README | ICCV 2025 | 3D-aware RoPE 텍스처 합성 | <https://github.com/oakshy/RomanTex> |
| 30 | ianhuang0630/BlenderAlchemyOfficial | GitHub README | ECCV 2024 | VLM 머티리얼 편집 루프 | <https://github.com/ianhuang0630/BlenderAlchemyOfficial> |
| 31 | mit-gfx/VLMaterial | GitHub README | ICLR 2025 | 이미지→Blender 노드 프로그램 | <https://github.com/mit-gfx/VLMaterial> |
| 32 | elliezu/SubstancePainterMCP | GitHub README | 2026-07 | Painter MCP 79개 도구 | <https://github.com/elliezu/SubstancePainterMCP> |
| 33 | parodyband/painter-mcp | GitHub README | 2026-09 | 관찰 중심 에이전트 워크플로 | <https://github.com/parodyband/painter-mcp> |
| 34 | matthieuhuguet/substance-designer-mcp | GitHub README | 2026-05 | Designer MCP와 레시피 | <https://github.com/matthieuhuguet/substance-designer-mcp> |
| 35 | SS-360/materialpilot ⚠ | GitHub README | 2026-09 | Material Maker MCP | <https://github.com/SS-360/materialpilot> |
| 36 | RodZill4/material-maker | GitHub README | 2026 | 오픈소스 절차 텍스처 도구 | <https://github.com/RodZill4/material-maker> |
| 37 | scenario-labs/blender-plugin | GitHub README | 2026-09 | 상용 PBR 생성 + 로컬 MCP | <https://github.com/scenario-labs/blender-plugin> |
| 38 | Kim2091/PBRify_Remix | GitHub README | 2026-02 | CC0 학습 PBR 생성 모델 | <https://github.com/Kim2091/PBRify_Remix> |
| 39 | NVIDIAGameWorks/ComfyUI-RTX-Remix | GitHub README | 2025~2026 | RTX Remix와 ComfyUI PBR 워크플로 | <https://github.com/NVIDIAGameWorks/ComfyUI-RTX-Remix> |
| 40 | NVIDIAGameWorks/toolkit-remix | GitHub README | 2026 | Generative AI 텍스처 리마스터, .mcp.json 존재 | <https://github.com/NVIDIAGameWorks/toolkit-remix> |
| 41 | prs-eth/Marigold | GitHub README | 2025-05 | IID Appearance/Lighting 모델 | <https://github.com/prs-eth/Marigold> |
| 42 | Stable-X/StableDelight | GitHub README | 2024~ | 스페큘러 제거 | <https://github.com/Stable-X/StableDelight> |
| 43 | HugoTini/DeepBump | GitHub README | - | color→normal→height/curvature | <https://github.com/HugoTini/DeepBump> |
| 44 | BoundingBoxSoftware/Materialize | GitHub README | - | 이미지→맵 변환 도구 | <https://github.com/BoundingBoxSoftware/Materialize> |
| 45 | spinagon/ComfyUI-seamless-tiling | GitHub README | - | 타일링 생성 기법 | <https://github.com/spinagon/ComfyUI-seamless-tiling> |
| 46 | carson-katri/dream-textures releases | GitHub releases | 2024-08-26 | 유지보수 정체 확인 | <https://github.com/carson-katri/dream-textures/releases> |
| 47 | AntonPalmqvist/physically-based-api | GitHub README | 2026 | CC0 PBR 값 DB | <https://github.com/AntonPalmqvist/physically-based-api> |
| 48 | physically-based-api materials.json | 데이터 | 2026 | 재질별 linear 색과 IOR 수치 | <https://raw.githubusercontent.com/AntonPalmqvist/physically-based-api/main/deploy/v2/materials.json> |
| 49 | RobLe3/cc-blender-skill | GitHub README | 2026-05 | Claude Code Blender 스킬 구성 | <https://github.com/RobLe3/cc-blender-skill> |
| 50 | cc-blender-skill blender-materials SKILL.md ⚠ | 스킬 문서 | 2026 | 수치형 머티리얼 레시피 | <https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-materials/SKILL.md> |
| 51 | cc-blender-skill materials overview.md | 스킬 문서 | 2026 | 흔한 실패와 절차 노드 체인 | <https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-materials/references/overview.md> |
| 52 | elithril/blender-kiln ⚠ | GitHub README | 2026-08 | 8단계 파이프라인과 실측 | <https://github.com/elithril/blender-kiln> |
| 53 | blender-kiln texturing-strategy.md | 스킬 문서 | 2026 | glTF 누락 맵 실측, 존 분류, 베이크 절차 | <https://raw.githubusercontent.com/elithril/blender-kiln/main/references/texturing-strategy.md> |
| 54 | blender-kiln uv-materials.md | 스킬 문서 | 2026 | Smart UV 값, 텍셀 밀도 표, ORM | <https://raw.githubusercontent.com/elithril/blender-kiln/main/references/uv-materials.md> |
| 55 | glTF-Blender-IO scene_gltf2.rst | 공식 문서 | 2026 | ORM 채널, Occlusion 그룹, Tangent 노멀 | <https://raw.githubusercontent.com/KhronosGroup/glTF-Blender-IO/main/docs/blender_docs/scene_gltf2.rst> |
| 56 | Blender source: node_shader_bsdf_principled.cc | 소스코드 | 2026-09 main | 현재 Principled 소켓 이름과 기본값 | <https://raw.githubusercontent.com/blender/blender/main/source/blender/nodes/shader/nodes/node_shader_bsdf_principled.cc> |
| 57 | Blender source: object_bake_api.cc | 소스코드 | 2026-09 main | bake 오퍼레이터 파라미터 기본값과 오류 메시지 | <https://raw.githubusercontent.com/blender/blender/main/source/blender/editors/object/object_bake_api.cc> |
| 58 | Blender source: uvedit_unwrap_ops.cc | 소스코드 | 2026-09 main | MINIMUM_STRETCH, pack shape_method | <https://raw.githubusercontent.com/blender/blender/main/source/blender/editors/uvedit/uvedit_unwrap_ops.cc> |
| 59 | Blender GPU shader: geometry (pointiness=0.5) | 소스코드 | 2026-09 main | EEVEE에서 Pointiness 미지원 증명 | <https://raw.githubusercontent.com/blender/blender/main/source/blender/gpu/shaders/material/gpu_shader_material_geometry.bsl.hh> |
| 60 | Blender GPU shader: bevel (pass-through) | 소스코드 | 2026-09 main | EEVEE에서 Bevel 미지원 증명 | <https://raw.githubusercontent.com/blender/blender/main/source/blender/gpu/shaders/material/gpu_shader_material_bevel.bsl.hh> |
| 61 | Infinigen table_marble.py | 소스코드 | 2026 | 대리석 노드 수치 | <https://raw.githubusercontent.com/princeton-vl/infinigen/main/src/infinigen/assets/materials/table_marble.py> |
| 62 | Infinigen wood.py | 소스코드 | 2026 | 나무 결 좌표 스트레치 수치 | <https://raw.githubusercontent.com/princeton-vl/infinigen/main/src/infinigen/assets/materials/wood/wood.py> |
| 63 | Infinigen brushed_metal.py | 소스코드 | 2026 | 브러시드 메탈 roughness 변동 | <https://raw.githubusercontent.com/princeton-vl/infinigen/main/src/infinigen/assets/materials/metal/brushed_metal.py> |
| 64 | Infinigen sofa_fabric.py | 소스코드 | 2026 | 패브릭 직조와 sheen 값 | <https://raw.githubusercontent.com/princeton-vl/infinigen/main/src/infinigen/assets/materials/fabric/sofa_fabric.py> |
| 65 | Infinigen edge_wear.py | 소스코드 | 2026 | Bevel 기반 엣지 마모 | <https://raw.githubusercontent.com/princeton-vl/infinigen/main/src/infinigen/assets/materials/wear_tear/edge_wear.py> |
| 66 | Infinigen scratches.py | 소스코드 | 2026 | 긁힘 절차 수치 | <https://raw.githubusercontent.com/princeton-vl/infinigen/main/src/infinigen/assets/materials/wear_tear/scratches.py> |
| 67 | princeton-vl/infinigen | GitHub README | 2026 | 라이선스(BSD-3), node_transpiler | <https://github.com/princeton-vl/infinigen> |
| 68 | EricWang12/PartUV | GitHub README | SIGGRAPH Asia 2025 | AI 메시용 파트 기반 UV | <https://github.com/EricWang12/PartUV> |
| 69 | mrven/Blender-Texel-Density-Checker | GitHub README | 2026 | 텍셀 밀도 도구 | <https://github.com/mrven/Blender-Texel-Density-Checker> |
| 70 | LaXHeXLuX/Trimmer | GitHub README | 2025 | 트림 시트 워크플로 | <https://github.com/LaXHeXLuX/Trimmer> |
| 71 | NVIDIA-Omniverse/usd-content-agents | GitHub README | 2026 | Material/Texture Agent 개요 | <https://github.com/NVIDIA-Omniverse/usd-content-agents> |
| 72 | Material Agent README | 문서 | 2026 | VLM 라이브러리 선택 10단계 | <https://raw.githubusercontent.com/NVIDIA-Omniverse/usd-content-agents/main/apps/material_agent/README.md> |
| 73 | Texture Agent README | 문서 | 2026 | UV 준비 검사와 PBR 생성 | <https://raw.githubusercontent.com/NVIDIA-Omniverse/usd-content-agents/main/apps/texture_agent/README.md> |
| 74 | dcc-mcp 조직 ⚠ | GitHub org | 2026 | 다중 DCC와 에셋 MCP 어댑터 목록 | <https://github.com/dcc-mcp> |
| 75 | dcc-mcp/dcc-asset-ambientcg | GitHub README | 2026-07 | ambientCG MCP 도구 | <https://github.com/dcc-mcp/dcc-asset-ambientcg> |
| 76 | dcc-mcp/dcc-mcp-epic | GitHub README | 2026 | Fab만 지원, Megascans 미지원 확인 | <https://github.com/dcc-mcp/dcc-mcp-epic> |
| 77 | BlenderKit/BlenderKit | GitHub README | 2026 | 라이브러리 규모, MCP 부재 | <https://github.com/BlenderKit/BlenderKit> |
| 78 | Poly-Haven/Public-API | GitHub README | 2026 | API 이용 조건 | <https://github.com/Poly-Haven/Public-API> |
| 79 | KINGWONWOO/Unreal_MCP_Persona | GitHub README(사례) | 2026-02 | Blender 노드→Unreal 비호환 교훈 | <https://github.com/KINGWONWOO/Unreal_MCP_Persona> |
| 80 | visualbruno/3DGenStudio | GitHub README | 2026-09-23 | ComfyUI 기반 생성→UV→텍스처링 오케스트레이터 | <https://github.com/visualbruno/3DGenStudio> |
| 81 | kijai/ComfyUI-Hunyuan3DWrapper | GitHub README | 2025 | xatlas UV, 버텍스 인페인팅 | <https://github.com/kijai/ComfyUI-Hunyuan3DWrapper> |
| 82 | ErikBurdett/blender-art-factory | GitHub README | 2026-09 | '기술 검증 통과 ≠ 보기 좋음' 품질 게이트 원칙 | <https://github.com/ErikBurdett/blender-art-factory> |
| 83 | GitHub issue search: Musgrave removed in Blender 4.1 ⚠ | GitHub 검색(이슈) | 2024-04 | Musgrave 노드 제거로 인한 호환성 문제 증거 | <https://github.com/search?q=Musgrave+removed+4.1+noise+texture&type=issues> |

**⚠ 신뢰도 경고가 붙은 출처**

- <https://github.com/search?q=Musgrave+removed+4.1+noise+texture&type=issues> — GitHub 검색 결과 페이지라 1차 출처가 아니고, 결과도 바뀝니다. Blender 소스(v4.0.0 node_shader_tex_musgrave.cc 존재 → v4.1.0에서 404, versioning_replace_musgrave_texture_node)로 바꿔야 합니다.
- <https://github.com/elithril/blender-kiln> — 스타 13개의 소규모 프로젝트입니다. README 스스로 갤러리 수치가 '스킬 실행 결과가 아니라 스크립트 결과'라고 밝히는데, 조사 결과는 이를 Claude+MCP 사례로 잘못 옮겼습니다. references/uv-materials.md는 angle_limit=66.0을 degree로 넘기는 코드(bpy는 라디안), AO 내보내기에 대한 공식 문서와 다른 설명을 담고 있어 수치를 그대로 인용하기에 부적합합니다.
- <https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-materials/SKILL.md> — 자체 검증만 거친 커뮤니티 스킬입니다. 금속 기준을 '≥0.5 sRGB'로 두어, 흔히 쓰는 PBR 가이드(sRGB 180~255 ≈ linear 0.46 이상)보다 느슨합니다. 연구자는 이를 'linear 0.5'로 바꿔 인용했습니다. 수치는 교차 검증하고 써야 합니다.
- <https://github.com/dcc-mcp> — 스타 0~1개인 어댑터 수십 개가 일괄 생성된 조직입니다. 커뮤니티 검증이 없고, dcc-mcp-epic README에는 Megascans 언급 자체가 없어 '미지원 명시'라는 인용이 원문과 맞지 않습니다.
- <https://github.com/SS-360/materialpilot> — 스타 5개의 0.1.0 preview입니다. README가 'Codex powered by GPT-5.6 was used as the primary engineering collaborator'라고 밝히는 AI 주도 개발 프로젝트로, 독립적인 사용 사례가 없습니다. 참고용으로만 써야 합니다.
- <https://github.com/alphaparkinc/genpark-realtime-neural-3d-mesh-pbr-texture-generator-skill> — 조사 결과에는 없지만 'texture mcp pbr' 검색 상위에 나오는, 과장된 이름의 AI 생성형 'skill' 저장소입니다. 지식 베이스에 섞이지 않도록 주의해야 합니다(SEO 성격).

<a id="07_aaa-rendering-lighting"></a>
## AAA 라이팅·렌더·아트디렉션

주제 원문: AAA 비주얼 품질: 라이팅·렌더링·카메라·아트 디렉션 (AI 에이전트가 MCP로 따를 수 있는 규칙으로 인코딩)

| # | 제목 | 유형 | 날짜 | 왜 유용한가 | URL |
|---|---|---|---|---|---|
| 1 | Bartindigital/blender-hyperrealism-skill (README, SKILL.md, references 01–11) ⚠ | GitHub 저장소 (에이전트 스킬) | 2026-07-31 | 실무자 57명의 튜토리얼을 출처와 함께 수치 규칙으로 정리한, 이 주제에서 가장 밀도 높은 자료입니다. | <https://github.com/Bartindigital/blender-hyperrealism-skill> |
| 2 | hyperrealism skill — 01-lighting.md | GitHub raw | 2026 | 켈빈, 볼류메트릭 밀도, 고보, 필 라이트, False Color 수치. | <https://raw.githubusercontent.com/Bartindigital/blender-hyperrealism-skill/main/references/01-lighting.md> |
| 3 | hyperrealism skill — 07-post-compositing.md | GitHub raw | 2026 | 글레어, CA, 그레인, CDL, AO 합성 수치. | <https://raw.githubusercontent.com/Bartindigital/blender-hyperrealism-skill/main/references/07-post-compositing.md> |
| 4 | hyperrealism skill — 10-mistakes-tools.md | GitHub raw | 2026 | 렌더가 가짜처럼 보이는 원인과 수정법, 추천 도구. | <https://raw.githubusercontent.com/Bartindigital/blender-hyperrealism-skill/main/references/10-mistakes-tools.md> |
| 5 | scenario-labs/skills — scenario-blender-lighting-rendering SKILL.md | GitHub raw (에이전트 스킬) | 2026 (Blender 5.2.1… | 측정형 품질 게이트, AgX 매핑 수치, EEVEE와 Cycles 파이널 설정. | <https://raw.githubusercontent.com/scenario-labs/skills/main/skills/dcc/blender/scenario-blender-lighting-rendering/SKILL.md> |
| 6 | scenario-labs/skills — scenario-blender-expert SKILL.md | GitHub raw | 2026 | 리뷰 루프 규칙과 Blender 5.2 API 함정. | <https://raw.githubusercontent.com/scenario-labs/skills/main/skills/dcc/blender/scenario-blender-expert/SKILL.md> |
| 7 | scenario-labs/skills — hard-surface / texturing-shading SKILL.md | GitHub raw | 2026 | 마이크로 bevel 규칙(최대 치수의 0.5%, 3 seg, Harden Normals, WN 마지막)과 albedo·roughness 감사 수치. | <https://raw.githubusercontent.com/scenario-labs/skills/main/skills/dcc/blender/scenario-blender-hard-surface/SKILL.md> |
| 8 | arjun988/blender-skills | GitHub 저장소 (스킬 팩) | 2026-07-10 | 조명, 카메라, 세트 드레싱, QA, 실측 치수 규칙. | <https://github.com/arjun988/blender-skills> |
| 9 | RobLe3/cc-blender-skill (lighting / rendering SKILL.md, CHANGELOG) | GitHub 저장소 (Claude Code 플러그인) | 2026-05-01 v1.3.0 | 재질 클래스별 3점 조명 비율과 에너지 공식. | <https://github.com/RobLe3/cc-blender-skill> |
| 10 | mcp-for-blender (ahujasid/blender-mcp) README | GitHub 저장소 (MCP) | 2026-09 | 기능, Poly Haven 해상도 권고. | <https://github.com/ahujasid/blender-mcp> |
| 11 | PyPI mcp-for-blender 2.1.0 | 패키지 레지스트리 | 2026-09-25 | 최신 버전과 날짜 확인. | <https://pypi.org/project/mcp-for-blender/> |
| 12 | blender-mcp issue #61: Feature request: teach server to render | GitHub 이슈 | 2026 | 렌더 도구 부재(not planned)와 우회책 확인. | <https://github.com/ahujasid/blender-mcp/issues/61> |
| 13 | Blender OCIO config (main) | 공식 소스 코드 | 2026-09 조회 | 5.x의 AgX, ACES 1.3/2.0, Khronos, HDR 뷰, 색공간 목록. | <https://raw.githubusercontent.com/blender/blender/main/release/datafiles/colormanagement/config.ocio> |
| 14 | Blender Cycles properties.py (main) | 공식 소스 코드 | 2026-09 조회 | Cycles 기본값(샘플, 바운스, 디노이즈, guiding, volume_biased). | <https://raw.githubusercontent.com/blender/blender/main/intern/cycles/blender/addon/properties.py> |
| 15 | Blender properties_render.py (main) | 공식 소스 코드 | 2026-09 조회 | EEVEE 식별자와 패널 속성, 색관리 working_space와 white balance, 레거시 속성 부재 확인. | <https://raw.githubusercontent.com/blender/blender/main/scripts/startup/bl_ui/properties_render.py> |
| 16 | Blender properties_data_light.py (main) | 공식 소스 코드 | 2026-09 조회 | 라이트 켈빈 온도, exposure, jitter 속성. | <https://raw.githubusercontent.com/blender/blender/main/scripts/startup/bl_ui/properties_data_light.py> |
| 17 | Blender compositor Glare node source | 공식 소스 코드 | 2026-09 조회 | Glare 타입(Bloom, Kernel 포함)과 기본값. | <https://raw.githubusercontent.com/blender/blender/main/source/blender/nodes/composite/nodes/node_composite_glare.cc> |
| 18 | Blender GitHub mirror tags | 공식 미러 | 2026-09-14 | 5.2.0(2026-07-13), 5.2.2(2026-09-14) 릴리스 확인. | <https://github.com/blender/blender/tags> |
| 19 | EaryChow/AgX | GitHub (색관리 원저장소) | — | AgX 16.5 stop, looks, Blender 4.0 기본 채택. | <https://github.com/EaryChow/AgX> |
| 20 | KhronosGroup/ToneMapping PBR_Neutral | 표준 문서 | — | 제품 색 재현용 톤매퍼 사양. | <https://github.com/KhronosGroup/ToneMapping/tree/main/PBR_Neutral> |
| 21 | RenderKit/oidn releases | GitHub 릴리스 | v2.5.1 8월 18일 | 최신 디노이저 버전. | <https://github.com/RenderKit/oidn/releases> |
| 22 | ue5-docs-mcp (UE 5.7 문서 Markdown 미러 + MCP) ⚠ | GitHub (공식 문서 미러) | 2026-07-17 | Epic 문서가 막힌 환경에서 MegaLights, Lumen, VSM, Substrate, Path Tracer, 5.7 릴리스 노트를 확인하는 데 썼습니다. | <https://github.com/CharlieCardenasToledo/ue5-docs-mcp> |
| 23 | UE 5.7 — MegaLights doc (mirror) | 공식 문서 미러 | UE 5.7 | 활성화 방법, cvar, 한계. | <https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/megalights-in-unreal-engine.md> |
| 24 | UE 5.7 — Release Notes (mirror) | 공식 문서 미러 | UE 5.7 | MegaLights Beta, Substrate와 PCG Production-Ready, Nanite Foliage Experimental. | <https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/unreal-engine-5-7-release-notes.md> |
| 25 | UE 5.7 — Lumen Technical Details (mirror) | 공식 문서 미러 | UE 5.7 | 벽 10 cm, 모듈 메시, Emissive Light Source, Hit Lighting. | <https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/lumen-technical-details-in-unreal-engine.md> |
| 26 | UE 5.7 — Virtual Shadow Maps (mirror) | 공식 문서 미러 | UE 5.7 | 16k 가상 해상도, SMRT cvar, Source Radius. | <https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/virtual-shadow-maps-in-unreal-engine.md> |
| 27 | UE 5.7 — Path Tracer (mirror) | 공식 문서 미러 | UE 5.7 | 활성화 순서, PPV 설정, 한계. | <https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/path-tracer-in-unreal-engine.md> |
| 28 | EpicGames/unreal-engine-skills-for-claude-code-plugin | GitHub (Epic 공식) | 2026-09 | UE 공식 MCP 연동 플러그인과 사용 지침. | <https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin> |
| 29 | ibrews/ue5-mcp SKILL.md ⚠ | GitHub raw (커뮤니티 스킬) | 2026-09 | Lumen mobility, emissive bloom 임계값, 5.7과 5.8 차이. | <https://raw.githubusercontent.com/ibrews/ue5-mcp/main/SKILL.md> |
| 30 | db-lyon/ue-mcp README | GitHub 저장소 | 2026-09 | UE 5.8+ 공식 도구 830개가 epic_*로 노출된다는 주장. | <https://github.com/db-lyon/ue-mcp> |
| 31 | Tencent-Hunyuan/Hunyuan3D-2.1 README | GitHub 저장소 | 2025-06-13 | RGB 텍스처에서 PBR 파이프라인으로의 전환 설명(생성형 메시에 조명이 구워지는 문제의 맥락). | <https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1> |

**⚠ 신뢰도 경고가 붙은 출처**

- <https://raw.githubusercontent.com/ibrews/ue5-mcp/main/SKILL.md> — 커뮤니티 스킬(스타 39개)이 Epic 공식 문서와 정면으로 모순되는 주장을 '확인됨'처럼 적고 있습니다. 'Lumen GI는 Movable만 반영, Stationary는 기여 0'과 'MovieRenderGraph는 5.8 전용'이 그 예입니다. UE 사실관계의 근거로 쓰면 안 되고, 크래시 패턴이나 API 함정 참고용으로만 쓰는 편이 안전합니다.
- <https://github.com/Bartindigital/blender-hyperrealism-skill> — 커밋 1개, 스타 0개이고, 유튜브 트랜스크립트를 LLM으로 요약해 만든 것으로 보이는 규칙집입니다. 버전이 섞인 수치가 많습니다. 4.3 이하 Glare Mix/Size, Cycles X에서 제거된 Branched Path Tracing, 4.1에서 제거된 Auto Smooth, 'HDRI strength ~1000' 등입니다. 출처가 표기돼 있어 유용하지만 수치는 5.x 소스로 한 번 더 걸러야 합니다.
- <https://github.com/CharlieCardenasToledo/ue5-docs-mcp> — 비공식 스크랩 미러입니다(스타 1개). 문서 본문은 Epic IP이고 개인·교육 목적으로 한정되어 있습니다. 변환 과정에서 표나 기본값이 빠지며, 같은 페이지 안에 버전 상태가 섞여 있습니다(Substrate가 본문은 Production-Ready, 제한사항 절은 Beta). 사실 확인 보조 자료로는 쓸 만하지만 '공식 출처'로 표기하면 안 됩니다.
- <https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-rendering/SKILL.md> — Blender 5.x 대상이라고 하면서 scene.eevee.use_gtao, use_bloom, use_ssr, use_ssr_refraction 코드가 남아 있습니다. 5.x RNA에 없는 속성이라 실행하면 오류가 납니다. 조명 레시피 부분은 신뢰할 만합니다.
- <https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/rendering/SKILL.md> — 'Eevee Next', AO On, Bloom처럼 4.1 이전이나 4.2–4.5 기준 개념이 섞여 있어 5.x 에이전트 규칙으로 바로 쓰기 어렵습니다(커밋 15개).

<a id="08_modeling-objects"></a>
## 오브젝트·가구·조형 모델링

주제 원문: AI로 오브젝트·가구·조형물을 올바른 형태/비율/디테일로 모델링하기 (치수 표준, 모델링 접근법, 부품 분해, 유기 조형, LLM/VLM 형상 프로그램 연구, 실패 모드와 bpy 자동 검사)

| # | 제목 | 유형 | 날짜 | 왜 유용한가 | URL |
|---|---|---|---|---|---|
| 1 | Infinigen GitHub README | GitHub repo | 2026-09 | Infinigen Indoors, Articulated, 2.0 브랜치 구조와 라이선스 | <https://github.com/princeton-vl/infinigen> |
| 2 | Infinigen HelloRoom.md | official docs | 2026-09 | 실내 씬 생성 명령과 오버라이드 | <https://raw.githubusercontent.com/princeton-vl/infinigen/main/docs/source/HelloRoom.md> |
| 3 | Infinigen GeneratingIndividualAssets.md | official docs | 2026-09 | 단일 에셋 생성과 export 명령 | <https://raw.githubusercontent.com/princeton-vl/infinigen/main/docs/source/GeneratingIndividualAssets.md> |
| 4 | Infinigen2.md | official docs | 2026-09 | 2.0 alpha 설치와 생성기 목록 | <https://raw.githubusercontent.com/princeton-vl/infinigen/main/docs/source/Infinigen2.md> |
| 5 | Infinigen CHANGELOG | changelog | 2026-09 | V2 chair, handle 생성기, crease+subsurf 재구성 | <https://raw.githubusercontent.com/princeton-vl/infinigen/main/docs/source/CHANGELOG.md> |
| 6 | Infinigen chair.py (indoors-stable) | source code | 2026-09 확인 | 의자 치수 분포와 부품 구조 | <https://raw.githubusercontent.com/princeton-vl/infinigen/indoors-stable/infinigen/assets/objects/seating/chairs/chair.py> |
| 7 | Infinigen dining_table.py | source code | 2026-09 확인 | 식탁 치수와 다리·스트레처 분포 | <https://raw.githubusercontent.com/princeton-vl/infinigen/indoors-stable/infinigen/assets/objects/tables/dining_table.py> |
| 8 | Infinigen simple_desk.py | source code | 2026-09 확인 | 책상 높이 N(0.73, 0.05) 등 | <https://raw.githubusercontent.com/princeton-vl/infinigen/indoors-stable/infinigen/assets/objects/shelves/simple_desk.py> |
| 9 | Infinigen bedframe.py | source code | 2026-09 확인 | 침대 프레임 치수 분포 | <https://raw.githubusercontent.com/princeton-vl/infinigen/indoors-stable/infinigen/assets/objects/seating/bedframe.py> |
| 10 | Infinigen kitchen_cabinet.py | source code | 2026-09 확인 | 캐비닛 판 두께 등 | <https://raw.githubusercontent.com/princeton-vl/infinigen/indoors-stable/infinigen/assets/objects/shelves/kitchen_cabinet.py> |
| 11 | Infinigen sofa.py | source code | 2026-09 확인 | 소파 파라미터 구조(상대 비율 포함) | <https://raw.githubusercontent.com/princeton-vl/infinigen/indoors-stable/infinigen/assets/objects/seating/sofa.py> |
| 12 | Blender 3D Print Toolbox __init__.py | source code | archived 2025-05 | 검사 기본값 | <https://raw.githubusercontent.com/blender/blender-addons/main/object_print3d_utils/__init__.py> |
| 13 | Blender 3D Print Toolbox mesh_helpers.py | source code | archived 2025-05 | BVHTree overlap 기반 교차 검사 코드 | <https://raw.githubusercontent.com/blender/blender-addons/main/object_print3d_utils/mesh_helpers.py> |
| 14 | Blender 3D Print Toolbox operators.py | source code | archived 2025-05 | non-manifold / degenerate 검사 코드 | <https://raw.githubusercontent.com/blender/blender-addons/main/object_print3d_utils/operators.py> |
| 15 | blender-addons mirror (archived) | GitHub repo | 2025-05-09 archived | 애드온 저장소 보관 상태 | <https://github.com/blender/blender-addons> |
| 16 | Archimesh kitchen / door / stairs maker | source code | archived 2025-05 | 주방·문·계단 기본 치수 | <https://raw.githubusercontent.com/blender/blender-addons/main/archimesh/achm_kitchen_maker.py> |
| 17 | Blender MOD_boolean.cc (main) | source code | 2026-09 | Manifold boolean solver 존재 확인 | <https://raw.githubusercontent.com/blender/blender/main/source/blender/modifiers/intern/MOD_boolean.cc> |
| 18 | FreeCAD ArchStairs.py | source code | 2026-09 | Blondel ratio 62–64 cm | <https://raw.githubusercontent.com/FreeCAD/FreeCAD/main/src/Mod/BIM/ArchStairs.py> |
| 19 | Holodeck prompts.py | source code | 2024 | LLM에게 cm 크기를 명시시키는 프롬프트 형식 | <https://raw.githubusercontent.com/allenai/Holodeck/main/ai2holodeck/generation/prompts.py> |
| 20 | build123d-mcp ⚠ | GitHub repo | 2026-09 | CAD MCP 도구, 설치, 성능 개선 수치 | <https://github.com/pzfreo/build123d-mcp> |
| 21 | build123d-mcp default_prompt.md | prompt | 2026-09 | 결정론적 검사를 시각 검사보다 먼저 하는 규칙 | <https://raw.githubusercontent.com/pzfreo/build123d-mcp/main/default_prompt.md> |
| 22 | build123d README | GitHub repo | 2026-09 | build123d 개요와 요구사항 | <https://raw.githubusercontent.com/gumyr/build123d/dev/README.md> |
| 23 | build123d joints docs | official docs | 2026-09 | 조인트 기반 조립 | <https://github.com/gumyr/build123d/blob/dev/docs/joints.rst> |
| 24 | AgentCAD | GitHub repo | 2026-09 | CAD CLI와 MCP | <https://github.com/jdilla1277/agentcad> |
| 25 | CadQuery | GitHub repo | 2026-09 | CadQuery 개요 | <https://github.com/CadQuery/cadquery> |
| 26 | BOSL2 | GitHub repo | 2026-09 | OpenSCAD attachments와 joiners | <https://github.com/BelfrySCAD/BOSL2> |
| 27 | fogleman/sdf | GitHub repo | 2026-09 | SDF 코드 모델링 | <https://github.com/fogleman/sdf> |
| 28 | MCP for Blender (ahujasid) | GitHub repo | 2026-09 | 주요 Blender MCP, 패키지명 변경 | <https://github.com/ahujasid/mcp-for-blender> |
| 29 | blend-ai | GitHub repo | 2026-09 | mesh 분석 도구를 포함한 MCP | <https://github.com/HoldMyBeer-gg/blend-ai> |
| 30 | blender-game-skills: blender-image-to-3d SKILL.md | agent skill | 2026-09 | IoU·비율 게이트, 단위 규약 | <https://raw.githubusercontent.com/majidmanzarpour/blender-game-skills/main/skills/blender-image-to-3d/SKILL.md> |
| 31 | blender-game-skills validate.py | source code | 2026-09 | 메쉬 검사 임계값과 코드 | <https://raw.githubusercontent.com/majidmanzarpour/blender-game-skills/main/skills/blender-image-to-3d/scripts/validate.py> |
| 32 | blender-game-skills world_gate.py | source code | 2026-09 | 실루엣 IoU와 폭 프로파일 | <https://raw.githubusercontent.com/majidmanzarpour/blender-game-skills/main/skills/blender-image-to-3d/scripts/world_gate.py> |
| 33 | blender-production SKILL.md | agent skill | 2026-09 | 빌드 순서와 defect ledger | <https://raw.githubusercontent.com/per-simmons/blender-production/master/SKILL.md> |
| 34 | blender-production realism.md | agent skill reference | 2026-09 | bevel과 macro / meso / micro 디테일 | <https://raw.githubusercontent.com/per-simmons/blender-production/master/references/realism.md> |
| 35 | unreal-home-wizard SKILL.md | agent skill | 2026-09 | 물리 논리 QA 체크리스트 | <https://raw.githubusercontent.com/amirmushichge/unreal-home-wizard/main/skills/unreal-home-wizard/SKILL.md> |
| 36 | PartNet dataset repo | dataset | 2019 | 부품 계층 | <https://github.com/daerduoCarey/partnet_dataset> |
| 37 | PartNet Chair-hier.txt | dataset | 2019 | 의자 부품 leaf 목록 | <https://raw.githubusercontent.com/daerduoCarey/partnet_dataset/master/stats/after_merging_label_ids/Chair-hier.txt> |
| 38 | ShapeAssembly | research code | 2020 | cuboid + attach 형상 프로그램 | <https://github.com/rkjones4/ShapeAssembly> |
| 39 | LL3M README | research code | 2026-09 확인 | 멀티 에이전트 구조와 서비스 중단 사실 | <https://raw.githubusercontent.com/threedle/ll3m/main/README.md> |
| 40 | BlenderLLM | research code | 2024-12 | CADBench 결과 | <https://github.com/FreedomIntelligence/BlenderLLM> |
| 41 | MeshCoder | research code | 2025-11 | 점군을 부품 코드로 변환 | <https://github.com/InternRobotics/MeshCoder> |
| 42 | CAD-Recode | research code | ICCV 2025 | 점군을 CadQuery 코드로 변환 | <https://github.com/filaPro/cad-recode> |
| 43 | Text2CAD | research code | NeurIPS 2024 | 프롬프트 난이도 수준별 CAD | <https://github.com/SadilKhan/Text2CAD> |
| 44 | CADCodeVerify (CAD_Code_Generation) | research code | ICLR 2025 | VLM 검증 질문 루프 | <https://github.com/Kamel773/CAD_Code_Generation> |
| 45 | CADFusion | research code | ICML 2025 | 시각 피드백 학습 | <https://github.com/microsoft/CADFusion> |
| 46 | LLaMA-Mesh | research code | 2024-11 | 메쉬를 텍스트로 다루는 LLM | <https://github.com/nv-tlabs/LLaMA-Mesh> |
| 47 | MeshLLM | research code | ICCV 2025 | primitive 분해 기반 메쉬 LLM | <https://github.com/Fangkang515/MeshLLM> |
| 48 | ShapeLLM-Omni | research code | NeurIPS 2025 | 네이티브 3D MLLM | <https://github.com/JAMESYJL/ShapeLLM-Omni> |
| 49 | BlenderGym-Open | benchmark | CVPR 2025 | generator-verifier 구조의 유효성 | <https://github.com/richard-guyunqi/BlenderGym-Open> |
| 50 | L3GO repo ⚠ | research code (empty) | 2025 | 부품 단위 조립 에이전트(코드 미공개) | <https://github.com/runopti/L3GO> |
| 51 | CADGenBench | benchmark | 2026 | CAD 생성·편집 평가 지표 | <https://github.com/huggingface/cadgenbench> |
| 52 | cadgenbench-build123d 모델 비교 ⚠ | third-party eval | 2026-07~09 | Opus 5 / GPT-5.6 Sol / Gemini 3.7 Flash 점수 | <https://raw.githubusercontent.com/pzfreo/cadgenbench-build123d/main/GEMINI_OPUS_GPT56_MCP_COMPARISON.md> |
| 53 | PartCrafter | research code | NeurIPS 2025 | 파트 단위 image-to-3D | <https://github.com/wgsxm/PartCrafter> |
| 54 | PartPacker | research code | 2025-06 | 파트 단위 생성 | <https://github.com/NVlabs/PartPacker> |
| 55 | OmniPart | research code | SIGGRAPH Asia 2025 | 파트 인식 생성 | <https://github.com/HKU-MMLab/OmniPart> |
| 56 | Hunyuan3D-Part | research code | 2025-09 | P3-SAM과 X-Part | <https://github.com/Tencent-Hunyuan/Hunyuan3D-Part> |
| 57 | Nova3D | GitHub repo | 2026-08 | 코드 네이티브 파트 생성 | <https://github.com/RareSense/Nova3D> |
| 58 | Sverchok | GitHub repo | 2026-09 | 파라메트릭 노드 | <https://github.com/nortikin/sverchok> |
| 59 | Archipack | GitHub repo | legacy | 건축 요소 애드온 | <https://github.com/s-leger/archipack> |
| 60 | awesome-ai-3d-modeling-robotics ⚠ | curated list | 2026-09 | 2026-09 GPT-6 Astra / Opus 5.5 / Fable 5.1 3D 사례 원문 링크 모음 | <https://github.com/Frank-ZY-Dou/awesome-ai-3d-modeling-robotics> |
| 61 | kitchen-twin ⚠ | case study repo | 2026-09 | Blender DSL과 독립 검증 사례 | <https://github.com/Frank-ZY-Dou/kitchen-twin> |
| 62 | blender-production repo ⚠ | case study repo | 2026-09 | Fallingwater 재현 skill | <https://github.com/per-simmons/blender-production> |
| 63 | unreal-home-wizard | case study repo | 2026-09 | 사진에서 UE 프로젝트로, 물리 QA | <https://github.com/amirmushichge/unreal-home-wizard> |

**⚠ 신뢰도 경고가 붙은 출처**

- <https://raw.githubusercontent.com/pzfreo/cadgenbench-build123d/main/GEMINI_OPUS_GPT56_MCP_COMPARISON.md> — build123d-mcp 저자(pzfreo)가 자기 도구로 한 비교라 독립 평가가 아니다. 모델마다 MCP 버전, 하네스, 실행 시기가 다르고, Opus 값은 'best' 제출(합성 run)이며, 토큰·비용 비교도 문서 스스로 directional이라고 밝힌다. 인용할 때 '단일 제3자'가 아니라 '도구 저자 자체 평가'로 표기해야 한다.
- <https://github.com/pzfreo/build123d-mcp> — 0.360→0.457 개선 수치는 도구 저자의 자기 보고이고 모델명을 밝히지 않았다. 리더보드 보고서로 교차 확인해야 한다.
- <https://github.com/Frank-ZY-Dou/awesome-ai-3d-modeling-robotics> — kitchen-twin 저자가 운영하는 2차 큐레이션이라 자기 사례가 포함되어 있고 GPT-6 Astra 중심이다. X·LinkedIn 원문을 인용 요약한 것이므로 수치(3,295개 오브젝트, 54시간 등)는 원 게시물 확인 전까지 '저자 주장'으로 표기해야 한다.
- <https://github.com/Frank-ZY-Dou/kitchen-twin> — 결과물만 공개된 저장소이고 파이프라인이 비공개라 방법론을 재현할 수 없다. findings의 'DSL(parts / joints / dimensions)' 구조는 원문에 없는 각색이다.
- <https://github.com/majidmanzarpour/blender-game-skills> — 커밋 1개(2026-09-24, Claude 공동 작성), 90★로 커뮤니티 검증 이력이 없다. 규칙 자체는 합리적이지만 '검증된 표준'이 아니라 참고 사례로 다뤄야 한다.
- <https://github.com/per-simmons/blender-production> — 커밋 1개, 0★, Claude 공동 작성이다. 내용은 원문과 일치하지만 성숙도가 낮다.
- <https://github.com/runopti/L3GO> — LICENSE 파일만 있는 빈 placeholder 저장소(커밋 1개)다. 방법 설명의 출처로 인용하면 안 되고 논문(NAACL 2025 demo)을 직접 인용해야 한다.
- <https://x.com/tomkrcha/status/2095756085890310311> — X 게시물을 직접 열람할 수 없어 큐레이션 리스트를 통해서만 확인했다(uncle_render, superalesha 링크도 같다). 인용한 SEO 스팸형 출처는 발견되지 않았고 인용 출처는 대부분 GitHub 1차 자료다.

<a id="09_scene-layout"></a>
## 배치·레이아웃

주제 원문: Object placement and scene layout: AI(LLM/VLM)와 MCP로 방·환경의 오브젝트 배치와 레이아웃을 그럴듯하게 만드는 방법 (연구, 도구, 실무 기법, 수치 규칙, 사례)

| # | 제목 | 유형 | 날짜 | 왜 유용한가 | URL |
|---|---|---|---|---|---|
| 1 | allenai/Holodeck GitHub | GitHub repo | 2023-12~ | 제약 기반 실내 레이아웃의 대표 오픈소스 | <https://github.com/allenai/Holodeck> |
| 2 | Holodeck prompts.py (object/wall constraints prompt) | 소스 코드(프롬프트) |  | 제약 어휘와 수치 정의(near 50-150 cm 등), 배치 지침 원문 | <https://raw.githubusercontent.com/allenai/Holodeck/main/ai2holodeck/generation/prompts.py> |
| 3 | Holodeck floor_objects.py (DFS/MILP solver) | 소스 코드 |  | solver 가중치, 회전 4방향, Shapely 충돌 검사 | <https://raw.githubusercontent.com/allenai/Holodeck/main/ai2holodeck/generation/floor_objects.py> |
| 4 | Holodeck issue #92 rotation doubts | GitHub issue | 2025-09-03 | 에셋 정면 정렬 실패 사례 | <https://github.com/allenai/Holodeck/issues/92> |
| 5 | sunfanyunn/LayoutVLM GitHub | GitHub repo | CVPR 2025 | VLM + 미분 최적화 레이아웃 | <https://github.com/sunfanyunn/LayoutVLM> |
| 6 | LayoutVLM base_prompt.py | 소스 코드(프롬프트) |  | 제약 함수 7종, 좌표·회전 규약 | <https://raw.githubusercontent.com/sunfanyunn/LayoutVLM/main/prompts/layoutvlm/base_prompt.py> |
| 7 | LayoutVLM grad_solver.py | 소스 코드 |  | Adam lr 0.01, 400 iter, IoU loss ×1000 등 solver 세부 | <https://raw.githubusercontent.com/sunfanyunn/LayoutVLM/main/src/layoutvlm/grad_solver.py> |
| 8 | LayoutVLM layoutvlm.py | 소스 코드 |  | 그룹핑, 시각 마크 렌더, self-consistency 필터 | <https://raw.githubusercontent.com/sunfanyunn/LayoutVLM/main/src/layoutvlm/layoutvlm.py> |
| 9 | LayoutVLM issue #9 mesh normalization | GitHub issue | 2025-07-13 | 스케일·회전 정규화 실패 사례 | <https://github.com/sunfanyunn/LayoutVLM/issues/9> |
| 10 | princeton-vl/infinigen GitHub | GitHub repo |  | Blender 네이티브 절차적 실내 생성 | <https://github.com/princeton-vl/infinigen> |
| 11 | Infinigen HelloRoom.md ⚠ | 공식 문서 |  | 실내 생성 명령, gin 옵션, 제약 제한 옵션 | <https://raw.githubusercontent.com/princeton-vl/infinigen/main/docs/source/HelloRoom.md> |
| 12 | Infinigen CHANGELOG.md | 공식 문서 |  | v1.4.0 Indoors부터 v2.0.0a2까지의 버전 이력 | <https://raw.githubusercontent.com/princeton-vl/infinigen/main/docs/source/CHANGELOG.md> |
| 13 | Infinigen2.md | 공식 문서 |  | 2.0 알파 상태, uv/Python 3.11 | <https://raw.githubusercontent.com/princeton-vl/infinigen/main/docs/source/Infinigen2.md> |
| 14 | Infinigen home.py constraints (v1.16.0) | 소스 코드 |  | constraint language 실례와 수치(소파–TV 2-3 m 등) | <https://raw.githubusercontent.com/princeton-vl/infinigen/v1.16.0/infinigen_examples/constraints/home.py> |
| 15 | Infinigen annealing.py (v1.16.0) | 소스 코드 |  | simulated annealing solver 구조 | <https://raw.githubusercontent.com/princeton-vl/infinigen/v1.16.0/infinigen/core/constraints/example_solver/annealing.py> |
| 16 | Infinigen ExportingToExternalFileFormats.md | 공식 문서 |  | USDC 내보내기 한계 | <https://raw.githubusercontent.com/princeton-vl/infinigen/main/docs/source/ExportingToExternalFileFormats.md> |
| 17 | atcelen/IDesign GitHub + agents.py/schemas.py/place_in_blender.py | GitHub repo | ECCV 2024 | 멀티에이전트 설계와 Blender 배치 코드 | <https://github.com/atcelen/IDesign> |
| 18 | IDesign place_in_blender.py | 소스 코드 |  | Blender 배치 절차와 +π 보정 quirk | <https://raw.githubusercontent.com/atcelen/IDesign/main/place_in_blender.py> |
| 19 | weixi-feng/LayoutGPT | GitHub repo | NeurIPS 2023 | in-context 레이아웃 생성 | <https://github.com/weixi-feng/LayoutGPT> |
| 20 | Scene-Weaver/SceneWeaver | GitHub repo | NeurIPS 2025 | reflect 에이전트와 Blender 소켓 모드 | <https://github.com/Scene-Weaver/SceneWeaver> |
| 21 | nepfaff/scenesmith | GitHub repo | ICML 2026 | 에이전트 장면 생성의 최신 레퍼런스 | <https://github.com/nepfaff/scenesmith> |
| 22 | SceneSmith furniture designer_agent.yaml | 프롬프트 |  | 클리어런스 수치, snap/facing 규칙, 검증 절차 | <https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/prompts/data/furniture_agent/designer_agent.yaml> |
| 23 | SceneSmith stateful_critic_agent.yaml | 프롬프트 |  | 비평 루브릭 6항목과 CHAOS DETECTION | <https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/prompts/data/furniture_agent/stateful_critic_agent.yaml> |
| 24 | SceneSmith base_furniture_agent.yaml | 설정 파일 |  | gpt-5.2, 라운드, 임계값, 렌더 해상도, 노이즈 수치 | <https://raw.githubusercontent.com/nepfaff/scenesmith/main/configurations/furniture_agent/base_furniture_agent.yaml> |
| 25 | SceneSmith base_manipuland_agent.yaml | 설정 파일 |  | 소품 물리 안착(5 s, dt 0.001), support surface 파라미터 | <https://raw.githubusercontent.com/nepfaff/scenesmith/main/configurations/manipuland_agent/base_manipuland_agent.yaml> |
| 26 | SceneSmith snapping_helpers.py | 소스 코드 |  | 스냅 알고리즘(0.01 m 스텝, 충돌 시 후퇴) | <https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/furniture_agents/tools/snapping_helpers.py> |
| 27 | SceneSmith wall designer_agent.yaml | 프롬프트 |  | 벽걸이 높이 규칙 | <https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/prompts/data/wall_agent/designer_agent.yaml> |
| 28 | NVlabs/sage | GitHub repo | CVPR 2026 | MCP 기반 장면 생성 서버 | <https://github.com/NVlabs/sage> |
| 29 | SAGE server/layout.py | 소스 코드 |  | FastMCP 레이아웃 툴 정의 | <https://raw.githubusercontent.com/NVlabs/sage/main/server/layout.py> |
| 30 | SAGE object_placement_planner.py | 소스 코드 |  | DFS solver 파라미터, 동선·점유율 규칙, 모델 호출 | <https://raw.githubusercontent.com/NVlabs/sage/main/server/objects/object_placement_planner.py> |
| 31 | hzxie/Awesome-3D-Scene-Generation ⚠ | 큐레이션 리스트 | 2026-09 확인 | 2025-2026 후속 연구 목록과 학회 정보 | <https://github.com/hzxie/Awesome-3D-Scene-Generation> |
| 32 | 3dlg-hcvc/SceneEval | GitHub repo | WACV 2026 | 레이아웃 품질 평가 지표 10종 | <https://github.com/3dlg-hcvc/SceneEval> |
| 33 | 3dlg-hcvc/hsm | GitHub repo | 3DV 2026 | 계층적 모티프 배치, 비용과 시간 | <https://github.com/3dlg-hcvc/hsm> |
| 34 | 3dlg-hcvc/smc (SceneMotifCoder) | GitHub repo | 3DV 2025 | 예시 기반 배치 프로그램 학습, Blender 예시 작성 | <https://github.com/3dlg-hcvc/smc> |
| 35 | Runder-sun/SceneReVis | GitHub repo | 2026-02 | 렌더 피드백 RL 사례 | <https://github.com/Runder-sun/SceneReVis> |
| 36 | 3DSceneAgent/Vibe3DScene | GitHub repo | 2026 | MCP + Blender-MCP 장면 에이전트 | <https://github.com/3DSceneAgent/Vibe3DScene> |
| 37 | GitHub topic: blender-mcp | GitHub topic 목록 | 2026-09 | Blender MCP 생태계 저장소 목록 | <https://github.com/topics/blender-mcp> |
| 38 | ahujasid/blender-mcp (mcp-for-blender) | GitHub repo | 2026-09 | 대표 Blender MCP와 사용상 한계 | <https://github.com/ahujasid/blender-mcp> |
| 39 | Blender source: mathutils_bvhtree.cc | Blender 소스(docstring) |  | BVHTree API 시그니처 | <https://raw.githubusercontent.com/blender/blender/main/source/blender/python/mathutils/mathutils_bvhtree.cc> |
| 40 | Blender source: rna_scene_api.cc | Blender 소스 |  | Scene.ray_cast 정의 | <https://raw.githubusercontent.com/blender/blender/main/source/blender/makesrna/intern/rna_scene_api.cc> |
| 41 | Blender source: bl_operators/rigidbody.py | Blender 소스 |  | bake_to_keyframes 연산자 | <https://raw.githubusercontent.com/blender/blender/main/scripts/startup/bl_operators/rigidbody.py> |
| 42 | Blender source: node_geo_distribute_points_on_faces.cc | Blender 소스 |  | Poisson Disk scatter 입력 소켓 | <https://raw.githubusercontent.com/blender/blender/main/source/blender/nodes/geometry/nodes/node_geo_distribute_points_on_faces.cc> |
| 43 | glTF 2.0 Specification | 공식 스펙 |  | 정면 +Z, +Y up, 단위 m | <https://raw.githubusercontent.com/KhronosGroup/glTF/main/specification/2.0/Specification.adoc> |
| 44 | arjun988/blender-skills set-dressing SKILL.md ⚠ | 에이전트 스킬 문서 |  | 세트 드레싱 밀도 구역과 스토리 클러스터 규칙 | <https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/set-dressing/SKILL.md> |
| 45 | HoldMyBeer-gg/blend-ai ⚠ | GitHub repo |  | snap, 물리 툴을 가진 Blender MCP | <https://github.com/HoldMyBeer-gg/blend-ai> |
| 46 | richard-guyunqi/BlenderGym-Open | GitHub repo | CVPR 2025 | VLM의 Blender placement 편집 벤치마크 | <https://github.com/richard-guyunqi/BlenderGym-Open> |
| 47 | PhyScene / DiffuScene / ATISS repos | GitHub repo | CVPR 2024 | 물리 guidance diffusion 레이아웃 | <https://github.com/PhyScene/PhyScene> |
| 48 | GradientSpaces/respace | GitHub repo | ICLR 2026 | 텍스트 기반 씬 편집(add/remove/swap) | <https://github.com/GradientSpaces/respace> |
| 49 | YxuanAr/Code-as-Room | GitHub repo | 2026 | top-down 이미지 → Blender 코드 | <https://github.com/YxuanAr/Code-as-Room> |
| 50 | 3dlg-hcvc/hssd | GitHub repo |  | HSSD 규모(211 씬, 18,656 객체) | <https://github.com/3dlg-hcvc/hssd> |

**⚠ 신뢰도 경고가 붙은 출처**

- <https://github.com/hzxie/Awesome-3D-Scene-Generation> — 2차 큐레이션 목록이다. SAGE의 'CVPR 2026' 같은 학회 표기가 이 목록에만 있고 원 저장소나 README에는 없다. 연구 흐름을 찾는 포인터로는 유용하지만, 학회와 수상 표기는 1차 출처(논문, 학회 페이지, 저장소)로 확인하기 전까지 '목록상 표기'로 한정할 것.
- <https://github.com/InternRobotics/MesaTask> — README 본문('Apache License')과 LICENSE 파일(MIT)이 서로 모순된다. 라이선스는 LICENSE 파일을 우선으로 삼을 것.
- <https://github.com/HoldMyBeer-gg/blend-ai> — 저장소 About('175 tools')과 README('186 tools across 27 modules')가 서로 달라 자기 모순이다. 툴 수는 버전마다 바뀌므로 KB에는 버전과 날짜를 함께 적을 것.
- <https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/set-dressing/SKILL.md> — 개인 프로젝트의 짧은 스킬 문서(약 2 KB)로, 수치 근거나 검증 없이 일반론만 담고 있다. SEO 스팸은 아니지만 '규칙'의 권위 있는 출처로 쓰기에는 부적절하다.
- <https://github.com/ROUJINN/SceneAssistant> — 라이선스가 없고 커밋은 3개다. 기본 VLM 호출이 'zhizengzeng' 제3자 API 중계 플랫폼을 거쳐 재현성과 데이터 보안이 불확실하다. 정량 결과도 미확인이다.
- <https://raw.githubusercontent.com/princeton-vl/infinigen/main/docs/source/HelloRoom.md> — main(v2.0 알파) 브랜치에 있지만 v1 전용 명령(infinigen_examples.generate_indoors)을 안내한다. 그런데 해당 모듈은 main에서 제거됐다(404). 문서와 코드가 불일치하므로 v1.16.0 태그의 문서를 인용할 것.

<a id="10_agent-workflow"></a>
## 에이전트 워크플로·프롬프팅

주제 원문: AI+MCP 3D 제작을 위한 에이전트 워크플로우 & 프롬프팅 노하우 (2026-09-26 기준): 시각 피드백 루프, 단계 분해, 결정적 bpy 스크립트, 버전·네이밍·단위 규약, API 버전 함정과 문서 주입, Claude Code(CLAUDE.md/Skills/Subagent/Hooks//goal)·Codex·Gemini 동등 기능, 컨텍스트/비용, 보안, 멀티 MCP 조합

| # | 제목 | 유형 | 날짜 | 왜 유용한가 | URL |
|---|---|---|---|---|---|
| 1 | ahujasid/blender-mcp (MCP for Blender) GitHub README | GitHub README (primary) | 2026-09-25 업데이트 | 설치 명령(Claude Code, Codex), safe mode, 텔레메트리, 제한 사항, 예시 프롬프트 | <https://github.com/ahujasid/blender-mcp> |
| 2 | mcp-for-blender addon.py (raw) | 소스 코드 (primary) | 2026-09 | get_scene_info 10개 제한, 스크린샷 max_size 기본값, exec에 타임아웃이 없다는 점 확인 | <https://raw.githubusercontent.com/ahujasid/blender-mcp/main/addon.py> |
| 3 | mcp-for-blender server.py (raw) | 소스 코드 (primary) | 2026-09 | asset_creation_strategy 프롬프트(스크린샷 전후 확인, trajectory feedback), 툴 목록, bpy_api_lookup / describe_node_type | <https://raw.githubusercontent.com/ahujasid/blender-mcp/main/src/blender_mcp/server.py> |
| 4 | PyPI mcp-for-blender | 패키지 레지스트리 | 2.1.0 = 2026-09-25 | 최신 버전과 릴리스 날짜 | <https://pypi.org/project/mcp-for-blender/> |
| 5 | Issue #347: tool-schema context cost 5,462 → 6,928 tokens | GitHub issue | 2026-09-05 | MCP 툴 스키마 토큰 비용 실측 | <https://github.com/ahujasid/blender-mcp/issues/347> |
| 6 | Claude connectors: Blender (Made by Blender Lab) | 공식 디렉토리 페이지 | 2026-04 등록, v1.0.1 | 공식 Blender connector의 존재, 제작 주체, 기능 요약 | <https://claude.com/connectors/blender> |
| 7 | Anthropic: Claude for Creative Work | 공식 발표 | 2026-04-28 | Blender 등 크리에이티브 커넥터 8종 발표, Blender Python API 개발 기부 | <https://www.anthropic.com/news/claude-for-creative-work> |
| 8 | RobLe3/cc-blender-skill | GitHub (스킬팩) | v1.3.0 (2026) | Claude Code용 Blender 스킬 30개, 검증 방식, 스스로 밝힌 한계 | <https://github.com/RobLe3/cc-blender-skill> |
| 9 | cc-blender-skill text-to-blender SKILL.md | 스킬 원문 | 2026 | fresh namespace 규칙, 네이밍, 11단계 조립 순서, 5.x 함정, 보고 형식 | <https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/text-to-blender/SKILL.md> |
| 10 | cc-blender-skill blender-pro-workflow SKILL.md | 스킬 원문 | 2026 | 11단계 프로 워크플로우와 비평 프로토콜 | <https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/blender-pro-workflow/SKILL.md> |
| 11 | cc-blender-skill blender-version-compat.md ⚠ | 스킬 레퍼런스 | 2026 | EEVEE 이름, action layers, use_auto_smooth, BSDF 입력 관련 버전 함정 | <https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/text-to-blender/references/blender-version-compat.md> |
| 12 | cc-blender-skill common-object-dimensions.md | 스킬 레퍼런스 | 2026 | 가구와 소품의 실측 치수표 | <https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/text-to-blender/references/common-object-dimensions.md> |
| 13 | cc-blender-skill reference-analysis-validator SKILL.md | 스킬 원문 | 2026 | 레퍼런스 비교 수치 기준(IoU, bbox 드리프트) | <https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/reference-analysis-validator/SKILL.md> |
| 14 | elithril/blender-kiln SKILL.md (Iron Rules) | 스킬 원문 | 2026-08-27 | Iron Rules 25개, export 체크리스트 8항목, 네이밍 | <https://raw.githubusercontent.com/elithril/blender-kiln/main/SKILL.md> |
| 15 | arjun988/blender-skills | GitHub (스킬팩) | 2026-07-10 | 94개 스킬, 멀티 플랫폼, qa-review, set-dressing | <https://github.com/arjun988/blender-skills> |
| 16 | arjun988 qa-review SKILL.md | 스킬 원문 | 2026 | QA 뷰 구성, 심각도 분류, SHIP 판정 형식 | <https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/qa-review/SKILL.md> |
| 17 | Gaius114 blender-space SKILL.md ⚠ | 스킬 원문 | 2026 | world-space 배치 수학 | <https://raw.githubusercontent.com/Gaius114/blender-claude-mcp/main/skill/blender-space/SKILL.md> |
| 18 | Gaius114 blender-research SKILL.md | 스킬 원문 | 2026 | spec_sheet 생성, sRGB → linear 변환, 러프니스 기준 | <https://raw.githubusercontent.com/Gaius114/blender-claude-mcp/main/skill/blender-research/SKILL.md> |
| 19 | newo-ether/blender-mcp skill SKILL.md | 스킬 원문 | 2026 | 구조화 툴 우선 원칙, 트랜잭셔널 노드 패치, 완료 보고 형식 | <https://raw.githubusercontent.com/newo-ether/blender-mcp/main/skills/blender-mcp/SKILL.md> |
| 20 | blend-ai workflows.py (auto_critique_workflow) | 소스 코드/프롬프트 | 2026-09 | 스크린샷 시점과 토큰 예산 규칙, 스케일 기준값 | <https://raw.githubusercontent.com/HoldMyBeer-gg/blend-ai/main/src/blend_ai/prompts/workflows.py> |
| 21 | hideki711014/roo-blendermcp-jp-rules README | GitHub README | 2026-05-14 | 현지화 UI 노드 이름 문제, 소형 모델 규칙 설계, 실패 패턴 | <https://raw.githubusercontent.com/hideki711014/roo-blendermcp-jp-rules/main/README.md> |
| 22 | EpicGames/unreal-engine-skills-for-claude-code-plugin | 공식 GitHub (Epic) | 2026 | Unreal MCP 연결 방법과 안전 규칙 | <https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin> |
| 23 | Epic unreal-mcp SKILL.md | 공식 스킬 원문 | 2026 | toolset 탐색 순서와 운영 규칙 | <https://raw.githubusercontent.com/EpicGames/unreal-engine-skills-for-claude-code-plugin/main/skills/unreal-mcp/SKILL.md> |
| 24 | Claude Code docs: Skills | 공식 문서 | 2026-09 | SKILL.md 필드, 스킬 위치, 크기 권장, context: fork | <https://code.claude.com/docs/en/skills> |
| 25 | Claude Code docs: Subagents | 공식 문서 | 2026-09 | 비평가 에이전트 정의 방법 | <https://code.claude.com/docs/en/sub-agents> |
| 26 | Claude Code docs: Hooks | 공식 문서 | 2026-09 | MCP 툴 matcher, 차단 방식, additionalContext | <https://code.claude.com/docs/en/hooks> |
| 27 | Claude Code docs: /goal | 공식 문서 | 2026-09 | 완료 조건 작성법과 평가 방식 | <https://code.claude.com/docs/en/goal> |
| 28 | Claude Code docs: MCP | 공식 문서 | 2026-09 | 출력 토큰 한도, 타임아웃, 이미지 처리, 보안 | <https://code.claude.com/docs/en/mcp> |
| 29 | Claude Code docs: Best practices | 공식 문서 | 2026-09 | 검증 수단 제공, CLAUDE.md 작성, 적대적 리뷰, 체크포인트의 한계 | <https://code.claude.com/docs/en/best-practices> |
| 30 | Claude Code docs: Costs | 공식 문서 | 2026-09 | 평균 비용, 토큰 절감 전략 | <https://code.claude.com/docs/en/costs> |
| 31 | Claude Code docs: Security | 공식 문서 | 2026-09 | 프롬프트 인젝션 대응, MCP 신뢰 모델 | <https://code.claude.com/docs/en/security> |
| 32 | Claude API docs: Vision | 공식 문서 | 2026-09 | 이미지 토큰 공식, high-res tier, 이미지 우선 배치 팁 | <https://platform.claude.com/docs/en/build-with-claude/vision> |
| 33 | Claude API docs: Pricing | 공식 문서 | 2026-09 | Opus 5.5, Sonnet 5, Fable 5.1 단가와 캐시 배수 | <https://platform.claude.com/docs/en/about-claude/pricing> |
| 34 | Claude API docs: Models overview | 공식 문서 | 2026-09 | 모델 ID, 컨텍스트 창, 기본 effort | <https://platform.claude.com/docs/en/about-claude/models/overview> |
| 35 | Anthropic Engineering: Code execution with MCP | 공식 엔지니어링 블로그 | 2025-11-04 | 툴 호출 대신 코드 실행 시 토큰 98.7% 절감 근거 | <https://www.anthropic.com/engineering/code-execution-with-mcp> |
| 36 | Anthropic Engineering: Writing effective tools for agents | 공식 엔지니어링 블로그 | 2025-09-11 | 툴 통합, 네임스페이스, 응답 토큰 효율 | <https://www.anthropic.com/engineering/writing-tools-for-agents> |
| 37 | upstash/context7 | GitHub README | 2026 | 문서 주입 MCP 설정과 사용법 | <https://github.com/upstash/context7> |
| 38 | nutti/fake-bpy-module | GitHub README | 5.2까지 지원 | 버전별 bpy 스텁 | <https://github.com/nutti/fake-bpy-module> |
| 39 | Gemini CLI docs: MCP server | 공식 문서 (GitHub) | 2026 | mcpServers 설정, includeTools, 이미지 결과 | <https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md> |
| 40 | Gemini CLI docs: GEMINI.md | 공식 문서 (GitHub) | 2026 | 컨텍스트 파일 계층과 AGENTS.md 지정 | <https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md> |
| 41 | CheshireJCat/create-3d-model-skill README | GitHub README | 2026-07-31 | Codex 스킬 경로와 $skill 프롬프트 예시 | <https://raw.githubusercontent.com/CheshireJCat/create-3d-model-skill/main/README.md> |
| 42 | GitHub topic: blender-mcp | GitHub 목록 | 2026-09-26 조회 | 생태계 저장소 목록과 최신 업데이트 날짜 | <https://github.com/topics/blender-mcp> |
| 43 | MAX-786/claude-3d-harness | GitHub README | 2026-09-21 | 스킬 라이브러리 통합, 품질 프로필 | <https://github.com/MAX-786/claude-3d-harness> |
| 44 | Bniya-cn/blender-design-master ⚠ | GitHub README | 2026-08-25 | 비평가 에이전트와 점수 게이트 | <https://github.com/Bniya-cn/blender-design-master> |
| 45 | ellmos-ai/ellmos-blender-use-mcp ⚠ | GitHub README | 2026-09-26 | headless QA와 CI 게이트 | <https://github.com/ellmos-ai/ellmos-blender-use-mcp> |
| 46 | bsantanna/roblox-flex-with-friends | GitHub (사례) | 2026-07-03 | 자율 개발 과정의 공간 검증 교훈 | <https://github.com/bsantanna/roblox-flex-with-friends> |

**⚠ 신뢰도 경고가 붙은 출처**

- <https://raw.githubusercontent.com/RobLe3/cc-blender-skill/main/plugin/skills/text-to-blender/references/blender-version-compat.md> — use_auto_smooth가 '4.x에 존재하고 5.x에서 제거'됐다고 적었는데 사실과 다르다. 실제로는 4.1에서 제거됐다(fake-bpy-module 4.0/4.1 스텁으로 확인). 버전 함정 표의 근거로 쓸 때는 1차 API로 교차 확인해야 한다.
- <https://raw.githubusercontent.com/Gaius114/blender-claude-mcp/main/skill/blender-space/SKILL.md> — 'dimensions는 scale=(1,1,1)일 때만 동작'이라는 설명이 틀렸다. dimensions는 스케일을 반영하고, 문제는 회전(로컬 축)이다. 문서가 이탈리아어라 오해가 더 커질 수 있다.
- <https://github.com/ThanhNguyxnOrg/blendops> — 3 stars, Draft v0인 초기 저장소다. ahujasid 스타 수를 '21K+'로 적어 정보가 오래됐다. 'Blender Lab MCP는 5.1+ 필요'의 유일한 출처인데 1차 근거가 없다.
- <https://github.com/ellmos-ai/ellmos-blender-use-mcp> — 2 stars 저장소인데 README가 '48h Security Response SLA', 'Enterprise security teams' 같은 AI 생성으로 보이는 마케팅 문구로 가득하다. 연구자는 수치(15분, KB)도 잘못 옮겼다. 채택 전에 실제 동작을 검증해야 한다.
- <https://github.com/SandeshBhat15/blender-mcp-antigravity-setup-guide> — 비공식 개인 가이드다. 옛 패키지명 `blender-mcp`에 fastmcp/mcp[cli]를 강제 주입하는 우회책을 쓰고, Windows 경로(C:\Users\...\.gemini\config\mcp_config.json)만 제시한다. Antigravity 공식 문서로 교차 확인되지 않았다.
- <https://github.com/Bniya-cn/blender-design-master> — 라이선스 미선언(재사용 권리 불명확), 1 star, Claude Code와 Cursor 경로는 설계만 있고 미검증이며, Codex 테스트는 Final Gate 7.4로 실패했다. '레퍼런스 설계'로만 인용해야 한다.

<a id="11_case-studies"></a>
## 사례 연구

주제 원문: AI+MCP(및 유사 에이전트 도구 사용) 3D 제작 사례 연구·쇼케이스 모음 (2025-03 BlenderMCP 공개 ~ 2026-09 GPT-6 Astra / Claude Fable 5.1 / Opus 5.5 시기)

| # | 제목 | 유형 | 날짜 | 왜 유용한가 | URL |
|---|---|---|---|---|---|
| 1 | ahujasid/blender-mcp (mcp-for-blender) README | GitHub README | 2026-09 확인 | 원조 BlenderMCP의 데모, 통합 서비스, 한계(작은 단계로 나누기, 저장 경고) | <https://github.com/ahujasid/blender-mcp> |
| 2 | per-simmons/unreal-agent-harness: AGENTIC-GAMEDEV-GUIDE.md | GitHub 문서(1차 제작 기록) | 2026-06-18~ | Claude와 UE 5.8 공식 Unreal MCP 설정 함정, 5가지 빌드 방식 비교, Cesium과 조명 수치 | <https://raw.githubusercontent.com/per-simmons/unreal-agent-harness/master/AGENTIC-GAMEDEV-GUIDE.md> |
| 3 | per-simmons/unreal-agent-harness: BUILD-LOG.md | GitHub 빌드 로그 | 2026-06-19~20 | 크래시와 스케일 오류, 그 수정 내역 | <https://raw.githubusercontent.com/per-simmons/unreal-agent-harness/master/BUILD-LOG.md> |
| 4 | Simon Willison TIL: Using Blender with coding agents on macOS | 작성자 블로그(TIL) 원문 | 2026-09-05 | GPT-6 Astra와 headless Blender의 최소 워크플로, 반복별 소요 시간, 스킬 생성 | <https://github.com/simonw/til/blob/main/llms/blender-coding-agents-macos.md> |
| 5 | simonw/gpt-6-astra-blender-pelican-bicycle (codex-transcript.md 포함) | GitHub 저장소 | 2026-09-05 | Codex 실행 기록 원본 | <https://github.com/simonw/gpt-6-astra-blender-pelican-bicycle> |
| 6 | PhiloLabs/fable51-worlds README | GitHub README | 2026-09 | Fable 5.1 에이전트 스웜 파이프라인과 Astra 비교 영상 | <https://github.com/PhiloLabs/fable51-worlds> |
| 7 | fable51-worlds Union Square FINAL_QA_REPORT.md | QA 리포트 | 2026-09-02 | 리뷰어 점수(재질 6/10 등)와 구체적 결함 목록. AAA와의 격차를 보여 주는 증거 | <https://raw.githubusercontent.com/PhiloLabs/fable51-worlds/main/union-square-sf/FINAL_QA_REPORT.md> |
| 8 | VizuaraAI/fable-visual-learning-pipeline README | GitHub README/튜토리얼 | 2026-09 | 품질 6항목 바, 렌더 설정과 비용·시간 수치, 함정 | <https://github.com/VizuaraAI/fable-visual-learning-pipeline> |
| 9 | Nipale-ai/fable-5-1-one-prompt-game | GitHub README | 2026-09-01 | 24분, $9.90, 토큰, 자기 검증 루프 수치 | <https://github.com/Nipale-ai/fable-5-1-one-prompt-game> |
| 10 | az9713/gpt-6-astra-tennis-game (Robo Open) | GitHub README + 개발 여정 문서 | 2026-09-05~ | Unity, Blender, Meshy 파이프라인의 실패 15건과 비용·시간 | <https://github.com/az9713/gpt-6-astra-tennis-game> |
| 11 | teshnizi2/astra-fable-3d-iris | GitHub 비교 연구 | 2026-09-08 | 사전 등록된 동일 프롬프트 비교와 기계적 결함 분석 | <https://github.com/teshnizi2/astra-fable-3d-iris> |
| 12 | hahaliu1029/house-3d | GitHub README | 2026-09-08 | 인테리어 4개 스타일에 대한 Astra와 Fable 비교 | <https://github.com/hahaliu1029/house-3d> |
| 13 | realsee-developer/realsee-astra-blender (+ prompts/quickstart.en.md) | GitHub README/프롬프트 | 2026-09-15 | 스캔을 실내로 복원하는 공개 프롬프트와 구조→가구→소품 순서 | <https://github.com/realsee-developer/realsee-astra-blender> |
| 14 | syaripin-i8i/blender-astra-texture-guide | GitHub README(일본어) | 2026-09-09 | 텍스처 재마감 절차와 실제 프롬프트 | <https://github.com/syaripin-i8i/blender-astra-texture-guide> |
| 15 | danielsobrado/Codex-and-Blender | GitHub README | 2026-09-13 | bpy를 원본으로 두고 MCP를 점검용으로 쓰는 구조 | <https://github.com/danielsobrado/Codex-and-Blender> |
| 16 | mohakmalviya/blender-astra-mcp | GitHub README | 2026-09-09 | MCP 배칭 토큰 측정 | <https://github.com/mohakmalviya/blender-astra-mcp> |
| 17 | ProfRino/Blender-MCP-Assembly-Skill | GitHub README/스킬 | 2026-05 | 의자 조립 전후 비교와 조립 규칙 | <https://github.com/ProfRino/Blender-MCP-Assembly-Skill> |
| 18 | RobLe3/cc-blender-skill | GitHub README/스킬 | 2026-05 | 작업 순서와 실패 렌더를 포함한 검증 | <https://github.com/RobLe3/cc-blender-skill> |
| 19 | viettranx/3dviz-pro-max | GitHub README/스킬 | 2026-09-11 | Latent Village 쇼케이스와 평가 점수 | <https://github.com/viettranx/3dviz-pro-max> |
| 20 | hi-godot/cyberpunk-hud-demo friction log | GitHub 문서 | 2026-04-15 | Godot MCP 도구의 빈틈과 우회 방법 | <https://raw.githubusercontent.com/hi-godot/cyberpunk-hud-demo/main/docs/friction-log-cyberpunk-hud.md> |
| 21 | flopperam/unreal-engine-mcp README | GitHub README | 2026-06 | GPT-5 대 Claude 대결과 객체 4,000개 이상 메트로폴리스 데모 링크, 고수준 도구 목록 | <https://github.com/flopperam/unreal-engine-mcp> |
| 22 | TripoGrowthLab/awesome-3d-prompts 카탈로그 | 큐레이션 카탈로그(벤더) | 2026-09-25 | 447개 사례의 프롬프트 원문, 모델, 날짜, X 원문 링크 | <https://raw.githubusercontent.com/TripoGrowthLab/awesome-3d-prompts/main/docs/catalog.en.md> |
| 23 | carpentry-liu/awesome-astra-3d data/cases.json | 큐레이션 DB(근거 등급 포함) | 2026-09-26 | OpenAI 공식 쇼케이스, 실패와 대조 사례, 한계 메모 | <https://raw.githubusercontent.com/carpentry-liu/awesome-astra-3d/main/data/cases.json> |
| 24 | yangqiong/gpt6-astra-3d README ⚠ | 큐레이션 라운드업 | 2026-09-05~ | Astra 출시일, 반응 상위 사례, Opus 5.5·Fable·Gemini 비교 수치 | <https://github.com/yangqiong/gpt6-astra-3d> |
| 25 | magiccreator-ai/awesome-gpt-6-astra ⚠ | 큐레이션 목록 | 2026-09-22 | Blender·3D 데모 24건 이상과 공통 한계 | <https://github.com/magiccreator-ai/awesome-gpt-6-astra> |
| 26 | Claude Opus 제품 페이지 | 공식 제품 페이지 | 2026-09-22 출시 명시 | Opus 5.5 출시일, 비전·computer use 강점 | <https://www.anthropic.com/claude/opus> |
| 27 | Claude Fable 제품 페이지 | 공식 제품 페이지 | 2026-09-01 발표 | Fable 5.1 포지셔닝(3D 언급 없음) | <https://www.anthropic.com/claude/fable> |
| 28 | breineng/how-to-suck | GitHub README | 2026-09-14 | 배포까지 간 Unity 게임의 시간과 구독 사용량 | <https://github.com/breineng/how-to-suck> |
| 29 | octopus7/astra-blender-forest | GitHub README(한국 개발자) | 2026-09-14 | 한국 사례. 대규모 인스턴싱과 UE 내보내기 | <https://github.com/octopus7/astra-blender-forest> |
| 30 | openerai/blender-previz-video | GitHub README(한국어 스킬) | 2026-09-08 | 한국어 Claude Code 스킬. 프리비즈→AI 영상 규칙 | <https://github.com/openerai/blender-previz-video> |
| 31 | Roblox/studio-rust-mcp-server | GitHub README(공식) | 2026-04-03 아카이브 | Roblox Studio 내장 MCP로 전환됐다는 사실 | <https://github.com/Roblox/studio-rust-mcp-server> |
| 32 | cagrikacmaz/gpt-6-astra-vs-gemini-3-8-flash | GitHub 비교 보고 | 2026-09-06 | Gemini 계열 비교 사례 | <https://github.com/cagrikacmaz/gpt-6-astra-vs-gemini-3-8-flash> |
| 33 | HurtzDonutStudios/ai-forge-mcp ⚠ | GitHub README(상업) | 2026-04 | 검증되지 않은 'AAA' 주장에 대한 비판적 검토 사례 | <https://github.com/HurtzDonutStudios/ai-forge-mcp> |
| 34 | OpenAI 개발자 블로그: Architectural visualization with Astra (접근 차단, 링크만 확인) | 공식 블로그(미열람) | 2026-09-04 | Solace 하우스 등 공식 건축 시각화 과정. 원문을 반드시 따로 확인해야 함 | <https://developers.openai.com/blog/architectural-visualization-with-astra> |

**⚠ 신뢰도 경고가 붙은 출처**

- <https://github.com/HurtzDonutStudios/ai-forge-mcp> — 유료 구독 상품의 마케팅 README다. 'AAA', '도구 565개' 같은 주장을 뒷받침할 공개 에셋이나 독립 검증이 없고, 코드는 Nuitka로 컴파일된 비공개다. 제3자 라이선스도 틀리게 적었다(Hunyuan3D를 MIT로 표기. 실제는 EU·영국·한국이 제외된 Tencent 커뮤니티 라이선스).
- <https://github.com/TripoGrowthLab/awesome-3d-prompts> — 3D 생성 벤더(Tripo)가 큐레이션했고 Tripo 사이트 CTA가 붙어 있다. 447건 중 216건(48%)이 원문 프롬프트가 아니라 Tripo가 쓴 'Build brief'다. 결과 품질은 검증하지 않았다. 프롬프트 템플릿 출처로는 유용하지만 '실제 사용된 프롬프트'로 인용할 때는 브리프 여부를 확인해야 한다.
- <https://github.com/yangqiong/gpt6-astra-3d> — X 게시물의 2차 요약이다. 데이터 손상이 있다. 금액의 '$'가 '<!-- creations:start -->' 주석으로 치환되어 있고, 같은 항목이 다른 순위 번호로 두 번 나온다. 헤더는 'Collected 2026-09-05 · Covering Sep 3–5'인데 행은 09-24까지 있다. 제목과 수치가 어긋나는 곳도 있다(zavrenn '3x fewer tokens' 대 61K/507K는 약 8.3배). 수치 인용 시 주의해야 한다.
- <https://github.com/magiccreator-ai/awesome-gpt-6-astra> — 상업 갤러리 magiccreator.ai로 유도하는 큐레이션이다. 2차 요약이고, Blender·3D 섹션은 '24건 이상'이 아니라 정확히 24건이다. 원문 검증은 제한적이다.
- <https://x.com/> — X 게시물 기반 사례(Matt Shumer, Tom Krcha, Stefan_3D_AI, zavrenn, 3DVR3, SpenserFX 등)의 시간·토큰·품질은 모두 작성자 자기 보고이고, 이번 검증에서도 원문에 접근하지 못했다. 모델 비교는 전부 n=1이다.

<a id="12_assets-pipeline-licensing"></a>
## 에셋·파이프라인·라이선스

주제 원문: 에셋 소스, 게임 레디 파이프라인, 라이선스·법률 (AI+MCP 3D 제작용, 2026-09 기준)

| # | 제목 | 유형 | 날짜 | 왜 유용한가 | URL |
|---|---|---|---|---|---|
| 1 | Tencent Hunyuan 3D 2.1 Community License (LICENSE) | 라이선스 원문 (GitHub) | 2025-06-13 | EU, 영국, 한국을 제외하는 Territory 조항, MAU 100만, 결과물로 다른 모델 개선 금지 | <https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/blob/main/LICENSE> |
| 2 | Tencent Hunyuan 3D 2.0 Community License | 라이선스 원문 | 2025-01-21 | 2.0에도 동일한 지역 제외 | <https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/LICENSE> |
| 3 | Tencent Hunyuan 3D Omni Community License | 라이선스 원문 | 2025-09-26 | 최신 릴리스까지 한국 제외가 유지됨 | <https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-Omni/main/License.txt> |
| 4 | Hunyuan3D-2.1 README | GitHub README | 2025-06 | 파이프라인 클래스, VRAM 요구량, PBR 출력 | <https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/README.md> |
| 5 | microsoft/TRELLIS.2 | GitHub README | 2025-12 ~ 2026 | MIT, 의존성 라이선스, GLB/PBR, decimation과 텍스처 옵션 | <https://github.com/microsoft/TRELLIS.2> |
| 6 | TRELLIS.2 issues (dinov3) | GitHub Issues | 2026-04 ~ 2026-08 | DINOv3 의존성 확인 | <https://github.com/microsoft/TRELLIS.2/issues?q=dinov3> |
| 7 | DINOv3 License | 라이선스 원문 | 2025-08-19 | 상업 이용 허용과 제한 조건 | <https://github.com/facebookresearch/dinov3/blob/main/LICENSE.md> |
| 8 | Poly Haven Public API + ToS | GitHub README/ToS | 2026 | CC0 에셋, 라이브 API 출처 표기 조건, 엔드포인트 | <https://github.com/Poly-Haven/Public-API> |
| 9 | ahujasid/blender-mcp README | GitHub README | 2026-09 | 에셋 소스 통합, 라이선스 커스텀 프로퍼티, Poly Pizza 69% CC-BY | <https://raw.githubusercontent.com/ahujasid/blender-mcp/main/README.md> |
| 10 | mcp-for-blender (PyPI) | 패키지 레지스트리 | 2026-09-25 | 최신 버전 2.1.0과 이름 변경 확인 | <https://pypi.org/project/mcp-for-blender/> |
| 11 | meshy-dev/meshy-mcp-server | 공식 GitHub | 2026-09 | 24개 MCP 도구, remesh/uv_unwrap 파라미터, 크레딧 | <https://github.com/meshy-dev/meshy-mcp-server> |
| 12 | meshy-dev/game-asset-pipeline | 공식 가이드 | 2026-05 | 폴리곤 예산, 엔진 임포트, 플랜별 라이선스 | <https://github.com/meshy-dev/game-asset-pipeline> |
| 13 | meshy-dev/Meshy-guide | 공식 가이드 | 2026-05 | 무료 CC BY 4.0, 유료 private commercial 라이선스 명시 | <https://github.com/meshy-dev/Meshy-guide> |
| 14 | Tripo Python SDK API.md ⚠ | 공식 SDK 문서 | 2025~2026 | smart_lowpoly와 convert_model의 정확한 파라미터와 기본값 | <https://raw.githubusercontent.com/VAST-AI-Research/tripo-python-sdk/master/docs/API.md> |
| 15 | trident-mcp MCP_TOOLS.md | 서드파티 MCP 문서 | 2026-07 | Tripo 2026 모델 버전, 변환 포맷, 리토폴 파라미터 | <https://raw.githubusercontent.com/mordor-forge/trident-mcp/main/docs/MCP_TOOLS.md> |
| 16 | Khronos 3DC Real-time Asset Creation Guidelines 1.0 | 표준 기구 가이드 | 2020-10 (v2.0은 2025… | 삼각형, 텍스처, 파일 크기, 노멀 규약, ORM 수치 기준 | <https://raw.githubusercontent.com/KhronosGroup/3DC-Asset-Creation/main/asset-creation-guidelines-1.0/RealtimeAssetCreationGuidelines.md> |
| 17 | Khronos glTF Asset Auditor | 공식 도구 | 2026 | PBR safe color 30~243, 텍스처 512~2048 등 자동 검사 | <https://github.com/KhronosGroup/glTF-Asset-Auditor> |
| 18 | Khronos glTF-Validator | 공식 도구 | 2026 | 스펙 검증 CLI, npm, 웹 | <https://github.com/KhronosGroup/glTF-Validator> |
| 19 | glTF-Blender-IO docs (scene_gltf2.rst) | 공식 문서 소스 | 2026 | 채널 매핑, 익스포트 옵션, 지원 확장 | <https://raw.githubusercontent.com/KhronosGroup/glTF-Blender-IO/main/docs/blender_docs/scene_gltf2.rst> |
| 20 | gltfpack README | 공식 README | 2026 | -si, -c/-cc, -tc 플래그와 Draco 미지원 | <https://raw.githubusercontent.com/zeux/meshoptimizer/master/gltf/README.md> |
| 21 | zeux/meshoptimizer | 공식 README | v1.3 | 단순화 API와 clusterlod | <https://github.com/zeux/meshoptimizer> |
| 22 | glTF-Transform | 공식 README | 2026 | optimize 등 CLI 명령 | <https://github.com/donmccurdy/glTF-Transform> |
| 23 | QRemeshify | GitHub README | 2024-10 | 쿼드 리메시 설정과 입력 준비 팁 | <https://github.com/ksami/QRemeshify> |
| 24 | MeshAnythingV2 | GitHub README | ICCV 2025 | 1,600면 제한, 사용법 | <https://github.com/buaacyw/MeshAnythingV2> |
| 25 | MeshAnything S-Lab License | 라이선스 원문 | 2024 | 비상업 제한 | <https://github.com/buaacyw/MeshAnything/blob/main/LICENSE.txt> |
| 26 | Allar UE5 Style Guide | 커뮤니티 표준 가이드 | 2026 | UE 에셋 네이밍 규칙 | <https://github.com/Allar/ue5-style-guide> |
| 27 | Send to Unreal: static-mesh.md | Epic 공식 도구 문서 | 2026 | 콜리전, LOD, 소켓 네이밍 | <https://raw.githubusercontent.com/EpicGamesExt/BlenderTools/main/docs/send2ue/asset-types/static-mesh.md> |
| 28 | allenai/objaverse-xl | GitHub README | 2024-08 | ODC-By와 객체별 라이선스, Polycam 비상업 | <https://github.com/allenai/objaverse-xl> |
| 29 | Bingeljell/image-to-3dlab | 사례 (GitHub) | 2026-09 | 로컬 게임 레디 파이프라인과 라이선스 게이트, provenance | <https://github.com/Bingeljell/image-to-3dlab> |
| 30 | Anthropic Commercial Terms | 약관 원문 | 2025-06-17 발효 | 출력물 소유와 양도 | <https://www.anthropic.com/legal/commercial-terms> |
| 31 | Anthropic Consumer Terms | 약관 원문 | 2025-10-08 발효 | 소비자 플랜 출력물 양도, 경쟁 모델 학습 금지 | <https://www.anthropic.com/legal/consumer-terms> |
| 32 | Stable Fast 3D LICENSE (Stability AI Community License) | 라이선스 원문 | 2024~2025 | 매출 100만 달러 기준, 결과물 소유 | <https://raw.githubusercontent.com/Stability-AI/stable-fast-3d/main/LICENSE.md> |
| 33 | dcc-mcp 조직 ⚠ | GitHub 조직 | 2026-07 | 에셋 소스 MCP 스킬 패밀리 | <https://github.com/dcc-mcp> |
| 34 | Tanshaydar/Quartermaster ⚠ | 사례 (GitHub) | 2026-09 | 보유 에셋 MCP 색인 패턴 | <https://github.com/Tanshaydar/Quartermaster> |
| 35 | AIWHOS/paper-ember-duel | 사례 (GitHub) | 2026-09 | GPT-6와 Rodin MCP, Blender, Godot 실제 과정 | <https://github.com/AIWHOS/paper-ember-duel> |
| 36 | KaelNebula/rodin-via-blender | 사례 (GitHub) | 2026-05 | 조형물 제작 파이프라인 (Claude Code 스킬) | <https://github.com/KaelNebula/rodin-via-blender> |
| 37 | 인공지능 기본법 조문 데이터 (제3자) ⚠ | 2차 자료 (법령 조문 데이터) | 2026-07 | 제31조 표시 의무와 시행일 2026-01-22 | <https://raw.githubusercontent.com/nfa-bigdata/ai-law-clause-search-set5-2026/main/%EC%A1%B0%ED%95%AD%EB%8D%B0%EC%9D%B4%ED%84%B0.json> |

**⚠ 신뢰도 경고가 붙은 출처**

- <https://raw.githubusercontent.com/devanshutak25/3d-resources/main/README.md> — README에 'built with Claude'라고 명시된 AI 보조 큐레이션 목록이고 1차 자료가 아닙니다. Megascans를 한 곳에서는 'Free with Unreal Engine', 다른 곳에서는 'only UE projects'로 적는 등 서로 모순되고 낡은 항목이 있습니다. 'Kenney 60,000+'는 유료 All-in-1 번들 항목의 수치인데, KB는 이를 CC0 무료 에셋 수로 읽었습니다. 라이선스나 가격 근거로 쓰면 안 됩니다.
- <https://raw.githubusercontent.com/VAST-AI-Research/tripo-python-sdk/master/docs/API.md> — 공식 문서지만 현행 SDK 소스(tripo3d/client.py, 0.4.2)와 맞지 않습니다. smart_lowpoly와 convert_model의 기본값이 바뀌었고, 새 인자와 새 모델 버전이 누락되어 있습니다. client.py를 1차 근거로 삼아야 합니다.
- <https://github.com/stepfun-ai/Step1X-3D> — README와 LICENSE는 Apache-2.0이라고 하지만, 저장소에 Tencent Hunyuan 라이선스 헤더가 붙은 코드(step1x3d_texture/custom_rasterizer, differentiable_renderer)와 nvdiffrast 의존성이 들어 있습니다. 1차 자료 안에서 라이선스 표기가 서로 모순됩니다.
- <https://raw.githubusercontent.com/microsoft/TRELLIS.2/main/README.md> — 라이선스 섹션에 nvdiffrast와 nvdiffrec만 '별도 라이선스'로 적혀 있습니다. 그 라이선스가 비상업이라는 점, DINOv3(Meta 라이선스)와 RMBG-2.0(BRIA) 의존성은 언급하지 않습니다. 1차 자료지만 라이선스 판단 근거로는 불완전합니다.
- <https://raw.githubusercontent.com/nfa-bigdata/ai-law-clause-search-set5-2026/main/%EC%A1%B0%ED%95%AD%EB%8D%B0%EC%9D%B4%ED%84%B0.json> — 제3자가 가공한 조문 데이터입니다. 이번에 대조한 제31조와 부칙 내용은 국가법령정보센터 PDF 텍스트와 형식이 일치해 신뢰할 만합니다. 다만 KB에는 law.go.kr 원문 링크를 1차 출처로 달아야 합니다.
- <https://github.com/Tanshaydar/Quartermaster> — 스타 2개인 초기 개인 프로젝트이고, 스토어 비공개 API와 세션 재생 방식으로 수집해 약관 위반 위험이 있습니다. 권장 도구 근거로 부적절합니다.
- <https://github.com/iQreu/blender-mcp-suite> — 스타 1개, 커밋 1개입니다. scene_measure와 scene_assert 기능이 있는 것은 확인했지만, 성숙도가 검증되지 않아 '권장' 근거로 쓰기에는 약합니다.
- <https://github.com/dcc-mcp> — 조직 저장소 91개 중 에셋 스킬은 대부분 스타 0~1개이고, 스타 수로 보아 이용이 거의 없는 초기 프로젝트입니다. 존재와 기능 설명은 맞지만 KB에서 성숙한 도구처럼 소개하면 안 됩니다.

<a id="13_research-papers"></a>
## 학술 연구

주제 원문: 3D 제작용 LLM/VLM 에이전트 학술 연구(2023–2026): 실무자를 위한 주석 참고문헌 — Claude/GPT + Blender MCP에 적용할 교훈 중심

| # | 제목 | 유형 | 날짜 | 왜 유용한가 | URL |
|---|---|---|---|---|---|
| 1 | hzxie/Awesome-3D-Scene-Generation (IJCV 2026 서베이 동반 목록) | curated list (GitHub) | 2026-09-18 push | LLM/에이전트 기반 씬 생성 논문 2024–2026(SceneSmith, SAGE, SceneOrchestra, NaLA, WorldClaw 등)의 arXiv 링크와 학회 정보를 제공합니다. | <https://github.com/hzxie/Awesome-3D-Scene-Generation> |
| 2 | xdlbw/Awesome-3D-Object-and-Scene-Generation (CSUR 2026) | curated list (GitHub) | 2026-08 | MeshCoder(NeurIPS 2025), Articulate-Anything, 절차적 관절 에셋 등 객체 수준 코드 생성 연구를 확인할 수 있습니다. | <https://github.com/xdlbw/Awesome-3D-Object-and-Scene-Generation> |
| 3 | BlenderGym 프로젝트 페이지 소스 | project page (primary) | 2025 | 245 씬, 5 과제, VeriRatio 0.62–0.73, 인간-VLM 정합률, 과제별 리더보드 | <https://raw.githubusercontent.com/BlenderGym/BlenderGym.github.io/main/index.html> |
| 4 | VIGA GitHub | GitHub README (primary) | 2026 | Generator/Verifier 교대 구조, 메모리, BlenderBench, 설치 방법 | <https://github.com/Fugtemypt123/VIGA> |
| 5 | 3DCodeBench GitHub + prompts ⚠ | GitHub README (primary) | 2026-06-01 | Blender 5.0 코딩 에이전트 벤치마크, 재사용 가능한 시스템/비평 프롬프트, Blender 5.0 API 함정 목록 | <https://github.com/gaoypeng/3dcodebench> |
| 6 | 3DCodeBench Blender 5.0 API reference | prompt/resource file | 2026-06 | LLM이 자주 틀리는 Blender 5.0 API 변경 사항을 CLAUDE.md에 바로 넣을 수 있습니다. | <https://raw.githubusercontent.com/gaoypeng/3dcodebench/main/prompts/blender_5_api_reference.txt> |
| 7 | BlenderAlchemy 공식 config | code/config (primary) | 2024 | 트리 탐색 하이퍼파라미터(4x8), visual imagination, hypothesis reversion 설정의 실제 값 | <https://raw.githubusercontent.com/ianhuang0630/BlenderAlchemyOfficial/main/configs/wood_to_marble.yaml> |
| 8 | SceneSmith 프로젝트 페이지 소스 | project page (primary) | 2026 | 계층 에이전트 구조와 정량 결과(3–6배 객체, 96% 안정, 사용자 205명 연구) | <https://raw.githubusercontent.com/scenesmith/scenesmith.github.io/main/index.html> |
| 9 | SceneReVis 프로젝트 페이지 소스 | project page (primary) | 2026-02 | LayoutGPT, LayoutVLM, Holodeck, SceneReVis의 충돌률과 경계 이탈률 비교표 | <https://raw.githubusercontent.com/SceneReVis/SceneReVis.github.io/main/index.html> |
| 10 | SGP-Bench 프로젝트 페이지 소스 | project page (primary) | 2025 | LLM이 코드만으로 시각 결과를 추론하는 능력의 한계 수치 | <https://raw.githubusercontent.com/sgp-bench/sgp-bench.github.io/main/index.html> |
| 11 | BlenderLLM GitHub | GitHub README (primary) | 2024-12 | 특화 모델의 구문 오류율 비교(Claude-3.5-Sonnet 15.6% 등)와 한계 명시 | <https://github.com/FreedomIntelligence/BlenderLLM> |
| 12 | LL3M GitHub | GitHub README (primary) | 2025-08 | 멀티에이전트와 BlenderRAG 구조, 모델 retire로 인한 서비스 중단 공지 | <https://github.com/threedle/ll3m> |
| 13 | Holodeck GitHub | GitHub README (primary) | 2023–2024 | LLM 제약 + DFS 솔버 + Objaverse 검색 구조, MILP에서 DFS로의 변경 이력 | <https://github.com/allenai/Holodeck> |
| 14 | NVlabs/sage GitHub | GitHub README (primary) | 2026 | MCP식 client/server 백엔드 구조, SAGE-10k 규모 | <https://github.com/NVlabs/sage> |
| 15 | Scene-Weaver/SceneWeaver GitHub | GitHub README (primary) | 2025 | tool card 기반 reason-act-reflect 에이전트와 사용 가능한 툴 목록 | <https://github.com/Scene-Weaver/SceneWeaver> |
| 16 | MeshCoder GitHub | GitHub README (primary) | 2025-08 | 파트별 Blender 코드 역변환, 100만 쌍 데이터, MegaParts 후속 | <https://github.com/InternRobotics/MeshCoder> |
| 17 | Frank-ZY-Dou/awesome-ai-3d-modeling-robotics ⚠ | curated list of case posts (G… | 2026-09-26 | GPT-6 Astra, Claude Opus 5.5, Fable 5.1 기반 Blender/UE 제작 사례 링크 모음(사례 조사 담당 참고용, 비검증) | <https://github.com/Frank-ZY-Dou/awesome-ai-3d-modeling-robotics> |
| 18 | ScoreIA La Forge results ⚠ | non-academic benchmark results | 2026-09-24 | 최신 모델을 MCP 3D 작업에서 비교한 드문 자료(신뢰도 낮음) | <https://github.com/drakkB/scoreia-forge-results> |

**⚠ 신뢰도 경고가 붙은 출처**

- <https://github.com/drakkB/scoreia-forge-results> — README가 스스로 밝히는 한계가 있습니다. 모델 신원은 자기 신고라 검증되지 않고 카드에 서명도 없습니다. 심판과 캠페인을 Claude Opus로 작성해 편향 가능성이 있습니다. 모델마다 하네스가 다릅니다(Claude Code, Codex CLI, Grok CLI). 도구가 Forge 전용 MCP의 부품 조립이라 Blender 모델링·텍스처 품질을 대표하지 못합니다. 동료심사를 거치지 않은 단일 업체 자료입니다.
- <https://github.com/Frank-ZY-Dou/awesome-ai-3d-modeling-robotics> — SEO 스팸은 아니고 출처 링크와 미디어 아카이브가 있는 큐레이션입니다. 다만 X/LinkedIn/YouTube 사례를 모은 2차 집계이고, 스스로 'Most cases use GPT-6 Astra'라고 밝힐 만큼 선택 편향이 있습니다. 모델 신원도 작성자 주장에 기대는 경우가 많습니다. 수치는 반드시 1차 출처(각 벤치마크 페이지나 논문)로 재확인해야 합니다. 한편 이 목록에 La Forge 외 최신 모델 3D/CAD 벤치마크가 여러 개 있으므로, 보고서의 '유일한 근거는 La Forge와 사례 모음'이라는 주장은 틀렸습니다.
- <https://github.com/gaoypeng/3dcodebench> — 신뢰할 만한 1차 출처이지만 라이선스 표기가 내부에서 모순됩니다(README는 MIT, LICENSE 파일은 Apache 2.0, factory는 BSD-3). 라이선스를 인용할 때는 LICENSE 파일을 기준으로 삼고 불일치를 명시해야 합니다.

<a id="g1_dimensions"></a>
## [보완] 실측 치수 표준

주제 원문: 실세계 가구·인테리어·인체 스케일 치수 표준 (AI 3D 모델링/배치용 레퍼런스, 출처 포함)

| # | 제목 | 유형 | 날짜 | 왜 유용한가 | URL |
|---|---|---|---|---|---|
| 1 | Standard Dining Chair Dimensions and How to Choose the Right One (Pop Maison) | 가구 브랜드 가이드 |  | 좌판 높이 17–19 in와 상판-좌판 10–12 in 관계를 제시한다. | <https://www.popmaison.com/blogs/guide/dining-chair-dimensions> |
| 2 | What Are the Typical Dimensions of a Standard Dining Chair? (Picket & Rail) | 가구 브랜드 가이드 |  | 좌판 깊이 16–18 in, 등받이 12–20 in. | <https://picketandrail.com/blogs/dining-blog/what-are-the-typical-dimensions-of-a-standard-dining-chair> |
| 3 | Standard Dining Chair Dimensions (2026) - Sizemarker | 치수 레퍼런스 |  | 의자 전체 높이 32–38 in. | <https://www.sizemarker.com/dimensions/standard-dining-chair-dimensions> |
| 4 | Standard Sofa Size Guide (Povison) | 가구 브랜드 가이드 |  | 3인 소파 183–244 cm, 가장 흔한 폭 213 cm. | <https://www.povison.com/blog/buying-guide/standard-sofa-size-guide.html> |
| 5 | Standard Sofa and Loveseat Sizes (RoomSketch3D) | 치수 레퍼런스 |  | 러브시트 132–183 cm 폭, 76–102 cm 깊이. | <https://roomsketch3d.com/help/dimensions/sofa-and-loveseat-dimensions> |
| 6 | Standard Sofa Dimensions (OMHU) | 가구 브랜드 가이드 |  | cm와 inch를 함께 제시하는 소파 치수. | <https://omhucph.com/blogs/inspiration/standard-sofa-dimensions> |
| 7 | 이스턴킹? 라지킹? 캘리포니아킹? 침대 크기의 모든 것 (브런치) | 한국 블로그 |  | 한국 S/SS/Q/K/LK 규격과 미국 킹 계열 비교. | <https://brunch.co.kr/@phapark/59> |
| 8 | 침대 사이즈 완벽 가이드 (슬립퍼) | 한국 매거진 |  | 한국 매트리스 규격과 2100 길이 옵션. | <https://sleeper.co.kr/magazine/01-bed-size-guide/bed-size-guide.html> |
| 9 | Mattress size guide 2026 (T3) | 리뷰 매체 |  | US/UK/EU 매트리스 규격 비교. | <https://www.t3.com/features/mattress-size-guide> |
| 10 | UK vs US mattress sizes (TechRadar) | 리뷰 매체 |  | UK King이 US Queen에 가깝다는 비교, EU가 UK보다 10 cm 길다는 점. | <https://www.techradar.com/health-fitness/mattresses/mattress-sizes-uk-vs-us-vs-eu> |
| 11 | 주방 싱크대 높이와 동선 설계 (치호건축사사무소) | 한국 건축사무소 블로그 |  | 한국 싱크대 850 mm가 키 160~165 cm 여성 기준 산업 표준이라는 설명. | <https://chiho.co.kr/blogroom/%EC%A3%BC%EB%B0%A9-%EC%8B%B1%ED%81%AC%EB%8C%80-%EB%86%92%EC%9D%B4%EC%99%80-%EB%8F%99%EC%84%A0-%EC%84%A4%EA%B3%84-%ED%82%A4%EB%B3%84-%EC%B5%9C%EC%A0%81-%EC%B9%98%EC%88%98-%EA%B3%B5%EA%B0%9C-%EC%A3%BC%EB%B0%A9%EC%84%A4%EA%B3%84> |
| 12 | 주방을 설계한다면 꼭 알아야 할 치수들 (ideabuild, Threads) | 한국 인테리어 실무 SNS |  | 아일랜드 700, 동선 900, 싱크대 900 권장, 미드웨이 650~750, 식탁 750, 의자 450, 상부장 깊이 350, 싱크대 깊이 650 이상. | <https://www.threads.com/@ideabuild_official/post/DQ8kvc-kRe7> |
| 13 | [중급] 주방 상부장 스타일 알아보기 (LX Z:IN) | 한국 제조사 가이드 |  | 하부장 850, 미드웨이 700, 상부장 750, 합계 약 2300의 모듈. | <https://www.lxzin.com/styling/style-guide/detail/5596> |
| 14 | [고급] 싱크대 설치 준비하기 (LX Z:IN) | 한국 제조사 가이드 |  | 싱크대 설치 치수. | <https://www.lxzin.com/styling/style-guide/detail/647> |
| 15 | NKBA Kitchen Planning Guidelines with Access Standards (PDF) | 업계 표준 가이드라인 |  | 미국 주방 통로, 트라이앵글, 식탁 여유 공간의 원문(이번에는 egress 차단으로 직접 열람하지 못함). | <https://media.nkba.org/uploads/2022/05/Kitchen-Planning-Guidelines.pdf> |
| 16 | Kitchen Dimensions: Code Requirements & NKBA Guidelines (CRD Design Build) | 시공사 블로그(NKBA 요약) |  | 통로 42/48 in, 트라이앵글 26 ft와 각 변 4–9 ft, 조리대 36 in. | <https://www.crddesignbuild.com/blog/kitchen-dimensions-code-requirements-nkba-guidelines/> |
| 17 | Kitchen Design Guidelines & Clearances (Wholesale Cabinet Supply) | 캐비닛 업체 가이드 |  | 상부장 하단 54 in, 조리대 위 18 in. | <https://www.thewcsupply.com/pages/kitchen-design-guidelines-standard-clearances> |
| 18 | Kitchen work triangle (Wikipedia) | 백과사전 |  | 워크 트라이앵글 개념과 수치. | <https://en.wikipedia.org/wiki/Kitchen_work_triangle> |
| 19 | 7 Base Cabinet Sizes (Allure) | 캐비닛 업체 가이드 |  | 하부장 34.5 in 높이, 24 in 깊이. | <https://www.allurekitchencabinet.com/blog/7-base-cabinet-sizes-standard-height-depth-width> |
| 20 | Wall Cabinet Sizes & Heights Chart (TC Wholesale Cabinetry) | 캐비닛 업체 가이드 |  | 미국 상부장 높이와 깊이. | <https://tcwholesalecabinetry.com/blog/wall-cabinet-sizes-types> |
| 21 | 일반적인 아파트 층고와 천장고 기준 (한국PM) | 한국 업계 블로그 |  | 층고 2.8~2.85 m, 천장고 2.3 m 기준. | <https://hkpm.co.kr/%EC%9D%BC%EB%B0%98%EC%A0%81%EC%9D%B8-%EC%95%84%ED%8C%8C%ED%8A%B8-%EC%B8%B5%EA%B3%A0%EC%99%80-%EC%B2%9C%EC%9E%A5%EA%B3%A0-%EA%B8%B0%EC%A4%80%EA%B3%BC-%EC%9D%98%EB%AF%B8-%EA%B4%80%EA%B3%84/> |
| 22 | [김수암 칼럼] 층고와 천장고가 높은 것도 경쟁력이다 (아파트관리신문) | 한국 언론 칼럼 |  | 천장고 2300 대부분, 일부 2350~2400. | <http://www.aptn.co.kr/news/articleView.html?idxno=49567> |
| 23 | 방문 사이즈 - 건재정보 (다음카페) | 한국 커뮤니티 |  | 욕실문 700×2000/800×2100, 방문 900 또는 1000×2100. | <https://m.cafe.daum.net/retirecountry/GbzJ/5?q=D_KkJLW6NS9QQ0> |
| 24 | 현관문 크기: 알아야 할 표준 치수 (APRO) | 도어 제조사 가이드 |  | 아파트 현관문 900/1000/1100×2100. | <https://aprodoor.com/front-door-sizes/> |
| 25 | 계단의 설치기준 (마이다스캐드) | 한국 법규 해설 |  | 단높이, 단너비, 손잡이, 대체 경사로 기준 해설. | <https://www.midascad.com/cad_archive/buildingact-4> |
| 26 | 건축물의 피난ㆍ방화구조 등의 기준에 관한 규칙 (국가법령정보센터) | 법령 원문 |  | 제15조 계단 기준(계단참, 난간, 유효높이 등). | <https://www.law.go.kr/LSW/lsLinkCommonInfo.do?lspttninfSeq=124056&chrClsCd=010202> |
| 27 | 법제처 민원인 해석 - 돌음계단 단너비 측정 (CaseNote) | 법령해석 |  | 주택건설기준 등에 관한 규정 제16조 관련 해석. | <https://casenote.kr/%EB%B2%95%EC%A0%9C%EC%B2%98/18-0465-d5162f> |
| 28 | 2015 IRC Residential Stairways and Ramps handout (Essex, CT) | 지자체 코드 요약 |  | IRC 단높이 7¾, 디딤판 10, 머리 여유 6'8". | <https://www.essexct.gov/DocumentCenter/View/449/Residential-Stairways-and-Ramps-2015-Irc-Handout-PDF> |
| 29 | Maximum and Minimum Handrail Heights (Viewrail) | 제조사 코드 해설 |  | IRC 손잡이 34–38 in. | <https://resources.viewrail.com/code-compliance/railing-code/maximum-and-minimum-handrail-heights> |
| 30 | IRC Stair Code Requirements (TradeMaster Calc) | 코드 레퍼런스 |  | IRC 계단 수치 요약. | <https://trademastercalc.com/reference/irc-stair-code> |
| 31 | 콘센트·스위치 위치 설계 가이드 (sunnysunnyday) | 한국 시공 실무 블로그 |  | 협탁용 콘센트 60~70 cm, 책상용 80~90 cm. | <https://sunnysunnyday.com/entry/%EC%8B%B1%ED%81%AC%EB%8C%80-%EC%95%9E%EC%97%90-%EC%BD%98%EC%84%BC%ED%8A%B8%EA%B0%80-%EC%9E%88%EB%8D%98-%ED%98%84%EC%9E%A5%EC%9D%84-%EC%9D%B4%EC%96%B4%EB%B0%9B%EA%B3%A0-%EB%82%98%EC%84%9C-%EC%A0%95%EB%A6%AC%ED%95%9C-%EC%BD%98%EC%84%BC%ED%8A%B8%C2%B7%EC%8A%A4%EC%9C%84%EC%B9%98-%EC%9C%84%EC%B9%98-%EC%84%A4%EA%B3%84-%EA%B0%80%EC%9D%B4%EB%93%9C-%EA%B3%B5%EA%B0%84%EB%B3%84-%EC%BD%98%EC%84%BC%ED%8A%B8-%EB%86%92%EC%9D%B4-%EC%8A%A4%EC%9C%84%EC%B9%98-%EB%B0%B0%EC%B9%98-%ED%9A%8C%EB%A1%9C-%EB%B6%84%EB%A6%AC-%EA%B8%B0%EC%A4%80> |
| 32 | 내력벽 비내력벽 구분 방법과 차이 (AJD) | 한국 인테리어 가이드 |  | 180 mm 이상이면 내력벽, 100 mm 내외면 비내력벽, 습식 벽 150 mm. | <https://www.ajd.co.kr/contents/basic-tip/detail/%EB%82%B4%EB%A0%A5%EB%B2%BD_%EB%B9%84%EB%82%B4%EB%A0%A5%EB%B2%BD_%EA%B5%AC%EB%B6%84_%EB%B0%A9%EB%B2%95%EA%B3%BC_%EC%B0%A8%EC%9D%B4%EF%BD%9C%EB%8F%84%EB%A9%B4%C2%B7%EB%91%90%EA%BB%98%EB%A1%9C_%EC%B2%A0%EA%B1%B0_%EA%B0%80%EB%8A%A5_%EC%97%AC%EB%B6%80_%ED%99%95%EC%9D%B8%ED%95%98%EA%B8%B0-72255> |
| 33 | 아파트 벽체두께는 얼마정도인가요? (클리앙) | 한국 커뮤니티 |  | 외벽 200, 내벽 150~200(가끔 100). | <https://www.clien.net/service/board/kin/12725939> |
| 34 | The ultimate guide to living room clearances (Homes & Gardens) | 인테리어 매체 |  | 소파-커피테이블 14–18 in, 통로 30–36 in, 러그 규칙. | <https://www.homesandgardens.com/interior-design/living-rooms/a-guide-to-living-room-clearances-measurements-and-spacing> |
| 35 | Ideal Living Room Layout Measurements (Apartment Therapy) | 인테리어 매체 |  | 거실 배치 치수 종합. | <https://www.apartmenttherapy.com/living-room-layouts-the-ideal-measurements-for-everything-in-the-room-206734> |
| 36 | Living Room Layout Rules: Traffic Flow, Conversation Zones, and TV Placement (Keck Furnit… | 가구점 가이드 |  | TV 거리 1.5–2.5배, 55인치 7–9 ft, 65인치 8–10 ft. | <https://keckfurniture.com/blog/living-room-layout-rules-traffic-flow-conversation-zones-and-tv-placement/> |
| 37 | Dining Table Space Guide (Eureka Ergonomic) | 가구 브랜드 가이드 |  | 식탁 주변 36 in 여유. | <https://eurekaergonomic.com/blogs/eureka-ergonomic-blog/dining-table-space-clearance-guide> |
| 38 | Table Size & Space Guidelines (Lamon Luther) | 가구 브랜드 가이드 |  | NKBA 인용 36/44 in 식탁 여유. | <https://www.lamonluther.com/resources/table-size-space-guidelines/> |
| 39 | Dining Table Size Guide Based on Number of People (NEPA Furniture) | 가구점 가이드 |  | 1인당 24 in(61 cm), 격식 있는 식사 28–30 in. | <https://www.nepafurniture.com/blog/home-furniture-32/dining-table-size-guide-based-on-number-of-people-414> |
| 40 | Pendant Lights Over Dining Table Height 2026 Guide (Fenchel Shades) | 조명 업체 가이드 |  | 식탁 위 30–34 in. | <https://www.fenchelshades.com/blog/post/pendant-lights-over-dining-table-height-standard-measurements-and-placement-guide-2026-usa> |
| 41 | Complete Pendant Light Height & Spacing Guide (Artika) | 조명 제조사 가이드 |  | 펜던트 높이와 간격. | <https://artika.com/blogs/inspiration/complete-pendant-height-spacing-guide> |
| 42 | How Far Apart Should Pendant Lights Be? (2Modern) | 조명 판매사 가이드 |  | 펜던트 간격 24–36 in. | <https://www.2modern.com/blogs/modern-how-to/how-far-apart-should-pendant-lights-be> |
| 43 | What Is the Rule of 57 for Hanging Art? (AS Hanging) | 액자 걸이 제조사 가이드 |  | 그림 중심 57 in(145 cm)=평균 눈높이. | <https://www.ashanging.com/en_us/help/what-is-the-rule-of-57> |
| 44 | Three Simple Rules To Follow When Hanging Art (Park West Gallery) | 갤러리 |  | 갤러리 관행 확인. | <https://www.parkwestgallery.com/blog/3-simple-rules-for-hanging-art/> |
| 45 | 사이즈코리아 제8차 한국인 인체치수 조사 결과 | 정부 공식 데이터 |  | 한국인 평균 키 남 172.5, 여 159.6 cm. | <https://sizekorea2022.kr/8th_results/> |
| 46 | 한국인 평균 키와 다리길이, 비만도 공개 (산업통상부 보도) | 정부 보도자료 |  | 제8차 조사 개요(6,839명, 430항목). | <https://www.motir.go.kr/kor/article/ATCL8764a1224/155118041/view> |
| 47 | Bar-Height vs. Counter-Height Furniture (POLYWOOD) | 가구 브랜드 가이드 |  | 카운터 스툴 24–26 in, 바 스툴 28–30 in, 커피테이블 16–18 in. | <https://www.polywood.com/blogs/buying-guides/bar-height-vs-counter-heights-for-stools-and-tables-whats-the-difference> |
| 48 | Nightstands & Bedside Tables Dimensions (Dimensions.com) | 치수 레퍼런스 |  | 협탁 24–28 in, 침대 높이 약 25 in. | <https://www.dimensions.com/collection/bedside-tables-nightstands> |
| 49 | How Tall Should a Nightstand Be? (Froy) | 가구 판매사 가이드 |  | 매트리스 상단 ±2 in 규칙. | <https://froy.com/blogs/tips/how-tall-should-a-nightstand-be-the-nightstand-height-guide> |
| 50 | KS G 4203 사무용 책상 및 테이블 (KSSN) | 한국산업표준 목록 |  | 사무용 책상 KS 규격 존재 확인. | <https://www.kssn.net/search/stddetail.do?itemNo=K001010111402> |
| 51 | KS 가구 규격의 치수 개정을 위한 사전 조사 연구 (대한인간공학회 2009) | 학술 발표 |  | KS G 4101(의자), KS G 4102(책상) 치수 항목 검토. | <https://www.esk.or.kr/conference/2009_fall/pdf/14_5.pdf> |
| 52 | 표준 사무용 의자 치수 (2026): BIFMA 범위 (Sizemarker) | 치수 레퍼런스 |  | BIFMA 좌판·등받이·팔걸이 범위. | <https://www.sizemarker.com/ko/dimensions/standard-office-chair-dimensions> |
| 53 | 사무용 책상의 기본 높이가 720mm 인가 봐요 (Todaysppc) | 한국 커뮤니티 |  | 한국 사무용 책상 720 mm 관행. | <http://m.todaysppc.com/renewal/view.php?id=free&page=11&page_num=15&category=&sn=off&ss=on&sc=on&keyword=&prev_no=&select_arrange=headnum&desc=asc&no=479576> |
| 54 | BILLY bookcase (IKEA US) | 제조사 제품 페이지 |  | BILLY 40×28×202 cm. | <https://www.ikea.com/us/en/p/billy-bookcase-white-50522040/> |
| 55 | IKEA PAX Dimensions (itemfits) | 치수 레퍼런스 |  | PAX 깊이 58 cm, 폭 50/75/100, 높이 201/236. | <https://itemfits.com/dimensions/ikea/ikea-pax> |
| 56 | IKEA Billy Bookcases Dimensions (Dimensions.com) | 치수 레퍼런스 |  | BILLY 도면 치수. | <https://www.dimensions.com/element/ikea-billy-bookcases> |
| 57 | LH주택평면계획기준 연구 (CODIL) | 공공 연구보고서(미열람) |  | 한국 공공주택 평면 기준(주방·실 치수) 추가 조사 후보. 이번에는 열람하지 못했다. | <https://www.codil.or.kr/filebank/original/RK/OTKCRK150014/OTKCRK150014.pdf> |

<a id="g2_korean_resources"></a>
## [보완] 한국어 자료

주제 원문: 한국어 자료 모음: AI + MCP로 하는 3D 제작(Blender/Unreal/Unity/SketchUp) — 유튜브·블로그·강의·커뮤니티·뉴스, AAA 품질에 필요한 3D 기초(PBR·라이팅·인테리어 렌더링) 포함

| # | 제목 | 유형 | 날짜 | 왜 유용한가 | URL |
|---|---|---|---|---|---|
| 1 | Claude AI와 블렌더 MCP로 3D 모델링 시작하기! 입문자 완전 정복 가이드 | blog |  | 가장 체계적인 한국어 입문 설치 가이드 | <https://media.fastcampus.co.kr/insight/ai_creative/blendermcp/> |
| 2 | Red Dot 수상자에게 배우는 AI 3D 모델링 (ft. 블렌더 MCP) | course |  | 국내 유일의 블렌더 MCP 유료 강의 | <https://fastcampus.co.kr/dgn_online_reddot> |
| 3 | 앤트로픽, 클로드에 크리에이티브 도구 9종 통합… 블렌더 (AI매터스) | news | 2026-04 | 크리에이티브 커넥터 한국어 보도 | <https://aimatters.co.kr/news-report/41239/> |
| 4 | 엔트로픽, 창작 소프트웨어 제어하는 '클로드 커넥터' 출시 (AI타임스) | news | 2026-04 | 교차 확인용 보도 | <https://www.aitimes.com/news/articleView.html?idxno=209904> |
| 5 | GPT-6 아스트라 활용법 총정리 (다나와 DPG) | news | 2026-09 | Astra 3D 사례를 한국어로 정리 | <https://dpg.danawa.com/news/view?boardSeq=60&listSeq=6058609> |
| 6 | 언리얼 엔진을 직접 다루는 AI, UE5.8 MCP 활용 게임 개발기 [전편] (게임뷰) | news |  | 언리얼 MCP 실전 개발기 | <https://www.gamevu.co.kr/news/articleView.html?idxno=60827> |
| 7 | 언리얼 에디터 안에 들어온 MCP 서버 (박재홍의 실리콘밸리) | blog |  | UE5.8 MCP 해설 | <https://wikidocs.net/blog/@jaehong/20632/> |
| 8 | UE5 + Claude Code + MCP 1. 환경 세팅 (velog) | blog |  | 언리얼 연동 실습 | <https://velog.io/@miniminichip/UE5-Claude-Code-MCP-1> |
| 9 | tahooki/unreal-blender-mcp Project-document.md | github |  | 한국어 통합 MCP 설계 문서(직접 열어 확인) | <https://github.com/tahooki/unreal-blender-mcp/blob/main/Project-document.md> |
| 10 | Aryeon0228/BlenderMCP | github |  | 한국어 README, 성능 수치(직접 열어 확인) | <https://github.com/Aryeon0228/BlenderMCP> |
| 11 | 블렌더 MCP 연결 원리, AI가 3D 게임 에셋 만드는 법 (tali.kr) | blog |  | 원리와 한계를 균형 있게 설명 | <https://tali.kr/blender-mcp-assets> |
| 12 | 블렌더 MCP 연결 완전 정복 (MKCGI) | blog | 2026-05 | 최신 연결 가이드 | <https://www.mkcgi.net/2026/05/mcp-ai-3d.html> |
| 13 | Mac에서 생성형 AI 클로드와 블랜더 MCP로 연결하기 (brunch) | blog |  | Mac 연결기 | <https://brunch.co.kr/@soonkyujang/221> |
| 14 | 클로드 블렌더 커넥터 사용법 (Threads @dddesign.io) | community |  | 공식 커넥터 설치 실전 팁 | <https://www.threads.com/@dddesign.io/post/DXsWAspka7F/%ED%81%B4%EB%A1%9C%EB%93%9C-%EB%B8%94%EB%A0%8C%EB%93%9C-%EC%BB%A4%ED%85%8D%ED%84%B0-%EC%82%AC%EC%9A%A9%EB%B2%95%EA%B3%B5%EC%8B%9D-%EA%B0%80%EC%9D%B4%EB%93%9C%EA%B0%80-%EB%B6%88%EC%B9%9C%EC%A0%88%ED%95%B4%EC%84%9C-%EB%A7%8C%EB%93%AC1-claude-%EB%8D%B0%EC%8A%A4%ED%81%AC%ED%83%91-%EC%84%B8%ED%8C%85-%EC%BB%A4%EB%84%A5%ED%84%B0-%EC%9D%B4%EB%8F%992-blender-%EA%B2%80%EC%83%89-%EC%84%A0%ED%83%9D3-enbaled-%EB%88%84?hl=ko> |
| 15 | 블렌더(Blender) MCP를 활용해서 3D 모델링 업무 자동화하기 (YouTube) | youtube |  | 한국어 자동화 영상 | <https://www.youtube.com/watch?v=UU_iqziC6mE> |
| 16 | Claude가 내 2D 로봇을 3D 모델로 만들었다 (YouTube) | youtube |  | 이미지→3D→웹 사례 | <https://www.youtube.com/watch?v=I5rtlgAvoV4> |
| 17 | 클로드 AI 커넥터(MCP)로 스케치업 자동 모델링 + AI 렌더링 (뽁숑이) | youtube |  | 건축·인테리어 MCP 사례 | <https://www.youtube.com/watch?v=GOaWRhrsQC0> |
| 18 | GPT 6 x 블렌더 3D = 이제는 바이브 모델링 시대 (YouTube) | youtube | 2026-09 | Astra를 다룬 한국어 영상 | <https://www.youtube.com/watch?v=_S4SaiNBlRk> |
| 19 | Claude Code + Unity MCP 연동하기 (YouTube) | youtube |  | 유니티 연동 영상 | <https://www.youtube.com/watch?v=XauWsKw7nco> |
| 20 | 모델러 없는 개발자가 AI로 3D 에셋 자급자족하는 법 (ft. Meshy) - 인프런 클립 | course |  | 생성 메시 최적화 수치 | <https://www.inflearn.com/clip/570> |
| 21 | 3D 캐릭터 아티스트 채디의 블렌더와 AI로 연출하는 매력적인 캐릭터 모델링 (Coloso) | course |  | AI와 수작업을 결합한 하이브리드 강의 | <https://coloso.co.kr/products/3ddesign-chedy> |
| 22 | 3D 코딩 대결...클로드 오퍼스 5.5 vs GPT-5.6 (AI타임스) | news |  | 모델별 3D 역량 비교 | <https://www.aitimes.com/news/articleView.html?idxno=215618> |
| 23 | NC AI '바르코 3D' 출시 (시사저널e) | news |  | 국내 기업 AI 3D 사례 | <https://www.sisajournal-e.com/news/articleView.html?idxno=417470> |
| 24 | NC·크래프톤, 게임 AI 활용 확대 (아주경제) | news | 2026-07-14 | 국내 게임사 동향 | <https://www.ajunews.com/view/20260714153538647> |
| 25 | 블렌더 라이팅 독학 가이드 (유정통 3D) | blog |  | 라이팅 기초와 품질 팁 | <https://yujungtong.com/blender-lighting-and-color/> |
| 26 | 블렌더 재질·텍스처 완벽 가이드, PBR과 노드 랭글러 (유정통 3D) | blog |  | PBR 연결 실무 | <https://yujungtong.com/%EB%B8%94%EB%A0%8C%EB%8D%94-%EC%9E%85%EB%AC%B8%EC%9E%90-%ED%95%84%EB%8F%85-pbr-%ED%85%8D%EC%8A%A4%EC%B2%98-%EC%A0%81%EC%9A%A9-%ED%95%B5%EC%8B%AC/> |
| 27 | 인테리어 렌더링 퀄리티를 향상시키는 7가지 필수 팁 (아키스케치) | blog |  | 인테리어 렌더링 체크리스트 | <https://www.archisketch.com/en/blog/67ce4dcab7dabf0012869791> |
| 28 | 블렌더 3.0에서 인테리어 디자인 하기 (인프런) | course |  | 인테리어 모델링 기초 | <https://www.inflearn.com/course/%EB%B8%94%EB%A0%8C%EB%8D%94-%EC%9D%B8%ED%85%8C%EB%A6%AC%EC%96%B4-%EB%94%94%EC%9E%90%EC%9D%B8> |
| 29 | Hunyuan3D 소개 (파이토치 한국 사용자 모임) | community |  | 생성형 3D 기술 소개 | <https://discuss.pytorch.kr/t/hunyuan3d-tencent-3d/5451> |
| 30 | 클리앙 — AI로 모델링 이젠 수준급 바이브모델링 10분도 안걸려 | community |  | 국내 사용자 반응 | <https://www.clien.net/service/board/park/19015735> |
| 31 | 클리앙 — Astra(GPT-6)로 만든 결과물 | community | 2026-09 | Astra 결과물 반응 | <https://www.clien.net/service/board/park/19258409> |

<a id="g3_videos_cases"></a>
## [보완] 영상·소셜 사례

주제 원문: 영상 튜토리얼·소셜 사례·공식 벤더 워크스루 (영어/일본어/중국어): GPT-6 Astra, Claude Opus 5.5 / Fable 5.1, Gemini × Blender·Unreal·Unity·Roblox·SketchUp MCP

| # | 제목 | 유형 | 날짜 | 왜 유용한가 | URL |
|---|---|---|---|---|---|
| 1 | Claude for Creative Work (Anthropic) | official_announcement | 2026-04-28 (2026-05… | 공식 커넥터 9종, Blender 커넥터 기능, 기부 방식 정정을 본문으로 확인 | <https://www.anthropic.com/news/claude-for-creative-work> |
| 2 | Using the Blender Connector in Claude · Claude Academy | official_tutorial | 2026 | 공식 설정 절차와 Desktop 전용 제약 | <https://academy.claude.com/tutorials/using-the-blender-connector-in-claude> |
| 3 | Blender connector (claude.com) | official_directory | 2026-04 추가 / v1.0.1 | 제작자 Blender Lab, 버전, 검증 상태 | <https://claude.com/connectors/blender> |
| 4 | SketchUp connector (claude.com) | official_directory | 2026-04 | build_model/get_docs/save_model 도구 목록 | <https://claude.com/connectors/sketchup> |
| 5 | Unity plugin (claude.com) | official_directory | 2026-09 | Unity 공식 Claude Code 플러그인 존재 확인 | <https://claude.com/plugins/unity> |
| 6 | Unity-Technologies/unity-agent-plugin | github_official | v0.1.6-beta | 설치 명령, 스킬 목록, 요구 사양 | <https://github.com/Unity-Technologies/unity-agent-plugin> |
| 7 | lab/blender_mcp (Blender Projects) | official_repo | 2026 | 공식 Blender Lab MCP 저장소 | <https://projects.blender.org/lab/blender_mcp> |
| 8 | Blender Lab | official_site | 2026 | Blender Lab 프로그램 소개 | <https://www.blender.org/lab/> |
| 9 | Support the official Blender Lab MCP server as a provider · Issue #7 · claude-3d-harness | github_issue | 2026-09-20 | 공식 MCP의 최소 도구 세트와 하네스 통합 요건 | <https://github.com/MAX-786/claude-3d-harness/issues/7> |
| 10 | Architectural visualization with Astra \| OpenAI Developers | official_blog | 2026-09 | Astra 아크비즈 공식 워크플로(검색 요약) | <https://developers.openai.com/blog/architectural-visualization-with-astra> |
| 11 | Building games with Astra \| OpenAI Developers | official_blog | 2026-09 | Astra 게임 제작 공식 워크플로(검색 요약) | <https://developers.openai.com/blog/how-to-build-games-with-astra> |
| 12 | GPT-6 Astra: A new generation of intelligence \| OpenAI | official_announcement | 2026-09-03 | Astra 출시 1차 출처 | <https://openai.com/index/gpt-6-astra/> |
| 13 | Build a Playable Unreal Engine 5 Level with AI (MCP + Claude Code) \| Epic Community tuto… | community_tutorial_vendor_pla… | 2026 | Fab 팩 + AI 배치 워크플로 | <https://dev.epicgames.com/community/learning/tutorials/bnJ0/build-a-playable-unreal-engine-5-level-with-ai-mcp-claude-code> |
| 14 | Unreal Engine 5.8 + Claude (MCP): crear sin límites \| Epic Community tutorial | community_tutorial_vendor_pla… | 2026 | 스페인어 입문 | <https://dev.epicgames.com/community/learning/tutorials/39oR/unreal-engine-5-8-claude-mcp-crear-sin-limites> |
| 15 | Community Tutorial: UE 5.8 + Claude Code con MCP desde CERO (Epic Forums) | forum | 2026 | 스페인어 완전 튜토리얼 | <https://forums.unrealengine.com/t/community-tutorial-unreal-engine-5-8-claude-code-con-mcp-desde-cero-tutorial-completo/2729874> |
| 16 | Unreal Engine 5.8 Preview: MCP Configuration and Testing with Claude and Kilo (YouTube) | video | 2026-05-14 | Preview 시기 MCP 구성 | <https://www.youtube.com/watch?v=dKzyTiitRIA> |
| 17 | Easy MCP Server Setup For Unreal Engine 5.8 And Claude AI (YouTube) | video | 2026-05-28 | VS Code 기반 초보자 셋업 | <https://www.youtube.com/watch?v=z-nMc1BYW4Q> |
| 18 | UE5.8 MCP Server Setup & Test — Official MCP with Claude Code (YouTube) | video | 2026-06-18 | 정식 공식 MCP 셋업 | <https://www.youtube.com/watch?v=Ko3dy_G75-s> |
| 19 | How to Connect Claude Code to Unreal Engine 5.8 with MCP (YouTube) | video | 2026-07-01 | 셋업 튜토리얼 | <https://www.youtube.com/watch?v=kP9d-Bv32SU> |
| 20 | Claude Code + Unreal Engine 5.8: Complete MCP Setup & Tutorial (YouTube) | video | 2026-08-18 | 가장 최근 완전 튜토리얼 | <https://www.youtube.com/watch?v=hUNTOltVTpQ> |
| 21 | I Connected Fable 5.1 To The Official Unreal Engine 5.8 MCP (YouTube) | video | 2026 | Fable 5.1 × UE 공식 MCP 실험 | <https://www.youtube.com/watch?v=94QPi_bM0IE> |
| 22 | Unity MCP Server: Connect Claude Code, Cursor, and other AI Agents \| Unity Blog | official_blog | 2026-05 | Unity 공식 MCP 소개 | <https://unity.com/blog/unity-ai-mcp-how-to-get-started> |
| 23 | Unity MCP \| Assistant 2.0.0-pre.1 (Unity Docs) | official_docs | 2026 | relay/IPC/승인 정책 | <https://docs.unity3d.com/Packages/com.unity.ai.assistant@2.0/manual/unity-mcp-overview.html> |
| 24 | Claude AI + MCP in Unity: The Complete Setup & Workflow (2026) (YouTube) | video | 2026-07 | Unity 셋업 영상 | <https://www.youtube.com/watch?v=UZCekUCWgGc> |
| 25 | How to Set Up Claude with Unity MCP in 3 Minutes (YouTube) | video | 2026 | 빠른 셋업 | <https://www.youtube.com/watch?v=oCqyOvcWf5M> |
| 26 | Unity MCP Complete Guide (gamedevllm) | blog | 2026 | `unity mcp configure claude-code`, 공식 플러그인 배포일(9/10) 언급 | <https://gamedevllm.com/en/unity-mcp-claude-codex-gemini-cursorcomplete-guide-en/> |
| 27 | Roblox/studio-rust-mcp-server | github_official | 2026-04-03 deprecat… | 구 서버 도구 목록과 지원 종료 확인 | <https://github.com/Roblox/studio-rust-mcp-server> |
| 28 | Roblox Studio MCP server: build games with Claude (2026) — Loadout | blog | 2026 | 내장 MCP 활성화 경로와 포트 | <https://useloadout.com/blog/roblox-mcp-server-setup/> |
| 29 | How to Connect Claude to Roblox Studio (August 2026 MCP Guide) | blog | 2026-08 | 최신 Roblox 가이드 | <https://backyarddrunkard.com/game-guides/connect-claude-to-roblox-studio-mcp-guide/> |
| 30 | I Built a Roblox Game Using Only AI Agents (Medium, Andy.G) | blog_experience | 2026 | Roblox 실사용 체험 | <https://medium.com/@andy.a.g/i-built-a-roblox-game-using-only-ai-agents-heres-what-happened-ed57b553facc> |
| 31 | Vibe Check: Opus 5.5 Is Pulling Our Codex Converts Back to Claude (Every) | review | 2026-09 | Opus 5.5 실사용 평가 | <https://every.to/vibe-check/vibe-check-opus-5-5-is-pulling-our-codex-converts-back-to-claude> |
| 32 | Vaibhav Sisinty on X: Opus 5.5 wildest demos thread | social | 2026-09-23 | 출시 직후 데모 큐레이션 | <https://x.com/VaibhavSisinty/status/2102667276252282952> |
| 33 | Claude OPUS 5.5 beats GPT 6 Astra in blender ? (YouTube) | video | ~2026-09-23 | 모델 비교 | <https://www.youtube.com/watch?v=Zgs9H8_RF3w> |
| 34 | Claude Opus 5.5 Is the New KING of 3D Design & Blender (YouTube) | video | 2026-09 | Opus 5.5 Blender 리뷰 | <https://www.youtube.com/watch?v=2M1TEH6JPKc> |
| 35 | I Tested Claude Fable 5 in Blender (5x Faster Than Opus 4.8) (YouTube) | video | 2026 | 속도 비교 주장 | <https://www.youtube.com/watch?v=hgl2zHnWwMg> |
| 36 | Claude Opus 5 + Blender MCP = Professional 3D Scenes (YouTube) | video | 2026 | Opus 5 씬 시연 | <https://www.youtube.com/watch?v=Ci9Xc-VPc04> |
| 37 | Astra + Blender MCP is kinda OP (YouTube Shorts) | video | 2026-09 | Astra MCP 데모 | <https://www.youtube.com/shorts/8fChl1944vg> |
| 38 | How To Connect Claude To Blender - Tutorial (YouTube) | video | 2026 | 셋업 영상 | <https://www.youtube.com/watch?v=Zo4JBa2r2WI> |
| 39 | I Tested Gemini 3.8 Flash With Antigravity — Coding, Blender & More (YouTube) | video | ~2026-09 | Gemini Blender 테스트 | <https://www.youtube.com/watch?v=BAoecDDSB7Q> |
| 40 | Reference Image to 3D Scene With GPT-6 Astra & Blender (Vagon) | blog_tutorial | 2026-09 | 레퍼런스 → 씬 튜토리얼 | <https://vagon.io/blog/reference-image-to-3d-scene-with-gpt-6-astra-blender> |
| 41 | GPT-6 Astra: from brief to editable scene (Fraktal Journal) | blog_case | 2026-09 | 스튜디오 관점 건축 워크플로 | <https://fraktal.design/blog/gpt-6-astra-from-model-to-architecture-workflow/> |
| 42 | OpenAI's GPT-6 Astra Shows Unprecedented Blender 3D Animation Skills (Stork.AI) | blog | 2026-09 | Astra 애니메이션 평가 | <https://www.stork.ai/blog/astras-blender-skills-are-unreal> |
| 43 | Blender with OpenAI Astra: Complete Guide + Starter Files (Kingy AI) | blog_tutorial | 2026-09 | 스타터 파일 | <https://kingy.ai/blog/blender-openai-astra-complete-guide/> |
| 44 | How To Connect Blender To Astra, Gemini CLI & Claude (AceCloud) | blog_tutorial | 2026-09 | 세 경로 비교 | <https://acecloud.ai/blog/connect-blender-astra-gemini-claude/> |
| 45 | GPT-6 Astra Review - How I AI (ChatPRD) | review | 2026-09 | 실사용 리뷰 | <https://www.chatprd.ai/how-i-ai/gpt-6-astra-review-hardware-3d-games-and-coding> |
| 46 | GPT-6 Astra 3D Generation: Incredible Examples So Far (Aituts) | blog_roundup | 2026-09 | 게임 데모 모음 | <https://aituts.com/gpt6-astra-game-demos/> |
| 47 | GPT-6 Astra Early Access: The First Real-World Builds (atoms.dev) | blog_roundup | 2026-09 | 얼리 액세스 사례 | <https://atoms.dev/blog/gpt-6-astra-early-access-examples> |
| 48 | Built with Astra (eChai) | showcase | 2026-09 | Astra 제작물 쇼케이스 | <https://echai.ventures/astra> |
| 49 | Claude Opus 5.5 + Blender MCP: Setup & What Changed (blendermcp.org) | blog_tutorial | 2026-09 | Opus 5.5 출시일·비용 문구 | <https://blendermcp.org/guides/claude-opus-5-5-blender> |
| 50 | Gemini for Blender: Setup, Feedback Loops & Limits (blenderai.org) | blog_tutorial | 2026 | Gemini 시각 피드백 루프, httpUrl | <https://blenderai.org/models/gemini> |
| 51 | Blender MCP Setup for Codex, Claude Code, Cursor, VS Code, Gemini CLI (StraySpark) | blog_tutorial | 2026 | 클라이언트별 설정 | <https://www.strayspark.studio/blog/blender-mcp-setup-codex-cursor-gemini-vscode-2026> |
| 52 | [Project Showcase] Control Blender 3D using Gemini/LLMs via MCP (Google AI Developers For… | forum | 2026 | Gemini 커뮤니티 사례 | <https://discuss.ai.google.dev/t/project-showcase-control-blender-3d-using-gemini-llms-via-model-context-protocol-mcp/110424> |
| 53 | Astra時代のコードファースト3Dモデリング (zenn) | blog_ja | 2026-09 | 일본어 코드 퍼스트 논고 | <https://zenn.dev/koher/articles/code-first-3d-modeling> |
| 54 | GPT-6 AstraでBlenderを操作して桃をつくってみた (note) | blog_ja | 2026-09 | 일본어 체험기 | <https://note.com/ekazu_10/n/n31ffbf2e0646> |
| 55 | Dramatically Improved Blender Production Capabilities with GPT-6 Astra (npaka, note) | blog_ja | 2026-09 | 일본어 평가 | <https://note.com/npaka/n/n9635d06c377f?hl=en> |
| 56 | GPT-6 Astra + Codex + Blender MCP (Criet, note) | blog_ja | 2026-09 | 일본어 체험기 | <https://note.com/snapreplica/n/n77a3c9fae946?hl=en> |
| 57 | GPT-6 AstraでBlenderの3D制作はどこまでできる？ (chatgpt-consulting.jp) | blog_ja | 2026-09 | 일본어 가이드 | <https://chatgpt-consulting.jp/how-much-can-you-do-with-blender-3d-creation-using-gpt-6-astra/> |
| 58 | Cline + Blender MCP 3D model (AWS builders.flash) | vendor_blog_ja | 2025-06 | 일본어 초기 사례 | <https://aws.amazon.com/jp/builders-flash/202506/cline-blender-mcp-3d-model> |
| 59 | 使用 Blender MCP 使用 Claude AI 创建 3D - 完整 26 分钟教程 (bilibili) | video_zh | 2025~2026 | 중국어 완전 튜토리얼 | <https://www.bilibili.com/video/BV1SrXrY6E8D/> |
| 60 | Claude + Blender 联动教程 - 利用 MCP 实现 AI 自动化 3D 工作流 (bilibili) | video_zh | 2026 | 공식 MCP 자동화 활용 | <https://www.bilibili.com/video/BV1PBLS6sEEA/> |
| 61 | 中文配音-Claude Code + Blender MCP：零基础一键生成 3D 环境 (bilibili) | video_zh | 2026 | Claude Code 환경 생성 | <https://www.bilibili.com/video/BV1RKXNBMEDX/> |
| 62 | AI操控电脑自主构建3D场景！BlenderMCP (bilibili) | video_zh | 2025 | BlenderMCP 소개 | <https://www.bilibili.com/video/BV1BVQBYuEPg/> |
| 63 | Blender将永远改变：Claude AI的到来 (bilibili) | video_zh | 2026 | 중국어권 반응 | <https://www.bilibili.com/video/BV1JZVu6aEXh/> |
| 64 | 3D建模终结者？Blender + MCP打造极致3D建模场景 (bilibili) | video_zh | 2025 | 효과 평가 영상 | <https://www.bilibili.com/video/BV1JTQ4YyE2N/> |
| 65 | 过了把3D建模的瘾！MCP让Cursor控制Blender (知乎) | blog_zh | 2025 | three.js 재구성 아이디어 | <https://zhuanlan.zhihu.com/p/29863179256?utm_psn=1883459135720380238> |
| 66 | Show HN: MCP server for Blender that builds 3D scenes via natural language | forum | 2025-07-20 | HN 토론 | <https://news.ycombinator.com/item?id=44622374> |
| 67 | Anthropic Joins the Blender Development Fund as Corporate Patron (HN) | forum | 2026-04 | 후원 관련 토론(이후 일회성 기부로 정정) | <https://news.ycombinator.com/item?id=47936370> |
| 68 | Fable 5.1 World Modeling (HN) | forum | 2026 | Fable 5.1 월드 모델링 토론 | <https://news.ycombinator.com/item?id=49541458> |
| 69 | From Blender MCP to 3D-Agent... Anthropic partners with Blender (Blender Artists) | forum | 2026-04~ | 아티스트 커뮤니티 반응 | <https://blenderartists.org/t/from-blender-mcp-to-3d-agent-anthropic-partners-with-blender-claude-ai-connector-now-official/1639106> |
| 70 | Blender MCP Server after Claude: MCP security for Blender scripting (Blender DevTalk) | forum | 2026 | 보안 논의 | <https://devtalk.blender.org/t/blender-mcp-server-after-claude-mcp-security-for-blender-scripting-3d-agent-notes/45131> |
| 71 | How to Use Blender MCP with Meshy MCP & Claude (2026 Guide) | vendor_tutorial | 2026 | 생성 MCP + Blender MCP 구성 | <https://www.meshy.ai/tutorials/blender-mcp-guide> |
| 72 | Generative 3D Tools Compared: Meshy, Rodin, Tripo, and CSM in April 2026 (StraySpark) | review | 2026-04 | 생성기 비교 | <https://www.strayspark.studio/blog/generative-3d-tools-comparison-meshy-rodin-tripo-csm-2026> |
| 73 | Best AI 3D Model Generator in 2026: I Tested 9 (Indie Hackers) | review | 2026 | 9종 실사용 비교 | <https://www.indiehackers.com/post/best-ai-3d-model-generator-in-2026-i-tested-9-of-the-best-and-here-is-what-i-found-70ecab1a0a> |
| 74 | Meshy vs Tripo vs Rodin vs Trellis: Best for Archviz (Visiomake) | review | 2026 | 아크비즈 관점 비교 | <https://visiomake.com/en/blog/best-ai-image-to-3d-tools-2026-comparison-archviz> |
| 75 | Unreal Engine AI: Claude and Gemini via MCP (Creative AI News) | blog | 2026 | UE 클라이언트 설정 자동 생성 | <https://www.creativeainews.com/articles/unreal-engine-ai-claude-gemini-mcp-2026/> |
| 76 | Blender MCP vs Unity MCP vs Unreal MCP (Mint) | blog | 2026 | 엔진별 MCP 비교 | <https://mint.gg/blog/3d-mcp-guide> |
| 77 | Claude Opus 5.5: 10 Amazing Things People Created (FavTutor) | blog_roundup | 2026-09 | Opus 5.5 사례 모음 | <https://favtutor.com/claude-opus-5-5-real-examples/> |
| 78 | Hyper3D: Claude Opus 5.5 3D Prompts & Examples | vendor_gallery | 2026-09 | 프롬프트 예시 | <https://hyper3d.ai/3d-prompts/models/claude-opus-5.5> |

<a id="g4_licensing_pricing"></a>
## [보완] 가격·라이선스·법규

주제 원문: 상용 약관·가격·라이선스·법규 (2026): AI 3D 생성 도구, 에셋 라이브러리, 스토어 AI 공개 규정, 저작권 및 AI 표시 의무

| # | 제목 | 유형 | 날짜 | 왜 유용한가 | URL |
|---|---|---|---|---|---|
| 1 | Tencent Hunyuan3D-2.1 LICENSE (GitHub 원문) | license text | 2025-06-13 | Territory(EU·UK·KR 제외), Output, MAU, 타 모델 개선 금지 조항 원문 | <https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/blob/main/LICENSE> |
| 2 | Tencent Hunyuan3D-2 LICENSE (GitHub 원문) | license text | 2025-01-21 | 2.0 버전의 동일한 지역 제한 확인 | <https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/LICENSE> |
| 3 | microsoft/TRELLIS.2 (MIT) | license text | 2026-09 확인 | 지역 제한 없는 대안 모델의 라이선스 | <https://github.com/microsoft/TRELLIS.2> |
| 4 | Anthropic Commercial Terms of Service | official terms | 2025-06-17 | 출력물 소유, 양도, 면책, 학습 금지 원문 | <https://www.anthropic.com/legal/commercial-terms> |
| 5 | Anthropic Consumer Terms of Service | official terms | 2025-10-08 | 소비자 요금제 출력물 양도와 학습 옵트아웃 | <https://www.anthropic.com/legal/consumer-terms> |
| 6 | Gemini API Additional Terms of Service | official terms | 2026 | Google의 생성 콘텐츠 소유권 비주장 | <https://ai.google.dev/gemini-api/terms> |
| 7 | OpenAI Terms of Use | official terms | 2026 | 출력물 소유권 양도 조항 | <https://openai.com/policies/row-terms-of-use/> |
| 8 | Meshy Pricing | vendor pricing | 2026 | 플랜과 라이선스(공식) | <https://www.meshy.ai/pricing> |
| 9 | Meshy Pricing 2026 (costbench) | aggregator | 2026-08 | 플랜별 가격과 무료 플랜 CC BY 4.0 요약 | <https://costbench.com/software/ai-3d-generation/meshy/> |
| 10 | Tripo Pricing | vendor pricing | 2026 | 플랜별 상업권 | <https://www.tripo3d.ai/pricing> |
| 11 | Tripo AI Pricing 2026 (costbench) | aggregator | 2026-08-29 | 가격과 API 단가 요약 | <https://costbench.com/software/ai-3d-generation/tripo-ai/> |
| 12 | Hyper3D Pricing | vendor pricing | 2026 | Rodin 구독 플랜 | <https://hyper3d.ai/pricing> |
| 13 | Rodin Gen 2 blog | vendor blog | 2025-10 | Gen-2 기능 | <https://hyper3d.ai/blog/rodin-gen-2> |
| 14 | Marble pricing / billing docs | vendor docs | 2026 | 플랜별 상업권 | <https://docs.worldlabs.ai/marble/support/account-billing> |
| 15 | TechCrunch: World Labs launches Marble | news | 2025-11-12 | Marble 출시와 가격 | <https://techcrunch.com/2025/11/12/fei-fei-lis-world-labs-speeds-up-the-world-model-race-with-marble-its-first-commercial-product/> |
| 16 | Tencent Hunyuan Global: 3D Generation API | vendor page | 2026 | HY 3D 글로벌 API 제공 | <https://www.tencentcloud.com/techpedia/148311?lang=en> |
| 17 | Adobe: Firefly into Substance 3D workflows | vendor press | 2024-03-18 | Text to Texture, Generative Background 출시 | <https://news.adobe.com/news/news-details/2024/adobe-brings-firefly-generative-ai-into-substance-3d-workflows> |
| 18 | Adobe for creativity connector in Claude | vendor blog | 2026-04-28 | 커넥터 범위(50개 이상 도구) | <https://blog.adobe.com/en/publish/2026/04/28/adobe-for-creativity-connector> |
| 19 | Introducing Adobe for ChatGPT | vendor blog | 2026-08-06 | ChatGPT 플러그인 범위 | <https://blog.adobe.com/en/publish/2026/08/06/introducing-adobe-chatgpt-create-edit-get-work-done-all-in-chatgpt> |
| 20 | Fab Transition FAQs | vendor FAQ | 2024-2025 | Megascans의 Fab 전환 | <https://support.fab.com/s/article/Fab-Transition-FAQs?language=en_US> |
| 21 | CG Channel: Megascans free until end of 2024 | news | 2024-10 | Standard License의 엔진 무관 조건과 무료 종료 | <https://www.cgchannel.com/2024/10/epic-games-has-made-megascans-free-to-all-but-only-until-the-end-of-2024/> |
| 22 | Game Developer: Sketchfab mandates AI disclosure | news | 2025-11 | CreatedWithAI 의무화(2025-12-11), Fab AI 정책 | <https://www.gamedeveloper.com/business/sketchfab-to-require-mandatory-ai-disclosure-epic-games-accounts-for-users> |
| 23 | Poly Haven License | license page | 2026 | CC0 | <https://polyhaven.com/license> |
| 24 | Game Asset Licenses Explained (Cinevva) | guide | 2026 | ambientCG CC0, BlenderKit RF·CC0 설명 | <https://app.cinevva.com/guides/game-asset-licenses> |
| 25 | Game Developer: Valve tweaks and clarifies AI disclosure rules | news | 2026-01 | Steam 2026 개정 내용 | <https://www.gamedeveloper.com/business/valve-tweaks-and-clarifies-ai-disclosure-rules-for-steam> |
| 26 | U.S. Copyright Office NewsNet 1060 | government | 2025-01-29 | Part 2 보고서 발표 | <https://www.copyright.gov/newsnet/2025/1060.html> |
| 27 | Crowell: Part 2 of AI Report | law firm analysis | 2025-02 | 프롬프트 불충분, Thaler 사례 | <https://www.crowell.com/en/insights/client-alerts/us-copyright-office-releases-part-2-of-artificial-intelligence-report-clarifying-copyrightability-of-generative-ai-outputs> |
| 28 | 한국저작권위원회: 생성형 인공지능 활용 저작물의 저작권 등록 안내서 | government | 2025-06 | AI 활용 저작물 등록 기준 원문 | <https://www.copyright.or.kr/information-materials/publication/research-report/view.do?brdctsno=54253> |
| 29 | 전자신문: AI 활용 창작물도 등록 가능, 정부 첫 가이드라인 | news | 2025-07-01 | 등록 안내서 요지 | <https://www.etnews.com/20250701000303> |
| 30 | 법률신문: 문체부 공정이용 안내서 발간 | news | 2026-02 | 2026-02-26 공정이용 안내서 | <https://www.lawtimes.co.kr/news/articleView.html?idxno=217415> |
| 31 | 대한민국 정책브리핑: 인공지능기본법 22일 시행, 워터마크 표시 의무 | government | 2026-01 | 시행일, 표시 의무, 계도기간 | <https://www.korea.kr/news/policyNewsView.do?newsId=148958380> |
| 32 | 대륜: AI 기본법 시행령 과태료 계도기간 | law firm | 2026-01 | 계도기간 세부 | <https://www.daeryunlaw.com/newsletter/news/246> |
| 33 | Cooley: EU AI Act Transparency Obligations Take Effect 2 August 2026 | law firm analysis | 2026-08-03 | 제50조 적용, Omnibus 영향 | <https://www.cooley.com/news/insight/2026/2026-08-03-eu-ai-act-transparency-obligations-take-effect-2-august-2026> |
| 34 | EU Code of Practice on Transparency of AI-generated Content | government | 2026 | 표시 의무 준수 경로 | <https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content> |

<a id="g5_aaa_practice"></a>
## [보완] AAA 실무·공식 변경사항

주제 원문: AAA 아트 디렉션·라이팅·렌더링 실무 가이드 + Blender 5.x / Unreal Engine 5.7–5.8 공식 변경점 (2026-09 기준)

| # | 제목 | 유형 | 날짜 | 왜 유용한가 | URL |
|---|---|---|---|---|---|
| 1 | Blender 5.0 Release Notes | 공식 릴리스 노트 | 2025-11 | 5.0 Cycles, EEVEE, API 변경의 1차 출처 | <https://developer.blender.org/docs/release_notes/5.0/> |
| 2 | Blender 5.0: Python API | 공식 릴리스 노트 | 2025-11 | MCP 스크립트 호환성에 영향을 주는 파괴적 변경 | <https://developer.blender.org/docs/release_notes/5.0/python_api/> |
| 3 | Blender 5.0: Color Management | 공식 릴리스 노트 | 2025-11 | ACEScg, ACES 2.0, AgX HDR | <https://developer.blender.org/docs/release_notes/5.0/color_management/> |
| 4 | EEVEE & Viewport - Blender 5.0 | 공식 릴리스 노트 | 2025-11 | EEVEE 식별자 변경 | <https://developer.blender.org/docs/release_notes/5.0/eevee/> |
| 5 | Blender 5.1 Release Notes | 공식 릴리스 노트 | 2026-03 | Python 3.13, 성능, 신규 노드 | <https://developer.blender.org/docs/release_notes/5.1/> |
| 6 | Blender 5.2 LTS Release Notes | 공식 릴리스 노트 | 2026-07 | 현재 안정판 기능 | <https://developer.blender.org/docs/release_notes/5.2/> |
| 7 | Blender 5.3 Release Notes (dev) | 공식 개발 문서 | 2026 | 다음 버전이 개발 중임을 확인 | <https://developer.blender.org/docs/release_notes/5.3/> |
| 8 | Blender 5.2 LTS is here: discover its 5 key features \| CG Channel | 업계 뉴스 | 2026-07 | 5.2 요약과 LTS 기간 교차 확인 | <https://www.cgchannel.com/2026/07/blender-5-2-lts-is-here-discover-its-5-key-features/> |
| 9 | Blender 5.1 is here: discover its 5 key features \| CG Channel | 업계 뉴스 | 2026-03 | 5.1 요약 교차 확인 | <https://www.cgchannel.com/2026/03/discover-5-key-features-in-blender-5-1/> |
| 10 | Blender 5.1 is here \| DIGITAL PRODUCTION | 업계 뉴스 | 2026-03-19 | 5.1 출시 시점 | <https://digitalproduction.com/2026/03/19/blender-5-1-is-here/> |
| 11 | Blender 5.2 LTS Released - Phoronix | 업계 뉴스 | 2026-07 | 5.2 교차 확인 | <https://www.phoronix.com/news/Blender-5.2-Released> |
| 12 | Light Objects - Blender 5.2 LTS Manual | 공식 매뉴얼 | 2026 | 라이트 단위(W, W/m²)와 노출 보정 | <https://docs.blender.org/manual/en/latest/render/lights/light_object.html> |
| 13 | Using Physically Correct Brightness in Cycles - Blendergrid | 실무 가이드 |  | Cycles 물리 밝기와 lux 범위 | <https://blendergrid.com/articles/cycles-physically-correct-brightness> |
| 14 | Unreal Engine 5.8 is now available | 공식 발표 | 2026-06-17 | 5.8 기능 1차 출처 | <https://www.unrealengine.com/news/unreal-engine-5-8-is-now-available> |
| 15 | Unreal Engine 5.8 Release Notes | 공식 릴리스 노트 | 2026-06 | 5.8 상세 | <https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes> |
| 16 | Unreal Engine 5.8 Performance Highlights - Tom Looman | 전문가 블로그 | 2026 | 5.8 성능 기능 해설 | <https://tomlooman.com/unreal-engine-5-8-performance-highlights/> |
| 17 | Unreal Engine 5.8 Debuts Lumen Lite and Production-Ready MegaLights (Guru3D) | 업계 뉴스 | 2026-06 | Lumen Lite 2배, Switch 2 60fps | <https://www.guru3d.com/story/unreal-engine-58-debuts-lumen-lite-and-productionready-megalights/> |
| 18 | Unreal Engine 5.7 is now available | 공식 발표 | 2025-11 | Substrate, PCG 정식화, MegaLights Beta | <https://www.unrealengine.com/news/unreal-engine-5-7-is-now-available> |
| 19 | Unreal Engine 5.7: foliage, PCG and in-Editor AI \| DIGITAL PRODUCTION | 업계 뉴스 | 2025-11-12 | 5.7 교차 확인 | <https://digitalproduction.com/2025/11/12/unreal-engine-5-7-foliage-pcg-and-in-editor-ai/> |
| 20 | Using Physical Lighting Units in Unreal Engine (5.8 docs) | 공식 문서 | 2026 | lux, EV100 기준 | <https://dev.epicgames.com/documentation/unreal-engine/using-physical-lighting-units-in-unreal-engine?lang=en-US> |
| 21 | Physical Lighting Units (UE 4.27 docs) | 공식 문서 |  | 태양, 달, 별 조도와 EV100 수치 | <https://docs.unrealengine.com/4.27/en-US/BuildingWorlds/LightingAndShadows/PhysicalLightUnits> |
| 22 | Lighting in Unreal with photography principles using PBL — Magnopus | 스튜디오 블로그 |  | 사진 원리 기반 물리 라이팅 실무 | <https://www.magnopus.com/blog/lighting-in-unreal-with-photography-principles> |
| 23 | Lumen Performance Guide (UE 5.8 docs) | 공식 문서 | 2026 | Lumen 품질과 성능 레버 | <https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-performance-guide-for-unreal-engine> |
| 24 | Lumen GI in UE5: Settings, Asset Prep, and Performance Tuning (2026) | 실무 블로그 | 2026 | Final Gather Quality 수치 | <https://bitsoulhosting.com/marketplace/blog/ue5-lumen-gi-settings-asset-prep-performance-2026> |
| 25 | Unreal MCP Plugin (UE 5.8): Setup, Limits, Alternatives \| Ludus AI | 실무 블로그 | 2026 | 공식 MCP 플러그인 셋업과 한계 | <https://ludusengine.com/blog/unreal-mcp-plugin-ue5-8-setup> |
| 26 | Epic's Official MCP Plugin Is Here (UE 5.8) \| StraySpark | 실무 블로그 | 2026 | 공식 MCP와 서드파티 비교 | <https://www.strayspark.studio/blog/epic-official-mcp-plugin-ue5-8-vs-third-party> |
| 27 | The Secret Ingredient to Photorealism — Blender Guru | 실무자 튜토리얼 |  | 다이내믹 레인지와 노출 원칙 | <https://andrew-price-a9bl.squarespace.com/tutorials/secret-ingredient-photorealism> |
| 28 | Cinematic Lighting in Blender • Creative Shrimp | 실무자 강좌 |  | Gleb Alexandrov 라이팅 강좌 | <https://www.creativeshrimp.com/cinematic-lighting-in-blender> |
| 29 | Interior Rendering: The Complete Guide [2026] - ArchRender | 실무 가이드 | 2026 | archviz 카메라, 샘플, 포털, 창 노출 | <https://www.archrender.ai/blog/interior-rendering-the-complete-guide-2026> |
| 30 | Modular Scene in UE4: Blockout, Vertex Paint, Decals (80.lv) | 80.lv 브레이크다운 |  | AAA식 모듈러 환경 워크플로 | <https://80.lv/articles/001agt-004adk-005cg-modular-scene-in-ue4-blockout-vertex-paint-decals> |
| 31 | SanXia Street 1940: Modular Approach, Trim Sheets, Decals (80.lv) | 80.lv 브레이크다운 |  | 트림 시트와 데칼 사례 | <https://80.lv/articles/005cg-001agt-sanxia-street-1940-modular-approach-trim-sheets-decals> |
| 32 | Get Away: Lighting & Composition in Environment Art (80.lv) | 80.lv 브레이크다운 |  | 구도와 라이팅 | <https://80.lv/articles/get-away-lighting-composition-in-environment-art> |
| 33 | Environment Art \| The Level Design Book | 실무 서적(웹) |  | 환경 아트 프로세스와 스토리텔링 | <https://book.leveldesignbook.com/process/env-art> |
| 34 | Environment Artist Playbook: From Blockout to Final Pass \| RMCAD | 교육 기관 블로그 |  | 블록아웃부터 최종 패스까지의 라이팅 단계 | <https://www.rmcad.edu/blog/environment-artist-playbook-from-blockout-to-final-pass/> |
| 35 | Why AI 3D Models Look Bad — and How to Fix It (Tripo) | 벤더 블로그 | 2025–2026 | AI 3D 결함 분류와 해결 | <https://www.tripo3d.ai/blog/why-ai-3d-models-look-bad> |
| 36 | Texel Density Standards for AAA First-Person Shooter Games? — polycount | 실무자 포럼 |  | 텍셀 밀도 관행 | <https://polycount.com/discussion/234887/texel-density-standards-for-aaa-first-person-shooter-games> |
| 37 | Beyond Extent │ Texel Density | 실무 해설 |  | 텍셀 밀도 원리 | <https://www.beyondextent.com/deep-dives/deepdive-texeldensity> |
| 38 | Kruithof curve (Wikipedia) | 백과사전 |  | 조도와 색온도의 쾌적성 관계 | <https://en.wikipedia.org/wiki/Kruithof_curve> |
| 39 | Illuminance Levels Indoors: Standard Lux Level Chart (Prana Air) | 업체 블로그 |  | 실내 공간별 lux | <https://www.pranaair.com/blog/us/illuminance-levels-indoors-the-standard-lux-levels/> |

<a id="g6_benchmarks_models"></a>
## [보완] 벤치마크·모델 비교

주제 원문: 최신 3D·CAD·공간지능 벤치마크와 프런티어 모델 정량 비교 (2026-09-27 기준)

| # | 제목 | 유형 | 날짜 | 왜 유용한가 | URL |
|---|---|---|---|---|---|
| 1 | ScoreIA La Forge results (open data, 2026-09-24) | GitHub 데이터 저장소 (직접 확인) | 2026-09-24 | MCP 전용 3D 과제의 최신 모델 8종 프로그램 채점 결과 | <https://github.com/drakkB/scoreia-forge-results> |
| 2 | arena-ai-leaderboards daily snapshots | GitHub 미러 (직접 확인) | 2026-09-26 | arena.ai Code, Vision, Text 보드의 최신 Elo와 CI, 투표 수 | <https://github.com/oolong-tea-2026/arena-ai-leaderboards> |
| 3 | Arena code.json snapshot 2026-09-26 | 데이터 파일 (직접 확인) | 2026-09-25 갱신 |  | <https://raw.githubusercontent.com/oolong-tea-2026/arena-ai-leaderboards/main/data/2026-09-26/code.json> |
| 4 | Arena vision.json snapshot 2026-09-26 | 데이터 파일 (직접 확인) | 2026-09-13 갱신 |  | <https://raw.githubusercontent.com/oolong-tea-2026/arena-ai-leaderboards/main/data/2026-09-26/vision.json> |
| 5 | Introducing Claude Opus 5.5 | 벤더 공식 발표 (직접 확인) | 2026-09-22 | OSWorld 2.0, Terminal-Bench 4.0 등 Astra 비교를 포함한 공식 표와 가격 | <https://www.anthropic.com/claude-opus-5-5> |
| 6 | Claude Fable 5.1 and Mythos 5.1 | 벤더 공식 발표 (직접 확인) | 2026-09 | OSWorld 2.0 partial/strict 등 공식 수치 | <https://www.anthropic.com/claude-fable-and-mythos-5-1> |
| 7 | Claude Sonnet 5 | 벤더 공식 발표 (직접 확인) | 2026-06-30 | Sonnet 5 수치는 차트 이미지뿐이라는 점 확인, 가격 $2/$10 | <https://www.anthropic.com/news/claude-sonnet-5> |
| 8 | GPT-6 Astra: A new generation of intelligence | 벤더 공식 발표 (차단, 검색 결과로만 확인) | 2026-09-03 |  | <https://openai.com/index/gpt-6-astra/> |
| 9 | GPT-6 Astra: Features, Benchmarks, and Pricing (DataCamp) | 2차 기사 |  | OSWorld 2.0 72.6%, ScreenSpot-Pro 92.7%, BenchCAD 95.9% 조건 설명 | <https://www.datacamp.com/blog/gpt-6-astra> |
| 10 | ScreenSpot Pro Leaderboard (BenchLM) | 집계 사이트 | 2026-09 |  | <https://benchlm.ai/benchmarks/screenspot-pro> |
| 11 | GPT-6 Astra Benchmark Results Analysis (DataLearnerAI) | 집계 사이트 |  | MMMU-Pro 86.9 | <https://www.datalearner.com/en/ai-models/pretrained-models/gpt-6-astra/analysis> |
| 12 | Best LLMs for 3D (modelgrep) | 집계 사이트 | 2026-09 | Design Arena 3D Elo | <https://modelgrep.com/best/3d> |
| 13 | Blender AI Leaderboard | 투표 아레나 (차단, 검색 요약) | 2026-09 |  | <https://blenderai.org/leaderboard> |
| 14 | Blender AI Arena Methodology | 아레나 방법론 (차단, 검색 결과) |  |  | <https://blenderai.org/methodology> |
| 15 | 3DCodeBench GitHub | GitHub (직접 확인) | 2026-06-01 |  | <https://github.com/gaoypeng/3dcodebench> |
| 16 | 3DCodeBench arXiv 2606.01057 | 학술 논문 (검색 요약) | 2026-06 |  | <https://arxiv.org/abs/2606.01057> |
| 17 | 3DHarnessBench arXiv 2609.06535 | 학술 논문 (검색 요약) | 2026-09 |  | <https://arxiv.org/html/2609.06535v1> |
| 18 | 3DHarnessBench GitHub | GitHub (직접 확인) |  |  | <https://github.com/llada60/3DHarnessBench> |
| 19 | BenchCAD LEADERBOARD.md | 공식 리더보드 (직접 확인) | 2026-06 |  | <https://github.com/BenchCAD/BenchCAD-main/blob/main/LEADERBOARD.md> |
| 20 | CADGenBench build123d-mcp comparison | 제3자 비교 문서 (직접 확인) | 2026-09 |  | <https://raw.githubusercontent.com/pzfreo/cadgenbench-build123d/main/GEMINI_OPUS_GPT56_MCP_COMPARISON.md> |
| 21 | CADWorld: Computer-Use Benchmark for Long-Horizon CAD | 학술 논문 (검색 요약) | 2026-09 |  | <https://arxiv.org/abs/2609.16251> |
| 22 | Gemini 3.8 Flash Benchmarks Explained (Vellum) | 2차 기사 | 2026-09 |  | <https://www.vellum.ai/blog/gemini-3-8-flash-benchmarks-explained> |
| 23 | Introducing Gemini 3.8 Flash and 3.8 Flash Cyber | 벤더 공식 (차단) | 2026-09-02 |  | <https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/> |
| 24 | Gemini 3.8 Flash: Benchmarks, Pricing and the Real Numbers (Fello AI) | 2차 기사 |  | 3.5 Pro 미출시 상태, OSWorld 2.0 59.0% | <https://felloai.com/gemini-3-8-flash/> |
| 25 | Grok 4.7 Release: Same Price, Longer Horizons (llm-stats) | 2차 기사 | 2026-09-21 |  | <https://llm-stats.com/blog/research/grok-4-7-launch> |
| 26 | xAI Launches Grok 4.7 (SQ Magazine) | 2차 기사 | 2026-09 |  | <https://sqmagazine.co.uk/xai-launches-grok-4-7-coding-model/> |
| 27 | GLM-5.3 vs Kimi K3 vs DeepSeek V4 Pro (Kingy AI) | 2차 기사 | 2026-08 |  | <https://kingy.ai/blog/glm-5-3-vs-kimi-k3-vs-deepseek-v4-pro/> |
| 28 | MineBench PR #152 (GPT-6 Astra Pro) | GitHub PR (직접 확인) | 2026-09-05 |  | <https://github.com/Ammaar-Alam/minebench/pull/152> |
| 29 | EASI issue #39 (GPT6 Astra) | GitHub 이슈 | 2026-09-12 | EASI에 Astra 평가 결과가 아직 없음 | <https://github.com/EvolvingLMMs-Lab/EASI/issues/39> |
| 30 | BlenderGym project page / leaderboard | 학술 프로젝트 페이지 (이전 세션 수집본 확인) | 2025 |  | <https://blendergym.github.io/> |
| 31 | VIGA arXiv 2601.11109 | 학술 논문 (검색 요약) | 2026-01 |  | <https://arxiv.org/abs/2601.11109> |
| 32 | Generating CAD Code with Vision-Language Models for 3D Designs (CADCodeVerify) | 학술 논문 (검색 요약) | 2024-10 |  | <https://arxiv.org/abs/2410.05340> |
| 33 | CAD-Recode arXiv 2412.14042 | 학술 논문 (검색 요약) | 2024-12 |  | <https://arxiv.org/pdf/2412.14042> |
| 34 | LayoutVLM arXiv 2412.02193 | 학술 논문 (검색 요약) | 2024-12 |  | <https://arxiv.org/html/2412.02193> |
| 35 | Holodeck arXiv 2312.09067 | 학술 논문 (검색 요약) | 2023-12 |  | <https://arxiv.org/html/2312.09067v2> |
| 36 | SceneSmith arXiv 2602.09153 | 학술 논문 (검색 요약) | 2026-02 |  | <https://arxiv.org/abs/2602.09153> |
| 37 | SceneCraft arXiv 2403.01248 | 학술 논문 (검색 요약) | 2024-03 |  | <https://arxiv.org/abs/2403.01248> |
| 38 | LL3M arXiv 2508.08228 | 학술 논문 (검색 요약) | 2025-08 |  | <https://arxiv.org/abs/2508.08228> |
| 39 | Claude Opus 5.5 WebDev Ranking Puts Anthropic Ahead of GPT-6 Astra (remio) | 2차 기사 | 2026-09-23 |  | <https://www.remio.ai/post/claude-opus-5-5-webdev-ranking-puts-anthropic-ahead-of-gpt-6-astra> |
| 40 | I Tried Claude Opus 5.5 vs GPT Astra in Blender (YouTube) | 영상 (내용 미확인, 존재만 확인) | 2026-09 |  | <https://www.youtube.com/watch?v=gr1v3ddUr7A> |

