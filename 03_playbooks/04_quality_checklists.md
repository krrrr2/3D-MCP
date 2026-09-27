# 품질 체크리스트: 모델링·재질·조명·배치·익스포트·라이선스·운영

> 기준일: 2026-09-27 · 단계마다 복사해서 쓰는 체크박스 목록입니다. 항목마다 확인 방법(눈·수치·스크립트)과 기준값을 달았고, [`scene_audit.py`](scripts/README.md)가 자동으로 잡는 항목은 `[A]`로 표시했습니다.

## 핵심 요약

- **숫자 먼저, 눈은 그다음입니다.** 결정적 검사(`scene_audit.py`, 이 문서의 `quick_checks()`, 재질 감사, glTF 검증)를 먼저 통과시키고, 그다음 4방향 렌더와 최종 렌더를 보고 비평합니다. 반대로 **숫자가 모두 통과해도 이미지가 틀리면 실패**입니다. 여러 스킬 저자가 같은 경고를 남겼습니다.
- **30초 빠른 점검은 1절**에 있습니다. "AI 결과가 싸 보이는 12가지"(Standard 뷰 변환, 기본 50 mm 카메라, 광원 크기 0, 정면광, 칼날 모서리, 균일한 roughness, 타일링, 등간격 배치, 스케일 오류, 과한 후처리, 구워진 조명, 생활감 부재)만 확인해도 CG 티의 대부분이 걸러집니다.
- **`scene_audit.py`가 자동으로 잡는 것**: 떠 있음, 바닥 아래로 박힘, 다른 물체 속으로 파고듦(`sunk_into`), 유닛 간 관통, 가구–벽·천장 메시 관통, `ceiling_z`를 주면 천장 위로 뚫림, 스케일 미적용·음수 스케일, non-manifold 엣지, 재질·UV 없음, 이름 기준 치수 범위 이탈(가구 방향 기준 폭·깊이·높이). `collection=`을 주면 그 컬렉션만 검사합니다.
- **`scene_audit.py`가 못 잡는 것**: 벽 메시 없이 바닥만 있을 때 방 경계 밖으로 나감(0.5절 코드로 보완), 완전히 들어간 물체, 한 유닛 안의 부품끼리 관통, 뒤집힌 노멀, 의도한 벽걸이 구분, 문·창·방 연결 같은 건축 상식(`building_audit.py`로 검사). 빈칸은 이 문서 0절의 보조 코드와 다른 가이드의 테스트된 코드로 메웁니다(0.4·0.5절 코드는 pip `bpy` **5.0.1**과 **4.2.23 LTS**에서 실행 확인).
- **기준값 대부분은 오픈소스 코드·에이전트 스킬에 들어 있는 값입니다.** 업계 표준이 아니라 출발점이므로, 레퍼런스 사진과 비교해 조정하세요. 출처끼리 충돌하는 값은 [실측 치수표](05_reference_dimensions.md)와 [라이팅 가이드](../02_guides/06_lighting_rendering_art_direction.md) 8절의 권장 기본값을 따릅니다.
- **[KR] 한국 사용자가 먼저 볼 것**: ① Tencent Hunyuan3D 계열(2.0·2.1·Omni·Part, BPT 등) 오픈웨이트 라이선스는 적용 지역에서 대한민국을 빼고 **출력물 사용도 제한**합니다. ② 한국어 UI에서는 새 노드 이름이 번역될 수 있으니 코드에서 노드를 `type`으로 찾습니다. ③ 치수는 한국 프리셋(구축 아파트 천장 2300 mm, 싱크대 850 mm, 방문 문틀 900×2100 mm)을 씁니다. ④ 인공지능기본법 제31조(2026-01-22 시행) 표시 의무 적용 여부를 검토합니다.
- **에이전트 운영의 함정**: Claude Code `/rewind`는 MCP로 바꾼 Blender 씬을 되돌리지 못하므로 `.blend` 증분 저장이 필수입니다. `BLENDER_MCP_SAFE_MODE=1`은 샌드박스가 아니고, 텔레메트리는 익명 사용 기록이 기본으로 켜져 있습니다(`DISABLE_TELEMETRY=true`로 끔). MCP 기본 스크린샷(긴 변 1000px)은 약 756토큰입니다.
- **한계**: 독립적으로 검증된 'AAA급' AI+MCP 결과물은 찾지 못했습니다. 이 체크리스트는 CG 티를 없애는 **하한선**이고, 최종 판정은 레퍼런스 비교와 사람 리뷰 게이트에서 내립니다.

---

## 0. 쓰는 법

### 0.1 표기

| 표기 | 뜻 |
|---|---|
| `[필수]` | 어기면 다음 단계로 넘어가지 않는 하드 게이트 |
| `[눈]` | 렌더·스크린샷을 보고 판단 |
| `[수치]` | 속성값이나 측정값을 출력해 판단(bpy 한두 줄) |
| `[스크립트]` | 이 저장소나 다른 가이드의 **테스트된** 코드로 판단(함수 이름 명시) |
| `[A]` | [`scene_audit.py`](scripts/README.md)가 자동으로 잡음. 괄호 안은 리포트의 issue 이름 |
| `[KR]` | 한국 사용자에게 특히 중요 |
| [스킬] | 에이전트 스킬 저자가 정한 값. 원문과 일치하는지는 검증했지만 업계 표준은 아님 |
| (미검증 주장) | 검증에서 신뢰도 낮은 출처로 분류된 자료의 값. 출발점으로만 사용 |
| (신뢰도 낮음) / (미확인) | 1차 출처를 확인하지 못함 / 확인 불가 |

체크박스는 그대로 복사해 이슈, PR 설명, `PROGRESS.md`, 에이전트 보고서에 붙여 쓰세요. 에이전트에게는 "각 항목에 `통과 / 실패(근거) / 해당 없음`으로 답하라"고 시키면 됩니다.

### 0.2 자동 점검 도구 한눈에

| 도구 | 잡는 것 | 위치 | 테스트 |
|---|---|---|---|
| `scene_audit.audit_scene()` | 떠 있음·바닥 관통·박힘(`sunk_into`)·유닛 간 관통·가구–벽/천장 관통·천장 돌출(`ceiling_z`)·스케일·non-manifold·재질/UV 없음·치수 범위 | [scripts/README](scripts/README.md) | Blender 4.2.23 LTS·5.0.1 |
| `building_audit.audit_building()` | 문(벽에 안 뚫림·뜸·열면 벽·허공)·창(창턱 높이·실내 창)·방(밀폐·갈 수 없음·창 없는 생활 공간·복도형)·벽 틈·계단 + 백룸 위험도 | [scripts/README](scripts/README.md) | 같음 |
| `placement_utils.check_clearances()` | 두 유닛 사이 평면(XY) 간격이 최소·최대 범위 안인지 | [scripts/README](scripts/README.md) | 같음 |
| `review_views.render_review_views()` | 위 정사영·정면·측면·3/4 원근 4장(오브젝트별 색) | [scripts/README](scripts/README.md) | 같음 |
| `quick_checks()` | 뷰 변환·카메라·광원 크기·켈빈 틴트·metallic 중간값·고정 roughness·유리 바운스·EEVEE 레이트레이싱·이름 규칙 | 이 문서 0.4절 | 5.0.1·4.2.23 LTS |
| 방 경계 검사 | 벽 메시 없이 숫자로만 정한 방 경계 밖으로 나감(scene_audit는 벽 메시가 있어야 잡음) | 이 문서 0.5절 | 5.0.1·4.2.23 LTS |
| `check_assembly()` | 한 가구 안의 부품 틈(GAP)·과한 겹침(TOO_DEEP)·계획에 없는 관통·떨어진 부품 | [모델링 가이드](../02_guides/07_modeling_objects_furniture_sculpture.md) 2.4절 | 4.2.23 LTS·5.0.1 |
| `pbr_audit.audit_materials()` | metallic 중간값, roughness 0, 어두운 금속, albedo 범위, 데이터 맵 sRGB, 중복 Output | [텍스처링 가이드](../02_guides/05_texturing_materials.md) 4.7절 | 4.2 LTS·5.0 |
| `review_render()` | 렌더 1회로 PNG·EXR·False Color·`clip_pct`·`value_range` 등 | [라이팅 가이드](../02_guides/06_lighting_rendering_art_direction.md) 2.3절 | 5.0.1·4.2.23 LTS |
| `glb_material_report` | 만든 맵이 GLB 슬롯에 실제로 들어갔는지 | [텍스처링 가이드](../02_guides/05_texturing_materials.md) 8.2절 | 같음 |
| `npx @gltf-transform/cli@4.5.0 validate out.glb` | glTF 스펙 오류(종료 코드 1) | [에셋·파이프라인 가이드](../02_guides/10_assets_pipeline_licensing.md) 2.6절 | 같은 가이드에서 테스트 |

### 0.3 `scene_audit.py` 자동 항목 대응표 (`[A]`)

기본 허용 오차는 5 mm(`tol=0.005`)입니다. 부모가 없는 최상위 오브젝트를 하나의 "유닛"으로 묶어 판정하므로, 의자 부품은 한 부모(Empty 등) 아래에 두세요. 이름의 **마지막 핵심 단어**가 `floor`·`ground`·`wall`·`ceiling`·`terrain`인 유닛(`Floor`, `Wall_N`, `north_wall`)은 구조물로 보고 떠 있음·치수 검사에서 빼며, 받침면으로만 씁니다. 구조물끼리의 관통은 검사하지 않지만 가구–구조물 관통은 잡습니다. `floor_lamp`·`wall_shelf`는 가구로 인식하니, 가구 이름을 `..._wall`로 끝내지 마세요.

| issue | 뜻 | 합격 기준 | 주의 |
|---|---|---|---|
| `floating_or_wall_mounted` | 바닥면 근처 5개 지점에서 아래로 쏜 레이에 받침면이 없음 | 0건. 벽걸이·천장등·액자는 의도한 것인지 목록으로 확인 | 벽 쪽은 벽과의 거리로 따로 검증 |
| `below_floor:<d>m` | 유닛 최저점이 바닥보다 5 mm 넘게 아래 | 0건 | `floor_z`를 넘겨야 동작 |
| `sunk_into:<상대>=<d>m` | 받침면(바닥 슬래브·다른 가구) 속으로 파고듦. 예전에는 '떠 있음'으로 오탐하던 경우 | 0건 | 계단이 슬래브에, 다리가 바닥에 박힌 경우. `snap_to_floor`·`drop_to_surface`로 다시 올림 |
| `above_ceiling:<d>m` | 유닛 꼭대기가 `ceiling_z`보다 5 mm 넘게 위 | 0건 | `ceiling_z`를 넘겨야 동작. 방과 건물 외관이 한 장면이면 `collection=`으로 방만 검사 |
| `interpenetrations[]` | 바운딩박스가 5 mm 넘게 겹치는 쌍 중 실제 면이 교차하는 쌍(가구–벽·천장 포함, 구조물끼리는 제외) | 0쌍 | 한 물체가 다른 물체 안에 **완전히** 들어간 경우는 못 잡음 → `bbox_overlap_depth_m`로 보조 판단. 테이블 밑 의자처럼 bbox만 겹치면 오탐하지 않음 |
| `unapplied_scale:<name>` | scale ≠ 1(허용 1e-4) | 0건 | bevel·solidify 폭 왜곡, 익스포트 스케일 오류의 원인 |
| `negative_scale:<name>` | 음수 스케일(미러링 흔적) | 0건 | 적용 후 노멀 재계산 |
| `non_manifold_edges:<name>=n` | 열린 경계·겹친 면 | 콜리전·boolean·3D 프린트·조형물 제작용이면 0. 렌더 전용이면 눈에 띄는 구멍만 없으면 됨 | 모디파이어 적용 **전** 원본 메시 기준 |
| `no_material:<name>` / `no_uv:<name>` | 재질 슬롯이 비었거나 UV 레이어 없음 | 최종 단계에서 0건 | 바닥·벽에도 적용됨 |
| `size_out_of_range:<key>.<axis>=…` | 이름 키워드(`chair`, `sofa`, `door` …) 기준 전체 치수 범위 이탈. 축은 가구 방향 기준 `w`(수평 긴 변)·`d`(수평 짧은 변)·`z`(높이) | 0건 | 이름은 영어 단어 단위로 맞춤(CamelCase `CoffeeTable`도 `coffee_table`로 인식, 한국어 이름은 인식 안 함). `armchair`·`counter_stool`은 자체 규칙이 있고, 90°·30° 돌린 가구도 오탐하지 않음. `table_lamp`·`door_handle`처럼 부속품 단어가 뒤에 붙으면 규칙 미적용. 한국 장면은 [치수표](05_reference_dimensions.md) 11절 `KR_SIZE_RULES` |

### 0.4 보조 점검 코드 `quick_checks()` (테스트 완료)

`scene_audit.py`가 보지 않는 렌더·재질·카메라·조명·이름 항목을 점검합니다. `quick_checks.py`로 저장해 쓰거나, MCP의 `execute_blender_code`에 통째로 붙여 넣으면 끝에서 자동 실행해 결과를 출력합니다. pip `bpy` 5.0.1과 4.2.23 LTS에서 일부러 만든 나쁜 장면(Standard 뷰, 기본 50 mm, 반경 0 라이트, 크기 0 Area, 켈빈 + 비흰색 틴트, metallic 0.7, transmission 바운스 12, 이름 `Chair.001`·`소파`·`CoffeeTable`)을 모두 잡았고, 고친 장면에서는 고정 roughness 경고만 남았습니다. 4.2에는 라이트 `use_temperature`가 없어 틴트 검사는 5.x에서만 돕니다.

