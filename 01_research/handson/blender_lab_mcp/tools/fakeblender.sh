#!/bin/sh
# BLENDER_PATH 로 지정한다. BPY_PYTHON = bpy 가 설치된 파이썬 경로
exec "$BPY_PYTHON" "$(dirname "$0")/fake_blender.py" "$@"
