# 컴퓨터 유즈 vs MCP vs 스크립트 — AI가 3D 도구를 다루는 모든 방법

> 기준일: 2026-09-27 · "컴퓨터 유즈로 직접 모델링하는 게 낫다"는 말이 맞는지 근거로 따져 보고, AI가 Blender·CAD·엔진을 다루는 방법 8가지를 언제 무엇을 쓸지 정리합니다.

## 핵심 요약

- **컴퓨터 유즈(Computer Use)** 는 AI가 스크린샷을 보고 마우스·키보드를 직접 움직여 프로그램을 사람처럼 조작하는 방식입니다. Claude(Claude Code·Desktop), OpenAI(Codex·API), 오픈소스 UI-TARS 등이 지원합니다.
- **"컴퓨터 유즈가 직접 모델링하는 게 낫다"는 말은 대체로 오해입니다.** 이 말은 GPT-6 Astra 출시 직후 "Astra의 Blender 실력은 새 컴퓨터 유즈 능력의 부산물"이라는 반응([Kyle Jeong, X](https://x.com/kylejeong/status/2097077446663372966), 신뢰도 낮음)에서 퍼진 것으로 보입니다. 그런데 OpenAI 공식 아키비즈 사례에서 Astra는 **bpy 스크립트를 Blender 백그라운드 모드로 실행해서 모델링**했고, 컴퓨터 유즈는 **렌더 이미지와 Blender 화면을 확인하는 데** 썼습니다([OpenAI 개발자 블로그](https://developers.openai.com/blog/architectural-visualization-with-astra), 검색 요약으로 확인).
- **벤더들도 "화면 조작은 마지막 수단"이라고 말합니다.** Claude Code 문서는 컴퓨터 유즈를 "가장 넓고 가장 느린 방법"이라 하고, MCP → Bash → 브라우저 → 컴퓨터 유즈 순서로 고른다고 명시합니다([Claude Code 문서](https://code.claude.com/docs/en/computer-use)). OpenAI도 GPT-6 Astra에는 화면 클릭조차 PyAutoGUI 코드로 하게 하는 code execution 방식을 권장합니다([OpenAI 가이드](https://developers.openai.com/api/docs/guides/tools-computer-use), 검색 요약).
- **정량 근거**:
  - FreeCAD를 화면 클릭으로 다루는 CAD 벤치마크(CADWorld)에서 최고 에이전트는 **17.5%**, 전문가는 87%였습니다([CADWorld](https://arxiv.org/abs/2609.16251)).
  - 18개 앱 440과제에서 화면 전용 에이전트는 59.1%였습니다. 명령 기반(CLI) 에이전트는 원래 스킬(CLI-Anything)만으로 48.2%였지만, 스킬을 보강하자 **69.3%로 역전**했습니다([GUI vs CLI](https://arxiv.org/abs/2606.24551)). 단, 69.3%는 검증기가 본 요구사항에 맞춰 빠진 스킬을 고친 조건입니다.
  - 화면과 CLI를 섞어 써야 하는 114과제(WeaveBench, 3D 포함)에서는 최고가 41.2%였고, **화면만 또는 CLI만 쓰게 하면 3.5% 이하**였습니다([WeaveBench](https://arxiv.org/abs/2606.09426)). 한쪽만 고집하지 말고 섞어 써야 한다는 근거입니다.
- **컴퓨터 유즈가 정말 나은 곳도 있습니다**: API·스크립트가 없는 프로그램, UI에서만 되는 기능, 실제 화면을 보고 확인해야 하는 경우입니다. 스컬프트 모드는 MCP로 접근이 안 된다는 평가가 있어서([MindStudio](https://www.mindstudio.ai/blog/claude-blender-mcp-real-world-performance)) 컴퓨터 유즈가 이론상 유일한 경로입니다. 하지만 **컴퓨터 유즈로 스컬프트해서 좋은 결과를 냈다는 검증된 사례는 찾지 못했습니다.** 유기체는 이미지→3D 생성기로 가는 편이 현실적입니다.
- **결론(권장 구성)**:
  - 만드는 것: **스크립트·MCP**
  - 확인과 GUI 전용 조작: **컴퓨터 유즈**
  - 유기체·조형: **생성형 3D**
  - 형태·배치 검사: **숫자 검사 스크립트**(이 저장소 `scene_audit.py`, `building_audit.py`)
  
  여러 Astra 가이드도 "MCP + 컴퓨터 유즈" 혼합을 권한다고 합니다([kingy.ai](https://kingy.ai/blog/blender-openai-astra-complete-guide/), [neural4d](https://blog.neural4d.com/user-guide/gpt-6-astra-blender-mcp/)) (미확인: 원문 열람 불가).

---

## 1. 컴퓨터 유즈란

AI가 **화면 스크린샷 → 판단 → 마우스 이동·클릭·드래그·키 입력 → 다시 스크린샷**을 반복하며 프로그램을 조작합니다. 사람이 쓰는 것과 똑같은 UI를 쓰기 때문에 API가 없는 프로그램도 다룰 수 있는 대신, 화면 좌표를 정확히 찍어야 하고(그라운딩) 단계마다 이미지 토큰이 듭니다.

| 제품 | 지원 환경 | 켜는 법 | 비고 |
|---|---|---|---|
| **Claude Code (CLI)** | macOS 전용, Pro/Max(Team·Enterprise 불가), claude.ai 로그인 필요(Bedrock 등 서드파티 경유 불가), 연구 프리뷰 | 대화형 세션에서 `/mcp` → `computer-use` 활성화(프로젝트별 유지) → macOS 접근성·화면 기록 권한 허용 | 비대화형(`-p`) 불가. 앱마다 세션 승인. 브라우저는 보기 전용, 터미널·IDE는 클릭 전용. 다른 앱은 숨김. `Esc`로 즉시 중단. 스크린샷은 자동 축소(예: 3456×2234 → 약 1372×887) ([문서](https://code.claude.com/docs/en/computer-use)) |
| **Claude Desktop** | macOS·Windows | 설정 > 일반에서 켬 | 같은 엔진, 거부 앱 목록 설정 가능 ([문서](https://code.claude.com/docs/en/computer-use)) |
| **OpenAI Codex** | Codex 데스크톱 앱(Windows 11 지원은 2026-05-29 추가). CLI 지원 여부는 미확인 | 앱 설정 > Plugins에서 Computer Use 설치 → 프롬프트에 `@Computer`나 앱 이름 | 로컬 또는 ChatGPT 모바일 앱으로 감독 ([AI타임스](https://www.aitimes.com/news/articleView.html?idxno=211135), [PCWorld](https://www.pcworld.com/article/3154677/openai-codex-can-finally-control-windows-11-pcs-on-its-own.html)) |
| **OpenAI API** | 직접 구현 | `computer` 도구 또는 **code execution**(PyAutoGUI·Playwright) | Astra에는 code execution 권장(`computer` 도구는 대안), VM·컨테이너 격리 권장 ([가이드](https://developers.openai.com/api/docs/guides/tools-computer-use), [개인 실습 저장소](https://github.com/piyo123/learning-computer-use-with-gpt-6-astra)) |
| **UI-TARS Desktop** (ByteDance) | 오픈소스(Apache 2.0), 로컬·원격 | 앱 설치 | 스크린샷을 보고 마우스·키보드로 조작하는 네이티브 GUI 에이전트. 구동 모델은 UI-TARS(오픈 가중치)와 Seed-1.5-VL/1.6 ([GitHub](https://github.com/bytedance/ui-tars-desktop)) |

벤더 발표 기준 컴퓨터 유즈 점수(OSWorld 2.0)는 Opus 5.5 81.8%(partial, max effort), GPT-6 Astra 72.6%(과제당 약 40분)입니다(**벤더 자체 보고**. 두 수치는 서로 다른 발표에서 나왔고 Anthropic 표에는 Astra가 없어 직접 비교 금지. 자세한 내용은 [AI 모델 가이드](01_ai_models_and_clients.md)). 참고로 2024년 원본 OSWorld(369과제)에서는 최고 모델이 12.24%(사람 72.36%)였습니다([OSWorld](https://arxiv.org/abs/2404.07972)). OSWorld 2.0은 과제와 채점 방식이 다른 별도 벤치마크라 두 숫자를 이어 붙여 비교할 수는 없고, 발전 방향만 참고하세요. 또 둘 다 일반 데스크톱 과제 점수이고, **3D·CAD처럼 정밀한 화면 조작은 여전히 약합니다**(아래 3절).

## 2. AI가 3D 도구를 다루는 8가지 방법

| # | 방법 | AI가 하는 일 | 정확도·재현성 | 속도·비용 | 잘하는 것 | 약한 것 |
|---|---|---|---|---|---|---|
| 1 | **헤드리스 스크립트** (`blender -b --python`) | bpy 코드를 쓰고 백그라운드 실행 → 렌더 파일을 봄 | 매우 높음(스크립트가 원본으로 남음) | 빠르고 쌈 | 건축·가구·하드서피스, 반복 빌드, CI | 실시간 상호작용, GUI 전용 기능 |
| 2 | **MCP (실행 중인 Blender·엔진)** | 장면 조회·코드 실행·스크린샷을 도구로 호출 | 높음(구조화된 결과) | 빠름 | 대화형 편집, 에셋 가져오기, 조회 | 긴 작업 타임아웃, 스컬프트 모드 접근 불가 |
| 3 | **컴퓨터 유즈 (화면 조작)** | 스크린샷 보고 클릭·드래그 | 낮음~중간(좌표 오차, 장기 작업 실패) | 가장 느리고 비쌈 | API 없는 앱, UI 전용 기능, 눈으로 확인 | 정밀 치수, 긴 빌드, 테마·버전 변화 |
| 4 | **하이브리드** (1·2 + 3) | 코드로 만들고 화면으로 확인 | 높음 | 중간 | 대부분의 실무 | 설정이 복잡 |
| 5 | **에이전트용 CLI 래퍼** (CLI-Anything 등) | 앱 기능을 JSON 명령으로 호출 | 높음 | 빠름 | GUI 대신 안정적인 명령 표면 | 스킬 커버리지 밖 기능 |
| 6 | **가드된 하네스·플러그인** (codex-blender-plugin 등) | 허용된 구조화 명령만 실행 | 높음, 안전 | 빠름 | 되돌릴 수 없는 작업 승인, 사람이 중간에 개입 | 허용 목록 밖 작업 |
| 7 | **생성형 3D** (이미지·텍스트 → 메시) | 생성기 호출, 후처리 코드 작성 | 형태는 좋고 치수·토폴로지는 약함 | 크레딧 과금 | 유기체·조형·캐릭터 베이스 | 정밀 치수, 부품 구조(파트 분리 필요) |
| 8 | **파라메트릭 CAD 코드** (build123d·CadQuery·OpenSCAD) | 치수 기반 코드 | 최고(mm 단위) | 빠름 | 가구 부품·제품·조인트 | 자유 곡면·유기체 |

- 5번 [CLI-Anything](https://github.com/HKUDS/CLI-Anything)은 Blender(테스트 208개)·GIMP(107개) 같은 앱의 코드베이스에서 에이전트용 CLI를 자동으로 만들어 주는 Claude Code 플러그인입니다. 실제 백엔드(Blender는 bpy)를 쓰고 모든 명령에 `--json` 출력이 있습니다. 스크린샷·클릭 기반 자동화의 취약성(테마·버전이 바뀌면 버튼 위치가 달라져 깨지는 문제 등)을 피하려는 방식입니다. 3절 GUI vs CLI 논문의 CLI 기준선(48.2%)이 바로 이 스킬 층이었습니다.
- 6번 [codex-blender-plugin](https://github.com/partme-ai/codex-blender-plugin)은 임의 Python을 기본으로 막고(`expert_python` 승인 필요), 삭제·덮어쓰기처럼 되돌릴 수 없는 작업은 1회용 승인 토큰을 요구합니다. Blender 데이터는 메인 스레드에서만 바꿉니다. 사람이 중간에 손으로 고치면 재개할 때 장면을 새로 조회한 뒤 이어서 작업합니다.
- 1·2번은 [Blender MCP 가이드](02_blender_mcp.md), 3D 생성은 [AI 3D 생성 가이드](04_ai_3d_generation.md), CAD 코드는 [모델링 가이드](07_modeling_objects_furniture_sculpture.md)를 보세요.

## 3. 근거: 화면 조작 vs 코드·도구 호출

| 연구·벤치마크 | 무엇을 쟀나 | 결과 | 시사점 |
|---|---|---|---|
| [GUI vs CLI](https://arxiv.org/abs/2606.24551) (2026-06) | 18개 앱·12개 범주 440과제, 같은 목표·검증기 | 화면 전용 최고 59.1%(GPT-5.4), CLI 원래 스킬(CLI-Anything) 48.2%(Codex GPT-5.5) → 검증기 기반으로 스킬을 고치면 **69.3%** | CLI의 병목은 모델보다 스킬 커버리지. 채우면 화면 조작보다 낫다(단, 69.3%는 검증기가 본 요구사항으로 스킬을 고친 조건). 화면 조작은 긴 작업에서 정확한 조작(그라운딩)이 병목 |
| [CADWorld](https://arxiv.org/abs/2609.16251) (2026-09) | FreeCAD를 화면으로 조작하는 200과제(11개 범주) | 최고 **17.5%** vs 전문가 87% | 약한 에이전트는 유효한 산출물조차 못 만들고, 강한 에이전트일수록 구조·형상·작업 과정 요건에서 실패(그럴듯하지만 틀린 결과). 주된 실패는 같은 동작 반복 루프와 공간 방향 착오. 정밀 CAD를 클릭으로 하는 건 아직 무리 |
| [WeaveBench](https://arxiv.org/abs/2606.09426) (2026-06) | 화면+CLI 혼합 114과제(8개 분야, Spatial/3D 포함) | 최고 41.2%(Claude Opus 4.7 + Claude Code). **화면만·CLI만 쓰면 3.5% 이하** | 섞어 써야 풀림. 결과만 채점하면 과대평가(가짜 스크린샷·렌더, 하드코딩 지표 등). 과정·산출물 검사 필요 |
| [3DHarnessBench](https://arxiv.org/abs/2609.06535) (2026-09) | Blender MCP로 3D를 코드로 복원(100개), 단일뷰·멀티뷰·능동 시점·전체 3D 상호작용 4개 조건 | 함수 호출 접근이 풍부해지면 모든 모델이 크게 개선되지만 개선 폭은 모델마다 크게 다름. 최고 Uni3D 0.927(멀티뷰와 전체 3D 상호작용 조건) | **보는 것(시점)과 조회 도구를 늘리는 것**이 대체로 품질을 올림. 단 단계마다 항상 오르는 것은 아니고 추가 시점이 해가 되는 모델도 있어 모델별 확인 필요 |
| [VideoCAD](https://arxiv.org/abs/2505.24838) | CAD UI 조작 영상 약 4만 1천 개(정확한 개수 미확인) | GPT-4.1의 돌출 횟수 추정 47%, 프레임 순서 36% | CAD 화면의 시간·3D 추론이 약함 |

**해석**: "화면을 사람처럼 쓰면 더 잘한다"는 직관과 달리, 3D·CAD에서는 **구조화된 명령(코드·MCP·CLI)으로 만들고 화면은 확인에 쓰는 쪽**이 정확하고 싸고 재현됩니다. 컴퓨터 유즈의 가치는 '만들기'보다 **'보기'와 'API가 없는 곳 메우기'** 에 있습니다.

## 4. 컴퓨터 유즈가 실제로 나은 경우

| 상황 | 이유 | 예 |
|---|---|---|
| API·스크립트가 없는 프로그램 | 다른 방법이 없음 | 일부 상용 렌더러·뷰어, 사내 툴, 웹 에셋 스토어 |
| UI에서만 되는 기능 | 스크립트로 노출 안 됨 | Blender 스컬프트 브러시 스트로크(MCP 불가 평가), 일부 애드온 패널 |
| **실제 화면을 보고 확인** | 렌더 파일이 아니라 앱 상태 자체를 봐야 할 때 | 뷰포트 표시 문제, 애드온 UI 오류, 노드 연결 상태 육안 확인 |
| 사람 작업 흐름 재현·튜토리얼 | 사람이 보는 그대로 기록 | 조작 과정을 보여 주는 영상 |
| 여러 앱 사이 복사·붙여넣기 | 앱 간 연결 API가 없을 때 | 이미지 편집기 → Blender 텍스처 |

**컴퓨터 유즈가 불리한 경우**: 치수가 중요한 가구·건축, 수백 개 오브젝트 배치, 반복 빌드, 긴 작업(한 과제에 수십 분), 비용 제한이 있는 작업, Blender 테마·버전이 자주 바뀌는 환경.

## 5. 스컬프트·유기체는 어떻게

- MCP·bpy로는 스컬프트 브러시를 쓸 수 없다는 평가가 있습니다([MindStudio](https://www.mindstudio.ai/blog/claude-blender-mcp-real-world-performance)). 컴퓨터 유즈로 브러시를 드래그하는 것은 원리상 가능하지만, **좋은 결과를 냈다는 검증된 사례를 찾지 못했습니다**(조사 공백).
- Astra 가이드들도 캐릭터·유기체는 Blender 지오메트리로 억지로 만들지 말고 **이미지→3D·텍스트→3D 생성기로 베이스를 만들라**고 권한다고 합니다([kingy.ai](https://kingy.ai/blog/blender-openai-astra-complete-guide/)) (미확인). 레퍼런스 이미지로 드래곤을 만든 사례는 헤드리스 Blender를 썼다고 합니다([Sarang Borude, X](https://x.com/doomdave/status/2096335588727349434), 신뢰도 낮음) (미확인).
- 권장 순서: 생성기(Rodin·Tripo·Meshy·TRELLIS.2)로 형태 → 리메시·UV·베이크를 스크립트로 → 필요하면 **사람이** 스컬프트로 다듬기 → 컴퓨터 유즈는 결과 확인. 생성된 메시의 특정 부위를 텍스트·이미지로 고치는 연구(ES3D, 3DEditFormer, EditFlow3D 등)도 나오고 있습니다([ES3D](https://arxiv.org/pdf/2608.15749), [EditFlow3D](https://arxiv.org/pdf/2608.03179), 연구 단계) (미확인: 논문 내용 미열람).

## 6. 권장 구성 (실전)

```
1. 계획        : 스펙·치수·관계 제약을 JSON으로 (모델: 추론 강한 모델)
2. 만들기      : 헤드리스 bpy 스크립트 또는 MCP execute_blender_code (코드가 원본)
3. 에셋        : 라이브러리 검색 / 생성형 3D (유기체·조형)
4. 숫자 검사   : scene_audit.py (떠 있음·관통·치수·천장) + building_audit.py (문·창·방·동선·백룸 위험도)
5. 눈 검사     : review_views.py 4방향 렌더 → AI 비평
6. 화면 확인   : 컴퓨터 유즈로 실제 Blender 화면·UI 상태 확인, API 없는 조작만 화면으로
7. 사람 마무리 : 미감·스컬프트·최종 판단
```

- 이 저장소의 검사 스크립트: [scripts/README](../03_playbooks/scripts/README.md).
- 비용 감각: 1920×1080 스크린샷 한 장은 Opus 5.5 기준 2,691토큰(약 $0.011)입니다. 컴퓨터 유즈는 동작마다 스크린샷을 찍으므로, 같은 작업을 코드로 하면 호출 수와 이미지 토큰이 크게 줄어듭니다([AI 모델 가이드](01_ai_models_and_clients.md) 6절).

## 7. 안전

- 컴퓨터 유즈는 샌드박스가 아니라 **실제 데스크톱**에서 동작합니다. Claude Code는 앱별 승인, 터미널을 스크린샷에서 제외, `Esc` 전역 중단, 세션 잠금을 둡니다([문서](https://code.claude.com/docs/en/computer-use)).
- OpenAI는 생성된 코드를 개인 작업 PC에서 돌리지 말고 네트워크·파일시스템·자격 증명을 제한한 VM·컨테이너에서 실행하라고 권합니다([가이드](https://developers.openai.com/api/docs/guides/tools-computer-use), 검색 요약).
- 화면에 보이는 웹페이지·문서의 지시문이 AI를 속이는 프롬프트 인젝션에 주의하세요. 작업 전에 `.blend`를 저장하세요.

## 흔한 실수와 해결

| 실수 | 증상 | 해결 |
|---|---|---|
| 컴퓨터 유즈로 가구·건축을 처음부터 클릭으로 모델링 | 느리고 비싸고 치수가 틀림, 중간에 실패 | 스크립트·MCP로 만들고 화면은 확인에만 |
| 화면만 보고 "잘 됐다"고 판단 | 떠 있음·관통·틈을 놓침, 가짜 성공 | `scene_audit.py`·`building_audit.py` 숫자 검사를 먼저 |
| 컴퓨터 유즈로 스컬프트 기대 | 형태가 뭉개지거나 진행이 안 됨 | 생성형 3D + 리메시, 스컬프트는 사람 |
| Blender 테마·레이아웃을 바꾼 뒤 화면 자동화가 깨짐 | 버튼을 못 찾음 | 기본 테마·영어 UI 고정, 가능한 기능은 CLI·MCP로 |
| 개인 PC에서 권한을 다 열고 실행 | 파일·계정 위험 | 앱별 승인, 격리 VM, 작업 전 저장 |

## 관련 문서

- [AI 모델 가이드](01_ai_models_and_clients.md): 모델별 컴퓨터 유즈 점수·비용, 클라이언트 비교
- [Blender MCP 가이드](02_blender_mcp.md): MCP·헤드리스 설치와 운영
- [AI 3D 생성 가이드](04_ai_3d_generation.md): 유기체·조형 생성
- [에이전트 워크플로 가이드](09_agent_workflow_prompting.md): 시각 피드백 루프
- [보조 스크립트](../03_playbooks/scripts/README.md): 숫자 검사(`scene_audit.py`, `building_audit.py`), 4방향 검토 렌더

## 원자료

- `01_research/raw/G7_computer_use.gap.json`: 이번 조사(웹 검색 16회 + Claude Code 공식 문서 원문 1건). 대부분 검색 결과 요약 기반이며 arXiv·openai.com 원문은 네트워크 정책으로 열지 못했습니다.
- `01_research/raw/G7_computer_use.verify.json`: 독립 사실 검증 25건(확인 17, 부분 5, 반박 0, 미확인 3). Claude Code 문서·GitHub 저장소·Anthropic 발표·Claude 비전 문서는 원문으로, 논문과 OpenAI 문서는 검색 요약으로 확인했습니다.
- `01_research/raw/G6_benchmarks_models.gap.json`: OSWorld 2.0 벤더 수치, CADWorld 1차 기록
- `01_research/raw/01_ai-models.research.json`: 클라이언트별 컴퓨터 유즈 지원, OpenAI 출시 데모
