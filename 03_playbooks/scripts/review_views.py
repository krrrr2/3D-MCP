"""
review_views.py - AI 비평(self-critique)용 다각도 검토 렌더를 한 번에 만든다.

뷰포트 스크린샷 한 장만으로는 떠 있는 물체, 관통, 배치 간격 문제를 놓치기 쉽다.
위(정사영) / 정면 / 측면 / 3/4 원근 4장을 렌더해서 AI 에게 함께 보여주면 배치·비율 오류를 훨씬 잘 잡는다.

사용
  paths = render_review_views("/tmp/review", engine="CYCLES", samples=16, res=768)
  -> ["/tmp/review/top.png", "/tmp/review/front.png", "/tmp/review/side.png", "/tmp/review/persp.png"]

- 원래 활성 카메라와 렌더 설정은 끝나면 복구한다.
- 검토용 카메라는 "_REVIEW_" 로 시작하는 이름으로 만들고 끝나면 삭제한다.
- engine: "CYCLES"(헤드리스 서버에서도 동작), "BLENDER_EEVEE"/"BLENDER_EEVEE_NEXT"(GPU 필요), "BLENDER_WORKBENCH"
"""

import math
import os

import bpy
from mathutils import Vector


def _scene_bounds(frame_ignore=("floor", "ground", "wall", "ceiling", "terrain")):
    """프레이밍 범위: 바닥·벽처럼 큰 구조물은 빼고 '내용물' 기준으로 잡는다 (없으면 전체)."""
    depsgraph = bpy.context.evaluated_depsgraph_get()
    meshes = [o for o in bpy.context.scene.objects
              if o.type == "MESH" and o.visible_get() and not o.name.startswith("_REVIEW_")]
    content = [o for o in meshes if not any(k in o.name.lower() for k in frame_ignore)]
    pts = []
    for o in (content or meshes):
        ev = o.evaluated_get(depsgraph)
        pts.extend(ev.matrix_world @ Vector(c) for c in ev.bound_box)
    if not pts:
        return Vector((-1, -1, 0)), Vector((1, 1, 1))
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return mn, mx