```python
import bpy, json, math, re

def quick_checks(scene=None):
    """scene_audit.py가 보지 않는 색관리·카메라·조명·재질·이름 항목을 점검한다.
    반환: [{"check", "value", "ok", "note"}] (ok: True 통과 / False 확인 필요 / None 참고값)"""
    sc = scene or bpy.context.scene
    bpy.context.view_layer.update()  # 위치를 바꾼 직후엔 matrix_world가 갱신되지 않음
    out = []
    add = lambda k, v, ok, note="": out.append({"check": k, "value": v, "ok": ok, "note": note})
    add("blender_version", bpy.app.version_string, None)

    vs = sc.view_settings
    add("view_transform", vs.view_transform, vs.view_transform != "Standard", "Standard 금지. AgX / Khronos PBR Neutral / ACES")
    add("exposure", round(vs.exposure, 2), None, "밝기는 램프가 아니라 exposure로")
    eng = sc.render.engine
    add("render_engine", eng, None)
    if eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
        rt = getattr(sc.eevee, "use_raytracing", None)
        add("eevee_raytracing", rt, rt is not False, "파이널은 켬(팩토리 기본은 꺼짐)")

    cam = sc.camera
    if cam is None:
        add("camera", None, False, "렌더 전 카메라 필요")
    else:
        d = cam.data
        add("camera_lens_mm", round(d.lens, 1), d.type != "PERSP" or abs(d.lens - 50.0) > 0.01, "기본 50 mm 그대로면 의도 확인")
        add("camera_height_m", round(cam.matrix_world.translation.z, 2), None, "사람 시점 약 1.6 m")
        add("camera_dof", d.dof.use_dof, None, "포토리얼 스틸은 보통 켬")

    glassy = False
    for mat in bpy.data.materials:
        if mat.users == 0 or mat.node_tree is None:
            continue
        nodes = mat.node_tree.nodes
        n_out = sum(1 for n in nodes if n.type == "OUTPUT_MATERIAL")
        if n_out != 1:
            add(f"mat:{mat.name}:outputs", n_out, False, "Material Output은 1개")
        for b in (n for n in nodes if n.type == "BSDF_PRINCIPLED"):
            m, r = b.inputs["Metallic"], b.inputs["Roughness"]
            if not m.is_linked and 0.05 < m.default_value < 0.95:
                add(f"mat:{mat.name}:metallic", round(m.default_value, 3), False, "0 또는 1만")
            if not r.is_linked:
                add(f"mat:{mat.name}:roughness_const", round(r.default_value, 3), False, "단일값 → 맵·노이즈로 변화")
            t = next((s for s in b.inputs if s.name == "Transmission Weight"), None)
            if t is not None and (t.is_linked or t.default_value > 0.5):
                glassy = True
    if eng == "CYCLES" and glassy:
        tb = sc.cycles.transmission_bounces
        add("cycles_transmission_bounces", tb, tb >= 16, "유리 많은 장면은 16 이상")

    for ob in sc.objects:
        if ob.type == "LIGHT":
            L = ob.data
            if L.type == "SUN":
                a = math.degrees(L.angle)
                add(f"light:{ob.name}:sun_angle_deg", round(a, 3), a >= 0.5, "실제 태양 약 0.53°, 부드럽게 2~5°")
            elif L.type == "AREA":
                add(f"light:{ob.name}:size_m", round(L.size, 3), L.size > 0, "0 금지")
            else:
                add(f"light:{ob.name}:radius_m", round(L.shadow_soft_size, 3), L.shadow_soft_size > 0, "0이면 칼 같은 그림자")
            if getattr(L, "use_temperature", False):
                white = all(abs(c - 1.0) < 1e-3 for c in L.color)
                add(f"light:{ob.name}:tint", [round(c, 3) for c in L.color], white, "켈빈 사용 시 color는 곱해지는 틴트 → 흰색")
        name = ob.name
        if re.search(r"\.\d{3}$", name):
            add(f"name:{name}", "suffix", False, ".001 접미사 = 복제 흔적, 이름 규칙 위반")
        elif not name.isascii():
            add(f"name:{name}", "non-ascii", False, "영어 snake_case 권장(치수 규칙·엔진 호환)")
        elif ob.parent is None and ob.type in ("MESH", "EMPTY") and re.search(r"[a-z][A-Z]", name) and "_" not in name:
            add(f"name:{name}", "CamelCase", False, "이름 규칙은 영어 snake_case(scene_audit는 CamelCase도 인식)")
    return out

if __name__ != "quick_checks":
    res = quick_checks()
    print(json.dumps({"fail": [r for r in res if r["ok"] is False], "info": [r for r in res if r["ok"] is None]},
                     ensure_ascii=False, indent=1))
```

- `ok: False`는 "확인 필요"입니다. `roughness_const`는 거의 모든 초기 재질에서 뜨는 경고라서 히어로·근경 재질만 고치면 됩니다.
- 이 테스트에서 `bpy.data.lights.new()`로 만든 Point 라이트의 반경 기본값이 **0**, Sun 각도 기본값이 **0.526°**, 팩토리 설정의 EEVEE 레이트레이싱이 **꺼짐**인 것을 두 버전에서 모두 확인했습니다. 광원 크기 0은 에이전트가 만든 장면에서 기본으로 생기는 결함입니다.

### 0.5 방 경계 검사: 벽 메시가 없을 때 (테스트 완료)

> **업데이트(2026-09-27)**: 이 절을 쓸 때의 `scene_audit.py`는 벽·천장을 관통 검사에서 빼서 벽 속 소파·천장을 뚫은 옷장을 놓쳤습니다. 지금은 스크립트를 고쳐 **벽·천장 메시가 있으면 가구–구조물 관통을 잡고, `audit_scene(ceiling_z=2.30)`으로 천장 위 돌출도 잡습니다**(테스트 통과). 아래 코드는 벽 메시 없이 바닥만 만든 블록아웃 단계처럼 **방 경계를 숫자로만 정한 경우**의 보조 검사로 쓰세요. SceneEval의 "Out of Bounds" 지표와 같은 검사입니다. 구조물 판정은 `scene_audit`과 같은 규칙(이름의 마지막 핵심 단어)을 써서, 방 밖으로 나간 `floor_lamp`·`wall_shelf`를 구조물로 착각해 건너뛰지 않습니다(4.2.23 LTS·5.0.1에서 확인).

```python
# rep = scene_audit.audit_scene(floor_z=0.0) 다음에 실행
room = dict(xmin=0.0, xmax=4.0, ymin=0.0, ymax=3.2, ceiling=2.3)   # 방 안쪽 치수(m). KR 구축 천장 2.3
tol = 0.005
STRUCT = ("floor", "ground", "wall", "ceiling", "terrain")          # scene_audit 기본 구조물 단어
for u in rep["units"]:
    if scene_audit.is_structure(u["name"], STRUCT):                  # 'Floor'·'Wall_N'만 건너뜀. 'floor_lamp'는 검사
        continue
    (x0, y0, z0), (x1, y1, z1) = u["bbox_min"], u["bbox_max"]
    if (x0 < room["xmin"] - tol or x1 > room["xmax"] + tol or y0 < room["ymin"] - tol
            or y1 > room["ymax"] + tol or z1 > room["ceiling"] + tol):
        print("OUT_OF_ROOM", u["name"], u["bbox_min"], u["bbox_max"])
```

직사각형 방 기준입니다. L자 방은 방을 직사각형 여러 개로 나눠 각각 검사하세요.

### 0.6 한 번에 돌리기

**MCP(실행 중인 Blender)에서**

```python
import sys, importlib
sys.path.append(r"C:\path\to\3D-MCP\03_playbooks\scripts")   # scene_audit.py 위치
sys.path.append(r"C:\path\to\my_checks")                      # quick_checks.py(0.4절)를 저장한 위치
import scene_audit, quick_checks
importlib.reload(scene_audit); importlib.reload(quick_checks)
rep = scene_audit.audit_scene(floor_z=0.0, ceiling_z=2.30)   # 한국 구축 천장. 한국 장면이면 size_rules=KR_SIZE_RULES(치수표 11절)
print(rep["summary"])
print([(u["name"], u["issues"]) for u in rep["units"] if u["issues"]])
print(rep["interpenetrations"])
print([r for r in quick_checks.quick_checks() if r["ok"] is False])
```

- `BLENDER_MCP_SAFE_MODE=1`에서 `sys.path` 조작과 파일 import가 허용되는지는 (미확인)입니다. 막히면 두 파일 내용을 그대로 붙여 넣으세요. bpy를 통한 저장·import/export·렌더는 safe mode에서도 허용됩니다(10.5절).

**헤드리스에서**

```bash
blender -b scene.blend --python-exit-code 1 --python 03_playbooks/scripts/scene_audit.py -- --floor-z 0 --ceiling-z 2.3 --out audit.json
blender -b scene.blend --python-exit-code 1 --python 03_playbooks/scripts/building_audit.py -- --collection House --out building.json   # 건물·여러 방일 때
blender -b scene.blend --python-exit-code 1 --python quick_checks.py
```

`--python-exit-code 1`이 없으면 스크립트에서 예외가 나도 종료 코드가 0이라 성공으로 오인합니다([빠른 시작](01_quickstart_setup.md) 3.3절).

---

## 1. 30초 빠른 점검

### 1.1 AI 결과가 싸 보이는 12가지

여러 실무자 자료와 에이전트 스킬이 공통으로 꼽는 "CG 티" 목록입니다([라이팅 가이드](../02_guides/06_lighting_rendering_art_direction.md) 7절과 같은 순서). 렌더 한 장과 `quick_checks()` 출력만 있으면 30초 안에 훑을 수 있습니다.

| # | 싸 보이는 증상 | 30초 확인 | 합격 기준 | 방법 |
|---|---|---|---|---|
| 1 | 하이라이트가 하얀 덩어리, 창이 날아감 | `view_transform`, False Color 한 장 | Standard 아님. 발광체·창 제외 클리핑 ≤ 0.5% [스킬] | [수치] `quick_checks`, [스크립트] `review_render` |
| 2 | "3D 뷰포트 같은" 사진, 넘어지는 수직선 | 렌즈·카메라 높이·pitch | 50 mm 기본값 그대로가 아님. 사람 시점 약 1.6 m. 건축은 pitch 90° + shift | [수치] `quick_checks` |
| 3 | 칼같이 딱딱한 그림자 경계 | 광원 반경·크기 | Point·Spot 반경 > 0, Area 크기 > 0, Sun 0.5° 이상 | [수치] `quick_checks` |
| 4 | 평평하고 모든 곳이 균일하게 밝음 | 키 방향, 명암 폭 | 키가 카메라 축에서 20° 이상 [스킬]. `value_range` ≥ 0.30 [스킬] | [스크립트] `key_angle_deg()`, `review_render` |
| 5 | 모서리에 하이라이트가 없음 | 하드서피스 메시의 Bevel 모디파이어 | 제조 모서리마다 bevel(폭은 2.4절) | [수치] `[o.name for o in bpy.data.objects if o.type=="MESH" and not any(m.type=="BEVEL" for m in o.modifiers)]` (5.0.1·4.2.23 확인) + [눈] 클로즈업 |
| 6 | 플라스틱·밀랍 같음 | metallic·roughness 값, 순흑·순백 픽셀 | metallic 0/1, roughness 변화(맵 표준편차 > 0.01 [스킬]), 순흑·순백·채도 100% 픽셀 ≈ 0 | [수치] `quick_checks`, `pbr_audit`, `review_render` |
| 7 | 반복 무늬, 옆 물체와 선명도가 다름 | 넓은 면 클로즈업 | 반복이 안 보임. 씬 전체 텍셀 밀도 통일 | [눈], Texel Density Checker |
| 8 | 격자처럼 줄 선 가구·소품 | 위 정사영 뷰 | 클러스터 + 작은 노이즈(가구 σ 3 cm·1°) | [눈] `review_views` top |
| 9 | 장난감·미니어처 같음 | 치수, 인체 더미와 비교 | 1 unit = 1 m, 스케일 적용, 치수 범위 안 | [A] `size_out_of_range`, `unapplied_scale` |
| 10 | 번짐·무지개 테두리·지글거리는 노이즈 | 합성 끈 렌더와 A/B | "좋아졌는데 무엇을 했는지 안 보임" 수준. 렌더 노이즈를 그레인으로 쓰지 않음 | [눈] `use_compositing` 끄고 비교 |
| 11 | 그림자 방향이 두 개, 반사와 배경이 따로 놂 | 생성 메시 albedo, HDRI 방향 | albedo에 음영·하이라이트 없음. HDRI 해 방향 = 태양 방향 | [눈] albedo만 렌더, HDRI 회전 비교 |
| 12 | 쇼룸·카탈로그 같음 | 클로즈업, 소품 구성 | 먼지·마모·손때가 물리적 원인이 있는 곳에. 스토리 비트당 소품 3~5개(최대 7) | [눈] |

### 1.2 AI 특유의 형태·배치 결함 (자동으로 먼저 거르기)

