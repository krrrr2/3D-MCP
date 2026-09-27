# Blender MCP 생태계 가이드

> 기준일: 2026-09-27 · Blender를 AI에 붙이는 길은 크게 둘입니다. 분석·문서 중심의 **공식 Blender Lab 서버**(Blender 5.1+)와 에셋·생성 중심의 **ahujasid MCP for Blender**(36 tool)입니다. 결과 품질은 어느 서버를 쓰느냐보다 스킬 규칙, 검증 루프, 버전별 API 지식에서 더 크게 갈립니다.

## 핵심 요약

- **공식 서버와 ahujasid는 다른 프로젝트입니다.** Claude의 공식 'Blender' 커넥터는 Blender 개발 조직인 Blender Lab이 만들었습니다(2026-04-28 발표, 커넥터 페이지 표기 v1.0.1, 최신 릴리스 v1.0.3(2026-09-11), Anthropic verified, GPL-3.0-or-later, 애드온 manifest `blender_version_min = 5.1.0`). ahujasid 'MCP for Blender'(구 blender-mcp)는 커뮤니티 프로젝트입니다(MIT, 약 29.4k stars, PyPI `mcp-for-blender` 2.1.0, 2026-09-25).
- **용도도 다릅니다.** 공식 서버는 작고 보수적입니다(.blend 분석, API·매뉴얼 문서, 스크린샷, 코드 실행). 에셋 다운로드나 AI 3D 생성 기능은 없습니다. ahujasid는 36개 tool로 Poly Haven·Sketchfab·Poly Pizza 에셋, Hyper3D Rodin·Hunyuan3D·Tripo 생성, GLB/FBX export까지 다룹니다. 단 Tripo는 유료 Premium 전용입니다.
- **공식 서버는 실제로 띄워서 확인했습니다**(4절). 도구는 26개입니다. v1.0.0 계열은 MCP 파이썬 SDK 2.x(2026-07-28~)와 맞지 않아 새로 설치하면 시작하자마자 죽으므로 **v1.0.2 이상**을 쓰거나 `mcp<2`를 고정하세요. 그 밖에 알아 둘 점은 이렇습니다. Allow Online Access가 필수입니다. 오류는 정상 응답 속 `status: "error"`로 옵니다. 렌더 결과는 Blender 임시 폴더에 저장돼 종료하면 사라집니다. GPU 없는 서버에서 EEVEE 렌더를 부르면 Blender가 죽습니다. 코드 실행 보호는 '샌드박스가 아니다'라고 스스로 밝힌 수준이고, HTTP 모드(`:8000`)는 CORS 전체 허용에 인증이 없습니다.
- **두 서버 모두 기본 포트가 `localhost:9876`이라 동시에 켜면 충돌합니다.** Scenario for Blender의 내장 MCP도 9876을 써서 세 개가 겹칠 수도 있습니다. 이름도 헷갈립니다. `uvx blender-mcp`는 이름과 달리 커뮤니티 서버(호환 래퍼)를 실행합니다.
- **자주 걸리는 운영 함정이 세 가지 있습니다.** ① ahujasid 소켓 타임아웃은 180초인데 애드온의 `exec()`에는 제한이 없어서, 긴 코드는 Blender를 멈춥니다. ② `get_scene_info`는 오브젝트 10개의 이름·타입·위치만 반환합니다. ③ tool 스키마만 6,928토큰입니다(28 tool 시점 측정값이고, 지금은 36개라 더 큽니다).
- **보안에 주의하세요.** `execute_blender_code`는 임의 Python을 실행하므로 사실상 OS 권한을 넘기는 것과 같습니다. `BLENDER_MCP_SAFE_MODE=1`은 MCP 경로만 검사하는 제한 장치일 뿐 **샌드박스가 아닙니다**. 익명 사용 텔레메트리가 기본으로 켜져 있으니 `DISABLE_TELEMETRY=true`를 권장합니다. CVE-2026-10661(Low) 이력도 있습니다.
- **LLM이 자주 틀리는 코드**: Principled BSDF v2 소켓 이름(4.0), `use_auto_smooth` 제거(**4.1**), EEVEE 식별자(4.2~4.x는 `BLENDER_EEVEE_NEXT`, 5.0부터 `BLENDER_EEVEE`), `scene.node_tree`→`compositing_node_group`(5.0), `action.fcurves` 제거(5.0), `use_nodes` 폐기 예고(5.0). 가장 싼 해결책은 코드를 쓰기 전에 `bpy_api_lookup`·`describe_node_type`으로 API를 **조회**하게 하는 것입니다.
- **[한국 사용자 주의]** Blender를 한국어 UI로 쓰면 새로 만든 노드 이름이 번역될 수 있어서 `nodes['Principled BSDF']` 같은 코드가 깨집니다(일본어 UI에서 확인됐고, 한국어도 같은 원리로 추정). 노드는 `type`으로 찾게 하고, Preferences > Interface > Translation에서 **New Data**를 끄거나 영어 UI를 쓰세요. 로컬 Hunyuan3D 백엔드는 **한국이 라이선스 적용 지역에서 빠져 있습니다.**
- **대안 서버**: 노드 편집에는 newo-ether 포크, 임의 코드를 막으려면 blend-ai(AGPL), 결정적 배치 검증에는 blender-ai-mcp, 로컬 LLM에는 공식 서버+llama.cpp 또는 blender-open-mcp가 맞습니다. 재현성과 CI가 중요하면 헤드리스 실행(`blender -b ... --python-exit-code 1`)을 쓰세요.
- **품질은 스킬 레이어에서 올라갑니다.** cc-blender-skill(30 skills: 실측 치수, 베벨, 조명 비율, QA 게이트)이나 공식 서버용 ra100 플러그인 같은 규칙 묶음을 쓰고, 이 저장소의 [검증 스크립트](../03_playbooks/scripts/README.md)(`scene_audit.py`·`placement_utils.py`·`review_views.py`·`building_audit.py`, Blender 4.2.23 LTS·5.0.1·5.2.2 LTS 테스트 통과)를 함께 돌리세요.

---

## 1. 어떤 서버를 고를까 (용도별)

