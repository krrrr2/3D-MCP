"""
문서 품질 자동 점검 (결정적 검사).

1) 외부 URL 추적성: 정리 문서(02_guides, 03_playbooks, 04_case_studies 등)에 쓰인 모든 http(s) URL이
   01_research/raw/*.json 원자료에 실제로 존재하는지 확인한다. (AI가 URL을 지어내는 것을 막기 위함)
2) 내부 링크: 저장소 안 상대 링크가 실제 파일을 가리키는지 확인한다.

사용: python3 01_research/tools/check_docs.py        (문제가 있으면 종료 코드 1)
"""

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = os.path.join(ROOT, "01_research", "raw")
SKIP = {os.path.join(ROOT, "01_research", "sources_catalog.md"), os.path.join(ROOT, "01_research", "verification_log.md")}

# 원자료에 없어도 되는 URL (도구 설치·문서 안내용으로 이 저장소가 직접 확인한 것)
ALLOW_PREFIXES = (
    "https://code.claude.com/docs/en/claude-code-on-the-web",
)

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
ANGLE = re.compile(r"<(https?://[^>\s]+)>")
BARE = re.compile(r"(?<![(<\"'])\bhttps?://[^\s)>\]\"'`|]+")


def norm(u):
    u = u.strip().rstrip(".,;:")
    u = u.split("#")[0]
    return u.rstrip("/")


def raw_corpus():
    text = []
    for p in glob.glob(os.path.join(RAW, "*.json")):
        with open(p, encoding="utf-8") as f:
            text.append(f.read())
    blob = "\n".join(text).replace("\\/", "/")
    urls = {norm(m) for m in re.findall(r"https?://[^\s\"'<>\\)\]]+", blob)}
    return blob, urls


def md_files():
    files = []
    for p in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True):
        if "/01_research/raw/" in p or p in SKIP or "/.git/" in p:
            continue
        files.append(p)
    return sorted(files)


def in_code_block_ranges(text):
    ranges, pos = [], 0
    for m in re.finditer(r"```.*?```", text, flags=re.S):
        ranges.append((m.start(), m.end()))
    return ranges


def main():
    blob, raw_urls = raw_corpus()
    problems = 0
    for p in md_files():
        rel = os.path.relpath(p, ROOT)
        with open(p, encoding="utf-8") as f:
            text = f.read()
        code = in_code_block_ranges(text)
        in_code = lambda i: any(a <= i < b for a, b in code)
        found = []
        for rx in (MD_LINK, ANGLE, BARE):
            for m in rx.finditer(text):
                if not in_code(m.start()):
                    found.append(m.group(1) if rx is not BARE else m.group(0))
        bad_ext, bad_int = set(), set()
        for u in found:
            if u.startswith(("http://", "https://")):
                n = norm(u)
                if n.startswith(ALLOW_PREFIXES):
                    continue
                if n not in raw_urls and n not in blob:
                    bad_ext.add(u)
            elif u.startswith(("mailto:", "#")):
                continue
            else:
                target = os.path.normpath(os.path.join(os.path.dirname(p), u.split("#")[0]))
                if u.split("#")[0] and not os.path.exists(target):
                    bad_int.add(u)
        if bad_ext or bad_int:
            print(f"\n## {rel}")
            for u in sorted(bad_ext):
                print(f"  [원자료에 없는 URL] {u}")
            for u in sorted(bad_int):
                print(f"  [깨진 내부 링크] {u}")
            problems += len(bad_ext) + len(bad_int)
    print(f"\n검사한 문서 {len(md_files())}개, 문제 {problems}건")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
