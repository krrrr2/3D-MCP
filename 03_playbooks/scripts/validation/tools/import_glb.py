"""GLB 를 빈 장면으로 가져와 .blend 로 저장 (Blender 기본 glTF 가져오기 = 사용자가 하는 그대로).

사용: python import_glb.py -- in.glb out.blend      (pip bpy 파이썬)  /  blender -b --python import_glb.py -- in.glb out.blend
"""
import sys

import bpy

glb, out = sys.argv[sys.argv.index("--") + 1:][:2]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
bpy.ops.wm.save_as_mainfile(filepath=out)
print("IMPORTED", len(bpy.data.objects), "objects")
