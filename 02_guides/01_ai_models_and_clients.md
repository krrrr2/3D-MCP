# AI 모델·MCP 클라이언트 선택 가이드 (아스트라·페이블·오푸스 5.5)

> 기준일: 2026-09-27 · '아스트라·페이블·오푸스 5.5'가 정확히 무엇인지 정리하고, 3D 작업마다 어떤 모델·effort·클라이언트를 쓸지, 비용이 얼마나 드는지 근거와 신뢰도를 붙여 정리했습니다.

## 핵심 요약

- **이름부터**: '아스트라'는 OpenAI **GPT-6 Astra**(2026-09-03 출시. 2차 출처로 확인했고 openai.com 원문은 열람하지 못함)입니다. Google의 'Project Astra'와는 관계없습니다. '페이블'은 Anthropic **Claude Fable 5.1**(2026-09-01, $10/$50), '오푸스 5.5'는 **Claude Opus 5.5**(2026-09-22, $4/$20, 1M 컨텍스트, 기본 effort medium)입니다.
- **절대 1위는 없습니다.** 세 모델을 같은 하네스·같은 MCP 서버로 비교한 통제 벤치마크가 아직 없고, 독립 지표마다 1위가 다릅니다. 공개된 모델 비교는 대부분 개인 테스트(n=1)이고 결과도 엇갈립니다. 그래서 이 문서는 순위 대신 **작업 유형별 선택 기준**을 제시합니다.
- **작업별 잠정 선택**: 공간·치수·CAD·사진/도면 재구성은 Astra(high 이상), 장시간 씬 빌드·룩뎁·애니메이션 타이밍·정밀 배치는 Opus 5.5, 가장 어려운 계획과 오케스트레이션은 Fable 5.1, 대량 반복은 Sonnet 5나 GPT-6 Sol, 저가 렌더 1차 검수는 Gemini 3.8 Flash가 맞습니다.
- **effort는 반드시 직접 지정하세요.** Codex에서 Astra의 기본 effort는 **low**이고(Codex models.json 기준, 단계는 low/medium/high/xhigh/max/ultra), Opus 5.5의 기본값은 **medium**입니다. 지정하지 않으면 품질이 떨어지고 모델 비교도 왜곡됩니다.
- **유기체·캐릭터는 어떤 LLM도 직접 모델링을 잘 못합니다.** 생성형 3D로 메시를 만들고 LLM은 조립·리깅·배치를 맡기세요. **한국 사용자 주의**: Tencent Hunyuan3D 계열 오픈웨이트 라이선스는 적용 지역에서 대한민국을 제외합니다.
- **모델을 바꾸기 전에 하네스부터 고치세요.** 실행 오류를 모델에 되돌려 주기만 해도 Blender 코드 실행 가능률이 0.69에서 0.97로 올랐다는 보고가 있습니다(3DCodeBench. 논문 요약에만 있는 수치로 **미확인**). 렌더→멀티뷰 비평→수치 검사 루프가 모델 차이보다 결과를 더 크게 바꿉니다.
- **클라이언트**: 3D 에이전트 작업에는 Claude Code와 Codex(CLI/앱)가 가장 적합합니다. 비개발자는 Claude Desktop에 공식 Blender 커넥터를 붙이는 방법이 가장 쉽습니다. ChatGPT 웹 채팅은 원격 MCP만 지원해 로컬 Blender에 직접 붙지 않습니다. Cursor는 활성 도구가 약 40개로 제한되고, Gemini CLI는 2026-06-18부터 소비자 티어 서비스를 끝내고 Antigravity CLI로 넘어갔습니다.
- **비용은 작업당으로 비교하세요.** 토큰 단가로는 Opus 5.5가 Astra의 40%이지만(Astra 가격은 보도 기준, 미확인) 출력 토큰을 훨씬 많이 써서, 한 개인 테스트에서는 작업당 비용이 비슷했습니다(개인 테스트, n=1). 1920×1080 스크린샷 한 장은 2,691토큰으로, Opus 5.5 기준 약 $0.011입니다.
- **'실행자 + 어드바이저' 조합은 기대만큼 효과가 없습니다.** Opus 5.5에 Fable 5.1 어드바이저를 붙인 공식 측정 결과는 +1.7점(노이즈 수준)에 비용이 약 2.1배였습니다.
- AI+MCP로 만든 결과물 가운데 독립적으로 'AAA급' 판정을 받은 사례는 찾지 못했습니다. 모델 선택은 품질의 일부이고, 나머지는 에셋, 검증 루프, 사람의 마무리에서 나옵니다([사례 모음](../04_case_studies/01_case_studies.md)).

---

## 1. 이름 정리: '아스트라·페이블·오푸스 5.5'는 정확히 무엇인가

### 1-1. 사용자가 말한 세 모델

