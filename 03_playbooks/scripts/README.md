# 보조 스크립트 (Blender용, 테스트 완료)

AI가 만든 장면에서 가장 자주 나오는 **형태·배치 오류**(떠 있는 물체, 서로 관통, 스케일 미적용, 비현실적 치수, 방향 오류)를
사람이 눈으로 찾지 않아도 되도록 자동으로 잡아 주는 스크립트입니다.
조사 결과 "숫자 검사를 먼저, 그다음 렌더로 눈 검사"가 가장 안정적인 방식으로 확인됐고(`02_guides/09_agent_workflow_prompting.md` 참고),
그 숫자 검사 부분을 바로 쓸 수 있게 만든 것입니다.

| 파일 | 역할 |
|---|---|
| `scene_audit.py` | 장면 전체 점검 → JSON 리포트 (떠 있음·바닥 아래로 박힘·다른 물체 속으로 파고듦(`sunk_into`)·천장 위로 뚫림·유닛 간 관통·가구–벽/천장 관통·스케일 미적용·음수 스케일·non-manifold·재질/UV 없음·이름 기준 치수 범위 이탈) |
| `placement_utils.py` | 배치 함수: 바닥 붙이기, 아래 표면에 올리기(책상 위 소품), 옆에 붙이기, 벽에 붙이기, 특정 지점 바라보기, 평면 간격 측정·규칙 검사 |
| `review_views.py` | AI 자기비평용 4방향 검토 렌더 (위 정사영 / 정면 / 측면 / 3/4 원근). 오브젝트마다 다른 색으로 칠해 겹침·간격이 잘 보이게 함 |
| `building_audit.py` | **건축 상식 검사** — "사람이 설계한 건물처럼 말이 되는가". 문(벽에 안 뚫림·뜸·열면 벽·허공/낭떠러지·막힘·좁음), 창(어정쩡한 창턱·높이 제각각·실내 창·창 앞 벽·가구가 가림), 방(밀폐·갈 수 없음·창 없는 생활 공간·복도처럼 길쭉함·천장 이상·빈 방·똑같은 빈 방 반복·벽이 빠진 가장자리), 벽(천장까지 안 닿아 뚫려 보임·끝 틈), 계단(단 높이 불균일·어디로도 안 감), 벽을 보고 앉는 의자 + **백룸 위험도**. **실제 AI 생성 건물 9개 장면으로 검증**([`validation/`](validation/README.md)) |
| `tests/test_scripts.py`, `tests/test_building_audit.py`, `tests/test_building_realworld.py` | 자동 테스트 (마지막 것은 실제 AI 장면에서 오탐이 났던 구조·문 여는 방향 등 15가지) |
| `validation/` | 실제 AI 건물 검증 기록·원자료(JSON)·재현 도구 |

**검증**: Blender **4.2.23 LTS**와 **5.0.1**(pip `bpy` 모듈, 헤드리스)에서 모든 테스트 통과. 5.x에서 폐기 예정인 `use_nodes` 경고가 나지 않게 했고, 한국어 UI에서 노드 이름이 번역되어도 동작하도록 노드를 이름이 아니라 타입으로 찾습니다.

## 규약 (스크립트가 가정하는 것)

