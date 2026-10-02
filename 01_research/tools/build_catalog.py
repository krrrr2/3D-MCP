"""
01_research/raw/*.json (원본 조사 데이터)에서 사람이 읽는 정리본을 결정적으로 생성한다.

생성물
  01_research/sources_catalog.md   주제별 출처 목록 (신뢰도 경고 표시 포함)
  01_research/verification_log.md  교차검증 결과 (확인/부분/반박/미확인, 항목 점검, 누락 지적)

원본(raw)은 절대 수정하지 않는다. 다시 만들려면:
  python3 01_research/tools/build_catalog.py
"""

import glob
import json
import os
import re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "raw")

TOPIC_TITLES = {
    "01_ai-models": "AI 모델 비교 (GPT-6 Astra / Claude / Gemini ...)",
    "02_blender-mcp": "Blender MCP 생태계",
    "03_dcc-cad-mcp": "기타 DCC·CAD·텍스처 앱 MCP",
    "04_engine-mcp": "게임 엔진·실시간 3D MCP",
    "05_ai-3d-generation": "AI 3D 생성 (Text/Image-to-3D)",
    "06_texturing-materials": "AI 텍스처링·PBR 재질",
    "07_aaa-rendering-lighting": "AAA 라이팅·렌더·아트디렉션",
    "08_modeling-objects": "오브젝트·가구·조형 모델링",
    "09_scene-layout": "배치·레이아웃",
    "10_agent-workflow": "에이전트 워크플로·프롬프팅",
    "11_case-studies": "사례 연구",
    "12_assets-pipeline-licensing": "에셋·파이프라인·라이선스",
    "13_research-papers": "학술 연구",
    "G1_dimensions": "[보완] 실측 치수 표준",
    "G2_korean_resources": "[보완] 한국어 자료",
    "G3_videos_cases": "[보완] 영상·소셜 사례",
    "G4_licensing_pricing": "[보완] 가격·라이선스·법규",
    "G5_aaa_practice": "[보완] AAA 실무·공식 변경사항",
    "G6_benchmarks_models": "[보완] 벤치마크·모델 비교",
    "G7_computer_use": "[보완] 컴퓨터 유즈 vs MCP vs 스크립트",
    "G8_blender_lab_mcp": "[보완] 공식 Blender Lab MCP 소스 정독·실제 구동",
    "G9_human_character": "[보완] 인체·캐릭터 조형 도구",
    "G10_organic_nature": "[보완] 유기물·자연·조형물 도구",
    "G11_architecture": "[보완] 건물·건축·평면·도시 배치 도구",
    "G12_tool_safety": "[보완] 3D 도구 보안(악성 애드온·.blend·MCP·모델 파일)",
    "G13_placement_libraries": "[보완] 조형·배치 라이브러리 재확인(BlenderProc 등)",
}

VERDICT_KO = {"confirmed": "✅ 확인", "partially": "🟡 부분", "refuted": "❌ 반박", "unverifiable": "❔ 미확인"}


def cell(s, limit=None):
    s = "" if s is None else str(s)
    s = s.replace("\r", " ").replace("\n", " ").replace("|", "\\|").strip()
    if limit and len(s) > limit:
        s = s[: limit - 1] + "…"
    return s


def link(url):
    url = (url or "").strip()
    return f"<{url}>" if url else ""


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def topics():
    keys = set()
    for p in glob.glob(os.path.join(RAW, "*.json")):
        keys.add(os.path.basename(p).split(".")[0])
    return sorted(keys, key=lambda k: (k.startswith("G"), int(re.match(r"G?(\d+)", k).group(1)), k))


def research_file(key):
    for kind in ("research", "gap"):
        p = os.path.join(RAW, f"{key}.{kind}.json")
        if os.path.exists(p):
            return p
    return None


