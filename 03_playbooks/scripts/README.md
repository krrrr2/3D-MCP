# 보조 스크립트 (Blender용, 테스트 완료)

AI가 만든 장면에서 가장 자주 나오는 **형태·배치 오류**(떠 있는 물체, 서로 관통, 스케일 미적용, 비현실적 치수, 방향 오류)를
사람이 눈으로 찾지 않아도 되도록 자동으로 잡아 주는 스크립트입니다.
조사 결과 "숫자 검사를 먼저, 그다음 렌더로 눈 검사"가 가장 안정적인 방식으로 확인됐고(`02_guides/09_agent_workflow_prompting.md` 참고),
그 숫자 검사 부분을 바로 쓸 수 있게 만든 것입니다.

| 파일 | 역할 |
|---|---|
| `scene_audit.py` | 장면 전체 점검 → JSON 리포트 (떠 있음·바닥 관통·유닛 간 관통·스케일 미적용·음수 스케일·non-manifold·재질/UV 없음·이름 기준 치수 범위 이탈) |
| `placement_utils.py` | 배치 함수: 바닥 붙이기, 아래 표면에 올리기(책상 위 소품), 옆에 붙이기, 벽에 붙이기, 특정 지점 바라보기, 평면 간격 측정·규칙 검사 |
| `review_views.py` | AI 자기비평용 4방향 검토 렌더 (위 정사영 / 정면 / 측면 / 3/4 원근). 오브젝트마다 다른 색으로 칠해 겹침·간격이 잘 보이게 함 |
| `tests/test_scripts.py` | 자동 테스트 |

**검증**: Blender **4.2.23 LTS**와 **5.0.1**(pip `bpy` 모듈, 헤드리스)에서 모든 테스트 통과. 5.x에서 폐기 예정인 `use_nodes` 경고가 나지 않게 했고, 한국어 UI에서 노드 이름이 번역되어도 동작하도록 노드를 이름이 아니라 타입으로 찾습니다.

## 규약 (스크립트가 가정하는 것)

- 1 Blender unit = 1 m, Z-up
- **"유닛" = 최상위 부모 기준 묶음.** 의자 부품(좌판·등받이·다리)은 하나의 부모(Empty 등) 아래 자식으로 두세요. 그래야 의자 전체를 하나로 보고 판정합니다. 부모 없이 부품만 흩어져 있으면 좌판이 "떠 있음"으로 나옵니다.
- 가구의 앞면은 **-Y** 방향 (Blender Front 뷰에서 보이는 면). `face_towards()`가 이 규약을 씁니다.
- 이름에 `floor`, `ground`, `wall`, `ceiling`이 들어간 유닛은 구조물로 보고 떠 있음·관통 검사에서 뺍니다(받침면으로는 사용).

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

> ahujasid MCP for Blender의 `BLENDER_MCP_SAFE_MODE=1`은 파일 I/O를 막으므로 (a)의 import나 렌더 저장이 막힐 수 있습니다. 그 경우 (b)를 쓰거나, 신뢰하는 로컬 작업에서만 safe mode를 끄세요.

## 사용법 2 — 헤드리스 (Claude Code / Codex가 스크립트로 빌드하는 방식)

```bash
blender -b scene.blend --python 03_playbooks/scripts/scene_audit.py -- --floor-z 0 --out audit.json
```

```python
# build.py 안에서
import sys; sys.path.append("03_playbooks/scripts")
from review_views import render_review_views
paths = render_review_views("review/", engine="CYCLES", samples=16, res=768)
# → review/top.png, front.png, side.png, persp.png 를 AI에게 보여 주고 비평시킨다
```

- GPU가 없는 서버에서는 `engine="CYCLES"`(CPU)만 동작합니다. EEVEE·Workbench는 GPU/EGL이 필요합니다.
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

간격·치수 기준값은 `03_playbooks/05_reference_dimensions.md`를 참고하세요. `scene_audit.py`의 `DEFAULT_SIZE_RULES`는 "명백한 오류"만 잡도록 넓게 잡은 범위이며, 필요하면 `audit_scene(size_rules={...})`로 바꿔 넣을 수 있습니다.

## 테스트 실행

```bash
python -m venv bpyenv && bpyenv/bin/pip install bpy==5.0.1     # 또는 "bpy==4.2.*"
bpyenv/bin/python 03_playbooks/scripts/tests/test_scripts.py
```

테스트 내용: 떠 있는 의자·상판을 관통한 상자·깊이 2.5 m 소파·스케일 미적용 오브젝트를 만들어 모두 잡아내는지, 테이블 아래로 넣은 의자(바운딩박스만 겹침)를 관통으로 **오탐하지 않는지**,
바닥 붙이기·표면 위 올리기(이미 표면 위일 때 다시 호출해도 뚫고 내려가지 않음)·옆 배치·방향 맞추기·간격 검사, 검토 렌더 4장 생성 후 임시 카메라/조명/월드/재질이 남지 않는지.

## 한계

- 떠 있음 판정은 "바닥면 근처 5개 지점에서 아래로 레이를 쏴서 받침면이 있는가"입니다. 벽걸이·천장등·선반 위 액자처럼 의도적으로 떠 있는 물체도 `floating_or_wall_mounted`로 표시되니, 의도한 것인지 확인하세요.
- 관통 판정은 삼각형 교차 기반입니다. 한 물체가 다른 물체 안에 **완전히** 들어가 면이 교차하지 않는 경우는 잡지 못합니다(바운딩박스 겹침 깊이로 보조 판단).
- 치수 범위 검사는 이름 키워드(`chair`, `table`, `sofa`, `bed`, `door` …)로 동작합니다. 이름을 영어로 짓는 규칙을 에이전트에게 주세요(`templates/CLAUDE.md` 참고).