| 상황 | 1순위 | 대안 | 이유 |
|---|---|---|---|
| Claude Desktop에서 가장 쉽게 쓰고 싶음 (Blender 5.1 이상. 로컬 앱이라 claude.ai 웹에서는 붙지 않음) | 공식 Blender 커넥터 | ahujasid | Anthropic 인증. 조사 기준으로 텔레메트리·외부 서비스 연동 없음 |
| 씬 분석·디버깅, 큰 .blend 점검(누락 텍스처, 링크 라이브러리) | 공식 서버 (`get_blendfile_summary_*`, `*_for_cli`) | — | GUI 없이 저장 파일을 분석 가능 |
| HDRI·텍스처·모델 에셋과 AI 3D 생성을 한 서버에서 | ahujasid | 공식 서버 + Meshy/Tripo MCP | 에셋·생성 tool 내장 |
| Codex(GPT-6 Astra) 사용 | ahujasid (README에 Codex 설정 있음) | 공식 서버 수동 설정, 헤드리스(Blender Agent Studio) | 2026-09에 'GPT Astra용 권장 서버' 질문이 올라옴([#351](https://github.com/ahujasid/blender-mcp/issues/351)) |
| Blender 4.2/4.5 LTS를 써야 함 | ahujasid(3.0+), blend-ai(4.2+) | newo-ether(4.2.22에서 테스트) | 공식 서버는 5.1 미만 불가 |
| 셰이더·Geometry Nodes 그래프 편집 | newo-ether 포크 | ra100 스킬(공식 서버용 노드 레퍼런스) | validate→apply→verify 트랜잭션 방식 |
| 임의 Python 실행이 불안함 | blend-ai | Scenario 내장 MCP(Python 실행 기본 OFF), 헤드리스 QA 분리 | 위험 import 차단 샌드박스 |
| 가구·배치를 수치로 검증 | 이 저장소 `scene_audit.py` (어느 서버에서나 동작) | blender-ai-mcp, glonorce BVH 검사 | 스크린샷만으로는 관통·부유를 놓침 |
| 씬을 클라우드로 보낼 수 없음(로컬 LLM) | 공식 서버 + llama.cpp | blender-open-mcp | 로컬 모델의 bpy 정확도는 낮으니 기대치를 낮출 것 |
| 재현성·대량 렌더·CI | 헤드리스 `blender -b` | sandraschi 헤드리스 MCP, better-blender-mcp 백그라운드 워커 | 소켓 타임아웃과 GUI 멈춤이 없음 |

**조합 예 (AAA 소품 제작)**: ① 스펙·실측 치수 확정 → ② ahujasid로 Poly Haven HDRI·텍스처 확보(또는 Meshy MCP로 생성) → ③ cc-blender-skill 규칙으로 하드서피스 모델링 → ④ 노드 그래프는 newo-ether → ⑤ StableGen으로 텍스처 보강 → ⑥ `scene_audit.py`와 `review_views.py`로 검증 → ⑦ 헤드리스로 최종 렌더. 한 Blender에는 **한 번에 서버 하나만** 붙이세요(포트 충돌, 9.1절 참고).

---

## 2. 공식 Blender Lab 서버 vs ahujasid MCP for Blender

### 2.1 비교표

| 항목 | Blender Lab 공식 서버 (= Claude 'Blender' 커넥터) | ahujasid MCP for Blender |
|---|---|---|
| 만든 곳 | Blender Foundation 내부 혁신 조직 Blender Lab([2025-11 출범](https://www.cgchannel.com/2025/11/blender-foundation-launches-the-blender-lab/)). Anthropic 발표문의 표현은 "The Blender developers have created an MCP connector"입니다 | Siddharth Ahuja(커뮤니티). README에 "not made by Blender"라고 명시 |
| Claude 커넥터 | 공식 커넥터([커넥터 페이지](https://claude.com/connectors/blender): Made by Blender Lab, v1.0.1, 2026-04 등록, Anthropic verified) | 아님. MCP를 직접 설정 |
| 소스·배포 | [projects.blender.org/lab/blender_mcp](https://projects.blender.org/lab/blender_mcp)(git 소스, .mcpb 번들), GitHub 미러 [bpype/blender_mcp](https://github.com/bpype/blender_mcp) | [GitHub](https://github.com/ahujasid/blender-mcp), PyPI [`mcp-for-blender`](https://pypi.org/project/mcp-for-blender/) |
| 라이선스 | GPL-3.0-or-later ([manifest](https://raw.githubusercontent.com/bpype/blender_mcp/main/addon/blender_mcp_addon/blender_manifest.toml)) | MIT (무료, 유료 Premium 티어 별도) |
| 버전 | v1.0.0 = 2026-04-27(미러 커밋). v1.0.2(2026-09-08, MCP SDK <2 고정)·v1.0.3(2026-09-11, 스크린샷 수정)은 [릴리스 페이지](https://projects.blender.org/lab/blender_mcp/releases) 검색 요약 기준. **Claude 커넥터 페이지는 2026-09-27에도 v1.0.1**(직접 확인) | 2.1.0 (2026-09-25). GitHub Releases 없이 롤링 배포 |
| Blender 요구 | **5.1.0 이상**(manifest `blender_version_min`) | 3.0 이상, Python 3.10+, uv |
| 구조 | MCP 클라이언트 ⇄ stdio ⇄ MCP 서버 프로세스 ⇄ TCP `localhost:9876`(null-byte 구분 JSON) ⇄ 애드온(GUI는 `bpy.app.timers`, 백그라운드는 `--command blender_mcp`). HTTP 전송도 지원(기본 `127.0.0.1:8000`) | MCP 클라이언트 ⇄ stdio ⇄ FastMCP 서버 ⇄ TCP `localhost:9876`(JSON `{type, params}`) ⇄ 애드온(`bpy.app.timers` 큐로 메인 스레드에서 실행) |
| tool 수 | **26개**(실측. README 목록 24개 + `search_api_docs`·`search_manual_docs`), prompt·resource 없음 | 36개 + prompt 1개 (`asset_creation_strategy`) |
| 강점 | .blend 포렌식, 번들 API 문서 조회, 백그라운드(`_for_cli`) 분석, 노드·모디파이어 설명, 일괄 수정, 미사용 데이터 정리, 애드온(UI 도구) 작성 | 에셋 라이브러리, AI 3D 생성, GLB/FBX export, API 조회 tool, 가장 넓은 클라이언트 지원(Claude Desktop/Code, Cursor, VS Code, Codex, OpenCode, Antigravity) |
| 없는 것 | 에셋 다운로드, 3D 생성 → 다른 MCP로 보완 | undo 처리, 큰 씬 요약(10개 제한) |
| 텔레메트리 | 없음(소스에 외부 네트워크 호출 코드 없음, 미러 소스 기준) | 익명 사용 기록 기본 ON, 콘텐츠 수집은 opt-in (10.3절) |
| 코드 실행 보호 | 약한 차단뿐(`sys.exit`·`wm.quit_blender`·설정 초기화 등만 막음, 소스에 "this isn't really a sandbox"). 애드온은 Allow Online Access가 꺼져 있으면 시작하지 않음(실측, [scenario-labs #3](https://github.com/scenario-labs/blender-plugin/issues/3) 보고와 일치) | safe mode (MCP 경로만 검사, 10.2절) |
| 맞는 작업 | 분석·디버깅·문서 기반 코딩·일괄 수정 | 에셋 조립과 생성 파이프라인, 빠른 씬 구성 |

배경: Anthropic은 2026-04-28 ['Claude for Creative Work'](https://www.anthropic.com/news/claude-for-creative-work)에서 크리에이티브 커넥터 9종(Ableton, Adobe for creativity, Affinity by Canva, Autodesk Fusion, Blender, Resolume Arena, Resolume Wire, SketchUp, Splice)을 발표했습니다. 3D와 직접 관련된 것은 Blender, Fusion, SketchUp입니다(나머지는 [기타 DCC·CAD 가이드](03_other_mcp_dcc_cad_engines.md)). 발표문에는 "커넥터로 Blender 인터페이스에 새 도구를 직접 추가할 수 있다"와 "다른 LLM에서도 쓸 수 있다"는 설명도 있습니다. Blender는 Anthropic의 후원을 Development Fund가 아닌 **일회성 기부**로 받았습니다(2026-05-01 수정).

### 2.2 이름 혼동 정리

| 보이는 이름 | 실제로 무엇인가 |
|---|---|
| `uvx mcp-for-blender` | ahujasid 커뮤니티 서버(현재 이름) |
| `uvx blender-mcp` (PyPI [blender-mcp](https://pypi.org/project/blender-mcp/) 2.0.0, 2026-09-16) | ahujasid의 **호환 래퍼**. 설치하면 mcp-for-blender가 깔립니다. **공식 서버가 아닙니다** |
| 실행 파일 `blender-mcp` (git 소스 `.../lab/blender_mcp.git`의 `mcp` 하위 폴더) | 공식 Blender Lab 서버. ahujasid의 옛 PyPI 이름과 같아서 혼동하기 쉽습니다 |
| blender-mcp.com, blendermcp.org | **비공식 사이트**. 여기서 받은 애드온 때문에 증상이 꼬인 사례가 있습니다([#339](https://github.com/ahujasid/blender-mcp/issues/339)). 설치 출처로 쓰지 마세요 |
| PyPI `mcp-blender` | 다른 개발자(brnv)의 별개 패키지. RFingAdam/mcp-blender와 무관합니다(5.1절) |
| 3D-Agent | 상용 제품이고 공식 커넥터와 무관합니다. 자사 마케팅 자료뿐이라 독립 검증이 안 됐습니다 |

ahujasid는 2026-09-16에 "공식이 아님을 분명히 하려고" 패키지 이름을 `mcp-for-blender`로 바꿨습니다. 기존 `uvx blender-mcp` 설정도 계속 동작합니다.

### 2.3 ahujasid에서 공식 서버로 옮길 때 tool 이름 매핑

스킬이나 프롬프트가 ahujasid tool 이름을 쓰고 있다면 다음처럼 바꿔야 합니다(출처: cc-blender-skill [PR #1](https://github.com/RobLe3/cc-blender-skill/pull/1), 제3자가 올린 Open PR).

| ahujasid | 공식 Blender Lab |
|---|---|
| `get_scene_info` | `get_objects_summary` |
| `get_object_info` | `get_object_detail_summary` |
| `get_viewport_screenshot` | `get_screenshot_of_area_as_image` |

---

## 3. ahujasid MCP for Blender: 36개 tool 분류

근거: [server.py](https://raw.githubusercontent.com/ahujasid/blender-mcp/main/src/blender_mcp/server.py)의 `@mcp.tool` 36개와 [addon.py](https://raw.githubusercontent.com/ahujasid/blender-mcp/main/addon.py) (2026-09 기준, 검증 에이전트가 직접 셈). 그룹 안의 정확한 tool 이름은 server.py를 확인하세요.

### 3.1 tool 분류표

| 그룹 | 수 | tool (확인된 이름 중심) | 용도 | 쓸 때 주의 |
|---|---|---|---|---|
| 상태·설정 | 2 | `get_addon_status`, `disable_telemetry` | 연결 상태, 통합(에셋·생성) 활성화 여부, 텔레메트리 끄기 | 세션을 시작하면 먼저 호출해 Blender 버전과 통합 상태를 확인 |
| 씬 조회 | 2 | `get_scene_info`, `get_object_info` | 씬 개요 / 오브젝트 상세 | `get_scene_info`는 **10개까지만**, 필드는 name·type·location(소수 2자리)뿐이고 치수가 없음. 치수는 `get_object_info`의 `world_bounding_box`로 확인 |
| 시각 확인 | 1 | `get_viewport_screenshot(max_size)` | 뷰포트 캡처 | MCP tool 기본값은 `max_size=1000`(docstring의 800은 오기). 16:9 기준 약 1000×563 = 756 이미지 토큰 |
| 코드 실행 | 1 | `execute_blender_code` | 임의 bpy 코드 실행 | 호출마다 새 namespace(`exec(code, {'bpy': bpy})`). 애드온 쪽 타임아웃 없음. 5~20줄 청크 권장 |
| API 조회 | 2 | `bpy_api_lookup`, `describe_node_type` | RNA 시그니처 JSON, 노드 소켓 스키마 | **노드·enum 코드 전에 반드시 호출**(11.3절) |
| Poly Haven | 6 | `get_polyhaven_categories`, `search_polyhaven_assets`, 미리보기, 다운로드, `set_texture`, `get_polyhaven_status` | CC0 HDRI·텍스처·모델(약 2,400개) | 다운로드가 메인 스레드에서 돌아 고해상도는 Blender를 멈춤. 카메라에서 멀면 1k/2k로 |
| Sketchfab | 4 | `get_sketchfab_status`, 검색·미리보기·다운로드 | Sketchfab 모델 | API 키 필요. 모델마다 라이선스가 다름 |
| Poly Pizza | 3 | 상태·검색·다운로드 | 로우폴리 약 10,600개 | 약 69%가 CC-BY라 저작자 표기 의무가 있음. attribution이 커스텀 속성(`polypizza_attribution`)으로 저장됨. `licence='CC0'` 필터로 표기 의무를 피할 수 있음. `target_size`·`normalize_size`로 실제 스케일에 맞출 것 |
| Hyper3D Rodin | 5 | `generate_hyper3d_model_via_text`, 이미지 기반 생성, 폴링, 임포트 | Text/Image-to-3D | 무료 체험 키는 하루 생성 수가 제한됨 |
| Hunyuan3D | 4 | `generate_hunyuan3d_model` 등 | Text/Image-to-3D | **[한국 주의]** 로컬 가중치 사용은 라이선스 범위 밖(3.3절). `input_image_url` 관련 CVE 이력(10.1절) |
| Tripo | 4 | `generate_tripo_model` 등 | Text/Image-to-3D | **Premium 전용**("Tripo is only available with MCP for Blender Premium") |
| 내보내기 | 1 | `export_scene` | GLB/FBX export | 게임레디 검사는 [에셋 파이프라인](10_assets_pipeline_licensing.md) 참고 |
| 피드백 | 1 | `record_trajectory_feedback` | 사용자의 수락·거절·수정을 기록 | 텔레메트리 콘텐츠 수집과 연결되니 동작을 이해하고 쓸 것 |
| **합계** | **36** | | | |

### 3.2 서버가 모델에 주입하는 규칙

ahujasid 서버는 FastMCP `instructions`와 prompt로 모델에게 다음 규칙을 직접 넣습니다. 다른 서버를 쓸 때도 그대로 가져다 쓸 만합니다.

- 노드는 이름이 아니라 **type으로 찾을 것**(UI 현지화 대응, 12절).
- enum 식별자를 하드코딩하지 말고 **런타임에 `enum_items`를 읽을 것**. 예외는 `scene.render.engine`인데, 애드온 엔진이 RNA enum에 없기 때문입니다.
- `material.diffuse_color`는 **뷰포트 표시 전용**입니다. 렌더 색은 셰이더 노드 입력으로 설정해야 합니다.
- `asset_creation_strategy` prompt: 작업 전에 항상 `get_scene_info`를 먼저 호출하고, 변경 전후로 `get_viewport_screenshot`을 찍고, 새로 생성하기 전에 기존 에셋을 먼저 검색합니다.
- `execute_blender_code` docstring: "step-by-step by breaking it into smaller chunks".

### 3.3 무료(BYOK) vs Premium

| 통합 | 자기 키(BYOK) | Premium 키 | 비고 |
|---|---|---|---|
| Poly Haven | 키 불필요 | — | CC0 |
| Sketchfab | `BLENDERMCP_SKETCHFAB_API_KEY` | — | 모델별 라이선스 확인 |
| Poly Pizza | 가능(`BLENDERMCP_POLYPIZZA_*`, 정확한 이름은 README) | — | CC-BY 표기 |
| Hyper3D Rodin | 가능(`BLENDERMCP_HYPER3D_*`) | 가능 | 체험 키 일일 한도 |
| Hunyuan3D | Tencent Cloud 키(SECRET_ID·SECRET_KEY) 또는 로컬 API URL | 가능 | **[한국 주의]** 아래 참고 |
| Tripo | **불가** | 전용 | 대안: [Tripo Python SDK](https://pypi.org/project/tripo3d/)나 ComfyUI 노드. 공식 [tripo-mcp](https://github.com/VAST-AI-Research/tripo-mcp)는 마지막 커밋 2025-04-14로 사실상 방치(비권장) |

- Premium은 2026-09-25 커밋('feat: integrate premium')으로 추가됐습니다. 기기 3대 활성화, 월 쿼터, Pro 플랜의 고품질 모델 제한이 있고, **가격은 확인하지 못했습니다**([Premium 페이지](https://www.mcp-for-blender.com/premium)).
- **[한국 주의] Hunyuan3D 라이선스**: Tencent Hunyuan3D 계열 오픈웨이트 라이선스([Hunyuan3D-2 LICENSE](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/LICENSE))의 적용 지역은 "worldwide, excluding the European Union, United Kingdom and South Korea"이고, 출력물 사용도 제한합니다. 따라서 **한국에서 로컬 가중치로 돌리는 것(ahujasid 로컬 API URL 모드, RFingAdam 로컬 백엔드, Hunyuan3D-2 공식 Blender 애드온 등)은 라이선스 범위 밖입니다.** Tencent Cloud API 경유 사용은 별도 약관을 따르는데, 그 원문은 확인하지 못했습니다. 자세한 내용은 [에셋·라이선스 가이드](10_assets_pipeline_licensing.md)를 보세요.

### 3.4 설치와 클라이언트 설정 요약

자세한 절차는 [빠른 시작](../03_playbooks/01_quickstart_setup.md)을 보세요. 핵심만 적으면 이렇습니다(README 기준).

1. `uvx mcp-for-blender install-addon`을 실행하거나 `addon.py`를 수동 설치합니다. uv는 공식 설치 스크립트로 설치하고, `pip install uv`는 권장하지 않습니다.
2. Edit > Preferences > Add-ons에서 'MCP for Blender'를 켭니다.
3. 3D 뷰포트에서 N 키 → 'MCP for Blender' 탭 → Start MCP Server를 누릅니다.
4. 클라이언트를 설정합니다. **uvx 서버를 터미널에서 따로 실행하지 마세요.** 클라이언트가 직접 띄웁니다.

```jsonc
// Claude Desktop: claude_desktop_config.json (프로젝트 .mcp.json도 같은 형식)
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["mcp-for-blender"],
      "env": { "DISABLE_TELEMETRY": "true", "BLENDER_MCP_SAFE_MODE": "1" }
    }
  }
}
```

```bash
# Claude Code (README 표기는 `--` 없이 쓰지만, 공식 문서는 옵션과 서버 명령을 `--`로 구분하라고 권장.
# --env 바로 뒤에 서버 이름을 두면 이름을 KEY=value로 읽으므로 --transport를 사이에 둠)
claude mcp add --env DISABLE_TELEMETRY=true --transport stdio blender -- uvx mcp-for-blender
# Codex CLI (Codex Desktop은 Settings → MCP servers → STDIO → uvx mcp-for-blender)
codex mcp add blender --env DISABLE_TELEMETRY=true -- uvx mcp-for-blender
```

```toml
# Codex: ~/.codex/config.toml
[mcp_servers.blender]
command = "uvx"
args = ["mcp-for-blender"]
env = { DISABLE_TELEMETRY = "true" }   # 조사 요약 기준. Codex 공식 문서(developers.openai.com)는 이번에 직접 열람하지 못함
tool_timeout_sec = 600
```

- Cursor(Windows)는 `"command": "cmd", "args": ["/c", "uvx", "mcp-for-blender"]`로 설정합니다.
- **Blender를 두 개 띄울 때**는 두 번째 서버를 `"args": ["mcp-for-blender", "--port", "9877"]`로 추가하고, 두 번째 Blender의 애드온 포트도 9877로 맞춥니다. blender-mcp-pro 기본 포트와 겹치니 주의하세요.
- Codex에서 GPT-6 Astra를 쓸 때는 reasoning effort 기본값이 low입니다. 작업에 맞게 명시하세요([모델 가이드](01_ai_models_and_clients.md)).

### 3.5 환경변수

| 변수 | 기본값 | 권장 | 설명 |
|---|---|---|---|
| `BLENDER_HOST` | `localhost` | 그대로 | 외부에 노출하지 말 것. 원격 Blender는 SSH 터널로 |
| `BLENDER_PORT` | `9876` | 충돌하면 변경 | 애드온 포트와 같아야 함 |
| `BLENDER_MCP_SAFE_MODE` | 꺼짐 | `1` | 직접 파일 I/O, 프로세스, 네트워크를 차단(10.2절) |
| `DISABLE_TELEMETRY` | 꺼짐(=수집) | `true` | 익명 사용 기록까지 전부 끔 |
| Sketchfab·Poly Pizza·Hyper3D·Hunyuan3D 키 | — | 필요할 때만 | 유료 생성 전에는 사용자 확인을 받게 할 것 |

---

## 4. 공식 Blender Lab 서버 상세

2026-09-27에 공식 서버를 **소스 전체를 읽고 실제로 띄워서** 확인했습니다. 소스는 GitHub 미러 [bpype/blender_mcp](https://github.com/bpype/blender_mcp/commit/98b0e49d98321d321c7e631389200f513f765d59)의 커밋 98b0e49(2026-05-05, v1.0.0 계열)이고, 환경은 pip `bpy` 5.2.2 LTS입니다. 26개 도구 중 24개를 MCP 클라이언트로 직접 불렀습니다. 절차·원본 응답·재현 도구는 [실제 구동 검증 기록](../01_research/handson/blender_lab_mcp/README.md)에 있습니다. blender.org와 projects.blender.org는 조사 환경에서 차단돼 있어서, 최신 릴리스(v1.0.2·v1.0.3) 정보는 검색 결과 요약만 봤습니다. 대신 다음으로 보완했습니다([후속 확인](../01_research/raw/G8_blender_lab_mcp.verify.json)). 공식 커밋을 2026-08-06까지 담은 파생 저장소 [bpy-dev/blender-mcp](https://github.com/bpy-dev/blender-mcp)의 git 이력과 비교했고, v1.0.3을 macOS에서 돌려 본 [외부 스모크 테스트](https://github.com/devotionn/blender-codex-lab/pull/1)(2026-09-22, 도구 26개)와 대조했습니다.

### 4.1 먼저 알아 둘 것 (실측)

1. **버전은 v1.0.2 이상을 쓰세요.** v1.0.0 계열은 의존성이 `mcp[cli]>=1.2.0`뿐입니다. 그래서 MCP 파이썬 SDK 2.0(2026-07-28) 이후 새로 설치하면 2.x가 깔리고, 서버가 import 단계에서 죽습니다(`No module named 'mcp.server.fastmcp'`). 클라이언트에는 `Connection closed`만 보여 원인을 찾기 어렵습니다. 검색 요약에 따르면 [v1.0.2(2026-09-08)](https://projects.blender.org/lab/blender_mcp/releases)가 "MCP SDK <2" 고정으로 이 문제를 고쳤습니다. 공식 코드를 담은 파생판도 같은 이유로 2026-09-06에 [MCP v1 고정](https://github.com/bpy-dev/blender-mcp/commit/e26ab0a9d556e5b076cd2d6fce93d2fbe4cd82b4)을 넣었습니다. 옛 태그를 써야 하면 `mcp[cli]<2`를 함께 고정하세요(4.3절).
2. **Allow Online Access를 켜야 합니다.** 끈 상태면 애드온이 `Online access must be enabled in the system preferences`라며 시작하지 않습니다. 명령줄에서는 `--online-mode`를 씁니다.
3. **오류는 대부분 정상 응답 안의 `status: "error"`로 옵니다.** 코드 예외, 렌더 실패, 없는 오브젝트가 모두 그렇습니다. MCP `isError`가 true인 경우는 스크린샷 실패와 연결 실패뿐이었습니다. 에이전트 규칙에 "결과의 status를 확인하라"를 넣으세요.
4. **렌더 도구는 지정한 폴더에 저장하지 않습니다.** 파일 이름만 떼어 `bpy.app.tempdir/blender_mcp/`에 저장하는데, 이 폴더는 Blender를 끄면 지워집니다. 필요하면 렌더 직후 `execute_blender_code`로 복사하세요. `render_viewport_to_path`는 이름과 달리 뷰포트 캡처가 아니라 현재 렌더 설정으로 하는 F12 렌더입니다.
5. **GPU·EGL이 없는 리눅스에서는 EEVEE 렌더 한 번에 Blender가 죽습니다**(`Couldn't open libEGL.so.1`). 헤드리스 서버에서는 렌더 엔진을 Cycles CPU로 바꾼 다음 렌더 도구를 부르세요.
6. **`execute_blender_code`의 보호 장치는 샌드박스가 아닙니다**(4.5절). `raise SystemExit` 한 줄로 백그라운드 Blender가 종료되고, 파일·OS 접근도 막지 않습니다.
7. **HTTP 모드는 필요할 때만 켜세요**(4.4절). CORS 전체 허용, DNS 리바인딩 보호 꺼짐, 인증 없음이라서 다른 Origin/Host 헤더로 보낸 요청으로도 코드가 실행됐습니다.

### 4.2 도구 26개

미러 README 목록은 24개입니다. 실제 서버는 문서 검색 2개를 더해 **26개**를 돌려줍니다. v1.0.3도 26개입니다(외부 스모크 테스트, 공식 `readme_tools.rst` 2026-08-06). `search_api_docs`·`search_manual_docs`는 2026-04-16 커밋으로 v1.0.0 전부터 있었습니다. prompts와 resources는 없습니다. 서버 instructions(약 5,900자)와 도구 스키마(약 14,700자)를 합치면, 영어 기준 대략 5천 토큰 안팎이 컨텍스트에 들어갑니다.

| 범주 | 도구 (R = readOnly, D = destructive 표시) | 실측 동작 |
|---|---|---|
| 코드 실행 | `execute_blender_code`(D), `execute_blender_code_for_cli`(D) | `result`에 dict를 넣어 반환합니다. print는 `stdout` 필드로 오고, Blender 객체는 `repr` 문자열로 바뀝니다 |
| .blend 점검 | `get_blendfile_summary_datablocks` / `_missing_files` / `_of_linked_libraries` / `_path_info` / `_usage_guess`(R), 각각의 `_for_cli`(R) | 데이터블록 수, 누락 파일, 링크 라이브러리, 저장 여부·백업, 용도 추정 |
| 씬 요약 | `get_objects_summary`(R), `get_object_detail_summary`(R) | 전체 오브젝트를 **개수 제한 없이** 반환합니다(1,019개 장면에서 확인). 큰 장면은 응답이 커집니다 |
| API·매뉴얼 | `get_python_api_docs`(R), `search_api_docs`(R), `search_manual_docs`(R) | 번들 문서는 Blender **5.1** API RST 2,173개와 매뉴얼 RST 2,217개입니다. 검색은 모든 단어가 들어 있어야 맞는 AND 방식이라 `bevel modifier segments`는 0건, `bevel segments`는 적중했습니다. 한국어 질의는 0건입니다 |
| 화면 | `get_screenshot_of_area_as_image`, `get_screenshot_of_window_as_image`, `get_screenshot_of_window_as_json`(R) | GUI 모드 전용. 백그라운드에서는 "not available" 응답 |
| UI 이동 | `jump_to_tab_by_name`, `jump_to_tab_by_space_type`, `jump_to_view3d_object_by_name`, `jump_to_view3d_object_data_by_name`(D) | GUI 모드 전용 |
| 렌더 | `render_viewport_to_path`(R), `render_thumbnail_to_path`(D) | 카메라가 필요합니다. 썸네일은 긴 변 320px, Cycles 16샘플. 저장 위치는 4.1절 4번 참고 |

- `_for_cli` 도구는 저장된 `.blend`를 새 Blender 프로세스에서 엽니다(`BLENDER_PATH`, 기본 `blender`). 지금 열린 파일이 수정 중이면 `이름_mcp_0001.blend` 사본을 저장해 분석하고 끝나면 지웁니다.
- `get_runtime_python_api_docs`는 **비공식 포크(bpy-dev) 전용**입니다. 공식 도구 목록의 근거로 bpy-dev 문서를 쓰면 안 됩니다.
- 공식 예시 과제와 LLM 통합 테스트는 모두 **분석·점검형**입니다. 데이터블록 이름 오타 수정, 재질 사용처 찾기, 카메라 기준 폴리곤 이상치("Analyze the scene and list the outliers: objects with highest polygon count but smaller size from the camera point of view"), 아마추어에 변형되지 않는 메시, 체크리스트 검증 같은 것들입니다. 생성보다 점검에 맞춰 설계됐습니다.
- 소스에 외부로 나가는 네트워크 코드가 없어서, 텔레메트리가 없다는 점은 소스로 확인했습니다.

### 4.3 설치

**애드온** (공식 [mcp/README.md](https://github.com/bpype/blender_mcp/blob/98b0e49d98321d321c7e631389200f513f765d59/mcp/README.md) 원문 기준):

1. Blender 5.1 이상에서 Preferences > Get Extensions > Repositories에 Blender Lab 확장 저장소 `https://lab.blender.org/`를 추가합니다.
2. MCP 애드온(확장 id `mcp`)을 찾아 설치하고 활성화합니다.
3. Preferences > System > Network에서 **Allow Online Access**를 켭니다. 애드온은 기본값(Auto Start 켜짐)이면 Blender 시작 1초 뒤 `localhost:9876`에서 서버를 엽니다. 애드온 환경설정에서 시작·중지 버튼과 오류 메시지를 볼 수 있습니다.

한국·일본 커뮤니티 후기([Threads @dddesign.io](https://www.threads.com/@dddesign.io/post/DXsWAspka7F/%ED%81%B4%EB%A1%9C%EB%93%9C-%EB%B8%94%EB%A0%8C%EB%93%9C-%EC%BB%A4%ED%85%8D%ED%84%B0-%EC%82%AC%EC%9A%A9%EB%B2%95%EA%B3%B5%EC%8B%9D-%EA%B0%80%EC%9D%B4%EB%93%9C%EA%B0%80-%EB%B6%88%EC%B9%9C%EC%A0%88%ED%95%B4%EC%84%9C-%EB%A7%8C%EB%93%AC1-claude-%EB%8D%B0%EC%8A%A4%ED%81%AC%ED%83%91-%EC%84%B8%ED%8C%85-%EC%BB%A4%EB%84%A5%ED%84%B0-%EC%9D%B4%EB%8F%992-blender-%EA%B2%80%EC%83%89-%EC%84%A0%ED%83%9D3-enbaled-%EB%88%84?hl=ko), [zenn](https://zenn.dev/shintama/articles/blender-official-mcp-claude?locale=en), [classmethod](https://dev.classmethod.jp/en/articles/claude-blender-connector-desktop-and-code/))에는 설치 링크를 Blender 창에 두 번 드래그하는 방법이 나옵니다. 1회차에 저장소가 추가되고 2회차에 애드온이 설치된다는 것인데, 위 1~2단계를 드래그로 하는 것과 같습니다. stefancrm 키트는 **두 경로(드래그 설치와 수동 설치)로 중복 설치하면 같은 ID의 애드온이 둘 생긴다**고 경고합니다. 한 경로만 쓰세요.

**Claude Desktop**: 설정 → 커넥터에서 'blender'를 검색해 설치하고, 위 애드온을 설치합니다([커넥터 페이지](https://claude.com/connectors/blender)의 애드온 안내 링크는 `lab.blender.org/mcp-server/#addon`).
- 커넥터 버전은 2026-09-27에 직접 확인했을 때도 **v1.0.1**입니다. 공식 최신 v1.0.3보다 뒤처져 있습니다. 이 커넥터가 SDK 2.x 문제의 영향을 받는지는 확인하지 못했습니다(추정: 번들이 uv로 의존성을 받는 구조라 가능성 있음). 연결이 곧바로 끊기면 4.1절 1번을 의심하고, 수동 설정(아래)으로 v1.0.2 이상을 쓰세요.
- **Windows에서 커넥터 설치가 실패하는 사례**: `uv.exe exited with code 1` / `error in 'egg_base' option: '.' does not exist or is not a directory`(Windows 11, Blender 5.1.1, 커넥터 v1.0.1). 설치 경로 `Claude Extensions`의 공백이 `%20`으로 넘어가는 문제가 겹친다는 분석이 있습니다. 공식 이슈([#24](https://projects.blender.org/lab/blender_mcp/issues/24))는 '특정 클라이언트 문제'로, [Claude Code 이슈](https://github.com/anthropics/claude-code/issues/54798)는 'not planned'로 닫혔습니다. 이럴 때는 수동 설정(git 소스 + uv)이 우회로입니다(검증된 해결책은 아님).

**Claude Code 등 수동 설정**: 공식 README의 서버 설치는 `pip install git+https://projects.blender.org/lab/blender_mcp.git#subdirectory=mcp`입니다. 다만 v1.0.0·v1.0.1을 받게 되면 SDK 2.x 문제에 걸리므로, 태그를 지정하거나 `mcp<2`를 함께 고정하세요.

```bash
# 방법 A: uvx 로 태그 지정 실행 (v1.0.3 태그 이름은 릴리스 페이지 표기 기준. 원문 확인 불가)
uvx --from 'git+https://projects.blender.org/lab/blender_mcp.git@v1.0.3#subdirectory=mcp' blender-mcp
# 옛 태그(v1.0.0·v1.0.1)라면 SDK 를 1.x 로 고정 (미러 소스로 동작 확인)
uvx --with 'mcp[cli]<2' --from 'git+https://projects.blender.org/lab/blender_mcp.git@v1.0.0#subdirectory=mcp' blender-mcp
```

```jsonc
// 방법 B: 클론 후 ~/.claude.json 의 mcpServers에 추가 ($HOME 확장이 안 되므로 절대경로 사용)
{
  "mcpServers": {
    "blender-lab": {
      "command": "/절대경로/uv",
      "args": ["--directory", "/절대경로/blender_mcp/mcp", "run", "blender-mcp"]
    }
  }
}
```

- **PyPI로는 공식 서버를 받을 수 없습니다.** 공식 서버의 패키지 이름도 `blender-mcp`인데, PyPI의 `blender-mcp`(2.0.0)는 ahujasid 서버로 넘겨 주는 래퍼입니다(2.2절).
- .mcpb 번들을 지원하는 클라이언트는 릴리스 페이지의 MCPB 파일을 쓰면 됩니다. 번들도 `uv run blender-mcp`로 의존성을 새로 받으므로, v1.0.0·v1.0.1 번들은 같은 SDK 2.x 문제에 걸릴 수 있습니다.
- **GUI 없이(서버·CI)**: 애드온이 명령줄 명령을 등록합니다. `blender --background --online-mode 파일.blend --command blender_mcp --port 9876`처럼 띄우면 됩니다. 이 모드에서는 요청을 하나씩 끝까지 처리하고, 스크린샷·UI 이동 도구는 쓸 수 없습니다.
- 공식 서버용 스킬은 [ra100/blender-claude-plugin](https://github.com/ra100/blender-claude-plugin)을 쓰세요(8절).

### 4.4 HTTP 모드와 로컬 LLM

- `blender-mcp --transport http`의 기본 주소는 **`127.0.0.1:8000`, 경로 `/`**입니다(streamable-http, stateless). `--port 9191`은 [로컬 LLM 문서](https://github.com/bpype/blender_mcp/blob/main/readme_local_llm.rst)의 예시 값입니다. 8000은 blender-open-mcp와 Unreal 5.8 공식 MCP의 기본 포트와 겹칩니다(9.1절).
- llama.cpp 웹 UI처럼 브라우저에서 붙는 클라이언트를 위해 **CORS를 전부 허용(`*`)하고 DNS 리바인딩 보호를 끕니다.** 공식 커밋 기준 2026-08-06까지 이 설정 파일은 바뀌지 않았습니다(v1.0.2·v1.0.3은 미확인). 인증도 없습니다. curl로 Origin 헤더를 외부 도메인(evil.example)으로 바꿔 initialize 없이 `execute_blender_code`를 불렀더니 실행됐습니다. `Host: attacker.example`도 통과했습니다. 실제 브라우저로 재현하지는 않았습니다. 그래도 HTTP 모드를 켜 둔 동안에는 브라우저로 연 웹페이지가 Blender 코드를 실행할 수 있는 구조로 보고, **쓸 때만 켜고, `--host 0.0.0.0`은 쓰지 마세요.** 평소에는 stdio(기본값)를 쓰면 됩니다.
- 저장소의 `chat_client`는 OpenAI 호환 `llama-server`(기본 :8080)와 Anthropic API(`ANTHROPIC_API_KEY`)에 붙습니다. llama.cpp 빌드 8218 이상에서 `llama-server --jinja --hf-repo ... --hf-file ...` 사용이 확인됐습니다.
- 로컬 모델에는 '분석과 간단한 편집' 정도만 기대하세요. 복잡한 모델링 품질은 frontier 모델과 차이가 큽니다.

### 4.5 코드 실행 안전장치와 한계값

| 항목 | 값·동작 | 근거 |
|---|---|---|
| 막는 것 | `sys.exit`, `bpy.ops.wm.quit_blender`, `wm.read_factory_settings`, `wm.read_factory_userpref`, `wm.read_userpref` | [weak_sandbox.py](https://github.com/bpype/blender_mcp/blob/98b0e49d98321d321c7e631389200f513f765d59/addon/blender_mcp_addon/weak_sandbox.py), 실측 |
| 못 막는 것 | `raise SystemExit`(Blender 종료), `os`·파일·네트워크·`subprocess` | 실측, 소스 설명 "this isn't really a sandbox" |
| MCP 서버 → 애드온 응답 대기 | 300초 | [connection.py](https://github.com/bpype/blender_mcp/blob/98b0e49d98321d321c7e631389200f513f765d59/mcp/blmcp/tools_helpers/connection.py) |
| `_for_cli` 서브프로세스 | 120초 | [blender_cli.py](https://github.com/bpype/blender_mcp/blob/98b0e49d98321d321c7e631389200f513f765d59/mcp/blmcp/tools_helpers/blender_cli.py) |
| 애드온의 요청 읽기 대기 | 10초 (실행 시간 제한이 아님. 실행 자체에는 제한이 없어 긴 코드는 Blender를 멈춤) | [mcp_to_blender_server.py](https://github.com/bpype/blender_mcp/blob/98b0e49d98321d321c7e631389200f513f765d59/addon/blender_mcp_addon/mcp_to_blender_server.py) |
| 요청 크기 | 10 MiB 초과는 거부 (응답 크기는 제한 없음. 12 MiB 반환 확인) | 실측 |
| 호스트·포트 | 애드온 환경설정 host/port. 서버 쪽은 `BLENDER_MCP_HOST`·`BLENDER_MCP_PORT`(기본 `localhost:9876`) | 소스 |
| 온라인 접근 | 꺼져 있으면 서버 시작 거부 | [애드온 `__init__.py`](https://github.com/bpype/blender_mcp/blob/98b0e49d98321d321c7e631389200f513f765d59/addon/blender_mcp_addon/__init__.py), 실측 |

이 저장소의 `building_audit.py`는 `execute_blender_code`에서 `sys.path.insert(0, "…/03_playbooks/scripts")` 후 import하면 그대로 동작했습니다(오브젝트 1,019개 장면에서 0.8초, [검증 기록](../01_research/handson/blender_lab_mcp/README.md#37-이-저장소-스크립트를-공식-mcp로-돌리기)).

### 4.6 아직 확인하지 못한 것

- v1.0.1의 변경 내용. v1.0.3 스크린샷 수정의 전체 내용도 확인하지 못했습니다. 관련된 공식 커밋으로 2026-08-06 [스크린샷 크기 한도 수정](https://github.com/bpy-dev/blender-mcp/commit/4309a39646e644261624bfcd2bca669b343b7621)은 확인했습니다. MCP 메시지 1 MB 한도에 JSON 포장분 여유 2 KiB를 두는 수정입니다
- v1.0.2·v1.0.3에서 HTTP 모드 보안 설정이 바뀌었는지(2026-08-06까지는 그대로)
- Claude Desktop 커넥터(v1.0.1)가 SDK 2.x 문제의 영향을 받는지
- GUI 모드의 스크린샷·UI 이동·지연 응답의 실제 동작. GUI 없는 환경이라 검증하지 못했습니다. 외부 스모크 테스트(macOS)도 GPU 가속은 검증하지 못했다고 적었습니다

---

## 5. 대안·보완 서버 비교

### 5.1 커뮤니티 서버와 포크

stars와 날짜는 조사 시점(2026-09-26~27) 기준입니다. 규모가 작은 저장소는 코드를 검토한 뒤 쓰세요.

| 서버 | 성격 | tool 수 | 라이선스 | 최신·활동 | Blender | stars | 이럴 때 | 주의 |
|---|---|---|---|---|---|---|---|---|
| [newo-ether/blender-mcp](https://github.com/newo-ether/blender-mcp) | ahujasid 포크 + 노드 트리 트랜잭션 편집 | 업스트림 + 노드 tool | MIT | [v1.19.0](https://github.com/newo-ether/blender-mcp/releases) (2026-09-21) | 4.2.22 LTS / 5.1.2 / 5.2 테스트 | 8 | 셰이더·GN을 LLM이 편집할 때 가장 안전 | 1인 유지보수, 설치 자동화가 Windows(PowerShell) 위주 |
| [blend-ai](https://github.com/HoldMyBeer-gg/blend-ai) | 샌드박스형 대형 툴셋 | 186 (27 모듈) | **AGPL-3.0-or-later** | [v1.7.0](https://github.com/HoldMyBeer-gg/blend-ai/releases) (2026-09-26) | 4.2 LTS+ (5.1까지 테스트, 4.0/4.1 미지원) | 148 | 임의 코드 실행을 막고 싶을 때 | AGPL(서비스에 넣으면 소스 공개 의무), 스키마 비용 |
| [RFingAdam/mcp-blender](https://github.com/RFingAdam/mcp-blender) | 대형 툴셋 + AI 생성(클라우드 Rodin/Meshy/Tripo, 로컬 TripoSR/SF3D/Hunyuan3D/ComfyUI), MSFS LOD·콜리전 | 218 | AGPL(v0.4.0부터, 이전 MIT) | 2026-09-10 | 4.2 LTS / 5.0 | 14 | 로컬 생성 백엔드, Ollama 비전 자기 개선 루프 | **`pip install mcp-blender` 금지**(PyPI 이름이 다른 패키지라 공급망 위험) → `git clone` 후 `pip install -e .`. [한국] 로컬 Hunyuan3D 라이선스 |
| [PatrykIti/blender-ai-mcp](https://github.com/PatrykIti/blender-ai-mcp) | 목표 우선 라우팅, 결정적 측정·assertion | 소수만 노출(게이트웨이) | Apache-2.0 | v3.3.0 (2026-05-04), 이후 커밋 없음 | 애드온 4.0+, E2E는 5.0 | 59 | 배치·공간 관계 검증 설계 참고 | 설정이 복잡함 |
| [harveyxiacn/blender-mcp](https://github.com/harveyxiacn/blender-mcp) | 동적 로딩(기본 32개, `blender_activate_skill`로 12개 그룹 켜기) | 359 | MIT | — | 4.x/5.x | 15 | tool 과다 문제의 해법 사례, 체크포인트, 절차적 재질 67종 | 소규모 |
| [glonorce/Blender_mcp](https://github.com/glonorce/Blender_mcp) | 다국어 intent 필터(컨텍스트 약 77% 절감), BVH 면 간 거리·관통 검사, 0~100 무결성 점수 | 69 | MIT | 2026-01 | 5.0+ | 6 | 관통·부유 검사 방식 참고 | 소규모 |
| [pakkio/mcp-blender](https://github.com/pakkio/mcp-blender) | 검증 중심, `capture_multiview_audit`(4뷰, 가림 진단, bbox 지표) | 146 (21 도메인) | 미확인 | v2.3.5 | — | 1 | 4방향 contact sheet 감사 | 소규모 |
| [dhakalnirajan/blender-open-mcp](https://github.com/dhakalnirajan/blender-open-mcp) | 로컬 LLM provider(Ollama, LM Studio, llama.cpp, OpenAI 호환) 런타임 전환 + PolyHaven | 적음 | MIT | 2026-09-04 | — | 120 | 씬을 클라우드로 보낼 수 없을 때 | MCP 서버는 `localhost:8000`(HTTP), 애드온만 9876 |
| [sandraschi/blender-mcp](https://github.com/sandraschi/blender-mcp) | 기본 헤드리스(`blender --background`), 선택적 GUI 브리지 | 41 portmanteau (150+ 작업) | MIT | 2026-09-18 | 3.0+ | 48 | 배치 export·렌더, .mcpb 설치(Python 불필요) | 헤드리스 EEVEE는 GPU가 필요할 수 있음 |
| [youichi-uda/blender-mcp-pro](https://github.com/youichi-uda/blender-mcp-pro) | 상용. 시작할 때 핵심 15개만 노출하고 `enable_tools(category)`로 추가(eager 모드도 있음) | 120+ (17 카테고리) | 애드온 MIT / 서버 독점 | $5/월(Gumroad, 7일 체험) 또는 $15 일회성(itch.io) | 4.0+ (5.0 권장) | 31 | 유료 지원을 원할 때 | 서버 비공개라 코드 감사 불가. 포트 9877 |
| [marlonka/better-blender-mcp](https://github.com/marlonka/better-blender-mcp) | ahujasid 포크: scene delta, staged edit, 백그라운드 워커(데드라인·취소), 품질 검사, 타임아웃 명령 자동 재실행 안 함 | — | MIT | 커밋 201개 | 5.2.1 LTS 테스트 | 0~2 | 긴 렌더·베이크 | 유지보수 지속성 불확실 |
| [owenpkent/blendmcp](https://github.com/owenpkent/blendmcp) | 텔레메트리 완전 제거 포크, 재연결 재시도, 버전 핸드셰이크 | — | MIT | v1.4.4 | 5.x | 소규모 | 프라이버시 | 소규모 |
| [lucasgfsvd/blender-mcp](https://github.com/lucasgfsvd/blender-mcp) (TESSA LABS) | 텔레메트리 제거 + CAE tool 약 40개(스칼라장 컬러, 단면, 치수선) | — | MIT | — | — | 소규모 | 엔지니어링 시각화 | 소규모 |
| [bpy-dev/blender-mcp](https://github.com/bpy-dev/blender-mcp) · [NThuesen/blender-game-mcp](https://github.com/NThuesen/blender-game-mcp) · [marble810/blender-mcp-connect](https://github.com/marble810/blender-mcp-connect) | 공식 서버 기반 비공식 배포판: 격리 서브프로세스, `BLENDER_MCP_CLI_BACKEND`, BlenderBench(27 tasks/270 rounds, CLIP 채점), 인스턴스 자동 발견 | — | GPL-3.0 | developer preview | — | 94 / 0 / 0 | 공식 서버 설치가 번거롭거나 헤드리스 분석이 필요할 때 | 비공식. marble810은 `uvx --from blender-mcp-connect==0.1.0 blender-mcp-connect` |
| [ellmos-blender-use-mcp](https://github.com/ellmos-ai/ellmos-blender-use-mcp) | 헤드리스 QA: FBX 재임포트 검사, 4뷰 시각 검사, 스크립트 실행(최대 10분, 출력 tail 8,000~50,000자) | 4 | MIT | 2026-09-26 | — | 2 | CI 게이트(열린 포트·애드온 없음) | (신뢰도 낮음) README에 규모에 비해 과장된 문구가 많음. 채택 전에 동작 검증 |

- PolyMCP용 Blender-MCP-Server(51 tool)는 원 저장소가 불분명하고 라이선스도 확인되지 않아 추천에서 뺐습니다(신뢰도 낮음).
- tool이 200~359개인 서버를 그대로 붙이면 컨텍스트를 크게 잡아먹습니다. 프로파일이나 필터를 쓰세요(9.4절).

### 5.2 보완 MCP (생성·문서)

| 도구 | 역할 | 비고 |
|---|---|---|
| [Meshy MCP](https://github.com/meshy-dev/meshy-mcp-server) (`@meshy-ai/meshy-mcp-server`, MIT) | text/image-to-3D, retexture, auto-rig, 3D 프린트 분석 | 유료 크레딧. Meshy Bridge 애드온 포트(5324)는 미확인. 생성 tool이 없는 공식 서버와 조합하기 좋음 |
| [Tripo 공식 tripo-mcp](https://github.com/VAST-AI-Research/tripo-mcp) (MIT, 약 206 stars, alpha) | Tripo 생성 + Tripo Blender 애드온 연동 | **비권장**: 마지막 커밋 2025-04-14로 사실상 방치(교차검증). Tripo가 필요하면 [SDK](https://pypi.org/project/tripo3d/) 경로를 쓰세요 |
| [Hunyuan3D-2 공식 Blender 애드온](https://github.com/Tencent-Hunyuan/Hunyuan3D-2) (약 15k stars) | 로컬 API 서버로 Blender 안에서 생성 | **[한국 주의]** 라이선스 지역 제외 |
| [Context7](https://github.com/upstash/context7) | 라이브러리 문서를 버전별로 주입 | Blender 문서가 등록돼 있는지는 미확인. Blender 전용 조회 tool이 더 직접적 |
| [fake-bpy-module](https://github.com/nutti/fake-bpy-module) | 2.78~5.2 bpy 스텁(`pip install fake-bpy-module-5.1`) | 오프라인으로 버전별 API 존재 여부 확인(11.3절) |

생성 모델 선택과 후처리는 [AI 3D 생성 가이드](04_ai_3d_generation.md)를 보세요.

---

## 6. 헤드리스 방식 (MCP 소켓 없이)

코딩 에이전트(Claude Code, Codex)가 `.py` 빌드 스크립트를 쓰고, Blender를 백그라운드로 실행해 .blend와 렌더 PNG를 만든 뒤, 그 이미지를 다시 읽어 비평하고 고치는 루프입니다. 스크립트가 곧 소스라서 재현하기 쉽고 git으로 관리할 수 있습니다. GUI 멈춤이나 소켓 타임아웃도 없고 CI에서 병렬 렌더를 돌릴 수 있습니다. 단점은 실시간 상호작용이 없다는 점과, 실행할 때마다 씬을 처음부터 다시 빌드하는 비용입니다.

| 선택지 | 내용 |
|---|---|
| 직접 CLI | `blender -b --factory-startup --python-exit-code 1 -P build.py -- --out renders/v003.png` |
| PyPI [bpy](https://pypi.org/project/bpy/) | `pip install bpy==5.2.2`(2026-09-15). **5.1 이상은 Python 3.13 전용, 5.0은 3.11.** 설치되는 wheel 하나는 210~402MB(모든 플랫폼 합계 약 1.2GB) |
| 공식 서버 `*_for_cli` | 저장된 .blend를 새 서브프로세스에서 분석·실행 |
| [ifBars/blender-agent-studio](https://github.com/ifBars/blender-agent-studio) | Codex 플러그인(51 stars, MIT). .blend와 생성 Python을 함께 보존하고, 실루엣 마스크로 레퍼런스와 비교하며, Poly Haven 1K–8K를 씀. Blender 5.2 LTS와 Bun 1.3.5+ 필요, 로컬 MCP 서버와 전문 스킬 11개 포함 |
| [minihellboy/claude-blender](https://github.com/minihellboy/claude-blender) | 헤드리스 서버 + `/blender-iterate`, `/blender-studio-shot`, `/blender-turntable` 슬래시 명령 |
| [sandraschi/blender-mcp](https://github.com/sandraschi/blender-mcp) | 헤드리스 MCP 서버(5.1절) |

빌드 스크립트 뼈대입니다.

```python
# build_scene.py
# 실행: blender -b --factory-startup --python-exit-code 1 -P build_scene.py -- --out renders/v003.png
import argparse, os, sys
import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
args = ap.parse_args(argv)
out = os.path.abspath(args.out)

# ... 씬 빌드 (get-or-create, 이름 접두사 GEO-/MAT-/LGT-/CAM-) ...

scene = bpy.context.scene
scene.render.filepath = out
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.splitext(out)[0] + ".blend")
print("done:", out)
```

- **`--python-exit-code 1`은 필수입니다.** 이 옵션이 없으면 스크립트에서 예외가 나도 종료 코드가 0이라, 에이전트나 CI가 실패를 성공으로 착각합니다([yardstake-ux #151](https://github.com/captproton/yardstake-ux/issues/151)).
- `--factory-startup`을 붙이면 개인 애드온과 설정의 영향을 없앨 수 있습니다.
- GPU가 없는 리눅스 서버에서는 EEVEE·Workbench 렌더에 GPU나 EGL 컨텍스트가 필요할 수 있습니다. 이럴 때는 Cycles(CPU)를 쓰세요. 이 저장소의 `review_views.py` 기본값도 Cycles입니다([스크립트 README](../03_playbooks/scripts/README.md)).
- MCP로 export하다 타임아웃이 나면 헤드리스로 넘기세요(blender-kiln 규칙). kiln은 대화형 MCP 경로와 헤드리스 경로의 결과가 **바이트 단위로 같았다**고 보고합니다(111.9kB GLB, 2,202 tris).
- 이 저장소 스크립트는 헤드리스로도 돌릴 수 있습니다: `blender -b scene.blend --python 03_playbooks/scripts/scene_audit.py -- --floor-z 0 --out audit.json`.

---

## 7. Blender 안에서 도는 AI 애드온

MCP 서버가 아니라 Blender UI 안에서 동작하는 도구들입니다. 에이전트(MCP)가 모델링과 배치를 맡고, 이런 애드온이 텍스처를 맡는 식으로 나눠 쓰는 방식이 유효합니다.

| 애드온 | 무엇 | 라이선스·비용 | 상태 | 주의 |
|---|---|---|---|---|
| [StableGen](https://github.com/sakalond/StableGen) | ComfyUI 백엔드(`127.0.0.1:8188`)로 여러 카메라 뷰에서 이미지를 생성해 메시에 투영 텍스처링(SDXL, FLUX.1-dev, Qwen Image Edit, FLUX.2 Klein). ControlNet(깊이·노멀), IPAdapter, PBR 분해, TRELLIS.2 메시 생성 | GPL-3.0, 무료(로컬 GPU) | v0.3.1 (2026-06-12), 929 stars | **Blender 4.2–4.5 또는 5.1+ 지원, 5.0 미지원**. VRAM 최소 8GB, FLUX/Qwen은 16GB+. 설치 용량 약 7.3~33GB. 가려진 면에 이음새나 누락이 생길 수 있음 |
| [Scenario for Blender](https://github.com/scenario-labs/blender-plugin) | 이미지·비디오·3D 메시·선택 메시 PBR 재질·오디오 생성, 씬 설명을 그레이박스로 바꾸는 Blockout, **내장 MCP** | 애드온 GPL-3.0-or-later, 생성은 Scenario 유료 크레딧 | 10 stars | Blender 5.0+, Allow Online Access 필요, GitHub Releases로만 배포. 내장 MCP가 `http://127.0.0.1:9876/mcp`라 **포트 9876 충돌**. 임의 Python 실행은 기본 OFF(보안상 장점) |
| [Blender-Copilot](https://github.com/halilogia/Blender-Copilot) | UI 안 채팅 에이전트. 읽기 전용 grounding tool, `bpy.ops.ed.undo_push()` 기반 원자적 undo, 파괴적 작업은 PENDING_APPROVAL(Y/N) 승인 | GPL-3.0 | 5.2.1 LTS 대상, 2 stars | 초기 단계. OpenAI 호환 엔드포인트(Ollama, LM Studio, OpenRouter) |
| [GitHubCopilotBlender](https://github.com/ULT7RA/GitHubCopilotBlender) | GitHub OAuth, 다중 모델 tool-calling | — | 초기 | — |
| [BlenderGPT](https://github.com/gd3kr/BlenderGPT) | GPT-4 시절 선구작 | MIT, 약 5k stars | 마지막 커밋 2023-06-10 | **레거시**. 현재 API 변경을 반영하지 못함 |

3D-Agent(상용)는 자사 SEO 자료 말고는 근거가 없고 가격 정보도 서로 모순돼서 추천에서 뺐습니다. 텍스처링 전반은 [텍스처링 가이드](05_texturing_materials.md)를 보세요.

---

## 8. Claude Code·Codex 스킬 레이어

MCP tool 위에 전문가 절차를 얹는 SKILL.md 묶음입니다. "멋지게" 같은 형용사 대신 수치 규칙(치수, 베벨, 조명 비율, 바운스)과 QA 게이트를 주기 때문에, 가구·소품의 형태 정확도가 눈에 띄게 올라갑니다. 단 스킬마다 전제로 하는 MCP의 tool 이름이 다르니 호환성을 확인하세요.

| 스킬·플러그인 | 대상 MCP | 규모·라이선스 | 핵심 내용 |
|---|---|---|---|
| [RobLe3/cc-blender-skill](https://github.com/RobLe3/cc-blender-skill) | **ahujasid(9876)**. 공식 서버로 옮기는 [PR #1](https://github.com/RobLe3/cc-blender-skill/pull/1)은 제3자가 올린 미병합 PR | v1.3.0, 30 skills, MIT, 70 stars | [text-to-blender](https://github.com/RobLe3/cc-blender-skill/blob/main/plugin/skills/text-to-blender/SKILL.md) 오케스트레이터. 실측 치수표, [모델링 규칙](https://github.com/RobLe3/cc-blender-skill/blob/main/plugin/skills/blender-modeling/SKILL.md)(Bevel 0.02m·3 seg·30°를 SubSurf 뷰 2/렌더 3보다 먼저, 모디파이어 순서 Mirror→Array→Solidify→Bevel→SubSurf→Boolean, 접합부 5~15mm 겹침, Boolean EXACT 후 노멀 정리), 5~20줄 청크, GEO-/MAT-/LGT-/CAM-/ARM- 접두사, 스크린샷 QA 게이트. Blender 5.1.1에서 6종(검, 병, 의자, 비행사 선글라스, 데스크램프, 방송용 아바타) E2E 검증. 실패 렌더도 공개했고, 트리거 평가는 TP 100%/FP 4%. 필요 패키지: opencv-python, numpy, scipy, Pillow |
| [ra100/blender-claude-plugin](https://github.com/ra100/blender-claude-plugin) | **공식 Blender Lab(5.1+)** | v1.3.0, 전문 스킬 8개, MIT | GN 약 373 / 셰이더 약 95 / 컴포지팅 약 80 노드 레퍼런스, Python 3.13 |
| [arjun988/blender-skills](https://github.com/arjun988/blender-skills) | ahujasid | 94 skills, 참조 파일 175+, MIT, 229 stars | blender-director 라우팅, qa-review(5뷰, Blocker/Major/Minor, SHIP/NO-SHIP), set-dressing, 스타일 스킬 30개 |
| [elithril/blender-kiln](https://github.com/elithril/blender-kiln) | ahujasid + 헤드리스 | MIT | 텍스트 브리프에서 웹용 GLB까지. Iron Rules **31개**(core 26 + batch 5), 8항목 export 체크. Blender 4.4 이상 |
| [Gaius114/blender-claude-mcp](https://github.com/Gaius114/blender-claude-mcp) | 자체 HTTP 브리지(7234) | 11 skills | spec_sheet 생성, 계획 검증 커널(`plan_validator.py`). 단 blender-space 문서의 "dimensions는 scale=1일 때만 유효" 설명은 틀림(11.1절) |
| [kevinbadi/blender-skills](https://github.com/kevinbadi/blender-skills) | ahujasid + Meshy | 라이선스 미표기 | Meshy image-to-3d, 턴테이블·돌리·크레인 카메라 무브(1920×1080/24fps, ProRes 4444 알파) |
| [jithinolickal/blender](https://github.com/jithinolickal/blender) | ahujasid | Apache-2.0 | 4각도 검사 프리셋, 마일스톤 저장·복원, 실전 오류 목록(`orphans_purge` 금지 등) |
| [CheshireJCat/create-3d-model-skill](https://github.com/CheshireJCat/create-3d-model-skill) | Codex | 소규모 | Codex `$create-3d-model` 호출 예시. 스킬 경로는 `~/.codex/skills`와 저장소 `.agents/skills`가 모두 보고됨(공식 문서 미확인) |
| [hideki711014/roo-blendermcp-jp-rules](https://github.com/hideki711014/roo-blendermcp-jp-rules) | 로컬 LLM + 현지화 UI | 규칙 4파일 | 일본어 UI 노드 이름 문제 해결법(12절) |
| [MAX-786/claude-3d-harness](https://github.com/MAX-786/claude-3d-harness) | newo-ether(기본), ahujasid(대체, `blender-mcp==2.0.0` 고정) | 58 SKILL.md 통합, MIT, 6 stars | 품질 프로필 fast(1280×720/64spp) · standard(1920×1080/256spp) · cinematic(512spp). README 사례: '비 오는 밤 일본 도시 옥상의 작은 방'(메시 449개)을 블록아웃에서 최종 프레임까지 3시간 미만. 공식 서버 지원은 [이슈 #7](https://github.com/MAX-786/claude-3d-harness/issues/7)에서 논의 중 |

설치 예시:

```bash
# cc-blender-skill (저장소 루트에서)
for skill in plugin/skills/*/; do ln -sfn "$(pwd)/$skill" "$HOME/.claude/skills/$(basename $skill)"; done

# ra100 (공식 서버용)
claude plugin marketplace add ra100/blender-claude-plugin
claude plugin install blender-skills@blender-claude-marketplace
```

- 스킬을 직접 만든다면 이 저장소의 템플릿([CLAUDE.md](../03_playbooks/templates/CLAUDE.md), [SKILL.md](../03_playbooks/templates/skills/blender-aaa-scene/SKILL.md))에서 시작하세요. 훅·서브에이전트·/goal 활용은 [에이전트 워크플로 가이드](09_agent_workflow_prompting.md)에 있습니다.
- Bniya-cn/blender-design-master(멀티에이전트와 시각 비평가 점수 게이트)는 라이선스가 선언돼 있지 않고, Codex 테스트에서도 Final Gate 평균 7.4로 통과하지 못했습니다. 설계 참고용으로만 보세요.

---

## 9. 운영 함정

### 9.1 포트

| 포트 | 누가 쓰나 | 충돌 |
|---|---|---|
| 9876 (TCP) | ahujasid 애드온, **공식 Blender Lab 애드온**, blend-ai, RFingAdam, blender-open-mcp 애드온 | 동시에 켜면 연결이 엉뚱한 서버로 가거나 실패 |
| 9876 (HTTP `/mcp`) | Scenario for Blender 내장 MCP | 위와 3중 충돌 가능 |
| 9877 | ahujasid 두 번째 인스턴스(관례), blender-mcp-pro 기본 | 서로 충돌 |
| 9191 | 공식 서버 HTTP 모드의 로컬 LLM 문서 예시 값 | — |
| 8000 (HTTP) | **공식 Blender Lab 서버 HTTP 모드 기본값**, blender-open-mcp MCP 서버, Unreal 5.8 공식 MCP 기본 | 셋 중 둘 이상을 HTTP로 켜면 충돌. 공식 서버는 `--port`로 바꿈 |
| 8080 | llama-server(공식 `chat_client` 연결 대상) | — |
| 8188 | ComfyUI(StableGen) | — |
| 7234 (HTTP) | Gaius114 브리지 | — |
| 5324 | Meshy Bridge(미확인) | — |

해결책은 ① 한 Blender에는 한 서버만 켜는 것입니다(가장 안전). ② 여러 Blender를 띄울 때는 ahujasid `--port`와 애드온 포트를 짝지어 바꿉니다. ③ newo-ether 포크는 `list_blender_instances`·`claim_blender_instance`로 인스턴스를 고르고, claim은 6시간 동안 활동이 없으면 만료됩니다. 한 Blender에서 두 애드온을 포트만 나눠 동시에 쓰는 조합은 검증된 사례가 없습니다.

### 9.2 타임아웃

| 계층 | 값 | 대응 |
|---|---|---|
| ahujasid 서버→애드온 소켓 | **180초** | 코드를 5~20줄 청크로 나눔. 무거운 작업은 해상도를 낮추거나 별도 프로세스로 |
| 공식 서버→애드온 소켓 / `_for_cli` 서브프로세스 | **300초 / 120초**(소스 확인). 애드온의 요청 읽기 대기 10초는 실행 시간 제한이 아님 | 긴 렌더·베이크는 헤드리스로. 요청은 10 MiB까지 |
| 애드온의 `exec()`(ahujasid·공식 모두) | **타임아웃 없음** | 큰 루프는 Blender 전체를 멈춤. 인터랙티브 작업에서는 해상도·반복 수에 상한을 둠 |
| Poly Haven 다운로드 | 메인 스레드 동기 처리 | 1k/2k로 요청 |
| MCP 클라이언트(Claude Desktop 등) | 약 4분에 포기하는 사례 관측 | 긴 작업은 헤드리스로 |
| Windows 버그 [#339](https://github.com/ahujasid/blender-mcp/issues/339)·[#357](https://github.com/ahujasid/blender-mcp/issues/357) | 연결은 되는데 명령이 처리되지 않고 약 4분 뒤 타임아웃(Blender 5.1.1/5.2.1). 프레이밍 불일치 의심, **아직 열려 있음** | Claude와 Blender 서버를 둘 다 재시작, 최신 버전으로 업데이트, 헤드리스로 우회 |
| Claude Code `MCP_TOOL_TIMEOUT` | 설정하지 않으면 약 28시간. `.mcp.json` 서버별 `"timeout"`(ms)으로 덮어쓸 수 있음(진행 알림으로 연장되지 않는 절대 한도라, 값을 넣으면 오히려 짧아질 수 있음) | — |
| Claude Code 유휴 타임아웃 `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT` | stdio 서버(ahujasid·공식 서버 기본) **30분**, HTTP·SSE·WebSocket 서버 **5분** | 진행 알림 없는 긴 Cycles 렌더는 중단될 수 있음 → 헤드리스([Claude Code MCP 문서](https://code.claude.com/docs/en/mcp)) |
| Gemini CLI | `timeout` 기본 600,000ms | [Gemini CLI MCP 문서](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md) |

최종 렌더와 베이크는 better-blender-mcp의 백그라운드 워커나 헤드리스 `blender -b` 서브프로세스에서 돌리세요.

### 9.3 `get_scene_info` 10개 제한과 씬 요약

ahujasid 애드온 코드는 `for i, obj in enumerate(bpy.context.scene.objects): if i >= 10: break`입니다(주석 'Reduced from 20 to 10'). 가구가 수십 개인 인테리어 씬에서는 모델이 나머지 오브젝트를 모른 채 작업하게 됩니다. 그러니 필요한 필드만 담은 압축 요약을 직접 출력하게 하세요.

```python
# execute_blender_code 로 실행: 모든 오브젝트의 월드 bbox 요약 (오브젝트 100개 기준 수천 토큰)
import bpy, json
from mathutils import Vector
bpy.context.view_layer.update()
rows = []
for o in bpy.context.scene.objects:
    if o.type not in {'MESH', 'LIGHT', 'CAMERA', 'EMPTY', 'CURVE'}:
        continue
    pts = [o.matrix_world @ Vector(c) for c in o.bound_box]
    mn = [min(p[i] for p in pts) for i in range(3)]
    mx = [max(p[i] for p in pts) for i in range(3)]
    col = o.users_collection[0].name if o.users_collection else ''
    rows.append([o.name, o.type, col, [round(v, 3) for v in mn], [round(mx[i] - mn[i], 3) for i in range(3)]])
print(json.dumps(rows, separators=(',', ':')))
```

- 이 출력을 씬 인덱스로 삼고, 필요한 오브젝트만 `get_object_info`로 상세 조회하세요.
- 떠 있음·관통·치수 이상까지 한 번에 보려면 이 저장소의 `scene_audit.py`를 쓰세요. 부모 단위로 묶어 판정하고 JSON 리포트를 냅니다([사용법](../03_playbooks/scripts/README.md)).
- 공식 서버에서는 `get_objects_summary`를 쓰고, 무거운 파일은 `get_blendfile_summary_*`로 개요부터 봅니다.
- 노드 트리 전체를 export하면 수십 KB가 됩니다. newo-ether v1.13.0의 slim 뷰는 30노드 export를 62KB에서 9.3KB로 줄였습니다.

### 9.4 컨텍스트·토큰 비용

- **tool 스키마**: ahujasid 스키마는 2026-08-19부터 09-03 사이 5,462토큰에서 6,928토큰으로 27% 늘었습니다(tool 25개→28개, [#347](https://github.com/ahujasid/blender-mcp/issues/347)). 지금은 36개라 더 클 가능성이 높습니다. 이 비용을 처음부터 전부 내는 것은 tool 정의를 한꺼번에 불러오는 클라이언트(Claude Desktop, Cursor, VS Code, Windsurf)입니다. **Claude Code는 MCP tool 정의를 지연 로딩**하므로 영향이 적습니다. 쓰지 않는 MCP는 끄세요.
- **스크린샷**: Claude 이미지 토큰은 ⌈w/28⌉×⌈h/28⌉입니다. 1000×563 캡처는 756토큰이고, 1920×1080은 Opus 5.5(high-res tier)에서 2,691토큰, standard tier에서 1,560토큰입니다([Vision 문서](https://platform.claude.com/docs/en/build-with-claude/vision)). 뷰포트 확인은 800~1000px로 충분합니다.
- **이미지 20개 제한**: 한 요청에 이미지가 20개를 넘으면(이전 턴 이미지와 tool_result 안의 스크린샷 포함) 이미지당 치수 제한이 더 엄격해집니다. 각 변을 2000px 이하로 줄이세요. 스크린샷 루프가 길어지면 `invalid_request_error`가 날 수 있습니다.
- **MCP 출력 한도**: Claude Code의 `MAX_MCP_OUTPUT_TOKENS`는 기본 25,000이고 10,000을 넘으면 경고합니다.
- 비용 계산과 모델별 단가는 [모델 가이드](01_ai_models_and_clients.md)와 [에이전트 워크플로 가이드](09_agent_workflow_prompting.md)를 보세요.

### 9.5 Windows·GUI 클라이언트 설치 문제

| 증상 | 원인 | 해결 |
|---|---|---|
| `spawn uvx ENOENT` | GUI로 실행한 Claude Desktop·Cursor는 터미널 PATH를 물려받지 않음 | `command`에 uvx 절대경로를 넣음(`where uvx`의 결과) |
| Python 버전 충돌(conda, pyenv, asdf) | 여러 Python이 섞임 | `"args": ["--python", "3.11", "mcp-for-blender"]`, `"env": {"UV_PYTHON_PREFERENCE": "only-managed"}` |
| 첫 명령만 실패 | 초기 연결 | 두 번째부터 되는 경우가 많음. 계속 실패하면 클라이언트와 Blender 서버를 둘 다 재시작 |
| WSL↔Windows 조합에서 스크린샷 실패 | 경로 문제(이슈 #187) | 같은 OS 안에서 실행 |
| 공식 애드온이 두 개 보임 | 드래그 설치와 수동 설치로 중복 설치 | 한 경로만 남김 |

### 9.6 undo와 버전 저장

- ahujasid 애드온은 **`undo_push`를 호출하지 않습니다.** AI가 만든 변경을 Ctrl+Z로 한 단계씩 되돌린다는 보장이 없습니다. README도 "Always save work before using it"을 강조합니다.
- **Claude Code의 `/rewind`는 Blender 상태를 되돌리지 못합니다.** 체크포인트는 Claude의 파일 편집 도구로 바꾼 것만 추적합니다.
- 단계마다 저장하세요. 다음 두 방법 모두 safe mode 검사를 통과하는 것이 확인됐습니다(2026-09-25 커밋 기준, bpy 5.0.1).

```python
import bpy
# (1) 증분 저장: 파일 이름 끝 번호를 올려 새 파일로 저장 (5.0.1과 4.2.23 LTS에 존재 확인.
#     chair.blend → chair1.blend처럼 저장되고, 작업 파일도 새 번호 파일로 바뀜. 한 번도 저장하지 않은 파일에는 쓸 수 없음)
bpy.ops.wm.save_mainfile(incremental=True)
# (2) 현재 작업 파일 경로는 그대로 두고 사본만 저장
bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath('//versions/scene_v003.blend'), copy=True)
# undo 단위를 만들고 싶으면 (Blender-Copilot 방식)
bpy.ops.ed.undo_push(message='AI: add chair')
```

Blender의 Save Versions 설정도 켜 두세요. harveyxiacn 서버의 named checkpoint도 같은 목적입니다.

### 9.7 Blender 버전 선택 (2026-09)

최신 안정판은 5.2.2(2026-09-14)이고 5.2 계열은 LTS로 표기됩니다. 4.5 LTS와 4.2 LTS도 함께 유지되고 있습니다.

| Blender | 공식 서버 | ahujasid | StableGen | 이 저장소 스크립트 | 비고 |
|---|---|---|---|---|---|
| 5.2.x | 가능(5.2.2 LTS에서 실측) | 가능(Windows 타임아웃 이슈 #357 보고) | 가능 | 테스트 통과(5.2.2 LTS) | newo-ether·better-blender-mcp·Blender Agent Studio가 5.2 대상. GN 모디파이어 API 변경 가능성(11.1절, 미확인) |
| 5.1.x | 가능(하한) | 가능 | 가능 | 미테스트 | cc-blender-skill E2E 검증 버전(5.1.1). Python 3.13 |
| 5.0.x | **불가** | 가능 | **불가** | 테스트 통과(5.0.1) | Python 3.11 |
| 4.5 / 4.2 LTS | **불가** | 가능 | 가능 | 테스트 통과(4.2.23) | blend-ai는 4.2+ |

공식 커넥터를 쓰려면 5.1 이상, 가능하면 5.2.x를 쓰세요. 파이프라인 때문에 4.x LTS에 묶여 있다면 ahujasid나 blend-ai를 쓰면 됩니다.

---

## 10. 보안

### 10.1 이력 (ahujasid)

| 날짜 | 건 | 내용 | 현재 |
|---|---|---|---|
| 2026-03-10 | [#202](https://github.com/ahujasid/blender-mcp/issues/202) | `generate_hunyuan3d_model`의 `input_image_url`이 http로 시작하지 않으면 `open()`으로 로컬 파일을 읽어 base64로 외부 API에 보냄(임의 파일 유출) | 아래 CVE의 실제 시나리오로 보임(명시적 연결은 없음). 최신 버전 사용 |
| 2026-06-02/03 | [CVE-2026-10661 / GHSA-qqw9-95ww-prfm](https://github.com/advisories/GHSA-qqw9-95ww-prfm) | CWE-74, CVSS v4 2.1(Low). 영향 범위는 커밋 7636d13까지, 패치 커밋은 5b37be25242e. GHSA 본문이 #202와 명시적으로 연결하지는 않음 | 최신 버전 사용 |
| — | [#207](https://github.com/ahujasid/blender-mcp/issues/207) | 샌드박스 요청 | 'not planned'로 종료 |
| 2026-04-20 | [#232](https://github.com/ahujasid/blender-mcp/issues/232) | 텔레메트리 기본 ON(consent default=True, 작성자 주장)과 GDPR 문제 제기 | closed |
| 2026-09-02 | 커밋 'feat: add safe mode for bounded code execution' | `BLENDER_MCP_SAFE_MODE` 추가(09-21에 보강 fix) | — |
| 2026-09-21 | 커밋 'update: opt-in telemetry' | **콘텐츠 수집만** opt-in으로 전환 | 익명 사용 기록은 여전히 기본 ON |

- 조사에서 확인하지 못한 것도 있습니다: 이슈 #360('무작위 서버로 무엇을 보내나')의 본문과 답변, tool 설명에 숨은 지시(무료 체험 추적)가 있었다는 외부 지적의 원문과 해소 여부.
- 소켓에는 **인증도 암호화도 없습니다.**

### 10.2 safe mode가 막는 것과 못 막는 것

| 막는 것 (`BLENDER_MCP_SAFE_MODE=1`) | 허용하는 것 |
|---|---|
| `open()`·`os` 같은 **직접** 파일 I/O | bpy 오퍼레이터를 통한 .blend 저장·열기 |
| 외부 프로그램 실행(프로세스) | import/export |
| 네트워크 | 렌더 |
| handlers·timers·drivers 등록(코드 영속화) | 모델링, 재질, 조명 |
| 외부 .blend append/link | — |

**한계: safe mode는 샌드박스가 아닙니다.** 검사는 MCP 서버 경로에만 걸립니다. 애드온 소켓(9876)은 **로컬의 어떤 프로세스가 보낸 raw `execute_code`든 그대로 받습니다.** 개발자도 "not a sandbox around Blender"라고 명시합니다.

- 이 저장소 스크립트를 `sys.path`에 추가해 import하는 방식이 safe mode에서 막히는지는 확인하지 못했습니다. 막히면 파일 내용을 그대로 붙여 넣는 방식을 쓰세요([스크립트 README](../03_playbooks/scripts/README.md)의 (b)).

### 10.3 텔레메트리 (ahujasid)

| 수집 항목 | 기본 | 끄는 법 |
|---|---|---|
| install ID, session ID, tool 이름, 성공 여부, 소요 시간, 버전, OS, 타임스탬프 | **ON** | `DISABLE_TELEMETRY=true`(또는 `disable_telemetry` tool) |
| 프롬프트, 코드, 스크린샷, trajectory(콘텐츠) | OFF(opt-in, 2026-09-21부터) | 동의하지 않으면 수집하지 않음 |

README에는 수집 데이터가 "to train AI models"에 쓰일 수 있다고 적혀 있습니다. 회사 씬이나 미공개 IP를 다룬다면 반드시 끄세요. 텔레메트리를 코드에서 아예 제거한 포크로 owenpkent/blendmcp, TESSA LABS 포크가 있습니다. 공식 Blender Lab 서버는 조사 기준으로 텔레메트리가 없습니다.

### 10.4 권장 설정 체크리스트

1. **작업 전 저장**하고, 스크립트는 git에 커밋합니다(9.6절).
2. `DISABLE_TELEMETRY=true`, `BLENDER_MCP_SAFE_MODE=1`을 설정합니다(3.4절 JSON 예시).
3. 애드온은 **localhost에만** 바인딩합니다. 원격 Blender는 SSH 터널로 연결하고, 공유 머신에서는 쓰지 않습니다. Epic도 Unreal 플러그인에 대해 "Localhost is not a trust boundary"라고 경고합니다([Epic 플러그인](https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin)).
4. 모르는 .blend, 외부 에셋 설명, 웹 콘텐츠는 **프롬프트 인젝션** 경로가 될 수 있습니다. 다운로드한 .blend의 자동 스크립트 실행(Auto Run Python Scripts)은 꺼 두세요.
5. 설치 출처는 PyPI `mcp-for-blender`, GitHub, projects.blender.org만 씁니다. 비공식 사이트와 `pip install mcp-blender`는 쓰지 않습니다.
6. `--dangerously-skip-permissions`는 쓰지 말고, 명시적 allow 규칙이나 auto mode를 쓰세요.
7. 격리가 더 필요하면 blend-ai(허용 import 5개: bpy, bmesh, mathutils, math, json, 셰이더 노드 64종 allowlist, 127.0.0.1 전용), Scenario 내장 MCP(Python 실행 기본 OFF), 헤드리스 QA를 별도 프로세스로 두거나 VM·dev container에서 실행합니다.
8. 파괴적 코드는 훅으로 막습니다(`orphans_purge`, `read_factory_settings`, `import os/subprocess/shutil`). 예시는 [에이전트 워크플로 가이드](09_agent_workflow_prompting.md)에 있습니다.
9. 공식 Blender Lab 서버의 HTTP 모드(`--transport http`)는 필요할 때만 켜고 끕니다. `--host 0.0.0.0`은 쓰지 않습니다(10.5절).

### 10.5 공식 Blender Lab 서버의 보호 범위 (실측)

| 항목 | 실제 동작 |
|---|---|
| 코드 실행 보호 | `sys.exit`, `wm.quit_blender`, `wm.read_factory_settings`, `wm.read_factory_userpref`, `wm.read_userpref`만 막습니다. 소스 설명이 "this isn't really a sandbox"이고, `raise SystemExit` 한 줄로 백그라운드 Blender가 꺼집니다. `os`·파일·네트워크·`subprocess`는 막지 않습니다 |
| 애드온 소켓(9876) | 인증과 암호화가 없습니다. 로컬의 어떤 프로세스든 JSON을 보내 코드를 실행할 수 있습니다(ahujasid와 같음) |
| HTTP 모드 | CORS `*`, DNS 리바인딩 보호 꺼짐, 인증 없음, stateless. curl로 외부 Origin/Host 헤더를 붙여 보낸 `execute_blender_code`가 실행됐습니다(4.4절) |
| 온라인 접근 | Allow Online Access가 꺼져 있으면 애드온이 서버를 열지 않습니다. 스위치로 쓸 수 있습니다 |
| 텔레메트리 | 없음(외부 네트워크 호출 코드 없음) |

정리하면 공식 서버의 코드 실행도 **OS 권한을 넘기는 것**과 같습니다. 대응은 ahujasid와 같습니다. 저장·버전 관리, 클라이언트의 권한 규칙과 훅, 격리 환경을 쓰세요. 차이는 ahujasid의 safe mode 같은 사전 검사가 없다는 점입니다.

---

## 11. Blender 4.x → 5.x API 변경 함정 (LLM이 틀리는 코드)

모델의 학습 데이터에는 2.8x~4.x 코드가 많아서 5.x에서 `KeyError`·`AttributeError`가 반복됩니다. **코드를 쓰기 전에 Blender 버전부터 확인하게 하세요**(`get_addon_status` 또는 `bpy.app.version`).

### 11.1 함정 표

"확인"은 검증 에이전트가 bpy 5.0.1, fake-bpy-module 4.0/4.1/4.2 스텁, GitHub 이슈로 직접 확인한 것입니다. "2차"는 서드파티 스킬 문서나 공식 릴리스 노트의 검색 요약만 근거인 것입니다(공식 문서 원문은 차단됨).

| 버전 | LLM이 쓰는 옛 코드 | 올바른 코드 | 증상 | 근거 |
|---|---|---|---|---|
| 4.0 | `bsdf.inputs['Specular']` | `'Specular IOR Level'` | KeyError | 확인 |
| 4.0 | `'Clearcoat'` (3.x 이름) | `'Coat Weight'` | KeyError | 확인(이름 존재) |
| 4.0 | `'Transmission'` | `'Transmission Weight'` | KeyError | 확인 |
| 4.0 | `'Emission'` | `'Emission Color'` | KeyError | 확인 |
| 4.0 | `'Subsurface'`, `'Subsurface Color'` | `'Subsurface Weight'` (`'Subsurface Color'`는 없음) | KeyError | `'Subsurface Color'` 부재는 확인, `'Subsurface Weight'`는 2차 |
| 4.0 | `'Sheen'` | `'Sheen Weight'` | KeyError | 2차 |
| 4.0 | `bpy.ops.xxx(override_dict, ...)` | `with bpy.context.temp_override(area=..., region=...):` | TypeError | 2차 |
| **4.1** | `mesh.use_auto_smooth = True` | Smooth by Angle 모디파이어 또는 Shade Smooth by Angle | AttributeError | 확인(4.1에서 제거. cc-blender-skill 호환 문서의 '5.x에서 제거'는 오류) |
| 4.2 | `mat.blend_method = ...` | `mat.surface_render_method`(값은 런타임 enum으로 조회) | AttributeError | 2차 |
| 4.2 | `scene.eevee.use_bloom = True` | 컴포지터 Glare(Bloom) 노드 | AttributeError | 2차 |
| 4.2~4.x | `engine = 'BLENDER_EEVEE'` | `'BLENDER_EEVEE_NEXT'` | enum TypeError | 확인(4.2 스텁) |
| 4.4 | — | layered action(`action.layers`) 도입 | — | 2차(blender-kiln이 4.4를 하한으로 잡은 이유) |
| **5.0** | `engine = 'BLENDER_EEVEE_NEXT'` | `'BLENDER_EEVEE'` | enum TypeError | 확인 |
| 5.0 | `scene.node_tree`, `scene.use_nodes = True` | `scene.compositing_node_group`(초깃값 None → `bpy.data.node_groups.new('Comp', 'CompositorNodeTree')`로 만들어 할당) | `'Scene' object has no attribute 'node_tree'` | 확인([AI-Render #171](https://github.com/benrugg/AI-Render/issues/171), [holo-card #172](https://github.com/EverettFish/holo-card-studio/issues/172)) |
| 5.0 | `mat.use_nodes = True`, `world.use_nodes = True` | 5.0부터 노드 트리가 기본이고 `use_nodes`는 폐기 예고(6.0에서 제거 예정). 4.x 호환이 필요하면 `if mat.node_tree is None:`일 때만 설정 | DeprecationWarning | 확인(bpy 5.0.1) |
| 5.0 | `action.fcurves`, `action.groups` | `bpy_extras.anim_utils.action_get_channelbag_for_slot(action, slot).fcurves` (또는 `action.layers[].strips[].channelbags[].fcurves`) | AttributeError | 확인 |
| 5.0 | `import bgl` | `gpu` 모듈 | ImportError | 2차 |
| 5.0 | `image.bindcode` | 제거됨 | AttributeError | 2차 |
| 5.0 | `CompositorNodeGamma` 등, `CompositorNodeFilter.filter_type` | 일부는 셰이더 노드로 대체(`ShaderNodeGamma`), `filter_type` 제거 | 노드 생성 실패 | 2차·이슈 |
| 5.1 | 컴파일된 외부 휠, user site-packages 의존 | Python 3.13(ABI 변경), user site-packages는 기본으로 불러오지 않음 | ImportError | 2차(PyPI bpy는 확인) |
| 5.1.2 | Glare 노드 옵션을 속성으로 설정 | 옵션이 입력 소켓으로 바뀜 | AttributeError | 2차(제3자 PR 관찰) |
| 5.1.2 | bmesh로 수정한 직후 치수 측정 | depsgraph 갱신(`bpy.context.view_layer.update()`) 후 측정 | 옛 값이 나옴 | 2차(제3자 PR 관찰) |
| 5.2 | `mod['Socket_2'] = 5.0` (GN 모디파이어 입력) | `mod.properties.inputs.Socket_2.value = 5.0`이라는 주장 | — | **미확인**: 5.2에서 `bpy_api_lookup`으로 먼저 확인할 것 |
| 공통 | `nodes['Principled BSDF']` | `next(n for n in nodes if n.type == 'BSDF_PRINCIPLED')` | 현지화 UI에서 KeyError | 확인(일본어 UI 사례, 12절) |
| 공통 | `node.inputs['Subsurface IOR']`(비활성 소켓) | `for inp in node.inputs: if inp.name == name:` 헬퍼 | KeyError | 확인(bpy 5.0.1) |
| 공통 | `mat.diffuse_color = (...)`로 색 지정 | Principled `'Base Color'` 입력 | 렌더에 반영 안 됨(뷰포트 전용) | 서버 instructions |
| 공통 | `bpy.ops.view3d.*`를 exec 안에서 호출 | `region_3d` 속성을 직접 조작 | context poll 실패 | 스킬 문서 |
| 공통 | `bpy.ops.outliner.orphans_purge()` | 이름으로 명시 삭제 | 재질 소실 | 스킬 문서 |
| 공통 | `obj.dimensions`로 배치 계산 | `matrix_world @ bound_box`로 구한 월드 AABB | 회전한 물체의 크기가 틀림(dimensions는 스케일은 반영하지만 로컬 축 기준) | 확인(bpy 5.0.1) |

### 11.2 버전 호환 스니펫

```python
import bpy
v = bpy.app.version
scene = bpy.context.scene

# 1) 렌더 엔진: 4.2~4.x만 _NEXT (engine은 enum 조회의 예외라 버전으로 분기)
scene.render.engine = 'BLENDER_EEVEE_NEXT' if (4, 2, 0) <= v < (5, 0, 0) else 'BLENDER_EEVEE'

# 2) 재질: 5.0+는 노드 트리가 기본, use_nodes는 4.x에서만
mat = bpy.data.materials.get('MAT-oak') or bpy.data.materials.new('MAT-oak')
if mat.node_tree is None:
    mat.use_nodes = True
bsdf = next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')  # 이름 대신 type

# 3) 소켓: 이름이 있는지 확인하고 설정 (비활성 소켓도 안전)
def set_input(node, name, value):
    for inp in node.inputs:
        if inp.name == name:
            inp.default_value = value
            return True
    print(f"warn: no input {name!r} on {node.bl_idname}")
    return False

set_input(bsdf, 'Base Color', (0.30, 0.18, 0.09, 1.0))   # 선형 색
set_input(bsdf, 'Roughness', 0.45)
set_input(bsdf, 'Coat Weight', 0.2)

# 4) 컴포지터 노드 트리
if v >= (5, 0, 0):
    ng = scene.compositing_node_group
    if ng is None:
        ng = bpy.data.node_groups.new('Comp', 'CompositorNodeTree')
        scene.compositing_node_group = ng
else:
    scene.use_nodes = True
    ng = scene.node_tree

# 5) enum은 하드코딩하지 말고 런타임 조회 (예: 이미지 포맷)
fmts = [i.identifier for i in scene.render.image_settings.bl_rna.properties['file_format'].enum_items]
print("blender", v, "formats", fmts[:5])
```

이 저장소의 `review_views.py`도 같은 원칙(type으로 노드 찾기, `node_tree is None`일 때만 `use_nodes`)으로 작성돼 4.2.23 LTS와 5.0.1에서 경고 없이 통과합니다(`scene_audit.py`는 노드를 다루지 않고 메시 bbox만 검사).

### 11.3 추측 대신 조회하게 하기

| 수단 | 어디서 | 쓰임 |
|---|---|---|
| `bpy_api_lookup`, `describe_node_type` | ahujasid | RNA 시그니처, 노드 소켓 스키마(설치된 버전 기준이라 정확) |
| `get_python_api_docs` (+ `search_api_docs`, `search_manual_docs` 추정) | 공식 Blender Lab | 번들 API 문서, 매뉴얼 |
| `search_blender_docs`, `get_blender_doc_page`, `search_geometry_node_types` | newo-ether | 공식 매뉴얼·API 검색 |
| [fake-bpy-module](https://github.com/nutti/fake-bpy-module) | pip | 버전별 스텁을 grep하거나, 생성한 스크립트를 pyright·mypy로 미리 검사(런타임 동작은 못 잡음) |

프롬프트나 스킬에 이렇게 못박아 두세요.

```text
Before writing any node code, call describe_node_type("ShaderNodeBsdfPrincipled")
and use exact socket names returned. Never guess enum identifiers.

노드·소켓·enum 코드를 쓰기 전에 반드시 bpy_api_lookup / describe_node_type 으로 조회하고,
조회 결과의 정확한 이름만 사용할 것. Blender 버전(bpy.app.version)을 먼저 출력할 것.
```

---

## 12. [한국 사용자] 한국어 UI 현지화 문제와 해결

**문제**: Blender의 새 데이터 이름 번역이 켜져 있으면, 스크립트로 새로 만든 노드(그리고 원리상 새 데이터블록)의 이름이 UI 언어로 붙습니다. 그러면 `mat.node_tree.nodes['Principled BSDF']`가 KeyError를 내고, `.get()`을 쓰면 None이 나와 이후 코드가 조용히 틀어집니다.

- **확인된 사례**: 일본어 UI(Blender 4.5.7 LTS)에서 'Principled BSDF'가 'プリンシプルBSDF'로 생성돼 스크립트가 깨졌습니다([roo-blendermcp-jp-rules](https://github.com/hideki711014/roo-blendermcp-jp-rules)).
- **한국어**: 같은 원리가 적용될 것으로 **추정**합니다. 한국어 UI에서 실제로 번역되는지는 실측하지 못했습니다.
- **설정 존재 확인**: 번역을 끄는 속성 `use_translate_new_dataname`(Preferences > Interface > Translation > New Data)이 bpy 5.0.1 `PreferencesView`에 실제로 있습니다(검증 에이전트 확인).

**해결 (권장 순서)**

1. **코드는 이름이 아니라 `type`으로 노드를 찾습니다.** 노드 type은 언어 설정과 무관합니다.

   ```python
   bsdf = next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
   out  = next(n for n in mat.node_tree.nodes if n.type == 'OUTPUT_MATERIAL')
   ```

2. **에이전트용 Blender에서는 New Data 번역을 끕니다.** UI는 한국어로 두고 데이터 이름만 영어로 만들 수 있습니다.

   ```python
   bpy.context.preferences.view.use_translate_new_dataname = False
   ```

   더 확실하게 하려면 에이전트 작업 중에는 UI 언어를 English로 둡니다.
3. **프로젝트 규칙에 명시합니다.** [CLAUDE.md 템플릿](../03_playbooks/templates/CLAUDE.md)에 다음을 넣으세요. "노드와 소켓은 이름 대신 type과 identifier로 찾을 것. UI 번역 때문에 이름이 바뀔 수 있음. 오브젝트·재질 이름은 영어 + 접두사(GEO-/MAT-/LGT-/CAM-)로 지을 것."
4. **이름은 영어로 짓게 합니다.** 이 저장소의 `scene_audit.py`는 `chair`, `table`, `sofa`, `bed`, `door` 같은 영어 키워드로 치수 범위를 검사합니다. 한국어 이름이면 이 검사가 동작하지 않습니다.
5. **이미 한국어 이름으로 만들어진 파일**은 type으로 찾아서 이름을 바꿉니다(예: `for n in nodes: if n.type == 'BSDF_PRINCIPLED': n.name = 'Principled BSDF'`).

**그 밖의 한국 관련 사항**

- 로컬 Hunyuan3D(ahujasid 로컬 API URL 모드, RFingAdam, 공식 애드온)는 **한국이 라이선스 적용 지역에서 제외**돼 있습니다(3.3절).
- 가구 치수는 한국 규격이 미국·유럽과 다른 경우가 있습니다. [실측 치수표](../03_playbooks/05_reference_dimensions.md)를 기준으로 삼으세요.
- 한국어 설치 후기: [Threads @dddesign.io](https://www.threads.com/@dddesign.io/post/DXsWAspka7F/%ED%81%B4%EB%A1%9C%EB%93%9C-%EB%B8%94%EB%A0%8C%EB%93%9C-%EC%BB%A4%ED%85%8D%ED%84%B0-%EC%82%AC%EC%9A%A9%EB%B2%95%EA%B3%B5%EC%8B%9D-%EA%B0%80%EC%9D%B4%EB%93%9C%EA%B0%80-%EB%B6%88%EC%B9%9C%EC%A0%88%ED%95%B4%EC%84%9C-%EB%A7%8C%EB%93%AC1-claude-%EB%8D%B0%EC%8A%A4%ED%81%AC%ED%83%91-%EC%84%B8%ED%8C%85-%EC%BB%A4%EB%84%A5%ED%84%B0-%EC%9D%B4%EB%8F%992-blender-%EA%B2%80%EC%83%89-%EC%84%A0%ED%83%9D3-enbaled-%EB%88%84?hl=ko)(공식 커넥터 설정 순서), [클리앙](https://www.clien.net/service/board/park/19015735)(아이디어 시각화부터 모델링·텍스처링까지 약 7~10분이 걸렸다는 후기, 개인 테스트 n=1, 원문 미열람). 더 많은 자료는 [한국어 자료 모음](../04_case_studies/02_korean_resources.md)에 있습니다.

---

## 흔한 실수와 해결

| 증상 | 원인 | 해결 |
|---|---|---|
| 연결은 되는데 엉뚱하게 반응하거나 연결 실패 | 공식·ahujasid(·Scenario) 애드온이 모두 9876을 잡음 | 한 번에 하나만 켜거나 포트를 짝지어 변경(9.1절) |
| `uvx blender-mcp`로 공식 서버를 띄웠다고 착각 | PyPI `blender-mcp`는 ahujasid 호환 래퍼 | 공식 서버는 git 소스나 커넥터로 설치(4.3절) |
| 공식 서버가 연결 직후 끊김(`Connection closed`), 로그에 `No module named 'mcp.server.fastmcp'` | v1.0.0·v1.0.1 + MCP SDK 2.x | v1.0.2 이상, 또는 `uvx --with 'mcp[cli]<2'`(4.1·4.3절) |
| 공식 애드온이 켜지지 않음, 환경설정에 `Online access must be enabled` | Allow Online Access 꺼짐 | Preferences > System > Network에서 켜기, 명령줄은 `--online-mode`(4.3절) |
| 공식 서버 렌더 파일이 지정한 경로에 없음 | `bpy.app.tempdir/blender_mcp/`에 저장, 종료 시 삭제 | 렌더 직후 `execute_blender_code`로 복사(4.1절) |
| 헤드리스 서버에서 렌더 도구를 부르자 Blender가 죽음 | EEVEE + EGL 없음 | 렌더 엔진을 Cycles CPU로 바꾼 뒤 호출(4.1절) |
| 공식 서버에서 코드가 실패했는데 에이전트가 성공으로 보고 | 오류가 `isError`가 아닌 `status: "error"`로 옴 | 에이전트 규칙에 status 확인을 넣기(4.1절) |
| `spawn uvx ENOENT` | GUI 클라이언트의 PATH | uvx 절대경로(9.5절) |
| Windows에서 공식 커넥터 설치 실패 `error in 'egg_base' option` | 커넥터 v1.0.1의 uv 빌드 + 설치 경로 공백 문제(분석) | git 소스 + uv 수동 설정으로 우회(4.3절) |
| 큰 씬에서 AI가 일부 오브젝트를 모름 | `get_scene_info` 10개 제한, 치수 정보 없음 | 압축 요약 스크립트, `get_object_info`, `scene_audit.py`(9.3절) |
| 180초 뒤 실패하거나 Blender가 멈춤 | 긴 코드, 고해상도 다운로드, 렌더를 메인 스레드에서 실행 | 5~20줄 청크, 1k/2k 텍스처, 헤드리스 렌더(9.2절) |
| `KeyError: 'Principled BSDF'` | 한국어 UI의 New Data 번역 | type으로 찾기, New Data 번역 끄기(12절) |
| `'Scene' object has no attribute 'node_tree'` | 5.0 API 변경 | `compositing_node_group`(11.2절) |
| `enum "BLENDER_EEVEE_NEXT" not found` | 5.x 식별자 변경 | 버전 분기(11.2절) |
| 색을 바꿨는데 렌더에 안 나옴 | `diffuse_color`는 뷰포트 전용이거나, Solid 셰이딩이라 안 보임 | Principled `Base Color` 설정, 뷰포트를 Material Preview로 전환 |
| Ctrl+Z나 `/rewind`로 AI 변경이 안 돌아감 | 애드온이 undo_push를 안 함, 체크포인트는 Blender 상태를 추적하지 않음 | 단계마다 증분 저장(9.6절) |
| 헤드리스 스크립트가 실패했는데 성공으로 보고됨 | 예외가 나도 종료 코드 0 | `--python-exit-code 1`(6절) |
| `pip install mcp-blender` 후 이상한 코드가 설치됨 | PyPI 이름이 다른 패키지 | RFingAdam은 소스로 설치(5.1절) |
| 헤드리스 리눅스에서 EEVEE 렌더 실패 | GPU·EGL 컨텍스트 없음 | Cycles(CPU) 사용 |
| 스크린샷 루프가 길어지자 `invalid_request_error` | 이미지 20개 초과 시 치수 제한 강화 | 각 변 2000px 이하, 캡처는 800~1000px(9.4절) |
| Tripo 생성이 안 됨 | ahujasid에서 Premium 전용 | Premium 구독, [Tripo SDK](https://pypi.org/project/tripo3d/)·ComfyUI 노드, 또는 다른 생성기(tripo-mcp는 방치 상태라 비권장) |
| 로컬 Hunyuan3D를 한국에서 사용 | 라이선스 지역 제외 | 다른 생성기를 쓰거나 Tencent Cloud 약관을 별도 검토 |
| Windows에서 명령이 약 4분 동안 무반응 | 미해결 이슈 #339/#357 | 재시작, 최신 버전, 헤드리스 우회 |

---

## 관련 문서

- [컴퓨터 유즈 vs MCP vs 스크립트](12_computer_use_and_other_methods.md): MCP·헤드리스·화면 조작을 언제 쓰나
- [목적·범위](../00_purpose/purpose_and_scope.md) · [조사 방법·신뢰도 정책](../01_research/research_method.md) · [출처 카탈로그](../01_research/sources_catalog.md) · [검증 로그](../01_research/verification_log.md)
- [AI 모델 비교·MCP 클라이언트·비용](01_ai_models_and_clients.md): Codex 기본 effort, 모델별 단가
- [기타 DCC·CAD·게임엔진 MCP](03_other_mcp_dcc_cad_engines.md): Fusion, SketchUp, Unreal 5.8 공식 MCP 등
- [AI 3D 생성](04_ai_3d_generation.md) · [텍스처링·재질](05_texturing_materials.md) · [라이팅·렌더](06_lighting_rendering_art_direction.md)
- [오브젝트·가구·조형 모델링](07_modeling_objects_furniture_sculpture.md) · [배치·레이아웃](08_scene_layout_placement.md)
- [에이전트 워크플로·프롬프팅](09_agent_workflow_prompting.md): 시각 피드백 루프, 훅, 서브에이전트, 비용
- [에셋·파이프라인·라이선스](10_assets_pipeline_licensing.md): Hunyuan3D 지역 제외, CC-BY 표기
- [빠른 시작](../03_playbooks/01_quickstart_setup.md) · [AAA 제작 플레이북](../03_playbooks/02_aaa_production_playbook.md) · [프롬프트 템플릿](../03_playbooks/03_prompt_templates.md) · [품질 체크리스트](../03_playbooks/04_quality_checklists.md)
- [보조 스크립트 사용법](../03_playbooks/scripts/README.md): `scene_audit.py`, `placement_utils.py`, `review_views.py`
- [CLAUDE.md 템플릿](../03_playbooks/templates/CLAUDE.md) · [Blender 스킬 템플릿](../03_playbooks/templates/skills/blender-aaa-scene/SKILL.md)
- [사례 모음](../04_case_studies/01_case_studies.md) · [한국어 자료](../04_case_studies/02_korean_resources.md)

## 원자료

- [`01_research/raw/02_blender-mcp.research.json`](../01_research/raw/02_blender-mcp.research.json): Blender MCP 생태계 조사(항목 19, 노하우 20, 사례 7)
- [`01_research/raw/02_blender-mcp.verify.json`](../01_research/raw/02_blender-mcp.verify.json): 독립 검증(판정 21, 항목 점검 16, 신뢰도 낮은 출처 8, 누락 항목 8)
- [`01_research/raw/10_agent-workflow.research.json`](../01_research/raw/10_agent-workflow.research.json): 에이전트 워크플로 조사(서버·스킬·API 함정·현지화 부분)
- [`01_research/raw/10_agent-workflow.verify.json`](../01_research/raw/10_agent-workflow.verify.json): 독립 검증(safe mode 범위, 스크린샷 기본값, `use_auto_smooth` 4.1, `use_translate_new_dataname` 확인 등)
- [`01_research/raw/G8_blender_lab_mcp.gap.json`](../01_research/raw/G8_blender_lab_mcp.gap.json): 공식 Blender Lab 서버 소스 정독·실제 구동 검증(항목 14, 노하우 6, 출처 23)
- [`01_research/handson/blender_lab_mcp/`](../01_research/handson/blender_lab_mcp/README.md): 위 검증의 절차, 도구 목록·호출 응답 원본, 재현 도구
- [`01_research/raw/G8_blender_lab_mcp.verify.json`](../01_research/raw/G8_blender_lab_mcp.verify.json): 남은 미확인 항목 후속 확인(판정 9: 확인 2 · 부분 4 · 미확인 3, 메인 에이전트 수행)
