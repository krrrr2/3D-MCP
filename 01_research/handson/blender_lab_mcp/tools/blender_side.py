"""pip bpy(5.1 이상) 안에서 공식 애드온의 백그라운드 서버를 `blender --background --online-mode FILE --command blender_mcp` 와 같은 경로로 띄운다.
(pip bpy 에는 blender 실행 파일이 없어서 확장 설치 대신 애드온 폴더를 sys.path 에 넣고 register() 한다)

사용: BLMCP_ADDON_DIR=<공식 저장소>/addon  python blender_side.py [scene.blend] [--port 9876] [--offline]
  --offline : 온라인 접근을 켜지 않고 실행 → 애드온이 시작을 거부하는지 확인
"""
import os
import sys

import bpy

sys.path.insert(0, os.environ["BLMCP_ADDON_DIR"])
args = sys.argv[1:]
port = "9876"
if "--port" in args:
    i = args.index("--port")
    port = args[i + 1]
    del args[i:i + 2]
offline = "--offline" in args
args = [a for a in args if a != "--offline"]
if args:
    bpy.ops.wm.open_mainfile(filepath=args[0])
if not offline:
    bpy.context.preferences.system.use_online_access = True   # = blender --online-mode
import blender_mcp_addon as A  # noqa: E402

A.register()
print("online", bpy.app.online_access, "file", bpy.data.filepath, flush=True)
sys.exit(A._cli_execute_handler(["--port", port]))
