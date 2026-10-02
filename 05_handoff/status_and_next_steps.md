# 진행 상태 · 결정 기록 · 다음 작업 (인수인계)

> 최종 갱신: 2026-09-27 · 브랜치 `claude/aaa-graphics-ai-modeling-u9zdts` · PR: https://github.com/krrrr2/3D-MCP/pull/1
> 이 문서만 읽으면 다른 사람이나 AI가 이어서 작업할 수 있도록 썼습니다.
>
> **다음 세션 시작점 (2026-09-27 세션 종료 시점)**: 사용자가 "그만하고 정리"를 요청해 이 세션의 작업은 여기서 끝났습니다. 미완료 작업은 없고, 남은 일은 6절의 선택 과제뿐입니다.
> 먼저 읽을 것:
> 1. [README](../README.md)
> 2. 이 문서 2·5·6절
> 3. 필요한 주제의 가이드
>
> 자주 묻는 것:
> - "배치·조형 보조 도구가 뭐가 있나" → [배치·조형 보조 도구 한눈에 보기](../03_playbooks/06_placement_structure_helpers.md) (맨 앞: MCP·스킬·컴퓨터 유즈용 도우미 표, 그다음 GitHub 라이브러리 표)
> - "공식 Blender MCP는 어떤가" → [Blender MCP 가이드 4절](../02_guides/02_blender_mcp.md)과 [구동 검증 기록](../01_research/handson/blender_lab_mcp/README.md)

## 1. 현재 목표

사용자 요청: "아스트라·페이블·오푸스 5.5 같은 AI와 MCP로 모델링·텍스처를 예쁘게 해서 AAA급 그래픽을 만드는 노하우, MCP 추천, 오브젝트·가구·조형·배치가 제대로 되기 위한 자료, 다른 사람들이 어떻게 했는지를 최대한 많이 수집해 체계적으로 정리."
상세 해석과 요구사항 대응표: [00_purpose/purpose_and_scope.md](../00_purpose/purpose_and_scope.md)

## 2. 현재 상태: 1차 완료

| 구분 | 상태 | 비고 |
|---|---|---|
| 조사 (13개 주제) | ✅ 완료 | 주제마다 조사 에이전트 1 + 독립 검증 에이전트 1 |
| 공백 보완 조사 (8개) | ✅ 완료 | 치수·라이선스는 독립 재검증까지. G7(컴퓨터 유즈)은 메인 에이전트가 직접 조사. G8(공식 Blender Lab MCP)은 소스 정독 + 실제 구동 검증 |
| 원자료 보존 | ✅ | `01_research/raw/` 49개 JSON (수정 금지) + 실제 구동 응답 원본 `01_research/handson/blender_lab_mcp/raw/` |
| 출처 카탈로그·검증 로그 | ✅ 자동 생성 | 고유 URL 약 1,470개 |
| 가이드 12편 · 플레이북 5편 · 템플릿 2 · 사례집 2 | ✅ 작성 | 약 13,800줄 |
| 문서 교차 검토 | ✅ 완료 | 5개 그룹 모두 독립 검토 완료(3~5그룹은 한도 해제 후 재실행). 아래 3절 참고 |
| 보조 스크립트 4종 + 테스트 | ✅ | `scene_audit`·`placement_utils`·`review_views`·`building_audit`, 테스트 3종 Blender 4.2.23 LTS·5.0.1·5.2.2 LTS 통과 |
| 공식 Blender Lab MCP 실제 구동 검증 | ✅ | bpy 5.2.2 LTS + 공식 서버(미러 98b0e49). 도구 26개 중 24개 호출, 공식 단위 테스트 102개 통과(mcp 1.30). SDK 2.x 비호환·HTTP 모드 CORS 전체 허용·렌더 저장 위치·EEVEE 헤드리스 종료 등 확인 → [검증 기록](../01_research/handson/blender_lab_mcp/README.md) |
| `building_audit` 실제 AI 건물 검증 | ✅ | 실제 AI 생성 건물 9개 장면(GPT-6 Astra 1, Fable 4, GPT-6 4). 오탐 25종 수정, 백룸 오경보 0 → [검증 기록](../03_playbooks/scripts/validation/README.md) |
| 배치·조형 보조 도구 색인 | ✅ | `03_playbooks/06_placement_structure_helpers.md`: 이 저장소 스크립트·가이드 코드, 배치 검사가 들어 있는 MCP, MCP 아닌 솔버·스킬·평가를 한 장에 모음(주요 Blender MCP에는 배치 검사 기능이 없음) |
| 인체·유기물·건물 도구 + 설치 안전 | ✅ | 2026-09-27 추가 조사(G9~G12, 읽기 전용, 핵심 주장 원문 대조). 가이드 `13_humans_organic_buildings.md`, `14_tool_install_safety.md`. 색인 06에 분야별 표 추가 |
| 문서 링크 자동 검사 | ✅ | 외부 URL 전부 원자료에 존재, 깨진 내부 링크 0 |

