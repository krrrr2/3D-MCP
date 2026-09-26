"""
scripts/ 의 보조 스크립트 자동 테스트.

실행 (Blender 없이 pip 의 bpy 모듈로):
  python -m venv bpyenv && bpyenv/bin/pip install bpy==5.0.1
  bpyenv/bin/python 03_playbooks/scripts/tests/test_scripts.py
또는 Blender 로:
  blender -b --python 03_playbooks/scripts/tests/test_scripts.py
"""

import math
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

import placement_utils as pu  # noqa: E402
import review_views as rv  # noqa: E402
import scene_audit as sa  # noqa: E402


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def box(name, size, loc, parent=None):
    """size=(x,y,z) m, loc=박스 중심. 스케일이 아니라 정점 좌표로 크기를 만든다(스케일 적용 상태)."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    o = bpy.context.active_object
    o.name = name
    for v in o.data.vertices:
        v.co = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
    o.location = loc
    if parent is not None:
        o.parent = parent
    mat = bpy.data.materials.get("M") or bpy.data.materials.new("M")
    o.data.materials.append(mat)
    return o


def empty(name, loc=(0, 0, 0)):
    e = bpy.data.objects.new(name, None)
    e.location = loc
    bpy.context.scene.collection.objects.link(e)
    return e


def table(name, x=0.0, y=0.0, z0=0.0, w=1.6, d=0.9, h=0.75, top=0.04):
    root = empty(name, (x, y, z0))
    box(name + "_top", (w, d, top), (0, 0, h - top / 2), root)
    leg_h = h - top
    for i, (sx, sy) in enumerate([(1, 1), (1, -1), (-1, 1), (-1, -1)]):
        box(f"{name}_leg{i}", (0.05, 0.05, leg_h), (sx * (w / 2 - 0.05), sy * (d / 2 - 0.05), leg_h / 2), root)
    return root


def chair(name, x=0.0, y=0.0, z0=0.0):
    root = empty(name, (x, y, z0))
    box(name + "_seat", (0.45, 0.45, 0.04), (0, 0, 0.45), root)
    box(name + "_back", (0.45, 0.04, 0.45), (0, 0.205, 0.695), root)
    for i, (sx, sy) in enumerate([(1, 1), (1, -1), (-1, 1), (-1, -1)]):
        box(f"{name}_leg{i}", (0.04, 0.04, 0.43), (sx * 0.2, sy * 0.2, 0.215), root)
    return root


def units_by_name(report):
    return {u["name"]: u for u in report["units"]}


def test_audit_detects_problems():
    reset()
    box("Floor", (10, 10, 0.02), (0, 0, -0.01))
    table("DiningTable", 0, 0)
    chair("Chair_ok", 0, -0.8)
    chair("Chair_floating", 1.2, -0.8, z0=0.1)
    box("Box_intersect", (0.3, 0.3, 0.3), (0.0, 0.0, 0.75))          # 상판을 관통
    box("Sofa_bad", (2.0, 2.5, 0.85), (3.0, 3.0, 0.425))              # 깊이 2.5m: 비정상
    s = box("Scaled_thing", (0.2, 0.2, 0.2), (-3.0, 0.0, 0.1))
    s.scale = (2.0, 1.0, 1.0)
    bpy.context.view_layer.update()

    rep = sa.audit_scene(floor_z=0.0)
    u = units_by_name(rep)
    assert not u["DiningTable"]["issues"] or all(not i.startswith(("floating", "size")) for i in u["DiningTable"]["issues"]), u["DiningTable"]
    assert "floating_or_wall_mounted" not in u["Chair_ok"]["issues"], u["Chair_ok"]
    assert "floating_or_wall_mounted" in u["Chair_floating"]["issues"], u["Chair_floating"]
    assert any(i.startswith("size_out_of_range:sofa.y") for i in u["Sofa_bad"]["issues"]), u["Sofa_bad"]
    assert any(i.startswith("unapplied_scale") for i in u["Scaled_thing"]["issues"]), u["Scaled_thing"]
    pairs = {(p["a"], p["b"]) for p in rep["interpenetrations"]}
    assert ("DiningTable", "Box_intersect") in pairs or ("Box_intersect", "DiningTable") in pairs, rep["interpenetrations"]
    # 의자를 테이블 아래로 넣어도(바운딩박스는 겹치지만 면은 교차 안 함) 관통으로 잡으면 안 된다
    assert not any("Chair_ok" in (p["a"], p["b"]) for p in rep["interpenetrations"]), rep["interpenetrations"]
    print("test_audit_detects_problems OK")


def test_placement_fixes():
    reset()
    box("Floor", (10, 10, 0.02), (0, 0, -0.01))
    t = table("Desk", 0, 0)
    c = chair("Chair_floating", 2.0, 0.0, z0=0.3)
    lamp = box("Lamp", (0.15, 0.15, 0.4), (0.3, 0.1, 1.5))
    bpy.context.view_layer.update()

    pu.snap_to_floor(c, 0.0)
    mn, _ = pu.world_bbox(c)
    assert abs(mn.z) < 1e-6, mn

    support = pu.drop_to_surface(lamp)
    mn, _ = pu.world_bbox(lamp)
    assert support == "Desk_top", support
    assert abs(mn.z - 0.75) < 1e-4, mn
    # 이미 표면 위에 있을 때 다시 호출해도 표면을 뚫고 내려가면 안 된다
    assert pu.drop_to_surface(lamp) == "Desk_top"
    mn, _ = pu.world_bbox(lamp)
    assert abs(mn.z - 0.75) < 1e-4, mn

    pu.place_next_to(c, t, side="-Y", gap=0.10)
    assert abs(pu.xy_clearance(c, t) - 0.10) < 1e-4, pu.xy_clearance(c, t)

    pu.face_towards(c, (0.0, 0.0, 0.0))
    # 의자 앞면(-Y)이 원점(테이블) 쪽을 향해야 한다: 의자는 테이블 -Y 쪽에 있으므로 앞면은 +Y 를 봐야 함
    fwd = c.matrix_world.to_3x3() @ Vector((0, -1, 0))
    to_target = (Vector((0, 0, 0)) - c.matrix_world.translation)
    to_target.z = 0
    assert fwd.normalized().dot(to_target.normalized()) > 0.999, (fwd, to_target)

    rep = sa.audit_scene(floor_z=0.0)
    u = units_by_name(rep)
    assert "floating_or_wall_mounted" not in u["Chair_floating"]["issues"], u["Chair_floating"]
    assert "floating_or_wall_mounted" not in u["Lamp"]["issues"], u["Lamp"]

    v = pu.check_clearances([("Chair_floating", "Desk", 0.3)])
    assert v and v[0]["clearance_m"] == 0.1, v
    print("test_placement_fixes OK")


def test_review_renders():
    reset()
    box("Floor", (4, 4, 0.02), (0, 0, -0.01))
    table("Table", 0, 0)
    with tempfile.TemporaryDirectory(prefix="review_") as out:
        paths = rv.render_review_views(out, engine="CYCLES", samples=2, res=128)
        assert len(paths) == 4 and all(os.path.getsize(p) > 0 for p in paths), paths
    # 임시 카메라/조명/월드/재질이 남지 않아야 한다
    assert not any(o.name.startswith("_REVIEW_") for o in bpy.data.objects)
    assert not any(m.name.startswith("_REVIEW_") for m in bpy.data.materials)
    assert bpy.context.view_layer.material_override is None
    print("test_review_renders OK")


if __name__ == "__main__":
    test_audit_detects_problems()
    test_placement_fixes()
    test_review_renders()
    print("ALL TESTS PASSED on Blender", bpy.app.version_string)
