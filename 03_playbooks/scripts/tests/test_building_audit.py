"""
building_audit.py 테스트: 정상적인 집은 아무것도 안 잡히고, 백룸처럼 이상한 집은 넣어 둔 기묘함이 모두 잡혀야 한다.

실행: bpyenv/bin/python 03_playbooks/scripts/tests/test_building_audit.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import bpy  # noqa: E402

import building_audit as ba  # noqa: E402
from test_scripts import box, reset  # noqa: E402

FT, CH, T = 0.02, 2.4, 0.1      # 바닥 윗면, 천장고, 벽 두께


def xy_box(name, x0, x1, y0, y1, z0, z1):
    return box(name, (x1 - x0, y1 - y0, z1 - z0), ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))


def floor(name, x0, x1, y0, y1, top=FT):
    return xy_box(name, x0, x1, y0, y1, top - 0.02, top)


def wall(name, x0, x1, y0, y1, z0=FT, z1=FT + CH):
    return xy_box(name, x0, x1, y0, y1, z0, z1)


def cut(w, center, size):
    c = box("_cutter_" + w.name + str(len(w.modifiers)), size, center)
    c.hide_set(True)
    c.hide_render = True
    m = w.modifiers.new("cut", "BOOLEAN")
    m.operation = "DIFFERENCE"
    m.object = c
    m.solver = "EXACT"


def door(name, w, x, y, along_x=True, z0=FT, width=0.9, height=2.1, do_cut=True):
    size = (width, 0.04, height) if along_x else (0.04, width, height)
    d = box(name, size, (x, y, z0 + height / 2))
    if do_cut:
        cut(w, (x, y, z0 + height / 2), (width, 0.4, height) if along_x else (0.4, width, height))
    return d


def window(name, w, x, y, sill, width=1.2, height=1.2, along_x=True, base=FT):
    z = base + sill + height / 2
    size = (width, 0.03, height) if along_x else (0.03, width, height)
    o = box(name, size, (x, y, z))
    cut(w, (x, y, z), (width, 0.4, height) if along_x else (0.4, width, height))
    return o


def codes(rep, obj=None):
    return {i["code"] for i in rep["issues"] if obj is None or i["object"] == obj}


def build_good_house():
    reset()
    box("Ground", (60, 60, 0.02), (4, 3, -0.01))
    floor("Floor_living", 0, 5, 0, 4)
    floor("Floor_bedroom", 5.1, 8.6, 0, 4)
    floor("Floor_bathroom", 5.1, 8.6, 4.1, 6.1)
    floor("Floor_hall", 0, 5, 4.1, 6.1)
    xy_box("Ceiling", -0.1, 8.7, -0.1, 6.2, FT + CH, FT + CH + 0.15)      # 15 cm 두께 슬래브
    ws = wall("Wall_S", -0.1, 8.7, -0.1, 0)
    wall("Wall_N", -0.1, 8.7, 6.1, 6.2)
    wall("Wall_W", -0.1, 0, 0, 6.1)
    we = wall("Wall_E", 8.6, 8.7, 0, 6.1)
    wx = wall("Wall_mid_x", 5, 5.1, 0, 6.1)
    wya = wall("Wall_mid_y_a", 0, 5, 4, 4.1)
    wall("Wall_mid_y_b", 5.1, 8.6, 4, 4.1)
    door("door_entrance", ws, 2.5, -0.05)
    door("door_living_hall", wya, 0.8, 4.05)
    door("door_living_bedroom", wx, 5.05, 2.0, along_x=False)
    door("door_hall_bath", wx, 5.05, 5.1, along_x=False)
    window("window_living_1", ws, 1.0, -0.05, 0.9)
    window("window_living_2", ws, 4.0, -0.05, 0.9)
    window("window_bedroom", we, 8.65, 2.0, 0.9, along_x=False)
    window("window_bath", we, 8.65, 5.1, 1.5, width=0.6, height=0.6, along_x=False)
    box("sofa_3seat", (2.1, 0.9, 0.85), (2.5, 3.4, FT + 0.425))
    box("coffee_table", (1.0, 0.5, 0.42), (2.5, 2.3, FT + 0.21))
    box("bed", (1.6, 2.1, 0.5), (7.4, 1.5, FT + 0.25))
    box("toilet", (0.4, 0.7, 0.8), (8.0, 5.6, FT + 0.4))
    box("console_table", (1.0, 0.35, 0.8), (3.5, 5.9, FT + 0.4))
    # 정상 계단: 단높이 0.17 × 3단 + 4번째 단 = 테라스(0.68), 단너비 0.28
    st = bpy.data.objects.new("stairs_garden", None)
    bpy.context.scene.collection.objects.link(st)
    for i in range(3):
        top = 0.17 * (i + 1)
        s = box(f"stairs_garden_step_{i}", (1.0, 0.28, top), (12 + 0.28 * i, 1.0, top / 2))
        s.parent = st
    floor("Floor_terrace", 12.7, 15.0, 0.5, 1.5, top=0.68)
    bpy.context.view_layer.update()


def build_weird_house():
    reset()
    box("Ground", (140, 60, 0.02), (25, 0, -0.01))
    xy_box("Ceiling", -0.1, 16.2, -3.2, 2.2, FT + CH, FT + CH + 0.15)
    floor("Floor_bedroom", 0, 4, 0, 4)
    floor("Floor_room_9", 4.1, 16.1, 0, 2)                        # 12 × 2 m 길쭉한 빈 방
    for i, x0 in enumerate((4.1, 7.2, 10.3), 1):
        floor(f"Floor_room_{i}", x0, x0 + 3, -3.1, -0.1)            # 똑같은 빈 방 3개
    floor("Floor_study", 0, 4, -3.1, -0.1)                          # 문 없는 방
    wa_w = wall("Wall_A_W", -0.1, 0, 0, 4)
    wa_n = wall("Wall_A_N", 0, 4, 4, 4.1)
    wad = wall("Wall_AD", 0, 4, -0.1, 0)
    wab = wall("Wall_AB", 4, 4.1, 0, 4)
    wbn = wall("Wall_B_N", 4.1, 16.1, 2, 2.1)
    wbc = wall("Wall_BC", 4.1, 13.3, -0.1, 0)
    wall("Wall_blocker", 9, 11, 2.5, 2.6)
    wall("Wall_blocker_2", 13.3, 14.7, 2.5, 2.6)
    wall("Wall_short", 14, 16, 1, 1.1, z1=FT + CH - 0.3)              # 천장까지 안 닿는 벽
    wall("Wall_crack_1", 30, 33, 0, 0.1)
    wall("Wall_crack_2", 33.1, 36, 0, 0.1)                           # 10 cm 틈
    door("door_entrance", wa_w, -0.05, 2.0, along_x=False, do_cut=False)   # 벽에 구멍 안 뚫음
    door("door_ab", wab, 4.05, 1.0, along_x=False, z0=FT + 0.3)            # 30 cm 떠 있는 문
    door("door_b_north", wbn, 10.0, 2.05)                                  # 열면 40 cm 앞이 벽
    for i, x in enumerate((5.6, 8.7, 11.8), 1):
        door(f"door_c{i}", wbc, x, -0.05)
    window("window_a1", wa_n, 1.0, 4.05, 0.9)
    window("window_a2", wa_n, 3.0, 4.05, 0.1, height=0.9)                 # 어정쩡한 창턱 + 높이 제각각
    window("window_ad", wad, 2.0, -0.05, 0.9)                              # 방↔방 실내 창
    window("window_b", wbn, 14.0, 2.05, 0.9)                               # 창 바로 앞이 벽
    box("wardrobe", (1.0, 0.6, 2.0), (1.0, 3.6, FT + 1.0))                  # 창 가림
    box("sofa_2seat", (1.6, 0.8, 0.8), (2.0, 0.6, FT + 0.4))               # 20 cm 앞 벽을 보고 앉음
    st = bpy.data.objects.new("stairs_broken", None)
    bpy.context.scene.collection.objects.link(st)
    for i, top in enumerate((0.17, 0.42, 0.54)):
        s = box(f"stairs_broken_step_{i}", (1.0, 0.3, top), (40 + 0.3 * i, 0, top / 2))
        s.parent = st
    floor("Floor_loft", 50, 54, 0, 4, top=3.02)
    wl = wall("Wall_loft", 54, 54.1, 0, 4, z0=3.02, z1=5.42)
    door("door_loft", wl, 54.05, 2.0, along_x=False, z0=3.02)              # 3 m 낭떠러지로 나가는 문
    bpy.context.view_layer.update()


def test_good_house():
    build_good_house()
    rep = ba.audit_building()
    assert rep["summary"]["errors"] == 0 and rep["summary"]["warnings"] == 0, rep["issues"]
    assert rep["summary"]["liminal_risk"] == "low", rep["summary"]
    rooms = {r["name"]: r for r in rep["rooms"]}
    assert rooms["Floor_living"]["doors"] == 3 and rooms["Floor_living"]["windows"] == 2, rooms["Floor_living"]
    assert abs(rooms["Floor_living"]["ceiling_h_m"] - CH) < 0.01
    print("test_good_house OK")


def test_weird_house():
    build_weird_house()
    rep = ba.audit_building()
    expect = {
        "door_entrance": {"opening_not_cut"},
        "door_ab": {"door_floating"},
        "door_b_north": {"door_faces_wall"},
        "door_loft": {"door_to_drop"},
        "window_a2": {"window_awkward_sill", "window_misaligned"},
        "window_a1": {"window_blocked"},
        "window_ad": {"interior_window"},
        "window_b": {"window_faces_wall"},
        "Floor_study": {"sealed_room", "empty_room"},
        "Floor_room_9": {"corridor_like_room", "empty_room"},
        "Floor_room_1": {"windowless_room", "empty_room"},
        "Wall_short": {"wall_short_of_ceiling"},
        "Wall_crack_1": {"wall_gap"},
        "stairs_broken": {"stair_uneven_risers", "stair_to_nowhere"},
        "sofa_2seat": {"seat_faces_wall"},
    }
    for obj, want in expect.items():
        got = codes(rep, obj)
        assert want <= got, (obj, want, got)
    assert any(i["code"] == "repetitive_empty_rooms" for i in rep["issues"])
    assert rep["summary"]["liminal_risk"] == "high", rep["summary"]
    # 정상 요소는 잡으면 안 된다
    for obj in ("door_c1", "door_c2", "Wall_AB", "Wall_BC", "window_b"):
        bad = codes(rep, obj) - {"window_faces_wall"}
        assert not bad, (obj, bad)
    print("test_weird_house OK — 백룸 위험도:", rep["summary"]["liminal_risk"], rep["summary"]["liminal_reasons"])


if __name__ == "__main__":
    test_good_house()
    test_weird_house()
    print("ALL BUILDING TESTS PASSED on Blender", bpy.app.version_string)