| 사용자가 말한 이름 | 정식 이름 (API ID) | 회사 | 출시 | API 단가 (입력/출력, 1M토큰당) | 컨텍스트 / 최대 출력 | 기본 effort | 확인 수준 |
|---|---|---|---|---|---|---|---|
| 아스트라 | **GPT-6 Astra** (`gpt-6-astra`) | OpenAI | 2026-09-03 (승인 조직 대상 제한 프리뷰로 시작해 순차 확대) | $10 / $50 **(미확인, 2차 보도)** | API 약 1.05M **(미확인)** · Codex 설정 272k(최대 872k) | Codex 기준 **low** | 모델 존재와 Codex 설정은 [openai/codex models.json](https://github.com/openai/codex/blob/main/codex-rs/models-manager/models.json)에서 확인. 출시일·가격·벤치마크는 [2차 기사](https://www.datacamp.com/blog/gpt-6-astra-vs-claude-fable-5-1)로만 확인 |
| 페이블 | **Claude Fable 5.1** (`claude-fable-5-1`) | Anthropic | 2026-09-01 | $10 / $50, 캐시 읽기 $0.25, 5분 캐시 쓰기 $12.50 | 1M / 128K | high | [공식 문서](https://platform.claude.com/docs/en/models/fable-5-1/overview)로 확인 |
| 오푸스 5.5 | **Claude Opus 5.5** (`claude-opus-5-5`) | Anthropic | 2026-09-22 | $4 / $20, 캐시 읽기 $0.20, 5분 캐시 쓰기 $5 | 1M / 128K (Batch는 300K 베타) | **medium** | [공식 문서](https://platform.claude.com/docs/en/models/opus-5-5/overview)로 확인 |

**GPT-6 Astra**
- Google DeepMind의 **Project Astra**와는 다른 제품입니다. Project Astra는 실시간 멀티모달 비서 연구 프로토타입이고, 일부 기능이 Gemini Live에 들어가 있을 뿐 3D MCP 작업과는 관계가 없습니다. 검색할 때는 'GPT-6 Astra Blender', 'Codex Astra'처럼 OpenAI 쪽 키워드를 붙이세요. 'GPT-5.6 Astra'라거나 'Astra 모델은 없다'고 쓴 글은 출시 전에 나온 낡은 SEO 글입니다.
- **effort 단계**: 기사에서는 API 기준 low~max 5단계로 소개합니다. 하지만 OpenAI가 직접 관리하는 [Codex models.json](https://github.com/openai/codex/blob/main/codex-rs/models-manager/models.json)을 보면 **low/medium/high/xhigh/max/ultra 6단계**이고(ultra는 'automatic task delegation'), **기본값은 low**입니다. Codex CLI **0.153.0 이상**이 필요하고, Fast 티어는 '2배 속도, 사용량 증가'로 표기되어 있습니다.
- 출시 데모에서는 씬 계획 → bpy 작성 → 백그라운드 렌더 → 이미지 확인 → 수정 루프로 Blender를 다뤘습니다. 광고된 3D 기능은 사진→3D, 스케치→3D, 분해도, 다부품 조립·리깅, 공간 추론입니다. 다만 이 기능들이 공식 기능인지 커뮤니티 데모인지는 1차 문서로 구분하지 못했습니다(미확인).

**Claude Fable 5.1**
- 모든 고객이 쓸 수 있는 Anthropic 최상위 모델입니다. adaptive thinking이 항상 켜져 있고, 응답 속도는 'Slower' 등급입니다. Claude Code는 **2.1.257 이상**이 필요합니다([CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md). 일부 자료에 나오는 2.1.255는 틀린 값). 은퇴는 2027-09-01 이후입니다.
- **Mythos 5.1**은 같은 모델을 제한된 곳에만 제공하는 버전입니다. [발표문](https://www.anthropic.com/claude-fable-and-mythos-5-1)은 사이버보안(CVP)·생명과학(LSVP) 검증 프로그램의 trusted access로, [모델 문서](https://platform.claude.com/docs/en/models/fable-5-1/overview)는 Project Glasswing 참가자 초대 전용으로 설명해 표현이 서로 다릅니다. 일반 사용자에게 '페이블'은 Fable 5.1입니다.

**Claude Opus 5.5**
- 장시간 에이전트 코딩과 지식 작업용 모델입니다. adaptive thinking이 항상 켜져 있어 끌 수 없고, **기본 effort가 medium**입니다(Opus 5는 high). 어려운 턴에서는 effort를 직접 올려야 합니다.
- Anthropic 제품 페이지는 'our best Opus model for vision and computer use'라고 소개합니다(3D·Blender 언급은 없음). [공식 문서](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5)는 Opus 5보다 **차트·다이어그램·스크린샷 판독**이 크게 좋아졌고, 위치 관계 이해와 여러 단계에 걸친 스크린샷 기반 컴퓨터 사용도 개선되었으며, 출력 속도가 30% 이상 빨라졌다고 설명합니다.
- Claude Code **2.1.280 이상**, Claude Desktop, claude.ai(유료 플랜), API, Bedrock, Vertex, Foundry에서 쓸 수 있고, 2026-09-22부터 [GitHub Copilot](https://github.blog/changelog/2026-09-22-claude-opus-5-5-is-now-available-in-github-copilot/)에서도 쓸 수 있습니다. 은퇴는 2027-09-22 이후입니다.

### 1-2. 함께 거론되는 모델

| 모델 | 출시 | API 단가 (1M토큰당) | 3D 관점의 요점 | 확인 수준 |
|---|---|---|---|---|
| GPT-6 Sol / GPT-6 Luna | 2026-09-22 (보도) | Sol $2/$10, Luna $0.10/$0.50 **(미확인)** | Astra 아래 저가 티어입니다. Codex models.json에서 존재를 확인했습니다(최소 클라이언트 0.155.0, Luna에는 ultra 단계가 없음). 같은 파일에 중간 티어 GPT-5.6 Terra도 있습니다 | 존재 확인, [가격·출시일은 보도](https://venturebeat.com/technology/openai-releases-gpt-6-sol-and-luna-models-slashing-api-costs-50-or-more)만 |
| Claude Sonnet 5 | 2026-06-30 | $2/$10 (2026-08-10부터 영구 가격) | 1M/128K, 기본 effort high, claude.ai Free/Pro의 기본 모델입니다 | [공식](https://www.anthropic.com/news/claude-sonnet-5) |
| Claude Haiku 4.5 | 현행 | $1/$5 | 200K/64K. 이미지는 표준 티어(긴 변 1568px)라 스크린샷 비평에 불리합니다 | [공식](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model) |
| Gemini 3.1 Pro | 2026-02-19 (BenchCAD 표에는 '2026-05'로 표기) | $2/$12 (입력 200k 초과 시 $4/$18) (보도) | Google Pro급 최신입니다. 3.5 Pro는 2026-05 I/O에서 발표만 되고 아직 나오지 않은 것으로 보입니다(보도는 미확인. 간접 근거로 Google 공식 [gemini-cli models.ts](https://github.com/google-gemini/gemini-cli/blob/main/packages/core/src/config/models.ts)에 Pro는 3.1까지만 있음) | 부분 확인 |
| Gemini 3.8 Flash | 2026-09-02 | $0.75/$3.75 (2026-12-31까지 프로모션, 보도) | 1M 컨텍스트, 약 305 tok/s로 싸고 빠른 비전 작업에 맞습니다 | 존재는 models.ts로 확인, 수치는 [보도](https://www.vellum.ai/blog/gemini-3-8-flash-benchmarks-explained) |
| xAI Grok 4.7 | 2026-09-21 | $2/$6 (200k 초과 시 $4/$12) **(미확인)** | 500K 컨텍스트, 텍스트·이미지 입력. 3D 공식 수치는 없습니다 | [docs.x.ai](https://docs.x.ai/developers/models) 미열람 |
| Kimi K3 (오픈웨이트) | 2026-07 | Kimi 플랫폼 과금 | 2.8T MoE(활성 104B), 1M 컨텍스트, 이미지·영상 입력. 개인이 호스팅하기엔 너무 크고 **커스텀 라이선스**입니다 | [GitHub README](https://github.com/MoonshotAI/Kimi-K3) 확인 |
| Qwen3.6-27B / Qwen3.8 | 2026-04~08 | 3.6은 Apache 2.0 오픈웨이트, 3.8-Max는 API $2/$6 | 로컬 실행 후보입니다. 체크포인트마다 비전 지원 여부가 다르니 확인이 필요합니다 | [부분 확인](https://huggingface.co/Qwen/Qwen3.6-27B) |
| DeepSeek V4.x / GLM-5.x | 2026-08~09 | 저가 | 싼 실행자로 거론되지만 3D 검증 자료는 거의 없습니다 | (신뢰도 낮음) |

---

## 2. 모델별 3D 강점과 약점

> 표기 규칙: (벤더 자체 보고) = 제조사 발표 수치, (개인 테스트, n=1) = 한 사람의 1회 비교, (제작자 보고) = 본인이 올린 데모, (미검증 주장) = 검증 단계에서 신뢰도 문제가 지적된 출처.

### 2-1. GPT-6 Astra: 공간·치수·재구성

| 구분 | 내용 |
|---|---|
| 강점 | **하드서피스·건축·사진/도면 재구성.** Hierarchy 에이전시와 Danny Stuart는 같은 시작 프롬프트로 Blender MCP 제작을 비교했고, '3D는 Astra가 큰 차이로 우세(렌더가 깔끔하고 손볼 곳이 적음), 소프트웨어 완성도와 오케스트레이션은 Fable 5.1'이라는 결론을 냈습니다([Hierarchy](https://hierarchy.ch/en/news/gpt-6-astra-vs-claude-fable-5-1), [Danny Stuart](https://dannystuart.substack.com/p/codex-astra-vs-claude-fable-battle)) (개인 테스트, n=1) |
| | 사례: 옛 증기기관차 그림 한 장을 편집 가능한 오브젝트 3,295개로 재구성했습니다([Tom Krcha](https://x.com/tomkrcha/status/2095756085890310311)) (제작자 보고). 출시 데모에서는 도면을 Blender 집으로 만든 뒤 걸어 다닐 수 있는 UE5 씬으로 옮겼습니다([Thomas Ricouard](https://x.com/Dimillian/status/2095596700815516004)) (모델 팀 데모라 선별된 결과일 수 있음) |
| | **토큰 효율**: 같은 단일 프롬프트 Blender 과제에서 출력 56.6k토큰으로, Opus 5.5의 199.6k보다 훨씬 적었습니다([Stefan 3D AI](https://x.com/Stefan_3D_AI/status/2102471841046786153)) (개인 테스트, n=1. 원문 미열람. 일반화 금지) |
| | GUI 그라운딩 ScreenSpot-Pro 92.7%([DataCamp](https://www.datacamp.com/blog/gpt-6-astra)) (벤더 자체 보고), Three.js 3D 장면 투표 Design Arena 3D 1위 1464([modelgrep](https://modelgrep.com/best/3d)) (신뢰도 낮음, 집계 사이트) |
| 약점 | **유기체·캐릭터**: Meshy 7과의 비교에서 '프리미티브 블록 근사' 수준에 머물렀습니다([HackerNoon](https://hackernoon.com/gpt-6-astra-vs-meshy-7-for-3d-creation-what-three-creator-workflows-reveal)). 반례로 토큰이 바닥날 때까지 자율 실행해 포토리얼 박쥐 모델을 만들었다는 보고가 있습니다([큐레이션 목록](https://github.com/magiccreator-ai/awesome-gpt-6-astra)) (제작자 보고). '항상 못한다'가 아니라 '비용 대비 비효율'로 이해하세요 |
| | **스타일 반복**(숲색 위주 팔레트)이 지적됩니다. **사진 재구성 때 원본에 없는 요소를 지어낸** 사례도 있습니다([AI매터스, 한국어](https://aimatters.co.kr/news-report/51830/)) |
| | **치수·방향 오류**: SketchUp MCP 농가 테스트에서 외관은 모델당 17~22분 만에 인상적으로 만들었지만, 인테리어 치수가 누락되고 문 여는 방향이 틀렸으며 Plus 주간 한도를 하루에 썼습니다([daily.dev 요약](https://daily.dev/posts/i-tested-gpt-astra-for-3d-modeling---this-is-getting-serious-to6zgaa2h), [원 영상](https://www.youtube.com/watch?v=SsBLhNgqTqQ)) (개인 테스트, n=1) |
| | 컴퓨터 사용 OSWorld 2.0은 72.6%(과제당 약 40분)입니다(벤더 자체 보고, partial/strict 조건 불명). 대략 네 번에 한 번은 실패한다는 뜻입니다. 시간·공간 동시 제약 과제(La Forge taille-3)에서는 88.1점으로 Opus 5.5(100)보다 낮았습니다 |
| 맡길 일 | 도면·사진·치수를 받아 매스와 가구를 배치하는 단계, 기계·하드서피스 재구성, 코드 CAD, 웹 3D(Three.js) |

### 2-2. Claude Opus 5.5: 장시간 씬 빌드·아트디렉션·정밀 제약

| 구분 | 내용 |
|---|---|
| 강점 | **공식 문서 기준 시각 판독 개선**: 밀집 차트의 값 읽기는 가장 낮은 effort에서도 Opus 5 최고 effort보다 정확했습니다(차트에 한정된 조건). 기술도면은 도구 없이도 effort를 올리면 좋아지고, PIL/OpenCV 기반 crop·zoom 도구를 쥐여 주면 밀집 이미지 정확도가 더 오릅니다([Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)) |
| | **독립 지표**: MCP 도구만으로 3D 기사를 조립하고 애니메이션하는 La Forge에서 6개 캠페인 평균 99.8, 가장 변별력이 큰 시간·공간 동시 제약 캠페인에서 100점이었습니다([ScoreIA 결과 데이터](https://github.com/drakkB/scoreia-forge-results)). 단, 채점기를 Claude Opus로 작성해 편향 가능성이 있다고 주최 측이 밝혔습니다. 사람 투표 Arena Code 보드에서는 1위(1827±18, 1,607표)입니다([2026-09-26 스냅샷](https://raw.githubusercontent.com/oolong-tea-2026/arena-ai-leaderboards/main/data/2026-09-26/code.json)). 이 보드는 3D 전용 지표가 아닙니다 |
| | **실사용 비교**: Stefan 3D AI 테스트에서 35분, 출력 199.6k토큰, 약 $13.3가 들었고 'Opus가 더 많은 요소를 동시에 다룬다'는 평을 받았습니다. 다만 모든 라운드에서 이긴 것은 아닙니다([Stefan](https://x.com/Stefan_3D_AI/status/2102471841046786153)) (개인 테스트, n=1). Nate Herk의 12개 과제 비교는 Opus 8 대 Astra 4였고, 대신 Astra가 총시간을 약 45%, 비용을 약 38% 덜 썼습니다([Nate Herk](https://x.com/nateherk/article/2102904721698599231)) (개인 테스트, n=1) |
| | 토큰 단가가 Astra의 40%입니다($4/$20) |
| 약점 | **출력 토큰이 많습니다.** 토큰 단가의 이점이 작업당 비용에서는 상쇄될 수 있습니다(위 Stefan 사례) |
| | **무인 루프 조기 종료**: 진행 상황을 보고한 뒤 텍스트로 턴을 끝내는 경향이 있어 무인 루프가 거기서 멈출 수 있습니다. 대응법은 7장에 있습니다 |
| | 발표문에 비전·공간·3D·CAD 벤치마크가 **하나도 없습니다**. Astra가 앞선 벤더 지표도 있습니다: Terminal-Bench-Science 0.1(58.7% 대 64.6%), AutomationBench(40.0% 대 41.4%)([Opus 5.5 발표](https://www.anthropic.com/claude-opus-5-5)) (벤더 자체 보고) |
| | **API 연동 함정**: forced `tool_choice`(any/tool)는 400 오류를 냅니다. 컴퓨터 사용은 `computer_toolset_20260801`만 받습니다(Claude API·Google Cloud 기준이고 Bedrock에서는 이전 버전도 동작). 도구 호출 사이의 텍스트는 thinking 블록으로 오므로 display 설정이 필요합니다([What's new](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5)) |
| 미검증 주장 | Brendan Jowett의 UE+Blender 게임 비교에서 'Opus가 전 항목 우위'였고 2시간 API 비용이 약 $60~70였다는 내용은 재게시 사이트([se7en.ws](https://se7en.ws/ai-claude-opus-5-5-surpasses-gpt-6-astra-in-unreal-engine-game-development/?lang=en))로만 확인했고 원본 영상은 보지 못했습니다. Higgsfield의 오브젝트 5,112개 신칸센(좌석 430개를 개별 오브젝트로)은 제품 홍보 게시물입니다([Higgsfield](https://x.com/higgsfield_ai/status/2102507018372436264)) (제작자 보고) |
| 맡길 일 | 장시간 씬 빌드, 룩뎁·조명·카메라 연출, 렌더 비평, 애니메이션 타이밍, 정밀 배치 실행 |

### 2-3. Claude Fable 5.1: 가장 어려운 계획·오케스트레이션

| 구분 | 내용 |
|---|---|
| 강점 | 최상위 계획 능력과 수 시간짜리 멀티스텝 작업. Terminal-Bench 4.0 55.8%, CursorBench 3.2.0 73.4%([발표](https://www.anthropic.com/claude-fable-and-mythos-5-1)) (벤더 자체 보고) |
| | Hierarchy·Danny Stuart 비교에서 뷰포트를 보며 스스로 고쳤고, Astra보다 빠르고 캐시 덕분에 저렴했으며 '아이디어가 더 다양하고 보기 좋다(better eye)'는 평을 받았습니다. 다만 소문자 마이크로카피를 과하게 넣는 버릇이 있었습니다 (개인 테스트, n=1) |
| | La Forge 평균 99.4, 시간·공간 제약 캠페인 97.7점, Arena Code 1751±10 |
| 약점 | 같은 비교에서 **순수 3D 품질은 Astra에 졌습니다** (개인 테스트, n=1). OpenAI 발표표에 실린 BenchCAD 'Fable 5.1 84.3% 대 Astra 95.9%'는 OpenAI 측이 측정한 값이고 Anthropic 발표에는 없습니다 (미확인) |
| | 느리고 비쌉니다($10/$50). Claude Pro에서는 크레딧으로 따로 과금되고 Free에서는 쓸 수 없습니다 |
| | OSWorld 2.0 partial이 자사 발표에서는 77.9%, Opus 5.5 발표에서는 80.7%로 서로 다르고, strict는 41.7%입니다 |
| 미검증 주장 | 부동산 주소 하나로 37초짜리 Blender 워크스루 영상을 만든 사례는 벤더의 콘텐츠 마케팅 글에서 나왔습니다([MindStudio](https://www.mindstudio.ai/blog/claude-fable-5-1-blender-video-generation)) |
| 맡길 일 | 코디네이터·어드바이저, 씬 전체와 파이프라인 설계, 툴·애드온 같은 소프트웨어 완성 |

### 2-4. 나머지 모델 한눈에

| 모델 | 3D에서 강한 점 | 약한 점 | 맡길 일 |
|---|---|---|---|
| Claude Sonnet 5 | 정적 조형 과제(La Forge maitre-2)는 100점 | 시간·공간 동시 제약 과제는 **19.5점**으로 급락. 어드바이저 패턴에서 조언 요청을 멈추는 경향이 관찰됨(저effort 조건. 과제에 따라 다름, 7-1 참고) | bpy 일괄 수정, 머티리얼 파라미터, 렌더 설정, 워커 |
| Claude Haiku 4.5 | 가장 쌈 | La Forge 평균 40.4, 저해상도 이미지 티어 | 에셋 검색, 네이밍, 파일 정리 서브에이전트. **공간 판단은 맡기지 말 것** |
| GPT-6 Sol | La Forge 평균 94.6, Arena Code 1681 | 시간·공간 제약 81.7 | Astra 아래에서 반복 bpy 수정, 파일·에셋 정리 |
| GPT-6 Luna | 가장 쌈 (가격 미확인) | 3D 자료 없음 | 분류, 네이밍 |
| Gemini 3.1 Pro | **도구 없이** 4뷰 렌더를 CAD 코드로 바꾸는 BenchCAD 공식 재채점 1위(IoU 0.289), Vision-QA·Code-QA도 1위([LEADERBOARD](https://github.com/BenchCAD/BenchCAD-main/blob/main/LEADERBOARD.md)) | 추가 시점이 주어지는 조건(3DHarnessBench Active Visual)에서 약하고 추가 시점이 오히려 해가 됨. Blender MCP 자료가 적고 무료 티어 레이트 리밋이 걸림돌 | CadQuery 코드 생성, 보조 비평 |
| Gemini 3.8 Flash | 싸고 빠름(약 305 tok/s), Terminal-Bench 2.1 90.8% (보도) | OSWorld 2.0 59.0% (비교 문장을 해석한 값, 신뢰도 낮음). Blender 테스트 드묾 | 대량 렌더·스크린샷 1차 검수, 에셋 분류, Three.js 프로토타입 |
| Grok 4.7 | La Forge 평균 96.2, Arena Code 1629 | 3D 공식 수치 없음, La Forge 블라인드 캠페인에서 흔들림 | 저가 조립·애니메이션 보조. Blender 연동은 [grok-blender-mcp](https://github.com/jaskirat1616/grok-blender-mcp)(Blender 4.2+, Safe Mode 기본, 변경마다 자동 undo, dry-run) |
| Kimi K3 | Design Arena 3D 2위 1417(신뢰도 낮음), Arena Code 1660, 3DHarnessBench 2군. 벤더 보고 OSWorld-Verified 84.8, MCPMark-Verified 94.5 | 최신 GUI 지표 OSWorld 2.0은 58.3으로 Fable 5(66.1)에 뒤짐. 커스텀 라이선스 | 호환 엔드포인트로 Claude Code·Cline·OpenCode에 붙인 저가 bpy 생성기 |
| Qwen3.6-27B / Qwen3.8 | Apache 2.0(3.6), 로컬 실행 가능. Qwen3.8-Max는 Arena Vision 2위(1302) | FreeCAD GUI 과제(CADWorld)에서 Qwen3.6 성공률 0~1.5% | 오프라인 초안·코드 생성. 최종 검수는 프런티어 모델 |
| DeepSeek V4.1 Flash / GLM-5.3 | Arena Code 1621 / 1619, La Forge 'deepseek-flash' 평균 91.3 | 3D 전용 검증이 거의 없고 라이선스 세부 미확인 | 대량 bpy 변형 생성 |

---

## 3. 작업 유형별 추천

> 아래 순위는 모두 **잠정적**입니다. 근거 대부분이 개인 테스트이거나 조건이 서로 다른 벤치마크입니다. 중요한 프로젝트라면 자기 과제 3~5개로 직접 A/B 테스트하세요(4-1의 해석 규칙 참고).

| 작업 유형 | 1순위 (effort) | 대안 | 근거 (신뢰도) | 반드시 같이 할 것 |
|---|---|---|---|---|
| **하드서피스·기계·건축 매스, 사진/도면 → 3D** | GPT-6 Astra (Codex, **high~xhigh**) | Opus 5.5 (high) | Hierarchy·Danny Stuart 비교 (n=1), 출시 데모, Tom Krcha 사례 (제작자 보고) | 치수·방향을 숫자로 주고, 완료 후 `dimensions`를 표로 보고하게 합니다. 사진에 없는 요소를 지어냈는지 대조합니다 |
| **파라메트릭 CAD (코드 CAD)** | Astra (도구 사용 BenchCAD 95.9%, 벤더 자체 보고·미확인) 또는 Opus 계열 (CADGenBench에서 Opus 5 0.677 > GPT-5.6 Sol 0.532, Astra는 미포함) | 도구 없이 한 번에 비전→CAD 코드: Gemini 3.1 Pro (BenchCAD 공식 0.289) | 측정 조건이 모두 달라 직접 비교 불가 | GUI 클릭보다 build123d/CadQuery + MCP를 쓰세요. FreeCAD GUI 과제 최고 성공률은 17.5%(전문가 87.0%)였고([CADWorld](https://arxiv.org/abs/2609.16251)), build123d-mcp를 붙이기만 해도 점수가 0.360에서 0.457로 올랐습니다([cadgenbench-build123d](https://github.com/pzfreo/cadgenbench-build123d)) |
| **유기체·캐릭터·조각** | **LLM 직접 모델링은 비권장.** 생성형 3D로 메시를 만들고 Astra나 Opus 5.5가 import → 스케일·피벗 정리 → 조립 → 리깅을 맡습니다 | — | Sculpt 모드는 MCP/Python 경로로 쓰기 어렵고 결과가 프리미티브 조합이 됩니다(조사 요약). Astra 대 Meshy 7 비교 | **한국: Hunyuan3D 계열 오픈웨이트는 한국이 라이선스 적용 지역 밖입니다.** 생성 도구 선택은 [04_ai_3d_generation](./04_ai_3d_generation.md)과 [10_assets_pipeline_licensing](./10_assets_pipeline_licensing.md)을 보세요 |
| **재질·셰이더 노드** | Opus 5.5 (high). 아트디렉션 감각이 낫다는 평이 다수 | Astra. 대량 파라미터 수정은 Sonnet 5 / GPT-6 Sol | 모델 간 **정량 비교가 없습니다.** 'Principled BSDF 수준은 되지만 복잡한 절차적 노드는 약하다'는 정성 평가뿐입니다. 참고로 BlenderGym(2025, GPT-4o) 머티리얼 과제의 광도 손실은 3.653으로 인간(0.629)의 약 6배였습니다 | 금지 목록형 아트디렉션(7-4 참고). **노드는 이름이 아니라 타입으로 찾게 하세요**(한국어 UI에서 이름이 바뀔 수 있음). [05_texturing_materials](./05_texturing_materials.md) |
| **배치·레이아웃** | 관계와 제약은 Astra (xhigh)나 Opus 5.5 (high~xhigh)가 만들고, **좌표는 솔버와 스크립트**가 정합니다 | — | BlenderGym에서 GPT-4o의 배치 오차(광도 손실 11.89)가 인간(0.423)의 약 28배였습니다([BlenderGym](https://blendergym.github.io/)). 제약 최적화를 쓴 LayoutVLM은 기준선보다 PSA가 40.8점 높았습니다([LayoutVLM](https://arxiv.org/html/2412.02193)) | [placement_utils.py](../03_playbooks/scripts/README.md)로 붙이고, `scene_audit.py`로 떠 있음·관통·치수 이탈을 검사합니다. [08_scene_layout_placement](./08_scene_layout_placement.md) |
| **렌더·스크린샷 비평** | Opus 5.5 (고해상도 이미지 + crop·zoom 도구) | Astra (ScreenSpot-Pro 92.7%, 벤더 자체 보고. [Roboflow Vision Evals](https://playground.roboflow.com/models/openai/gpt-6-astra) 1위 평균 86.6%). 1차 필터는 Gemini 3.8 Flash | 사람 투표 Arena Vision은 상위 30개 모델이 35점 안에 몰려 있어 변별력이 없습니다([vision.json](https://raw.githubusercontent.com/oolong-tea-2026/arena-ai-leaderboards/main/data/2026-09-26/vision.json)) | `review_views.py`로 위·정면·측면·3/4 뷰를 만듭니다. 추가 시점이 어떤 모델에는 오히려 해가 되므로 모델별로 A/B 테스트합니다([3DHarnessBench](https://arxiv.org/html/2609.06535v1)) |
| **장시간 에이전트 (수십 분~수 시간 씬 빌드)** | Opus 5.5 (Claude Code, high, `max_tokens` 128000) | Fable 5.1 (코디네이터·가장 어려운 계획), Astra (과제당 수십 분 단위) | La Forge, Stefan, Nate Herk 결과의 방향이 일치합니다 (각각 한계 있음) | 체크리스트 파일과 조기 종료 재지시(2~3회 한도). 정본은 Git의 bpy/YAML로 둡니다(7-3) |
| **애니메이션 타이밍·정밀 시간·공간 제약** | Opus 5.5 | Fable 5.1 | La Forge taille-3: Opus 5.5 100 / Fable 5.1 97.7 / Grok 4.7 90.4 / Astra 88.1 / Sol 81.7 / Sonnet 5 19.5 / Haiku 6.5 (편향 가능) | Sonnet·Haiku급 하위 티어는 쓰지 않습니다 |
| **대량 반복** (소품 200개 재질 수정, 네이밍, 렌더 설정) | Sonnet 5 / GPT-6 Sol (medium) | Haiku 4.5·GPT-6 Luna(분류·네이밍), DeepSeek·Kimi API | 단가 | 공간 판단은 맡기지 않고, 결과는 스크립트로 검사합니다 |
| **웹 3D (Three.js/R3F)** | Astra | Kimi K3, Fable 5.1 | Design Arena 3D (신뢰도 낮음) | — |
| **로컬·오프라인** | Qwen3.6-27B 등 + Ollama/vLLM + MCP 클라이언트(Cline, OpenCode) + [blender-open-mcp](https://github.com/dhakalnirajan/blender-open-mcp) | Kimi K3·DeepSeek (API) | 프런티어 모델과 격차가 큽니다 | **Ollama 자체는 MCP를 지원하지 않습니다.** MCP를 말하는 클라이언트를 따로 붙여야 합니다 |

### 3-1. 라우팅 예시 (조사에서 제안된 구성, 효과가 측정된 것은 아님)

```text
[계획·설계]   Fable 5.1 또는 Opus 5.5 (xhigh)   → scene.yaml (치수·에셋·카메라·합격 기준)
[매스·배치]   GPT-6 Astra (Codex, high~xhigh)   → build_scene.py, 관계 제약 → 솔버/placement_utils
[룩뎁·조명]   Opus 5.5 (Claude Code, high)       → 재질·조명·카메라·렌더 설정
[일괄 수정]   Sonnet 5 / GPT-6 Sol (medium)      → 소품 수백 개의 재질 파라미터, 네이밍
[1차 검수]    Gemini 3.8 Flash                   → 4방향 검토 렌더 대량 스크리닝
[최종 검수]   Opus 5.5 또는 Astra (high)         → scene_audit.py JSON + 렌더 비평 → 수정 지시
```

모델을 섞으면 비용이 늘고 캐시를 모델끼리 공유할 수 없습니다. **먼저 한 모델로 effort만 바꿔 보고**, 그래도 부족한 단계만 분리하세요(7-1 참고).

---

## 4. 벤치마크: 벤더 보고와 독립 평가를 나눠 읽기

### 4-1. 해석 규칙

1. **벤더 발표 수치와 독립 재채점 수치를 같은 열에 넣지 마세요.** 대표적인 예가 BenchCAD입니다. OpenAI가 발표한 'Astra 95.9%'는 도구(렌더→측정→수정)를 쓴 조건의 점수이고, 공식 리더보드는 도구 없이 채점한 0~1 척도 IoU입니다(최고 0.289, 벤더 보고 행을 넣어도 최고 0.384). 둘은 척도와 조건이 달라 비교할 수 없습니다. 척도가 맞지 않는 집계 사이트 값(예: 'Opus 5.5 0.730')은 근거로 쓰지 마세요.
2. **조건을 같이 적으세요**: effort, 도구 사용 여부, partial/strict, 과제당 소요 시간.
3. **아레나 Elo는 오차범위(±)가 겹치면 동률로 봅니다.** 출시 직후 모델은 표본이 적으니 1~2주 뒤에 다시 확인하세요.
4. **3D 전용 통제 벤치마크는 아직 없습니다.** La Forge가 가장 가깝지만 모델마다 하네스가 다르고 Gemini·Kimi·Qwen·GLM은 참가하지 않았습니다.
5. **Codex에서 Astra를 effort 지정 없이 돌린 비교는 무효입니다**(기본값 low).

### 4-2. 벤더 자체 보고 (측정 조건이 서로 다름)

| 지표 | Opus 5.5 | Fable 5.1 | GPT-6 Astra | 조건·주의 |
|---|---|---|---|---|
| OSWorld 2.0 (컴퓨터 사용) | 81.8% (partial, max effort) | 77.9% (자사 발표) / 80.7% (Opus 5.5 발표), strict 41.7% | 72.6% (OpenAI, partial/strict 불명, 과제당 약 40분) | 같은 표에서 비교된 적이 없습니다 |
| Terminal-Bench 4.0 | 66.4% | 55.8% | 57.9% (Anthropic 표에 인용된 OpenAI 보고치, high) | 일부 2차 기사의 57.7%는 Anthropic 표 기준 57.9%로 정정 |
| FrontierCode v1.1 | 54.4% (max) / 54.6% (medium) | — | 53.3% | Opus 5.5는 medium에서도 Astra 최고점보다 높고 비용은 약 1/5 |
| GDPval-AA | 1846 (v2.1) | 1735 (v2.1) / 1853 (v2, Fable 발표) | 1542 | 버전이 다릅니다 |
| HLE (도구 사용) | 67.7% | 65.0% | 57.2% | — |
| Terminal-Bench-Science 0.1 | 58.7% | 52.6% | **64.6%** | Astra 우세 |
| AutomationBench | 40.0% | 31.4% | **41.4%** | Astra 우세 |
| Chartography (도구 사용) | 89.0% | — | — | 시각 차트 인식 |
| ScreenSpot-Pro (GUI 그라운딩) | — | (Fable 5: 87.3%) | 92.7% | [집계 사이트](https://benchlm.ai/benchmarks/screenspot-pro) 경유 |
| BenchCAD (OpenAI 발표, 도구 사용) | — | 84.3% (OpenAI 측정) | 95.9% | **미확인.** 공식 리더보드와 척도가 다릅니다 |

출처: [Opus 5.5 발표](https://www.anthropic.com/claude-opus-5-5), [Fable 5.1 발표](https://www.anthropic.com/claude-fable-and-mythos-5-1), [DataCamp(Astra)](https://www.datacamp.com/blog/gpt-6-astra). **Opus 5.5 발표문에는 비전·3D·CAD 지표가 전혀 없습니다.**

### 4-3. 독립 평가 (3D 관련)

| 벤치마크 (시점) | 무엇을 재나 | 결과 | 한계 | 신뢰도 |
|---|---|---|---|---|
| [La Forge](https://github.com/drakkB/scoreia-forge-results) (2026-09-24) | MCP 도구만으로 3D 기사 조립·애니메이션, LLM 심판 없이 프로그램 채점([방법](https://scoreia.ai/forge/en/method/)) | 6개 캠페인 평균(조사 측 계산): Opus 5.5 99.8 / Fable 5.1 99.4 / Astra 97.9 / Grok 4.7 96.2 / Sol 94.6 / DeepSeek flash 91.3 / Sonnet 5 81.1 / Haiku 4.5 40.4 | 모델마다 하네스가 다름(Claude Code·Codex CLI·Grok CLI·API 루프), 심판을 Opus로 작성, 커미션당 최신 1회 시도만 반영. **모델링·텍스처 품질은 재지 않음** | 높음 (데이터 공개) |
| [Arena Code](https://github.com/oolong-tea-2026/arena-ai-leaderboards) (2026-09-25) | 웹·앱 코드 생성에 대한 사람 선호 | Opus 5.5 max 1827±18 / Astra max 1792±11 / Fable 5.1 max 1751±10 / Kimi K3 1660 / Grok 4.7 1629 / GLM-5.3 1619. Gemini는 상위 20위 밖 | 3D 전용 아님. Opus 5.5 표본 1,607표 | 높음 |
| Arena Vision (2026-09-13) | 이미지 이해 선호 | 상위 30개가 1310~1275 사이. Fable 5.1 1289±12, Astra 1284±17 | Opus 5.5 출시 전이고 변별력이 거의 없음 | 높음 |
| [Design Arena 3D](https://modelgrep.com/best/3d) | Three.js/WebGL 장면 코드 | Astra 1464 / Kimi K3 1417 / Fable 5.1 1415 | 집계 사이트 경유, Opus 5.5·투표 수 없음 | 낮음 |
| [BenchCAD 공식](https://github.com/BenchCAD/BenchCAD-main/blob/main/LEADERBOARD.md) (2026-06) | 4뷰 렌더 → CadQuery, 도구 없음, IoU×실행률 | Gemini 3.1 Pro 0.289 / Opus 4.7 0.269 / Sonnet 4.6 0.222 / GPT-5.3 0.179 (벤더 보고 행: Mythos 5 0.384) | Astra·Opus 5.5·Fable 5.1 미등재 | 높음 |
| [CADGenBench + build123d-mcp](https://raw.githubusercontent.com/pzfreo/cadgenbench-build123d/main/GEMINI_OPUS_GPT56_MCP_COMPARISON.md) | 코드 CAD 생성·편집 (STEP 유효성) | Opus 5 0.677 / GPT-5.6 Sol 0.532 / Gemini 3.7 Flash 0.508 (셋 다 81개 중 80개 유효) | 하네스·MCP 버전이 다른 제3자 단일 비교 | 중간 |
| [CADWorld](https://arxiv.org/abs/2609.16251) (2026-09) | FreeCAD GUI 장기 과제 200개 | GPT-5.4 17.5% / Opus 4.8 16.0% / **전문가 87.0%** | 최신 모델 미평가, 검색 요약 기반 | 중간 |
| [3DCodeBench](https://github.com/gaoypeng/3dcodebench) (2026-06) | Blender 5.0 bpy로 212개 카테고리 절차적 생성 | 멀티턴 오류 피드백으로 실행 가능률 0.69 → 0.97, 3DCodeArena Elo 1위 GPT-5.5(1163) | GPT-5.5 세대까지만 평가. 수치는 [논문](https://arxiv.org/abs/2606.01057) 요약 기준이고 GitHub README에는 없음 | 중간 |
| [3DHarnessBench](https://github.com/llada60/3DHarnessBench) (2026-09) | 3D 대상을 Blender 코드로 복원 (단일뷰 → 멀티뷰 → 능동 시점 → 함수 호출) | 접근 범위가 넓을수록 모든 모델이 개선. Opus 5가 능동 시점·완전 3D 상호작용 두 조건에서 1위 | Opus 5.5·Fable 5.1 미평가. Astra 포함 여부는 출처마다 다름 | 중간 |
| [BlenderGym](https://blendergym.github.io/) (2025) | 배치·조명·머티리얼 등 5개 편집 과제 | GPT-4o 배치 광도 손실 11.89 대 인간 0.423 | 2025년 모델에서 갱신이 멈춤 | 높음 (설계 참고용) |
| [MineBench](https://github.com/Ammaar-Alam/minebench/pull/152) | 복셀 건축 | Astra Pro 15/15 완료, 프롬프트당 평균 25분 53.5초, 총 $34.71 | 순위·점수 미확인 | 중간 |
| Blender AI Arena | Blender 결과물 블라인드 투표 | 5자 동률(1,687표)이라는 요약과 Opus 5.5 1897±79라는 요약이 **서로 충돌** | 운영 주체 불명, 상용 제품(3D-Agent) 참가 | 낮음 (미검증 주장) |

공간지능 벤치마크 모음 EASI에는 GPT-6 Astra 평가 요청 이슈([#39](https://github.com/EvolvingLMMs-Lab/EASI/issues/39), 2026-09-12)만 있고 결과는 없습니다.

---

## 5. MCP 클라이언트 비교

### 5-1. 비교표

| 클라이언트 | 로컬 stdio | 도구 결과 이미지 → 모델 | 도구 수 | 3D 적합도 | 주의 |
|---|---|---|---|---|---|
| **Claude Code** (CLI, Desktop의 Code 탭) | O (stdio·HTTP·SSE·WebSocket) | O, 인라인 전달(PNG/JPEG/GIF/WebP) | tool search 기본 활성(v2.1.274~)이라 도구가 많아도 대응. `ANTHROPIC_BASE_URL`로 다른 모델을 붙이면 비활성 | **매우 높음**: 서브에이전트·스킬·훅, 긴 세션 | Claude 모델 전용. CLI 컴퓨터 사용은 macOS·Pro/Max·연구 프리뷰 한정이고 Team/Enterprise, 서드파티 제공자, `-p` 비대화형에서는 불가([computer use](https://code.claude.com/docs/en/computer-use)) |
| **Claude Desktop** | O (공식 커넥터) | O | — | 비개발자에게 가장 쉬움: Customize > Connectors > Blender | 컴퓨터 사용은 macOS·Windows 지원. 장시간 자율 루프와 Git 재현성은 Claude Code가 나음 |
| claude.ai 웹 | X (원격 커넥터만) | O | — | 클라우드형 SketchUp 커넥터는 사용 가능 | 메시지당 이미지 20장 |
| **Codex** CLI·앱·IDE, ChatGPT 데스크톱(Codex·Work 모드) | O (`~/.codex/config.toml` 공유) | O (조사 요약 기준) | `enabled_tools`/`disabled_tools`로 조절 | **매우 높음**: Astra를 쓰는 가장 깔끔한 경로 | Astra는 0.153.0+, Sol/Luna는 0.155.0+. Windows 네이티브 앱 컴퓨터 사용 버그([#42214](https://github.com/openai/codex/issues/42214), 2026-09-02 기준 open) |
| ChatGPT 웹 채팅 (개발자 모드) | **X** (원격 MCP: SSE, Streamable HTTP, OAuth만) | — | — | 낮음 | 로컬 Blender는 터널이 필요합니다([OpenAI Help](https://help.openai.com/en/articles/12584461-developer-mode-apps-and-full-mcp-connectors-in-chatgpt-beta)) |
| Cursor | O (`.cursor/mcp.json`) | O: direct/embedded/linked 모두 전달([MCPJam 보고](https://www.mcpjam.com/clients/cursor/tool-testing)) | **활성 도구가 약 40개를 넘으면 일부가 조용히 빠짐**([mcpverdict](https://mcpverdict.com/mcp/clients/cursor/)) | 중간: 여러 모델을 한 IDE에서 전환하며 비교하기 좋음 | 커뮤니티 Blender 서버 하나가 도구 36개라 다른 서버를 같이 켜면 한도를 넘습니다 |
| VS Code + GitHub Copilot | O | 미확인 | — | 중간 | MCP GA는 1.102(2025-07), [MCP Apps](https://code.visualstudio.com/blogs/2026/01/26/mcp-apps-support)는 2026-01 |
| Windsurf / Cline / OpenCode | O | **미확인** | — | Cline·OpenCode는 로컬 모델 백엔드와 결합하기 좋음 | 이미지 결과 처리를 1차 문서로 확인하지 못함 |
| Gemini CLI → Antigravity CLI/IDE | O (`settings.json`의 `mcpServers` / Antigravity는 `mcp_config.json`) | 미확인 | — | 중간: Gemini 3.8 Flash를 싸게 씀 | Gemini CLI는 2026-06-18부터 무료·Google AI Pro·Ultra 요청 처리를 중단했습니다(2026-05-19 공지). Code Assist Standard/Enterprise, Google Cloud, 유료 API 키는 계속 지원됩니다([공지](https://github.com/google-gemini/gemini-cli/discussions/27274)). 옛 튜토리얼 상당수가 낡았습니다 |
| Grok Build / Grok CLI | O | grok-blender-mcp가 뷰포트 스크린샷 제공 | — | 낮음~중간 | [Grok Build 플러그인](https://github.com/franjorub/grok-build-blender-plugin)은 공식 Blender Lab 서버를 git 태그 v1.0.0으로 고정합니다 |

### 5-2. Blender 서버 등록: 먼저 알아야 할 것

- **`uvx blender-mcp`나 `uvx mcp-for-blender`는 공식 서버가 아닙니다.** 둘 다 커뮤니티 표준인 ahujasid 'MCP for Blender'를 실행합니다([PyPI mcp-for-blender](https://pypi.org/project/mcp-for-blender/), [PyPI blender-mcp](https://pypi.org/project/blender-mcp/)). 신규 설치는 `mcp-for-blender`를 권장합니다.
- Claude 공식 **Blender 커넥터**는 Blender 개발자 조직인 Blender Lab이 만든 별도 서버입니다. 애드온이 필요하고, 애드온 manifest의 `blender_version_min`이 5.1.0이라 Blender 5.1 이상에서 돌아갑니다. Claude Desktop 밖에서 쓸 때는 git 소스에서 설치합니다([커넥터 페이지](https://claude.com/connectors/blender). 커넥터 페이지 자체에는 Blender 버전 요구가 적혀 있지 않음).
- **두 서버 모두 localhost:9876을 쓰므로 하나만 켜세요.** 서버별 기능 차이, 텔레메트리, `BLENDER_MCP_SAFE_MODE`는 [02_blender_mcp](./02_blender_mcp.md)에서 다룹니다.

**Claude Code** (`.mcp.json`, 프로젝트 공유용):

```json
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["mcp-for-blender"],
      "env": { "DISABLE_TELEMETRY": "true", "BLENDER_MCP_SAFE_MODE": "1" },
      "timeout": 600000
    }
  }
}
```

한 줄로 등록할 때는 `claude mcp add blender -- uvx mcp-for-blender`를 씁니다(팀 공유는 `--scope project`). `"timeout"`의 의미는 5-3의 주의 상자를 보세요.

**공식 Blender Lab 서버** (Claude Desktop 외 클라이언트에서 쓸 때. 태그는 조사 시점 2차 자료 기준이고, 커넥터 표기는 v1.0.1이므로 최신 태그를 확인하세요):

```bash
uvx --from "git+https://projects.blender.org/lab/blender_mcp.git@v1.0.0#subdirectory=mcp" blender-mcp
```

첫 실행 때는 git 빌드와 의존성(약 41개) 다운로드 때문에 기본 MCP 시작 타임아웃을 넘길 수 있습니다. Claude Code라면 `MCP_TIMEOUT=120000 claude`처럼 시작 타임아웃(ms)을 늘려 실행하세요. 등록 명령과 `~/.claude.json` 예시는 [빠른 시작 1.5절](../03_playbooks/01_quickstart_setup.md)에 있습니다.

**Codex** (`~/.codex/config.toml`, **effort를 꼭 지정**):

```toml
model = "gpt-6-astra"
model_reasoning_effort = "high"   # 지정하지 않으면 Codex 기본값 low

[mcp_servers.blender]
command = "uvx"
args = ["mcp-for-blender"]
env = { DISABLE_TELEMETRY = "true", BLENDER_MCP_SAFE_MODE = "1" }
startup_timeout_sec = 30
tool_timeout_sec = 600
```

Codex 설정 키 이름과 기본값은 Codex 문서의 검색 요약에서 가져왔고 원문은 열람하지 못했습니다. 오류가 나면 공식 문서로 확인하세요. 프로젝트별 설정은 `.codex/config.toml`에 두며, 신뢰된 프로젝트에서만 적용됩니다([Codex MCP 문서](https://developers.openai.com/codex/mcp)). 등록 후 `codex mcp list`로 확인합니다.

### 5-3. 3D 작업에 맞춘 한도·타임아웃

기본값은 3D 작업에 맞지 않습니다. 렌더는 60초를 넘기 쉽고, 씬 덤프는 출력 한도에 걸려 잘립니다.

| 항목 | 기본값 | 3D 권장 | 설정 위치 |
|---|---|---|---|
| Claude Code MCP 출력 한도 | 25,000토큰 (10,000에서 경고) | 50,000 | 환경변수 `MAX_MCP_OUTPUT_TOKENS` |
| Claude Code 도구 타임아웃 (호출당 절대 한도) | `MCP_TOOL_TIMEOUT` 미설정 시 약 28시간 | 서버별로 정하려면 600000 (ms, 10분) | `.mcp.json`의 `"timeout"` (진행 알림으로 연장되지 않는 절대 한도. 1000 이상이면 유휴 타임아웃의 하한도 겸함, v2.1.203+) |
| Claude Code 서버 시작 타임아웃 | — | 공식 서버 첫 실행 때 120000 (ms) 정도 | 환경변수 `MCP_TIMEOUT` (예: `MCP_TIMEOUT=120000 claude`) |
| Claude Code 도구 유휴 타임아웃 (응답·진행 알림이 없을 때) | stdio **30분**, HTTP·SSE·WebSocket·claude.ai 커넥터 **5분** | 진행 출력 없이 오래 걸리는 렌더·베이크가 있으면 조정 | `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT` (ms, `0`이면 끔) |
| Codex 서버 시작 타임아웃 | 10초 (이번 조사에서 재확인 못 함) | 30 | `startup_timeout_sec` |
| Codex 도구 타임아웃 | 60초 (이번 조사에서 재확인 못 함) | 600 | `tool_timeout_sec` |
| 커뮤니티 Blender 서버 소켓 타임아웃 | 180초 | 클라이언트 값을 늘려도 서버 쪽 한도가 남으므로, 긴 렌더는 `blender -b` 헤드리스로 분리 | 서버 내부 |
| Cursor 활성 도구 | 약 40개 | 40개 미만 유지 | 설정 |
| Gemini CLI 원격 서버 | `httpUrl`=Streamable HTTP, `url`=구형 SSE | Blender 서버는 기본이 stdio(`command`/`args`)라서 **원격 HTTP로 띄운 경우에만** 해당 | `settings.json` ([문서](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md)) |

출처: [Claude Code MCP 문서](https://code.claude.com/docs/en/mcp), [Codex MCP 문서](https://developers.openai.com/codex/mcp).

> **주의**: stdio 서버에 `"timeout": 600000`을 넣으면 한도가 늘어나는 것이 아니라 **기본 약 28시간이던 절대 한도가 10분으로 줄어듭니다.** 이 값은 HTTP 서버(예: UE 5.8 공식 MCP)에서 기본 5분 유휴 타임아웃과 60초 첫 응답 대기를 늘릴 때 효과가 있습니다. 커뮤니티 Blender 서버는 어차피 서버 쪽 소켓 타임아웃(180초)이 먼저 걸리므로, 긴 렌더는 헤드리스로 분리하세요.

---

## 6. 비용·요금제·스크린샷 토큰

### 6-1. API 단가 (1M토큰당, 2026-09-27 기준)

| 모델 | 입력 | 출력 | 캐시 읽기 | 그 밖에 | 확인 수준 |
|---|---|---|---|---|---|
| Claude Fable 5.1 | $10 | $50 | $0.25 | 5분 캐시 쓰기 $12.50 | 공식 |
| Claude Opus 5.5 | $4 | $20 | $0.20 | 5분 캐시 쓰기 $5, Batch 50%, Fast mode $8/$40(최대 2.5배 속도) | 공식. Fast mode는 문서상 API 전용 연구 프리뷰, 발표문은 Claude Code·Claude Platform에서도 사용 가능하다고 설명 |
| Claude Sonnet 5 | $2 | $10 | — | — | 공식 |
| Claude Haiku 4.5 | $1 | $5 | — | — | 공식 |
| GPT-6 Astra | $10 | $50 | $1 (캐시 입력) | Batch/Flex 50%, Fast 2배. '입력 272k 초과 시 요청 전체를 $20/$75로 재과금'한다는 보도 | **미확인** (재과금 보도는 신뢰도 낮은 출처. Codex 설정의 컨텍스트가 272k인 점은 확인) |
| GPT-6 Sol / Luna | $2 / $0.10 | $10 / $0.50 | — | 영구 가격이라는 보도 | **미확인** |
| Gemini 3.1 Pro | $2 | $12 | — | 입력 200k 초과 시 $4/$18 | 보도 |
| Gemini 3.8 Flash | $0.75 | $3.75 | — | 2026-12-31까지 프로모션 | 보도 |
| Grok 4.7 | $2 | $6 | $0.50 | 200k 초과 시 $4/$12 | **미확인** |
| Qwen3.8-Max (API) | $2 | $6 | — | — | 보도 |

### 6-2. 구독 요금제에서 쓸 때

- **Claude**([Fable 요금제 안내](https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan)): Fable 5.1은 **Free에서 쓸 수 없고**, Pro와 Team/Enterprise 표준 좌석은 **크레딧으로 따로 과금**됩니다. Max와 Team/Enterprise 프리미엄 좌석은 **주간 한도의 50%까지 포함**되고, 사용량 기반 Enterprise는 API 단가로 과금됩니다. Fable 5를 Pro에 포함하던 프로모션은 2026-07-19에 끝났고 Fable 5.1은 대상이 아니었습니다. Opus 5.5는 유료 플랜에서 씁니다.
- **ChatGPT/Codex**: 'Plus에서 Astra는 채팅이 아닌 Work와 Codex에서만 제한적으로 제공되고, 채팅에서는 GPT-6 Pro라는 이름으로 Pro·Business·Enterprise에 제공된다'는 보도가 있지만 **미확인**입니다. Codex models.json에는 Astra의 사용 가능 플랜으로 free·go·plus·pro·business·enterprise가 모두 들어 있어 Codex 경로는 더 넓게 열려 있을 수 있습니다. 플랜별 사용량은 [OpenAI Help](https://help.openai.com/en/articles/20001516-managing-usage-with-gpt-6-astra-in-work-and-codex)에서 직접 확인하세요.
- **실제 소모 사례**: SketchUp에서 Astra로 건축 모델 3종을 만든 테스트는 **Plus 주간 한도를 하루에** 썼습니다 (개인 테스트, n=1). Claude + Blender MCP로 도넛 튜토리얼을 2시간 반복한 테스트는 월 $200 Max 플랜 세션 한도의 약 60%를 썼다고 합니다([MindStudio](https://www.mindstudio.ai/blog/claude-blender-mcp-60-percent-tokens-donut-test-results)) (미검증 주장, 벤더 블로그, 모델 버전 미기재).

### 6-3. 작업당 비용 사례 (모두 참고값)

| 사례 | 모델 | 시간 | 토큰 | 비용 | 신뢰도 |
|---|---|---|---|---|---|
| 단일 프롬프트 절차적 Blender 10초 샷 ([Stefan](https://x.com/Stefan_3D_AI/status/2102471841046786153)) | Opus 5.5 / Astra (max effort로 맞춤) | 35분 / 28분 | 출력 199.6k / 56.6k | 약 $13.3 / 약 $14.5 | 개인 테스트, n=1, 원문 미열람 |
| 12개 실사용 과제 ([Nate Herk](https://x.com/nateherk/article/2102904721698599231)) | Opus 5.5 대 Astra | Astra가 약 45% 짧음 | — | Astra가 약 38% 저렴 | 개인 테스트, n=1 |
| MineBench 복셀 건축 15개 ([PR #152](https://github.com/Ammaar-Alam/minebench/pull/152)) | Astra Pro (max, 출력 상한 128k) | 프롬프트당 평균 25분 53.5초 | — | 총 $34.71 | GitHub PR 직접 확인 |
| CADGenBench 81개 과제 전체 ([비교 문서](https://raw.githubusercontent.com/pzfreo/cadgenbench-build123d/main/GEMINI_OPUS_GPT56_MCP_COMPARISON.md)) | Opus 5 (xhigh) | — | GPT-5.6 Sol보다 44% 많음 | API 환산 약 $724.77 | 제3자 비교, 방향성 참고용 |

**교훈**: 토큰 단가가 싸다고 작업당 비용이 싼 것은 아닙니다. 새 파이프라인을 짤 때는 대표 과제 하나를 두 모델로 끝까지 돌려서 **시간·토큰·비용·수정 횟수**를 기록한 다음 결정하세요.

### 6-4. 스크린샷 토큰 계산 (Claude)

Claude 4.7 이후 모델(Sonnet 5, Opus 5.5, Fable 5.1)은 **고해상도 이미지 티어**(긴 변 최대 2576px, 최대 4,784 비주얼 토큰)를 씁니다. 토큰 수는 **⌈가로/28⌉ × ⌈세로/28⌉**입니다([Vision 문서](https://platform.claude.com/docs/en/build-with-claude/vision)).

| 이미지 | 토큰 | Opus 5.5 입력 비용 | Fable 5.1 입력 비용 |
|---|---|---|---|
| 768×768 (검토 렌더용 저해상도) | 784 | 약 $0.003 | 약 $0.008 |
| 1092×1092 | 1,521 | 약 $0.006 | 약 $0.015 |
| 1920×1080 (뷰포트 캡처) | 2,691 | **약 $0.011** | 약 $0.027 |
| 2576×1449 (16:9, 상한) | 4,784 | 약 $0.019 | 약 $0.048 |
| 4방향 검토 1회 (768px × 4장) | 3,136 | 약 $0.013 | 약 $0.031 |

(768px·4방향·2576px 행은 문서의 계산식으로 직접 계산한 값입니다.)

- **한 요청에 이미지가 20장을 넘으면 각 이미지가 2000px 이하**여야 합니다. claude.ai는 메시지당 20장까지입니다.
- 컴퓨터 사용 도구 결과로 돌려주는 스크린샷이 한도를 넘으면 **자동 축소되지 않고 거부**됩니다.
- Claude Code 컴퓨터 사용은 스크린샷을 자동으로 줄입니다(16인치 Retina 3456×2234 → 약 1372×887).
- Haiku 4.5는 표준 티어(긴 변 1568px)라 세부 비평에 불리합니다.
- **운용 팁**: 평소 반복 검토는 768~1092px로 보내고, 비교가 필요한 시점만 고해상도로 보내세요. 긴 세션에서는 Files API의 `file_id`로 참조해 요청 크기를 줄입니다.
- OpenAI·Google 모델의 이미지 토큰 규칙은 이번 조사에서 확인하지 않았습니다.

---

## 7. 모델 조합과 하네스: 실제 효과가 확인된 것과 아닌 것

### 7-1. 검증 결과 요약

| 조합·방법 | 측정 결과 | 판정 |
|---|---|---|
| **Opus 5.5(high) 실행자 + Fable 5.1 어드바이저** | Anthropic 내부 에이전트 코딩 벤치마크에서 90.1%, 시도당 $2.92. Opus 5.5 단독(high)보다 **+1.7점**으로 실행 간 노이즈 경계 수준이고, **비용은 약 2.1배**([공식 문서](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)) | **기본 구성으로 권하지 않습니다.** '비용 대비 효율적'이라는 일부 요약은 문서 취지와 반대입니다. 쓰더라도 구도·공간 배치 같은 어려운 결정 시점에만 쓰고, 실행자가 실제로 조언을 요청하도록(과제당 2~3회) 지시해야 효과가 납니다 |
| Sonnet 5 실행자 + 어드바이저 | SWE-bench Pro 저effort 조건에서는 조언 요청을 멈췄지만, DeepSWE에서는 계속 요청해 23점이 올랐습니다 | 과제에 따라 다릅니다 |
| **한 모델에서 effort만 조절** (Opus 5.5, SWE-bench Pro, high 기준) | low: 약 8점 하락, 비용 약 1/3 / medium: 약 2.5점 하락, 비용 약 70% / xhigh: 1.4점 상승, 비용 2.5배 | **여러 모델을 섞기 전에 먼저 시도하세요.** 반복 수정 턴은 medium, 레이아웃·치수 설계 턴만 xhigh |
| Astra effort | xhigh가 medium보다 토큰을 1.76~2.52배 씁니다([2차 분석](https://trilogyai.substack.com/p/astra-reasoning-effort-token-usage)). Max 53분 대 Medium 25분 사례([MindStudio](https://www.mindstudio.ai/blog/gpt-6-astra-video-game-development))도 있습니다 (벤더 블로그, 미검증) | 기본은 high. 비교 실험은 같은 단계로 고정합니다 |
| **생성형 3D + LLM 조립** (Astra + Tripo P2.0, Grok 4.6 + Meshy) | 제작자 보고 사례만 있고 정량 비교는 없습니다([큐레이션 목록](https://github.com/magiccreator-ai/awesome-gpt-6-astra)) | 유기체의 사실상 표준 분업 |
| 작업별 라우팅 (3-1) | 측정 없음 | 개인 테스트들의 방향과는 맞지만 검증되지 않았습니다 |
| **하네스 개선 (모델 고정)** | 멀티턴 오류 피드백으로 실행 가능률 0.69 → 0.97(3DCodeBench, 논문 요약 기준으로 미확인). build123d-mcp 연결로 0.360 → 0.457, 유효율 88% → 100%. 생성·검증 역할을 번갈아 하는 VIGA는 원샷 대비 BlenderGym +35.32%, BlenderBench +124.70%([VIGA](https://arxiv.org/abs/2601.11109)). BlenderGym은 예산이 클수록 검증에 연산을 더 쓰는 쪽이 유리하다고 보고했습니다 | **가장 먼저 할 일.** 모델을 바꾸는 것보다 효과가 큽니다 |

### 7-2. Claude 장시간 세션 설정 (Opus 5.5 / Fable 5.1)

- **effort 명시**: Opus 5.5는 medium에서 시작해 필요한 턴만 올립니다. Claude API에서는 **per-message effort(베타)**로 캐시를 깨지 않고 턴마다 effort를 바꿀 수 있습니다.
- **긴 턴**: `max_tokens`를 128000으로 둡니다. 긴 컨텍스트는 **compaction on demand(베타)**로 압축할 수 있습니다([What's new](https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5)).
- **조기 종료 방지**: `TODO.md`에 '모델링 → UV → 머티리얼 → 조명 → 카메라 → 렌더'를 적어 두고, 턴이 끝났는데 열린 항목이 남아 있으면 "Your task list still has open items: ... Continue with them."을 자동으로 넣습니다(2~3회 한도). 공식 'Unattended agentic runs' 시스템 프롬프트도 함께 씁니다([Prompting 가이드](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)).
- **밀집 이미지**: 와이어프레임, 노드 그래프, 기술도면에는 crop·zoom 도구를 줍니다. 예: "렌더를 crop해서 문손잡이 높이를 픽셀로 재고, 기준 치수와 비교하라."(기준 치수는 [05_reference_dimensions](../03_playbooks/05_reference_dimensions.md)에서 숫자로 넣기)
- 규칙 파일과 스킬은 [templates/CLAUDE.md](../03_playbooks/templates/CLAUDE.md), [blender-aaa-scene 스킬](../03_playbooks/templates/skills/blender-aaa-scene/SKILL.md)을 가져다 쓰세요.

### 7-3. 모델·클라이언트를 바꿔도 이어지게: 정본은 Git에

- **정본(source of truth)은 Git의 bpy/YAML로 두고, MCP 라이브 세션은 점검용으로만 씁니다.** 라이브 씬에 쌓인 변경은 재현하기 어렵고, 컨텍스트가 길어지면 품질도 떨어집니다. 이렇게 해 두면 Codex(Astra)와 Claude Code(Opus 5.5)를 오가며 같은 씬을 이어서 작업할 수 있습니다.
- 예: `scene.yaml`(치수·카메라·에셋) → `build_scene.py` → `blender -b -P build_scene.py`로 클린 빌드 → `render.png`와 `validation.json` 생성 → 에이전트가 수정하면 커밋. 합격 기준 파일이나 검증 코드가 바뀌면 롤백합니다.
- 참고 템플릿:
  - [Codex-and-Blender](https://github.com/danielsobrado/Codex-and-Blender) (MIT, Codex 0.153.0+): YAML/JSON 구성 → 결정론적 bpy → Blender CLI 클린 빌드. MCP는 '비정본 점검 레이어'이고, `acceptance.yaml`로 합격 기준을 고정하며, 보호 파일이 바뀌면 롤백합니다.
  - [claude-3d-harness](https://github.com/MAX-786/claude-3d-harness) (MIT): Claude Code 스킬 58개(라이브러리 5개), 프로필 3개(fast/standard/cinematic), 워크플로 6개. 두 번 수정해도 남는 결함은 세 번째로 추측하지 않고 refinement 스킬로 넘깁니다(일부 요약에 나오는 '최대 4회 수정'은 README에 없음).
  - [3DHarnessBench](https://github.com/llada60/3DHarnessBench): 멀티뷰·능동 시점·완전 3D 상호작용 설정용 SKILL.md, MCP 어댑터, 뷰포트 전용 서비스를 그대로 가져다 쓸 수 있습니다.
- 이 저장소의 테스트 완료 스크립트([scripts/README.md](../03_playbooks/scripts/README.md), Blender 4.2.23 LTS·5.0.1에서 테스트 통과)를 빌드 스크립트에 넣어, 어떤 모델이 만들었든 같은 기준으로 검사하세요.
  - `scene_audit.py`: 떠 있음, 관통, 스케일 미적용, 치수 범위 이탈을 JSON으로 보고
  - `placement_utils.py`: 바닥에 붙이기, 표면 위에 올리기, 벽에 붙이기, 간격 검사
  - `review_views.py`: 위·정면·측면·3/4 검토 렌더
- **회귀 테스트**: 모델이나 프롬프트를 바꿀 때 La Forge 공개 MCP 엔드포인트(`https://scoreia.ai/forge/mcp`)에 클라이언트를 연결하면 결정적으로 채점되는 비교를 할 수 있습니다. 단, 채점기 편향 가능성은 감안하세요.

### 7-4. 아트디렉션 프롬프트: 막연한 지시 대신 금지 목록

Opus 5.5 공식 가이드는 '제너릭한 AI 느낌을 피하라' 같은 막연한 지시가 기본 스타일 하나를 다른 기본 스타일로 바꿀 뿐이라고 설명합니다. Astra 결과물에서도 비슷한 팔레트가 반복된다는 비판이 있습니다.

```text
금지: 채도 높은 숲색·청록 팔레트, 균일한 3점 조명, 정면 대칭 구도,
      모든 표면 roughness 0.5 동일.
따를 것: 레퍼런스 3장의 색온도(실내 3200K, 창광 5600K).
완료 후: 각 오브젝트 dimensions와 바닥 접지(min z = 0) 여부를 표로 보고.
```

첫 결과를 보고 금지 목록을 늘려 갑니다. 더 많은 템플릿은 [03_prompt_templates](../03_playbooks/03_prompt_templates.md)에 있습니다.

---

## 8. 한국 사용자 체크포인트

> **한국 사용자 주의** 아래 항목은 해외 튜토리얼에 거의 나오지 않지만 한국에서는 결과나 법적 위험을 바꿉니다.

1. **생성형 3D 라이선스**: Tencent Hunyuan3D 계열 오픈웨이트(2.0/2.1/Omni/Part, HY-World, HY-Motion, BPT)의 라이선스는 적용 지역에서 **EU·영국·대한민국을 제외**하고 출력물 사용도 제한합니다. 한국에서 로컬로 쓰는 것은 라이선스 범위 밖입니다. Tencent Cloud API 약관은 별개이고 원문을 확인하지 못했습니다. 커뮤니티 Blender MCP 서버의 Hunyuan3D 연동을 쓸 때도 어느 경로(로컬 가중치인지 API인지)인지 확인하세요 → [10_assets_pipeline_licensing](./10_assets_pipeline_licensing.md)
2. **오픈웨이트 LLM 라이선스**: Kimi K3는 커스텀 라이선스입니다. 매출 2천만 달러를 넘는 MaaS 운영자는 별도 계약이 필요하고, MAU 1억 또는 월매출 2천만 달러를 넘으면 'Kimi K3' 표기 의무가 생깁니다. Qwen3.6 오픈웨이트는 Apache 2.0입니다. Arena Code 12위에 오른 Tencent의 오픈 모델 hy4-preview는 이번 조사에서 라이선스를 확인하지 않았으니, 같은 회사의 Hunyuan3D 전례를 감안해 LICENSE 파일의 지역 조항부터 보세요.
3. **한국어 UI와 노드 이름**: Blender를 한국어 UI로 쓰면 현지화 때문에 노드 이름이 바뀌어, 모델이 이름으로 노드를 찾는 스크립트가 깨질 수 있습니다. 프롬프트에 '노드는 이름이 아니라 타입으로 찾을 것'을 넣으세요. 이 저장소의 스크립트는 이미 타입으로 찾습니다 → [05_texturing_materials](./05_texturing_materials.md)
4. **Windows 사용자**: Claude Code CLI의 컴퓨터 사용은 macOS 전용이고, Claude Desktop은 Windows도 지원합니다. Codex에는 Windows 네이티브 앱 컴퓨터 사용 버그(#42214)가 열려 있습니다. MCP로 Blender를 다루는 데는 컴퓨터 사용이 필요 없으므로 MCP 경로를 우선하세요.
5. **치수 규격**: 모델에게 가구·공간 치수를 맡기지 말고 한국 규격 치수를 숫자로 넣으세요 → [05_reference_dimensions](../03_playbooks/05_reference_dimensions.md)
6. **한국어 자료**: [AI매터스, 'GPT-6 아스트라 vs 클로드 페이블 5.1, 성능표만 보면 놓치는 차이'](https://aimatters.co.kr/news-report/51830/)는 컴퓨터 사용 성공률이 실제로 무엇을 뜻하는지와 사진 재구성 환각을 짚습니다. 더 많은 자료는 [02_korean_resources](../04_case_studies/02_korean_resources.md)에 있습니다.

---

## 흔한 실수와 해결

| 실수 | 증상 | 해결 |
|---|---|---|
| Codex에서 Astra를 effort 지정 없이 사용 | 결과가 기대보다 거칠고, 다른 모델과 비교하면 Astra가 불리하게 나옴 | `model_reasoning_effort = "high"`(레이아웃·치수 턴은 xhigh) |
| Opus 5.5를 기본값(medium) 그대로 사용 | 어려운 배치·구도 판단이 얕음 | 어려운 턴만 high/xhigh로. API는 per-message effort(베타) |
| `uvx blender-mcp`를 공식 서버로 착각 | 공식 커넥터 문서와 도구 구성이 다름 | 커뮤니티판임을 알고 쓰거나, 공식 서버는 git 소스에서 설치 |
| 공식·커뮤니티 Blender 서버를 동시에 켬 | 연결 실패, 엉뚱한 서버가 응답 | 둘 다 localhost:9876이므로 하나만 켬 |
| ChatGPT 웹 채팅에 로컬 Blender를 붙이려 함 | 연결 불가 | Codex CLI/앱 또는 ChatGPT 데스크톱의 Codex·Work 모드 사용 |
| Cursor에 MCP 서버를 여러 개 켬 | 일부 도구가 조용히 사라짐 | 활성 도구 40개 미만. 커뮤니티 Blender 서버만으로 36개 |
| 렌더를 MCP 도구로 오래 돌림 | 60초(Codex)·180초(커뮤니티 서버 소켓)·유휴 30분(Claude Code stdio. HTTP 서버는 5분)에서 끊김 | 타임아웃을 늘리고, 긴 렌더는 `blender -b` 헤드리스로 분리 |
| 큰 씬 덤프를 그대로 반환 | 출력이 잘려 모델이 씬을 잘못 이해함 | `MAX_MCP_OUTPUT_TOKENS=50000`, 덤프는 요약·필터링해서 반환 |
| 벤더 수치를 한 표에 섞어 순위를 매김 | 'Astra 95.9% 대 Gemini 0.289' 같은 무의미한 비교 | 벤더 보고와 독립 재채점을 다른 열에, 조건 병기 |
| 아레나 1위를 절대 순위로 해석 | 표본이 적은 신규 모델 순위가 1~2주 뒤 뒤집힘 | 오차범위가 겹치면 동률, 1~2주 뒤 재확인 |
| 스크린샷을 늘 원본 해상도로 보냄 | 토큰 비용 급증, 20장 초과 시 오류 | 반복 검토는 768~1092px, 필요한 시점만 고해상도 |
| 무인 루프를 걸어 두고 자리를 비움 (Opus 5.5) | 진행 보고 후 턴이 끝나 작업이 멈춤 | 체크리스트 + 미완료 항목 자동 재지시(2~3회) |
| Claude API에서 `tool_choice: any/tool` 강제 | Opus 5.5·Fable 5.1에서 400 오류 | `auto` + 프롬프트로 도구 지시 |
| '제너릭한 AI 느낌을 피하라'고만 지시 | 다른 제너릭 스타일로 바뀔 뿐 | 금지 목록 + 레퍼런스 수치(색온도 등) |
| 렌더가 마젠타(분홍)로 나오는데 컨텍스트 탓으로 봄 | 원인을 못 찾음 | Blender에서 마젠타는 보통 이미지 텍스처 경로 누락입니다. 누락 파일 검사 후 절대경로로 재연결 |
| 사진·도면 재구성 결과를 그대로 믿음 | 원본에 없는 요소, 틀린 문 방향 | 원본과 대조, 치수·회전축을 표로 보고하게 한 뒤 검사 |
| 로컬 모델용으로 Ollama만 설치 | MCP 도구가 안 보임 | Ollama는 MCP를 말하지 않음. Cline·OpenCode 같은 MCP 클라이언트를 따로 연결 |
| Gemini CLI 옛 튜토리얼을 그대로 따라 함 | 무료·Pro 계정에서 동작 안 함 | 2026-06-18 이후 Antigravity CLI로 전환, 또는 유료 API 키·Code Assist |

---

## 관련 문서

- [컴퓨터 유즈 vs MCP vs 스크립트](12_computer_use_and_other_methods.md): 컴퓨터 유즈가 모델링에 정말 나은지, 방법 8가지 비교
- [00 목적·범위](../00_purpose/purpose_and_scope.md) · [조사 방법·신뢰도 정책](../01_research/research_method.md) · [출처 카탈로그](../01_research/sources_catalog.md) · [검증 로그](../01_research/verification_log.md)
- [02 Blender MCP 생태계](./02_blender_mcp.md): 공식 Blender Lab 서버와 ahujasid MCP for Blender 비교, 보안, API 함정
- [03 기타 DCC·CAD·게임엔진 MCP](./03_other_mcp_dcc_cad_engines.md): SketchUp·Fusion 커넥터, Unreal·Unity 등
- [04 AI 3D 생성](./04_ai_3d_generation.md): 유기체·캐릭터를 맡길 생성 모델
- [05 텍스처링·재질](./05_texturing_materials.md) · [06 라이팅·렌더·아트디렉션](./06_lighting_rendering_art_direction.md)
- [07 오브젝트·가구·조형 모델링](./07_modeling_objects_furniture_sculpture.md) · [08 배치·레이아웃](./08_scene_layout_placement.md)
- [09 에이전트 워크플로·프롬프팅](./09_agent_workflow_prompting.md): 시각 피드백 루프, 토큰·비용, 보안
- [10 에셋·파이프라인·라이선스](./10_assets_pipeline_licensing.md) · [11 학술 연구](./11_research_papers.md)
- [빠른 시작: 설치·연결](../03_playbooks/01_quickstart_setup.md) · [AAA 제작 플레이북](../03_playbooks/02_aaa_production_playbook.md) · [프롬프트 템플릿](../03_playbooks/03_prompt_templates.md) · [품질 체크리스트](../03_playbooks/04_quality_checklists.md) · [실측 치수 기준표](../03_playbooks/05_reference_dimensions.md)
- [보조 스크립트(scene_audit / placement_utils / review_views)](../03_playbooks/scripts/README.md)
- [사례 모음](../04_case_studies/01_case_studies.md) · [한국어 자료](../04_case_studies/02_korean_resources.md)

## 원자료

- [`01_research/raw/01_ai-models.research.json`](../01_research/raw/01_ai-models.research.json): 프런티어 모델·클라이언트·벤치마크 1차 조사
- [`01_research/raw/01_ai-models.verify.json`](../01_research/raw/01_ai-models.verify.json): 독립 검증(정정: Astra effort 6단계·기본 low, Terminal-Bench 57.9%, Fable 5.1 Claude Code 2.1.257, `uvx blender-mcp`는 커뮤니티판, 어드바이저 효과 해석 등)
- [`01_research/raw/G6_benchmarks_models.gap.json`](../01_research/raw/G6_benchmarks_models.gap.json): 3D·CAD·공간지능 벤치마크 보완 조사(La Forge, Arena 스냅샷, CADGenBench, CADWorld 등)