- 1 Blender unit = 1 m, Z-up
- **"유닛" = 최상위 부모 기준 묶음.** 의자 부품(좌판·등받이·다리)은 하나의 부모(Empty 등) 아래 자식으로 두세요. 그래야 의자 전체를 하나로 보고 판정합니다. 부모 없이 부품만 흩어져 있으면 좌판이 "떠 있음"으로 나옵니다.
- 가구의 앞면은 **-Y** 방향 (Blender Front 뷰에서 보이는 면). `face_towards()`가 이 규약을 씁니다.
- **이름은 영어 snake_case로, 종류 단어를 넣어서** 짓습니다(예: `dining_table_01`, `SM_Armchair_A`). 치수 검사는 이름의 단어(`chair`, `table`, `sofa`, `bed`, `door` …)로 규칙을 고릅니다. CamelCase도 인식하고, `door_handle`·`table_lamp`처럼 부속품 단어가 뒤에 붙으면 규칙을 적용하지 않습니다. 한국어 이름은 인식하지 않습니다.
- **구조물 판정은 이름의 마지막 핵심 단어로** 합니다. `Floor`, `Wall_N`, `floor_plane`, `north_wall`, `Ceiling_01` → 구조물 / `wall_shelf`, `floor_lamp` → 가구. 구조물은 받침면으로만 쓰이고 떠 있음·치수 검사에서 빠집니다. 가구가 벽·천장을 뚫고 들어간 경우는 관통으로 잡습니다(구조물끼리는 검사하지 않음). 그러니 가구 이름을 `..._wall`로 끝내지 마세요.
- 치수는 **가구 자체 방향 기준**(루트의 Z 회전을 되돌려서)으로 폭 `w`(수평 긴 변)·깊이 `d`(수평 짧은 변)·높이 `z`를 잽니다. 90°나 임의 각도로 돌린 가구도 오탐하지 않습니다.

## 사용법 1 — Blender MCP(실행 중인 Blender)에서

`execute_blender_code`는 호출마다 새 네임스페이스에서 실행됩니다. 두 가지 방법이 있습니다.

**(a) 경로를 추가하고 import (권장)**

```python
import sys
sys.path.append(r"C:\path\to\3D-MCP\03_playbooks\scripts")   # 이 저장소를 받은 위치
import importlib, scene_audit, placement_utils as pu
importlib.reload(scene_audit); importlib.reload(pu)

report = scene_audit.audit_scene(floor_z=0.0)
print(report["summary"])
for u in report["units"]:
    if u["issues"]:
        print(u["name"], u["issues"])
print(report["interpenetrations"])
```

**(b) 파일 내용을 그대로 붙여 넣기**: `scene_audit.py` 전체를 붙여 넣으면 끝에서 자동으로 점검을 실행하고 JSON을 출력합니다.

> ahujasid MCP for Blender의 `BLENDER_MCP_SAFE_MODE=1`은 `open()`·`os` 같은 **직접** 파일 I/O, 프로세스 실행, 네트워크를 막습니다. bpy를 통한 저장·렌더·import/export는 허용됩니다(교차검증 결과, `02_guides/02_blender_mcp.md` 보안 절 참고). 다만 `sys.path`를 바꿔 이 저장소 모듈을 import하는 방식이 허용되는지는 **미확인**이고, `review_views.py`는 `os.makedirs`를 쓰므로 safe mode 사전 검사에 걸릴 수 있습니다. 막히면 (b) 붙여 넣기 방식이나 헤드리스(사용법 2)를 쓰세요.

## 사용법 2 — 헤드리스 (Claude Code / Codex가 스크립트로 빌드하는 방식)

```bash
blender -b scene.blend --python 03_playbooks/scripts/scene_audit.py -- --floor-z 0 --ceiling-z 2.3 --collection Room --out audit.json
```

```python
# build.py 안에서
import sys; sys.path.append("03_playbooks/scripts")
from review_views import render_review_views
paths = render_review_views("review/", engine="CYCLES", samples=16, res=768)
# → review/top.png, front.png, side.png, persp.png 를 AI에게 보여 주고 비평시킨다
```

- GPU가 없는 서버에서는 `engine="CYCLES"`(CPU)만 동작합니다. EEVEE·Workbench는 GPU/EGL이 필요합니다.
- 출력 폴더는 `"//review/"`처럼 .blend 파일 기준 상대 경로로 줘도 됩니다(내부에서 `bpy.path.abspath`로 변환).
- Blender GUI(MCP 연결)에서는 `engine="BLENDER_WORKBENCH"`가 가장 빠릅니다(오브젝트별 랜덤 색 + 외곽선).

