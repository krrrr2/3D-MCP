# 배치·조형 보조 도구 한눈에 보기

> 기준일: 2026-09-27 · 이 문서는 **색인**입니다. 각 도구의 상세 설명·출처·수치는 링크한 가이드에 있습니다.
> 질문: "구조물·조형·가구를 문제없이 배치하게 돕는 스크립트나 보조 도구가 있나? MCP에 들어 있나?"

## 결론 먼저

- **주요 Blender MCP 서버에는 배치 검사 기능이 사실상 없습니다.** 공식 Blender Lab 서버(도구 26개)는 분석·문서·코드 실행 중심입니다. ahujasid MCP for Blender(36개)에도 스냅·충돌·물리 같은 배치 전용 도구가 없습니다. 둘 다 `execute_blender_code`로 직접 구현해야 합니다.
- 배치 검사를 도구로 넣은 곳은 **일부 커뮤니티 MCP**(blend-ai, blender-ai-mcp, glonorce, pakkio, Vibe3DScene, SAGE)와 **CAD 계열 MCP**(build123d-mcp, OpenSCAD MCP)입니다. 규모가 작거나 라이선스·설정 부담이 있습니다.
- 실전에서 쓸 만한 것은 **MCP가 아닌 보조 수단**입니다. 셋 중 하나 이상을 어느 MCP 위에서든 `execute_blender_code`나 헤드리스로 돌리면 됩니다.
  - 좌표를 대신 푸는 **솔버**
  - 붙이고 검사하는 **스크립트**
  - 규칙을 강제하는 **스킬**
- 가장 빨리 쓸 수 있는 것은 **이 저장소의 스크립트**입니다. Blender 4.2.23 LTS·5.0.1·5.2.2 LTS에서 테스트를 통과했고, 공식 MCP에서 import 실행도 확인했습니다.

## GitHub 라이브러리 바로 찾기

"조형·배치가 잘 되게 해 주는 라이브러리"로 자주 떠올리는 것들입니다. 2026-10-02에 GitHub 원 저장소의 마지막 커밋과 LICENSE를 다시 확인했습니다. 설치·실행은 하지 않았습니다.