| 증상 | 흔한 원인 | 자동 검사 |
|---|---|---|
| 떠 있는 가구, 바닥에 박힌 다리 | LLM이 z값을 추측, origin과 실제 정점 위치 혼동 | [A] `floating_or_wall_mounted`, `below_floor`, `sunk_into` |
| '분해된 의자'(부품 사이 틈) | 좌표 즉흥 계산 | [스크립트] `check_assembly()` → `GAP`, `DETACHED` |
| 치수가 절반 | `size=1` 큐브에 half-extent를 scale로 줌 | [A] `size_out_of_range`, 스펙 대비 치수 비교 |
| 가구끼리 관통 | 좌표 직접 지정, 충돌 검사 생략 | [A] `interpenetrations` |
| 소파가 벽을, 장이 천장을 뚫음 | 방 경계 미확인 | [A] `above_ceiling`(`audit_scene(ceiling_z=...)`), 벽·천장 메시와의 `interpenetrations`. 벽 메시가 없으면 0.5절 방 경계 검사 |
| 문이 벽에 안 뚫림, 열면 벽, 문 없는 방, 창 없는 거실 | 방·문·창을 따로따로 배치 | [스크립트] `building_audit.audit_building()` → `summary.errors` 0, `liminal_risk` |
| 엉뚱한 방향을 보는 가구 | 에셋 정면 규약 불일치, yaw 부호 오류 | [수치] 정면(-Y)과 대상 방향 내적 > 0.9(7.2절) |

---

## 2. 모델링

### 2.1 스케일·트랜스폼·원점

- [ ] `[필수]` **단위 규약**: 1 unit = 1 m, Z-up, 원점 = 바닥 접점(바닥 중앙), 가구 정면 = -Y. 확인: [수치] `scene.unit_settings`, 원점 위치.
- [ ] `[필수][A]` **스케일 적용**: 모든 메시 scale = (1, 1, 1)(허용 1e-4), 음수 스케일 없음. 확인: `unapplied_scale`, `negative_scale`. 처방: `transform_apply(rotation=True, scale=True)` 후 bevel 다시 적용.
- [ ] **치수는 월드 bbox로 잽니다**: `obj.dimensions`는 스케일을 반영하지만 **로컬 축 기준이라 회전을 반영하지 않습니다**(검증에서 "scale=1일 때만 유효"라는 스킬 설명은 틀린 것으로 정정). 배치·검사에는 `matrix_world @ bound_box`로 구한 월드 AABB(축 정렬 바운딩박스)를 씁니다. 확인: [수치] `scene_audit` 리포트의 `dimensions_m`(월드 x·y·z)과 `size_wdh_m`(가구 방향 기준 폭·깊이·높이. 치수 규칙은 이 값으로 비교).
- [ ] **위치를 바꾼 직후 `bpy.context.view_layer.update()`**: 갱신 전에는 `matrix_world`가 옛 값입니다(0.4절 테스트에서도 확인).
- [ ] **CAD(mm) 가져오기**: build123d 등은 mm가 기본이므로 0.001배 후 스케일 적용.

### 2.2 형태·비율