def build_sources():
    out = ["# 출처 카탈로그 (자동 생성)", "",
           "> `01_research/raw/` 원본 조사 데이터에서 `tools/build_catalog.py` 로 생성한 파일입니다. 직접 수정하지 마세요.",
           "> ⚠ 표시는 교차검증 에이전트가 신뢰도 문제(SEO성 AI 생성 글, 1차 출처와 모순 등)를 지적한 출처입니다.", ""]
    all_urls = set()
    toc, body = [], []
    for key in topics():
        rp = research_file(key)
        if not rp:
            continue
        r = load(rp)
        vp = os.path.join(RAW, f"{key}.verify.json")
        unreliable = {}
        if os.path.exists(vp):
            v = load(vp)
            for u in v.get("unreliable_sources", []):
                unreliable[u["url"].strip()] = u.get("reason", "")
        title = TOPIC_TITLES.get(key, key)
        anchor = key.lower()
        toc.append(f"- [{title}](#{anchor}) — 출처 {len(r.get('sources', []))}개")
        body += [f'<a id="{anchor}"></a>', f"## {title}", "", f"주제 원문: {cell(r.get('topic'))}", "",
                 "| # | 제목 | 유형 | 날짜 | 왜 유용한가 | URL |", "|---|---|---|---|---|---|"]
        for i, s in enumerate(r.get("sources", []), 1):
            url = s.get("url", "").strip()
            all_urls.add(url)
            warn = " ⚠" if url in unreliable else ""
            body.append(f"| {i} | {cell(s.get('title'), 90)}{warn} | {cell(s.get('source_type'), 30)} | "
                        f"{cell(s.get('date'), 20)} | {cell(s.get('why_useful'), 140)} | {link(url)} |")
        if unreliable:
            body += ["", "**⚠ 신뢰도 경고가 붙은 출처**", ""]
            for u, reason in unreliable.items():
                body.append(f"- {link(u)} — {cell(reason, 300)}")
        body.append("")
        for it in r.get("items", []):
            all_urls.update(x.strip() for x in it.get("urls", []))
        for c in r.get("case_studies", []) + r.get("measurements", []):
            all_urls.update(x.strip() for x in c.get("urls", []))
    out += ["## 목차", ""] + toc + ["", f"항목·사례에 인용된 URL까지 합친 고유 URL 수: **{len(all_urls)}개**", ""] + body
    return "\n".join(out) + "\n"


def build_verification():
    out = ["# 교차검증 로그 (자동 생성)", "",
           "> 조사 에이전트와 **독립된** 검증 에이전트가 핵심 주장을 1차 출처로 다시 확인한 결과입니다.",
           "> 가이드 문서는 이 결과를 우선합니다: ❌ 반박된 내용은 정정값을 쓰고, ❔ 미확인 내용은 '미확인'으로 표시합니다.",
           "> `tools/build_catalog.py` 로 생성. 직접 수정하지 마세요.", "",
           "## 요약", "", "| 주제 | ✅ 확인 | 🟡 부분 | ❌ 반박 | ❔ 미확인 | 항목 문제 | 신뢰도 경고 출처 | 누락 지적 |",
           "|---|---|---|---|---|---|---|---|"]
    body = []
    for key in topics():
        vp = os.path.join(RAW, f"{key}.verify.json")
        if not os.path.exists(vp):
            continue
        v = load(vp)
        verdicts = v.get("verdicts") or v.get("checks") or []
        cnt = Counter(d.get("verdict") for d in verdicts)
        item_issues = [c for c in v.get("item_checks", []) if c.get("status") != "ok"]
        title = TOPIC_TITLES.get(key, key)
        out.append(f"| {title} | {cnt['confirmed']} | {cnt['partially']} | {cnt['refuted']} | {cnt['unverifiable']} | "
                   f"{len(item_issues)} | {len(v.get('unreliable_sources', []))} | {len(v.get('missed_items', []))} |")
        body += [f"## {title}", "", "### 주장별 판정", "", "| 판정 | 주장 | 정정·메모 | 근거 |", "|---|---|---|---|"]
        order = {"refuted": 0, "partially": 1, "unverifiable": 2, "confirmed": 3}
        for d in sorted(verdicts, key=lambda d: order.get(d.get("verdict"), 9)):
            note = d.get("correction") or d.get("note") or ""
            ev = " ".join(link(u) for u in (d.get("evidence_urls") or [])[:3])
            body.append(f"| {VERDICT_KO.get(d.get('verdict'), d.get('verdict'))} | {cell(d.get('claim'), 220)} | "
                        f"{cell(note, 320)} | {ev} |")
        if item_issues:
            body += ["", "### 항목 점검에서 문제가 발견된 것", ""]
            for c in item_issues:
                body.append(f"- **{cell(c.get('name'), 80)}** ({c.get('status')}): {cell(c.get('detail'), 400)}")
        if v.get("missed_items"):
            body += ["", "### 검증자가 지적한 누락 항목", ""]
            for m in v["missed_items"]:
                body.append(f"- **{cell(m.get('name'), 100)}** — {cell(m.get('why_important'), 300)} {link(m.get('url'))}")
        if v.get("notes"):
            body += ["", "### 메모", ""] + [f"- {cell(n, 400)}" for n in v["notes"]]
        body.append("")
    return "\n".join(out + [""] + body) + "\n"


def main():
    with open(os.path.join(ROOT, "sources_catalog.md"), "w", encoding="utf-8") as f:
        f.write(build_sources())
    with open(os.path.join(ROOT, "verification_log.md"), "w", encoding="utf-8") as f:
        f.write(build_verification())
    print("written: sources_catalog.md, verification_log.md")


if __name__ == "__main__":
    main()