## 건축 상식 검사 — `building_audit.py`

`scene_audit.py`가 물리 오류(떠 있음·관통·치수)를 잡는다면, 이 스크립트는 **백룸(Backrooms)처럼 기묘한 결과**를 만드는 건축적 비상식을 잡습니다. 특정 국가 법규가 아니라 넓게 잡은 "상식 범위"입니다(임계값은 `LIMITS`에서 조정).

```python
import sys; sys.path.append(r"...\3D-MCP\03_playbooks\scripts")
import building_audit
rep = building_audit.audit_building(collection="House")     # collection 생략 시 장면 전체
print(rep["summary"])            # errors, warnings, liminal_risk(low/medium/high), liminal_reasons
for i in rep["issues"]:
    print(i["severity"], i["code"], i["object"], i["detail"])
```

**역할 인식**(에이전트에게 이렇게 짓게 하세요. `obj["role"]`, `obj["room_type"]` 커스텀 프로퍼티가 있으면 그것이 우선)
- 방 바닥 `Floor_<방종류>[_번호]`(예: `Floor_living`, `Floor_bedroom_2`, `Floor_hall`, `Floor_bathroom`) — 방 종류로 창 필요 여부·복도 여부를 판단합니다. 1 m² 미만 바닥 조각은 소품으로 봅니다.
- 외부 지면 `Ground`(없으면 모델 바깥을 '모델링되지 않은 외부'로 봄), 벽 `Wall_...`(`LINTEL_`·`HEADER_`도 벽), 천장 `Ceiling...`, 지붕 `..._roof`, 문 `Door_...`, 창 `Window_...`, 난간 `railing`, 마감재 `FRAME_`·`SKIRT_`·`COVE_`·`..._trim`
- **한국어·중국어 이름도 됩니다.** 끝 단어로 판정: `거실_바닥`·`현관문`·`거실_창문`·`외벽_남`, `主卧 · 地坪`·`开启木门`·`玻璃窗`. `창가_소파`(소파)·`双门冰箱`(냉장고)처럼 수식어로 쓰인 단어는 역할로 보지 않습니다.
- 이름으로 못 정하면 컬렉션 이름(`.../Walls`, `.../Floors`, `..._Ceiling_Grid`)을 참고합니다. 이름도 속성도 없으면(Plane, Cube) `no_rooms_found` 경고 — "오류 0"이 통과를 뜻하지 않게 했습니다.
- 계단은 이름에 `stair(s)`가 들어간 부모 아래 단을 자식 메시로(`stairs_main_step_0` …).
- 문·창 구멍은 **벽에 실제로 뚫려 있어야** 합니다(Boolean이든 벽을 나눠 만들든). 구멍이 없으면 `opening_not_cut`이고 방 연결로 치지 않습니다.

**가져온 장면·합친 메시도 됩니다**(실제 AI 장면에서 확인한 구조)
- glTF/three.js에서 가져와 `house/floors/openings`처럼 그룹 아래 들어 있는 장면 → 방 규모 그룹은 풀어서 검사
- 벽 전체가 메시 하나 → 떨어진 조각별로 나누고, 문·창 자리의 벽 방향·두께는 문·창과 주변 벽면에서 직접 잼(이때 벽 단위 두께·끝 틈 검사는 생략하고 `notes`에 표시)
- 여러 창이 오브젝트 하나 → 가까운 조각끼리 묶어 창별로 나눔. 커튼이 창에 포함돼 있어도 창턱은 **실제 구멍** 높이로 잼
- 90° 열린 문짝, 구멍 옆에 겹쳐 둔 미닫이 문짝, 문짝 없는 출입구·아치, 베이창(飘窗), 발코니 유리문(채광으로 셈), 오픈 셀 격자 천장