## 3. 교차 검토 현황 (중요)

문서 작성 후 5개 그룹으로 나눠 독립 검토자를 돌렸는데, **사용량 주간 한도에 걸려 3개 그룹의 에이전트 검토가 실패**했습니다.

| 그룹 | 문서 | 검토 |
|---|---|---|
| 1 | 01 AI 모델, 02 Blender MCP, 03 기타 MCP, 빠른 시작 | ✅ 에이전트 검토 완료 |
| 2 | 04 AI 3D 생성, 05 텍스처, 06 라이팅, 10 라이선스 | ✅ 에이전트 검토 완료 |
| 3 | 07 모델링, 08 배치, 치수표, 체크리스트 | ✅ 에이전트 검토 완료(재실행) |
| 4 | 09 워크플로, 11 연구, 제작 플레이북, 프롬프트 템플릿, CLAUDE.md, SKILL.md | ✅ 에이전트 검토 완료(재실행) |
| 5 | 사례 모음, 한국어 자료 | ✅ 에이전트 검토 완료(재실행) |
| G7 | 12 컴퓨터 유즈 가이드 + 원자료 G7 | ✅ 독립 검증 25건: 확인 17 · 부분 5 · 반박 0 · 미확인 3 (`raw/G7_computer_use.verify.json`) |

메인 에이전트가 3~5그룹에 대해 한 점검:
- 작성자·검토자가 남긴 "다른 문서가 맞춰야 할 사항" 목록을 전부 모아 문서 전체를 검색하고 고쳤습니다: MCP 유휴 타임아웃(stdio 30분·HTTP 5분), `BLENDER_MCP_SAFE_MODE` 범위(직접 파일 I/O만 차단, bpy 저장·렌더는 허용), tripo-mcp 비권장(2025-04-14 이후 방치), Step1X-3D 텍스처 모듈의 Hunyuan 코드 포함, CADGenBench는 도구 저자 자체 평가, kiln 갤러리는 헤드리스 스크립트 결과, 치수표의 검증 정정(계단참 2 m, NKBA 813/914/1118, K/LK 범위, 천장고 구축/신축).
- `check_docs.py`로 모든 문서의 외부 URL이 원자료에 있는지 확인했습니다(지어낸 URL 0건).
- 각 작성자는 원자료와 검증 결과를 직접 읽고 반영하도록 지시받았고, 대부분의 정정(Lumen Static/Stationary, `use_auto_smooth` 4.1 제거, Iron Rules 31개, 스크린샷 기본 1000px 등)이 이미 반영되어 있음을 확인했습니다.

