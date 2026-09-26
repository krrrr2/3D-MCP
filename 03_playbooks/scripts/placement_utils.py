"""
placement_utils.py - AI 에이전트가 오브젝트를 "말이 되게" 배치하도록 돕는 함수 모음.

좌표 규칙 (Blender 기본): Z-up, 단위 m. 가구 모델의 "앞면"은 -Y 방향을 보도록 모델링하는 것을 권장
(Blender Front 뷰(Numpad 1)가 -Y 쪽에서 +Y 를 바라보므로, 앞면이 카메라를 향함).

주요 함수
  world_bbox(obj)                          -> (min, max)  부모+자식 전체의 월드 AABB
  snap_to_floor(obj, floor_z=0.0)          바닥에 정확히 붙이기
  drop_to_surface(obj)                     아래 방향 레이캐스트로 가장 가까운 받침면 위에 올리기 (책상 위 소품 등)
  place_next_to(obj, target, side, gap)    target 옆(+X/-X/+Y/-Y)에 gap 만큼 띄워 붙이기 (Z 는 유지)
  place_against_wall(obj, wall_y, gap)     등을 벽(+Y 쪽 벽)에 붙이기
  face_towards(obj, target_point)          Z 축 회전만으로 앞면(-Y)이 target 을 보게 하기
  xy_clearance(a, b)                       두 유닛 사이 평면(XY) 최소 간격 (통로·동선 확인용)
  check_clearances(rules)                  [(a, b, min_m), ...] 규칙 위반 목록 반환

사용: execute_blender_code 에 이 파일 내용 + 호출 코드를 함께 붙여 넣거나, 헤드리스에서 import.
"""

import math

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def _unit_meshes(obj):
    objs = [obj] + list(obj.children_recursive)
    return [o for o in objs if o.type == "MESH"]


def world_bbox(obj):
    """obj 와 모든 자식 메시(모디파이어 적용 상태)의 월드 좌표 AABB."""
    depsgraph = bpy.context.evaluated_depsgraph_get()
    pts = []
    for m in _unit_meshes(obj):
        ev = m.evaluated_get(depsgraph)
        pts.extend(ev.matrix_world @ Vector(c) for c in ev.bound_box)
    if not pts:  # Empty 등 메시가 없는 경우 위치만
        p = obj.matrix_world.translation
        return p.copy(), p.copy()
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return mn, mx


def _move(obj, delta):
    obj.location += delta
    bpy.context.view_layer.update()


def snap_to_floor(obj, floor_z=0.0):
    mn, _ = world_bbox(obj)
    _move(obj, Vector((0, 0, floor_z - mn.z)))


def _world_bvh(mesh_obj, depsgraph):
    ev = mesh_obj.evaluated_get(depsgraph)
    me = ev.to_mesh()
    try:
        mw = ev.matrix_world
        verts = [mw @ v.co for v in me.vertices]
        polys = [tuple(p.vertices) for p in me.polygons]
    finally:
        ev.to_mesh_clear()
    return BVHTree.FromPolygons(verts, polys)


def drop_to_surface(obj, max_drop=10.0, eps=1e-4):
    """바닥 근처 5개 지점에서 아래로 레이를 쏘고, 가장 높은 받침면 위에 올린다.

    자기 자신(자식 포함)은 레이 대상에서 제외하므로, 이미 표면에 붙어 있는 경우에도
    그 표면을 뚫고 떨어지지 않는다. 성공 시 받침 오브젝트 이름, 받침이 없으면 None.
    """
    depsgraph = bpy.context.evaluated_depsgraph_get()
    own = {o.name for o in [obj] + list(obj.children_recursive)}
    mn, mx = world_bbox(obj)
    candidates = []
    for o in bpy.context.scene.objects:
        if o.type != "MESH" or o.name in own or not o.visible_get():
            continue
        omn, omx = world_bbox(o)
        if omx.x < mn.x or omn.x > mx.x or omx.y < mn.y or omn.y > mx.y or omn.z > mn.z + eps:
            continue
        candidates.append((o, _world_bvh(o, depsgraph)))
    best = None  # (surface_z, name)
    for fx, fy in [(0.5, 0.5), (0.15, 0.15), (0.85, 0.15), (0.15, 0.85), (0.85, 0.85)]:
        origin = Vector((mn.x + (mx.x - mn.x) * fx, mn.y + (mx.y - mn.y) * fy, mn.z + eps))
        for o, bvh in candidates:
            loc, _n, _i, _d = bvh.ray_cast(origin, Vector((0, 0, -1)), max_drop)
            if loc is not None and (best is None or loc.z > best[0]):
                best = (loc.z, o.name)
    if best is None:
        return None
    _move(obj, Vector((0, 0, best[0] - mn.z)))
    return best[1]


