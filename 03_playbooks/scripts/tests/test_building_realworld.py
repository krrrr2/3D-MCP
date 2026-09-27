"""
building_audit.py 실전 패턴 테스트 — 실제 AI 생성 건물(Realsee×GPT-6 Astra, house-3d의 Fable·GPT-6)을
검사하며 오탐이 났던 구조를 작은 장면으로 재현한다. 정상 패턴은 아무것도 안 잡혀야 하고, 이상 패턴은 잡혀야 한다.

실행: bpyenv/bin/python 03_playbooks/scripts/tests/test_building_realworld.py
(검증 기록: 03_playbooks/scripts/validation/README.md)
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import bpy  # noqa: E402

import building_audit as ba  # noqa: E402
from test_building_audit import CH, FT, codes, floor, wall, xy_box  # noqa: E402
from test_scripts import box, reset  # noqa: E402

TOP = FT + CH


def boxes_mesh(name, rects, parent=None):
    """여러 상자를 '한 메시'로 합친 오브젝트 (three.js mergeGeometries·재질별 합치기와 같은 구조)."""
    verts, faces = [], []
    for x0, x1, y0, y1, z0, z1 in rects:
        b = len(verts)
        verts += [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        faces += [(b, b + 3, b + 2, b + 1), (b + 4, b + 5, b + 6, b + 7), (b, b + 1, b + 5, b + 4),
                  (b + 1, b + 2, b + 6, b + 5), (b + 2, b + 3, b + 7, b + 6), (b + 3, b, b + 4, b + 7)]
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.parent = parent
    return ob


def empty(name, parent=None, **props):
    ob = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(ob)
    ob.parent = parent
    for k, v in props.items():
        ob[k] = v
    return ob


def under(parent, *objs):
    for o in objs:
        o.parent = parent
    return objs[0] if len(objs) == 1 else objs


def wall_rects(x0, x1, y0, y1, holes=(), z0=FT, z1=TOP):
    """벽을 구멍 기준으로 나눈 상자들. holes = [(s0, s1, hz0, hz1)] (s 는 벽 긴 방향 좌표)."""
    along_x = (x1 - x0) >= (y1 - y0)
    a0, a1 = (x0, x1) if along_x else (y0, y1)

    def r(s0, s1, zz0, zz1):
        return (s0, s1, y0, y1, zz0, zz1) if along_x else (x0, x1, s0, s1, zz0, zz1)
    out, cur = [], a0
    for s0, s1, hz0, hz1 in sorted(holes):
        out.append(r(cur, s0, z0, z1))
        if hz0 > z0:
            out.append(r(s0, s1, z0, hz0))
        if hz1 < z1:
            out.append(r(s0, s1, hz1, z1))
        cur = s1
    out.append(r(cur, a1, z0, z1))
    return out


def audit():
    bpy.context.view_layer.update()
    return ba.audit_building()


def opening(rep, name):
    return next(o for o in rep["openings"] if o["name"] == name)


def rooms(rep):
    return {r["name"]: r for r in rep["rooms"]}


# ----------------------------------------------------------------------------- 정상 패턴

def test_merged_walls_in_container_groups():
    """벽 전체가 메시 하나 + house/structure/floors/openings 그룹 (glTF·three.js 가져오기 구조).
    문짝은 90° 열려 옆벽(남쪽 벽)에 붙어 있음 (Realsee 게임룸 문과 같은 상황)."""
    reset()
    house = empty("house")
    structure = empty("structure", house)
    floors = empty("floors", house)
    openings = empty("openings", house)
    furn = empty("furnishings", house)
    rects = (wall_rects(-0.1, 7.1, -0.1, 0, [(1.0, 2.2, FT + 0.9, FT + 2.1), (5.0, 6.2, FT + 0.9, FT + 2.1)])
             + wall_rects(-0.1, 7.1, 3.0, 3.1)
             + wall_rects(-0.1, 0, 0, 3.0, [(1.0, 2.0, FT, FT + 2.1)])
             + wall_rects(7.0, 7.1, 0, 3.0)
             + wall_rects(4.0, 4.1, 0, 3.0, [(0.1, 1.0, FT, FT + 2.1)]))
    boxes_mesh("walls", rects, structure)
    under(floors, floor("floor-living", 0, 4, 0, 3), floor("floor-bedroom", 4.1, 7, 0, 3))
    under(house, xy_box("ceiling_slab", -0.1, 7.1, -0.1, 3.1, TOP, TOP + 0.15))
    # 방 사이 문: 경첩 y=0.1, 침실 쪽으로 90° 열려 남쪽 벽 면(y=0)에 붙은 문짝
    d1 = empty("opening-d1", openings, role="door")
    under(d1, xy_box("leaf", 4.1, 5.0, 0.02, 0.06, FT, FT + 2.08))
    ent = empty("opening-entry", openings, role="door")
    under(ent, xy_box("leaf_entry", -0.07, -0.03, 1.02, 1.98, FT, FT + 2.08))
    for nm, x in (("opening-w1", 1.6), ("opening-w2", 5.6)):
        w = empty(nm, openings, role="window")
        under(w, xy_box(nm + "_glass", x - 0.58, x + 0.58, -0.06, -0.04, FT + 0.92, FT + 2.08))
    under(furn, box("sofa", (2.0, 0.9, 0.8), (2.0, 2.4, FT + 0.4)), box("bed", (1.6, 2.0, 0.5), (5.8, 2.0, FT + 0.25)))
    rep = audit()
    assert rep["summary"]["errors"] == 0 and rep["summary"]["warnings"] == 0, rep["issues"]
    d = opening(rep, "opening-d1")
    assert set(d["sides"]) == {"floor-living", "floor-bedroom"} and 0.8 <= d["width_m"] <= 0.95, d
    assert set(opening(rep, "opening-entry")["sides"]) == {"floor-living", "EXTERIOR"}
    rm = rooms(rep)
    assert rm["floor-living"]["doors"] == 2 and rm["floor-living"]["windows"] == 1, rm["floor-living"]
    assert rm["floor-bedroom"]["doors"] == 1 and rm["floor-bedroom"]["windows"] == 1, rm["floor-bedroom"]
    print("test_merged_walls_in_container_groups OK")


def two_rooms(mid_holes=(), south_holes_a=(), south_holes_b=()):
    """A(0~3) | B(3.1~6) 두 방, 벽은 따로따로. 남쪽 벽에 구멍 가능."""
    reset()
    floor("Floor_living", 0, 3, 0, 3)
    floor("Floor_bedroom", 3.1, 6, 0, 3)
    xy_box("Ceiling", -0.1, 6.1, -0.1, 3.1, TOP, TOP + 0.15)
    walls = {}
    for nm, rects in (("Wall_S_a", wall_rects(-0.1, 3.0, -0.1, 0, south_holes_a)),
                      ("Wall_S_b", wall_rects(3.0, 6.1, -0.1, 0, south_holes_b)),
                      ("Wall_N", wall_rects(-0.1, 6.1, 3.0, 3.1)),
                      ("Wall_W", wall_rects(-0.1, 0, 0, 3.0, [(1.0, 2.0, FT, FT + 2.1)])),
                      ("Wall_E", wall_rects(6.0, 6.1, 0, 3.0)),
                      ("Wall_mid", wall_rects(3.0, 3.1, 0, 3.0, mid_holes))):
        walls[nm] = boxes_mesh(nm, rects)
    box("Door_entry", (0.04, 0.96, 2.08), (-0.05, 1.5, FT + 1.04))
    box("sofa", (1.8, 0.8, 0.8), (1.5, 2.4, FT + 0.4))
    box("bed", (1.4, 2.0, 0.5), (4.8, 1.8, FT + 0.25))
    return walls


def test_sliding_door_parked_beside_opening():
    """두 짝 미닫이가 열린 채 구멍 옆에 겹쳐 주차 (house-3d GPT-6 욕실 문과 같은 구조)."""
    two_rooms(mid_holes=[(1.0, 1.8, FT, FT + 2.1)], south_holes_a=[(1.0, 2.2, FT + 0.9, FT + 2.1)],
              south_holes_b=[(4.0, 5.2, FT + 0.9, FT + 2.1)])
    sl = empty("Door_bath_sliding")
    under(sl, xy_box("leaf_1", 3.12, 3.16, 1.81, 2.23, FT, FT + 2.1), xy_box("leaf_2", 3.18, 3.22, 1.82, 2.24, FT, FT + 2.1))
    box("Window_a", (1.16, 0.02, 1.16), (1.6, -0.05, FT + 1.5))
    box("Window_b", (1.16, 0.02, 1.16), (4.6, -0.05, FT + 1.5))
    rep = audit()
    d = opening(rep, "Door_bath_sliding")
    assert set(d["sides"]) == {"Floor_living", "Floor_bedroom"} and 0.7 <= d["width_m"] <= 0.9, d
    assert not codes(rep, "Door_bath_sliding"), codes(rep, "Door_bath_sliding")
    print("test_sliding_door_parked_beside_opening OK")


def test_curtain_window_and_bay_window():
    """창 오브젝트에 바닥까지 내려오는 커튼이 포함 + 창턱 의자(베이창·飘窗) 바깥쪽 끝에 있는 창."""
    reset()
    floor("Floor_bedroom", 0, 4, 0, 4)
    xy_box("Ceiling", -0.1, 4.9, -0.1, 4.1, TOP, TOP + 0.15)
    boxes_mesh("Wall_S", wall_rects(-0.1, 4.1, -0.1, 0, [(1.4, 2.6, FT + 0.9, FT + 2.1)]))
    boxes_mesh("Wall_N", wall_rects(-0.1, 4.1, 4.0, 4.1))
    boxes_mesh("Wall_W", wall_rects(-0.1, 0, 0, 4.0, [(1.5, 2.4, FT, FT + 2.1)]))
    boxes_mesh("Wall_E", wall_rects(4.0, 4.1, 0, 4.0, [(1.0, 3.0, FT + 0.45, FT + 2.1)]))       # 베이 쪽으로 뚫린 벽
    boxes_mesh("Wall_bay_sides", [(4.1, 4.8, 0.9, 1.0, FT, TOP), (4.1, 4.8, 3.0, 3.1, FT, TOP)])
    boxes_mesh("Wall_bay_outer", wall_rects(4.7, 4.8, 1.0, 3.0, [(1.0, 3.0, FT + 0.45, FT + 2.1)]))
    box("bay_seat", (0.6, 2.0, 0.45), (4.4, 2.0, FT + 0.225))                                    # 걸터앉는 턱 = 가구
    box("Door_room", (0.04, 0.86, 2.08), (-0.05, 1.95, FT + 1.04))
    w = empty("Window_south")
    under(w, xy_box("glass", 1.42, 2.58, -0.06, -0.04, FT + 0.92, FT + 2.08),
          xy_box("curtain", 1.2, 2.8, 0.12, 0.16, FT + 0.01, FT + 2.35))                          # 바닥까지 내린 커튼
    box("Window_bay", (0.02, 1.96, 1.61), (4.75, 2.0, FT + 0.45 + 0.825))
    box("bed", (1.6, 2.0, 0.5), (2.6, 2.6, FT + 0.25))
    rep = audit()
    s = opening(rep, "Window_south")
    assert 0.85 <= s["sill_m"] <= 0.95, s
    b = opening(rep, "Window_bay")
    assert "Floor_bedroom" in b["sides"] and 0.4 <= b["sill_m"] <= 0.5, b
    assert rooms(rep)["Floor_bedroom"]["windows"] == 2, rooms(rep)["Floor_bedroom"]
    bad = codes(rep) - {"wall_gap"}          # 베이 옆벽 끝 처리는 이 테스트의 관심사가 아님
    assert not bad, rep["issues"]
    print("test_curtain_window_and_bay_window OK")


def test_glazed_balcony_door_counts_as_daylight():
    """창은 없고 발코니로 난 유리 미닫이만 있는 거실 = 창 없는 방이 아니다 (Fable 거실)."""
    reset()
    floor("Floor_living", 0, 4, 0, 3)
    floor("Floor_balcony", 0, 4, -1.6, -0.2)
    xy_box("Ceiling", -0.1, 4.1, -1.7, 3.1, TOP, TOP + 0.15)
    boxes_mesh("Wall_S", wall_rects(-0.1, 4.1, -0.2, 0, [(0.8, 3.2, FT, FT + 2.2)]))
    boxes_mesh("Wall_N", wall_rects(-0.1, 4.1, 3.0, 3.1))
    boxes_mesh("Wall_W", wall_rects(-0.1, 0, 0, 3.0, [(1.0, 2.0, FT, FT + 2.1)]))
    boxes_mesh("Wall_E", wall_rects(4.0, 4.1, 0, 3.0))
    box("railing_balcony", (4.0, 0.05, 1.1), (2.0, -1.62, FT + 0.55))
    d = empty("Door_balcony")
    g = under(d, xy_box("glass", 0.82, 3.18, -0.11, -0.09, FT + 0.02, FT + 2.18))
    mat = bpy.data.materials.new("Glass")
    g.data.materials.append(mat)
    box("Door_entry", (0.04, 0.96, 2.08), (-0.05, 1.5, FT + 1.04))
    box("sofa", (2.0, 0.9, 0.8), (2.0, 2.4, FT + 0.4))
    box("lounge_chair", (0.7, 0.7, 0.8), (3.4, -1.1, FT + 0.4))
    rep = audit()
    liv = rooms(rep)["Floor_living"]
    assert liv["glazed_doors_to_outside"] == ["Door_balcony"] and "windowless_room" not in codes(rep, "Floor_living"), liv
    assert "door_size" not in codes(rep, "Door_balcony"), codes(rep, "Door_balcony")      # 2.4 m 유리 미닫이는 정상
    print("test_glazed_balcony_door_counts_as_daylight OK")


def test_korean_chinese_names():
    """이름이 한국어·중국어인 장면: 끝 단어가 핵심 (창가_소파 = 소파, 양문냉장고 = 냉장고, 窗边绿植 = 화분)."""
    reset()
    cases = {"거실 · 바닥": "floor", "침실_바닥": "floor", "현관문": "door", "안방문": "door", "거실_창문": "window",
             "외벽_남": "wall", "창가_소파": "furniture", "양문냉장고": "furniture", "벽걸이_시계": "furniture",
             "主卧 · 地坪": "floor", "bathroom-west · 密封上吊移门": "door", "细金属框玻璃窗": "window",
             "次卧2窗边绿植": "furniture", "哑光平板双门冰箱": "furniture", "客厅极简落地帘": "furniture",
             "主卧 · 天花": "ceiling", "法式铁艺阳台栏杆": "railing", "合批 · wall": "wall"}
    for nm, want in cases.items():
        ob = bpy.data.objects.new(nm, None)
        got = ba._role(ob)
        assert got == want, (nm, want, got)
    assert ba._room_type(bpy.data.objects.new("阳台 · 地坪", None)) == "outdoor"
    assert ba._room_type(bpy.data.objects.new("화장실_바닥", None)) == "service"
    print("test_korean_chinese_names OK")


def test_furniture_parts_named_like_structure():
    """가구 조립품 속 'InnerWall'·'GoalDoor'·'cabinet_door' 부품은 벽·문이 아니다 (Realsee 푸스볼 테이블)."""
    two_rooms(mid_holes=[(1.0, 1.9, FT, FT + 2.1)], south_holes_a=[(1.0, 2.2, FT + 0.9, FT + 2.1)],
              south_holes_b=[(4.0, 5.2, FT + 0.9, FT + 2.1)])
    box("Door_mid", (0.04, 0.88, 2.08), (3.05, 1.45, FT + 1.04))
    box("Window_a", (1.16, 0.02, 1.16), (1.6, -0.05, FT + 1.5))
    box("Window_b", (1.16, 0.02, 1.16), (4.6, -0.05, FT + 1.5))
    fb = empty("Foosball_table")
    under(fb, box("Foosball.InnerWall.1", (1.2, 0.02, 0.2), (1.5, 0.55, FT + 0.8)),
          box("Foosball.GoalDoor", (0.02, 0.2, 0.1), (0.9, 0.8, FT + 0.8)),
          box("Foosball.Body", (1.3, 0.7, 0.8), (1.5, 0.8, FT + 0.4)))
    cab = empty("Kitchen_cabinet")
    under(cab, box("cabinet_body", (1.0, 0.5, 0.9), (4.6, 2.6, FT + 0.45)), box("cabinet_door_L", (0.5, 0.02, 0.8), (4.35, 2.34, FT + 0.45)))
    rep = audit()
    assert rep["summary"]["doors"] == 2 and rep["summary"]["walls"] == 6, rep["summary"]
    assert rep["summary"]["errors"] == 0, rep["issues"]
    print("test_furniture_parts_named_like_structure OK")


def test_open_grid_ceiling_hides_plenum():
    """오픈 셀 격자 천장(가는 막대 여러 개) 위의 설비 공간 틈은 안 보인다 (Realsee 바)."""
    reset()
    floor("Floor_bar", 0, 4, 0, 4)
    for nm, rects in (("Wall_S", wall_rects(-0.1, 4.1, -0.1, 0)), ("Wall_N", wall_rects(-0.1, 4.1, 4.0, 4.1)),
                      ("Wall_W", wall_rects(-0.1, 0, 0, 4.0, [(1.5, 2.4, FT, FT + 2.1)])), ("Wall_E", wall_rects(4.0, 4.1, 0, 4.0)),
                      ("Wall_mid", wall_rects(2.0, 2.1, 2.5, 4.0))):
        boxes_mesh(nm, rects)
    grid = bpy.data.collections.new("Bar_Observed_Open_Ceiling_Grid")
    bpy.context.scene.collection.children.link(grid)
    for i in range(14):
        for nm, rect in ((f"GRID_x_{i}", (0, 4, 0.1 + i * 0.3, 0.12 + i * 0.3)), (f"GRID_y_{i}", (0.1 + i * 0.3, 0.12 + i * 0.3, 0, 4))):
            ob = xy_box(nm, *rect, TOP - 0.05, TOP)
            for c in ob.users_collection:
                c.objects.unlink(ob)
            grid.objects.link(ob)
    xy_box("Ceiling_dark_plenum", -0.1, 4.1, -0.1, 4.1, TOP + 0.4, TOP + 0.45)
    box("Door_entry", (0.04, 0.86, 2.08), (-0.05, 1.95, FT + 1.04))
    box("bar_table", (0.8, 0.8, 0.75), (1.0, 1.0, FT + 0.375))
    box("Window_bar", (1.0, 0.02, 1.0), (3.0, -0.05, FT + 1.5))
    rep = audit()
    assert not any(i["code"] == "wall_short_of_ceiling" for i in rep["issues"]), rep["issues"]
    ch = rooms(rep)["Floor_bar"]["ceiling_h_m"]
    assert ch is not None and CH - 0.1 <= ch <= CH, ch
    print("test_open_grid_ceiling_hides_plenum OK")


def test_stepped_bay_wall_is_not_a_hole():
    """아래는 벽, 위는 안쪽으로 물러난 계단식 벽(턱 위 선반) = 유리 없는 창 구멍이 아니다 (Realsee 거실 베이)."""
    reset()
    floor("Floor_living", 0, 4, 0, 4)
    xy_box("Ceiling", -0.1, 4.1, -0.1, 4.1, TOP, TOP + 0.15)
    boxes_mesh("Wall_S", wall_rects(-0.1, 4.1, -0.1, 0, [(1.4, 2.6, FT + 0.9, FT + 2.1)]))
    boxes_mesh("Wall_N", wall_rects(-0.1, 4.1, 4.0, 4.1))
    boxes_mesh("Wall_E", wall_rects(4.0, 4.1, 0, 4.0, [(1.5, 2.4, FT, FT + 2.1)]))
    boxes_mesh("Wall_W_lower", [(-0.1, 0, 0, 4.0, FT, 1.6)])
    boxes_mesh("Wall_W_upper", [(0.2, 0.3, 0, 4.0, 1.6, TOP)])
    boxes_mesh("Wall_W_ledge", [(0, 0.2, 0, 4.0, 1.59, 1.6)])
    box("Door_entry", (0.04, 0.86, 2.08), (4.05, 1.95, FT + 1.04))
    box("Window_s", (1.16, 0.02, 1.16), (2.0, -0.05, FT + 1.5))
    box("sofa", (2.0, 0.9, 0.8), (2.0, 2.4, FT + 0.4))
    rep = audit()
    liv = rooms(rep)["Floor_living"]
    assert not liv["glassless_window_openings"] and "room_edge_open" not in codes(rep, "Floor_living"), (liv, rep["issues"])
    print("test_stepped_bay_wall_is_not_a_hole OK")


# ----------------------------------------------------------------------------- 이상 패턴

def test_desk_half_blocks_door_and_wardrobe_covers_window():
    """책상이 문 폭 절반을 막음(좁은 통로), 책장이 문 전체를 막음(막힘), 옷장이 창을 가림, 수전만 있는 창은 정상."""
    two_rooms(mid_holes=[(1.0, 2.2, FT, FT + 2.1)], south_holes_a=[(1.0, 2.2, FT + 0.9, FT + 2.1)],
              south_holes_b=[(4.0, 5.2, FT + 0.9, FT + 2.1)])
    box("Door_double", (0.04, 1.16, 2.08), (3.05, 1.6, FT + 1.04))                   # 양개문 1.2 m
    box("Window_a", (1.16, 0.02, 1.16), (1.6, -0.05, FT + 1.5))
    box("Window_b", (1.16, 0.02, 1.16), (4.6, -0.05, FT + 1.5))
    box("desk", (0.6, 0.7, 0.75), (3.5, 1.85, FT + 0.375))                              # 문 앞 0.2 m, 폭 0.7 가림 → 남은 폭 0.5
    box("wardrobe", (1.1, 0.6, 2.0), (4.6, 0.35, FT + 1.0))                              # 창 앞을 막는 옷장
    box("faucet", (0.05, 0.05, 0.3), (1.6, 0.25, FT + 1.05))                             # 창 앞 수전 = 가림 아님
    rep = audit()
    assert "door_narrow" in codes(rep, "Door_double"), rep["issues"]
    assert "window_blocked" in codes(rep, "Window_b") and "window_blocked" not in codes(rep, "Window_a"), rep["issues"]
    # 책장이 문 전체를 막으면 오류
    box("bookcase", (0.4, 1.4, 2.0), (3.35, 1.6, FT + 1.0))
    rep = audit()
    assert "door_blocked" in codes(rep, "Door_double"), rep["issues"]
    print("test_desk_half_blocks_door_and_wardrobe_covers_window OK")


def test_door_without_hole_in_merged_walls():
    """벽이 한 메시로 합쳐진 장면에서도 구멍 없는 문은 잡는다."""
    reset()
    boxes_mesh("walls", wall_rects(-0.1, 6.1, -0.1, 0) + wall_rects(-0.1, 6.1, 3.0, 3.1) + wall_rects(-0.1, 0, 0, 3.0)
               + wall_rects(6.0, 6.1, 0, 3.0) + wall_rects(3.0, 3.1, 0, 3.0))
    floor("Floor_a", 0, 3, 0, 3)
    floor("Floor_b", 3.1, 6, 0, 3)
    xy_box("Ceiling", -0.1, 6.1, -0.1, 3.1, TOP, TOP + 0.15)
    box("Door_fake", (0.04, 0.86, 2.08), (3.05, 1.5, FT + 1.04))
    rep = audit()
    assert "opening_not_cut" in codes(rep, "Door_fake"), rep["issues"]
    assert {"sealed_room"} <= codes(rep, "Floor_a") and {"sealed_room"} <= codes(rep, "Floor_b"), rep["issues"]
    print("test_door_without_hole_in_merged_walls OK")


def test_nothing_recognized_is_not_a_pass():
    """이름이 Plane·Cube 뿐이라 아무것도 못 알아보면 '오류 0'이 아니라 경고를 낸다 (v1 은 GLB 장면에서 조용히 통과했음)."""
    reset()
    box("Plane", (6, 4, 0.02), (3, 2, 0.01))
    box("Cube", (6, 0.1, 2.4), (3, -0.05, 1.2))
    box("Cube.001", (0.1, 4, 2.4), (-0.05, 2, 1.2))
    rep = audit()
    assert "no_rooms_found" in codes(rep), rep["issues"]
    print("test_nothing_recognized_is_not_a_pass OK")


if __name__ == "__main__":
    test_merged_walls_in_container_groups()
    test_sliding_door_parked_beside_opening()
    test_curtain_window_and_bay_window()
    test_glazed_balcony_door_counts_as_daylight()
    test_korean_chinese_names()
    test_furniture_parts_named_like_structure()
    test_open_grid_ceiling_hides_plenum()
    test_stepped_bay_wall_is_not_a_hole()
    test_desk_half_blocks_door_and_wardrobe_covers_window()
    test_door_without_hole_in_merged_walls()
    test_nothing_recognized_is_not_a_pass()
    print("ALL REAL-WORLD PATTERN TESTS PASSED on Blender", bpy.app.version_string)