**재검토 결과(2026-09-27)**: 사용량 한도가 풀려 3~5그룹 독립 검토와 G7 검증을 다시 돌렸습니다. 스크립트 개선 이후 낡은 설명(부분 문자열 매칭, 벽·천장 관통 미검출 등) 정정, 반박된 표현("엔진 MCP 설정에서 하루를 날림" 등) 정정, 미확인 수치 표시, 약어 설명, 코드 조각 수정(08 가이드 4.6절, 체크리스트 0.5절; 두 Blender 버전에서 실행 확인)이 반영됐습니다. `save_mainfile(incremental=True)`는 메인 에이전트가 4.2.23 LTS·5.0.1에서 직접 확인했습니다(번호 파일로 저장되고 현재 파일도 그쪽으로 바뀜, 저장 안 한 파일에서는 RuntimeError).

**남은 위험**: 네트워크 정책으로 원문을 열지 못한 출처는 여전히 검색 요약 기반입니다(5절).

## 3.5 추가 요청 반영 (PR 생성 후)

| 요청 | 반영 |
|---|---|
| "스크립트로 가구 배치 실수를 잡나? 건물 조형은?" | 데모로 확인 후 `scene_audit.py` 개선: 박힘(`sunk_into`)을 떠 있음으로 오탐하던 문제 수정, 컬렉션 범위 검사(`collection=`) 추가 |
| "한국 기준이 아니라 사람이 만든 것처럼 상식적인지, 백룸처럼 기묘한 걸 잡아야" | `building_audit.py` 신규: 문·창·방 연결·동선·벽·계단·앉는 방향의 상식 검사 + 백룸 위험도. 정상 집 0건, 이상한 집은 넣은 기묘함 전부 검출(테스트) |
| "컴퓨터 유즈가 직접 모델링하는 게 낫다는데?" | 웹 조사 후 `02_guides/12_computer_use_and_other_methods.md` 작성. 결론: 만드는 건 스크립트·MCP, 컴퓨터 유즈는 확인·API 없는 조작용 |
| "문은 건물 디자인 생각해서 어느 쪽으로 열려야 합당할지 정하고, 렌더링까지 하면 되지?" | 맞음. `building_audit`가 여닫이문마다 4가지 방향을 실제로 돌려 보고 설계 규칙으로 추천, 모델에 열어 둔 방향은 존중하되 부딪히면 경고. Fable 설계 데이터와 여는 쪽 24/24 일치, Fable 코드의 경첩 반전 버그 발견. 평면도에 궤적을 그려 렌더 |
| "확인 못 한 것(Astra·Tripo·Rodin·네이버/한국어 원문)은 빼고, 블렌더 공식 MCP를 조사" | 공식 서버 소스(서버·애드온·테스트)를 전부 읽고, bpy 5.2.2 안에서 애드온 서버를 띄워 공식 MCP 서버에 MCP 클라이언트로 붙어 도구를 실제 호출. 가이드 4절 전면 개정(도구 26개, 설치 원문, Online Access 필수, SDK 2.x 문제와 v1.0.2 수정, 타임아웃·크기 제한, 약한 샌드박스, HTTP 모드 위험, 렌더 저장 위치), 빠른 시작·보안 절·흔한 실수 갱신. 제외 항목은 5절 끝으로 이동. 기록: `01_research/handson/blender_lab_mcp/` |
| "인체조형·유기물·건물 배치 각자 있나? 평가 좋은 거나 최신 조사. 악성코드·DLL 조심" | 하위 조사 4개(인체, 유기물, 건물, 보안)를 **다운로드·설치·실행 금지** 조건으로 돌리고, 핵심 주장을 GitHub·PyPI·LICENSE·로컬 bpy로 대조. 조사 에이전트의 오류 2건 정정: 텔레메트리 '옵트인' → 실제로는 익명 사용 기록 기본 ON, Infinigen `nature-stable`은 브랜치가 아니라 태그. 가이드 13·14 작성, Blender MCP 가이드 보안 절에 CVE 4건 반영 |
| "네트워크 정책 때문에 안 되는 건 빼고 2번(실제 AI 건물로 검증)만" | `building_audit.py` v2. Realsee×GPT-6 Astra 재구성 공간(v1 오류 18·경고 10 → 오류 0·경고 1), house-3d의 같은 아파트를 Fable·GPT-6가 만든 8개 장면(v1은 방을 하나도 못 알아보고 '오류 0' → 최종 오류 0~1·경고 6~9, 남은 지적은 좌표·렌더·원본 데이터로 확인한 실제 문제). 합친 벽·가져온 GLB 그룹·한중 이름·격자 천장·열린/미닫이 문 처리, `tests/test_building_realworld.py` 추가. 기록: `03_playbooks/scripts/validation/` |

