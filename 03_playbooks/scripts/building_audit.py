"""
building_audit.py - "사람이 설계한 건물처럼 말이 되는가"를 점검하는 스크립트 (건축 상식 검사).

scene_audit.py 가 '떠 있음·관통·치수' 같은 물리 오류를 잡는다면, 이 스크립트는
백룸(Backrooms)처럼 기묘한 결과를 만드는 **건축적 비상식**을 잡는다.

  문     : 벽에 안 뚫림, 바닥에서 뜸, 문을 열면 바로 벽, 허공·낭떠러지로 나감, 같은 방으로 되돌아옴, 가구가 막음, 크기 이상
  창문   : 벽에 안 뚫림, 어정쩡한 창턱 높이, 천장을 파고듦, 실내 벽에 난 창(방↔방), 창 바로 앞이 벽, 가구가 막음,
           같은 벽 창들의 높이가 제각각
  방     : 문 없는 밀폐된 방, 입구에서 갈 수 없는 방, 창 없는 거실·침실, 복도처럼 길쭉한 방, 천장 없음/너무 낮음/너무 높음,
           텅 빈 방, 똑같은 빈 방의 반복, 복도 비율 과다
  벽     : 천장까지 안 닿음(위가 뚫림), 벽 끝 사이 틈, 두께 이상
  계단   : 단 높이 불균일, 단 높이·너비 비상식(2R+T), 어디로도 안 이어짐
  가구   : 앉는 가구가 코앞의 벽을 보고 있음
  종합   : 백룸 위험도(liminal_risk) — 창 없는 방·복도 과다·빈 방·반복·밀폐 방 등 이유와 함께

근거
  - 문 앞 비움 구역 = 문 폭 × 문 폭 (NVlabs SAGE 배치 솔버), 문은 방과 방/외부를 잇고 창은 외벽에 둔다 (Holodeck, Infinigen Indoors)
  - 동선으로 모든 방에 갈 수 있어야 함 (SceneSmith Reachability 채점 항목)
  - 그 밖의 임계값은 특정 국가 법규가 아니라 넓게 잡은 "상식 범위"다. 02_guides/08_scene_layout_placement.md 참고.

이름 규칙 (에이전트에게 이렇게 짓게 하세요. 커스텀 프로퍼티 obj["role"], obj["room_type"] 가 있으면 그것이 우선)
  방 바닥   : Floor_<방종류>[_번호]   예) Floor_living, Floor_bedroom_2, Floor_hall, Floor_bathroom
  외부 지면 : Ground / Terrain
  벽        : ..._wall 또는 Wall_...  예) Wall_N, exterior_wall_3
  천장·지붕 : Ceiling..., ..._roof
  문·창     : ..._door / Door_01, ..._window / Window_01   (door_handle, window_sill 처럼 뒤에 다른 단어가 오면 부속품)
  계단      : stair / stairs / staircase 가 들어간 부모 아래에 단(step)을 자식 메시로
  나머지    : 가구

벽의 문·창 구멍은 Boolean(DIFFERENCE) 등으로 **실제로 뚫어야** 합니다. 커터 오브젝트는 숨기면 검사에서 빠집니다.

사용
  import building_audit; rep = building_audit.audit_building(collection="House")
  blender -b house.blend --python building_audit.py -- --collection House --out building.json
scene_audit.py 와 같은 폴더에 두세요 (공통 함수를 가져다 씁니다). Blender 4.2 LTS / 5.0 에서 테스트.
"""

import json
import math
import os
import statistics
import sys

import bpy
from mathutils import Vector, geometry
from mathutils.bvhtree import BVHTree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else ".")
import scene_audit as sa  # noqa: E402

# 방 종류 단어 → 분류
CIRCULATION = {"corridor", "hall", "hallway", "entry", "entrance", "foyer", "lobby", "stairwell", "passage", "vestibule"}
SERVICE = {"bathroom", "bath", "toilet", "wc", "restroom", "powder", "ensuite", "closet", "storage", "pantry", "utility",
           "laundry", "dressing", "walkin", "garage", "basement", "attic", "mudroom", "boiler", "shower"}
OUTDOOR = {"balcony", "terrace", "veranda", "porch", "deck", "patio"}
HABITABLE = {"living", "bedroom", "kitchen", "dining", "office", "study", "family", "den", "library", "playroom",
             "guest", "master", "kids", "nursery", "room", "ldk", "gym", "lounge", "salon", "loft", "studio", "suite"}
