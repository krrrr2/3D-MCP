"""
scene_audit.py - AI가 만든 Blender 장면의 형태/배치 오류를 자동 점검하는 스크립트.

검사 항목
  - 오브젝트(부모 기준으로 묶은 "유닛")별 실제 치수(m), 위치, 바닥 높이
  - 떠 있음(floating): 아래에 받쳐주는 면이 없음 (벽걸이/천장 조명이면 정상일 수 있음)
  - 바닥 아래로 박힘(below_floor), 다른 물체 속으로 파고듦(sunk_into: 슬래브에 박힌 계단, 바닥에 박힌 다리 등)
  - 서로 관통(interpenetration): 바운딩박스가 겹치고 실제 면끼리 교차
  - 스케일 미적용 / 음수 스케일
  - Non-manifold 엣지, 재질 없음, UV 없음
  - 이름 키워드(chair, table, sofa ...) 기준 치수 범위 벗어남 (가구 자체 방향 기준 폭 w·깊이 d·높이 z 로 비교)
  - (선택) 천장 위로 뚫고 나감(above_ceiling), 벽·천장 등 구조물과의 관통

사용법
  1) blender-mcp 의 execute_blender_code 에 파일 전체를 붙여 넣으면 결과 JSON 이 출력됩니다.
  2) 헤드리스: blender -b scene.blend --python scene_audit.py -- --floor-z 0 --out report.json
  3) 모듈: from scene_audit import audit_scene; report = audit_scene(floor_z=0.0)

Blender 4.2 LTS 이상 / 5.x 에서 동작하도록 작성했습니다 (bpy 4.2.23 LTS, 5.0.1 로 테스트).
"""

import json
import math
import re
import sys

import bmesh
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

# 이름에 키워드가 들어간 유닛의 치수 허용 범위 (미터, [min, max]).
#   w = 수평 긴 변, d = 수평 짧은 변 (가구 자체 방향 기준이라 90° 돌려도 같은 값), z = 높이
# 근거: 03_playbooks/05_reference_dimensions.md (한국·미국·유럽 값을 모두 포함하도록 넓게 잡은 "명백한 오류" 탐지용 범위)
DEFAULT_SIZE_RULES = {
    "dining_table": {"z": [0.68, 0.80]},
    "coffee_table": {"z": [0.30, 0.55]},
    "console_table": {"z": [0.70, 0.95]},
    "bar_table": {"z": [0.95, 1.12]},
    "bedside_table": {"z": [0.40, 0.80]},
    "nightstand": {"z": [0.40, 0.80]},
    "desk": {"z": [0.68, 0.80]},
    "table": {"z": [0.35, 0.80]},
    "bar_stool": {"z": [0.68, 1.30]},
    "counter_stool": {"z": [0.50, 1.20]},
    "stool": {"z": [0.40, 0.85]},
    "armchair": {"z": [0.60, 1.10], "w": [0.60, 1.10], "d": [0.60, 1.10]},
    "chair": {"z": [0.70, 1.20], "w": [0.35, 0.80], "d": [0.35, 0.80]},
    "sofa": {"z": [0.60, 1.10], "w": [1.20, 3.50], "d": [0.70, 1.20]},
    "bed": {"z": [0.30, 1.40], "w": [1.85, 2.45], "d": [0.80, 2.30]},
    "wardrobe": {"z": [1.60, 2.45], "d": [0.33, 0.70]},
    "bookshelf": {"z": [0.70, 2.40], "d": [0.20, 0.45]},
    "bookcase": {"z": [0.70, 2.40], "d": [0.20, 0.45]},
    "double_door": {"z": [1.95, 2.50]},
    "door": {"z": [1.80, 2.50], "w": [0.60, 1.20]},
    "bar_counter": {"z": [0.98, 1.10]},
    "counter": {"z": [0.84, 0.96]},
}

# 키워드 바로 뒤에 이 단어가 오면 "그 가구의 부속품/다른 물건"으로 보고 규칙을 적용하지 않는다.
# 예: door_handle, table_lamp, chair_cushion, desk_lamp
ACCESSORY_TOKENS = {
    "handle", "knob", "lamp", "light", "plant", "cushion", "pillow", "cover", "rug", "mat",
    "leg", "legs", "top", "seat", "back", "backrest", "arm", "frame", "panel", "part", "decor",
    "cloth", "runner", "vase", "clock", "sign", "stopper", "hinge", "lock",
}