## 4. 주요 결정과 이유

| 결정 | 이유 |
|---|---|
| 원자료(JSON)와 정리 문서를 분리하고, 카탈로그·검증 로그는 스크립트로 생성 | 사용자 지침(원본 보존, 가공 분리). 원자료에서 언제든 재생성 가능 |
| 검증 결과가 조사 결과보다 우선 | 2026년 자료에 AI 생성 SEO 블로그가 많아, 조사 단계 요약만으로는 오류가 섞임 |
| 모델 "순위" 대신 "작업 유형별 선택" | 통제된 비교가 없고 개인 테스트(n=1) 결과가 엇갈림 |
| 문서의 URL은 원자료에 있는 것만 허용하고 스크립트로 강제 | AI 작성 문서의 URL 환각 방지 |
| 보조 스크립트를 직접 만들고 두 Blender 버전에서 테스트 | 조사 결론("숫자 검사 먼저, 렌더 검사 나중")을 바로 쓸 수 있게. 형태·배치 요구사항(R3·R4)의 실행 수단 |
| 스크립트의 치수 규칙을 가구 방향 기준(w/d/z)·단어 단위 매칭으로 개선, 천장·벽 관통 검사 추가 | 치수표 작성 중 발견된 오탐(회전, `armchair`, `door_handle` 등)과 한국 구축 천장(2.3 m) 관통 미검출 문제 |
| 한국 사용자 경고를 문서마다 반복 | Hunyuan3D 라이선스의 한국 제외는 모르고 쓰면 법적 문제가 되고, 여러 사례·도구가 Hunyuan에 의존 |
| 사용자 요청이 "최대한 많이"여서 기본 규모 가이드(에이전트 10개 미만)보다 크게 실행 | 조사 26 + 보완 8 + 작성·검토 23 에이전트 |

## 5. 확인하지 못한 것 (중요도 순)

1. **공식 Blender Lab MCP의 남은 부분**: v1.0.1 변경 내용, v1.0.2·v1.0.3의 전체 변경 내용(특히 HTTP 설정. 2026-08-06 공식 커밋까지는 그대로), 커넥터(v1.0.1)가 SDK 2.x 문제의 영향을 받는지, GUI 모드(스크린샷·UI 이동·지연 응답) 실제 동작. 소스·백그라운드 동작과 후속 확인(v1.0.3 도구 26개, 커넥터 v1.0.1, Windows 설치 실패 원인)은 2026-09-27에 완료([검증 기록](../01_research/handson/blender_lab_mcp/README.md) 4절, `raw/G8_blender_lab_mcp.verify.json`).
2. **UE 5.8 출시일(2026-06-17)**, Unity 공식 MCP 요건·요금, Roblox 내장 MCP 도구 목록(공식 문서 차단).
3. **`BLENDER_MCP_SAFE_MODE=1`(ahujasid)에서 `sys.path` 추가 후 import가 되는지**. 공식 서버에서는 된다는 것을 확인했습니다.
4. 한국어 UI에서 노드 이름이 실제로 번역되는지(일본어 UI 사례로 추정, 설정 `use_translate_new_dataname`의 존재는 확인).
5. 논문 본문 수치 일부(arXiv 차단), 3DCodeBench 0.69→0.97 수치.