| 라이브러리 | 하는 일 | 라이선스 | 상태 | 주의 |
|---|---|---|---|---|
| [BlenderProc](https://github.com/DLR-RM/BlenderProc) (DLR) | **물체 배치**: 표면 위 포즈 샘플링(`sample_poses_on_surface`), 충돌 검사, 물리로 떨어뜨려 안착(`simulate_physics_and_fix_final_poses`) | GPL-3.0 | v2.8.0(2024-10), 커밋 2026-01 | 자체 Blender 4.2.1을 공식 서버에서 받아 **별도 프로세스**로 실행. 작업 중인 Blender 5.x 안에서 import하는 방식이 아님 |
| [Infinigen](https://github.com/princeton-vl/infinigen) (Princeton) | **조형 + 배치**: 나무·바위·생물·지형 생성기, 실내 가구 제약 배치(Infinigen Indoors) | BSD-3 | 커밋 2026-08 | 자연 에셋은 `nature-stable` 태그(구 bpy) → 별도 환경에서 뽑아 가져오기 |
| [fogleman/sdf](https://github.com/fogleman/sdf) | **유기 조형**: 파이썬 코드로 SDF를 조합(smooth union) → 메시 | MIT | 커밋 2024-08(정체) | Blender 5.x에서는 내장 SDF 노드로 같은 일을 할 수 있음 |
| [Sverchok](https://github.com/nortikin/sverchok) | **파라메트릭 조형**: 600개 이상 노드(격자, 파빌리온, 트위스트) | GPL-3.0 | 커밋 2026-09 | 큰 노드 그래프는 에이전트가 틀리기 쉬움 |
| [Kubric](https://github.com/google-research/kubric) (Google) | 물리(PyBullet) 기반 다물체 배치 장면 생성 | Apache-2.0 | 커밋 2026-05 | Blender 2.93 고정 → 아이디어 참고용 |
| Holodeck · LayoutVLM · SceneSmith · HSM | 관계 제약 → 솔버로 가구 좌표 | 각자 다름 | — | [08 배치 가이드 3.1절](../02_guides/08_scene_layout_placement.md) |

- **지금 Blender 5.x 작업에 바로 쓰기 좋은 것**:
  - 이 저장소 스크립트(아래 1절)
  - 08 가이드의 물리 안착 코드(4.7절). BlenderProc의 "표면 샘플링 → 물리 안착 → 포즈 고정"과 같은 원리를 bpy로 구현한 것입니다.
  - Blender 5.x 내장 SDF 노드
- 원자료: [`G13_placement_libraries.gap.json`](../01_research/raw/G13_placement_libraries.gap.json)

## 1. 이 저장소에 이미 있는 것 (바로 사용)

| 필요 | 도구 | 하는 일 | 위치 |
|---|---|---|---|
| 붙여서 놓기 | `placement_utils.py` | 바닥 붙이기, 아래 표면 위에 올리기(책상 위 소품), 옆·벽에 붙이기, 특정 지점 바라보기, 평면 간격 측정·규칙 검사 | [scripts/README.md](scripts/README.md) "배치 함수 예시" |
| 물리 오류 검사 | `scene_audit.py` | 떠 있음, 바닥 아래로 박힘, 다른 물체 속으로 파고듦, 천장 뚫림, 가구끼리·가구–벽 관통, 스케일 미적용, 치수 범위 이탈(가구 방향 기준) → JSON | [scripts/README.md](scripts/README.md) |
| 건축 상식 검사 | `building_audit.py` | 문(안 뚫림·뜸·열면 벽·막힘), **문 여는 방향 추천과 궤적 검사**, 창, 방 연결·동선, 벽 틈, 계단, 벽 보고 앉는 의자, 백룸 위험도 | [scripts/README.md](scripts/README.md) "건축 상식 검사", [실제 AI 건물 검증 기록](scripts/validation/README.md) |
| 눈으로 확인 | `review_views.py` | 위·정면·측면·3/4 검토 렌더(오브젝트마다 다른 색) | [scripts/README.md](scripts/README.md) |
| 가구 한 개 조립 검사 | `check_assembly()` (가이드 코드) | 부품 연결 맵 기준 틈(GAP), 과도한 겹침, 계획에 없는 관통, 바닥과 이어지지 않은 부품 | [07 모델링 가이드 2.4절](../02_guides/07_modeling_objects_furniture_sculpture.md) |
| 관계 → 좌표 | `grid_solver.py` (가이드 코드) | "벽에 붙여, 소파를 바라보게" 같은 관계 제약 JSON을 격자 DFS로 풀어 (x, y, yaw) 산출. 순수 Python | [08 배치 가이드 4.4절](../02_guides/08_scene_layout_placement.md) |
| 소품 자연 안착 | rigid body 안착 코드 (가이드 코드) | 소품을 살짝 띄우고 물리로 떨어뜨려 받침면에 안착 | [08 배치 가이드 4.7절](../02_guides/08_scene_layout_placement.md) |
| 에셋 정규화 | 정규화 코드 (가이드 코드) | 가져온 에셋의 실측 높이·원점(바닥 중앙)·정면(-Y)·트랜스폼 적용. 배치 품질의 절반 | [08 배치 가이드 4.1절](../02_guides/08_scene_layout_placement.md), [04 AI 3D 생성 가이드](../02_guides/04_ai_3d_generation.md) |
| 야외 산포 | 밀도 페인트 + 산포 코드 (가이드 코드) | 길·건물 주변을 비우고 최소 간격을 지키며 나무·바위 배치 | [08 배치 가이드 7.3절](../02_guides/08_scene_layout_placement.md) |

- 스크립트 4종은 테스트 스위트가 있습니다. "가이드 코드"는 작성 때 4.2.23 LTS·5.0.1에서 실행해 확인했지만 테스트 스위트에는 없습니다(인수인계 문서 6절 5번: 스크립트로 옮기기).
- 권장 순서는 이렇습니다.
  1. 정규화
  2. 관계 제약 → 솔버로 좌표
  3. `placement_utils`로 붙이기
  4. `scene_audit` + `building_audit`로 숫자 검사
  5. `review_views`로 눈 검사
  6. 한 번에 하나씩 고치기

  자세한 이유는 [08 배치 가이드 2절](../02_guides/08_scene_layout_placement.md)의 4단계 루프를 보세요.

## 2. MCP 안에 배치·조형 검사가 들어 있는 것

| 도구 | 들어 있는 기능 | 주의 | 상세 |
|---|---|---|---|
| 공식 Blender Lab 서버 | **없음**(분석·문서·코드 실행) | 이 저장소 스크립트를 import해서 쓰면 됨(확인) | [02 Blender MCP 가이드 4절](../02_guides/02_blender_mcp.md) |
| ahujasid MCP for Blender | **없음**(에셋·생성 중심) | `execute_blender_code`로 직접 구현 | [08 배치 가이드 3.2절](../02_guides/08_scene_layout_placement.md) |
| blend-ai | 스냅(Transforms), 원점, rigid body·bake, OpenGL 렌더 피드백 | AGPL-3.0 | 같은 곳 |
| Vibe3DScene | 자체 MCP + 에이전트, VLM 시각 검사 위에 관통 검사 옵션(기본 임계 2 cm) | 설정 요소 많음(Redis 등) | 같은 곳 |
| blender-ai-mcp | 결정적 측정·assertion(배치·공간 관계 검증) | 설정 복잡, 2026-05 이후 커밋 없음 | [02 Blender MCP 가이드 5.1절](../02_guides/02_blender_mcp.md) |
| glonorce/Blender_mcp | BVH 면 간 거리·관통 검사, 0~100 무결성 점수 | 소규모 | 같은 곳 |
| pakkio/mcp-blender | `capture_multiview_audit`(4뷰, 가림 진단, bbox 지표) | 소규모, 라이선스 미확인 | 같은 곳 |
| SAGE (NVlabs) | FastMCP 서버 + 제약 DFS 배치 솔버 + 물리 critic | USD/Isaac 중심, 무거움 | [08 배치 가이드 3.1절](../02_guides/08_scene_layout_placement.md) |
| build123d-mcp | measure / compare(끼워맞춤·간섭) / validate. 조인트로 조립 위치 계산 | 정밀 부품용(CAD). Blender로는 가져와 마감 | [07 모델링 가이드 3.2·3.3절](../02_guides/07_modeling_objects_furniture_sculpture.md) |
| OpenSCAD MCP (+BOSL2) | 앵커 배치(`attach`)로 접촉이 구조적으로 보장, 일부 서버는 조립 간섭 검사 | 메시 품질·UV 없음 | 같은 곳 |
| Pascal Editor | 건축 에디터 + MCP, `furniture-fit` 스킬(가구 풋프린트 판정) | 웹 에디터라 렌더 품질은 별도 | [03 기타 MCP 가이드](../02_guides/03_other_mcp_dcc_cad_engines.md) |

DCC·엔진 쪽에도 비슷한 검사가 있습니다. 3ds Max 접촉 검사, RhinoMCP 측정, Fusion 간섭 검사, Unity 격리 스크린샷 등은 [03 기타 MCP 가이드](../02_guides/03_other_mcp_dcc_cad_engines.md) 핵심 요약을 보세요.

## 3. MCP가 아닌 보조 수단

| 종류 | 대표 | 핵심 아이디어 | 상세 |
|---|---|---|---|
| 제약 솔버 | Holodeck(DFS), LayoutVLM(미분 가능 최적화), Infinigen Indoors(제약 언어 + annealing, Blender 네이티브), SAGE | LLM은 관계만 쓰고 좌표는 솔버가 풂. 한 비교에서 충돌률이 LLM 직접 좌표 40.8% → 제약+솔버 12.7% | [08 배치 가이드 1·3.1절](../02_guides/08_scene_layout_placement.md) |
| 렌더 → 평가 → 수정 루프 | SceneReVis, SceneSmith(물리·방향·도달 가능성 검사), VIGA | 2뷰 이상 렌더 + 루브릭 + 원자 연산. 충돌률 4.5%까지 낮춘 보고 | 같은 곳 |
| 반복 패턴 함수 | HSM/SMC | 식탁 세팅·책장·욕실 소품을 `place_row`·`place_stack`·`place_grid` 같은 함수로 | 같은 곳 |
| 조립 스킬 | ProfRino Assembly Skill, cc-blender-skill | 코드 전에 연결 맵, 결합부 겹침 5~15 mm만 허용, QA 게이트 | [07 모델링 가이드 6절](../02_guides/07_modeling_objects_furniture_sculpture.md), [02 Blender MCP 가이드 8절](../02_guides/02_blender_mcp.md) |
| 조형 방법 | SDF smooth union, 메타볼, Mesh to Volume → voxel remesh → Multires/Displace | 버텍스를 직접 만지지 않아 깨짐이 적음 | [07 모델링 가이드 7절](../02_guides/07_modeling_objects_furniture_sculpture.md) |
| 평가 지표 | SceneEval | 충돌·통행·경계 이탈·열림부 여유는 스크립트로, 관계·지지·접근성은 VLM으로. 에이전트 셀프 체크리스트로 사용 | [08 배치 가이드 3.4절](../02_guides/08_scene_layout_placement.md) |
| 치수 기준 | 실측 치수표 | 가구·통로·천장고 mm 값(한국 프리셋 포함) | [실측 치수표](05_reference_dimensions.md), [08 배치 가이드 6절](../02_guides/08_scene_layout_placement.md) |

## 4. 상황별 추천

| 상황 | 추천 조합 |
|---|---|
| 방 하나에 가구 배치 | 관계 제약 JSON → `grid_solver` → `placement_utils` → `scene_audit` → `review_views` |
| 건물·평면(문·창·방) | 위 + `building_audit`(문 여는 방향 포함). 평면 초안은 Pascal Editor도 가능 |
| 가구 한 개를 부품으로 조립 | 부품 스펙 JSON + 연결 맵 → 조립 헬퍼 → `check_assembly()` → `scene_audit` |
| 조인트·하드웨어처럼 mm 정밀 | build123d(-mcp)로 부품·조립 → Blender로 가져와 마감 |
| 조형물·유기 형상 | SDF·볼륨 방식으로 형태 → remesh → 받침대 접촉만 `scene_audit`로 확인 |
| 소품 흩뿌리기 | 받침면 위에 띄우고 rigid body 안착 → `scene_audit` |
| 야외 | 밀도 페인트 + 최소 간격 산포(08 가이드 7절) |

## 5. 분야별 전용 도구 (인체·유기물·건물)

상세 설명, 라이선스, 안전 신호는 [인체·유기물·건물 도구 가이드](../02_guides/13_humans_organic_buildings.md)에 있습니다. 설치 전에는 [설치 안전 가이드](../02_guides/14_tool_install_safety.md)의 점검표를 보세요.

| 분야 | 형태는 이것으로 | 검사는 이것으로 | MCP로 붙는 것 |
|---|---|---|---|
| **인체·캐릭터** | MPFB2(무료, bpy 스크립트), Anny·MHR(Apache-2.0). 사진이면 SAM 3D Body. SMPL-X는 비상업 | 양팔 폭 ≈ 키, 리그 규칙(영향 본 ≤ 4, 무가중치 0, 버텍스/본 ≥ 5), 5포즈 변형·자기교차 검사 | Meshy·Tripo 공식 MCP(생성·리깅). MPFB2·Anny 전용 MCP는 아직 없음 → `execute_blender_code`로 호출 |
| **유기물·자연** | 나무 생성기(Sapling·Modular Tree·The Grove), **Blender 5.x 내장 SDF 노드**, Infinigen 자연 팩토리(별도 환경) | 표면 분포 + 레이캐스트 접촉 검사, 최소 간격 | 전용 MCP 드묾. 접촉 단언 도구(blender-ai-mcp) 조합 |
| **건물·평면** | 평면 JSON(방 그래프 + 면적) → 검사 → Bonsai(IFC)·Home Builder 5로 3D화, 또는 도면 입력 | `building_audit.py`, IfcOpenShell ifctester(IDS)·ifcclash, TopologicPy 도달 그래프, JuPedSim 피난 | **IfcOpenShell 공식 MCP**(`ifcopenshell-mcp`), MCP4IFC·Bonsai_mcp, RhinoAI(공식), Revit 2027 공식(읽기 전용, 검사용) |
| **도시·단지** | OSM 윤곽 + DEM 지형(blosm, BlenderGIS) | 윤곽 꼭짓점 아래 지형 레이캐스트 → 기단 높이 | — |

## 관련 문서

- [13 인체·유기물·건물 도구](../02_guides/13_humans_organic_buildings.md) · [14 설치 안전](../02_guides/14_tool_install_safety.md) · [08 배치·레이아웃 가이드](../02_guides/08_scene_layout_placement.md) · [07 오브젝트·가구·조형 모델링](../02_guides/07_modeling_objects_furniture_sculpture.md) · [02 Blender MCP](../02_guides/02_blender_mcp.md) · [03 기타 MCP](../02_guides/03_other_mcp_dcc_cad_engines.md)
- [보조 스크립트 사용법](scripts/README.md) · [품질 체크리스트](04_quality_checklists.md) · [인수인계](../05_handoff/status_and_next_steps.md)