ROOM_WORDS = CIRCULATION | SERVICE | OUTDOOR | HABITABLE | {"bed", "level", "ground", "first", "second", "upper", "lower"}
SEATING = {"sofa", "chair", "armchair", "bench", "couch", "stool"}
# 'wall_shelf', 'floor_lamp', 'door_handle', 'window_sill' 처럼 구조 단어 뒤에 붙으면 가구·부속품으로 보는 단어
ATTACHED = {"shelf", "shelves", "lamp", "light", "lights", "sconce", "art", "painting", "picture", "poster", "photo",
            "frame", "clock", "mirror", "cabinet", "cupboard", "tv", "hook", "rack", "decor", "plant", "planter", "fan",
            "vent", "socket", "outlet", "switch", "sign", "handle", "knob", "sill", "trim", "molding", "moulding",
            "baseboard", "curtain", "curtains", "blind", "blinds", "rug", "mat", "carpet", "cushion", "stopper", "hinge"}

# 상식 범위 (m). 특정 법규가 아니라 "이 범위를 벗어나면 사람이 설계한 건물로 보기 어렵다"는 넓은 기준
LIMITS = {
    "door_h": (1.90, 2.70), "door_w": (0.60, 2.00), "door_float": 0.05, "door_front_wall": 0.60,
    "door_drop": 0.40, "window_w": (0.30, 6.00), "window_h": (0.30, 3.20),
    "sill_awkward": (0.03, 0.25), "sill_high": 1.80, "window_front_wall": 0.50, "window_align": 0.05,
    "ceiling_h": (2.10, 4.50), "corridor_aspect": 4.0, "corridor_min_w": 0.80, "corridor_fraction": 0.35,
    "wall_t": (0.05, 0.60), "wall_top_gap": 0.02, "wall_end_gap": (0.01, 0.30),
    "riser": (0.12, 0.22), "tread": (0.22, 0.38), "blondel": (0.55, 0.70), "riser_spread": 0.01,
    "seat_front_wall": 0.50, "repeat_rooms": 3,
}


# ----------------------------------------------------------------------------- 기본 도구

def _role(obj):
    r = obj.get("role") if hasattr(obj, "get") else None
    if r:
        return str(r).lower()
    toks = sa._name_tokens(obj.name)
    core = list(toks)
    while len(core) > 1 and sa._TRAILING_NOISE.match(core[-1]):
        core.pop()
    head = core[-1] if core else ""
    first = toks[0] if toks else ""
    plain = not any(t in ATTACHED for t in toks[1:])   # 뒤에 부속품 단어가 없음
    if head == "floor" or (first == "floor" and plain):
        return "floor"
    if head in ("ground", "terrain", "lawn", "yard"):
        return "ground"
    for role in ("wall", "ceiling", "roof", "door", "window"):
        # Wall_N / Wall_mid_x / north_wall / Door_bedroom / Window_living_2 모두 인식, wall_shelf·door_handle 은 가구
        if (head == role and not (toks and toks[-1] in ATTACHED)) or (first == role and plain):
            return role
    if any(t in ("stair", "stairs", "staircase", "stairway") for t in toks):
        return "stair"
    if head in ("column", "pillar", "beam", "post"):
        return "column"
    return "furniture"


def _room_type(obj):
    rt = obj.get("room_type") if hasattr(obj, "get") else None
    toks = [str(rt).lower()] if rt else sa._name_tokens(obj.name)
    for group, name in ((CIRCULATION, "circulation"), (SERVICE, "service"), (OUTDOOR, "outdoor"), (HABITABLE, "habitable")):
        if any(t in group for t in toks):
            return name
    if "bed" in toks:
        return "habitable"
    return "unknown"


def _collect_units(collection):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    scoped = None
    if collection is not None:
        scoped = {o.name for o in bpy.data.collections[collection].all_objects}
    units = []
    for root in [o for o in bpy.context.scene.objects if o.parent is None]:
        meshes = sa._mesh_objects_under(root)
        if not meshes:
            continue
        if scoped is not None and root.name not in scoped and not any(m.name in scoped for m in meshes):
            continue
        verts, polys, per_mesh = [], [], []
        for m in meshes:
            v, p = sa._world_verts_and_polys(m, depsgraph)
            off = len(verts)
            verts.extend(v)
            polys.extend(tuple(i + off for i in poly) for poly in p)
            if v:
                per_mesh.append((m, sa._bbox_of_points(v)))
        if not verts:
            continue
        bmin, bmax = sa._bbox_of_points(verts)
        units.append({
            "root": root, "name": root.name, "role": _role(root), "meshes": meshes, "per_mesh": per_mesh,
            "verts": verts, "polys": polys, "bbox": (bmin, bmax), "bvh": BVHTree.FromPolygons(verts, polys),
        })
    for u in units:
        u["frame"] = _frame(u)
    return units