- [ ] `[필수]` **스펙 먼저**: 코드 전에 부품별 치수 명세(JSON)가 있고 사람이 승인함. 확인: [눈] 스펙 파일 존재. 방법은 [모델링 가이드](../02_guides/07_modeling_objects_furniture_sculpture.md) 2.3절.
- [ ] `[필수][A]` **전체 치수 범위**: 이름 키워드별 범위 안. 확인: `size_out_of_range`. 한국 장면은 [치수표](05_reference_dimensions.md) 11절 `KR_SIZE_RULES`.
- [ ] **관계 치수**(절대값보다 중요): 좌판 = 식탁 상판 − 250~305 mm, 스툴 좌판 = 카운터 − 230~305 mm, 협탁 윗면 = 매트리스 윗면 ± 50 mm, 커피테이블 높이 = 소파 좌판 − 0~50 mm. 확인: [수치] 두 부품의 윗면 z 차이.
- [ ] `[KR]` **한국 프리셋**: 식탁 720~750 mm, 좌판 450 mm, 싱크대 850 mm(신축 900), 방문 문틀 900×2100 mm(문짝은 약 60 mm 작음), 구축 아파트 천장 2300 mm(IKEA PAX 2360 mm는 안 들어감), Q 매트리스 1500×2000 mm. 한 장면에 미국·한국 프리셋을 섞지 않습니다. 전체 표는 [치수표](05_reference_dimensions.md).
- [ ] **같은 가구를 반복하면 범위 안에서 조금씩 다르게**: 모든 의자를 정확히 450 mm로 만들면 오히려 CG처럼 보입니다([치수표](05_reference_dimensions.md) 0.3절).
- [ ] **스케일 단서와 함께 봅니다**: 인체 더미(KR 남 1.725 m / 여 1.596 m)와 문틀을 임시로 넣고 4방향 렌더로 비교한 뒤 최종 렌더 전에 숨김. 확인: [눈] `review_views`.
- [ ] **레퍼런스 사진이 있으면 실루엣을 수치로 비교**: 같은 종류끼리(마스크 대 마스크) 비교합니다. 참고 기준값: 블록아웃 IoU ≥ 0.85·비율 오차 5% 이내, 형태 단계 IoU ≥ 0.90·2% 이내([blender-image-to-3d](https://raw.githubusercontent.com/majidmanzarpour/blender-game-skills/main/skills/blender-image-to-3d/SKILL.md), 커밋 1개짜리 커뮤니티 스킬의 값이라 미검증 주장). 사진에서 스케일을 잡을 때는 **카메라부터 맞추고** 형상을 고칩니다.
- [ ] **Infinigen 값을 표준으로 쓰지 않음**: Infinigen 의자는 좌판 윗면이 약 0.47~0.54 m로 표준(0.43~0.48 m)보다 높습니다. 랜덤 생성 범위이지 실측 표준이 아닙니다.

### 2.3 부품 결합 ("분해된 의자" 막기)

- [ ] `[필수]` **연결 맵**: 부품마다 무엇과, 어느 면으로, 얼마나 겹쳐 붙는지 코드 전에 적어 둠([ProfRino Assembly Skill](https://github.com/ProfRino/Blender-MCP-Assembly-Skill) 방식. 라이선스 확인 결과는 [모델링 가이드](../02_guides/07_modeling_objects_furniture_sculpture.md) 6절).
- [ ] `[필수]` **틈 0, 계획에 없는 관통 0**: 연결 맵에 적은 쌍만 5~15 mm 겹침 허용, 나머지 겹침은 실패. 확인: [스크립트] `check_assembly()` → `[]`.
- [ ] **큐브 크기 규약**: `primitive_cube_add(size=2)`에 half-extent를 scale로 주거나, 치수를 메시 정점에 굽고 scale은 1로 둠. `size=1` 큐브에 half-extent를 주면 **치수가 절반**이 됩니다(4.2.23 LTS·5.0.1에서 확인, [모델링 가이드](../02_guides/07_modeling_objects_furniture_sculpture.md) 6절).
- [ ] **두 점을 잇는 부재(다리·레일·파이프)는 Euler 회전 대신 두 점 사이에 직접 생성**: 실린더 회전 축·순서 오류가 흔합니다.
- [ ] **부품 계층 누락 없음**: PartNet 계층을 체크리스트로 씁니다. 의자 = `chair_back` / `chair_seat` / `chair_base`(leg, bar_stretcher, runner, foot) / `chair_arm`. 무엇을 뺐는지 이유를 적게 합니다([PartNet Chair-hier](https://raw.githubusercontent.com/daerduoCarey/partnet_dataset/master/stats/after_merging_label_ids/Chair-hier.txt)).
- [ ] **현실적인 부재 두께**: 원목 식탁 상판 25~40 mm, 에이프런 70~100 × 20~25 mm, 판재 가구 18 mm 합판·MDF, 뒤판 3~6 mm, 문·서랍 틈 2~3 mm(조사 제안값, 원문 검증 안 됨).
- [ ] **부품 이름과 계층**: `<category>_<part>_<pos>`(`chair_leg_FL`), 빈 오브젝트 `chair_ROOT`(원점 바닥 중앙)에 parent. scene_audit가 의자를 한 유닛으로 판정하려면 부모가 필요합니다.

### 2.4 베벨·노멀·셰이딩

- [ ] `[필수]` **제조 모서리마다 bevel**: 크기를 모르면 최대 치수의 0.5% 폭 [스킬, 저자 추가값], 렌더 3 segments·게임 1~2, angle 30°, Harden Normals, Weighted Normal(Keep Sharp)은 스택 맨 끝([scenario hard-surface](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/dcc/blender/scenario-blender-hard-surface/SKILL.md)). 확인: [수치] 1.1절 #5 한 줄 + [눈] 클로즈업.
- [ ] **재질별 bevel 폭(경험치, 원문 검증 안 됨)**: 원목 1~3 mm, 도장 MDF 0.5~1.5 mm, 금속 0.3~1 mm, 석재 2~5 mm, 사출 플라스틱 0.5~2 mm, 패브릭 쿠션 10~30 mm. **스케일 적용 후** 넣습니다.
- [ ] **Auto Smooth 코드 없음**: `use_auto_smooth`는 **4.1에서 제거**됐습니다(5.x가 아님). Smooth by Angle 모디파이어를 씁니다. 확인: [수치] 스크립트에 `use_auto_smooth`가 있으면 `hasattr` 분기.
- [ ] **뒤집힌 노멀 없음**: scene_audit는 검사하지 않습니다. 확인: [눈] 뷰포트 Face Orientation 오버레이. 처방: `bmesh.ops.recalc_face_normals` 또는 `normals_make_consistent(inside=False)`.
- [ ] **Z-fighting 없음**: 같은 평면에서 겹치는 면은 0.1~0.5 mm 띄우거나 합칩니다. 확인: [눈] 그레이징 앵글 렌더.
- [ ] **곡면 제품**: 저폴리 베이스 + crease 또는 holding loop + Subdivision(level 2, 렌더 3). Infinigen 2.0은 테이블 다리·램프·천장등·손잡이를 이 방식으로 다시 만들었습니다([CHANGELOG](https://raw.githubusercontent.com/princeton-vl/infinigen/main/docs/source/CHANGELOG.md)).

### 2.5 메시 무결성

- [ ] `[A]` **non-manifold 엣지**: 콜리전·boolean·프린트·조형물 제작용이면 0(`non_manifold_edges`). 처방: merge by distance(1e-4), 구멍 메우기, 커터도 manifold로.
- [ ] **Boolean**: solver는 Exact 또는 Manifold(Manifold는 최근 버전에만 있으니 버전 확인). 커터는 숨기고(`hide_render`), 적용 전후 non-manifold 개수를 비교.
- [ ] **종이처럼 얇은 판 없음**: 3D Print Toolbox 두께 검사의 `thickness_min`을 가구용으로 0.005~0.01 m로 올려 검사([mesh_helpers.py](https://raw.githubusercontent.com/blender/blender-addons/main/object_print3d_utils/mesh_helpers.py)). 노멀이 올바르다는 전제가 필요합니다.
- [ ] **면적 0인 면·떨어진 정점·와이어 엣지 없음**: 확인: [수치] bmesh로 `f.calc_area() < 1e-9` 개수.
- [ ] **메시를 텍스트로 직접 찍지 않음**: 정점 좌표 나열 대신 primitive·modifier·bmesh 연산으로 구성(프로파일 커브만 예외).

### 2.6 AI 생성 메시를 가져왔을 때

- [ ] `[필수]` **정규화**: 스케일·원점·트랜스폼 적용, 중복 정점 병합, 노멀 재계산을 **가져오자마자**([AI 3D 생성 가이드](../02_guides/04_ai_3d_generation.md) 6.2절 코드).
- [ ] **감량은 Voxel Remesh 먼저, Decimate 나중**: 바로 decimate하면 의자 다리·난간 같은 얇은 형상이 부서집니다.
- [ ] **텍스처에 조명이 구워지지 않았는지**: albedo에 그림자·하이라이트가 있으면 새 조명에서 광원이 둘인 것처럼 보입니다. 확인: [눈] Emission으로 albedo만 렌더. 처방: PBR 출력 옵션으로 다시 받거나 라이브러리 재질로 교체.
- [ ] **통짜 메시 대신 파트 분리 또는 재모델링**: 파트별 bbox와 주축을 뽑아 표준 치수로 스냅한 뒤 bpy primitive로 다시 만들고, 원본은 IoU 비교용 레퍼런스로만 씁니다.
- [ ] `[KR]` **생성 모델 라이선스**를 9절에서 먼저 확인(Hunyuan 계열은 한국 제외).

### 2.7 조형물·유기 형상

- [ ] **형태는 암시적 표면으로**: SDF(smooth union k 0.03~0.08)·metaball·Mesh to Volume으로 잡고, voxel remesh(0.003~0.01 m) → Multires·Displace → Decimate → normal·AO bake 순서(조사 제안값).
- [ ] **받침대·설치 부재는 하드서피스로 따로**(bevel 포함).
- [ ] **실물 제작(FRP 등)이면 수밀성·셸 두께·언더컷을 따로 검증**합니다([rodin-via-blender](https://github.com/KaelNebula/rodin-via-blender) 사례).

---

## 3. 재질·텍스처

### 3.1 PBR 값 범위

- [ ] `[필수]` **Metallic은 0 또는 1**: 중간값은 칠 벗겨진 경계 같은 전환부 마스크와 안티앨리어싱 픽셀에만. 확인: [수치] `quick_checks`, `pbr_audit`.
- [ ] **금속 Base Color는 밝게**: 실측 linear 값 예시 알루미늄 0.916, 크롬 (0.654, 0.685, 0.701), 구리 (0.932, 0.623, 0.522)([physicallybased.info materials.json](https://raw.githubusercontent.com/AntonPalmqvist/physically-based-api/main/deploy/v2/materials.json), CC0). "어두운 금속"은 대개 roughness나 오염 문제입니다. `pbr_audit`는 금속인데 최대 채널이 linear 0.4 미만이면 경고합니다.
- [ ] **비금속 albedo 범위**: sRGB 30~240(scenario 감사 기준 30~243, 벗어나는 픽셀 2% 미만 [스킬]). glTF Asset Auditor 기본 "PBR safe color"도 30~243입니다. 실측 linear 범위는 숯 0.02 ~ 눈 0.85이고 콘크리트 0.51입니다. UE Path Tracer 문서는 diffuse Base Color를 0.8 미만으로 두라고 권합니다.
- [ ] **Roughness 0 금지**: 0.01~0.02 이상. 거울·크롬도 약간은 둡니다.
- [ ] **비금속 Specular**: IOR 1.5, Specular IOR Level 0.5(기본값) 유지.
- [ ] **발광 재질**: Principled `Emission Strength` 기본값이 0이므로 발광이 필요하면 값을 넣었는지 확인.
- [ ] **녹은 비금속**: 녹슨 부위는 Metallic 0(physicallybased.info의 Rust는 비금속).

### 3.2 색공간·노멀 규약·노드 구조

- [ ] `[필수]` **색공간**: Base Color·Emission 이미지만 sRGB, roughness·metallic·normal·height·AO·ORM은 Non-Color. 확인: [스크립트] `pbr_audit`. 이름은 `'Non-Color'` → `'Linear Rec.709'` → `'Linear'` 순서로 시도([ahujasid addon.py](https://raw.githubusercontent.com/ahujasid/blender-mcp/main/addon.py)).
- [ ] **노멀맵 경로**: Image(Non-Color) → Normal Map 노드(Tangent Space) → Principled Normal. Blender·glTF는 OpenGL(Y+, Poly Haven `nor_gl`), DirectX(`nor_dx`) 맵은 G 채널 반전. 확인: [눈] 요철이 뒤집혀 보이지 않는지.
- [ ] **재질 하나에 Material Output 1개, Principled 1개**: 중복되면 뷰포트는 맞는데 렌더가 회색이 되는 비결정적 셰이딩이 생깁니다([issue #190](https://github.com/ahujasid/blender-mcp/issues/190)). 재질 스크립트는 `nodes.clear()` 후 다시 만드는 멱등 구조로.
- [ ] `[KR]` **노드는 이름이 아니라 `type`으로 찾기**: `next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')`. 한국어 UI에서 새 노드 이름이 번역되면 `nodes['Principled BSDF']`가 실패합니다(일본어 UI 실사례, [hideki711014 규칙](https://github.com/hideki711014/roo-blendermcp-jp-rules)).
- [ ] **Principled v2 소켓 이름**: `Specular IOR Level`, `Coat Weight`, `Transmission Weight`, `Subsurface Weight`, `Emission Color`(`Subsurface Color`는 없음). 비활성 소켓은 문자열 키 접근이 KeyError이므로 순회해서 찾기.
- [ ] **폐기·제거된 API 없음**: Musgrave 노드(4.1 제거 → Noise의 fBM 등), `mat.use_nodes = True`(5.0 폐기 예고 → `if bpy.app.version < (5, 0, 0)`로 분기).

### 3.3 타일링·스케일

- [ ] **Mapping 스케일 = 표면 크기 ÷ 텍스처 실측 크기**: 예) 바닥 6 m, 텍스처 2 m → 3. Poly Haven은 실측 크기(`polyhaven_scale_mm`)를 줍니다. 확인: [눈] 타일·나뭇결 크기가 가구 치수와 맞는지.
- [ ] **mcp-for-blender는 2026-09-21 이후 버전**(PR #367 반영, 2.1.0은 2026-09-25): 이전 버전은 Poly Haven normal·displacement 연결 누락, Mapping TEXTURE 모드로 타일링 역전(2 m 텍스처가 4 m 면에서 1.993회가 아니라 0.509회 반복) 버그가 있었습니다([PR #367](https://github.com/ahujasid/blender-mcp/pull/367)). 노드를 손으로 짜지 말고 `set_texture`를 쓰세요.
- [ ] **반복이 안 보임**: 넓은 면은 두 번째 텍스처 블렌딩, 브레이크업 마스크, 트라이플래너(룩뎁 임시용). 확인: [눈] 넓은 면 클로즈업.
- [ ] **해상도**: Poly Haven은 1k~2k로 받고 카메라 가까운 히어로만 4k(한 단계마다 용량 약 4배).

### 3.4 변화·마모

- [ ] **roughness에 공간 변화**: 맵이나 노이즈로, 표준편차 > 0.01 [스킬]. 확인: [수치] `quick_checks`의 `roughness_const` 목록 중 히어로 재질.
- [ ] **개체별 변화**: 같은 의자 10개가 완전히 같은 색이 아님(Object Info Random → HSV 약간). 확인: [눈].
- [ ] **결함은 원인에 맞는 채널로, 한 레이어에 하나**: 긁힘 → Normal/Bump, 지문·기름 → Roughness만, 먼지 → 위를 향한 면(Normal Z 마스크), 틈새 때 → AO·Pointiness 마스크. 위치는 "왜 거기가 닳았나"를 따릅니다.
- [ ] **렌더러별 마스크 동작 확인**: EEVEE에서 Geometry Pointiness는 상수 0.5, Bevel 노드는 입력 노멀 통과(소스 확인). AO 노드는 EEVEE에서도 동작하지만 화면 공간이라 결과가 다릅니다. EEVEE 스크린샷으로 "마모가 안 보인다"며 값을 올리지 말고 Cycles로 확인하고, 게임·glTF용이면 **베이크**합니다.
- [ ] **4단 구성**: 베이스 + 변화 + 마모 + 오염. AAA급 웨더링이 필요하면 Substance 3D Painter MCP 쪽이 효율적입니다([텍스처링 가이드](../02_guides/05_texturing_materials.md) 5.4절).

### 3.5 AI로 만든 텍스처

- [ ] **albedo에 조명·그림자·하이라이트 없음**: 확인: [눈] albedo만 렌더(2.6절과 같음).
- [ ] **Meshy는 `enable_pbr=true`를 명시**(기본 false), `remove_lighting`(기본 true, meshy-6/latest만), 기존 UV 유지는 `enable_original_uv=true`. `texture_resolution` 4k·8k는 **Base Color에만** 적용되고 PBR 맵은 2K로 남습니다([postprocessing.ts](https://raw.githubusercontent.com/meshy-dev/meshy-mcp-server/main/src/schemas/postprocessing.ts)).
- [ ] **이미지 생성 모델에게 normal·roughness·metallic 맵을 "그려 달라"고 하지 않음**: albedo만 생성하고 데이터 맵은 전용 추정기나 height 베이크로 만듭니다.
- [ ] **여러 뷰 투영 이음새·가림 영역 없음**: 확인: [눈] 다리 안쪽·좌판 아래 등 가려진 면.
- [ ] **도구가 "성공"을 반환해도 노드 연결을 렌더로 확인**: Poly Haven 버그 사례의 교훈입니다.

---

## 4. UV·베이크

### 4.1 UV

- [ ] `[A]` **UV 레이어 있음**: `no_uv` 0건(최종 단계).
- [ ] **AI 생성 메시·리토폴 결과는 UV를 새로 폄**: 생성기 UV는 리토폴을 거치면 깨집니다. 하드서피스·가구는 Smart UV Project(`angle_limit=math.radians(66)` — **라디안**, `island_margin=0.02`) → Pack Islands(`shape_method='CONCAVE'`), 유기체는 Unwrap `MINIMUM_STRETCH`.
- [ ] **겹침·늘어짐 없음**(의도한 미러 겹침 제외). 확인: [눈] 체커 텍스처, glTF Asset Auditor의 UV 겹침·거터 검사.
- [ ] **섬 여백**: 2K에 4~8 px 정도(xatlas padding 관례). 베이크 margin보다 작으면 번짐이 섞입니다.
- [ ] **텍셀 밀도를 씬 전체에서 통일**: 목표값 예) 콘솔·PC 10.24~20.48 px/cm, 모바일·웹 5.12~10.24 px/cm(업계 관례, 신뢰도 낮음). 숫자보다 **통일**이 중요합니다. 확인: [수치] [Texel Density Checker](https://github.com/mrven/Blender-Texel-Density-Checker)(v2026.1.1).
- [ ] **PartUV를 쓰면 라이선스 확인**: 프로젝트는 Apache-2.0이지만 필수 전처리 PartField는 NVIDIA 비상업 라이선스입니다(9.2절).

### 4.2 베이크

- [ ] `[필수]` **모든 재질 슬롯이 실제로 구워졌는지 이미지로 확인**: 재질에 활성 + 선택된 Image Texture 노드가 없으면 **오류 없이 그 슬롯을 건너뛰고** `{'FINISHED'}`를 반환합니다(5.0.1 메시지 "No active and selected image texture node found in material…", 4.2는 "No active image found in material…"). 조용히 일부만 구워지는 게 가장 흔한 사고입니다.
- [ ] **Base Color는 `type='DIFFUSE'`, `pass_filter={'COLOR'}`**: 기본 pass_filter로 구우면 조명이 섞입니다.
- [ ] **Metallic은 전용 타입이 없음**: Metallic 입력을 Emission에 임시 연결해 `type='EMIT'`로 굽고 원래 연결을 복구.
- [ ] **Normal은 `normal_space='TANGENT'`**, 이미지는 Non-Color.
- [ ] **해상도는 이미지 노드 기준**: `width/height`(기본 512)는 외부 파일 저장 때만 쓰입니다. 인자로 안 준 값은 씬 Bake 패널 값을 씁니다.
- [ ] **margin**: 2K에 16 px, 4K에 16~32 px(일반 실무 값). Cycles에서만 베이크됩니다.
- [ ] **고폴리 → 로폴리**: `use_selected_to_active=True`, `cage_extrusion`, `max_ray_distance`를 지정하고 결과에 구멍·번짐이 없는지 [눈].
- [ ] **절차 노드·Displacement·SSS는 게임·glTF로 나가지 않음**: 베이크하거나 normal로 굽습니다.

---

## 5. 라이팅·렌더

### 5.1 색관리·노출

- [ ] `[필수]` **뷰 변환이 Standard가 아님**: 포토리얼 기본 AgX(+ Look Medium High Contrast 또는 Punchy), 제품·SKU 색 일치는 Khronos PBR Neutral, HDR 납품·파이프라인 표준은 ACES 2.0. 확인: [수치] `quick_checks`. OCIO 파일 기본값은 Standard이고 새 씬 AgX는 4.0 이후 씬 기본값이므로, `--factory-startup`이나 새 씬에서는 **반드시 다시 확인**합니다([config.ocio](https://raw.githubusercontent.com/blender/blender/v5.2.2/release/datafiles/colormanagement/config.ocio)).
- [ ] **밝기는 램프 일괄 조정이 아니라 `view_settings.exposure`로**: 광량비(key:fill:rim)를 지킵니다.
- [ ] `[필수]` **클리핑**: 발광체·창을 뺀 클리핑 픽셀 ≤ 0.5% [스킬]. AgX는 클리핑을 부드럽게 숨기므로(선형 4.0 → 표시 약 0.91) 표시 이미지가 아니라 **False Color와 EXR 수치**로 판정합니다. 확인: [스크립트] `review_render` → `clip_pct`.
- [ ] **피사체 노출**: False Color에서 피사체가 회색(≈ 0 EV). 무엇을 날릴지는 의도적으로 고릅니다.
- [ ] **명암 폭**: `value_range` ≥ 0.30 [스킬]. 흑백으로 봐도 형태가 읽힘(squint test).
- [ ] **순흑·순백·채도 100% 픽셀 없음**(의도한 검은 배경 제외). 확인: `pure_black_pct`, `sat100_pct`.

### 5.2 광원

- [ ] `[필수]` **광원 크기 0 금지**: Point·Spot 반경 > 0, Area 크기 > 0, Sun 각도 0.5° 이상(실제 태양 0.526~0.545°, 부드럽게 2~5°). bpy로 만든 라이트는 반경 0이 기본입니다(0.4절 테스트, [DNA_light_types.h](https://raw.githubusercontent.com/blender/blender/main/source/blender/makesdna/DNA_light_types.h)). 확인: [수치] `quick_checks`.
- [ ] **색은 RGB 추측 대신 켈빈**: 5.x는 `use_temperature=True; temperature=…`([properties_data_light.py](https://raw.githubusercontent.com/blender/blender/v5.2.2/scripts/startup/bl_ui/properties_data_light.py)). 켜면 `color`가 곱해지는 틴트로 바뀌므로 **흰색으로 되돌립니다**(확인: `quick_checks`의 `tint`). 기준: 촛불 약 1800 K, 텅스텐 3200 K, 주광 5500 K, 흐림 6500 K, 달빛 8000 K 이상([arjun988 lighting](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/lighting/SKILL.md) [스킬]). 실내 실용광은 2700 K 안팎. 네온·SF 광원만 RGB.
- [ ] **키는 카메라 축에서 20° 이상**: 기본 배치 카메라 축에서 40°, 위로 35°, 피사체 반경의 3배 거리, 광원 크기 = 피사체 반경([scenario lighting](https://raw.githubusercontent.com/scenario-labs/skills/main/skills/dcc/blender/scenario-blender-lighting-rendering/SKILL.md) [스킬]). 확인: [스크립트] `key_angle_deg()`([라이팅 가이드](../02_guides/06_lighting_rendering_art_direction.md) 3.3절).
- [ ] **필은 key:fill 3~4:1에서 시작 → 레퍼런스 그림자 밀도에 맞춤**: 필을 쌓아 그림자를 없애지 않습니다. 필은 그럴듯한 반사면 근처에만.
- [ ] **실내 World 기여 < 10%** [스킬]: Light Group으로 분리 렌더해 비교.
- [ ] **광원마다 존재 이유**: World 0, 램프 전부 끈 상태에서 HDRI → 키 → 실용광 → 고보 순으로 하나씩 추가했고, 이름이 역할을 말함(`LGT_Key_Main`, `LGT_Fill_Soft`).
- [ ] **HDRI 해 방향 = 태양 방향**, 배경과 반사가 같은 환경.

### 5.3 렌더 설정

- [ ] **렌더를 파일로 저장해서 봄**: ahujasid MCP for Blender에는 렌더 tool이 없습니다([#61](https://github.com/ahujasid/blender-mcp/issues/61), not planned). 뷰포트 스크린샷은 최종 색관리·GI·DOF와 다르므로 판정 근거가 아닙니다.
- [ ] **EEVEE 식별자**: 5.0+ `BLENDER_EEVEE`, 4.2~4.x `BLENDER_EEVEE_NEXT`(enum에서 골라 쓰기). `use_bloom`·`use_ssr`·`use_gtao`는 5.x에 없어 AttributeError.
- [ ] **EEVEE 파이널은 레이트레이싱 켬**: 팩토리 기본은 꺼짐(0.4절 테스트). 확인: [수치] `quick_checks`의 `eevee_raytracing`. 같은 장면 Cycles 레퍼런스와 약 30% 이내 [스킬].
- [ ] **Cycles**: adaptive threshold 0.01·OIDN(Albedo + Normal)이 기본값(소스 확인). 유리가 많으면 transmission bounces 16 이상 [스킬]. 확인: `quick_checks`. 파이어플라이가 보일 때만 clamp indirect(기본 10)를 낮춥니다.
- [ ] **렌더 노이즈를 그레인 대용으로 쓰지 않음**: 완전히 디노이즈하고 그레인은 마지막에 따로.
- [ ] **Glare는 타입을 명시**: 5.x 기본 타입은 **Streaks**(Bloom 아님). 5.x 소켓 범위는 Size·Strength 0~1, Iterations 2~5이고, 구버전 값(Size 8~9, mix −0.7)은 입력할 수 없습니다([node_composite_glare.cc](https://raw.githubusercontent.com/blender/blender/v5.2.2/source/blender/nodes/composite/nodes/node_composite_glare.cc)).
- [ ] **후처리는 절제**: 효과를 분명히 보이게 올렸다가 의식되지 않을 때까지 내림. 확인: [눈] `use_compositing` 끈 렌더와 A/B.
- [ ] **판정용 출력은 EXR**: PNG에는 뷰 변환이 구워집니다.

### 5.4 Unreal Engine일 때

UE 5.7 문서의 비공식 Markdown 미러로 확인한 내용입니다(공식 원문과 직접 대조하지 못함). 자세한 값은 [라이팅 가이드](../02_guides/06_lighting_rendering_art_direction.md) 4절.

- [ ] **Lumen**: Static 라이트만 미지원(Stationary·Movable은 GI에 반영, [Lumen GI 문서 미러](https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine.md)). 벽 두께 10 cm 이상(Software RT 문맥), 작은 발광 메시는 Emissive Light Source 켬([Lumen 기술 문서 미러](https://raw.githubusercontent.com/CharlieCardenasToledo/ue5-docs-mcp/main/docs-md-py/en-us/unreal-engine/lumen-technical-details-in-unreal-engine.md)).
- [ ] **거울·크롬끼리 비치는 장면**: Lumen 반사 바운스(기본 1)를 올림(PPV 최대 8, HWRT Hit Lighting 필요).
- [ ] **VSM 그림자**: 로컬 라이트 Source Radius 기본 0 → 실제 광원 크기로, directional은 Source Angle.
- [ ] **Substrate 다층 재질**: 새 프로젝트 기본 Blendable GBuffer를 Adaptive로 바꿈.
- [ ] **노출**: 룩뎁 중 자동 노출을 끄고 고정. Bloom은 PPV Threshold로 제어("emissive 1.0 초과" 규칙은 경험칙일 뿐).
- [ ] **물리 단위를 섞지 않음**: Directional lux, Sky Light·Emissive cd/m², 로컬 라이트는 Candela·Lumen·Unitless 중 하나.
- [ ] **파이널(Path Tracer + MRQ)**: diffuse Base Color < 0.8, Spatial × Temporal 샘플 곱이 8을 넘으면 `r.TemporalAASamples`를 맞추거나 AA를 None으로.

---

## 6. 카메라·구도

- [ ] `[필수]` **카메라 존재**(렌더 전). 확인: [수치] `quick_checks`의 `camera`.
- [ ] **초점거리를 샷 의도로 정함**: 와이드 18~28 mm, 스토리·제품 35~50 mm, 인물·히어로 85~135 mm([arjun988 camera-cinematography](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/camera-cinematography/SKILL.md) [스킬]). 실내는 24~35 mm. 기본 50 mm를 그대로 두지 않습니다. 확인: [수치] `camera_lens_mm`.
- [ ] **사람 시점 높이 1.6~1.7 m**(레퍼런스 사진 높이가 있으면 그것을 따름). 확인: [수치] `camera_height_m`.
- [ ] **수직선이 서 있음**: 건축·인테리어는 카메라 pitch 수평(90°) + Shift Y로 투시 보정. 확인: [눈] 벽 모서리가 기울지 않았는지.
- [ ] **DOF가 없지도 과하지도 않음**: 초점은 거리값 대신 Empty 대상으로. 과한 DOF는 미니어처처럼 보입니다(f-stop 수치 규칙은 hyperrealism 스킬의 값이라 미검증 주장, 출발점 f/5.6).
- [ ] **움직임이 있으면 모션블러**.
- [ ] **구도를 조명·디테일보다 먼저 고정**: 후보 여러 개를 저품질로 렌더해 비교한 뒤 하나 고정. 프레임 밖이나 흐려질 곳의 디테일은 낭비입니다.
- [ ] **한 뷰에 히어로 하나**, 전경·중경·배경 레이어, 리딩 라인, 수평선 수평, 프레임 가장자리 탄젠트 없음, 디테일 사이 쉬는 공간(attention budget). 확인: [눈] 썸네일·흑백으로 봐도 히어로가 먼저 읽힘.
- [ ] **스케일 단서**: 인체 더미·문 등 크기를 아는 물체가 화면이나 검토 렌더에 있음. [KR] 문 높이 2.03~2.13 m는 미국 인치 규격이므로 한국 장면은 문틀 2100 mm 기준.
- [ ] **검토 뷰 세트**: `review_views`(위·정면·측면·3/4)로 형태·배치를 보고, 최종 카메라 렌더로 룩을 봅니다. 검토용 이미지는 긴 변 약 1000 px면 충분합니다(10.6절).

---

## 7. 배치

### 7.1 물리적 타당성

- [ ] `[필수][A]` **부유 0**: `floating_or_wall_mounted` 목록이 의도한 벽걸이·천장등·선반 위 액자뿐.
- [ ] `[필수][A]` **바닥 아래로 박힘·다른 물체 속으로 파고듦 0**: `below_floor`, `sunk_into`.
- [ ] `[필수][A]` **유닛 간 관통 0**: `interpenetrations` 빈 목록. 완전히 들어간 물체는 `bbox_overlap_depth_m`로 보조 확인.
- [ ] `[필수][A]` **벽·천장 관통 0**: 벽·천장 메시가 있으면 `interpenetrations`에 가구–벽·천장 쌍이 없고, `audit_scene(ceiling_z=2.30)`의 `above_ceiling` 0건. 벽 메시가 없으면 0.5절 방 경계 검사(`OUT_OF_ROOM` 0건). [KR] 구축 아파트 천장 2300 mm에서 키 큰 수납(PAX 2360 등)을 특히 확인.
- [ ] **건물·여러 방이면 건축 상식 검사**: [스크립트] `building_audit.audit_building(collection=...)`의 `summary.errors` 0, `liminal_risk`가 `high`가 아님(문이 벽에 뚫렸는지, 열면 벽·허공인지, 문 없는 방·창 없는 거실·복도형 빈 방 반복 등). **`no_rooms_found` 경고가 있으면 통과가 아닙니다**(방을 못 알아봐서 오류가 0으로 나온 것). 이름 규칙(`Floor_living`, `Wall_N`, `Door_01`, `Window_01`, 한국어는 `거실_바닥`·`현관문`처럼 끝 단어가 역할)은 [scripts/README](scripts/README.md)를 따릅니다.
- [ ] **한 유닛 안의 부품 관통**은 `check_assembly()`로(scene_audit는 일부러 제외).
- [ ] **소품은 받침면 위에**: `placement_utils.drop_to_surface()`로 가장 높은 받침면에 올리거나, rigid body로 2~5 cm 위에서 떨어뜨려 안착시킨 뒤 변환을 굳힘. 안착 후 45° 이상 기울었거나 1 m 이상 이동했으면 실패로 보고 다시 배치(SceneSmith 소품 설정, [base_manipuland_agent.yaml](https://raw.githubusercontent.com/nepfaff/scenesmith/main/configurations/manipuland_agent/base_manipuland_agent.yaml)).
- [ ] **고폴리 에셋은 decimate 프록시로 검사**: 그대로 돌리면 MCP 소켓 타임아웃(180초)에 걸립니다.

### 7.2 방향

- [ ] `[필수]` **정면 규약 통일**: 이 저장소는 가구 정면 = -Y(Blender Front 뷰에서 보이는 면). glTF 원본은 정면 +Z, Y-up이라 가져오면 -Y가 됩니다. 에셋마다 정면을 정규화한 뒤 배치합니다(I-Design의 `+π` 보정은 규약 불일치의 흔적).
- [ ] **바라보기 검증**: 정면(-Y) 벡터와 대상 방향의 내적 > 0.9(SceneSmith `check_facing_tool`과 같은 발상). 정면이 -Y인 에셋의 yaw = `atan2(dx, -dy)`(수학적으로 검증됨). 설정은 `placement_utils.face_towards()`.
- [ ] **기능적 정면이 방 안쪽**: 서랍장·옷장·가전은 정면이 방을 향하고, 의자는 테이블을 향함.
- [ ] **벽 붙이기 간격**: 벽 면에서 1~5 cm(`place_against_wall(gap=…)`, SceneSmith 스냅 마진 0.01 m).

### 7.3 동선·간격

권장 기본값은 [치수표](05_reference_dimensions.md) 8절(출처 간 충돌 정리)을 따릅니다. 확인은 [스크립트] `placement_utils.check_clearances([(A, B, 최소, 최대), …])`(평면 AABB 사이 거리)와 [눈] 위 정사영.

- [ ] `[필수]` **주동선**: 하드 760 mm 이상, 기본 900 mm. SceneSmith 프롬프트 0.7~1.0 m, SAGE 주요 가구 사이 60~90 cm.
- [ ] `[필수]` **문 여는 방향을 정하고 궤적 비우기**: 방 문은 그 방 안쪽으로, 경첩은 벽 모서리 쪽, 좁은 욕실은 바깥여닫이, 두 문이 서로 부딪히지 않게. [스크립트] `building_audit`의 `swing.recommended`대로 `open_door()`로 열고 `door_swing_*` 경고 0. 궤적(문 폭 반지름 1/4 원)에 가구 없음.
- [ ] `[필수]` **문 앞 비우기**: 문 스윙 영역(약 문 폭 × 문 폭)에 가구 없음. SAGE 솔버는 문 폭 × 문 폭 정사각형을 막고, "90 cm 회전반경"은 프롬프트 문구입니다([object_placement_planner.py](https://raw.githubusercontent.com/NVlabs/sage/main/server/objects/object_placement_planner.py)).
- [ ] **창 앞**: 이유 없이 막지 않음(SAGE 솔버는 창 앞 여유를 계산하지 않으므로 직접 keep-out을 둠).
- [ ] **소파–커피테이블 350~450 mm**(기본 400). 출처별로 SceneSmith 0.3~0.5 m, Infinigen 0.45~0.6 m로 다릅니다.
- [ ] **식탁–벽 915 mm 이상**(의자 빼기), 뒤로 걸어 지나가면 1118 mm.
- [ ] **침대 옆 600 mm 이상**(기본 750).
- [ ] **소파–TV장 약 2~3 m**(Infinigen soft 비용항), 55형 기준 약 2.4 m.
- [ ] **벽 장식**: 그림 중심 약 1450 mm(SceneSmith 1.4~1.7 m), 가구 위면 + 200~250 mm, 같은 종류 벽걸이는 같은 높이(Holodeck 지침).

### 7.4 밀도·리듬

- [ ] **가구 점유율 약 30~40%**(SAGE 프롬프트 규칙). 확인: [수치] 가구 바닥 면적 합 ÷ 방 면적.
- [ ] **축 정렬·등간격이 아님**: 스냅 뒤 자연 노이즈를 소량 — 가구 XY σ 0.03 m·yaw σ 1°, 소품 XY σ 0.01 m·yaw σ 3°(SceneSmith Natural 프로파일, [base_furniture_agent.yaml](https://raw.githubusercontent.com/nepfaff/scenesmith/main/configurations/furniture_agent/base_furniture_agent.yaml)). 쇼룸 컨셉이면 노이즈 없음(planner가 키워드로 스타일 선택).
- [ ] **무작위도 과하지 않음**: SceneSmith 비평가는 '혼돈'도 결함으로 봅니다(CHAOS DETECTION).
- [ ] **반복 인스턴스는 회전·스케일을 살짝 다르게**. 확인: [눈] 위 정사영.

### 7.5 초점·스토리

- [ ] **초점 1개**(TV 벽·벽난로·창 전망)와 기능 그룹(대화·식사·작업·수면)을 먼저 정하고 그룹 사이 동선을 그은 뒤 배치. 초점이 없으면 가구가 벽을 따라 흩어진 '대기실' 배치가 됩니다.
- [ ] **스토리 비트당 소품 3~5개(최대 7) + 마모·데칼 단서 1~2개**. 균일하게 깔린 잡동사니 금지(아트디렉션 체크리스트 수준의 근거).
- [ ] **히어로 구역은 의도는 높게 잡음은 낮게, 배경은 실루엣만, 이동·카메라 경로는 비움**.
- [ ] **스케일 매칭**: 책상–의자, 식탁–의자처럼 관련 가구끼리 높이 관계가 맞음(2.2절 관계 치수).

### 7.6 야외 산포

- [ ] **LLM이 좌표를 찍지 않고 산포 파라미터만 조정**: Distribute Points on Faces를 **Poisson Disk**로(Distance Min으로 최소 간격 보장).
- [ ] **최소 간격(경험치, 미검증)**: 큰 나무 3~6 m, 관목 1~2 m, 바위 0.5~2 m. 길·건물 주변은 밀도 0, 거리 기반 falloff.
- [ ] **정렬·변주**: 나무는 월드 Z, 바위·풀은 표면 Normal. 균일 스케일 0.8~1.2, Z 회전 랜덤, 바위는 표면에 10~20% 묻음, 클러스터 3·5·7개.
- [ ] 확인: [눈] 위 정사영 + 카메라 뷰. 산포 코드는 [배치 가이드](../02_guides/08_scene_layout_placement.md) 7.3절(4.2.23 LTS·5.0.1 확인).

### 7.7 4뷰 렌더 비평과 종료 조건

- [ ] **숫자 검사(7.1~7.3) 통과 후** 4뷰(`review_views`: 위 정사영·정면·측면·3/4)를 VLM에 보여 줍니다. 원근 뷰만으로는 거리를 잘 못 읽습니다.
- [ ] **점수형 루브릭**: SceneSmith 6항목(Realism, Functionality, Layout, Completeness, Prompt Following, Reachability) 0~10점. 모두 9점 이상이면 종료, 최대 3라운드(소품 2라운드), 한 항목이 2점 이상 또는 총점이 1점 이상 떨어지면 체크포인트 롤백을 검토(자동이 아니라 planner 판단), 충돌이 있으면 Realism ≤ 4([critic](https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/prompts/data/furniture_agent/stateful_critic_agent.yaml), [planner](https://raw.githubusercontent.com/nepfaff/scenesmith/main/scenesmith/prompts/data/furniture_agent/stateful_planner_agent.yaml)).
- [ ] **최종 표는 SceneEval 10개 지표**로: Collision, Navigability, Out of Bounds, Opening Clearance(여기까지 기하 검사) + Object Count, Attribute, Obj-Obj Relationship, Obj-Architecture Relationship, Support, Accessibility(VLM 판정)([SceneEval](https://github.com/3dlg-hcvc/SceneEval)).
- [ ] `[필수]` **DONE 조건을 프롬프트에 하드 규칙으로**: `collisions==[] AND floating==[] AND blocked_doors==[] AND min_walkway>=0.9m`. 풀 수 없는 충돌은 그 오브젝트를 지우는 편이 낫습니다(SceneSmith 디자이너 지시).

---

## 8. 익스포트·엔진

### 8.1 내보내기 전

- [ ] `[필수]` **재질은 Principled BSDF 하나**, 절차 노드(Noise·Voronoi·ColorRamp 등)·Displacement·SSS는 **베이크**(glTF는 절차 노드를 버림).
- [ ] **ORM 패킹**: R = AO, G = Roughness, B = Metal. Blender 익스포터는 metallic = B, roughness = G를 같은 이미지에서 읽습니다([glTF-Blender-IO 문서](https://raw.githubusercontent.com/KhronosGroup/glTF-Blender-IO/main/docs/blender_docs/scene_gltf2.rst)).
- [ ] **AO는 `glTF Material Output`이라는 이름의 노드 그룹의 Occlusion 입력으로**. `[KR]` 이 그룹은 스크립트에서 정확한 영어 이름으로 만듭니다(New Data 번역 주의).
- [ ] **트랜스폼 적용**(스케일은 `[A]` `unapplied_scale`, 회전은 [수치] `rotation_euler`), merge by distance(0.0001 m), 노멀 재계산.
- [ ] **고아 데이터는 이름으로 명시 삭제**: `orphans_purge`는 금지(재질 소실 사고).
- [ ] **라이선스 메타는 커스텀 프로퍼티 → glTF extras**로 실어 보냄(9.4절).
- [ ] **내보낼 때 옵션**: +Y up, Apply Modifiers, UV·Normals·Tangents 포함, Custom Properties를 extras로.

### 8.2 검증

- [ ] `[필수]` **glTF 스펙 오류 0**: `npx @gltf-transform/cli@4.5.0 validate out.glb`의 종료 코드 0. npm `gltf-validator`는 CLI가 아니라 라이브러리라서 `npx gltf-validator out.glb`는 동작하지 않습니다([에셋 가이드](../02_guides/10_assets_pipeline_licensing.md) 2.6절 테스트).
- [ ] **에셋 규칙**: [glTF Asset Auditor](https://github.com/KhronosGroup/glTF-Asset-Auditor) 프로파일(기본 텍스처 512~2048·2의 거듭제곱·PBR 30~243·삼각형 최대 100,000·파일 최대 5,120 KB·UV 겹침·거터·텍셀 밀도). 웹·AR 기준이라 AAA 히어로에는 값을 조정합니다.
- [ ] **슬롯 감사**: 만든 맵이 GLB 슬롯에 모두 들어갔는지(`glb_material_report`). AO·Displacement·SSS·절차 노드는 조용히 빠집니다.
- [ ] **재임포트 + 4뷰 렌더**로 형태·재질 확인, 엔진 임포트 테스트(스케일·축·재질 연결).
- [ ] **익스포트 후 다시 `scene_audit`**: 재임포트한 파일에서도 issue 0.

### 8.3 네이밍

- [ ] **UE 규칙**: 정적 메시 `SM_`(또는 `S_`), 스켈레탈 `SK_`, 재질 `M_`/`MI_`, 텍스처 `T_<이름>_D/_N/_ORM`([Allar 스타일 가이드](https://github.com/Allar/ue5-style-guide), 커뮤니티 가이드. UE5용은 v2 브랜치).
- [ ] **콜리전·LOD·소켓 접두사**: `UCX_`(볼록)·`UBX_`·`UCP_`·`USP_` + `[렌더메시이름]_##`, LOD는 `_LOD0` 접미사, 소켓은 `SOCKET_`([Send to Unreal 문서](https://raw.githubusercontent.com/EpicGamesExt/BlenderTools/main/docs/send2ue/asset-types/static-mesh.md)).
- [ ] **`.001` 같은 숫자 접미사·한글·CamelCase 없음**: 확인: [수치] `quick_checks`의 `name:*`. 파일 이름은 a-z, 0-9, `_`, `-`(Khronos 가이드 v2.0).
- [ ] **scene_audit 치수 규칙과 맞는 snake_case 영어 키워드**(`coffee_table`, `dining_table`)를 포함.

### 8.4 폴리곤·텍스처 예산

- [ ] **숫자로 정함**("게임레디" 대신): 모바일 소품 1K~5K tris, PC·콘솔 전경 소품 5K~50K tris(Meshy 가이드, 벤더 자체 보고), 웹·AR은 삼각형 10만 이하·파일 5 MB 이하·텍스처 1K~2K·Normal 2K 권장(Khronos 가이드 1.0).
- [ ] **LOD**: LOD1 50%, LOD2 25%. 엔진용 LOD는 `gltfpack -si 0.5 -kn -km -noq -ke`처럼 **양자화 끔(-noq)과 extras 유지(-ke)**를 붙입니다. 기본값은 양자화를 켜고 extras를 버립니다([gltfpack README](https://raw.githubusercontent.com/zeux/meshoptimizer/master/gltf/README.md)).
- [ ] **텍스처는 2의 거듭제곱, BaseColor·Normal 2K 한 세트 + ORM**부터 시작하고 히어로만 올림.
- [ ] **엔진 원본은 압축하지 않음**: meshopt·KTX2 확장은 모든 임포터가 지원하지 않습니다. gltfpack은 Draco를 지원하지 않습니다.

### 8.5 스케일·축·규약

- [ ] **glTF**: 1 unit = 1 m, +Y up, 정면 +Z, 왼쪽 +X([glTF 2.0 스펙](https://raw.githubusercontent.com/KhronosGroup/glTF/main/specification/2.0/Specification.adoc)). Blender(Z-up, 정면 -Y)에서 익스포터가 변환합니다.
- [ ] **노멀 규약**: glTF·Blender·Unity는 OpenGL(green up) + MikkTSpace. UE는 DirectX 규약으로 알려져 있어 Flip Green Channel이 필요할 수 있음(1차 문서 미확인).
- [ ] **Unity**: Meshy 결과처럼 cm로 나온 FBX가 100배로 들어오면 Scale Factor 0.01.
- [ ] **UE Nanite**: 불투명 정적 소품에 켬. 스켈레탈·반투명·모바일 대상의 최신 지원 범위는 (미확인)이라 공식 문서로 확인.
- [ ] **원점 = 바닥 중앙**(Khronos 가이드 v2.0, 이 저장소 규약과 같음).

---

## 9. 라이선스·provenance

### 9.1 `[KR]` 한국에서 쓰면 안 되는 것부터 확인

- [ ] `[필수][KR]` **Tencent Hunyuan3D 계열 오픈웨이트 미사용 또는 법률 검토 완료**: 2.0·2.1·Omni·Part, HY-World, HY-Motion, BPT의 커뮤니티 라이선스는 적용 지역(Territory)에서 **EU·영국·대한민국을 제외**하고, 지역 밖에서의 **출력물 사용도** 허용하지 않습니다([Hunyuan3D 2.1 LICENSE](https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/LICENSE), [BPT License](https://raw.githubusercontent.com/Tencent-Hunyuan/bpt/main/License)). 라이선스 정의에는 가중치뿐 아니라 inference 코드도 포함됩니다. 해외 서버에서 만든 결과물을 한국에서 쓰는 것도 해당합니다.
- [ ] `[KR]` **mcp-for-blender의 Hunyuan3D 연동**은 경로가 둘입니다. 로컬 API(기본 `http://localhost:8081`)는 오픈웨이트를 돌리므로 위 제외 조항이 그대로 적용되고, Tencent Cloud API(SecretId/SecretKey) 경로는 별개 약관을 따르는데 한국 적용 여부는 (미확인)입니다. Cloud 경로를 쓴다면 국제 계정(ap-singapore) 엔드포인트 토글이 필요합니다.
- [ ] `[KR]` **Hunyuan 코드가 섞인 파생 저장소**: Step1X-3D는 README·LICENSE가 Apache-2.0이지만 텍스처 모듈에 Hunyuan 라이선스 헤더가 붙은 코드가 있습니다([mesh_render.py](https://raw.githubusercontent.com/stepfun-ai/Step1X-3D/main/step1x3d_texture/differentiable_renderer/mesh_render.py)). 텍스처 단계를 쓰기 전에 법률 검토.

### 9.2 비상업 전용 확인

- [ ] **연구·비상업 라이선스를 상업 파이프라인에서 뺐는지**: CHORD(Research-Only), PartPacker·LLaMA-Mesh(NVIDIA 비상업), Text2CAD(CC BY-NC-SA 4.0), CAD-Recode(CC BY-NC 4.0), ShapeAssembly(상업 제품 포함 금지), LL3M(비상업 데모 라이선스), MeshAnything(S-Lab 비상업), VLMaterial 데이터(CC BY-NC), MeshRipple(LICENSE 없음 = 권리 유보).
- [ ] **"MIT"라도 의존성 확인**: TRELLIS.2 공식 `to_glb` 텍스처 베이크는 nvdiffrast(NVIDIA Source Code License, 3.3조 비상업)를 쓰고([nvdiffrast LICENSE](https://raw.githubusercontent.com/NVlabs/nvdiffrast/main/LICENSE.txt), 관련 [이슈 #22](https://github.com/microsoft/TRELLIS.2/issues/22) 무응답), 배경 제거에 BRIA RMBG-2.0을 씁니다([#175](https://github.com/microsoft/TRELLIS.2/issues/175)). PartUV의 PartField, Material Anything의 Text2Tex 설정(CC BY-NC-SA 3.0)도 같은 문제입니다.
- [ ] **이미지 생성 단계 가중치**: 예) image-to-3dlab은 Qwen-Image 2.1 가중치를 비상업으로 분류합니다.

### 9.3 에셋 소스

- [ ] `[필수]` **라이선스 화이트리스트**: CC0, CC-BY, CC-BY-SA만 허용하고 NC(비상업)·ND(변경 금지)는 제외. Sketchfab·Objaverse는 모델마다 라이선스가 다릅니다(Objaverse의 Polycam 데이터는 학술 비상업).
- [ ] **CC-BY 표기**: Poly Pizza는 약 69%가 CC-BY라 표기 의무가 있고, mcp-for-blender가 `polypizza_attribution`을 커스텀 프로퍼티로 저장합니다.
- [ ] **Poly Haven**: 에셋은 CC0(표기 불필요)이지만 라이브 API를 앱에서 노출하면 'Powered by Poly Haven' 같은 크레딧이 필요하고, 모든 API 호출에 앱 이름과 일치하는 고유 Referer 또는 User-Agent가 필요합니다([ToS](https://github.com/Poly-Haven/Public-API/blob/master/ToS.md)).
- [ ] **생성 서비스 플랜 기록**: Meshy 무료 플랜 결과물은 CC BY 4.0(Meshy 표기 필요), 유료는 private commercial([Meshy-guide](https://github.com/meshy-dev/Meshy-guide)). 업그레이드 시 소급 여부는 (미확인). Tripo·Rodin 결과물 약관은 (미확인).
- [ ] **Stable Fast 3D**: 본인과 계열사 합산 연매출 100만 달러 미만일 때 무료 상업 이용, 상업 이용 전 등록 필수, 배포 시 'Powered by Stability AI'.
- [ ] **스토어 에셋의 AI 사용 조항**: Fab·Megascans의 NoAI 태그와 라이선스 티어는 원문을 확인하지 못했습니다(신뢰도 낮음). `NoAI` 에셋은 AI 입력으로 쓰지 않습니다.

### 9.4 provenance 기록

- [ ] `[필수]` **에셋마다 기록**: 출처 URL, 저자, 라이선스, 생성 모델·버전·플랜, 파라미터·시드, 입력 이미지 해시, 사람이 한 수정. 형식 예: image-to-3dlab의 `.provenance.json`, mcp-for-blender의 커스텀 프로퍼티(`polyhaven_licence` 등).
- [ ] **GLB까지 따라가는지**: 커스텀 프로퍼티 → glTF extras로 내보내고, gltfpack을 쓰면 `-ke`. 빌드 때 `credits.csv` 자동 생성([에셋 가이드](../02_guides/10_assets_pipeline_licensing.md) 5.4절 코드).
- [ ] **사람의 창작 기여 흔적**: `_gen`(AI 원본) → `_retopo` → `_sculpt` → `_final` 버전 파일과 수정 내용 커밋. 순수 AI 산출물은 저작권 보호가 약하다는 것이 미국 저작권청·한국 안내서의 취지입니다(원문 미열람).
- [ ] **라이선스가 불명확한 에셋은 배포 빌드에서 뺌**.

### 9.5 법규·플랫폼

- [ ] `[KR]` **인공지능기본법 제31조(2026-01-22 시행) 검토**: ① 사전고지(위반 시 과태료 3천만원 이하는 ①항에만), ② 생성형 AI 결과물 표시, ③ 실제와 구분하기 어려운 가상 이미지·영상은 명확히 고지하되 예술적·창의적 표현물은 향유를 저해하지 않는 방식 가능(게임과 관련), ④ 방법·예외는 대통령령. 개발 중 AI로 만든 에셋(사전 생성)에 어떻게 적용되는지는 불분명하므로 법률 검토가 필요합니다. 근거는 제3자 조문 데이터이고 법령 원문은 직접 열람하지 못했습니다([조문 데이터](https://raw.githubusercontent.com/nfa-bigdata/ai-law-clause-search-set5-2026/main/%EC%A1%B0%ED%95%AD%EB%8D%B0%EC%9D%B4%ED%84%B0.json)).
- [ ] **Steam 콘텐츠 설문의 AI 공개**(Pre-Generated·Live-Generated): 최신 문구는 원문 미확인(신뢰도 낮음). 생성 도구·플랜·라이선스 기록을 보관합니다.
- [ ] **모델 출력물 소유**: Anthropic 상업 약관은 출력물을 고객 소유로 두고 권리를 양도합니다([Commercial Terms](https://www.anthropic.com/legal/commercial-terms), 2025-06-17 발효). OpenAI·Google 약관은 이번 조사에서 원문 미확인. 약관상 소유와 제3자 권리 침해 책임은 별개입니다.
- [ ] **유명 디자인·IP 복제 금지**(레퍼런스 이미지 포함).

---

## 10. 에이전트 운영 (저장·보안·비용)

### 10.1 세션 시작

- [ ] **버전 확인**: `bpy.app.version_string`을 출력하고 프롬프트에 명시. 2026-09 기준 안정판 5.2.2(2026-09-14), 4.5 LTS·4.2 LTS 병행. main 브랜치는 5.3 alpha라 5.2 규칙의 근거로 쓰지 않습니다. PyPI `bpy` 5.1+는 Python 3.13 전용, 5.0은 3.11.
- [ ] **Blender MCP 서버는 하나만**: 공식 Blender Lab 서버(Claude 'Blender' 커넥터, 애드온 필요, Blender 5.1.0 이상)와 커뮤니티 ahujasid MCP for Blender(`mcp-for-blender` 2.1.0, `uvx blender-mcp`는 호환 래퍼)는 **둘 다 localhost:9876**을 씁니다. Scenario 플러그인의 로컬 MCP도 9876입니다. 동시에 켜지 않습니다.
- [ ] `[KR]` **UI 언어**: 영어 UI를 쓰거나 Preferences > Interface > Translation에서 'New Data' 번역을 끔(속성 `use_translate_new_dataname`이 5.0.1에 있음은 확인, 실제 번역 동작은 미확인). 오브젝트 이름은 코드에서 영어로 직접 지정.
- [ ] **스킬·규칙 파일 로드**: 프로젝트 규칙(`CLAUDE.md`/`AGENTS.md`)에 단위·이름·금지 목록, 치수 블록([치수표](05_reference_dimensions.md) 10절)이 들어 있음. 템플릿은 [templates/CLAUDE.md](templates/CLAUDE.md).
- [ ] **모델 effort 명시**: Codex의 GPT-6 Astra 기본 reasoning effort는 low, Claude Opus 5.5 기본 effort는 medium입니다. 비평·검증 단계에는 effort를 명시합니다([AI 모델 가이드](../02_guides/01_ai_models_and_clients.md)).

### 10.2 저장·되돌리기

- [ ] `[필수]` **단계마다 `.blend` 증분 저장**: `bpy.ops.wm.save_mainfile(incremental=True)` 또는 `save_as_mainfile(filepath=…, copy=True)`. 둘 다 5.0.1·4.2.23 LTS에서 동작하고 safe mode 검증기를 통과합니다.
- [ ] **`/rewind`를 믿지 않음**: Claude Code 체크포인트는 Claude의 파일 편집 도구로 바꾼 것만 추적하고 외부 프로세스(MCP로 바꾼 Blender 씬)는 추적하지 않습니다([best practices](https://code.claude.com/docs/en/best-practices)).
- [ ] **Unreal**: MCP 편집이 항상 undo되지 않으므로 대량 변경 전후로 저장.
- [ ] **파괴적 작업 금지 목록**: `orphans_purge`, 공장 초기화(`read_factory_settings`), 새 파일 열기, 내가 만들지 않은 오브젝트 수정·삭제. decimate·삭제는 제안 → 전후 비교 → 사용자 선택. hooks로 강제하면 더 안전합니다([에이전트 가이드](../02_guides/09_agent_workflow_prompting.md) 8.4절).

### 10.3 실행 방식

- [ ] **`execute_blender_code`는 작고 멱등적인 청크로**: 호출 하나에 부품 하나 또는 단계 하나, get-or-create, 매번 import 다시, 마지막 줄에 한 줄 요약 print. 호출마다 새 네임스페이스라 Python 변수는 남지 않습니다.
- [ ] **타임아웃 계층**: ahujasid 서버–애드온 소켓 180초, 애드온 `exec()`에는 타임아웃이 없음(무한 루프는 Blender를 멈춤). 1분 넘는 작업(최종 Cycles 렌더·대형 익스포트·베이크)은 `blender -b … --python-exit-code 1`로 헤드리스 실행. Claude Code의 MCP 타임아웃 값은 [에이전트 가이드](../02_guides/09_agent_workflow_prompting.md) 11절.
- [ ] **씬 파악은 요약 스크립트로**: `get_scene_info`는 오브젝트를 최대 10개만, 치수 없이 돌려줍니다. 전체 월드 bbox 요약을 출력하는 스크립트를 쓰고, 대상만 `get_object_info`로 자세히 봅니다.
- [ ] **API가 불확실하면 조회 먼저**: `bpy_api_lookup`, `describe_node_type`(ahujasid), `fake-bpy-module-<버전>` 스텁.
- [ ] **재현 가능한 원본**: 최종 빌드는 `scripts/build_<asset>.py` 같은 파일로 남기고 헤드리스로 다시 돌려 같은 결과가 나오는지 확인.

### 10.4 검증 루프

- [ ] `[필수]` **숫자 먼저**(0.2절 도구) → **눈**(4방향 + 최종 렌더). 숫자가 통과해도 이미지가 틀리면 실패.
- [ ] **한 번에 한 변수만** 바꾸고(조명·재질·카메라·배치 중 하나) 같은 카메라로 다시 렌더해 이전 태그와 나란히 비교.
- [ ] **예/아니오 질문으로 비평**: "잘 됐는지 봐 줘" 대신 요청을 판정할 예/아니오 질문 8~12개를 먼저 만들고 근거와 함께 답하게 한 뒤 "아니오"만 수치가 들어간 수정 지시로 바꿉니다(CADCodeVerify 방식).
- [ ] **만든 쪽이 채점하지 않음**: 읽기 전용 비평가 subagent, Blocker / Major / Minor / Note 분류, SHIP / SHIP WITH NOTES / NO-SHIP 판정([arjun988 qa-review](https://raw.githubusercontent.com/arjun988/blender-skills/main/.claude/skills/qa-review/SKILL.md) 형식).
- [ ] **결함 원장**: 위치·뷰 / 결함 / 증거 / 추정 원인 / 변경 / 검증을 한 줄씩. 가장 큰 결함 하나만 고침. 조명이나 재질로 형태 결함을 가리지 않음.
- [ ] **종료 조건**: 최대 라운드(예: 3) 또는 점수 기준. 같은 문제로 교정이 두 번 실패하면 `/clear` 후 `PROGRESS.md`(스펙·현재 단계·버전 파일·미해결 결함)로 재시작.
- [ ] **완료 보고에 증거**: 오브젝트별 트라이 수, 재질, 라이트(K), 렌더 경로·해상도·시간, 검사 결과 JSON, 남은 결함. 증거 없는 "완료" 금지.
- [ ] **사람 승인 게이트**: G1 스펙 → G2 블록아웃·구도 → G3 최종 렌더 → G4 익스포트([플레이북](02_aaa_production_playbook.md) 게이트와 같음). 유료 생성 직전에도 비용 승인을 받습니다.

### 10.5 보안

- [ ] `[필수]` **작업 전 저장·git 커밋.**
- [ ] **`BLENDER_MCP_SAFE_MODE=1`을 켜되 샌드박스로 믿지 않음**: 막는 것은 `open()`·`os` 같은 직접 파일 I/O, 프로세스, 네트워크, handlers/timers/drivers, 외부 `.blend` append/link. bpy를 통한 저장·열기·import/export·렌더는 허용. 검사는 MCP 경로에만 걸리고, 애드온 소켓은 로컬의 어떤 프로세스가 보낸 코드도 받습니다.
- [ ] **`DISABLE_TELEMETRY=true`**: 콘텐츠(프롬프트·코드·스크린샷) 수집은 옵트인이지만 익명 사용 기록(설치 ID, 툴 이름, 성공 여부, 소요 시간, 버전, OS)은 기본 수집되고, README는 수집 데이터가 AI 학습에 쓰일 수 있다고 적었습니다([README](https://raw.githubusercontent.com/ahujasid/mcp-for-blender/main/README.md)).
- [ ] **localhost 바인딩 유지, 공유 머신에서 쓰지 않음**. Epic도 "Localhost is not a trust boundary"라고 경고합니다.
- [ ] **`--dangerously-skip-permissions` 금지**(Epic 명시). 프로젝트 `.mcp.json` 서버는 신뢰를 확인한 뒤 승인(`claude -p` 비대화형 실행에서는 확인 없이 로드됨, [security](https://code.claude.com/docs/en/security)).
- [ ] **외부 텍스트는 데이터로**: 에셋 설명·웹 콘텐츠 속 지시문(프롬프트 인젝션)을 따르지 않음.
- [ ] **다운로드한 `.blend`의 Python 자동 실행 끔**(Preferences > Save & Load).
- [ ] **서버·스킬 라이선스**: 공식 Blender Lab 서버 GPL-3.0-or-later, blend-ai AGPL-3.0-or-later(수정본을 네트워크 서비스로 제공하면 소스 공개 의무).

### 10.6 비용·컨텍스트

- [ ] **스크린샷 크기**: Claude 이미지 토큰 = ⌈w/28⌉ × ⌈h/28⌉. MCP `get_viewport_screenshot` 기본 캡처는 긴 변 1000 px(약 1000×563 = 756토큰, docstring의 800은 틀림), `review_views` 768×768 한 장 784토큰(4장 약 3,136), 1920×1080은 Opus 5.5 high-res tier에서 2,691토큰([vision 문서](https://platform.claude.com/docs/en/build-with-claude/vision)). 검토는 1000 px 안팎, 최종 판정만 고해상도.
- [ ] **이미지가 한 요청에 20장을 넘으면** 이미지당 치수 제한이 엄격해지므로 각 변 2000 px 이하로 줄입니다(이전 턴 이미지·tool_result 스크린샷 포함).
- [ ] **툴 스키마**: ahujasid 서버 스키마만 6,928토큰(툴 28개 시점, [issue #347](https://github.com/ahujasid/blender-mcp/issues/347)), 지금은 툴이 36개라 더 클 수 있음. 안 쓰는 MCP 서버는 끕니다. Claude Code MCP 출력 한도 `MAX_MCP_OUTPUT_TOKENS` 기본 25,000(10,000 넘으면 경고).
- [ ] **세션 비용 감**: 툴 호출 60회·평균 컨텍스트 80k 가정에서 Sonnet 5 약 $2.5, Opus 5.5 약 $4.0, Fable 5.1 약 $8.7(가정 기반 추정치, 실측 아님). 단가(1M 토큰당 입력/출력) Opus 5.5 $4/$20, Sonnet 5 $2/$10, Fable 5.1 $10/$50([가격 문서](https://platform.claude.com/docs/en/about-claude/pricing)).
- [ ] **유료 생성은 확인 후**: mcp-for-blender의 Tripo 생성은 유료 Premium 전용이고 Hyper3D·Hunyuan3D도 Premium 키 경로가 있습니다. Meshy 크레딧 예: 텍스처링 2K/4K 10, 8K 15, Meshy 7 image-to-3D 메시 20(텍스처 포함 30), remesh 5, UV 5. 호출 전 비용을 보여 주고 승인받습니다.

---

## 11. 단계별 게이트 묶음과 DONE 조건

[AAA 제작 플레이북](02_aaa_production_playbook.md)의 단계(0~11)와 사람 승인 게이트(G1~G4)에 맞춰, 단계마다 이 문서의 어느 절을 돌리면 되는지 정리했습니다.

| 플레이북 단계 | 이 문서의 절 | 통과 조건 요약 |
|---|---|---|
| 시작 전(세션) | 10.1, 10.2, 10.5 | 버전 명시, Blender MCP 서버 하나, 증분 저장 경로, 텔레메트리·safe mode 설정 |
| 0 목표·레퍼런스·스펙 → **G1** | 2.2, 9.1, 9.2 | 부품 스펙 JSON·연결 맵 승인, 라이선스가 걸리는 도구 없음 |
| 1 스케일 블록아웃 | 2.1, 2.2 | 스케일·치수 `[A]` 통과, 인체 더미와 비교 |
| 2 카메라·구도 고정 → **G2** | 6 | 카메라 고정, 렌즈·높이·수직선 |
| 3 라이트 v1 | 5.1, 5.2 | 뷰 변환, 노출, 광원 크기·켈빈 |
| 4 에셋 조달 결정 | 2.6, 9.1~9.4 | 라이선스 화이트리스트, provenance 기록 시작 |
| 5 히어로 모델링 | 2.3~2.7, 1.2 | `check_assembly()` = `[]`, 베벨·노멀·무결성 |
| 6 배치 | 7 | 부유·박힘·관통·천장·방 경계·문·동선 위반 0건, 건물이면 `building_audit` 오류 0건, 4뷰 루브릭 |
| 7 재질·텍스처 | 3, 4 | `pbr_audit` 0건, 색공간, 타일링, UV·베이크 슬롯 전부 |
| 8 라이트 v2 | 5.2, 5.3 | 키 각도, 필 비율, 실내 World 기여, 렌더 설정 |
| 9 디테일·스토리·마모 | 3.4, 7.5, 1.1절 #12 | 원인에 맞는 마모 채널, 스토리 비트 |
| 10 최종 렌더·합성 → **G3** | 5.1, 5.3, 1.1 | `clip_pct` ≤ 0.5%, 12가지 통과, 비평가 SHIP |
| 11 익스포트·검증·provenance → **G4** | 8, 9.4, 9.5 | glTF 검증 종료 코드 0, 슬롯 감사, provenance·크레딧, 사람 SHIP |

**`CLAUDE.md`·`AGENTS.md`나 `/goal`에 붙여 넣는 DONE 블록**(`/goal` 평가자는 대화에 출력된 텍스트만 보므로 결과를 숫자로 출력하게 합니다):

```text
DONE 조건 (모두 텍스트로 출력해 증명할 것):
- scene_audit: summary.units_with_issues == 0 (의도한 벽걸이는 목록으로 명시), interpenetrating_pairs == 0
- 벽 메시가 없으면 방 경계 검사 OUT_OF_ROOM 0건, check_clearances 위반 0건 (주동선 >= 0.9 m, 문 스윙 영역 비움)
- 건물·여러 방이면 building_audit: summary.errors == 0, liminal_risk != "high", no_rooms_found 경고 없음
- quick_checks: ok == False 항목 0건 (roughness_const는 히어로 재질만 해결)
- pbr_audit 위반 0건, 베이크 슬롯 전부 확인
- review_render: clip_pct <= 0.5 (발광체 제외), value_range >= 0.30
- 비평가 판정 SHIP (평균 >= 8, 항목 최저 >= 7)
- export: gltf-transform validate 종료 코드 0, provenance/credits 갱신
- versions/ 에 최신 _v###.blend 저장 로그
- 20턴이 지나면 중단하고 남은 결함 목록을 보고
```

비평가 점수 게이트(평균 8 이상, 항목 7 이상)는 blender-design-master의 설계 값입니다. 그 저장소는 라이선스를 선언하지 않았고 자체 Codex 테스트에서도 Final Gate 평균 7.4로 통과하지 못했으므로, 기준값의 참고로만 씁니다.

---

## 흔한 실수와 해결

| 실수 | 증상 | 해결 |
|---|---|---|
| 뷰포트 스크린샷으로 최종 품질 판정 | 렌더와 색·그림자·DOF가 다름 | `execute_blender_code`나 헤드리스로 렌더를 파일로 저장해서 판정(5.3절) |
| AgX 화면만 보고 노출 OK | 창·하늘 디테일이 날아간 걸 모름 | False Color와 EXR 수치(`clip_pct`)로 판정(5.1절) |
| scene_audit 통과 = 배치 완료로 착각 | 벽 메시 없는 장면에서 방 밖으로 나감, 문·창·방 연결의 비상식, 동선·방향·스토리는 scene_audit가 안 잡음 | `ceiling_z` 지정, 0.5절 방 경계 검사, `building_audit`, 4뷰 렌더 비평 |
| 부모 없이 부품만 흩어 둠 | 좌판이 `floating_or_wall_mounted`로 나옴, 의자 전체 판정 불가 | 부품을 `chair_ROOT` Empty 아래로 묶음 |
| 이름을 한글로 짓거나 종류 단어를 빼먹음 | 치수 규칙이 적용되지 않음(CamelCase는 인식하지만 엔진·파일 규칙과 어긋남) | 영어 snake_case(`coffee_table`), `quick_checks`의 `name:*` 확인 |
| bpy로 만든 라이트를 그대로 둠 | 칼같이 딱딱한 그림자 | 반경·크기 > 0(`quick_checks`) |
| 켈빈을 켜고 색도 칠함 | 의도보다 주황·파랑이 과함 | `use_temperature`면 `color`를 흰색으로 |
| 베이크가 "성공"했다고 믿음 | 일부 재질만 구워지고 나머지는 빈 이미지 | 재질마다 활성 이미지 노드 확인, 결과 이미지를 모두 열어 봄(4.2절) |
| EEVEE 스크린샷으로 마모 조정 | Pointiness·Bevel 마스크가 안 보여 값을 과하게 올림 | Cycles로 확인하고 게임용은 베이크(3.4절) |
| `npx gltf-validator`로 검증 | "could not determine executable" 오류 | `npx @gltf-transform/cli@4.5.0 validate out.glb` |
| gltfpack 기본값으로 엔진용 LOD | 임포터 호환 문제, 라이선스 메타 삭제 | `-noq -ke` 추가 |
| Hunyuan3D 결과물을 한국 프로젝트에 사용 | 라이선스 범위 밖(출력물 포함) | 9.1절, 대안 도구와 법률 검토 |
| `/rewind`로 되돌리려 함 | Blender 씬은 그대로 | 단계별 증분 저장본을 다시 엶(10.2절) |
| 한 번에 여러 변수 수정 | 무엇이 효과를 냈는지 모르고 값이 진동 | 한 변수만, 같은 카메라로 A/B(10.4절) |

## 관련 문서

- [README](../README.md) — 저장소 개요·읽는 순서
- [조사 방법·신뢰도 정책](../01_research/research_method.md)
- [AI 모델·클라이언트](../02_guides/01_ai_models_and_clients.md) — 모델별 effort·비용
- [Blender MCP 생태계](../02_guides/02_blender_mcp.md) — 포트·타임아웃·safe mode
- [AI 3D 생성](../02_guides/04_ai_3d_generation.md) — 생성 메시 후처리·QA 수치
- [텍스처링·재질](../02_guides/05_texturing_materials.md) — `pbr_audit`, 베이크 코드, 슬롯 감사
- [라이팅·렌더·아트디렉션](../02_guides/06_lighting_rendering_art_direction.md) — `review_render()`, 12가지 원인 상세, 규칙 충돌 기본값
- [오브젝트·가구·조형물 모델링](../02_guides/07_modeling_objects_furniture_sculpture.md) — `check_assembly()`, 조립 규칙
- [배치·레이아웃](../02_guides/08_scene_layout_placement.md) — 솔버, 소품 안착, 산포 코드
- [에이전트 워크플로·프롬프팅](../02_guides/09_agent_workflow_prompting.md) — hooks, 비평가 subagent, 타임아웃
- [에셋·파이프라인·라이선스](../02_guides/10_assets_pipeline_licensing.md) — glTF 검증, 네이밍, provenance 코드
- [빠른 시작](01_quickstart_setup.md) — 설치·보안 설정
- [AAA 제작 플레이북](02_aaa_production_playbook.md) — 게이트 순서
- [프롬프트 템플릿](03_prompt_templates.md)
- [실측 치수·간격 기준표](05_reference_dimensions.md) — 한국 프리셋, `KR_SIZE_RULES`
- [보조 스크립트 README](scripts/README.md) — `scene_audit.py`, `placement_utils.py`, `review_views.py`, `building_audit.py`
- [프로젝트 규칙 템플릿](templates/CLAUDE.md) · [스킬 템플릿](templates/skills/blender-aaa-scene/SKILL.md)
- [사례 모음](../04_case_studies/01_case_studies.md) · [한국어 자료](../04_case_studies/02_korean_resources.md)

## 원자료

이 문서의 근거 원자료(`01_research/raw/`, 수정하지 않음). 검증 결과(`*.verify.json`)의 정정·조건을 우선 적용했습니다.

- `07_aaa-rendering-lighting.research.json`, `07_aaa-rendering-lighting.verify.json` — 색관리·노출 게이트, 광원·카메라 규칙, Glare 5.x 범위(구버전 값 반박), UE Lumen(Stationary 반영, 커뮤니티 주장 반박)
- `08_modeling-objects.research.json`, `08_modeling-objects.verify.json` — 스펙 우선, 부품 결합, bevel·메시 검사, FLOATING 단일 레이 오탐 지적, 연구 코드 비상업 라이선스
- `09_scene-layout.research.json`, `09_scene-layout.verify.json` — SceneSmith·SAGE·Infinigen·Holodeck 수치, 루브릭·종료 조건, SAGE 문 차단 영역 정정
- `06_texturing-materials.research.json`, `06_texturing-materials.verify.json` — PBR 값, 색공간, Poly Haven 버그, 베이크 무음 건너뛰기, EEVEE 마스크, Meshy PBR 2K
- `12_assets-pipeline-licensing.research.json`, `12_assets-pipeline-licensing.verify.json` — glTF·Khronos 기준, 네이밍, gltfpack 옵션, Hunyuan·nvdiffrast·Step1X-3D 라이선스, 인공지능기본법 제31조
- `10_agent-workflow.research.json`, `10_agent-workflow.verify.json` — 저장·safe mode·텔레메트리 정정, 스크린샷 기본 1000 px, 이미지 20장 제한, 비용 추정
- 치수 기본값 일부는 [실측 치수표](05_reference_dimensions.md)(G1 보완 조사)를 따랐고, 0.4·0.5절 코드와 1.1절 한 줄 검사는 이 문서를 쓰면서 pip `bpy` 5.0.1·4.2.23 LTS로 실행해 확인했습니다(2026-09-27).