**판정 단계**: 문 앞 0.6 m 통로가 폭 0.45 m도 안 남으면 `door_blocked`(오류), 0.45~0.6 m면 `door_narrow`(경고). 창은 가구가 **창 면적의 25% 이상**을 가릴 때만 `window_blocked`.

**문 여는 방향 — 설계 상식으로 정하고 검사합니다.** 여닫이문마다 경첩 위치(양쪽 문설주) × 여는 쪽(양쪽 방) 4가지를 실제로 돌려 보고(문짝을 10°씩 열며 5개 높이로 레이), 아래 순서로 가장 합당한 것을 `openings[i]["swing"]["recommended"]`에 넣습니다.
1. 80° 이상 열릴 때까지 가구·벽·다른 문·계단에 안 부딪힐 것 (필수)
2. 방 문은 복도·거실이 아니라 **그 방 안쪽으로**(욕실·수납 > 침실·서재 > 거실·주방 > 복도). 같은 급이면 작은 방 쪽
3. 좁은 욕실(4.5 m² 미만)은 안쪽으로 90°까지 다 안 열리면(변기·세면대) **바깥여닫이**
4. 경첩은 **벽 모서리 쪽**(열면 문짝이 옆벽에 붙음)
5. 두 문이 열리며 서로 부딪히면 다른 조합을 찾음. 동점이면 열린 문짝이 같은 방의 다른 문 앞을 가리지 않는 쪽
6. 현관은 지역 관례를 설정으로: `limits={"entry_swing": "out"}`(한국·일본 아파트는 보통 바깥여닫이) / `"in"` / `"any"`(기본)
7. 폭 1.1 m 초과는 양개문, 이름에 sliding·pocket·미닫이·移门이 있거나 넓은 유리문·2 m 초과는 미닫이로 보고 궤적 검사를 하지 않음

모델에 문짝이 이미 (살짝) 열려 있으면 그 방향을 읽어 **설계자의 선택을 존중**하고 검사만 합니다. 결과: 어느 쪽으로도 못 열면 `door_swing_blocked`, 모델에 열어 둔 방향이 부딪히면 `door_swing_conflict`(대신 열 방향 제시), 두 문이 어떻게 해도 부딪히면 `door_swing_collide`. 추천 이유는 `swing["why"]`에 한국어로 적힙니다.

```python
rep = building_audit.audit_building(limits={"entry_swing": "out"})
for op in rep["openings"]:
    if op["kind"] == "door" and op["swing"]["recommended"]:
        print(op["name"], "→", op["swing"]["recommended"]["opens_into"], "|", op["swing"]["why"])
# 추천대로 문짝을 연다 (닫힌 문짝 오브젝트, 양개문은 문짝마다)
leaf = rep["openings"][0]["swing"]["recommended"]["leaves"][0]
building_audit.open_door(bpy.data.objects["Door_bedroom"], leaf, angle_deg=85)
# 평면도 검토: 문 여는 궤적(1/4 원)을 바닥에 그림 — 초록 = 추천, 빨강 = 모델에 열어 둔 방향이 부딪힘
building_audit.add_swing_symbols(rep)   # 컬렉션 "_door_swings", 확인 후 지우세요
```

**검사 근거**: 문 앞 비움 구역 = 문 폭 × 문 폭(NVlabs SAGE 배치 솔버), 문은 방과 방·외부를 잇고 창은 외벽에(Holodeck·Infinigen Indoors), 모든 방에 동선으로 갈 수 있어야 함(SceneSmith Reachability). 나머지 범위(창턱 0.03~0.25 m는 어정쩡함, 천장 2.1~4.5 m, 2×단높이+단너비 0.55~0.70 m 등)는 상식 기준입니다.