def _look_at(cam_obj, target):
    direction = Vector(target) - cam_obj.location
    cam_obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def _make_camera(name, ortho_scale=None, lens=35.0):
    data = bpy.data.cameras.new(name)
    if ortho_scale is not None:
        data.type = "ORTHO"
        data.ortho_scale = ortho_scale
    else:
        data.lens = lens
    data.clip_end = 1000.0
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def _random_color_material():
    """오브젝트마다 다른 색이 나오는 임시 재질 (Workbench 의 Random 색상과 같은 효과를 Cycles 에서)."""
    mat = bpy.data.materials.new("_REVIEW_random")
    if mat.node_tree is None:  # Blender 4.x. (5.0+ 는 기본으로 노드가 있고 use_nodes 는 폐기 예정)
        mat.use_nodes = True
    nt = mat.node_tree
    # 한국어 등 현지화 UI 에서는 노드 "이름"이 번역될 수 있으므로 타입으로 찾는다
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    info = nt.nodes.new("ShaderNodeObjectInfo")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    els = ramp.color_ramp.elements
    els[0].color = (0.85, 0.35, 0.30, 1.0)
    els[1].color = (0.30, 0.45, 0.85, 1.0)
    for pos, col in [(0.25, (0.90, 0.75, 0.30, 1.0)), (0.5, (0.35, 0.75, 0.40, 1.0)), (0.75, (0.70, 0.40, 0.80, 1.0))]:
        e = els.new(pos)
        e.color = col
    nt.links.new(info.outputs["Random"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.8
    return mat


def render_review_views(out_dir, engine="CYCLES", samples=16, res=768, margin=1.3, neutral_world=True,
                        color_mode="random", frame_ignore=("floor", "ground", "wall", "ceiling", "terrain")):
    """다각도 검토 렌더.

    engine: 헤드리스/GPU 없는 서버는 "CYCLES". Blender GUI(blender-mcp)에서는 "BLENDER_WORKBENCH" 가 가장 빠르다.
    neutral_world: 검토하는 동안만 밝은 회색 월드로 바꿔 형태가 잘 보이게 한다(끝나면 원래 월드로 복구).
    color_mode: "random" = 오브젝트마다 다른 색(배치·겹침 확인용), "materials" = 실제 재질 그대로.
    """
    scene = bpy.context.scene
    os.makedirs(out_dir, exist_ok=True)
    mn, mx = _scene_bounds(frame_ignore)
    center = (mn + mx) / 2
    size = mx - mn
    span = max(size.x, size.y, size.z, 0.5) * margin
    dist = span * 2.5

    # 설정 백업
    prev = {
        "camera": scene.camera,
        "engine": scene.render.engine,
        "rx": scene.render.resolution_x,
        "ry": scene.render.resolution_y,
        "pct": scene.render.resolution_percentage,
        "path": scene.render.filepath,
    }
    prev_samples = scene.cycles.samples if hasattr(scene, "cycles") else None
    prev_device = scene.cycles.device if hasattr(scene, "cycles") else None
    shading = scene.display.shading
    prev_shading = (shading.light, shading.color_type, shading.show_cavity, shading.show_object_outline)
    view_layer = bpy.context.view_layer
    prev_override = view_layer.material_override

    views = {
        "top": (Vector((center.x, center.y, mx.z + dist)), max(size.x, size.y) * margin),
        "front": (Vector((center.x, mn.y - dist, center.z)), max(size.x, size.z) * margin),
        "side": (Vector((mx.x + dist, center.y, center.z)), max(size.y, size.z) * margin),
        "persp": (Vector((center.x + span * 1.2, center.y - span * 1.6, center.z + span * 0.9)), None),
    }
    cams, paths = [], []
    prev_world, temp_world = scene.world, None
    if neutral_world:
        temp_world = bpy.data.worlds.new("_REVIEW_world")
        if temp_world.node_tree is None:  # Blender 4.x
            temp_world.use_nodes = True
        bg = next(n for n in temp_world.node_tree.nodes if n.type == "BACKGROUND")
        bg.inputs["Color"].default_value = (0.7, 0.7, 0.7, 1.0)
        bg.inputs["Strength"].default_value = 1.0
        scene.world = temp_world
    temp_light = None
    if not any(o.type == "LIGHT" for o in scene.objects):
        # 조명이 없는 장면도 형태가 보이도록 임시 태양광 추가 (끝나면 삭제)
        ldata = bpy.data.lights.new("_REVIEW_sun", "SUN")
        ldata.energy = 1.5
        temp_light = bpy.data.objects.new("_REVIEW_sun", ldata)
        temp_light.rotation_euler = (math.radians(50), 0.0, math.radians(30))
        scene.collection.objects.link(temp_light)
    temp_mat = None
    try:
        scene.render.engine = engine
        if engine == "CYCLES":
            scene.cycles.samples = samples
            scene.cycles.device = "CPU"
        if engine == "BLENDER_WORKBENCH":
            shading.light = "STUDIO"
            shading.color_type = "RANDOM" if color_mode == "random" else "MATERIAL"
            shading.show_cavity = True
            shading.show_object_outline = True
        elif color_mode == "random":
            temp_mat = _random_color_material()
            view_layer.material_override = temp_mat
        scene.render.resolution_x = res
        scene.render.resolution_y = res
        scene.render.resolution_percentage = 100
        for name, (loc, ortho) in views.items():
            cam = _make_camera("_REVIEW_" + name, ortho_scale=max(ortho, 0.5) if ortho else None)
            cam.location = loc
            if name == "top":
                cam.rotation_euler = (0.0, 0.0, 0.0)  # -Z 를 내려다봄, 화면 위쪽 = +Y
            else:
                _look_at(cam, center)
            cams.append(cam)
            scene.camera = cam
            path = os.path.join(out_dir, f"{name}.png")
            scene.render.filepath = path
            bpy.ops.render.render(write_still=True)
            paths.append(path)
    finally:
        scene.camera = prev["camera"]
        scene.render.engine = prev["engine"]
        scene.render.resolution_x = prev["rx"]
        scene.render.resolution_y = prev["ry"]
        scene.render.resolution_percentage = prev["pct"]
        scene.render.filepath = prev["path"]
        if prev_samples is not None:
            scene.cycles.samples = prev_samples
            scene.cycles.device = prev_device
        shading.light, shading.color_type, shading.show_cavity, shading.show_object_outline = prev_shading
        view_layer.material_override = prev_override
        if temp_mat is not None:
            bpy.data.materials.remove(temp_mat)
        for cam in cams:
            data = cam.data
            bpy.data.objects.remove(cam, do_unlink=True)
            bpy.data.cameras.remove(data)
        if temp_light is not None:
            ldata = temp_light.data
            bpy.data.objects.remove(temp_light, do_unlink=True)
            bpy.data.lights.remove(ldata)
        if temp_world is not None:
            scene.world = prev_world
            bpy.data.worlds.remove(temp_world)
    return paths
