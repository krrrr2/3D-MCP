"""BLENDER_PATH 흉내: `blender --background FILE --python-expr CODE` 형식만 지원한다.
공식 서버의 *_for_cli 도구는 이 형식으로 Blender 를 부르므로, blender 실행 파일이 없는 pip bpy 환경에서 이것으로 대신한다.
fakeblender.sh 가 이 파일을 bpy 가 설치된 파이썬으로 실행한다."""
import sys

import bpy

a = sys.argv[1:]
assert a[0] == "--background" and a[2] == "--python-expr", a
bpy.ops.wm.open_mainfile(filepath=a[1])
exec(compile(a[3], "<python-expr>", "exec"), {"__name__": "__main__"})