**테스트**
- `test_building_audit.py`: 정상적인 집은 오류·경고 0건, 일부러 이상하게 만든 집(구멍 안 뚫린 현관, 30 cm 뜬 문, 열면 벽인 문, 3 m 낭떠러지 문, 창턱 10 cm 창, 방↔방 실내 창, 가구가 가린 창, 문 없는 방, 12×2 m 빈 방, 똑같은 빈 방 3개, 천장까지 안 닿는 벽, 10 cm 벽 틈, 단 높이 제각각인 계단, 벽을 보고 앉은 소파)은 전부 잡고 백룸 위험도 `high`
- `test_building_realworld.py`: 실제 AI 장면에서 오탐이 났던 구조(합친 벽+그룹, 옆벽에 붙은 열린 문, 주차된 미닫이, 커튼·베이창, 발코니 유리문, 한·중 이름, 'Wall'이라는 가구 부품, 격자 천장, 계단식 벽)는 안 잡고, 반쯤 막힌 문·완전히 막힌 문·옷장에 가린 창·구멍 없는 문·아무것도 못 알아본 장면은 잡음. 문 여는 방향: 방 안쪽·모서리 경첩 추천, 막히면 반대쪽, 양쪽 다 막히면 경고, 모델에 열어 둔 문이 옷장에 부딪힘, 현관 지역 관례, 미닫이, 욕실 모서리 두 문이 서로 부딪히지 않게 조정
- **실제 AI 건물 9개**(Realsee × GPT-6 Astra 1, house-3d Fable 판 4, GPT-6 판 4): v1은 오류 18건(대부분 오탐) 또는 "아무것도 못 알아보고 오류 0"이었고, 최종은 백룸 오경보 0건, 남은 지적은 모두 좌표·렌더·원본 데이터로 확인한 실제 문제 → [검증 기록](validation/README.md)

**못 잡는 것**: 합친 벽의 벽 단위 두께·틈, 곡선 벽의 정밀 판정, 미감(재질·조명·비례의 아름다움). 이건 4방향 렌더 비평과 사람 눈으로 봐야 합니다. 큰 장면(오브젝트 1,000개)은 1~2분 걸립니다.

## 배치 함수 예시

```python
import placement_utils as pu
import bpy
O = bpy.data.objects

pu.snap_to_floor(O["Sofa"], 0.0)                       # 바닥에 붙이기
pu.place_against_wall(O["Sofa"], wall_y=2.5, gap=0.05)  # +Y 쪽 벽(안쪽 면 y=2.5)에 등 붙이기
pu.place_next_to(O["SideTable"], O["Sofa"], side="+X", gap=0.05)
pu.drop_to_surface(O["Lamp"])                           # 아래에 있는 가장 높은 표면(사이드테이블) 위로
pu.face_towards(O["Armchair"], O["CoffeeTable"].location)

# 동선·간격 규칙 검사: (A, B, 최소 m, 최대 m)
print(pu.check_clearances([
    ("Sofa", "CoffeeTable", 0.35, 0.50),   # 소파–커피테이블 간격
    ("DiningTable", "Wall_N", 0.90, None),  # 식탁 의자 빼는 공간
]))
```

간격·치수 기준값은 `03_playbooks/05_reference_dimensions.md`를 참고하세요. `scene_audit.py`의 `DEFAULT_SIZE_RULES`는 한국·미국·유럽 값을 모두 포함하도록 넓게 잡은 "명백한 오류" 탐지용 범위입니다(식탁·커피테이블·콘솔·바 테이블·협탁·책상·바/카운터 스툴·암체어·의자·소파·침대·옷장·책장·문·주방 상판 등). 프로젝트에 맞게 바꾸려면 `audit_scene(size_rules={"armchair": {...}, **DEFAULT_SIZE_RULES})`처럼 넘기세요.

```python
# 한국 구축 아파트(천장 2.3 m) 기준 점검 예
report = scene_audit.audit_scene(floor_z=0.0, ceiling_z=2.30)

# 방 내부와 건물 외관을 한 장면에 둘 때: 컬렉션별로 따로 검사 (천장 규칙은 방에만)
room_rep = scene_audit.audit_scene(floor_z=0.0, ceiling_z=2.30, collection="Room")
bldg_rep = scene_audit.audit_scene(floor_z=0.0, collection="Building")
# units[*].size_wdh_m = [폭, 깊이, 높이], units[*].size_rule = 적용된 규칙 이름
```