def _frame(u):
    """루트의 Z 회전 기준 로컬 프레임: 중심, 로컬 x/y 축, 로컬 크기, 긴 축/두께 축."""
    yaw = u["root"].matrix_world.to_euler("XYZ").z
    c, s = math.cos(yaw), math.sin(yaw)
    ax, ay = Vector((c, s, 0.0)), Vector((-s, c, 0.0))
    xs = [v.dot(ax) for v in u["verts"]]
    ys = [v.dot(ay) for v in u["verts"]]
    zs = [v.z for v in u["verts"]]
    ex, ey = max(xs) - min(xs), max(ys) - min(ys)
    center = ax * ((max(xs) + min(xs)) / 2) + ay * ((max(ys) + min(ys)) / 2)
    center.z = (max(zs) + min(zs)) / 2
    if ex >= ey:
        long_ax, normal, length, thick = ax, ay, ex, ey
    else:
        long_ax, normal, length, thick = ay, ax, ey, ex
    return {"center": center, "ax": ax, "ay": ay, "ex": ex, "ey": ey, "zmin": min(zs), "zmax": max(zs),
            "long": long_ax, "normal": normal, "length": length, "thick": thick, "yaw": yaw}


def _cast(units, origin, direction, dist, with_normal=False):
    best = None
    for u in units:
        loc, nrm, _i, d = u["bvh"].ray_cast(origin, direction, dist)
        if loc is not None and (best is None or d < best[1]):
            best = (loc, d, u, nrm)
    if best is None:
        return None
    return best if with_normal else best[:3]


def _aabb_overlap(a, b):
    (amin, amax), (bmin, bmax) = a, b
    return min(min(amax[i], bmax[i]) - max(amin[i], bmin[i]) for i in range(3))


def _zone_aabb(origin, along, depth, across, width, z0, z1):
    pts = []
    for dd in (0.0, depth):
        for ww in (-width / 2, width / 2):
            p = origin + along * dd + across * ww
            pts.append(Vector((p.x, p.y, z0)))
            pts.append(Vector((p.x, p.y, z1)))
    return sa._bbox_of_points(pts)


def _top_area(u):
    """윗면(법선이 위를 향하고 bbox 최상단 근처) 면적 = 방 바닥 면적."""
    area, top = 0.0, u["bbox"][1].z
    V = u["verts"]
    for poly in u["polys"]:
        pts = [V[i] for i in poly]
        if len(pts) < 3 or any(abs(p.z - top) > 0.005 for p in pts):
            continue
        n = geometry.normal(pts)
        if n.z < 0.9:
            continue
        for k in range(1, len(pts) - 1):
            area += geometry.area_tri(pts[0], pts[k], pts[k + 1])
    return area


# ----------------------------------------------------------------------------- 메인 점검

