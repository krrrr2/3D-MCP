# 빠른 시작: 설치·연결·보안 설정

> 기준일: 2026-09-27 · AI(Claude Opus 5.5·Fable 5.1, GPT-6 Astra)를 MCP로 Blender·Unreal·Unity에 처음 연결하는 사람을 위한 경로별(A~D) 단계 안내. 설치 → 연결 확인 → 첫 테스트 → 보안·저장·타임아웃 설정 순서로 따라 하면 됩니다.

## 핵심 요약

- **경로는 넷입니다.** A: Claude Desktop + 공식 Blender 커넥터(가장 쉬움, Blender 5.1 이상). B: Claude Code/Codex + 커뮤니티 서버 ahujasid MCP for Blender(에셋·AI 3D 생성 연동이 가장 많음). C: 헤드리스 `blender -b --python` 스크립트 빌드(재현성, 긴 렌더). D: Unreal 5.8 공식 MCP 또는 Unity MCP(게임 레벨). 무엇을 고를지는 [8절 결정표](#8-어떤-경로를-고를까--결정표)를 보세요.
- **추천 조합**: 대화하면서 만드는 단계는 A나 B로, 최종 빌드와 렌더는 C로 합니다. B의 호출 하나는 서버 소켓 타임아웃 180초를 넘을 수 없어서, 긴 렌더와 베이크는 어차피 C로 넘겨야 합니다.
- **공식 커넥터와 ahujasid는 서로 다른 프로젝트**입니다. 공식은 Blender Lab이 만든 서버이고, ahujasid는 커뮤니티 서버입니다. `uvx blender-mcp`와 `uvx mcp-for-blender`는 **둘 다 커뮤니티 서버를 실행**합니다. 두 애드온 모두 `localhost:9876`을 쓰니 **한 Blender에서 동시에 켜지 마세요.**
- **B의 보안 기본값**은 `BLENDER_MCP_SAFE_MODE=1`과 `DISABLE_TELEMETRY=true`입니다. safe mode는 샌드박스가 아닙니다. 텔레메트리는 끄지 않으면 익명 사용 기록을 기본으로 수집합니다.
- **저장 습관**: Claude Code의 `/rewind`는 MCP로 바꾼 Blender 상태를 되돌리지 못합니다. 단계가 끝날 때마다 `bpy.ops.wm.save_mainfile(incremental=True)`로 저장하세요. Blender 4.2.23 LTS와 5.0.1에서 동작을 확인했고, safe mode에서도 허용됩니다.
- **effort 명시**: Codex에서 GPT-6 Astra의 기본 reasoning effort는 `low`입니다. `model_reasoning_effort = "high"`처럼 직접 지정하세요. Claude Opus 5.5의 기본 effort는 medium입니다.
- **[한국 사용자] 한국어 UI 주의**: UI를 현지화하면 새로 만든 노드 이름도 번역될 수 있어 `nodes['Principled BSDF']` 같은 코드가 깨집니다. 영어 UI를 쓰거나 New Data 번역을 끄세요. 이 저장소의 스크립트는 노드를 이름이 아니라 type으로 찾기 때문에 영향을 받지 않습니다.
- **[한국 사용자] Hunyuan3D 로컬 가중치 금지**: Tencent Hunyuan3D 계열 오픈웨이트 라이선스는 적용 지역에서 대한민국을 제외합니다. B 경로에서 Hunyuan3D를 로컬 모드로 붙이지 마세요.
- **Unreal 5.8**: `ModelContextProtocol`과 `AllToolsets` 플러그인을 켜고, 콘솔에서 `ModelContextProtocol.StartServer 8123`, `ModelContextProtocol.GenerateClientConfig ClaudeCode`를 실행합니다. Epic 공식 Claude Code 플러그인도 있습니다.
- **연결되면 바로 검증 루프를 붙이세요.** [`03_playbooks/scripts/`](scripts/README.md)의 `scene_audit.py`(숫자 검사)와 `review_views.py`(4방향 검토 렌더)는 Blender 4.2.23 LTS·5.0.1·5.2.2 LTS에서 테스트를 통과했습니다.

---

## 0. 시작 전에 알아 둘 것

### 0.1 연결 구조 한 장

Blender MCP는 공식이든 커뮤니티든 아래 구조입니다([ahujasid server.py](https://raw.githubusercontent.com/ahujasid/blender-mcp/main/src/blender_mcp/server.py), [공식 서버 미러](https://github.com/bpype/blender_mcp)).

```
AI 클라이언트 (Claude Desktop / Claude Code / Codex / Cursor)
   │  stdio  ← 클라이언트가 MCP 서버 프로세스를 직접 띄움
MCP 서버 프로세스 (uvx mcp-for-blender  또는  공식 blender-mcp)
   │  TCP  localhost:9876
Blender 애드온 (N 패널에서 "서버 시작" → 명령을 메인 스레드 timer 큐로 실행)
```

이 구조에서 세 가지가 나옵니다.

1. **MCP 서버를 터미널에서 따로 실행하지 마세요.** 클라이언트가 직접 띄웁니다. 따로 띄우면 인스턴스가 둘이 됩니다([ahujasid README](https://github.com/ahujasid/blender-mcp)).
2. **포트 9876은 하나만 쓸 수 있습니다.** 공식 애드온, ahujasid 애드온, Scenario for Blender 내장 MCP(`http://127.0.0.1:9876/mcp`)가 모두 이 포트를 씁니다([Scenario 저장소](https://github.com/scenario-labs/blender-plugin)).
3. **애드온은 Blender 메인 스레드에서 코드를 실행합니다.** 코드가 오래 걸리면 Blender UI가 멈추고 다음 명령도 기다립니다. 그래서 코드를 5~20줄 단위로 잘게 나눠 보내야 합니다.

### 0.2 이름 정리 (가장 흔한 혼동)

| 부르는 이름 | 실체 | 설치 방법 | 라이선스 | 포트 |
|---|---|---|---|---|
| Claude 'Blender' 커넥터 | **Blender Lab 공식 MCP 서버**. [claude.com 커넥터 페이지](https://claude.com/connectors/blender) 표기: Made by Blender Lab, Anthropic verified, v1.0.1, 2026년 4월 추가 | Claude Desktop 커넥터 + Lab 애드온. 다른 클라이언트는 git 소스로 설치 | GPL-3.0-or-later ([manifest](https://raw.githubusercontent.com/bpype/blender_mcp/main/addon/blender_mcp_addon/blender_manifest.toml)) | 9876 |
| MCP for Blender (구 blender-mcp) | **ahujasid 커뮤니티 서버**. 약 29.4k stars. README가 스스로 "not made by Blender"라고 밝힘 | `uvx mcp-for-blender` ([PyPI 2.1.0, 2026-09-25](https://pypi.org/project/mcp-for-blender/)) | MIT | 9876 |
| `uvx blender-mcp` | 위 커뮤니티 서버의 **호환 래퍼**(blender-mcp 2.0.0, 2026-09-16). 공식 서버가 아님 | 기존 설정은 그대로 동작하지만 새로 설치할 때는 `mcp-for-blender` 권장 ([PyPI](https://pypi.org/project/blender-mcp/)) | MIT | 9876 |
| blender-mcp.com, blendermcp.org | **비공식 사이트**. 공식 서버와도, ahujasid와도 무관 | 여기서 애드온을 받지 마세요([이슈 #339](https://github.com/ahujasid/blender-mcp/issues/339)에서 문제 원인으로 거론) | — | — |

- Anthropic은 2026-04-28 [Claude for Creative Work](https://www.anthropic.com/news/claude-for-creative-work)에서 크리에이티브 커넥터 9종(Ableton, Adobe for creativity, Affinity by Canva, Autodesk Fusion, Blender, Resolume Arena, Resolume Wire, SketchUp, Splice)을 발표했습니다. 3D와 직접 관련된 것은 Blender, Fusion, SketchUp입니다. 발표문 원문은 "The Blender developers have created an MCP connector"이고, 다른 LLM에서도 쓸 수 있다고 적혀 있습니다.

### 0.3 공통 준비물과 버전

| 항목 | 2026-09-27 기준 | 비고 |
|---|---|---|
| Blender | 최신 안정판 **5.2.2**(2026-09-14). 4.5 LTS와 4.2 LTS 병행 | 경로 A는 **5.1.0 이상**(공식 애드온 manifest의 `blender_version_min`). B는 README 기준 3.0 이상 |
| uv / uvx | Astral 공식 설치 스크립트로 설치 | `pip install uv`는 README가 권장하지 않음 |
| Python | B: 3.10 이상. C(pip `bpy`): **bpy 5.1 이상은 Python 3.13 전용, bpy 5.0은 3.11** | [PyPI bpy](https://pypi.org/project/bpy/) 5.2.2(2026-09-15). 플랫폼별 wheel 하나가 210~402MB |
| git | 공식 서버를 Claude Code·Codex에 붙일 때 필요 | 공식 서버는 PyPI가 아니라 git 소스에서 설치 |
| Claude Code | Opus 5.5는 v2.1.280 이상, Fable 5.1은 v2.1.257 이상 | [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) |
| Codex CLI | GPT-6 Astra는 0.153.0 이상 | [Codex models.json](https://github.com/openai/codex/blob/main/codex-rs/models-manager/models.json) |
| Unreal Engine | 5.8(공식 MCP 플러그인, Experimental) | 5.7 이하는 커뮤니티 서버(4.1절) |

- 모델과 요금은 [AI 모델·클라이언트 가이드](../02_guides/01_ai_models_and_clients.md)에서 다룹니다. 요약하면 Claude Opus 5.5는 $4/$20(1M 컨텍스트, 기본 effort medium, Anthropic 표현으로는 vision과 computer use에 가장 좋은 Opus), Fable 5.1은 $10/$50, Sonnet 5는 $2/$10입니다(1M 토큰당 입력/출력). GPT-6 Astra는 2026-09-03 출시로 2차 출처에서 확인했고, openai.com 원문은 열람하지 못했습니다. Google의 'Project Astra'와는 다른 제품입니다.
- **ChatGPT 웹 채팅은 로컬 Blender에 붙지 않습니다.** 원격 MCP만 지원하기 때문입니다([OpenAI 도움말](https://help.openai.com/en/articles/12584461-developer-mode-apps-and-full-mcp-connectors-in-chatgpt-beta), 검색 요약으로 확인). GPT-6 Astra로 Blender를 다루려면 Codex CLI, Codex 앱, IDE 확장을 쓰세요.

### 0.4 한국 사용자 체크리스트

> **[한국 사용자] 설치 전에 세 가지를 먼저 정하세요.**
>
> 1. **Blender UI 언어**: 한국어 UI에서는 새로 만든 노드 이름이 번역될 수 있습니다. 일본어 UI에서 'Principled BSDF'가 'プリンシプルBSDF'로 생성돼 스크립트가 깨진 사례가 문서로 남아 있습니다([roo-blendermcp-jp-rules](https://github.com/hideki711014/roo-blendermcp-jp-rules)). 한국어도 같은 원리가 적용될 가능성이 높습니다(추정). 대응은 둘 중 하나입니다.
>    - 영어 UI를 씁니다.
>    - Preferences > Interface > Translation에서 **New Data** 번역을 끕니다. 코드로는 `bpy.context.preferences.view.use_translate_new_dataname = False`입니다. 이 속성이 4.2.23 LTS와 5.0.1에 있다는 것은 확인했지만, 실제로 번역이 꺼지는 동작은 확인하지 못했습니다.
> 2. **Hunyuan3D**: 2.0/2.1/Omni/Part, HY-World, HY-Motion, BPT 등 Tencent Hunyuan3D 계열 오픈웨이트 라이선스([Hunyuan3D-2 LICENSE](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/LICENSE))는 적용 지역을 "worldwide, excluding the European Union, United Kingdom and South Korea"로 정하고 출력물 사용도 제한합니다. **한국에서 로컬 가중치로 돌리는 것은 라이선스 범위 밖**입니다. ahujasid의 Hunyuan3D 로컬 API URL 모드도 여기에 해당합니다. Tencent Cloud API 경유 사용은 별도 약관을 따르는데, 원문은 확인하지 못했습니다(미확인). 자세한 내용은 [에셋·라이선스 가이드](../02_guides/10_assets_pipeline_licensing.md)를 보세요.
> 3. **Windows 환경**: 경로 B에는 Windows 전용으로 열려 있는 문제가 있습니다(연결은 되는데 명령이 처리되지 않다가 약 4분 뒤 타임아웃되는 이슈 [#339](https://github.com/ahujasid/blender-mcp/issues/339), [#357](https://github.com/ahujasid/blender-mcp/issues/357), Blender 5.1.1·5.2.1 보고). Windows에서 막히면 경로 A나 C를 먼저 시도해 보세요.
>
> 한국어 설치 후기(Threads, 클리앙)는 [한국어 자료 모음](../04_case_studies/02_korean_resources.md)에 모았습니다. 대부분 원문을 열람하지 못하고 검색 요약으로만 확인한 것이라 신뢰도는 낮습니다.

---

## 1. 경로 A: Claude Desktop + 공식 Blender 커넥터 (Blender Lab)

**이럴 때**: 코드를 모르는 사람, Blender 5.1 이상을 쓰는 사람, 씬 분석·디버깅·일괄 수정·문서 기반 스크립트 작성이 주목적인 사람. 공식 서버는 **에셋 다운로드나 AI 3D 생성 기능이 없습니다.** 필요하면 B를 쓰거나 Meshy MCP 같은 생성 MCP를 따로 붙이세요([Blender MCP 가이드](../02_guides/02_blender_mcp.md)).

### 1.1 준비물

- Claude Desktop(macOS 또는 Windows)과 Claude 계정. 커넥터 추가에 별도 요금은 없다고 조사됐지만, '모든 Claude 플랜에서 쓸 수 있다'는 설명은 발표문에 없어 확인하지 못했습니다(검색 요약 기준). Opus 5.5와 Fable 5.1은 유료 플랜에서만 쓸 수 있습니다.
- Blender **5.1.0 이상**(권장: 5.2.2). 근거는 GitHub 미러에 있는 공식 애드온 manifest의 `blender_version_min = "5.1.0"`입니다. [커넥터 페이지](https://claude.com/connectors/blender)에는 버전 요구가 적혀 있지 않습니다.
- 인터넷 연결과 Blender의 **Allow Online Access**. 꺼져 있으면 공식 애드온이 `Online access must be enabled in the system preferences`라며 서버를 열지 않습니다(2026-09-27 실제 구동으로 확인, [검증 기록](../01_research/handson/blender_lab_mcp/README.md)).

### 1.2 설치 단계

1. **Blender 쪽 준비**: Blender 5.1 이상을 실행하고 Edit > Preferences > System에서 Allow Online Access를 켭니다.
2. **Lab 애드온 설치**: 공식 README의 방법은 두 단계입니다. ① Preferences > Get Extensions > Repositories에 Blender Lab 확장 저장소 `https://lab.blender.org/`를 추가하고, ② 목록에서 MCP 애드온을 찾아 설치·활성화합니다([공식 mcp/README.md](https://github.com/bpype/blender_mcp/blob/98b0e49d98321d321c7e631389200f513f765d59/mcp/README.md)).
   - [blender.org/lab/mcp-server](https://www.blender.org/lab/mcp-server/) 페이지의 설치 링크를 Blender 창에 **두 번** 드래그해도 됩니다(한국·일본 커뮤니티 후기). 1회차 드래그가 ①, 2회차가 ②에 해당합니다.
   - 드래그 설치와 수동 설치를 **둘 다 하지 마세요.** 같은 ID의 애드온이 두 개 생긴다는 경고가 있습니다([stefancrm 설치 키트](https://github.com/stefancrm/claude-blender-mcp-connector-setup-kit)).
3. **애드온 활성화와 서버 시작**: Edit > Preferences > Add-ons에서 Blender Lab MCP 애드온이 켜져 있는지 확인합니다. Auto Start가 기본으로 켜져 있어 Blender를 시작하면 1초 뒤 `localhost:9876`에서 서버가 열립니다. 애드온 설정에는 host, port, polling, auto-start 항목과 시작·중지 버튼이 있고, 서버가 안 열리면 오류 문구가 거기에 표시됩니다([미러 README](https://github.com/bpype/blender_mcp)).
4. **ahujasid 애드온 끄기**: 예전에 커뮤니티 애드온(MCP for Blender)이나 Scenario for Blender를 설치했다면 비활성화합니다. 포트 9876을 먼저 잡고 있으면 커넥터가 엉뚱한 서버에 붙습니다.
5. **Claude Desktop 쪽**: 설정(Customize) → Connectors에서 `blender`를 검색해 Blender 커넥터를 추가하고 활성화합니다. 'Anthropic & Partners' 섹션에 있다는 후기가 있지만 공식 원문은 미확인입니다.

> .mcpb 번들을 지원하는 다른 클라이언트는 공식 릴리스 페이지의 MCPB 파일로 설치할 수 있습니다([projects.blender.org/lab/blender_mcp](https://projects.blender.org/lab/blender_mcp), 원문 미열람). **v1.0.2 이상**을 고르세요. v1.0.0·v1.0.1은 2026-07-28 이후 새로 설치하면 MCP SDK 2.x와 맞지 않아 시작하자마자 끊길 수 있습니다([Blender MCP 가이드 4.1절](../02_guides/02_blender_mcp.md)).

### 1.3 연결 확인

1. Claude Desktop의 새 대화에서 Blender 커넥터가 켜져 있는지(도구 목록에 보이는지) 확인합니다.
2. 아래 첫 번째 테스트 프롬프트를 보냅니다. Blender 버전과 오브젝트 목록이 돌아오면 연결된 것입니다.
3. 응답이 없으면 순서대로 확인합니다: Blender에서 서버가 시작됐는가 → Allow Online Access가 켜져 있는가 → 9876을 다른 애드온이 잡고 있지 않은가(macOS/Linux `lsof -i :9876`, Windows `netstat -ano | findstr 9876`) → Blender 버전이 5.1 이상인가.

### 1.4 첫 테스트 프롬프트

```text
[1. 연결 확인] Blender에 연결됐는지 확인해 줘. Blender 버전과 현재 씬의 오브젝트 목록
(이름, 타입, 위치)을 표로 보여 줘. 아무것도 수정하지 마.

[2. 공식 예시 프롬프트] Analyze the scene and list the outliers: objects with highest
polygon count but smaller size from the camera point of view.

[3. 작은 수정] 기존 오브젝트는 건드리지 말고, 원점에서 +X로 2 m 떨어진 곳에
한 변 0.45 m 정육면체 'GEO-test_box'를 바닥(z=0)에 붙여 만들어 줘.
만든 뒤 오브젝트 치수를 출력하고 뷰포트 스크린샷으로 확인해 줘.

[4. 저장] 현재 파일을 bpy.ops.wm.save_mainfile(incremental=True)로 번호 붙여 저장해 줘.
파일이 아직 한 번도 저장되지 않았다면 먼저 경로를 물어봐.
```

- 2번은 공식 페이지에 소개된 예시입니다([Blender MCP 가이드 4절](../02_guides/02_blender_mcp.md) 참고).
- 공식 서버의 도구는 26개입니다(실측). 대표 도구는 `execute_blender_code`, `get_objects_summary`, `get_object_detail_summary`, `get_blendfile_summary_missing_files`(누락 텍스처), `get_python_api_docs`, `search_api_docs`·`search_manual_docs`(번들 문서 검색), 화면 캡처(`get_screenshot_of_area_as_image` 등), `render_viewport_to_path`입니다.
- 이 서버는 코드 실행 결과를 `result` 변수(dict)로 돌려주고, 실패도 대부분 `status: "error"`가 든 정상 응답으로 돌려줍니다. 렌더 도구는 지정 경로가 아니라 Blender 임시 폴더에 저장합니다(가이드 4.1절).
- Anthropic 발표문에 따르면 이 커넥터로 Claude가 **새 도구를 Blender 인터페이스에 직접 추가**할 수도 있습니다("add new tools directly to Blender's interface"). 반복 작업을 버튼이나 패널로 만들고 싶을 때 요청해 보세요.

### 1.5 (선택) 같은 공식 서버를 Claude Code·Codex에 붙이기

공식 서버는 PyPI에 없고 **git 소스에서 실행**합니다. PyPI의 `blender-mcp`는 커뮤니티 서버입니다. 공식 README의 설치 명령은 `pip install git+https://projects.blender.org/lab/blender_mcp.git#subdirectory=mcp`입니다. 아래 uvx 형식은 공식 서버를 git 태그로 고정해 쓰는 [franjorub 플러그인](https://github.com/franjorub/grok-build-blender-plugin)에서 가져왔습니다(2차 출처).

```bash
# 공식 서버 실행 형식 (2차 출처: franjorub/grok-build-blender-plugin)
# v1.0.2 이상 태그를 쓰세요. v1.0.3 태그 이름은 릴리스 페이지 표기 기준(원문 미확인)
uvx --from 'git+https://projects.blender.org/lab/blender_mcp.git@v1.0.3#subdirectory=mcp' blender-mcp

# v1.0.0·v1.0.1 태그라면 MCP SDK를 1.x로 고정해야 시작됩니다 (미러 소스로 동작 확인)
uvx --with 'mcp[cli]<2' --from 'git+https://projects.blender.org/lab/blender_mcp.git@v1.0.0#subdirectory=mcp' blender-mcp

# Claude Code에 등록 (조합 예시, 직접 실행 검증은 하지 않음)
claude mcp add blender-lab -- uvx --from 'git+https://projects.blender.org/lab/blender_mcp.git@v1.0.3#subdirectory=mcp' blender-mcp

# Codex CLI에 등록 (조합 예시, 미검증)
codex mcp add blender-lab -- uvx --from 'git+https://projects.blender.org/lab/blender_mcp.git@v1.0.3#subdirectory=mcp' blender-mcp
```

또는 저장소를 클론하고 `~/.claude.json`의 `mcpServers`에 넣습니다. `$HOME`은 확장되지 않으니 **절대경로**를 쓰세요([stefancrm 키트](https://github.com/stefancrm/claude-blender-mcp-connector-setup-kit)).

```jsonc
{
  "mcpServers": {
    "blender-lab": {
      "command": "/절대경로/uv",
      "args": ["--directory", "/절대경로/blender_mcp/mcp", "run", "blender-mcp"]
    }
  }
}
```

- **첫 실행은 느립니다.** git 소스를 빌드하고 PyPI 의존성 약 41개를 내려받기 때문에 클라이언트의 서버 시작 타임아웃을 넘을 수 있습니다. Claude Code라면 `MCP_TIMEOUT=120000 claude`처럼 시작 타임아웃(ms)을 늘려 실행하세요.
- 버전: GitHub 미러는 v1.0.0 계열입니다. 검색 요약에 따르면 [릴리스 페이지](https://projects.blender.org/lab/blender_mcp/releases)의 v1.0.2(2026-09-08)가 "MCP SDK <2" 고정을, v1.0.3(2026-09-11)이 스크린샷 도구 수정을 담았습니다. v1.0.0 계열을 SDK 고정 없이 설치하면 `No module named 'mcp.server.fastmcp'`로 죽는 것을 직접 확인했습니다. 설치 전에 공식 저장소에서 최신 태그를 확인하세요.
- 공식 서버는 stdio 외에 HTTP 모드도 지원합니다. `blender-mcp --transport http`의 기본값은 `127.0.0.1:8000`, 경로 `/`입니다. `--port 9191`은 [readme_local_llm.rst](https://github.com/bpype/blender_mcp/blob/main/readme_local_llm.rst)의 예시 값입니다. CORS 전체 허용에 인증이 없으니 필요할 때만 켜세요(가이드 4.4절). 로컬 LLM(llama.cpp) 연결은 이 문서를 참고하세요.
- GUI 없이 쓰려면 `blender --background --online-mode 파일.blend --command blender_mcp`로 애드온 서버를 띄웁니다. 이 모드에서는 스크린샷·UI 이동 도구를 쓸 수 없습니다.
- 공식 서버용 Claude Code 스킬은 [Blender MCP 가이드](../02_guides/02_blender_mcp.md)의 스킬 절(ra100/blender-claude-plugin)을 보세요.

### 1.6 권장 보안·저장 설정

- 공식 서버에는 텔레메트리나 외부 서비스 연동이 없다고 조사됐습니다. 하지만 **`execute_blender_code`는 임의 Python을 실행**하고, 그 안전장치(확인 문구, 샌드박스 여부)는 원문으로 확인하지 못했습니다. 신뢰하지 않는 .blend 파일이나 프롬프트를 넣지 마세요.
- 작업 전에 저장합니다. 단계마다 `bpy.ops.wm.save_mainfile(incremental=True)`(6.2절).
- 애드온 host는 `localhost`로 둡니다. 원격 Blender가 필요하면 포트를 열지 말고 SSH 터널을 쓰세요.

### 1.7 자주 나는 오류 (경로 A)

| 증상 | 원인 | 해결 |
|---|---|---|
| 커넥터는 켜져 있는데 도구가 응답하지 않음 | Blender 서버를 시작하지 않음, Allow Online Access 꺼짐, Blender 5.1 미만 | 1.3절 순서대로 확인 |
| 엉뚱한 도구 목록(Poly Haven 등)이 보이거나 명령이 이상하게 동작 | ahujasid 애드온이나 Scenario 애드온이 9876을 먼저 잡음 | 다른 애드온을 끄고 Blender 재시작 |
| 애드온이 두 개 보임 | 드래그 설치와 수동 설치를 중복 | 하나를 제거 |
| "에셋을 받아 와", "3D 모델을 생성해"가 안 됨 | 공식 서버에는 해당 기능이 없음 | 경로 B, 또는 생성 MCP(Meshy MCP 등)를 추가 |
| Claude Code에서 공식 서버가 시작 중 타임아웃 | 첫 git 빌드와 의존성 다운로드가 오래 걸림 | `MCP_TIMEOUT` 증가(1.5절) |
| 렌더 화면이 마젠타(분홍) | 대개 이미지 텍스처 파일 누락 | `get_blendfile_summary_missing_files`로 누락 경로 확인 후 재연결 |

---

## 2. 경로 B: Claude Code / Codex + ahujasid MCP for Blender

**이럴 때**: Poly Haven·Sketchfab·Poly Pizza 에셋 검색, Hyper3D Rodin·Hunyuan3D 생성, GLB/FBX 내보내기를 에이전트가 직접 해야 할 때. Blender 5.0 이하를 쓸 때. GPT-6 Astra(Codex)를 쓸 때. 클라이언트 지원 범위가 가장 넓습니다(Claude, Cursor, VS Code, Codex, OpenCode, Antigravity).

### 2.1 준비물

- Blender 3.0 이상(README 기준). 이 저장소의 보조 스크립트는 4.2.23 LTS·5.0.1·5.2.2 LTS에서 테스트했습니다.
- Python 3.10 이상, uv(공식 설치 스크립트로 설치).
- MCP 클라이언트 하나: Claude Code, Codex CLI/앱, Claude Desktop, Cursor 등.
- 선택: Sketchfab·Poly Pizza·Hyper3D·Hunyuan3D API 키. **Tripo 생성은 유료 Premium 전용**이라 자기 키로는 쓸 수 없습니다([server.py](https://raw.githubusercontent.com/ahujasid/blender-mcp/main/src/blender_mcp/server.py)). Premium 가격은 확인하지 못했습니다([Premium 페이지](https://www.mcp-for-blender.com/premium)). Tripo가 필요하면 Tripo 공식 [tripo-mcp](https://github.com/VAST-AI-Research/tripo-mcp)(MIT, alpha)가 대안입니다.

### 2.2 설치 단계 (Blender 쪽)

1. 애드온을 설치합니다: `uvx mcp-for-blender install-addon`. 또는 저장소의 `addon.py`를 Edit > Preferences > Add-ons에서 파일로 설치합니다.
2. Edit > Preferences > Add-ons에서 **'Interface: MCP for Blender'** 를 켭니다.
3. 3D 뷰포트에서 `N` 키 → **'MCP for Blender'** 탭 → **Start MCP Server**를 누릅니다(기본 포트 9876).
4. 공식 Blender Lab 애드온이 켜져 있다면 끕니다(포트 충돌).

### 2.3 클라이언트 등록

**Claude Code** ([README](https://github.com/ahujasid/blender-mcp) 명령에 `--` 구분자를 더한 형태):

```bash
claude mcp add blender -- uvx mcp-for-blender
# 환경변수까지 한 줄로: --env 바로 뒤에 서버 이름이 오면 이름을 KEY=value로 읽으므로 --transport를 사이에 둠
claude mcp add --env DISABLE_TELEMETRY=true --env BLENDER_MCP_SAFE_MODE=1 --transport stdio blender -- uvx mcp-for-blender
```

README는 `claude mcp add blender uvx mcp-for-blender`처럼 `--` 없이 적지만, Claude Code 문서는 Claude 옵션과 서버 명령을 `--`로 나누라고 권합니다([Claude Code MCP 문서](https://code.claude.com/docs/en/mcp)).

팀과 설정을 공유하거나 환경변수·타임아웃까지 파일로 고정하려면 프로젝트 루트의 `.mcp.json`을 씁니다(`--scope project`로 만들 수 있음). 권장 설정은 아래와 같습니다.

```jsonc
// .mcp.json (Claude Code 프로젝트) — Claude Desktop의 claude_desktop_config.json도 같은 형식
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["mcp-for-blender"],
      "env": {
        "BLENDER_MCP_SAFE_MODE": "1",
        "DISABLE_TELEMETRY": "true"
      },
      "timeout": 600000          // (선택) 호출당 절대 한도(ms). 미설정 시 약 28시간이라 늘리는 효과는 없고,
                                 // ahujasid는 서버 소켓 180초가 먼저 걸림. 5절 참고
    }
  }
}
```

**Codex CLI / 앱 / IDE 확장** (셋이 `~/.codex/config.toml`을 공유):

```bash
codex mcp add blender -- uvx mcp-for-blender
codex mcp list        # 등록 확인
```

```toml
# ~/.codex/config.toml
model = "gpt-6-astra"
model_reasoning_effort = "high"     # Codex에서 Astra 기본값은 low. low/medium/high/xhigh/max/ultra

[mcp_servers.blender]
command = "uvx"
args = ["mcp-for-blender"]
startup_timeout_sec = 30            # 기본 10초(원문 미재확인)
tool_timeout_sec = 600              # 기본 60초(원문 미재확인). 렌더는 60초를 쉽게 넘음

[mcp_servers.blender.env]           # env 키: 검색 요약 기준, Codex 공식 문서 원문 미열람
BLENDER_MCP_SAFE_MODE = "1"
DISABLE_TELEMETRY = "true"
```

- Codex Desktop은 Settings → MCP servers → STDIO에 `uvx mcp-for-blender`를 추가합니다.
- effort 단계(`low/medium/high/xhigh/max/ultra`)와 기본값 `low`는 OpenAI의 [Codex models.json](https://github.com/openai/codex/blob/main/codex-rs/models-manager/models.json) 기준입니다. 비교하거나 실사용할 때 effort를 적지 않으면 low로 돌아 품질이 낮게 나옵니다.
- config.toml의 키 이름(`startup_timeout_sec`, `tool_timeout_sec`, `env`)은 [Codex MCP 문서](https://developers.openai.com/codex/mcp)의 검색 요약에서 가져왔습니다. 원문은 열람하지 못했으니 오류가 나면 공식 문서로 확인하세요.

**Claude Desktop** (커뮤니티 서버를 쓰는 경우): `claude_desktop_config.json`에 위 `.mcp.json`과 같은 `mcpServers` 블록을 넣습니다(`timeout` 줄은 빼세요). 이때 **공식 Blender 커넥터는 꺼 두세요.**

**Cursor (Windows)**: `"command": "cmd", "args": ["/c", "uvx", "mcp-for-blender"]`. Cursor는 활성 도구가 합계 약 40개를 넘으면 일부를 조용히 빠뜨리니, 안 쓰는 MCP 서버를 끄세요.

**Blender를 두 개 띄울 때**: 두 번째 서버를 `"args": ["mcp-for-blender", "--port", "9877"]`로 추가하고, 두 번째 Blender의 애드온 포트도 9877로 맞춥니다. blender-mcp-pro의 기본 포트가 9877이니 함께 쓴다면 다른 번호를 고르세요.

### 2.4 연결 확인

- Claude Code: `/mcp`에서 `blender` 서버가 connected인지 봅니다.
- Codex: `codex mcp list`.
- 그다음 "get_addon_status로 연결 상태와 Blender 버전을 알려 줘"를 보냅니다. `get_addon_status`는 36개 도구 중 하나입니다.
- **첫 명령만 실패하고 두 번째부터 되는 경우가 많습니다.** 계속 실패하면 클라이언트와 Blender 서버를 둘 다 재시작하세요.

### 2.5 첫 테스트 프롬프트

```text
[1] get_scene_info로 씬을 확인하고, 기존 오브젝트는 수정하거나 삭제하지 마.
[2] execute_blender_code로 아래를 실행해. 다시 실행해도 결과가 같게(get-or-create) 써.
    - 원점에서 +X 2 m 위치에 한 변 0.45 m 정육면체 'GEO-test_box'를 바닥(z=0)에 붙여 생성
    - 마지막 줄에 이름·치수·최저 z를 JSON 한 줄로 print
[3] get_viewport_screenshot으로 결과를 보고, 기대값과 다른 점을 3줄 이내로 적어.
[4] bpy.ops.wm.save_mainfile(incremental=True)로 저장해. 파일이 한 번도 저장되지 않았으면 경로를 먼저 물어봐.
```

에이전트가 [2]에서 만들어야 하는 코드는 대략 이렇습니다. bpy 5.0.1과 4.2.23 LTS에서 두 번 연속 실행해 오브젝트가 하나만 생기는 것을 확인했습니다.

```python
import bpy, json
ob = bpy.data.objects.get("GEO-test_box")
if ob is None:
    bpy.ops.mesh.primitive_cube_add(size=0.45, location=(2.0, 0.0, 0.225))
    ob = bpy.context.active_object
    ob.name = "GEO-test_box"
bpy.context.view_layer.update()
print(json.dumps({"name": ob.name, "dims": [round(v, 3) for v in ob.dimensions],
                  "min_z": round(min((ob.matrix_world @ v.co).z for v in ob.data.vertices), 3)}))
```

- `execute_blender_code`는 호출마다 **새 namespace**에서 실행됩니다. 앞 호출의 Python 변수는 남지 않으니 오브젝트는 이름으로 다시 찾게 하세요(`GEO-`, `MAT-`, `LGT-`, `CAM-` 접두사 권장).
- 에셋 테스트는 가볍게 시작합니다: "Poly Haven에서 실내 HDRI 하나를 **1k**로 받아 월드에 적용해 줘". Poly Haven 다운로드는 메인 스레드에서 돌아서 고해상도를 요청하면 Blender가 멈춥니다.
- README의 대표 데모 프롬프트는 "Create a beach vibe using HDRIs, textures, and models like rocks and vegetation"입니다.

**바로 이어서 할 것: 이 저장소의 검사 스크립트 연결** ([scripts/README.md](scripts/README.md)):

```python
import sys
sys.path.append(r"C:\path\to\3D-MCP\03_playbooks\scripts")   # 이 저장소를 받은 위치
import importlib, scene_audit
importlib.reload(scene_audit)
report = scene_audit.audit_scene(floor_z=0.0)
print(report["summary"])            # 떠 있음·관통·스케일 미적용·치수 이탈 등 요약
```

safe mode에서 이 `sys.path` import가 막히면 `scene_audit.py` 파일 내용을 통째로 `execute_blender_code`에 붙여 넣으세요. 끝에서 자동으로 점검을 실행하고 JSON을 출력합니다.

### 2.6 권장 보안 설정 (경로 B)

| 설정 | 값 | 무엇을 하나 | 주의 |
|---|---|---|---|
| `BLENDER_MCP_SAFE_MODE` | `1` | MCP로 들어온 코드를 검사해 **직접** 파일 I/O(`open()`, `os`), 외부 프로세스, 네트워크, handlers·timers·drivers, 외부 .blend append/link를 막음. 2026-09-02 커밋으로 추가 | **샌드박스가 아닙니다.** 검사는 MCP 경로에만 걸리고, 애드온 소켓은 로컬의 다른 프로세스가 보낸 코드도 그대로 받습니다. bpy 오퍼레이터를 통한 저장·열기, import/export, 렌더는 허용됩니다 |
| `DISABLE_TELEMETRY` | `true` | 텔레메트리를 **전부** 끔 | 2026-09-21 커밋 이후 콘텐츠(프롬프트, 코드, 스크린샷, 궤적) 수집은 옵트인이 됐지만, 익명 사용 기록(install ID, 세션 ID, 도구 이름, 성공 여부, 소요 시간, 버전, OS)은 **끄지 않으면 기본 수집**됩니다. README는 수집 데이터가 AI 모델 학습에 쓰일 수 있다고 적고 있습니다 |
| `BLENDER_HOST` | `localhost` | 애드온 접속 주소 | 외부에 노출하지 마세요. 소켓에는 인증도 암호화도 없습니다. 원격은 SSH 터널로 |
| 버전 | 최신(2.1.0 이상) | 2026 CVE 4건(10661·10662·10688 Low, 66004 Poly Haven 경로 조작 Moderate, 커밋 30a3308 수정) 반영 버전. 목록은 [Blender MCP 가이드 10.1절](../02_guides/02_blender_mcp.md) | [GHSA](https://github.com/advisories/GHSA-qqw9-95ww-prfm). 로컬 파일을 읽어 외부 API로 보내는 구체적 시나리오는 [이슈 #202](https://github.com/ahujasid/blender-mcp/issues/202)에 있음(GHSA 본문이 #202와 명시적으로 연결하지는 않음) |

- 근거: [README](https://github.com/ahujasid/blender-mcp), [커밋 로그](https://github.com/ahujasid/blender-mcp/commits/main), [텔레메트리 이슈 #232](https://github.com/ahujasid/blender-mcp/issues/232).
- 더 강한 격리가 필요하면 임의 코드 실행을 막은 [blend-ai](https://github.com/HoldMyBeer-gg/blend-ai)(허용 import 5개, 127.0.0.1 전용, AGPL-3.0-or-later)를 검토하세요.
- **유료 생성 API는 호출 전에 사용자 확인**을 받도록 프롬프트나 [CLAUDE.md 템플릿](templates/CLAUDE.md)에 적어 두세요.

### 2.7 자주 나는 오류 (경로 B)

| 증상 | 원인 | 해결 |
|---|---|---|
| `spawn uvx ENOENT` | GUI로 실행한 Claude Desktop·Cursor는 터미널 PATH를 물려받지 않음 | `command`에 uvx **절대경로**(`where uvx` / `which uvx` 결과)를 넣음 |
| Python 버전 충돌(conda, pyenv, asdf 환경) | 엉뚱한 Python이 잡힘 | `"args": ["--python", "3.11", "mcp-for-blender"]`, `"env": {"UV_PYTHON_PREFERENCE": "only-managed"}` |
| 연결은 되는데 명령이 처리되지 않다가 약 4분 뒤 타임아웃(Windows) | 열린 이슈 [#339](https://github.com/ahujasid/blender-mcp/issues/339)·[#357](https://github.com/ahujasid/blender-mcp/issues/357)(프레이밍 불일치 의심, Blender 5.1.1·5.2.1 보고) | 클라이언트와 Blender 재시작, 비공식 사이트에서 받은 애드온 제거. 계속되면 경로 A나 C |
| WSL의 클라이언트 ↔ Windows의 Blender에서 스크린샷 실패 | 경로 문제(이슈 #187) | 클라이언트와 Blender를 같은 OS에서 실행 |
| 서버가 두 개 뜨거나 연결이 꼬임 | 터미널에서 `uvx mcp-for-blender`를 따로 실행함 | 터미널 프로세스를 끄고 클라이언트에만 맡김 |
| 약 180초에서 명령이 끊김 | 서버 소켓 타임아웃 180초(server.py) | 코드를 5~20줄로 나누기. 렌더·베이크는 해상도·샘플을 낮추거나 경로 C로 |
| Poly Haven 다운로드 중 Blender 멈춤 | 다운로드가 메인 스레드에서 돎 | 1k·2k로 요청 |
| 씬이 큰데 AI가 오브젝트를 일부만 앎 | `get_scene_info`는 오브젝트를 **10개까지만** 반환하고 치수도 없음 | 압축 씬 요약 코드를 실행하게 하거나 `scene_audit.audit_scene()` 사용 |
| Tripo 생성 실패 | Premium 전용 | Premium 구독, 또는 [Tripo SDK](https://pypi.org/project/tripo3d/)·ComfyUI 노드(공식 tripo-mcp는 2025-04-14 이후 방치, 비권장) |
| `KeyError: 'Principled BSDF'` | 한국어 등 현지화 UI에서 노드 이름이 번역됨 | `next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')` |
| `'BLENDER_EEVEE_NEXT'` 관련 오류 | 5.x에서 식별자가 `'BLENDER_EEVEE'`로 바뀜(4.2~4.x는 `_NEXT`) | `'BLENDER_EEVEE' if bpy.app.version >= (5, 0, 0) else 'BLENDER_EEVEE_NEXT'` |
| `mat.use_nodes` DeprecationWarning | 5.0에서 폐기 예고(6.0에서 제거 예정) | `if bpy.app.version < (5, 0, 0): mat.use_nodes = True` |
| 컨텍스트가 금방 참 | 도구 스키마만 약 6,928토큰(28개 도구 시점 측정, [#347](https://github.com/ahujasid/blender-mcp/issues/347)). 지금은 36개라 더 클 가능성이 큼 | 도구 정의를 한꺼번에 불러오는 클라이언트(Claude Desktop, Cursor)에서는 안 쓰는 MCP를 끔. Claude Code는 지연 로딩이라 영향이 적음 |

---

## 3. 경로 C: 헤드리스 스크립트 빌드 + 렌더 확인

**이럴 때**: 결과를 재현해야 할 때(스크립트가 곧 소스), git으로 버전 관리할 때, GUI 멈춤이나 소켓 타임아웃 없이 긴 렌더를 돌릴 때, CI에서 여러 변형을 병렬로 렌더할 때. GPT-6 Astra 출시 데모에서도 headless Blender와 Python으로 만들고 렌더를 확인하는 방식이 쓰였다고 보고됐습니다(모델 팀의 자기 보고). MCP 없이 Claude Code나 Codex가 파일을 쓰고 명령을 실행하는 것만으로 됩니다.

### 3.1 준비물

- Blender 설치본(`blender` 실행 파일이 PATH에 있거나 절대경로를 앎). 또는 PyPI `bpy` 모듈: `pip install bpy==5.2.2`는 **Python 3.13 venv**가 필요하고, `bpy==5.0.1`은 Python 3.11입니다.
- GPU가 없는 리눅스 서버에서는 **Cycles(CPU)만** 확실히 동작합니다. EEVEE와 Workbench 렌더는 GPU나 EGL 컨텍스트가 필요할 수 있습니다(이 저장소 스크립트 테스트 환경에서 확인한 제약).
- 이미지를 읽을 수 있는 에이전트(Claude Code의 Read, Codex의 이미지 입력).

### 3.2 최소 빌드 스크립트

아래 `build_scene.py`는 바닥, 4인 식탁(상판과 다리 4개를 Empty 부모로 묶음), 조명, 카메라를 만들고 .blend 저장 → 렌더 → 결과 요약 출력까지 합니다. **bpy 5.0.1과 4.2.23 LTS에서 그대로 실행해 확인했습니다.**

```python
"""build_scene.py - 헤드리스 빌드 최소 예제 (Blender 4.2 LTS ~ 5.x)
실행: blender -b --factory-startup --python-exit-code 1 -P build_scene.py -- --out renders/v001.png
"""
import json
import os
import sys

import bpy

# 1) '--' 뒤 인자 파싱
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
args = dict(zip(argv[::2], argv[1::2]))
out_png = os.path.abspath(args.get("--out", "renders/v001.png"))
out_blend = os.path.abspath(args.get("--blend", os.path.splitext(out_png)[0] + ".blend"))
samples = int(args.get("--samples", "32"))
os.makedirs(os.path.dirname(out_png), exist_ok=True)

# 2) 매번 빈 씬에서 시작 (스크립트가 곧 소스이므로 재실행해도 같은 결과)
for ob in list(bpy.data.objects):
    bpy.data.objects.remove(ob, do_unlink=True)
scene = bpy.context.scene
scene.unit_settings.system = "METRIC"   # 1 BU = 1 m


def make_mat(name, rgb, roughness):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    if bpy.app.version < (5, 0, 0):       # 5.0부터 use_nodes는 폐기 예고(항상 True)
        mat.use_nodes = True
    # 노드는 이름이 아니라 type으로 찾는다 (한국어 UI에서 이름이 번역될 수 있음)
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def box(name, size, loc, mat, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)  # 스케일 적용
    ob.data.materials.append(mat)
    if parent:
        ob.parent = parent
    return ob


wood = make_mat("MAT-wood", (0.30, 0.18, 0.10), 0.45)
floor_mat = make_mat("MAT-floor", (0.60, 0.60, 0.58), 0.8)

# 3) 바닥 + 테이블(상판 + 다리 4개를 Empty 부모 아래로 묶음: scene_audit의 '유닛' 규약)
box("GEO-floor", (4, 4, 0.02), (0, 0, -0.01), floor_mat)
bpy.ops.object.empty_add(location=(0, 0, 0))
table = bpy.context.active_object
table.name = "dining_table"
W, D, H, T = 1.50, 0.90, 0.75, 0.035          # 4인 식탁 예시 치수(m)
box("GEO-table_top", (W, D, T), (0, 0, H - T / 2), wood, table)
for i, (sx, sy) in enumerate([(1, 1), (1, -1), (-1, 1), (-1, -1)]):
    box(f"GEO-table_leg{i}", (0.07, 0.07, H - T),
        (sx * (W / 2 - 0.10), sy * (D / 2 - 0.10), (H - T) / 2), wood, table)

# 4) 조명·카메라·월드
bpy.ops.object.light_add(type="AREA", location=(2.0, -2.0, 3.0))
key = bpy.context.active_object
key.name = "LGT-key"
key.data.energy = 500
key.data.size = 2.0
key.rotation_euler = (0.9, 0.0, 0.8)
bpy.ops.object.camera_add(location=(3.2, -3.2, 2.2), rotation=(1.15, 0.0, 0.785))
scene.camera = bpy.context.active_object
scene.camera.name = "CAM-main"
if scene.world is None:
    scene.world = bpy.data.worlds.new("World")
if bpy.app.version < (5, 0, 0):
    scene.world.use_nodes = True
bg = next(n for n in scene.world.node_tree.nodes if n.type == "BACKGROUND")
bg.inputs["Color"].default_value = (0.05, 0.05, 0.06, 1.0)

# 5) 렌더 설정: GPU 없는 서버에서는 CYCLES(CPU)
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = samples
scene.render.resolution_x, scene.render.resolution_y = 1280, 720
scene.render.filepath = out_png

# 6) 저장 → 렌더 → 요약 출력(에이전트가 파싱)
bpy.ops.wm.save_as_mainfile(filepath=out_blend)
bpy.ops.render.render(write_still=True)
print("BUILD_RESULT " + json.dumps({
    "blender": bpy.app.version_string,
    "blend": out_blend,
    "png": out_png,
    "objects": len(scene.objects),
}, ensure_ascii=False))
```

- 식탁 치수 1.50×0.90 m, 높이 0.75 m는 예시입니다. 실제 값은 [실측 치수 기준표](05_reference_dimensions.md)에서 가져오세요.
- 실측 스케일, 부모 묶음, 스케일 적용, type 기반 노드 탐색은 이후 `scene_audit.py`가 오탐 없이 동작하기 위한 전제이기도 합니다.

### 3.3 실행과 확인

```bash
# 1) 빌드 + 렌더. --python-exit-code 1이 없으면 스크립트 예외가 나도 종료 코드가 0이라 성공으로 오인합니다
blender -b --factory-startup --python-exit-code 1 -P build_scene.py -- --out renders/v001.png --samples 32

# 2) 숫자 검사: 떠 있음, 관통, 스케일 미적용, 이름 기준 치수 범위 이탈
blender -b renders/v001.blend --python 03_playbooks/scripts/scene_audit.py -- --floor-z 0 --out renders/v001_audit.json
```

```python
# 3) 눈 검사용 4방향 렌더 (build_scene.py 끝이나 별도 스크립트에서)
import sys; sys.path.append("03_playbooks/scripts")
from review_views import render_review_views
paths = render_review_views("renders/review_v001/", engine="CYCLES", samples=16, res=768)
# → top.png, front.png, side.png, persp.png : 오브젝트마다 다른 색이라 겹침·간격이 잘 보임
```

위 예제 씬으로 실행하면 `scene_audit` 요약이 `units_with_issues: 0, interpenetrating_pairs: 0`으로 나오고, 4방향 렌더 4장이 생성됩니다(bpy 5.0.1에서 확인).

- `--factory-startup`은 사용자 애드온과 설정을 불러오지 않습니다. 매번 같은 조건으로 빌드하려는 의도입니다.
- 생성 스크립트는 .blend와 함께 git으로 관리하세요. 에이전트가 나중에 파라미터만 바꿔 다시 빌드할 수 있습니다([blender-agent-studio](https://github.com/ifBars/blender-agent-studio)의 설계 철학).
- 더 큰 구조가 필요하면 [Codex-and-Blender](https://github.com/danielsobrado/Codex-and-Blender)(MIT)처럼 `scene.yaml`(치수·에셋·카메라) → 결정적 bpy → CLI 클린 빌드로 정본을 두고, MCP 라이브 세션은 점검용으로만 씁니다. 합격 기준(`acceptance.yaml`)을 파일로 고정하면 에이전트가 기준을 몰래 낮추지 못합니다.
- 설치된 Blender 없이 API 시그니처만 확인하려면 [fake-bpy-module](https://github.com/nutti/fake-bpy-module)(`pip install fake-bpy-module-5.1` 형식) 스텁을 에이전트에게 grep하게 하세요.

### 3.4 에이전트에게 주는 첫 프롬프트 (Claude Code / Codex 공통)

```text
Blender를 헤드리스로 써서 작업해. MCP는 쓰지 않는다.
1) scripts/build_scene.py를 작성해(1 BU = 1 m, Z-up, 가구는 부모 Empty 아래로 묶기,
   노드는 type으로 찾기, 5.0 미만에서만 use_nodes 설정).
2) blender -b --factory-startup --python-exit-code 1 -P scripts/build_scene.py -- --out renders/v001.png 로 실행해.
   종료 코드가 0이 아니면 traceback 전체를 읽고 고쳐서 다시 실행해.
3) 03_playbooks/scripts/scene_audit.py로 감사하고, review_views.render_review_views로 4방향 렌더를 만들어.
4) PNG를 직접 열어 보고, 스펙 대비 차이를 '부품 / 기대값 / 관찰값 / 수정안' 표로 3줄 이내로 적어.
5) 감사 이슈 0건이고 눈 검사에서 문제가 없을 때까지 v002, v003… 으로 번호를 올리며 반복해.
   숫자 검사를 통과해도 이미지가 틀리면 실패다.
```

### 3.5 자주 나는 오류 (경로 C)

| 증상 | 원인 | 해결 |
|---|---|---|
| 스크립트가 실패했는데 에이전트가 성공이라고 보고 | Blender는 `--python` 예외에도 기본 종료 코드 0([yardstake-ux #151](https://github.com/captproton/yardstake-ux/issues/151)) | `--python-exit-code 1` |
| 리눅스 서버에서 EEVEE 렌더 실패 | GPU/EGL 컨텍스트 없음 | `engine="CYCLES"`, `cycles.device="CPU"` |
| `pip install bpy` 실패 | Python 버전 불일치 | bpy 5.1 이상은 Python 3.13, 5.0은 3.11 venv |
| 인자가 무시됨 | `--` 뒤 인자만 스크립트 몫 | `sys.argv[sys.argv.index("--") + 1:]` |
| 렌더 파일이 엉뚱한 위치에 저장됨 | 상대경로 기준이 실행 위치와 다름 | `os.path.abspath()`로 절대경로 사용 |
| 4.x 예제 코드가 5.x에서 `AttributeError` | API 변경(`scene.node_tree` → `scene.compositing_node_group`, `action.fcurves` 제거, `use_auto_smooth`는 4.1에서 제거 등) | 코드 전에 `bpy.app.version`을 확인하게 하고, [Blender MCP 가이드](../02_guides/02_blender_mcp.md)의 API 함정 표를 스킬에 넣기 |

---

## 4. 경로 D: 게임 엔진 (Unreal 5.8 공식 MCP / Unity)

### 4.1 Unreal Engine 5.8 공식 MCP (Epic, Experimental)

**이럴 때**: 인터랙티브 레벨, 대규모 월드, Lumen·Nanite 환경에서 배치·PCG 산포·조명·포스트를 AI에게 맡길 때. 히어로 에셋의 모델링, 베벨, UV는 Blender(A~C)에서 만들고 엔진에서 조립하는 분업이 권장됩니다.

**준비물**

- UE 5.8. 플러그인 경로는 `Engine/Plugins/Experimental/ModelContextProtocol`입니다. 기본 주소는 `http://127.0.0.1:8000/mcp`입니다([Epic 공식 Claude Code 플러그인 README](https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin)).
- 엔진 빌드 종류는 자료끼리 충돌합니다. [ibrews](https://github.com/ibrews/ue5-mcp/blob/main/SKILL.md)는 소스 빌드가 필요하다고 적었지만, [per-simmons](https://github.com/per-simmons/unreal-agent-harness/blob/master/docs/UNREAL-MCP-ENABLE.md)는 Epic Games Launcher판 5.8로 작업했습니다. ibrews 쪽은 프리뷰 시절 정보로 보입니다.
- Claude Code 또는 Codex. 공식 문서([Unreal MCP in Unreal Editor](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor?lang=en-US))는 조사 환경에서 차단돼 검색 요약만 확인했습니다.

**설치·연결 단계**

1. `.uproject`(또는 Edit > Plugins)에서 **ModelContextProtocol**, **AllToolsets**, **PythonScriptPlugin**을 켭니다. Toolset Registry는 자동으로 켜집니다. **AllToolsets가 없으면 서버가 도구를 하나도 노출하지 않습니다**(Epic README: "the server exposes none without it"). 5.8에서는 두 플러그인이 스스로 켜진다는 보고도 있습니다([UnrealEngine_Bridge](https://github.com/JosephOIbrahim/UnrealEngine_Bridge)). PythonScriptPlugin 필수 여부는 per-simmons 문서에만 있습니다.
2. 에디터를 재시작하고 콘솔(`~`)에서 서버를 띄웁니다. 기본 포트 8000은 다른 프로그램과 자주 충돌하니 8123을 권장합니다.
   ```text
   ModelContextProtocol.StartServer 8123
   ModelContextProtocol.GenerateClientConfig ClaudeCode      (Codex라면: ... GenerateClientConfig Codex)
   ```
   두 번째 명령은 **프로젝트 루트에 `.mcp.json`**을 만듭니다. Claude Code는 그 폴더에서 실행하세요.
3. 자동 시작: `Saved/Config/<Platform>Editor/EditorPerProjectUserSettings.ini`에 아래 키를 넣습니다(섹션 이름과 정확한 위치는 [per-simmons 문서](https://github.com/per-simmons/unreal-agent-harness/blob/master/docs/UNREAL-MCP-ENABLE.md) 참고).
   ```ini
   bAutoStartServer=True
   ServerPortNumber=8123
   ServerUrlPath=/mcp
   ```
4. **Epic 공식 Claude Code 플러그인**(MIT)을 설치합니다. `unreal-mcp` 스킬, SessionStart hook, 에디터를 재시작해도 MCP 세션을 유지해 주는 Experimental 프록시(`Engine/Plugins/Experimental/ModelContextProtocol/Extras/Proxy`)가 들어 있습니다.
   ```text
   /plugin install unreal-engine-skills-for-claude-code@claude-plugins-official
   ```
   Codex용으로는 공식 플러그인을 옮긴 [WildCake/unreal-engine-mcp-codex](https://github.com/WildCake/unreal-engine-mcp-codex) 스킬이 있습니다(헤드리스 러너 로그는 `Saved/AgentRuns/`).

**연결 확인과 첫 테스트**

- Claude Code에서 `/mcp`로 연결을 확인하고 "List all actors in the current level"을 보냅니다(Epic 스킬의 확인 방법).
- 도구는 `tools/list`에 바로 나오지 않는 tool-search 방식입니다. `list_toolsets` → `describe_toolset` → `call_tool` 순서로 부르고, `toolset_name`(예: `"PCGToolset.PCGToolset"`)과 `tool_name`은 따로 넘깁니다. 가장 간단한 호출은 `SceneTools.get_current_level`입니다.

```text
[첫 테스트] 현재 레벨의 액터를 모두 나열하고(수정 금지), 뷰포트를 캡처해서 보여 줘
(EditorAppToolset.CaptureViewport). 그다음 레벨에 StaticMeshActor 'SM_TestCube'를
(0, 0, 50)에 하나만 추가하고, 추가 결과를 다시 읽어 위치를 확인해 줘.
작업 전후로 레벨을 저장해.
```

**운영 규칙**(Epic 스킬 [unreal-mcp SKILL.md](https://raw.githubusercontent.com/EpicGames/unreal-engine-skills-for-claude-code-plugin/main/skills/unreal-mcp/SKILL.md) 기준)

- 대량 변경 전후로 저장하고 커밋합니다. **MCP 편집이 항상 undo되지는 않습니다.**
- 컴파일과 셰이더 작업이 끝날 때까지 기다린 뒤 호출합니다.
- **호출은 직렬로** 보냅니다. 에디터의 게임 스레드는 하나뿐이라, 병렬로 보내면(특히 PCG 실행) 에디터가 멈춥니다.
- 결과는 반드시 다시 읽어 확인합니다. 예외 없이 status만 돌려주는 도구가 많습니다.
- PIE(에디터 내 플레이) 중인지 확인하고 작업합니다.

**보안**

- Epic README 원문 경고: **"Localhost is not a trust boundary."** 서버에는 origin 검증만 있습니다.
- `ProgrammaticToolset.execute_tool_script`는 **임의 Python을 실행**하는 특권 연산입니다. 툴셋 API를 통해 프로젝트 콘텐츠를 바꾸거나 지울 수 있으니 안전한 샌드박스로 다루지 마세요.
- `--dangerously-skip-permissions`를 쓰지 말고, 공유 머신에서 서버를 띄우지 마세요(Epic 권고).
- Python Remote Execution을 쓰지 않는다면 `DefaultEngine.ini`에 `bRemoteExecution=False`를 둡니다(per-simmons 권장).

**자주 나는 오류 (Unreal)**

| 증상 | 원인 | 해결 |
|---|---|---|
| 도구가 하나도 안 보이거나 최소 툴셋만 보임 | AllToolsets 플러그인이 꺼져 있음 | AllToolsets를 켜고 에디터 재시작 |
| 서버 시작 실패 | 포트 8000 충돌 | `StartServer 8123` + ini 자동 시작 |
| 새로 추가한 커스텀 툴이 안 보임 | 새 툴은 에디터를 완전히 재시작해야 반영됨(Live Coding 불가) | 에디터 재시작 |
| 프로젝트를 바꾸자 연결이 끊김 | 프로젝트를 바꾸면 이전 서버가 종료됨 | 다시 StartServer, 또는 ini 자동 시작 |
| 에디터를 재시작할 때마다 세션이 끊김 | 서버가 에디터 프로세스 안에 있음 | Epic 플러그인의 Experimental 프록시 |
| success라는데 실제로 바뀐 게 없음 | 속성 이름 오류(`auto_possess_ai` ✗ → `AutoPossessAI`), Mobility·RelativeLocation은 Actor가 아니라 RootComponent에 있음, BP 클래스 경로의 `_C` 누락 | PascalCase 사용, 쓴 뒤 다시 읽어 비교([ibrews SKILL.md](https://github.com/ibrews/ue5-mcp/blob/main/SKILL.md)) |
| Python `print()` 결과가 에이전트에게 안 돌아옴 | 출력이 엔진 로그로만 감 | 임시 Note 액터의 `tags`에 결과를 쓰고 속성 조회로 읽은 뒤 삭제 |
| 임포트한 FBX가 100배 크기 | Blender와 익스포터의 단위 불일치 | 임포트 직후 bounds 조회로 확인 |

**UE 5.7 이하**: [ChiR24/Unreal_mcp](https://github.com/ChiR24/Unreal_mcp)(MIT, UE 5.0~5.8, Node 20.19 이상, 안정판 0.5.30, 0.6은 beta 태그)가 landscape, foliage, 하늘·날씨 도구까지 가장 폭넓습니다. 플러그인 없이 가볍게 시작하려면 [runreal/unreal-mcp](https://github.com/runreal/unreal-mcp)(`npx -y @runreal/unreal-mcp`, UE 5.4 이상, 도구 20개)가 있습니다. 다만 runreal은 Python **Remote Execution을 켜야** 동작하므로 위 보안 권장과 충돌합니다. 에디터 전체 권한을 넘긴다는 점을 이해하고 쓰세요. 자세한 비교는 [기타 MCP·게임엔진 가이드](../02_guides/03_other_mcp_dcc_cad_engines.md)를 보세요.

### 4.2 Unity

**공식 Unity MCP**(com.unity.ai.assistant 패키지 포함)는 Unity 도메인이 모두 차단돼 설치 절차를 1차 확인하지 못했습니다. 검색 요약에 따르면 Unity 6 이상에서 Edit > Project Settings > AI > Unity MCP의 Unity Bridge가 Running(초록)인지 확인하고 클라이언트를 연결합니다([공식 문서](https://docs.unity3d.com/Packages/com.unity.ai.assistant@2.18/manual/integration/unity-mcp-overview.html), 원문 미열람). 최소 버전은 '6000.0 이상'이라는 요약과 달리, 미러된 구버전 패키지(1.0.0-pre.12)는 6000.2를 요구합니다([needle-mirror](https://github.com/needle-mirror/com.unity.ai.assistant)). **최소 버전과 요금은 미확인**입니다.

그래서 빠른 시작은 커뮤니티 표준 **[CoplayDev MCP for Unity](https://github.com/CoplayDev/unity-mcp)**(MIT, 약 14.5k stars, v10.2.0 2026-09-01, Unity 2021.3 LTS~6.x, 도구 47개)로 안내합니다.

1. Python 3.10 이상을 설치합니다.
2. Unity Package Manager에서 git URL로 패키지를 추가합니다(OpenUPM도 가능).
   ```text
   https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#main
   ```
3. Window → MCP for Unity → **Configure All Detected Clients**를 실행합니다. 설치돼 있는 클라이언트(README 기준 Claude Desktop, VS Code, Cursor, Windsurf, Cline, Gemini CLI 등)를 찾아 설정합니다.
4. (선택) 3D 생성: Window → MCP for Unity → Asset Gen 탭에서 Tripo·Meshy 키를 넣습니다. 키는 OS 키체인에 저장됩니다. `generate_model`과 Sketchfab `import_model`을 쓸 수 있습니다.
5. 연결 확인 예시: "현재 씬의 GameObject 목록을 보여 줘. 수정하지 마."(`manage_scene` 도구 사용을 기대)

- 대안인 [IvanMurzak/Unity-MCP](https://github.com/IvanMurzak/Unity-MCP)(Apache-2.0, 70개 이상 도구)는 오브젝트 하나만 떼어 렌더하는 `screenshot-isolated`가 있어 가구·소품 형태 검수에 좋습니다. OpenUPM(`com.ivanmurzak.unity.mcp`)이나 `npm install -g unity-mcp-cli`로 설치하고, **프로젝트 경로에 공백이 있으면 안 됩니다.**

### 4.3 (참고) Godot

가장 가벼운 시작은 `claude mcp add godot -- npx @coding-solo/godot-mcp`입니다(Node 18 이상, 필요하면 `GODOT_PATH` 지정, [Coding-Solo/godot-mcp](https://github.com/Coding-Solo/godot-mcp)). 시네마틱 카메라 스크린샷이 필요하면 godot-ai(Godot 4.7 이상)를 보세요([기타 MCP·게임엔진 가이드](../02_guides/03_other_mcp_dcc_cad_engines.md)).

---

## 5. MCP 타임아웃 설정 모음

| 위치 | 설정 | 기본값 | 권장 | 비고 |
|---|---|---|---|---|
| ahujasid 서버 | 소켓 타임아웃 | **180초**(server.py 고정값) | 코드 5~20줄 청크 | 클라이언트 타임아웃을 늘려도 호출 하나는 180초를 넘지 못함. 긴 렌더는 경로 C |
| Claude Desktop | 도구 호출 | 약 4분에 포기하는 사례 관찰 | — | 공식 값은 미확인 |
| Claude Code | `MCP_TIMEOUT`(서버 **시작** 타임아웃, ms) | — | 공식 서버 첫 실행 때 120000 정도 | `MCP_TIMEOUT=120000 claude` |
| Claude Code | `.mcp.json` 서버별 `"timeout"`(ms) / `MCP_TOOL_TIMEOUT` | 설정하지 않으면 약 28시간 | stdio 서버는 그대로. HTTP 서버(UE 5.8 등)는 600000 | 호출당 **절대 한도**(진행 알림으로 연장 안 됨). 값을 넣으면 28시간이 그 값으로 줄어듦. 1000 이상이면 유휴 타임아웃의 하한도 겸하고(v2.1.203+), HTTP 서버의 첫 응답 대기(기본 60초)도 이 값까지 늘어남. [Claude Code MCP 문서](https://code.claude.com/docs/en/mcp) |
| Claude Code | `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`(유휴 타임아웃, ms) | stdio 서버 **30분**, HTTP·SSE·WebSocket·claude.ai 커넥터 **5분**(v2.1.203 이전에는 stdio 제외) | 긴 작업 전에 명시적으로 설정, `0`이면 끔 | 응답도 진행 알림도 없이 오래 걸리는 Cycles 렌더·베이크가 끊길 수 있음. 2026-09-27에 공식 문서로 재확인(두 검증 기록의 5분/30분 차이는 전송 방식 차이) |
| Claude Code | `MAX_MCP_OUTPUT_TOKENS` | 25,000(10,000 초과 시 경고) | 50000 | 큰 씬 덤프·스크린샷이 잘릴 때. 이미지도 이 한도에 포함됨 |
| Codex | `startup_timeout_sec` / `tool_timeout_sec` | 10 / 60(원문 미재확인) | 30 / 600 | `[mcp_servers.blender]` 아래 |
| Gemini CLI | `timeout`(ms) | 600,000 | 그대로 | `settings.json`의 `mcpServers` |
| Blender Lab 공식 서버 | 서버 측 타임아웃 | 미확인 | — | 긴 작업은 `_for_cli` 도구나 경로 C |

- 스크린샷이 쌓이는 긴 세션에서는 이미지 한도도 걸립니다. 한 요청의 이미지가 20장을 넘으면(이전 턴과 tool_result 안의 스크린샷 포함) 각 이미지를 긴 변 2000px 이하로 줄여야 합니다([Claude Vision 문서](https://platform.claude.com/docs/en/build-with-claude/vision)). ahujasid `get_viewport_screenshot`은 MCP로 호출하면 기본 `max_size=1000`입니다.

---

## 6. 보안·저장 설정 모음

### 6.1 보안 체크리스트 (모든 경로 공통)

- [ ] 작업 전에 저장하고, 스크립트는 git에 커밋합니다.
- [ ] 서버와 애드온은 `localhost`에만 바인딩합니다. 공유 머신에서는 쓰지 않습니다.
- [ ] B: `BLENDER_MCP_SAFE_MODE=1`, `DISABLE_TELEMETRY=true`, 최신 버전(2.1.0 이상).
- [ ] `--dangerously-skip-permissions`를 쓰지 않습니다. 필요하면 명시적 allow 규칙이나 auto mode를 씁니다.
- [ ] 프로젝트 `.mcp.json`의 서버는 내용을 확인한 뒤 승인합니다. `claude -p`(비대화형) 실행에서는 확인 없이 로드된다는 점을 기억하세요([Claude Code 보안 문서](https://code.claude.com/docs/en/security)).
- [ ] 출처를 모르는 .blend 파일, 에셋 설명, 웹 페이지를 에이전트에게 그대로 넘기지 않습니다(프롬프트 인젝션).
- [ ] 유료 생성 API(Hyper3D, Tripo, Meshy 등)는 호출 전에 사용자 확인을 받게 합니다.
- [ ] 비공식 사이트(blender-mcp.com, blendermcp.org)와 GitHub 복제 저장소에서 애드온을 받지 않습니다.
- [ ] Blender의 Auto Run Python Scripts를 끈 채로 둡니다(악성 .blend 사례, [설치 안전 가이드](../02_guides/14_tool_install_safety.md)).
- [ ] **[한국]** Hunyuan3D 로컬 가중치(ahujasid 로컬 API URL 모드 포함)를 연결하지 않습니다.

### 6.2 저장 습관

```python
import bpy
if not bpy.data.filepath:                       # 처음 한 번은 경로를 지정해 저장
    bpy.ops.wm.save_as_mainfile(filepath=r"C:\work\chair\chair.blend")
bpy.ops.wm.save_mainfile(incremental=True)      # chair.blend → chair1.blend → chair2.blend ...
print("saved:", bpy.data.filepath)
```

- bpy 5.0.1과 4.2.23 LTS에서 `chair.blend → chair1.blend → chair2.blend`로 저장되고, 이후 작업은 새 파일에서 이어지는 것을 확인했습니다. ahujasid safe mode 검증기도 통과합니다(2026-09-25 커밋 기준).
- 현재 파일은 그대로 두고 사본만 남기려면 `bpy.ops.wm.save_as_mainfile(filepath="//versions/scene_v003.blend", copy=True)`를 씁니다.
- **Claude Code의 `/rewind`는 Blender 상태를 되돌리지 못합니다.** 체크포인트는 Claude의 파일 편집 도구로 바꾼 것만 추적합니다([best practices](https://code.claude.com/docs/en/best-practices)). ahujasid 애드온에는 `undo_push` 처리도 없어서, AI가 만든 변경을 Ctrl+Z로 한 단계씩 되돌린다는 보장이 없습니다.
- Unreal: 대량 변경 전후 저장, 세션 시작 전 Git 또는 Perforce 커밋, 에셋 삭제 전 참조 확인.

---

## 7. 연결 후 첫 30분: 이 저장소 자산 붙이기

1. **프로젝트 규칙**: [templates/CLAUDE.md](templates/CLAUDE.md)를 작업 폴더에 복사합니다(Codex는 `AGENTS.md`로 이름만 바꿔 사용). 단위(1 BU = 1 m), 이름 규칙, 금지 작업(orphans_purge, 공장 초기화), 저장 규칙이 들어 있습니다.
2. **스킬**: [templates/skills/blender-aaa-scene/SKILL.md](templates/skills/blender-aaa-scene/SKILL.md)를 `.claude/skills/`에 넣으면 스펙 → 빌드 → 감사 → 검토 루프를 따릅니다.
3. **검사 스크립트**: [scripts/README.md](scripts/README.md)의 사용법 1(MCP)이나 2(헤드리스)로 `scene_audit.py`, `placement_utils.py`, `review_views.py`를 연결합니다.
4. **첫 실전**: [AAA 제작 플레이북](02_aaa_production_playbook.md)의 1단계부터 따라 하고, [프롬프트 템플릿](03_prompt_templates.md)과 [품질 체크리스트](04_quality_checklists.md)를 옆에 둡니다.

---

## 8. 어떤 경로를 고를까 — 결정표

| 상황 | 추천 | 이유 |
|---|---|---|
| 코드를 모르고 가장 쉽게 시작하고 싶다 | **A** | 커넥터 클릭 + 애드온 설치로 끝. 텔레메트리·외부 서비스 연동 없음(조사 기준, 원문 미열람) |
| Blender 5.0 이하를 써야 한다 | **B** 또는 **C** | 공식 서버는 5.1.0 이상 |
| 에셋 검색(Poly Haven·Sketchfab·Poly Pizza)이나 AI 3D 생성을 에이전트가 직접 해야 한다 | **B** | 공식 서버에는 없음. Tripo는 Premium 전용 |
| GPT-6 Astra를 쓰고 싶다 | **B**(Codex) 또는 **C** | ChatGPT 웹은 로컬 MCP 불가. effort를 high 이상으로 명시 |
| 씬 분석, 누락 텍스처 찾기, 문서 기반 스크립트, 대량 일괄 수정 | **A** | .blend 포렌식과 API·매뉴얼 문서 도구가 강점 |
| 결과를 재현하고 git으로 관리, CI 배치 렌더 | **C** | 스크립트가 곧 소스. 소켓 타임아웃 없음 |
| 렌더·베이크가 3분 넘게 걸린다 | **C** | ahujasid 호출당 180초 상한 |
| Windows에서 B가 계속 타임아웃된다 | **A** 또는 **C** | #339·#357이 열려 있음 |
| 보안 요구가 엄격하다(사내 자산) | **C**, 또는 A + 저장 규칙 | C는 열린 포트가 없음. B를 써야 하면 safe mode + 텔레메트리 끄기 + blend-ai 검토 |
| 인터랙티브 게임 레벨, 대규모 월드, Lumen·PCG | **D**(UE 5.8) | 배치·산포·조명은 엔진에서, 히어로 에셋은 Blender에서 |
| Unity 프로젝트 | **D**(CoplayDev) | 공식 Unity MCP는 요구 사항 미확인 |
| Geometry Nodes·셰이더 노드를 AI가 직접 편집 | B 계열 포크 [newo-ether](https://github.com/newo-ether/blender-mcp) | validate → apply → verify 트랜잭션 도구 |
| 로컬 LLM만 써야 한다 | A의 HTTP 모드 + llama.cpp | 기대치는 '분석과 간단한 편집' 정도([Blender MCP 가이드](../02_guides/02_blender_mcp.md)) |
| AAA급 결과물을 목표로 한다 | **A 또는 B로 대화형 제작 + C로 최종 빌드·렌더 + 사람의 마무리** | 독립적으로 검증된 'AAA급' AI+MCP 결과물은 찾지 못했습니다. 고품질은 에셋·생성 모델 + 에이전트 조립 + 검증 루프 + 사람의 마무리를 합친 하이브리드에서 나옵니다 |

**한 줄 판단**: 처음이면 A(5.1 이상) 또는 B로 연결만 확인하고, 첫 작품부터 C의 빌드 스크립트와 `scene_audit.py`를 같이 쓰세요. AI는 '감독이 필요한 협업자'로 두는 것이 현실적입니다.

---

## 흔한 실수와 해결

| 실수 | 결과 | 해결 |
|---|---|---|
| 공식 커넥터와 ahujasid 애드온을 동시에 켬 | 9876 충돌. 엉뚱한 서버에 연결되거나 연결 실패 | 한 번에 하나만. 포트를 나누거나 애드온을 끔 |
| `uvx blender-mcp`를 공식 서버로 착각 | 커뮤니티 서버가 설치됨 | 공식 서버는 git 소스(1.5절) |
| MCP 서버를 터미널에서 따로 실행 | 인스턴스 중복, 연결 꼬임 | 클라이언트에만 맡김 |
| Codex에서 effort를 지정하지 않음 | GPT-6 Astra가 `low`로 돌아 품질이 낮게 나옴 | `model_reasoning_effort = "high"` 이상 |
| 긴 렌더를 MCP 한 번으로 호출 | 180초나 유휴 타임아웃에 끊김 | 청크로 나누고, 렌더는 헤드리스로 |
| safe mode를 샌드박스로 믿음 | 로컬 다른 프로세스의 코드는 그대로 실행됨 | 신뢰하지 않는 입력 금지, 필요하면 blend-ai |
| `DISABLE_TELEMETRY`를 안 켬 | 익명 사용 기록이 기본 수집됨 | `DISABLE_TELEMETRY=true` |
| `/rewind`를 믿고 저장 안 함 | Blender 변경은 복구 불가 | `save_mainfile(incremental=True)` |
| 한국어 UI에서 노드를 이름으로 찾음 | `KeyError` | type으로 찾기, 영어 UI 또는 New Data 번역 끄기 |
| 헤드리스에서 `--python-exit-code 1` 누락 | 실패를 성공으로 오인 | 항상 붙이기 |
| UE 공식 MCP에서 AllToolsets를 안 켬 | 도구 0개 | AllToolsets 활성화 |
| UE MCP 호출을 병렬로 보냄 | 에디터 멈춤 | 직렬화 |
| 한국에서 Hunyuan3D 로컬 가중치 사용 | 라이선스 범위 밖 | 다른 생성 모델이나 에셋 라이브러리 사용 |

---

## 관련 문서

- [README (읽는 순서)](../README.md) · [목적·범위](../00_purpose/purpose_and_scope.md) · [조사 방법·신뢰도](../01_research/research_method.md) · [출처 카탈로그](../01_research/sources_catalog.md) · [교차검증 로그](../01_research/verification_log.md)
- [AI 모델·클라이언트·비용](../02_guides/01_ai_models_and_clients.md): 모델 선택, effort, 클라이언트별 제한
- [Blender MCP 생태계](../02_guides/02_blender_mcp.md): 공식 vs ahujasid 상세, 대안 서버, API 버전 함정
- [기타 DCC·CAD·게임엔진 MCP](../02_guides/03_other_mcp_dcc_cad_engines.md): Unreal·Unity·Godot 상세
- [에이전트 워크플로·프롬프팅](../02_guides/09_agent_workflow_prompting.md): 시각 피드백 루프, 스킬·hooks, 토큰·비용
- [에셋·파이프라인·라이선스](../02_guides/10_assets_pipeline_licensing.md): Hunyuan3D 한국 제외 등
- [AAA 제작 플레이북](02_aaa_production_playbook.md) · [프롬프트 템플릿](03_prompt_templates.md) · [품질 체크리스트](04_quality_checklists.md) · [실측 치수 기준표](05_reference_dimensions.md)
- [CLAUDE.md 템플릿](templates/CLAUDE.md) · [스킬 템플릿](templates/skills/blender-aaa-scene/SKILL.md) · [보조 스크립트](scripts/README.md)
- [사례 모음](../04_case_studies/01_case_studies.md) · [한국어 자료](../04_case_studies/02_korean_resources.md) · [진행 상태](../05_handoff/status_and_next_steps.md)

## 원자료

- [`01_research/raw/02_blender-mcp.research.json`](../01_research/raw/02_blender-mcp.research.json), [`02_blender-mcp.verify.json`](../01_research/raw/02_blender-mcp.verify.json): 공식·커뮤니티 서버 설치, 포트, safe mode·텔레메트리 정정, 공식 서버 manifest(5.1.0, GPL), Allow Online Access 보고
- [`01_research/raw/01_ai-models.research.json`](../01_research/raw/01_ai-models.research.json), [`01_ai-models.verify.json`](../01_research/raw/01_ai-models.verify.json): 클라이언트 설정, Codex effort 6단계와 기본 low, 공식 서버 git 설치, Claude Code 버전 요구
- [`01_research/raw/04_engine-mcp.research.json`](../01_research/raw/04_engine-mcp.research.json), [`04_engine-mcp.verify.json`](../01_research/raw/04_engine-mcp.verify.json): UE 5.8 공식 MCP 절차, Epic 플러그인, Unity·Godot 서버
- [`01_research/raw/10_agent-workflow.research.json`](../01_research/raw/10_agent-workflow.research.json), [`10_agent-workflow.verify.json`](../01_research/raw/10_agent-workflow.verify.json): 헤드리스 방식, 저장 습관, safe mode 범위, 타임아웃, 한국어 UI 노드 이름 문제
- 이 문서의 코드(`build_scene.py`, get-or-create 테스트, 증분 저장, scene_audit·review_views 연동)는 작성 중 pip `bpy` 5.0.1과 4.2.23 LTS(헤드리스)에서 실행해 확인했습니다. 설치 명령 중 '조합 예시'와 '미검증'으로 표시한 것은 실행하지 않았습니다.