def _mesh_objects_under(root):
    objs = [root] + list(root.children_recursive)
    return [o for o in objs if o.type == "MESH" and o.visible_get()]


def _world_verts_and_polys(obj, depsgraph):
    """모디파이어가 적용된(평가된) 메시를 월드 좌표 정점/폴리곤으로 반환."""
    ob_eval = obj.evaluated_get(depsgraph)
    mesh = ob_eval.to_mesh()
    try:
        mw = ob_eval.matrix_world
        verts = [mw @ v.co for v in mesh.vertices]
        polys = [tuple(p.vertices) for p in mesh.polygons]
    finally:
        ob_eval.to_mesh_clear()
    return verts, polys


def _bbox_of_points(points):
    xs = [p.x for p in points]
    ys = [p.y for p in points]
    zs = [p.z for p in points]
    return Vector((min(xs), min(ys), min(zs))), Vector((max(xs), max(ys), max(zs)))


def _bbox_overlap_depth(a, b):
    """두 AABB 의 축별 겹침 깊이 중 최솟값 (음수면 떨어져 있음)."""
    (amin, amax), (bmin, bmax) = a, b
    return min(min(amax[i], bmax[i]) - max(amin[i], bmin[i]) for i in range(3))


def _mesh_stats(obj):
    bm = bmesh.new()
    try:
        bm.from_mesh(obj.data)
        non_manifold = sum(1 for e in bm.edges if not e.is_manifold)
        ngons = sum(1 for f in bm.faces if len(f.verts) > 4)
        tris = sum(len(f.verts) - 2 for f in bm.faces)
    finally:
        bm.free()
    return non_manifold, ngons, tris


def _name_tokens(name):
    """'SM_DiningTable.001' -> ['sm', 'dining', 'table', '001'] (CamelCase·구분자·숫자 분리)."""
    name = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name)
    return [t for t in re.split(r"[^a-z0-9]+", name.lower()) if t]


def _size_rule_for(name, rules):
    """이름 토큰에 규칙 키워드가 '단어 단위로 연속해서' 들어 있으면 그 규칙을 돌려준다.

    - 긴 키워드 우선 (dining_table 이 table 보다 먼저)
    - indoor_plant 의 'door', turntable 의 'table' 처럼 단어 일부만 같은 경우는 매칭하지 않음
    - door_handle, table_lamp 처럼 키워드 뒤에 부속품 단어가 오면 매칭하지 않음
    """
    tokens = _name_tokens(name)
    for key in sorted(rules, key=lambda k: (len(k.split("_")), len(k)), reverse=True):
        kt = key.split("_")
        n = len(kt)
        for i in range(len(tokens) - n + 1):
            if tokens[i:i + n] == kt:
                nxt = tokens[i + n] if i + n < len(tokens) else None
                if nxt in ACCESSORY_TOKENS:
                    continue
                return key, rules[key]
    return None, None


_TRAILING_NOISE = re.compile(r"^(\d+|[a-z]|north|south|east|west|left|right|front|back|main|plane|slab|mesh|geo)$")


def _is_structure(name, structure_names):
    """이름의 '마지막 핵심 단어'가 구조물 단어인지. Wall_N, Floor_01, floor_plane -> 구조물 / wall_shelf, wall_lamp -> 가구."""
    tokens = _name_tokens(name)
    while len(tokens) > 1 and _TRAILING_NOISE.match(tokens[-1]):
        tokens.pop()
    return bool(tokens) and tokens[-1] in structure_names


def _oriented_size(root, verts):
    """유닛 루트의 Z 회전(yaw)을 되돌린 좌표계에서 잰 (w, d, h). w >= d."""
    yaw = root.matrix_world.to_euler("XYZ").z
    c, s = math.cos(-yaw), math.sin(-yaw)
    xs = [v.x * c - v.y * s for v in verts]
    ys = [v.x * s + v.y * c for v in verts]
    zs = [v.z for v in verts]
    dx, dy = max(xs) - min(xs), max(ys) - min(ys)
    return max(dx, dy), min(dx, dy), max(zs) - min(zs)


