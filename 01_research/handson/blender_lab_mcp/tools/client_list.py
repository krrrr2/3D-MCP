"""공식 blender-mcp 서버를 stdio 로 띄워 initialize·tools/list·prompts/list·resources/list 결과를 JSON 으로 저장한다.
사용: BLMCP_BIN=<venv>/bin/blender-mcp python client_list.py out.json   (mcp SDK 가 설치된 파이썬으로 실행)"""
import asyncio
import json
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main(out_path):
    params = StdioServerParameters(command=os.environ.get("BLMCP_BIN", "blender-mcp"), env=dict(os.environ))
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            init = await s.initialize()
            out = {"server": init.serverInfo.model_dump(), "protocol": init.protocolVersion,
                   "instructions": init.instructions, "capabilities": init.capabilities.model_dump(exclude_none=True)}
            tools = (await s.list_tools()).tools
            out["tools"] = [t.model_dump(exclude_none=True) for t in tools]
            out["prompts"] = [p.model_dump(exclude_none=True) for p in (await s.list_prompts()).prompts]
            out["resources"] = [x.model_dump(exclude_none=True) for x in (await s.list_resources()).resources]
            with open(out_path, "w") as f:
                json.dump(out, f, indent=1, ensure_ascii=False, default=str)
            print(init.serverInfo, init.protocolVersion, len(tools), "tools")
            for t in tools:
                a = t.annotations
                print(f"{t.name:50s} readOnly={getattr(a, 'readOnlyHint', None)} destructive={getattr(a, 'destructiveHint', None)}"
                      f" | params={list((t.inputSchema or {}).get('properties', {}).keys())}")

asyncio.run(main(sys.argv[1]))