def audit_building(collection=None, limits=None):
    L = dict(LIMITS, **(limits or {}))
    units = _collect_units(collection)
    by_role = {}
    for u in units:
        by_role.setdefault(u["role"], []).append(u)
    walls, floors, grounds = by_role.get("wall", []), by_role.get("floor", []), by_role.get("ground", [])
    ceilings = by_role.get("ceiling", []) + by_role.get("roof", [])
    doors, windows = by_role.get("door", []), by_role.get("window", [])
    furniture = by_role.get("furniture", [])
    solids = walls + by_role.get("column", [])
    ground_like = floors + grounds
    issues = []

    def add(sev, code, obj, detail):
        issues.append({"severity": sev, "code": code, "object": obj, "detail": detail})

    def classify(p, ref_z):
        """점 p 아래를 보고 방/외부/허공 판정. ref_z = 문·창이 속한 층 바닥 높이 추정치."""
        hit = _cast(ground_like, Vector((p.x, p.y, p.z)), Vector((0, 0, -1)), 100.0)
        if hit is None:
            return {"kind": "void", "top": None, "unit": None}
        loc, _d, u = hit
        kind = "room" if u["role"] == "floor" else "exterior"
        return {"kind": kind, "top": loc.z, "unit": u}

    room_info = {u["name"]: {"doors": [], "windows": [], "furniture": [], "unit": u} for u in floors}
    graph = {u["name"]: set() for u in floors}
    graph["EXTERIOR"] = set()

    # --- 문·창 공통
    def host_wall(o):
        best, best_v = None, 0.0
        for w in walls:
            ov = [min(o["bbox"][1][i], w["bbox"][1][i]) - max(o["bbox"][0][i], w["bbox"][0][i]) for i in range(3)]
            if min(ov) > -0.02:
                vol = max(ov[0], 0.001) * max(ov[1], 0.001) * max(ov[2], 0.001)
                if vol > best_v:
                    best, best_v = w, vol
        return best

    def opening_report(o, kind):
        f = o["frame"]
        w = host_wall(o)
        if w is None:
            add("error", f"{kind}_not_in_wall", o["name"], f"{kind}가 어떤 벽에도 끼워져 있지 않습니다(허공에 선 {kind}).")
            return None
        wf = w["frame"]
        n, along = wf["normal"], wf["long"]
        t = wf["thick"]
        width = abs((o["bbox"][1] - o["bbox"][0]).dot(along)) if abs(along.x) > 1e-6 or abs(along.y) > 1e-6 else f["length"]
        width = max(width, 0.05)
        c = Vector((f["center"].x, f["center"].y, 0.0))
        # 벽 두께 중심선으로 투영
        wc = Vector((wf["center"].x, wf["center"].y, 0.0))
        c = c - n * (c - wc).dot(n)
        zmin, zmax = o["bbox"][0].z, o["bbox"][1].z
        probe_z = zmin + 1.0 if kind == "door" else (zmin + zmax) / 2
        # 1) 구멍이 실제로 뚫렸나 (벽 BVH 만 대상으로 벽 두께를 가로지르는 레이)
        heights = (zmin + 0.3, zmin + 1.0) if kind == "door" else ((zmin + zmax) / 2,)
        for hz in heights:
            start = Vector((c.x, c.y, hz)) - n * (t / 2 + 0.05)
            hit = _cast([w], start, n, t + 0.1)
            if hit is not None:
                add("error", "opening_not_cut", o["name"],
                    f"{w['name']}에 {kind} 구멍이 뚫려 있지 않습니다(높이 {hz:.2f} m에서 벽에 막힘). Boolean으로 구멍을 내세요.")
                break
        # 2) 양쪽 판정
        sides = []
        for sgn in (1, -1):
            d = n * sgn
            start = Vector((c.x, c.y, probe_z)) + d * (t / 2 + 0.01)
            ahead = _cast(solids + furniture, start, d, 3.0)
            side = classify(start + d * 0.5, zmin)
            side["dir"] = d
            side["start"] = start
            side["ahead"] = (ahead[1], ahead[2]) if ahead else None
            sides.append(side)
        return {"wall": w, "n": n, "along": along, "c": c, "width": width, "zmin": zmin, "zmax": zmax, "sides": sides}

    # --- 문
    for o in doors:
        r = opening_report(o, "door")
        if r is None:
            continue
        h = r["zmax"] - r["zmin"]
        if not (L["door_h"][0] <= h <= L["door_h"][1]):
            add("warning", "door_size", o["name"], f"문 높이 {h:.2f} m (상식 범위 {L['door_h'][0]}~{L['door_h'][1]} m)")
        if not (L["door_w"][0] <= r["width"] <= L["door_w"][1]):
            add("warning", "door_size", o["name"], f"문 폭 {r['width']:.2f} m (상식 범위 {L['door_w'][0]}~{L['door_w'][1]} m)")
        tops = [s["top"] for s in r["sides"] if s["kind"] == "room" and s["top"] is not None]
        ref = max(tops) if tops else max((s["top"] for s in r["sides"] if s["top"] is not None), default=None)
        if ref is not None:
            gap = r["zmin"] - ref
            if gap > L["door_float"]:
                add("error", "door_floating", o["name"], f"문 아랫단이 바닥보다 {gap:.2f} m 떠 있습니다.")
            elif gap < -L["door_float"]:
                add("error", "door_sunk", o["name"], f"문 아랫단이 바닥보다 {-gap:.2f} m 아래에 박혀 있습니다.")
        names = []
        for s in r["sides"]:
            if s["ahead"] is not None and s["ahead"][1]["role"] in ("wall", "column") and s["ahead"][0] < L["door_front_wall"]:
                add("error", "door_faces_wall", o["name"],
                    f"문을 열면 {s['ahead'][0]:.2f} m 앞이 벽({s['ahead'][1]['name']})입니다. 지나갈 수 없는 문.")
            if s["kind"] == "void":
                add("error", "door_to_void", o["name"], "문 한쪽 아래에 바닥도 지면도 없습니다(허공으로 나가는 문).")
            elif ref is not None and s["top"] is not None and ref - s["top"] > L["door_drop"]:
                add("error", "door_to_drop", o["name"],
                    f"문 한쪽이 {ref - s['top']:.2f} m 낭떠러지입니다(발코니·계단 없이 밖으로 나가는 문).")
            names.append(s["unit"]["name"] if s["kind"] == "room" else ("EXTERIOR" if s["kind"] == "exterior" else None))
            # 문 앞 비움 구역: 문 폭 × 문 폭 (SAGE 솔버와 같은 기준), 최소 0.8 m
            zone = _zone_aabb(Vector((r["c"].x, r["c"].y, 0)) + s["dir"] * (r["wall"]["frame"]["thick"] / 2), s["dir"],
                              max(r["width"], 0.8), r["along"], r["width"], r["zmin"] + 0.03, r["zmin"] + 2.0)
            for fu in furniture:
                if fu["bbox"][1].z - fu["bbox"][0].z < 0.03:
                    continue  # 러그 등 바닥 깔개
                if _aabb_overlap(zone, fu["bbox"]) > 0.02:
                    add("error", "door_blocked", o["name"], f"문 앞 통로를 {fu['name']}가 막고 있습니다.")
        a, b = names
        if a is not None and a == b and a != "EXTERIOR":
            add("warning", "door_same_room", o["name"], f"문 양쪽이 같은 방({a})입니다. 의미 없는 문.")
        for nm in (a, b):
            if nm in room_info:
                room_info[nm]["doors"].append(o["name"])
        if a and b and a != b:
            graph.setdefault(a, set()).add(b)
            graph.setdefault(b, set()).add(a)

    # --- 창문
    window_rows = []
    for o in windows:
        r = opening_report(o, "window")
        if r is None:
            continue
        h = r["zmax"] - r["zmin"]
        if not (L["window_w"][0] <= r["width"] <= L["window_w"][1]) or not (L["window_h"][0] <= h <= L["window_h"][1]):
            add("warning", "window_size", o["name"], f"창 크기 {r['width']:.2f} × {h:.2f} m 가 상식 범위를 벗어납니다.")
        rooms = [s for s in r["sides"] if s["kind"] == "room"]
        outs = [s for s in r["sides"] if s["kind"] != "room"]
        floor_top = max((s["top"] for s in rooms), default=None)
        if floor_top is None:
            floor_top = max((s["top"] for s in r["sides"] if s["top"] is not None), default=0.0)
        sill = r["zmin"] - floor_top
        if sill < -0.02:
            add("error", "window_below_floor", o["name"], f"창 아랫단이 바닥보다 {-sill:.2f} m 아래입니다.")
        elif L["sill_awkward"][0] < sill < L["sill_awkward"][1]:
            add("warning", "window_awkward_sill", o["name"],
                f"창턱 높이 {sill:.2f} m: 바닥까지 내린 창(0)도 일반 창(0.3 m 이상)도 아닌 어정쩡한 높이입니다.")
        elif sill > L["sill_high"]:
            add("warning", "window_too_high", o["name"], f"창턱 높이 {sill:.2f} m: 사람 눈높이보다 높아 밖이 안 보입니다(의도한 고창이 아니면 이상).")
        for s in rooms:
            ch = _cast(ceilings + floors, Vector((s["start"].x, s["start"].y, s["top"] + 0.05)), Vector((0, 0, 1)), 20.0)
            if ch is not None and r["zmax"] > ch[0].z + 0.01:
                add("error", "window_cuts_ceiling", o["name"], f"창 윗단이 천장보다 {r['zmax'] - ch[0].z:.2f} m 높습니다.")
        if len(rooms) == 2 and rooms[0]["unit"] is not rooms[1]["unit"]:
            add("warning", "interior_window", o["name"],
                f"실내 벽에 난 창입니다({rooms[0]['unit']['name']} ↔ {rooms[1]['unit']['name']}). 외벽이 아니면 이상해 보입니다.")
        for s in outs:
            if s["ahead"] is not None and s["ahead"][1]["role"] in ("wall", "column") and s["ahead"][0] < L["window_front_wall"]:
                add("warning", "window_faces_wall", o["name"], f"창 바깥 {s['ahead'][0]:.2f} m 앞이 벽입니다(열어도 벽만 보이는 창).")
        for s in rooms:
            zone = _zone_aabb(Vector((r["c"].x, r["c"].y, 0)) + s["dir"] * (r["wall"]["frame"]["thick"] / 2), s["dir"], 0.4,
                              r["along"], r["width"], floor_top + 0.03, r["zmax"])
            for fu in furniture:
                if fu["bbox"][1].z > r["zmin"] + 0.1 and _aabb_overlap(zone, fu["bbox"]) > 0.02:
                    add("warning", "window_blocked", o["name"], f"{fu['name']}가 창을 가리고 있습니다.")
            if s["unit"]["name"] in room_info:
                room_info[s["unit"]["name"]]["windows"].append(o["name"])
        window_rows.append((o["name"], r["wall"]["name"], round(floor_top, 1), r["zmin"], r["zmax"]))

    # 같은 벽·같은 층 창들의 높이 정렬
    groups = {}
    for name, wall, lvl, zmin, zmax in window_rows:
        groups.setdefault((wall, lvl), []).append((name, zmin, zmax))
    for (wall, _lvl), rows in groups.items():
        if len(rows) < 2:
            continue
        head_med = statistics.median(z for _, _, z in rows)
        for name, _zmin, zmax in rows:
            if abs(zmax - head_med) > L["window_align"]:
                add("warning", "window_misaligned", name,
                    f"{wall}의 다른 창들과 윗선 높이가 {abs(zmax - head_med):.2f} m 다릅니다(창 높이가 제각각인 벽).")

    # --- 가구 → 방 소속
    for fu in furniture:
        bmin, bmax = fu["bbox"]
        p = Vector(((bmin.x + bmax.x) / 2, (bmin.y + bmax.y) / 2, bmin.z + 0.05))
        hit = _cast(floors, p, Vector((0, 0, -1)), 0.5)
        if hit is not None:
            room_info[hit[2]["name"]]["furniture"].append(fu["name"])

    # --- 방
    reach = set()
    stack = ["EXTERIOR"]
    while stack:
        cur = stack.pop()
        if cur in reach:
            continue
        reach.add(cur)
        stack.extend(graph.get(cur, ()))
    has_entrance = bool(graph["EXTERIOR"])
    rooms_out, total_area, circ_area = [], 0.0, 0.0
    for name, info in room_info.items():
        u = info["unit"]
        f = u["frame"]
        rtype = _room_type(u["root"])
        area = _top_area(u) or f["ex"] * f["ey"]
        w_, d_ = max(f["ex"], f["ey"]), min(f["ex"], f["ey"])
        aspect = w_ / max(d_, 1e-6)
        top = u["bbox"][1].z
        ch = _cast(ceilings + [x for x in floors if x is not u], Vector((f["center"].x, f["center"].y, top + 0.05)),
                   Vector((0, 0, 1)), 20.0)
        ceil_h = (ch[0].z - top) if ch is not None else None
        total_area += area
        if rtype == "circulation":
            circ_area += area
        row = {"name": name, "type": rtype, "area_m2": round(area, 2), "size_m": [round(w_, 2), round(d_, 2)],
               "ceiling_h_m": round(ceil_h, 2) if ceil_h is not None else None,
               "doors": len(set(info["doors"])), "windows": len(set(info["windows"])), "furniture": len(info["furniture"])}
        rooms_out.append(row)
        if rtype == "outdoor":
            continue
        if not info["doors"]:
            add("error", "sealed_room", name, "문이 하나도 없는 밀폐된 방입니다.")
        elif has_entrance and name not in reach:
            add("error", "unreachable_room", name, "입구에서 문을 따라 갈 수 없는 방입니다.")
        if rtype in ("habitable", "unknown") and not info["windows"]:
            add("warning", "windowless_room", name, f"창이 없는 {'거실·침실 등 생활 공간' if rtype == 'habitable' else '방'}입니다.")
        if rtype == "circulation":
            if d_ < L["corridor_min_w"]:
                add("warning", "corridor_too_narrow", name, f"복도 폭 {d_:.2f} m")
        elif aspect > L["corridor_aspect"]:
            add("warning", "corridor_like_room", name, f"가로세로비 {aspect:.1f}:1 — 방이 아니라 복도처럼 길쭉합니다.")
        if ceil_h is None:
            add("warning", "no_ceiling", name, "방 위에 천장·지붕이 없습니다.")
        elif not (L["ceiling_h"][0] <= ceil_h <= L["ceiling_h"][1]):
            add("warning", "ceiling_height", name, f"천장 높이 {ceil_h:.2f} m (상식 범위 {L['ceiling_h'][0]}~{L['ceiling_h'][1]} m)")
        if rtype in ("habitable", "unknown") and not info["furniture"]:
            add("warning", "empty_room", name, "가구가 하나도 없는 빈 방입니다.")
    if floors and doors and not has_entrance:
        add("error", "no_entrance", "(building)", "외부로 통하는 문이 하나도 없습니다.")

    # 똑같은 빈 방의 반복
    sig = {}
    for row in rooms_out:
        if row["furniture"] == 0 and row["type"] != "outdoor":
            key = (round(row["size_m"][0], 1), round(row["size_m"][1], 1), row["ceiling_h_m"], row["windows"])
            sig.setdefault(key, []).append(row["name"])
    repeated = [v for v in sig.values() if len(v) >= L["repeat_rooms"]]
    for names in repeated:
        add("warning", "repetitive_empty_rooms", ", ".join(names), f"크기가 같은 빈 방 {len(names)}개가 반복됩니다.")

    # --- 벽
    for w in walls:
        f = w["frame"]
        if not (L["wall_t"][0] <= f["thick"] <= L["wall_t"][1]):
            add("warning", "wall_thickness", w["name"], f"벽 두께 {f['thick']:.2f} m")
        wtop = w["bbox"][1].z
        hit = _cast(ceilings + floors, Vector((f["center"].x, f["center"].y, wtop - 0.01)), Vector((0, 0, 1)), 1.01, True)
        # 아래를 향한 면(천장 밑면)에 먼저 닿으면 그 사이가 빈 것. 위를 향한 면이면 이미 슬래브 안에서 시작(= 붙어 있음)
        if hit is not None and hit[3].z < 0:
            gap = hit[0].z - wtop
            if gap > L["wall_top_gap"]:
                add("error", "wall_short_of_ceiling", w["name"], f"벽 위와 천장 사이가 {gap:.2f} m 비어 있습니다.")
        others = [x for x in walls + by_role.get("column", []) if x is not w]
        openings = doors + windows
        for sgn in (1, -1):
            end = Vector((f["center"].x, f["center"].y, f["center"].z)) + f["long"] * sgn * (f["length"] / 2)
            # 벽 끝면 위의 여러 점(두께 양쪽 × 높이 3단)에서 이웃 벽까지의 최소 거리. L자·T자로 맞물리면 0
            pts = [end]
            for side in (-1, 1):
                for hz in (w["bbox"][0].z + 0.1, f["center"].z, w["bbox"][1].z - 0.1):
                    q = end + f["normal"] * side * (f["thick"] / 2)
                    pts.append(Vector((q.x, q.y, hz)))
            best = None
            for x in others:
                if min(end[i] - x["bbox"][1][i] if end[i] > x["bbox"][1][i] else x["bbox"][0][i] - end[i]
                       if end[i] < x["bbox"][0][i] else 0.0 for i in range(3)) > L["wall_end_gap"][1] + 0.1:
                    continue
                dmin, near = None, None
                for q in pts:
                    if all(x["bbox"][0][i] - 0.002 <= q[i] <= x["bbox"][1][i] + 0.002 for i in range(3)):
                        dmin, near = 0.0, q
                        break
                    loc, _n, _i, dist = x["bvh"].find_nearest(q)
                    if loc is not None and (dmin is None or dist < dmin):
                        dmin, near = dist, loc
                if dmin is not None and (best is None or dmin < best[0]):
                    best = (dmin, near, x)
            if best is None:
                continue
            dist, loc, x = best
            if L["wall_end_gap"][0] < dist < L["wall_end_gap"][1]:
                mid = (end + loc) / 2
                if not any(all(o["bbox"][0][i] - 0.02 <= mid[i] <= o["bbox"][1][i] + 0.02 for i in range(3)) for o in openings):
                    add("error", "wall_gap", w["name"], f"{x['name']}와 벽 끝 사이에 {dist:.2f} m 틈이 있습니다(모서리가 뚫려 보임).")

    # --- 계단
    for st in by_role.get("stair", []):
        cand = [mb for mb in st["per_mesh"] if {"step", "tread", "steps"} & set(sa._name_tokens(mb[0].name))]
        steps = sorted(cand or st["per_mesh"], key=lambda mb: mb[1][1].z)
        if len(steps) < 3:
            add("warning", "stair_unanalyzable", st["name"], "단이 개별 메시가 아니라서 단 높이를 검사할 수 없습니다(단을 자식 메시로 나누세요).")
            continue
        tops = [bb[1].z for _, bb in steps]
        centers = [((bb[0] + bb[1]) / 2) for _, bb in steps]
        risers = [b - a for a, b in zip(tops, tops[1:])]
        treads = [math.hypot(b.x - a.x, b.y - a.y) for a, b in zip(centers, centers[1:])]
        base = _cast(ground_like, Vector((centers[0].x, centers[0].y, steps[0][1][0].z + 0.01)), Vector((0, 0, -1)), 5.0)
        if base is not None:
            risers.insert(0, tops[0] - base[0].z)
        if max(risers) - min(risers) > L["riser_spread"]:
            add("error", "stair_uneven_risers", st["name"],
                f"단 높이가 제각각입니다({min(risers):.3f}~{max(risers):.3f} m). 사람이 걸려 넘어지는 계단.")
        r_med = statistics.median(risers)
        t_med = statistics.median(treads) if treads else 0.0
        if not (L["riser"][0] <= r_med <= L["riser"][1]):
            add("warning", "stair_riser", st["name"], f"단 높이 {r_med:.3f} m (상식 범위 {L['riser'][0]}~{L['riser'][1]} m)")
        if treads and not (L["tread"][0] <= t_med <= L["tread"][1]):
            add("warning", "stair_tread", st["name"], f"단 너비 {t_med:.3f} m (상식 범위 {L['tread'][0]}~{L['tread'][1]} m)")
        if treads and not (L["blondel"][0] <= 2 * r_med + t_med <= L["blondel"][1]):
            add("warning", "stair_blondel", st["name"], f"2×단높이+단너비 = {2 * r_med + t_med:.3f} m (보폭 공식 0.55~0.70 m 밖)")
        last_top, last_c = tops[-1], centers[-1]
        landing = False
        for g in ground_like + [x for x in furniture if "landing" in sa._name_tokens(x["name"])]:
            gt = g["bbox"][1].z
            if last_top - 0.02 <= gt <= last_top + r_med + 0.03:
                gmin, gmax = g["bbox"]
                dx = max(gmin.x - last_c.x, 0, last_c.x - gmax.x)
                dy = max(gmin.y - last_c.y, 0, last_c.y - gmax.y)
                if math.hypot(dx, dy) < 1.0:
                    landing = True
                    break
        if not landing:
            add("error", "stair_to_nowhere", st["name"], "계단 맨 위가 어떤 바닥에도 이어지지 않습니다.")

    # --- 앉는 가구가 코앞의 벽을 보고 있음
    for fu in furniture:
        toks = sa._name_tokens(fu["name"])
        if not any(t in SEATING for t in toks) or any(t in sa.ACCESSORY_TOKENS for t in toks):
            continue
        f = fu["frame"]
        front = -f["ay"]
        start = Vector((f["center"].x, f["center"].y, fu["bbox"][0].z + 0.5))
        hit = _cast([x for x in solids + furniture if x is not fu], start, front, 5.0)
        if hit is not None and hit[2]["role"] in ("wall", "column"):
            gap = hit[1] - f["ey"] / 2
            if gap < L["seat_front_wall"]:
                add("warning", "seat_faces_wall", fu["name"], f"앉는 방향 {max(gap, 0):.2f} m 앞이 벽입니다(벽을 보고 앉는 배치).")

    # --- 종합: 백룸 위험도
    reasons = []
    hab = [r for r in rooms_out if r["type"] in ("habitable", "unknown")]
    if hab and sum(1 for r in hab if r["windows"] == 0) / len(hab) >= 0.5:
        reasons.append("생활 공간의 절반 이상에 창이 없음")
    if total_area > 0 and circ_area / total_area > L["corridor_fraction"]:
        reasons.append(f"복도 면적 비율 {circ_area / total_area:.0%}")
    if sum(1 for i in issues if i["code"] == "corridor_like_room") >= 2:
        reasons.append("복도처럼 길쭉한 방이 여러 개")
    if hab and sum(1 for r in hab if r["furniture"] == 0) / len(hab) >= 0.5:
        reasons.append("생활 공간의 절반 이상이 빈 방")
    if repeated:
        reasons.append("똑같은 빈 방의 반복")
    if any(i["code"] in ("sealed_room", "unreachable_room", "no_entrance") for i in issues):
        reasons.append("갈 수 없거나 밀폐된 방")
    if any(i["code"] in ("door_faces_wall", "door_to_void", "door_to_drop") for i in issues):
        reasons.append("어디로도 안 가는 문")
    risk = "high" if len(reasons) >= 3 else ("medium" if reasons else "low")

    report = {
        "rooms": rooms_out,
        "issues": issues,
        "summary": {
            "rooms": len(rooms_out), "doors": len(doors), "windows": len(windows), "walls": len(walls),
            "errors": sum(1 for i in issues if i["severity"] == "error"),
            "warnings": sum(1 for i in issues if i["severity"] == "warning"),
            "liminal_risk": risk, "liminal_reasons": reasons, "collection": collection,
        },
    }
    return report


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    collection, out = None, None
    for k, v in zip(argv[::2], argv[1::2]):
        if k == "--collection":
            collection = v
        elif k == "--out":
            out = v
    text = json.dumps(audit_building(collection=collection), ensure_ascii=False, indent=2)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
    print(text)


if __name__ != "building_audit":
    main()