def _is_supported(unit, others, floor_z, tol):
    """유닛 바닥 근처 여러 지점에서 아래로 레이를 쏴서, 다른 유닛의 면이 바닥 높이 ±tol 안에 있는지 확인.

    자기 자신은 BVH 목록에 넣지 않으므로, 받침면과 바닥면이 같은 높이(동일 평면)여도 정확히 잡힌다.
    """
    bmin, bmax = unit["bbox"]
    if floor_z is not None and abs(bmin.z - floor_z) <= tol:
        return True, "floor"
    sx, sy = (bmax.x - bmin.x), (bmax.y - bmin.y)
    samples = [(0.5, 0.5), (0.1, 0.1), (0.9, 0.1), (0.1, 0.9), (0.9, 0.9)]
    down = Vector((0, 0, -1))
    for other in others:
        (omin, omax) = other["bbox"]
        # XY 가 겹치고, 상대의 윗면이 내 바닥 근처에 있을 수 있는 경우만
        if omax.x < bmin.x or omin.x > bmax.x or omax.y < bmin.y or omin.y > bmax.y:
            continue
        if omin.z > bmin.z + tol or omax.z < bmin.z - tol:
            continue
        for fx, fy in samples:
            origin = Vector((bmin.x + sx * fx, bmin.y + sy * fy, bmin.z + tol))
            loc, _n, _i, _d = other["bvh"].ray_cast(origin, down, 2 * tol)
            if loc is not None:
                return True, other["root"].name
    return False, None


