"""공식 blender-mcp 서버(stdio)에 붙어 plan(JSON: [[label, tool, args], ...])의 도구를 차례로 부르고 결과를 저장한다.
args 안의 문자열은 환경변수를 펼친다(예: ${SCRATCH}/scene.blend).
사용: BLMCP_BIN=<venv>/bin/blender-mcp BLENDER_PATH=<fakeblender.sh> python client_call.py plan.json out.json"""
import asyncio
import base64
import json
import os
import sys
import time

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def expand(x):
    if isinstance(x, str):
        return os.path.expandvars(x)
    if isinstance(x, dict):
        return {k: expand(v) for k, v in x.items()}
    return x


async def main(plan_path, out_path):
    with open(plan_path) as f:
        plan = json.load(f)
    res = []
    params = StdioServerParameters(command=os.environ.get("BLMCP_BIN", "blender-mcp"), env=dict(os.environ))
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            for label, tool, args in plan:
                t0 = time.time()
                try:
                    cr = await s.call_tool(tool, expand(args))
                    items = []
                    for c in cr.content:
                        if c.type == "text":
                            items.append({"text": c.text})
                        elif c.type == "image":
                            p = os.path.join(os.path.dirname(os.path.abspath(out_path)), f"img_{label}.png")
                            with open(p, "wb") as f:
                                f.write(base64.b64decode(c.data))
                            items.append({"image": p, "mime": c.mimeType})
                        else:
                            items.append({"other": c.type})
                    row = {"label": label, "tool": tool, "isError": cr.isError, "sec": round(time.time() - t0, 2),
                           "content": items, "structured": cr.structuredContent}
                except Exception as e:  # 연결 끊김 등
                    row = {"label": label, "tool": tool, "exception": repr(e), "sec": round(time.time() - t0, 2)}
                res.append(row)
                txt = json.dumps(row.get("structured") or row.get("content") or row.get("exception"), ensure_ascii=False, default=str)
                print(f"[{label}] {tool} isError={row.get('isError')} {row['sec']}s :: {txt[:400]}", flush=True)
    with open(out_path, "w") as f:
        json.dump(res, f, indent=1, ensure_ascii=False, default=str)

asyncio.run(main(sys.argv[1], sys.argv[2]))
