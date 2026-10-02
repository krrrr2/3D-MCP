# 사례 모음: AI + MCP로 3D를 만든 사람들은 어떻게 했나

> 기준일: 2026-09-27 · GPT-6 Astra, Claude Fable 5.1·Opus 5.5 등을 MCP·스크립트로 3D 도구에 연결해 결과물을 만든 공개 사례 약 140건을 중복 없이 모아 "누가·무엇을·어떻게·결과·교훈"으로 정리했습니다. 독립적으로 검증된 'AAA급' 결과는 없었고, 잘된 사례는 모두 **[사람이 만든 에셋·실측 데이터 + 에이전트 조립 + 검증 루프 + 사람의 디렉션]** 구조였습니다.

## 핵심 요약

- **규모와 흐름.** [1절 표](#1-한눈에-보는-표)에 113건, 2.8~2.11절에 입문 경험기·연구형·비판 대상·업계 사례 약 30건을 더 모았습니다. 사례는 2026-09-03 GPT-6 Astra 출시(2차 출처로 확인) 직후 크게 늘었습니다. 방식은 세 갈래입니다. ① Blender MCP로 실행 중인 Blender를 조작, ② Codex·Claude Code가 `blender --background --python`으로 bpy 스크립트를 돌리는 headless 방식, ③ 엔진 공식 MCP(UE 5.8 실험적 Unreal MCP, Roblox Studio 내장 MCP)로 레벨 조립. 셋을 섞는 사례가 가장 많습니다.
- **'AAA급'은 없었습니다.** 공개 점수가 붙은 최고 사례인 PhiloLabs의 Fable 5.1 에이전트 스웜 Union Square 디지털 트윈도 조정하지 않은 리뷰어 점수가 재질 6, 시각 충실도 6, 조명 7/10이었습니다(목표 8.5~9). "세부가 꽤 틀린다", "화면이 거칠고 건물에 오류가 있다"고 작성자 스스로 밝힌 사례가 많습니다.
- **잘된 사례의 공통 구조.** ① 사람이 만든 에셋과 실측 데이터(CC0 모듈러 키트, Fab 팩, City Sample, OSM·LiDAR·스캔)에서 출발하고, ② 유기체·캐릭터는 이미지→3D로 베이스를 만든 뒤 에이전트가 UV·리깅·텍스처를 손보고, ③ '예쁘다'를 체크리스트로 쪼개고(Vizuara 6항목), ④ 탑다운·눈높이·플레이어 시점 스크린샷으로 검증하고, ⑤ 빌더와 리뷰어를 분리하고, ⑥ 사람이 결함 목록을 주며 2~21회 반복했습니다.
- **가구·인테리어는 순서가 같았습니다.** 벽·바닥·천장·개구부 같은 구조 → 주요 가구 → 소품. 가구는 개별 오브젝트로 나누고, 근거 없는 방은 지어내지 말고 기록합니다(Realsee 공개 프롬프트). 천장고나 문 폭 같은 치수 하나를 앵커로 받습니다. 그래도 세부 정확도는 부족하다는 평이 대부분입니다.
- **실패는 반복됩니다.** 임포트 스케일 100배(서로 무관한 두 사례), 이미지→3D 결과가 작게 들어옴, 떠 있거나 파고드는 부품, 옆에서 보면 얇은 캐릭터, 핀 구멍 누락, 뒤집힌 벽 와인딩, 1~3m마다 반복되는 텍스처, 연결되지 않은 노멀맵, 틀린 캡처 경로가 여러 사례에서 나왔습니다. 숫자로 잡을 수 있는 것은 이 저장소의 [`scene_audit.py`·`placement_utils.py`·`review_views.py`](../03_playbooks/scripts/README.md)(Blender 4.2.23 LTS·5.0.1·5.2.2 LTS에서 테스트 통과)로 먼저 잡으세요. 문이 벽에 안 뚫렸거나 열면 벽에 막히는 문, 갈 수 없는 방 같은 건축 상식 오류는 [`building_audit.py`](../03_playbooks/scripts/README.md)가 잡습니다.
- **모델 비교는 거의 모두 n=1이고 결과가 엇갈립니다.** 같은 Blender 과제에서 Astra가 시간·토큰을 덜 썼다는 보고, 제품 비율·연출은 Opus 5.5가 낫다는 보고, 3D 렌더는 Astra가 크게 이겼다는 보고가 함께 있습니다. 절대 순위 대신 작업 유형별로 고르세요. **Codex에서 Astra의 기본 effort는 low**라서, effort를 밝히지 않은 비교는 걸러서 봐야 합니다.
- **비용·시간 감각.** 짧은 반복 1회 2분39초~5분59초(Simon Willison), 원프롬프트 게임 24분·$9.90(Nipale), 테니스 게임 프로토타입 52분·세션 4시간23분(Robo Open), 사람 디렉션 10시간·21회(SpenserFX), 협동 게임 첫 반복 39시간(How to Suck). 대부분 작성자 자기 보고입니다.
- **SNS의 '포토리얼'을 조심하세요.** 상당수는 Blender 그레이박스·프리비즈 위에 Seedance 2.5 같은 AI 비디오를 입힌 것이라 3D 에셋 품질과는 다른 이야기입니다. 이 문서는 해당 사례에 **[AI 영상]** 을 붙였습니다.
- **[한국 사용자] 사례를 따라 하기 전에 라이선스를 확인하세요.** 여러 사례가 Tencent Hunyuan3D를 쓰는데, Hunyuan3D 계열(2.0/2.1/Omni/Part, HY-World, HY-Motion, BPT) 오픈웨이트 라이선스는 적용 지역에서 대한민국·EU·영국을 빼고 출력물 사용까지 막습니다. 한국어 UI에서는 노드 이름이 번역되어 사례 코드가 `KeyError`를 낼 수 있습니다. GitHub에서 확인한 한국 관련 사례는 소수입니다(7절).
- **출처 품질 차이가 큽니다.** 사례 상당수는 큐레이션 저장소를 거친 X 게시물입니다. Tripo 카탈로그는 447건 중 48%가 원문 프롬프트가 아니라 Tripo가 쓴 요약 브리프이고, yangqiong 라운드업은 금액 기호가 깨져 있습니다. 벤더 SEO 블로그와 재가공 기사는 '신뢰도 낮음'으로 표시했습니다.

---

## 0. 이 문서 읽는 법

### 0.1 신뢰도 표기

| 표기 | 뜻 | 예 |
|---|---|---|
| **검증됨** | 독립 검증 에이전트가 저장소 README·로그·코드 같은 1차 자료로 수치를 다시 확인함 | Nipale 게임, Robo Open, PhiloLabs |
| **검증됨(정정 반영)** | 확인은 됐지만 조사 단계 서술 일부가 틀려 정정값으로 바꿈 | How to Suck(주간 한도 해석), per-simmons(TRELLIS 평가) |
| **1차 공개** | 제작자가 코드·로그·결과물을 공개했지만 수치를 따로 재확인하지는 않음 | Gaius114, MMMvinki |
| **자기 보고** | 제작자 SNS 게시물(X 등)만 있음. 이번 조사에서 원문을 열지 못해 큐레이션 저장소를 거쳐 확인 | Tom Krcha, Matt Shumer |
| **2차 요약** | 큐레이션 목록, 기사, 검색 요약으로만 확인 | Tripo 카탈로그 인용 사례 |
| **벤더 쇼케이스 / 벤더 문서** | 회사가 자사 모델·제품 홍보용으로 낸 사례나 공식 문서. 선별 편향이 있음 | OpenAI 'Solace', Higgsfield, Meshy 파이프라인 |
| **신뢰도 낮음** | 검증 단계에서 신뢰도 낮은 출처로 지적됨(벤더 SEO 블로그, 재가공 기사, 증빙 없는 1커밋 저장소). 근거로 쓰지 않고 '미검증 주장'으로만 남김 | MindStudio, ixbt, AI Forge |
| **[AI 영상]** | 최종 화면이 3D 렌더가 아니라 AI 비디오 모델 출력 | openerai 프리비즈 스킬 |

- 수치 옆 **(n=1)** 은 한 사람이 한 번 해 본 결과라는 뜻입니다.
- 표의 '-'는 공개되지 않았다는 뜻입니다.
- 이 조사 환경에서는 x.com, youtube.com, openai.com, blender.org 등이 차단되어 있었습니다([조사 방법](../01_research/research_method.md)). 그래서 X·YouTube 사례의 품질은 직접 보지 못했습니다.

### 0.2 사례 출처로 쓴 큐레이션 저장소

| 저장소 | 규모·특징 | 주의 |
|---|---|---|
| [TripoGrowthLab/awesome-3d-prompts](https://github.com/TripoGrowthLab/awesome-3d-prompts) | 447건(2026-07-19~09-25). 모델별 Astra 291, Fable 5.1 79, Opus 5.5 33, Kimi K3 20, Fable 5 18, Opus 5 13. 게임 121, 씬 97, 인터랙티브 90, 애니메이션 82, 에셋 54. Blender 관련 96~97건(그중 Astra 81~82건, 52건이 09-03~06에 몰림) | 3D 생성 벤더(Tripo)의 큐레이션. **216건(48%)은 원문 프롬프트가 아니라 Tripo가 쓴 'Build brief'**. 결과 품질 미검증 |
| [carpentry-liu/awesome-astra-3d](https://github.com/carpentry-liu/awesome-astra-3d) | Astra 사례 194건 + 방법 참고 12건. 근거 등급 official 15, author 63, secondary 116, reference 12. 한계·실패 메모가 붙음 | 중국어 위주. "수록·작성자 주장·링크 접근 가능 ≠ 재현됨"을 스스로 명시 |
| [yangqiong/gpt6-astra-3d](https://github.com/yangqiong/gpt6-astra-3d) | Astra 출시 뒤 3D 게시물을 X 반응 순으로 정리. 모델 간 시간·토큰 A/B 수치가 많음 | 금액의 '$'가 HTML 주석으로 깨짐(예: `~<!-- -->3.3`), 같은 항목이 다른 번호로 중복, 헤더 기간(9/3~5)과 행 날짜(9/24까지) 불일치 |
| [magiccreator-ai/awesome-gpt-6-astra](https://github.com/magiccreator-ai/awesome-gpt-6-astra) | Blender & 3D 섹션 24건 | 상업 갤러리로 유도하는 큐레이션. 항목마다 '제작자 보고, 미검증' 문구 |
| [Frank-ZY-Dou/awesome-ai-3d-modeling-robotics](https://raw.githubusercontent.com/Frank-ZY-Dou/awesome-ai-3d-modeling-robotics/main/README.md) | 모델링·로보틱스 사례와 벤치마크 목록 | kitchen-twin 저자가 운영. 스스로 'Most cases use GPT-6 Astra'라고 밝힐 만큼 Astra 편향 |

### 0.3 모델·도구 이름 메모

- **'아스트라'** = OpenAI **GPT-6 Astra**(2026-09-03 출시, 2차 출처로 확인, openai.com 원문 미열람). Google의 'Project Astra'와는 다릅니다. Codex 기준 reasoning 단계는 low/medium/high/xhigh/max/ultra이고 **기본값은 low**입니다.
- **'페이블'** = Anthropic **Claude Fable 5.1**(2026-09-01, 입력/출력 $10/$50 per 1M). **Claude Opus 5.5**는 2026-09-22 출시, $4/$20, 1M 컨텍스트, 기본 effort medium이고, 공식 페이지는 "vision과 computer use에 가장 좋은 Opus"라고 소개합니다([Opus](https://www.anthropic.com/claude/opus)). 발표문 표에는 3D·CAD 지표가 없습니다.
- 'GPT 5.6 Sol'(2026-07 게시물)과 'GPT-6 Sol'(2026-09 비교)이 둘 다 나옵니다. 원문 표기대로 두었습니다.
- 사례에서 그냥 "Blender MCP"라고 쓴 경우 대부분 커뮤니티 서버 **MCP for Blender**(ahujasid, 구 blender-mcp, PyPI mcp-for-blender 2.1.0, 2026-09-25)입니다. Claude의 공식 'Blender' 커넥터는 **Blender Lab 공식 MCP 서버**(2026-04-28 발표, 커넥터 v1.0.1, 애드온 manifest `blender_version_min` 5.1.0, GPL-3.0-or-later, git 소스 설치)로 별개입니다. 둘 다 `localhost:9876`을 쓰므로 동시에 켤 수 없습니다. 자세한 차이는 [Blender MCP 생태계](../02_guides/02_blender_mcp.md)를 보세요.

---

## 1. 한눈에 보는 표

ID 앞 글자는 분야입니다. **A** 인테리어·가구·건축, **P** 제품·하드서피스·기계·CAD, **E** 환경·도시·레벨, **G** 게임, **C** 조형·캐릭터, **V** 영상·렌더·프리비즈, **T** 텍스처·재질·에셋 파이프라인. 상세 설명은 2절에 있습니다.

| ID | 날짜 | 누가 | 모델 | 도구·MCP | 만든 것 | 시간·비용 | 결과 품질 | 신뢰도 | 링크 |
|---|---|---|---|---|---|---|---|---|---|
| A1 | 2026-09-03~04 | Thomas Ricouard(OpenAI) | GPT-6 Astra | Blender Python, Cycles → UE5 | 정원 주택 'Solace'(건축·가구·재질·조명 편집 가능), Cycles 카메라 투어, UE5 실내 워크스루 | - | 공식 쇼케이스, X 좋아요 7.1K·조회 230만 | 벤더 쇼케이스 | [OpenAI 블로그](https://developers.openai.com/blog/architectural-visualization-with-astra)(미열람), [X](https://x.com/Dimillian/status/2095596700815516004) |
| A2 | 2026-09-03 | Tom Krcha | Astra | Blender | 주택 사진 1장 → 가구·가전·장난감이 분리된 편집 가능 씬, 로컬 60fps 워크스루 | - | 반응 큼, 치수 정확도 미검증 | 자기 보고 | [X](https://x.com/tomkrcha/status/2095598645190291775) |
| A3 | 2026-09-11~15 | realsee-developer | Astra(Codex) | Blender 5.2.1 LTS, Realsee 스캔 | 스캔(원본 396파일, 5.66 GiB) → 벽·바닥·천장·문·창을 따로 편집하는 .blend, 85초 워크스루, USDZ | - | 구조 복원 성공, 스크립트는 이 공간 전용 | 검증됨 | [GitHub](https://github.com/realsee-developer/realsee-astra-blender) |
| A4 | 2026-09-05~08 | hahaliu1029 | Astra, Fable 5.1 | Blender Cycles, Three.js | 평면도 1장 → 프렌치·이탈리안·모던·송대풍 4스타일(모던: 공간 9, 가구 64점) | 비공개 | 작성자 "엄격한 순위 불가" | 1차 공개 | [GitHub](https://github.com/hahaliu1029/house-3d) |
| A5 | 2026-09-11 | Zhiyang(Frank) Dou | Astra | 자체 Blender 모델링 언어, ViPE 스캔, Three.js | 휴대폰 영상 → 실험실 주방 트윈(에셋 32, 작동 조인트 138) | - | 저자 "얇고 반짝이는 것은 아직 약함" | 1차 공개(결과만) | [GitHub](https://github.com/Frank-ZY-Dou/kitchen-twin) |
| A6 | 2026-09-21 | AmirMušić | Astra(Codex 스킬) | UE 5.8, Unreal Editor Python | 매물 사진 20장+파노라마 → 걸어 다닐 수 있는 UE 프로젝트, 물리 논리 QA | - | 떠 있음·관통 결함을 체크리스트로 차단 | 1차 공개(스킬) | [GitHub](https://github.com/amirmushichge/unreal-home-wizard) |
| A7 | 2026-09-16 | Wentao Zhu | Astra | Blender MCP | 방 사진 → 경첩·문·서랍 관절 가구 인터랙티브 씬 + 데모 영상 | - | 미확인 | 2차 요약 | [X](https://x.com/walterzhu8/status/2100139076816916977) |
| A8 | 2026-09-23 | yamahigashi | Astra | Imagegen 2.5, Tripo P2.0, Blender MCP + computer use | 참조 이미지·평면도 → 소품 분해·생성 → 배치한 주택 | - | 작성자 "세부가 꽤 틀림" | 2차 요약 | [X](https://x.com/yamahigashi/status/2102727459657617891) |
| A9 | 2026-09-04 | おのふみ | Astra | Blender MCP | 가구를 꺼내고 돌릴 수 있는 방, 같은 치수의 평면도·워크스루 1베드룸 | - | - | 2차 요약 | [X](https://x.com/onofumi_AI/status/2096020860121596003) |
| A10 | 2026-09-24 | AIパースおじさん | Opus 5.5 | Claude Code | 평면도 → 가구 포함, 층을 고를 수 있는 2층 주택 뷰어 | - | 미확인 | 2차 요약 | [X](https://x.com/uncle_render/status/2103080046537904576) |
| A11 | 2026-09-08 | Doron Taussy | Astra | - | IKEA 의자 사진 1장 → 치수·재질 전환·부품 검사·분해도·flat-pack·조립 인터랙티브 모델 | - | 미확인 | 자기 보고 | [LinkedIn](https://www.linkedin.com/posts/doron-taussy_i-gave-astra-one-photo-of-an-ikea-chair-and-activity-7503069971481182209-ay6a) |
| A12 | 2026-09-24 | Shimecki | Opus 5.5 | - | 새 침대가 아이 방에 맞는지 확인 | - | 미확인 | 자기 보고 | [X](https://x.com/scheemunai/status/2103059885361598633) |
| A13 | 2026-09 | YouTube 'I Tested GPT Astra for 3D Modeling' 제작자 | Astra | SketchUp + MCP(Ruby 실행) | 앞뒤 사진, 치수 평면도, 19쪽 농가 도면 세트로 주택 3채 | 모델당 17~22분, Plus 주간 할당량을 하루에 소진 | 외관은 인상적, 인테리어 부정확·치수 누락·문 방향 오류 | 2차 요약 | [YouTube](https://www.youtube.com/watch?v=SsBLhNgqTqQ) |
| A14 | 2026 | McNeel(공식 문서) | MCP 클라이언트 | Rhino MCP Platform, Rhino 8/9, Grasshopper 2 | 월넛 커피 테이블, 나선 계단, 의자 5종 변형 | - | 공식 권장 레시피(품질 수치 없음) | 벤더 문서 | [레시피](https://raw.githubusercontent.com/mcneel/RhinoAI/rhino-9.x/docs/content/docs/try-it-out/recipes.md) |
| A15 | 2026 | rhino-mcp 사용자 | 미상 | tanishqbhattad/rhino-mcp(도구 123) | 1:1 고딕 대성당, 오브젝트 약 8,000 | - | invalid geometry 0(README) | 자기 보고 | [GitHub](https://github.com/tanishqbhattad/rhino-mcp) |
| A16 | 2026-04-28 | Trimble·Anthropic | Claude | SketchUp 커넥터(build_model·get_docs·save_model) | 방 증축, 가구, 사이트 콘셉트 | 무료 30개 저장(보도 기준, 미확인) | 공식 출시 | 벤더 문서 | [커넥터](https://claude.com/connectors/sketchup) |
| A17 | 2026(추정) | 뽁숑이(한국 유튜버) | Claude | SketchUp MCP + AI 렌더러 | 건축·인테리어 매스 + AI 렌더 | - | - | 2차 요약 | [YouTube](https://www.youtube.com/watch?v=GOaWRhrsQC0) |
| A18 | 2026-09 | Pat Simmons | Astra(목록 기준) | blender-production 스킬, Blender 5.1.2+ | Fallingwater 재현·플라이스루 | 목록에 "무인 연산 54시간" 인용 | 규칙 기반 QA | 2차 요약(스킬은 1커밋) | [GitHub](https://github.com/per-simmons/blender-production) |
| A19 | 2026-09 | Bad Decisions Studio | Astra | Blender | 아이폰 사진 몇 장 → 실존 건물 | 30분 이내 | 사진 재구성에서 원본에 없는 요소를 지어낸다는 지적도 있음 | 자기 보고 | [X](https://x.com/badxstudio/status/2095982983379653113) |
| A20 | 2026-09-08 | SpenserFX | Astra | Blender(MacBook Pro) | 빈티지 체육관(농구 골대 구조, 바닥재) | 10시간, 수정 21회, 130만 폴리곤 | 사람의 반복 디렉션이 필요 | 2차 요약 | [X](https://x.com/SpenserFX/status/2097439078866166018) |
| A21 | 2026-09 | MindStudio 블로그 보도 | Fable 5.1 | Blender MCP | 주소 1개 → 시애틀 주택 37초 시네마틱 워크스루 | - | "프로덕션 품질 증거 아님" 단서 | 신뢰도 낮음 | [MindStudio](https://www.mindstudio.ai/blog/claude-fable-5-1-blender-video-generation) |
| A22 | 2026-05 | aigeboku | Claude, Gemini(이미지) | Blender 4.5 LTS+, Blender MCP, Hitem3D API | "create classroom furniture" → 교실 가구 생성·배치 | Hitem3D 유료 | 결과 증빙 없음(1커밋) | 신뢰도 낮음 | [GitHub](https://github.com/aigeboku/blender-ai-3d-setup) |
| A23 | 2026-09 | Fraktal(디자인 스튜디오) | Astra | Codex, Blender, UE5 | 설계 브리프 → 가구 배치 주택 → UE5 투어 | - | 수치 없음 | 2차 요약 | [Fraktal](https://fraktal.design/blog/gpt-6-astra-from-model-to-architecture-workflow/) |
| A24 | 2026-09 | Vagon 블로그 | Astra | Blender(클라우드 워크스테이션) | 레퍼런스 이미지 → 편집 가능 씬 | - | 수치 없음 | 2차 요약 | [Vagon](https://vagon.io/blog/reference-image-to-3d-scene-with-gpt-6-astra-blender) |
| A25 | 2026 | Linfeng Zhao | 미상 | 런타임 코드 공개 | 스탠퍼드 주방 영상 → 작동 서랍이 있는 MuJoCo 씬 | - | - | 1차 공개 | [GitHub](https://github.com/openretriever/retriever) |
| P1 | 2026-09-04 | Tom Krcha | Astra | Blender(주로 MCP, 가끔 computer use로 확인) | 옛 증기기관차 그림 → 바퀴·차축·서스펜션·로드까지 이름 붙은 편집 가능 오브젝트 3,295개 | "몇 분" | 치수 미검증 | 자기 보고 | [X](https://x.com/tomkrcha/status/2095756085890310311) |
| P2 | 2026-09-08 | teshnizi2 | Astra, Fable 5.1(high) | Blender 5.2.1 EEVEE, Codex CLI 0.153.4 / Claude Code 2.1.263(도구 끔) | 6날 기계식 조리개 열림·닫힘·분해·재조립 애니메이션 | - | 둘 다 작동, 둘 다 기계적 결함 | 검증됨 | [GitHub](https://github.com/teshnizi2/astra-fable-3d-iris) |
| P3 | 2026-09-22~24 | Higgsfield AI | Opus 5.5 | Blender + Higgsfield 도구 | 좌석 430개까지 분리한 신칸센(오브젝트 5,112), 풍차, 사진 → 건물 붕괴 시뮬, 목탄 드로잉 질감 씬 | 풍차 15분(목록에서 미확인) | 홍보 게시물 | 벤더 쇼케이스 | [X](https://x.com/higgsfield_ai/status/2102507018372436264) |
| P4 | 2026-09 초 | Danny Stuart / Hierarchy Agency | Astra vs Fable 5.1 | Blender MCP, Three.js | iPod Classic 분해도 히어로 섹션 / 도면 → UE 워크스루 | - | 3D는 Astra가 큰 차이로 우세(작성자) | 2차 요약 | [Substack](https://dannystuart.substack.com/p/codex-astra-vs-claude-fable-battle), [Hierarchy](https://hierarchy.ch/en/news/gpt-6-astra-vs-claude-fable-5-1) |
| P5 | 2026-09-06 | Alexey Fateev | Astra, Fable 5.1 | Blender MCP | 4×3090 GPU 워크스테이션 사진 4장 → 모델·애니메이션 웹사이트 | - | 미확인 | 2차 요약 | [X](https://x.com/superalesha/status/2096706133121540436) |
| P6 | 2026-09-22~24 | 3DVR3 | Opus 5.5 vs Astra | Blender | Quest 3 헤드셋 사진 → 모델 | - | 두께·기울기·흑백 밸런스는 Opus 5.5 우세 | 2차 요약 | [X](https://x.com/3DVR3/status/2102656183186387182) |
| P7 | 2026-07-30 | Spectro | Opus 5(이후 Fable 5.1) | Blender, 서브에이전트, GLB 주입 | 건담급 메카 블루프린트(엔진·유압·콕핏·무기·다리 리그) | - | 작성자 만족, 공학 타당성 미검증 | 2차 요약 | [X](https://x.com/Spectromachina/status/2082760534500188606) |
| P8 | 2026-09-05~09 | Nick Scarcella, Hirokazu Yokohara, sokun, AIRIlab, iPentec | Astra | Houdini MCP·Python, Rhino, 3ds Max MCP | OP-1 Field 신디사이저, 파라메트릭 비행기 HDA, 참조 이미지 건축, 같은 우주선을 Blender·3ds Max로 | Rhino 약 40분 | "여러 번 수정 필요", "떠 있는 글자·비율 수정 필요" | 2차 요약 | [carpentry-liu](https://github.com/carpentry-liu/awesome-astra-3d) |
| P9 | 2026-05(v1.3.0) | RobLe3 | Claude(Claude Code) | cc-blender-skill 30종 + ahujasid MCP(9876), Blender 5.1.1 | 검, 병, 의자, 선글라스, 데스크 램프, 방송용 아바타 | 테스트 Haiku·패치 Opus로 약 10배 절감 | 하드서피스 재현 가능, 곡면 가구·얼굴은 범위 밖 | 검증됨 | [GitHub](https://github.com/RobLe3/cc-blender-skill) |
| P10 | 2026 | Gaius114 | Claude(Claude Code) | 자체 애드온(HTTP 7234), 스킬 11 + plan_validator | 도넛, 에스프레소 잔, 와인병, 과일 바구니 | - | renders/ 폴더 공개 | 1차 공개 | [GitHub](https://github.com/Gaius114/blender-claude-mcp) |
| P11 | 2026-09-08 | KANA | Astra | Blender MCP | 일본 꽃집 익스플로디드 뷰 분해·재조립 애니메이션 | - | 편집 파일 비공개 | 2차 요약 | [X](https://x.com/KanaWorks_AI/status/2097153139795468365) |
| P12 | 2026(04 업데이트) | ReshefElisha | Opus 4.7 | jarvis-onshape-mcp(도구 60+) | 공학 도면 → CAD 부품(3티어, 변형 8종) | 브리프당 150턴 예산 | 사람 사양 1.000/0.615, 자율 비전 0.533/0.000(n=1) | 검증됨 | [RESEARCH.md](https://raw.githubusercontent.com/ReshefElisha/jarvis-onshape-mcp/main/RESEARCH.md) |
| P13 | 2026-07~09 | pzfreo | Opus 5, GPT-5.6 Sol, Gemini 3.7 Flash | build123d-mcp | CADGenBench 81 fixture STEP 생성·편집 | Opus 실행 API 환산 약 $724.77 | 0.677 / 0.532 / 0.508, 셋 다 80/81 valid | 도구 저자 자체 평가 | [비교 문서](https://raw.githubusercontent.com/pzfreo/cadgenbench-build123d/main/GEMINI_OPUS_GPT56_MCP_COMPARISON.md) |
| P14 | 2025~2026 | neka-nat | Claude Desktop | freecad-mcp(XML-RPC) | 플랜지, 장난감 자동차, 2D 도면 → 3D | - | README 데모 GIF | 1차 공개 | [GitHub](https://github.com/neka-nat/freecad-mcp) |
| P15 | 2026 | brookstalley | Claude | Cordyceps(Grasshopper MCP), Rhino 8.21+ | GH 조형 → bake → 재질·렌더 → 오빗 애니 | - | 품질 평가 없음 | 1차 공개 | [GitHub](https://github.com/brookstalley/cordyceps) |
| E1 | 2026-06-18~24 | per-simmons | Claude(Claude Code, 버전 미명시) | UE 5.8 공식 Unreal MCP(실험적), headless Blender, Cesium v2.27, City Sample, Meshy, TRELLIS | 뉴욕(빌드 방식 5가지 비교), PCG 글래스 타워 49, 파리 블록, 아르데코 블록 | "배관 작업에 시간을 잡아 두라" | "real but raw", 가로 수준 사실감 한계 | 검증됨(정정 반영) | [GitHub](https://github.com/per-simmons/unreal-agent-harness) |
| E2 | 2026-09-02 | PhiloLabs | Fable 5.1 에이전트 스웜(09-05 Astra 비교 영상) | Three.js, OSM, USGS 3DEP, Playwright | Union Square SF 약 800×720m(건물 492, 개구부 11,950, 모듈 28,003, 보행자 220, 차량 109) | - | 조정 없는 점수 재질 6·시각 6·조명 7·성능 6/10 | 검증됨 | [QA 리포트](https://raw.githubusercontent.com/PhiloLabs/fable51-worlds/main/union-square-sf/FINAL_QA_REPORT.md) |
| E3 | 2026-09-03 | Matt Shumer | Astra | Unreal Engine | 거리 단위로 다듬은 맨해튼 월드, 자율 에이전트 사회 월드 | 약 1주 | 반응 최대(좋아요 17.4K, 조회 340만), 에셋 출처·정확도 미공개 | 자기 보고 | [X](https://x.com/mattshumer_/status/2095609734845927525) |
| E4 | 2026-07-21 | Martin Puli | Fable 5 vs GPT 5.6 Sol | Blender MCP + 스킬, 발자국·높이·좌표 크롤링 에이전트 | 실측 맨해튼 Blender 모델, 도시 합성 | - | 텍스처·재질은 약점(작성자) | 자기 보고 | [X](https://x.com/MartinPulitano/status/2079387760478073087) |
| E5 | 2026-09-13~14 | octopus7(한국 사례로 추정) | ChatGPT 채팅(Astra는 저장소 이름 기준) | Blender 4.2+ Python, UE Python | 300×300m 로우폴리 호수 숲: 나무 3,800, 인스턴스 16,573, 재사용 메시 127 | - | 순수 Python 테스트 30개, 콜리전·LOD 범위 밖 | 검증됨 | [GitHub](https://github.com/octopus7/astra-blender-forest) |
| E6 | 2025 하반기 | flopperam(현재 Aura 소유) | Claude, GPT-5 | unreal-engine-mcp(고수준 건축 도구, UE 5.5~5.7) | 프롬프트 1회로 객체 4,000+ 메트로폴리스, 모델 건축 대결 | - | 프리미티브 위주(추정) | 1차 공개 | [GitHub](https://github.com/flopperam/unreal-engine-mcp) |
| E7 | 2026(UE 5.8 이후) | Epic 개발자 커뮤니티 튜토리얼 | Claude(Claude Code) | UE 5.8 내장 MCP, Fab 환경 팩 | Third Person 템플릿 → 플레이 가능한 가을 숲 레벨 | - | 사람이 만든 에셋 + AI 배치 | 2차 요약(본문 미열람) | [튜토리얼](https://dev.epicgames.com/community/learning/tutorials/bnJ0/build-a-playable-unreal-engine-5-level-with-ai-mcp-claude-code) |
| E8 | 2026-09-12 | Dan Elton | Astra → Fable 5.1 | Blender | 역사 사진 2,000장으로 1893 시카고 만국박람회 재현, 약 5분 워크스루 | - | 작성자 "거칠고 건물에 오류" | 자기 보고 | [X](https://x.com/moreisdifferent/status/2098795017955418202) |
| E9 | 2026-09-05~20 | Givros | Astra | 자체 Blender 스킬·프롬프트 라이브러리 | Cozy Lake + 프랑스 마을 확장 월드 | - | 조회 47.9만 | 2차 요약 | [X](https://x.com/givros/status/2096219700879331665) |
| E10 | 2026 | MAX-786 | Claude(Claude Code) | claude-3d-harness(SKILL 58개), newo-ether blender-mcp | 비 오는 밤 일본 도시 옥상의 작은 방(메시 오브젝트 449) | 그레이 블록아웃 → 최종 프레임 3시간 미만 | - | 1차 공개(README) | [GitHub](https://github.com/MAX-786/claude-3d-harness) |
| E11 | 2026-09-13 | danielsobrado | Astra | YAML → bpy → headless CLI, 멀티뷰 리뷰, MCP는 점검용 | Coastal Jungle 데모 | - | 정량 수치 없음 | 1차 공개 | [GitHub](https://github.com/danielsobrado/Codex-and-Blender) |
| E12 | 2026-09-10 | MMMvinki | 미명시 | blender-mcp 애드온(GUI 모드), Blender 4.5, Three.js | 어린왕자 행성 8개(각 5,120 tris), 22본 캐릭터, 소품 | - | 검증 인프라가 상당히 필요 | 1차 공개 | [GitHub](https://github.com/MMMvinki/little-prince-planet-world) |
| E13 | 2026-09 | 다나와 DPG 정리(국내외 사례) | Astra | Blender, Codex, computer use | Backrooms 분위기 3D 영상, 도시 게임 | 프롬프트 약 5개로 30분 + 내보내기 20분 / 게임 5일 | 품질 검증 없음 | 2차 요약 | [다나와](https://dpg.danawa.com/news/view?boardSeq=60&listSeq=6058609) |
| E14 | 2026-09-23 | Vaibhav Sisinty(큐레이션) | Opus 5.5 | UE 외 | 출시 당일 데모 모음: 클레이메이션, 3D 게임, 광학 실험실, UE 도시 전체 | - | 개별 세부 미확인 | 2차 요약 | [X](https://x.com/VaibhavSisinty/status/2102667276252282952) |
| E15 | 2026-06-17(보도 기준, 미확인) | Epic Games(State of Unreal 2026) | Claude, Gemini | UE 5.8 실험적 MCP | 워크스루(프롭 배치, 절차적 도시, 조명 아트 디렉션, 보도 기준) | - | UE6 통합 발표 내용은 미확인 | 2차 요약 | [YouTube](https://www.youtube.com/watch?v=AlV__BFg8qk) |
| E16 | 2025-03 | Siddharth Ahuja | Claude(Claude Desktop, 당시 모델) | BlenderMCP 원조, Poly Haven, Hyper3D Rodin | "드래곤이 지키는 던전" 로우폴리 씬, HDRI·바위·식생을 가져온 해변 씬 | - | 바이럴, 생태계의 출발점(현재 약 29.4k stars) | 1차 공개 | [GitHub](https://github.com/ahujasid/blender-mcp) |
| G1 | 2026-09-01 | Nipale-ai | Fable 5.1(effort high) | Blender 5.2 headless, FLUX.2, LTX-2.5, ACE-Step, three.js, Playwright | HTML 1개(4.4MB) 아레나 게임: 메시 12개 GLB, 홀로 빌보드 영상, 신스웨이브 루프 | 24분, $9.90, 75턴, 출력 95,832 토큰 | 재시도 없이 1라운드 통과 | 검증됨 | [GitHub](https://github.com/Nipale-ai/fable-5-1-one-prompt-game) |
| G2 | 2026-09-05~ | az9713 | Astra(Codex) | Unity 6000.5.7f1 + URP 17.5.0, Blender 5.2.1, Meshy API | 'Robo Open' 테니스(토이 로봇 2체, 16본 리그, Windows 실행 파일) | 프로토타입 52분, 세션 4시간23분, Meshy 30크레딧 | 프로토타입 수준, 실패 22건 공개 | 검증됨(정정 반영) | [GitHub](https://github.com/az9713/gpt-6-astra-tennis-game) |
| G3 | 2026-09-14 | breineng | Astra(Codex) | Unity 6000.3.6f1, Netcode, Blender, ElevenLabs | 'How to Suck' 1~4인 협동 청소기 게임(17개 언어, 배포) | 첫 반복 39시간, 전체 개발에 Pro x20 주간 한도 2회분 | 실제 배포, 비주얼은 스타일라이즈드 인디(미검증) | 검증됨(정정 반영) | [GitHub](https://github.com/breineng/how-to-suck) |
| G4 | 2026-09-05~20 | Givros | Astra | Roblox Studio MCP, Blender | MeshPart·PBR 카트 레이서(AI 상대, 체크포인트, 랩 기록) | - | - | 2차 요약 | [X](https://x.com/givros/status/2096219700879331665) |
| G5 | 2026-07-03 | bsantanna | Claude Code(커스텀 스킬) | Blender MCP + Luau 린트·타입·테스트 | Roblox 게임(존 5, 미니게임 5, Luau 모듈 100+) | 며칠 | 플레이 가능 | 1차 공개 | [GitHub](https://github.com/bsantanna/roblox-flex-with-friends) |
| G6 | 2025-03 | Chong-U | Claude(Cursor) | chongdashu/unreal-mcp(UE 5.5) | 프롬프트만으로 Flappy Bird 클론(BP 생성·노드 연결) | - | Unreal MCP 붐의 시작, 그래픽보다 게임플레이 | 자기 보고 | [X](https://x.com/chongdashu/status/1906117550447960569) |
| G7 | 2026-09 | Chong-U | Fable 5.1 | Unity + Blender | 테니스 게임(G2 Robo Open의 원작 영상) | - | 프로젝트 파일 비공개 | 2차 요약 | [YouTube](https://www.youtube.com/watch?v=DQfL_l5lRpk) |
| G8 | 2026-09-05~06 | Cagri Kacmaz | Astra High vs Gemini 3.8 Flash High | ChatGPT 빌드 하네스 / Antigravity, WebGL | 같은 PROMPT.md로 문명 시뮬 수직 슬라이스 | - | Astra는 3D·카메라 작동, Gemini는 지형 평평·카메라 실패 | 1차 공개 | [GitHub](https://github.com/cagrikacmaz/gpt-6-astra-vs-gemini-3-8-flash) |
| G9 | 2026-09 | OpenAI 'Building games with Astra' 계열로 소개 | Astra | Codex | Void Explorer(성계 2,048, 절차 행성 1만+) | - | 세부 미확인 | 2차 요약(신뢰도 낮음) | [aituts](https://aituts.com/gpt6-astra-game-demos/) |
| G10 | 2026-09-05 | X 트렌딩 '1시간 이내 3D 게임' | Astra | Codex + 이미지 생성 | 플레이 가능한 3D 게임 프로토타입 | 약 45분 | 그래픽은 이미지 생성 트릭 | 2차 요약 | [X 트렌딩](https://x.com/i/trending/2096209432053190780) |
| G11 | 2026-09-10~13 | AIWHOS | GPT-6/Codex | Hyper3D Rodin MCP(Gen-2.5 Medium/Raw), BANG, Blender, Godot 4.7.2 | 'Paper Ember Duel' 3D 보스전 | - | 플레이 가능, 상업 재사용 불허 | 1차 공개 | [GitHub](https://github.com/AIWHOS/paper-ember-duel) |
| G12 | 2026-04-15 | hi-godot | Claude(Claude Code) | Godot AI MCP(도구 46, 작업 120+) | 사이버펑크 HUD·일시정지 메뉴(.tscn 직접 편집 없음) | 약 2시간(미확인) | 도구 빈틈을 정직하게 기록 | 검증됨(부분) | [friction log](https://raw.githubusercontent.com/hi-godot/cyberpunk-hud-demo/main/docs/friction-log-cyberpunk-hud.md) |
| G13 | 2026 | Andy.G | Claude Code | Roblox Studio MCP | AI 에이전트만으로 만든 Roblox 게임 | - | 미확인 | 2차 요약 | [Medium](https://medium.com/@andy.a.g/i-built-a-roblox-game-using-only-ai-agents-heres-what-happened-ed57b553facc) |
| G14 | 미확인 | @secret_canada_(한국어 Threads) | Claude Code | Unity, mcp-unity, 무료 에셋 | 캐주얼 드리프트 게임 프로토타입 | 약 30분 | - | 자기 보고 | [Threads](https://www.threads.com/@secret_canada_/post/DTCjtmzjJPD/video-%EC%9D%B4%EC%A0%A0-unity3d-mcp-%EB%A1%9C-%ED%81%B4%EB%A1%9C%EB%93%9C-%EC%BD%94%EB%93%9C-%EB%B6%99%EC%97%AC%EC%84%9C-%EA%B2%8C%EC%9E%84%EB%A7%8C%EB%93%9C%EB%8A%94%EA%B2%8C%EA%B0%80%EB%8A%A5%ED%95%B4%EC%A7%90-%EC%98%A4%EB%8A%98-%EC%B2%98%EC%9D%8C-30%EB%B6%84-%EC%A0%95%EB%8F%84-%EC%9B%8C%EB%B0%8D%EC%97%85-%EC%9C%BC%EB%A1%9C-%EB%93%9C%EB%A6%AC%ED%94%84%ED%8A%B8-%EA%B2%8C%EC%9E%84-%EC%9D%84-%EB%A7%8C%EB%93%A4%EC%96%B4-%EB%B3%B4%EA%B3%A0%EC%8B%B6%EC%96%B4%EC%84%9C-%EB%AC%B4?hl=ko) |
| G15 | 2026-09 | AiBattle | Astra Max vs Medium | Godot | Godot 게임 | Max 53분(Pro x5 주간 한도 4%), Medium 25분(1%) | - | 2차 요약 | [yangqiong](https://github.com/yangqiong/gpt6-astra-3d) |
| G16 | 2026-09 | RealFedeURU | Fable 5.1 + Astra + Meshy | Blender, Godot | 기획·코드는 Fable, 3D·Blender는 Astra, 일부 에셋은 Meshy, 통합은 Godot | - | - | 2차 요약 | [yangqiong](https://github.com/yangqiong/gpt6-astra-3d) |
| G17 | 2026-09 | Stefan_3D_AI | Astra | Blender, 영상 → 모캡 | 게임 제작 11일째, 공격 애니메이션을 직접 촬영해 모캡으로 대체 | 11일 이상 | Astra가 어색한 애니메이션을 끝내 해결하지 못함 | 2차 요약 | [yangqiong](https://github.com/yangqiong/gpt6-astra-3d) |
| G18 | 2026 | oliver-io | 미상 | 자체 UE 5.7 TS/C++ MCP(에디터 액션 약 285, 스킬 20+) | 플레이 가능한 멀티플레이 'HOVERBALL' | - | - | 1차 공개(미검증) | [GitHub](https://github.com/oliver-io/unreal-harness) |
| G19 | 2026-09-24~25 보도 | Brendan Jowett(YouTube) | Opus 5.5 vs Astra | UE, Blender MCP | 원프롬프트 인디 게임 씬 | 60~120분, Opus 2시간 API 약 $60~70 | "Opus가 모든 테스트 우세" | 신뢰도 낮음(재가공 기사) | [ixbt](https://ixbt.games/en/news/2026/09/25/438160-ii-claude-opus-55-obosel-gpt-6-astra-v-sozdanii-igr-na-unreal-engine.html) |
| G20 | 2026 | 게임뷰 기사(한국어) | 미확인 | UE 5.8 내장 MCP, UMG, Niagara | UE 5.8 게임·월드 비주얼, 머티리얼 수식 어노테이션 | - | "MCP로 현재 상황을 인식하게 된 점이 핵심" | 2차 요약 | [게임뷰](https://www.gamevu.co.kr/news/articleView.html?idxno=60827) |
| G21 | 2026 | GameDev Academy 튜토리얼 | 'GPT Astra'(모델명 미검증) | Codex, Blender MCP, Godot | Blender 에셋 → Godot 씬 | - | "샷의 느낌은 모른다" → 방향·QA는 사람 | 신뢰도 낮음 | [GameDev Academy](https://gamedevacademy.org/gpt-astra-blender-mcp-tutorial/) |
| C1 | 2026-09-09 | @happy_modeling | Astra(High) vs Meshy 7 | Blender / Meshy 7 | 같은 일러스트 → 캐릭터 2종 | 8분 대 3분 | 얼굴·옷 디테일은 Meshy 우세 | 2차 요약 | [X](https://x.com/happy_modeling/status/2097832650534990331) |
| C2 | 2026-09-13 | さ(@_sagyoai) | Astra | Blender MCP | Tripo 캐릭터 UV를 옷본 구조로 재구성, 4096² 재베이크 | 프롬프트 1회(자기 보고) | 프로젝트 파일 미검증 | 2차 요약(프롬프트 공개) | [X](https://x.com/_sagyoai/status/2098980384260456813) |
| C3 | 2026-09-09 | syaripin-i8i | Astra | Blender 5.1.2, MCP + Python, 이미지 생성 | Tripo 캐릭터 의상 텍스처 재마감(부위별 프롬프트 7개) | - | 얼굴·눈·머리·형태 보존 | 1차 공개 | [GitHub](https://github.com/syaripin-i8i/blender-astra-texture-guide) |
| C4 | 2026-09-20 | Hirokazu Yokohara | Astra(Ultra effort) | Blender sculpt | 생성형 3D 없이 사람처럼 단계별로 스컬프팅 | - | "예상보다 깨끗" | 2차 요약 | [yangqiong](https://github.com/yangqiong/gpt6-astra-3d) |
| C5 | 2026-09 | mizchi | Astra 계열 | Blender, Three.js 뷰어, IK | 로우폴리 여행자 → 22본 리그·IK·보행·여러 캐릭터 | - | 측면이 얇은 초안 수정(몸통 깊이 1.45배), 동작 딱딱함 | 1차 공개 | [GitHub](https://github.com/mizchi/modeling-playground) |
| C6 | 2026-09 초 | Stefan_3D_AI | Astra | Blender MCP, Tripo P2.0 | 생성 부품 조립 → 리깅 → 애니메이션 | - | "3D 공간 탐색 능력에 놀람" | 자기 보고(게시물 ID 불일치) | [X](https://x.com/Stefan_3D_AI/status/2096481425050743048) |
| C7 | 2026-09 | insaneUEFN | Astra | Tripo P2, Blender, Substance Painter | Tripo 베이스 → 휠 지오메트리 수정·UV 최적화 → 텍스처 | - | - | 2차 요약 | [yangqiong](https://github.com/yangqiong/gpt6-astra-3d) |
| C8 | 2026-09 | Alix Ollivier | Astra | Blender | 포토리얼 박쥐(토큰이 소진될 때까지 자율 실행) | - | '유기체는 모두 약하다'의 반례(자기 보고) | 2차 요약 | [magiccreator](https://github.com/magiccreator-ai/awesome-gpt-6-astra) |
| C9 | 2026-09 | Sarang Borude / Vatroslav | Astra | headless Blender | 드래곤 / 메카 | - | 좋은 결과(요약 기준) | 2차 요약 | [Tripo 카탈로그](https://github.com/TripoGrowthLab/awesome-3d-prompts) |
| C10 | 2026-09 | icesixgod | Astra | Blender 스킬 | 원화를 1순위로 두고 8방향+탑뷰 9뷰 레퍼런스로 캐릭터 | - | - | 1차 공개(스킬) | [GitHub](https://github.com/icesixgod/awesome-astra-blender-characters) |
| C11 | 2026-05 | KaelNebula | Claude(Claude Code) | Hyper3D Rodin(fal.ai), Blender MCP | 4면 레퍼런스 → 1.1~2.0m FRP 쇼핑몰 조형물 OBJ/STL/GLB + 도색 사양 | - | 결과 증빙 없음(1커밋) | 신뢰도 낮음 | [GitHub](https://github.com/KaelNebula/rodin-via-blender) |
| C12 | 2026-09 | AIWHOS | Codex | Hyper3D Rodin, Blender MCP | 스케치 → 캐릭터(Design Lock, 사람 승인 게이트) | - | README: 실제 생성·임포트·리깅 미테스트 | 신뢰도 낮음 | [GitHub](https://github.com/AIWHOS/sketch-to-3d-codex) |
| C13 | 미확인 | 한국어 유튜버 | Claude | Blender MCP | 2D 로봇 그림 → 3D → 웹 랜딩 페이지 | - | 미확인 | 2차 요약 | [YouTube](https://www.youtube.com/watch?v=I5rtlgAvoV4) |
| C14 | 2026 | squall01337 | 에이전트 | GVHMR, Mixamo 리그, headless Blender | 고정 카메라 영상 → SMPL-X → Mixamo 리타겟 → 2×2 리뷰 영상 모캡 루프 | - | - | 1차 공개 | [GitHub](https://github.com/squall01337/mixamo-llm-mocap) |
| V1 | 2026-09 | Vizuara | Fable 5.1(Claude Code) | Blender 5.2 bpy, Modal A10G, ElevenLabs, ffmpeg | 심장·DNA·중력 등 8~15분 교육 챕터 영상 5편 | 8분3초 챕터 10,964프레임을 A10G 약 50대로 84분 | 수정은 보통 2라운드, 실패 청크 0 | 검증됨 | [GitHub](https://github.com/VizuaraAI/fable-visual-learning-pipeline) |
| V2 | 2026-09-04~05 | Simon Willison | Astra Medium(ChatGPT macOS 앱 Codex 모드) | 로컬 headless Blender CLI(MCP 없음) | 펠리컨 자전거 → 해변 축제 → 석양 퍼레이드, 이후 Blender 스킬 생성 | 2분39초 / 3분51초 / 5분59초 | 토이풍 일러스트 | 검증됨 | [TIL](https://github.com/simonw/til/blob/main/llms/blender-coding-agents-macos.md) |
| V3 | 2026-09-08 | openerai(한국어 스킬) | Claude(Claude Code) | Blender 5.0+, Higgsfield Bridge MCP, Seedance 2.5 | 그레이박스 프리비즈로 카메라·컷·동선 고정 → video-to-video | - | 최종 화면은 AI 영상 **[AI 영상]** | 1차 공개 | [GitHub](https://github.com/openerai/blender-previz-video) |
| V4 | 2026-09-22~23 | Stefan_3D_AI | Opus 5.5 vs Astra(Max로 맞춤) | Blender(절차적 생성만), 빌드 타임랩스 | 10초 렌더 샷, 이후 VFX·캐릭터 애니·풀 씬 라운드 | Opus 35분·출력 199.6k / Astra 28분·56.6k | 모든 라운드를 Opus가 이긴 것은 아님 | 자기 보고(미확인) | [X](https://x.com/Stefan_3D_AI/status/2102471841046786153) |
| V5 | 2026-09 | tonysuri | Astra | Blender | 원본 이미지와 카메라를 맞춘 로마 전장, 2fps 타임랩스, 오브젝트별 GLB | - | - | 2차 요약(프롬프트) | [Tripo 카탈로그](https://github.com/TripoGrowthLab/awesome-3d-prompts) |
| V6 | 2026-09 | Stork.AI 블로그 | Astra | Blender | Astra의 Blender 3D 애니메이션 사례 정리 | - | "후처리가 적게 필요한 에셋"이라는 평 | 2차 요약 | [Stork.AI](https://www.stork.ai/blog/astras-blender-skills-are-unreal) |
| V7 | 2026 | AI타임스 기사 | Opus 5.5, Fable 5.1, GPT-5.6 | 3D 코드 생성 | 물고기 떼·소용돌이·폭풍 속 배·쓰나미 애니, 관람차·제어실 씬 | - | 연출은 Opus 5.5, 비용·속도는 GPT-5.6 | 2차 요약 | [AI타임스](https://www.aitimes.com/news/articleView.html?idxno=215618) |
| T1 | 2026-09-14 보고, 09-21 병합 | Greg Zaal(Poly Haven) | 모델 무관 | mcp-for-blender Poly Haven 통합, Blender 5.2.1 | normal·displacement 미연결, 타일링 역전 수정 | 다운로드 49% 감소 | 테스트 248개와 함께 병합 | 검증됨 | [PR #367](https://github.com/ahujasid/blender-mcp/pull/367) |
| T2 | 2026-08-09 종료 | psiQAQ(보고) | - | blender-mcp | 반복 갱신으로 Output·Principled 노드가 중복 → 렌더가 회색 | - | 노드 초기화 헬퍼로 수정 | 1차 공개 | [이슈 #190](https://github.com/ahujasid/blender-mcp/issues/190) |
| T3 | 2026-08 | elithril | (갤러리는 스크립트 경로) | blender-kiln, gltf-transform, gltfpack | GLB 소품 15종, 21,879 tris | 1,456.2kB → 132.7kB(91%) | MCP·headless 결과가 바이트 단위로 동일 | 검증됨(정정 반영) | [GitHub](https://github.com/elithril/blender-kiln) |
| T4 | 2026-02 | KINGWONWOO(한국 개발자로 추정) | Claude, Nano Banana | Claude MCP, Nano Banana MCP, unreal-blender-mcp, UE5 | Blender 노드 셰이더가 UE로 안 넘어가 텍스처 기반 PBR로 전환 | - | 교훈 사례 | 1차 공개 | [GitHub](https://github.com/KINGWONWOO/Unreal_MCP_Persona) |
| T5 | 2026-09 | zorrobyte | Claude Code(MCP 클라이언트) | Qwen-Image, Pixal3D/TRELLIS.2, Blender, meshoptimizer | 상자·펌프 게임 소품(LOD, 콜리전, PBR, manifest) | crate 11.1분, pump 15.6분(RTX 5090) | Khronos validator 통과, Godot 4.7.2 임포트 | 검증됨 | [GitHub](https://github.com/zorrobyte/asset-studio) |
| T6 | 2026-09 | Bingeljell | - | Pixal3D, Hunyuan3D-MLX, TRELLIS.2, SF3D | 같은 입력으로 로컬 백엔드 5종 비교 + 리토폴·리페인트·압축 | TRELLIS.2 Mac 15~35분 | Pixal3D가 원패스 최상, Hunyuan은 한국 불가 게이트 | 검증됨 | [GitHub](https://github.com/Bingeljell/image-to-3dlab) |
| T7 | 2026 | Scenario | 에이전트 무관 | Scenario MCP | 보물상자 소품 worked example | - | 벤더 표준 절차 | 벤더 문서 | [SKILL.md](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/scenario-3d/SKILL.md) |
| T8 | 2026-05 | Meshy | Meshy 5/6/7 | Meshy API·MCP, Unity/UE5/Godot | 엔진별 게임 에셋 파이프라인 | preview 약 30초, refine 약 2분 | 공식 1차 자료 | 벤더 문서 | [GitHub](https://github.com/meshy-dev/game-asset-pipeline) |
| T9 | 2026-09 | SS-360 | Codex·GPT-5.6(개발 도구) | MaterialPilot MCP, Material Maker 1.7 | '버려진 공장 바닥' 편집 가능 절차 재질 + 2048 PBR | - | 0.1.0 preview | 1차 공개(검증 없음) | [GitHub](https://github.com/SS-360/materialpilot) |
| T10 | 2026 | NVIDIA Omniverse | VLM 선택 | usd-content-agents Material Agent | USD 에셋 부위별 물리 기반 재질 할당 | - | Beta | 1차 공개 | [GitHub](https://github.com/NVIDIA-Omniverse/usd-content-agents) |
| T11 | 2025~2026-02 | Kim2091, NVIDIA | 자체 모델(CC0 데이터 학습) | PBRify_Remix, ComfyUI-RTX-Remix | 구형 게임 텍스처 업스케일 + PBR 맵 | - | 학습 데이터 출처가 명확 | 검증됨 | [GitHub](https://github.com/Kim2091/PBRify_Remix) |
| T12 | 2026-05 | matthieuhuguet | Claude Code 등 | substance-designer-mcp, SD 15.0.3 | cracked concrete·weathered steel·절벽 heightmap 그래프(노드 37~44) | - | 병렬 호출하면 멈춤 | 1차 공개 | [GitHub](https://github.com/matthieuhuguet/substance-designer-mcp) |
| T13 | 2025-10~2026-09 | sakalond 외 | SDXL, FLUX, Qwen-Image-Edit, TRELLIS.2 | StableGen(Blender 애드온) | 생성 → 멀티뷰 재텍스처 → PBR 분해 → 베이크 | - | Blender 5.0 미지원 | 검증됨 | [릴리스](https://github.com/sakalond/StableGen/releases) |
| T14 | 2023~2026 | Princeton VL | - | Infinigen | 절차 실내 재질(대리석·나무·브러시드 메탈·패브릭·엣지 마모) | - | 수치는 풍부, metallic 0.37 같은 비물리 중간값 | 검증됨 | [edge_wear.py](https://raw.githubusercontent.com/princeton-vl/infinigen/main/src/infinigen/assets/materials/wear_tear/edge_wear.py) |
| T15 | 2026 | dcc-mcp 조직 | 미상 | dcc-mcp-marmoset, Toolbag 4.03+/5.x | FBX PBR 룩뎁 렌더(1920×1080) | - | 예제 1건 | 1차 공개 | [GitHub](https://github.com/dcc-mcp/dcc-mcp-marmoset) |

---

## 2. 분야별 상세

주요 사례는 **어떻게 했나(단계) → 잘된 점 → 한계 → 교훈** 순서로 적고, 나머지는 분야 끝의 짧은 표로 묶었습니다.

### 2.1 인테리어·가구·건축

#### A3. Realsee 스캔 → 편집 가능한 Blender 실내 (2026-09-11~15 · Astra/Codex · 검증됨)

**어떻게**
1. Realsee 내보내기(CAD, 포인트클라우드, 파노라마, 텍스처 스캔. 원본 396개 파일, 5.66 GiB)를 입력으로 줍니다.
2. 공개 프롬프트로 순서를 강제합니다([prompts/quickstart](https://github.com/realsee-developer/realsee-astra-blender)).
   ```text
   first understand how the areas connect, then build the walls, floors, ceilings,
   doors, windows, and openings. Add the main furniture afterward, leaving small
   objects until later... Model only spaces evidenced by the inputs.
   Record unclear areas instead of inventing additional rooms.
   ```
3. 소스끼리 위치·스케일을 맞추고 원본 스캔은 숨긴 참조로 남깁니다.
4. 저장한 뒤 다시 열어 벽 한 구간과 문 하나를 실제로 편집해 봅니다(`tools/project.py` smoke 테스트가 저장 → 재열기 → 편집을 별도 프로세스 3개로 확인).
5. 후속 지시: "가구를 숨기고 평면도와 입구 → 각 방 연결을 보여 줘."

**잘된 점**: 구조가 먼저라는 순서와 "근거 없는 공간은 만들지 말고 기록" 규칙이 명확합니다. 편집 가능성을 말이 아니라 테스트로 증명합니다. 코드·프롬프트는 MIT입니다(데이터 권리는 별도).
**한계**: 스크립트가 이 공간 전용이라 그대로 다른 집에 쓸 수 없습니다(README에 명시).
**교훈**: 공간 구조가 틀리면 가구 배치는 전부 의미가 없습니다. 근거 없이 방을 추가하는 것이 흔한 오류라서, 프롬프트 규칙으로 막아야 합니다.

#### A1. OpenAI 런치 데모 'Solace' 하우스 (2026-09-03~04 · Astra · 벤더 쇼케이스)

**어떻게(확인된 범위)**: Blender Python으로 씬을 만들고 → 미리보기 렌더로 구도·조명을 조정하고 → Cycles 카메라 투어를 렌더한 뒤 → UE5로 옮겨 실내를 자유롭게 걸어 다니게 했습니다. OpenAI 공식 워크스루는 "Codex의 Astra + 같은 컴퓨터의 Blender + 둘 다 접근하는 프로젝트 폴더" 구성이 가장 실용적이고, 코드 작성·실행 → 결과 검사 → 프리뷰 렌더 → 문제 식별 → 수정 루프를 돈다고 설명합니다(검색 요약 기준, 원문 미열람).
같은 계열 쇼케이스로 Courtyard House(외관, 지붕을 걷어낸 단면, 평면도 연동), Architecture Studio(같은 방 데이터로 치수 평면도와 3D를 동기화해 가구 배치·회전·마감 변경), Physics Museum이 있고, 같은 글에 HELIOS 태양 집광 구조물, AURELION-07 순양함, 지베르니 수련 정원도 있습니다([carpentry-liu cases.json](https://raw.githubusercontent.com/carpentry-liu/awesome-astra-3d/main/data/cases.json)).
**잘된 점**: 지오메트리·머티리얼·조명을 편집 가능한 상태로 UE5까지 넘겼습니다.
**한계**: 원문이 차단되어 세부 단계·시간·토큰을 확인하지 못했습니다. 모델 팀의 런치 데모라 선별된 결과입니다.
**교훈**: **평면도와 3D를 같은 데이터에서 동기화하는 구조**(Architecture Studio)가 가구 배치를 고칠 때 유리합니다.

#### A5. kitchen-twin: 휴대폰 영상 → 조인트가 있는 주방 트윈 (2026-09-11 · Astra · 1차 공개, 파이프라인 비공개)

**어떻게**: 휴대폰 워크스루 영상 → ViPE metric scan → 인스턴스 분할 → 에셋별 치수 측정 → Astra가 작은 Blender 모델링 언어로 모든 에셋을 작성 → **독립 verifier 세션**이 영상 프레임과 스캔으로 대조하며 반복 렌더 검증 → export(scene.glb 약 15MB). verifier 규칙은 "must justify every complaint with a frame"입니다([큐레이션 README](https://raw.githubusercontent.com/Frank-ZY-Dou/awesome-ai-3d-modeling-robotics/main/README.md)).
**잘된 점**: 측정값에서 출발하고 검증 세션을 따로 둬서 에셋 32개, 작동 조인트 138개를 만들었습니다.
**한계**: 저자가 "thin and shiny things are still weak, a few objects are drafts, the room shell needs another pass"라고 밝혔습니다. 파이프라인 소스가 비공개라 재현할 수 없습니다. 조사 단계에서 적은 'parts/joints/dimensions DSL' 구조와 MJCF/URDF 출력은 README에 없는 내용(큐레이션 요약)입니다.
**교훈**: 가구 치수는 모델의 기억이 아니라 **측정값**에서 가져오고, 검증자에게는 "근거 프레임 없는 지적 금지"를 규칙으로 줍니다.

#### A6. Unreal Home Wizard: 매물 사진 → 걸어 다닐 수 있는 UE 프로젝트 (2026-09-21 · Astra/Codex 스킬 · 1차 공개)

**어떻게**([SKILL.md](https://raw.githubusercontent.com/amirmushichge/unreal-home-wizard/main/skills/unreal-home-wizard/SKILL.md))
1. 사진 재현 모드: 임의로 다시 디자인하지 않습니다.
2. 보이는 모든 오브젝트의 physical logic, support, mounting, placement를 하나씩 검증합니다.
3. floating, 관입, 구멍, light leak, Z-fighting을 결함으로 보고 수리합니다.
4. 러프 레이아웃 승인 → 최종 뷰 승인의 두 단계 게이트를 둡니다.
5. 천장고나 문 폭 같은 알려진 치수 하나를 물어 스케일을 맞춥니다.

**잘된 점**: "사용자는 1차 버그 탐지자가 아니다"라는 원칙으로, 떠 있는 쿠션·지지 없는 조명·바닥에서 뜬 가구가 최종 결과에 남지 않게 했습니다.
**한계**: Codex용 스킬이고 결과 품질 수치는 없습니다(조사 단계의 'Sol·Opus 5.5도 명시'는 원문에 없음).
**교훈**: 물리 논리 검사는 에이전트가 먼저 하게 하세요. 이 저장소의 [`scene_audit.py`](../03_playbooks/scripts/README.md)가 떠 있음(`floating_or_wall_mounted`), 바닥이나 다른 물체 속으로 박힘(`sunk_into`), 유닛 간 관통, 가구가 벽·천장 오브젝트를 뚫음, 지정한 천장 높이(`ceiling_z=2.30` 등) 위로 솟음을 숫자로 잡습니다. 방만 따로 보려면 `collection="Room"`처럼 컬렉션 범위를 지정합니다.

#### A4. 같은 평면도로 4가지 인테리어 스타일 비교 (2026-09-05~08 · Astra vs Fable 5.1 · 1차 공개)

**어떻게**: 주거 평면도 한 장으로 공간 9개, 배색 3종, 가구 64점(모던 기준)을 만들고, Cycles로 8K 데스크톱·4K 모바일 파노라마와 Three.js 실시간 뷰어를 만들었습니다. 송대풍은 박물관 자료를 조사해 설계했습니다. 같은 방·같은 스타일로 3분짜리 3200×1800 비교 영상 2편을 만들었습니다.
**한계**: 원본 프롬프트·시간·비용·샘플링을 공개하지 않았고 카메라와 조명도 달라서, 작성자가 직접 "엄격한 순위 불가"라고 밝혔습니다. 모델명은 유지보수자 라벨 기준입니다. 저장소 라이선스는 Apache-2.0입니다.
**교훈**: 비교 방법(같은 기기·같은 방·같은 시점)과 비교 항목(가구 비례, 동선, 재질, 조명)은 그대로 가져다 쓸 만합니다.

#### A13. SketchUp MCP로 건축 모델링 3종 테스트 (2026-09 · Astra · 2차 요약)

**어떻게**: MCP 서버로 SketchUp에 Ruby 스크립트를 실행해 ① 앞·뒤 사진으로 집 재현, ② 치수가 적힌 평면도로 모델링, ③ 오픈소스 19쪽 도면 세트로 농가 전체를 지었습니다([daily.dev 요약](https://daily.dev/posts/i-tested-gpt-astra-for-3d-modeling---this-is-getting-serious-to6zgaa2h)).
**결과**: 모델당 17~22분에 외관은 인상적이었지만, 인테리어 정확도가 떨어지고 치수가 빠졌으며 **문 여는 방향이 틀렸습니다**. 토큰을 많이 써서 Plus 주간 할당량을 하루에 소진했습니다. 제작자 평은 "아직 사람 모델러를 대체할 수준은 아니지만 가까워지고 있다"입니다.
**교훈**: 문 스윙 방향, 개구부 치수 같은 인테리어 요소는 스펙에 명시하고 따로 검사해야 합니다. 치수 기준은 [실측 치수표](../03_playbooks/05_reference_dimensions.md)를 쓰세요. 문이 벽에 실제로 뚫렸는지, 열면 벽·허공으로 나가는지는 [`building_audit.py`](../03_playbooks/scripts/README.md)로 검사할 수 있습니다(문은 `Door_...`, 방 바닥은 `Floor_living`처럼 이름 규칙을 지켜야 함).

#### 사진·평면도 한 장에서 가구가 있는 공간으로 (A2, A7~A12)

| 사례 | 어떻게 | 잘된 점 | 한계 |
|---|---|---|---|
| A2 Tom Krcha | 주택 사진 1장을 주고 "모든 디테일을 편집 가능한 개별 오브젝트로" 만들라고 요구 | 가구·가전·장난감까지 분리, 60fps 워크스루 | 치수 정확도 미검증. 같은 작성자의 Porsche 서브디비전 사례(09-09) 교훈은 "Naive prompts will fail, refined systematic prompts written by an expert succeed" |
| A7 Wentao Zhu | 아래 프롬프트 한 번 | 관절 가구 요구의 좋은 템플릿 | 결과 품질 미확인 |
| A8 yamahigashi | 참조 이미지·평면도 → 요소 분해 → 소품마다 Imagegen 2.5로 디자인 → Tripo P2.0으로 3D → Blender MCP + computer use로 배치 | 한 번에 소품까지 배치 | 작성자 "세부가 꽤 틀리지만 한 번에 이만큼 나오는 건 대단하다" |
| A9 おのふみ | Blender MCP로 구성하고 편집 가능한 Blender 데이터 유지 | 가구를 꺼내고 돌릴 수 있음 | 2차 요약. UE 월드빌딩 조언: "샷별 배경이 아니라 이야기가 일어나는 실제 공간(문 뒤에 무엇이 있는지)을 설계하라" |
| A10 AIパースおじさん | 평면도 → Claude Code로 모델과 뷰어 생성 | Opus 5.5 가구 배치 사례 | 세부 공정 미확인 |
| A11 Doron Taussy | IKEA 의자 사진 1장 → 치수, 재질 전환, 부품 검사, 분해도, flat-pack, 자가 조립 | 가구 부품 분해 주제에 가장 직접적인 사례 | 자기 보고(원문 미열람) |
| A12 Shimecki | 새 침대가 아이 방에 맞는지 Opus 5.5로 확인 | 배치·치수 확인 용도 | 자기 보고 |

```text
# A7 Wentao Zhu가 쓴 프롬프트 (Tripo 카탈로그 경유, 2차)
Given the room photo I provided, use Blender MCP to build an interactive 3D scene and
render it into a demo video. Include articulated object motion (hinges, doors, drawers)
and use sensible camera moves to show these effects.
```

#### A14. McNeel Rhino MCP 공식 레시피 (2026 · 벤더 문서)

치수를 mm 단위로 박아 넣은 프롬프트로 만들고, 대화로 고치는 방식입니다([레시피](https://raw.githubusercontent.com/mcneel/RhinoAI/rhino-9.x/docs/content/docs/try-it-out/recipes.md), [make-this-parametric](https://raw.githubusercontent.com/mcneel/RhinoAI/rhino-9.x/docs/content/docs/advanced/make-this-parametric.md)).
- 월넛 커피 테이블: 상판 1200×600×30mm, 다리 400mm, 5° 벌어짐
- 나선 계단: 20단, 단 높이 250mm, 반경 1.5m, 30mm 오크 트레드(단 높이는 레시피 값이니 실제 설계는 [실측 치수표](../03_playbooks/05_reference_dimensions.md)의 계단 기준으로 확인하세요)
- 프리미티브를 좌판에 섞은 의자 5종 변형
- 스케치는 '해석 먼저' 프롬프트로 처리하고, 사람이 만든 모델은 Grasshopper 2(GH2) 슬라이더 그래프로 역설계합니다. 'Random scatter … No overlaps'(5×5m 영역에 구 200개) 레시피와, `get_viewport_image`로 스케치 각도에 맞춰 비교하라는 안내도 있습니다.

**교훈**: 가구·건축 요소는 치수를 숫자로 주면 형태가 안정됩니다. 결과를 파라메트릭 그래프로 남기면 비율을 나중에 바꿀 수 있습니다.

#### 그 밖의 인테리어·건축 사례

| 사례 | 무엇을·어떻게 | 한계·교훈 |
|---|---|---|
| A15 rhino-mcp 고딕 대성당 | 아치·리브 볼트·트레이서리·몰딩 전용 도구 + 의도 검증(bbox, 엔벨로프, 워터타이트)으로 1:1 대성당(약 8,000 오브젝트) | README 자기 보고. **건축 요소 전용 고수준 도구**가 규모를 만든다 |
| A16 SketchUp 커넥터(공식) | 텍스트·음성 + 참조 이미지·스케치·평면도·치수를 올리면 클라우드 SketchUp 세션에서 지오메트리를 만들고 치수를 반복 검증, 결과는 SketchUp에서 다듬음([Trimble 발표](https://news.trimble.com/2026-04-28-Trimble-Links-SketchUp-with-Anthropics-Claude,-Bringing-New-Conversational-AI-powered-Capabilities-to-3D-Modeling)) | 도구 3개뿐. '무료 30개 저장'은 미확인 |
| A17 뽁숑이 | Claude 커넥터(MCP)로 SketchUp 자동 모델링 → AI 렌더링 | 건축·인테리어 실무 관점의 한국어 시연 |
| A18 Fallingwater | 세션 확인 → 브리프를 검사 기준으로 변환 → 의존 순서대로 빌드(단위·레퍼런스·큰 형태·카메라 → 구조·두께·조인트·틈 → 재질 → 조명) → 렌더 벤치마크 → 증거 기반 QA와 defect ledger | 스킬은 커밋 1개, 0★, Claude 공동 작성. '무인 54시간'은 큐레이션 인용 |
| A19 Bad Decisions Studio | 휴대폰 사진을 참조로 넣어 30분 안에 건물 재구성([AI매터스](https://aimatters.co.kr/news-report/51830/)) | 다른 보고에서는 사진 재구성 때 원본에 없는 요소를 지어낸다는 지적 |
| A20 SpenserFX | 사람이 약 10시간, 21라운드에 걸쳐 골대 구조와 바닥 마감을 지시 | 고품질 결과에는 **사람의 반복 디렉션**이 필요하다는 대표 사례 |
| A21 MindStudio 보도 | 주소와 느슨한 브리프 → 지오메트리·지형·인테리어·조명·조경 코드 → 카메라 경로 → 프리뷰 스틸 자가 점검 → 최종 렌더 | **신뢰도 낮음**(벤더 SEO 블로그, 서버 종류·재현 절차 없음). 미검증 주장으로만 참고 |
| A22 aigeboku | Claude Desktop + Blender MCP, Gemini로 레퍼런스 이미지, Hitem3D API로 GLB, 여러 에셋 병렬 생성 | **신뢰도 낮음**(커밋 1개, 결과 증빙 없음). 설정 가이드로만 참고 |
| A23 Fraktal / A24 Vagon | 설계 브리프·레퍼런스 이미지 → Astra가 Blender 씬 코드 작성 → 비교·수정 → (UE5 탐색) | 디자인 스튜디오·클라우드 벤더의 워크플로 글. 수치 없음 |
| A25 retriever | 스탠퍼드 주방 영상 → 작동 서랍이 있는 MuJoCo 씬. 런타임 코드 공개 | kitchen-twin과 같은 계열의 '영상 → 조인트 수납가구' |

> **실무자 평가**: Adam Keating은 "looks like the thing you want"는 쉬워졌지만 "The gap remains in the last mile - particularly in manufacturing"이라고 적었습니다([LinkedIn](https://www.linkedin.com/posts/adammichaelkeating_astra-is-far-better-at-understanding-geometry-activity-7503061853816696832-7CRf), 자기 보고).

#### 인테리어·가구 사례에서 나온 규칙

1. **구조 → 주요 가구 → 소품** 순서로 짓습니다(A3, A6, A8).
2. 가구는 **개별 오브젝트**로 나누고 이름을 붙입니다(A2, A9). 이 저장소 스크립트는 의자 부품을 하나의 부모 아래 묶는 규약을 씁니다([스크립트 규약](../03_playbooks/scripts/README.md)).
3. **치수 앵커**를 하나 받습니다(천장고나 문 폭). 한국 아파트·가구 규격은 [실측 치수표](../03_playbooks/05_reference_dimensions.md)에 따로 있습니다. 천장고를 정했으면 `scene_audit.audit_scene(ceiling_z=2.30)`처럼 넘겨 천장을 뚫는 가구를 잡습니다.
4. **근거 없는 공간·요소는 만들지 말고 기록**합니다(A3). 사진 재구성에서 지어내기가 흔합니다(A19).
5. 가구를 숨긴 **탑다운 평면도**와 입구에서 각 방으로 가는 동선을 확인합니다(A3). 가구 간격은 [`placement_utils.check_clearances()`](../03_playbooks/scripts/README.md)로, 갈 수 없는 방·문 없는 방은 [`building_audit.py`](../03_playbooks/scripts/README.md)로 숫자 검사합니다.
6. 문·서랍이 움직여야 하면 처음부터 **관절 구조**를 요구합니다(A5, A7).
7. 문 스윙 방향·치수 누락은 모델이 자주 틀리므로 스펙에 적고 검사합니다(A13). 열면 벽에 막히거나 허공으로 나가는 문은 `building_audit.py`가 잡습니다.

### 2.2 제품·하드서피스·기계·CAD

#### P1. 증기기관차 그림 → 편집 가능한 오브젝트 3,295개 (2026-09-04 · Astra · 자기 보고)

**어떻게**: 오래된 증기기관차 그림 한 장을 주고 바퀴, 차축, 서스펜션, 로드까지 이름 붙은 기계 어셈블리로 재구성하게 했습니다. 디테일 수준은 프롬프트로 조절했고, 도구 경로는 "primarily MCP, with occasional computer-use checks"로 밝혀져 있습니다. 이후 Three.js 런타임 코드만으로 기차를 생성하는 'living code' 버전도 공개했습니다.
**잘된 점**: 대규모 부품 분해 모델링이 가능하다는 것을 보였습니다(작성자 보고로 몇 분 만에).
**한계**: 치수 정확도는 검증되지 않았습니다.
**교훈**: 기계·하드서피스는 **부품 단위로 이름 붙인 계층**으로 만들게 하면 이후 수정과 애니메이션이 쉬워집니다. 같은 작성자의 교훈: 전문가가 쓴 체계적 프롬프트는 성공하고, 순진한 프롬프트는 실패합니다.

#### P2. 같은 프롬프트로 6날 기계식 조리개 (2026-09-08 · Astra vs Fable 5.1 · 검증됨)

**어떻게**: 프롬프트 해시를 동결하고 비교 프로토콜을 사전 등록한 뒤, 생성 코드를 고치지 않고 같은 하네스(Blender 5.2.1 LTS EEVEE, 64 samples, AgX, 960×960, 30fps, 16초)에서 렌더해 나란히 비교했습니다. 실패한 시도 기록도 남겼고, 생성 코드는 네트워크 차단 래퍼에서 실행했습니다. 도구를 끈 **순수 코드 생성 비교**라서 MCP나 시각 피드백 루프는 없습니다.
**결과**: 두 모델 모두 실제로 변하는 개구부와 액추에이터를 구현했습니다. 결함도 둘 다 있었습니다.
- Astra: 지지 스페이서가 액추에이터와 겹치고, 일부 날이 피벗 축에서 빠지기 전에 옆으로 움직였습니다.
- Fable 5.1: 날 뿌리에 핀 구멍이 없고, 받침대가 후면판과 닿지 않았습니다.
**한계**: 과제 1개, 하네스가 서로 달라(Codex CLI 0.153.4 대 Claude Code 2.1.263) 순위 근거로 쓸 수 없습니다. 작성자도 순위를 매기지 않았습니다.
**교훈**: **"움직이는 것처럼 보이는 것"과 "기계적으로 맞는 것"은 다릅니다.** 관절·결합은 렌더만 보지 말고 겹침·접촉을 숫자로 확인하세요. 비교 프로토콜은 5.4절에 정리했습니다.

#### P9. cc-blender-skill: 스킬로 소품 6종 엔드투엔드 검증 (v1.3.0 · Claude Code · 검증됨)

**어떻게**: 오케스트레이터 `text-to-blender`가 10단계로 진행합니다. 의도 파악 → MCP 확인 → 월드 리셋(color 0.04/0.04/0.05, strength 0.4) → 실측 치수 조회(7개 카테고리 치수표) → 하위 스킬 로드 → 조립 순서대로 5~20줄 청크 실행 → scene/object info와 스크린샷으로 검증 → 반복 → 수치와 렌더 경로 보고. 작업 순서는 block-out → camera → lighting → forms → materials → detail → render → composite → export로 고정합니다. 레퍼런스가 있으면 IoU·SSIM·bbox 드리프트로 검증하고, 기준에 못 미치면 quality-refinement-autoloop가 원인을 진단하고 스킬을 패치해 다시 빌드합니다.
**잘된 점**: 실패한 렌더까지 저장소에 공개했습니다('no cherry-picking'). 검증용 proof render 28장이 있고, 트리거 평가는 TP 100%, FP 4%입니다. 테스트는 Haiku, 패치는 Opus로 나눠 약 10배 싸게 돌립니다.
**한계**: 저자가 곡면 가구, 프로파일 컷, 다듬어진 실루엣, 사람 얼굴, 얇은 금속의 스펙큘러 플레어를 범위 밖으로 밝혔습니다. Sonnet 4.6·Opus 4.7·Haiku 4.5 기준이라 최신 모델에서는 재검증이 필요합니다. rendering 스킬에 5.x에서 없어진 EEVEE 속성(`use_gtao`, `use_bloom` 등)이 남아 있습니다. **공식 Blender Lab MCP로 "이전했다"는 서술은 틀렸습니다.** PR #1은 제3자가 올린 미병합 PR이고, main은 여전히 ahujasid 서버(9876)를 씁니다.
**교훈**: 치수표 + 고정 순서 + 시각 검증 + 실패 진단 루프를 스킬로 묶으면 하드서피스 소품은 재현 가능한 품질이 나옵니다. 미감은 여전히 사람 몫입니다.

**같이 볼 스킬**: [ProfRino/Blender-MCP-Assembly-Skill](https://github.com/ProfRino/Blender-MCP-Assembly-Skill)은 의자가 '분해되어 보이는' 문제를 막는 규칙집입니다(의자 조립 Before/After 예시). 규칙은 다음과 같습니다.
- 연결부·접촉면·최소 겹침(5mm)을 먼저 계획합니다.
- cube는 `size=2`로 만들어 scale 값이 half-extent(절반 길이)와 같게 합니다. LLM의 대표 버그는 size=1에 scale을 줘서 치수가 절반이 되는 것입니다.
- 다리·봉 같은 방향성 부재는 Euler 회전 대신 bmesh로 두 점 사이를 잇습니다.
- 스케일 직후 transform을 적용하고, `verify_bounds()`·`verify_overlap()`·`audit_all()`을 호출합니다.

LICENSE 파일은 없고 정량 평가도 없습니다. 이 저장소의 `scene_audit.py`는 한 유닛(부모) **안의** 부품 틈·관통은 검사하지 않으므로, 부품 조립은 [오브젝트 모델링 가이드](../02_guides/07_modeling_objects_furniture_sculpture.md) 2.4절의 `check_assembly()`로 확인하세요.

#### P12. Onshape MCP 도면 → CAD (Opus 4.7 · 검증됨)

**어떻게**: 사람이 쓴 사양 대 자율 비전 분해, 단순(Model Mania 2025) 대 복잡(2021) 부품의 2×2 실험을 브리프당 150턴 예산으로 돌렸습니다. plan-from-render, 렌더 비교, 치수 교차 확인, OCR 같은 개선책도 시험했습니다.
**결과**: 사람 사양 1.000/0.615, 자율 비전 0.533/0.000. 이 값은 바디 존재·부피·bbox·토폴로지·IoU·Chamfer 6개 층을 합친 composite 점수이고, 각 칸은 부품 하나(n=1)입니다. 2021 자율 실행의 0.000은 151턴 한도에 걸려 export하지 못한 결과입니다. 개선책 중 feature를 먼저 나열하는 plan-from-render만 +0.04(노이즈 수준)였고 나머지는 퇴행했습니다. 주요 실패 원인은 파생 윤곽(derived outline), 돌출·함몰 혼동(polarity), 8~12px 치수 텍스트였습니다.
**교훈**: 원문 결론 "Opus 4.7 executes CAD reliably. It does not yet read engineering drawings reliably." **도면 해석은 사람이 스펙으로 바꿔 주는 것**이 가장 큰 개선입니다.

#### P13. CADGenBench에서 build123d-mcp로 3개 모델 비교 (2026-07~09 · 도구 저자 자체 평가)

**어떻게**: 과제 유형별 범용 프롬프트(checkpoint-first, validity-as-invariant)로 MCP에서 증분 빌드 → measure → compare → validate → 제출. fixture별 튜닝은 금지했습니다.
**결과**: Opus 5 0.6771(생성 0.6583/편집 0.7058), GPT-5.6 Sol 0.5319, Gemini 3.7 Flash 0.5078, 셋 다 81개 중 80개 valid. 편집 점수는 거의 같았고 차이는 생성에서 났습니다. build123d-mcp README는 도구만 붙여도 한 모델의 점수가 0.360에서 0.457로, validity가 88%에서 100%로 올랐다고 보고합니다(모델명 미공개).
**한계**: 비교한 사람이 도구 저자 본인이고, Opus 값은 여러 제출 중 'best'이며, MCP 버전(0.3.81/0.3.79/0.3.83)·하네스·실행 시기가 모두 다릅니다. 토큰·비용 비교(Opus +44%, 약 $724.77)는 문서 스스로 방향성 참고용이라고 밝힙니다.
**교훈**: 정밀 부품은 **코드 CAD(build123d/CadQuery) + 측정·검증 도구**가 안정적입니다. FreeCAD GUI를 클릭하는 에이전트는 최고 성공률도 17.5%에 그쳤습니다(CADWorld, 전문가 87.0%).

#### P3. Higgsfield의 Opus 5.5 쇼케이스 (2026-09-22~24 · 벤더 쇼케이스)

좌석 430개까지 개별 오브젝트로 만든 신칸센(오브젝트 5,112), 모델링·리깅·텍스처링·애니메이션까지 한 풍차, 사진 한 장으로 재구성해 구조 붕괴 시뮬레이션을 돌린 건물, 목탄 드로잉 질감을 유지한 3D 씬입니다([X 1](https://x.com/higgsfield_ai/status/2102507018372436264), [X 2](https://x.com/higgsfield_ai/status/2102453658889953717), [Opus 5.5 데모 목록](https://github.com/magiccreator-ai/awesome-claude-opus-5-5-demos)). 하드서피스 대량 반복 구조와 리깅·애니메이션 파이프라인을 처리할 수 있다는 홍보입니다. 큐레이션 목록에는 'product showcase'로 표시되어 있고, '15분 풍차'는 해당 목록에서 찾지 못했습니다.

#### 그 밖의 제품·하드서피스 사례

| 사례 | 무엇을·어떻게 | 한계·교훈 |
|---|---|---|
| P4 Danny Stuart / Hierarchy | 같은 시작 프롬프트로 두 모델에 Blender MCP 작업. Astra는 Python 작성 → 백그라운드 렌더 → 이미지 확인 → 비례가 맞을 때까지 수정 | 결론 "공간 작업은 Astra, 소프트웨어 완성과 오케스트레이션은 Fable 5.1"(5절) |
| P5 Alexey Fateev | 사진 4장으로 GPU 리그를 두 모델이 각각 모델링 | 세부 결과 미확인 |
| P6 3DVR3 | Quest 3 사진 → 모델. Opus 5.5가 부위별로 나눠 작업 | 두께·기울기·흑백 밸런스는 Opus 5.5 우세(n=1) |
| P7 Spectro | "에이전트를 붙여 다리 설계를 맡겨", "새 GLB를 씬에 주입해", "엔진과 파워트레인은 재사용할 수 있게 저장해"처럼 부위별로 서브에이전트에 배분, 제약을 따르는 다리 리그로 힘 계산까지 요구 | 공학 타당성 미검증. **부위별 모듈을 저장해 재사용**하는 흐름이 유용 |
| P8 Houdini·Rhino·3ds Max | 참조 이미지를 주고 DCC를 직접 조작. Rhino는 구조 생성·레이어 관리·디테일 수정 | "여전히 문제가 있다"(Nick), "여러 번 수정 요청 필요"(Yokohara), "떠 있는 글자, 비율 수정 필요"(iPentec). Rhino 40분은 계획안 수준. **효율은 좋지만 마감은 사람 몫** |
| P10 Gaius114 | research 스킬로 spec_sheet → 분해 계획을 plan_validator로 검증 → execute → render → analyze → iterate | 형상을 만들기 전 **계획 검증 게이트**로 한 번에 통째로 만들 때의 실패를 줄임 |
| P11 KANA 꽃집 | 의미 있는 구조 레이어로 분해, 자판기 패널과 병·캔까지 분리, 요소마다 타이밍·속도 다르게, 분해 상태에서 멈췄다가 역재생, 분해 구간은 중립 스튜디오 배경, **모든 오브젝트와 컬렉션에 이름** | 편집 파일 비공개. 계층 분해·이름 요구가 배치·편집에 유리하다는 예 |
| P14 FreeCAD MCP | Claude Desktop 자연어 → FreeCAD 안에서 Python 실행 → 스크린샷 피드백 | CAD MCP 중 가장 많이 쓰임(2.5k★) |
| P15 Cordyceps | Grasshopper(GH) 캔버스 구성·배선 → Rhino bake → 포토리얼 재질 → 조명·렌더 → 카메라 오빗 | 품질 평가 없음 |

### 2.3 환경·도시·레벨

#### E1. Claude + UE 5.8 공식 Unreal MCP로 뉴욕·도시 구축 (2026-06-18~24 · Claude Code · 검증됨, 정정 반영)

**어떻게**
1. 루프: 행동(`mcp__unreal__call_tool`) → `EditorAppToolset.CaptureViewport`(좌표 그리드 주석 포함) → `ue_qa.py`로 base64를 디코드해 작은 PNG와 JSON 사이드카로 → 판독 → 수정. 수 MB짜리 base64 PNG가 컨텍스트를 채우지 않게 파일로 뺐습니다.
2. 빌드 단계마다 **탑다운, 눈높이, 플레이어 시점** 3각도 QA를 했습니다. 에셋 준비는 병렬, 에디터 변경은 직렬(게임 스레드가 하나)로 처리했습니다.
3. 같은 도시를 5가지 방식으로 비교했습니다([가이드](https://raw.githubusercontent.com/per-simmons/unreal-agent-harness/master/AGENTIC-GAMEDEV-GUIDE.md)).

| 방식 | 결과 |
|---|---|
| M1 프리미티브 | 흰 박스 |
| M2 CC0 키트(Quaternius downtown-city-megakit, 모듈 153개) | **가장 깨끗한 실제 건물** |
| M4 headless Blender | 형태 제어는 좋지만 재질 없음 |
| M5 Meshy(fal.ai) | 약 4분, PBR이지만 얼룩지고 스케일·방향이 틀림 |
| M6 TRELLIS(Replicate) | 약 1분, 알아볼 수 있고 가볍고 부드러움, 색만 있음, "looked good, just small" |

4. 실제 도시 데이터: Cesium for Unreal v2.27(소스 빌드) + Google Photorealistic 3D Tiles, NYC Building Footprints(heightroof), 2017 NYC 1-ft LiDAR DEM(EPSG:2263 피트 → ×0.3048), Blender-OSM(OSM 높이 태그는 약 31%에만 있음), Epic City Sample. Cesium 가로 수준 설정은 가이드가 MaximumScreenSpaceError 6(히어로 샷 4), MaximumCachedBytes 1GB, ForbidHoles true를 권했지만, BUILD-LOG는 비행 중에는 4가 너무 공격적이라 8로 되돌렸습니다(4는 정지 히어로 샷에만).
5. 사실감 패스: 변주, PBR 노멀, 데칼, 장식, 거리 소품. 가장 사실적인 결과는 깊은 베벨 릴리프와 청동 장식(2번째 머티리얼 슬롯)으로 돌과 금속의 대비를 준 **아르데코 블록**이었습니다([REALISM-GUIDE](https://github.com/per-simmons/unreal-agent-harness/blob/master/docs/REALISM-GUIDE.md)). 파리 오스만 블록은 파사드 변형 12, 톤 5, 가로수 20, 가로등 12, 벤치 6, 주차 차량 5대입니다. PCG(절차적 콘텐츠 생성)로는 글래스 grammar 타워 49개(7×7, ISM(Instanced Static Mesh) 147개, 빈 스폰 0, 파사드 틴트 5종)를 City Sample 프로젝트 안의 빈 Startup 맵에 세웠고, 같은 날 글래스 타워 14개를 실제 City Sample 레벨에 배치했습니다([PCG-GUIDE](https://github.com/per-simmons/unreal-agent-harness/blob/master/docs/PCG-GUIDE.md)).

**실패와 수정**
- Boeing 787 메시가 100배(약 6km)로 들어옴 → `RelativeScale3D=0.01`
- 조명: 골든아워 PPV(Post Process Volume) 노출 11이 클리핑 → PPV를 빼고 오토 노출 + 4000K·피치 -8° 골든아워 → 너무 주황빛이라 6500K·피치 -38°·강도 6으로 복귀
- 노멀 강도 8과 1.5는 과했고 0.3이 적정
- City Sample chair-kit은 폭 축이 달라 조립이 들쭉날쭉
- Cesium 스플랫 서브시스템 크래시 → 엔진 쪽 패치, Cesium 타일셋에 FocusOnActors를 쓰면 크래시
- UE MCP 설정 함정(원문 표현은 'Gotchas that cost an hour'): `bAutoStartServer=false`라 직접 시작해야 함, 기본 포트 8000이 다른 앱과 충돌해 `EditorPerProjectUserSettings.ini`에서 8123으로 변경, 기본 비활성 툴셋 플러그인 약 28개 → AllToolsets + PythonScriptPlugin 활성화, `StaticMeshTools.import_file`은 FBX/OBJ만 받고 GLB는 안 됨

**잘된 점**: 공식 MCP만으로 도시 규모 배치·조명·QA 루프가 가능함을 수치와 함정까지 공개한 가장 구체적인 기록입니다.
**한계**: 무료 소스 중 도시 전체이면서 가로 수준까지 선명한 것은 없었습니다(Google 타일은 가로 수준에서 녹아내리고, 스플랫은 블록 하나 단위). macOS·M4 Max 기준이고 Claude 버전을 밝히지 않았습니다. **LICENSE 파일이 없어 재사용 권한이 없습니다.** Sci-fi 스테이션 실내는 계획만 있고 조립은 대기 상태입니다(조사 단계의 'SF 실내를 만들었다'는 틀림).
**교훈**: "에이전트는 우리가 눈을 만들어 주지 않으면 못 본다." "하네스가 학습보다 낫다." 결론은 **CC0 키트는 대량 반복용, Blender는 고유 형태용, 이미지→3D는 일회성 소품용**입니다. "실험적 AI 도구는 진짜지만 거칠다(real but raw). 배관 작업에 시간을 잡아 두라."

#### E2. Fable 5.1 에이전트 스웜의 Union Square SF 트윈과 리뷰어 9명의 점수 (2026-09-02 · 검증됨)

**어떻게**
1. 정찰 에이전트가 지도, 표고, 상점 센서스를 출처와 신뢰도 표시와 함께 수집
2. 스크립트로 파사드 모듈, 가구, 차량 키트 생성
3. JSON 스펙에서 Three.js가 조립
4. Playwright로 고정 시점 34곳을 캡처해 실사진과 나란히 비교(시트 147장)
5. 리뷰어 에이전트 9명(건축가, SF 현지인, 환경 아트, 테크 아트, 인터랙션 등)이 리포트 → 수정 사이클. 원칙은 **"빌더는 자기 작업을 채점하지 않는다"**

**결과**(조정하지 않은 2차 패스 점수, [FINAL_QA_REPORT](https://raw.githubusercontent.com/PhiloLabs/fable51-worlds/main/union-square-sf/FINAL_QA_REPORT.md))

| 항목 | 점수 | 목표 |
|---|---|---|
| 지리 정확도 | 7.5 | 9 |
| 건물 인지도 | 5.5(수정 후 추정 6.5) | 9 |
| 상점 | 6 | - |
| 가로 디테일 | 6 | - |
| 시각 충실도 | 6 | 8.5 |
| 재질 | 6 | 8.5 |
| 조명 | 7 | 8.5 |
| 성능 | 6(가로 57~89fps) | 8.5 |
| 완성도 | 6.5 | - |

잡아낸 결함: 벽 폴리곤 와인딩 반전으로 벽이 사라짐, 도로 마킹 z 미러링, 떠 있는 옥상 박스, 환경맵 이중 계산으로 노출 과다. 남은 문제: 1~3m마다 반복되는 절차적 텍스처, 블록 같은 보행자 손. 교토 히가시야마와 Death Star Trench Run 오마주도 같은 방식으로 만들었습니다.
**한계**: 게임 엔진이 아닌 순수 Three.js라 오프라인 렌더 품질과는 다릅니다. 코드는 MIT, 데이터(OSM ODbL, USGS 3DEP)는 별도 라이선스입니다.
**교훈**: 최상급 에이전트 파이프라인으로도 AAA에는 못 미친다는 가장 정직한 증거입니다. 빌더/리뷰어 분리, 실사진과 같은 시점 비교, 조정하지 않은 점수 공개는 그대로 따라 할 만합니다.

#### E5. [한국 추정] ChatGPT 채팅만으로 만든 300×300m 호수 숲 → UE HISM (2026-09-13~14 · 검증됨)

**어떻게**: 50×50m 셀 36개로 나누고 seed 42로 결정적으로 생성합니다. 반복 오브젝트는 메시 데이터블록을 공유합니다. `01_build_scene.py`(Blender 4.2+) → `02_export_unreal.py`(셀·에셋 ID별 FBX와 배치 매니페스트) → UE에서 `03_import_unreal.py`. 반복 에셋은 셀·에셋 ID별 HISM(Hierarchical Instanced Static Mesh), 고유 오브젝트는 Static Mesh Actor로 보냅니다.
**결과**: 지형, 호수·연못, 트레일, 나무 3,800그루(랜드마크 포함 3,839), 인스턴스 16,573개, 재사용 메시 127개, 랜드마크 영역 12곳(호숫가 마을, 캠프장, 과수원, 전망대). 순수 Python 테스트 30개(지오메트리, 배치, 결정성, Blender→UE 변환). MIT.
**한계**: 콜리전, LOD, World Partition은 범위 밖이고, Blender·UE 런타임 실행은 검증 기록에 없습니다. '한국 사례'라는 근거는 README_KO뿐이고, README는 "ChatGPT 대화, Codex 아님"이라고만 적었으며 Astra라는 이름은 저장소 이름에만 나옵니다.
**교훈**: 채팅만으로도 **코드 패키지 형태**로 받으면 대규모 배치가 됩니다. 반복 요소는 인스턴싱, 생성은 seed 고정, 검증은 테스트로.

#### E7. Epic 커뮤니티: Fab 환경 팩 + Claude Code + UE 5.8 내장 MCP로 가을 숲 레벨 (2026 · 2차 요약)

**어떻게**: Claude Code를 UE 5.8 내장 MCP에 연결 → Fab 환경 팩 임포트 → 에이전트가 Third Person 템플릿을 플레이 가능한 가을 숲 레벨로 바꿈(배치·구성). 포럼 토론 스레드와 스페인어 입문 튜토리얼도 있습니다.
**교훈**: **사람이 만든 고품질 에셋 + AI 배치**가 AAA급 시각 품질을 가장 확실하게 얻는 방법입니다. 에이전트의 강점(배치, 반복, 블루프린트)과 약점(메시·텍스처 품질)을 분리합니다. 본문은 열람하지 못했습니다.

#### E4·E3. 실측 데이터 대 비공개 대형 데모

- **E4 Martin Puli**(2026-07-21): 처음에 자기 집을 만들었더니 "찌그러지고 회색인 플라스틱 모형 같은 쓰레기"가 나왔습니다. 그래서 여러 출처에서 건물 발자국·높이·좌표를 긁어 오는 에이전트를 만들고 Blender 도구로 짓게 하자 뉴욕이 제대로 나왔습니다. .blend가 '살아 있어서' 문장 몇 개로 타워를 추가하고 도로를 옮기고 부에노스아이레스와 뉴욕을 합칠 수 있습니다. 텍스처와 재질은 여전히 약점이라며 조언을 구했습니다. 공개하겠다던 저장소는 찾지 못했습니다. 교훈: **실제 장소와 치수는 모델의 기억이 아니라 데이터에서.**
- **E3 Matt Shumer**(2026-09-03): 일주일 동안 구역·거리 단위로 평가 체크리스트를 유지하며 다듬었다고 요약됩니다(Tripo 브리프). 출시 초기 가장 반응이 큰 3D 사례지만 에셋 출처와 정확도는 공개되지 않았습니다. E1은 같은 뉴욕에서 "가로 수준 파사드 데이터가 없다"는 한계를 기록했으니 비교해서 보세요.

#### E10. claude-3d-harness: 옥상 방 씬 3시간 미만 (2026 · 1차 공개)

잡을 fast/standard/cinematic 프로필(fast 1280×720/64spp, standard 1920×1080/256spp, cinematic 512spp)로 나누고, modeling/product/photography/animation/environment/cinematic 중 워크플로를 고르고, 5개 라이브러리의 SKILL 58개를 버전 고정·체크섬으로 관리하고, 단계마다 체크포인트 렌더를 찍습니다. README에 '비 오는 밤 일본 도시 옥상의 작은 방'(메시 오브젝트 449)을 그레이 블록아웃에서 최종 프레임까지 3시간 안에 만든 사례가 있습니다. 서버는 newo-ether(기본)와 ahujasid(대체)이고, 공식 Blender Lab 서버 지원은 [이슈 #7](https://github.com/MAX-786/claude-3d-harness/issues/7)에서 논의 중입니다. 공식 서버에는 구조화된 노드 도구와 Poly Haven 연동이 없어서 기존 스킬이 얼마나 동작할지가 미해결입니다.

#### 그 밖의 환경·레벨 사례

| 사례 | 무엇을·어떻게 | 한계·교훈 |
|---|---|---|
| E6 flopperam | LLM이 액터를 하나씩 찍는 대신 `create_town`, `construct_house`, `construct_mansion`, `create_maze` 같은 파라메트릭 건축 함수를 호출 | **규모는 고수준 도구 설계에서 나온다**. 결과는 프리미티브 위주(추정). 로컬판은 UE 5.5~5.7만 지원, 호스팅판은 별개 서버·API 키 필요 |
| E8 Dan Elton | "download 2,000 historical photographs … create a 3D reconstruction in Blender" | 작성자 스스로 "화면이 거칠고 건물에 오류, 한 건물은 기존 모델을 가져다 썼는지도 모르겠다". 대규모 역사 복원의 한계를 보여 주는 정직한 사례 |
| E9 Givros Cozy Lake | 자체 Blender 스킬과 프롬프트 라이브러리(유료 판매)로 월드를 확장 | 2차 요약 |
| E11 Codex-and-Blender | YAML/JSON 설정 → 결정적 bpy → headless CLI → Astra 멀티뷰 리뷰 → (선택) MCP 실시간 점검. `acceptance.yaml` 불변, MCP 수정은 반드시 원본에 반영, `reproducibility_check.py`로 클린 빌드 2회 비교 | **"Git 설정 + Blender Python이 원본, MCP는 점검 레이어"**. MIT, 정량 수치 없음 |
| E12 어린왕자 행성 | 생성 스크립트를 파일로 보관해 클라이언트로 실행, GLB를 파싱하는 테스트로 본 구조·스키닝·애니·발 위치를 구면 카메라 252곳에서 검증 | 플러그인 타이머 의존 때문에 headless가 아닌 GUI 모드 필요. 모델링 마찰은 줄었지만 **검증 인프라가 상당히 필요** |
| E13 다나와 DPG | 프롬프트 약 5개로 30분 만에 모델링·연출, 내보내기 20분 더. 이미지를 Codex에 올려 Blender 파일로 변환하는 방식도 소개 | '50분 만에 유튜브 영상' 헤드라인. 품질 검증 없음(검색 요약) |
| E14 Opus 5.5 출시일 스레드 | 커뮤니티 데모 큐레이션(클레이메이션, 3D 게임, 작동하는 광학 실험실, UE 도시 전체) | 개별 제작자·세부는 미확인 |
| E15 State of Unreal 2026 | UE 5.8 Experimental MCP 워크스루 영상(프롭 배치, 절차적 도시, 조명 아트 디렉션으로 보도) | UE6에 Claude·Gemini를 MCP로 통합, Early Access 2027년 말 목표라는 보도는 1차 출처 미확인 |
| E16 BlenderMCP 원조 데모 | Claude Desktop에서 애드온 소켓 서버에 `{type, params}` JSON 명령. 'Create a low poly scene in a dungeon, with a dragon guarding a pot of gold', 'Create a beach vibe using HDRIs, textures, and models like rocks and vegetation'(Poly Haven 자동 검색·임포트) | README가 밝힌 한계: 복잡한 작업은 작은 단계로, Poly Haven 다운로드 중 Blender가 멈춤, 코드 실행 전 저장 필수. 2026-09 멀티뷰 피드백 PR(#353, 미병합)과 검사 도구 18개 PR(#359, 소유자가 닫음)이 올라온 것은 '보는 능력' 부족의 방증 |

### 2.4 게임

#### G1. 프롬프트 1개, 24분, $9.90: Fable 5.1이 만든 3D 게임 (2026-09-01 · 검증됨)

**어떻게**: 프롬프트의 핵심 요구는 "모든 에셋을 직접 보고 나서 수락하라"였습니다. 모델은 Blender 5.2 headless bpy로 이름 붙은 메시 12개를 담은 `assets.glb`를, FLUX.2 Q8로 스카이와 텍스처를, LTX-2.5 i2v로 홀로 빌보드 영상을, ACE-Step으로 음악을 만들었습니다. 음악 7곡을 생성해 스펙트로그램에서 무음 구간을 찾아 6곡을 버리고, `make_loop.py`로 27마디·112BPM·1.2초 크로스페이드 루프를 만들었습니다. Blender 출력을 보려고 **자체 뷰어와 스크린샷 스크립트**를 만들었고, Playwright로 웨이브1 → 상점 → 업그레이드 → 웨이브2를 플레이한 뒤 bloom·조명·발광 강도를 튜닝했습니다. 로컬 RTX 5090.
**결과**: HTML 파일 하나(4.4MB). 75턴, 출력 95,832 토큰, 재시도 없이 1라운드 통과. 같은 프롬프트를 GLM-5.3에 준 [비교 저장소](https://github.com/Nipale-ai/glm-5-3-one-prompt-game)는 27분에 다른 게임이 나왔습니다.
**교훈**: **스스로 검증하는 에이전트**의 모범 사례입니다. "보고 나서 수락하라"는 요구 하나가 품질 루프를 만듭니다.

#### G2. Robo Open: 실패 22건을 공개한 Codex/Astra + Blender + Meshy + Unity 테니스 게임 (2026-09-05~ · 검증됨, 정정 반영)

**어떻게**([DEVELOPMENT-JOURNEY](https://raw.githubusercontent.com/az9713/gpt-6-astra-tennis-game/main/DEVELOPMENT-JOURNEY.md))
1. 사람은 의도·범위를 정하고 승인만 했습니다(모델링·리깅·코딩 개입 없음).
2. **4단계 프리플라이트**를 무료 픽스처로 먼저 통과: Unity 프로젝트, 에디터 자동화(Unity Pipeline 0.6.0-exp.1), Blender 애니메이션 임포트, Windows와 WebGL 빌드.
3. 그다음 Meshy로 로봇 1체를 생성했습니다(30크레딧). 에이전트가 제안한 400크레딧 상한을 사람이 승인했고, 실패한 요청은 원장을 대조한 뒤에만 재시도했습니다.
4. Meshy 자동 리깅이 HTTP 422로 실패하자 재제출 대신 Blender 스크립트로 16본 리그를 직접 짰습니다. GLB를 1.8m로 정규화하고 발을 지면에 맞췄습니다.

**실패와 수정(22건 중 일부)**
- FBX가 100배(2m 로봇이 200m)로 들어옴 → `apply_scale_options='FBX_SCALE_UNITS'`
- 백그라운드 테스트에서 스킨 애니메이션이 정지 → `AnimationCullingType.AlwaysAnimate`, `SkinnedMeshRenderer.updateWhenOffscreen`
- 자동화 스크린샷이 URP 조명을 틀리게 찍음(Camera.Render 경로 문제) → `RenderPipeline.SubmitRenderRequest`. **"나쁜 스크린샷은 씬이 아니라 캡처 경로에 대한 증거"**
- WebGL 개발 빌드 링크 실패(정상 빌드 성공까지 53분), C# 타입 오류

**결과**: 프로토타입 52분, 세션 전체 4시간23분. 토이 로봇 2체(16본 리그, 클립 6개), 코럴 코트, CPU 상대, 서브·발리·파워·로브, 점수, 메뉴가 있는 Windows 실행 파일. 품질은 '프로토타입 수준 애니메이션과 접촉 판정'입니다. v0.3에서 사람 플레이테스트로 리턴 불가 문제를 찾아 고쳤고, 현재 v0.5.1입니다. 원작은 Chong-U의 Fable 5.1 영상(G7)이지만 원작 자산 없이 새로 재구성했습니다.
**교훈**: **유료 생성 API는 싼 픽스처로 파이프라인을 끝까지 검증한 뒤에** 씁니다. 크레딧 상한과 원장을 둡니다. 스크린샷 장치 자체도 검증 대상입니다.

#### G3. How to Suck: AI가 만든 Unity 협동 게임 (2026-09-14 · 검증됨, 정정 반영)

'AI가 혼자서 완성 게임을 만들 수 있는가' 실험입니다. 작성자는 코드, 3D(Blender), 애니메이션, 환경, UI, 멀티플레이(Netcode for GameObjects, EOS/Steam)를 모두 AI가 만들었다고 밝혔습니다. 효과음은 ElevenLabs, 오디오 자동 평가는 Qwen2-Audio·CLAP으로 했습니다. 결과는 1~4인 1인칭 청소기 협동 게임(장소 3곳, 계약 6개, 청소기 4단계, 17개 언어)이고 Windows 다운로드를 제공합니다.
**시간·비용**: 첫 자율 반복에 39시간. **Pro x20 구독의 주간 한도 2회분은 첫 반복이 아니라 이후 반복까지 포함한 전체 개발 소모량**입니다(README: "The two weekly limits cover the project's development, including subsequent iterations").
**한계**: 호스트 마이그레이션은 구현하지 않았습니다. 비주얼은 스타일라이즈드 인디 수준으로 판단됩니다(미검증).
**교훈**: 실제 배포까지 간 드문 사례입니다. 장기 작업은 시간보다 **구독 한도**가 병목이 됩니다.

#### G5. Roblox 게임 + Blender MCP로 3D 공간 검증 (2026-07-03 · 1차 공개)

Claude Code가 커스텀 스킬과 탐색·설계·리뷰 에이전트로 존 5개, 미니게임 5개, Luau 모듈 100개 이상의 Roblox 게임을 며칠 만에 만들었습니다. 코드 검증(format, lint, type-check, unit test, build, playtest)에 더해, Blender MCP로 모델을 참조하고 공간 관계를 측정하고 지오메트리를 재구성하고 머티리얼을 베이크해 export했으며, 여러 각도 스크린샷으로 공간 정합성을 확인했습니다. 핵심 교훈은 원문 그대로 "3D space can't be verified from code alone. A position that looks right numerically can float, clip, or face the wrong way." 비용·시간은 공개되지 않았습니다.

#### G11. Paper Ember Duel: Rodin MCP + Blender + Godot 보스전 (2026-09-10~13 · 1차 공개)

GPT-6/Codex로 기획과 코드를 쓰고, Hyper3D Rodin MCP에서 'Gen-2.5 Medium / Raw' 백만 면급 원본을 생성했습니다(웹의 Extreme-High는 의도적으로 피함). BANG으로 캐릭터를 메시 부품 8개로 나눴습니다(자동 스키닝은 아님). 그다음 Blender에서 메시 연결, 폴리곤 감소, 스킨 웨이트, 무기 그립 위치를 손으로 보정해 Godot 4.7.2(Compatibility 렌더러)로 가져갔습니다. 플레이 가능한 Mac 빌드가 나왔습니다. README는 "프로젝트 코드와 아트는 통일된 오픈소스 라이선스가 없고 상업적 재사용은 불허"라고 명시합니다. 교훈: **생성 원본은 고폴리라서 엔진 투입 전 감면이 필수**이고, 캐릭터 분해·웨이트는 여전히 손이 갑니다.

#### G12. Godot AI MCP로 만든 사이버펑크 HUD의 마찰 로그 (2026-04-15 · 검증됨, 부분)

`.tscn`·`.tres`를 직접 편집하지 않고 MCP 도구만으로 체력·실드 바, 쿨다운 링, 탄약, 로그 피드, 설정 패널이 있는 일시정지 메뉴를 만들었습니다. 호출은 `node_*` 약 15회, `ui_build_layout` 6회, `theme_*` 12회, `animation_*` 12회, `input_map_*` 9회, `batch_execute` 1회(`node_create` 7개를 한 번에) 등입니다. 빈틈: 씬 인스턴싱 도구 없음(런타임 로더 스크립트로 우회), 게임 뷰 스크린샷(`editor_screenshot source='game'`) 실패로 CanvasLayer HUD가 캡처되지 않음, 상하좌우 테두리를 따로 지정할 수 없음, `theme_create`가 폴더를 자동으로 만들지 않음. '약 2시간'은 로그와 README에서 확인되지 않았습니다. UI 사례지만, **MCP 도구가 모든 것을 커버하지 못하면 스크립트로 우회**해야 한다는 교훈은 3D에도 그대로 적용됩니다.

#### 그 밖의 게임 사례

| 사례 | 무엇을·어떻게 | 한계·교훈 |
|---|---|---|
| G4 Givros 카트 레이서 | 프롬프트: Blender에서 메시·UV·베이크 텍스처 마감 → 최적화된 MeshPart로 임포트 → 게임 안에서 스케일·피벗·재질·콜리전 검증 → 실제 게임플레이 스크린샷을 보며 반복, **플레이스홀더 금지** | 2차 요약. Roblox 공식 [studio-rust-mcp-server](https://github.com/Roblox/studio-rust-mcp-server)는 2026-04-03 아카이브, 지금은 Studio 내장 MCP 권장 |
| G6·G7 Chong-U | 2025-03 Cursor + Claude로 블루프린트(BP) 클래스 생성·컴포넌트·노드 연결·컴파일해 Flappy Bird 클론. 2026-09 Fable 5.1 Unity + Blender 테니스 영상('FABLE 5.1 Is Here And It's PERFECT For Vibe Coding Games') | Unreal MCP 붐의 시작. 그래픽보다 게임플레이 프로토타이핑 |
| G8 Cagri Kacmaz | 동일한 PROMPT.md, 수동 QA·인터랙션 테스트·녹화로 비교 | 작성자가 "과학적 벤치마크 아님"이라고 명시 |
| G9·G10 Astra 게임 붐 | Void Explorer(성계 2,048, 행성 1만+), 약 45분 만에 만든 게임 | 45분 게임은 에셋을 모델링하지 않고 **이미지 생성으로 그래픽을 해결**. AAA가 목표라면 이 트릭은 프리비즈에서만 |
| G13 Andy.G | 모든 Lua 코드 작성, 오브젝트 생성, 속성 변경을 Claude Code가 MCP로 | 결과 품질 미확인 |
| G14 @secret_canada_ | Unity 설치 → Claude Code → mcp-unity 연결 → 무료 에셋으로 약 30분 워밍업 | "캐주얼 게임이라면 며칠 안에" 평가 |
| G15 AiBattle | 같은 Godot 게임을 Astra Max와 Medium으로 | Max 53분(Pro x5 주간 한도 4%), Medium 25분(1%). effort가 비용을 4배 바꿈 |
| G16 RealFedeURU | 기획·코드 Fable 5.1, 3D·Blender Astra, 일부 에셋 Meshy, 통합 Godot | 모델을 **역할별로 나눠 쓰는** 예 |
| G17 Stefan 11일 게임 | Astra가 어색한 공격 애니메이션을 끝내 못 만들어, 직접 휘두르는 모습을 촬영해 영상→모캡으로 붙임 | **애니메이션은 사람 데이터로 보완**하는 하이브리드가 기본 |
| G18 HOVERBALL | UE 5.7용 자체 TS/C++ MCP(에디터 액션 약 285, 스킬 20+)로 멀티플레이 게임 | 공식 MCP 이전 세대의 하네스 사례 |
| G19 Brendan Jowett | 60~120분 동안 AI가 Blender에서 모델을 만들고 UE로 게임 구성, "Opus delivers results a million times better than Astra" | **신뢰도 낮음**: 원본 영상 미확인, 같은 영상을 재요약한 기사(ixbt, se7en.ws)만 있음 |
| G20 게임뷰 | 에이전트가 MCP로 에디터를 조작하고 화면을 읽음, 이해하기 어려운 머티리얼 수식에 어노테이션을 달아 질문, UMG·나이아가라에 활용([후편](https://www.gamevu.co.kr/news/articleView.html?idxno=60830)) | 한국어 개발기 |
| G21 GameDev Academy | Codex에 Blender MCP 등록 → Astra가 Python 생성·실행 → 렌더를 다시 보여 주며 반복 → Godot 프로젝트 생성·테스트 | **신뢰도 낮음**(모델명·MCP 종류 미검증). "샷이 어떤 느낌이어야 하는지는 모른다" → 방향과 최종 QA는 사람 |

> **게임 에셋 제약은 숫자로 주세요.** Jonathan Plumb의 프롬프트(Tripo 카탈로그 경유): "Keep the main render mesh under 15,000 triangles. Name objects clearly, set the forward direction for Unity, create simple collision geometry, apply transforms, save the .blend, and export a game-ready FBX. Show viewport screenshots for approval before export." Andrew Walko는 "Everything you need is in Assets/ithappy/Cartoon_City_Free"처럼 **이 폴더의 에셋만으로 조립하라**고 지시했습니다.

### 2.5 조형·캐릭터

#### C2. Tripo 캐릭터 UV 재구성과 4K 재베이크 (2026-09-13 · Astra + Blender MCP · 2차 요약, 프롬프트 공개)

긴 프롬프트로 **사람 아티스트의 순서**를 강제했습니다.
1. 사본 저장 → 원본 UV·이미지 유지 → 새 UV 맵 `UV_Final` 생성
2. 모든 방향에서 관찰해 봉제선 설계 → 부위별 언랩
3. 체커와 Stretch로 왜곡 확인 → Pin/Relax
4. 결 방향을 V축에 정렬, 텍셀 밀도 맞춤, 4K 기준 마진 16px, 아일랜드 간격 32px 이상
5. 구 UV에서 새 UV로 베이크: base color는 Diffuse Color나 Emit만(조명·AO를 굽지 않음), 노멀은 새 UV 기준으로 재베이크
6. 전후 비교

작성자는 한 번의 프롬프트로 끝났다고 보고했지만 프로젝트 파일은 확인하지 못했습니다. UV·베이크를 AI에게 맡길 때 쓸 수 있는 가장 구체적인 공개 프롬프트입니다. 교훈: Smart UV Project로 끝내면 페인팅하기 어려운 조각난 UV가 나옵니다. **순서를 프롬프트에 박으세요.**

#### C3. Tripo 캐릭터 의상 텍스처를 한 부위씩 재마감 (2026-09-09 · 1차 공개)

순서는 읽기 → 백업 → 부위·UV 분석 → 이미지 생성(부위별 실제 프롬프트 7개 공개) → 위치 보정·분할 적용 → 거칠기·노멀 강도 조정 → 전후 비교 → 확인본 저장입니다. 치마, 소매, 리본, 몸통, 다리·신발 재질을 새 무늬로 바꾸면서 얼굴·눈·머리·형태는 보존했습니다. **한 부위 결과를 확인한 뒤에 옆 부위로 넓힙니다.** 다른 서비스 모델이나 텍스처 없는 모델에서는 검증하지 않았습니다(일본어, Blender 5.1.2).

#### C5. 모델링 플레이그라운드: 측면 두께와 자동 테스트 (2026-09 · 1차 공개)

GLB와 .blend를 생성하고, 테스트로 "눈이 얼굴 안에 묻히지 않았는지", "보행 36프레임 동안 어떤 정점도 지면 아래로 파고들지 않는지"를 검사했습니다. 정면 참조로 만든 초안은 **옆에서 보면 얇아서**, 머리 앞뒤 폭을 좌우 폭과 비슷하게 늘리고 몸통 깊이를 1.45배로 고쳤습니다. 동작은 딱딱했고 얼굴·비율을 여러 번 조정해야 했습니다. GLB 표준에는 Blender IK 제약이 저장되지 않습니다. 교훈: 정면·측면·3/4·후면 렌더를 반복마다 요구하세요. [`review_views.py`](../03_playbooks/scripts/README.md)가 위·정면·측면·3/4 원근 4장을 오브젝트별 색으로 렌더합니다.

#### C1. 같은 일러스트: Astra 직접 모델링 대 Meshy 7 (2026-09-09 · 2차 요약)

Astra(High)는 Blender에서 직접 모델링해 전신 형태와 의상을 재현했지만, 얼굴과 옷 디테일은 이미지→3D인 Meshy 7이 앞섰습니다(8분 대 3분). **캐릭터·유기체는 생성형이 유리하고 에이전트는 후처리를 맡는 분업**을 뒷받침합니다. 성공한 캐릭터 사례 다수(chimerast VRM, Nano 표정, C7 insaneUEFN, Stefan의 말)가 Tripo·Meshy 베이스에 에이전트 후처리를 붙인 하이브리드였습니다. Hyper3D Rodin MCP로 용이나 우주선을 만든 뒤 부품을 분리해 조립한 사례도 있습니다.

#### 레퍼런스 뷰 규칙 (C9, C10)

AI가 만든 레퍼런스 시트는 뷰끼리 모순이 있어서, 뷰마다 역할과 충돌 해소 규칙을 줘야 합니다. Sarang Borude 드래곤 프롬프트(Tripo 카탈로그 경유):

```text
Use the side view for overall proportions, the front view for width and stance,
the top and back views for wings and tail... Use geometry for anything affecting
the silhouette... normal maps, bump or restrained displacement only for micro-detail.
```

해부학적 블록아웃을 확인한 뒤에 2·3차 디테일을 올립니다. icesixgod 스킬은 8방향 + 탑뷰, 총 9뷰를 생성하되 원화를 1순위 기준으로 삼습니다.

#### 그 밖의 조형·캐릭터 사례

| 사례 | 무엇을·어떻게 | 한계·교훈 |
|---|---|---|
| C4 Yokohara | 생성형 3D 없이, 사람에게 가르치듯 단계별 지시로 스컬프팅(Astra Ultra effort) | "예상보다 깨끗하게 나왔다" |
| C6 Stefan + Tripo P2.0 | Tripo로 부품 메시 생성 → Astra가 Blender MCP로 배치·조립·리깅·애니 | 큐레이션 목록에는 같은 작성자의 'Scorpid Creature Animation'(Tripo P2.0 모델에 애니 5개, Unity 통합)이 다른 게시물 ID로 올라 있어 귀속이 불확실 |
| C8 Alix Ollivier 박쥐 | 토큰이 소진될 때까지 자율 실행한 포토리얼 박쥐 | '모든 모델이 유기체에 약하다'는 단정의 반례(자기 보고). 약점 서술에 조건을 붙여야 함 |
| C11 rodin-via-blender | 정면·후면·좌·우 4장 → Rodin(bbox, 캐릭터 tier) → Blender MCP에서 Voxel/QuadriFlow/Subsurf로 표면 정리 → Shrinkwrap·Boolean 데칼 → 수밀성·스케일·셸 두께·언더컷 검사 → 제작사 전달 | **신뢰도 낮음**(1커밋, 결과 증빙 없음). 실물 조형에도 같은 리메시·검증 원칙이 적용된다는 워크플로 아이디어로만 참고 |
| C12 sketch-to-3d-codex | 스케치 검사 → Design Lock → 마스터 후보 2~4개 중 사용자 선택 → 개별 뷰 승인 → Rodin → Blender. 정체성이 중요한 캐릭터는 머리·몸을 따로 검수 | **신뢰도 낮음**: README가 "Hyper3D was configured but not exposed to this session, so no live generation … was tested"라고 밝힘. 설계만 된 워크플로 |
| C13 한국어 유튜브 | Claude + Blender MCP로 2D 로봇 이미지를 3D로 옮기고 랜딩 페이지에 적용 | 품질 미확인 |
| C14 mixamo-llm-mocap | 고정 카메라 영상 → GVHMR로 SMPL-X 추출 → Mixamo 리그 리타겟 → headless Blender 키 입력 → 2×2 리뷰 영상 → 충실도 평가 | 에이전트가 모캡 루프 전체를 돌릴 수 있음(G17과 같은 해법) |

### 2.6 영상·렌더·프리비즈

#### V1. Vizuara: Fable 5.1이 Blender 키트와 샷 빌더를 짜서 교육 영상 5편 (2026-09 · 검증됨)

**어떻게**
1. 내레이션 타이밍을 뼈대로 샷을 나눕니다.
2. 샷마다 EEVEE 720p 1프레임 **컨택트시트**를 만듭니다(M1 8GB에서 샷당 2~16초).
3. 사람이 **6항목 바**로 결함 목록을 씁니다.
4. `/vl-fix-shots`가 먼저 측정하고, 고치고, 증거 프레임을 렌더합니다.
5. 통과하면 Modal에서 Cycles 1080p, 24fps, DOF, 모션 블러, 384 samples로 최종 렌더합니다(A10G에서 프레임당 12~44초).

6항목 바(클라이언트의 "very, very beautiful"을 쪼갠 것): ① 히어로 에셋에 3단계 스케일 디테일(맨 프리미티브 금지) ② 파티클·대기·아웃포커스 전경 ③ 표면을 뚫고 들어가는 매치컷 ④ 모든 샷에 카메라와 피사체 움직임 ⑤ 문장마다 시각적 증거 ⑥ 섹션별 팔레트와 조명 테마. 수정 지시 예: "s30: washed grey, tissue must be warm and matte; s06: fist is a cluster of balls".

**결과**: 심장 챕터(8분3초, 10,964프레임)를 청크 709개로 나눠 A10G 약 50대에서 84분에 렌더, 실패 0, 합성 5분 추가. 수정은 보통 2라운드였고, 모델 자체 리뷰보다 사람 눈이 결정적이었습니다.
**함정**: headless에서 GPU 컴포지터가 segfault → CPU로 전환, 디노이저는 OptiX 대신 OIDN(Intel Open Image Denoise), 카메라 배치 전에 초점 거리를 재서 청크가 새까맣게 나옴, shape key 레이캐스트가 basis가 아닌 활성 키 기준으로 계산됨.
**한계**: 교육 영상용(비실시간)이고 Modal 비용은 밝히지 않았습니다. **LICENSE 파일이 없어 라이선스 미지정**입니다.
**교훈**: "작은 모델도 뭔가 만들긴 하지만 이 바를 넘으려면 훨씬 많은 라운드가 필요하다." **'예쁘다'를 체크리스트로 쪼개면** 수정이 두 번이면 끝납니다.

#### V2. Simon Willison: 프롬프트 3번과 Blender 스킬 (2026-09-04~05 · Astra Medium · 검증됨)

MCP 없이 로컬 Blender를 headless로 불렀습니다.
1. "Use the already install /Applications/Blender to render a scene of a pelican riding a bicycle" → 2분39초
2. "OK add a background and a lot of flair" → 3분51초
3. "OK make it a whole lot better" → 5분59초

모델이 렌더 이미지를 보고 겹친 지면 같은 문제를 스스로 고쳤습니다. 첫 실행은 샌드박스 제한으로 Blender가 크래시해 권한을 받아 다시 돌렸습니다([transcript](https://github.com/simonw/gpt-6-astra-blender-pelican-bicycle/blob/main/codex-transcript.md)). 마지막에 "Create a quick skill that describes how to use the currently installed Blender based on what you learned"로 스킬을 만들어 이후 작업에 재사용했습니다. 이후 Images 2.5 참조 이미지와 Astra high로 파베르제풍 달걀도 만들었습니다(2026-09-09). 결과는 토이풍 일러스트 품질이고, 작성자 평은 "Modern frontier models have got really good at using Blender."입니다. 교훈: **bpy 스크립트를 원본으로 남기고, 배운 것을 스킬로 굳히세요.**

#### V3. [AI 영상] Blender 프리비즈 → AI 영상 한국어 스킬 (2026-09-08 · 1차 공개)

인테이크 → 샷 설계 → 블로킹 브리프 → Blender 실행 → 뷰포트 렌더 → 레퍼런스 정리 → 4블록 생성 프롬프트 → 리비전 순서입니다. Higgsfield Bridge 커넥터와 Blender 플러그인(`bl_*` MCP 도구, `bl_get_skill` 모듈 blender-greybox, blender-lighting-camera 등)을 쓰고, MCP가 연결되지 않으면 핸드오프 모드로 바뀝니다. 13개 규칙의 핵심은 "블로킹 영상은 카메라 궤적·컷·타이밍·동선을, 텍스트 프롬프트는 재질·조명·그레이딩·의상을 맡고, **둘이 충돌하면 블로킹이 이긴다**"를 명시하는 것입니다. 블로킹 마스터는 스타일만 바꿔(실사, 2D 애니, 스톱모션) 재사용할 수 있습니다.
**주의**: 최종 화면은 3D 렌더가 아니라 Seedance 2.5 같은 영상 모델 출력입니다. 워크플로 원출처는 Higgsfield 블로그의 @adilinthewild 글(2026-08-28)이고, 이 저장소는 그 방법론을 한국어 Claude Code 스킬로 **재구성**한 것입니다. LICENSE 파일은 없고 README에 '문서 텍스트는 MIT'라고만 적혀 있습니다. Blender 5.0 이상이 필요합니다.

#### SNS '포토리얼' 결과를 볼 때 AI 영상 합성물을 가려내는 법

PixVerse, Higgsfield, AI追光实验室 사례처럼 Blender에서 카메라와 동선만 고정하고 최종 화면은 Seedance 2.5 같은 영상 모델이 만드는 방식이 늘었습니다. 시네마틱이 목표라면 좋은 선택지지만 **실시간 3D나 게임 에셋에는 쓸 수 없습니다.**

| 확인할 것 | 3D 렌더일 가능성이 높음 | AI 영상일 가능성이 높음 |
|---|---|---|
| 공개 파일 | .blend, GLB, 씬 스크립트 공개 | 영상만 공개 |
| 도구 언급 | Cycles, EEVEE, Lumen, 렌더 샘플 수 | Seedance, video-to-video, v2v, Higgsfield, PixVerse |
| 뷰포트·와이어프레임 | 빌드 타임랩스, 와이어프레임, 뷰포트 캡처가 있음 | 그레이박스 영상과 완성 영상만 있음 |
| 프레임 간 일관성 | 형태·텍스처가 카메라 이동에도 고정 | 디테일이 프레임마다 미세하게 바뀌거나 녹아내림 |
| 편집 가능성 | "가구를 옮겨 다시 렌더" 같은 후속 편집 시연 | 스타일만 바꾼 재생성 |

#### 그 밖의 영상·렌더 사례

| 사례 | 무엇을·어떻게 | 한계·교훈 |
|---|---|---|
| V4 Stefan 원프롬프트 샷 | 한 프롬프트로 Blender만 써서 모든 요소를 절차적으로 만들고 10초 샷을 렌더, 빌드 과정 기록. 이후 VFX·캐릭터 애니·풀 씬 라운드를 같은 조건으로 | 수치는 5절. "Opus가 훨씬 많은 요소를 동시에 다룬다, Astra도 좋은 라이벌", 모든 라운드를 Opus가 이긴 것은 아님([후속 X](https://x.com/Stefan_3D_AI/status/2103113590446440763)) |
| V5 tonysuri 로마 전장 | "save a viewport screenshot into a numbered timelapse/ folder after every meaningful addition... assemble those frames into a timelapse video at 2 fps". 카메라를 원본 이미지와 정확히 맞추고 오브젝트마다 GLB로 export | **제작 과정을 증거로 남기게 하면** 어디서 망가졌는지 추적 가능 |
| V6 Stork.AI | Astra의 Blender 애니메이션 사례 정리 | 아크비즈·영화 프리프로덕션에 "후처리가 적게 필요한 에셋"을 기여할 수 있다는 평(2차) |
| V7 AI타임스 | 같은 프롬프트로 여러 모델의 3D 애니 결과 비교 | 카메라 앵글·노을 안개·텍스트 레이아웃 연출은 Opus 5.5, 비용·속도는 GPT-5.6, Fable 5.1은 최종 연출 정교함이 떨어짐(검색 요약) |
| E13 Backrooms 영상 | Blender로 만든 3D 영상(다나와 정리) | 3D 렌더 영상, 품질 검증 없음 |
| P3 목탄 드로잉 씬 | Opus 5.5 + Higgsfield로 목탄 질감을 유지한 3D 씬 | 벤더 쇼케이스 |

### 2.7 텍스처·재질·에셋 파이프라인

#### T1. Poly Haven 텍스처가 '평평하고 스케일이 틀렸던' 문제와 수정 (2026-09-14 보고, 09-21 병합 · 검증됨)

Poly Haven 운영자 Greg Zaal이 [이슈 #361](https://github.com/ahujasid/blender-mcp/issues/361)에서 버그 6개를 보고했습니다.
- 맵 이름 매칭이 'normal'을 찾는데 API는 'nor_gl'/'nor_dx'라서, normal과 displacement가 다운로드만 되고 연결되지 않음
- 모든 맵을 받아 1k 텍스처 하나에 7.4MB(필요량 1.9MB)
- 검색 결과를 관련도가 아니라 slug 순으로 20개에서 자름
- HDRI를 패킹하지 않음
- Mapping 노드 TEXTURE 모드 때문에 타일링이 역전(2m 텍스처가 4m 면에서 1.993회가 아니라 0.509회 반복)

[PR #367](https://github.com/ahujasid/blender-mcp/pull/367)에서 Poly Haven 자체 머티리얼 구조를 참조하는 단일 테이블로 바꾸고, Mapping을 POINT로 바꾸고, 필요한 맵만 받게 하고, .blend 원본 임포트와 테스트 248개를 추가했습니다(Blender 5.2.1 E2E). 다운로드는 49% 줄었습니다(1k 텍스처 860개 기준 4,150MB → 2,100MB). 연결 누락은 '다운로드 시 머티리얼 생성' 경로의 버그였고 `set_texture` 경로에는 별도의 이름 파싱 버그가 있었으므로, "모든 경로에서 항상 평평"은 과장입니다.
**교훈**: 도구가 '성공'을 반환해도 **노드 연결을 렌더로 확인**하세요. 최신 mcp-for-blender(2.1.0, 2026-09-25)를 쓰세요.

#### T3. blender-kiln: 15개 에셋 갤러리와 사라지는 맵 (2026-08 · 검증됨, 정정 반영)

8단계 파이프라인(CONFIG → BRIEF → SOURCE → IMPORT → CLEANUP → TEXTURING → OPTIMIZE → EXPORT)과 Iron Rules 31개(core 26 + batch 5)를 가진 Claude Code 스킬입니다. 대화형 MCP 경로와 headless 경로의 결과가 **바이트 단위로 같았습니다**(111.9kB GLB, 2,202 tris, 재질 3개. Blender 5.0과 5.2 LTS에서 측정, 하한 4.4).
**정정**: README는 15개 에셋 갤러리(21,879 tris, 1,456.2kB → 132.7kB, 91% 감소)에 대해 "They were not produced by running the skill ... this is blender --background --python, the scripted-modeling path only"라고 명시합니다. 즉 이 수치는 Claude/MCP·Poly Haven·Hunyuan3D로 만든 결과가 아닙니다.
**측정 교훈**: Poly Haven american_walnut_veneer의 맵 7개 중 baseColor, metallicRoughness, normal만 GLB에 남고 AO와 Displacement는 빠졌습니다(PR #367 이전 동작 기준). 절차 노드·SSS·displacement는 base color나 normal로 **베이크**해야 하고, glTF 내보내기 전에 '다운로드한 맵과 채워진 슬롯'을 비교하는 감사가 필요합니다. `references/uv-materials.md`의 `angle_limit=66.0 # degrees`는 bpy의 라디안 규칙과 어긋나니 그대로 쓰지 마세요.

#### T5. asset-studio: 로컬 RTX 5090 텍스트 → 게임용 에셋 (2026-09 · 검증됨)

1. 프롬프트를 '단일 객체, 단색 배경, 3/4 view, soft-lit, 텍스트 없음'으로 다시 씁니다.
2. Qwen-Image-2512 Lightning 8(1328², 8 step)로 레퍼런스 이미지를 만듭니다.
3. Pixal3D/TRELLIS.2(balanced 1024 또는 quality 1536 cascade, 후보 2개)로 master 메시(최대 1M tri, 4096² PBR)를 만듭니다.
4. Blender에서 meshoptimizer로 decimate, UV 재전개, color/metal-rough/normal 베이크, LOD 50%/25%, convex hull 콜리전을 만듭니다.
5. Khronos validator로 검사합니다.

MCP 도구(generate, status, artifacts, retry, open_in_blender)로 Claude Code에서 호출합니다. crate는 954,901 → 7,998 tri로 11.1분, 펌프는 997,520 → 19,803 tri로 15.6분, 예산만 바꾼 재최적화는 약 80초. Godot 4.7.2 임포트를 테스트했습니다. 0BSD. **주의**: 기본 matting이 gated 비상업 라이선스인 BRIA RMBG-2.0이라 상업용이면 알파 PNG를 직접 넣으세요.

#### T6. image-to-3dlab: 로컬 백엔드 5종 비교 (2026-09 · 검증됨)

Pixal3D, Hunyuan3D-MLX 2종, TRELLIS.2, Stable Fast 3D를 같은 입력으로 돌렸습니다. Pixal3D는 "Best results… one pass, no repaint needed"로 색 채도 보존이 가장 좋았습니다. TRELLIS.2는 충실도가 가장 높지만 Mac(M5)에서 15~35분이 걸리고 플랫 아트에서 색 오류가 났습니다. Hunyuan MLX는 geometry가 가장 깨끗했지만, 저자가 **한국·EU·영국에서는 쓸 수 없게 막아 두었습니다**(라이선스 적용 지역 제외). Finish 단계는 voxel remesh → decimate(예: 90만 → 4만 면) → 선택적 Hunyuan 2.1 PBR 리페인트(약 6분) → JPEG 2048 재인코딩(32MB → 5MB 미만)이고, 결과물마다 `.provenance.json`을 붙여 라이선스를 추적합니다. RMBG-2.0은 라이선스 문제로 기본 비활성입니다. 저장소 코드는 Apache-2.0이지만 README가 "Qwen-Image 2.1 … Those weights are non-commercial"이라고 밝혀, **텍스트→이미지를 거친 결과물은 비상업**으로 분류됩니다.

#### T4. [한국 추정] Blender 노드 셰이더가 UE로 안 넘어가 텍스처 PBR로 전환 (2026-02 · 1차 공개)

Claude MCP(Blender 모델링) + Nano Banana MCP(PBR 텍스처) + Unreal 브리지 구성에서, Nano Banana로 "4096x4096 PBR stone wall texture" 같은 프롬프트로 BaseColor·Normal·Roughness·Metallic 4장을 만들어 UE Content/Textures에 저장했습니다. 이미지 모델이 데이터 맵까지 '그리는' 방식은 물리적 일관성을 검증하기 어렵기 때문에, **albedo만 생성하고 데이터 맵은 추정기나 베이크로 만드는 편**이 안전합니다(분석). 교훈: 엔진으로 넘길 재질은 처음부터 텍스처로 굽습니다.

#### 그 밖의 텍스처·파이프라인 사례

| 사례 | 무엇을·어떻게 | 한계·교훈 |
|---|---|---|
| T2 중복 노드 | PolyHaven 머티리얼 생성과 `set_texture`가 기존 노드를 지우지 않고 매번 추가 → Output·Principled가 여러 개 → 뷰포트는 맞는데 렌더는 회색 | `nodes.clear()`로 Output 1개·Principled 1개를 보장하는 헬퍼로 수정. **에이전트의 재질 코드는 멱등이어야 함** |
| T7 Scenario 보물상자 | recommend로 text-to-image 모델 선택 → 'single centered subject on a plain background' → image-to-3D recommend → `model_schema_get` → `model_run(wait=false)` → `jobs_wait` → `asset_display` → `asset_download` | 흔한 실수(스키마 안 보고 실행, 로컬 경로 전달, 모델 ID 하드코딩)도 정리. 벤더 문서 |
| T8 Meshy game-asset-pipeline | art_style 선택, preview(약 30초) → refine(약 2분) → Remesh 1K~300K tris(모바일 1K~5K, PC/콘솔 전경 5K~50K) → 최대 4K PBR → Unity는 Scale 0.01, UE5 정적 소품은 Nanite | 무료 플랜 출력물은 CC BY 4.0(Meshy 표기), 유료는 비공개 상업 라이선스 |
| T9 MaterialPilot | 392개 노드 디스크립터 조회 → 스냅샷 → 패치 dry-run → 그래프 정리 → 결정적 검증 → .ptex 저장 → 2048 내보내기 → SHA-256 산출물 검증 | 평면 이미지가 아닌 **계속 편집할 수 있는 재질**. 0.1.0 preview, Apache-2.0 |
| T10 NVIDIA Material Agent | USD 최적화 → 부위별 렌더 → 기술 문서에서 재질 정보 추출 → VLM 예측 → 이름 검증·수리 → 반복 인스턴스 조화 → 적용 → 비교 렌더 | 설계 원칙 "시각 증거가 권위, 기술 문서는 보조". 가구·소품 재질을 정확히 고르는 레퍼런스(Beta) |
| T11 PBRify_Remix | ambientCG CC0로만 학습한 모델로 DXT1 압축·디더링·헤일로 복원 + normal/roughness 추가 | '윤리적 AI 텍스처' 사례. RTX Remix Toolkit에는 공식 MCP 서버도 내장됨 |
| T12 Substance Designer MCP | `build_material_graph` 레시피 79개로 노드 37~44개, height/normal/roughness/AO/basecolor/metallic 출력 그래프 | 한 번에 도구 하나만 호출(병렬 시 멈춤), 도구 수 표기가 README 안에서 불일치 |
| T13 StableGen | v0.3.0(2026-03) TRELLIS.2 생성과 PBR 분해(albedo·roughness·metallic·normal·height·AO·emission), v0.3.1(2026-06-12) 폴더 배치·다색 프린트 | 오픈소스 로컬로 '형상 인식 AI 텍스처 → PBR → UV 베이크'가 가능. GPL-3.0, Blender 5.0 미지원 |
| T14 Infinigen 재질 | Python으로 Blender 노드 기술, 파라미터 랜덤화(예: 나무 roughness uniform(0,0.4)) | 레시피 수치는 LLM 참고서로 훌륭하지만 edge_wear의 Metallic 0.3745/0.3855는 게임 PBR 규칙(0/1)에서 벗어남 → 0/1 마스크로 재구성 |
| T15 Marmoset MCP | FBX 임포트 → Albedo/Normal/Roughness/Metallic/Occlusion 슬롯 → 프레이밍 → 참조 검증 → 렌더 | 예제 1건. dcc-mcp 조직 저장소는 대부분 0~1★ |

재질 규칙 전반은 [텍스처링·재질 가이드](../02_guides/05_texturing_materials.md), 3D 생성 도구 선택은 [AI 3D 생성 가이드](../02_guides/04_ai_3d_generation.md)를 보세요.

### 2.8 입문·도구 설정 경험기 (짧게)

| 사례 | 날짜 | 내용 | 신뢰도 |
|---|---|---|---|
| 공식 Blender 커넥터 설정기(한국·일본) | 2026-04~05 | Claude Desktop → 설정 → 커넥터 → 'blender' 검색 → Enable → 공식 링크에서 파일 받아 Blender에 드래그. 클리앙 사용자는 아이디어 시각화부터 모델링·텍스처링까지 약 7~10분 후기([클리앙](https://www.clien.net/service/board/park/19015735), [zenn](https://zenn.dev/shintama/articles/blender-official-mcp-claude?locale=en), [classmethod](https://dev.classmethod.jp/en/articles/claude-blender-connector-desktop-and-code/)). Threads 글의 "드래그는 반드시 2번"은 검증되지 않았고, 두 경로로 중복 설치하면 같은 ID가 둘 생긴다는 경고도 있음 | 2차 요약 |
| MindStudio 도넛 테스트 | 2026 | Blender MCP로 2시간 대화하며 도넛 튜토리얼 씬. Max 세션 토큰 약 60%, 스프링클이 접시를 뚫고 컵이 도넛과 겹치고 카메라 각도가 틀리고 화면이 마젠타로 물듦([원문](https://www.mindstudio.ai/blog/claude-blender-mcp-60-percent-tokens-donut-test-results)) | **신뢰도 낮음**(벤더 블로그, 모델 버전 미명시, 마젠타는 보통 텍스처 누락 표시). 같은 업체의 [실사용 평가](https://www.mindstudio.ai/blog/claude-blender-mcp-real-world-performance) 결론 "감독이 필요한 협업자이지 자율 3D 아티스트가 아니다"는 다른 사례들과 방향이 같음 |
| note.com 체험기 | 2026-09 | 'Interface: MCP for Blender' 애드온 → ChatGPT Desktop 연결 → 복숭아 모델링([季和](https://note.com/ekazu_10/n/n31ffbf2e0646)). Codex가 무대·바닥·배경 오브젝트 추가, 형태·재질·조명·카메라·렌더 처리([Criet](https://note.com/snapreplica/n/n77a3c9fae946?hl=en), [npaka](https://note.com/npaka/n/n9635d06c377f?hl=en)) | 2차 요약(글별 귀속 일부 불확실) |
| zenn 코드 퍼스트 | 2026-09 | MCP 대신 코드만으로 3D 씬을 만드는 '코드 퍼스트 3D 모델링' 논고([zenn](https://zenn.dev/koher/articles/code-first-3d-modeling)) | 2차 요약 |
| bilibili·zhihu | 2025~2026 | 공식 MCP로 씬 정리·머티리얼 자동 수리·지오메트리 노드·애니 자동화([bilibili](https://www.bilibili.com/video/BV1PBLS6sEEA/)), 26분 완전 튜토리얼([bilibili](https://www.bilibili.com/video/BV1SrXrY6E8D/)), 중국어 더빙([bilibili](https://www.bilibili.com/video/BV1RKXNBMEDX/)), Cursor + Blender MCP로 만든 씬을 읽어 three.js 인터랙티브 페이지로 재구성([zhihu](https://zhuanlan.zhihu.com/p/29863179256?utm_psn=1883459135720380238)) | 2차 요약(상당수 2025년 BlenderMCP 기준) |
| Show HN·AWS·Google 포럼 | 2025-06~2026 | 멀티 LLM Blender MCP 서버([Show HN](https://news.ycombinator.com/item?id=44622374), 2025-07-20), Cline + Blender MCP([AWS builders.flash](https://aws.amazon.com/jp/builders-flash/202506/cline-blender-mcp-3d-model), 2025-06), Gemini로 Blender 제어([포럼](https://discuss.ai.google.dev/t/project-showcase-control-blender-3d-using-gemini-llms-via-model-context-protocol-mcp/110424)) | 2차 요약 |
| 일본어 UI + 로컬 9B 모델 | 2026-05 | Roo Code + Ollama qwen3.5:9b로 일본어 UI Blender 4.5.7 LTS 제어. 규칙 4파일에 관찰한 실패(Solid 모드라 색이 안 보임, 치수 추측, Suzanne을 구로 오인, 결과 과장)를 실패 예시로 넣음 → 시각 검증 5/5, Suzanne 인식 5/6, 충돌 회피 2/2([GitHub](https://github.com/hideki711014/roo-blendermcp-jp-rules)) | 1차 공개. **현지화 UI의 노드 이름 번역을 type 기반 탐색으로 해결**(7.3절) |
| Codex + Higgsfield CLI | 2026-09-08 | 설치 자동화 → 테스트 씬 → 크레딧 확인 → **생성 전마다 사용자 승인** → 레퍼런스 기반 씬([GitHub](https://github.com/Arnie936/codex-blender-higgsfield)) | 1차 공개 |
| blender-design-master | 2026-08-25 | 읽기 전용 visual-critic과 점수 게이트(평균 8, 최저 7)를 둔 멀티에이전트. Codex Level 0 테스트에서 Final Gate 평균 7.4로 **미통과**([GitHub](https://github.com/Bniya-cn/blender-design-master)) | 1차 공개, 라이선스 미선언 |
| 배칭 측정 | 2026-09-09 | 동일 변환 50개를 개별 호출하면 1,949 토큰, 배치 1회면 1,018 토큰(페이로드 47.77% 감소)([GitHub](https://github.com/mohakmalviya/blender-astra-mcp)) | 1차 공개. 전체 비용이 47.77% 준다는 뜻은 아님 |
| 3dviz-pro-max 스킬 | 2026-09-11 | 'Frames, not assurances' 원칙, 전후 평가 기준선 21 → 19→23→23→25점(30점 만점, n=1)([GitHub](https://github.com/viettranx/3dviz-pro-max)) | 1차 공개 |
| [한국] 소켓 상주형 BlenderMCP | 2026(추정) | 블렌더를 띄워 둔 채 소켓으로 명령, 명령당 0.1~1초라고 주장(비교 대상은 ahujasid 서버가 아니라 명령마다 Blender를 새로 띄우는 방식의 10~15초)([GitHub](https://github.com/Aryeon0228/BlenderMCP)) | 자기 보고 |
| [한국] Unreal + Blender 통합 MCP | 미확인 | 중앙 서버(8300)에서 Blender(8400)·Unreal(8500)로 Python 명령 중계, LangChain 메모리([설계 문서](https://github.com/tahooki/unreal-blender-mcp/blob/main/Project-document.md)) | 1차 공개(한국어 문서) |

### 2.9 연구·벤치마크형 사례

논문 전체와 수치는 [학술 연구](../02_guides/11_research_papers.md)에 있습니다. 여기서는 '어떻게 했나' 관점만 짧게 적습니다.

| 사례 | 어떻게 | 결과·교훈 |
|---|---|---|
| [SceneSmith](https://github.com/nepfaff/scenesmith)(저장소 설명상 ICML 2026 Spotlight, MIT) | 단계마다 planner가 designer → critic(6항목 0~10점) → designer 사이클을 최대 3회, 모두 9점 이상이면 조기 종료, 점수가 떨어지면 체크포인트 롤백을 고려. 위치·회전을 바꿀 때마다 `check_physics`. 151단어 프롬프트로 커뮤니티 센터 전체(탁구대 옆 라켓 같은 맥락 배치) | 객체 간 충돌 0, 물리 시뮬레이션 후 안정 96%, 사용자 205명 연구에서 기준선 대비 평균 사실감 승률 92%(프로젝트 페이지, 저자 자체 보고). 기본 에이전트 GPT-5, GPU 45GB 이상 권장. 에셋 생성에 Hunyuan3D-2 옵션이 있어 **한국에서는 다른 소스로 교체** |
| [SAGE](https://github.com/NVlabs/sage)(NVIDIA, Apache-2.0) | 레이아웃을 FastMCP 툴로 노출. LLM이 객체마다 제약 4~5개를 쓰고 DFS 솔버가 bbox 충돌(전체 치수 +3.5cm)과 문 차단 영역을 고려해 풀고, 소품은 후보 150개 중 physics critic으로 거름 | 'MCP 서버 + 제약 솔버 + 물리 critic'이 1만 씬 규모로 동작. 프롬프트 규칙: 점유율 30~40%, 동선 60~90cm |
| [SceneWeaver](https://github.com/Scene-Weaver/SceneWeaver)(NeurIPS 2025, BSD-3) | Infinigen Blender를 소켓 서버로 띄우고 에이전트가 붙어 도구를 반복 호출하며 자기 평가·수정, 사용자는 Blender UI에서 실시간 확인 | blender-mcp와 같은 소켓 브리지 구조의 학술 레퍼런스 |
| [Vibe3DScene](https://github.com/3DSceneAgent/Vibe3DScene)(Apache-2.0) | LangGraph + 자체 MCP 서버·애드온(ahujasid 서버는 감사 목록에만 있음), 기본 VLM 시각 검사에 형상 관통 검사(기본 임계 0.02m) 추가 | **"VLM 눈만으로는 관통을 못 잡는다"**를 기하 검사로 보완 |
| [I-Design](https://github.com/atcelen/IDesign)(ECCV 2024) | scene graph → 백트래킹 좌표 → Objaverse 에셋을 Blender에 배치: 부모 해제, transform 적용, 원점을 bounds로, 목표 치수에 비균일 scale, z 회전에 +π 보정 | +π 보정은 에셋 정면 규약 불일치의 증거, 비균일 스케일은 가구 비율 왜곡 |
| Holodeck [#92](https://github.com/allenai/Holodeck/issues/92) / LayoutVLM [#9](https://github.com/sunfanyunn/LayoutVLM/issues/9) | 에셋 파일은 정면이 안 맞는데 씬에서는 축 정렬되어 나오고 회전 메타를 못 찾음 / 렌더 시 일부 메시 스케일·회전 오류 | 둘 다 메인테이너 무응답. **레이아웃 알고리즘보다 에셋 정면 축·실측 스케일 정규화가 먼저** |
| [SceneReVis](https://github.com/Runder-sun/SceneReVis)(MIT) | Blender 4.0.2로 overhead + diagonal 2뷰 렌더 → VLM 추론 + voxel 물리 보상 → add/move/rotate 도구로 반복 수정을 RL로 학습한 7B 모델 | 경계 이탈 2.0%, 충돌 4.5%(저자 측정, 같은 표의 Holodeck 12.7%/12.7%). '2뷰 렌더 + 루브릭 + 툴 수정' 구조는 상용 모델 MCP 루프에도 적용 가능 |
| [VIGA](https://github.com/Fugtemypt123/VIGA)(MIT) | Generator가 계획·코드 실행·에셋 검색으로 씬 코드를 쓰고 Verifier가 다중 시점 렌더를 목표와 비교, 계획·코드 diff·렌더 이력을 메모리에 누적 | 원샷 대비 BlenderGym +35%, BlenderBench +125%(검색 요약). 레퍼런스 이미지 → 씬 재현 루프의 대표 구현 |
| [LL3M](https://github.com/threedle/ll3m) | 계획 → 문서 검색(BlenderRAG) → 코드 → 디버그 → 자동 개선 → 사용자 가이드 개선(Claude Sonnet 3.7) | 모델이 retire되어 **서버 중단**. 저장소는 클라이언트뿐이고 비상업 데모 라이선스. 모델 의존 서비스의 수명 위험 |
| [BlenderAlchemy](https://github.com/ianhuang0630/BlenderAlchemyOfficial)(ECCV 2024) | VLM이 재질 노드 스크립트 편집 후보를 내고 렌더를 비교해 트리 탐색(깊이 4 × 폭 8), 개선이 없으면 되돌림 | 한 번에 코드를 쓰는 것보다 **시각 평가 반복**이 목표 재질에 잘 수렴. MCP 루프에 '후보 N개 → 렌더 → VLM 선택'을 넣는 근거 |
| [3DCodeBench](https://github.com/gaoypeng/3dcodebench) | Claude Code·Codex·Gemini CLI 하네스가 Blender 5.0으로 212개 카테고리 모델링, 트라이얼 82,042건·transcript 2,767개 공개 | 멀티턴 오류 피드백으로 실행 가능률 0.69 → 0.97, 렌더에 성공해도 떠 있거나 분리된 부품이 흔함(둘 다 논문 요약에만 있고 GitHub README에는 없어 **미확인**) |
| [La Forge](https://github.com/drakkB/scoreia-forge-results)(ScoreIA) | 8개 모델이 MCP 도구만으로 공용 부품을 조립해 3D 기사와 걷기·회전·베기 애니메이션을 만들고, 프로그램이 cm·도 단위로 채점 | 수치는 5.2절. Forge 전용 MCP의 부품 조립이라 모델링·텍스처 품질은 재지 않음 |
| [MineBench](https://github.com/Ammaar-Alam/minebench/pull/152) | Astra Pro(max reasoning, 출력 상한 128k)가 복셀 도구로 벤치 프롬프트 15개 전부 생성 | 평균 25분53.5초, 총 약 $34.71, 평균 JSON 128.53 MiB |
| [Unreal Agent Benchmark](https://github.com/44-99/unreal-agent-benchmark) | 과제 3개(Coastal Village Explorer 60분/$15 등)와 100점 채점표, 컴파일·PIE(에디터 안 플레이 테스트)·저장 후 재오픈·Win64 패키징·패키지 실행·스모크 테스트 6개 게이트 | 공식 점수는 아직 없음. **스크린샷 데모와 실제 제품의 차이**를 보는 비판적 기준 |

### 2.10 비판적으로 볼 사례

| 사례 | 주장 | 문제 |
|---|---|---|
| [AI Forge MCP](https://github.com/HurtzDonutStudios/ai-forge-mcp) | MCP 서버 16개, 도구 565개로 '컨셉 → 메시 → UV → 텍스처 → 리깅 → 애니 → LOD → UE5' 12단계 AAA 게임 에셋 풀 파이프라인, 'AI Legends' MMO 제작 | 플레이 가능한 데모·공개 에셋·독립 검증 없음. Nuitka로 컴파일된 비공개 코드, 월 $35/$65/$149(Founder). **README가 Hunyuan3D를 'MIT'라고 잘못 적음**(실제는 한국 제외 Tencent 커뮤니티 라이선스). 'AAA'를 내건 마케팅은 증거부터 요구해야 한다는 반면교사 |
| YouTube 비교 영상 제목 | 'Claude OPUS 5.5 beats GPT 6 Astra in blender ?', 'Claude Opus 5.5 Is the New KING of 3D Design & Blender', 'I Tested Claude Fable 5 in Blender (5x Faster Than Opus 4.8)' | 제목·설명만 확인. 모델 출시 직후 조회수 경쟁성 영상이 몰림. **프롬프트·시간·비용·실패 장면을 공개한 영상만 근거로** |
| MindStudio 블로그(A21, 도넛) | 한 프롬프트로 주택 워크스루, 2시간·토큰 60% | 벤더 SEO 블로그, 측정 조건 불명 |
| 재가공 기사(G19 등) | "a million times better" | ixbt·se7en.ws는 같은 영상의 재요약, geeky-gadgets는 영상 요약형 기사. 독립 출처로 셀 수 없음 |
| [ibrews UE5 MCP Field Manual](https://github.com/ibrews/ue5-mcp) | "Stationary 라이트는 Lumen GI에 기여 0", "MovieRenderGraph는 5.8 전용", "왕복 검증하면 99%, 안 하면 80%" | 앞의 두 주장은 Epic 문서와 모순(Static만 미지원, 5.7 릴리스 노트에 MRG 개선). 80/99%는 정량 근거 없음. **크래시 패턴·API 함정 참고용으로만** |
| Blender AI Arena(blenderai.org) | 시즌 3 5자 동률(1,687표) 또는 Opus 5.5 1897±79 | Blender 재단과 무관한 사이트, 상용 제품(3D-Agent) 참가, 시즌·결과가 출처마다 다름. 원문 미열람 |
| TRELLIS.2 결함률 census([이슈 #181](https://github.com/microsoft/TRELLIS.2/issues/181)) | TRELLIS.2 출력 91.1%가 non-watertight | 수리 서비스 벤더(Topoheal)의 홍보성 이슈, 표본 n=101, 2026-09-01 원저자가 표를 **철회** |

### 2.11 업계·라이선스 맥락 사례

| 사례 | 내용 | 시사점 |
|---|---|---|
| Hunyuan3D 라이선스 반발(2025-01~06) | 2.0 공개 직후 [Hacker News](https://news.ycombinator.com/item?id=42786403)에서 EU·영국·한국 제외가 지적되고, 개방형 라이선스 채택 요청 [이슈 #50](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/issues/50)이 올라옴. 2.1에서도 같은 조항 유지([LICENSE](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/LICENSE)) | 한국 크리에이터는 다른 생성 소스가 필요(7.2절) |
| Fab·Sketchfab의 AI 생성 표시 | Fab은 'Created with AI' 자가 신고와 NoAI 메타 태그를 운영하고 신고 누락을 약관 위반으로 봄([Fab 지원 문서](https://support.fab.com/s/article/Introducing-NoAI-meta-tags-and-Created-with-AI-self-declaration?language=en_US)). Sketchfab은 2025-12-11부터 판매 여부와 관계없이 모든 AI 모델에 표시 요구([Game Developer](https://www.gamedeveloper.com/business/sketchfab-to-require-mandatory-ai-disclosure-epic-games-accounts-for-users)) | 조사 단계의 "AI 범람 때문에 NoAI 태그를 도입했다"는 순서는 틀림. NoAI 태그는 Sketchfab 2023-02, ArtStation 2022-12에 이미 있었음 |
| Thaler 'A Recent Entrance to Paradise' | 순수 AI 생성물 저작권 등록 거절, 미국 저작권청 Part 2 보고서의 기준 사례([Crowell](https://www.crowell.com/en/insights/client-alerts/us-copyright-office-releases-part-2-of-artificial-intelligence-report-clarifying-copyrightability-of-generative-ai-outputs)) | 사람의 표현적 기여(수정, 선택·배열)를 기록해 두어야 함. 한국 기준은 [에셋·라이선스 가이드](../02_guides/10_assets_pipeline_licensing.md) |
| [한국] NC AI 바르코 3D | 리니지M 배경 원화팀 도입, 2~3주 작업을 약 1주로 단축([시사저널e](https://www.sisajournal-e.com/news/articleView.html?idxno=417470), [NC](https://about.ncsoft.com/news/article/gameai_01_260424)). 홍보 문구는 "3D 애셋 제작 4주 → 3분" | MCP 기반은 아님. 국내 게임사가 MCP 3D 파이프라인을 공개한 사례는 찾지 못함 |

---

## 3. 고품질 사례의 공통점

사례 전체에서 결과가 좋았던 것들을 역으로 따라가면 같은 요소가 반복됩니다.

| # | 공통점 | 근거 사례 | 이렇게 적용하세요 |
|---|---|---|---|
| 1 | **사람이 만든 에셋·실측 데이터에서 출발** | E1 CC0 키트가 가장 깨끗, E7 Fab 팩 + AI 배치, E5 메시 127개를 16,573번 인스턴싱, A3 스캔, E2 OSM·USGS, E4 크롤링, A5 측정 | "이 폴더의 에셋만으로 조립하라". 반복 요소는 인스턴싱. 치수는 [실측 치수표](../03_playbooks/05_reference_dimensions.md)와 데이터에서 |
| 2 | **생성은 역할을 나눠서** | C1 얼굴·옷은 Meshy 우세, C6·C7 생성 베이스 + 에이전트 후처리, P1·P9 하드서피스는 코드 | 유기체·캐릭터는 이미지→3D, 가구·기계는 파라메트릭 코드, 조립·UV·리깅은 에이전트([AI 3D 생성](../02_guides/04_ai_3d_generation.md)) |
| 3 | **'예쁘다'를 체크리스트로** | V1 6항목 바(수정 2라운드), E2 리뷰어별 점수와 목표치 | 품질 기준을 항목·수치로 쓰고 샷마다 판정([품질 체크리스트](../03_playbooks/04_quality_checklists.md)) |
| 4 | **에이전트에게 '눈'을 먼저 단다** | E1 CaptureViewport 디코드, G1 자체 뷰어, G5 여러 각도 스크린샷 | 변경마다 캡처 → 파일로 저장 → 판독 → 수정. 탑다운(겹침)·눈높이(미관)·플레이어 시점(스케일 감각) 3각도. Blender에서는 [`review_views.py`](../03_playbooks/scripts/README.md) |
| 5 | **숫자 검사를 먼저** | A6 물리 논리 QA, 3DCodeBench '렌더 성공해도 떠 있는 부품 흔함'(논문 요약, 미확인), Vibe3DScene 관통 검사 | [`scene_audit.py`](../03_playbooks/scripts/README.md)로 떠 있음·박힘·관통·스케일·치수를 0건으로 만든 뒤 렌더 비평. 건물·방이 있으면 [`building_audit.py`](../03_playbooks/scripts/README.md)로 문·창·방 연결도 검사 |
| 6 | **빌더와 리뷰어 분리 + 증거** | E2 "빌더는 자기 작업을 채점하지 않는다", A5 "근거 프레임 없는 지적 금지", V5 번호 붙은 타임랩스 | 읽기 전용 비평가, 실사진과 같은 시점 비교, 단계별 스크린샷 보존([에이전트 워크플로](../02_guides/09_agent_workflow_prompting.md)) |
| 7 | **스크립트를 원본으로** | V2 headless + 스킬, E11 "MCP 수정은 원본에 반영", E5 seed 고정, T3 MCP·headless 바이트 동일 | MCP는 점검·실험 레이어. 재현이 필요한 빌드는 `build_*.py` + `blender -b` |
| 8 | **엔진 제약을 숫자로** | 2.4절 Jonathan Plumb(15,000 tri, 전방축, 콜리전), G4 "플레이스홀더 금지" | 삼각형 예산, 전방축, 피벗, 콜리전, 이름 규칙을 프롬프트에 |
| 9 | **싼 픽스처로 파이프라인부터** | G2 프리플라이트 4단계 → Meshy 30크레딧만 사용 | 크기를 아는 픽스처(2m 캐릭터 등)로 임포트·빌드를 끝까지 검증한 뒤 유료 생성 |
| 10 | **사람의 반복 디렉션** | A20 10시간·21회, V1 2라운드, P6 부위별 작업 | 결함을 한 줄 목록으로 되돌려 주기. 사람 승인 게이트는 스펙·구도·최종 판정 |

### 사람이 만드는 AAA 환경의 구조와 비교

AI 사례에서 남은 문제(반복 텍스처, 밋밋한 표면)는 사람 AAA 아티스트들이 이미 정형화한 단계로 풀립니다.

| 사람 AAA 단계 | 사람 사례 | AI 사례에서 대응되는 문제 |
|---|---|---|
| 블록아웃 → 모듈러 키트 → 트림 시트 | [Detroit 영감 모듈러 씬](https://80.lv/articles/001agt-004adk-005cg-modular-scene-in-ue4-blockout-vertex-paint-decals), [SanXia Street 1940](https://80.lv/articles/005cg-001agt-sanxia-street-1940-modular-approach-trim-sheets-decals), [사막 씬](https://80.lv/articles/building-a-desert-scene-with-modular-kit-trim-sheets) | E1 CC0 키트가 가장 깨끗 |
| 버텍스 페인트·RGBA 마스크 변주·데칼 | Detroit 씬: 데칼과 버텍스 페인트가 모듈러 반복을 깨는 핵심 | E2 1~3m마다 반복되는 절차적 텍스처 |
| 절차적 변주 시스템 | [모듈러 고딕 환경](https://80.lv/articles/making-of-a-modular-gothic-environment-with-procedural-systems-trim-sheets-custom-shaders) | E1 파리 블록 파사드 변형 12·톤 5 |
| 라이팅·구도로 시선 유도 | [Get Away](https://80.lv/articles/get-away-lighting-composition-in-environment-art) | V1 섹션별 팔레트·조명 테마 |
| 다이내믹 레인지·노출 기준·베벨·불완전함 | [Andrew Price 포토리얼리즘](https://andrew-price-a9bl.squarespace.com/tutorials/secret-ingredient-photorealism) | E1 노출 클리핑, E2 환경맵 이중 계산 노출 과다, 맨 프리미티브 |

전 과정을 단계와 게이트로 정리한 것은 [AAA 제작 플레이북](../03_playbooks/02_aaa_production_playbook.md)에 있습니다.

---

## 4. 반복되는 실패 패턴과 대책

| # | 실패 패턴 | 실제 사례 | 대책 | 이 저장소 도구·문서 |
|---|---|---|---|---|
| 1 | 임포트 스케일 100배 | E1 Boeing 787 약 6km, G2 2m 로봇이 200m | FBX 내보내기에 `apply_scale_options='FBX_SCALE_UNITS'`, UE에서 `RelativeScale3D=0.01`, 크기를 아는 픽스처로 먼저 테스트. "스케일 오류는 이후 모든 것을 조용히 망가뜨린다" | `scene_audit.py`(이름 기준 치수 범위, 스케일 미적용) |
| 2 | 이미지→3D 결과가 작고 축이 다름 | E1 TRELLIS "just small", 약 1.4m로 들어오고 Y-up(사례 요약) | 임포트 직후 bounds 실측, 축 확인, 목표 크기로 정규화(G2는 1.8m, 발을 지면에) | `placement_utils.snap_to_floor()` |
| 3 | 떠 있거나 분리된 부품 | E2 떠 있는 옥상 박스, 폭발한 의자(ProfRino), A6 떠 있는 쿠션, 3DCodeBench | 연결부·접촉면을 먼저 계획, cube `size=2`, 스케일 적용, 부품은 부모로 묶기 | `scene_audit.py`(floating, `sunk_into`), `placement_utils.drop_to_surface()`. 한 유닛 안의 부품 틈은 `scene_audit.py`가 보지 않으므로 [오브젝트 모델링](../02_guides/07_modeling_objects_furniture_sculpture.md) 2.4절 `check_assembly()` |
| 4 | 관통·겹침 | P2 스페이서가 액추에이터와 겹침, 도넛 스프링클이 접시를 뚫음(신뢰도 낮음) | 형상 관통 검사(Vibe3DScene 0.02m), 간격 규칙 | `scene_audit.py`(유닛 간 `interpenetrations`, 가구–벽·천장 관통), `check_clearances()` |
| 5 | 옆에서 보면 얇음 | C5 몸통 깊이 1.45배로 수정 | 정면·측면·3/4·후면 렌더를 매 반복 | `review_views.py`(side) |
| 6 | 움직이지만 기계적으로 틀림 | P2 핀 구멍 없음, 받침대 미접촉, 날이 축에서 빠지기 전 옆으로 이동 | 관절·결합을 숫자로 검사, 분해 애니메이션으로 확인 | [오브젝트 모델링](../02_guides/07_modeling_objects_furniture_sculpture.md) |
| 7 | 벽이 사라짐·도로 마킹 뒤집힘 | E2 와인딩 반전, z 미러링 | 노멀 방향·백페이스 확인, 고정 시점 비교 | `review_views.py` |
| 8 | 텍스처 반복 | E2 1~3m마다 반복 | 트림 시트, 데칼, 버텍스 페인트, 재질 변주(3절) | [텍스처링·재질](../02_guides/05_texturing_materials.md) |
| 9 | 노멀맵 미연결·타일링 역전 | T1 PR #367 이전 Poly Haven 통합 | 렌더로 노드 연결 확인, 최신 버전 사용 | - |
| 10 | 렌더가 회색 | T2 중복 Output·Principled | 재질 코드를 멱등으로(노드 초기화) | - |
| 11 | 엔진으로 옮기면 재질이 사라짐 | T4 노드 셰이더 미전달, T3 walnut 맵 7개 중 3개만 생존 | 텍스처로 베이크, 내보내기 전 '다운로드한 맵 대 채워진 슬롯' 감사 | [에셋 파이프라인](../02_guides/10_assets_pipeline_licensing.md) |
| 12 | 노출 과다·클리핑·색 틀어짐 | E2 환경맵 이중 계산, E1 PPV 노출 11 → 오토 노출 → 6500K | 노출 기준을 먼저 잡고 한 번에 하나씩 바꾸기 | [라이팅·렌더](../02_guides/06_lighting_rendering_art_direction.md) |
| 13 | 노멀 강도 과다 | E1 8·1.5 → 0.3 | 작은 값부터 올리기 | - |
| 14 | 캡처 경로가 틀림 | G2 URP 조명 오류·애니 컬링, G12 게임 뷰 캡처 실패, V2 첫 실행 샌드박스 크래시 | 캡처 장치 자체를 검증(SubmitRenderRequest, AlwaysAnimate), 권한 확인 | - |
| 15 | 얼굴·옷 디테일 부족 | C1 Astra 직접 모델링 | 생성 모델 베이스 + 에이전트 후처리 | [AI 3D 생성](../02_guides/04_ai_3d_generation.md) |
| 16 | 딱딱한 애니메이션 | G17 11일째 해결 못함, C5 | 모캡(C14) 하이브리드 | - |
| 17 | 사진 재구성에서 지어내기·세부 오류 | A19 지적, E8 건물 오류, A8 "세부가 꽤 틀림" | "근거 없는 공간·요소는 만들지 말고 기록", 레퍼런스와 같은 시점 비교 | [프롬프트 템플릿](../03_playbooks/03_prompt_templates.md) |
| 18 | 인테리어 치수 누락·문 방향 오류 | A13 SketchUp 테스트 | 치수·문 스윙을 스펙에 명시, 간격 규칙 검사 | `check_clearances()`, `building_audit.py`(안 뚫린 문, 열면 벽·허공인 문), [실측 치수표](../03_playbooks/05_reference_dimensions.md) |
| 19 | 에셋 정면·축 규약 불일치 | E1 chair-kit 폭 축, Holodeck #92, LayoutVLM #9, I-Design +π | 에셋 정면 축과 실측 스케일을 정규화하고 메타데이터로 유지 | `placement_utils.face_towards()`(정면 -Y 규약) |
| 20 | headless 렌더 함정 | V1 GPU 컴포지터 segfault, OptiX, 초점 거리, shape key 레이캐스트 | CPU 컴포지터, OIDN, 카메라 배치 후 초점 측정 | - |
| 21 | MCP 도구에 빈틈 | G12 씬 인스턴싱 없음, ahujasid에 렌더 전용 도구 없음(이슈 #61 not planned) | `execute_blender_code`나 스크립트로 우회, 렌더→확인 절차를 스킬로 | [Blender MCP](../02_guides/02_blender_mcp.md) |
| 22 | 엔진 MCP 설정 함정마다 시간을 날림(원문 'cost an hour') | E1 자동 시작 꺼짐, 포트 8000 충돌, 비활성 툴셋 약 28개, GLB 임포트 불가 | 설정 체크리스트 | [빠른 시작](../03_playbooks/01_quickstart_setup.md), [기타 MCP](../02_guides/03_other_mcp_dcc_cad_engines.md) |
| 23 | 외부 생성 API 실패 | G2 Meshy 자동 리깅 422 | 재제출 대신 대체 경로(Blender 스크립트 리그), 원장 대조 후 재시도 | - |
| 24 | 토큰·비용 폭증 | 같은 과제 Opus 507K(zavrenn), 스크린샷 누적 | 편집을 한 번의 배치로(페이로드 47.77% 감소), 큰 이미지·로그는 파일로, effort 조절 | [AI 모델·비용](../02_guides/01_ai_models_and_clients.md) |
| 25 | 모델 은퇴로 서비스 중단 | LL3M(Sonnet 3.7 retire) | 워크플로를 특정 모델 버전에 묶지 않기 | - |
| 26 | 라이선스 오기 | AI Forge의 'Hunyuan3D MIT' | 제3자 README를 믿지 말고 원 LICENSE 확인 | 7.2절 |

---

## 5. 모델 비교 사례 (n=1 주의)

### 5.1 개인·팀 비교

| 비교 | 날짜 | 과제·조건 | 결과 | 주의 | 신뢰도 |
|---|---|---|---|---|---|
| P2 teshnizi2 | 09-08 | 6날 조리개, 프롬프트 동결, 같은 렌더 설정, 도구 끔 | 둘 다 작동, 둘 다 기계적 결함, 순위 없음 | 하네스 다름, 과제 1개 | 검증됨 |
| A4 hahaliu1029 | 09-05~08 | 같은 평면도 4스타일 | 작성자 "엄격한 순위 불가" | 카메라·조명 다름 | 1차 공개 |
| E2 PhiloLabs | 09-05 | 같은 브리프로 Fable 5.1 스웜 대 Astra 결과 나란히 영상 | Astra 쪽 점수는 없음 | - | 검증됨(Fable 점수만) |
| V4 Stefan_3D_AI | 09-22~23 | Blender 절차적 원프롬프트 10초 샷, Max로 맞춤 | Opus 5.5 35분·출력 199.6k·약 $13.3 / Astra 28분·56.6k·약 $14.5. 드로리안은 Opus 73분·218k | 금액은 2차 요약 기준(원 큐레이션의 통화 기호 손상), X 원문 미확인 | 자기 보고 |
| zavrenn | 09-22~24 | 같은 Blender 과제, Max | "결과는 거의 같음", Astra 43분·출력 61K 대 Opus 1시간57분·507K | 제목은 '3x fewer tokens'인데 수치는 약 8.3배. **한쪽은 출력, 다른 쪽은 전체 토큰일 가능성** → 배율 근거로 쓰지 말 것([X](https://x.com/zavrenn/status/2103181133198639614)) | 2차 요약 |
| P6 3DVR3 | 09-22~24 | Quest 3 사진 → 모델 | Opus 5.5가 두께·기울기·흑백 밸런스 우세, 부위별로 나눠 작업 | n=1 | 2차 요약 |
| P4 Danny Stuart / Hierarchy | 09 초 | 같은 시작 프롬프트, Blender MCP | 3D는 Astra가 큰 차이로 우세(렌더가 깔끔, 손볼 곳 적음). Fable 5.1은 뷰포트를 보며 스스로 고치고 더 빠르고 싸며 아이디어가 다양하지만 마이크로카피를 과하게 넣는 버릇 | 결론 "공간 작업은 Astra, 소프트웨어 완성·오케스트레이션은 Fable 5.1" | 2차 요약 |
| E4 Martin Puli | 07-21 | 맨해튼 | "GPT 5.6 Sol이 Fable 5를 크게 이긴다" | 이전 세대 | 자기 보고 |
| C1 happy_modeling | 09-09 | 같은 일러스트 → 캐릭터 | Meshy 7이 얼굴·옷 우세, 8분 대 3분 | LLM 대 생성 모델 비교 | 2차 요약 |
| G8 Cagri Kacmaz | 09-05~06 | 같은 PROMPT.md, 문명 시뮬 | Astra High는 3D·카메라 작동, Gemini 3.8 Flash High는 지형 평평·카메라 실패 | 하네스 다름, "과학적 벤치마크 아님" | 1차 공개 |
| G1 Nipale 대 GLM-5.3 | 09-01 | 같은 프롬프트·같은 머신 | Fable 5.1 24분, GLM-5.3 27분에 다른 게임 | 오픈 모델 대조 | 검증됨 |
| G15 AiBattle | 09 | 같은 Godot 게임, Astra Max 대 Medium | 53분(주간 한도 4%) 대 25분(1%) | effort 차이만 비교 | 2차 요약 |
| V7 AI타임스 | 2026 | 같은 프롬프트 3D 애니 | 연출 Opus 5.5, 비용·속도 GPT-5.6, Fable 5.1 연출 정교함 부족 | 검색 요약 | 2차 요약 |
| Every Vibe Check | 09 | 팀 일상 업무 | 마리오카트형 게임에서 Opus 5.5가 Fable 5.1보다 훨씬 좋았다는 비교 인용, "Fable 5.1과 동급이거나 약간 낫다"([Every](https://every.to/vibe-check/vibe-check-opus-5-5-is-pulling-our-codex-converts-back-to-claude)) | 귀속은 검색 요약 기준 | 2차 요약 |
| Nate Herk 12개 과제 | 09-23~24 | 웹·영상 편집·3D 게임·여행 플래너 등 | Opus 8 대 Astra 4. Astra는 총시간 약 45%, 비용 약 38% 적음([X 아티클](https://x.com/nateherk/article/2102904721698599231)) | 요약 기사가 저품질(geeky-gadgets) | 신뢰도 낮음 |
| G19 Brendan Jowett | 09-24~25 | UE + Blender 게임 | "Opus 5.5 모든 테스트 우세" | 재가공 기사만 | 신뢰도 낮음 |
| RobLe3(P9) | 2026-05 | 역할 분담 | 테스트는 Haiku, 패치는 Opus로 약 10배 저렴 | 이전 세대 모델 | 검증됨 |

### 5.2 구조화된 벤치마크 (참고)

같은 하네스·같은 MCP 서버로 GPT-6 Astra, Opus 5.5, Fable 5.1, Gemini, 오픈웨이트를 한꺼번에 비교한 통제 3D 벤치마크는 2026-09 현재 없습니다. 아래 수치는 조건이 서로 달라 한 표에서 순위를 매기면 안 됩니다.

| 벤치마크 | 무엇을 재나 | 결과 | 주의 |
|---|---|---|---|
| La Forge(2026-09-24) | MCP 도구만으로 3D 기사 조립·애니, 프로그램 채점 | 6개 캠페인 단순평균(이 조사가 계산) Opus 5.5 99.8, Fable 5.1 99.4, Astra 97.9, Grok 4.7 96.2, GPT-6 Sol 94.6, DeepSeek flash 91.3, Sonnet 5 81.1, Haiku 4.5 40.4. 시간·공간 동시 제약(taille-3)은 Opus 5.5 100, Astra 88.1, Sonnet 5 19.5 | 하네스가 모델마다 다름, 심판을 Opus로 작성, 모델 신원은 자기 신고, 모델링·텍스처 품질은 측정 안 함 |
| [Arena Code](https://raw.githubusercontent.com/oolong-tea-2026/arena-ai-leaderboards/main/data/2026-09-26/code.json)(2026-09-25) | 웹·앱 코드 사람 투표 Elo | Opus 5.5 max 1827±18, Astra max 1792±11, Fable 5.1 max 1751±10 | 3D 전용 아님, Opus 5.5 표본 1,607표 |
| [Design Arena 3D](https://modelgrep.com/best/3d) | Three.js/WebGL 3D 장면 코드 투표 | Astra 1464, Kimi K3 1417, Fable 5.1 1415 | 집계 사이트 경유, Opus 5.5 없음, 신뢰도 낮음 |
| [3DHarnessBench](https://github.com/llada60/3DHarnessBench)(2026-09) | 3D 물체 → Blender 코드 복원, 접근 조건 4가지 | Opus 5가 Active Visual·Full 3D Interaction 1위, 함수 호출 접근이 늘수록 모든 모델 개선 | Opus 5.5·Fable 5.1 미평가 |
| CADGenBench(P13) | build123d-mcp로 CAD 생성·편집 | Opus 5 0.677, GPT-5.6 Sol 0.532, Gemini 3.7 Flash 0.508 | 도구 저자 자체 평가 |
| BenchCAD | 4뷰 렌더 → CadQuery | 공식 재채점(도구 없음, 0~1 척도) 최고 Gemini 3.1 Pro IoU 0.289, 벤더 보고(†) 최고는 Claude Mythos 5 0.384. OpenAI 발표 'Astra 95.9%'는 도구를 쓴 조건의 다른 척도 **(벤더 자체 보고, 원문 미확인)** | 두 수치를 같은 표에 두지 말 것 |
| MineBench | 복셀 건축 | Astra Pro 15/15 생성, 평균 25분53.5초, $34.71 | 순위 점수 미확인 |

### 5.3 사례에서 보이는 경향 (잠정)

| 작업 | 사례에서 나온 경향 | 근거 | 신뢰도 |
|---|---|---|---|
| Blender 하드서피스·기계 재구성, 3D 렌더 | Astra 선호 보고가 많음 | P1, P4, Design Arena 3D | 낮음~중간(대부분 n=1) |
| 같은 과제의 시간·토큰 | Astra가 적게 쓴다는 보고가 반복 | V4, zavrenn, Nate Herk | 낮음(토큰 종류 혼재) |
| 제품 비율·연출 디테일·정밀 시간·공간 제약 | Opus 5.5 우세 보고 | P6, V7, La Forge taille-3 | 낮음~중간 |
| 기획·코드·오케스트레이션·자가 검증 | Fable 5.1 선호 보고 | P4, G1, G16, E2 | 낮음 |
| 캐릭터 얼굴·옷 | LLM 직접 모델링보다 이미지→3D | C1 | 낮음 |
| CAD 도면 해석 | 사람이 스펙으로 바꿔 주는 것이 모델 교체보다 효과 큼 | P12, P13 | 중간 |

모델 선택 기준 전체는 [AI 모델 비교·선택](../02_guides/01_ai_models_and_clients.md)에 있습니다. 벤치마크 전반의 결론도 같습니다. **모델을 바꾸기 전에 하네스(렌더→검증→수정 루프, 멀티턴 오류 피드백, 전용 MCP 도구)를 먼저 개선하세요.**

### 5.4 직접 비교할 때 지킬 것

P2와 A4에서 가져온 프로토콜입니다.
1. 프롬프트를 동결하고 해시를 남깁니다.
2. 같은 하네스, 같은 MCP 서버, 같은 Blender 버전과 렌더 설정을 씁니다. **effort를 명시합니다**(Codex의 Astra 기본값은 low, Opus 5.5 기본값은 medium).
3. 생성 코드를 고치지 않고 렌더합니다. 실패한 시도도 기록합니다.
4. 같은 기기, 같은 방, 같은 카메라 시점으로 나란히 봅니다.
5. 시간과 토큰은 출력 토큰인지 전체 토큰인지, 구독 한도인지 API 금액인지 구분해 적습니다.
6. 한 과제로 순위를 매기지 않습니다.

---

## 6. 비용·시간 참고값

대부분 작성자 자기 보고이고, 조건(모델, effort, 하드웨어, 플랜)이 다릅니다. 예산 감을 잡는 용도로만 쓰세요.

| 구분 | 사례 | 값 | 조건 | 신뢰도 |
|---|---|---|---|---|
| 짧은 반복 | V2 Simon Willison | 2분39초 / 3분51초 / 5분59초 | Astra Medium, headless Blender, 프롬프트 3개 | 검증됨 |
| 짧은 반복 | V1 Vizuara 컨택트시트 | 샷당 2~16초 | EEVEE 720p 1프레임, M1 8GB | 검증됨 |
| 단일 모델 | C1 happy_modeling | 8분(Astra) 대 3분(Meshy 7) | 캐릭터 1체 | 2차 요약 |
| 단일 모델 | A13 SketchUp | 모델당 17~22분, Plus 주간 할당량을 하루에 | Astra, 주택 | 2차 요약 |
| 단일 모델 | P8 Rhino | 약 40분(계획안 수준) | Astra | 2차 요약 |
| 단일 씬 | A19 Bad Decisions | 30분 이내 | 사진 → 건물 | 자기 보고 |
| 단일 씬 | E10 claude-3d-harness | 3시간 미만, 메시 449 | 블록아웃 → 최종 프레임 | 1차 공개 |
| 원프롬프트 | G1 Nipale | 24분, $9.90, 75턴, 출력 95,832 토큰 | Fable 5.1 high, RTX 5090 로컬 생성 | 검증됨 |
| 원프롬프트 | V4 Stefan | Opus 5.5 35분·199.6k / Astra 28분·56.6k, 드로리안 Opus 73분·218k | Max, 금액은 2차 요약 기준 | 자기 보고 |
| 원프롬프트 | zavrenn | Astra 43분·출력 61K / Opus 1시간57분·507K | 토큰 종류 혼재 가능 | 2차 요약 |
| 게임 | G15 AiBattle | Max 53분(Pro x5 주간 한도 4%) / Medium 25분(1%) | Astra, Godot | 2차 요약 |
| 게임 | G10 X 트렌딩 | 약 45분 | 그래픽은 이미지 생성 | 2차 요약 |
| 게임 | G14 드리프트 | 약 30분 | Claude Code + mcp-unity | 자기 보고 |
| 게임 | G2 Robo Open | 프로토타입 52분, 세션 4시간23분, WebGL 정상 빌드까지 53분, Meshy 30크레딧(상한 400 승인) | Astra/Codex, Unity | 검증됨 |
| 게임 | G19 Brendan Jowett | 60~120분, Opus 5.5 2시간 API 약 $60~70 | 재가공 기사 | 신뢰도 낮음 |
| 장기 | A20 SpenserFX | 10시간, 수정 21회, 130만 폴리곤 | 사람 디렉션 | 2차 요약 |
| 장기 | E13 도시 게임 | 5일 | 다나와 정리 | 2차 요약 |
| 장기 | G3 How to Suck | 첫 반복 39시간, 전체 개발에 Pro x20 주간 한도 2회분 | Astra/Codex, Unity | 검증됨(정정 반영) |
| 장기 | A18 Fallingwater | "무인 연산 54시간" | 큐레이션 인용 | 2차 요약 |
| 렌더 | V1 Vizuara | 프레임당 12~44초(A10G), 8분 챕터 10,964프레임을 A10G 약 50대로 84분 + 합성 5분 | Cycles 1080p 384 samples | 검증됨 |
| 3D 생성 | E1 per-simmons | Meshy 약 4분, TRELLIS 약 1분 | fal.ai / Replicate | 검증됨 |
| 3D 생성 | T5 asset-studio | crate 11.1분, pump 15.6분, 재최적화 약 80초 | RTX 5090 로컬 | 검증됨 |
| 3D 생성 | T6 image-to-3dlab | TRELLIS.2 15~35분, Hunyuan 리페인트 약 6분, Qwen-Image 약 4.5분 | Apple Silicon | 검증됨 |
| 3D 생성 | T8 Meshy | preview 약 30초, refine 약 2분 | 벤더 문서 | 벤더 문서 |
| 벤치 | MineBench Astra Pro | 프롬프트당 평균 25분53.5초, 15개 총 $34.71 | max reasoning | 1차 공개 |
| 벤치 | P13 CADGenBench | Opus 5 실행 API 환산 약 $724.77(GPT-5.6 Sol 대비 토큰 +44%) | 81 fixture | 도구 저자 자체 평가 |
| 입문 | 공식 커넥터 설정기 | 아이디어 → 모델링·텍스처링 약 7~10분 | 클리앙 후기 | 2차 요약 |
| 절약 | 배칭 | 변환 50개: 개별 1,949 토큰 대 배치 1,018 토큰 | cl100k_base | 1차 공개 |
| 절약 | T1 Poly Haven 수정 | 다운로드 49% 감소 | 1k 텍스처 860개 | 검증됨 |
| 업계 | NC AI 바르코 3D | 배경 작업 2~3주 → 약 1주 | MCP 아님 | 2차 요약 |

**읽는 법**
- 구독 한도 %는 플랜마다 다르고, API 환산 금액은 모델 단가와 출력/전체 토큰 구분에 따라 달라집니다. 단가는 [AI 모델·비용 가이드](../02_guides/01_ai_models_and_clients.md)를 보세요.
- 같은 과제라도 effort가 비용을 크게 바꿉니다(G15: 4배). 반복 단계는 낮게, 최종 단계는 높게 주는 방식이 여러 사례에서 쓰였습니다.
- yangqiong 라운드업의 금액은 '$'가 깨져 있어 통화 단위를 확인하지 못했습니다.

---

## 7. 한국 사용자 관점 메모

### 7.1 한국 관련 사례

| 사례 | 성격 | 비고 |
|---|---|---|
| E5 octopus7 숲 | GitHub 1차 공개, 검증됨 | 한국 사례라는 근거는 README_KO뿐(추정) |
| V3 openerai 프리비즈 스킬 | 한국어 Claude Code 스킬 | 해외 방법론(Higgsfield 블로그)의 한국어 재구성, [AI 영상] |
| T4 KINGWONWOO | Claude + Nano Banana + UE 파이프라인 | 한국 개발자로 추정 |
| 2.8절 Aryeon0228, tahooki | 한국어 문서의 MCP 도구 | 자기 보고·설계 문서 |
| E13 다나와 DPG, G20 게임뷰, V7 AI타임스 | 한국어 기사 | 검색 요약 기준 |
| A17 뽁숑이, C13 2D 로봇, G14 드리프트 게임 | 한국어 유튜브·Threads | 품질 미확인 |
| 한국어 'GPT-6 × 블렌더' 영상 | [바이브 모델링](https://www.youtube.com/watch?v=_S4SaiNBlRk), [모델링 & 애니메이션](https://www.youtube.com/watch?v=JT9kgRePJ-E) | 제목·요약만 확인 |
| 클리앙 결과물 게시글 | [Astra 결과물](https://www.clien.net/service/board/park/19258409) | 커뮤니티 평은 "속도는 빠르지만 고급 모델러 수준에는 못 미침, 인디 프로토타입 정도" |
| 공식 커넥터 설치 요령(Threads) | [dddesign.io](https://www.threads.com/@dddesign.io/post/DXsWAspka7F/%ED%81%B4%EB%A1%9C%EB%93%9C-%EB%B8%94%EB%A0%8C%EB%93%9C-%EC%BB%A4%ED%85%8D%ED%84%B0-%EC%82%AC%EC%9A%A9%EB%B2%95%EA%B3%B5%EC%8B%9D-%EA%B0%80%EC%9D%B4%EB%93%9C%EA%B0%80-%EB%B6%88%EC%B9%9C%EC%A0%88%ED%95%B4%EC%84%9C-%EB%A7%8C%EB%93%AC1-claude-%EB%8D%B0%EC%8A%A4%ED%81%AC%ED%83%91-%EC%84%B8%ED%8C%85-%EC%BB%A4%EB%84%A5%ED%84%B0-%EC%9D%B4%EB%8F%992-blender-%EA%B2%80%EC%83%89-%EC%84%A0%ED%83%9D3-enbaled-%EB%88%84?hl=ko) | "드래그 2번"은 미검증 |
| 인프런 Meshy 클립 | [강의](https://www.inflearn.com/clip/570) | Meshy 결과가 처음 100만 폴리곤 넘음 → 리메시로 약 1만 |

한국어 자료 전체는 [한국어 자료 모음](02_korean_resources.md)에 있습니다. 한국어 유튜브·블로그 원문은 네트워크 차단으로 대부분 확인하지 못했고, MCP 기반 3D 파이프라인을 공개한 국내 게임사 사례도 찾지 못했습니다.

### 7.2 사례를 한국에서 재현할 때의 라이선스 점검

| 사례·도구 | 걸리는 구성요소 | 문제 | 대안 |
|---|---|---|---|
| mcp-for-blender의 Hunyuan3D 연동(로컬 모드), 2.10 AI Forge의 ForgeHunyuan, T6의 Hunyuan-MLX, SceneSmith의 Hunyuan3D-2 옵션, T3 kiln의 Hunyuan3D 소스 | Tencent Hunyuan3D 계열 오픈웨이트(2.0/2.1/Omni/Part, HY-World, HY-Motion, BPT) | 라이선스 적용 지역에서 **대한민국·EU·영국 제외**, Territory 밖 출력물 사용도 금지 → 한국에서 로컬 사용은 라이선스 범위 밖 | Tripo·Meshy·Rodin 같은 상용 서비스(플랜별 상업권 확인), TRELLIS.2(아래 주의), Stable Fast 3D(연매출 100만 달러 미만 + 등록 필요). Tencent Cloud API 경유는 별도 약관(원문 미확인)이고, 한국 계정은 국제(ap-singapore) 엔드포인트 토글이 필요 |
| T5 asset-studio, TRELLIS.2 파이프라인 | 기본 배경 제거기 BRIA RMBG-2.0 | gated 비상업 라이선스 | 알파 PNG를 직접 입력 |
| TRELLIS.2 공식 GLB 베이크 | nvdiffrast(NVIDIA Source Code License) | 비상업(연구·평가) 제한, DINOv3 조건 | 상업 프로덕션 전 의존성 검토 |
| T6 텍스트 → 이미지 경로 | Qwen-Image 2.1 가중치 | 비상업 | 다른 이미지 모델 |
| E1 per-simmons, V1 Vizuara, P9 참고 스킬 ProfRino, 2.8 Bniya-cn | 저장소 자체 | LICENSE 파일 없음 → 코드 재사용 권한 없음 | 방법만 참고하고 직접 작성 |
| G11 Paper Ember Duel | 저장소 자체 | 상업 재사용 불허 명시 | 참고용 |
| T8 Meshy 무료 플랜 | 출력물 | CC BY 4.0(Meshy 표기 필요) | 유료 플랜은 비공개 상업 라이선스 |

한국 인공지능기본법(2026-01-22 시행) 제31조의 생성형 AI 결과물 표시 의무와 저작권 등록 기준은 [에셋·라이선스 가이드](../02_guides/10_assets_pipeline_licensing.md)에 정리했습니다.

### 7.3 한국어 UI에서 사례 코드가 깨지는 문제

해외 사례 코드는 영어 UI를 전제로 `nodes["Principled BSDF"]`처럼 노드를 **이름**으로 찾는 경우가 많습니다. 한국어·일본어 UI에서 새로 만든 데이터의 이름이 번역되면 `KeyError`가 납니다. 일본어 UI 사례(2.8절, 로컬 9B 모델)는 노드를 `type`으로 찾는 방식으로 해결했습니다. 이 저장소의 [보조 스크립트](../03_playbooks/scripts/README.md)도 노드를 타입으로 찾도록 만들어 한국어 UI에서 동작합니다. 다만 오브젝트 이름은 영어로 지어야 합니다. `scene_audit.py`는 이름의 영어 단어(`chair`, `SM_Armchair_A`처럼 snake_case·CamelCase 모두 인식)로 치수 규칙을 고르고, 한국어 이름('의자')은 인식하지 않습니다. Preferences에서 새 데이터 이름 번역(New Data)을 끄는 방법도 있습니다([에이전트 워크플로](../02_guides/09_agent_workflow_prompting.md)).

### 7.4 치수

사례 대부분은 미국·일본·중국 공간을 기준으로 만들었습니다. 한국 아파트의 천장고, 문, 주방 상판, 침대 규격은 다를 수 있으니 [실측 치수표](../03_playbooks/05_reference_dimensions.md)의 한국 기준으로 스펙을 주세요. 예를 들어 구축 아파트(천장고 2300 mm)라면 `scene_audit.audit_scene(floor_z=0.0, ceiling_z=2.30, collection="Room")`으로 천장을 뚫는 가구를 잡을 수 있습니다. 예컨대 높이 236 cm짜리 IKEA PAX 옷장은 2300 mm 천장에 들어가지 않습니다.

---

## 흔한 실수와 해결

사례를 참고하거나 따라 할 때 자주 생기는 실수입니다.

| 실수 | 왜 문제인가 | 해결 |
|---|---|---|
| X 게시물 수치를 사실처럼 인용 | 작성자 자기 보고이고 원문 미확인 | '자기 보고(n=1)'로 표기, 저장소·로그가 있는 사례를 우선 |
| Tripo 카탈로그 프롬프트를 원문으로 착각 | 48%가 Tripo가 쓴 'Build brief' | 항목의 'Build brief based on the linked work' 표시 확인 |
| yangqiong 금액을 그대로 사용 | '$'가 HTML 주석으로 깨짐, 중복 행 | 원 게시물이나 다른 출처와 대조 |
| 토큰 배율을 단순 비교(61K 대 507K) | 출력 토큰과 전체 토큰이 섞였을 가능성 | 토큰 종류를 확인하고, 모르면 배율을 쓰지 않음 |
| SNS 영상의 '포토리얼'을 3D 품질로 판단 | AI 비디오를 입힌 경우가 많음 | 2.6절 체크리스트로 [AI 영상] 여부 확인 |
| effort를 모르는 채로 모델 비교 | Codex의 Astra는 기본 low | 비교 시 effort를 명시(5.4절) |
| '공개 저장소 = 재사용 가능'으로 착각 | LICENSE 없는 저장소가 많음 | LICENSE 파일 확인(7.2절) |
| 사례 스크립트를 다른 공간·에셋에 그대로 실행 | Realsee처럼 공간 전용인 경우가 많음 | 방법(순서·규칙)만 가져오고 코드는 새로 |
| 벤더 쇼케이스를 평균 품질로 기대 | 선별된 결과 | 1차 공개·검증 사례(E2의 6~7/10)를 기준선으로 |
| "Blender MCP"가 어느 서버인지 확인하지 않음 | 공식 Blender Lab 서버와 ahujasid 서버는 도구 구성이 다르고 둘 다 9876 포트 | 사례의 서버를 확인하고 한 Blender에 서버 하나만([Blender MCP](../02_guides/02_blender_mcp.md)) |
| 오래된 사례 코드를 최신 Blender에서 실행 | EEVEE 식별자(4.2~4.x `BLENDER_EEVEE_NEXT`, 5.x `BLENDER_EEVEE`), `use_gtao` 등 제거된 속성, 5.0의 `use_nodes` 폐기 예고 | 버전 함정 표([Blender MCP](../02_guides/02_blender_mcp.md)) 확인. 현재 안정판은 5.2.2(2026-09-14, 5.2 계열은 LTS) |
| 논문·데모 서비스를 따라 하다 막힘 | 쓰던 모델이 retire(LL3M) | 모델 설정을 바꾸고 워크플로를 특정 모델에 묶지 않음 |
| 한국에서 Hunyuan3D 사례를 그대로 재현 | 라이선스 적용 지역에서 한국 제외 | 7.2절 대안으로 교체 |

---

## 관련 문서

- [목적·범위](../00_purpose/purpose_and_scope.md) · [조사 방법·신뢰도 정책](../01_research/research_method.md) · [출처 카탈로그](../01_research/sources_catalog.md) · [검증 로그](../01_research/verification_log.md)
- [AI 모델 비교·선택·비용](../02_guides/01_ai_models_and_clients.md): Astra·Fable 5.1·Opus 5.5 선택 기준, effort, 단가
- [Blender MCP 생태계](../02_guides/02_blender_mcp.md): 공식 Blender Lab 서버 대 ahujasid MCP for Blender, 보안, 버전 함정
- [기타 DCC·CAD·게임엔진 MCP](../02_guides/03_other_mcp_dcc_cad_engines.md): UE 5.8 Unreal MCP, Unity, Godot, Roblox, SketchUp, Rhino
- [AI 3D 생성](../02_guides/04_ai_3d_generation.md) · [텍스처링·재질](../02_guides/05_texturing_materials.md) · [라이팅·렌더·아트디렉션](../02_guides/06_lighting_rendering_art_direction.md)
- [오브젝트·가구·조형 모델링](../02_guides/07_modeling_objects_furniture_sculpture.md) · [배치·레이아웃](../02_guides/08_scene_layout_placement.md)
- [에이전트 워크플로·프롬프팅](../02_guides/09_agent_workflow_prompting.md) · [에셋·파이프라인·라이선스](../02_guides/10_assets_pipeline_licensing.md) · [학술 연구](../02_guides/11_research_papers.md)
- [빠른 시작](../03_playbooks/01_quickstart_setup.md) · [AAA 제작 플레이북](../03_playbooks/02_aaa_production_playbook.md) · [프롬프트 템플릿](../03_playbooks/03_prompt_templates.md) · [품질 체크리스트](../03_playbooks/04_quality_checklists.md) · [실측 치수표](../03_playbooks/05_reference_dimensions.md)
- [CLAUDE.md 템플릿](../03_playbooks/templates/CLAUDE.md) · [Blender 스킬 템플릿](../03_playbooks/templates/skills/blender-aaa-scene/SKILL.md)
- [보조 스크립트 사용법](../03_playbooks/scripts/README.md): `scene_audit.py`, `placement_utils.py`, `review_views.py`, `building_audit.py`
- [한국어 자료 모음](02_korean_resources.md)

## 원자료

- [`01_research/raw/11_case-studies.research.json`](../01_research/raw/11_case-studies.research.json): 사례 연구 조사(사례 35, 항목 20, 노하우 24)
- [`01_research/raw/11_case-studies.verify.json`](../01_research/raw/11_case-studies.verify.json): 독립 검증. 반영한 주요 정정: UE 5.8 Unreal MCP는 '실험적', Blender Lab MCP는 GPL-3.0, mcp-for-blender의 Tripo는 Premium 전용·텔레메트리 기본 수집, PR #353 미병합·#359 거절, per-simmons의 TRELLIS 평가·조명 순서·'cost an hour'·LICENSE 없음, Robo Open 실패 22건·v0.3 사람 플레이테스트, How to Suck 주간 한도 해석, Vizuara 라이선스 미지정, openerai는 한국어 재패키징, octopus7 한국·Astra 추정, flopperam 로컬판 UE 5.5~5.7, Godot HUD '약 2시간' 미확인, zavrenn 토큰 배율 주의, Tripo 카탈로그 48% 브리프, AI Forge 신뢰도 낮음
- [`01_research/raw/G3_videos_cases.gap.json`](../01_research/raw/G3_videos_cases.gap.json): 영상·소셜·벤더 워크스루 보완 조사(사례 28)
- 사례 배열을 통합한 나머지 원자료: [`01_ai-models`](../01_research/raw/01_ai-models.research.json)(사례 12), [`02_blender-mcp`](../01_research/raw/02_blender-mcp.research.json)(7), [`03_dcc-cad-mcp`](../01_research/raw/03_dcc-cad-mcp.research.json)(9), [`04_engine-mcp`](../01_research/raw/04_engine-mcp.research.json)(7), [`05_ai-3d-generation`](../01_research/raw/05_ai-3d-generation.research.json)(8), [`06_texturing-materials`](../01_research/raw/06_texturing-materials.research.json)(10), [`07_aaa-rendering-lighting`](../01_research/raw/07_aaa-rendering-lighting.research.json)(6), [`08_modeling-objects`](../01_research/raw/08_modeling-objects.research.json)(8), [`09_scene-layout`](../01_research/raw/09_scene-layout.research.json)(8), [`10_agent-workflow`](../01_research/raw/10_agent-workflow.research.json)(8), [`12_assets-pipeline-licensing`](../01_research/raw/12_assets-pipeline-licensing.research.json)(6), [`13_research-papers`](../01_research/raw/13_research-papers.research.json)(7), [`G2_korean_resources`](../01_research/raw/G2_korean_resources.gap.json)(10), [`G4_licensing_pricing`](../01_research/raw/G4_licensing_pricing.gap.json)(3), [`G5_aaa_practice`](../01_research/raw/G5_aaa_practice.gap.json)(7), [`G6_benchmarks_models`](../01_research/raw/G6_benchmarks_models.gap.json)(3)
- 정정에 반영한 검증 파일: [`01_ai-models.verify`](../01_research/raw/01_ai-models.verify.json)(Stefan 수치 미확인, 신뢰도 낮은 출처 목록, Higgsfield 풍차 미확인, Stefan Tripo 게시물 ID 불일치, BenchCAD 'Astra 95.9%'와 3DCodeBench 0.69→0.97 미확인), [`02_blender-mcp.verify`](../01_research/raw/02_blender-mcp.verify.json)(cc-blender-skill 공식 서버 이전 서술 반박, MindStudio·GameDev Academy 신뢰도 낮음, claude-3d-harness 옥상 사례), [`05_ai-3d-generation.verify`](../01_research/raw/05_ai-3d-generation.verify.json)(sketch-to-3d-codex 미테스트, rodin-via-blender·aigeboku 증빙 없음, TRELLIS.2 결함률 철회), [`06_texturing-materials.verify`](../01_research/raw/06_texturing-materials.verify.json)(blender-kiln 갤러리는 스크립트 경로, Poly Haven 버그 경로), [`08_modeling-objects.verify`](../01_research/raw/08_modeling-objects.verify.json)(kitchen-twin DSL 각색, Home Wizard 모델명, CADGenBench 해석, IKEA 의자·침대·Adam Keating 누락 보완), [`09_scene-layout.verify`](../01_research/raw/09_scene-layout.verify.json)(Vibe3DScene 자체 서버, SAGE 수치), [`10_agent-workflow.verify`](../01_research/raw/10_agent-workflow.verify.json)(Bniya-cn Final Gate 7.4·라이선스 없음, kiln Iron Rules 31), [`12_assets-pipeline-licensing.verify`](../01_research/raw/12_assets-pipeline-licensing.verify.json)(image-to-3dlab Qwen-Image 비상업, Hunyuan 국제 엔드포인트), [`13_research-papers.verify`](../01_research/raw/13_research-papers.verify.json)(La Forge 한계, LL3M 코드 비공개, SceneSmith 충돌 0·승률은 기준선 대비 평균, 3DCodeBench trial·transcript 수), [`G4_licensing_pricing.verify`](../01_research/raw/G4_licensing_pricing.verify.json)(NoAI 태그 인과 정정)
