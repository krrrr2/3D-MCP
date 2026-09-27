"""검사 결과를 눈으로 확인하기 위한 평면도 렌더 (천장·지붕 숨김, 역할별 색: 벽 검정·문 빨강·창 파랑·가구 무작위).

사용: python render_plan.py -- scene.blend out.png <중심 x> <중심 y> <보이는 폭 m> [자를 높이 m=2.3]
GPU 없는 서버에서도 되도록 Cycles CPU 로 그린다 (EEVEE·Workbench 는 EGL 필요).
"""
import os
import random
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import building_audit as ba  # noqa: E402

args = sys.argv[sys.argv.index("--") + 1:]
bpy.ops.wm.open_mainfile(filepath=args[0])
out = os.path.abspath(args[1])
cx, cy, span = float(args[2]), float(args[3]), float(args[4])
cut = float(args[5]) if len(args) > 5 else 2.3
sc = bpy.context.scene

for o in sc.objects:                       # 평면도: 천장·지붕·자를 높이 위는 숨김
    if o.type != "MESH":
        continue
    root = o
    while root.parent is not None and not ba._is_container(root.parent):
        root = root.parent
    zmin = min((o.matrix_world @ Vector(c)).z for c in o.bound_box)
    if ba._role(root) in ("ceiling", "roof") or zmin > cut:
        o.hide_render = True

random.seed(3)
COLORS = {"wall": (0.15, 0.15, 0.18, 1), "floor": (0.85, 0.82, 0.75, 1), "door": (0.9, 0.2, 0.2, 1),
          "window": (0.2, 0.5, 1.0, 1), "trim": (0.6, 0.6, 0.6, 1), "ground": (0.4, 0.55, 0.35, 1)}
mats = {}


def mat(key, rgba):
    if key not in mats:
        m = bpy.data.materials.new(key)
        if m.node_tree is None:
            m.use_nodes = True
        bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
        bsdf.inputs[0].default_value = rgba
        mats[key] = m
    return mats[key]


for root in ba._unit_roots():
    r = ba._role(root)
    rgba = COLORS.get(r) or (random.uniform(.3, 1), random.uniform(.3, .9), random.uniform(.2, .6), 1)
    m = mat(r if r in COLORS else "f_" + root.name, rgba)
    for o in [root] + list(root.children_recursive):
        if o.type == "MESH":
            o.data.materials.clear()
            o.data.materials.append(m)

cam = bpy.data.objects.new("plan_cam", bpy.data.cameras.new("plan_cam"))
sc.collection.objects.link(cam)
cam.data.type = "ORTHO"
cam.data.ortho_scale = span
cam.location = (cx, cy, 30)
cam.rotation_euler = (0, 0, 0)
sc.camera = cam
sun = bpy.data.objects.new("plan_sun", bpy.data.lights.new("plan_sun", "SUN"))
sun.data.energy = 3.5
sun.rotation_euler = (0.3, 0.2, 0)
sc.collection.objects.link(sun)
sc.world = sc.world or bpy.data.worlds.new("plan_world")
sc.world.color = (0.8, 0.8, 0.8)
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = 12
sc.cycles.use_denoising = False
sc.render.use_compositing = False
sc.render.use_sequencer = False
sc.render.resolution_x = sc.render.resolution_y = 900
sc.render.filepath = out
bpy.ops.render.render(write_still=True)
print("saved", out)