def audit_scene(floor_z=None, tol=0.005, size_rules=None, ceiling_z=None,
                structure_names=("floor", "ground", "wall", "ceiling", "terrain"), collection=None):
    """장면을 점검해서 dict 리포트를 반환한다.

    collection: 컬렉션 이름. 주면 그 컬렉션(하위 컬렉션 포함)에 든 유닛만 보고하고, ceiling_z 도 그 유닛에만 적용한다.
        (방 내부와 건물 외관처럼 천장 높이가 다른 것을 한 장면에서 따로 검사할 때. 받침면·관통 상대는 장면 전체를 쓴다)

    floor_z: 바닥 높이(m). None 이면 바닥 판정은 레이캐스트 결과만 사용.
    ceiling_z: 천장 높이(m). 주면 이보다 위로 나간 유닛을 above_ceiling 으로 표시 (예: 한국 구축 아파트 2.3).
    tol: 접촉/관통 판정 허용 오차(m). 기본 5mm.
    structure_names: 이 단어가 이름에 들어간 유닛은 구조물(바닥·벽·천장)로 본다.
        구조물은 떠있음·치수 검사에서 빠지고 받침면으로만 쓰이며, 구조물끼리의 관통은 검사하지 않는다.
        가구가 벽·천장을 뚫고 들어간 경우(가구–구조물 관통)는 검사한다.
    """
    size_rules = DEFAULT_SIZE_RULES if size_rules is None else size_rules
    depsgraph = bpy.context.evaluated_depsgraph_get()

    # 1) 최상위 부모 기준으로 유닛 구성
    roots = [o for o in bpy.context.scene.objects if o.parent is None]
    units = []
    for root in roots:
        meshes = _mesh_objects_under(root)
        if not meshes:
            continue
        verts, polys = [], []
        for m in meshes:
            v, p = _world_verts_and_polys(m, depsgraph)
            off = len(verts)
            verts.extend(v)
            polys.extend(tuple(i + off for i in poly) for poly in p)
        if not verts:
            continue
        bmin, bmax = _bbox_of_points(verts)
        units.append({
            "root": root, "meshes": meshes, "verts": verts, "polys": polys, "bbox": (bmin, bmax),
            "bvh": BVHTree.FromPolygons(verts, polys),  # 월드 좌표 BVH (받침/관통 판정용)
        })

    if collection is not None:
        col = bpy.data.collections[collection]
        scoped = {o.name for o in col.all_objects}
        in_scope = lambda u: u["root"].name in scoped or any(m.name in scoped for m in u["meshes"])
    else:
        in_scope = lambda u: True

    report = {"units": [], "interpenetrations": [], "summary": {}}
    ignored = lambda name: _is_structure(name, structure_names)

    # 2) 관통 검사 (먼저 계산해서 '박힘' 판정에도 씀): 바운딩박스가 tol 이상 겹치는 쌍만 정밀 검사
    partners = {i: [] for i in range(len(units))}
    for i in range(len(units)):
        for j in range(i + 1, len(units)):
            a, b = units[i], units[j]
            if ignored(a["root"].name) and ignored(b["root"].name):
                continue  # 구조물끼리(벽–바닥 등)는 검사하지 않음
            depth = _bbox_overlap_depth(a["bbox"], b["bbox"])
            if depth <= tol:
                continue
            pairs = a["bvh"].overlap(b["bvh"])
            if not pairs:
                continue
            partners[i].append(j)
            partners[j].append(i)
            if in_scope(a) or in_scope(b):
                report["interpenetrations"].append({
                    "a": a["root"].name, "b": b["root"].name,
                    "intersecting_face_pairs": len(pairs),
                    "bbox_overlap_depth_m": round(depth, 4),
                })

    # 3) 유닛별 검사
    for idx, u in enumerate(units):
        if not in_scope(u):
            continue
        root, (bmin, bmax) = u["root"], u["bbox"]
        dims = bmax - bmin
        issues = []
        for m in u["meshes"]:
            s = m.scale
            if any(abs(c - 1.0) > 1e-4 for c in s):
                issues.append(f"unapplied_scale:{m.name}={tuple(round(c, 3) for c in s)}")
            if s.x * s.y * s.z < 0:
                issues.append(f"negative_scale:{m.name}")
            nm, _ngons, _tris = _mesh_stats(m)
            if nm:
                issues.append(f"non_manifold_edges:{m.name}={nm}")
            if not any(slot.material for slot in m.material_slots):
                issues.append(f"no_material:{m.name}")
            if not m.data.uv_layers:
                issues.append(f"no_uv:{m.name}")

        support = None
        if not ignored(root.name):
            if ceiling_z is not None and bmax.z > ceiling_z + tol:
                issues.append(f"above_ceiling:{round(bmax.z - ceiling_z, 4)}m")
            below = floor_z is not None and bmin.z < floor_z - tol
            if below:
                issues.append(f"below_floor:{round(floor_z - bmin.z, 4)}m")
            supported, support = _is_supported(u, [o for o in units if o is not u], floor_z, tol)
            if not supported:
                # 받침면보다 아래로 파고든 경우: '떠 있음'이 아니라 '박힘'으로 보고
                # 관통 상대의 윗면이 내 바닥보다 위, 내 꼭대기 이하에 있으면 그 위에 '박혀' 있는 것
                sunk = [units[j] for j in partners[idx]
                        if bmin.z + tol < units[j]["bbox"][1].z <= bmax.z]
                if sunk:
                    o = max(sunk, key=lambda o: o["bbox"][1].z)
                    issues.append(f"sunk_into:{o['root'].name}={round(min(o['bbox'][1].z, bmax.z) - bmin.z, 4)}m")
                    support = o["root"].name
                elif not below:
                    issues.append("floating_or_wall_mounted")

        w, d, h = _oriented_size(root, u["verts"])
        key, rule = _size_rule_for(root.name, size_rules) if not ignored(root.name) else (None, None)
        if rule:
            measured = {"w": w, "d": d, "z": h}
            for axis, (lo, hi) in rule.items():
                val = measured[axis]
                if not (lo <= val <= hi):
                    issues.append(f"size_out_of_range:{key}.{axis}={round(val, 3)}m (expected {lo}-{hi})")

        report["units"].append({
            "name": root.name,
            "parts": [m.name for m in u["meshes"]],
            "dimensions_m": [round(dims.x, 4), round(dims.y, 4), round(dims.z, 4)],
            "size_wdh_m": [round(w, 4), round(d, 4), round(h, 4)],
            "size_rule": key,
            "bbox_min": [round(c, 4) for c in bmin],
            "bbox_max": [round(c, 4) for c in bmax],
            "supported_by": support,
            "issues": issues,
        })

    n_issue_units = sum(1 for u in report["units"] if u["issues"])
    report["summary"] = {
        "units": len(report["units"]),
        "units_with_issues": n_issue_units,
        "interpenetrating_pairs": len(report["interpenetrations"]),
        "floor_z": floor_z,
        "ceiling_z": ceiling_z,
        "collection": collection,
        "tolerance_m": tol,
    }
    return report


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    floor_z, ceiling_z, collection, out, tol = None, None, None, None, 0.005
    for k, v in zip(argv[::2], argv[1::2]):
        if k == "--floor-z":
            floor_z = float(v)
        elif k == "--ceiling-z":
            ceiling_z = float(v)
        elif k == "--collection":
            collection = v
        elif k == "--out":
            out = v
        elif k == "--tol":
            tol = float(v)
    report = audit_scene(floor_z=floor_z, ceiling_z=ceiling_z, tol=tol, collection=collection)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
    print(text)


# blender-mcp 의 execute_blender_code 는 exec() 로 실행하므로 __name__ 이 "__main__" 이 아닐 수 있다.
# 그래서 "모듈로 import 된 경우"만 제외하고 항상 실행한다.
if __name__ != "scene_audit":
    main()
