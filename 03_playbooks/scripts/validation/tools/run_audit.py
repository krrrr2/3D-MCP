""".blend 를 열어 building_audit 를 돌리고 JSON 저장 + 요약 출력.

사용: python run_audit.py -- scene.blend out.json
"""
import json
import os
import sys
import time

import bpy

blend, out = sys.argv[sys.argv.index("--") + 1:][:2]
bpy.ops.wm.open_mainfile(filepath=blend)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import building_audit as ba  # noqa: E402

t = time.time()
rep = ba.audit_building()
rep["summary"]["seconds"] = round(time.time() - t, 1)
with open(out, "w", encoding="utf-8") as f:
    json.dump(rep, f, ensure_ascii=False, indent=1)
for i in rep["issues"]:
    print(i["severity"], i["code"], i["object"], "|", i["detail"])
print(json.dumps(rep["summary"], ensure_ascii=False))
