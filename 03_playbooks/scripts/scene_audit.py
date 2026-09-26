"""
scene_audit.py - AI가 만든 Blender 장면의 형태/배치 오류를 자동 점검하는 스크립트.

검사 항목
  - 오브젝트(부모 기준으로 묶은 "유닛")별 실제 치수(m), 위치, 바닥 높이
  - 떠 있음(floating): 아래에 받쳐주는 면이 없음 (벽걸이/천장 조명이면 정상일 수 있음)
  - 바닥 아래로 박힘(below_floor)
  - 서로 관통(interpenetration): 바운딩박스가 겹치고 실제 면끼리 교차
  - 스케일 미적용 / 음수 스케일
  - Non-manifold 엣지, 재질 없음, UV 없음
  - 이름 키워드(chair, table, sofa ...) 기준 치수 범위 벗어남

사용법
  1) blender-mcp 의 execute_blender_code 에 파일 전체를 붙여 넣으면 결과 JSON 이 출력됩니다.
  2) 헤드리스: blender -b scene.blend --python scene_audit.py -- --floor-z 0 --out report.json
  3) 모듈: from scene_audit import audit_scene; report = audit_scene(floor_z=0.0)

Blender 4.2 LTS 이상 / 5.0 에서 동작하도록 작성했습니다 (bpy 5.0.1 로 테스트).
"""

import json
import sys

import bmesh
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

# 이름에 키워드가 들어간 유닛의 전체 치수 허용 범위 (미터, [min, max]).
# 근거: 03_playbooks/05_reference_dimensions.md. 여유 있게 잡은 "명백한 오류" 탐지용 범위입니다.
DEFAULT_SIZE_RULES = {
    "dining_table": {"z": [0.68, 0.80]},
    "coffee_table": {"z": [0.30, 0.55]},
    "desk": {"z": [0.68, 0.80]},
    "table": {"z": [0.35, 0.80]},
    "stool": {"z": [0.40, 0.85]},
    "chair": {"z": [0.70, 1.20], "x": [0.35, 0.80], "y": [0.35, 0.80]},
    "sofa": {"z": [0.60, 1.10], "y": [0.70, 1.20], "x": [1.20, 3.50]},
    "bed": {"z": [0.30, 1.40], "x": [0.85, 2.30], "y": [1.85, 2.40]},
    "door": {"z": [1.95, 2.50], "x": [0.60, 1.20]},
    "counter": {"z": [0.84, 0.96]},
    "bookshelf": {"z": [0.70, 2.40], "y": [0.20, 0.45]},
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


def _size_rule_for(name, rules):
    lname = name.lower().replace(" ", "_").replace("-", "_")
    # 긴 키워드 우선 (dining_table 이 table 보다 먼저 매칭되도록)
    for key in sorted(rules, key=len, reverse=True):
        if key in lname:
            return key, rules[key]
    return None, None


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


def audit_scene(floor_z=None, tol=0.005, size_rules=None, ignore_names=("floor", "ground", "wall", "ceiling")):
    """장면을 점검해서 dict 리포트를 반환한다.

    floor_z: 바닥 높이(m). None 이면 바닥 판정은 레이캐스트 결과만 사용.
    tol: 접촉/관통 판정 허용 오차(m). 기본 5mm.
    ignore_names: 이 단어가 이름에 들어간 유닛은 떠있음/관통 검사에서 제외(바닥, 벽 등 구조물).
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

    report = {"units": [], "interpenetrations": [], "summary": {}}
    ignored = lambda name: any(k in name.lower() for k in ignore_names)

    # 2) 유닛별 검사
    for u in units:
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

        if not ignored(root.name):
            if floor_z is not None and bmin.z < floor_z - tol:
                issues.append(f"below_floor:{round(floor_z - bmin.z, 4)}m")
            supported, support = _is_supported(u, [o for o in units if o is not u], floor_z, tol)
            if not supported:
                issues.append("floating_or_wall_mounted")
        else:
            support = None

        key, rule = _size_rule_for(root.name, size_rules)
        if rule:
            for axis, (lo, hi) in rule.items():
                val = getattr(dims, axis)
                if not (lo <= val <= hi):
                    issues.append(f"size_out_of_range:{key}.{axis}={round(val, 3)}m (expected {lo}-{hi})")

        report["units"].append({
            "name": root.name,
            "parts": [m.name for m in u["meshes"]],
            "dimensions_m": [round(dims.x, 4), round(dims.y, 4), round(dims.z, 4)],
            "bbox_min": [round(c, 4) for c in bmin],
            "bbox_max": [round(c, 4) for c in bmax],
            "supported_by": support,
            "issues": issues,
        })

    # 3) 관통 검사: 바운딩박스가 tol 이상 겹치는 쌍만 정밀 검사
    for i in range(len(units)):
        for j in range(i + 1, len(units)):
            a, b = units[i], units[j]
            if ignored(a["root"].name) or ignored(b["root"].name):
                continue
            depth = _bbox_overlap_depth(a["bbox"], b["bbox"])
            if depth <= tol:
                continue
            pairs = a["bvh"].overlap(b["bvh"])
            if pairs:
                report["interpenetrations"].append({
                    "a": a["root"].name, "b": b["root"].name,
                    "intersecting_face_pairs": len(pairs),
                    "bbox_overlap_depth_m": round(depth, 4),
                })

    n_issue_units = sum(1 for u in report["units"] if u["issues"])
    report["summary"] = {
        "units": len(report["units"]),
        "units_with_issues": n_issue_units,
        "interpenetrating_pairs": len(report["interpenetrations"]),
        "floor_z": floor_z,
        "tolerance_m": tol,
    }
    return report


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    floor_z, out, tol = None, None, 0.005
    for k, v in zip(argv[::2], argv[1::2]):
        if k == "--floor-z":
            floor_z = float(v)
        elif k == "--out":
            out = v
        elif k == "--tol":
            tol = float(v)
    report = audit_scene(floor_z=floor_z, tol=tol)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
    print(text)


# blender-mcp 의 execute_blender_code 는 exec() 로 실행하므로 __name__ 이 "__main__" 이 아닐 수 있다.
# 그래서 "모듈로 import 된 경우"만 제외하고 항상 실행한다.
if __name__ != "scene_audit":
    main()
