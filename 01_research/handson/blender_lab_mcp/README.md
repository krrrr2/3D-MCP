# 공식 Blender Lab MCP 서버: 실제 구동 검증 기록

> 작성: 2026-09-27 · 결론 요약은 [Blender MCP 가이드 4절](../../../02_guides/02_blender_mcp.md#4-공식-blender-lab-서버-상세) · 구조화 원자료: [`../../raw/G8_blender_lab_mcp.gap.json`](../../raw/G8_blender_lab_mcp.gap.json) · 응답 원본: [`raw/`](raw/) · 재현 도구: [`tools/`](tools/)

## 1. 왜 했나

사용자 요청은 "확인 못 한 항목(Astra 공식 정보, Tripo·Rodin 약관, 네이버·한국어 원문)은 빼고, **블렌더 공식 MCP를 조사**하라"였습니다.
그전까지 가이드의 공식 서버 내용은 검색 요약과 제3자 설치 키트에 기대고 있었고, "미확인"으로 남긴 항목(최신 도구 목록, 코드 실행 안전장치, 타임아웃, 설치 원문)도 있었습니다.
그래서 **소스를 전부 읽고, 실제로 띄워서 도구를 하나씩 불러 보는** 방식으로 확인했습니다.

## 2. 무엇으로 했나

| 항목 | 내용 |
|---|---|
| 소스 | GitHub 미러 [bpype/blender_mcp](https://github.com/bpype/blender_mcp/commit/98b0e49d98321d321c7e631389200f513f765d59) 커밋 98b0e49(2026-05-05, 커밋 95개). 서버 `blender-mcp` 1.0.0, 애드온 `mcp` 1.0.0(`blender_version_min` 5.1.0). blender.org·projects.blender.org는 네트워크 정책으로 차단돼 미러를 `git clone`해 읽음 |
| Blender | pip `bpy` 5.2.2 LTS(Python 3.13). blender 실행 파일은 받을 수 없어서 애드온 폴더를 `sys.path`에 넣고 `register()` 후 애드온의 CLI 핸들러(`--command blender_mcp`와 같은 경로)로 서버를 띄움 |
| MCP 서버 | 미러의 `mcp/` 폴더를 venv에 설치. MCP 파이썬 SDK는 최신 2.2.0과 `mcp[cli]<2`(1.30.0) 두 가지로 시험 |
| 클라이언트 | MCP 파이썬 SDK의 stdio 클라이언트로 `initialize`, `tools/list`, `tools/call`. `_for_cli` 도구는 `BLENDER_PATH`에 bpy로 흉내 낸 `fakeblender.sh`를 지정 |
| 장면 | house-3d Fable 판을 GLB로 옮긴 `.blend`(오브젝트 약 1,000개, [building_audit 검증](../../../03_playbooks/scripts/validation/README.md)에 쓴 것) |
| 환경 | 리눅스 컨테이너, GPU·EGL 없음 |

## 3. 결과

### 3.1 설치·시작

| 확인한 것 | 결과 |
|---|---|
| 온라인 접근이 꺼진 상태로 시작 | **거부**: `Online access must be enabled in the system preferences` / `Use --online-mode ...`, 종료 코드 1 |
| `preferences.system.use_online_access = True` 후 시작 | `MCP server started on localhost:9876` |
| MCP SDK 2.2.0으로 서버 실행 | **import 단계에서 즉시 종료**: `No module named 'mcp.server.fastmcp'. This is mcp 2.x, where FastMCP was renamed to MCPServer ...`. 클라이언트에는 `Connection closed`만 보임 |
| `uvx --from <소스>/mcp blender-mcp` | 위와 같은 오류(최신 2.x를 받기 때문) |
| `uvx --with 'mcp[cli]<2' --from <소스>/mcp blender-mcp` | 정상 |
| 공식 단위 테스트 4개 파일 | mcp 1.30.0: **102 passed** / mcp 2.2.0: 19 failed, 16 errors, 7 passed |

- 원인: `pyproject.toml`의 의존성이 `mcp[cli]>=1.2.0`뿐이고 잠금 파일이 없습니다. PyPI 기준 mcp 2.0.0은 2026-07-28에 나왔습니다. 그 뒤로 v1.0.0 계열을 새로 설치하면 2.x가 깔려 서버가 죽습니다.
- 검색 결과 요약에 따르면 [릴리스 페이지](https://projects.blender.org/lab/blender_mcp/releases)의 v1.0.2(2026-09-08)가 이 문제를 "Make sure the system uses the MCP SDK <2"로 고쳤습니다. v1.0.3(2026-09-11)은 "Fix the long standing screenshot capture tool"입니다. 페이지 원문은 차단돼 열지 못했습니다.

### 3.2 도구 목록: 26개

README 목록은 24개인데, 실제 서버는 **26개**를 돌려줍니다(`search_api_docs`, `search_manual_docs`가 추가). 이 두 검색 도구는 2026-04-16 커밋으로 v1.0.0 전부터 있었습니다. prompts와 resources는 0개입니다.

| 표시 | 도구 |
|---|---|
| `readOnlyHint` | `get_blendfile_summary_{datablocks, missing_files, of_linked_libraries, path_info, usage_guess}` 와 각각의 `_for_cli`, `get_objects_summary`, `get_object_detail_summary`, `get_python_api_docs`, `search_api_docs`, `search_manual_docs`, `get_screenshot_of_area_as_image`, `get_screenshot_of_window_as_image`, `get_screenshot_of_window_as_json`, `render_viewport_to_path` |
| `destructiveHint` | `execute_blender_code`, `execute_blender_code_for_cli`, `jump_to_tab_by_name`, `jump_to_tab_by_space_type`, `jump_to_view3d_object_by_name`, `jump_to_view3d_object_data_by_name`, `render_thumbnail_to_path` |

- 모델에 들어가는 분량: 서버 instructions 약 5,900자 + 도구 이름·설명·입력 스키마 약 14,700자입니다. 영어 기준 대략 5천 토큰 안팎(문자 수÷4로 어림)입니다.
- 원본: [`raw/tools_list.json`](raw/tools_list.json). instructions와 도구 설명 원문 포함, Blender Authors 저작, GPL-3.0-or-later.

### 3.3 도구별 호출 결과 (백그라운드 모드)

| 도구 | 결과 |
|---|---|
| `get_objects_summary` | 컬렉션 트리와 오브젝트(이름·타입·부모·데이터·선택·표시), 0.06초. 오브젝트 1,019개를 **전부** 돌려줌(개수 제한 없음 → 큰 장면은 응답이 큼) |
| `get_object_detail_summary` | 변환·치수·부모·모디파이어·재질·컬렉션. 없는 이름이면 `status: error`와 함께 **전체 오브젝트 이름 목록** |
| `get_blendfile_summary_*` 5종 | 데이터블록 수, 누락 파일, 링크 라이브러리, 경로·저장 여부·백업 파일, 용도 추정(Modeling 25점 등) 모두 정상 |
| `execute_blender_code` | `result = {...}`에 dict를 넣어 반환. print 출력은 `stdout` 필드로 옴. dict가 아니면 안내 오류. Blender 객체는 `repr` 문자열로 바뀜. 예외는 트레이스백 |
| `get_python_api_docs` | `bpy.types.BevelModifier` 전문. 없는 식별자는 `found: false` |
| `search_api_docs` / `search_manual_docs` | 모든 단어가 한 문단(또는 경로·제목)에 있어야 맞는 AND 검색. `bevel modifier segments`는 0건, `bevel segments`는 `bpy.ops.mesh.bevel` 적중. 영어 문서라 한국어 질의는 0건. 0.2~1.5초 |
| `*_for_cli` | 다른 `.blend`를 새 프로세스로 열어 실행(3~4초). **지금 열려 있는 파일이 수정 중이면** `이름_mcp_0001.blend` 사본을 저장해 분석하고 지움 |
| `render_thumbnail_to_path` / `render_viewport_to_path` | 카메라가 없으면 `Cannot render, no camera`. Cycles CPU에서는 정상(1~2.5초) |
| 렌더 + EEVEE | **Blender 프로세스가 죽음**(`Couldn't open libEGL.so.1`, 종료 코드 134). 이후 모든 호출이 `Cannot connect to Blender` |
| `get_screenshot_of_window_as_json`, `jump_to_*` | `Not available in background mode` / `Window layout is not available in background mode` |
| `get_screenshot_of_window_as_image` | MCP `isError: true` — `Screenshots are not available in background mode` |

- **렌더 결과는 요청한 경로에 저장되지 않습니다.** `output_path`에서 파일 이름만 떼어 `bpy.app.tempdir/blender_mcp/`에 저장하고 그 경로를 돌려줍니다. 이 폴더는 Blender가 끝나면 지워집니다(실측). 필요하면 렌더 직후 `execute_blender_code`로 복사하세요.
- `render_viewport_to_path`는 이름과 달리 OpenGL 뷰포트 캡처가 아니라 **현재 렌더 설정으로 하는 F12 렌더**입니다. 썸네일은 긴 변 320px에 Cycles 16샘플입니다. EEVEE 샘플 조정은 `BLENDER_EEVEE_NEXT`일 때만 적용되는데, 5.x의 식별자는 `BLENDER_EEVEE`라 5.x에서는 적용되지 않습니다.
- **오류가 대부분 "정상 응답 속 `status: error`"로 옵니다.** MCP의 `isError`가 true인 경우는 스크린샷 이미지와 연결 실패뿐이었습니다. 에이전트 규칙에 "결과의 status를 확인하라"를 넣어야 합니다.

### 3.4 한계값

| 항목 | 값 | 확인 방법 |
|---|---|---|
| MCP 서버 → 애드온 응답 대기 | 300초 | 소스(`connection.py`) |
| `_for_cli` 서브프로세스 | 120초 | 소스(`blender_cli.py`) |
| 애드온이 요청을 읽는 대기 | 10초(실행 시간 제한 아님) | 소스 |
| 요청 크기 | 최대 10 MiB | 11 MiB 코드 → `Request exceeds 10485760 byte limit` |
| 응답 크기 | 제한 없음 | 12 MiB 문자열 반환 성공(5.8초) |
| 호스트·포트 | `BLENDER_MCP_HOST`/`BLENDER_MCP_PORT`, 기본 `localhost:9876` | 소스 |

### 3.5 약한 샌드박스

| 코드 | 결과 |
|---|---|
| `sys.exit(0)` | 막힘 (`sys.exit() is not allowed in LLM-generated code`) |
| `bpy.ops.wm.quit_blender()` / `read_factory_settings()` | 막힘 |
| `raise SystemExit(0)` | **Blender 종료**. 실행기가 `Exception`만 잡고 `SystemExit`(BaseException)는 못 잡음 |
| `os.getcwd()`, `os.listdir('/home/user')` | 그대로 실행(파일·OS 제한 없음) |

소스 설명 그대로 "this isn't really a sandbox"입니다. 실수를 줄이는 장치일 뿐 격리가 아니므로, 저장·버전 관리·클라이언트 권한 규칙으로 막아야 합니다.

### 3.6 HTTP 모드

`blender-mcp --transport http`는 기본값으로 `http://127.0.0.1:8000/`에서 뜹니다(streamable-http, stateless, 경로 `/`). llama.cpp 웹 UI 같은 브라우저 클라이언트를 위해 **CORS를 전부 허용하고 DNS 리바인딩 보호를 끕니다.** 인증도 없습니다.

| 요청 (curl) | 결과 |
|---|---|
| `OPTIONS /`, Origin 헤더를 외부 도메인(evil.example)으로 | 200, `access-control-allow-origin: *` |
| `POST /` 같은 Origin, initialize 없이 `tools/call execute_blender_code` | 200, **코드 실행 결과 반환** |
| `Host: attacker.example:8000`으로 `tools/list` | 200 |

- 브라우저에서 악성 페이지로 직접 재현하지는 않았습니다. 최신 브라우저의 로컬 네트워크 접근 제한이 이를 얼마나 막는지도 확인하지 못했습니다. 그래도 "HTTP 모드를 켜 둔 동안 브라우저로 연 웹페이지가 Blender에서 코드를 실행할 수 있는 구조"이므로 필요할 때만 켜세요.
- 8000번은 blender-open-mcp와 Unreal 5.8 공식 MCP의 기본 포트와 겹칩니다. 로컬 LLM 문서의 `--port 9191`은 예시 값입니다.

### 3.7 이 저장소 스크립트를 공식 MCP로 돌리기

`execute_blender_code`에 아래처럼 넣으면 그대로 동작했습니다(Fable 현대식 장면, **0.8초**, 방 10·문 9·창 9, 오류 0·경고 3). 이는 [검증 기록](../../../03_playbooks/scripts/validation/README.md)의 결과와 같습니다.

```python
import sys
sys.path.insert(0, "/절대경로/3D-MCP/03_playbooks/scripts")
import building_audit as ba
rep = ba.audit_building()
result = {"summary": rep["summary"], "issues": rep["issues"][:20]}
```

### 3.8 기타

- 소스(`mcp/blmcp`, 애드온)에 외부로 나가는 네트워크 코드가 없습니다. 텔레메트리가 없다는 기존 서술을 소스로 확인했습니다. `chat_client`만 LLM API를 부릅니다.
- 번들 문서: Blender **5.1** Python API RST 2,173개(15 MB), 매뉴얼 RST 2,217개(13 MB).
- PyPI `blender-mcp`(2.0.0)는 ahujasid 서버로 넘겨 주는 래퍼입니다. 공식 서버의 패키지 이름도 `blender-mcp`라서 **PyPI 이름으로는 공식 서버를 받을 수 없습니다.**
- 공식 예시와 LLM 통합 테스트의 과제는 모두 **분석·점검형**입니다. 데이터블록 이름 오타 수정, 재질 사용처 찾기, 폴리곤 이상치, 아마추어에 변형되지 않는 메시, 체크리스트 검증 같은 것들입니다.

## 4. 후속 확인과 남은 것

사용자 요청으로 남은 항목을 한 번 더 확인했습니다. 원자료는 [`../../raw/G8_blender_lab_mcp.verify.json`](../../raw/G8_blender_lab_mcp.verify.json)에 있고, 독립 검증이 아니라 메인 에이전트가 확인한 것입니다. projects.blender.org·lab.blender.org는 이번에도 연결되지 않았습니다.

| 항목 | 결과 | 근거 |
|---|---|---|
| v1.0.3의 도구 수 | **26개로 같음** | [외부 스모크 테스트](https://github.com/devotionn/blender-codex-lab/pull/1)(2026-09-22, v1.0.3, Blender 5.2.2 LTS macOS), 공식 `readme_tools.rst`(2026-08-06) |
| Claude 커넥터 버전 | **v1.0.1**(2026-09-27 커넥터 페이지 직접 확인). 공식 최신 v1.0.3보다 뒤처짐 | [커넥터 페이지](https://claude.com/connectors/blender) |
| SDK 2.x 문제 | 공식 코드를 담은 파생판도 2026-09-06에 같은 이유로 MCP v1 고정. 2026-08-06 공식 코드의 의존성은 아직 상한 없음 | [bpy-dev/blender-mcp](https://github.com/bpy-dev/blender-mcp) git 이력 |
| v1.0.3 스크린샷 수정 | 관련 공식 커밋 확인: 스크린샷 크기 한도에 JSON 포장분 2 KiB 여유(2026-08-06). v1.0.3 수정의 전부인지는 미확인 | 파생판에 포함된 공식 커밋 4309a39 |
| HTTP 모드 설정 | 2026-08-06 공식 커밋까지 서버 설정 파일 변경 없음. v1.0.2·v1.0.3은 미확인 | 같은 git 이력 비교 |
| Windows 설치 실패 | 커넥터 v1.0.1이 uv 빌드 중 `egg_base` 오류로 실패. 설치 경로 공백 문제가 겹친다는 분석. 공식·Claude Code 이슈 모두 클라이언트 문제로 닫힘 | [Claude Code 이슈](https://github.com/anthropics/claude-code/issues/54798), [공식 #24](https://projects.blender.org/lab/blender_mcp/issues/24)(검색 요약) |

아직 남은 것:

- v1.0.1의 변경 내용
- v1.0.2·v1.0.3의 전체 변경 내용(특히 HTTP 설정)
- 커넥터(v1.0.1)가 SDK 2.x 문제의 영향을 받는지
- GUI 모드의 스크린샷·UI 이동·지연 응답 실제 동작
- 실제 blender 실행 파일이 필요한 공식 통합 테스트와 LLM 통합 테스트

## 5. 다시 해 보려면

```bash
# 0) 공식 소스 (projects.blender.org 가 되면 그쪽, 아니면 미러)
git clone https://github.com/bpype/blender_mcp.git && cd blender_mcp && git checkout 98b0e49

# 1) Blender 쪽: bpy 5.1 이상
python3.13 -m venv bpyvenv && bpyvenv/bin/pip install "bpy==5.2.2"
BLMCP_ADDON_DIR=$PWD/addon bpyvenv/bin/python <이 폴더>/tools/blender_side.py scene.blend &
#    --offline 을 붙이면 온라인 접근 검사로 거부되는 것을 볼 수 있음

# 2) MCP 서버 쪽: mcp<2 고정 (고정하지 않으면 3.1의 import 오류 재현)
python3.13 -m venv srv && srv/bin/pip install ./mcp "mcp[cli]<2" pytest
BLMCP_BIN=$PWD/srv/bin/blender-mcp srv/bin/python <이 폴더>/tools/client_list.py tools_list.json

# 3) 도구 호출 (plans/*.json 안의 ${SCRATCH} 는 .blend 를 둔 폴더)
export SCRATCH=/장면/폴더 BPY_PYTHON=$PWD/bpyvenv/bin/python BLENDER_PATH=<이 폴더>/tools/fakeblender.sh
BLMCP_BIN=$PWD/srv/bin/blender-mcp srv/bin/python <이 폴더>/tools/client_call.py <이 폴더>/tools/plans/plan1.json out1.json

# 4) 공식 단위 테스트
srv/bin/python -m pytest -q tests/test_tool_listing.py tests/test_mcp_server.py tests/test_rst_parse.py tests/test_rst_search.py
```

- `plan3b.json`에는 EEVEE 렌더가 없습니다. EEVEE 렌더로 Blender가 죽는 것은 첫 시도(`plan3`)에서 확인했고, 결과는 [`raw/tool_call_results.json`](raw/tool_call_results.json)의 `3_eevee_crash`에 있습니다. `raise SystemExit`도 서버를 끄므로 plan 마지막에 두었습니다.
- 10 MiB 초과 요청 시험(11 MiB 코드)은 파일 크기 때문에 plan에서 뺐습니다. 필요하면 `"#" + "a"*(11*1024*1024)`를 코드로 보내면 됩니다.

| 파일 | 역할 |
|---|---|
| `tools/blender_side.py` | pip bpy 안에서 공식 애드온의 백그라운드 서버 실행 |
| `tools/fake_blender.py`, `tools/fakeblender.sh` | `_for_cli`용 `BLENDER_PATH` 대체(`--background FILE --python-expr CODE` 형식만) |
| `tools/client_list.py` | initialize·목록 조회 결과 저장 |
| `tools/client_call.py` | plan대로 도구 호출·결과 저장 |
| `tools/plans/*.json` | 실제로 쓴 호출 목록 |
| `raw/tools_list.json` | 목록 조회 응답 원본 |
| `raw/tool_call_results.json` | 호출 결과(긴 문자열 700자, 긴 목록 15개에서 자름) |
| `raw/run_notes.json` | 콘솔 출력 발췌(온라인 접근, SDK 2.x 오류, 단위 테스트, EEVEE, SystemExit, HTTP, PyPI) |