> `placement_utils`의 함수들은 시작할 때 `view_layer.update()`를 호출하므로, 직전에 `obj.location`을 바꿨어도 새 위치 기준으로 계산합니다. 직접 `matrix_world`를 읽는 코드를 쓸 때는 먼저 `bpy.context.view_layer.update()`를 부르세요.

## 테스트 실행

```bash
python -m venv bpyenv && bpyenv/bin/pip install bpy==5.0.1     # 또는 "bpy==4.2.*"
bpyenv/bin/python 03_playbooks/scripts/tests/test_scripts.py
bpyenv/bin/python 03_playbooks/scripts/tests/test_building_audit.py
bpyenv/bin/python 03_playbooks/scripts/tests/test_building_realworld.py
```

테스트 내용
- 떠 있는 의자·상판을 관통한 상자·깊이 2.5 m 소파·스케일 미적용 오브젝트를 모두 잡아내는지, 테이블 아래로 넣은 의자(바운딩박스만 겹침)를 관통으로 **오탐하지 않는지**
- 박힘 판정: 바닥에 5 cm 박힌 암체어, 슬래브에 7.5 cm 박힌 계단을 "떠 있음"이 아니라 `sunk_into`로 보고. 컬렉션 범위 검사(방 천장 규칙이 건물 기둥에 적용되지 않음), 기둥 위 15 cm 뜬 지붕 슬래브 검출
- 이름 매칭(CamelCase, `door_handle`·`table_lamp`·`turntable`·`indoor_plant` 제외, 암체어가 의자 규칙에 걸리지 않음), 구조물 판정(`Wall_N` vs `wall_shelf`)
- 90°·30° 회전한 소파의 폭·깊이 오탐 없음, 천장(2.30 m)을 뚫은 옷장, 벽 속으로 박힌 수납장 검출, 벽–바닥은 검사하지 않음
- 바닥 붙이기·표면 위 올리기(이미 표면 위일 때 다시 호출해도 뚫고 내려가지 않음)·옆 배치·벽에 붙이기·방향 맞추기·간격 검사
- 검토 렌더 4장 생성(절대 경로와 `//review/` 상대 경로), 끝난 뒤 임시 카메라/조명/월드/재질이 남지 않는지

## 한계

- 떠 있음 판정은 "바닥면 근처 5개 지점에서 아래로 레이를 쏴서 받침면이 있는가"입니다. 벽걸이·천장등·선반 위 액자처럼 의도적으로 떠 있는 물체도 `floating_or_wall_mounted`로 표시되니, 의도한 것인지 확인하세요.
- 관통 판정은 삼각형 교차 기반입니다. 한 물체가 다른 물체 안에 **완전히** 들어가 면이 교차하지 않는 경우는 잡지 못합니다(바운딩박스 겹침 깊이로 보조 판단).
- 치수 범위 검사는 이름 키워드(`chair`, `table`, `sofa`, `bed`, `door` …)로 동작합니다. 이름을 영어로 짓는 규칙을 에이전트에게 주세요(`templates/CLAUDE.md` 참고).
- **검사하지 않는 것**: 뒤집힌 노멀, 한 유닛 **내부** 부품끼리의 관통·틈(의자 다리와 좌판 사이 등 — 이건 `02_guides/07_modeling_objects_furniture_sculpture.md`의 조립 연결 맵 검사 참고), 방 경계(벽 없이 바닥만 있을 때 바닥 밖으로 나감).
- 만드는 도중(유닛이 반쯤 조립된 상태)에는 떠 있음·치수 경고가 나오는 게 정상입니다. 합격/불합격은 유닛이 완성된 뒤에 판단하세요.
