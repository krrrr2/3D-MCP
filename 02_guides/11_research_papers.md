# 학술 연구 가이드: 3D 에이전트 연구에서 실무로 가져올 것

> 기준일: 2026-09-27 · 2023~2026년 LLM/VLM 3D 제작 연구 약 50편과 3D·CAD 벤치마크를 주제별로 정리하고, 연구들이 합의한 7가지 원칙을 Blender MCP 작업 순서 8단계로 옮겼습니다.

## 핵심 요약

- **연구 세대가 한두 세대 전입니다.** 확인한 논문은 대부분 GPT-4o/GPT-4V, Claude 3.5~3.7, GPT-5 세대로 실험했습니다. **GPT-6 Astra, Claude Fable 5.1, Opus 5.5를 직접 평가한 동료심사 논문은 찾지 못했습니다.** 논문 수치는 절대값이 아니라 "어느 방향이 효과가 있나"를 판단하는 근거로만 쓰세요.
- **7대 합의**: ① 렌더→비평 폐루프 ② 생성보다 검증에 연산 투자 ③ 좌표는 솔버, LLM은 관계·제약 ④ 처음부터 만들기보다 검색·재사용 ⑤ 파라메트릭 부품 코드 ⑥ 계층 단계 생성 + 물리 검증 ⑦ LLM은 렌더를 보지 않고는 결과를 상상하지 못함.
- **모델을 바꾸는 것보다 하네스를 고치는 효과가 더 큽니다.** 이미지→Blender 역설계 에이전트 VIGA는 원샷 대비 BlenderGym +35.32%, BlenderBench +124.70%였고(arXiv 요약 기준), CAD 벤치에서는 build123d-mcp 도구만 붙여도 같은 모델의 점수가 0.360에서 0.457로 올랐습니다(도구 저자 자체 보고, 2026-06). 3DHarnessBench에서도 도구 접근 범위를 넓히자 모든 모델이 개선됐습니다.
- **배치는 "충돌을 하드 조건으로 막고 배치 후 따로 검사"가 핵심입니다.** 같은 비교표(SceneReVis 측정)에서 충돌률은 LLM 직접 좌표 40.8% → 제약 솔버 12.7% → 렌더·평가·수정 루프 + 물리 보상 4.5%였습니다. 미분 최적화(충돌이 soft 손실 항)를 쓴 LayoutVLM도 36.8%였으니 "솔버만 쓰면 된다"로 일반화하면 안 됩니다.
- **아직 안 되는 것**: GPT-4o의 Blender 배치 편집 오차는 사람의 약 28배(BlenderGym)였고, VLM 검증기와 사람의 판정 일치율은 0.66(사람끼리 0.79)에 그쳤습니다. FreeCAD GUI를 클릭해 장기 작업을 하는 에이전트는 최고 17.5%로 전문가 87.0%에 크게 못 미쳤습니다. 메시 좌표를 토큰으로 직접 뽑는 방식(LLaMA-Mesh 등)은 저폴리에 머뭅니다.
- **최신 모델을 같은 조건으로 비교한 통제 벤치마크는 없습니다.** OpenAI가 발표한 BenchCAD "Astra 95.9%"(도구 사용, 벤더 자체 보고)와 공식 재채점 최고점 "Gemini 3.1 Pro 0.289"(도구 없음, IoU)는 척도가 달라 나란히 놓으면 안 됩니다. 절대 순위 대신 **과제별 잠정 선택**만 하세요([AI 모델 가이드](01_ai_models_and_clients.md)).
- **재현성 리스크가 실제로 터졌습니다.** LL3M은 논문에 쓴 Claude Sonnet 3.7이 retire되자(2026-02-19) 서버를 닫았습니다. Scene Language, BlenderGym의 Claude 기준선도 원래 설정으로는 돌아가지 않습니다. 프롬프트·툴 정의를 모델 중립으로 쓰고, 모델 ID·effort·Blender 버전을 로그에 남기세요.
- **[한국 사용자] 연구 코드 상당수가 비상업 라이선스입니다**(LL3M, LLaMA-Mesh, CAD-Recode, Text2CAD, CAD-Assistant, VLMaterial 데이터). SceneSmith·SceneAssistant·WorldClaw가 쓰는 **Hunyuan3D 계열 오픈웨이트는 라이선스 적용 지역에서 대한민국을 제외**합니다. 상업 작업에는 아이디어만 가져오세요.
- **실무 레시피 8단계**(7절): 레퍼런스 이미지 → 객체·관계 JSON → 파트별 함수 또는 에셋 검색·생성 → 솔버 배치와 충돌·물리 검사 → 4시점 렌더 → 체크리스트 비평 → 후보 비교·되돌리기 → 로그. 4~7단계는 이 저장소의 테스트된 스크립트([`scene_audit.py`, `placement_utils.py`, `review_views.py`](../03_playbooks/scripts/README.md))로 바로 돌릴 수 있습니다.

---

## 1. 이 문서를 읽는 법

### 1.1 수치 표기 규칙

| 표기 | 뜻 |
|---|---|
| (저자 보고) | 논문 저자가 자기 방법을 잰 값. 대부분의 학술 수치가 여기에 해당 |
| (경쟁 논문 측정) | 다른 논문이 비교 대상으로 다시 잰 값. 원 논문 수치와 다를 수 있음 |
| (arXiv 요약 기준) | arXiv가 조사 환경에서 차단되어 검색 요약으로만 확인한 값. 원문 표는 미열람 |
| (벤더 자체 보고) | 모델 제조사가 발표한 값 |
| (미검증 주장) | 독립 검증에서 신뢰도 문제가 지적된 출처의 값. 결론의 근거로 쓰지 않음 |
| (신뢰도 낮음) / (미확인) | 출처끼리 어긋나거나 1차 확인을 못 한 값 |

### 1.2 조사 환경의 한계

- arxiv.org, openreview, *.github.io, HuggingFace가 차단되어, 대부분의 사실은 **GitHub 공식 저장소 README, 프로젝트 페이지 소스(raw.githubusercontent.com), LICENSE 파일**로 확인했습니다. 논문 본문에만 있는 수치(SceneCraft의 CLIP 점수, LL3M 정량 평가, Articulate-Anything 성공률 등)는 확인하지 못했습니다.
- 학술 연구 조사의 핵심 주장은 독립 검증 에이전트가 다시 확인했고(판정 15건, 항목 점검 19건), 정정 내용을 이 문서에 반영했습니다. 벤치마크 보완 조사(G6) 수치는 일부만 AI 모델 조사 검증에서 교차 확인됐고, 나머지는 출처별 신뢰도로 표기했습니다([검증 로그](../01_research/verification_log.md)).
- 한국어 학술 자료(KCI, 국내 학회)는 조사하지 못했습니다.

---

## 2. 연구 7대 합의