def place_next_to(obj, target, side="+X", gap=0.05, align="center"):
    """target 의 side 쪽에 obj 를 gap(m) 띄워 배치. align: 'center' | 'front' | 'back' (다른 축 정렬)."""
    omn, omx = world_bbox(obj)
    tmn, tmx = world_bbox(target)
    ocen, tcen = (omn + omx) / 2, (tmn + tmx) / 2
    d = Vector((0, 0, 0))
    if side == "+X":
        d.x = (tmx.x + gap) - omn.x
    elif side == "-X":
        d.x = (tmn.x - gap) - omx.x
    elif side == "+Y":
        d.y = (tmx.y + gap) - omn.y
    elif side == "-Y":
        d.y = (tmn.y - gap) - omx.y
    else:
        raise ValueError("side must be one of +X, -X, +Y, -Y")
    other = "y" if side in ("+X", "-X") else "x"
    if align == "center":
        setattr(d, other, getattr(tcen, other) - getattr(ocen, other))
    elif align == "front":   # -Y(앞) 면 정렬
        if other == "y":
            d.y = tmn.y - omn.y
    elif align == "back":
        if other == "y":
            d.y = tmx.y - omx.y
    _move(obj, d)


def place_against_wall(obj, wall_y, gap=0.02):
    """+Y 쪽에 있는 벽(내측 면 y=wall_y)에 등을 붙인다. 앞면(-Y)은 방 안쪽을 본다."""
    _, omx = world_bbox(obj)
    _move(obj, Vector((0, (wall_y - gap) - omx.y, 0)))


def face_towards(obj, target_point):
    """Z 축 회전만 바꿔서 obj 의 앞면(-Y)이 target_point 를 향하게 한다."""
    target_point = Vector(target_point)
    loc = obj.matrix_world.translation
    dx, dy = target_point.x - loc.x, target_point.y - loc.y
    if abs(dx) < 1e-9 and abs(dy) < 1e-9:
        return
    # 로컬 -Y 가 (dx, dy) 를 향하도록: 회전각 = atan2(dy, dx) + 90°
    obj.rotation_euler.z = math.atan2(dy, dx) + math.pi / 2
    bpy.context.view_layer.update()


def xy_clearance(a, b):
    """두 유닛의 평면(XY) AABB 사이 최소 거리. 겹치면 0."""
    amn, amx = world_bbox(a)
    bmn, bmx = world_bbox(b)
    dx = max(0.0, max(amn.x, bmn.x) - min(amx.x, bmx.x))
    dy = max(0.0, max(amn.y, bmn.y) - min(amx.y, bmx.y))
    return math.hypot(dx, dy)


def check_clearances(rules):
    """rules: [(obj_a_name, obj_b_name, min_m, max_m_or_None), ...] -> 위반 목록."""
    out = []
    for rule in rules:
        a_name, b_name, lo = rule[0], rule[1], rule[2]
        hi = rule[3] if len(rule) > 3 else None
        a, b = bpy.data.objects.get(a_name), bpy.data.objects.get(b_name)
        if a is None or b is None:
            out.append({"a": a_name, "b": b_name, "error": "object not found"})
            continue
        d = xy_clearance(a, b)
        if d < lo or (hi is not None and d > hi):
            out.append({"a": a_name, "b": b_name, "clearance_m": round(d, 3), "expected": [lo, hi]})
    return out