**사용자 결정으로 확인 대상에서 제외(2026-09-27)**: "확인 못 한 것은 빼라"는 요청에 따라 아래는 더 쫓지 않습니다. 문서에는 지금처럼 '2차 출처·미확인' 표시를 유지합니다.
- OpenAI 공식 자료로 GPT-6 Astra의 가격·컨텍스트·BenchCAD 수치·공식 3D 기능 확인
- 상용 3D 생성 서비스 약관(Tripo·Rodin 출력물 라이선스, Tencent Cloud Hunyuan API의 한국 이용 조건)
- 네이버·velog 등 한국어 자료 원문 확인과 한국어 검색 보강

## 6. 다음 작업 (우선순위)

1. ~~3~5그룹 문서 전수 검토~~ → **완료**(2026-09-27 재실행).
2. ~~공식 Blender Lab MCP 조사~~ → **완료**(2026-09-27, 소스 정독 + 실제 구동). 남은 것: blender 실행 파일이 있는 환경에서 v1.0.3 태그로 다시 확인(HTTP 설정·스크린샷 수정), GUI 모드에서 스크린샷·UI 이동 도구 확인, 공식 통합 테스트(`tests/test_blender_mcp_with_blender.py`) 실행. 재현 도구는 `01_research/handson/blender_lab_mcp/tools/`.
3. **실제 Blender GUI + MCP로 스크립트 검증**: 공식 서버 백그라운드 모드에서 `building_audit` import 실행은 확인. 남은 것은 ahujasid safe mode에서의 import, GUI에서의 Workbench 검토 렌더.
4. ~~`building_audit.py`를 실제 AI 생성 건물로 검증~~ → **완료**(2026-09-27, 9개 장면). ~~문 여는 방향~~ → **설계 규칙으로 추천·검사 완료**(Fable 설계 데이터와 여는 쪽 24/24 일치). 남은 것: 실제 AI가 만든 **다층 건물·경사 지붕·곡선 벽** 장면 확보 후 재검증, 합친 벽의 벽 단위 두께·틈 검사, 이름 없는 유리문의 여닫이/미닫이 구분. 검증 도구는 `03_playbooks/scripts/validation/tools/`.
5. **가이드 안의 테스트된 코드 블록을 `03_playbooks/scripts/`로 이동 + 테스트 추가**: `check_assembly()`(07 가이드, 부품 연결 맵 검사), `provenance_tools`·`make_ucx`/`make_lods`(10 가이드), 재질 감사·베이크 코드(05 가이드 4.7·7.3절), `review_render()`(06 가이드).
6. ~~Blender 5.2(Python 3.13 bpy)에서 스크립트 테스트~~ → **완료**(5.2.2 LTS, 테스트 3종 통과).
7. **인체 비례·리그 검사 스크립트(`human_audit.py` 가칭)**: 13 가이드 1.4절의 수치 게이트를 `03_playbooks/scripts/`에 스크립트로 만들고 MPFB2 인체로 테스트. 검사 항목은 양팔 폭 ≈ 키, 영향 본 ≤ 4, 무가중치 0, 버텍스/본 ≥ 5, 자기교차.
8. **`building_audit`의 IFC 모드**: Bonsai/IfcOpenShell 모델이면 문–벽 개구부 관계와 IfcSpace로 직접 검사하고, TopologicPy식 도달 그래프를 추가(13 가이드 3.3절).
9. **정기 갱신**: 모델·MCP 서버·라이선스가 매주 바뀌므로, 월 1회 정도 핵심 사실(각 가이드의 "핵심 요약")을 재확인. 공식 Blender MCP는 새 릴리스가 나오면 `handson/blender_lab_mcp/tools/`로 도구 목록부터 다시 뽑아 비교.

## 7. 작업 이력 (커밋 순)