| # | 합의 | 근거(수치) | 주의·반례 | 실무 적용 |
|---|---|---|---|---|
| 1 | **렌더→비평 폐루프가 표준** | SceneCraft, BlenderAlchemy, LL3M, [VIGA](https://github.com/Fugtemypt123/VIGA), CADCodeVerify, Articulate-Anything, SceneReVis, SceneSmith, Code2Worlds가 모두 "코드 → 실행 → 렌더 → 비평 → 수정" 루프를 씁니다. 원샷 생성은 기준선으로만 등장합니다. VIGA 원샷 대비 +35.32%(BlenderGym), +124.70%(BlenderBench)([arXiv 2601.11109](https://arxiv.org/abs/2601.11109), arXiv 요약 기준) | 렌더 비용이 큽니다(BlenderAlchemy). 비용이 문제면 SceneOrchestra처럼 전체 계획을 먼저 세우고 단계 경계에서만 렌더합니다 | 매 수정 뒤 [`review_views.py`](../03_playbooks/scripts/README.md)로 4방향 렌더 |
| 2 | **생성보다 검증에 연산을 쓴다** | [BlenderGym](https://raw.githubusercontent.com/BlenderGym/BlenderGym.github.io/main/index.html)(CVPR 2025 Highlight)은 검증 비율(VeriRatio) 0.33, 0.62, 0.73을 비교해 **적정 비율이 존재하고, 총 연산이 클수록 검증 비중을 높이는 편이 유리**함을 보였습니다. 검증기 추론을 늘린 오픈 모델이 폐쇄 모델 검증기를 넘기도 했습니다 | 조사 원본의 "최적 VeriRatio 0.62~0.73"은 **과잉 해석으로 정정**됐습니다(세 값만 실험). 검증기와 사람의 일치율은 Claude-3.5-Sonnet 0.66, 사람끼리 0.79 | 후보 2~3개를 만들어 렌더하고, 순서를 바꿔 두 번 비교 판정. 숫자 검사를 먼저 |
| 3 | **좌표는 솔버, LLM은 관계·제약** | [SceneReVis 비교표](https://raw.githubusercontent.com/SceneReVis/SceneReVis.github.io/main/index.html)(침실+거실 평균) 충돌률: LayoutGPT 40.8%, ReSpace 41.1%, DiffuScene 37.7%, LayoutVLM 36.8%, I-Design 16.2%, Holodeck 12.7%, SceneReVis 4.5%. Holodeck(DFS 솔버), I-Design(백트래킹), Infinigen Indoors(제약 언어 + 솔버)가 같은 방향입니다 | 모두 **경쟁 논문(SceneReVis)이 잰 값**입니다. 미분 최적화를 쓰는 LayoutVLM도 36.8%였으므로 "충돌을 **하드 조건**으로 막고 배치 후 따로 검사"가 핵심입니다. LLM 없이 프로그램 탐색으로 씬 오류를 고치는 연구([SIGGRAPH Asia 2025](https://arxiv.org/abs/2510.16147))도 같은 방향 | LLM은 `against_wall`, `in_front_of`, `face_to` 관계를 JSON으로, 좌표는 [`placement_utils.py`](../03_playbooks/scripts/README.md)·솔버가 계산([배치 가이드](08_scene_layout_placement.md)) |
| 4 | **처음부터 만들기보다 검색·재사용** | Holodeck(Objaverse 검색), I-Design(OpenShape), SceneSmith(HSSD/Objaverse/PartNet-Mobility), Make-it-Real(재질 라이브러리), LL3M(Blender API 문서 검색), SAGE(TRELLIS 에셋·MatFuse 재질 생성을 별도 서버로) | Objaverse 에셋은 품질 편차가 큽니다. AAA 룩이 필요하면 고품질 라이브러리로 교체합니다 | 유기체·조각은 생성 모델이나 라이브러리에서 가져오고, 코드는 정규화·배치·재질·조명을 맡음([3D 생성 가이드](04_ai_3d_generation.md)) |
| 5 | **파라메트릭 부품 코드** | 3D-GPT(생성 함수의 파라미터만 추론), SceneCraft(재사용 spatial skill library), Scene Language(loop·transform 프리미티브), MeshCoder(파트별 Blender 코드, 100만 쌍 학습), SceneMotifCoder(배열 모티프 프로그램), CADEvolve(파라메트릭 생성기 진화), [Procedura](https://arxiv.org/abs/2608.26238)(파트 프로그램 + 검증 가능한 결합) | 복잡한 유기 형상은 파라메트릭 코드로 잘 안 됩니다(4번과 병행) | `def make_chair(seat_h=0.45, ...)`처럼 함수부터 쓰고 파트에 이름을 붙임([모델링 가이드](07_modeling_objects_furniture_sculpture.md)) |
| 6 | **계층 단계 생성 + 물리 검증** | [SceneSmith](https://raw.githubusercontent.com/scenesmith/scenesmith.github.io/main/index.html)(ICML 2026 Spotlight): 평면도 → 가구 → 벽 부착물 → 천장 → 소품, 단계마다 designer/critic/orchestrator. 기존 대비 객체 3~6배, 객체 간 충돌 0(프로젝트 페이지; [arXiv 요약](https://arxiv.org/abs/2602.09153)에는 "2% 미만"), 시뮬레이션 후 96% 안정, 사용자 205명 연구에서 기준선 대비 평균 승률 사실감 92%·프롬프트 충실도 91%(저자 보고) | 로봇 시뮬레이션용 씬이라 조명·재질 미감은 따로 다듬어야 합니다 | 단계마다 게이트, 소품은 rigid body로 안착·안정성 검사([배치 가이드 4.7절](08_scene_layout_placement.md)) |
| 7 | **LLM은 렌더 없이 결과를 상상하지 못한다** | [SGP-Bench](https://raw.githubusercontent.com/sgp-bench/sgp-bench.github.io/main/index.html)(ICLR 2025 Spotlight): GPT-4o(2024-08-06)가 렌더 없이 SVG 프로그램의 의미를 맞힌 비율 64.8%(색 87.3%, 추론 50.4%), CAD 72.9%. SGP-MNIST에서는 모든 모델이 5.5~13.0%로 우연 수준(10%) | 2024~2025 모델 기준입니다 | 코드만 보고 "완료"라고 판단하지 않게 하고, 매번 렌더 이미지를 보여 줌 |

---

## 3. 아직 안 되는 것

| 한계 | 근거 | 실무 대응 |
|---|---|---|
| 사람에게 쉬운 Blender 편집도 VLM은 크게 뒤짐 | [BlenderGym](https://blendergym.github.io/) GPT-4o 대 사람(광도 손실 PL, 낮을수록 좋음): 블렌드셰이프 9.140 vs 0.934, **배치 11.89 vs 0.423(약 28배)**, 배치 Chamfer 11.22 vs 1.532, 지오메트리 6.747 vs 1.269, 조명 2.410 vs 1.239, 재질 3.653 vs 0.629. 배치 N-CLIP은 Claude 3.5 Sonnet 51.76, GPT-4o 30.38(낮을수록 좋음) | 격차가 가장 큰 배치는 솔버와 검사 스크립트에 맡깁니다 |
| VLM 판정을 사람만큼 믿을 수 없음 | BlenderGym: 검증기-사람 일치율 0.66 vs 사람끼리 0.79 | 숫자 검사 먼저, 판정은 순서를 바꿔 두 번, 최종 룩은 사람 |
| 코드만 보고 모양을 추론하지 못함 | SGP-Bench SGP-MNIST 5.5~13.0% | 매 반복 렌더 |
| 실행 성공 ≠ 올바른 형상 | 3DCodeBench: 실패는 주로 API 불일치에서 나오고, 렌더에 성공해도 떠 있거나 분리된 부품이 흔했습니다([arXiv 2606.01057](https://arxiv.org/abs/2606.01057), arXiv 요약 기준) | 실행 성공 뒤 [`scene_audit.py`](../03_playbooks/scripts/README.md)로 부유·관통 검사 |
| 소형 특화 모델은 범위가 좁음 | [BlenderLLM](https://github.com/FreedomIntelligence/BlenderLLM): 구문 오류율 3.4%로 범용 모델(15.6~21.4%)보다 낮지만, README가 스스로 "기본 모델링만, 멀티모달 입력 없음, 멀티턴 수정 없음"이라고 밝힘 | AAA 품질에는 프런티어 모델 + 렌더 루프 |
| 메시 좌표 직접 생성은 저폴리 | [LLaMA-Mesh](https://github.com/nv-tlabs/LLaMA-Mesh), [MeshLLM](https://github.com/Fangkang515/MeshLLM): 컨텍스트 길이 때문에 면 수가 제한됨 | 코드·절차적 모델링 또는 3D 생성 모델 + 리토폴로지 |
| GUI 클릭형 CAD 장기 작업 | [CADWorld](https://arxiv.org/abs/2609.16251)(FreeCAD GUI 200과제): 최고 GPT-5.4 17.5%, Opus 4.8 16.0%, 전문가 87.0%. Qwen3.6·MiniMax M3 등은 0~1.5%(arXiv 요약 기준) | GUI 조작보다 코드 CAD(CadQuery, build123d) + MCP |
| 분포 밖 입력에서 성능 저하 | [MeshCoder](https://github.com/InternRobotics/MeshCoder) README: TRELLIS 생성물 같은 입력에서 성능이 떨어짐 | 생성 메시 → 코드 역변환은 결과를 렌더로 확인 |
| 사소한 미감을 두고 끝없이 반복 | [3DCodeBench 비평 프롬프트](https://raw.githubusercontent.com/gaoypeng/3dcodebench/main/prompts/visual_critique_system_prompt_text.txt)가 "사소한 미감에 대한 과도한 반복을 피하고 큰 구조 문제만 지적"하라고 명시 | 종료 조건을 정하고, 룩 개발은 사람 단계로 분리 |
| 최신 모델·MCP 방식의 학술 평가 공백 | Astra·Fable 5.1·Opus 5.5 평가 논문 없음. **MCP 툴 호출과 직접 코드 실행을 비교한 학술 연구도 없음**(SAGE가 MCP 구현을 참고했다는 감사 문구 수준) | 자기 과제로 A/B 테스트 |
| "AAA급" 결과를 독립 검증한 사례 없음 | 연구 시스템은 대부분 로봇 시뮬레이션·데이터셋 생성용 | 연구는 구조(루프·솔버·검증)만 가져오고 미감은 [조명·렌더 가이드](06_lighting_rendering_art_direction.md)로 |

---

## 4. 주제별 주석 참고문헌

열 설명: **확인된 결과**에는 README·프로젝트 페이지·검증에서 확인된 수치만 적었습니다. 확인하지 못한 수치는 "(미확인)"입니다. **코드·라이선스**는 상업 파이프라인 사용 가능 여부 판단용입니다.

### 4.1 오브젝트 모델링 코드 에이전트·표현

| 연구 (학회·날짜) | 아이디어·핵심 기법 | 확인된 결과 | 코드·라이선스 | 실무 교훈 |
|---|---|---|---|---|
| [3D-GPT](https://github.com/Chuny1/3DGPT) (3DV 2025, arXiv 2310.12945) | 3개 에이전트(과제 분배·개념화·모델링)가 Infinigen 절차적 생성 함수의 **파라미터만** 추론. 함수 문서를 컨텍스트로 제공 | 정량 평가 제한적 | **점진 공개**: 에이전트 구현만 있고 수정 Infinigen·파서는 "upcoming". LICENSE 표기 없음, `openai==0.27.8`(구버전 API) 고정 | 지오메트리를 직접 짜게 하지 말고, 문서화된 생성기를 툴로 노출하고 LLM은 파라미터만 채우게 함 |
| [BlenderAlchemy](https://github.com/ianhuang0630/BlenderAlchemyOfficial) (ECCV 2024) | edit generator가 후보 편집 여러 개 → VLM이 렌더를 비교해 선택하는 트리 탐색. 텍스트 목표를 T2I "상상 이미지"로 만들어 기준으로 삼고, 나빠지면 이전 가설로 되돌림 | 정량 (미확인). [예제 config](https://raw.githubusercontent.com/ianhuang0630/BlenderAlchemyOfficial/main/configs/wood_to_marble.yaml): tree_dims `4x8`(깊이 4 × 폭 8), num_tries 4, edit_style `rewrite_code`, 동시 렌더 8, 동시 평가 4. **예제 config 값이지 코드 전역 기본값은 아님** | 코드 공개. Infinigen Blender 바이너리 전제. GPT-4V가 가장 좋았고 Gemini·Claude·Ollama 지원 | 편집 대상을 재질 노드 트리 하나처럼 좁히고, 후보 3~8개를 렌더 비교, 나빠지면 스냅샷 복귀 |
| [BlenderLLM](https://github.com/FreedomIntelligence/BlenderLLM) (arXiv 2412.14203, 2024-12) | Qwen2.5-Coder-7B를 BlendNet(지시-스크립트 12K쌍)으로 미세조정 + self-improvement | CADBench-Sim 0.748±0.085(GPT-4o 0.565). 구문 오류율 3.4%. 비교 모델 오류율은 15.6~21.4%인데, **어느 모델이 15.6%인지 조사끼리 어긋남**(Claude-3.5-Sonnet 또는 o1-Preview, README 표 재확인 필요) | Apache-2.0, 가중치 공개 | 도메인 파인튜닝은 "실행 가능률"을 올림. 평가 축(속성·공간 관계·지시 준수)은 자체 검수 체크리스트로 차용 |
| [LL3M](https://github.com/threedle/ll3m) (UChicago 3DL, 2025-08) | 역할 분담 멀티에이전트(README 기준 plan/retrieve/write/debug/refine) + **BlenderRAG**(Blender API 문서 검색)로 BMesh·modifier·셰이더 노드 활용 | 정량 (미확인). BlenderMCP 기준선보다 디테일이 좋고 연속 편집에서 정체성을 유지했다는 정성 비교 (신뢰도 낮음) | **[비상업 학술·평가 라이선스](https://raw.githubusercontent.com/threedle/ll3m/main/LICENSE)**. 저장소는 로그인형 데모의 클라이언트와 Blender 4.4 애드온뿐, 파이프라인 코드 비공개. **Claude Sonnet 3.7 retire로 서버 중단**([README](https://raw.githubusercontent.com/threedle/ll3m/main/README.md)) → 현재 사용 불가 | 쓰는 Blender 버전의 API 문서를 검색해 붙인다. 특정 모델 버전에 묶지 않는다 |
| [VIGA](https://github.com/Fugtemypt123/VIGA) (arXiv 2601.11109, 2026-01, ECCV 2026) | 한 에이전트가 Generator(계획·코드 실행·에셋 검색·씬 조회)와 Verifier(다중 시점 렌더 비교)를 번갈아 맡음. 계획·코드 diff·렌더 이력 메모리. 새 벤치 BlenderBench(Level 1~3) | 원샷 대비 BlenderGym +35.32%, SlideBench +117.17%, BlenderBench +124.70%(arXiv 요약 기준). 백본별 절대 점수 (미확인) | MIT, 스타 약 1.3k. conda 환경 4개(agent/blender/sam/sam3d), NVIDIA GPU 권장, 예제는 `--model=gpt-5` + SAM3D | 참조 이미지와 같은 카메라로 렌더해 나란히 비교, 반복마다 계획·diff·스크린샷 경로를 로그로 누적 |
| [MeshCoder](https://github.com/InternRobotics/MeshCoder) (NeurIPS 2025) | 점군 → **파트별로 나뉜 편집 가능한 Blender 코드**. 복잡한 형상용 고수준 API, 41 카테고리 100만 object-code 쌍으로 학습 | 기존보다 재구성 품질이 높고 코드 수정으로 형상·토폴로지 편집 가능(README). 분포 밖 입력에서 저하 | MIT. 2025-11에 코드·체크포인트·데이터 10만 쌍 공개. 후속 MegaParts(1.5, 최대 300파트·256K 토큰) 코드는 공개 예정 | 생성 메시를 파트 코드로 역변환. 프런티어 모델에도 "파트별 함수 + 고수준 API"로 모델링을 지시 |
| [LLaMA-Mesh](https://github.com/nv-tlabs/LLaMA-Mesh) (arXiv 2411.09595, 2024-11) | OBJ 텍스트(정점·면)를 그대로 토큰으로 LLaMA-3.1-8B SFT | 저폴리 한정(정확한 면 수 (미확인)) | **[NVIDIA License](https://raw.githubusercontent.com/nv-tlabs/LLaMA-Mesh/main/LICENSE) 3.3조: 연구·평가 목적 비상업만**. 학습 데이터 미공개 | 블록아웃 장난감 수준. AAA에는 코드·생성 모델 경로 |
| [MeshLLM](https://github.com/Fangkang515/MeshLLM) (ICCV 2025) | 메시를 primitive-mesh로 분해해 부분 조립으로 이해·생성, 150만+ 샘플 LoRA | README에 비교 수치 없음 | 코드 공개 | 큰 메시는 파트로 쪼개야 LLM이 다룸 → 프런티어 모델에도 파트 단위 제작 지시 |
| L3GO (NAACL 2025 Demo) | 에이전트가 부품을 하나씩 추가하며 위치·충돌 피드백을 받아 "다리 5개 의자" 같은 비관습 객체 조립 | (미확인) (신뢰도 낮음) | [공식 저장소](https://github.com/runopti/L3GO)가 비어 있음 | 부품 하나 추가할 때마다 bbox·접촉 확인 후 다음으로 |
| [Infinigen](https://github.com/princeton-vl/infinigen) / [ProcFunc](https://github.com/princeton-vl/procfunc) (Princeton) | Blender 기반 완전 절차적 자연·실내 생성기. ProcFunc는 geometry nodes ↔ Python 트랜스파일러와 함수형 API | ProcFunc 저장소가 **LLM/VLM 실험을 공개**([EXPERIMENTS.md](https://raw.githubusercontent.com/princeton-vl/procfunc/main/experiments/EXPERIMENTS.md): BlenderGym 재질·지오메트리 편집, 처음부터 생성). 조사 원본의 "LLM 언급 없음"은 정정됨 | Infinigen **BSD-3**(상용 가능). ProcFunc LICENSE 파일 404 → 라이선스 (미확인). ProcFunc는 `bpy==4.2.0`, Python 3.11, arXiv 2604.26943(2026-04 제출) | `uv run procfunc transpile x.blend --node_trees <트리> --output <파일>`로 기존 GN 에셋을 LLM이 편집할 수 있는 Python으로 변환. 3D-GPT·BlenderGym·BlenderAlchemy·3DCodeBench가 모두 Infinigen 위에서 동작 |
| [Procedura](https://arxiv.org/abs/2608.26238) (arXiv 2608.26238, 2026-08) | 부품을 파라메트릭 프로그램으로 만들고 **typed mate(기계적으로 검증 가능한 결합) + 솔버**로 조립. mate 게이트가 떠 있거나 파고드는 파트를 측정해 거부. 파트별 PBR 할당, material critic, 관절화 | 수치 (미확인). MechBench-36 사용, Gemini 3.7 Flash / GPT-5.6-sol 구성 | (미확인) | 가구·오브젝트를 "제대로" 만드는 문제에 가장 직접적인 2026 연구. 이 저장소의 조립 검사(`check_assembly()`, [모델링 가이드](07_modeling_objects_furniture_sculpture.md))가 같은 발상의 경량판 |

### 4.2 씬 레이아웃·배치 (2023~2025)

2026년 연구는 4.6절에 따로 모았습니다. 충돌률 비교는 [배치 가이드 1.1절](08_scene_layout_placement.md)에도 같은 표가 있습니다.

| 연구 (학회·날짜) | 아이디어·핵심 기법 | 확인된 결과 | 코드·라이선스 | 실무 교훈 |
|---|---|---|---|---|
| SceneCraft (ICML 2024, arXiv 2403.01248) | 텍스트 → 관계형 scene graph → Blender Python. inner loop는 GPT-4V가 렌더를 보고 제약 함수 수정, outer loop는 반복되는 수정을 **spatial skill library**로 축적(파인튜닝 없음) | BlenderGPT 계열보다 CLIP·제약 준수·사람 평가에서 앞선다고 보고(수치 (미확인)) | 공식 코드 못 찾음. **같은 이름의 다른 논문(NeurIPS 2024, layout-guided)과 혼동 주의** | 자주 쓰는 배치 함수(`place_on_surface`, `align_to_wall`)를 .py 라이브러리로 저장해 다음 씬에서 import |
| [LayoutGPT](https://github.com/weixi-feng/LayoutGPT) (NeurIPS 2023) | CSS 비슷한 레이아웃 형식 + 유사 예시 k개 in-context로 **LLM이 좌표를 직접** 출력 | 경계 이탈 24.7%, 충돌 40.8%, 품질 7.5/10(경쟁 논문 측정) | 코드 공개 | 좌표를 직접 받아야 한다면 few-shot + 사후 충돌·경계 검사 필수 |
| [Holodeck](https://github.com/allenai/Holodeck) (CVPR 2024, AI2) | LLM(현재 코드 기본 `gpt-4o-2024-05-13`)이 방 구조·객체 목록·**관계 제약**을 쓰고 DFS 솔버(2023-12 이전엔 MILP)가 좌표 계산, Objaverse 검색 | 경계 이탈 12.7%, 충돌 12.7%, 품질 7.8(경쟁 논문 측정). ProcTHOR 대비 전체 선호 64.4%(arXiv 요약 기준) | 코드 공개. 2023-12-28 이전 코드는 `--use_milp False` 필요 | LLM은 "벽에 붙임·가까이·마주봄·중앙 정렬"만 출력, 좌표는 솔버. Objaverse 에셋은 고품질로 교체 |
| [I-Design](https://github.com/atcelen/IDesign) (ECCV 2024) | Interior Designer·Architect·Engineer 에이전트가 대화로 scene graph를 만들고 백트래킹으로 배치. OpenShape 검색, Blender 배치, GPT-V 채점 | 경계 이탈 16.7%, 충돌 16.2%, 품질 7.8(경쟁 논문 측정) | 코드 공개. README에 Docker 안내 없음. 기본 설정이 `gpt-4`, `gpt-4-1106-preview`, `gpt-3.5-turbo-1106`(autogen)로 구형 고정 | 역할 분담 프롬프트(스타일 / 동선·치수 / 충돌·좌표)와 VLM 자동 채점 |
| Chat2Layout (IEEE TVCG 2025, arXiv 2407.21333) | 대화형 MLLM 가구 배치. 학습 없는 visual-text prompting, 정보량이 큰 최소 예시 선택(O2O-Search), 시각 피드백으로 갱신 | (미확인) | 코드 공개 여부 (미확인)([프로젝트 페이지 소스](https://raw.githubusercontent.com/CassieJuice/chat2layout/main/index.html)만 확인) | 결과 이미지를 다시 보여 주며 회전·스케일·재배치를 대화로 지시 |
| [LayoutVLM](https://github.com/sunfanyunn/LayoutVLM) (CVPR 2025, Stanford) | VLM이 초기 포즈 + 공간 관계를 함께 내고, 이를 **미분 가능 목적함수**(rotated IoU 등)로 바꿔 최적화 | 자체 논문: 11개 방 유형 평균 PSA 58.8로 I-Design보다 40.8점 높음([arXiv 요약](https://arxiv.org/html/2412.02193)). SceneReVis 측정에서는 충돌 36.8% | 코드 공개, Holodeck/Objaverse 전처리 호환 | 에셋마다 bbox·정면 방향을 정규화해 제공. 지표에 따라 순위가 바뀜 → 충돌은 따로 하드 검사 |
| [Global-Local Tree Search](https://github.com/dw-dengwei/TreeSearchGen) (CVPR 2025, arXiv 2503.18476) | 방 → 영역 → 바닥 객체 → 지지 객체의 계층 트리 탐색(기본 MCTS). VLM 공간 추론을 돕는 **이모지 격자 표현**(가구 0.3 m, 소품 0.1 m) | 정량 (미확인). 2026 확장판(arXiv 2606.06002)은 PRM-guided MCTS, Paint3D 재텍스처링, 3DTindo-Bench 추가 | Apache-2.0. Blender 3.3+, Holodeck 에셋 DB | VLM에게 원시 좌표 대신 top-down 격자 지도(셀 라벨)를 보여 주고 칸 단위로 고르게 함 |
| [DirectLayout](https://github.com/rxjfighting/DirectLayout) (NeurIPS 2025, arXiv 2506.05341) | CoT 공간 추론으로 수치 레이아웃 직접 생성, CoT 기반 레이아웃 보상, 에셋·레이아웃 반복 정렬 | (미확인) | 추론 파이프라인만 공개, 학습 모델 비공개(README는 최신 LLM으로 비슷한 결과 가능하다고 설명) | 통로 폭·가구 간 거리를 먼저 계산하게 하고, 실제 에셋 bbox를 받은 뒤 다시 정렬 |
| [SceneMotifCoder](https://github.com/3dlg-hcvc/smc) (3DV 2025 Oral) | 쌓인 접시 같은 예시에서 반복 배열 패턴(motif)을 meta-program으로 추출, LLM이 인스턴스화, 기하 최적화로 물리 타당성 확보 | (미확인) | MIT. HSSD(약 72 GB) 필요 | 책장·식기·진열대는 `stack`, `row`, `grid`, `scatter_on_surface` 같은 모티프 함수로 재사용 |
| [Scene Language](https://github.com/zzyunzhi/scene-language) (CVPR 2025 Highlight, arXiv 2410.16770) | 씬을 프로그램(계층·반복) + 단어(의미) + 임베딩(외형)으로 표현. LLM이 `transform_shape`, `loop`, `concat_shapes`로 Python 작성 | (미확인) | 코드 공개. README 권장·기본 모델은 **Claude 3.7 Sonnet**(예시 결과는 3.5 Sonnet). 둘 다 retire → `engine/constants.py`에서 모델 교체 필요 | 대칭·반복·계층(기둥 열, 도시 블록)은 loop와 함수로 |
| [SceneWeaver](https://github.com/Scene-Weaver/SceneWeaver) (NeurIPS 2025, arXiv 2509.20414) | reason-act-reflect 에이전트가 **tool card**(데이터 기반 초기화, LLM 배치, Infinigen 규칙, 에셋 검색, 수정 도구)에서 골라 반복 정제. 물리 타당성·시각 현실감·의미 정합 자기평가 | 정량 표 (미확인) | 코드 공개. Blender 3.6, Azure OpenAI 의존 | MCP 서버마다 "언제 쓰나·입력·출력·한계"를 1~3줄 tool card로 CLAUDE.md에 정리 |
| Scenethesis (ICLR 2026, arXiv 2505.02836) | LLM이 객체 범주·계층 초안 → 비전 모듈이 **가이던스 이미지**를 생성해 scene graph와 5DoF 포즈 추출 → 최적화로 충돌·안정성 보정 → judge가 공간 일관성 검증 | 정량 결과 없음(정성) | 코드 미공개([프로젝트 페이지 소스](https://raw.githubusercontent.com/scenethesis/Scenethesis/main/index.html)) | 텍스트만으로 배치하지 말고 컨셉 이미지를 먼저 만들고 거기서 위치·관계를 추출 |
| 3D-Generalist (3DV 2026, arXiv 2507.06484) | 레이아웃·재질·조명·에셋 편집을 액션으로 내는 VLM 정책 + self-improvement | (미확인) (신뢰도 낮음) | [공식 저장소](https://github.com/sunfanyunn/3D-Generalist) 비어 있음 | 씬 개선을 "액션 시퀀스"로 보는 관점만 참고 |

### 4.3 재질

| 연구 (학회·날짜) | 아이디어·핵심 기법 | 확인된 결과 | 코드·라이선스 | 실무 교훈 |
|---|---|---|---|---|
| [VLMaterial](https://github.com/mit-gfx/VLMaterial) (ICLR 2025 Spotlight, MIT) | 입력 이미지 → **Blender 셰이더 노드 그래프를 만드는 Python 프로그램**. LLaVA-NeXT(LLaMA-3 8B) LoRA, 상용 LLM(OpenAI API)으로 프로그램 구조 증강 + 노드 파라미터 증강 | (미확인) | 코드·가중치 **MIT**, 재질 데이터셋 **CC BY-NC 4.0(비상업)**. 파인튜닝에 48 GB 이상 VRAM 권장 | 재질은 텍스처를 그리게 하기보다 절차적 노드 코드로(해상도 무관, 편집 가능). 참조 사진과 렌더를 비교하며 파라미터 조정 |
| [Make-it-Real](https://github.com/Aleafy/Make_it_Real) (NeurIPS 2024) | GPT-4V가 부위별 재질을 인식·설명 → 설명이 달린 재질 라이브러리에서 매칭 → albedo·roughness·metallic·normal 맵 생성 | 정량 (미확인). GPT-4V가 재질을 효과적으로 인식함을 보임 | MIT, Blender 렌더 연동 | VLM에게 파트별 재질·색·거칠기 범위를 JSON으로 라벨링시키고 PBR 라이브러리(Poly Haven, ambientCG 등)에서 고르게 함([텍스처 가이드](05_texturing_materials.md)) |
| BlenderAlchemy (4.1절) | 재질 노드 스크립트를 후보 편집 + 렌더 비교로 수정(나무 → 대리석 시연) | 위 참조 | 위 참조 | 재질 편집도 후보 비교 + 되돌리기 |
| SAGE MatFuse, Procedura material critic (4.6절, 4.1절) | 재질 생성을 별도 서버로 분리(SAGE), 파트별 PBR 할당 뒤 재질 비평(Procedura) | (미확인) | 위 참조 | 재질 단계에 전용 비평자를 둠 |

BlenderGym 재질 과제에서 GPT-4o의 광도 손실은 3.653으로 사람(0.629)의 약 6배였습니다. 재질은 배치보다 격차가 작지만 여전히 사람 검수가 필요합니다.

### 4.4 CAD 코드 생성

| 연구 (학회·날짜) | 아이디어·핵심 기법 | 확인된 결과 | 코드·라이선스 | 실무 교훈 |
|---|---|---|---|---|
| [CAD-Recode](https://github.com/filaPro/cad-recode) (ICCV 2025, arXiv 2412.14042) | 점군 → CadQuery Python. Qwen2-1.5B + 선형층 1개, 절차적으로 만든 100만 CAD 시퀀스로 학습. v1.5(2025-03) | DeepCAD 평균 Chamfer 0.30(×10³, 이전 최고 3.43), IoU 92.0%, 모든 벤치에서 무효율 1% 미만([arXiv 요약](https://arxiv.org/pdf/2412.14042)) | **[CC BY-NC 4.0](https://raw.githubusercontent.com/filaPro/cad-recode/main/LICENSE.md)(비상업)**. HF 데모 있음 | 정밀 부품은 CadQuery·build123d 같은 코드 CAD로 만든 뒤 Blender로 가져옴. 생성 코드는 범용 LLM이 편집 가능 |
| [cadrille](https://github.com/col14m/cadrille) (arXiv 2505.22914, ICLR 2026) | 점군·이미지·텍스트 → CadQuery. SFT 후 **온라인 피드백 RL**(실행·기하 검증이 보상) | 2025-05 기준 DeepCAD·Fusion360·CC3D SOTA(저자 보고) | SFT·RL 가중치 공개, RL 학습 코드 비공개 | 실행 → 비교 → 재시도 루프가 품질을 크게 올린다는 근거 |
| [Text2CAD](https://github.com/SadilKhan/Text2CAD) (NeurIPS 2024 Spotlight) | 초보~전문가 수준 텍스트 → 파라메트릭 CAD 시퀀스. DeepCAD 기반 약 17만 모델, 텍스트 주석 약 66만 개 | (미확인) | 데이터·체크포인트·데모 공개, 학습 코드 비공개. **[CC BY-NC-SA 4.0](https://raw.githubusercontent.com/SadilKhan/Text2CAD/main/LICENSE)(비상업)** | 형용사 대신 **치수·스케치 평면·돌출 방향과 깊이**를 적은 전문가 수준 프롬프트일수록 정확 |
| [CADCodeVerify](https://github.com/Kamel773/CAD_Code_Generation) / CADPrompt (ICLR 2025, arXiv 2410.05340) | VLM이 렌더된 CAD 객체에 대해 **검증 질문을 스스로 만들고 답한 뒤**, 불일치를 코드 수정 피드백으로 사용. CADPrompt는 객체 200개(메시·설명·전문가 코드) | GPT-4 적용 시 점군 거리 7.30% 감소, 성공률 +5.0%([arXiv 요약](https://arxiv.org/abs/2410.05340)). 향상 폭은 크지 않음 | 코드·데이터 공개, 라이선스 (미확인) | 비평 프롬프트에서 "다리가 4개인가?", "좌판 높이가 폭의 절반쯤인가?" 같은 예/아니오 질문을 먼저 만들고 이미지로 답하게 한 뒤, "아니오"만 수정 |
| [CAD-Assistant](https://github.com/dimitrismallis/CAD-Assistant) (ICCV 2025, arXiv 2412.13810) | 툴 증강 VLLM이 FreeCAD Python API 코드를 생성·실행. 스케치 렌더 툴, 3D solid 인식기. SGP-Bench 2D/3D(1,700 파일)로 평가 | (미확인) | **Attribution-NonCommercial**. Docker 지원 | CAD 앱 MCP에도 "코드 실행 + 렌더 + 형상 질의" 툴 세트를 갖추면 범용 과제를 풀 수 있음 |
| [CADFusion](https://github.com/microsoft/CADFusion) (ICML 2025, Microsoft) | 텍스트→CAD LLM을 순차 학습과 **시각 피드백 단계(렌더 기반 선호 DPO)**로 번갈아 학습(v1.0 5라운드, v1.1 9라운드) | (미확인). 출력 .step/.stl/.obj, GPT-4o VLM 점수로 평가 | 코드·가중치 공개 | 렌더 기반 시각 평가가 코드 품질 개선의 핵심 신호 → 후보 여러 개를 렌더하고 VLM 선호로 고르기 |
| [CAD-Coder](https://github.com/anniedoris/CAD-Coder) / [Text-to-CadQuery](https://github.com/Text-to-CadQuery/Text-to-CadQuery) (2025) | 이미지 → CadQuery 오픈 VLM(이미지-스크립트 163K쌍) / Text2CAD 데이터를 CadQuery로 재주석해 오픈 LLM 6종 미세조정 | README에 비교 수치 없음 | 데이터·모델 공개 | **CadQuery가 LLM 친화적 CAD 표현으로 자리 잡음** |
| [CADEvolve](https://github.com/zhemdi/CADEvolve) (arXiv 2602.16317, 2026) | 수작업 CadQuery 시드 46개 → VLM이 이끄는 프로그램 편집 + 기하 검증으로 약 8,000개 파트 생성기 진화, 약 130만 스크립트 데이터셋 | (미확인) | 데이터·모델 공개(HF) | 가구·소품 함수 라이브러리를 LLM으로 늘릴 때: 기존 함수를 변형 → 실행·렌더 검증 → 통과한 것만 라이브러리에 편입 |

### 4.5 물리·관절·4D

| 연구 (학회·날짜) | 아이디어·핵심 기법 | 확인된 결과 | 코드·라이선스 | 실무 교훈 |
|---|---|---|---|---|
| [GPT4Motion](https://github.com/jiaxilv/GPT4Motion) (CVPR 2024 PBDL Workshop, Best Paper Runner-Up) | GPT-4가 Blender 물리 시뮬레이션(강체·천·유체) 스크립트를 쓰고, 렌더한 엣지·깊이 시퀀스를 ControlNet + SD에 넣어 영상 생성 | 기본 물리 시나리오 3가지 | 코드 공개(2024-04-16) | 물리적 움직임은 LLM이 상상하지 말고 시뮬레이터에 맡김. LLM은 질량·마찰·바람 같은 설정만 코드로 |
| [Articulate-Anything](https://github.com/vlongle/articulate-anything) (ICLR 2025, arXiv 2410.13882) | VLM actor-critic이 텍스트·이미지·비디오에서 URDF 코드 생성, 움직임 렌더를 critic이 보고 수정 | (미확인) | 코드 공개. `claude-3-5-sonnet` 옵션은 retire(2025-10-28)로 동작 안 함 | 문·서랍·경첩도 "코드 → 움직임 렌더 → 비평" 루프로 검증 |
| [Code2Worlds](https://github.com/AIGeeksGroup/Code2Worlds) (ICML 2026) | 검색 증강 객체 생성과 레이아웃 오케스트레이션을 분리한 dual-stream. 동역학 코드를 VLM-Motion Critic이 영상을 보고 수정. 렌더는 Infinigen | Code4D에서 SGS +41%, Richness +49%(저자 보고) | 코드 공개. Infinigen 설치 필요 | 애니메이션·물리도 "코드 → 시뮬레이션 → 프레임 비평 → 수정" 루프 |

### 4.6 2026년 흐름

| 흐름 | 대표 연구 | 핵심 기법·확인된 결과 | 코드·라이선스 | 실무 의미 |
|---|---|---|---|---|
| **시뮬레이션 준비 씬 대량 생성** | [SceneSmith](https://github.com/nepfaff/scenesmith) (ICML 2026 Spotlight, arXiv 2602.09153) | 5단계 계층 + designer/critic/orchestrator. SAM3D(32 GB)·Hunyuan3D-2(24 GB) 생성 또는 HSSD·Objaverse·PartNet-Mobility 검색, 관절·질량·관성 추정, +Y forward / Z up 정규화, Drake(네이티브)·MuJoCo·USD(실험적) 출력. 결과는 2절 표. 자동 평가기와 사람 라벨 일치 99.7% | MIT. 기본 에이전트 GPT-5(OpenAI 키 필수). 전체 파이프라인 45 GB+ GPU 권장 | 에셋 방향·스케일 정규화, 단계별 체크포인트, 마지막 물리 시뮬레이션. **Hunyuan3D-2 경로는 한국에서 쓰지 말 것**(8절) |
| | [SAGE](https://github.com/NVlabs/sage) (CVPR 2026, arXiv 2602.10116, NVIDIA) | embodied 과제 → LLM(GPT)·VLM(Qwen) + TRELLIS 에셋 생성 + MatFuse 재질 + 레이아웃 솔버를 **서버/클라이언트 구조**로 조합해 Isaac Sim용 USD 생성. SAGE-10k: 10,000씬, 50개 방 유형, 565K개 생성 객체 | Apache-2.0(구성요소는 각자 라이선스). MCP 언급은 "MCP client/server 구현을 참고했다"는 감사 문구 수준 | 에셋 생성·재질 생성·레이아웃 솔버를 각각 별도 툴(MCP 서버)로 두는 아키텍처의 참고 사례 |
| | [SceneCode](https://github.com/wangpuyi/SceneCode) (arXiv 2605.19587) | planner-designer-critic 루프로 레이아웃, 객체는 5가지 코드 생성 전략 → **파트별 Blender Python + 관절 메타데이터** → 시뮬레이션 에셋(SDF)으로 컴파일 | 코드 공개, Blender 4.4, 체크포인트 재개. 수치 (미확인) | 가구를 통짜 메시가 아니라 파트 코드 + 관절로 만들면 서랍·문·높이 수정이 쉬움 |
| **멀티턴 RL 배치 모델** | [SceneReVis](https://github.com/Runder-sun/SceneReVis) (arXiv 2602.09432, 2026-02) | Render → Evaluate → Revise. 원자 연산 6개(add, move, rotate, scale, replace, remove)만 사용. SceneChain-12K(궤적 11,444개, 렌더 약 80K) SFT + voxel 물리 보상 GRPO로 7B 학습. 경계 이탈 2.0%, 충돌 4.5%, 품질 8.8/10(저자 보고) | MIT, [SceneReVis-7B](https://github.com/Runder-sun/SceneReVis) 체크포인트 공개, 3D-FUTURE/Objaverse 에셋 | MCP 편집 툴을 6개 원자 연산으로 제한하고 매 턴 렌더 + 충돌·경계 검사 결과를 돌려줌 |
| **효율화: 툴 호출 궤적 일괄 예측** | [SceneOrchestra](https://github.com/yunhe24/sceneorchestra) (ECCV 2026, arXiv 2604.19907) | SceneWeaver식 반복 대신 전체 툴 호출 시퀀스를 한 번에 예측. SFT + DPO orchestrator, 후보 순위를 매기는 discriminator 능력은 orchestrator로 증류되고 최종 씬은 orchestrator 혼자 생성. 잘못된 궤적은 기본 3회 재시도 | 코드 공개(신생). 효율 수치 (미확인) | 비용·시간이 문제면 "전체 계획 먼저 → 단계 경계에서만 렌더 검증" |
| **시각 피드백 에이전트** | [SceneAssistant](https://github.com/ROUJINN/SceneAssistant) (arXiv 2603.12238) | action API로 오픈 보캐뷸러리 씬 구성. 객체별 Hunyuan3D-2 생성, Z-Image 이미지, EEVEE 렌더. 약 20스텝 동안 **매 스텝 미리보기 PNG + JSON 씬 상태** | 코드 공개. 기본 모델 `gemini-3-flash-preview`. README에 TRELLIS 언급 없음(조사 원본 정정) | "이미지 + 구조화된 상태 JSON"을 매 턴 함께 모델에 줌 |
| | VIGA (4.1절) | Generator/Verifier 교대 + 진화형 메모리 | MIT | 반복 로그를 다음 턴 컨텍스트로 |
| **코딩 에이전트 벤치마크** | 3DCodeBench, 3DHarnessBench, VoxelCodeBench (5절) | Blender 5.0 절차적 모델링을 Claude Code·Codex·Gemini CLI 하네스로 평가, 3D 대상 복원을 도구 접근 수준별로 평가 | 5절 | 자기 파이프라인 회귀 테스트 재료 |
| **4D·물리** | Code2Worlds (4.5절) | 동역학 코드 + 영상 비평 | 코드 공개 | 애니메이션도 루프로 |
| **오픈월드** | [WorldClaw](https://github.com/Tencent-Hunyuan/Hunyuan3D-WorldClaw) (Tencent Hunyuan, arXiv 2608.05248, 2026-08-07) | 레이아웃 계획 → Hunyuan3D 에셋 생성 → 배치 → 지형 → 검증. 스타 약 1.3k | 2026-09 기준 README에 설치·라이선스·결과 없음 | 레벨 규모 파이프라인 설계 참고. **Hunyuan3D 기반이라 한국 라이선스 주의** |
| **파라메트릭 + 검증 가능한 결합** | Procedura, CADEvolve, ProcFunc (4.1절, 4.4절) | 파트 프로그램 + mate 검사, 생성기 진화, GN ↔ Python | 위 참조 | 부품 조립을 수치로 검사 |

**제목·번호만 확인한 후속 연구**(방법·결과 미확인, [hzxie 목록](https://github.com/hzxie/Awesome-3D-Scene-Generation)·[xdlbw 목록](https://github.com/xdlbw/Awesome-3D-Object-and-Scene-Generation) 기준): HOG-Layout(CVPR 2026), NaLA(ECCV 2026), R³L(ICML 2026), ReSpace(ICLR 2026, SceneReVis 표에 충돌 41.1%로 등장), OptiScene, MesaTask, SpatialGrammar, Code-as-Room, "Agentic 3D Scene Generation with Spatially Contextualized VLMs", HOLODECK 2.0(arXiv 2508.05899), WorldCraft(arXiv 2502.15601). CAD 쪽 신규 벤치 RealCADBench(arXiv 2609.03773), P3D-Bench(2606.11152), MUSE(2605.28579), CADENA(2608.00799), 검증기 없는 CAD 테스트 시간 확장(2608.09706)도 존재만 확인했습니다. hzxie 목록의 "IJCV 2026" 표기는 README에서 확인되지 않았습니다(arXiv 2505.05474 배지만 있음).

---

## 5. 벤치마크 현황

### 5.1 한눈에 보기

"최신 모델" 열은 GPT-6 Astra, Claude Fable 5.1, Opus 5.5가 들어 있는지를 뜻합니다.

| 벤치마크 | 재는 것 | 조건(도구·하네스·척도) | 최신 모델 | 확인된 결과 | 신뢰도 |
|---|---|---|---|---|---|
| [BlenderGym](https://github.com/richard-guyunqi/BlenderGym-Open) (CVPR 2025 Highlight, 2025-04) | 시작 씬 → 목표 씬 Blender 코드 편집. 수작업 씬 245개, 5개 과제(블렌드셰이프·배치·절차적 지오메트리·조명·절차적 재질) | generator + verifier VLM. PL·N-CLIP·Chamfer, 낮을수록 좋음 | 없음(2025 모델: GPT-4o, Claude 3.5, Gemini 1.5 Flash, Qwen2-VL 등) | 리더보드는 VLM 시스템 13개 + Human(조사 원본의 "20개 이상"은 정정). 대부분 과제 1위 GPT-4o, 배치는 PL/CD 기준 Gemini-1.5-flash, N-CLIP 기준 GPT-4o. 사람과의 격차는 3절 | 높음(프로젝트 페이지). 평가에 쓴 Claude 모델은 retire |
| BlenderBench ([VIGA](https://github.com/Fugtemypt123/VIGA), 2026) | 다단계 3D 편집(Level 1~3) | 에이전트 | 없음 | VIGA 원샷 대비 +124.70%(arXiv 요약 기준) | 중간 |
| [3DCodeBench](https://github.com/gaoypeng/3dcodebench) / 3DCodeArena (arXiv 2606.01057, 2026-06-01) | Blender 5.0 bpy 절차적 객체 모델링. 212 카테고리 × 60 seed = 12,720 인스턴스(Infinigen 레퍼런스) | text→3D, image→3D, 멀티턴(traceback 피드백, T=3), 코딩 에이전트 하네스(Claude Code·Codex·Gemini CLI·agy). 실행 가능률, SigLIP-2/DINOv3, Chamfer/Uni3D, LLM 심판, 사람 선호 Elo | 없음(GPT-5.5·Opus 4.7·Gemini 3.1 Pro 세대) | trial 82,042개, 생성 스크립트 81,605개, 에이전트 transcript 2,767개 공개(README 확인). 멀티턴 오류 피드백으로 평균 실행 가능률 0.69 → 0.97, Opus 4.7·GPT-5.5·GPT-5.4는 재시도 후 1.000, Elo 1위 GPT-5.5 1163(Gemini 3.1 Pro보다 16점 높음)(arXiv 요약 기준, **README에는 없어 미확인**) | 구조는 높음, 수치는 중간. 라이선스 표기가 README(MIT)와 [LICENSE](https://raw.githubusercontent.com/gaoypeng/3dcodebench/main/LICENSE)(Apache 2.0)로 어긋나고 factory 스크립트는 Infinigen BSD-3 → LICENSE 파일 기준으로 인용 |
| [3DHarnessBench](https://github.com/llada60/3DHarnessBench) (arXiv 2609.06535, 2026-09) | 3D 대상을 Blender Python으로 복원 | 단일 뷰 → 멀티뷰 → Active Visual(임의 시점 요청) → Full 3D Interaction(함수 호출로 대상 접근) | Astra는 GitHub 설정에 있음(arXiv v1 요약 목록엔 없음). Opus 5.5·Fable 5.1 없음 | 접근 범위가 넓을수록 모든 모델 개선. Opus 5가 Active Visual·Full 3D 모두 1위, Fable 5·GPT-5.6 Sol·Kimi K3·Qwen3.8 Max가 2군, Gemini 3.1 Pro·MiniMax M3는 Active Visual에서 약함([arXiv 요약](https://arxiv.org/html/2609.06535v1)). "최고 Uni3D 0.927"은 (미확인). SKILL.md·MCP 어댑터·뷰포트 전용 서비스 등 하네스 자산 공개 | 중간 |
| [SGP-Bench](https://github.com/sgp-bench/sgp-bench) (ICLR 2025 Spotlight) | 렌더 없이 SVG·CAD 프로그램 의미 이해 | 질의응답 | 없음 | 2절 7번 참조. Symbolic Instruction Tuning(72K) 제안 | 높음 |
| [VoxelCodeBench](https://github.com/facebookresearch/VoxelCodeBench) (Meta, arXiv 2604.02580) | Python 코드로 복셀 3D 장면 생성 | Unreal Engine 자동 실행 + 다중 카메라 스크린샷 평가. Claude(Bedrock)·Gemini·OpenAI 지원 | (미확인) | 모델별 결과 (미확인) | 중간 |
| [BenchCAD 공식](https://github.com/BenchCAD/BenchCAD-main/blob/main/LEADERBOARD.md) (2026-06 갱신) | 4뷰 렌더 → CadQuery(Vision2Code), Vision-QA, Code-QA. 106개 부품군·17,900 프로그램 | **도구 없음**, 원시 출력 직접 재채점. IoU-score = voxel IoU × 실행률(0~1) | 없음 | Gemini 3.1 Pro 0.289, Opus 4.7 0.269, Sonnet 4.6 0.222, GPT-5.3 0.179. 벤더 보고 † 행: Mythos 5 0.384, Opus 4.8 0.273 | 높음 |
| BenchCAD (OpenAI 발표, 2026-09-03) | 같은 이름, 다른 조건 | **도구 사용**(렌더 → 측정 → 수정), 기하 중첩 점수(%) | Astra·Fable 5.1 | Astra 95.9%, Fable 5.1 84.3%(OpenAI 측정), GPT-5.6 Sol 83.3%([2차 기사](https://www.datacamp.com/blog/gpt-6-astra)) | (벤더 자체 보고, 미확인). Anthropic 발표문에는 BenchCAD 수치 없음 |
| [CADGenBench + build123d-mcp](https://raw.githubusercontent.com/pzfreo/cadgenbench-build123d/main/GEMINI_OPUS_GPT56_MCP_COMPARISON.md) (2026-07~09) | [CADGenBench](https://github.com/huggingface/cadgenbench) 81 fixture 생성 + 편집, STEP 유효성 | 모델마다 하네스 다름(Claude Code / Codex / Antigravity), MCP 0.3.79~0.3.83 | 없음 | Opus 5(xhigh) 0.677 > GPT-5.6 Sol(xhigh) 0.532 > Gemini 3.7 Flash(high) 0.508, 셋 다 80/81 유효. 편집 점수는 비슷하고 차이는 생성에서. Opus 토큰 +44%, API 환산 약 $724.77. 도구만 붙여도 같은 모델이 0.360 → 0.457, 유효율 88% → 100%(2026-06) | 중간. 비교자가 build123d-mcp 저자 본인이고, Opus 값은 여러 제출 중 최고 제출, MCP 버전·하네스·실행 시기가 모두 다름. 저자도 토큰·비용 비교는 방향성만이라고 명시 |
| [CADWorld](https://arxiv.org/abs/2609.16251) (arXiv 2609.16251, 2026-09) | FreeCAD GUI 장기 작업 200개, 11개 기계 CAD 워크플로 | 컴퓨터 사용 에이전트 | 없음 | 3절 참조 | 중간(arXiv 요약 기준) |
| La Forge (ScoreIA, 2026-09-24) | 전용 MCP 툴(`enter_forge`/`forge_add`/`forge_keyframe`/`seal_forge`)로 갑옷 부품 조립 + 애니메이션 | 프로그램 채점(bbox, 관절각, 궤적). **하네스 다름**(Claude Code 서브에이전트 / Codex CLI / Grok CLI) | 있음 | 6개 캠페인 단순평균 Opus 5.5 99.8, Fable 5.1 99.4, Astra 97.9, Grok 4.7 96.2, GPT-6 Sol 94.6, Sonnet 5 81.1, Haiku 4.5 40.4. 차이는 지정 프레임 정밀 동작(taille-3: Opus 5.5 100, Astra 88.1, Sonnet 5 19.5)에서 크게 벌어졌고 정적 조립은 상위권이 거의 만점([결과 저장소](https://github.com/drakkB/scoreia-forge-results)) | **(미검증 주장)**: 모델 신원 자기 신고·미서명, 심판과 캠페인을 Claude Opus로 작성(주최 측이 편향 가능성 명시), 채점 규칙 사후 수정, Blender 모델링·텍스처 능력은 재지 않음 |
| Arena Code / Vision (2026-09-25 / 09-13 갱신) | 일반 코드·이미지 이해 사람 투표 Elo | 3D 전용 아님(대리 지표) | Code: 있음 / Vision: Opus 5.5 없음 | Code: Opus 5.5 max 1827±18(1,607표), Astra max 1792±11, Fable 5.1 max 1751±10([스냅샷](https://raw.githubusercontent.com/oolong-tea-2026/arena-ai-leaderboards/main/data/2026-09-26/code.json)). Vision: 상위 30개가 35점 안([스냅샷](https://raw.githubusercontent.com/oolong-tea-2026/arena-ai-leaderboards/main/data/2026-09-26/vision.json)) → 변별력 거의 없음 | 높음(제3자 미러) |
| Design Arena 3D | Three.js/WebGL 3D 장면 코드 사람 투표 | 집계 사이트 경유 | 일부 | Astra 1464, Kimi K3 1417, Fable 5.1 1415([modelgrep](https://modelgrep.com/best/3d)). Opus 5.5 점수 없음 | (신뢰도 낮음) |
| Blender AI Arena | Blender 결과물 사람 투표(Glicko-2) | 에이전트 제품(3D-Agent)과 원시 모델 혼재 | 있음 | 출처끼리 어긋남: "5자 동률(1,687표)" 대 "Opus 5.5 1897±79"([leaderboard](https://blenderai.org/leaderboard), 원문 차단) | (신뢰도 낮음, 미확인). Blender 재단 공식 사이트 아님 |
| MineBench | 복셀 건축 사람 투표(Bradley-Terry) | 도구 모드(`voxel.exec`) | Astra Pro 추가 | 순위 (미확인). Astra Pro(max reasoning) 15개 프롬프트 평균 25분 53.5초, 총 $34.71, 평균 JSON 128.53 MiB([PR #152](https://github.com/Ammaar-Alam/minebench/pull/152)) | 중간(비용·시간 데이터로만 유용) |
| CADArena | CAD | — | — | 사례 모음 목록에 "Opus 5.5 max 0.750, Astra 0.671, Fable 5.1 0.662"로 나오지만 보완 조사에서 벤치마크 자체를 확인하지 못함 | (미확인, 미검증 주장) |

### 5.2 비교하기 전에 확인할 조건

1. **도구 사용 여부와 척도.** BenchCAD가 대표 예입니다. 도구를 쓴 "95.9%"와 도구 없는 IoU "0.289"는 같은 이름의 다른 시험입니다. 한 표의 같은 열에 넣지 마세요.
2. **하네스.** Claude Code, Codex CLI, Antigravity, Grok CLI는 도구·컨텍스트 관리가 다릅니다. La Forge와 CADGenBench는 모델 비교가 아니라 "모델 + 하네스" 비교입니다.
3. **effort.** Codex에서 GPT-6 Astra의 기본 reasoning은 `low`입니다(단계는 low/medium/high/xhigh/max/ultra). Opus 5.5 기본 effort는 `medium`입니다. effort를 적지 않은 비교는 버리세요.
4. **partial/strict와 측정 주체.** 예: Fable 5.1의 OSWorld 2.0 partial은 자사 발표문 77.9%, Opus 5.5 발표문 80.7%, strict는 41.7%입니다([Fable 5.1 발표](https://www.anthropic.com/claude-fable-and-mythos-5-1), [Opus 5.5 발표](https://www.anthropic.com/claude-opus-5-5)). 참고로 Opus 5.5 발표문에는 3D·CAD·공간 추론 지표가 없습니다(시각 관련은 차트 인식 Chartography 89.0%뿐, 벤더 자체 보고).
5. **표본과 CI.** 출시 직후 모델은 표본이 적어 CI가 넓습니다(Arena Code Opus 5.5 ±18, Blender AI Arena ±79). CI가 겹치면 동률입니다.
6. **모델 세대.** 학술 벤치는 대부분 한두 세대 전 모델에서 멈춰 있습니다.

### 5.3 벤치마크에서 나온 실무 결론

- **하네스를 먼저 고치세요**: 멀티턴 오류 피드백, 렌더 → 다시점 검증 → 수정 루프, 전용 MCP 도구. 위 수치들이 모두 같은 방향입니다.
- **추가 시점 도구는 모델별로 A/B 하세요.** 3DHarnessBench Active Visual에서는 추가 시점이 어떤 모델에는 도움이, 어떤 모델에는 해가 됐습니다.
- **CAD는 GUI 클릭보다 코드 CAD + MCP.** CADWorld 17.5% 대 CADGenBench 80/81 유효.
- **자체 회귀 테스트는 프로그램 채점기로.** LLM 심판보다 bbox·접촉·치수 같은 결정적 검사가 재현됩니다. 이 저장소의 [`scene_audit.py`](../03_playbooks/scripts/README.md)가 그 역할을 합니다. 채점기를 특정 모델로 작성했다면 그 모델에 유리한 편향이 생길 수 있으니 규칙은 사람이 검토하세요.
- **과제별 잠정 선두**(모두 잠정, 최종 선택은 [AI 모델 가이드](01_ai_models_and_clients.md)):

| 과제 | 잠정 선두 | 근거와 한계 |
|---|---|---|
| 도구 없이 4뷰 → CAD 코드 | Gemini 3.1 Pro | BenchCAD 공식 0.289. 최신 세대 미등재 |
| 3D 대상 → Blender 코드 복원 | Opus 5 | 3DHarnessBench. Opus 5.5·Fable 5.1 미평가 |
| 코드 CAD 생성·편집 + MCP | Opus 5 | CADGenBench 0.677. 제3자 단일, Astra 미포함 |
| 도구 사용 CAD 재구성 | Astra | 95.9%(벤더 자체 보고, 미확인) |
| Three.js/WebGL 3D 장면 코드 | Astra | Design Arena 3D (신뢰도 낮음) |
| Blender 절차적 모델링 코드 | GPT-5.5(2026-06 세대 기준) | 3DCodeArena Elo(arXiv 요약 기준) |
| MCP 조립·타이밍 정밀 애니메이션 | Opus 5.5·Fable 5.1 | La Forge taille-3 (미검증 주장) |

---

## 6. 재현성 리스크

### 6.1 모델 retire로 멈춘 연구 코드

Anthropic 공식 일정([model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)): Claude 3.5 Sonnet 2025-10-28, Claude 3.7 Sonnet 2026-02-19(deprecation 공지 2025-10-28), Claude 3 Haiku 2026-04-20 retire.

| 연구 | 묶인 모델·환경 | 현재 상태 | 대응 |
|---|---|---|---|
| LL3M | Claude Sonnet 3.7 | **서버 중단, 사용 불가**. 파이프라인 코드도 비공개 | 아이디어(역할 분담 + API 문서 RAG)만 차용 |
| Scene Language | 기본 Claude 3.7 Sonnet(예시는 3.5 Sonnet) | 둘 다 retire | `engine/constants.py`에서 모델 교체 후 결과 재확인 |
| BlenderGym | Claude-3.5-Sonnet, Claude-3-Haiku 기준선 | 원래 조건으로 재현 불가 | 수치는 역사 기록으로만 |
| Articulate-Anything | `claude-3-5-sonnet` 옵션 | 해당 옵션 동작 안 함 | 다른 모델로 교체 |
| I-Design | `gpt-4`, `gpt-4-1106-preview`, `gpt-3.5-turbo-1106` | 구형 모델에 고정(현재 제공 여부는 확인 필요) | autogen 설정 교체 |
| 3D-GPT | `openai==0.27.8` | 구버전 SDK 고정 | 최신 SDK로 포팅 필요 |
| Holodeck | `gpt-4o-2024-05-13` | 스냅샷 이름 고정 | 모델 이름을 설정으로 분리 |
| SceneSmith, VIGA / SceneAssistant | 기본 GPT-5 / `gemini-3-flash-preview` | 모델 이름이 코드·예제에 고정(현재 제공 여부는 이번 조사에서 확인하지 않음) | 모델 이름을 설정으로 분리 |

### 6.2 Blender 버전 드리프트

연구 코드가 요구하는 Blender는 제각각입니다: TreeSearchGen 3.3+, SceneWeaver 3.6, BlenderAlchemy Infinigen 번들 바이너리, ProcFunc `bpy==4.2.0`(Python 3.11), LL3M·SceneCode 4.4, 3DCodeBench 5.0. 2026-09 현재 Blender 안정판은 **5.2.2**(2026-09-14)이고 4.5 LTS·4.2 LTS가 병행됩니다. PyPI `bpy`는 5.1부터 **Python 3.13 전용**, 5.0은 3.11입니다. 연구 코드를 최신판에서 돌리면 아래 API 차이에서 깨집니다.

| API | 바뀐 점 | 정정·출처 |
|---|---|---|
| EEVEE 엔진 식별자 | 5.0: `'BLENDER_EEVEE'`, 4.2~4.x: `'BLENDER_EEVEE_NEXT'` | Blender 소스로 교차 확인 |
| Noise Texture 출력 | 5.0 표시 이름 `Factor`, identifier는 여전히 `Fac` | 이름 대신 identifier로 찾기 |
| Musgrave Texture | 제거 → Noise Texture로 | **5.0이 아니라 4.1에서 제거**(3DCodeBench 참조 파일의 "5.0 변경점" 표현은 오해 소지) |
| `Mesh.use_auto_smooth` | 제거 → `shade_auto_smooth` / `shade_smooth_by_angle` | **4.1에서 제거** |
| `bgl` 모듈 | 제거 → `gpu` 모듈 | 5.0에서 제거(4.4에는 있음) |
| `Material.use_nodes`, `World.use_nodes` | 5.0에서 폐기 예고(노드 트리가 기본으로 존재) | `node_tree is None`일 때만 켜기 |
| 프리미티브 추가 | `location`을 안 주면 3D 커서 위치에 생성 | `location=(0,0,0)` 명시 |
| GeoNodes CaptureAttribute | `capture_items.new()` 필요 | 3DCodeBench 참조 파일 |

3DCodeBench의 [Blender 5.0 API 참조 파일](https://raw.githubusercontent.com/gaoypeng/3dcodebench/main/prompts/blender_5_api_reference.txt)은 CLAUDE.md에 넣기 좋은 함정 목록이지만, 위처럼 "언제 바뀌었나"가 틀린 항목이 있습니다. 버전 분기가 필요한 코드는 이렇게 씁니다(Blender 4.2.23 LTS, 5.0.1의 pip `bpy`로 실행 확인).

```python
import bpy
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE' if bpy.app.version >= (5, 0, 0) else 'BLENDER_EEVEE_NEXT'

mat = bpy.data.materials.new("Stone")
if mat.node_tree is None:                 # 4.x. 5.0+는 노드 트리가 기본으로 있고 use_nodes는 폐기 예정
    mat.use_nodes = True
nt = mat.node_tree
bsdf = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')   # 노드는 이름이 아니라 타입으로 찾기
noise = nt.nodes.new('ShaderNodeTexNoise')                          # Musgrave 대신 Noise
fac = next(s for s in noise.outputs if s.identifier == 'Fac')        # 5.0 표시 이름 'Factor', identifier 'Fac'
nt.links.new(fac, bsdf.inputs['Roughness'])

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.5))  # location을 항상 명시
obj = bpy.context.active_object
obj.data.materials.append(mat)
bpy.ops.object.shade_smooth_by_angle(angle=0.5236)                    # use_auto_smooth 대체
```

> **[한국 사용자] 노드 이름 번역 문제**: 한국어 UI에서 새 데이터 이름 번역이 켜져 있으면 `nodes["Principled BSDF"]` 같은 **노드 이름 조회가 실패**합니다. 3DCodeBench 참조 파일은 "GeoNodes 입력은 인덱스가 아니라 이름으로"라고 권하지만, 노드는 `type`/`bl_idname`으로, 소켓은 `identifier`로 찾는 편이 언어·버전 차이에 모두 안전합니다. 이 저장소 스크립트도 이 방식을 씁니다.

### 6.3 재현성 체크리스트

- [ ] 프롬프트·툴 정의·CLAUDE.md를 **모델 중립**으로 쓴다(특정 모델 이름·버릇에 기대지 않음).
- [ ] 로그에 **모델 ID, effort, 하네스(Claude Code/Codex 버전), MCP 서버 이름·버전, Blender 버전**을 남긴다. 공식 Blender Lab 서버와 ahujasid MCP for Blender는 도구 구성이 다르고, 둘 다 `localhost:9876`을 쓰니 동시에 켜지 않는다([Blender MCP 가이드](02_blender_mcp.md)).
- [ ] MCP 서버·`bpy`·Blender 버전을 고정한다(`@latest` 금지).
- [ ] 새 모델이 나오면 같은 과제 세트로 **회귀 테스트**한다. 3DCodeBench 카테고리 일부 + `scene_audit.py` 결정적 검사를 쓰면 LLM 심판 없이 비교할 수 있다.
- [ ] 최종 결과물은 **사람이 읽고 고칠 수 있는 .py**로 버전 관리한다(LL3M·Scene Language의 교훈).

---

## 7. Blender MCP 실무 레시피 8단계

연구 합의를 Blender MCP 작업 순서로 옮긴 것입니다. 어느 MCP 서버(공식 Blender Lab 커넥터, ahujasid MCP for Blender)를 쓰든 같은 순서가 통합니다. 전 과정 게이트는 [AAA 제작 플레이북](../03_playbooks/02_aaa_production_playbook.md), 스킬 형태는 [스킬 템플릿](../03_playbooks/templates/skills/blender-aaa-scene/SKILL.md)에 있습니다.

| 단계 | 할 일 | 근거 연구 | 이 저장소 도구 | 통과 조건 |
|---|---|---|---|---|
| ① 레퍼런스 | 참조·컨셉 이미지 2~3장 → 1장 선택 | BlenderAlchemy visual imagination, Scenethesis 가이던스 이미지 | [프롬프트 템플릿](../03_playbooks/03_prompt_templates.md) | 기준 이미지 1장 확정 |
| ② 계획 JSON | 객체 목록·치수·관계 제약을 JSON으로, 단계(평면도 → 가구 → 벽 → 천장 → 소품) 지정 | SceneCraft scene graph, Holodeck 제약, SceneSmith 5단계, I-Design 역할 분담 | [치수 기준표](../03_playbooks/05_reference_dimensions.md) | 모든 객체에 mm 치수, 객체당 제약 3~5개 |
| ③ 제작 | 파트별 파라메트릭 함수로 모델링, 유기체·조각은 에셋 검색·생성 후 정규화 | 3D-GPT, MeshCoder, Scene Language, Procedura / Holodeck, SceneSmith | [모델링 가이드](07_modeling_objects_furniture_sculpture.md), [3D 생성 가이드](04_ai_3d_generation.md) | 실행 오류 0(traceback 최대 3회 재시도) |
| ④ 배치·검사 | 좌표는 스크립트 솔버, 충돌·경계·부유·물리 안정성 검사 | Holodeck, LayoutVLM, SceneReVis, SceneSmith | `placement_utils.py`, `scene_audit.py` | 관통 0, 의도하지 않은 부유 0 |
| ⑤ 4시점 렌더 | 위(정사영)·정면·측면·3/4 | VIGA 다중 시점, TreeSearchGen 격자 지도 | `review_views.py` | 4장 생성 |
| ⑥ 체크리스트 비평 | 예/아니오 질문 + 큰 구조 문제만 | CADCodeVerify, 3DCodeBench 비평 프롬프트, BlenderGym 검증기 | [품질 체크리스트](../03_playbooks/04_quality_checklists.md) | `NEEDS_FIX: NO` |
| ⑦ 후보 비교·되돌리기 | 후보 2~3개 렌더 비교, 나빠지면 스냅샷 복귀 | BlenderAlchemy 트리 탐색·가설 되돌리기, BlenderGym 검증 연산 | `save_as_mainfile(copy=True)` | 이전보다 나은 후보만 채택 |
| ⑧ 로그 | 계획·코드 diff·렌더 경로·남은 문제·모델/버전 기록 | VIGA 진화형 메모리, SceneWeaver 단계 기록 | `progress.md` | 다음 턴이 최근 3회분을 읽음 |

### ① 레퍼런스·컨셉 이미지를 먼저 확보

- 텍스트 목표("북유럽풍 거실")는 VLM 비평의 기준으로 약합니다. BlenderAlchemy는 텍스트를 T2I로 그린 "상상 이미지"를, Scenethesis는 가이던스 이미지를 기준으로 삼았습니다.
- 이미지 생성 모델로 2~3장 → 1장 선택 → 객체 목록과 대략적 배치를 이미지에서 추출 → 이후 비평 때마다 첨부합니다.
- 치수는 이미지에서 추정하지 말고 표준값에서 가져옵니다(②).

### ② 객체 목록과 관계를 JSON으로 계획

좌표를 쓰게 하지 말고 관계만 쓰게 합니다. 조사 원본에 있던 예시 형식입니다.

```json
{
  "objects": [
    {"id": "sofa", "bbox": [2.1, 0.9, 0.8]},
    {"id": "coffee_table", "bbox": [1.2, 0.6, 0.45]},
    {"id": "tv_stand", "bbox": [1.8, 0.4, 0.5]}
  ],
  "relations": [
    ["sofa", "against_wall", "north"],
    ["coffee_table", "in_front_of", "sofa", 0.45],
    ["tv_stand", "face_to", "sofa"]
  ],
  "stage": "furniture"
}
```

- SceneSmith처럼 평면도 → 대형 가구 → 벽 부착물 → 천장 → 소품 순서로 단계를 나누고, 단계가 끝날 때마다 top-down과 눈높이 렌더로 게이트를 둡니다.
- 소품 단계에서는 받침면(테이블 상판, 선반) 목록을 먼저 뽑고 그 위에만 배치합니다.
- **[한국 사용자]** 한국 아파트 천장고·문·매트리스 규격은 미국 예시와 다릅니다. 치수는 [실측 치수 기준표](../03_playbooks/05_reference_dimensions.md)에서 mm 값으로 넘기세요.

### ③ 파트별 파라메트릭 함수, 또는 검색·생성

프롬프트 예(3D-GPT·MeshCoder·3DCodeBench [시스템 프롬프트](https://raw.githubusercontent.com/gaoypeng/3dcodebench/main/prompts/text_to_3d_system_prompt.txt)의 "파라메트릭 루프·bmesh·modifier·array/mirror" 방향을 따른 것):

```text
먼저 치수 표(좌판 높이 0.45 m, 좌판 폭 0.5 m, 다리 두께 0.035 m, 등받이 높이 0.4 m)를 써라.
그다음 def make_chair(seat_h=0.45, seat_w=0.5, leg_th=0.035, back_h=0.4)를 작성하고 호출하라.
파트 이름은 Seat, Backrest, Leg_FL/FR/BL/BR로 하고 모두 빈 부모 "Chair" 아래에 둔다.
파트마다 world bbox를 print해서 접촉과 부유를 스스로 확인하라.
노드와 소켓은 이름이 아니라 type과 identifier로 찾아라.
```

- 유기체·조각·고디테일 소품은 코드로 처음부터 만들지 말고 생성 모델이나 라이브러리에서 가져온 뒤, 코드로 **실제 치수 스케일, 원점(바닥 중앙), 방향(SceneSmith는 +Y forward / Z up, 이 저장소 스크립트는 정면 -Y)**을 정규화합니다. 규약은 한 곳에 고정하세요([배치 가이드 4.1절](08_scene_layout_placement.md)).
- 실행 오류는 traceback 전체를 돌려주고 3회 안팎 재시도합니다(3DCodeBench 멀티턴 T=3). 3번 실패하면 "기능을 줄인 최소 버전부터 다시"로 전략을 바꿉니다.
- Blender 버전별 API 함정(6.2절)과 쓰는 버전의 API 문서를 컨텍스트에 넣습니다(LL3M BlenderRAG).

### ④ 좌표는 솔버, 그리고 충돌·경계·물리 검사

- `placement_utils.py`의 `snap_to_floor`, `drop_to_surface`, `place_against_wall`, `place_next_to`, `face_towards`, `check_clearances`로 관계를 좌표로 바꿉니다. 솔버 전체 코드는 [배치 가이드 4.4절](08_scene_layout_placement.md)에 있습니다.
- 편집 툴은 SceneReVis처럼 소수의 원자 연산(add, move, rotate, scale, replace, remove)으로 제한하고, 매 턴 "상태 JSON + 4뷰 이미지 + 충돌 목록"을 함께 줍니다(SceneAssistant 패턴).
- 소품은 rigid body로 떨어뜨려 안착시키고 안정성을 봅니다. 검증된 코드와 함정(기본 충돌 여백 0.04 m 때문에 약 4 cm 떠서 멈춤)은 [배치 가이드 4.7절](08_scene_layout_placement.md)에 있습니다. 안정성만 볼 때의 예시 기준(60프레임, 2 cm 이상 이동 또는 5° 이상 회전이면 "불안정")은 조사자가 제안한 값이고, SceneSmith 설정은 1 m 이상 이동 또는 45° 이상 기울면 실패입니다.

### ⑤ 4시점 렌더

- `review_views.py`는 위(정사영)·정면·측면·3/4 원근을 오브젝트별 다른 색으로 렌더합니다. MCP로 GUI Blender에 붙었을 때는 `engine="BLENDER_WORKBENCH"`가 가장 빠르고, GPU 없는 헤드리스에서는 `engine="CYCLES"`만 동작합니다.
- 배치 판단용으로는 top-down 정사영 위에 격자와 객체 라벨을 얹어 "C7 셀", "D4–F8 영역"처럼 칸 단위로 말하게 하면 공간 추론 오류가 줄어듭니다(TreeSearchGen: 가구 0.3 m, 소품 0.1 m 격자).
- 사진을 재현할 때는 참조 이미지와 같은 카메라로 렌더해 나란히 비교합니다(VIGA).

### ⑥ 체크리스트 형식 비평

**숫자 검사가 먼저, 눈 검사는 그다음**입니다. `scene_audit.py` 결과(관통·부유·치수 이탈)를 먼저 고치고 나서 렌더를 비평시킵니다. 비평 프롬프트는 3DCodeBench [visual critique 형식](https://raw.githubusercontent.com/gaoypeng/3dcodebench/main/prompts/visual_critique_system_prompt_text.txt)과 CADCodeVerify의 자기 검증 질문을 합친 것입니다.

```text
기준 이미지와 설명, 그리고 4장의 렌더(top/front/side/persp)를 비교하라.
1) 먼저 예/아니오 질문 8~12개를 만들어라. 예: "다리가 4개인가?", "모든 다리가 바닥에 닿는가?",
   "좌판 높이가 폭의 약 0.9배로 보이는가?", "소파가 북쪽 벽에 붙어 있는가?"
2) 각 질문에 렌더를 근거로 답하라. 어느 뷰에서 확인했는지 적어라.
3) 누락 부품, 떠 있는 지오메트리, 비율 오류, 정렬 오류, 형태 오류만 100단어 이하 bullet로 적어라.
   사소한 미감(색감, 미세한 곡률)은 지적하지 마라.
4) 큰 구조 문제가 없으면 "NEEDS_FIX: NO", 있으면 "NEEDS_FIX: YES"와 수정할 코드를 써라.
```

- VLM 판정은 사람과 일치율이 0.66 수준입니다. 중요한 판정은 이미지 순서를 바꿔 두 번 묻고, 두 번 다 같은 결론일 때만 채택합니다.
- 룩 개발(조명·컬러 그레이딩)은 이 루프에서 빼서 사람 단계나 별도 단계로 넘깁니다.

### ⑦ 후보 비교와 되돌리기

- 편집 전에 스냅샷을 저장합니다. ahujasid 애드온은 `undo_push`를 부르지 않고 Claude Code `/rewind`는 Blender 상태를 되돌리지 못하므로, **저장한 파일이 유일하게 믿을 수 있는 롤백 수단**입니다([배치 가이드 4.10절](08_scene_layout_placement.md)).
- 예산이 허락하면 후보 2~3개를 만들어 렌더하고 비교 판정(토너먼트)으로 고릅니다. BlenderGym 결과대로 **총 예산이 클수록 생성보다 검증에 더 씁니다**.
- 종료 조건 예: `NEEDS_FIX: NO` 2회 연속 또는 최대 5회(조사자 제안), 또는 SceneSmith식 "항목별 점수 모두 기준 이상이면 종료, 최대 3라운드, 점수가 떨어지면 체크포인트로 롤백"([배치 가이드 4.9절](08_scene_layout_placement.md)).

④~⑦을 한 번에 돌리는 코드입니다. `execute_blender_code`는 호출마다 새 네임스페이스에서 실행되므로 매번 경로 추가와 import를 합니다(`engine="CYCLES"`로 Blender 4.2.23 LTS, 5.0.1의 pip `bpy` 헤드리스 실행 확인. Workbench는 GPU가 있는 GUI에서 쓰세요).

```python
import sys, os, json, bpy
sys.path.append(r"C:\path\to\3D-MCP\03_playbooks\scripts")   # 이 저장소를 받은 위치
import importlib, scene_audit, review_views
importlib.reload(scene_audit); importlib.reload(review_views)

n = 3                                             # 반복 번호
root = bpy.path.abspath("//")                    # 작업 .blend를 먼저 저장해 둘 것
os.makedirs(os.path.join(root, "snap"), exist_ok=True)   # 폴더가 없으면 저장이 실패함
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(root, "snap", f"v{n:02d}.blend"), copy=True)

report = scene_audit.audit_scene(floor_z=0.0)     # 숫자 검사 먼저
print(json.dumps(report["summary"], ensure_ascii=False))
for u in report["units"]:
    if u["issues"]:
        print(u["name"], u["issues"])

paths = review_views.render_review_views(         # 그다음 4방향 검토 렌더
    os.path.join(root, "review", f"v{n:02d}"),
    engine="BLENDER_WORKBENCH")                   # GUI 연결 시. 헤드리스·GPU 없음이면 "CYCLES"
print(paths)
```

> `BLENDER_MCP_SAFE_MODE=1`(ahujasid 서버)은 파일 I/O를 막아 import·스냅샷 저장·렌더 저장이 실패할 수 있습니다. 신뢰하는 로컬 작업에서만 끄거나, 스크립트 내용을 붙여 넣는 방식을 쓰세요([스크립트 사용법](../03_playbooks/scripts/README.md)). safe mode는 샌드박스가 아닙니다.

### ⑧ 계획·코드 diff·렌더 이력 로그

VIGA의 진화형 메모리처럼 반복마다 파일에 누적하고, 매 턴 시작 때 최근 3회분을 읽게 합니다.

```markdown
## 반복 3 — 2026-09-27 14:10
- 모델/effort/하네스: claude-opus-5-5 / high / Claude Code 2.1.x
- Blender / MCP 서버: 4.5 LTS / MCP for Blender 2.1.0
- 목표: 소파–커피테이블 간격 0.35~0.50 m 맞추기
- 변경: coffee_table move(0, +0.12, 0)  (diff: logs/v03.diff)
- 스냅샷: snap/v03.blend, 렌더: review/v03/{top,front,side,persp}.png
- audit: 관통 0, 부유 0 / 비평: NEEDS_FIX: NO (1회째)
- 남은 문제: 러그가 소파 앞다리 아래로 5 cm 부족
```

긴 세션에서 이전 결정을 잊고 같은 실수를 반복하는 일을 막고, 6.3절의 재현성 기록도 겸합니다. 되돌린 뒤에는 "이전 시도와 실패 이유"를 남겨 같은 수정을 반복하지 않게 합니다.

---

## 8. 한국 사용자 체크포인트

| 항목 | 내용 | 대응 |
|---|---|---|
| **Hunyuan3D 계열 라이선스** | [Hunyuan3D-2 라이선스](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2/main/LICENSE) 등 Tencent 오픈웨이트(2.0/2.1/Omni/Part 등)는 적용 지역에서 EU·영국·대한민국을 제외하고 출력물 사용도 제한합니다. SceneSmith(Hunyuan3D-2 경로), SceneAssistant(객체 생성)가 여기에 걸리고, WorldClaw도 Hunyuan3D로 에셋을 만듭니다(WorldClaw 자체 라이선스는 미확인) | 한국에서는 이 경로를 로컬로 쓰지 말고 검색·다른 생성기로 대체([3D 생성 가이드](04_ai_3d_generation.md), [라이선스 가이드](10_assets_pipeline_licensing.md)). Tencent Cloud API 약관은 별개(원문 미확인) |
| **비상업 연구 코드** | LL3M(학술·평가 전용), LLaMA-Mesh(NVIDIA 비상업), CAD-Recode(CC BY-NC 4.0), Text2CAD(CC BY-NC-SA 4.0), CAD-Assistant(Attribution-NonCommercial), VLMaterial 데이터(CC BY-NC 4.0) | 상업 파이프라인에는 아이디어만. 상용 가능한 것은 Infinigen(BSD-3), SceneSmith·SceneReVis·VIGA·MeshCoder·Make-it-Real·SceneMotifCoder(MIT), SAGE·TreeSearchGen·BlenderLLM(Apache-2.0) 등. 쓰기 전에 LICENSE 파일을 직접 확인 |
| **한국어 UI 현지화** | 새 데이터 이름 번역이 켜져 있으면 노드 이름 조회가 실패 | 노드는 `type`, 소켓은 `identifier`로(6.2절). 오브젝트 이름은 영어로 지어야 `scene_audit.py` 치수 검사가 동작 |
| **한국 치수 규격** | 연구 시스템의 치수 규칙(SceneSmith·Infinigen 등)은 미국·유럽 기준 | [실측 치수 기준표](../03_playbooks/05_reference_dimensions.md)의 한국 값을 mm로 넘김 |
| **한국어 학술 자료** | 이번 조사에서 KCI·국내 학회 자료는 조사하지 못함 | [한국어 자료 모음](../04_case_studies/02_korean_resources.md) 참고, 추가 조사 필요 |

---

## 흔한 실수와 해결

| 실수 | 결과 | 해결 |
|---|---|---|
| 논문 수치를 최신 모델 성능으로 읽음 | 기대치 과장 | 연구 세대(GPT-4o~GPT-5)를 확인하고 방향만 참고 |
| BenchCAD "95.9%"와 공식 IoU를 한 표에 둠 | 틀린 모델 순위 | 도구 사용·척도·측정 주체가 같은지 먼저 확인(5.2절) |
| "VeriRatio 0.62~0.73이 최적"을 규칙처럼 씀 | 근거 없는 고정 비율 | 세 값만 실험됨. "예산이 클수록 검증 비중을 늘린다"로 적용 |
| "솔버/최적화만 쓰면 충돌이 없다" | 여전히 관통 | 충돌은 하드 조건으로 + 배치 후 `scene_audit.py`로 따로 검사 |
| LLM에게 z 좌표까지 직접 쓰게 함 | 떠 있거나 박힌 가구 | z는 `snap_to_floor`·`drop_to_surface`로 계산 |
| 코드 실행 성공을 완료로 간주 | 부품이 떠 있거나 분리됨 | 숫자 검사 → 4뷰 렌더 → 체크리스트 비평 |
| 비평이 미세한 미감까지 지적하게 둠 | 끝없는 반복, 품질 저하 | 큰 구조 문제만, 종료 조건 명시 |
| 연구 코드의 모델 이름을 그대로 둠 | retire된 모델로 실행 실패(LL3M, Scene Language) | 모델 이름을 설정으로 분리, 모델 중립 프롬프트 |
| 3DCodeBench API 목록을 "5.0 변경점"으로 믿음 | 4.x에서 잘못된 분기 | 6.2절의 정정된 버전 정보를 사용 |
| 연구 코드의 라이선스를 "코드 공개"로만 봄 | 상업 사용 위반 | LICENSE 파일 확인, 비상업이면 아이디어만(8절) |
| effort를 적지 않고 모델 비교 | Codex Astra 기본 `low`로 품질 과소평가 | effort·하네스·버전을 비교 기록에 명시 |
| 스냅샷 없이 반복 수정 | 좋아졌던 상태로 못 돌아감 | 매 편집 전 `save_as_mainfile(copy=True)` |
| 공식 Blender 커넥터와 ahujasid 서버를 동시에 켬 | `localhost:9876` 충돌 | 하나만 사용([Blender MCP 가이드](02_blender_mcp.md)) |

---

## 관련 문서

- [00 목적·범위](../00_purpose/purpose_and_scope.md), [조사 방법·신뢰도 정책](../01_research/research_method.md), [출처 카탈로그](../01_research/sources_catalog.md), [검증 로그](../01_research/verification_log.md)
- [01 AI 모델·클라이언트](01_ai_models_and_clients.md): 모델별 과제 라우팅, effort, 비용
- [02 Blender MCP](02_blender_mcp.md): 공식 Blender Lab 서버 vs ahujasid MCP for Blender, safe mode, API 함정
- [03 기타 DCC·CAD·엔진 MCP](03_other_mcp_dcc_cad_engines.md): build123d-mcp 등 코드 CAD MCP
- [04 AI 3D 생성](04_ai_3d_generation.md): 검색·생성 경로, Hunyuan3D 라이선스
- [05 텍스처·재질](05_texturing_materials.md): 절차적 노드 레시피, PBR 규칙
- [06 조명·렌더·아트디렉션](06_lighting_rendering_art_direction.md): 연구가 다루지 않는 미감
- [07 오브젝트·가구·조형 모델링](07_modeling_objects_furniture_sculpture.md): 파트 분해, 조립 검사, Procedura 대응
- [08 배치·레이아웃](08_scene_layout_placement.md): 충돌률 표, 솔버 코드, rigid body 안착, 체크포인트
- [09 에이전트 워크플로·프롬프팅](09_agent_workflow_prompting.md): 시각 피드백 루프, 14절 "연구가 뒷받침하는 원칙"
- [10 에셋·파이프라인·라이선스](10_assets_pipeline_licensing.md)
- [AAA 제작 플레이북](../03_playbooks/02_aaa_production_playbook.md), [프롬프트 템플릿](../03_playbooks/03_prompt_templates.md), [품질 체크리스트](../03_playbooks/04_quality_checklists.md), [실측 치수 기준표](../03_playbooks/05_reference_dimensions.md)
- [CLAUDE.md 템플릿](../03_playbooks/templates/CLAUDE.md), [스킬 템플릿](../03_playbooks/templates/skills/blender-aaa-scene/SKILL.md), [보조 스크립트](../03_playbooks/scripts/README.md)
- [사례 모음](../04_case_studies/01_case_studies.md), [한국어 자료](../04_case_studies/02_korean_resources.md)

## 원자료

- [`01_research/raw/13_research-papers.research.json`](../01_research/raw/13_research-papers.research.json): 학술 연구 1차 조사(항목 48, 노하우 18, 사례 7). 7대 합의와 8단계 레시피의 원형
- [`01_research/raw/13_research-papers.verify.json`](../01_research/raw/13_research-papers.verify.json): 독립 검증(판정 15, 항목 점검 19, 누락 6). 반영한 주요 정정: BlenderGym VeriRatio 과잉 해석과 리더보드 모델 수(13개), LayoutVLM 충돌률 해석, LL3M 코드 비공개·비상업 라이선스, 3DCodeBench 라이선스 불일치, Scene Language 기본 모델(3.7 Sonnet) 뒤바뀜, ProcFunc LLM 실험 존재, LLaMA-Mesh 비상업, 3D-GPT 부분 공개, I-Design Docker 부재·구형 모델, Blender API 변경 시점(4.1), La Forge 신뢰도, Procedura·retire 일정·SIGGRAPH Asia 2025 프로그램 탐색 누락 보완
- [`01_research/raw/G6_benchmarks_models.gap.json`](../01_research/raw/G6_benchmarks_models.gap.json): 3D·CAD 벤치마크와 최신 모델 정량 비교 보완 조사(BenchCAD 공식 vs 벤더, CADGenBench, CADWorld, 3DHarnessBench, 3DCodeArena, Arena 스냅샷, VIGA·CADCodeVerify·CAD-Recode·LayoutVLM·Holodeck 논문 수치)
- 교차 참조: [`01_research/raw/08_modeling-objects.verify.json`](../01_research/raw/08_modeling-objects.verify.json)(CAD-Recode·Text2CAD·LL3M LICENSE 파일 확인), [`01_research/verification_log.md`](../01_research/verification_log.md)(3DCodeBench 0.69→0.97 미확인, 3DHarnessBench 모델 목록, BenchCAD 95.9% 미확인)
