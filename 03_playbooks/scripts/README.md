# 보조 스크립트 (Blender용, 테스트 완료)

AI가 만든 장면에서 가장 자주 나오는 **형태·배치 오류**(떠 있는 물체, 서로 관통, 스케일 미적용, 비현실적 치수, 방향 오류)를
사람이 눈으로 찾지 않아도 되도록 자동으로 잡아 주는 스크립트입니다.
조사 결과 "숫자 검사를 먼저, 그다음 렌더로 눈 검사"가 가장 안정적인 방식으로 확인됐고(`02_guides/09_agent_workflow_prompting.md` 참고),
그 숫자 검사 부분을 바로 쓸 수 있게 만든 것입니다.

| 파일 | 역할 |
|---|---|
| `scene_audit.py` | 장면 전체 점검 → JSON 리포트 (떠 있음·바닥 아래로 박힘·천장 위로 뚫림·유닛 간 관통·가구–벽/천장 관통·스케일 미적용·음수 스케일·non-manifold·재질/UV 없음·이름 기준 치수 범위 이탈) |
| `placement_utils.py` | 배치 함수: 바닥 붙이기, 아래 표면에 올리기(책상 위 소품), 옆에 붙이기, 벽에 붙이기, 특정 지점 바라보기, 평면 간격 측정·규칙 검사 |
| `review_views.py` | AI 자기비평용 4방향 검토 렌더 (위 정사영 / 정면 / 측면 / 3/4 원근). 오브젝트마다 다른 색으로 칠해 겹침·간격이 잘 보이게 함 |
| `tests/test_scripts.py` | 자동 테스트 |

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
blender -b scene.blend --python 03_playbooks/scripts/scene_audit.py -- --floor-z 0 --ceiling-z 2.3 --out audit.json
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
# units[*].size_wdh_m = [폭, 깊이, 높이], units[*].size_rule = 적용된 규칙 이름
```

> `placement_utils`의 함수들은 시작할 때 `view_layer.update()`를 호출하므로, 직전에 `obj.location`을 바꿨어도 새 위치 기준으로 계산합니다. 직접 `matrix_world`를 읽는 코드를 쓸 때는 먼저 `bpy.context.view_layer.update()`를 부르세요.

## 테스트 실행

```bash
python -m venv bpyenv && bpyenv/bin/pip install bpy==5.0.1     # 또는 "bpy==4.2.*"
bpyenv/bin/python 03_playbooks/scripts/tests/test_scripts.py
```

테스트 내용
- 떠 있는 의자·상판을 관통한 상자·깊이 2.5 m 소파·스케일 미적용 오브젝트를 모두 잡아내는지, 테이블 아래로 넣은 의자(바운딩박스만 겹침)를 관통으로 **오탐하지 않는지**
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