| 단계 | 내용 |
|---|---|
| 1 | 목적 문서, 보조 스크립트 3종 + 테스트 |
| 2 | 13개 주제 원자료 + 검증, 카탈로그 생성기, 조사 방법 문서 |
| 3 | 6개 공백 보완 원자료 + 검증 |
| 4 | 문서 링크 검사기, 요구사항–문서 대응표 |
| 5 | 가이드·플레이북·사례집 초안, 템플릿 |
| 6 | 1·2그룹 교차 검토 반영, 문서 간 불일치 일괄 수정 |
| 7 | `scene_audit.py` 개선(방향 기준 치수, 단어 매칭, 천장·벽 관통) + 관련 문서 정합 |
| 8 | README, 인수인계 문서 |
| 9 | 추가 요청: `building_audit.py`(건축 상식·백룸 위험도), 컴퓨터 유즈 가이드(12), PR 생성 |
| 10 | `building_audit.py` v2: 실제 AI 건물 9개 장면으로 검증·오탐 수정, 실전 패턴 테스트, 검증 기록(`03_playbooks/scripts/validation/`) |
| 11 | 문 여는 방향: 설계 규칙으로 추천(방 안쪽·모서리 경첩·좁은 욕실 바깥·문끼리 충돌 회피·현관 지역 관례), 궤적 검사, `open_door()`·`add_swing_symbols()`, 평면도 렌더(`render_plan.py --swings`) |
| 12 | 공식 Blender Lab MCP 소스 정독·실제 구동 검증(`01_research/handson/blender_lab_mcp/`, 원자료 G8), Blender MCP 가이드 4절·10.5절·빠른 시작 개정, 스크립트 테스트 5.2.2 LTS 통과, 제외 항목 정리 |
| 13 | 공식 MCP 남은 항목 후속 확인(v1.0.3 도구 수, 커넥터 버전, 공식 커밋 2026-08-06까지 비교, Windows 설치 실패 원인), 원자료 `G8_blender_lab_mcp.verify.json` |
| 14 | 배치·조형 보조 도구 색인(`03_playbooks/06_placement_structure_helpers.md`), 다음 세션 시작점 정리 |
| 15 | 인체·유기물·건물 도구와 설치 안전 추가 조사(G9~G12 + 원문 대조), 가이드 13·14, Blender MCP 보안 절 CVE 4건, README·색인·목적 대응표 갱신 |
| 16 | 조형·배치 라이브러리 재확인: BlenderProc(물리 배치) 추가, 색인 06 맨 앞에 'GitHub 라이브러리 바로 찾기' 표(원자료 G13) |
| 17 | MCP·스킬·컴퓨터 유즈용 배치·조형 도우미(원자료 G14): blender-ai-mcp 배치 매크로, dream-loop, blender-asset-mcp, ViSculpt 등. 색인 06 맨 앞에 표. blend-ai → blenderwright 개명과 LICENSE MIT 확인으로 문서 7곳의 AGPL 표기 정정 |

## 8. 이어서 작업하는 법

```bash
git checkout claude/aaa-graphics-ai-modeling-u9zdts
python3 01_research/tools/check_docs.py          # 문서 링크 상태
python3 01_research/tools/build_catalog.py       # 원자료를 추가했다면 카탈로그 재생성
python3 -m venv bpyenv && bpyenv/bin/pip install bpy==5.0.1   # 5.2.2 는 python3.13 venv 필요
bpyenv/bin/python 03_playbooks/scripts/tests/test_scripts.py
bpyenv/bin/python 03_playbooks/scripts/tests/test_building_audit.py
bpyenv/bin/python 03_playbooks/scripts/tests/test_building_realworld.py
```

- 원자료를 고치지 말고 새 파일로 추가하세요(예: `raw/V1_recheck.verify.json`).
- 문서를 고친 뒤에는 반드시 `check_docs.py`를 돌리세요.
